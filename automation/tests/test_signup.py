"""로그인 페이지에서 시작하는 회원가입 진입(1단계) 및 상세 정보 입력 페이지 UI 노출,
회원가입 완료(Happy Path)/중복 이메일 재가입 시도를 검증하는 테스트.

Source of Truth:
- docs/tc/signup-delete-account.md (TC-SIGNUP-DELETE-ACCOUNT-001, 002, 004, 005, 006, 007)
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙)

이 파일은 TC-001(로그인 페이지에서 신규 Name/Email 입력 후 Signup 클릭 시 `/signup`으로
이동하고 입력한 Name/Email 값이 자동 반영되는지), TC-002(상세 정보 입력 페이지가 상단/
ADDRESS INFORMATION/하단 3개 영역 구성으로 노출되는지), TC-004(선택 필드를 비운 채 필수
필드만 입력해도 가입이 완료되는지), TC-005(가입 완료 시 안내 문구/Continue 버튼/로그아웃
상태 네비게이션이 함께 노출되는지), TC-006(Continue 클릭 시 Home 랜딩 및 로그아웃 상태
유지), TC-007(이미 가입된 이메일로 재가입 시도 시 에러 메시지 노출)을 다룬다.

TC-001, 002, 007은 "Create Account" 버튼을 클릭하지 않으므로 실제 계정이 생성되지 않아
별도 cleanup이 필요 없다. TC-004, 005, 006은 각 테스트가 `_complete_signup()` 헬퍼를 통해
실제로 automationexercise.com에 신규 계정을 생성한다(AUTOMATION_GUIDE 11.2절 동적 계정
생성 및 ROADMAP.md Phase 2 범위 내에서 이미 승인된 동작). 각 테스트는 서로 다른 테스트가
만든 계정을 재사용하지 않고 매번 `_complete_signup()`을 개별 호출해 독립적으로 신규 계정을
생성한다(AUTOMATION_GUIDE 10절 테스트 독립성).

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(LoginPage/SignupPage/
AccountCreatedPage/HomePage)는 화면 조작/조회만 담당한다(Assertion 없음).

민감정보 관리: 이 파일이 사용하는 데이터는 utils.account_factory.generate_signup_data()가
매 실행마다 생성하는 더미 값이며, 실제 개인정보나 비밀번호를 코드에 하드코딩하지 않는다.
TC-007에서 사용하는 기존 이메일(actest1)의 비밀번호는 사용하지 않으며(재가입 시도만
확인하므로 비밀번호가 필요 없음), 이메일 값은 config.accounts.get_account()로 로드한다.
"""

from config.accounts import get_account
from config.settings import BASE_URL
from pages.account_created_page import AccountCreatedPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.account_factory import generate_signup_data


def _complete_signup(driver) -> dict:
    """테스트 내부 전용 회원가입 완료 헬퍼(3개 이상 테스트에서 재사용).

    TC-004/005/006이 모두 "필수 필드만 입력해 가입을 완료한 상태"를 사전 조건으로
    요구하므로 이 파일 안에서만 재사용하는 짧은 로직이다. AUTOMATION_GUIDE 19절에 따라
    특정 Feature 하나(signup-delete-account)에서만 쓰이는 로직을 별도 config/utils
    모듈로 섣불리 공통화하지 않고, 이 테스트 파일 내부 함수로만 둔다(test_login.py의
    `_login` 헬퍼와 동일한 패턴).

    선택 필드(Title/Date of Birth/체크박스 2종/Company/Address 2)는 절대 입력하지
    않는다(TC-SIGNUP-DELETE-ACCOUNT-004: 선택 필드를 비운 채 필수 필드만 입력해도
    가입이 가능한지 확인하는 시나리오).
    """
    signup_data = generate_signup_data()
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.start_signup(signup_data["name"], signup_data["email"])

    signup_page = SignupPage(driver)
    signup_page.fill_mandatory_fields(
        signup_data["password"],
        signup_data["first_name"],
        signup_data["last_name"],
        signup_data["address"],
        signup_data["country"],
        signup_data["state"],
        signup_data["city"],
        signup_data["zipcode"],
        signup_data["mobile_number"],
    )
    signup_page.click_create_account()

    return signup_data


def test_signup_redirects_and_prefills_name_email(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-001: 로그인 페이지에서 신규 Name/Email 입력 후 Signup
    클릭 시 `/signup`으로 이동하고 입력한 Name/Email 값이 자동 반영되는지 확인한다."""
    signup_data = generate_signup_data()
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.start_signup(signup_data["name"], signup_data["email"])

    signup_page = SignupPage(driver)
    signup_page.wait_for_url_contains("/signup")
    current_url = driver.current_url
    prefilled_name = signup_page.get_prefilled_name()
    prefilled_email = signup_page.get_prefilled_email()

    assert "/signup" in current_url, (
        f"상세 정보 입력 페이지(/signup)로 이동해야 하지만 그렇지 않음 "
        f"(기대: '/signup' 포함, 실제: {current_url})"
    )
    assert prefilled_name == signup_data["name"], (
        f"Name 입력란에 자동 반영된 값이 로그인 페이지에서 입력한 값과 다름 "
        f"(기대: {signup_data['name']!r}, 실제: {prefilled_name!r})"
    )
    assert prefilled_email == signup_data["email"], (
        f"Email 입력란에 자동 반영된 값이 로그인 페이지에서 입력한 값과 다름 "
        f"(기대: {signup_data['email']!r}, 실제: {prefilled_email!r})"
    )


def test_signup_page_shows_all_sections(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-002: 상세 정보 입력 페이지가 상단(Title/Name/Email/
    Password/DOB/체크박스 2종), ADDRESS INFORMATION, 하단(Mobile Number/Create Account
    버튼) 3개 영역 구성으로 빠짐없이 노출되는지 확인한다."""
    signup_data = generate_signup_data()
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.start_signup(signup_data["name"], signup_data["email"])

    signup_page = SignupPage(driver)
    signup_page.wait_for_url_contains("/signup")
    is_top_section_visible = signup_page.is_top_section_visible()
    is_address_section_visible = signup_page.is_address_section_visible()
    is_bottom_section_visible = signup_page.is_bottom_section_visible()

    assert is_top_section_visible, (
        f"상단 영역(Title/Name/Email/Password/DOB/체크박스 2종)의 모든 항목이 노출되어야 "
        f"하지만 그렇지 않음 (기대: True, 실제: {is_top_section_visible})"
    )
    assert is_address_section_visible, (
        f"ADDRESS INFORMATION 영역의 모든 항목이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_address_section_visible})"
    )
    assert is_bottom_section_visible, (
        f"하단 영역(Mobile Number, Create Account 버튼)의 모든 항목이 노출되어야 하지만 "
        f"그렇지 않음 (기대: True, 실제: {is_bottom_section_visible})"
    )


def test_signup_with_only_mandatory_fields_succeeds(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-004: 선택 필드(Title/Date of Birth/체크박스 2종/Company/
    Address 2)를 모두 비운 채 필수 필드만 입력해도 별도 에러 없이 "ACCOUNT CREATED!" 완료
    페이지(`/account_created`)로 정상 이동해 가입이 완료되는지 확인한다."""
    _complete_signup(driver)

    account_created_page = AccountCreatedPage(driver)
    account_created_page.wait_for_url_contains("/account_created")
    current_url = driver.current_url

    assert "/account_created" in current_url, (
        f"필수 필드만 입력해도 가입 완료 페이지(/account_created)로 이동해야 하지만 "
        f"그렇지 않음 (기대: '/account_created' 포함, 실제: {current_url})"
    )


def test_account_created_page_shows_confirmation(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-005: 가입 완료 시 "ACCOUNT CREATED!" 페이지에 안내
    문구/Continue 버튼이 노출되고, 상단 네비게이션은 로그아웃 상태 메뉴로 노출되는지(자동
    로그인되지 않는지) 확인한다."""
    _complete_signup(driver)

    account_created_page = AccountCreatedPage(driver)
    account_created_page.wait_for_url_contains("/account_created")
    confirmation_text = account_created_page.get_confirmation_text()

    home_page = HomePage(driver)
    is_logged_out_menu_visible = home_page.is_logged_out_menu_visible()

    assert "successfully created" in confirmation_text, (
        f'안내 문구에 "successfully created"가 포함되어야 하지만 그렇지 않음 '
        f"(기대: 'successfully created' 포함, 실제: {confirmation_text!r})"
    )
    assert is_logged_out_menu_visible, (
        f"가입 완료 직후에도 자동 로그인되지 않고 로그아웃 상태 메뉴(Signup / Login)가 "
        f"노출되어야 하지만 그렇지 않음 (기대: True, 실제: {is_logged_out_menu_visible})"
    )


def test_continue_from_account_created_lands_on_home(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-006: "ACCOUNT CREATED!" 페이지에서 "Continue" 클릭 시
    Home(`https://automationexercise.com/`)으로 랜딩되며, 방금 생성한 계정으로 자동
    로그인되어 로그인 상태 메뉴로 전환되는지 확인한다.

    [2026-08-30 갱신] 최초 구현 시 TC-006 Expected Result는 "로그아웃 상태 유지"였으나,
    실제 pytest 실행(Selenium, 3회 독립 재현) 결과 Continue 클릭 시 방금 생성한 계정으로
    자동 로그인됨을 확인해 사용자 승인 하에 TC-006/PRD REQ-SIGNUP-DELETE-ACCOUNT-007을
    갱신했다(docs/tc/signup-delete-account.md, docs/prd/feature/signup-delete-account.md
    변경 이력 참고). 이 테스트도 갱신된 Expected Result에 맞춰 재작성되었다.
    """
    signup_data = _complete_signup(driver)

    account_created_page = AccountCreatedPage(driver)
    account_created_page.wait_for_url_contains("/account_created")
    account_created_page.click_continue()

    home_page = HomePage(driver)
    home_page.wait_for_url_to_be(BASE_URL)
    current_url = driver.current_url
    is_logged_in_menu_visible = home_page.is_logged_in_menu_visible()
    logged_in_user_text = home_page.get_logged_in_user_text()

    assert current_url == BASE_URL, (
        f"Continue 클릭 시 Home({BASE_URL})으로 랜딩해야 하지만 그렇지 않음 "
        f"(기대: {BASE_URL}, 실제: {current_url})"
    )
    assert is_logged_in_menu_visible, (
        f"Continue 클릭 후 방금 생성한 계정으로 자동 로그인되어 로그인 상태 메뉴(Logout/"
        f"Delete Account)가 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_logged_in_menu_visible})"
    )
    assert signup_data["name"] in logged_in_user_text, (
        f'"Logged in as" 텍스트에 방금 생성한 계정 이름이 포함되어야 하지만 그렇지 않음 '
        f"(기대: {signup_data['name']!r} 포함, 실제: {logged_in_user_text!r})"
    )


def test_signup_with_existing_email_shows_error(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-007: 이미 가입된 이메일로 재가입 시도 시 상세 정보 입력
    페이지로 전환되지 않고 "Email Address already exist!" 에러 메시지가 노출되는지
    확인한다. 이 테스트는 "Create Account"를 호출하지 않으므로 실제 신규 계정을 생성하지
    않는다."""
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.start_signup("QA Existing Email Check", account["email"])

    error_message = login_page.get_signup_error_message()
    expected_message = "Email Address already exist!"

    assert error_message == expected_message, (
        f"에러 메시지가 기대값과 다름 (기대: {expected_message!r}, 실제: {error_message!r})"
    )
