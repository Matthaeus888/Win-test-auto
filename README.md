

Claude Code를 활용해 요구사항 정의부터 CI 결과 알림까지 QA 프로세스 전체를, 중요한
의사결정 지점(자동화 대상 선정, Commit, Push)에서는 사람의 승인을 유지한 채 자동화하는
프로젝트입니다.

대상 서비스는 이커머스 연습 사이트 [automationexercise.com](https://automationexercise.com/)이며,
Selenium + pytest + Page Object Model 기반으로 자동화 테스트를 구현합니다.

## 프로젝트 목표

- 반복적인 QA 작업(TC 작성, 자동화 코드 구현, 테스트 실행, 리포팅)의 자동화
- 요구사항 → 산출물 → 코드 → 실행 결과 간의 추적성 확보
- 자동화 대상 선정, Commit, Push 등 중요한 의사결정 지점에서 사용자 통제권 유지

## QA 자동화 워크플로우

```
1. 요구사항 기반 PRD 작성
2. PRD 기반 전체 기능 Test Case 생성
3. 사용자가 TC를 검토하고 자동화 대상 선정        (사용자 승인)
4. 선정된 자동화 TC 기반 개발 Roadmap 작성
5. Roadmap 기반 테스트 자동화 코드 구현
6. 자동화 테스트 실행 및 결과 검증
7. 코드 리뷰
8. Git Commit                                   (사용자 승인)
9. Git Push                                     (사용자 승인)
10. GitHub Actions 기반 CI 실행
11. CI 결과를 Slack으로 알림
```

각 단계의 상세 원칙은 [`CLAUDE.md`](./CLAUDE.md)에 정의되어 있습니다.

## 디렉터리 구조

```
qa-process/
├── docs/
│   ├── prd/                        # Project/Feature PRD
│   │   └── feature/
│   ├── tc/                         # Test Case, Feature별 자동화 대상 선정 결과
│   │   └── automation-candidates/
│   ├── roadmap/ROADMAP.md          # 자동화 개발 Roadmap 및 진행 현황
│   └── automation/AUTOMATION_GUIDE.md  # 자동화 코드 개발 기준 (Source of Truth)
├── automation/                     # 자동화 테스트 코드
│   ├── pages/                      # Page Object (화면별 1클래스, BasePage 상속)
│   ├── tests/                      # pytest 테스트 (Assertion 전담)
│   ├── config/                     # Base URL, 계정 등 환경 설정
│   ├── utils/                      # 화면과 무관한 공통 로직
│   ├── test_data/                  # 정적 테스트 데이터
│   ├── conftest.py                 # WebDriver fixture, 실패 시 스크린샷 hook
│   ├── screenshots/, reports/      # 실행 산출물 (git 미추적)
│   └── requirements.txt, pytest.ini
├── scripts/
│   ├── notify_slack/               # CI 실패 시 Slack Webhook 알림 스크립트
│   ├── setup/                      # Windows 로컬 환경 세팅 스크립트 (환경/MCP/Git/검증)
│   └── sheets_sync/                # TC 작성 Agent용 Google Sheets 연동 모듈
├── .github/workflows/ci.yml        # GitHub Actions CI 워크플로우
├── .claude/agents/, .claude/skills/  # Sub Agent / Skill 정의
└── CLAUDE.md                       # 프로젝트 최상위 지침
```

## 로컬 환경 세팅 (Windows)

저장소를 처음 받은 PC에서는 아래 스크립트로 실행 환경 · AI Agent(MCP) · Git · CI 연결을
순서대로 준비합니다. 자세한 절차는 [`docs/setup/WINDOWS_SETUP.md`](./docs/setup/WINDOWS_SETUP.md)를
참고하세요.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup\1-setup-env.ps1    # Python/.venv/의존성/.env
powershell -ExecutionPolicy Bypass -File scripts\setup\2-setup-mcp.ps1    # playwright / shrimp MCP 연결
powershell -ExecutionPolicy Bypass -File scripts\setup\3-setup-git.ps1    # git init + GitHub 원격 연결
powershell -ExecutionPolicy Bypass -File scripts\setup\4-verify.ps1       # 테스트 실행으로 동작 확인
```

commit과 push는 스크립트가 임의로 수행하지 않고 실행 중 사용자 확인을 받습니다(`CLAUDE.md` 14·18절).

## 자동화 테스트 실행 (로컬)

```bash
cd automation
pip install -r requirements.txt
cp .env.example .env   # ACTEST1~3_PASSWORD 값을 채운 뒤 사용 (git에 커밋하지 않음)

pytest tests/                                        # 전체 실행
pytest tests/test_login.py                            # 파일 단위 실행
pytest tests/test_cart.py::test_add_to_cart_shows_modal  # 단일 테스트 실행
```

리포트는 `automation/reports/`(HTML + JUnit XML), 실패 시 스크린샷은
`automation/screenshots/`에 저장됩니다(둘 다 git 미추적).

## CI/CD

`.github/workflows/ci.yml`(GitHub Actions)이 아래 조건에서 `automation/tests/` 전체를
headless Chrome으로 실행합니다.

- `master` 브랜치 push 시
- 매일 한국시간(KST) 오전 9시 스케줄 실행
- GitHub Actions 탭에서 수동 실행(workflow_dispatch)

실행 결과(HTML 리포트 + JUnit XML + 실패 스크린샷)는 Artifact로 업로드되며, 테스트 실패
시에만 `scripts/notify_slack/notify.py`가 실패한 테스트의 파일:라인과 에러 메시지를 요약해
Slack Webhook으로 알립니다.

## 기술 스택

| 항목 | 선택 |
|---|---|
| 언어 | Python (자동화 코드 한정 PEP8 예외: 4칸 들여쓰기, snake_case) |
| 자동화 도구 | Selenium WebDriver |
| 테스트 러너 | pytest |
| 설계 패턴 | Page Object Model |
| 리포팅 | pytest-html + JUnit XML |
| CI/CD | GitHub Actions |
| 알림 | Slack (CI 결과 알림 전용) |

## 주요 문서

- [`CLAUDE.md`](./CLAUDE.md) — 프로젝트 전체 워크플로우 및 원칙 (Source of Truth 최상위)
- [`docs/prd/project-prd.md`](./docs/prd/project-prd.md) — Project PRD
- [`docs/roadmap/ROADMAP.md`](./docs/roadmap/ROADMAP.md) — 자동화 개발 Roadmap 및 진행 현황
- [`docs/automation/AUTOMATION_GUIDE.md`](./docs/automation/AUTOMATION_GUIDE.md) — 자동화 코드 개발 기준
- [`docs/setup/WINDOWS_SETUP.md`](./docs/setup/WINDOWS_SETUP.md) — Windows 로컬 환경(AI Agent/Git/CI) 세팅 절차

## 진행 현황

Feature Phase 1~7(로그인/로그아웃, 회원가입/계정삭제, 상단 네비게이션, 상품 검색, 장바구니,
상품 상세, 페이지별 UI — Approved TC 76건)과 Phase Final(GitHub Actions CI + Slack 알림
연동)까지 구현이 완료되어 있습니다. 상세 진행 이력은
[`docs/roadmap/ROADMAP.md`](./docs/roadmap/ROADMAP.md) 9절을 참고하세요.
