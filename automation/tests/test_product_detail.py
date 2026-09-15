"""상품 상세(product-detail) 기능을 검증하는 테스트.

Source of Truth:
- docs/tc/product-detail.md (TC-PRODUCT-DETAIL-001, 002, 008, 015, 016, 021)
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙),
  10절(테스트 독립성)

이 파일은 다음 Approved TC 6건을 다룬다(`docs/tc/automation-candidates/product-detail.md`
참고, 나머지 21건은 Rejected로 자동화 대상이 아님):
- TC-001: Home 페이지 상품 카드의 "View Product" 링크 클릭 시 이동한 URL이
  `/product_details/{id}` 패턴을 따르는지.
- TC-002: 존재하는 상품 ID로 직접 URL 접근 시 상세 페이지가 정상 노출되는지(이미지/상품명/
  가격 화면 구성요소 노출).
- TC-008: 가격이 "Rs. {숫자}" 형식으로 노출되는지.
- TC-015 (P0): 정상 수량을 지정한 상태에서 "Add to cart" 클릭 시 리스트 페이지와 동일한 담기
  확인 모달(`pages/add_to_cart_modal.py`)이 노출되는지.
- TC-016: Quantity 입력란 스피너 아래 버튼을 반복 조작해도 1 미만으로 내려가지 않는지.
- TC-021: WRITE YOUR REVIEW 3개 필수값을 올바르게 입력하고 Submit 클릭 시 성공 메시지가
  노출되고 1~2초 후 필드가 자동 초기화되는지.

모든 TC는 로그인/로그아웃 상태와 무관하다(Feature PRD에 로그인 필요 조건이 명시되지 않음,
`docs/tc/product-detail.md` 공통 Preconditions 참고). 테스트 데이터는 상품 ID 1("Blue Top",
단가 Rs. 500 - `tests/test_cart.py`에서 이미 실측 검증된 값과 동일)을 사용한다.

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(HomePage/ProductDetailPage/
AddToCartModal)는 화면 조작/조회만 담당한다(Assertion 없음). "Add to cart" 확인 모달은
신규 정의 없이 Phase 5에서 정의된 `AddToCartModal`을 그대로 재사용한다(ROADMAP.md Phase 6
항목).
"""

import re

from pages.add_to_cart_modal import AddToCartModal
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage

# 이 파일 전체에서 사용하는 테스트 대상 상품(위 파일 docstring 참고)
_PRODUCT_ID = 1
_PRODUCT_NAME = "Blue Top"

# 상품 상세 URL 패턴("https://automationexercise.com/product_details/{숫자}")
_PRODUCT_DETAIL_URL_PATTERN = re.compile(
    r"^https://automationexercise\.com/product_details/\d+$"
)

# 가격 표기 형식 패턴("Rs. {숫자}")
_PRICE_FORMAT_PATTERN = re.compile(r"^Rs\. \d+$")


def test_view_product_link_navigates_to_product_details_url_pattern(driver):
    """TC-PRODUCT-DETAIL-001: Home 페이지 임의 상품 카드에서 "View Product" 링크 클릭 시
    이동한 URL이 `https://automationexercise.com/product_details/{id}` 패턴(마지막 경로가
    숫자인 상품 ID)을 따른다."""
    home_page = HomePage(driver)
    home_page.navigate()
    home_page.click_view_product_on_card(0)

    home_page.wait_for_url_contains("product_details")
    actual_url = driver.current_url
    assert _PRODUCT_DETAIL_URL_PATTERN.match(actual_url), (
        f"'View Product' 클릭 시 이동한 URL이 '/product_details/{{id}}' 패턴을 따라야 "
        f"하지만 그렇지 않음 (실제: {actual_url!r})"
    )


def test_direct_url_access_shows_product_detail_page(driver):
    """TC-PRODUCT-DETAIL-002: 존재하는 상품 ID로 상세 페이지 URL에 직접 접근하면 별도
    에러 없이 페이지가 정상적으로 노출되며, 상품 이미지/상품명/가격 등 화면 구성요소가
    표시된다."""
    detail_page = ProductDetailPage(driver)
    detail_page.navigate(_PRODUCT_ID)

    is_image_visible = detail_page.is_image_visible()
    assert is_image_visible is True, (
        f"존재하는 상품 ID로 접근 시 상품 이미지가 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_image_visible})"
    )

    product_name = detail_page.get_product_name()
    assert product_name == _PRODUCT_NAME, (
        f"상품명이 {_PRODUCT_NAME!r}로 노출되어야 하지만 그렇지 않음 "
        f"(기대: {_PRODUCT_NAME!r}, 실제: {product_name!r})"
    )

    price_text = detail_page.get_price_text()
    assert price_text, (
        f"가격 정보가 빈 값이 아니어야 하지만 빈 값으로 노출됨 (실제: {price_text!r})"
    )


def test_price_is_displayed_in_rs_currency_format(driver):
    """TC-PRODUCT-DETAIL-008: 상품 상세 페이지의 가격이 "Rs. {숫자}" 형태로 Rs. 단위와
    함께 노출된다."""
    detail_page = ProductDetailPage(driver)
    detail_page.navigate(_PRODUCT_ID)

    price_text = detail_page.get_price_text()
    assert _PRICE_FORMAT_PATTERN.match(price_text), (
        f"가격이 'Rs. {{숫자}}' 형식으로 노출되어야 하지만 그렇지 않음 (실제: {price_text!r})"
    )


def test_add_to_cart_shows_confirmation_modal(driver):
    """TC-PRODUCT-DETAIL-015 (P0): Quantity 입력란에 정상적인 수량 값(2)을 입력한 상태에서
    "Add to cart" 버튼을 클릭하면 Home/Products 리스트 페이지와 동일한 담기 확인 모달
    (초록 체크 아이콘, "Added!", 안내 문구, "View Cart" 링크, "Continue Shopping" 버튼)이
    노출된다. 모달 자체의 상세 구성은 `cart.md` TC-CART-001에서 이미 검증되었으므로
    (`AddToCartModal` 재사용), 이 테스트는 상세 페이지 고유의 Quantity 입력값 캡처 →
    장바구니 반영 → 공유 모달 렌더링이 새롭게 결합되는지에 집중한다."""
    detail_page = ProductDetailPage(driver)
    detail_page.navigate(_PRODUCT_ID)
    detail_page.set_quantity("2")
    detail_page.click_add_to_cart()

    modal = AddToCartModal(driver)
    is_visible = modal.is_visible()
    assert is_visible is True, (
        f"정상 수량으로 'Add to cart' 클릭 시 담기 확인 모달이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_visible})"
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

    continue_text = modal.get_continue_shopping_button_text()
    assert continue_text == "Continue Shopping", (
        f"버튼 텍스트가 'Continue Shopping'이어야 하지만 그렇지 않음 "
        f"(기대: 'Continue Shopping', 실제: {continue_text!r})"
    )

    modal.click_continue_shopping()


def test_quantity_spinner_does_not_go_below_minimum(driver):
    """TC-PRODUCT-DETAIL-016: Quantity 입력란 기본값(1)에서 스피너 아래(▼) 버튼을 여러
    차례 조작해도 값이 1 미만으로 내려가지 않고 1에서 멈춘다."""
    detail_page = ProductDetailPage(driver)
    detail_page.navigate(_PRODUCT_ID)

    initial_quantity = detail_page.get_quantity_value()
    assert initial_quantity == "1", (
        f"Quantity 입력란 기본값이 1이어야 하지만 그렇지 않음 "
        f"(기대: '1', 실제: {initial_quantity!r})"
    )

    detail_page.click_quantity_spin_down(times=5)

    final_quantity = detail_page.get_quantity_value()
    assert final_quantity == "1", (
        f"스피너 아래 버튼을 반복 조작해도 Quantity가 1 미만으로 내려가지 않아야 하지만 "
        f"그렇지 않음 (기대: '1', 실제: {final_quantity!r})"
    )


def test_review_submission_shows_success_message_and_auto_resets_fields(driver):
    """TC-PRODUCT-DETAIL-021: WRITE YOUR REVIEW 섹션의 Your Name/Email Address/리뷰 내용
    3개 필수값을 모두 올바르게 입력하고 Submit 클릭 시 초록색 "Thank you for your review."
    성공 메시지가 노출되고, 1~2초 경과 후 3개 입력 필드가 자동으로 빈 값으로 초기화된다."""
    detail_page = ProductDetailPage(driver)
    detail_page.navigate(_PRODUCT_ID)
    detail_page.submit_review(
        name="QA Automation",
        email="qa.automation.review@example.com",
        review_text="Great product, exactly as described. (자동화 테스트로 등록된 리뷰)",
    )

    success_message = detail_page.get_review_success_message()
    expected_message = "Thank you for your review."
    assert success_message == expected_message, (
        f"리뷰 제출 성공 메시지가 {expected_message!r}이어야 하지만 그렇지 않음 "
        f"(기대: {expected_message!r}, 실제: {success_message!r})"
    )

    detail_page.wait_for_review_fields_cleared()
    name_value, email_value, review_value = detail_page.get_review_field_values()
    assert name_value == "", (
        f"성공 메시지 노출 후 Your Name 필드가 자동으로 빈 값이 되어야 하지만 그렇지 않음 "
        f"(실제: {name_value!r})"
    )
    assert email_value == "", (
        f"성공 메시지 노출 후 Email Address 필드가 자동으로 빈 값이 되어야 하지만 그렇지 않음 "
        f"(실제: {email_value!r})"
    )
    assert review_value == "", (
        f"성공 메시지 노출 후 리뷰 내용 필드가 자동으로 빈 값이 되어야 하지만 그렇지 않음 "
        f"(실제: {review_value!r})"
    )
