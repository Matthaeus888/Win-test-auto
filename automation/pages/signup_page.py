"""상세 정보 입력 페이지(/signup, "ENTER ACCOUNT INFORMATION")를 다루는 Page Object.

Source of Truth:
- docs/tc/signup-delete-account.md (TC-SIGNUP-DELETE-ACCOUNT-001, 002, 004, 005, 006, 007
  이 페이지의 필수 필드 입력/조회를 사용. 002 = 3개 영역 노출, 001 = Name/Email 자동 반영,
  004 = 선택 필드를 비운 채 필수 필드만 입력해도 가입 가능)
- docs/prd/feature/signup-delete-account.md REQ-SIGNUP-DELETE-ACCOUNT-002~005
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-30, https://automationexercise.com/signup):
`/login` 페이지의 "New User Signup!" 영역에 임의 Name/Email(실제 서비스에 영향을 주지 않는
테스트 전용 값)을 입력하고 Signup 버튼을 클릭해 `/signup` 페이지로 진입한 뒤(계정 생성이
아니라 단순 페이지 이동이므로 AUTOMATION_GUIDE 5.3절 위반 아님), `browser_snapshot`으로
"Enter Account Information"/"Address Information" 2개 영역 구조를 먼저 확인하고,
`browser_evaluate`로 폼 내 모든 input/select/button 요소의 id/name/data-qa 속성을 전수
조회했다. **Create Account 버튼은 실측 과정에서 클릭하지 않았다**(실제 Production 계정
생성 방지, AUTOMATION_GUIDE 5.3절).

- 상단 영역(Title, Name*, Email*, Password*, Date of Birth, 체크박스 2종)과 ADDRESS
  INFORMATION 영역(First name*, Last name*, Company, Address*, Address 2, Country*,
  State*, City*, Zipcode*), 하단 영역(Mobile Number*, Create Account 버튼)의 모든 입력
  요소가 각각 고유한 `id` 속성을 갖고 있음을 확인했다(예: `id="name"`, `id="email"`,
  `id="password"`, `id="days"`/`id="months"`/`id="years"`, `id="newsletter"`/`id="optin"`,
  `id="id_gender1"`/`id="id_gender2"`(Title 라디오), `id="first_name"`, `id="last_name"`,
  `id="company"`, `id="address1"`, `id="address2"`, `id="country"`, `id="state"`,
  `id="city"`, `id="zipcode"`, `id="mobile_number"`). `document.querySelectorAll('#' + id)`로
  전 항목 count=1임을 확인해 AUTOMATION_GUIDE 6.1절 1순위(`id`)를 그대로 적용했다.
- Email 입력란(`id="email"`)은 이전 단계(로그인 페이지)에서 입력한 값이 자동 반영된 채
  `disabled` 속성이 걸려 있음을 확인했다(TC-SIGNUP-DELETE-ACCOUNT-001의 "Email 값이 동일하게
  노출된다"는 Expected Result와 일치, 수정 불가 상태로 노출만 됨).
- "Create Account" 버튼은 `id`/`name`이 없으나 `data-qa="create-account"` 속성이
  페이지 전체에서 1개뿐임을 확인해(count=1) 2순위(`data-qa`) 기준으로 Locator를 정의했다.
- "Enter Account Information"/"Address Information" 두 영역 제목(h2)은 id/data-qa/name이
  없고 공통 CSS 클래스(`h2.title.text-center`)가 두 제목 사이에 중복되어(count=2) 4순위
  (CSS Selector)로는 고유 식별이 불가능함을 확인했다. 이에 따라 5순위(상대 XPath, 텍스트
  결합)로 각 제목의 텍스트를 결합한 XPath를 사용했다(Full XPath가 아닌 텍스트 조건 기반
  상대 XPath).
- Country 선택란(`id="country"`)은 `<select>` 요소이므로 Page Layer에서
  `selenium.webdriver.support.ui.Select`로 감싸 값을 지정한다.

[Phase 2 Task 7 버그 수정, 2026-08-30] TC-SIGNUP-DELETE-ACCOUNT-002 자동화 테스트 실행 중
`//h2[normalize-space(text())='Enter Account Information']`(및 Address Information
버전)이 실제로는 0건 매칭됨을 실측으로 확인했다. Playwright MCP로 실제 DOM을 재조회한
결과 두 h2 모두 `<h2><b>Enter Account Information</b></h2>` 구조로, 텍스트가 h2의 직계
텍스트 노드가 아니라 자식 `<b>` 태그 안에 있어 XPath `text()`(직계 텍스트 노드만 선택)로는
매칭되지 않음을 확인했다(`document.evaluate`로 old locator count=0 재현). `text()`를
`.`(context node 자체의 문자열 값, 자손 텍스트까지 포함)으로 교체한 결과
`//h2[normalize-space(.)='Enter Account Information']`/`...'Address Information'`
각각 count=1로 고유 매칭됨을 확인해 두 Locator를 수정했다(여전히 5순위 상대 XPath 범주,
Full XPath 아님).
"""

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class SignupPage(BasePage):
    """상세 정보 입력 페이지(/signup)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/type_text/is_element_visible/find_element)만 사용해 요소를 조작·조회한다.
    """

    # 상단 영역 ("ENTER ACCOUNT INFORMATION")
    TOP_SECTION_HEADING = (
        By.XPATH,
        "//h2[normalize-space(.)='Enter Account Information']",
    )
    TITLE_MR_RADIO = (By.ID, "id_gender1")
    TITLE_MRS_RADIO = (By.ID, "id_gender2")
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    DOB_DAY_SELECT = (By.ID, "days")
    DOB_MONTH_SELECT = (By.ID, "months")
    DOB_YEAR_SELECT = (By.ID, "years")
    NEWSLETTER_CHECKBOX = (By.ID, "newsletter")
    OPTIN_CHECKBOX = (By.ID, "optin")

    # ADDRESS INFORMATION 영역
    ADDRESS_SECTION_HEADING = (
        By.XPATH,
        "//h2[normalize-space(.)='Address Information']",
    )
    FIRST_NAME_INPUT = (By.ID, "first_name")
    LAST_NAME_INPUT = (By.ID, "last_name")
    COMPANY_INPUT = (By.ID, "company")
    ADDRESS_INPUT = (By.ID, "address1")
    ADDRESS2_INPUT = (By.ID, "address2")
    COUNTRY_SELECT = (By.ID, "country")
    STATE_INPUT = (By.ID, "state")
    CITY_INPUT = (By.ID, "city")
    ZIPCODE_INPUT = (By.ID, "zipcode")

    # 하단 영역
    MOBILE_NUMBER_INPUT = (By.ID, "mobile_number")
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")

    def fill_mandatory_fields(
        self,
        password: str,
        first_name: str,
        last_name: str,
        address: str,
        country: str,
        state: str,
        city: str,
        zipcode: str,
        mobile_number: str,
    ) -> None:
        """필수(*) 입력 필드만 입력한다.

        Title/Date of Birth/체크박스 2종/Company/Address 2 등 선택 필드는 건드리지
        않는다(TC-SIGNUP-DELETE-ACCOUNT-004: 선택 필드를 비운 채 필수 필드만 입력해도
        가입이 가능한지 확인하는 시나리오에서 사용). Name/Email은 이전 단계(로그인
        페이지)에서 입력한 값이 자동 반영되므로 이 메서드에서 다시 입력하지 않는다.
        """
        self.type_text(self.PASSWORD_INPUT, password)
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.ADDRESS_INPUT, address)
        self.select_country(country)
        self.type_text(self.STATE_INPUT, state)
        self.type_text(self.CITY_INPUT, city)
        self.type_text(self.ZIPCODE_INPUT, zipcode)
        self.type_text(self.MOBILE_NUMBER_INPUT, mobile_number)

    def select_country(self, country: str) -> None:
        """Country 드롭다운에서 표시 텍스트(예: "United States") 기준으로 값을 선택한다."""
        element = self.find_element(self.COUNTRY_SELECT)
        try:
            Select(element).select_by_visible_text(country)
            self.logger.info("Country 선택 완료: %s", country)
        except NoSuchElementException:
            self.logger.error("Country 드롭다운에 존재하지 않는 옵션 텍스트: %s", country)
            raise

    def click_create_account(self) -> None:
        """"Create Account" 버튼을 클릭한다."""
        self.click(self.CREATE_ACCOUNT_BUTTON)

    def is_top_section_visible(self) -> bool:
        """상단 영역(Title/Name/Email/Password/DOB/체크박스 2종)의 전 항목 노출 여부를 반환한다.

        모든 요소가 노출되는 경우에만 True를 반환한다(TC-SIGNUP-DELETE-ACCOUNT-002).
        """
        return (
            self.is_element_visible(self.TOP_SECTION_HEADING)
            and self.is_element_visible(self.TITLE_MR_RADIO)
            and self.is_element_visible(self.TITLE_MRS_RADIO)
            and self.is_element_visible(self.NAME_INPUT)
            and self.is_element_visible(self.EMAIL_INPUT)
            and self.is_element_visible(self.PASSWORD_INPUT)
            and self.is_element_visible(self.DOB_DAY_SELECT)
            and self.is_element_visible(self.DOB_MONTH_SELECT)
            and self.is_element_visible(self.DOB_YEAR_SELECT)
            and self.is_element_visible(self.NEWSLETTER_CHECKBOX)
            and self.is_element_visible(self.OPTIN_CHECKBOX)
        )

    def is_address_section_visible(self) -> bool:
        """ADDRESS INFORMATION 영역의 전 항목 노출 여부를 반환한다.

        모든 요소가 노출되는 경우에만 True를 반환한다(TC-SIGNUP-DELETE-ACCOUNT-002).
        """
        return (
            self.is_element_visible(self.ADDRESS_SECTION_HEADING)
            and self.is_element_visible(self.FIRST_NAME_INPUT)
            and self.is_element_visible(self.LAST_NAME_INPUT)
            and self.is_element_visible(self.COMPANY_INPUT)
            and self.is_element_visible(self.ADDRESS_INPUT)
            and self.is_element_visible(self.ADDRESS2_INPUT)
            and self.is_element_visible(self.COUNTRY_SELECT)
            and self.is_element_visible(self.STATE_INPUT)
            and self.is_element_visible(self.CITY_INPUT)
            and self.is_element_visible(self.ZIPCODE_INPUT)
        )

    def is_bottom_section_visible(self) -> bool:
        """하단 영역(Mobile Number, Create Account 버튼)의 전 항목 노출 여부를 반환한다.

        모든 요소가 노출되는 경우에만 True를 반환한다(TC-SIGNUP-DELETE-ACCOUNT-002).
        """
        return self.is_element_visible(
            self.MOBILE_NUMBER_INPUT
        ) and self.is_element_visible(self.CREATE_ACCOUNT_BUTTON)

    def get_prefilled_name(self) -> str:
        """Name 입력란에 자동 반영된 값을 조회해 반환한다(Assertion 없음).

        TC-SIGNUP-DELETE-ACCOUNT-001: 로그인 페이지에서 입력한 Name 값이 이 페이지에도
        동일하게 노출되는지 확인할 때 사용한다.
        """
        return self.find_element(self.NAME_INPUT).get_attribute("value")

    def get_prefilled_email(self) -> str:
        """Email 입력란에 자동 반영된 값을 조회해 반환한다(Assertion 없음).

        TC-SIGNUP-DELETE-ACCOUNT-001: 로그인 페이지에서 입력한 Email 값이 이 페이지에도
        동일하게 노출되는지 확인할 때 사용한다. 이 입력란은 실측 결과 `disabled` 상태로
        노출만 되고 수정은 불가능하다(위 docstring 참고).
        """
        return self.find_element(self.EMAIL_INPUT).get_attribute("value")
