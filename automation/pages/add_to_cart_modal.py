""""Add to cart" 클릭 시 노출되는 담기 확인 모달(id="cartModal")을 다루는 공유 Page Object.

Source of Truth:
- docs/tc/cart.md (TC-CART-001, 002, 003)
- docs/prd/feature/cart.md REQ-CART-001("Add to Cart" 확인 모달의 원 정의)
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

이 모달은 Home(`/`)/Products(`/products`) 목록 페이지의 상품 카드는 물론, 상품 상세 페이지
(`/product_details/{id}`)의 "Add to cart" 버튼 클릭 시에도 동일하게 노출되는 공유 컴포넌트다
(REQ-CART-001이 원 정의이며 `product-detail.md`가 재사용한다고 PRD/Candidate 문서에 명시됨,
ROADMAP.md Phase 5/6 근거). 이에 따라 특정 화면에 종속되지 않는 별도 Page Object로 분리했으며,
Phase 6(product-detail)에서도 신규 정의 없이 그대로 재사용한다(ROADMAP.md Phase 6 항목).

Locator 확정 근거(Playwright MCP 실측, 2026-08-31, https://automationexercise.com/,
https://automationexercise.com/product_details/1, 로그아웃 상태):
- Home 페이지 상품 카드(`.features_items .col-sm-4 .productinfo .add-to-cart`)의
  "Add to cart" 버튼을 클릭해 모달을 실제로 노출시킨 뒤 `browser_evaluate`로 DOM을 조회했다.
  모달 컨테이너는 `id="cartModal"`이며 페이지 전체 기준 `document.querySelectorAll('#cartModal')
  .length === 1`로 고유함을 확인했다(6.1절 1순위 id 적용). 상품 상세 페이지에서도 "Add to
  cart" 버튼(`.btn.btn-default.cart`) 클릭 시 동일하게 `#cartModal`(`display: block`)이
  노출됨을 재확인해, 목록 페이지와 상세 페이지가 완전히 동일한 모달 컴포넌트를 공유함을
  검증했다.
- 모달 내부 구조(`#cartModal` 기준 상대 CSS Selector, 각각 `document.querySelectorAll(...)
  .length`로 스코프 내 고유성 확인 완료):
  - `.icon-box`(1개) - 상단 아이콘 컨테이너. 아이콘 자체(`<i class="material-icons">`)는
    텍스트 글리프 없이 `.icon-box`의 `background-color: rgb(130, 206, 52)`(초록색)로만
    표현됨을 `getComputedStyle`로 확인했다(TC-CART-001 Expected Result "초록색 체크
    아이콘"의 "초록색" 부분은 이 배경색으로 판정, 글리프 자체는 사이트 폰트 로딩 이슈로
    보이나 이 Phase의 검증 대상이 아님).
  - `.modal-title`(1개) - 텍스트 "Added!".
  - `.modal-body p:first-of-type`(1개, `:first-of-type`은 표준 CSS 가상 클래스로 Full XPath가
    아님) - 안내 문구 "Your product has been added to cart." 단독 조회용. `.modal-body`
    안에는 `p.text-center` 클래스를 공유하는 문단이 2개(안내 문구, View Cart 링크를 감싼
    문단) 있어 클래스만으로는 고유하지 않아 `:first-of-type`으로 범위를 좁혔다.
  - `.modal-body a[href='/view_cart']`(1개) - "View Cart" 링크. 텍스트 "View Cart",
    `color: rgb(66, 139, 202)`(파란색)를 확인했다.
  - `.close-modal`(1개) - "Continue Shopping" 버튼(`data-dismiss="modal"`). 텍스트
    "Continue Shopping", `background-color: rgb(130, 206, 52)`(초록색)를 확인했다.
- "Continue Shopping" 클릭 시 모달이 닫히고(`data-dismiss="modal"`, 부트스트랩 표준 동작)
  실제 페이지 이동은 발생하지 않음을 확인했다(TC-CART-002 대응, `<button>` 요소이며
  `<a href="...">`가 아니라 페이지 전체 이동을 트리거하지 않으므로 Google Vignette 광고
  개입 위험이 없어 `click()`을 그대로 사용, `click_and_retry_if_vignette()` 불필요).
- "View Cart" 링크(`<a href="/view_cart">`)는 실제 페이지 전체 이동을 트리거하므로(TC-CART-003
  대응) `HomePage.click_cart()` 등과 동일하게 `click_and_retry_if_vignette()`를 사용한다.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AddToCartModal(BasePage):
    """담기 확인 모달(id="cartModal")의 화면 조작/조회를 담당하는 공유 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/click_and_retry_if_vignette/get_text/get_css_value/is_element_visible)만
    사용해 요소를 조작·조회한다. Home/Products 목록 페이지와 상품 상세 페이지가 모두
    공유하는 컴포넌트이므로 특정 페이지 URL을 다루는 `navigate()`는 제공하지 않는다.
    """

    MODAL = (By.ID, "cartModal")
    ICON_BOX = (By.CSS_SELECTOR, "#cartModal .icon-box")
    TITLE = (By.CSS_SELECTOR, "#cartModal .modal-title")
    BODY_MESSAGE = (By.CSS_SELECTOR, "#cartModal .modal-body p:first-of-type")
    VIEW_CART_LINK = (By.CSS_SELECTOR, "#cartModal .modal-body a[href='/view_cart']")
    CONTINUE_SHOPPING_BUTTON = (By.CSS_SELECTOR, "#cartModal .close-modal")

    def is_visible(self) -> bool:
        """모달의 노출 여부를 반환한다."""
        return self.is_element_visible(self.MODAL)

    def get_icon_box_background_color(self) -> str:
        """아이콘 컨테이너(`.icon-box`)의 배경색(`background-color`)을 조회해 반환한다
        (Assertion 없음)."""
        return self.get_css_value(self.ICON_BOX, "background-color")

    def get_title_text(self) -> str:
        """모달 제목("Added!") 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.TITLE)

    def get_body_message_text(self) -> str:
        """안내 문구("Your product has been added to cart.") 텍스트를 조회해 반환한다
        (Assertion 없음)."""
        return self.get_text(self.BODY_MESSAGE)

    def get_view_cart_link_text(self) -> str:
        """"View Cart" 링크 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.VIEW_CART_LINK)

    def get_view_cart_link_color(self) -> str:
        """"View Cart" 링크의 글자색(`color`)을 조회해 반환한다(Assertion 없음)."""
        return self.get_css_value(self.VIEW_CART_LINK, "color")

    def click_view_cart(self) -> None:
        """"View Cart" 링크를 클릭해 장바구니(`/view_cart`) 페이지로 이동한다.

        실제 페이지 전체 이동(`<a href="/view_cart">`)을 트리거하므로 Google Vignette 광고
        개입 위험이 있어 `click_and_retry_if_vignette()`를 사용한다(위 docstring 참고).
        """
        self.click_and_retry_if_vignette(self.VIEW_CART_LINK)

    def get_continue_shopping_button_text(self) -> str:
        """"Continue Shopping" 버튼 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.CONTINUE_SHOPPING_BUTTON)

    def get_continue_shopping_button_background_color(self) -> str:
        """"Continue Shopping" 버튼의 배경색(`background-color`)을 조회해 반환한다
        (Assertion 없음)."""
        return self.get_css_value(self.CONTINUE_SHOPPING_BUTTON, "background-color")

    def click_continue_shopping(self) -> None:
        """"Continue Shopping" 버튼을 클릭해 모달을 닫는다.

        `data-dismiss="modal"` 버튼으로 페이지 이동을 트리거하지 않으므로(위 docstring
        참고) 일반 `click()`을 사용한다.
        """
        self.click(self.CONTINUE_SHOPPING_BUTTON)
