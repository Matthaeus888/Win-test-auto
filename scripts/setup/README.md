# setup

Windows 로컬 환경에서 `qa-process` 저장소를 실행 가능한 상태로 만드는 세팅 스크립트입니다.
원 저장소가 macOS 기준(`.mcp.json` 의 `/Users/...` 경로)으로 작성되어 있어, 이 스크립트들이
해당 부분을 Windows 경로/실행 방식으로 대체합니다.

전체 절차와 배경 설명은 [`docs/setup/WINDOWS_SETUP.md`](../../docs/setup/WINDOWS_SETUP.md)에
있습니다. 이 문서는 스크립트 요약만 담습니다.

## 실행 순서

저장소 루트에서 PowerShell 로 실행합니다.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup\1-setup-env.ps1
powershell -ExecutionPolicy Bypass -File scripts\setup\2-setup-mcp.ps1
powershell -ExecutionPolicy Bypass -File scripts\setup\3-setup-git.ps1 -RemoteUrl https://github.com/<계정>/qa-process.git
powershell -ExecutionPolicy Bypass -File scripts\setup\4-verify.ps1
```

| 스크립트 | 역할 | 주요 옵션 |
|---|---|---|
| `1-setup-env.ps1` | 필수 도구 점검, `.venv` 생성, 의존성 설치, `.env` 준비, 런타임 디렉터리 생성 | - |
| `2-setup-mcp.ps1` | shrimp-task-manager clone/build, Windows 경로 기준 `.mcp.json` 작성 | `-ShrimpDir`, `-SkipShrimp` |
| `3-setup-git.ps1` | `git init`, 브랜치 master 고정, 민감정보 검사, 승인 후 commit/push | `-RemoteUrl` |
| `4-verify.ps1` | 설정 점검 후 pytest 실행, HTML/JUnit 리포트 생성 | `-TestPath`, `-All`, `-Headless` |

## 설계상 지켜지는 원칙

- `3-setup-git.ps1` 은 commit 과 push 를 각각 사용자 확인(`y` 입력) 없이 수행하지 않습니다
  (`CLAUDE.md` 14절, 18절).
- commit 직전 `.env`, `service-account*.json`, `*-credentials.json` 등이 스테이징에 포함되면
  중단합니다 (`CLAUDE.md` 17절).
- shrimp-task-manager 는 저장소 바깥(`%USERPROFILE%\automation`)에 설치해 커밋 대상에서
  제외합니다.
- 모든 스크립트는 반복 실행해도 안전하도록 이미 완료된 항목을 건너뜁니다.
