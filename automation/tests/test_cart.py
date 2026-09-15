"""장바구니(상품 담기 포함) 기능을 검증하는 테스트.

Source of Truth:
- docs/tc/cart.md (TC-CART-001, 002, 003, 004, 005, 006, 008, 009, 010, 011, 014, 015, 016)
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙),
  10절(테스트 독립성), 11절(테스트 데이터 관리)

이 파일은 다음 Approved TC 13건을 다룬다(Rejected 3건 TC-CART-007/012/013은 자동화 대상이
아니므로 다루지 않음, `docs/tc/automation-candidates/cart.md` 참고):
- TC-001/002/003: Home 페이지 상품 카드 "Add to cart" 클릭 시 담기 확인 모달(`#cartModal`,
  `pages/add_to_cart_modal.py`)의 구성요소/버튼/링크 동작.
- TC-004: Home과 Products 페이지에서 각각 담은 상품이 하나의 장바구니로 병합되는지.
- TC-005: 리스트 페이지에서 동일 상품을 7회 반복 담으면 별도 행이 아닌 기존 행의 Quantity가
  누적되는지(테스트 데이터: 사용자 승인된 예시값 "Sleeveless Dress", 단가 Rs.1000).
- TC-006: 상품 상세 페이지에서 Quantity를 지정해 담으면 지정한 수량이 그대로 반영되는지.
- TC-008/009: 장바구니 특정 상품 삭제, 전체 삭제 시 빈 카트 상태 전환.
- TC-010/011: "Proceed To Checkout" 클릭 시 로그인 상태별 분기(로그아웃 → 로그인 요구 모달,
  로그인 → `/checkout` 바로 이동).
- TC-014/015/016: 로그인 상태별 장바구니 데이터 정합성(로그아웃 시 항상 빈 카트로 보임,
  로그아웃 상태에서 담은 상품이 로그인 시 반영됨, 로그인 중 담은 상품이 재로그인 시 유지됨).

[TC-006 관련 설계 판단 - ROADMAP.md Phase 5 항목] 정식 `ProductDetailPage` Page Object는
Phase 6(product-detail)에서 별도로 정의될 예정이므로(cart의 담기 확인 모달을 재사용하는
전제), 이 Phase에서는 신규 Page Object 파일을 만들지 않고 TC-CART-006 전용 최소 상호작용만
이 테스트 파일 내부에 국소적으로 구현한다(`_add_product_from_detail_page()`). Page Layer의
안정성(광고 오버레이 방어, 로깅, Explicit Wait)은 잃지 않도록 `pages.base_page.BasePage`를
직접 인스턴스화해 재사용하며, `time.sleep()`은 사용하지 않는다.

[TC-011/014/015/016 테스트 독립성 설계] 이 4개 TC는 로그인 상태가 필요하며 실제로 장바구니에
상품을 추가/조회하므로, 동일한 고정 계정을 여러 TC가 공유하면 실행 순서에 따라 장바구니
상태가 달라지는 의존성이 생길 수 있다(AUTOMATION_GUIDE 10절 테스트 독립성 원칙 위배 위험).
이를 방지하기 위해 4개 TC에 서로 다른 고정 계정을 배정했다(TC-011/016: actest1,
TC-014: actest2, TC-015: actest3). 각 테스트는 `try`/`finally`로 자신이 추가한 상품을
장바구니에서 삭제해 정리하며(`_cleanup_cart_item()`), 정리는 assertion 실패 여부와 무관하게
항상 시도된다.

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(HomePage/ProductsPage/CartPage/
AddToCartModal/CheckoutPage/LoginPage)는 화면 조작/조회만 담당한다(Assertion 없음).

민감정보 관리: 고정 계정(actest1~3)의 비밀번호는 `config.accounts.get_account()`를 통해
`automation/.env`(git 미추적)에서만 로드하며, 이 파일 어디에도 실제 비밀번호 값을
하드코딩하지 않는다.
"""

import logging
from typing import Optional

from selenium.webdriver.common.by import By

from config.accounts import get_account
from config.settings import BASE_URL
from pages.add_to_cart_modal import AddToCartModal
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.text import normalize_whitespace

logger = logging.getLogger(__name__)

# TC-CART-006 전용 최소 Locator(위 파일 docstring "TC-006 관련 설계 판단" 참고).
# Playwright MCP 실측 확인 완료(2026-08-31, https://automationexercise.com/product_details/1):
# Quantity 입력란은 id="quantity"(페이지 전체 기준 1개, 6.1절 1순위 id 적용)이고, "Add to
# cart" 버튼은 id/data-qa가 없어 .btn.btn-default.cart(페이지 전체 기준 1개, 4순위 CSS
# Selector)를 사용한다. 실제로 Quantity를 7로 지정해 클릭한 결과 장바구니에 Quantity 7/
# Total Rs.3500(단가 Rs.500 x 7, product_id=1 "Blue Top")이 정확히 반영됨을 Playwright
# MCP로 사전 확인했다.
_DETAIL_QUANTITY_INPUT = (By.ID, "quantity")
_DETAIL_ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btn.btn-default.cart")


def _add_product_from_detail_page(driver, product_id: int, quantity: int) -> None:
    """상품 상세 페이지(`/product_details/{id}`)에서 Quantity를 지정해 "Add to cart"를
    클릭한다(TC-CART-006 전용, 위 파일 docstring 참고).

    정식 Page Object를 만들지 않지만, `BasePage`를 직접 인스턴스화해 `type_text()`/
    `click()`이 제공하는 광고 오버레이 방어·로깅·Explicit Wait을 그대로 활용한다.
    """
    url = f"{BASE_URL.rstrip('/')}/product_details/{product_id}"
    driver.get(url)
    detail_page = BasePage(driver)
    detail_page.type_text(_DETAIL_QUANTITY_INPUT, str(quantity))
    detail_page.click(_DETAIL_ADD_TO_CART_BUTTON)


def _cleanup_cart_item(cart_page: CartPage, product_name: Optional[str]) -> None:
    """테스트가 로그인 계정 장바구니에 추가한 상품을 정리한다(위 파일 docstring
    "TC-011/014/015/016 테스트 독립성 설계" 참고).

    `product_name`이 None이면(상품 추가 자체가 실행되지 못하고 예외가 발생한 경우) 아무
    것도 하지 않는다. 이미 삭제되어 있거나 애초에 없는 경우도 조용히 반환한다(정리 대상이
    없을 뿐 오류가 아니므로).

    [2026-08-31 코드 리뷰 반영] 이 함수는 `finally` 블록에서만 호출되는 정리(cleanup)
    전용 로직이다. Python의 `finally` 예외 전파 규칙상 여기서 예외가 그대로 전파되면
    try 블록에서 실제로 발생한 assertion 실패를 덮어써, 테스트가 진짜 원인이 아닌
    `TimeoutException`/`NoSuchElementException` 등으로 실패한 것처럼 잘못 보고되는
    문제가 있었다. 따라서 정리 자체가 실패하더라도 예외를 전파하지 않고 경고 로그만
    남긴 뒤 반환한다 — 정리 실패는 이 로그를 근거로 별도로(예: 테스트 계정 장바구니
    수동 확인) 사용자에게 보고한다.
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


def test_add_to_cart_modal_shows_expected_components(driver):
    """TC-CART-001: Home 페이지 상품 카드에서 "Add to cart" 클릭 시 담기 확인 모달이 규정된
    구성요소(초록색 체크 아이콘, "Added!" 제목, 안내 문구, 파란색 "View Cart" 링크, 초록색
    "Continue Shopping" 버튼)와 함께 노출된다.

    색상 검증은 스크린샷 픽셀 비교 대신 `WebElement.value_of_css_property()` 기반
    `BasePage.get_css_value()`로 조회한 계산된 CSS 값에 RGB 성분이 포함되는지 확인하는
    방식을 사용한다(브라우저별 rgb()/rgba() 포맷 차이에 영향받지 않도록 부분 문자열
    비교)."""
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_add_to_cart_on_card(0)

    modal = AddToCartModal(driver)
    is_visible = modal.is_visible()
    assert is_visible is True, (
        f"'Add to cart' 클릭 시 담기 확인 모달이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_visible})"
    )

    icon_color = modal.get_icon_box_background_color()
    assert "130, 206, 52" in icon_color, (
        f"모달 아이콘 배경색이 초록색(rgb 130, 206, 52)이어야 하지만 그렇지 않음 "
        f"(실제: {icon_color!r})"
    )

    title_text = modal.get_title_text()
    assert title_text == "Added!", (
        f"모달 제목이 'Added!'이어야 하지만 그렇지 않음 (기대: 'Added!', 실제: {title_text!r})"
    )

    body_message = modal.get_body_message_text()
    expected_message = "Your product has been added to cart."
    assert body_message == expected_message, (
        f"모달 안내 문구가 {expected_message!r}이어야 하지만 그렇지 않음 "
        f"(기대: {expected_message!r}, 실제: {body_message!r})"
    )

    view_cart_text = modal.get_view_cart_link_text()
    assert view_cart_text == "View Cart", (
        f"'View Cart' 링크 텍스트가 'View Cart'이어야 하지만 그렇지 않음 "
        f"(기대: 'View Cart', 실제: {view_cart_text!r})"
    )

    view_cart_color = modal.get_view_cart_link_color()
    assert "66, 139, 202" in view_cart_color, (
        f"'View Cart' 링크 글자색이 파란색(rgb 66, 139, 202)이어야 하지만 그렇지 않음 "
        f"(실제: {view_cart_color!r})"
    )

    continue_text = modal.get_continue_shopping_button_text()
    assert continue_text == "Continue Shopping", (
        f"버튼 텍스트가 'Continue Shopping'이어야 하지만 그렇지 않음 "
        f"(기대: 'Continue Shopping', 실제: {continue_text!r})"
    )

    continue_color = modal.get_continue_shopping_button_background_color()
    assert "130, 206, 52" in continue_color, (
        f"'Continue Shopping' 버튼 배경색이 초록색(rgb 130, 206, 52)이어야 하지만 그렇지 않음 "
        f"(실제: {continue_color!r})"
    )

    modal.click_continue_shopping()


def test_continue_shopping_closes_modal_without_navigation(driver):
    """TC-CART-002: 담기 확인 모달에서 "Continue Shopping" 버튼 클릭 시 모달만 닫히고
    담기를 시도했던 페이지(Home)가 그대로 유지된다."""
    home_page = HomePage(driver)
    home_page.navigate()
    initial_url = driver.current_url

    home_page.click_add_to_cart_on_card(0)
    modal = AddToCartModal(driver)
    modal.click_continue_shopping()

    is_modal_visible = modal.is_visible()
    assert is_modal_visible is False, (
        f"'Continue Shopping' 클릭 후 모달이 닫혀야 하지만 여전히 노출됨 "
        f"(기대: False, 실제: {is_modal_visible})"
    )

    current_url = driver.current_url
    assert current_url == initial_url, (
        f"'Continue Shopping' 클릭 후 다른 페이지로 이동하지 않고 Home 페이지가 그대로 "
        f"유지되어야 하지만 그렇지 않음 (기대: {initial_url!r}, 실제: {current_url!r})"
    )


def test_view_cart_link_navigates_to_cart_page(driver):
    """TC-CART-003: 담기 확인 모달에서 "View Cart" 링크 클릭 시 장바구니
    (`https://automationexercise.com/view_cart`) 페이지로 이동한다."""
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_add_to_cart_on_card(0)

    modal = AddToCartModal(driver)
    modal.click_view_cart()

    cart_page = CartPage(driver)
    expected_url = f"{BASE_URL.rstrip('/')}/view_cart"
    cart_page.wait_for_url_to_be(expected_url)
    actual_url = driver.current_url
    assert actual_url == expected_url, (
        f"'View Cart' 클릭 시 장바구니 페이지로 이동해야 하지만 그렇지 않음 "
        f"(기대: {expected_url!r}, 실제: {actual_url!r})"
    )


def test_products_added_from_home_and_products_pages_merge_into_same_cart(driver):
    """TC-CART-004: Home 페이지와 Products 페이지에서 각각 담은 상품(상품 A, 상품 B)이 별도의
    장바구니로 분리되지 않고 하나의 장바구니 목록에 함께 노출된다."""
    home_page = HomePage(driver)
    home_page.navigate()
    product_a_name = home_page.get_product_names()[0]
    home_page.click_add_to_cart_on_card(0)
    AddToCartModal(driver).click_continue_shopping()

    products_page = ProductsPage(driver)
    products_page.navigate()
    product_b_name = products_page.get_product_names()[1]
    products_page.click_add_to_cart_on_card(1)
    AddToCartModal(driver).click_continue_shopping()

    cart_page = CartPage(driver)
    cart_page.navigate()
    cart_names = [normalize_whitespace(name) for name in cart_page.get_product_names()]

    assert normalize_whitespace(product_a_name) in cart_names, (
        f"Home 페이지에서 담은 상품 A({product_a_name!r})가 장바구니에 노출되어야 하지만 "
        f"그렇지 않음 (장바구니 상품 목록: {cart_names})"
    )
    assert normalize_whitespace(product_b_name) in cart_names, (
        f"Products 페이지에서 담은 상품 B({product_b_name!r})가 장바구니에 노출되어야 하지만 "
        f"그렇지 않음 (장바구니 상품 목록: {cart_names})"
    )


def test_repeated_add_to_cart_accumulates_quantity_on_list_page(driver):
    """TC-CART-005: 리스트 페이지 "Add to cart"는 항상 1개씩만 담기며, 동일 상품을 7회
    반복해서 담으면 별도 행이 아닌 기존 행의 Quantity가 누적된다.

    테스트 데이터는 `docs/tc/cart.md`에서 사용자가 승인한 예시값("Sleeveless Dress", 단가
    Rs.1000)을 그대로 사용한다. Playwright MCP 실측 결과 실제 사이트에서도 해당 상품의 단가가
    Rs.1000으로 승인된 예시값과 정확히 일치함을 확인했다(`products_page.py` docstring
    "Phase 5 확장" 참고, 상품명 DOM 텍스트에만 연속 공백 차이가 있어 `normalize_whitespace()`로 비교)."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    card_index = products_page.find_card_index_by_product_name("Sleeveless Dress")

    for _ in range(7):
        products_page.click_add_to_cart_on_card(card_index)
        AddToCartModal(driver).click_continue_shopping()

    cart_page = CartPage(driver)
    cart_page.navigate()

    row_count = cart_page.get_cart_row_count()
    assert row_count == 1, (
        f"동일 상품을 7회 반복 담아도 장바구니 행은 1개만 유지되어야 하지만 그렇지 않음 "
        f"(기대: 1개, 실제: {row_count}개)"
    )

    quantity = cart_page.get_quantity_by_product_name("Sleeveless Dress")
    assert quantity == "7", (
        f"7회 반복 담기 후 Quantity가 7이어야 하지만 그렇지 않음 (기대: '7', 실제: {quantity!r})"
    )

    total = cart_page.get_total_by_product_name("Sleeveless Dress")
    expected_total = "Rs. 7000"
    assert total == expected_total, (
        f"7회 반복 담기 후 Total이 {expected_total!r}이어야 하지만 그렇지 않음 "
        f"(기대: {expected_total!r}, 실제: {total!r})"
    )


def test_specified_quantity_from_detail_page_reflected_in_cart(driver):
    """TC-CART-006: 상품 상세 페이지에서 담을 개수(7)를 지정해 담으면, 리스트 페이지에서
    1개씩만 담기는 것(TC-CART-005)과 달리 지정한 수량이 그대로 장바구니에 반영된다."""
    _add_product_from_detail_page(driver, product_id=1, quantity=7)

    modal = AddToCartModal(driver)
    modal.click_view_cart()

    cart_page = CartPage(driver)
    expected_url = f"{BASE_URL.rstrip('/')}/view_cart"
    cart_page.wait_for_url_to_be(expected_url)

    quantity = cart_page.get_quantity_by_product_name("Blue Top")
    assert quantity == "7", (
        f"상세 페이지에서 지정한 수량(7)이 장바구니 Quantity에 그대로 반영되어야 하지만 "
        f"그렇지 않음 (기대: '7', 실제: {quantity!r})"
    )

    total = cart_page.get_total_by_product_name("Blue Top")
    expected_total = "Rs. 3500"
    assert total == expected_total, (
        f"상세 페이지에서 지정한 수량(7)에 따라 Total이 {expected_total!r}이어야 하지만 "
        f"그렇지 않음 (기대: {expected_total!r}, 실제: {total!r})"
    )


def test_deleting_one_product_removes_only_that_product(driver):
    """TC-CART-008: 장바구니에서 특정 상품 행의 삭제(x) 버튼 클릭 시 해당 상품만 삭제되고
    나머지 상품은 그대로 남는다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    product_names = products_page.get_product_names()
    product_to_delete = product_names[0]
    product_to_keep = product_names[1]

    products_page.click_add_to_cart_on_card(0)
    AddToCartModal(driver).click_continue_shopping()
    products_page.click_add_to_cart_on_card(1)
    AddToCartModal(driver).click_continue_shopping()

    cart_page = CartPage(driver)
    cart_page.navigate()
    row_count_before = cart_page.get_cart_row_count()
    assert row_count_before == 2, (
        f"삭제 시나리오 준비를 위해 서로 다른 상품 2개가 장바구니에 담겨 있어야 하지만 "
        f"그렇지 않음 (기대: 2개, 실제: {row_count_before}개)"
    )

    cart_page.delete_product_by_name(product_to_delete)
    cart_page.wait_for_cart_row_count(1)

    remaining_names = [normalize_whitespace(name) for name in cart_page.get_product_names()]
    assert normalize_whitespace(product_to_delete) not in remaining_names, (
        f"삭제한 상품({product_to_delete!r})이 장바구니에서 제거되어야 하지만 여전히 남아있음 "
        f"(장바구니 상품 목록: {remaining_names})"
    )
    assert normalize_whitespace(product_to_keep) in remaining_names, (
        f"삭제하지 않은 상품({product_to_keep!r})은 그대로 남아있어야 하지만 그렇지 않음 "
        f"(장바구니 상품 목록: {remaining_names})"
    )


def test_deleting_all_products_shows_empty_cart_state(driver):
    """TC-CART-009: 장바구니에 담긴 모든 상품을 삭제하면 빈 카트 안내 상태로 전환된다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    product_name = products_page.get_product_names()[0]
    products_page.click_add_to_cart_on_card(0)
    AddToCartModal(driver).click_continue_shopping()

    cart_page = CartPage(driver)
    cart_page.navigate()

    cart_page.delete_product_by_name(product_name)
    cart_page.wait_for_cart_row_count(0)

    is_empty_visible = cart_page.is_empty_cart_message_visible()
    assert is_empty_visible is True, (
        f"마지막 상품 삭제 직후 빈 카트 안내 상태로 전환되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_empty_visible})"
    )

    empty_message = cart_page.get_empty_cart_message_text()
    expected_substring = "Cart is empty!"
    assert expected_substring in empty_message, (
        f"빈 카트 안내 문구에 {expected_substring!r}가 포함되어야 하지만 그렇지 않음 "
        f"(실제: {empty_message!r})"
    )


def test_proceed_to_checkout_shows_login_required_modal_when_logged_out(driver):
    """TC-CART-010: 로그아웃 상태에서 "Proceed To Checkout" 버튼 클릭 시 로그인/회원가입을
    요구하는 모달이 노출되며, `/checkout` 페이지로는 이동하지 않는다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.click_add_to_cart_on_card(0)
    AddToCartModal(driver).click_continue_shopping()

    cart_page = CartPage(driver)
    cart_page.navigate()
    cart_page.click_proceed_to_checkout()

    checkout_page = CheckoutPage(driver)
    is_modal_visible = checkout_page.is_login_required_modal_visible()
    assert is_modal_visible is True, (
        f"로그아웃 상태에서 'Proceed To Checkout' 클릭 시 로그인 요구 모달이 노출되어야 "
        f"하지만 그렇지 않음 (기대: True, 실제: {is_modal_visible})"
    )

    title_text = checkout_page.get_title_text()
    assert title_text == "Checkout", (
        f"모달 제목이 'Checkout'이어야 하지만 그렇지 않음 (기대: 'Checkout', 실제: {title_text!r})"
    )

    body_message = checkout_page.get_body_message_text()
    expected_message = "Register / Login account to proceed on checkout."
    assert expected_message in body_message, (
        f"모달 안내 문구에 {expected_message!r}가 포함되어야 하지만 그렇지 않음 "
        f"(실제: {body_message!r})"
    )

    link_text = checkout_page.get_register_login_link_text()
    assert link_text == "Register / Login", (
        f"'Register / Login' 링크 텍스트가 'Register / Login'이어야 하지만 그렇지 않음 "
        f"(기대: 'Register / Login', 실제: {link_text!r})"
    )

    continue_text = checkout_page.get_continue_on_cart_button_text()
    assert continue_text == "Continue On Cart", (
        f"버튼 텍스트가 'Continue On Cart'이어야 하지만 그렇지 않음 "
        f"(기대: 'Continue On Cart', 실제: {continue_text!r})"
    )

    continue_color = checkout_page.get_continue_on_cart_button_background_color()
    assert "130, 206, 52" in continue_color, (
        f"'Continue On Cart' 버튼 배경색이 초록색(rgb 130, 206, 52)이어야 하지만 그렇지 않음 "
        f"(실제: {continue_color!r})"
    )

    current_url = driver.current_url
    expected_cart_url = f"{BASE_URL.rstrip('/')}/view_cart"
    assert current_url == expected_cart_url, (
        f"모달이 노출된 채 '/checkout' 페이지로는 이동하지 않아야 하지만 그렇지 않음 "
        f"(기대: {expected_cart_url!r}에 그대로 있음, 실제: {current_url!r})"
    )


def test_proceed_to_checkout_navigates_directly_when_logged_in(driver):
    """TC-CART-011: 로그인 상태에서 "Proceed To Checkout" 버튼 클릭 시 별도 모달 없이
    `https://automationexercise.com/checkout` 페이지로 바로 이동한다."""
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    cart_page = CartPage(driver)
    product_name = None
    try:
        products_page = ProductsPage(driver)
        products_page.navigate()
        product_name = products_page.get_product_names()[0]
        products_page.click_add_to_cart_on_card(0)
        AddToCartModal(driver).click_continue_shopping()

        cart_page.navigate()
        cart_page.click_proceed_to_checkout()

        checkout_page = CheckoutPage(driver)
        is_modal_visible = checkout_page.is_login_required_modal_visible()
        assert is_modal_visible is False, (
            f"로그인 상태에서는 로그인 요구 모달이 노출되지 않아야 하지만 노출됨 "
            f"(기대: False, 실제: {is_modal_visible})"
        )

        expected_url = f"{BASE_URL.rstrip('/')}/checkout"
        cart_page.wait_for_url_to_be(expected_url)
        actual_url = driver.current_url
        assert actual_url == expected_url, (
            f"로그인 상태에서 'Proceed To Checkout' 클릭 시 '/checkout'으로 바로 이동해야 "
            f"하지만 그렇지 않음 (기대: {expected_url!r}, 실제: {actual_url!r})"
        )
    finally:
        _cleanup_cart_item(cart_page, product_name)


def test_cart_shows_empty_when_logged_out_even_if_account_has_items(driver):
    """TC-CART-014: 로그인 상태에서 상품을 담아둔 계정이라도, 로그아웃 상태의 Cart 화면은
    항상 빈 카트 상태로 노출된다."""
    account = get_account("actest2")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    cart_page = CartPage(driver)
    product_name = None
    try:
        products_page = ProductsPage(driver)
        products_page.navigate()
        product_name = products_page.get_product_names()[0]
        products_page.click_add_to_cart_on_card(0)
        AddToCartModal(driver).click_continue_shopping()

        home_page = HomePage(driver)
        home_page.navigate()
        home_page.click_logout()

        cart_page.navigate()
        is_empty_visible = cart_page.is_empty_cart_message_visible()
        assert is_empty_visible is True, (
            f"계정에 실제로 담긴 상품이 있어도 로그아웃 상태에서는 빈 카트로 노출되어야 "
            f"하지만 그렇지 않음 (기대: True, 실제: {is_empty_visible})"
        )
    finally:
        # 담아둔 상품을 정리하려면 다시 로그인해야 한다. 재로그인 자체가 실패해도
        # try 블록의 assertion 실패를 덮어쓰지 않도록(2026-08-31 코드 리뷰 반영,
        # _cleanup_cart_item()과 동일한 이유) 예외를 여기서 흡수하고 경고만 남긴다.
        try:
            login_page.navigate()
            login_page.login(account["email"], account["password"])
            login_page.wait_for_url_to_be(BASE_URL)
        except Exception:
            logger.warning(
                "테스트 정리(cleanup)를 위한 재로그인에 실패함(수동 확인 필요): %s",
                account["email"],
                exc_info=True,
            )
        else:
            _cleanup_cart_item(cart_page, product_name)


def test_cart_added_while_logged_out_is_merged_after_login(driver):
    """TC-CART-015: 로그아웃 상태에서 담은 상품이 이후 로그인하면 해당 계정의 장바구니에
    반영되어 노출된다."""
    cart_page = CartPage(driver)
    product_name = None
    try:
        products_page = ProductsPage(driver)
        products_page.navigate()
        product_name = products_page.get_product_names()[0]
        products_page.click_add_to_cart_on_card(0)
        AddToCartModal(driver).click_continue_shopping()

        account = get_account("actest3")
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login(account["email"], account["password"])
        login_page.wait_for_url_to_be(BASE_URL)

        cart_page.navigate()
        cart_names = [normalize_whitespace(name) for name in cart_page.get_product_names()]
        assert normalize_whitespace(product_name) in cart_names, (
            f"로그아웃 상태에서 담은 상품({product_name!r})이 로그인 후 장바구니에 반영되어야 "
            f"하지만 그렇지 않음 (장바구니 상품 목록: {cart_names})"
        )
    finally:
        _cleanup_cart_item(cart_page, product_name)


def test_cart_added_while_logged_in_persists_after_relogin(driver):
    """TC-CART-016: 로그인 상태에서 담은 상품이 로그아웃 후 동일 계정으로 재로그인하면 다시
    유지되어 노출된다."""
    account = get_account("actest1")
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(account["email"], account["password"])
    login_page.wait_for_url_to_be(BASE_URL)

    cart_page = CartPage(driver)
    product_name = None
    try:
        products_page = ProductsPage(driver)
        products_page.navigate()
        product_name = products_page.get_product_names()[0]
        products_page.click_add_to_cart_on_card(0)
        AddToCartModal(driver).click_continue_shopping()

        home_page = HomePage(driver)
        home_page.navigate()
        home_page.click_logout()

        login_page.navigate()
        login_page.login(account["email"], account["password"])
        login_page.wait_for_url_to_be(BASE_URL)

        cart_page.navigate()
        cart_names = [normalize_whitespace(name) for name in cart_page.get_product_names()]
        assert normalize_whitespace(product_name) in cart_names, (
            f"로그인 중 담은 상품({product_name!r})이 재로그인 후에도 유지되어야 하지만 "
            f"그렇지 않음 (장바구니 상품 목록: {cart_names})"
        )
    finally:
        _cleanup_cart_item(cart_page, product_name)
