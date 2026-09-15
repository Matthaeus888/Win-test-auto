"""각 페이지별 UI(Home/Products/Cart/Signup-Login/Checkout) 화면 구성요소를 검증하는 테스트.

Source of Truth:
- docs/tc/page-ui.md (TC-PAGE-UI-006, 009, 015, 019, 020, 021, 023, 024, 025, 026, 028,
  029, 030, 031, 032, 033, 034, 035, 036, 037, 039 — 총 21건)
- docs/prd/feature/page-ui.md
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙),
  10절(테스트 독립성), 11절(테스트 데이터 관리)

이 파일이 다루는 21건 Approved TC의 화면별 구성:
- Home 페이지: TC-006(FEATURES ITEMS 카드 그리드/구성요소), 009(RECOMMENDED ITEMS 캐러셀
  다음 화살표), 023/024(CATEGORY 아코디언 펼침/단일 오픈), 025(카테고리 하위 메뉴 클릭 시
  이동), 026(브랜드 클릭 시 이동), 028(브랜드 표시 개수와 실제 개수 일치), 029(카테고리
  필터링 정확성), 030(브랜드 필터링 정확성), 031(모든 카테고리/브랜드 최소 1개 이상 상품
  존재, 전수 확인).
- Products 페이지: TC-015(ALL PRODUCTS 카드 그리드), 032/033(좌측 사이드바 CATEGORY
  아코디언 펼침/단일 오픈).
- Cart 페이지: TC-019(빈 카트 안내), 020(Proceed To Checkout 버튼), 021(상품 목록 표
  컬럼/삭제 버튼).
- Checkout 페이지(`/checkout`, 로그인 상태 + 장바구니 상품 1개 이상 전제): TC-034(Address
  Details 영역 노출), 035(주소 자동 채움), 036(Review Your Order 표 컬럼), 037(Total
  Amount 노출), 039(Place Order 버튼 노출).

[Checkout 진입 방식] `/checkout`은 반드시 `CartPage.click_proceed_to_checkout()`으로
진입한다. `driver.get()`으로 직접 접근하면 Review Your Order 표/Total Amount가 비정상적으로
비어 보이는 현상이 실측으로 확인되었다(`pages/checkout_page.py` docstring "Phase 7 확장"
참고).

[TC-034/036/037/039 계정 배정] 4개 TC 모두 "로그인 + 장바구니 상품 1개 이상" 상태가
필요하며, 동일한 고정 계정을 여러 TC가 공유하면 실행 순서에 따라 장바구니 상태 의존성이
생길 수 있다(AUTOMATION_GUIDE 10절 테스트 독립성). `test_cart.py`와 동일한 설계로 서로 다른
고정 계정을 배정하고(TC-034/039: actest1, TC-036: actest2, TC-037: actest3), 각 테스트는
`try`/`finally`로 자신이 추가한 상품을 장바구니에서 삭제해 정리한다.

[TC-035 테스트 데이터] 원본 TC의 Precondition은 "기존 재사용 계정(actest1)의 최초 가입 시
이름/주소 정보"를 비교 기준으로 전제하지만, 그 값은 자동화가 통제하지 않는 외부 정보라 알 수
없다. `test_top_navigation.py`의 TC-TOP-NAVIGATION-006과 동일한 설계 판단에 따라, 이
테스트가 스스로 신규 계정을 생성(Phase 2 `utils/account_factory.py` 재사용)하고 그 계정에
직접 지정한 이름/주소 값과 Checkout에 자동 표시된 값을 비교하는 자기완결적(self-contained)
방식으로 자동화한다(AUTOMATION_GUIDE 10절 테스트 독립성 원칙에 부합). 생성한 계정은 테스트
종료 시 "Delete Account"로 정리한다(AUTOMATION_GUIDE 11.2절 "생성한 계정을 테스트 내에서
정리할 수 있는 경우, 가능한 범위에서 정리").

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(HomePage/ProductsPage/CartPage/
CheckoutPage/CategoryProductsPage/BrandProductsPage/ProductDetailPage/LoginPage/
SignupPage/AccountCreatedPage/AccountDeletedPage/AddToCartModal)는 화면 조작/조회만
담당한다(Assertion 없음).

민감정보 관리: 고정 계정(actest1~3)의 비밀번호는 `config.accounts.get_account()`를 통해
`automation/.env`(git 미추적)에서만 로드하며, 이 파일 어디에도 실제 비밀번호 값을
하드코딩하지 않는다. TC-035에서 생성하는 신규 계정의 비밀번호는 `utils/account_factory.
generate_signup_data()`가 매 실행마다 동적으로 생성하는 테스트 전용 더미 값이다.
"""

import logging
import re
from typing import Optional

from config.accounts import get_account
from config.settings import BASE_URL
from pages.account_created_page import AccountCreatedPage
from pages.account_deleted_page import AccountDeletedPage
from pages.add_to_cart_modal import AddToCartModal
from pages.brand_products_page import BrandProductsPage
from pages.cart_page import CartPage
from pages.category_products_page import CategoryProductsPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_detail_page import ProductDetailPage
from pages.products_page import ProductsPage
from pages.signup_page import SignupPage
from utils.account_factory import generate_signup_data
from utils.text import normalize_whitespace

logger = logging.getLogger(__name__)


def _cleanup_cart_item(cart_page: CartPage, product_name: Optional[str]) -> None:
    """테스트가 로그인 계정 장바구니에 추가한 상품을 정리한다.

    `test_cart.py`의 동일 이름 헬퍼와 같은 목적/구현이며, Test Layer 전용 로직이라 Feature
    단위(파일 단위)로 각자 국소적으로 유지한다(AUTOMATION_GUIDE 19절 "특정 Feature 하나에서만
    쓰이는 로직을 섣불리 공통화하지 않는다" - 이 프로젝트에서 이미 Test 파일마다 유사한
    로그인/담기 플로우를 각자 재구현해온 기존 관례와 일관성을 맞춤, `test_top_navigation.py`의
    TC-006이 `test_signup.py`의 가입 플로우를 재구현한 것과 동일한 판단).

    `finally` 블록에서만 호출되는 정리 전용 로직이므로, 정리 자체가 실패해도 예외를
    전파하지 않고 경고 로그만 남긴다(원래 assertion 실패를 덮어쓰지 않기 위함).
    """
    if product_name is None:
        return
    try:
        cart_page.navigate()
        names_before = cart_page.get_product_names()
        normalized_names_before = [normalize_whitespace(n) for n in names_before]
        if normalize_whitespace(product_name) not in normalized_names_before:
            return
        cart_page.delete_product_by_name(product_name)
        cart_page.wait_for_cart_row_count(len(names_before) - 1)
    except Exception:
        logger.warning(
            "테스트 정리(cleanup) 중 장바구니 상품 삭제에 실패함(수동 확인 필요): %s",
            product_name,
            exc_info=True,
        )


def _login(driver, account_name: str) -> dict:
    """고정 계정으로 로그인하고 Home으로 이동 완료를 대기한 뒤 계정 정보를 반환한다."""
    account = get_account(account_name)
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)
    return account


def _clear_cart(driver) -> None:
    """로그인 계정의 장바구니에 남아있는 모든 상품을 삭제해 빈 상태로 만든다.

    [pytest 실행 중 재현·확인] 고정 계정(actest1~3)은 Production 단일 환경에서
    Phase 5(cart)를 포함한 이전 실행들이 재사용해온 계정이며, `_cleanup_cart_item()`이
    각 테스트가 추가한 상품은 정리하지만 그 이전에 이미 남아있던 leftover 데이터까지
    보장하지는 않는다. 실제로 `actest2` 계정 장바구니에 이 Phase의 테스트가 추가하기 전부터
    상품 1개가 이미 남아있어 "장바구니 상품 1개" 전제가 깨지는 현상이 재현되었다(Test Data
    문제로 분류, Automation Code 자체의 결함은 아님). 로그인 직후 이 헬퍼로 장바구니를
    항상 빈 상태로 정리한 뒤 테스트 자신의 상품만 담아 전제 조건을 자기완결적으로
    보장한다(AUTOMATION_GUIDE 10절 테스트 독립성).
    """
    cart_page = CartPage(driver)
    cart_page.navigate()
    names = cart_page.get_product_names()
    if not names:
        return
    for name in names:
        current_count = cart_page.get_cart_row_count()
        cart_page.delete_product_by_name(name)
        cart_page.wait_for_cart_row_count(current_count - 1)
    logger.info("로그인 계정 장바구니에 남아있던 leftover 상품 %s건 정리 완료", len(names))


def _add_first_product_to_cart(driver) -> str:
    """Products 페이지 첫 번째 상품을 장바구니에 담고 담긴 상품명을 반환한다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    product_name = products_page.get_product_names()[0]
    products_page.click_add_to_cart_on_card(0)
    AddToCartModal(driver).click_continue_shopping()
    return product_name


def _go_to_checkout(driver) -> CheckoutPage:
    """Cart 페이지에서 "Proceed To Checkout"을 클릭해 `/checkout`으로 진입한다(위 파일
    docstring "Checkout 진입 방식" 참고, `driver.get()` 직접 접근 금지)."""
    cart_page = CartPage(driver)
    cart_page.navigate()
    cart_page.click_proceed_to_checkout()
    checkout_page = CheckoutPage(driver)
    checkout_page.wait_for_url_contains("/checkout")
    return checkout_page


# ---------------------------------------------------------------------------
# Home 페이지 - FEATURES ITEMS 그리드 / RECOMMENDED ITEMS 캐러셀
# ---------------------------------------------------------------------------


def test_features_items_grid_shows_three_column_layout_with_card_details(driver):
    """TC-PAGE-UI-006: Home 페이지 "FEATURES ITEMS" 섹션이 한 행 3개 카드 그리드 형태로
    노출되고, 각 카드에 이미지/가격(Rs. 단위)/상품명/Add to cart/View Product가 모두
    노출된다."""
    home_page = HomePage(driver)
    home_page.navigate()

    card_count = home_page.get_product_card_count()
    assert card_count > 0, (
        f"FEATURES ITEMS 섹션에 상품 카드가 1개 이상 노출되어야 하지만 그렇지 않음 "
        f"(기대: >0, 실제: {card_count})"
    )

    is_three_column = home_page.is_cards_in_three_column_grid()
    assert is_three_column is True, (
        f"모든 상품 카드가 한 행 3개 그리드 클래스(col-sm-4)를 가져야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_three_column})"
    )

    price = home_page.get_product_price_on_card(0)
    assert price.startswith("Rs."), (
        f"카드 가격이 'Rs.' 단위로 노출되어야 하지만 그렇지 않음 (실제: {price!r})"
    )

    name = home_page.get_product_names()[0]
    assert name, f"카드 상품명이 비어있지 않아야 하지만 그렇지 않음 (실제: {name!r})"

    is_image_visible = home_page.is_image_visible_on_card(0)
    assert is_image_visible is True, (
        f"카드 상품 이미지가 노출되어야 하지만 그렇지 않음 (기대: True, 실제: {is_image_visible})"
    )

    is_add_to_cart_visible = home_page.is_add_to_cart_visible_on_card(0)
    assert is_add_to_cart_visible is True, (
        f"카드 'Add to cart' 버튼이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_add_to_cart_visible})"
    )

    is_view_product_visible = home_page.is_view_product_visible_on_card(0)
    assert is_view_product_visible is True, (
        f"카드 'View Product' 링크가 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_view_product_visible})"
    )


def test_recommended_items_carousel_changes_on_next_arrow_click(driver):
    """TC-PAGE-UI-009: "RECOMMENDED ITEMS" 캐러셀의 오른쪽(다음) 화살표 클릭 시 노출
    상품이 즉시 전환된다."""
    home_page = HomePage(driver)
    home_page.navigate()

    initial_name = home_page.get_recommended_item_active_name()
    home_page.click_recommended_items_next()
    new_name = home_page.wait_for_recommended_item_active_name_change(initial_name)

    assert new_name != initial_name, (
        f"다음 화살표 클릭 시 노출 상품이 전환되어야 하지만 그렇지 않음 "
        f"(전환 전: {initial_name!r}, 전환 후: {new_name!r})"
    )


# ---------------------------------------------------------------------------
# Products 페이지 - ALL PRODUCTS 그리드
# ---------------------------------------------------------------------------


def test_all_products_grid_shows_card_with_full_info(driver):
    """TC-PAGE-UI-015: Products 페이지 "ALL PRODUCTS" 섹션이 Home 페이지 FEATURES ITEMS와
    동일한 카드 그리드 구조(이미지/가격/상품명/Add to cart/View Product)로 노출된다."""
    products_page = ProductsPage(driver)
    products_page.navigate()

    card_count = products_page.get_product_card_count()
    assert card_count > 0, (
        f"ALL PRODUCTS 섹션에 상품 카드가 1개 이상 노출되어야 하지만 그렇지 않음 "
        f"(기대: >0, 실제: {card_count})"
    )

    price = products_page.get_product_price_on_card(0)
    assert price.startswith("Rs."), (
        f"카드 가격이 'Rs.' 단위로 노출되어야 하지만 그렇지 않음 (실제: {price!r})"
    )

    name = products_page.get_product_names()[0]
    assert name, f"카드 상품명이 비어있지 않아야 하지만 그렇지 않음 (실제: {name!r})"

    is_image_visible = products_page.is_image_visible_on_card(0)
    assert is_image_visible is True, (
        f"카드 상품 이미지가 노출되어야 하지만 그렇지 않음 (기대: True, 실제: {is_image_visible})"
    )

    is_add_to_cart_visible = products_page.is_add_to_cart_visible_on_card(0)
    assert is_add_to_cart_visible is True, (
        f"카드 'Add to cart' 버튼이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_add_to_cart_visible})"
    )

    is_view_product_visible = products_page.is_view_product_visible_on_card(0)
    assert is_view_product_visible is True, (
        f"카드 'View Product' 링크가 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_view_product_visible})"
    )


# ---------------------------------------------------------------------------
# CATEGORY 아코디언 (Home/Products 공통)
# ---------------------------------------------------------------------------


def test_home_category_accordion_expands_submenu_on_click(driver):
    """TC-PAGE-UI-023: Home 페이지 CATEGORY 아코디언에서 "WOMEN" 클릭 시 하위 메뉴
    (DRESS, TOPS & SHIRTS, SAREE 등)가 펼쳐진다."""
    home_page = HomePage(driver)
    home_page.navigate()

    home_page.click_category("WOMEN")
    home_page.wait_for_category_submenu_state("WOMEN", True)
    is_expanded = home_page.is_category_submenu_expanded("WOMEN")
    assert is_expanded is True, (
        f"'WOMEN' 클릭 시 하위 메뉴가 펼쳐져야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_expanded})"
    )

    sublinks = home_page.get_category_submenu_link_texts("WOMEN")
    # 실측 결과 하위 메뉴 텍스트는 CSS text-transform: uppercase로 렌더링되어 Selenium
    # `.text`(렌더링된 화면 텍스트 기준)가 대문자로 반환됨을 확인했다(pytest 실행으로
    # 재현·확인, 원본 DOM 텍스트는 "Dress"/"Tops"/"Saree"이지만 이 사이트 CSS로 인해
    # 화면에는 대문자로 보이고 Selenium도 이를 그대로 반환함).
    for expected in ("DRESS", "TOPS", "SAREE"):
        assert expected in sublinks, (
            f"'WOMEN' 하위 메뉴에 {expected!r}가 포함되어야 하지만 그렇지 않음 "
            f"(실제 하위 메뉴: {sublinks})"
        )


def test_home_category_accordion_single_open_closes_previous(driver):
    """TC-PAGE-UI-024: Home 페이지 CATEGORY 아코디언에서 "WOMEN"을 펼친 뒤 "MEN"을 클릭하면
    "MEN" 하위 메뉴가 펼쳐지고 "WOMEN" 하위 메뉴는 닫힌다(단일 오픈)."""
    home_page = HomePage(driver)
    home_page.navigate()

    home_page.click_category("WOMEN")
    home_page.wait_for_category_submenu_state("WOMEN", True)
    assert home_page.is_category_submenu_expanded("WOMEN") is True, (
        "사전 조건: 'WOMEN' 하위 메뉴가 먼저 펼쳐져 있어야 함"
    )

    home_page.click_category("MEN")
    home_page.wait_for_category_submenu_state("MEN", True)
    home_page.wait_for_category_submenu_state("WOMEN", False)
    is_men_expanded = home_page.is_category_submenu_expanded("MEN")
    is_women_expanded = home_page.is_category_submenu_expanded("WOMEN")

    assert is_men_expanded is True, (
        f"'MEN' 클릭 시 하위 메뉴가 펼쳐져야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_men_expanded})"
    )
    assert is_women_expanded is False, (
        f"'MEN' 클릭 시 이전에 펼쳐져 있던 'WOMEN' 하위 메뉴는 닫혀야 하지만 그렇지 않음 "
        f"(기대: False, 실제: {is_women_expanded})"
    )


def test_products_category_accordion_expands_submenu_on_click(driver):
    """TC-PAGE-UI-032: Products 페이지 좌측 사이드바 CATEGORY 아코디언에서 "WOMEN" 클릭 시
    하위 메뉴가 펼쳐진다."""
    products_page = ProductsPage(driver)
    products_page.navigate()

    products_page.click_category("WOMEN")
    products_page.wait_for_category_submenu_state("WOMEN", True)
    is_expanded = products_page.is_category_submenu_expanded("WOMEN")
    assert is_expanded is True, (
        f"'WOMEN' 클릭 시 하위 메뉴가 펼쳐져야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_expanded})"
    )


def test_products_category_accordion_single_open_closes_previous(driver):
    """TC-PAGE-UI-033: Products 페이지 좌측 사이드바에서 "WOMEN"을 펼친 뒤 "MEN"을 클릭하면
    "MEN" 하위 메뉴가 펼쳐지고 "WOMEN" 하위 메뉴는 닫힌다(단일 오픈)."""
    products_page = ProductsPage(driver)
    products_page.navigate()

    products_page.click_category("WOMEN")
    products_page.wait_for_category_submenu_state("WOMEN", True)
    assert products_page.is_category_submenu_expanded("WOMEN") is True, (
        "사전 조건: 'WOMEN' 하위 메뉴가 먼저 펼쳐져 있어야 함"
    )

    products_page.click_category("MEN")
    products_page.wait_for_category_submenu_state("MEN", True)
    products_page.wait_for_category_submenu_state("WOMEN", False)
    is_men_expanded = products_page.is_category_submenu_expanded("MEN")
    is_women_expanded = products_page.is_category_submenu_expanded("WOMEN")

    assert is_men_expanded is True, (
        f"'MEN' 클릭 시 하위 메뉴가 펼쳐져야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_men_expanded})"
    )
    assert is_women_expanded is False, (
        f"'MEN' 클릭 시 이전에 펼쳐져 있던 'WOMEN' 하위 메뉴는 닫혀야 하지만 그렇지 않음 "
        f"(기대: False, 실제: {is_women_expanded})"
    )


# ---------------------------------------------------------------------------
# CATEGORY/BRANDS 클릭 이동 및 필터링 정확성
# ---------------------------------------------------------------------------


def test_category_submenu_click_navigates_to_category_products_page(driver):
    """TC-PAGE-UI-025: CATEGORY 하위 메뉴("MEN" > "Jeans") 클릭 시 해당 카테고리 상품 목록
    페이지(`/category_products/{id}`)로 이동하며, 브레드크럼/제목/상품 그리드가 노출된다."""
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_category("MEN")
    home_page.wait_for_category_submenu_state("MEN", True)
    # CSS text-transform: uppercase로 렌더링되어 Selenium이 반환하는 링크 텍스트는
    # 대문자("JEANS")이다(위 test_home_category_accordion_expands_submenu_on_click의
    # 동일 근거 참고).
    home_page.click_category_submenu_link("MEN", "JEANS")

    category_page = CategoryProductsPage(driver)
    category_page.wait_for_url_contains("/category_products/")
    current_url = driver.current_url
    assert "/category_products/" in current_url, (
        f"'/category_products/{{id}}' 형태의 URL로 이동해야 하지만 그렇지 않음 "
        f"(실제: {current_url})"
    )

    breadcrumb = category_page.get_breadcrumb_texts()
    assert breadcrumb == ["Products", "Men > Jeans"], (
        f"브레드크럼이 ['Products', 'Men > Jeans']이어야 하지만 그렇지 않음 "
        f"(실제: {breadcrumb})"
    )

    # [pytest 실행 중 재현·확인] 제목 일부 단어("PRODUCTS")에만 CSS로 대문자 렌더링이
    # 적용되어("Men - Jeans PRODUCTS") Selenium 렌더링 텍스트 기준으로는 대소문자가
    # 혼재되므로, 대소문자를 무시하고 비교한다(공백 정규화 후 대문자 통일 비교).
    title = normalize_whitespace(category_page.get_title_text()).upper()
    assert title == "MEN - JEANS PRODUCTS", (
        f"제목이 'Men - Jeans Products'(공백/대소문자 정규화 후)이어야 하지만 그렇지 않음 "
        f"(실제: {title!r})"
    )

    card_count = category_page.get_product_card_count()
    assert card_count > 0, (
        f"카테고리 상품 그리드에 상품이 1개 이상 노출되어야 하지만 그렇지 않음 "
        f"(기대: >0, 실제: {card_count})"
    )


def test_brand_click_navigates_to_brand_products_page(driver):
    """TC-PAGE-UI-026: "BRANDS" 목록의 브랜드명("H&M") 클릭 시 해당 브랜드 상품 목록
    페이지(`/brand_products/{브랜드명}`)로 이동하며, 브레드크럼/제목/상품 그리드가
    노출된다."""
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_brand("H&M")

    brand_page = BrandProductsPage(driver)
    brand_page.wait_for_url_contains("/brand_products/")
    current_url = driver.current_url
    assert "/brand_products/H&M" in current_url, (
        f"'/brand_products/H&M' 형태의 URL로 이동해야 하지만 그렇지 않음 (실제: {current_url})"
    )

    breadcrumb = brand_page.get_breadcrumb_texts()
    assert breadcrumb == ["Products", "H&M"], (
        f"브레드크럼이 ['Products', 'H&M']이어야 하지만 그렇지 않음 (실제: {breadcrumb})"
    )

    # 카테고리 페이지와 동일하게 제목 일부 단어에만 CSS 대문자 렌더링이 적용될 수 있어(위
    # test_category_submenu_click_navigates_to_category_products_page 참고) 대소문자를
    # 무시하고 비교한다.
    title = normalize_whitespace(brand_page.get_title_text()).upper()
    assert title == "BRAND - H&M PRODUCTS", (
        f"제목이 'Brand - H&M Products'(공백/대소문자 정규화 후)이어야 하지만 그렇지 않음 "
        f"(실제: {title!r})"
    )

    card_count = brand_page.get_product_card_count()
    assert card_count > 0, (
        f"브랜드 상품 그리드에 상품이 1개 이상 노출되어야 하지만 그렇지 않음 "
        f"(기대: >0, 실제: {card_count})"
    )


def test_brand_product_count_matches_displayed_count(driver):
    """TC-PAGE-UI-028: BRANDS 섹션에 표시된 브랜드별 괄호 숫자가 해당 브랜드 상품 목록
    페이지의 실제 노출 개수와 일치한다."""
    home_page = HomePage(driver)
    home_page.navigate()
    brand_link_texts = home_page.get_brand_link_texts()
    assert brand_link_texts, "BRANDS 목록이 비어있지 않아야 함(사전 조건)"

    # [pytest 실행 중 재현·확인] 괄호 개수(`<span class="pull-right">`)가 float 배치되어
    # Selenium 렌더링 텍스트에서는 "(6)POLO"가 아니라 "(6)\nPOLO"처럼 줄바꿈으로 분리되어
    # 반환됨을 확인했다(원본 DOM `textContent`는 줄바꿈 없이 "(6)Polo"). `re.DOTALL`로
    # 줄바꿈도 매칭하고 이름 부분은 앞뒤 공백/줄바꿈을 추가로 정리한다.
    match = re.match(r"^\((\d+)\)(.+)$", brand_link_texts[0], re.DOTALL)
    assert match, f"BRANDS 목록 텍스트 형식이 예상과 다름 (실제: {brand_link_texts[0]!r})"
    expected_count = int(match.group(1))
    brand_name = match.group(2).strip()

    home_page.click_brand(brand_name)
    brand_page = BrandProductsPage(driver)
    brand_page.wait_for_url_contains("/brand_products/")
    actual_count = brand_page.get_product_card_count()

    assert actual_count == expected_count, (
        f"BRANDS 섹션 표시 개수({expected_count})와 '{brand_name}' 상품 목록 페이지의 실제 "
        f"노출 개수가 일치해야 하지만 그렇지 않음 (기대: {expected_count}, 실제: {actual_count})"
    )


def test_category_products_page_shows_only_matching_category(driver):
    """TC-PAGE-UI-029: CATEGORY 클릭으로 이동한 상품 목록 페이지("MEN" > "Jeans")에
    노출되는 모든 상품이 실제로 해당 카테고리에 속한다(무관한 카테고리 상품이 섞여 노출되지
    않음)."""
    category_page = CategoryProductsPage(driver)
    category_page.navigate(6)  # Men > Jeans (Home 페이지 아코디언 실측으로 확인된 id)

    breadcrumb = category_page.get_breadcrumb_texts()
    expected_category = breadcrumb[-1]  # 예: "Men > Jeans"

    product_ids = category_page.get_product_detail_ids()
    assert product_ids, "카테고리 상품 목록 페이지에 상품이 1개 이상 있어야 함(사전 조건)"

    detail_page = ProductDetailPage(driver)
    for product_id in product_ids:
        detail_page.navigate(product_id)
        category_text = detail_page.get_category_text()
        assert expected_category in category_text, (
            f"상품 id {product_id}의 카테고리({category_text!r})에 선택한 카테고리 "
            f"({expected_category!r})가 포함되어야 하지만 그렇지 않음"
        )


def test_brand_products_page_shows_only_matching_brand(driver):
    """TC-PAGE-UI-030: BRANDS 클릭으로 이동한 상품 목록 페이지("H&M")에 노출되는 모든 상품이
    실제로 해당 브랜드에 해당한다(무관한 브랜드 상품이 섞여 노출되지 않음)."""
    brand_name = "H&M"
    brand_page = BrandProductsPage(driver)
    brand_page.navigate(brand_name)

    product_ids = brand_page.get_product_detail_ids()
    assert product_ids, "브랜드 상품 목록 페이지에 상품이 1개 이상 있어야 함(사전 조건)"

    detail_page = ProductDetailPage(driver)
    for product_id in product_ids:
        detail_page.navigate(product_id)
        brand_text = detail_page.get_brand_text()
        assert brand_name in brand_text, (
            f"상품 id {product_id}의 브랜드({brand_text!r})에 선택한 브랜드({brand_name!r})가 "
            f"포함되어야 하지만 그렇지 않음"
        )


def test_all_categories_and_brands_have_at_least_one_product(driver):
    """TC-PAGE-UI-031: 모든 CATEGORY 하위 카테고리와 BRANDS 항목에 최소 1개 이상의 상품이
    존재하며 0개로 노출되는 항목이 없다(전수 확인)."""
    home_page = HomePage(driver)
    home_page.navigate()

    category_page = CategoryProductsPage(driver)
    for category_name in ("WOMEN", "MEN", "KIDS"):
        home_page.click_category(category_name)
        home_page.wait_for_category_submenu_state(category_name, True)
        sublinks = home_page.get_category_submenu_links(category_name)
        assert sublinks, f"'{category_name}' 카테고리에 하위 메뉴가 1개 이상 있어야 함"
        for link_text, category_id in sublinks:
            category_page.navigate(category_id)
            count = category_page.get_product_card_count()
            assert count >= 1, (
                f"카테고리 '{category_name} > {link_text}'(id={category_id})에 상품이 "
                f"1개 이상 노출되어야 하지만 그렇지 않음 (기대: >=1, 실제: {count})"
            )

    # href에서 원본 대소문자 그대로의 브랜드명을 추출한다(get_brand_link_texts()가 반환하는
    # CSS 대문자 렌더링 텍스트를 그대로 사용하면 BrandProductsPage.navigate()가 원본
    # 대소문자만 인식하는 실제 사이트에서 0건으로 조회되는 문제가 pytest 실행으로 확인됨,
    # home_page.py의 get_brand_names_from_href() docstring 참고).
    brand_names = home_page.get_brand_names_from_href()
    assert brand_names, "BRANDS 목록이 비어있지 않아야 함(사전 조건)"

    brand_page = BrandProductsPage(driver)
    for brand_name in brand_names:
        brand_page.navigate(brand_name)
        count = brand_page.get_product_card_count()
        assert count >= 1, (
            f"브랜드 '{brand_name}'에 상품이 1개 이상 노출되어야 하지만 그렇지 않음 "
            f"(기대: >=1, 실제: {count})"
        )


# ---------------------------------------------------------------------------
# Cart 페이지 - 빈 카트 안내 / Proceed To Checkout / 상품 목록 표 컬럼
# ---------------------------------------------------------------------------


def test_empty_cart_shows_guidance_message_and_link(driver):
    """TC-PAGE-UI-019: 장바구니가 비어있는 상태에서 안내 문구와 "here" 링크가 노출된다."""
    cart_page = CartPage(driver)
    cart_page.navigate()

    is_message_visible = cart_page.is_empty_cart_message_visible()
    assert is_message_visible is True, (
        f"빈 카트 안내 문구가 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_message_visible})"
    )

    message = cart_page.get_empty_cart_message_text()
    assert "Cart is empty!" in message, (
        f"안내 문구에 'Cart is empty!'가 포함되어야 하지만 그렇지 않음 (실제: {message!r})"
    )
    assert "here" in message and "buy products" in message, (
        f"안내 문구에 'here'/'buy products' 관련 텍스트가 포함되어야 하지만 그렇지 않음 "
        f"(실제: {message!r})"
    )

    is_link_visible = cart_page.is_empty_cart_link_visible()
    assert is_link_visible is True, (
        f"'here' 링크가 노출되어야 하지만 그렇지 않음 (기대: True, 실제: {is_link_visible})"
    )

    link_text = cart_page.get_empty_cart_link_text()
    assert link_text == "here", (
        f"링크 텍스트가 'here'이어야 하지만 그렇지 않음 (기대: 'here', 실제: {link_text!r})"
    )


def test_cart_shows_proceed_to_checkout_button_when_items_present(driver):
    """TC-PAGE-UI-020: 장바구니에 상품이 담긴 상태에서 화면 우측 상단에 "Proceed To
    Checkout" 버튼이 노출된다."""
    _add_first_product_to_cart(driver)

    cart_page = CartPage(driver)
    cart_page.navigate()
    is_visible = cart_page.is_proceed_to_checkout_button_visible()
    assert is_visible is True, (
        f"'Proceed To Checkout' 버튼이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_visible})"
    )


def test_cart_shows_table_columns_and_delete_button_when_items_present(driver):
    """TC-PAGE-UI-021: 장바구니에 상품이 담긴 상태에서 상품 목록 표의 컬럼(Item/
    Description/Price/Quantity/Total)과 삭제(x) 아이콘 버튼이 올바르게 노출된다."""
    product_name = _add_first_product_to_cart(driver)

    cart_page = CartPage(driver)
    cart_page.navigate()

    row_count = cart_page.get_cart_row_count()
    assert row_count == 1, (
        f"장바구니에 담은 상품 1개가 행 1개로 노출되어야 하지만 그렇지 않음 "
        f"(기대: 1, 실제: {row_count})"
    )

    is_image_visible = cart_page.is_row_image_visible(product_name)
    assert is_image_visible is True, (
        f"'Item' 컬럼(이미지)이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_image_visible})"
    )

    cart_names = [normalize_whitespace(name) for name in cart_page.get_product_names()]
    assert normalize_whitespace(product_name) in cart_names, (
        f"'Description' 컬럼에 담은 상품명({product_name!r})이 노출되어야 하지만 그렇지 않음 "
        f"(실제: {cart_names})"
    )

    category_path = cart_page.get_category_path_by_product_name(product_name)
    assert " > " in category_path, (
        f"'Description' 컬럼에 카테고리 경로(예: 'Women > Tops')가 노출되어야 하지만 "
        f"그렇지 않음 (실제: {category_path!r})"
    )

    quantity = cart_page.get_quantity_by_product_name(product_name)
    assert quantity, f"'Quantity' 컬럼이 노출되어야 하지만 그렇지 않음 (실제: {quantity!r})"

    total = cart_page.get_total_by_product_name(product_name)
    assert total.startswith("Rs."), (
        f"'Total' 컬럼이 'Rs.' 단위로 노출되어야 하지만 그렇지 않음 (실제: {total!r})"
    )

    is_delete_visible = cart_page.is_delete_button_visible_by_product_name(product_name)
    assert is_delete_visible is True, (
        f"각 행 맨 끝에 삭제(x) 아이콘 버튼이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_delete_visible})"
    )


# ---------------------------------------------------------------------------
# Checkout 페이지 - Address Details / Review Your Order / Total Amount / Place Order
# ---------------------------------------------------------------------------


def test_checkout_shows_address_details_section(driver):
    """TC-PAGE-UI-034: 로그인 상태로 장바구니에 상품이 담긴 채 `/checkout` 페이지 진입 시
    "Address Details" 영역(Delivery/Billing Address)이 노출된다."""
    _login(driver, "actest1")
    _clear_cart(driver)

    cart_page = CartPage(driver)
    product_name = None
    try:
        product_name = _add_first_product_to_cart(driver)
        checkout_page = _go_to_checkout(driver)

        is_heading_visible = checkout_page.is_address_details_heading_visible()
        assert is_heading_visible is True, (
            f"'Address Details' 섹션 제목이 노출되어야 하지만 그렇지 않음 "
            f"(기대: True, 실제: {is_heading_visible})"
        )

        is_delivery_visible = checkout_page.is_delivery_address_visible()
        assert is_delivery_visible is True, (
            f"'Your Delivery Address' 영역이 노출되어야 하지만 그렇지 않음 "
            f"(기대: True, 실제: {is_delivery_visible})"
        )

        is_billing_visible = checkout_page.is_billing_address_visible()
        assert is_billing_visible is True, (
            f"'Your Billing Address' 영역이 노출되어야 하지만 그렇지 않음 "
            f"(기대: True, 실제: {is_billing_visible})"
        )
    finally:
        _cleanup_cart_item(cart_page, product_name)


def test_checkout_review_your_order_table_shows_cart_columns(driver):
    """TC-PAGE-UI-036: Address Details 영역 아래 "Review Your Order" 영역에 Cart 페이지와
    동일한 컬럼 구성(Item/Description/Price/Quantity/Total)의 상품 목록 표가 노출된다."""
    _login(driver, "actest2")
    _clear_cart(driver)

    cart_page = CartPage(driver)
    product_name = None
    try:
        product_name = _add_first_product_to_cart(driver)
        checkout_page = _go_to_checkout(driver)

        is_heading_visible = checkout_page.is_review_order_heading_visible()
        assert is_heading_visible is True, (
            f"'Review Your Order' 섹션 제목이 노출되어야 하지만 그렇지 않음 "
            f"(기대: True, 실제: {is_heading_visible})"
        )

        row_count = checkout_page.get_review_order_row_count()
        assert row_count == 1, (
            f"장바구니에 담은 상품 1개가 표 행 1개로 노출되어야 하지만 그렇지 않음 "
            f"(기대: 1, 실제: {row_count})"
        )

        are_columns_visible = checkout_page.is_review_order_first_row_columns_visible()
        assert are_columns_visible is True, (
            f"Item/Description/Price/Quantity/Total 5개 컬럼이 모두 노출되어야 하지만 "
            f"그렇지 않음 (기대: True, 실제: {are_columns_visible})"
        )
    finally:
        _cleanup_cart_item(cart_page, product_name)


def test_checkout_shows_total_amount_below_review_order_table(driver):
    """TC-PAGE-UI-037: "Review Your Order" 표 하단에 Total Amount(합계 금액)가 노출된다."""
    _login(driver, "actest3")
    _clear_cart(driver)

    cart_page = CartPage(driver)
    product_name = None
    try:
        product_name = _add_first_product_to_cart(driver)
        checkout_page = _go_to_checkout(driver)

        is_visible = checkout_page.is_total_amount_visible()
        assert is_visible is True, (
            f"Total Amount가 노출되어야 하지만 그렇지 않음 (기대: True, 실제: {is_visible})"
        )

        total_amount_text = checkout_page.get_total_amount_text()
        assert total_amount_text.startswith("Rs."), (
            f"Total Amount가 'Rs.' 단위로 노출되어야 하지만 그렇지 않음 "
            f"(실제: {total_amount_text!r})"
        )
    finally:
        _cleanup_cart_item(cart_page, product_name)


def test_checkout_shows_place_order_button(driver):
    """TC-PAGE-UI-039: `/checkout` 페이지 하단에 "Place Order" 버튼이 노출된다."""
    _login(driver, "actest1")
    _clear_cart(driver)

    cart_page = CartPage(driver)
    product_name = None
    try:
        product_name = _add_first_product_to_cart(driver)
        checkout_page = _go_to_checkout(driver)

        is_visible = checkout_page.is_place_order_button_visible()
        assert is_visible is True, (
            f"'Place Order' 버튼이 노출되어야 하지만 그렇지 않음 "
            f"(기대: True, 실제: {is_visible})"
        )
    finally:
        _cleanup_cart_item(cart_page, product_name)


def test_checkout_address_details_auto_filled_from_signup_data(driver):
    """TC-PAGE-UI-035: Address Details의 Delivery/Billing Address에 회원가입 시 입력한
    이름/주소 정보가 자동으로 채워져 표시된다.

    [설계 판단 - 원본 TC와 다름] 위 파일 docstring "TC-035 테스트 데이터" 참고 - 기존
    재사용 계정(actest1)의 최초 가입 정보에 의존하지 않고, 이 테스트가 스스로 신규 계정을
    생성해 자기완결적으로 비교한다.
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

    cart_page = CartPage(driver)
    product_name = None
    try:
        product_name = _add_first_product_to_cart(driver)
        checkout_page = _go_to_checkout(driver)

        delivery_text = checkout_page.get_delivery_address_text()
        billing_text = checkout_page.get_billing_address_text()

        expected_fields = (
            signup_data["first_name"],
            signup_data["last_name"],
            signup_data["address"],
            signup_data["city"],
            signup_data["state"],
            signup_data["zipcode"],
            signup_data["country"],
        )
        for field_value in expected_fields:
            assert field_value in delivery_text, (
                f"Delivery Address에 회원가입 정보({field_value!r})가 자동으로 채워져야 "
                f"하지만 그렇지 않음 (실제 Delivery Address: {delivery_text!r})"
            )
            assert field_value in billing_text, (
                f"Billing Address에 회원가입 정보({field_value!r})가 자동으로 채워져야 "
                f"하지만 그렇지 않음 (실제 Billing Address: {billing_text!r})"
            )
    finally:
        _cleanup_cart_item(cart_page, product_name)
        # 이 테스트가 생성한 계정을 정리한다(AUTOMATION_GUIDE 11.2절 "가능한 범위에서
        # 정리"). 정리 자체가 실패해도 위 assertion 실패를 덮어쓰지 않도록 예외를 흡수하고
        # 경고만 남긴다(_cleanup_cart_item과 동일한 이유).
        try:
            home_page.navigate()
            home_page.click_delete_account()
            account_deleted_page = AccountDeletedPage(driver)
            account_deleted_page.wait_for_url_contains("/delete_account")
        except Exception:
            logger.warning(
                "테스트 정리(cleanup)를 위한 계정 삭제에 실패함(수동 확인 필요): %s",
                signup_data["email"],
                exc_info=True,
            )
