<#
.SYNOPSIS
  qa-process 저장소를 Windows 로컬 환경에서 실행 가능한 상태로 준비한다.

.DESCRIPTION
  다음 작업을 순서대로 수행한다(이미 되어 있으면 건너뛴다 - 반복 실행해도 안전).
    1. 필수 도구(Python / Git / Node.js / Chrome) 설치 여부 확인
    2. 저장소 루트에 가상환경(.venv) 생성
    3. automation / scripts 의존성 설치
    4. .env.example 을 .env 로 복사 (값은 사용자가 직접 채움)
    5. 실행에 필요한 디렉터리(shrimp_data 등) 생성

  이 스크립트는 Git commit/push 를 수행하지 않는다(CLAUDE.md 14절, 18절).
  Git 연결은 3-setup-git.ps1 에서 별도로 진행한다.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\setup\1-setup-env.ps1
#>

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$VenvDir = Join-Path $RepoRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

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

function Test-Command([string]$Name) {
  return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

Write-Host "저장소 경로: $RepoRoot"

# ---------------------------------------------------------------------------
# 1. 필수 도구 확인
# ---------------------------------------------------------------------------
Write-Step "1/5 필수 도구 확인"

$missing = @()

if (Test-Command "python") {
  $pyVersion = (& python --version 2>&1) -join " "
  Write-Ok "Python: $pyVersion"
} else {
  $missing += "Python 3.9 이상 (https://www.python.org/downloads/windows/ - 설치 시 'Add python.exe to PATH' 체크)"
}

if (Test-Command "git") {
  $gitVersion = (& git --version 2>&1) -join " "
  Write-Ok "Git: $gitVersion"
} else {
  $missing += "Git for Windows (https://git-scm.com/download/win)"
}

if (Test-Command "node") {
  $nodeVersion = (& node --version 2>&1) -join " "
  Write-Ok "Node.js: $nodeVersion"
} else {
  $missing += "Node.js LTS (https://nodejs.org/ - Playwright MCP / shrimp-task-manager MCP 실행에 필요)"
}

$chromePaths = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromePaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if ($chrome) {
  Write-Ok "Chrome: $chrome"
} else {
  $missing += "Google Chrome (Selenium 테스트 실행 브라우저)"
}

if ($missing.Count -gt 0) {
  Write-Host ""
  Write-Host "다음 항목을 먼저 설치한 뒤 이 스크립트를 다시 실행하세요." -ForegroundColor Red
  $missing | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
  exit 1
}

# ChromeDriver 는 Selenium 4.20+ 의 Selenium Manager 가 자동으로 내려받으므로 별도 설치하지 않는다.

# ---------------------------------------------------------------------------
# 2. 가상환경 생성
# ---------------------------------------------------------------------------
Write-Step "2/5 Python 가상환경(.venv) 준비"

if (Test-Path $VenvPython) {
  Write-Ok ".venv 가 이미 존재합니다 (재생성하지 않음)"
} else {
  & python -m venv $VenvDir
  if (-not (Test-Path $VenvPython)) {
    throw ".venv 생성에 실패했습니다: $VenvDir"
  }
  Write-Ok ".venv 생성 완료"
}

& $VenvPython -m pip install --upgrade pip --quiet
Write-Ok "pip 최신화 완료"

# ---------------------------------------------------------------------------
# 3. 의존성 설치
# ---------------------------------------------------------------------------
Write-Step "3/5 의존성 설치"

$requirementFiles = @(
  (Join-Path $RepoRoot "automation\requirements.txt"),
  (Join-Path $RepoRoot "scripts\sheets_sync\requirements.txt")
)

foreach ($req in $requirementFiles) {
  if (Test-Path $req) {
    Write-Host "  설치 중: $req"
    & $VenvPython -m pip install -r $req --quiet
    Write-Ok (Split-Path $req -Leaf)
  } else {
    Write-Warn2 "파일이 없어 건너뜀: $req"
  }
}

# ---------------------------------------------------------------------------
# 4. .env 파일 준비
# ---------------------------------------------------------------------------
Write-Step "4/5 .env 파일 준비"

$envPairs = @(
  @{ Example = (Join-Path $RepoRoot ".env.example");            Target = (Join-Path $RepoRoot ".env") },
  @{ Example = (Join-Path $RepoRoot "automation\.env.example"); Target = (Join-Path $RepoRoot "automation\.env") }
)

foreach ($pair in $envPairs) {
  if (-not (Test-Path $pair.Example)) {
    Write-Warn2 "템플릿 없음: $($pair.Example)"
    continue
  }
  if (Test-Path $pair.Target) {
    Write-Ok "이미 존재하여 유지: $($pair.Target)"
  } else {
    Copy-Item $pair.Example $pair.Target
    Write-Ok "생성됨(값은 직접 채워야 함): $($pair.Target)"
  }
}

# ---------------------------------------------------------------------------
# 5. 런타임 디렉터리 생성
# ---------------------------------------------------------------------------
Write-Step "5/5 런타임 디렉터리 확인"

$runtimeDirs = @(
  (Join-Path $RepoRoot "shrimp_data"),
  (Join-Path $RepoRoot "automation\reports"),
  (Join-Path $RepoRoot "automation\screenshots")
)

foreach ($dir in $runtimeDirs) {
  if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
    Write-Ok "생성됨: $dir"
  } else {
    Write-Ok "확인됨: $dir"
  }
}

Write-Host ""
Write-Host "환경 준비가 끝났습니다." -ForegroundColor Green
Write-Host ""
Write-Host "다음 단계:"
Write-Host "  1) automation\.env 에 테스트 계정 비밀번호(ACTEST1~3_PASSWORD)를 채우세요."
Write-Host "     계정은 https://automationexercise.com/ 에서 직접 3개 가입한 뒤"
Write-Host "     automation\test_data\accounts.json 의 이메일도 본인 계정으로 바꿔야 합니다."
Write-Host "  2) MCP 연결:  powershell -ExecutionPolicy Bypass -File scripts\setup\2-setup-mcp.ps1"
Write-Host "  3) Git 연결:  powershell -ExecutionPolicy Bypass -File scripts\setup\3-setup-git.ps1"
Write-Host "  4) 동작 확인: powershell -ExecutionPolicy Bypass -File scripts\setup\4-verify.ps1"
Write-Host ""
Write-Host "자세한 내용은 docs\setup\WINDOWS_SETUP.md 를 참고하세요."
