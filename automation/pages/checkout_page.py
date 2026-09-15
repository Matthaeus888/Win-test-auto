"""로그인 요구 모달(id="checkoutModal") 및 `/checkout` 진입 골격을 다루는 Page Object.

Source of Truth:
- docs/tc/cart.md (TC-CART-010, 011)
- docs/prd/feature/cart.md REQ-CART-008/009
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

[Phase 5 범위 한정] ROADMAP.md Phase 5 항목에 따라 이 Page Object는 "로그인 요구 모달 +
`/checkout` 기본 골격"만 다룬다. `/checkout` 페이지의 Address Details, Review Your Order 등
화면 구성요소는 `page-ui.md` TC-PAGE-UI-034~041 범위이며 Phase 7(page-ui)에서 확장 예정이므로
이 Task에서는 만들지 않는다.

Locator 확정 근거(Playwright MCP 실측, 2026-08-31, https://automationexercise.com/view_cart,
로그아웃 상태, 장바구니에 상품 1개 담긴 상태에서 "Proceed To Checkout" 버튼 클릭):
- 로그인 요구 모달은 "Proceed To Checkout" 버튼 클릭 시 Cart 페이지(`/view_cart`) 위에
  노출되며(페이지 이동 없이 URL이 그대로 `/view_cart`로 유지됨을 `window.location.href`로
  확인), 컨테이너는 `id="checkoutModal"`로 페이지 전체 기준
  `document.querySelectorAll('#checkoutModal').length === 1`을 확인했다(6.1절 1순위 id
  적용). "Add to Cart" 확인 모달(`#cartModal`, `add_to_cart_modal.py`)과는 별개의 컨테이너다.
- 모달 내부 구조(`#checkoutModal` 기준 상대 CSS Selector, 각각 스코프 내 개수로 고유성 확인):
  - `.icon-box`(1개) - 상단 아이콘 컨테이너("사람 아이콘", TC-CART-010 Expected Result).
  - `.modal-title`(1개) - 텍스트 "Checkout".
  - `.modal-body`(1개) - 안내 문구("Register / Login account to proceed on checkout.")와
    "Register / Login" 링크를 감싼 문단 2개를 포함하는 컨테이너. `#cartModal`과 달리 이
    모달은 두 문단의 텍스트를 조합해 확인해도 TC 판정에 지장이 없어(안내 문구와 링크 텍스트가
    서로 다른 문자열이라 부분 문자열 포함 여부로 판정 가능) 별도로 `:first-of-type`까지
    좁히지 않고 컨테이너 전체 텍스트를 조회하는 `get_body_message_text()`를 제공한다.
  - `.modal-body a[href='/login']`(1개) - "Register / Login" 링크.
  - `.close-checkout-modal`(1개) - "Continue On Cart" 버튼(`data-dismiss="modal"`). 텍스트
    "Continue On Cart", `background-color: rgb(130, 206, 52)`(초록색, TC-CART-010 Expected
    Result "하단 초록색 'Continue On Cart' 버튼"과 일치)를 확인했다.
- "Continue On Cart" 클릭 시 모달만 닫히고(`data-dismiss="modal"`) 페이지 이동은 발생하지
  않음을 확인했다(`<button>` 요소, `click()` 그대로 사용).
- "Register / Login" 링크(`<a href="/login">`)는 실제 페이지 전체 이동을 트리거하므로
  `click_and_retry_if_vignette()`를 사용한다(다른 Page Object의 페이지 이동 링크와 동일 패턴).
- `/checkout` URL 자체는 로그아웃 상태에서 직접 접근해도 서버가 페이지를 렌더링함(Address
  Details가 비어있는 골격 상태)을 확인했으나, Approved TC(TC-CART-010/011)는 "Proceed To
  Checkout" 버튼 클릭이라는 트리거를 통한 진입만 다루므로 이 Page Object는 별도의
  `navigate()`를 제공하지 않는다(진입은 `CartPage.click_proceed_to_checkout()`이 담당).
  로그인 상태에서 버튼 클릭 시 모달 없이 `/checkout`으로 바로 이동하는지(TC-CART-011)는
  `BasePage.wait_for_url_contains("/checkout")`로 확인한다(이 Page Object에 별도 메서드를
  추가하지 않음 - 이미 BasePage가 제공).

Phase 7 확장(Address Details/Review Your Order/Total Amount/Place Order, Playwright MCP
실측, 2026-09-01, https://automationexercise.com/checkout - 5.4절 "MCP 브라우저와 실제
테스트(Selenium) 환경이 다르게 동작함" 관련 참고: 이번 세션의 MCP 브라우저에 예상치 못한
기존 로그인 세션/장바구니 데이터가 남아있어 이를 그대로 조회만 하고 활용했다,
`pages/home_page.py` docstring "예상치 못한 관찰 사항" 참고. 실제 pytest(Selenium) 실행
시에는 반드시 `CartPage.click_proceed_to_checkout()`으로 진입해야 하며(`/checkout`을
`driver.get()`으로 직접 접근하면 Review Your Order 표/Total Amount가 비정상적으로
비어보이는 현상이 관찰됨) 이 Page Object는 그 전제를 그대로 따른다):
- 섹션 제목은 `h2.heading`(페이지 전체 기준 2개: "Address Details", "Review Your Order")로,
  텍스트로 구분해야 해 6.1절 5순위 상대 XPath를 사용한다.
- "Your Delivery Address"는 `#address_delivery`, "Your Billing Address"는
  `#address_invoice`(각각 페이지 전체 기준 1개, 6.1절 1순위 id 적용)이며, 순수 텍스트로
  구성된 `<li>` 목록(이름/회사(빈칸)/주소1/주소2/도시-주-우편번호/국가/전화번호)이고 입력
  요소(input 등)는 없음을 확인했다(REQ-PAGE-UI-031 read-only 특성과 일치, 단 read-only
  자체를 검증하는 TC-PAGE-UI-040은 Approved 대상이 아니라 이 Phase에서 별도 메서드를
  추가하지 않는다).
- Review Your Order 표는 `table.table-condensed`(id 없음, Cart 페이지의
  `#cart_info_table`과 다른 별도 컨테이너, 페이지 전체 기준 1개)이며, 행
  (`table.table-condensed tbody tr`) 내부에 Cart 페이지와 완전히 동일한 클래스
  (`.cart_product img`/`.cart_description`/`.cart_price`/`.cart_quantity`/`.cart_total`)를
  그대로 재사용하는 마크업임을 확인했다(장바구니와 같은 템플릿 partial로 추정).
- Total Amount는 표의 마지막 행(`tbody tr:last-child`) 안의 `.cart_total_price`이며,
  일반 상품 행에도 동일 클래스(`.cart_total`의 자식 `.cart_total_price`)가 존재해 스코프를
  마지막 행으로 좁혀야 고유해짐을 확인했다(위 파일 docstring과 별개로 Cart 행과 클래스를
  공유하므로 스코핑 필요).
- "Place Order" 버튼은 `a.check_out[href='/payment']`(페이지 전체 기준 1개, 텍스트
  "Place Order")로 확인했다. 실제 클릭(`/payment`로 이동)은 Approved TC(TC-PAGE-UI-039,
  "노출 여부"만 검증)의 범위가 아니므로 이 Page Object에 클릭 메서드를 추가하지 않는다
  (CLAUDE.md 12절 "불필요한 코드 생성 금지").
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """로그인 요구 모달(id="checkoutModal")의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/click_and_retry_if_vignette/get_text/get_css_value/is_element_visible)만
    사용해 요소를 조작·조회한다.
    """

    LOGIN_REQUIRED_MODAL = (By.ID, "checkoutModal")
    ICON_BOX = (By.CSS_SELECTOR, "#checkoutModal .icon-box")
    TITLE = (By.CSS_SELECTOR, "#checkoutModal .modal-title")
    BODY_MESSAGE = (By.CSS_SELECTOR, "#checkoutModal .modal-body")
    REGISTER_LOGIN_LINK = (By.CSS_SELECTOR, "#checkoutModal .modal-body a[href='/login']")
    CONTINUE_ON_CART_BUTTON = (By.CSS_SELECTOR, "#checkoutModal .close-checkout-modal")

    # Address Details(Phase 7, TC-PAGE-UI-034/035) - Playwright MCP 실측 확인 완료(위
    # docstring "Phase 7 확장" 참고)
    ADDRESS_DETAILS_HEADING = (
        By.XPATH, "//h2[contains(@class, 'heading') and normalize-space(.)='Address Details']"
    )
    DELIVERY_ADDRESS = (By.ID, "address_delivery")
    BILLING_ADDRESS = (By.ID, "address_invoice")

    # Review Your Order / Total Amount(Phase 7, TC-PAGE-UI-036/037) - Playwright MCP
    # 실측 확인 완료(위 docstring "Phase 7 확장" 참고)
    REVIEW_ORDER_HEADING = (
        By.XPATH,
        "//h2[contains(@class, 'heading') and normalize-space(.)='Review Your Order']",
    )
    REVIEW_ORDER_TABLE = (By.CSS_SELECTOR, "table.table-condensed")
    # [2026-09-01 pytest 실행 중 재현·확인] `tbody tr` 전체를 대상으로 하면 상품 행뿐 아니라
    # 표 맨 마지막의 "Total Amount" 행(`<tr><td></td><td></td><td colspan="2">...</td>
    # <td><p class="cart_total_price">...</p></td></tr>`, id 속성 없음)까지 포함되어 상품
    # 개수가 실제보다 1개 많게 조회되는 현상이 확인되었다(예: 상품 1개를 담았는데 행 2개로
    # 조회됨). 상품 행에만 존재하는 `id="product-{id}"` 속성으로 범위를 좁혀 Total Amount
    # 행을 제외했다(Cart 페이지의 `#cart_info_table tbody tr`도 동일하게 `id="product-{id}"`
    # 를 가짐을 실측으로 재확인).
    REVIEW_ORDER_ROWS = (By.CSS_SELECTOR, "table.table-condensed tbody tr[id]")
    REVIEW_ROW_IMAGE = (By.CSS_SELECTOR, ".cart_product img")
    REVIEW_ROW_DESCRIPTION = (By.CSS_SELECTOR, ".cart_description")
    REVIEW_ROW_PRICE = (By.CSS_SELECTOR, ".cart_price")
    REVIEW_ROW_QUANTITY = (By.CSS_SELECTOR, ".cart_quantity")
    REVIEW_ROW_TOTAL = (By.CSS_SELECTOR, ".cart_total")
    TOTAL_AMOUNT = (
        By.CSS_SELECTOR, "table.table-condensed tbody tr:last-child .cart_total_price"
    )

    # Place Order 버튼(Phase 7, TC-PAGE-UI-039) - Playwright MCP 실측 확인 완료
    PLACE_ORDER_BUTTON = (By.CSS_SELECTOR, "a.check_out[href='/payment']")

    def is_login_required_modal_visible(self) -> bool:
        """로그인 요구 모달의 노출 여부를 반환한다."""
        return self.is_element_visible(self.LOGIN_REQUIRED_MODAL)

    def get_title_text(self) -> str:
        """모달 제목("Checkout") 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.TITLE)

    def get_body_message_text(self) -> str:
        """모달 본문(안내 문구 + "Register / Login" 링크 텍스트 포함) 전체 텍스트를 조회해
        반환한다(Assertion 없음)."""
        return self.get_text(self.BODY_MESSAGE)

    def get_register_login_link_text(self) -> str:
        """"Register / Login" 링크 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.REGISTER_LOGIN_LINK)

    def click_register_login(self) -> None:
        """"Register / Login" 링크를 클릭해 로그인 페이지(`/login`)로 이동한다.

        실제 페이지 전체 이동(`<a href="/login">`)을 트리거하므로
        `click_and_retry_if_vignette()`를 사용한다(위 docstring 참고).
        """
        self.click_and_retry_if_vignette(self.REGISTER_LOGIN_LINK)

    def get_continue_on_cart_button_text(self) -> str:
        """"Continue On Cart" 버튼 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.CONTINUE_ON_CART_BUTTON)

    def get_continue_on_cart_button_background_color(self) -> str:
        """"Continue On Cart" 버튼의 배경색(`background-color`)을 조회해 반환한다
        (Assertion 없음)."""
        return self.get_css_value(self.CONTINUE_ON_CART_BUTTON, "background-color")

    def click_continue_on_cart(self) -> None:
        """"Continue On Cart" 버튼을 클릭해 모달을 닫는다(Cart 페이지에 그대로 남음).

        `data-dismiss="modal"` 버튼으로 페이지 이동을 트리거하지 않으므로 일반 `click()`을
        사용한다.
        """
        self.click(self.CONTINUE_ON_CART_BUTTON)

    def is_address_details_heading_visible(self) -> bool:
        """"Address Details" 섹션 제목의 노출 여부를 반환한다(Phase 7,
        TC-PAGE-UI-034)."""
        return self.is_element_visible(self.ADDRESS_DETAILS_HEADING)

    def is_delivery_address_visible(self) -> bool:
        """"Your Delivery Address" 영역의 노출 여부를 반환한다(Phase 7,
        TC-PAGE-UI-034)."""
        return self.is_element_visible(self.DELIVERY_ADDRESS)

    def is_billing_address_visible(self) -> bool:
        """"Your Billing Address" 영역의 노출 여부를 반환한다(Phase 7,
        TC-PAGE-UI-034)."""
        return self.is_element_visible(self.BILLING_ADDRESS)

    def get_delivery_address_text(self) -> str:
        """"Your Delivery Address" 영역 전체 텍스트를 조회해 반환한다(Phase 7,
        TC-PAGE-UI-035, Assertion 없음)."""
        return self.get_text(self.DELIVERY_ADDRESS)

    def get_billing_address_text(self) -> str:
        """"Your Billing Address" 영역 전체 텍스트를 조회해 반환한다(Phase 7,
        TC-PAGE-UI-035, Assertion 없음)."""
        return self.get_text(self.BILLING_ADDRESS)

    def is_review_order_heading_visible(self) -> bool:
        """"Review Your Order" 섹션 제목의 노출 여부를 반환한다(Phase 7,
        TC-PAGE-UI-036)."""
        return self.is_element_visible(self.REVIEW_ORDER_HEADING)

    def get_review_order_row_count(self) -> int:
        """"Review Your Order" 표의 상품 행 개수를 반환한다(Phase 7, Assertion 없음).

        `driver.find_elements()`(복수형)는 대상이 없으면 즉시 빈 리스트를 반환하고
        `WebDriverWait` 폴링을 하지 않는다(`CartPage.get_cart_row_count()`와 동일한
        구현 패턴).
        """
        count = len(self.driver.find_elements(*self.REVIEW_ORDER_ROWS))
        self.logger.debug("Review Your Order 표 행 개수 조회 완료: %s", count)
        return count

    def is_review_order_first_row_columns_visible(self) -> bool:
        """"Review Your Order" 표 첫 번째 행의 5개 컬럼(Item/Description/Price/Quantity/
        Total)이 모두 노출되는지 반환한다(Phase 7, TC-PAGE-UI-036).

        모든 컬럼이 노출되는 경우에만 True를 반환한다.
        """
        row = self.find_element(self.REVIEW_ORDER_ROWS)
        return (
            bool(row.find_elements(*self.REVIEW_ROW_IMAGE))
            and bool(row.find_elements(*self.REVIEW_ROW_DESCRIPTION))
            and bool(row.find_elements(*self.REVIEW_ROW_PRICE))
            and bool(row.find_elements(*self.REVIEW_ROW_QUANTITY))
            and bool(row.find_elements(*self.REVIEW_ROW_TOTAL))
        )

    def is_total_amount_visible(self) -> bool:
        """Total Amount(합계 금액)의 노출 여부를 반환한다(Phase 7, TC-PAGE-UI-037)."""
        return self.is_element_visible(self.TOTAL_AMOUNT)

    def get_total_amount_text(self) -> str:
        """Total Amount(합계 금액) 텍스트를 조회해 반환한다(Phase 7, Assertion 없음)."""
        return self.get_text(self.TOTAL_AMOUNT)

    def is_place_order_button_visible(self) -> bool:
        """"Place Order" 버튼의 노출 여부를 반환한다(Phase 7, TC-PAGE-UI-039)."""
        return self.is_element_visible(self.PLACE_ORDER_BUTTON)
