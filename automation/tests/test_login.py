"""로그인 페이지(/login) 진입/UI 노출, 로그인 성공/실패, 세션 유지/로그아웃을 검증하는 테스트.

Source of Truth:
- docs/tc/login-logout.md (TC-LOGIN-LOGOUT-001, 002, 003, 004, 005, 006, 010, 011, 013,
  014, 015)
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙)

이 파일은 TC-001, 002, 003(로그아웃 상태 진입/UI 노출), TC-004, 005, 006, 013(로그인
성공/실패), TC-010, 011, 014, 015(로그인 세션 유지 및 로그아웃)를 다룬다.

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(LoginPage/HomePage)는 화면
조작/조회만 담당한다(Assertion 없음).

민감정보 관리: 고정 계정(actest1)의 비밀번호는 config.accounts.get_account()를 통해
automation/.env(git 미추적)에서만 로드하며, 이 파일 어디에도 실제 비밀번호 값을
하드코딩하지 않는다.
"""

from config.accounts import get_account
from config.settings import BASE_URL
from pages.home_page import HomePage
from pages.login_page import LoginPage


def _login(driver, account_name: str = "actest1") -> None:
    """테스트 내부 전용 로그인 헬퍼(2개 이상 테스트에서 재사용).

    TC-010/011/014/015가 모두 "로그인 상태"를 사전 조건으로 요구하므로 이 파일
    안에서만 재사용하는 짧은 로직이다. AUTOMATION_GUIDE 19절에 따라 특정 Feature
    하나(login-logout)에서만 쓰이는 로직을 별도 config/utils 모듈로 섣불리
    공통화하지 않고, 이 테스트 파일 내부 함수로만 둔다.
    """
    account = get_account(account_name)
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])


def test_login_page_shows_login_and_signup_sections(driver):
    """TC-LOGIN-LOGOUT-001: `/login` 진입 시 로그인 폼 영역과 New User Signup 영역이 함께 노출된다."""
    login_page = LoginPage(driver)
    login_page.navigate()

    is_login_form_visible = login_page.is_login_form_visible()
    is_signup_visible = login_page.is_new_user_signup_visible()

    assert is_login_form_visible, (
        f'"Login to your account" 영역이 노출되어야 하지만 노출되지 않음 '
        f"(기대: True, 실제: {is_login_form_visible})"
    )
    assert is_signup_visible, (
        f'"New User Signup!" 영역이 노출되어야 하지만 노출되지 않음 '
        f"(기대: True, 실제: {is_signup_visible})"
    )


def test_navigate_to_login_via_top_navigation(driver):
    """TC-LOGIN-LOGOUT-002: 상단 네비게이션 "Signup/Login" 클릭으로 로그인 페이지(`/login`)에 도달한다."""
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_signup_login()

    login_page = LoginPage(driver)
    current_url = driver.current_url
    is_login_form_visible = login_page.is_login_form_visible()

    assert "/login" in current_url, (
        f"로그인 페이지(/login)로 이동해야 하지만 그렇지 않음 "
        f"(기대: '/login' 포함, 실제: {current_url})"
    )
    assert is_login_form_visible, (
        f'"Login to your account" 영역이 노출되어야 하지만 노출되지 않음 '
        f"(기대: True, 실제: {is_login_form_visible})"
    )


def test_navigate_to_login_via_direct_url(driver):
    """TC-LOGIN-LOGOUT-003: URL(`/login`) 직접 진입으로 로그인 페이지에 도달한다."""
    login_page = LoginPage(driver)
    login_page.navigate()

    current_url = driver.current_url
    is_login_form_visible = login_page.is_login_form_visible()

    assert "/login" in current_url, (
        f"로그인 페이지(/login)가 정상적으로 노출되어야 하지만 그렇지 않음 "
        f"(기대: '/login' 포함, 실제: {current_url})"
    )
    assert is_login_form_visible, (
        f'"Login to your account" 영역이 노출되어야 하지만 노출되지 않음 '
        f"(기대: True, 실제: {is_login_form_visible})"
    )


def test_login_with_valid_credentials_lands_on_home(driver):
    """TC-LOGIN-LOGOUT-004: 유효한 계정으로 로그인 성공 시 Home으로 랜딩하고 로그인 상태
    메뉴(Logout/Delete Account)와 "Logged in as {유저명}" 텍스트가 노출된다."""
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    home_page = HomePage(driver)
    current_url = driver.current_url
    is_logged_in_menu_visible = home_page.is_logged_in_menu_visible()
    logged_in_user_text = home_page.get_logged_in_user_text()

    assert current_url == BASE_URL, (
        f"로그인 성공 시 Home({BASE_URL})으로 랜딩해야 하지만 그렇지 않음 "
        f"(기대: {BASE_URL}, 실제: {current_url})"
    )
    assert is_logged_in_menu_visible, (
        f"로그인 상태 메뉴(Logout/Delete Account)가 노출되어야 하지만 노출되지 않음 "
        f"(기대: True, 실제: {is_logged_in_menu_visible})"
    )
    assert "Logged in as" in logged_in_user_text, (
        f'"Logged in as" 텍스트가 노출되어야 하지만 노출되지 않음 '
        f"(기대: 'Logged in as' 포함, 실제: {logged_in_user_text!r})"
    )


def test_login_with_nonexistent_email_shows_error(driver):
    """TC-LOGIN-LOGOUT-005: 존재하지 않는 이메일로 로그인 시도 시 에러 메시지가 노출된다."""
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("notexist_qa_test@test.com", "anyvalue")

    error_message = login_page.get_error_message()
    expected_message = "Your email or password is incorrect!"

    assert error_message == expected_message, (
        f"에러 메시지가 기대값과 다름 (기대: {expected_message!r}, 실제: {error_message!r})"
    )


def test_login_with_wrong_password_shows_same_error(driver):
    """TC-LOGIN-LOGOUT-006: 존재하는 이메일에 잘못된 비밀번호 입력 시 TC-005와 동일한
    에러 메시지가 노출된다(이메일 오류와 구분되지 않음)."""
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], "wrong-password-qa")

    error_message = login_page.get_error_message()
    expected_message = "Your email or password is incorrect!"

    assert error_message == expected_message, (
        f"에러 메시지가 기대값과 다름 (기대: {expected_message!r}, 실제: {error_message!r})"
    )


def test_login_redirects_to_home_when_reentering_login_page(driver):
    """TC-LOGIN-LOGOUT-010: 로그인 상태에서 `/login` URL로 직접 재진입 시 Home으로
    리다이렉트된다(로그인 폼이 노출되지 않음)."""
    _login(driver)

    login_page = LoginPage(driver)
    login_page.navigate()

    current_url = driver.current_url

    assert current_url == BASE_URL, (
        f"로그인 상태에서 /login 재진입 시 Home({BASE_URL})으로 리다이렉트되어야 하지만 "
        f"그렇지 않음 (기대: {BASE_URL}, 실제: {current_url})"
    )


def test_login_state_persists_after_refresh(driver):
    """TC-LOGIN-LOGOUT-011: 로그인 상태에서 새로고침(F5) 후에도 상단 네비게이션이 로그인
    상태 메뉴로 계속 유지된다."""
    _login(driver)

    driver.refresh()

    home_page = HomePage(driver)
    is_logged_in_menu_visible = home_page.is_logged_in_menu_visible()

    assert is_logged_in_menu_visible, (
        f"새로고침 후에도 로그인 상태 메뉴(Logout/Delete Account)가 유지되어야 하지만 "
        f"그렇지 않음 (기대: True, 실제: {is_logged_in_menu_visible})"
    )


def test_logout_via_top_navigation(driver):
    """TC-LOGIN-LOGOUT-014: 상단 네비게이션 "Logout" 클릭 시 로그인 페이지(`/login`)로
    랜딩하고 로그인 폼이 노출된다."""
    _login(driver)

    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_logout()

    login_page = LoginPage(driver)
    login_page.wait_for_url_contains("/login")
    current_url = driver.current_url
    is_login_form_visible = login_page.is_login_form_visible()

    assert "/login" in current_url, (
        f"Logout 클릭 시 로그인 페이지(/login)로 랜딩해야 하지만 그렇지 않음 "
        f"(기대: '/login' 포함, 실제: {current_url})"
    )
    assert is_login_form_visible, (
        f'Logout 후 "Login to your account" 영역이 노출되어야 하지만 노출되지 않음 '
        f"(기대: True, 실제: {is_login_form_visible})"
    )


def test_logout_via_direct_url(driver):
    """TC-LOGIN-LOGOUT-015: 로그인 상태에서 URL(`/logout`) 직접 접근으로도 동일하게
    로그아웃되어 로그인 페이지(`/login`)로 랜딩한다."""
    _login(driver)

    driver.get(BASE_URL + "logout")

    login_page = LoginPage(driver)
    current_url = driver.current_url
    is_login_form_visible = login_page.is_login_form_visible()

    assert "/login" in current_url, (
        f"/logout 직접 접근 시 로그인 페이지(/login)로 랜딩해야 하지만 그렇지 않음 "
        f"(기대: '/login' 포함, 실제: {current_url})"
    )
    assert is_login_form_visible, (
        f'/logout 직접 접근 후 "Login to your account" 영역이 노출되어야 하지만 노출되지 '
        f"않음 (기대: True, 실제: {is_login_form_visible})"
    )


def test_login_with_long_special_char_input_shows_error(driver):
    """TC-LOGIN-LOGOUT-013: 매우 긴 이메일/특수문자 비밀번호 입력 시에도 별도 클라이언트
    제한 없이 동일한 에러 메시지가 노출된다."""
    login_page = LoginPage(driver)
    login_page.navigate()
    long_email = "a" * 100 + "@test.com"
    login_page.login(long_email, "!@#$%^&*()_+" * 5)

    error_message = login_page.get_error_message()
    expected_message = "Your email or password is incorrect!"

    assert error_message == expected_message, (
        f"에러 메시지가 기대값과 다름 (기대: {expected_message!r}, 실제: {error_message!r})"
    )
