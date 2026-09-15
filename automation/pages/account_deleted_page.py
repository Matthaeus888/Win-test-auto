"""계정삭제 완료 페이지(/delete_account, "ACCOUNT DELETED!")를 다루는 Page Object.

Source of Truth:
- docs/tc/signup-delete-account.md
  (TC-SIGNUP-DELETE-ACCOUNT-011: 계정삭제 처리 후 "ACCOUNT DELETED!" 완료 페이지 이동,
  안내 문구, "Continue" 버튼, 로그아웃 상태 네비게이션이 함께 노출되는지 확인.
  TC-SIGNUP-DELETE-ACCOUNT-012: 이 페이지에서 "Continue" 클릭 시 로그아웃 상태로 Home으로
  랜딩되는지 확인.
  TC-SIGNUP-DELETE-ACCOUNT-016: 로그아웃 상태(미인증)에서 URL로 직접 접근해도 이 완료
  페이지가 그대로 노출되는 결함 의심 항목 — 이번 실측에서 이 방식(URL 직접 접근)을 조회
  목적으로만 활용했다.)
- docs/prd/feature/signup-delete-account.md REQ-SIGNUP-DELETE-ACCOUNT-012/013
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 5.3절(Playwright MCP는
  조회·탐색 전용), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-30, https://automationexercise.com/delete_account):
docs/tc/signup-delete-account.md의 TC-SIGNUP-DELETE-ACCOUNT-016(결함 의심 항목)에 이미
기록되어 있듯, 로그아웃 상태에서 이 URL에 직접 접근해도 완료 페이지가 그대로 노출되므로
`browser_navigate`로 URL에 바로 진입해(실제 로그인/계정삭제 없이 페이지 구조만 조회하는
목적, Production 데이터 변경 없음 — AUTOMATION_GUIDE 5.3절) `browser_snapshot`과
`browser_evaluate`로 구조를 확인했다. `AccountCreatedPage`(2026-08-30 구현)와 구조가
매우 유사함을 확인했으며 동일한 실측 절차를 그대로 적용했다.

- "Account Deleted!" 제목(h2)은 `data-qa="account-deleted"` 속성을 가지며
  `document.querySelectorAll('[data-qa="account-deleted"]')` 결과 count=1로 페이지 전체에서
  고유함을 확인했다(AUTOMATION_GUIDE 6.1절 2순위 `data-qa` 적용 대상).
- "Continue" 버튼은 `AccountCreatedPage`와 동일하게 실제로는 `<button>`이 아니라
  `<a href="/" data-qa="continue-button" class="btn btn-primary">Continue</a>` 링크임을
  확인했다. `data-qa="continue-button"`도 페이지 전체에서 count=1로 고유해(참고로
  `a[href="/"]` 단독 조건으로는 로고/Home 메뉴 링크까지 포함해 count=3으로 고유하지 않음을
  함께 확인했다) 동일하게 2순위(`data-qa`) 기준을 적용했다.
- 안내 문구("Your account has been permanently deleted!")를 담은 `<p>`는 id/data-qa/name이
  없고, 인라인 스타일(`style="font-size: 20px; font-family: garamond;"`)이 동일 섹션의 두
  번째 `<p>`("You can create new account to take advantage of member privileges...")와
  중복되어(동일 스타일 속성 count=2) CSS 속성 선택자만으로는 고유 식별이 불가능함을 확인했다.
  이에 따라 `AccountCreatedPage.CONFIRMATION_TEXT`와 동일한 패턴으로 5순위(상대 XPath, 텍스트
  결합)를 사용해 `//p[contains(text(), 'permanently deleted')]`로 정의했으며,
  `document.evaluate()`로 이 XPath가 페이지 내에서 정확히 1개(count=1)의 `<p>`만 가리킴을
  확인했다.
- 참고: `browser_evaluate`로 위 `<p>`를 조회했을 때 "Language Resources"라는 문구가 텍스트에
  추가로 붙어 조회된 적이 있었으나(`google-anno-skip` class를 가진 `<div>`가 삽입된 형태),
  `fetch()`로 서버가 실제로 응답하는 원본 HTML을 직접 조회해 비교한 결과 해당 `<p>` 태그
  안에는 그런 문구가 전혀 없음을 확인했다(원본:
  `<p style="font-size: 20px; font-family: garamond;">Your account has been permanently
  deleted!</p>`). `AccountCreatedPage` 구현 시 확인된 것과 동일하게, 이 문구는 Playwright
  MCP 브라우저 세션에 주입된 확장 프로그램/광고 주석(annotation) 아티팩트이며 실제 페이지
  마크업이 아니므로, Selenium(ChromeDriver, 확장 프로그램 없는 클린 브라우저) 실행 시에는
  재현되지 않을 것으로 판단한다. 다만 실제 pytest 실행 시 텍스트 비교 방식(정확히 일치 vs
  부분 포함)에 따라 영향이 있을 수 있으므로, 이후 이 Page Object를 사용하는 테스트 작성 시
  `in` 등 부분 포함 방식으로 검증하는 것이 안전하다는 점을 참고로 남긴다(이 Page Object
  자체는 Assertion을 수행하지 않으므로 이 결정은 Test Layer의 몫이다).

설계 결정(AUTOMATION_GUIDE 19절, Task Notes 명시): `AccountCreatedPage`와 구조가 유사하지만
화면 단위 1 Page 클래스 원칙에 따라 공통 부모 클래스로 섣불리 추상화하지 않고 `BasePage`를
직접 상속하는 별도 Page 클래스로 구현한다.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AccountDeletedPage(BasePage):
    """계정삭제 완료 페이지(/delete_account)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/get_text)만 사용해 요소를 조작·조회한다.
    """

    # 안내 문구("Your account has been permanently deleted!")
    CONFIRMATION_TEXT = (By.XPATH, "//p[contains(text(), 'permanently deleted')]")

    # "Continue" 버튼(실제로는 <a> 링크, href="/")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def get_confirmation_text(self) -> str:
        """안내 문구 텍스트를 조회해 반환한다(Assertion 없음).

        TC-SIGNUP-DELETE-ACCOUNT-011: "Your account has been permanently deleted!" 등의
        안내 문구가 노출되는지 확인할 때 사용한다.
        """
        return self.get_text(self.CONFIRMATION_TEXT)

    def click_continue(self) -> None:
        """"Continue" 버튼을 클릭한다.

        TC-SIGNUP-DELETE-ACCOUNT-012: 클릭 시 로그아웃 상태로 Home(`/`)으로 랜딩되는지
        확인할 때 사용한다.

        [2026-08-30 Task 10 회귀 실행 중 추가] `AccountCreatedPage.click_continue()`와
        동일하게, 실제 페이지 이동(`<a href="/">`)이므로 Google Vignette 전면 광고가
        클릭을 가로채 URL 끝에 `#google_vignette`만 추가된 채 실제 이동이 되지 않는
        현상이 재현되었다(전체 스위트 회귀 실행 중 관찰, `AccountCreatedPage`는 이미
        이 방어가 있었으나 이 클래스에는 누락되어 있었음).

        [2026-08-30 코드 리뷰 반영, finding #3] 당시 두 Page Object에 동일한 재클릭
        로직을 각각 복붙했던 것이 바로 이 누락(회귀)의 원인이었으므로,
        `BasePage.click_and_retry_if_vignette()`로 통합해 중복을 제거했다.
        """
        self.click_and_retry_if_vignette(self.CONTINUE_BUTTON)
