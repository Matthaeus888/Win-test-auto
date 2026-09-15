"""Products 페이지(/products)를 다루는 Page Object.

Source of Truth:
- docs/tc/top-navigation.md (TC-TOP-NAVIGATION-001, 002, 004, 005)
- docs/prd/feature/top-navigation.md 상단 네비게이션 시나리오
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-30, https://automationexercise.com/products,
로그아웃 상태):
- 상단 네비게이션(`ul.navbar-nav`, 실제 class 속성값 "nav navbar-nav") 하위 8개 `<li><a>`
  (Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video Tutorials/Contact us)가
  `home_page.py`가 실측한 Home 페이지(`/`)와 완전히 동일한 마크업 구조임을
  browser_evaluate로 재확인했다(class/개수/id·data-qa·name 부재 여부 모두 동일). 이에
  따라 HomePage와 동일하게 4순위(안정적인 CSS Selector, href 기반)를 사용한다.
- **HomePage와의 차이점(중요)**: Products 페이지에서는 `a[href='/']`,
  `a[href='/view_cart']`가 페이지 전체 기준으로 **고유하지 않음**을
  `document.querySelectorAll(...)`.length로 실측 확인했다.
  - `a[href='/']`은 2개 존재 — 상단 네비게이션의 "Home" 메뉴(`<a href="/"><i
    class="fa fa-home"></i> Home</a>`) 외에, 헤더 로고 이미지 링크(`<a href="/"><img
    src="/static/images/home/logo.png" ...></a>`)가 동일 href를 가진다.
  - `a[href='/view_cart']`도 2개 존재 — 상단 네비게이션의 "Cart" 메뉴 외에, "Add to
    cart" 확인 모달 내부의 "View Cart" 링크(`<a href="/view_cart"><u>View
    Cart</u></a>`)가 동일 href를 가진다(Products 목록 페이지는 상품 카드마다 "Add to
    cart" 모달을 갖고 있어 이 중복 요소가 DOM에 존재한다).
  - 따라서 `HOME_LINK`는 `ul.navbar-nav` 컨테이너로 범위를 좁힌 CSS Selector
    (`ul.navbar-nav a[href='/']`)를 사용해 고유성을 확보했다
    (`document.querySelectorAll("ul.navbar-nav a[href='/']").length === 1`로 검증
    완료). `a[href='/view_cart']`도 동일하게 2개 존재함을 확인했으나, Approved TC
    (TC-TOP-NAVIGATION-001~006) 중 Products 페이지에서 "Cart" 메뉴를 클릭해야 하는
    TC가 없어(TC-004/005는 `navigate()`로 페이지를 직접 이동) 2026-08-31 코드 리뷰에서
    미사용(dead code)으로 지적되어 `CART_LINK`/`click_cart()`를 제거했다(CLAUDE.md
    12절 "불필요한 코드 생성 금지"). 이후 Phase에서 실제로 필요해지면 이 실측 근거를
    참고해 다시 추가하면 된다.
  - 반면 `SIGNUP_LOGIN_LINK`(`a[href='/login']`)는 Products 페이지에서도 페이지 전체
    기준 1개뿐임을 재확인해(HomePage와 동일), 범위를 좁히지 않고 그대로 재사용한다.

로그인 상태 전용 Locator(LOGOUT_LINK, DELETE_ACCOUNT_LINK, LOGGED_IN_AS_TEXT) 처리 근거:
- Playwright MCP는 조회·탐색 전용 도구로 실제 로그인 상태를 만들 수 없어(AUTOMATION_GUIDE
  5.3절), 이 Task에서는 Products 페이지에서 직접 실측하지 못했다. 다만 `home_page.py`가
  2026-08-29 Task 5(실제 pytest 실행, 고정 계정 actest1로 실제 로그인)에서 이미 실측
  확정한 `a[href='/logout']`, `a[href='/delete_account']`,
  `//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]` 3개
  Locator와 위에서 재확인한 대로 Products 페이지의 `ul.navbar-nav` 컨테이너가 Home
  페이지와 완전히 동일한 구조라는 근거로 동일 값을 그대로 사용한다. **로그인 상태에서의
  최종 검증은 이 Task의 범위가 아니며, 후속 테스트 Task(pytest 실행)에서 실제 로그인 후
  확인된다.**
- 로그아웃 상태 DOM에는 `/logout`, `/delete_account` 링크가 존재하지 않음(각 0개)을
  Products 페이지에서도 재확인했다(HomePage와 동일한 서버 조건부 렌더링 방식).

Locator 확정 근거(Playwright MCP 실측, 2026-08-31, https://automationexercise.com/products
및 https://automationexercise.com/products?search=shirt /
https://automationexercise.com/products?search=zzzzznonexistent) - Phase 4 Task 1
(검색 기능 확장):
- 검색창/버튼은 `browser_evaluate`로 `document.querySelector('#search_product')` /
  `#submit_search`가 각각 1개씩 존재함을 확인했다. 두 요소 모두 `id` 속성이 존재해(6.1절
  1순위) `SEARCH_INPUT`/`SEARCH_BUTTON`을 `By.ID`로 정의했다. `id="search_product"`,
  `id="submit_search"`이며 페이지 하단 뉴스레터 구독 입력창(`Your email address`)과는
  별개의 요소임을 확인했다(뉴스레터 입력창은 다른 id를 사용, 혼동 없음).
- 섹션 제목은 `.features_items h2.title` 하나뿐임을
  `document.querySelectorAll('.features_items h2.title').length === 1`로 확인했다(전체
  목록 상태에서는 텍스트 "All Products", 검색 실행 후에는 "Searched Products" — 화면
  표시는 CSS `text-transform`으로 대문자화되어 "ALL PRODUCTS"/"SEARCHED PRODUCTS"로
  보이지만 DOM 텍스트 자체는 대소문자 혼용임). id/data-qa가 없어 4순위(안정적 CSS
  Selector)를 적용했다.
- 상품 카드 반복 컨테이너는 `.features_items .col-sm-4`(카드 1개 = 이미지/가격/상품명/
  Add to cart를 담은 `.product-image-wrapper`와 "View Product" 링크를 담은 `.choose`
  형제 요소를 모두 포함하는 최상위 반복 단위)로 확정했다. `/products` 전체 목록에서
  `document.querySelectorAll('.features_items .col-sm-4').length === 34`(실제 상품
  카드 수와 일치)임을 확인했고, `?search=shirt` 결과 페이지에서는 13개로 정확히
  줄어듦을 확인했다(id/data-qa 없어 4순위 CSS Selector 적용, `.product-image-wrapper`
  단독으로는 "View Product" 링크를 포함하지 않아 카드 전체 단위로는 부족함을 실측으로
  확인하고 상위 `.col-sm-4`를 채택).
- 카드 내부 상대 Locator는 각 카드(`.col-sm-4`) 기준으로 다음과 같이 확정했다(모두 카드
  스코프 내 1개씩만 존재함을 `querySelectorAll` count로 확인):
  - `PRODUCT_CARD_IMAGE` = `.productinfo img` (카드당 1개)
  - `PRODUCT_CARD_PRICE` = `.productinfo h2` (카드당 1개, 예: "Rs. 500")
  - `PRODUCT_CARD_NAME` = `.productinfo p` (카드당 1개, 예: "Blue Top")
  - `PRODUCT_CARD_ADD_TO_CART` = `.productinfo .add-to-cart` — 카드 마크업에는
    hover 시 노출되는 `.product-overlay .overlay-content` 안에도 동일한 클래스
    (`.add-to-cart`)를 가진 버튼이 중복 존재해(카드 스코프에서 `.add-to-cart`만으로는
    2개) `.productinfo` 하위로 범위를 좁혀 1개로 고유화했다. `.productinfo` 내부의
    버튼은 `getComputedStyle`로 `display: inline-block`, `visibility: visible`임을
    확인해 기본 노출(hover 불필요) 상태임도 확인했다.
  - `PRODUCT_CARD_VIEW_PRODUCT` = `.choose a` (카드당 1개, `href="/product_details/{id}"`)
- 검색 결과 0건 페이지(`?search=zzzzznonexistent`)에서 `.features_items .col-sm-4`가
  0개이고 섹션 제목 요소(`.features_items h2.title`)는 그대로 존재("Searched
  Products")하며, "No result"류의 별도 안내 문구는 `document.body.innerText`에
  없음을 확인했다(TC-PRODUCT-SEARCH-003 기대 결과와 일치).

Phase 5 확장(Add to cart 클릭, Playwright MCP 실측, 2026-08-31,
https://automationexercise.com/products, 로그아웃 상태):
- 기존 `PRODUCT_CARD_ADD_TO_CART`(`.productinfo .add-to-cart`)를 그대로 재사용해 실제 클릭
  동작을 확인했다. 카드 내부 버튼은 페이지 전체에서 카드 수만큼 중복 존재하는 셀렉터라
  `BasePage.click(locator)`로는 특정 카드를 지정할 수 없어, `_get_card_element(index)`로
  조회한 `WebElement`를 `BasePage.click_element(element)`로 직접 클릭하는 방식을
  사용한다(`home_page.py`와 동일한 패턴). 클릭 시 담기 확인 모달(`id="cartModal"`)이
  노출됨을 재확인했다(`pages/add_to_cart_modal.py` docstring 참고). 확인 후 방금 담은
  상품은 장바구니에서 삭제해 탐색 세션을 원상 복구했다.
- TC-CART-005 테스트 데이터("Sleeveless Dress", 단가 Rs.1000)를 실측한 결과, 실제 상품
  카드 목록에 존재하는 상품명은 DOM 텍스트 그대로 `"Sleeveless  Dress"`(단어 사이에 공백이
  2칸)이며 단가는 "Rs. 1000"으로 `docs/tc/cart.md` 승인된 예시값과 정확히 일치함을
  확인했다(가격 불일치 없음, 상품명은 공백 개수만 다름 - `find_card_index_by_product_name()`이
  비교 시 공백을 정규화해 처리한다). `.features_items .col-sm-4`에서 34개 카드 중 3번째
  (index=2, `data-product-id="3"`)로 확인됐다.

Phase 7 확장(CATEGORY 아코디언, Playwright MCP 실측, 2026-09-01,
https://automationexercise.com/products, 로그아웃 상태):
- 좌측 사이드바의 `#accordian`/`.panel-heading a`/`.panel-collapse` 구조가 `home_page.py`가
  실측한 Home 페이지 구조와 완전히 동일함을 재확인했다(`document.querySelectorAll('#accordian')
  .length === 1`, `.panel-heading a[data-toggle="collapse"][data-parent="#accordian"]`가
  3개). Home 페이지와 별개 Page 클래스이므로(화면 단위 1 Page 클래스 원칙) 동일한 Locator/
  메서드를 이 클래스에도 독립적으로 정의한다(`home_page.py` "Phase 7 확장" docstring 참고,
  동일한 실측 근거 재사용).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from pages.base_page import BasePage
from utils.text import normalize_whitespace


class ProductsPage(BasePage):
    """Products 페이지(/products)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/get_text/is_element_visible/find_element)만 사용해 요소를 조작·조회한다.
    화면 단위 1 Page 클래스 원칙에 따라 HomePage와 마크업 패턴은 유사하지만 별도 클래스로
    구현한다(Phase 2의 AccountCreatedPage/AccountDeletedPage와 동일한 설계 결정).
    """

    # 상단 네비게이션 - Playwright MCP 실측 확인 완료(위 docstring 참고)
    # HOME_LINK는 페이지 내 중복 href(로고)와 구분하기 위해 ul.navbar-nav 컨테이너로
    # 범위를 좁혔다(HomePage와의 차이점, 위 docstring 참고).
    HOME_LINK = (By.CSS_SELECTOR, "ul.navbar-nav a[href='/']")

    # 상단 네비게이션(로그아웃 상태) - Playwright MCP 실측 확인 완료(HomePage와 동일값)
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

    # 상단 네비게이션(로그인 상태) - HomePage 실측 결과를 근거로 동일 값 사용(위 docstring
    # 참고, 최종 검증은 후속 테스트 Task에서 수행)
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/delete_account']")
    LOGGED_IN_AS_TEXT = (
        By.XPATH,
        "//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]",
    )

    # 상단 네비게이션 메뉴 구성 전체 조회용(ul.navbar-nav 하위 모든 li>a, 8개 실측 확인)
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "ul.navbar-nav li > a")

    # 검색 기능(Phase 4 Task 1) - Playwright MCP 실측 확인 완료(위 docstring 참고)
    # id 속성이 실제로 존재함을 확인해 6.1절 1순위(id)를 적용한다.
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")

    # 상품 목록 상단 섹션 제목 - "ALL PRODUCTS"/"SEARCHED PRODUCTS" 공용(위 docstring 참고)
    SECTION_TITLE = (By.CSS_SELECTOR, ".features_items h2.title")

    # 검색 결과/전체 목록 공용 상품 카드 컨테이너(카드 1개 = .col-sm-4 전체 반복 단위,
    # find_elements로 복수 조회 대상). 위 docstring 참고.
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".features_items .col-sm-4")

    # 카드 내부 요소 - 카드 하나(WebElement)를 기준으로 한 상대 Locator(위 docstring 참고).
    PRODUCT_CARD_IMAGE = (By.CSS_SELECTOR, ".productinfo img")
    PRODUCT_CARD_PRICE = (By.CSS_SELECTOR, ".productinfo h2")
    PRODUCT_CARD_NAME = (By.CSS_SELECTOR, ".productinfo p")
    # hover 시 노출되는 .product-overlay 내부에도 동일 클래스가 중복 존재해(위 docstring
    # 참고) .productinfo 하위로 범위를 좁혀 고유화했다.
    PRODUCT_CARD_ADD_TO_CART = (By.CSS_SELECTOR, ".productinfo .add-to-cart")
    PRODUCT_CARD_VIEW_PRODUCT = (By.CSS_SELECTOR, ".choose a")

    # CATEGORY 아코디언(Phase 7, TC-PAGE-UI-032/033) - Playwright MCP 실측 확인 완료
    # (위 docstring "Phase 7 확장" 참고, home_page.py와 동일값)
    CATEGORY_HEADING_WOMEN = (By.CSS_SELECTOR, "#accordian .panel-heading a[href='#Women']")
    CATEGORY_HEADING_MEN = (By.CSS_SELECTOR, "#accordian .panel-heading a[href='#Men']")
    CATEGORY_HEADING_KIDS = (By.CSS_SELECTOR, "#accordian .panel-heading a[href='#Kids']")
    CATEGORY_SUBMENU_WOMEN = (By.ID, "Women")
    CATEGORY_SUBMENU_MEN = (By.ID, "Men")
    CATEGORY_SUBMENU_KIDS = (By.ID, "Kids")

    _CATEGORY_LOCATORS = {
        "WOMEN": (CATEGORY_HEADING_WOMEN, CATEGORY_SUBMENU_WOMEN),
        "MEN": (CATEGORY_HEADING_MEN, CATEGORY_SUBMENU_MEN),
        "KIDS": (CATEGORY_HEADING_KIDS, CATEGORY_SUBMENU_KIDS),
    }

    def navigate(self) -> None:
        """Products 페이지(/products)로 이동한다."""
        url = f"{BASE_URL.rstrip('/')}/products"
        self.driver.get(url)
        self.logger.info("Products 페이지로 이동: %s", url)

    def click_home(self) -> None:
        """"Home" 메뉴를 클릭한다.

        [Phase 3 Task, 2026-08-30 실측] TC-TOP-NAVIGATION-001 pytest 실행 중 재현·확인한
        결함: 이 메뉴 클릭이 실제 페이지 전체 이동(`<a href="/">`)을 트리거하는데, 클릭 직후
        Google Vignette 전면 광고(뷰포트 전체를 덮는 iframe)가 개입해 URL이
        `.../products#google_vignette`에 머물고 실제 Home으로 이동하지 못하는 현상을
        독립 재현 스크립트로 확인했다(BasePage.click_and_retry_if_vignette() docstring에
        이미 기술된 것과 동일한 결함 패턴). `click()` 대신 이미 검증된
        `click_and_retry_if_vignette()`를 사용해 1회 재클릭으로 우회한다.
        """
        self.click_and_retry_if_vignette(self.HOME_LINK)

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
        메뉴 항목을 한 번에 조회한다.
        """
        self.find_element(self.NAV_MENU_ITEMS)
        elements = self.driver.find_elements(*self.NAV_MENU_ITEMS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("상단 네비게이션 메뉴 텍스트 조회 완료: %s", texts)
        return texts

    def search_product(self, keyword: str) -> None:
        """검색창에 keyword를 입력하고 돋보기 아이콘 버튼을 클릭해 검색을 실행한다."""
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        self.logger.info("상품 검색 실행 완료(검색어 입력 후 버튼 클릭)")

    def search_and_press_enter(self, keyword: str) -> None:
        """검색창에 keyword를 입력한 뒤 돋보기 버튼은 클릭하지 않고 Enter 키만 입력한다.

        TC-PRODUCT-SEARCH-008("Enter 키 입력만으로는 검색이 실행되지 않는지 확인") 전용
        동작으로, `BasePage`에는 Enter 키 입력 공통 메서드가 없고 이 Feature에서만 필요한
        1회성 로직이라 신규 공통 메서드를 추가하지 않고 이 메서드 내부에서 직접
        구현한다(AUTOMATION_GUIDE 19절 "특정 Feature 하나에서만 쓰이는 로직을 섣불리
        공통화하지 않는다").
        """
        self.type_text(self.SEARCH_INPUT, keyword)
        self.find_element(self.SEARCH_INPUT).send_keys(Keys.ENTER)
        self.logger.info("검색어 입력 후 Enter 키 입력 완료(버튼 클릭 없음)")

    def get_section_title(self) -> str:
        """상품 목록 상단 섹션 제목("ALL PRODUCTS"/"SEARCHED PRODUCTS")을 조회해
        반환한다(Assertion 없음)."""
        return self.get_text(self.SECTION_TITLE)

    def _wait_for_results_rendered(self) -> None:
        """상품 목록(전체/검색 결과) 렌더링이 끝날 때까지 대기한다(Assertion 없음).

        [2026-08-31 코드 리뷰 반영, finding 2] `SECTION_TITLE`은 전체 목록/검색 결과
        0건/N건 모든 상태에서 항상 존재하는 요소라, 이 요소가 보일 때까지
        `WebDriverWait`으로 대기하면(`get_text()` 재사용) URL 변경 직후 상품 카드
        그리드가 아직 렌더링되지 않은 시점에 `get_product_card_count()`/
        `get_product_names()`가 호출되어 카드를 놓치는 경쟁 조건을 방지할 수 있다.
        """
        self.get_text(self.SECTION_TITLE)

    def get_product_card_count(self) -> int:
        """노출된 상품 카드 개수를 반환한다(Assertion 없음).

        `driver.find_elements()`(복수형)는 대상 요소가 없으면 즉시 빈 리스트를
        반환하고 `WebDriverWait` 폴링을 하지 않으므로, 검색 결과가 0건인 페이지
        (TC-PRODUCT-SEARCH-003)에서도 무한 대기 없이 안전하게 0을 반환한다. 다만
        그 전에 `_wait_for_results_rendered()`로 목록 렌더링 자체는 먼저 대기한다.
        """
        self._wait_for_results_rendered()
        count = len(self.driver.find_elements(*self.PRODUCT_CARDS))
        self.logger.debug("상품 카드 개수 조회 완료: %s", count)
        return count

    def get_product_names(self) -> list[str]:
        """카드별 상품명 텍스트 목록을 순서대로 반환한다(Assertion 없음).

        [2026-08-31 코드 리뷰 반영, finding 2/4] `get_product_card_count()` 호출을
        통한 간접 존재 확인 대신 `_wait_for_results_rendered()`로 직접 렌더링을
        대기한 뒤 `driver.find_elements()`(복수형, 없으면 즉시 빈 리스트)로 한 번만
        조회한다. 기존에는 동일한 `PRODUCT_CARDS` 셀렉터를 3회(카드 개수 확인용
        `find_elements`, 대기용 `find_element`, 실제 조회용 `find_elements`)
        중복 조회했는데, 이를 1회로 줄였다.
        """
        self._wait_for_results_rendered()
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        names = [card.find_element(*self.PRODUCT_CARD_NAME).text.strip() for card in cards]
        self.logger.debug("상품 카드 이름 목록 조회 완료: %s", names)
        return names

    def _get_card_element(self, index: int) -> WebElement:
        """index번째 상품 카드 `WebElement`를 조회해 반환한다(Assertion 없음).

        [2026-08-31 코드 리뷰 반영, finding 2/3] `get_product_price_on_card()`,
        `is_image_visible_on_card()`, `is_add_to_cart_visible_on_card()`,
        `is_view_product_visible_on_card()` 4개 메서드에 중복돼 있던
        `self.driver.find_elements(*self.PRODUCT_CARDS)[index]` 조회 로직을 이 비공개
        헬퍼로 통합했다. index가 실제 카드 개수를 벗어나면 `IndexError`가 발생하는데,
        이를 조용히 삼키지 않고 원인(요청 index/실제 카드 개수)을 `logger.error(...)`로
        남긴 뒤 그대로 재전파한다(AUTOMATION_GUIDE 15절 "예외를 조용히 삼키지
        않는다"). Page Layer 원칙에 따라 Assertion은 수행하지 않는다.
        """
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        try:
            return cards[index]
        except IndexError:
            self.logger.error(
                "요청한 카드 index가 범위를 벗어남(index: %s, 실제 카드 개수: %s)",
                index,
                len(cards),
            )
            raise

    def get_product_price_on_card(self, index: int) -> str:
        """index번째 카드 내부 가격 텍스트를 조회해 반환한다(Assertion 없음)."""
        card = self._get_card_element(index)
        price = card.find_element(*self.PRODUCT_CARD_PRICE).text.strip()
        self.logger.debug("%s번째 카드 가격 조회 완료: %s", index, price)
        return price

    def is_image_visible_on_card(self, index: int) -> bool:
        """index번째 카드 내부 상품 이미지의 노출 여부를 반환한다."""
        card = self._get_card_element(index)
        elements = card.find_elements(*self.PRODUCT_CARD_IMAGE)
        return bool(elements) and elements[0].is_displayed()

    def is_add_to_cart_visible_on_card(self, index: int) -> bool:
        """index번째 카드 내부 "Add to cart" 버튼의 노출 여부를 반환한다."""
        card = self._get_card_element(index)
        elements = card.find_elements(*self.PRODUCT_CARD_ADD_TO_CART)
        return bool(elements) and elements[0].is_displayed()

    def is_view_product_visible_on_card(self, index: int) -> bool:
        """index번째 카드 내부 "View Product" 링크의 노출 여부를 반환한다."""
        card = self._get_card_element(index)
        elements = card.find_elements(*self.PRODUCT_CARD_VIEW_PRODUCT)
        return bool(elements) and elements[0].is_displayed()

    def click_add_to_cart_on_card(self, index: int) -> None:
        """index번째 상품 카드의 "Add to cart" 버튼을 클릭한다(Phase 5, 위 docstring 참고).

        카드 내부 버튼은 페이지 전체에서 카드 수만큼 중복 존재하는 셀렉터라
        `BasePage.click(locator)`로는 특정 카드를 지정할 수 없으므로,
        `_get_card_element(index)`로 조회한 `WebElement`를
        `BasePage.click_element(element)`로 직접 클릭한다.
        """
        card = self._get_card_element(index)
        add_to_cart_button = card.find_element(*self.PRODUCT_CARD_ADD_TO_CART)
        self.click_element(add_to_cart_button)
        self.logger.info("%s번째 상품 카드의 'Add to cart' 클릭 완료", index)

    def find_card_index_by_product_name(self, product_name: str) -> int:
        """상품명(공백 정규화 후 비교)과 일치하는 첫 카드의 index를 찾아 반환한다
        (Assertion 없음).

        TC-CART-005처럼 특정 상품(예: "Sleeveless Dress")을 상품 카탈로그 내 위치와
        무관하게 이름으로 찾아야 하는 시나리오에 사용한다. 실측 결과 일부 상품명의 DOM
        텍스트에 연속 공백이 포함되어 있어(위 docstring 참고) 비교 전 공백을 정규화한다.

        Raises:
            ValueError: 일치하는 상품명을 가진 카드가 없는 경우(원인을 로깅한 뒤 재전파).
        """
        names = self.get_product_names()
        target = normalize_whitespace(product_name)
        for index, name in enumerate(names):
            if normalize_whitespace(name) == target:
                return index
        self.logger.error(
            "상품명과 일치하는 카드를 찾을 수 없음: %s (조회된 상품명 목록: %s)",
            product_name,
            names,
        )
        raise ValueError(f"상품명과 일치하는 카드를 찾을 수 없음: {product_name}")

    def click_category(self, category_name: str) -> None:
        """CATEGORY 아코디언에서 지정한 카테고리(WOMEN/MEN/KIDS)의 헤딩을 클릭해 하위 메뉴를
        펼치거나 접는다(TC-PAGE-UI-032/033, `home_page.py`와 동일한 구현 패턴).

        [코드 리뷰 반영] 클릭+재클릭 로직은 `home_page.py`의 `click_category()`와 거의
        동일하게 중복 구현돼 있었으므로 `BasePage.click_and_wait_for_class_toggle()`로
        통합했다(실측 근거·회귀 경위는 해당 메서드 docstring 참고 - Google Vignette 광고
        개입, 아코디언 토글의 비멱등성 등).

        Raises:
            KeyError: 지원하지 않는 카테고리명인 경우(원인을 로깅한 뒤 재전파).
        """
        try:
            heading_locator, submenu_locator = self._CATEGORY_LOCATORS[category_name]
        except KeyError:
            self.logger.error("지원하지 않는 카테고리명: %s", category_name)
            raise
        self.click_and_wait_for_class_toggle(heading_locator, submenu_locator)
        self.logger.info("CATEGORY 아코디언 '%s' 헤딩 클릭 완료", category_name)

    def is_category_submenu_expanded(self, category_name: str) -> bool:
        """지정한 카테고리(WOMEN/MEN/KIDS)의 하위 메뉴가 펼쳐진 상태인지 즉시 조회해 반환한다
        (TC-PAGE-UI-032/033, Assertion 없음, `home_page.py`와 동일한 구현/판단 근거 -
        Bootstrap collapse의 `in` 클래스로 판정, 트랜지션 도중 상태를 대기하려면
        `wait_for_category_submenu_state()`를 먼저 호출해야 함).

        Raises:
            KeyError: 지원하지 않는 카테고리명인 경우(원인을 로깅한 뒤 재전파).
        """
        try:
            _, submenu_locator = self._CATEGORY_LOCATORS[category_name]
        except KeyError:
            self.logger.error("지원하지 않는 카테고리명: %s", category_name)
            raise
        element = self.find_element(submenu_locator)
        return "in" in (element.get_attribute("class") or "").split()

    def wait_for_category_submenu_state(
        self, category_name: str, expanded: bool, timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        """지정한 카테고리(WOMEN/MEN/KIDS)의 하위 메뉴가 `expanded` 상태(펼침/닫힘)가 될
        때까지 대기한다(TC-PAGE-UI-032/033, Assertion 없음, `home_page.py`와 동일한
        구현 패턴).

        Raises:
            KeyError: 지원하지 않는 카테고리명인 경우(원인을 로깅한 뒤 재전파).
        """
        try:
            _, submenu_locator = self._CATEGORY_LOCATORS[category_name]
        except KeyError:
            self.logger.error("지원하지 않는 카테고리명: %s", category_name)
            raise
        self.wait_for_element_class_state(submenu_locator, "in", expanded, timeout)
