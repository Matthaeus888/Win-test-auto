"""로그인 상태에서 상단 네비게이션 "Delete Account" 클릭 시 즉시 계정삭제가 처리되고,
"ACCOUNT DELETED!" 완료 페이지의 안내 문구/Continue 버튼/네비게이션 상태, Continue 클릭 시
로그아웃 상태로 Home 랜딩되는지를 검증하는 테스트.

Source of Truth:
- docs/tc/signup-delete-account.md
  (TC-SIGNUP-DELETE-ACCOUNT-010: 로그인 상태에서 "Delete Account" 클릭 시 별도 확인 절차
  없이 즉시 `/delete_account`로 이동하는지.
  TC-SIGNUP-DELETE-ACCOUNT-011: 삭제 완료 페이지의 안내 문구/Continue 버튼이 노출되고
  상단 네비게이션이 로그아웃 상태 메뉴로 노출되는지.
  TC-SIGNUP-DELETE-ACCOUNT-012: Continue 클릭 시 로그아웃 상태로 Home 랜딩되는지.)
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙),
  11.1절(계정삭제 TC는 재사용 고정 계정(actest1~3)을 삭제 대상으로 사용하지 않고, 사전에
  회원가입 절차로 별도 생성한 "삭제 전용" 테스트 계정을 사용)

삭제 대상 계정은 항상 이 테스트가 사전에 신규 가입한 "삭제 전용" 계정이며, 재사용 고정
계정(actest1~3)은 사용하지 않는다.

[_signup_and_login 재확인 결과] 이 헬퍼는 원래 "가입 완료 → Continue → Home(로그아웃) →
로그인 페이지에서 별도 로그인" 순서를 상정했으나, TC-SIGNUP-DELETE-ACCOUNT-006이
2026-08-30에 갱신된 대로(docs/tc/signup-delete-account.md 변경 이력 참고) "ACCOUNT
CREATED!" 페이지에서 "Continue" 클릭 시 방금 생성한 계정으로 이미 자동 로그인됨을
`tests/test_signup.py::test_continue_from_account_created_lands_on_home` 실제 pytest
재실행(PASSED, `home_page.is_logged_in_menu_visible()` True 확인)으로 재확인했다. 따라서
`LoginPage.login()`을 이용한 별도 재로그인 단계는 불필요하며(CLAUDE.md 12절 "불필요한 코드
작성 금지"), 이 헬퍼는 Continue 클릭 후 Home 랜딩까지만 수행하고 별도 로그인 호출을
추가하지 않는다.

[TC-SIGNUP-DELETE-ACCOUNT-013/014 추가, 2026-08-30] 위 3개 TC(010~012)는 "삭제 직전까지"만
확인하면 충분했지만, 아래 2개 TC는 "삭제까지 완결된" 계정 상태가 사전 조건으로 필요하다.
- TC-SIGNUP-DELETE-ACCOUNT-013: 삭제된 계정의 이메일/비밀번호로 재로그인 시도 시 로그인되지
  않고 "Your email or password is incorrect!" 에러가 노출되는지 확인한다
  (`LoginPage.get_error_message()`, TC-LOGIN-LOGOUT-005/006/013에서 이미 실측 확인된
  `.login-form p` Locator를 그대로 재사용).
- TC-SIGNUP-DELETE-ACCOUNT-014: 삭제된 계정의 이메일로 재가입 시도 시 "Email Address already
  exist!" 에러 없이 정상적으로 신규 가입(재가입)이 진행되는지 확인한다.

이를 위해 기존 `_signup_and_login`(가입 완료 후 로그인 상태까지만 확보)과 별개로,
`_signup_login_and_delete`(계정삭제까지 완료한 상태를 확보) 헬퍼를 신규로 추가했다.

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(LoginPage/SignupPage/
AccountCreatedPage/AccountDeletedPage/HomePage)는 화면 조작/조회만 담당한다(Assertion
없음).

민감정보 관리: 이 파일이 사용하는 데이터는 utils.account_factory.generate_signup_data()가
매 실행마다 생성하는 더미 값이며, 실제 개인정보나 비밀번호를 코드에 하드코딩하지 않는다.
"""

from config.settings import BASE_URL
from pages.account_created_page import AccountCreatedPage
from pages.account_deleted_page import AccountDeletedPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.account_factory import generate_signup_data


def _signup_and_login(driver) -> dict:
    """테스트 내부 전용 "삭제 전용" 신규 계정 생성 및 로그인 상태 확보 헬퍼(3개 테스트에서
    재사용).

    회원가입 전체 절차(LoginPage.start_signup → SignupPage.fill_mandatory_fields →
    click_create_account())를 완료한 뒤 "ACCOUNT CREATED!" 페이지에서 Continue를 클릭해
    Home으로 랜딩한다. 위 모듈 docstring에서 설명한 대로 이 시점에 이미 방금 생성한
    계정으로 자동 로그인되어 있으므로 별도의 `LoginPage.login()` 재로그인 단계는 넣지
    않는다.

    AUTOMATION_GUIDE 19절에 따라 특정 Feature(signup-delete-account)에서만 쓰이는 로직을
    별도 config/utils 모듈로 섣불리 공통화하지 않고, `test_signup.py`의 `_complete_signup`
    헬퍼와 동일한 패턴으로 이 테스트 파일 내부 함수로만 둔다.

    Returns:
        회원가입에 사용한 데이터(dict, generate_signup_data() 반환값과 동일).
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

    account_created_page = AccountCreatedPage(driver)
    account_created_page.wait_for_url_contains("/account_created")
    account_created_page.click_continue()

    home_page = HomePage(driver)
    home_page.wait_for_url_to_be(BASE_URL)

    return signup_data


def _signup_login_and_delete(driver) -> dict:
    """테스트 내부 전용 "삭제까지 완결된" 신규 계정 상태 확보 헬퍼(TC-013/014 2개 테스트에서
    재사용).

    `_signup_and_login(driver)`로 신규 가입 및 로그인 상태를 확보한 뒤,
    `HomePage.click_delete_account()` → `AccountDeletedPage.wait_for_url_contains(
    "/delete_account")`까지 수행해 계정 삭제 처리가 완료된 상태로 만든다. TC-010~012
    전용이던 `_signup_and_login`은 "삭제 직전"까지만 확인하면 충분했으나, TC-013/014는
    "삭제까지 완결된" 계정의 이메일/비밀번호가 필요하므로 별도 헬퍼로 분리한다(위 모듈
    docstring 참고).

    Returns:
        회원가입에 사용한 데이터(dict, generate_signup_data() 반환값과 동일). email/password
        모두 포함되어 있으며 이 시점에 해당 계정은 이미 삭제 처리가 완료된 상태다.
    """
    signup_data = _signup_and_login(driver)

    home_page = HomePage(driver)
    home_page.click_delete_account()

    account_deleted_page = AccountDeletedPage(driver)
    account_deleted_page.wait_for_url_contains("/delete_account")

    return signup_data


def test_delete_account_without_confirmation(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-010: 로그인 상태에서 상단 네비게이션 "Delete Account"
    클릭 시 별도 확인(컨펌) 절차 없이 즉시 "ACCOUNT DELETED!" 완료 페이지(`/delete_account`)
    로 이동하는지 확인한다."""
    _signup_and_login(driver)

    home_page = HomePage(driver)
    home_page.click_delete_account()

    account_deleted_page = AccountDeletedPage(driver)
    account_deleted_page.wait_for_url_contains("/delete_account")
    current_url = driver.current_url

    assert "/delete_account" in current_url, (
        f"'Delete Account' 클릭 시 별도 확인 절차 없이 즉시 계정삭제 완료 페이지"
        f"(/delete_account)로 이동해야 하지만 그렇지 않음 "
        f"(기대: '/delete_account' 포함, 실제: {current_url})"
    )


def test_account_deleted_page_shows_confirmation(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-011: 계정삭제 처리 후 "ACCOUNT DELETED!" 완료 페이지에
    안내 문구("Your account has been permanently deleted!" 등)와 Continue 버튼이
    노출되고, 상단 네비게이션이 로그아웃 상태 메뉴로 노출되는지 확인한다."""
    _signup_and_login(driver)

    home_page = HomePage(driver)
    home_page.click_delete_account()

    account_deleted_page = AccountDeletedPage(driver)
    account_deleted_page.wait_for_url_contains("/delete_account")
    confirmation_text = account_deleted_page.get_confirmation_text()
    is_logged_out_menu_visible = home_page.is_logged_out_menu_visible()

    assert "permanently deleted" in confirmation_text, (
        f'안내 문구에 "permanently deleted"가 포함되어야 하지만 그렇지 않음 '
        f"(기대: 'permanently deleted' 포함, 실제: {confirmation_text!r})"
    )
    assert is_logged_out_menu_visible, (
        f"계정삭제 완료 후 상단 네비게이션이 로그아웃 상태 메뉴(Signup / Login)로 노출되어야 "
        f"하지만 그렇지 않음 (기대: True, 실제: {is_logged_out_menu_visible})"
    )


def test_continue_from_account_deleted_lands_on_home(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-012: "ACCOUNT DELETED!" 페이지에서 "Continue" 클릭 시
    Home(`https://automationexercise.com/`)으로 랜딩되며, 로그아웃 상태로 전환되는지
    확인한다."""
    _signup_and_login(driver)

    home_page = HomePage(driver)
    home_page.click_delete_account()

    account_deleted_page = AccountDeletedPage(driver)
    account_deleted_page.wait_for_url_contains("/delete_account")
    account_deleted_page.click_continue()

    home_page.wait_for_url_to_be(BASE_URL)
    current_url = driver.current_url
    is_logged_out_menu_visible = home_page.is_logged_out_menu_visible()

    assert current_url == BASE_URL, (
        f"Continue 클릭 시 Home({BASE_URL})으로 랜딩해야 하지만 그렇지 않음 "
        f"(기대: {BASE_URL}, 실제: {current_url})"
    )
    assert is_logged_out_menu_visible, (
        f"Continue 클릭 후 로그아웃 상태 메뉴(Signup / Login)가 노출되어야 하지만 "
        f"그렇지 않음 (기대: True, 실제: {is_logged_out_menu_visible})"
    )


def test_relogin_with_deleted_account_shows_error(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-013: 삭제된 계정의 이메일/비밀번호로 `/login` 페이지에서
    재로그인 시도 시 로그인되지 않고 "Your email or password is incorrect!" 에러 메시지가
    노출되는지 확인한다."""
    deleted_account = _signup_login_and_delete(driver)

    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(deleted_account["email"], deleted_account["password"])
    error_message = login_page.get_error_message()

    expected_error_message = "Your email or password is incorrect!"
    assert error_message == expected_error_message, (
        f"삭제된 계정으로 재로그인 시도 시 에러 메시지가 정확히 일치해야 하지만 그렇지 않음 "
        f"(기대: {expected_error_message!r}, 실제: {error_message!r})"
    )


def test_resignup_with_deleted_account_email_succeeds(driver):
    """TC-SIGNUP-DELETE-ACCOUNT-014: 삭제된 계정의 이메일로 `/login` 페이지의 "New User
    Signup!" 영역에서 재가입 시도 시 "Email Address already exist!" 에러 없이 상세 정보
    입력 페이지(`/signup`)로 정상 이동하고, 최종적으로 "ACCOUNT CREATED!" 완료 페이지
    (`/account_created`)까지 가입이 정상 완료되는지 확인한다."""
    deleted_account = _signup_login_and_delete(driver)

    new_signup_data = generate_signup_data()
    new_signup_data["email"] = deleted_account["email"]

    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.start_signup(new_signup_data["name"], new_signup_data["email"])

    signup_page = SignupPage(driver)
    is_top_section_visible = signup_page.is_top_section_visible()

    assert is_top_section_visible, (
        f"삭제된 계정의 이메일로 재가입 시도 시 'Email Address already exist!' 에러 없이 "
        f"상세 정보 입력 페이지(/signup)로 정상 이동해야 하지만 그렇지 않음 "
        f"(기대: 상단 영역(Enter Account Information) 노출 True, 실제: "
        f"{is_top_section_visible})"
    )

    signup_page.fill_mandatory_fields(
        new_signup_data["password"],
        new_signup_data["first_name"],
        new_signup_data["last_name"],
        new_signup_data["address"],
        new_signup_data["country"],
        new_signup_data["state"],
        new_signup_data["city"],
        new_signup_data["zipcode"],
        new_signup_data["mobile_number"],
    )
    signup_page.click_create_account()

    account_created_page = AccountCreatedPage(driver)
    account_created_page.wait_for_url_contains("/account_created")
    current_url = driver.current_url

    assert "/account_created" in current_url, (
        f"필수 필드 입력 후 Create Account 클릭 시 최종적으로 회원가입 완료 페이지"
        f"(/account_created)로 이동해 재가입이 정상 완료되어야 하지만 그렇지 않음 "
        f"(기대: '/account_created' 포함, 실제: {current_url})"
    )
