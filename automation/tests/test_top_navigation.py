"""상단 네비게이션 "Home"/"Products"/"Cart" 메뉴가 로그인 상태와 무관하게 항상 동일한
URL로 이동하는지, 그리고 여러 페이지를 순회해도 메뉴 구성이 일관되게 유지되는지 검증하는
테스트.

Source of Truth:
- docs/tc/top-navigation.md (TC-TOP-NAVIGATION-001, 002, 003, 004, 005)
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙)

이 파일은 TC-001("Home" 메뉴 클릭 시 항상 Home으로 이동), TC-002("Products" 메뉴 클릭 시
항상 /products로 이동), TC-003("Cart" 메뉴 클릭 시 항상 /view_cart로 이동), TC-004(로그인
상태에서 Home/Products/Cart 페이지를 이동해도 메뉴 구성과 "Logged in as {유저명}" 표시가
동일하게 유지), TC-005(로그아웃 상태에서 동일 페이지를 이동해도 메뉴 구성이 동일하게 유지)를
다룬다.

TC-001~003은 원본 TC 문서의 Test Steps 설계(2단계 순차 검증: 1. 로그아웃 상태 확인 → 2.
유효한 테스트 계정으로 로그인 후 재확인)를 그대로 반영해, 한 테스트 함수 안에서 로그아웃
상태와 로그인 상태를 모두 assert한다.

TC-004/005는 각각 로그인 상태/로그아웃 상태 하나만 다루며(원본 TC 문서 기준), 두 테스트는
서로 독립적으로 자신의 상태를 스스로 셋업한다(AUTOMATION_GUIDE 10절 테스트 독립성).

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(HomePage/ProductsPage/CartPage/
LoginPage)는 화면 조작/조회만 담당한다(Assertion 없음).

민감정보 관리: 고정 계정(actest1)의 비밀번호는 config.accounts.get_account()를 통해
automation/.env(git 미추적)에서만 로드하며, 이 파일 어디에도 실제 비밀번호 값을
하드코딩하지 않는다. 신규 회원가입 없이 기존 고정 계정만 로그인에 사용한다.
"""

from config.accounts import get_account
from config.settings import BASE_URL
from pages.account_created_page import AccountCreatedPage
from pages.cart_page import CartPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.signup_page import SignupPage
from utils.account_factory import generate_signup_data


def test_home_link_navigates_to_home_regardless_of_login_state(driver):
    """TC-TOP-NAVIGATION-001: Products 페이지에서 "Home" 메뉴 클릭 시 로그인 상태와
    무관하게 항상 Home(BASE_URL)으로 이동한다."""
    # 1. 로그아웃 상태로 Products 페이지에 진입해 "Home" 메뉴를 클릭하고 이동 URL을 확인한다.
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.click_home()

    home_page = HomePage(driver)
    home_page.wait_for_url_to_be(BASE_URL)
    current_url_logged_out = driver.current_url

    assert current_url_logged_out == BASE_URL, (
        f"로그아웃 상태에서 'Home' 메뉴 클릭 시 Home({BASE_URL})으로 이동해야 하지만 "
        f"그렇지 않음 (기대: {BASE_URL}, 실제: {current_url_logged_out})"
    )

    # 2. 유효한 테스트 계정으로 로그인한 뒤 Products 페이지로 이동해 "Home" 메뉴를 다시
    #    클릭하고 이동 URL을 확인한다.
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    products_page.navigate()
    products_page.click_home()
    home_page.wait_for_url_to_be(BASE_URL)
    current_url_logged_in = driver.current_url

    assert current_url_logged_in == BASE_URL, (
        f"로그인 상태에서 'Home' 메뉴 클릭 시 Home({BASE_URL})으로 이동해야 하지만 "
        f"그렇지 않음 (기대: {BASE_URL}, 실제: {current_url_logged_in})"
    )


def test_products_link_navigates_to_products_regardless_of_login_state(driver):
    """TC-TOP-NAVIGATION-002: Home 페이지에서 "Products" 메뉴 클릭 시 로그인 상태와
    무관하게 항상 /products로 이동한다."""
    # 1. 로그아웃 상태로 Home 페이지에서 "Products" 메뉴를 클릭하고 이동 URL을 확인한다.
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_products()

    products_page = ProductsPage(driver)
    products_page.wait_for_url_contains("/products")
    current_url_logged_out = driver.current_url

    assert "/products" in current_url_logged_out, (
        f"로그아웃 상태에서 'Products' 메뉴 클릭 시 '/products'로 이동해야 하지만 "
        f"그렇지 않음 (기대: '/products' 포함, 실제: {current_url_logged_out})"
    )

    # 2. 유효한 테스트 계정으로 로그인한 뒤 Home 페이지로 이동해 "Products" 메뉴를 다시
    #    클릭하고 이동 URL을 확인한다.
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    home_page.navigate()
    home_page.click_products()
    products_page.wait_for_url_contains("/products")
    current_url_logged_in = driver.current_url

    assert "/products" in current_url_logged_in, (
        f"로그인 상태에서 'Products' 메뉴 클릭 시 '/products'로 이동해야 하지만 "
        f"그렇지 않음 (기대: '/products' 포함, 실제: {current_url_logged_in})"
    )


def test_cart_link_navigates_to_cart_regardless_of_login_state(driver):
    """TC-TOP-NAVIGATION-003: Home 페이지에서 "Cart" 메뉴 클릭 시 로그인 상태와
    무관하게 항상 /view_cart로 이동한다."""
    # 1. 로그아웃 상태로 Home 페이지에서 "Cart" 메뉴를 클릭하고 이동 URL을 확인한다.
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_cart()

    cart_page = CartPage(driver)
    cart_page.wait_for_url_contains("/view_cart")
    current_url_logged_out = driver.current_url

    assert "/view_cart" in current_url_logged_out, (
        f"로그아웃 상태에서 'Cart' 메뉴 클릭 시 '/view_cart'로 이동해야 하지만 "
        f"그렇지 않음 (기대: '/view_cart' 포함, 실제: {current_url_logged_out})"
    )

    # 2. 유효한 테스트 계정으로 로그인한 뒤 Home 페이지로 이동해 "Cart" 메뉴를 다시
    #    클릭하고 이동 URL을 확인한다.
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    home_page.navigate()
    home_page.click_cart()
    cart_page.wait_for_url_contains("/view_cart")
    current_url_logged_in = driver.current_url

    assert "/view_cart" in current_url_logged_in, (
        f"로그인 상태에서 'Cart' 메뉴 클릭 시 '/view_cart'로 이동해야 하지만 "
        f"그렇지 않음 (기대: '/view_cart' 포함, 실제: {current_url_logged_in})"
    )


def test_nav_menu_consistent_across_pages_when_logged_in(driver):
    """TC-TOP-NAVIGATION-004: 로그인 상태에서 Home→Products→Cart 순으로 이동해도 상단
    네비게이션 메뉴 구성과 "Logged in as {유저명}" 표시가 세 페이지 모두 동일하게
    유지된다."""
    # 0. 유효한 테스트 계정으로 로그인한다.
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    # 1. Home 페이지에서 메뉴 구성과 "Logged in as {유저명}" 표시를 확인한다.
    home_page = HomePage(driver)
    home_page.navigate()
    home_items = home_page.get_nav_menu_item_texts()
    home_user = home_page.get_logged_in_user_text()

    # 2. Products 페이지로 이동해 동일한 항목을 다시 확인한다.
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_items = products_page.get_nav_menu_item_texts()
    products_user = products_page.get_logged_in_user_text()

    # 3. Cart 페이지로 이동해 동일한 항목을 다시 확인한다.
    cart_page = CartPage(driver)
    cart_page.navigate()
    cart_items = cart_page.get_nav_menu_item_texts()
    cart_user = cart_page.get_logged_in_user_text()

    assert home_items == products_items == cart_items, (
        f"로그인 상태에서 Home/Products/Cart 페이지의 상단 네비게이션 메뉴 구성이 동일해야 "
        f"하지만 그렇지 않음 (Home: {home_items}, Products: {products_items}, "
        f"Cart: {cart_items})"
    )

    assert home_user == products_user == cart_user, (
        f"로그인 상태에서 Home/Products/Cart 페이지의 'Logged in as {{유저명}}' 표시가 "
        f"동일해야 하지만 그렇지 않음 (Home: {home_user}, Products: {products_user}, "
        f"Cart: {cart_user})"
    )


def test_nav_menu_consistent_across_pages_when_logged_out(driver):
    """TC-TOP-NAVIGATION-005: 로그아웃 상태에서 Home→Products→Cart 순으로 이동해도 상단
    네비게이션 메뉴 구성이 세 페이지 모두 동일하게 유지된다("Logged in as" 표시는 없음)."""
    # 1. 로그아웃 상태로 Home 페이지에서 메뉴 구성을 확인한다.
    home_page = HomePage(driver)
    home_page.navigate()
    home_items = home_page.get_nav_menu_item_texts()

    # 2. Products 페이지로 이동해 동일한 항목을 다시 확인한다.
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_items = products_page.get_nav_menu_item_texts()

    # 3. Cart 페이지로 이동해 동일한 항목을 다시 확인한다.
    cart_page = CartPage(driver)
    cart_page.navigate()
    cart_items = cart_page.get_nav_menu_item_texts()

    assert home_items == products_items == cart_items, (
        f"로그아웃 상태에서 Home/Products/Cart 페이지의 상단 네비게이션 메뉴 구성이 동일해야 "
        f"하지만 그렇지 않음 (Home: {home_items}, Products: {products_items}, "
        f"Cart: {cart_items})"
    )


def test_logged_in_user_text_matches_signup_name(driver):
    """TC-TOP-NAVIGATION-006: "Logged in as {유저명}"의 유저명이 회원가입 시 입력한 Name
    값과 동일하게 노출되는지 확인한다.

    [설계 판단 - 원본 TC와 다름] 원본 TC-TOP-NAVIGATION-006의 Precondition은 "기존 재사용
    계정(actest1)의 최초 가입 시 Name 값"을 비교 기준으로 전제한다. 하지만 actest1이 실제로
    어떤 Name으로 가입되었는지는 자동화가 통제하지 않는 외부 정보라 알 수 없다. 이에 따라
    Phase 2(signup-delete-account)에서 확립된 회원가입 플로우(test_signup.py의
    `_complete_signup` 패턴)를 그대로 재사용해, 이 테스트가 스스로 신규 계정을 생성하고 그
    계정에 직접 지정한 Name 값과 로그인 후 표시되는 "Logged in as" 텍스트를 비교하는
    자기완결적(self-contained) 방식으로 자동화한다(AUTOMATION_GUIDE 10절 테스트 독립성
    원칙에 부합, 다른 테스트나 외부 계정 정보에 의존하지 않음). "ACCOUNT CREATED!" 페이지의
    "Continue" 클릭 시 방금 생성한 계정으로 자동 로그인되는 동작은 Phase 2 Task 8에서 실측
    확인되었다(test_signup.py의 test_continue_from_account_created_lands_on_home 참고).
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
    logged_in_user_text = home_page.get_logged_in_user_text()

    assert signup_data["name"] in logged_in_user_text, (
        f'"Logged in as" 텍스트에 회원가입 시 입력한 Name이 포함되어야 하지만 그렇지 않음 '
        f"(기대: {signup_data['name']!r} 포함, 실제: {logged_in_user_text!r})"
    )
