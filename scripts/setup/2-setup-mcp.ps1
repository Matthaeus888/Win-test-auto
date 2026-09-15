<#
.SYNOPSIS
  AI Agent(Claude Code)가 사용하는 MCP 서버를 Windows 환경에 맞게 연결한다.

.DESCRIPTION
  - playwright MCP: npx 로 실행되므로 별도 설치 없이 .mcp.json 설정만 필요하다.
    (Windows 에서는 npx 를 직접 spawn 하면 실패하는 경우가 있어 cmd /c 로 감싼다)
  - shrimp-task-manager MCP: 저장소를 clone 하고 build 해야 하므로 이 스크립트에서 처리한다.
    저장소 바깥(기본값 %USERPROFILE%\automation)에 두어 qa-process 저장소 커밋 대상에서 제외한다.

  마지막에 실제 경로가 반영된 .mcp.json 을 저장소 루트에 기록한다.

.PARAMETER ShrimpDir
  shrimp-task-manager 를 설치할 로컬 경로. 기본값 %USERPROFILE%\automation\mcp-shrimp-task-manager

.PARAMETER SkipShrimp
  shrimp-task-manager 설치를 건너뛰고 playwright MCP 만 설정한다.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File scripts\setup\2-setup-mcp.ps1
#>

param(
  [string]$ShrimpDir = (Join-Path $env:USERPROFILE "automation\mcp-shrimp-task-manager"),
  [switch]$SkipShrimp
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$McpFile = Join-Path $RepoRoot ".mcp.json"
$ShrimpRepoUrl = "https://github.com/cjo4m06/mcp-shrimp-task-manager.git"

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

function ConvertTo-JsonPath([string]$Path) {
  # JSON 안에서는 역슬래시 이스케이프 문제를 피하기 위해 슬래시 경로를 쓴다.
  # Node.js 는 Windows 에서도 슬래시 경로를 정상 처리한다.
  return ($Path -replace '\\', '/')
}

Write-Host "저장소 경로: $RepoRoot"

# ---------------------------------------------------------------------------
# 1. shrimp-task-manager 설치/빌드
# ---------------------------------------------------------------------------
$shrimpEntry = Join-Path $ShrimpDir "dist\index.js"
$shrimpReady = $false

if ($SkipShrimp) {
  Write-Step "1/2 shrimp-task-manager (건너뜀)"
  Write-Warn2 "-SkipShrimp 옵션이 지정되어 설치하지 않습니다."
} else {
  Write-Step "1/2 shrimp-task-manager MCP 설치"

  if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    throw "Node.js 가 설치되어 있지 않습니다. 먼저 1-setup-env.ps1 을 실행하세요."
  }

  if (Test-Path $shrimpEntry) {
    Write-Ok "이미 빌드되어 있음: $shrimpEntry"
    $shrimpReady = $true
  } else {
    $parent = Split-Path $ShrimpDir -Parent
    if (-not (Test-Path $parent)) {
      New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if (-not (Test-Path (Join-Path $ShrimpDir ".git"))) {
      Write-Host "  clone: $ShrimpRepoUrl"
      & git clone --depth 1 $ShrimpRepoUrl $ShrimpDir
    }

    Push-Location $ShrimpDir
    try {
      Write-Host "  npm install ..."
      & cmd /c "npm install" | Out-Null
      Write-Host "  npm run build ..."
      & cmd /c "npm run build" | Out-Null
    } finally {
      Pop-Location
    }

    if (Test-Path $shrimpEntry) {
      Write-Ok "빌드 완료: $shrimpEntry"
      $shrimpReady = $true
    } else {
      Write-Warn2 "빌드 산출물($shrimpEntry)을 찾지 못했습니다. shrimp MCP 없이 .mcp.json 을 작성합니다."
      Write-Warn2 "shrimp-task-manager 는 선택 사항이며, 없어도 PRD/TC/자동화 워크플로우는 동작합니다."
    }
  }
}

# ---------------------------------------------------------------------------
# 2. .mcp.json 작성
# ---------------------------------------------------------------------------
Write-Step "2/2 .mcp.json 작성"

$dataDir = Join-Path $RepoRoot "shrimp_data"
if (-not (Test-Path $dataDir)) {
  New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
}

$servers = [ordered]@{
  playwright = [ordered]@{
    type    = "stdio"
    command = "cmd"
    args    = @("/c", "npx", "-y", "@playwright/mcp@latest")
    env     = @{}
  }
}

if ($shrimpReady) {
  $servers["shrimp-task-manager"] = [ordered]@{
    type    = "stdio"
    command = "node"
    args    = @((ConvertTo-JsonPath $shrimpEntry))
    env     = [ordered]@{
      DATA_DIR      = (ConvertTo-JsonPath $dataDir)
      TEMPLATES_USE = "en"
      ENABLE_GUI    = "false"
    }
  }
}

if (Test-Path $McpFile) {
  $backup = "$McpFile.bak"
  Copy-Item $McpFile $backup -Force
  Write-Ok "기존 파일 백업: $backup"
}

$payload = [ordered]@{ mcpServers = $servers }
$json = $payload | ConvertTo-Json -Depth 6

# ConvertTo-Json 이 슬래시를 이스케이프하지 않도록 정리하고, BOM 없는 UTF-8 로 기록한다.
$json = $json -replace '\\/', '/'
[System.IO.File]::WriteAllText($McpFile, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Ok "작성 완료: $McpFile"

Write-Host ""
Write-Host "--- .mcp.json 내용 ---" -ForegroundColor DarkGray
Get-Content $McpFile | Write-Host
Write-Host "----------------------" -ForegroundColor DarkGray

Write-Host ""
Write-Host "MCP 설정이 끝났습니다." -ForegroundColor Green
Write-Host "Claude Code 를 이 저장소 폴더에서 다시 실행하면 .mcp.json 을 읽어 MCP 서버를 연결합니다."
Write-Host "  cd `"$RepoRoot`""
Write-Host "  claude"
Write-Host "연결 상태는 Claude Code 안에서 /mcp 명령으로 확인할 수 있습니다."
