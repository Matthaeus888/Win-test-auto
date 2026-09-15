<#
.SYNOPSIS
  로컬 환경에서 자동화 테스트가 실제로 동작하는지 확인한다.

.DESCRIPTION
  1. .venv / 의존성 / .env 구성 상태를 점검한다.
  2. 지정한 테스트 파일을 실행하고 HTML + JUnit XML 리포트를 남긴다.
     기본값은 로그인 테스트(tests/test_login.py) 한 파일이며, 전체 실행은 -All 로 지정한다.

  결과 해석은 CLAUDE.md 13절(테스트 실패 원인을 Automation Code / Test Data /
  Test Environment / 실제 Product 문제 중 하나로 구분)을 따른다. 실패를 임의로
  PASS 처리하지 않는다.

.PARAMETER TestPath
  실행할 테스트 경로(automation 디렉터리 기준). 기본값 tests/test_login.py

.PARAMETER All
  automation/tests 전체를 실행한다.

.PARAMETER Headless
  CI 와 동일하게 headless 모드로 실행한다(환경변수 CI=true).

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\setup\4-verify.ps1
  powershell -ExecutionPolicy Bypass -File scripts\setup\4-verify.ps1 -All -Headless
#>

param(
  [string]$TestPath = "tests/test_login.py",
  [switch]$All,
  [switch]$Headless
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$AutomationDir = Join-Path $RepoRoot "automation"
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

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

# ---------------------------------------------------------------------------
# 1. 사전 점검
# ---------------------------------------------------------------------------
Write-Step "1/2 사전 점검"

if (-not (Test-Path $VenvPython)) {
  throw ".venv 가 없습니다. 먼저 1-setup-env.ps1 을 실행하세요."
}
Write-Ok "가상환경 확인: $VenvPython"

& $VenvPython -c "import selenium, pytest, dotenv" 2>$null
if ($LASTEXITCODE -ne 0) {
  throw "의존성이 설치되어 있지 않습니다. 1-setup-env.ps1 을 다시 실행하세요."
}
Write-Ok "selenium / pytest / python-dotenv 확인"

$envFile = Join-Path $AutomationDir ".env"
if (-not (Test-Path $envFile)) {
  Write-Warn2 "automation\.env 가 없습니다. 로그인 관련 테스트는 실패합니다."
} else {
  $envContent = Get-Content $envFile -Raw
  $emptyKeys = @()
  foreach ($key in @("ACTEST1_PASSWORD", "ACTEST2_PASSWORD", "ACTEST3_PASSWORD")) {
    if ($envContent -match "(?m)^\s*$key\s*=\s*$") { $emptyKeys += $key }
  }
  if ($emptyKeys.Count -gt 0) {
    Write-Warn2 "값이 비어 있는 항목: $($emptyKeys -join ', ') - 로그인 관련 테스트가 실패합니다."
  } else {
    Write-Ok "automation\.env 계정 비밀번호 채워짐"
  }
}

$accountsFile = Join-Path $AutomationDir "test_data\accounts.json"
if (Test-Path $accountsFile) {
  $accountsRaw = Get-Content $accountsFile -Raw
  if ($accountsRaw -match "actest1@test\.com") {
    Write-Warn2 "test_data\accounts.json 이 예시 이메일(actest1@test.com) 그대로입니다."
    Write-Warn2 "automationexercise.com 에 직접 가입한 본인 계정 이메일로 바꿔야 통과합니다."
  } else {
    Write-Ok "test_data\accounts.json 이 사용자 계정으로 설정됨"
  }
}

# ---------------------------------------------------------------------------
# 2. 테스트 실행
# ---------------------------------------------------------------------------
Write-Step "2/2 테스트 실행"

if ($All) { $TestPath = "tests/" }

if ($Headless) {
  $env:CI = "true"
  Write-Host "  실행 모드: headless (CI=true)"
} else {
  Remove-Item Env:\CI -ErrorAction SilentlyContinue
  Write-Host "  실행 모드: headed (브라우저 창이 열립니다)"
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$htmlReport = "reports/report_$timestamp.html"
$xmlReport = "reports/results_$timestamp.xml"

Push-Location $AutomationDir
try {
  & $VenvPython -m pytest $TestPath --html=$htmlReport --self-contained-html --junitxml=$xmlReport
  $exitCode = $LASTEXITCODE
} finally {
  Pop-Location
}

Write-Host ""
if ($exitCode -eq 0) {
  Write-Host "테스트 통과" -ForegroundColor Green
} else {
  Write-Host "테스트 실패 (pytest exit code: $exitCode)" -ForegroundColor Red
  Write-Host "실패 원인을 아래 4가지 중 하나로 구분한 뒤 대응하세요 (CLAUDE.md 13절)." -ForegroundColor Yellow
  Write-Host "  - Automation Code 문제 / Test Data 문제 / Test Environment 문제 / 실제 Product 문제"
  Write-Host "실패 스크린샷: automation\screenshots\"
}

Write-Host "리포트: $(Join-Path $AutomationDir $htmlReport)"
exit $exitCode
