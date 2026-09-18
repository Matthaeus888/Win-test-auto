# Development Guidelines

이 문서는 `qa-process` 저장소에서 작업하는 AI Agent(Claude Code, Sub Agent, Skill 포함) 전용
운영 규칙이다. 일반 개발/QA 지식은 담지 않으며, 이 저장소에서만 유효한 규칙과 파일 라우팅
정보만 담는다.

**이 문서는 저장소 루트의 `CLAUDE.md`(프로젝트 최상위 지침)와 충돌할 수 없다.
두 문서의 내용이 다르게 보이면 항상 CLAUDE.md가 우선한다.**

---

## 1. Project Overview

### 무엇을 만드는가

- `automationexercise.com`(이커머스 연습 사이트)에 대한 QA 산출물(PRD → TC → 자동화 대상
  선정 → Roadmap → Selenium 자동화 코드)을 사용자 승인 지점을 유지하며 생성하는 프로젝트.
- 자동화 코드는 아직 구현되지 않았다. 현재 저장소에는 `/docs` 산출물, `.claude/agents`,
  `.claude/skills`, `scripts/sheets_sync`(Google Sheets 연동 스크립트)만 존재한다.

### 이 저장소에서 유일하게 확정된 기술 스택

- 문서: Markdown (`/docs` 하위)
- 자동화 코드(예정): Python + Selenium + pytest + Page Object Model
  (`docs/automation/AUTOMATION_GUIDE.md` 1절 참조)
- Sheet 연동: Python 스크립트 `scripts/sheets_sync/sheets_sync.py` (gspread + google-auth)
- Task 관리: `shrimp-task-manager` MCP (`DATA_DIR=shrimp_data/`, `.mcp.json` 참조)

---

## 2. Source of Truth 라우팅 (판단 전 반드시 확인)

작업 중 규칙/기준 판단이 필요하면 아래 표로 "어느 문서를 Read해야 하는지" 먼저 확인한다.
아래 문서의 세부 내용을 이 파일에 옮겨 적지 않는다 — 원본이 바뀌면 이 파일이 stale해지므로,
항상 원본 문서를 직접 Read한다.

| 판단 대상 | 반드시 Read할 문서 |
|---|---|
| 워크플로우 전체 원칙, 승인 게이트, Git/Slack/Secret 운영 원칙 | `CLAUDE.md` (저장소 루트) |
| TC 작성 품질 기준·컬럼 정의·Priority 산정·Naming Rule | `.claude/skills/tc-writing/SKILL.md` |
| 자동화 대상 선정 평가 기준(Automation Score, Hard Rule 등) | `.claude/skills/automation-judge/SKILL.md` |
| 자동화 코드 작성 방식(언어/구조/Locator/Wait/Naming/CI 등) | `docs/automation/AUTOMATION_GUIDE.md` |
| 요구사항(Feature 단위) | `docs/prd/feature/{slug}.md` (승인된 것만) |
| 프로젝트 전체 요구사항/대상 서비스 정보 | `docs/prd/project-prd.md` |
| Test Scenario | `docs/tc/{slug}.md` (승인된 것만) |
| 자동화 대상 확정 여부/Approved TC 목록 | `docs/tc/automation-judge/{slug}.md` |
| 자동화 구현 순서/Phase 범위 | `docs/roadmap/ROADMAP.md` (승인된 것만) |
| Google Sheets 연동 방법/제약 | `scripts/sheets_sync/sheets_sync.py` 상단 docstring, `scripts/sheets_sync/README.md` |
| Google Docs 연동 방법/제약 (PRD/Roadmap) | `scripts/docs_sync/docs_sync.py` 상단 docstring, `scripts/docs_sync/README.md` |
| 로컬(Windows) 실행 환경/MCP/Git/CI Secret 세팅 절차 | `docs/setup/WINDOWS_SETUP.md`, `scripts/setup/README.md` |
| 각 Agent의 담당 범위/워크플로우 | 해당 Agent 정의 파일(`.claude/agents/**/*.md`) |

- 두 문서의 내용이 서로 다르게 보이면 **임의로 하나를 선택하지 않는다.** 충돌 내용을
  사용자에게 보고하고 확인·승인을 받은 뒤에만 다음 작업을 진행한다(CLAUDE.md 8절).

---

## 3. 디렉터리/파일 배치 규칙

### 3.1 기존 구조 (실제 존재)

```
docs/prd/project-prd.md
docs/prd/feature/{slug}.md
docs/tc/{slug}.md
docs/tc/automation-judge/{slug}.md
docs/roadmap/ROADMAP.md
docs/automation/AUTOMATION_GUIDE.md
.claude/agents/{prd-agent, tc-agent, automation-judge-agent}.md   # 산출물 작성 계열
.claude/agents/dev/{roadmap-agent, automation-developer-agent}.md    # 개발 계열
.claude/skills/{tc-writing, automation-judge}/SKILL.md
scripts/sheets_sync/sheets_sync.py
scripts/docs_sync/docs_sync.py
scripts/notify_slack/notify.py
scripts/setup/*.ps1                                                   # 로컬(Windows) 실행 환경 세팅 스크립트
docs/setup/WINDOWS_SETUP.md                                           # 로컬 환경 세팅 절차
.github/workflows/ci.yml
shrimp_data/                                                          # shrimp-task-manager DATA_DIR, 직접 수정 금지
```

### 3.2 신규 파일 생성 시 규칙

- 새 산출물 문서는 반드시 위 3.1 구조의 대응 하위 디렉터리에 만든다. 예: 새 Feature PRD →
  `docs/prd/feature/{slug}.md`, 새 Feature TC → `docs/tc/{slug}.md`. 임의의 새 최상위
  디렉터리를 만들지 않는다.
- 자동화 코드(`automation/` 등)를 처음 생성할 때는 `docs/automation/AUTOMATION_GUIDE.md`
  3절에 정의된 예정 구조(`automation/pages`, `automation/tests`, `automation/utils`,
  `automation/config`, `automation/test_data`, `automation/conftest.py`,
  `automation/pytest.ini`, `automation/requirements.txt`)를 그대로 따른다. 이 구조와 다르게
  만들어야 할 이유가 생기면, AUTOMATION_GUIDE.md를 먼저 갱신하고 사용자 확인을 받은 뒤 반영한다.
- Google Sheets 연동이 필요한 새 기능은 `scripts/sheets_sync/sheets_sync.py`를 확장하거나
  호출하는 방식으로 구현한다. Agent/Skill이 Google Sheets API를 직접 호출하는 별도 경로를
  새로 만들지 않는다.
- Google Docs 연동(PRD/Roadmap 등 서술형 문서)이 필요한 새 기능은 `scripts/docs_sync/docs_sync.py`
  를 확장하거나 호출하는 방식으로 구현한다. Agent/Skill이 Google Docs API를 직접 호출하는
  별도 경로를 새로 만들지 않는다. 표 형태 데이터(TC/Judge)와 서술형 문서(PRD/Roadmap)는
  각각 `sheets_sync`/`docs_sync`로 모듈이 분리되어 있으므로 서로 섞어 쓰지 않는다.
- `.github/workflows/ci.yml`(CI)은 이미 생성되어 있다. CLAUDE.md 15절/AUTOMATION_GUIDE.md
  16절에 정의된 CI 운영 흐름(Push → Actions → 테스트 실행 → Report → 판정 → Slack)을 벗어나는
  변경이 필요하면 사용자 확인을 받은 뒤 반영한다.
- 로컬 환경 세팅 스크립트는 `scripts/setup/` 아래에만 둔다. 이 스크립트들은 산출물이 아니라
  환경 구성 도구이므로 `docs/` 하위에 만들지 않는다.

### 3.3 신규 Agent/Skill 추가 위치

- 산출물(문서) 작성 책임의 Agent → `.claude/agents/` 바로 아래.
- 코드/개발 실행 책임의 Agent(구현, 실행, Roadmap 등 개발팀 관점) → `.claude/agents/dev/`
  아래.
- 특정 산출물의 "작성 규칙/평가 기준"(워크플로우가 아닌 판단 기준)을 재사용 가능하게 분리해야
  하면 Agent 정의에 직접 쓰지 않고 `.claude/skills/{skill-name}/SKILL.md`로 분리한 뒤 Agent가
  이를 Read해서 따르게 한다(`tc-agent` + `tc-writing`, `automation-judge-agent` +
  `automation-judge` 패턴을 따른다).
- 새 Agent 정의 파일은 다음을 반드시 포함한다: frontmatter(`name`, `description`, `model`,
  `tools`), 담당 범위가 아닌 것(다른 Agent 책임)을 명시하는 절, 사용하는 Skill/Guide가 있으면
  "자체 정의하지 않고 Read해서 따른다"는 명시적 문장.

---

## 4. 언어·네이밍 규칙 (전역 vs Python 예외)

| 대상 | 규칙 | 근거 |
|---|---|---|
| Markdown 문서(PRD/TC/Roadmap/Guide 등) | 한국어 작성, 변수/식별자성 표현 외 전부 한국어 | `~/.claude/CLAUDE.md` |
| `scripts/sheets_sync` 등 기존 비-자동화 Python 코드 | 전역 스타일(2칸 들여쓰기) 유지, 변수명 영어 | `~/.claude/CLAUDE.md`, 기존 코드 컨벤션 |
| `automation/` 하위 Selenium 자동화 Python 코드 | **PEP8 예외 적용**: 4칸 들여쓰기, snake_case 함수/변수, UPPER_SNAKE_CASE 상수(Locator), PascalCase + `Page` 접미사 클래스 | `AUTOMATION_GUIDE.md` 1.1절, 18절 (2026-08-27 사용자 승인) |
| 주석 | 한국어 | `~/.claude/CLAUDE.md`, `AUTOMATION_GUIDE.md` 17절 |
| 커밋 메시지 | 한국어 | `~/.claude/CLAUDE.md` |

**주의**: 전역 CLAUDE.md의 "들여쓰기 2칸/camelCase" 기본 스타일을 `automation/` 하위 Python
코드에 적용하지 않는다. 이 예외는 Python 자동화 코드에만 한정되며, Markdown 문서나
`scripts/sheets_sync`의 기존 컨벤션까지 바꾸지 않는다.

---

## 5. 항상 사용자 승인이 필요한 작업 (CLAUDE.md 18절과 동일, 재확인용)

다음 5가지는 워크플로우 단계와 무관하게 항상 사용자 승인 필요. 임의로 확정/실행하지 않는다.

1. Project PRD 승인
2. Feature PRD 승인
3. TC 자동화 대상 최종 선정
4. Git Commit
5. Git Push

---

## 6. 절대 하지 말아야 할 것 (프로젝트 관찰 사실 기반)

- `상태: 승인완료`로 표시된 문서(PRD/TC/Roadmap/Judge 문서)를 후속 작업에서 임의로 수정하지
  않는다. 수정이 필요하면 사유·영향을 사용자에게 보고하고 재승인 후에만 반영한다.
- `scripts/sheets_sync/sheets_sync.py`의 TC 시트 대상으로 update/delete를 새로 구현하지
  않는다(append/list만 제공하도록 설계된 의도적 제약).
- `scripts/sheets_sync/sheets_sync.py`의 Judge 시트에서 `QA Decision`, `QA Comment`
  컬럼에 쓰기 동작을 추가하지 않는다(사용자 작성 전용, AI는 읽기만 가능).
- Slack 연동을 Commit/Push 등 승인 용도로 사용하지 않는다(CI 결과 알림 전용,
  `CLAUDE.md` 16절).
- `automation/` Python 코드에서 `time.sleep()`으로 대기하지 않는다(Explicit Wait만 사용,
  `AUTOMATION_GUIDE.md` 7절).
- `automation/` Python 코드에서 Full XPath(`/html/body/div[1]/...`)를 사용하지 않는다
  (`AUTOMATION_GUIDE.md` 6.1절).
- Page 클래스(`*Page`)에 Assertion을 작성하지 않는다 — Assertion은 Test 함수(`test_*`)에서만
  수행한다(`AUTOMATION_GUIDE.md` 4절).
- `.env`, `service-account*.json`, `*-credentials.json`, `credentials.json` 파일을 커밋하지
  않는다(`.gitignore`에 이미 등록됨). 커밋 전 변경 파일에 민감정보가 없는지 확인한다.
- PRD에 없는 요구사항/기대 동작을 TC나 Roadmap에서 임의로 새로 만들지 않는다.
- 한 Agent가 다른 Agent의 담당 범위(각 Agent 정의 파일의 "다른 단계는 이 에이전트의 책임
  범위가 아닙니다" 절 참조)에 해당하는 산출물을 대신 생성하지 않는다.
- 현재 작업 단계의 다음 단계 산출물을 미리 만들지 않는다(예: TC 작성 중 Roadmap이나 자동화
  코드를 먼저 만들지 않음).

---

## 7. AI 의사결정 기준 (모호한 상황)

- 상위 산출물(PRD/TC/Roadmap) 간 내용이 충돌하면: 임의 선택 금지 → 2절 Source of Truth 표로
  우선순위 확인 → 그래도 판단 불가하면 사용자에게 충돌 내용을 보고하고 확인 후 진행.
  (예외: 자동화 코드 "작성 방식"에 대한 판단은 항상 `AUTOMATION_GUIDE.md`가 최우선이며, 다른
  문서와 비교할 필요 없이 바로 따른다.)
- 새 파일을 어디에 만들지 애매하면: 3절 디렉터리 규칙을 먼저 확인 → 대응 항목이 없으면 임의
  생성하지 않고 사용자에게 배치 위치를 제안·확인.
- Requirement ID, Priority, Automation Score 등 판단 근거가 부족하면 추측으로 확정하지 않고
  사용자에게 확인한다(각 Skill 문서의 해당 절 참조).
- 테스트 실패 원인이 불명확하면 임의로 PASS 처리하거나 추측하지 않고, CLAUDE.md 13절의 4개
  범주(Automation Code / Test Data / Test Environment / 실제 Product 문제) 중 하나로
  구분을 시도한 뒤 불명확하면 사용자에게 보고한다.

---

## 변경 이력

| 날짜 | 변경 사유 |
|---|---|
| 2026-09-15 | Windows 로컬 환경 대응. macOS 절대경로 제거, `scripts/setup`·`docs/setup` 배치 규칙 및 CI 생성 완료 상태 반영. |
| 2026-08-27 | 최초 작성. 저장소 실제 구조(`docs/`, `.claude/agents`, `.claude/skills`,
`scripts/sheets_sync`) 및 `CLAUDE.md`/`AUTOMATION_GUIDE.md`/각 Skill 문서 분석 기반. |
