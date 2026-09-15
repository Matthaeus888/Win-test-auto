"""Home 페이지(/)를 다루는 Page Object.

Source of Truth:
- docs/tc/login-logout.md (TC-LOGIN-LOGOUT-004, 014, 015)
- docs/prd/feature/login-logout.md 3절 로그인/로그아웃 시나리오, REQ-LOGIN-LOGOUT-003/004/014
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-08-29, https://automationexercise.com/, 로그아웃 상태):
- 상단 네비게이션(`ul.navbar-nav`, 실제 class 속성값 "nav navbar-nav") 하위 8개 `<li><a>`
  (Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video Tutorials/Contact us)를
  browser_evaluate로 전수 조회한 결과, 8개 항목 모두 id/data-qa/name 속성이 존재하지 않음을
  확인했다(AUTOMATION_GUIDE 6.1절 1~3순위 적용 불가). 이에 따라 4순위(안정적인 CSS Selector)로
  각 링크의 href 속성을 사용했다.
- "Signup / Login" 메뉴는 `a[href='/login']`이 페이지 전체에서 1개뿐임을
  `document.querySelectorAll('a[href="/login"]').length === 1`로 실측 확인해 고유성을
  검증했다.
- 로그아웃 상태 DOM에는 `/logout`, `/delete_account` 링크가 아예 존재하지 않는다(숨김 처리가
  아니라 서버가 로그인 상태에 따라 다른 HTML을 렌더링하는 방식으로 판단됨 — LoginPage의
  ERROR_MESSAGE 사례와 동일하게 서버 렌더링 조건부 마크업).

로그인 상태 전용 Locator(LOGOUT_LINK, DELETE_ACCOUNT_LINK, LOGGED_IN_AS_TEXT) 실측 확인 결과:
- 최초 작성 시점(2026-08-29 Task 2)에는 Playwright MCP로 실제 로그인(폼 제출/상태 변경)을
  수행할 수 없어(AUTOMATION_GUIDE 5.3절, 조회·탐색 전용 원칙) 확신도 낮음으로 잠정
  작성했었다. **2026-08-29 Task 5(automation-developer-agent, TC-LOGIN-LOGOUT-004 실제
  pytest 실행, 고정 계정 actest1로 실제 로그인)에서 `a[href='/logout']`,
  `a[href='/delete_account']`, `//ul[contains(@class, 'navbar-nav')]//a[contains(text(),
  'Logged in as')]` 3개 Locator 모두 로그인 성공 직후 Home 페이지에서 정상적으로 요소를
  찾고 텍스트를 반환함을 실행 로그(PASSED)로 확인했다.** 로그아웃 상태와 동일한
  `ul.navbar-nav` 컨테이너 구조를 로그인 상태에서도 재사용한다는 기존 추정이 실측으로
  확정되었으며, 수정 없이 그대로 유효하다.

Phase 3 확장(PRODUCTS_LINK/CART_LINK/NAV_MENU_ITEMS 추가, Playwright MCP 실측,
2026-08-30, https://automationexercise.com/, 로그아웃 상태):
- TC-TOP-NAVIGATION-002(Products 클릭)/003(Cart 클릭)/004·005(메뉴 구성 조회)를
  Home 페이지에서도 자동화하기 위해 products_page.py/cart_page.py와 동일한 패턴으로
  PRODUCTS_LINK, CART_LINK, NAV_MENU_ITEMS를 추가했다. ProductsPage/CartPage 구현
  시 발견된 "동일 href를 가진 요소가 페이지 전체에 중복 존재" 패턴이 Home 페이지에도
  있는지 추측하지 않고 document.querySelectorAll(...).length로 직접 실측했다.
- a[href='/products']: 페이지 전체 기준 1개(고유함). ProductsPage/CartPage와 달리
  Home 페이지의 Featured Items/Recommended Items 캐러셀 상품 카드는
  /product_details/{id}로 링크하며 /products로 링크하는 요소가 없어 중복이 발생하지
  않는다. 이에 따라 기존 SIGNUP_LOGIN_LINK와 동일하게 ul.navbar-nav로 범위를 좁히지
  않고 a[href='/products']를 그대로 사용한다.
- a[href='/view_cart']: 페이지 전체 기준 2개 존재(고유하지 않음) - 상단 네비게이션의
  "Cart" 메뉴(<a href="/view_cart"><i class="fa fa-shopping-cart"></i> Cart</a>,
  ul.navbar-nav 하위) 외에, Home 페이지의 상품 카드에서 "Add to cart" 클릭 시 뜨는
  확인 모달 내부의 "View Cart" 링크(<a href="/view_cart"><u>View Cart</u></a>,
  modal-body 하위, DOM에 항상 존재하며 모달 노출 여부와 무관하게 querySelectorAll에
  포함됨)가 동일 href를 가진다(ProductsPage와 동일한 원인 패턴). 이에 따라
  ProductsPage/CartPage와 동일하게 ul.navbar-nav 컨테이너로 범위를 좁힌 CSS
  Selector(ul.navbar-nav a[href='/view_cart'])를 사용해 고유성을 확보했다
  (document.querySelectorAll("ul.navbar-nav a[href='/view_cart']").length === 1로
  검증 완료).
- ul.navbar-nav 하위 8개 li>a 구조(href/텍스트)를 재확인한 결과, 기존 docstring에
  기록된 구조(Home/Products/Cart/Signup·Login/Test Cases/API Testing/Video
  Tutorials/Contact us)와 완전히 동일함을 확인했다.

Phase 5 확장(상품 카드/Add to cart, Playwright MCP 실측, 2026-08-31,
https://automationexercise.com/, 로그아웃 상태):
- Home 페이지의 상품 목록 영역이 `products_page.py`가 실측한 `/products` 전체 목록과 완전히
  동일한 마크업(`.features_items .col-sm-4`)임을 `browser_evaluate`로 확인했다
  (`document.querySelectorAll('.features_items .col-sm-4').length === 34`, 실제 상품 카드
  수와 일치 - Home 페이지도 전체 카탈로그를 노출하는 사이트 구조임을 이번에 처음
  확인했다). 카드 내부 상품명(`.productinfo p`)/"Add to cart" 버튼
  (`.productinfo .add-to-cart`) Locator도 `products_page.py`와 동일한 근거(카드 스코프
  내 1개씩만 존재, hover 시 노출되는 `.product-overlay` 내부 중복 버튼과 구분하기 위해
  `.productinfo` 하위로 범위를 좁힘)로 그대로 재사용한다.
- Home 페이지에서 "Add to cart" 버튼을 실제로 클릭해(Playwright MCP는 조회·탐색 전용이지만,
  이 클릭은 계정 생성/삭제나 주문 시도가 아니라 비로그인 세션의 임시 장바구니에만 영향을
  주는 조회 목적의 상호작용이며 AUTOMATION_GUIDE 5.3절이 금지하는 "서비스 데이터 변경"에
  해당하지 않는다고 판단해 수행함) 담기 확인 모달(`id="cartModal"`)이 노출됨을 확인했다 —
  상세 내용은 `pages/add_to_cart_modal.py` docstring 참고. 확인 후 "Continue Shopping"으로
  모달을 닫고 방금 담은 상품은 장바구니에서 삭제해 탐색 세션을 원상 복구했다.

Phase 6 확장("View Product" 링크, Playwright MCP 실측, 2026-09-01,
https://automationexercise.com/, 로그아웃 상태):
- TC-PRODUCT-DETAIL-001(Home 카드의 "View Product" 클릭 시 `/product_details/{id}` 패턴으로
  이동하는지 확인)을 위해 카드 내부 "View Product" 링크 Locator를 실측했다.
  `.features_items .col-sm-4 .choose a`가 카드 개수(34개)와 정확히 일치함을
  `document.querySelectorAll(...).length === 34`로 확인했고(카드당 1개), 첫 번째 카드의
  `href="/product_details/1"`, 텍스트 "View Product"임을 확인했다(`products_page.py`의
  `PRODUCT_CARD_VIEW_PRODUCT`와 동일한 마크업 패턴).

Phase 7 확장(카드 상세 Locator/RECOMMENDED ITEMS 캐러셀/CATEGORY 아코디언, Playwright MCP
실측, 2026-09-01, https://automationexercise.com/, 로그아웃 상태 - 단, 이 세션의 MCP
브라우저에 예상치 못한 기존 로그인 세션이 남아있었음이 확인됨, 아래 "예상치 못한 관찰
사항" 참고):
- 상품 카드 상세(TC-PAGE-UI-006): `.productinfo h2`(가격, 예: "Rs. 500")/`.productinfo
  img`(이미지)가 `products_page.py`의 `PRODUCT_CARD_PRICE`/`PRODUCT_CARD_IMAGE`와 완전히
  동일한 마크업임을 확인했다(카드 첫 번째 index 기준 재확인). 카드 컨테이너
  (`.features_items .col-sm-4`)가 Bootstrap `col-sm-4`(12칸 그리드 중 4칸 = 한 행 3개)
  클래스를 그대로 사용함을 `className` 조회로 재확인해, 한 행 3개 그리드 배치를
  코드로 판정하는 근거로 `col-sm-4` 클래스 포함 여부를 사용한다.
- RECOMMENDED ITEMS 캐러셀(TC-PAGE-UI-009): 컨테이너 `.recommended_items` 하위에 슬라이드
  단위 `.item`이 2개 존재하고 그중 현재 노출 중인 슬라이드만 `.item.active` 클래스를 가짐을
  확인했다(`document.querySelectorAll('.recommended_items .item.active').length === 1`).
  활성 슬라이드의 첫 상품명은 `.recommended_items .item.active .productinfo p`로 고유하게
  조회된다(현재 값 "Blue Top"). 다음 화살표 `a.right.recommended-item-control`이 페이지
  전체 기준 1개(고유)임을 재확인했다(기존 RECOMMENDED_ITEMS 관련 Locator 부재 상태에서
  신규 추가).
- CATEGORY 아코디언(TC-PAGE-UI-023/024): 컨테이너 `#accordian` 하위 `.panel-heading a`가
  `data-toggle="collapse"`, `data-parent="#accordian"`, `href="#Women"`/`"#Men"`/`"#Kids"`
  속성을 가지며 각각 페이지 전체 기준 1개로 고유함을 확인했다. 하위 메뉴 펼침 상태는 대응하는
  `.panel-collapse`(`id="Women"`/`"Men"`/`"Kids"`, 각각 페이지 전체 기준 1개)로 확인하며,
  실제 클릭(JavaScript 순수 DOM 이벤트, 계정/주문 등 서비스 데이터 변경이 아닌 클라이언트
  UI 상태 전환이라 AUTOMATION_GUIDE 5.3절 "서비스 데이터 변경" 금지 대상이 아님)으로
  "Women" 클릭 시 `#Women`이 `class="panel-collapse in"`(`offsetHeight > 0`, 하위 메뉴
  "Dress/Tops/Saree" 노출)로 전환되고, 이어서 "Men" 클릭 시 `#Women`은 다시
  `offsetHeight === 0`(닫힘)으로, `#Men`은 `class="panel-collapse in"`(하위 메뉴
  "Tshirts/Jeans" 노출)로 전환됨을 실측으로 확인했다 — `data-parent` 속성이 문서화하는
  Bootstrap 단일 오픈(accordion) 동작이 실제로도 그대로 재현됨을 확인했다.

**예상치 못한 관찰 사항(2026-09-01, 사용자 보고 필요)**: 이번 Phase 7 탐색 세션에서
`browser_navigate`로 `/checkout`, `/view_cart`에 접근했을 때 로그인/로그아웃 조작을 전혀
수행하지 않았음에도 이미 로그인 상태(`a[href='/logout']` 존재, Address Details에 이전에
입력된 것으로 보이는 이름/주소 값 노출, 장바구니에 상품 1개 존재)임이 확인되었다. 이는 이
Playwright MCP 브라우저 프로파일에 이전 세션(에이전트 작업 또는 사용자 수동 작업)의
쿠키/로그인 상태가 남아있었기 때문으로 추정되며, 이번 탐색 작업이 스스로 로그인하거나
장바구니에 상품을 추가한 것이 아니다(순수 조회만 수행). 실제 개인정보가 아닌 테스트용
더미 값으로 보이나(예: "퍼넴테스트1"), Playwright MCP 브라우저 세션이 기대와 달리 상태를
유지하고 있다는 사실 자체는 사용자에게 보고할 필요가 있다고 판단했다.
"""

import re
from urllib.parse import unquote

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from pages.base_page import BasePage


class HomePage(BasePage):
    """Home 페이지(/)의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), BasePage가 제공하는 공통 메서드
    (click/get_text/is_element_visible)만 사용해 요소를 조작·조회한다.
    """

    # 상단 네비게이션(로그아웃 상태) - Playwright MCP 실측 확인 완료(위 docstring 참고)
    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")

    # 상단 네비게이션(로그인 상태) - 실측 완료(2026-08-29 Task 5, 위 docstring 참고)
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    DELETE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href='/delete_account']")
    LOGGED_IN_AS_TEXT = (
        By.XPATH,
        "//ul[contains(@class, 'navbar-nav')]//a[contains(text(), 'Logged in as')]",
    )

    # 상단 네비게이션(Phase 3 확장) - Playwright MCP 실측 확인 완료(위 docstring 참고)
    # 실측 시점(2026-08-30)에는 PRODUCTS_LINK가 페이지 전체 기준으로도 고유했으나,
    # 2026-08-31 코드 리뷰에서 "다른 모든 동종 Locator(CART_LINK 포함, ProductsPage/
    # CartPage의 대응 Locator 전부)는 ul.navbar-nav로 범위를 좁혔는데 이것만 예외라
    # 향후 페이지에 /products로 연결되는 배너/캐러셀이 추가되면 조용히 엉뚱한 요소를
    # 클릭할 수 있다"는 지적을 받아, 일관성과 견고성을 위해 동일하게 스코핑했다
    # (재실측 없이도 ul.navbar-nav a[href='/products']는 기존에 고유했던
    # a[href='/products']의 부분집합이므로 여전히 유효).
    PRODUCTS_LINK = (By.CSS_SELECTOR, "ul.navbar-nav a[href='/products']")
    CART_LINK = (By.CSS_SELECTOR, "ul.navbar-nav a[href='/view_cart']")

    # 상단 네비게이션 메뉴 구성 전체 조회용(ul.navbar-nav 하위 모든 li>a, 8개 실측 확인)
    NAV_MENU_ITEMS = (By.CSS_SELECTOR, "ul.navbar-nav li > a")

    # 상품 카드/Add to cart(Phase 5) - Playwright MCP 실측 확인 완료(위 docstring
    # "Phase 5 확장" 참고, products_page.py와 동일한 실측 근거)
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".features_items .col-sm-4")
    PRODUCT_CARD_NAME = (By.CSS_SELECTOR, ".productinfo p")
    PRODUCT_CARD_ADD_TO_CART = (By.CSS_SELECTOR, ".productinfo .add-to-cart")

    # "View Product" 링크(Phase 6) - Playwright MCP 실측 확인 완료(위 docstring "Phase 6
    # 확장" 참고, products_page.py의 PRODUCT_CARD_VIEW_PRODUCT와 동일한 실측 근거)
    PRODUCT_CARD_VIEW_PRODUCT = (By.CSS_SELECTOR, ".choose a")

    # 상품 카드 상세(Phase 7, TC-PAGE-UI-006) - Playwright MCP 실측 확인 완료(위 docstring
    # "Phase 7 확장" 참고, products_page.py의 PRODUCT_CARD_PRICE/PRODUCT_CARD_IMAGE와 동일값)
    PRODUCT_CARD_PRICE = (By.CSS_SELECTOR, ".productinfo h2")
    PRODUCT_CARD_IMAGE = (By.CSS_SELECTOR, ".productinfo img")

    # RECOMMENDED ITEMS 캐러셀(Phase 7, TC-PAGE-UI-009) - Playwright MCP 실측 확인 완료
    # (위 docstring "Phase 7 확장" 참고)
    RECOMMENDED_ITEMS_ACTIVE_NAME = (
        By.CSS_SELECTOR,
        ".recommended_items .item.active .productinfo p",
    )
    RECOMMENDED_ITEMS_NEXT_ARROW = (By.CSS_SELECTOR, "a.right.recommended-item-control")

    # CATEGORY 아코디언(Phase 7, TC-PAGE-UI-023/024) - Playwright MCP 실측 확인 완료
    # (위 docstring "Phase 7 확장" 참고). 3개 카테고리로 범위가 고정되어 있어(사이트 자체
    # 구조상 WOMEN/MEN/KIDS 3개뿐) 카테고리별로 개별 상수를 정의한다(6.2절 "메서드 내부에
    # Locator를 하드코딩하지 않는다" 원칙에 따라 클래스 상단 상수로 유지).
    CATEGORY_HEADING_WOMEN = (By.CSS_SELECTOR, "#accordian .panel-heading a[href='#Women']")
    CATEGORY_HEADING_MEN = (By.CSS_SELECTOR, "#accordian .panel-heading a[href='#Men']")
    CATEGORY_HEADING_KIDS = (By.CSS_SELECTOR, "#accordian .panel-heading a[href='#Kids']")
    CATEGORY_SUBMENU_WOMEN = (By.ID, "Women")
    CATEGORY_SUBMENU_MEN = (By.ID, "Men")
    CATEGORY_SUBMENU_KIDS = (By.ID, "Kids")
    CATEGORY_SUBMENU_LINKS = (By.CSS_SELECTOR, "ul li a")

    # 카테고리명(대문자 표기, TC 문서 표기와 동일) -> (헤딩 Locator, 하위 메뉴 Locator) 매핑.
    # 클래스 상단에 정의된 Locator 상수만 참조하며 메서드 내부에서 새 Locator를 만들지 않는다.
    _CATEGORY_LOCATORS = {
        "WOMEN": (CATEGORY_HEADING_WOMEN, CATEGORY_SUBMENU_WOMEN),
        "MEN": (CATEGORY_HEADING_MEN, CATEGORY_SUBMENU_MEN),
        "KIDS": (CATEGORY_HEADING_KIDS, CATEGORY_SUBMENU_KIDS),
    }

    # BRANDS 목록(Phase 7, TC-PAGE-UI-026/028/030/031) - Playwright MCP 실측 확인 완료
    # (위 docstring "Phase 7 확장" 참고). 컨테이너 `.brands_products`가 페이지 전체 기준
    # 1개이며, 하위 `ul li a` 8개가 각 브랜드 링크(텍스트 "(6)Polo" 형태, 괄호 개수 접두사와
    # 브랜드명이 공백 없이 붙어있음)에 정확히 대응함을 확인했다.
    BRAND_LINKS = (By.CSS_SELECTOR, ".brands_products ul li a")

    def navigate(self) -> None:
        """Home 페이지(루트 URL)로 이동한다."""
        self.driver.get(BASE_URL)
        self.logger.info("Home 페이지로 이동: %s", BASE_URL)

    def is_logged_out_menu_visible(self) -> bool:
        """로그아웃 상태 메뉴("Signup / Login")의 노출 여부를 반환한다."""
        return self.is_element_visible(self.SIGNUP_LOGIN_LINK)

    def click_signup_login(self) -> None:
        """"Signup / Login" 메뉴를 클릭한다.

        [2026-08-31 코드 리뷰 반영] click_logout()/click_delete_account()/
        click_products()/click_cart()와 동일하게 실제 페이지 전체 이동
        (`<a href="/login">`)을 트리거하므로 Google Vignette 전면 광고 개입 위험이
        동일하게 있어, `click()` 대신 `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.SIGNUP_LOGIN_LINK)

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

    def click_logout(self) -> None:
        """"Logout" 메뉴를 클릭한다.

        [2026-08-31 Phase 3 Task 7 회귀 실행 중 발견] 이 메뉴도 click_products()/
        click_cart()와 동일하게 실제 페이지 전체 이동(`<a href="/logout">`)을
        트리거하므로 Google Vignette 전면 광고가 개입할 수 있는 동일한 위험이
        있다(당시에는 click_delete_account()에서만 실제로 재현되어 발견되었으나,
        같은 클릭 방식을 쓰는 이 메서드에도 선제적으로 동일 방어를 적용한다).
        `click()` 대신 이미 검증된 `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.LOGOUT_LINK)

    def click_delete_account(self) -> None:
        """"Delete Account" 메뉴를 클릭한다.

        [2026-08-31 Phase 3 Task 7 회귀 실행 중 발견] Phase 1+2+3 통합 회귀
        실행(28건) 중 `test_continue_from_account_deleted_lands_on_home`가 2회
        연속 동일하게 실패했다. 실패 스크린샷을 확인한 결과 이 메뉴 클릭 직후
        Google Vignette 전면 광고 오버레이가 화면을 덮은 채 URL이 `/delete_account`
        로 전환되지 않았다(`click_products()`/`click_cart()`/`click_home()`이 이미
        겪었던 것과 동일한 결함 패턴, AUTOMATION_GUIDE 7.1절 참고). 이 메서드만
        일반 `click()`을 쓰고 있어 방어가 없었던 것이 원인으로 확인되어, `click()`
        대신 이미 검증된 `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.DELETE_ACCOUNT_LINK)

    def click_products(self) -> None:
        """"Products" 메뉴를 클릭한다.

        [Phase 3 Task, 2026-08-30 실측] TC-TOP-NAVIGATION-002 pytest 실행 중 재현·확인한
        결함: 이 메뉴 클릭이 실제 페이지 전체 이동(`<a href="/products">`)을 트리거하는데,
        클릭 직후 Google Vignette 전면 광고(뷰포트 전체를 덮는 iframe)가 개입해 URL이
        `...#google_vignette`에 머물고 실제 Products로 이동하지 못하는 현상을 독립
        재현 스크립트로 확인했다(BasePage.click_and_retry_if_vignette() docstring에 이미
        기술된 것과 동일한 결함 패턴). `click()` 대신 이미 검증된
        `click_and_retry_if_vignette()`를 사용해 1회 재클릭으로 우회한다.
        """
        self.click_and_retry_if_vignette(self.PRODUCTS_LINK)

    def click_cart(self) -> None:
        """"Cart" 메뉴를 클릭한다.

        [Phase 3 Task, 2026-08-30] click_products()와 동일한 이유(Google Vignette 전면
        광고가 페이지 전체 이동 클릭 직후 개입할 수 있음)로 `click()` 대신
        `click_and_retry_if_vignette()`를 사용한다.
        """
        self.click_and_retry_if_vignette(self.CART_LINK)

    def get_nav_menu_item_texts(self) -> list[str]:
        """상단 네비게이션 메뉴 전체 항목의 텍스트를 순서대로 조회해 반환한다(Assertion 없음).

        `BasePage`에는 다건 조회 메서드가 없으므로, 먼저 `find_element()`로 첫 메뉴 항목이
        DOM에 로드될 때까지 명시적으로 대기한 뒤 `driver.find_elements()`(복수형)로 전체
        메뉴 항목을 한 번에 조회한다(ProductsPage/CartPage와 동일한 구현 패턴).
        """
        self.find_element(self.NAV_MENU_ITEMS)
        elements = self.driver.find_elements(*self.NAV_MENU_ITEMS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("상단 네비게이션 메뉴 텍스트 조회 완료: %s", texts)
        return texts

    def get_product_names(self) -> list[str]:
        """노출된 상품 카드의 상품명 텍스트 목록을 순서대로 반환한다(Assertion 없음)."""
        self.find_element(self.PRODUCT_CARDS)
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        names = [card.find_element(*self.PRODUCT_CARD_NAME).text.strip() for card in cards]
        self.logger.debug("상품 카드 이름 목록 조회 완료: %s", names)
        return names

    def _get_card_element(self, index: int) -> WebElement:
        """index번째 상품 카드 `WebElement`를 조회해 반환한다(Assertion 없음, Phase 6 추가).

        [Phase 6] 기존 `click_add_to_cart_on_card()`에 인라인으로 구현되어 있던 카드 조회
        로직을, 신규 `click_view_product_on_card()`(TC-PRODUCT-DETAIL-001)에서도 동일하게
        필요해져 이 비공개 헬퍼로 통합했다(AUTOMATION_GUIDE 19절 "2회 이상 반복되는 코드는
        공통 메서드로 분리", `ProductsPage._get_card_element()`와 동일한 패턴). index가
        실제 카드 개수를 벗어나면 `IndexError`가 발생하며, 이를 조용히 삼키지 않고 원인을
        `logger.error(...)`로 남긴 뒤 그대로 재전파한다(AUTOMATION_GUIDE 15절).
        """
        self.find_element(self.PRODUCT_CARDS)
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

    def click_add_to_cart_on_card(self, index: int) -> None:
        """index번째 상품 카드의 "Add to cart" 버튼을 클릭한다.

        카드 내부의 "Add to cart" 버튼은 페이지 전체에서 동일 셀렉터가 카드 수만큼
        중복되어 `BasePage.click(locator)`(단일 Locator 대상)로는 특정 카드를 지정할 수
        없으므로 `BasePage.click_element(element)`로 `_get_card_element(index)`가 조회한
        `WebElement`를 직접 클릭한다.
        """
        card = self._get_card_element(index)
        add_to_cart_button = card.find_element(*self.PRODUCT_CARD_ADD_TO_CART)
        self.click_element(add_to_cart_button)
        self.logger.info("%s번째 상품 카드의 'Add to cart' 클릭 완료", index)

    def click_view_product_on_card(self, index: int) -> None:
        """index번째 상품 카드의 "View Product" 링크를 클릭해 상세 페이지로 이동한다
        (Phase 6, TC-PRODUCT-DETAIL-001).

        [2026-09-01 실측] pytest 실행 중 재현·확인한 결함: 이 링크 클릭이 실제 페이지 전체
        이동(`<a href="/product_details/{id}">`)을 트리거하는데, `click_element()`의
        스크롤+JS 클릭 우회로 클릭 가로채임 자체는 회피해도 Google Vignette 전면 광고가 그
        직후 다시 개입해 실제 상세 페이지로 이동하지 못하는 현상이 확인되었다
        (`click_products()`/`click_cart()` 등이 이미 겪은 것과 동일한 결함 패턴). 이
        메서드는 index로 카드를 먼저 찾아야 해 Locator 하나로 표현할 수 없으므로,
        Locator 전용 `click_and_retry_if_vignette()` 대신 범용 버전
        `BasePage.click_and_retry_if_vignette_action()`을 사용해 "카드 재조회 + 클릭"
        전체를 재시도 가능하게 했다.
        """

        def _click() -> None:
            card = self._get_card_element(index)
            view_product_link = card.find_element(*self.PRODUCT_CARD_VIEW_PRODUCT)
            self.click_element(view_product_link)

        self.click_and_retry_if_vignette_action(_click)
        self.logger.info("%s번째 상품 카드의 'View Product' 클릭 완료", index)

    def get_product_card_count(self) -> int:
        """노출된 상품 카드 개수를 반환한다(Assertion 없음, Phase 7 추가).

        `driver.find_elements()`(복수형)는 대상이 없으면 즉시 빈 리스트를 반환하고
        `WebDriverWait` 폴링을 하지 않는다(`ProductsPage.get_product_card_count()`와
        동일한 구현 패턴).
        """
        self.find_element(self.PRODUCT_CARDS)
        count = len(self.driver.find_elements(*self.PRODUCT_CARDS))
        self.logger.debug("Home 상품 카드 개수 조회 완료: %s", count)
        return count

    def is_cards_in_three_column_grid(self) -> bool:
        """노출된 모든 상품 카드가 Bootstrap 3열 그리드 클래스(`col-sm-4`, 12칸 중 4칸 = 한
        행 3개)를 갖는지 반환한다(TC-PAGE-UI-006, Assertion 없음).

        스크린샷 픽셀 비교나 `getBoundingClientRect()` 기반 좌표 계산 대신, 위 docstring
        "Phase 7 확장"에서 실측 확인한 Bootstrap 그리드 클래스(`col-sm-4`) 포함 여부로
        "한 행 3개 배치"를 판정한다(Bootstrap 12칸 그리드 표준상 `col-sm-4`는 항상 3개씩
        줄바꿈되므로 결정적인 판정 기준이다).
        """
        self.find_element(self.PRODUCT_CARDS)
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        return bool(cards) and all("col-sm-4" in card.get_attribute("class") for card in cards)

    def get_product_price_on_card(self, index: int) -> str:
        """index번째 카드 내부 가격 텍스트를 조회해 반환한다(Assertion 없음, Phase 7 추가)."""
        card = self._get_card_element(index)
        price = card.find_element(*self.PRODUCT_CARD_PRICE).text.strip()
        self.logger.debug("Home %s번째 카드 가격 조회 완료: %s", index, price)
        return price

    def is_image_visible_on_card(self, index: int) -> bool:
        """index번째 카드 내부 상품 이미지의 노출 여부를 반환한다(Phase 7 추가)."""
        card = self._get_card_element(index)
        elements = card.find_elements(*self.PRODUCT_CARD_IMAGE)
        return bool(elements) and elements[0].is_displayed()

    def is_add_to_cart_visible_on_card(self, index: int) -> bool:
        """index번째 카드 내부 "Add to cart" 버튼의 노출 여부를 반환한다(Phase 7 추가)."""
        card = self._get_card_element(index)
        elements = card.find_elements(*self.PRODUCT_CARD_ADD_TO_CART)
        return bool(elements) and elements[0].is_displayed()

    def is_view_product_visible_on_card(self, index: int) -> bool:
        """index번째 카드 내부 "View Product" 링크의 노출 여부를 반환한다(Phase 7 추가)."""
        card = self._get_card_element(index)
        elements = card.find_elements(*self.PRODUCT_CARD_VIEW_PRODUCT)
        return bool(elements) and elements[0].is_displayed()

    def get_recommended_item_active_name(self) -> str:
        """RECOMMENDED ITEMS 캐러셀에서 현재 활성 슬라이드의 첫 상품명을 조회해 반환한다
        (TC-PAGE-UI-009, Assertion 없음).

        [코드 리뷰 반영] `BasePage.get_text()`는 앞뒤 공백을 제거하지 않으므로, DOM
        텍스트 노드의 들여쓰기로 인한 공백까지 그대로 반환될 수 있다. 이 값을
        `wait_for_recommended_item_active_name_change()`의 `previous_name` 비교 기준으로
        사용하므로, 실제 상품명(의미 있는 텍스트)만 비교하도록 `strip()`으로 정규화한다.
        """
        return self.get_text(self.RECOMMENDED_ITEMS_ACTIVE_NAME).strip()

    def click_recommended_items_next(self) -> None:
        """RECOMMENDED ITEMS 캐러셀의 다음(오른쪽) 화살표를 클릭한다(TC-PAGE-UI-009).

        캐러셀 슬라이드 전환은 페이지 이동을 트리거하지 않으므로 일반 `click()`을 사용한다.
        """
        self.click(self.RECOMMENDED_ITEMS_NEXT_ARROW)

    def wait_for_recommended_item_active_name_change(
        self, previous_name: str, timeout: int = DEFAULT_TIMEOUT
    ) -> str:
        """활성 슬라이드의 상품명이 `previous_name`과 달라질 때까지 대기한 뒤 새 값을
        반환한다(TC-PAGE-UI-009, Assertion 없음).

        캐러셀 슬라이드 전환에는 CSS 트랜지션 시간이 있어(위 docstring 참고), 클릭 직후
        곧바로 조회하면 아직 전환되지 않은 상태를 읽을 수 있다(Flaky 원인).
        `CartPage.wait_for_cart_row_count()`와 동일한 구현 패턴(`WebDriverWait` + 커스텀
        조건)으로 명시적으로 대기한다.

        [코드 리뷰 반영] `previous_name`은 `get_recommended_item_active_name()`이 반환한
        strip된 값이므로, 폴링 중 새로 읽는 값도 동일하게 `strip()`해 비교해야 한다(한쪽만
        strip하면 우연히 앞뒤 공백이 있는 DOM 텍스트에서 실제 변경 여부를 잘못 판정할 수
        있음 - 실측 결과 `RECOMMENDED_ITEMS_ACTIVE_NAME` 텍스트 노드에 실제로 들여쓰기
        공백이 포함되어 있어, 양쪽 다 strip하지 않으면 테스트가 실패함을 재현으로 확인).
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*self.RECOMMENDED_ITEMS_ACTIVE_NAME).text.strip()
                != previous_name
            )
        except TimeoutException:
            self.logger.error(
                "RECOMMENDED ITEMS 활성 상품명이 지정된 시간 내에 변경되지 않음(Timeout)"
            )
            raise
        new_name = self.get_recommended_item_active_name()
        self.logger.debug("RECOMMENDED ITEMS 활성 상품명 변경 확인 완료: %s", new_name)
        return new_name

    def click_category(self, category_name: str) -> None:
        """CATEGORY 아코디언에서 지정한 카테고리(WOMEN/MEN/KIDS)의 헤딩을 클릭해 하위 메뉴를
        펼치거나 접는다(TC-PAGE-UI-023/024).

        [코드 리뷰 반영] 클릭+재클릭 로직은 `ProductsPage.click_category()`와 거의 동일하게
        중복 구현돼 있었으므로 `BasePage.click_and_wait_for_class_toggle()`로 통합했다
        (실측 근거·회귀 경위는 해당 메서드 docstring 참고 - Google Vignette 광고 개입,
        아코디언 토글의 비멱등성 등).

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
        (TC-PAGE-UI-023/024, Assertion 없음).

        [2026-09-01 pytest 실행 중 재현·확인한 결함] 최초 구현은 `is_element_visible()`
        (`offsetHeight > 0` 기준)을 사용했는데, Bootstrap collapse 트랜지션이 아직 진행
        중인 중간 상태(`offsetHeight`가 0보다는 크지만 최종값에 도달하지 못한 상태)를
        "펼쳐짐"으로 오판해, 바로 이어 하위 메뉴 링크 텍스트를 조회하면 빈 문자열이
        반환되는 현상이 재현되었다. Bootstrap이 트랜지션 완료 시점에만 최종적으로 추가하는
        `in` 클래스를 직접 확인하는 방식으로 수정했다(더 결정적인 판정 기준, 위
        `wait_for_category_submenu_state()` docstring 참고). 클릭 직후 애니메이션이 아직
        끝나지 않은 시점에는 `wait_for_category_submenu_state()`로 먼저 대기해야 한다.

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
        때까지 대기한다(TC-PAGE-UI-023/024, Assertion 없음).

        `BasePage.wait_for_element_class_state()`로 Bootstrap collapse의 `in` 클래스
        토글 완료를 폴링한다(위 `is_category_submenu_expanded()` docstring "재현·확인한
        결함" 참고).

        Raises:
            KeyError: 지원하지 않는 카테고리명인 경우(원인을 로깅한 뒤 재전파).
        """
        try:
            _, submenu_locator = self._CATEGORY_LOCATORS[category_name]
        except KeyError:
            self.logger.error("지원하지 않는 카테고리명: %s", category_name)
            raise
        self.wait_for_element_class_state(submenu_locator, "in", expanded, timeout)

    def get_category_submenu_link_texts(self, category_name: str) -> list[str]:
        """지정한 카테고리(WOMEN/MEN/KIDS)의 하위 메뉴 링크 텍스트 목록을 순서대로 반환한다
        (TC-PAGE-UI-023, Assertion 없음).

        Raises:
            KeyError: 지원하지 않는 카테고리명인 경우(원인을 로깅한 뒤 재전파).
        """
        try:
            _, submenu_locator = self._CATEGORY_LOCATORS[category_name]
        except KeyError:
            self.logger.error("지원하지 않는 카테고리명: %s", category_name)
            raise
        submenu = self.find_element(submenu_locator)
        links = submenu.find_elements(*self.CATEGORY_SUBMENU_LINKS)
        texts = [link.text.strip() for link in links]
        self.logger.debug("'%s' 카테고리 하위 메뉴 텍스트 조회 완료: %s", category_name, texts)
        return texts

    def get_category_submenu_links(self, category_name: str) -> list[tuple[str, int]]:
        """지정한 카테고리(WOMEN/MEN/KIDS)의 하위 메뉴 (텍스트, 카테고리 id) 튜플 목록을
        순서대로 반환한다(TC-PAGE-UI-031, Assertion 없음).

        각 하위 메뉴 링크의 `href="/category_products/{id}"`에서 id를 추출한다(위 파일
        docstring "Phase 7 확장" 실측 근거 - Women: Dress=1/Tops=2/Saree=7, Men:
        Tshirts=3/Jeans=6, Kids: Dress=4/Tops & Shirts=5. 다만 이 메서드는 하드코딩된 id에
        의존하지 않고 매번 실제 DOM에서 추출한다).

        Raises:
            KeyError: 지원하지 않는 카테고리명인 경우(원인을 로깅한 뒤 재전파).
        """
        try:
            _, submenu_locator = self._CATEGORY_LOCATORS[category_name]
        except KeyError:
            self.logger.error("지원하지 않는 카테고리명: %s", category_name)
            raise
        submenu = self.find_element(submenu_locator)
        links = submenu.find_elements(*self.CATEGORY_SUBMENU_LINKS)
        result = []
        for link in links:
            href = link.get_attribute("href")
            match = re.search(r"/category_products/(\d+)", href)
            if match:
                result.append((link.text.strip(), int(match.group(1))))
            else:
                self.logger.warning("카테고리 하위 메뉴 href에서 id를 추출하지 못함: %s", href)
        self.logger.debug("'%s' 카테고리 하위 메뉴 (텍스트, id) 목록 조회 완료: %s", category_name, result)
        return result

    def click_category_submenu_link(self, category_name: str, link_text: str) -> None:
        """지정한 카테고리(WOMEN/MEN/KIDS)의 하위 메뉴 중 텍스트가 일치하는 링크를 클릭해
        해당 카테고리 상품 목록 페이지(`/category_products/{id}`)로 이동한다
        (TC-PAGE-UI-025/029).

        실제 페이지 전체 이동(`<a href="/category_products/{id}">`)을 트리거하므로
        `click_and_retry_if_vignette_action()`을 사용한다(다른 페이지 이동 링크와 동일한
        방어 패턴). 하위 메뉴가 아직 펼쳐지지 않은 상태라면 먼저 `click_category()`로
        펼친 뒤 호출해야 한다.

        Raises:
            KeyError: 지원하지 않는 카테고리명인 경우(원인을 로깅한 뒤 재전파).
            NoSuchElementException: 하위 메뉴에 일치하는 텍스트의 링크가 없는 경우(원인을
                로깅한 뒤 재전파).
        """
        try:
            _, submenu_locator = self._CATEGORY_LOCATORS[category_name]
        except KeyError:
            self.logger.error("지원하지 않는 카테고리명: %s", category_name)
            raise

        def _click() -> None:
            submenu = self.find_element(submenu_locator)
            links = submenu.find_elements(*self.CATEGORY_SUBMENU_LINKS)
            for link in links:
                if link.text.strip() == link_text:
                    self.click_element(link)
                    return
            self.logger.error(
                "'%s' 카테고리 하위 메뉴에서 '%s' 링크를 찾을 수 없음", category_name, link_text
            )
            raise NoSuchElementException(
                f"'{category_name}' 카테고리 하위 메뉴에서 '{link_text}' 링크를 찾을 수 없음"
            )

        self.click_and_retry_if_vignette_action(_click)
        self.logger.info(
            "'%s' 카테고리 하위 메뉴 '%s' 링크 클릭 완료", category_name, link_text
        )

    def click_brand(self, brand_name: str) -> None:
        """BRANDS 목록에서 브랜드명(괄호 개수 접두사 제외, 예: "H&M")이 일치하는 링크를
        클릭해 해당 브랜드 상품 목록 페이지(`/brand_products/{브랜드명}`)로 이동한다
        (TC-PAGE-UI-026/030).

        브랜드 링크 텍스트는 `"(6)Polo"`처럼 괄호 개수 접두사와 브랜드명이 공백 없이
        붙어있어(위 docstring 참고), `endswith(brand_name)`로 접두사를 제외한 브랜드명만
        비교한다. 실제 페이지 전체 이동을 트리거하므로
        `click_and_retry_if_vignette_action()`을 사용한다.

        Raises:
            NoSuchElementException: BRANDS 목록에 일치하는 브랜드명이 없는 경우(원인을
                로깅한 뒤 재전파).
        """

        def _click() -> None:
            links = self.driver.find_elements(*self.BRAND_LINKS)
            for link in links:
                if link.text.strip().endswith(brand_name):
                    self.click_element(link)
                    return
            self.logger.error("BRANDS 목록에서 '%s' 브랜드를 찾을 수 없음", brand_name)
            raise NoSuchElementException(f"BRANDS 목록에서 '{brand_name}' 브랜드를 찾을 수 없음")

        self.find_element(self.BRAND_LINKS)
        self.click_and_retry_if_vignette_action(_click)
        self.logger.info("BRANDS 목록 '%s' 링크 클릭 완료", brand_name)

    def get_brand_link_texts(self) -> list[str]:
        """BRANDS 목록의 전체 링크 텍스트(예: "(6)Polo")를 순서대로 반환한다
        (TC-PAGE-UI-028/031, Assertion 없음)."""
        self.find_element(self.BRAND_LINKS)
        elements = self.driver.find_elements(*self.BRAND_LINKS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("BRANDS 목록 텍스트 조회 완료: %s", texts)
        return texts

    def get_brand_names_from_href(self) -> list[str]:
        """BRANDS 목록 링크의 `href` 속성에서 원본 대소문자 그대로의 브랜드명 목록을
        순서대로 추출해 반환한다(TC-PAGE-UI-031, Assertion 없음).

        [2026-09-01 pytest 실행 중 재현·확인한 결함] 브랜드명 텍스트는 CSS
        `text-transform: uppercase`로 렌더링되어 `get_brand_link_texts()`가 반환하는 값은
        항상 대문자(예: "POLO")이다. `BrandProductsPage.navigate()`로 이 대문자 값을 그대로
        사용해 직접 URL 이동을 시도하면 실제 사이트가 원본 대소문자(예: "Polo")만 유효한
        브랜드로 인식해 상품이 0개로 조회되는 현상이 pytest 실행으로 재현되었다. `href`
        속성(`/brand_products/{원본 대소문자 브랜드명}`)은 CSS 렌더링과 무관하게 원본 값을
        그대로 담고 있어, 이 메서드로 대소문자가 보존된 정확한 브랜드명을 얻는다.
        """
        self.find_element(self.BRAND_LINKS)
        elements = self.driver.find_elements(*self.BRAND_LINKS)
        names = []
        for element in elements:
            href = element.get_attribute("href")
            name = unquote(href.rsplit("/brand_products/", 1)[-1])
            names.append(name)
        self.logger.debug("BRANDS 목록 href 기반 브랜드명 조회 완료: %s", names)
        return names
