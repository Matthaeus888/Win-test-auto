# Windows 로컬 환경 세팅 가이드

이 문서는 `qa-process` 저장소를 Windows PC에서 **AI Agent(Claude Code) + Git + CI** 가 모두
연결된 상태로 돌리기 위한 절차를 정리한 것입니다.

원 저장소는 macOS 기준으로 작성되어 있었고(`.mcp.json` 의 `/Users/...` 경로), 이 문서와
`scripts/setup/` 의 스크립트가 그 부분을 Windows 환경으로 대체합니다.

- 저장소 경로: `C:\Users\8j8n\Downloads\qa-process-master\qa-process-master`
- 아래 명령은 모두 **저장소 루트**에서 PowerShell 로 실행합니다.

---

## 0. 전체 그림

```
[요구사항]
   │  prd-agent
   ▼
docs/prd/project-prd.md, docs/prd/feature/{slug}.md      ← 사용자 승인
   │  tc-agent  (+ tc-writing Skill, sheets_sync)
   ▼
docs/tc/{slug}.md                                        (Google Sheets 기록 가능)
   │  automation-candidate-agent (+ automation-candidate Skill)
   ▼
docs/tc/automation-candidates/{slug}.md                  ← 사용자 승인(자동화 대상 확정)
   │  roadmap-agent
   ▼
docs/roadmap/ROADMAP.md                                  ← 사용자 승인
   │  automation-developer-agent (+ playwright MCP 로 Locator 조사)
   ▼
automation/pages, automation/tests  (Selenium + pytest + POM)
   │  로컬 실행 → 코드 리뷰 → Git Commit / Push  ← 사용자 승인
   ▼
GitHub Actions (.github/workflows/ci.yml) → 리포트 Artifact → 실패 시 Slack 알림
```

승인이 필요한 5개 작업(Project PRD / Feature PRD / 자동화 대상 최종 선정 / Commit / Push)은
`CLAUDE.md` 18절에 정의되어 있으며, 세팅 스크립트도 이 원칙을 따릅니다(3-setup-git.ps1 은
commit/push 전에 반드시 사용자 확인을 받습니다).

---

## 1. 사전 설치

| 항목 | 용도 | 확인 |
|---|---|---|
| Python 3.9 이상 | Selenium/pytest 실행 | 설치 시 **Add python.exe to PATH** 체크 |
| Git for Windows | 버전 관리, GitHub 연동 | `git --version` |
| Node.js LTS | Playwright MCP / shrimp-task-manager MCP 실행 | `node --version` |
| Google Chrome | 테스트 실행 브라우저 | 최신 버전 권장 |
| Claude Code | AI Agent 실행 | `npm install -g @anthropic-ai/claude-code` |

ChromeDriver는 따로 설치하지 않습니다. Selenium 4.20+ 의 Selenium Manager가 Chrome 버전에
맞는 드라이버를 자동으로 내려받습니다.

---

## 2. 실행 환경 준비

```powershell
cd C:\Users\8j8n\Downloads\qa-process-master\qa-process-master
powershell -ExecutionPolicy Bypass -File scripts\setup\1-setup-env.ps1
```

수행 내용

- 필수 도구 설치 여부 검사 (하나라도 없으면 안내 후 중단)
- 저장소 루트에 가상환경 `.venv` 생성
- `automation/requirements.txt`, `scripts/sheets_sync/requirements.txt` 설치
- `.env.example` → `.env`, `automation/.env.example` → `automation/.env` 복사 (이미 있으면 유지)
- `shrimp_data/`, `automation/reports/`, `automation/screenshots/` 생성

반복 실행해도 안전합니다(이미 되어 있는 항목은 건너뜁니다).

### 2.1 테스트 계정 준비 (중요)

저장소에 들어 있는 `actest1@test.com` 등은 원 작성자의 계정이라 그대로는 로그인 테스트가
통과하지 않습니다.

1. <https://automationexercise.com/> 에서 테스트용 계정을 3개 가입합니다.
2. `automation/test_data/accounts.json` 의 이메일을 본인 계정으로 교체합니다.

   ```json
   {
     "actest1": {"email": "본인계정1@example.com"},
     "actest2": {"email": "본인계정2@example.com"},
     "actest3": {"email": "본인계정3@example.com"}
   }
   ```

3. `automation/.env` 에 각 계정의 비밀번호를 채웁니다.

   ```
   ACTEST1_PASSWORD=...
   ACTEST2_PASSWORD=...
   ACTEST3_PASSWORD=...
   ```

`.env` 는 `.gitignore` 에 포함되어 있어 커밋되지 않습니다(`CLAUDE.md` 17절).

---

## 3. AI Agent(MCP) 연결

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup\2-setup-mcp.ps1
```

수행 내용

- `shrimp-task-manager` 를 `%USERPROFILE%\automation\mcp-shrimp-task-manager` 에 clone + build
  (저장소 바깥에 두어 커밋 대상에서 제외)
- 실제 경로가 반영된 `.mcp.json` 을 저장소 루트에 기록 (기존 파일은 `.mcp.json.bak` 으로 백업)

Windows 에서는 `npx` 를 직접 실행하면 MCP 연결이 실패하는 경우가 있어, playwright MCP 는
`cmd /c npx ...` 형태로 설정합니다.

shrimp-task-manager 가 필요 없으면 아래처럼 건너뛸 수 있습니다. 없어도 PRD → TC → 자동화
워크플로우는 정상 동작합니다.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup\2-setup-mcp.ps1 -SkipShrimp
```

### 3.1 Claude Code 실행 및 확인

```powershell
cd C:\Users\8j8n\Downloads\qa-process-master\qa-process-master
claude
```

Claude Code 안에서

- `/mcp` — playwright / shrimp-task-manager 연결 상태 확인
- `/agents` — `prd-agent`, `tc-agent`, `automation-candidate-agent`, `roadmap-agent`,
  `automation-developer-agent` 인식 여부 확인

`CLAUDE.md` 와 `shrimp-rules.md` 는 저장소 루트에 있으므로 이 폴더에서 실행할 때 자동으로
읽힙니다. 각 Agent의 담당 범위는 `.claude/agents/**/*.md`, 판단 기준은
`.claude/skills/*/SKILL.md` 와 `docs/automation/AUTOMATION_GUIDE.md` 에 정의되어 있습니다.

---

## 4. Git 연결

### 4.1 GitHub 에 빈 저장소 만들기

GitHub → **New repository** → 이름(예: `qa-process`) → **README/.gitignore/license 추가 없이**
빈 상태로 생성합니다(초기 커밋이 있으면 첫 push 가 충돌합니다).

### 4.2 로컬 저장소 초기화 + 원격 연결

```powershell
# 원격 주소 없이 로컬 초기화만
powershell -ExecutionPolicy Bypass -File scripts\setup\3-setup-git.ps1

# 원격까지 한 번에
powershell -ExecutionPolicy Bypass -File scripts\setup\3-setup-git.ps1 -RemoteUrl https://github.com/<계정>/qa-process.git
```

수행 내용

- `git config --global user.name / user.email` 확인 (없으면 안내 후 중단)
- `git init` 및 기본 브랜치 `master` 설정 — CI가 `master` push 를 트리거로 쓰기 때문입니다
- 스테이징 파일에 `.env`, `service-account*.json` 등 민감정보가 섞였는지 검사 (있으면 중단)
- 커밋 대상 파일과 예정 Commit Message 를 보여준 뒤 **y 입력 시에만** commit
- 원격 연결 후 **y 입력 시에만** push

`CLAUDE.md` 14절/18절대로 commit 과 push 는 각각 별도 확인을 거칩니다.

첫 push 시 GitHub 로그인 창이 뜨면 브라우저 인증 또는 Personal Access Token 으로 로그인합니다.

---

## 5. GitHub Secrets 등록

push 후 CI가 정상 동작하려면 GitHub 저장소에서
**Settings → Secrets and variables → Actions → New repository secret** 으로 등록합니다.

| Secret 이름 | 필수 | 값 |
|---|---|---|
| `ACTEST1_PASSWORD` | 필수 | 테스트 계정 1 비밀번호 |
| `ACTEST2_PASSWORD` | 필수 | 테스트 계정 2 비밀번호 |
| `ACTEST3_PASSWORD` | 필수 | 테스트 계정 3 비밀번호 |
| `SLACK_WEBHOOK_URL` | 선택 | Slack Incoming Webhook URL |

`SLACK_WEBHOOK_URL` 이 없으면 Slack 알림 step 은 건너뛰고 CI 는 정상 진행됩니다.

### 5.1 Slack Webhook 발급

1. <https://api.slack.com/apps> → Create New App → From scratch
2. 알림을 받을 워크스페이스 선택
3. **Incoming Webhooks** 활성화 → **Add New Webhook to Workspace** → 채널 선택
4. 발급된 `https://hooks.slack.com/services/...` URL 을 `SLACK_WEBHOOK_URL` Secret 으로 등록

Slack 은 CI 결과 알림 전용입니다. Commit/Push 승인 용도로 쓰지 않습니다(`CLAUDE.md` 16절).

---

## 6. 동작 확인

```powershell
# 로그인 테스트 한 파일만, 브라우저 창을 띄워서 실행
powershell -ExecutionPolicy Bypass -File scripts\setup\4-verify.ps1

# 전체 테스트를 CI 와 동일한 headless 로 실행
powershell -ExecutionPolicy Bypass -File scripts\setup\4-verify.ps1 -All -Headless
```

- 리포트: `automation/reports/report_{타임스탬프}.html`
- 실패 스크린샷: `automation/screenshots/`
- 둘 다 git 미추적입니다.

직접 pytest 를 쓰려면:

```powershell
cd automation
..\.venv\Scripts\python.exe -m pytest tests\
..\.venv\Scripts\python.exe -m pytest tests\test_cart.py::test_add_to_cart_shows_modal
```

테스트가 실패하면 임의로 PASS 처리하지 않고 원인을 아래 4가지로 구분합니다
(`CLAUDE.md` 13절).

- Automation Code 문제 / Test Data 문제 / Test Environment 문제 / 실제 Product 문제

---

## 7. Google Sheets 연동 (선택)

TC와 자동화 후보 평가 결과를 구글 시트에 기록하려면 추가 설정이 필요합니다.

1. Google Cloud Console 에서 **Google Sheets API** 활성화
2. 서비스 계정 생성 → JSON 키 발급
3. 기록 대상 Spreadsheet 의 공유 설정에서 **서비스 계정 이메일을 편집자로 추가**
   (프로젝트 전체 권한이 아니라 해당 문서만 공유 — 최소 권한 원칙)
4. 저장소 루트 `.env` 에 값을 채웁니다.

   ```
   GOOGLE_SERVICE_ACCOUNT_FILE=C:\Users\8j8n\secrets\qa-process-credentials.json
   GOOGLE_SHEET_ID=...
   GOOGLE_WORKSHEET_NAME=TC
   GOOGLE_CANDIDATE_SHEET_ID=...
   GOOGLE_CANDIDATE_WORKSHEET_NAME=Automation Candidates
   ```

   `GOOGLE_CANDIDATE_SHEET_ID` 는 `GOOGLE_SHEET_ID` 와 **다른 Spreadsheet 문서**여야 합니다
   (같은 문서의 다른 탭이 아님).

5. 확인

   ```powershell
   .venv\Scripts\python.exe scripts\sheets_sync\sheets_sync.py list
   ```

JSON 키 파일은 저장소 바깥에 두는 것을 권장합니다. 저장소 안에 둔다면 `.gitignore` 의
`service-account*.json`, `*-credentials.json` 패턴에 맞는 이름을 쓰세요.

자세한 사용법은 `scripts/sheets_sync/README.md` 를 참고하세요.

---

## 8. 일상 작업 흐름

```powershell
cd C:\Users\8j8n\Downloads\qa-process-master\qa-process-master
claude
```

Claude Code 안에서 단계별로 Agent에게 요청합니다. 예:

- "checkout 기능 Feature PRD를 작성해줘" → `prd-agent` → 검토 후 승인
- "승인된 checkout PRD로 TC를 작성해줘" → `tc-agent` (`tc-writing` Skill 기준 적용)
- "checkout TC의 자동화 대상을 평가해줘" → `automation-candidate-agent` → **최종 선정은 사용자**
- "확정된 자동화 대상으로 Roadmap을 갱신해줘" → `roadmap-agent` → 승인
- "Roadmap Phase N을 구현해줘" → `automation-developer-agent` (Locator 조사에 playwright MCP 사용)

구현이 끝나면 로컬 실행 → 리뷰 → 승인 후 commit → 승인 후 push → GitHub Actions 실행 →
실패 시 Slack 알림 순으로 이어집니다.

---

## 9. 자주 겪는 문제

| 증상 | 원인 / 해결 |
|---|---|
| `... 스크립트를 로드할 수 없습니다` | 실행 정책 문제. 명령 앞에 `powershell -ExecutionPolicy Bypass -File` 을 붙여 실행 |
| `python` 을 찾을 수 없음 | Python 설치 시 PATH 미등록. 재설치하거나 시스템 환경 변수에 직접 추가 |
| Chrome 과 드라이버 버전 불일치 | Chrome 을 최신으로 업데이트. Selenium Manager 가 드라이버를 다시 내려받음 |
| `/mcp` 에 playwright 가 안 뜸 | Node.js 설치 확인 후 `2-setup-mcp.ps1` 재실행, Claude Code 재시작 |
| 로그인 테스트만 무더기 실패 | 2.1의 계정 설정(accounts.json + .env) 미완료 |
| CI 에서 로그인 테스트 실패 | GitHub Secrets(`ACTEST1~3_PASSWORD`) 미등록 |
| push 했는데 CI 가 안 돌음 | 브랜치가 `master` 가 아님. `git branch -M master` 후 재push |
| 한글이 깨져 보임 | PowerShell 에서 `chcp 65001` 실행 후 재시도 |

---

## 변경 이력

| 날짜 | 변경 사유 |
|---|---|
| 2026-09-15 | 최초 작성. macOS 기준 저장소를 Windows 로컬 환경(AI Agent + Git + CI)에서 실행하기 위한 세팅 절차 정리. |
