<#
.SYNOPSIS
  qa-process 저장소를 로컬 Git 저장소로 초기화하고 GitHub 원격 저장소에 연결한다.

.DESCRIPTION
  CLAUDE.md 14절(Git 사용 원칙) / 18절(User Approval 원칙)에 따라 이 스크립트는
  commit 과 push 를 각각 사용자 확인 없이 수행하지 않는다. 각 단계마다 변경 내용을
  보여주고 명시적으로 'y' 를 입력해야 진행한다.

  수행 순서
    1. git 사용자 정보(user.name / user.email) 확인
    2. git init (없을 때만) 및 기본 브랜치 master 설정 - CI(.github/workflows/ci.yml)가
       master push 를 트리거로 쓰기 때문에 master 로 맞춘다
    3. 민감정보 파일(.env, 서비스 계정 키)이 추적 대상에 포함되지 않았는지 검사
    4. 사용자 확인 후 최초 commit
    5. 원격 저장소 연결 및 사용자 확인 후 push

.PARAMETER RemoteUrl
  연결할 GitHub 원격 저장소 주소. 예: https://github.com/<계정>/qa-process.git
  생략하면 원격 연결과 push 는 건너뛴다.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\setup\3-setup-git.ps1
  powershell -ExecutionPolicy Bypass -File scripts\setup\3-setup-git.ps1 -RemoteUrl https://github.com/myid/qa-process.git
#>

param(
  [string]$RemoteUrl = ""
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

function Write-Step([string]$Message) {
  Write-Host ""
  Write-Host "=== $Message ===" -ForegroundColor Cyan
}

function Write-Ok([string]$Message) {
  Write-Host "  [OK] $Message" -ForegroundColor Green
}

function Write-Warn2([string]$Message) {
  Write-Host "  [!] $Message" -ForegroundColor Yellow
}

function Confirm-Action([string]$Question) {
  Write-Host ""
  $answer = Read-Host "$Question (y/N)"
  return ($answer -eq "y" -or $answer -eq "Y")
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "Git 이 설치되어 있지 않습니다. 먼저 1-setup-env.ps1 을 실행하세요."
}

Set-Location $RepoRoot
Write-Host "저장소 경로: $RepoRoot"

# ---------------------------------------------------------------------------
# 1. Git 사용자 정보
# ---------------------------------------------------------------------------
Write-Step "1/5 Git 사용자 정보 확인"

$userName = (& git config --global user.name) 2>$null
$userEmail = (& git config --global user.email) 2>$null

if ([string]::IsNullOrWhiteSpace($userName) -or [string]::IsNullOrWhiteSpace($userEmail)) {
  Write-Warn2 "git 전역 사용자 정보가 설정되어 있지 않습니다. 아래 명령을 먼저 실행하세요."
  Write-Host '    git config --global user.name "이름"'
  Write-Host '    git config --global user.email "you@example.com"'
  exit 1
}
Write-Ok "user.name = $userName / user.email = $userEmail"

# ---------------------------------------------------------------------------
# 2. git init
# ---------------------------------------------------------------------------
Write-Step "2/5 로컬 저장소 초기화"

if (Test-Path (Join-Path $RepoRoot ".git")) {
  Write-Ok ".git 이 이미 존재합니다 (초기화 건너뜀)"
} else {
  & git init | Out-Null
  Write-Ok "git init 완료"
}

$currentBranch = (& git symbolic-ref --short HEAD) 2>$null
if ([string]::IsNullOrWhiteSpace($currentBranch)) { $currentBranch = "" }

if ($currentBranch -ne "master") {
  # 아직 커밋이 없으면 HEAD 만 옮기고, 커밋이 있으면 브랜치명을 변경한다.
  $hasCommit = $false
  & git rev-parse --verify HEAD *> $null
  if ($LASTEXITCODE -eq 0) { $hasCommit = $true }

  if ($hasCommit) {
    & git branch -M master
  } else {
    & git symbolic-ref HEAD refs/heads/master
  }
  Write-Ok "기본 브랜치를 master 로 설정 (CI 트리거 브랜치와 일치)"
} else {
  Write-Ok "현재 브랜치: master"
}

# ---------------------------------------------------------------------------
# 3. 민감정보 검사
# ---------------------------------------------------------------------------
Write-Step "3/5 민감정보 포함 여부 검사 (CLAUDE.md 17절)"

& git add -A

$staged = @(& git diff --cached --name-only | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
$secretPatterns = @('(^|/)\.env$', '(^|/)\.env\.local$', 'service-account.*\.json$', '.*-credentials\.json$', '(^|/)credentials\.json$')
$violations = @()

foreach ($file in $staged) {
  foreach ($pattern in $secretPatterns) {
    if ($file -match $pattern) {
      $violations += $file
      break
    }
  }
}

if ($violations.Count -gt 0) {
  Write-Host ""
  Write-Host "민감정보 파일이 커밋 대상에 포함되어 있습니다. 중단합니다." -ForegroundColor Red
  $violations | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  Write-Host ".gitignore 를 확인한 뒤 'git reset' 으로 스테이징을 해제하고 다시 실행하세요." -ForegroundColor Red
  exit 1
}
Write-Ok "민감정보 파일 없음 (스테이징 파일 $($staged.Count)개)"

# ---------------------------------------------------------------------------
# 4. 최초 commit (사용자 승인 필요)
# ---------------------------------------------------------------------------
Write-Step "4/5 Commit (사용자 승인 필요)"

& git rev-parse --verify HEAD *> $null
$alreadyCommitted = ($LASTEXITCODE -eq 0)

if ($staged.Count -eq 0) {
  Write-Ok "커밋할 변경 사항이 없습니다."
} else {
  Write-Host ""
  Write-Host "커밋 대상 파일 (상위 30개):" -ForegroundColor DarkGray
  $staged | Select-Object -First 30 | ForEach-Object { Write-Host "  $_" }
  if ($staged.Count -gt 30) { Write-Host "  ... 외 $($staged.Count - 30)개" }

  if ($alreadyCommitted) {
    $commitMessage = "chore: Windows 로컬 실행 환경 설정 반영"
  } else {
    $commitMessage = "chore: QA 자동화 프로세스 저장소 초기 커밋"
  }

  Write-Host ""
  Write-Host "예정 Commit Message: $commitMessage" -ForegroundColor Yellow

  if (Confirm-Action "위 내용으로 commit 하시겠습니까?") {
    & git commit -m $commitMessage | Out-Null
    Write-Ok "commit 완료"
  } else {
    & git reset | Out-Null
    Write-Warn2 "commit 을 취소했습니다 (스테이징도 해제). 원격 연결 단계로 넘어갑니다."
  }
}

# ---------------------------------------------------------------------------
# 5. 원격 저장소 연결 및 push (사용자 승인 필요)
# ---------------------------------------------------------------------------
Write-Step "5/5 원격 저장소 연결 / Push (사용자 승인 필요)"

if ([string]::IsNullOrWhiteSpace($RemoteUrl)) {
  $existingRemote = (& git remote get-url origin) 2>$null
  if (-not [string]::IsNullOrWhiteSpace($existingRemote)) {
    Write-Ok "이미 연결된 origin: $existingRemote"
    $RemoteUrl = $existingRemote
  } else {
    Write-Warn2 "RemoteUrl 이 지정되지 않아 원격 연결을 건너뜁니다."
    Write-Host ""
    Write-Host "나중에 연결하려면 GitHub 에서 빈 저장소를 만든 뒤 아래를 실행하세요."
    Write-Host "  git remote add origin https://github.com/<계정>/qa-process.git"
    Write-Host "  git push -u origin master"
    exit 0
  }
} else {
  $existingRemote = (& git remote get-url origin) 2>$null
  if ([string]::IsNullOrWhiteSpace($existingRemote)) {
    & git remote add origin $RemoteUrl
    Write-Ok "origin 연결: $RemoteUrl"
  } elseif ($existingRemote -ne $RemoteUrl) {
    & git remote set-url origin $RemoteUrl
    Write-Ok "origin 변경: $existingRemote -> $RemoteUrl"
  } else {
    Write-Ok "origin 이미 연결됨: $RemoteUrl"
  }
}

& git rev-parse --verify HEAD *> $null
if ($LASTEXITCODE -ne 0) {
  Write-Warn2 "커밋이 없어 push 를 건너뜁니다."
  exit 0
}

Write-Host ""
Write-Host "push 대상: origin/master ($RemoteUrl)" -ForegroundColor Yellow
if (Confirm-Action "지금 push 하시겠습니까?") {
  & git push -u origin master
  Write-Ok "push 완료"
  Write-Host ""
  Write-Host "push 직후 GitHub Actions(QA Automation CI)가 자동 실행됩니다."
  Write-Host "실행 전에 GitHub 저장소 Settings > Secrets and variables > Actions 에서"
  Write-Host "ACTEST1_PASSWORD / ACTEST2_PASSWORD / ACTEST3_PASSWORD (필요 시 SLACK_WEBHOOK_URL)"
  Write-Host "를 먼저 등록해야 테스트가 정상 통과합니다."
} else {
  Write-Warn2 "push 를 취소했습니다. 준비되면 'git push -u origin master' 로 직접 실행하세요."
}
