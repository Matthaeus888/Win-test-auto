"""Cart 페이지(/view_cart)를 다루는 Page Object.

Source of Truth:
- docs/tc/top-navigation.md (TC-TOP-NAVIGATION-003, 004, 005)
- docs/prd/feature/top-navigation.md 상단 네비게이션 시나리오
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-30, https://automationexercise.com/view_cart,
로그아웃 상태, 빈 장바구니 상태):
- 상단 네비게이션(`ul.navbar-nav`, 실제 class 속성값 "nav navbar-nav") 하위 8개 `<li><a>`
  (Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video Tutorials/Contact us)가
  `home_page.py`/`products_page.py`가 실측한 구조와 완전히 동일한 마크업임을
  browser_evaluate로 재확인했다(class/개수/href 값 모두 동일). 이에 따라 HomePage/
  ProductsPage와 동일하게 4순위(안정적인 CSS Selector, href 기반)를 사용한다.
- **HOME_LINK/PRODUCTS_LINK 고유성 실측 결과(중요)**: Cart 페이지에서도 ProductsPage와
  마찬가지로 `a[href='/']`, `a[href='/products']`가 페이지 전체 기준으로 **고유하지
  않음**을 `document.querySelectorAll(...).length`로 실측 확인했다.
  - `a[href='/']`은 페이지 전체 기준 **3개** 존재 — 상단 네비게이션의 "Home" 메뉴
    (`<a href="/"><i class="fa fa-home"></i> Home</a>`) 외에, 헤더 로고 이미지 링크
    (`<a href="/"><img src="/static/images/home/logo.png" ...></a>`), 그리고 Cart
    페이지 상단 브레드크럼의 "Home" 링크(`<a href="/">Home</a>`, 브레드크럼은
    ProductsPage/HomePage에는 없는 Cart 페이지 고유 요소)까지 총 3개가 동일 href를
    가진다(ProductsPage의 2개보다 1개 더 많음 — 브레드크럼 때문).
  - `a[href='/products']`도 페이지 전체 기준 **2개** 존재 — 상단 네비게이션의
    "Products" 메뉴 외에, 실측 시점에 장바구니가 비어 있어 노출된 "Cart is empty!
    Click here to buy products." 안내 메시지의 "here" 링크
    (`<a href="/products"><u>here</u></a>`)가 동일 href를 가진다.
  - `ul.navbar-nav` 컨테이너로 범위를 좁히면(`ul.navbar-nav a[href='/']`,
    `ul.navbar-nav a[href='/products']`) 각각 고유해짐을
    (`document.querySelectorAll(...).length === 1`로) 검증했으나, Approved TC
    (TC-TOP-NAVIGATION-001~006) 중 Cart 페이지에서 "Home"/"Products" 메뉴를 클릭해야
    하는 TC가 없어(TC-004/005는 `navigate()`로 페이지를 직접 이동) 2026-08-31 코드
    리뷰에서 미사용(dead code)으로 지적되어 `HOME_LINK`/`PRODUCTS_LINK`와
    `click_home()`/`click_products()`를 제거했다(CLAUDE.md 12절 "불필요한 코드 생성
    금지"). 이후 Phase에서 실제로 필요해지면 이 실측 근거를 참고해 다시 추가하면 된다.
  - 반면 `SIGNUP_LOGIN_LINK`(`a[href='/login']`)는 Cart 페이지에서도 페이지 전체
    기준 1개뿐임을 재확인해(HomePage/ProductsPage와 동일), 범위를 좁히지 않고 그대로
    재사용한다.

로그인 상태 전용 Locator(LOGOUT_LINK, DELETE_ACCOUNT_LINK, LOGGED_IN_AS_TEXT) 처리 근거:
- Playwright MCP는 조회·탐색 전용 도구로 실제 로그인 상태를 만들 수 없어(AUTOMATION_GUIDE
  5.3절), 이 Task에서는 Cart 페이지에서 직접 실측하지 못했다. 다만 `home_page.py`가
  2026-08-29 Task 5(실제 pytest 실행, 고정 계정 actest1로 실제 로그인)에서 이미 실측
  확정하고 `products_page.py`가 동일 `ul.navbar-nav` 구조 근거로 재사용한
  `a[href='/logout']`, `a[href='/delete_account']`,
  `//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]` 3개
  Locator를, 이 Task에서 재확인한 Cart 페이지의 `ul.navbar-nav` 컨테이너가 Home/Products
  페이지와 완전히 동일한 구조라는 근거로 동일하게 재사용한다. **로그인 상태에서의 최종
  검증은 이 Task의 범위가 아니며, 후속 테스트 Task(pytest 실행)에서 실제 로그인 후
  확인된다.**
- 로그아웃 상태 DOM에는 `/logout`, `/delete_account` 링크가 존재하지 않음(각 0개)을
  Cart 페이지에서도 재확인했다(HomePage/ProductsPage와 동일한 서버 조건부 렌더링 방식).

Phase 5 확장(장바구니 목록/삭제/빈 카트/Proceed To Checkout, Playwright MCP 실측,
2026-08-31, https://automationexercise.com/view_cart, 로그아웃 상태):
- 상품이 담긴 상태에서 `#cart_info_table`(id, 페이지 전체 기준 1개)을 실측한 결과, 상품 1행당
  `<tr id="product-{id}">` 구조이며 `id`/`data-qa` 속성이 없는 하위 요소는 클래스 기반 CSS로
  범위를 좁혔다(6.1절 4순위). 각 행 내부에서 아래 셀렉터가 행(`WebElement`) 스코프 기준
  1개씩만 존재함을 확인했다:
  - `.cart_description h4 a`(상품명, `href="/product_details/{id}"`)
  - `.cart_price p`(단가, 예: "Rs. 500")
  - `.cart_quantity button`(수량, `<button class="disabled">7</button>` - `disabled` 클래스만
    있고 실제 `disabled` 속성/`readonly`는 없으나 편집 불가 동작 자체는 TC-CART-007 Rejected로
    자동화 대상이 아니라 이 Phase에서는 텍스트 조회만 사용)
  - `.cart_total p`(합계, 예: "Rs. 3500")
  - `.cart_quantity_delete`(삭제 버튼, `<a class="cart_quantity_delete" data-product-id="{id}">`)
- 상품 상세 페이지(`/product_details/1`)에서 Quantity를 7로 지정해 담은 뒤 장바구니 행을
  재조회한 결과 `Quantity: 7`, `Total: Rs. 3500`(단가 Rs.500 x 7)로 정확히 반영됨을
  실측으로 확인했다(TC-CART-006 판정에 사용, 상세 페이지 담기 수량이 장바구니에 그대로
  전달되는 것을 재확인).
- 삭제(`.cart_quantity_delete`) 클릭은 페이지 전체 리로드 없이 AJAX로 처리됨을 확인했다(클릭
  전후 `document.title`/URL이 변하지 않고, 곧바로 `#cart_info_table tbody tr` 개수만
  감소). 이에 따라 삭제 직후 즉시 행 개수를 조회하면 아직 갱신되지 않은 상태를 읽을 수
  있어(Flaky 원인), `wait_for_cart_row_count()`로 명시적으로 대기한 뒤 조회하도록 설계했다.
- 마지막 상품을 삭제하면 `#cart_info_table`은 DOM에서 제거되지 않고 `display: none`으로
  전환되며(`getComputedStyle().display === 'none'`), 대신 `id="empty_cart"`
  (페이지 전체 기준 1개, 6.1절 1순위 id 적용) 요소가 `display: block`으로 전환되어 "Cart is
  empty! Click here to buy products." 문구가 노출됨을 확인했다(`page-ui.md`
  TC-PAGE-UI-019와 동일 문구, TC-CART-009/014 판정에 사용). `EC.visibility_of_element_located`
  기반 `BasePage.is_element_visible()`은 `WebElement.is_displayed()`를 사용해
  `display: none`을 정확히 "보이지 않음"으로 판정하므로 이 전환을 그대로 활용할 수 있다.
- "Proceed To Checkout" 버튼은 `id`/`data-qa`가 없고 `<a class="btn btn-default
  check_out">Proceed To Checkout</a>` 형태로 `href` 속성 자체가 없는(JavaScript로 동작을
  분기하는) 요소이며, `.check_out` 클래스가 페이지 전체 기준 1개로 고유함을 확인했다(6.1절
  4순위). 로그인 상태에서 클릭 시 실제로 `/checkout`으로 페이지 전체 이동이 발생하므로(TC-CART-011),
  다른 페이지 이동 링크와 동일하게 `click_and_retry_if_vignette()`를 사용한다.

Phase 7 확장(상품 목록 표 컬럼/빈 카트 링크, Playwright MCP 실측, 2026-09-01,
https://automationexercise.com/view_cart, 상품 1개 담긴 상태 - 5.4절 "MCP 브라우저와 실제
테스트(Selenium) 환경이 다르게 동작함" 관련 참고: 이번 세션의 MCP 브라우저에 예상치 못한
기존 로그인 세션/장바구니 데이터가 남아있어 이를 그대로 조회만 하고 활용했다,
`pages/home_page.py` docstring "예상치 못한 관찰 사항" 참고):
- 장바구니 행(TC-PAGE-UI-021) 내부에 `.cart_product img`(이미지, 행 스코프 1개)/
  `.cart_description p`(상품명 아래 카테고리 경로, 예: "Women > Tops", 행 스코프 1개)가
  각각 고유하게 존재함을 확인했다(기존 `ROW_PRODUCT_NAME`은 `.cart_description h4 a`로
  상품명만 조회, 카테고리 경로는 별도 `<p>`).
- 빈 카트 안내(TC-PAGE-UI-019) 내부의 "here" 링크는 `#empty_cart a`(페이지 전체 기준 1개,
  `href="/products"`, 텍스트 "here")로 고유하게 식별된다.
- "Proceed To Checkout" 버튼(TC-PAGE-UI-020) 노출 여부는 기존 `PROCEED_TO_CHECKOUT_BUTTON`
  Locator를 그대로 재사용해 `is_element_visible()`로 조회한다(신규 Locator 불필요).
"""

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from pages.base_page import BasePage
from utils.text import normalize_whitespace


class CartPage(BasePage):
    """Cart 페이지(/view_cart)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/get_text/is_element_visible/find_element)만 사용해 요소를 조작·조회한다.
    화면 단위 1 Page 클래스 원칙에 따라 HomePage/ProductsPage와 마크업 패턴은 유사하지만
    별도 클래스로 구현한다(ProductsPage와 동일한 설계 결정).
    """

    # 상단 네비게이션(로그아웃 상태) - Playwright MCP 실측 확인 완료(HomePage/ProductsPage와 동일값)
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

    # 상단 네비게이션(로그인 상태) - HomePage/ProductsPage 실측 결과를 근거로 동일 값 사용
    # (위 docstring 참고, 최종 검증은 후속 테스트 Task에서 수행)
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/delete_account']")
    LOGGED_IN_AS_TEXT = (
        By.XPATH,
        "//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]",
    )

    # 상단 네비게이션 메뉴 구성 전체 조회용(ul.navbar-nav 하위 모든 li>a, 8개 실측 확인)
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "ul.navbar-nav li > a")

    # 장바구니 목록/삭제/빈 카트/Proceed To Checkout(Phase 5) - Playwright MCP 실측 확인
    # 완료(위 docstring "Phase 5 확장" 참고). `#cart_info_table`은 행 스코프 CSS Selector
    # (CART_ROWS)에 이미 포함되어 있어 별도 상수로 정의하지 않는다(CLAUDE.md 12절 "불필요한
    # 코드 생성 금지").
    CART_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    EMPTY_CART_MESSAGE = (By.ID, "empty_cart")
    PROCEED_TO_CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".check_out")

    # 장바구니 행(WebElement) 기준 상대 Locator(위 docstring 참고). 단가(`.cart_price p`)는
    # Approved TC 중 이를 조회하는 시나리오가 없어(TC-CART-005/006은 합계로 판정) 상수를
    # 추가하지 않았다(CLAUDE.md 12절).
    ROW_PRODUCT_NAME = (By.CSS_SELECTOR, ".cart_description h4 a")
    ROW_QUANTITY = (By.CSS_SELECTOR, ".cart_quantity button")
    ROW_TOTAL = (By.CSS_SELECTOR, ".cart_total p")
    ROW_DELETE_BUTTON = (By.CSS_SELECTOR, ".cart_quantity_delete")
    # 상품 목록 표 컬럼(Phase 7, TC-PAGE-UI-021) - Playwright MCP 실측 확인 완료(위
    # docstring "Phase 7 확장" 참고)
    ROW_IMAGE = (By.CSS_SELECTOR, ".cart_product img")
    ROW_CATEGORY_PATH = (By.CSS_SELECTOR, ".cart_description p")

    # 빈 카트 안내 "here" 링크(Phase 7, TC-PAGE-UI-019) - Playwright MCP 실측 확인 완료
    EMPTY_CART_LINK = (By.CSS_SELECTOR, "#empty_cart a")

    def navigate(self) -> None:
        """Cart 페이지(/view_cart)로 이동한다."""
        url = f"{BASE_URL.rstrip('/')}/view_cart"
        self.driver.get(url)
        self.logger.info("Cart 페이지로 이동: %s", url)

    def is_logged_out_menu_visible(self) -> bool:
        """로그아웃 상태 메뉴("Signup / Login")의 노출 여부를 반환한다."""
        return self.is_element_visible(self.SIGNUP_LOGIN_LINK)

    def is_logged_in_menu_visible(self) -> bool:
        """로그인 상태 메뉴(Logout, Delete Account)의 노출 여부를 반환한다.

        두 메뉴가 모두 노출되는 경우에만 True를 반환한다.
        """
        return self.is_element_visible(self.LOGOUT_LINK) and self.is_element_visible(
            self.DELETE_ACCOUNT_LINK
        )

    def get_logged_in_user_text(self) -> str:
        """"Logged in as {유저명}" 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.LOGGED_IN_AS_TEXT)

    def get_nav_menu_item_texts(self) -> list[str]:
        """상단 네비게이션 메뉴 전체 항목의 텍스트를 순서대로 조회해 반환한다(Assertion 없음).

        `BasePage`에는 다건 조회 메서드가 없으므로, 먼저 `find_element()`로 첫 메뉴 항목이
        DOM에 로드될 때까지 명시적으로 대기한 뒤 `driver.find_elements()`(복수형)로 전체
        메뉴 항목을 한 번에 조회한다(ProductsPage와 동일한 구현 패턴).
        """
        self.find_element(self.NAV_MENU_ITEMS)
        elements = self.driver.find_elements(*self.NAV_MENU_ITEMS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("상단 네비게이션 메뉴 텍스트 조회 완료: %s", texts)
        return texts

    def get_cart_row_count(self) -> int:
        """장바구니에 담긴 상품 행 개수를 반환한다(Assertion 없음).

        `driver.find_elements()`(복수형)는 대상이 없으면 즉시 빈 리스트를 반환하고
        `WebDriverWait` 폴링을 하지 않으므로, 빈 카트 상태에서도 무한 대기 없이 안전하게
        0을 반환한다.
        """
        count = len(self.driver.find_elements(*self.CART_ROWS))
        self.logger.debug("장바구니 행 개수 조회 완료: %s", count)
        return count

    def get_product_names(self) -> list[str]:
        """장바구니에 담긴 상품명 목록을 행 순서대로 반환한다(Assertion 없음)."""
        rows = self.driver.find_elements(*self.CART_ROWS)
        names = [row.find_element(*self.ROW_PRODUCT_NAME).text.strip() for row in rows]
        self.logger.debug("장바구니 상품명 목록 조회 완료: %s", names)
        return names

    def _find_row_by_product_name(self, product_name: str) -> WebElement:
        """상품명(공백 정규화 후 비교)과 일치하는 첫 장바구니 행을 찾아 반환한다
        (Assertion 없음).

        [2026-08-31 코드 리뷰 반영] 일치하는 행이 없는 경우의 에러 로그에 쓸 상품명
        목록을 검색 루프 중에 함께 수집해, 실패 경로에서 동일한 `find_element()` 조회를
        한 번 더 반복하지 않도록 했다.

        Raises:
            NoSuchElementException: 일치하는 상품명을 가진 행이 없는 경우(원인을 로깅한 뒤
                재전파, AUTOMATION_GUIDE 15절 "예외를 조용히 삼키지 않는다").
        """
        rows = self.driver.find_elements(*self.CART_ROWS)
        target = normalize_whitespace(product_name)
        row_names = []
        for row in rows:
            name = row.find_element(*self.ROW_PRODUCT_NAME).text.strip()
            row_names.append(name)
            if normalize_whitespace(name) == target:
                return row
        self.logger.error(
            "장바구니에서 상품명과 일치하는 행을 찾을 수 없음: %s (조회된 상품명 목록: %s)",
            product_name,
            row_names,
        )
        raise NoSuchElementException(f"장바구니에서 상품명을 찾을 수 없음: {product_name}")

    def get_quantity_by_product_name(self, product_name: str) -> str:
        """상품명으로 장바구니 행을 찾아 Quantity 텍스트를 조회해 반환한다(Assertion 없음)."""
        row = self._find_row_by_product_name(product_name)
        quantity = row.find_element(*self.ROW_QUANTITY).text.strip()
        self.logger.debug("'%s' 상품 Quantity 조회 완료: %s", product_name, quantity)
        return quantity

    def get_total_by_product_name(self, product_name: str) -> str:
        """상품명으로 장바구니 행을 찾아 Total 텍스트를 조회해 반환한다(Assertion 없음)."""
        row = self._find_row_by_product_name(product_name)
        total = row.find_element(*self.ROW_TOTAL).text.strip()
        self.logger.debug("'%s' 상품 Total 조회 완료: %s", product_name, total)
        return total

    def delete_product_by_name(self, product_name: str) -> None:
        """상품명으로 장바구니 행을 찾아 삭제(x) 버튼을 클릭한다.

        삭제는 AJAX로 처리되어 이 메서드 반환 시점에 DOM 갱신이 아직 끝나지 않았을 수
        있으므로(위 docstring 참고), 삭제 결과 확인은 호출부에서
        `wait_for_cart_row_count()` 등으로 명시적으로 대기해야 한다.
        """
        row = self._find_row_by_product_name(product_name)
        delete_button = row.find_element(*self.ROW_DELETE_BUTTON)
        self.click_element(delete_button)
        self.logger.info("'%s' 상품 삭제 버튼 클릭 완료", product_name)

    def wait_for_cart_row_count(self, expected_count: int, timeout: int = DEFAULT_TIMEOUT) -> None:
        """장바구니 행 개수가 기대값이 될 때까지 대기한다(Assertion 없음).

        상품 삭제는 AJAX로 처리되어 페이지 전체 리로드 없이 DOM만 갱신되므로(위 docstring
        참고), 삭제 클릭 직후 곧바로 행 개수를 조회하면 아직 갱신되지 않은 상태를 읽을 수
        있다(Flaky 원인). `WebDriverWait`으로 행 개수가 기대값에 도달할 때까지 명시적으로
        대기한다.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: len(d.find_elements(*self.CART_ROWS)) == expected_count
            )
            self.logger.debug("장바구니 행 개수가 기대값(%s)에 도달함", expected_count)
        except TimeoutException:
            self.logger.error(
                "장바구니 행 개수가 기대값(%s)에 도달하지 않음(Timeout)", expected_count
            )
            raise

    def is_empty_cart_message_visible(self) -> bool:
        """빈 카트 안내 문구("Cart is empty! ...")의 노출 여부를 반환한다."""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE)

    def get_empty_cart_message_text(self) -> str:
        """빈 카트 안내 문구 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.EMPTY_CART_MESSAGE)

    def click_proceed_to_checkout(self) -> None:
        """"Proceed To Checkout" 버튼을 클릭한다.

        로그인 상태에서는 실제 페이지 전체 이동(`/checkout`)을 트리거하므로(위 docstring
        참고) `click_and_retry_if_vignette()`를 사용한다. 로그아웃 상태에서는 페이지 이동
        없이 로그인 요구 모달(`CheckoutPage`)이 노출된다.
        """
        self.click_and_retry_if_vignette(self.PROCEED_TO_CHECKOUT_BUTTON)

    def is_proceed_to_checkout_button_visible(self) -> bool:
        """"Proceed To Checkout" 버튼의 노출 여부를 반환한다(Phase 7, TC-PAGE-UI-020)."""
        return self.is_element_visible(self.PROCEED_TO_CHECKOUT_BUTTON)

    def is_row_image_visible(self, product_name: str) -> bool:
        """상품명으로 장바구니 행을 찾아 이미지의 노출 여부를 반환한다(Phase 7,
        TC-PAGE-UI-021)."""
        row = self._find_row_by_product_name(product_name)
        elements = row.find_elements(*self.ROW_IMAGE)
        return bool(elements) and elements[0].is_displayed()

    def get_category_path_by_product_name(self, product_name: str) -> str:
        """상품명으로 장바구니 행을 찾아 카테고리 경로(예: "Women > Tops") 텍스트를 조회해
        반환한다(Phase 7, TC-PAGE-UI-021, Assertion 없음)."""
        row = self._find_row_by_product_name(product_name)
        category_path = row.find_element(*self.ROW_CATEGORY_PATH).text.strip()
        self.logger.debug("'%s' 상품 카테고리 경로 조회 완료: %s", product_name, category_path)
        return category_path

    def is_delete_button_visible_by_product_name(self, product_name: str) -> bool:
        """상품명으로 장바구니 행을 찾아 삭제(x) 버튼의 노출 여부를 반환한다(Phase 7,
        TC-PAGE-UI-021)."""
        row = self._find_row_by_product_name(product_name)
        elements = row.find_elements(*self.ROW_DELETE_BUTTON)
        return bool(elements) and elements[0].is_displayed()

    def is_empty_cart_link_visible(self) -> bool:
        """빈 카트 안내 문구 내 "here" 링크의 노출 여부를 반환한다(Phase 7,
        TC-PAGE-UI-019)."""
        return self.is_element_visible(self.EMPTY_CART_LINK)

    def get_empty_cart_link_text(self) -> str:
        """빈 카트 안내 문구 내 "here" 링크 텍스트를 조회해 반환한다(Phase 7,
        TC-PAGE-UI-019, Assertion 없음)."""
        return self.get_text(self.EMPTY_CART_LINK)
