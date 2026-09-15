---
문서유형: Automation Guide
상태: 승인완료
참고: refer_CLAUDE.md(타 프로젝트 개발 규칙) 구조를 참고하되, 규칙 내용은 본 프로젝트에서
      사용자와 별도로 확정한 결정 사항을 따름
최초 작성일: 2026-08-27
최근 변경일: 2026-09-02
승인일: 2026-08-27
---

# AUTOMATION_GUIDE.md - QA Process 자동화 코드 개발 기준

## 0. 문서 목적 및 범위

이 문서는 `qa-process` 프로젝트의 **자동화 코드 개발 기준**을 정의하는 Source of Truth이며,
다음 작업에서 공통 판단 근거로 사용합니다.

- 자동화 개발 Roadmap 작성
- Shrimp Task 생성 및 작업 분해
- 자동화 코드 개발
- 코드 리뷰 및 테스트 실행/검증

이 문서는 **기능별 요구사항(로그인, 장바구니 등)을 다루지 않습니다.** 기능별 요구사항은
`docs/prd/feature/{slug}.md`(Feature PRD)와 `docs/tc/{slug}.md`(TC)를 Source of Truth로
합니다. 이 문서와 PRD/TC/Roadmap의 내용이 서로 다르게 보이면, 요구사항·시나리오 판단은 항상
PRD/TC를 기준으로 하고, **코드 작성 방식(구조/컨벤션/원칙)에 대한 판단만 이 문서를 기준으로**
합니다.

**아직 실제 코드, 디렉터리, 설정 파일은 생성되지 않았습니다.** 이 문서는 앞으로 자동화 코드를
작성할 때 따를 규칙을 정의하며, 이후 실제 구현 상태가 이 문서와 달라지면(CLAUDE.md 8절
"실제 구현 상태 = Repository Code" 원칙에 따라) 문서를 갱신합니다.

### 0.1 자동화 대상 범위

이 문서가 정의하는 규칙이 적용되는 자동화 대상은 다음 조건을 **모두** 만족하는 TC로 한정합니다
(`automation-candidate-agent`가 정의한 조건과 동일).

```
Candidate 문서(docs/tc/automation-candidates/{slug}.md) 상태 = 자동화대상확정
AND
QA Decision = Approved
```

2026-08-27 기준 대상 Feature와 Approved TC 건수는 다음과 같습니다(상세 TC 목록은 각
Candidate 문서를 Source of Truth로 참조하며, 이 문서에 전체 TC를 복제하지 않습니다).

| Feature | Approved TC 수 |
|---|---|
| cart | 13 |
| login-logout | 11 |
| page-ui | 21 |
| product-detail | 6 |
| product-search | 7 |
| signup-delete-account | 11 |
| top-navigation | 6 |

이 범위는 프로젝트마다 달라질 수 있으므로, 이 문서의 원칙 자체는 특정 Feature 목록에 종속되지
않고 재사용 가능하게 작성합니다.

---

## 1. Technology Stack

| 항목 | 결정 | 비고 |
|---|---|---|
| 언어 | **Python** | 1.1절 "코딩 스타일 예외" 적용 대상 |
| 자동화 도구 | **Selenium WebDriver** | |
| 테스트 러너 | **pytest** | |
| 설계 패턴 | **Page Object Model (POM)** | |
| 리포팅 | **pytest-html + JUnit XML(`--junitxml`) 병행** | HTML은 사람이 보는 Artifact, JUnit XML은 Slack 실패 메시지 조립용 |
| 실행 브라우저 | **Chrome (ChromeDriver)** | Project PRD 테스트 환경(Chrome) 기준 |
| 대상 환경 | Production 단일 환경 (`https://automationexercise.com/`) | 별도 dev/staging 없음(Project PRD 3절) |
| CI/CD | **GitHub Actions** | Push 시 자동 테스트 실행(16절) |
| 알림 | **Slack** | 실패 시 실패 원인 요약 포함 알림(CLAUDE.md 16절: 승인 용도 아님, 결과 알림 전용) |
| 패키지 버전 관리 | `requirements.txt` (미생성) | 실제 구현 시작 시 작성 |

### 1.1 코딩 스타일 예외 (중요)

프로젝트 전역 CLAUDE.md는 "들여쓰기 2칸, camelCase/PascalCase(컴포넌트)"를 기본 스타일로
정의하지만, **Python 자동화 코드에 한해 다음과 같이 PEP8을 우선 적용하는 예외를 사용자
승인(2026-08-27)으로 확정합니다.**

- 들여쓰기: **4칸** (2칸 아님)
- 변수/함수명: **snake_case** (camelCase 아님)
- 클래스명: PascalCase (전역 규칙과 동일, 충돌 없음)
- 상수(Locator 등): UPPER_SNAKE_CASE

이유: `black`/`flake8` 등 Python 표준 도구 체인이 4칸 들여쓰기와 PEP8 네이밍을 전제로 하고,
Selenium/표준 라이브러리 API 자체가 snake_case이므로 일관성을 위해 예외를 인정합니다. 이
예외는 **이 프로젝트의 Python 자동화 코드에만 적용**되며, PRD/TC/Roadmap 등 Markdown
문서나 다른 언어로 작성될 도구(`scripts/sheets_sync`의 기존 코드 포함)의 컨벤션까지 바꾸는
것은 아닙니다.

---

## 2. Automation Architecture

- **Page Object Model (POM)**을 채택합니다. 1개 웹 페이지(또는 명확히 구분되는 주요 화면
  영역)당 1개 Page 클래스를 작성합니다.
- 모든 Page 클래스는 공통 기능을 제공하는 `BasePage`를 상속합니다.
- Page 객체는 WebDriver 인스턴스 1개만 보유하며, 그 외 상태 변수를 최소화합니다.
- Page Layer와 Test Layer의 책임은 4절 기준을 따릅니다.

---

## 3. Project Structure (예정)

**아래 구조는 아직 생성되지 않은 예정 구조입니다.** 실제 구현을 시작하는 시점에 이 구조에 맞춰
생성합니다.

```
qa-process/
├── automation/
│   ├── pages/               # Page Object 클래스
│   │   ├── base_page.py
│   │   └── ...
│   ├── tests/                # 테스트 코드 (pytest)
│   │   ├── test_login.py
│   │   └── ...
│   ├── utils/                 # 화면과 무관한 공통 로직
│   ├── config/                 # 환경 설정(URL, 타임아웃 등)
│   ├── test_data/               # 정적 테스트 데이터(계정 이메일 등, 비밀번호 제외)
│   ├── screenshots/               # 실패 시 스크린샷(git 미추적)
│   ├── reports/                     # pytest-html/JUnit XML 리포트(git 미추적)
│   ├── conftest.py                   # pytest fixture
│   ├── pytest.ini                     # pytest 설정
│   └── requirements.txt                # Python 의존성
├── docs/                                # 기존 산출물(PRD/TC/Roadmap/Automation Guide)
├── scripts/sheets_sync/                  # 기존 Google Sheet 연동 스크립트(자동화 코드와 별개)
└── .github/workflows/                      # CI 워크플로우(미생성)
```

- `automation/` 하위 구조는 이 프로젝트의 자동화 코드 전용이며, 기존 `scripts/sheets_sync`
  (QA 프로세스 도구 스크립트)와는 목적이 다르므로 혼용하지 않습니다.
- 실제 디렉터리를 만들 때 위 구조와 다르게 조정해야 할 이유가 생기면, 이 문서를 먼저 갱신하고
  사용자 확인을 받은 뒤 반영합니다(CLAUDE.md 7절).

### 3.1 Import 경로 규칙

`automation/pytest.ini`가 저장소 루트가 아닌 `automation/` 디렉터리 안에 위치하고
`automation/` 자체에는 `__init__.py`가 없으므로, `automation/tests/`를 pytest로 실행하면
`automation/`이 사실상의 루트 패키지 경로가 된다(`automation`을 top-level 패키지로 인식하지
않음, 실측 확인됨 — 2026-08-27 Phase 0 Task 4).

- 모든 `automation/` 하위 코드(Page Object, 테스트, utils, config, test_data 등)는
  **`automation.` prefix 없이** `automation/` 자체를 루트로 삼아 import한다.
  - 올바른 예: `from pages.base_page import BasePage`, `from config.settings import BASE_URL`
  - 잘못된 예(실행 시 `ModuleNotFoundError` 발생): `from automation.pages.base_page import BasePage`
- 이 규칙은 `automation/` 하위 코드 사이의 상호 import에만 적용된다. `automation/` 바깥
  코드(`scripts/sheets_sync` 등)에서 `automation/` 코드를 import하는 시나리오는 현재
  범위에 없다.

---

## 4. Page Object / Layer 책임

### 4.1 Page Layer 책임

- 대상 화면의 모든 Locator를 클래스 상단에 상수로 정의합니다.
- 클릭/입력/스크롤 등 화면 조작 메서드를 제공합니다.
- 조회 메서드는 값을 **반환만** 합니다.
- **Assertion을 절대 수행하지 않습니다.**

### 4.2 Test Layer 책임

- Page 객체의 메서드를 호출해 시나리오를 구성합니다.
- 테스트에 필요한 데이터를 준비/정리합니다(11절 참고).
- Page에서 반환받은 값과 기대값을 비교해 **Assertion을 수행**합니다.
- 원칙: Page는 "어떻게 하는가", Test는 "무엇을 검증하는가"만 담당합니다.

```python
# pages/login_page.py
class LoginPage(BasePage):
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.login-button")

    def login(self, email: str, password: str) -> None:
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)


# tests/test_login.py
def test_login_with_invalid_password(driver, login_page):
    login_page.login("actest1@test.com", "wrong-password")
    assert login_page.get_error_message() == "Your email or password is incorrect!"
```

---

## 5. 실제 페이지 탐색 규칙 (Playwright MCP 기반)

Selenium 코드를 작성하기 전 실제 페이지 구조와 Locator 후보를 조사·검증하는 개발 보조
도구로 **Playwright MCP**를 사용합니다(사용자 확정, 2026-08-27).

### 5.0 사전 준비 상태 (확인 완료)

**2026-08-27 기준으로 이 저장소/세션에 Playwright MCP 서버가 연결되어 있음을
확인했습니다**(`mcp__playwright__browser_snapshot`, `browser_evaluate`,
`browser_navigate` 등 도구 목록에서 확인됨). 이에 따라 아래 5.1~5.4 규칙을 실제
자동화 코드 작성 전 탐색 절차로 바로 적용할 수 있습니다. 서버 설정(설치/등록) 자체는
이 문서의 범위가 아닙니다.

### 5.1 사용 목적

- Playwright MCP는 Selenium 테스트 코드에 사용할 실제 페이지 구조와 Locator 후보를
  조사하고 검증하기 위한 **개발 보조 도구**로 사용합니다.
- 프로덕션 테스트 실행 도구는 **Selenium WebDriver**이며, Playwright MCP를 Selenium
  코드 실행 대신 사용하지 않습니다.

### 5.2 기본 탐색 순서

Selenium 코드를 작성하기 전에 다음 순서로 실제 페이지를 확인합니다.

1. 대상 기능의 Feature PRD(`docs/prd/feature/{slug}.md`)와 TC(`docs/tc/{slug}.md`)
   시나리오를 먼저 확인합니다.
2. Playwright MCP로 대상 페이지(`https://automationexercise.com/`)에 접근합니다.
3. `browser_snapshot`으로 페이지 구조와 대상 요소를 먼저 확인합니다.
4. snapshot만으로 정보가 부족하면 `browser_evaluate`로 DOM 속성을 확인합니다.
5. 확인한 정보를 기반으로 6절 우선순위에 따라 Selenium Locator를 작성합니다.
6. 작성한 Locator가 실제 대상 요소를 고유하게 식별하는지(동일 조건에 일치하는 요소가
   1개뿐인지) 검증합니다.

### 5.3 browser_evaluate 사용 기준

`browser_evaluate`는 다음 정보가 snapshot에서 충분히 확인되지 않을 때만 사용합니다.

- id, name, role, aria-label, placeholder
- data-testid 등 data-* 속성(실제 존재가 확인되는 경우에 한함)
- 대상 요소의 텍스트
- 상위·하위 DOM 관계
- 동일 조건에 일치하는 요소 개수

**금지**: 페이지 상태를 변경하거나 서비스 데이터를 조작하기 위한 JavaScript 실행(실제 계정
생성/삭제, 주문 시도 등)에는 사용하지 않습니다. Playwright MCP는 오직 **조회·탐색** 목적에만
한정하며, 승인되지 않은 Production 데이터 변경은 CLAUDE.md 11절 원칙을 그대로 따릅니다.

### 5.4 사용자 확인 요청 기준

다음 사유로 Playwright MCP를 이용한 직접 확인이 불가능한 경우에만 사용자에게 스크린샷이나
추가 정보를 요청합니다.

- 로그인 계정이나 권한이 없음
- OTP, 2FA 또는 CAPTCHA가 필요함
- 사내망이나 특정 네트워크 환경이 필요함
- 사용자별 데이터가 있어야 재현 가능함
- MCP 브라우저와 실제 테스트(Selenium) 환경이 다르게 동작함
- 대상 요소나 요구사항이 여러 의미로 해석될 수 있음

단순히 Locator가 제공되지 않았다는 이유만으로 작업을 중단하지 않습니다.

---

## 6. Locator 작성 원칙

### 6.1 우선순위

1. `id` 속성
2. `data-qa` 속성(테스트 전용 속성, 존재가 확인된 화면에 한함 — 아래 실측 근거 참고)
3. `name` 속성
4. 안정적인 CSS Selector(구조 변경에 덜 민감한 속성 기반)
5. 상대 XPath (텍스트/속성 결합 등 다른 방법으로 고유 식별이 어려울 때만, 최후 수단)

**Full XPath(`/html/body/div[1]/...`)는 절대 금지**합니다 — DOM 구조 변경에 매우 취약해
유지보수가 불가능합니다.

> 최초 작성 시점(2026-08-27)에는 `automationexercise.com`이 `data-testid` 같은 테스트
> 전용 속성을 제공하지 않는다고 보아 참고 프로젝트(`refer_CLAUDE.md`)의 "data-* 속성"
> 우선순위 단계를 제외했었습니다. 이후 Phase 1 Task 2(LoginPage 구현, 2026-08-29)에서
> automation-developer-agent가 Playwright MCP로 `/login` 페이지(로그인 폼 + 회원가입 폼)를
> 실측한 결과 `data-qa` 속성(예: `data-qa="login-email"`, `data-qa="login-password"`,
> `data-qa="login-button"`, `data-qa="signup-name"`, `data-qa="signup-email"`,
> `data-qa="signup-button"`)이 실제로 존재하며, 특히 `name="email"`이 같은 페이지 내
> 로그인/회원가입 두 폼에 중복 존재해 `name` 단독으로는 고유 식별이 불가능한 반면
> `data-qa`는 두 폼 사이에서 겹치지 않는 고유값임을 확인했습니다. 이에 따라 위 5절 원칙대로
> 우선순위를 갱신했습니다(사용자 승인, 2026-08-29). `data-qa`가 확인되지 않은 화면 요소는
> 이 우선순위를 적용할 수 없으므로 그대로 3순위(`name`)부터 적용합니다.

### 6.2 정의 위치

모든 Locator는 Page 클래스 상단에 `UPPER_SNAKE_CASE` 상수로 정의합니다. 메서드 내부에
Locator를 하드코딩하지 않습니다.

---

## 7. Wait 처리 원칙

- **`time.sleep()` 사용을 금지**합니다. 고정 시간 대기는 테스트를 느리고 불안정하게 만듭니다.
- Selenium의 `WebDriverWait` + `expected_conditions`로 **Explicit Wait**를 기본으로
  사용합니다.
- 반복되는 Wait 로직은 `BasePage`의 공통 메서드로 래핑합니다(예: `wait_and_click`,
  `wait_and_get_text` 등 — 실제 메서드명은 구현 시 확정).

### 7.1 광고 오버레이(Ad Overlay) 처리 (2026-08-30 추가)

`automationexercise.com`은 Production 단일 환경이며, 사이트 자체가 아닌 제3자(Google
Ads) 네트워크가 페이지 진입 시 **무작위로** 전면 광고 오버레이(Google Vignette 등,
화면 전체를 덮고 "Close" 컨트롤이 있는 모달)를 주입하는 것이 사용자 제보 스크린샷
(2026-08-30)으로 확인되었습니다. 이 광고 콘텐츠 자체는 Project PRD "8. 기타
제약사항" 및 각 TC 문서 공통 Preconditions에 따라 **검증 대상이 아니지만**, 실제
클릭/입력을 가로막아 자동화 테스트를 실패시킬 수 있습니다.

- **처리 위치**: `BasePage`가 `_dismiss_ad_overlay_if_present()` 공통 메서드를
  제공하며, `click()`과 `type_text()` 시작 시점에 자동으로 호출됩니다. 오버레이가
  떠 있으면 "Close" 컨트롤을 클릭해 닫고, 없으면(대부분의 경우) 짧은 타임아웃
  (1.5초) 후 조용히 통과합니다.
- **모든 Page Object가 자동으로 적용받음**: `BasePage`를 상속하기만 하면 별도 구현
  없이 이 방어 로직이 적용됩니다. 새로운 Page Object를 작성할 때 광고 처리 로직을
  **개별적으로 추가하지 마십시오** — 이미 `BasePage.click()`/`type_text()`를
  사용하는 것만으로 충분합니다.
- **Locator 예외 사항**: 광고 DOM은 제3자가 매번 다르게 주입해 Playwright MCP로
  사전에 결정적으로 재현·검증할 수 없으므로, 5절의 "실제 페이지 탐색 절차"는 이
  Locator(`BasePage.AD_OVERLAY_CLOSE_BUTTON`)에는 예외적으로 적용하지 않으며, 화면에
  노출되는 "Close" 텍스트 기반의 최선(best-effort) 탐색을 사용합니다. 광고 마크업이
  바뀌어 이 Locator가 더 이상 동작하지 않게 되면 `BasePage` 한 곳만 수정하면
  됩니다(모든 Page Object에 공통 적용).
- **성능 트레이드오프**: 오버레이가 없는 일반적인 경우에도 매 `click()`/`type_text()`
  호출마다 최대 1.5초의 짧은 대기가 추가됩니다(사용자 승인 완료, 안정성을 우선).
  `get_text()`/`is_element_visible()`/`find_element()`처럼 호출 빈도가 높은 조회
  전용 메서드에는 적용하지 않습니다(Selenium이 occlusion을 검사하지 않아 실질적
  차단 위험이 낮고, 성능 비용 대비 효익이 낮기 때문).

---

## 8. Assertion 원칙

- Assertion은 **Test Layer에서만** 수행합니다(4.1절과 연결).
- pytest의 `assert`를 사용하며, 실패 메시지에 **기대값과 실제값을 모두 포함**합니다.

```python
assert actual_count == expected_count, f"Expected {expected_count}, but got {actual_count}"
```

---

## 9. Fixture 원칙

- WebDriver 생성/종료는 `conftest.py`의 fixture로 관리하며, `yield` 패턴으로 테스트 종료 후
  리소스 정리(`driver.quit()`)를 보장합니다.
- 기본 `scope`는 **`function`**으로 설정해 테스트마다 새 WebDriver를 생성합니다(10절 테스트
  독립성과 직결).
- 자주 쓰이는 Page 객체도 fixture로 제공해 테스트 코드의 반복을 줄입니다.

```python
@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)
```

---

## 10. 테스트 독립성

- 각 테스트는 **단독 실행 가능**해야 하며, 다른 테스트의 실행 순서에 의존하지 않습니다.
- 각 테스트는 스스로 필요한 상태(로그인 등)를 셋업합니다.
- 테스트가 생성한 데이터(회원가입으로 만든 계정 등)는 가능한 범위에서 해당 테스트 내에서
  정리합니다(11절 데이터 관리 원칙과 연결).
- 이 원칙은 CLAUDE.md 10절 "Isolated/Reproducible/Idempotent" 원칙을 자동화 코드 수준에서
  구체화한 것입니다.

---

## 11. 테스트 데이터 관리

이 프로젝트는 dev/staging 없이 **Production 단일 환경**이고, 로그인에 재사용할 고정 계정
3개(`actest1~3@test.com`)와, 회원가입/계정삭제처럼 계정 자체를 생성·삭제하는 시나리오가
공존합니다. 이 특성을 반영해 **하이브리드 방식**을 채택합니다(사용자 승인 완료).

### 11.1 고정 계정 재사용 (로그인 상태가 필요한 시나리오)

- 로그인/로그아웃, 장바구니, 상품 상세 등 "이미 존재하는 계정으로 로그인"이 필요한 TC는
  사전 준비된 계정 3개를 재사용합니다.
- 계정 **이메일**은 `test_data/accounts.json` 등 설정 파일로 관리합니다.
- 계정 **비밀번호**는 어떤 파일에도 하드코딩하지 않고 `.env`(환경변수)로만 관리합니다
  (12절 참고).

### 11.2 동적 생성 (계정을 생성/삭제하는 시나리오)

- 회원가입, 계정삭제 TC처럼 매 실행마다 신규 계정이 필요한 경우, `utils`의 Factory 함수로
  임의 이메일을 동적 생성합니다(예: `f"test_{uuid.uuid4().hex[:8]}@example.com"`).
- 이렇게 하면 고정 계정이 삭제 테스트로 소모되는 사고를 방지하고, Production 데이터 오염을
  최소화할 수 있습니다(CLAUDE.md 11절 "테스트 간 데이터 오염과 의존성 최소화").
- 생성한 계정을 테스트 내에서 정리(삭제)할 수 있는 경우, 가능한 범위에서 정리합니다.

### 11.3 공통 원칙

- 테스트 데이터를 코드에 직접 하드코딩하지 않습니다.
- Production 데이터(실제 사용자 데이터 등)를 생성/수정/삭제하는 작업은 CLAUDE.md 11절에
  따라 사용자의 명시적 승인 없이 수행하지 않습니다. 여기서 다루는 "계정 생성/삭제"는 TC에서
  이미 승인된 테스트 목적의 계정에 한정합니다.

---

## 12. 환경변수 및 민감정보 관리

- 비밀번호 등 민감정보는 코드에 절대 작성하지 않고 환경변수로 관리합니다
  (`python-dotenv` + `.env`).
- `.env`는 `.gitignore`에 포함해 git에 커밋되지 않도록 합니다(이미 프로젝트
  `.gitignore`에 `.env` 규칙이 존재하며, 자동화 코드용 변수도 동일한 방식을 따릅니다).
- CI(GitHub Actions) 환경에서는 GitHub Secrets로 관리합니다(CLAUDE.md 17절과 동일).
- 로그, 리포트(HTML/JUnit XML), 실패 스크린샷 어디에도 비밀번호 등 민감정보가 노출되지
  않도록 합니다.

---

## 13. Logging

- `print()` 대신 Python 표준 `logging` 모듈을 사용합니다.
- 로그 레벨 기준:
  - `DEBUG`: Locator 탐색, 요소 상태 등 상세 진단 정보
  - `INFO`: 로그인, 페이지 이동, 클릭 등 주요 액션
  - `WARNING`: 재시도, 느린 응답 등
  - `ERROR`: 예외 발생, 요소를 찾지 못함 등
  - `CRITICAL`: 드라이버 크래시 등 심각한 오류
- 비밀번호 등 민감정보는 로그에 마스킹 처리합니다.
- 로그 저장 경로/포맷/로테이션 방식은 실제 구현 시 확정합니다(현재 미정).

---

## 14. 실패 시 Screenshot / Artifact

- pytest hook(`pytest_runtest_makereport`)을 이용해 테스트 **실패 시에만** 자동으로
  스크린샷을 캡처합니다.
- 파일명 규칙: `{테스트_함수명}_{상태}_{YYYY-MM-DD_HH-MM-SS}.png`
- 저장 위치: `automation/screenshots/`(git 미추적)
- 스크린샷에 민감정보(비밀번호 입력값 등)가 노출되지 않도록 주의합니다.
- CI 실행 시 실패 스크린샷과 리포트(pytest-html, JUnit XML)는 GitHub Actions Artifact로
  업로드해 사후 확인이 가능하도록 합니다(16절 CI/CD와 연결, 실제 워크플로우 파일은 별도
  단계에서 작성 — CLAUDE.md 15절).

---

## 15. Exception Handling

- 프로젝트 전역 CLAUDE.md "에러 핸들링 필수" 원칙을 자동화 코드에서는 다음과 같이
  구체화합니다.
- 불필요하게 광범위한 `except Exception:` 처리를 지양하고, Selenium이 실제로 발생시키는
  구체적 예외(`TimeoutException`, `NoSuchElementException` 등)를 명시적으로 처리합니다.
- 예외 발생 시 반드시 로그를 남겨(`logger.error(...)`) 이후 디버깅이 가능하게 합니다.
- 예외를 조용히 삼키지 않습니다(로깅 없이 `pass` 처리 금지).

---

## 16. CI/CD

- GitHub Actions를 사용하며, **GitHub Push 시 자동으로 자동화 테스트가 실행**됩니다.
- 실행 흐름(CLAUDE.md 15절과 동일): `Git Push → GitHub Actions → 자동화 테스트 실행 →
  Test Report 생성 → 결과 판정 → Slack Notification`
- **실패 시 Slack 알림에는 어떤 부분(테스트/Feature)에서 실패했는지 알 수 있는 정보를
  포함**합니다. JUnit XML 결과를 파싱해 실패한 테스트 이름과 사유 요약을 메시지에 포함하는
  방식을 사용합니다(1절 리포팅 결정과 연결).
- 이 문서는 CI **운영 원칙**만 정의하며, 실제 GitHub Actions Workflow(YAML) 파일과 Slack
  연동 스크립트는 별도 구현 단계에서 작성합니다(CLAUDE.md 15절과 동일한 범위 제한).
- Slack은 결과 알림 전용이며 Commit/Push 승인 용도로 사용하지 않습니다(CLAUDE.md 16절).

---

## 17. Coding Convention

- 1.1절의 "코딩 스타일 예외"에 따라 **PEP8**을 기준으로 합니다.
  - 들여쓰기: 4칸
  - 한 줄 최대 길이: 100자 권장
  - 타입힌트를 함수 파라미터/반환값에 권장(가독성 확보)
- 주석은 프로젝트 전역 CLAUDE.md에 따라 **한국어**로 작성합니다.
- 변수명/함수명은 영어를 사용합니다(전역 CLAUDE.md "변수명/함수명: 영어" 원칙 유지, 표기법만
  1.1절 예외에 따라 snake_case).

---

## 18. Naming Convention

| 대상 | 규칙 | 예시 |
|---|---|---|
| 파일명 | snake_case | `login_page.py`, `test_login.py` |
| 클래스명 | PascalCase | `LoginPage`, `BasePage` |
| Page 객체 클래스 | `Page` 접미사 필수 | `LoginPage` (O), `Login` (X) |
| 메서드명 | snake_case, 동사로 시작 | `click_login_button`, `get_error_message` |
| 테스트 함수명 | `test_` 접두사 | `test_login_with_valid_credentials` |
| 변수명 | snake_case | `search_keyword`, `product_count` |
| 상수(Locator 등) | UPPER_SNAKE_CASE | `LOGIN_BUTTON`, `EMAIL_INPUT` |

---

## 19. 공통 코드 분리 기준

- **2회 이상 반복**되는 코드는 공통 메서드/함수로 분리합니다(CLAUDE.md 12절 "불필요한 중복
  구현 금지"와 연결).
- **BasePage**: 모든 Page에서 필요한 공통 화면 조작(요소 찾기, 클릭, Wait 래핑 등).
- **utils**: 화면과 무관한 순수 로직(랜덤 데이터 생성, 문자열/날짜 처리 등).
- 특정 Feature 하나에서만 쓰이는 로직을 섣불리 공통화하지 않습니다(과도한 추상화 지양).

---

## 20. 테스트 실행 및 검증

### 20.1 테스트 실행 범위와 시점 (2026-08-31 명확화)

개발 Roadmap의 Phase 진행 과정에서 테스트를 "언제, 어느 범위까지" 실행할지를 3단계로
구분합니다. 범위를 넓게 잡을수록(특히 전체 통합테스트) 실행 시간이 길고 제3자 광고 등
Test Environment 요인에 따른 불안정성(7.1절, 22절)에 노출될 여지도 커지므로, 아래처럼
시점을 명확히 구분해 불필요한 반복 실행을 피합니다.

1. **Phase 내부, 코드 작성 단위(Task)마다**: Page Object 메서드나 테스트 함수를 새로
   작성/수정할 때마다, 그 범위에 해당하는 테스트를 즉시 실행해 동작을 검증합니다. 실행 없이
   "완료"로 간주하지 않습니다(CLAUDE.md 13절과 동일).
   ```bash
   # 예: 이번에 작성/수정한 테스트 함수 하나만 pytest 노드 ID로 지정해 실행
   # (`-k`는 테스트 함수명을 대상으로 매칭하므로, TC ID가 아니라 실제 함수명을 지정한다.
   # TC ID와 함수명의 대응 관계는 각 테스트 함수의 docstring에 기록되어 있다.)
   pytest automation/tests/test_cart.py::test_repeated_add_to_cart_accumulates_quantity_on_list_page
   ```
2. **Phase 코드 작성 완료 시**: 해당 Phase의 Approved TC 전체를 대상으로 pytest를
   실행해 PASSED/FAILED/ERROR를 확인합니다. 실행 범위는 **해당 Phase의 테스트 파일로
   한정**하며, 다른 Phase까지 포함한 전체 통합테스트는 이 시점에 진행하지 않습니다.
   ```bash
   # 예: Phase 5(cart) 완료 시 — cart Phase 범위로만 한정
   pytest automation/tests/test_cart.py --html=automation/reports/report_phase5.html --junitxml=automation/reports/results_phase5.xml
   ```
3. **전체 통합테스트(Full Regression)**: 개발 Roadmap상 모든 Feature Phase의 코드
   작성이 완료된 이후, CI/CD 연동 Phase(Phase Final) 착수 직전 시점에 **1회만** 진행합니다.
   그 이전 개별 Phase 완료 시점마다 반복적으로 전체 통합테스트를 수행하지 않습니다.
   ```bash
   # 예: 모든 Feature Phase 완료 후, CI/CD Phase 착수 직전 1회
   pytest automation/tests/ --html=automation/reports/report_full.html --junitxml=automation/reports/results_full.xml
   ```

- 테스트 실패 시 원인을 CLAUDE.md 13절의 4가지 범주(Automation Code / Test Data / Test
  Environment / 실제 Product 문제) 중 하나로 구분하려고 시도하며, 원인이 불명확하면 추측으로
  결론 내리지 않고 사용자에게 보고합니다.
- 실패를 회피하기 위해 무한/반복적으로 재시도하지 않습니다.

---

## 21. 코드 작성 후 Self Review 체크리스트

코드 작성을 완료로 보고하기 전에 다음을 자체 점검합니다.

- [ ] `time.sleep()`을 사용하지 않았는가? (Explicit Wait 사용)
- [ ] Full XPath를 사용하지 않았는가?
- [ ] 모든 Locator가 Page 클래스 상단에 상수로 정의되어 있는가?
- [ ] Page Layer에 Assertion이 없는가?
- [ ] 모든 Page 클래스가 `BasePage`를 상속하는가?
- [ ] 각 테스트가 다른 테스트 실행 순서에 의존하지 않는가?
- [ ] 계정 정보/비밀번호가 코드에 하드코딩되지 않았는가?
- [ ] `print()` 대신 `logging`을 사용했는가?
- [ ] 예외를 광범위하게 처리하지 않고 구체적으로 처리·로깅했는가?
- [ ] 파일명(snake_case)/클래스명(PascalCase, `~Page` 접미사)/함수명(snake_case,
      동사 시작)/테스트 함수명(`test_` 접두사) 규칙을 지켰는가?
- [ ] 4칸 들여쓰기를 사용했는가?
- [ ] 코드 작성 후 실제로 pytest를 실행해 결과(PASSED/FAILED/ERROR)를 확인했는가?
- [ ] 실패 시 스크린샷이 저장되었는가?
- [ ] (Locator를 새로 작성한 경우) 5절 절차에 따라 Playwright MCP로 실제 페이지 구조를
      확인하고 Locator의 고유성을 검증했는가?

---

## 22. 알려진 Production 사이트 결함 (Known Site Defects)

이 절은 자동화 코드/Locator/Assertion 자체는 정상 동작하지만, `automationexercise.com`
Production 사이트 쪽 결함으로 인해 테스트가 실패(또는 실패할 수 있는)하는 사례를
기록합니다. CLAUDE.md 13절 "실제 Product 문제" 범주로 분류된 사례가 대상입니다.

이미 7.1절("광고 오버레이 처리")도 넓게 보면 Production 사이트 쪽 이슈에 대응하는
선례이지만, 광고 오버레이는 자동화 코드가 **매번 방어 로직으로 우회 처리**하는 사례이고
Wait 처리와 직접 관련되어 있어 원래 자리(7.1절)에 그대로 둡니다. 이 절에서는 중복
서술하지 않고 7.1절을 참고하도록 교차 참조만 남깁니다(→ 7.1절 참고).

### 22.1 `/logout` 세션 처리 결함 (2026-08-31 추가)

- **발견 경위**: Phase 4 회귀 확인 작업 중 `automation/tests/test_login.py::
  test_logout_via_direct_url`(TC-LOGIN-LOGOUT-015, Phase 1에서 이미 구현·검증되어
  커밋(`ae6ba0c`)·push된 테스트, 이번 조사 시점까지 자동화 코드는 전혀 변경되지
  않았음을 git log/diff로 확인)이 2026-08-31 15:46와 15:49 두 차례 재현 가능하게
  실패했다. 이후 별도로 3회 재실행했을 때는 0/3 실패로, 매번 재현되지는 않는
  **간헐적** 결함이다.
- **[2026-09-02 추가] CI(GitHub Actions, headless Chrome) 환경에서도 재현 확인**:
  Phase Final Task 5(실제 GitHub Actions 실행 검증) 중 Slack 알림 실전 테스트를
  위해 의도적 실패 테스트 1건을 포함해 push한 실행(run `33599258272`)에서, 의도한
  테스트 외에 `test_logout_via_direct_url`이 함께 실패했다. 실패 메시지가 로컬
  재현 사례와 동일(`/logout` 접근 후 Home 랜딩, 세션은 로그인 상태로 남음)해
  기존과 같은 결함으로 판단했다. 이로써 이 결함이 로컬(headed) 환경에 국한되지
  않고 GitHub Actions의 headless Chrome/CI 환경에서도 동일하게 재현됨을 처음으로
  확인했다 — 자동화 코드의 headless 분기(Task 1, `conftest.py`)나 CI 환경 자체의
  문제가 아니라 Production 사이트 `/logout` 엔드포인트 자체의 간헐적 결함이라는
  기존 결론을 재확인하는 근거다.
- **증상**: 실패 시점 스크린샷(아래 증거 파일 경로) 2장 모두에서 `/logout` 직접
  접근 후 Home으로는 정상 랜딩했지만, 상단 네비게이션에 "Logout / Delete Account /
  Logged in as 테스트1"이 로그인 상태 그대로 남아 있었다. 즉 서버 세션이 실제로는
  종료되지 않은 채 사용자에게는 Home 페이지가 그대로 응답되는 상태였다.
- **근거**: Playwright MCP(조회 전용)로 로그아웃되지 않은 상태에서
  `https://automationexercise.com/logout`에 직접 접근해 재확인한 결과 **HTTP 500**
  Django 에러 페이지가 노출됨을 확인했다.
  - `KeyError at /logout: 'user_id'`
  - `Exception Location: .../django/contrib/sessions/backends/base.py, line 72, in __delitem__`
  - `website/views.py, line 216, in logout: del request.session['user_id']`
  - 즉 사이트의 `/logout` 뷰가 세션에 `user_id` 키가 이미 없는 경우(중복 로그아웃,
    세션 만료 등 타이밍에 따라 발생 가능)를 예외 처리 없이 `del`로 접근해 서버
    측에서 크래시하는 결함이 실제로 존재한다.
- **결론/분류**: 자동화 코드/Locator/Assertion은 모두 의도한 대로 정확하게
  판정하고 있으며, 이는 CLAUDE.md 13절 기준 **"실제 Product 문제"**(Production
  사이트 `/logout` 엔드포인트의 세션 처리 결함)로 분류한다. Automation Code, Test
  Data, Test Environment 문제가 아니다.
- **관련 TC / 증거 파일**:
  - TC: `TC-LOGIN-LOGOUT-015` (`docs/tc/login-logout.md`)
  - 실패 스크린샷:
    `automation/screenshots/test_logout_via_direct_url_failed_2026-08-31_15-46-12.png`,
    `automation/screenshots/test_logout_via_direct_url_failed_2026-08-31_15-49-56.png`
  - 리포트: `automation/reports/results_full.xml`
- **대응 방침**:
  - 이 결함을 이유로 `test_logout_via_direct_url`의 Assertion을 완화하거나 실패를
    자동으로 우회 처리하지 않는다. 자동화 코드는 현재 Assertion을 그대로 유지한다.
  - 이 TC가 향후 다시 실패하면, 이 알려진 결함(간헐적 세션 처리 이슈)에 해당하는지를
    **우선 검토 대상으로 삼되**, 매번 자동으로 "알려진 이슈니까 PASS"로 간주하지
    않는다. 실제 원인이 매번 이 결함과 동일한지 스크린샷/응답 상태로 재확인하고,
    확인 전까지는 CLAUDE.md 13절 원칙에 따라 계속 실패(FAILED)로 보고한다.
  - 이 결함이 TC-015 자체의 시나리오나 Expected Result 재작성이 필요하다고
    판단되는 경우, 이 에이전트가 TC 문서를 직접 수정하지 않고 그 필요성만 사용자에게
    보고한 뒤 `tc-agent`로의 위임을 제안한다(CLAUDE.md 6절 역할 분리 원칙).
  - 사이트 자체의 결함(서버 코드 수정)은 이 프로젝트의 자동화 코드/문서 범위 밖이며
    별도 조치 대상이 아니다.

---

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-27 | 최초 작성. `refer_CLAUDE.md` 분석 및 사용자 확인(자동화 대상 범위, 언어/프레임워크,\
 데이터 관리, 리포팅, CI/CD 등)을 거쳐 초안 작성 및 즉시 사용자 승인. | 승인완료 |
| 2026-08-27 | 자동화 코드 작성 전 실제 페이지 구조를 확인할 개발 보조 도구가 필요해 "5. 실제\
 페이지 탐색 규칙" 절 신규 추가(사용자 요청). 이에 따라 5절 이후 절 번호를 전체 재정렬하고,\
 기존 절 번호 참조 오류 2건(2절의 "5절"→"4절", Fixture 절의 "9절"→"10절", Screenshot 절의\
 "15절"→"16절", Tech Stack 표의 "9절"→"16절")을 함께 수정. | 승인완료 |
| 2026-08-27 | 5절의 도구를 claude-in-chrome Skill에서 **Playwright MCP**로 변경(사용자\
 확정 — 이 프로젝트에서 Playwright MCP를 사용하기로 결정). 단, 2026-08-27 기준 이 세션에\
 Playwright MCP 서버가 아직 연결되어 있지 않음을 5.0절에 명시(실제 사용 전 서버 연결 확인\
 필요). | 승인완료 |
| 2026-08-27 | 5.0절 갱신: 이 세션 도구 목록에서 Playwright MCP 서버(`mcp__playwright__*`)\
 연결이 확인되어, "미연결" 상태를 "연결 확인 완료"로 수정(사용자 확인). | 승인완료 |
| 2026-08-27 | Phase 0 Task 4(conftest.py/config 작성) 구현 중 automation-developer-agent가\
 실제 pytest 실행으로 재현·확인한 사실을 반영해 "3.1 Import 경로 규칙" 절 신규 추가\
 (automation/pytest.ini 위치상 automation. prefix import가 실제로는 동작하지 않고\
 automation/을 루트로 삼는 import만 동작함, 사용자 승인 완료). | 승인완료 |
| 2026-08-29 | Phase 1 Task 2(LoginPage 구현) 중 automation-developer-agent가 Playwright MCP로\
 `/login` 페이지를 실측해 `data-qa` 속성이 실제로 존재함을 확인(로그인/회원가입 두 폼에서\
 `name="email"`이 중복되어 `name` 단독으로는 고유 식별 불가함도 함께 확인)한 사실을 반영해\
 6.1절 Locator 우선순위에 `data-qa`(2순위, id 다음 name 이전)를 추가(사용자 승인 완료). | 승인완료 |
| 2026-08-30 | 사용자가 automationexercise.com에서 간헐적으로 노출되는 광고 오버레이\
 스크린샷을 제보하고, 모든 페이지 진입 시 이를 감지해 "Close"로 닫은 뒤 본래 동작이\
 시작되도록 처리하고 앞으로의 모든 서브에이전트 코드 작업에 반영해달라고 요청함(사용자\
 승인). 이에 따라 "7.1 광고 오버레이(Ad Overlay) 처리" 절 신규 추가 —\
 `BasePage._dismiss_ad_overlay_if_present()`를 `click()`/`type_text()` 시작 시점에\
 호출하도록 구현했고(automation/pages/base_page.py), Phase 1(test_login.py 11건)/\
 Phase 2(test_signup.py 6건) 전체 재실행으로 회귀 없음을 확인했다. 새 Page Object는\
 `BasePage` 상속만으로 자동 적용되므로 개별 구현이 불필요함을 명시. | 승인완료 |
| 2026-08-31 | Phase 4 회귀 확인 중 발견된 TC-LOGIN-LOGOUT-015(`/logout` 세션 처리 결함)\
 재현 사례를 사용자 승인에 따라 알려진 Production 사이트 결함으로 신규 기록(22절 신설). | 승인완료 |
| 2026-08-31 | 사용자 요청에 따라 20절에 "20.1 테스트 실행 범위와 시점" 신설. 테스트 실행을\
 (1) Phase 내부 코드 작성 단위(Task)마다 관련 테스트 실행, (2) Phase 코드 작성 완료 시\
 해당 Phase 범위로 한정한 테스트 실행(다른 Phase를 포함한 전체 통합테스트는 이 시점에\
 진행하지 않음), (3) 전체 통합테스트는 개발 Roadmap상 모든 Feature Phase 완료 후 CI/CD\
 Phase(Phase Final) 착수 직전에 1회만 진행 — 3단계로 명확히 구분(사용자 승인). | 승인완료 |
| 2026-08-31 | Phase 5(cart) 코드 리뷰에서 발견된 사항 반영. 20.1절 1번(Task 단위 실행)\
 예시 명령어가 `pytest -k "TC_CART_005"` 형태였는데, `-k`는 테스트 함수명을 대상으로\
 매칭하고 실제 테스트 함수명은 TC ID가 아닌 서술형 영문(예:\
 `test_repeated_add_to_cart_accumulates_quantity_on_list_page`)이라 해당 명령어로는\
 테스트가 0건 수집되는 결함을 수정 — pytest 노드 ID(`파일::함수명`) 형태의 실제 동작하는\
 예시로 교체하고, TC ID와 함수명의 대응 관계는 각 테스트 함수 docstring에서 확인한다는\
 설명을 추가. | 승인완료 |
| 2026-09-02 | 사용자 승인에 따라 22.1절에 CI 재현 사례 추가. Phase Final Task 5(실제\
 GitHub Actions 실행 검증) 중 Slack 알림 실전 테스트 과정에서 `test_logout_via_direct_url`\
 (TC-LOGIN-LOGOUT-015)이 GitHub Actions의 headless Chrome 환경에서도 로컬과 동일한\
 증상으로 재현됨을 확인 — 기존에는 로컬(headed) 재현만 기록되어 있었음. 이 결함이\
 headless 분기나 CI 환경 자체의 문제가 아니라 Production `/logout` 엔드포인트의\
 간헐적 결함이라는 기존 결론을 재확인. 다른 절의 내용은 변경하지 않음. | 승인완료 |
