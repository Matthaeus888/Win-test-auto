"""상품 상세 페이지(/product_details/{id})를 다루는 Page Object.

Source of Truth:
- docs/tc/product-detail.md (TC-PRODUCT-DETAIL-001, 002, 008, 015, 016, 021)
- docs/prd/feature/product-detail.md 3절 사용자 조작 시나리오, REQ-PRODUCT-DETAIL-001/002/
  009/010/016/017/023/025
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

"Add to cart" 클릭 시 노출되는 담기 확인 모달은 `pages/add_to_cart_modal.py`
(`AddToCartModal`)가 Home/Products 리스트 페이지와 공유하는 컴포넌트로 이미 정의되어
있으므로(REQ-CART-001 원 정의, `cart.md` Phase 5), 이 파일에서는 신규로 정의하지 않고
그대로 재사용한다(ROADMAP.md Phase 6 항목).

Locator 확정 근거(Playwright MCP 실측, 2026-09-01, https://automationexercise.com/product_details/1,
로그아웃 상태):
- 상품 이미지: `.view-product img`가 페이지 전체 기준 1개임을
  `document.querySelectorAll('.view-product img').length === 1`로 확인했다(6.1절 4순위).
- 상품명: `.product-information h2`가 페이지 전체 기준 1개(텍스트 "Blue Top")임을 확인했다.
- 가격: `.product-information` 내부에 `<span><span>Rs. 500</span>...</span>` 구조로
  중첩되어 있어, `.product-information span span`(페이지 전체 기준 1개, 텍스트 "Rs. 500")로
  가격 전용 span만 고유하게 지정했다(바깥쪽 `<span>`은 Quantity/Add to cart 버튼까지 포함하는
  컨테이너라 가격 텍스트만 별도로 조회하려면 안쪽 span이 필요함).
- Quantity 입력란: `<input type="number" name="quantity" id="quantity" value="1" min="1">`
  로 `id` 속성이 존재해(6.1절 1순위) `By.ID, "quantity"`를 사용한다(페이지 전체 기준 1개,
  `tests/test_cart.py`의 `_DETAIL_QUANTITY_INPUT`과 동일값으로 이미 2026-08-31에 실측
  검증된 값을 재사용). `min="1"` 속성이 네이티브 스피너 자체에도 이미 최솟값 제약을 걸고
  있음을 확인했다(TC-PRODUCT-DETAIL-016 기대 결과와 일치하는 근거).
- "Add to cart" 버튼: `<button type="button" class="btn btn-default cart">`로 id/data-qa가
  없어 `.btn.btn-default.cart`(페이지 전체 기준 1개, 4순위 CSS Selector)를 사용한다
  (`tests/test_cart.py`의 `_DETAIL_ADD_TO_CART_BUTTON`과 동일값 재사용).
- WRITE YOUR REVIEW 폼(`#review-form`) 하위 요소: `#name`(Your Name), `#email`(Email
  Address), `#review`(리뷰 내용 textarea), `#button-review`(Submit 버튼) 모두 `id` 속성이
  존재해(6.1절 1순위) 각각 페이지 전체 기준 1개임을 확인했다.
- 리뷰 제출 성공 메시지: `#review-section`(`class="form-row hide"`, 기본 숨김)의 하위
  `.alert-success span`(텍스트 "Thank you for your review.")이 페이지 전체 기준 1개임을
  확인했다. 승인된 TC-PRODUCT-DETAIL-021/REQ-PRODUCT-DETAIL-025의 Expected Result 문구
  "Thank you for your review."와 실제 DOM 텍스트가 정확히 일치함을 확인했다(불일치 없음).
- Quantity 스피너 아래(▼) 버튼(TC-PRODUCT-DETAIL-016) 관련: 네이티브
  `<input type="number">`의 스피너 버튼은 브라우저가 렌더링하는 UI Shadow 영역으로 별도의
  DOM 요소/Locator가 존재하지 않아 Selenium `click()`으로 좌표 없이 직접 지정할 수 없다.
  HTML 표준상 포커스된 number input에서 `ArrowDown`/`ArrowUp` 키 입력은 스피너 아래/위
  버튼 클릭과 동일하게 `stepDown()`/`stepUp()`을 트리거하는 네이티브 동작이며, Selenium의
  `send_keys()`는 브라우저에 신뢰된(trusted) 키 이벤트를 전달하므로(Playwright MCP
  `browser_evaluate`의 JavaScript `dispatchEvent`와 달리 이 사이트의 실제 브라우저 자동화
  실행 환경에서 그대로 재현된다) 스피너 버튼 클릭의 결정적이고 이식성 있는 대체 수단으로
  `ArrowDown` 키 입력을 사용한다(`click_quantity_spin_down()`). 이 대체 수단은 좌표 기반
  클릭(브라우저/DPI에 따라 스피너 버튼 위치가 달라질 수 있어 불안정)보다 안정적이다.

Phase 7 확장(Category/Brand 텍스트, Playwright MCP 실측, 2026-09-01,
https://automationexercise.com/product_details/1, 로그아웃 상태):
- TC-PAGE-UI-029/030(카테고리/브랜드 필터링 정확성 - 목록 페이지의 각 상품이 실제로 해당
  카테고리/브랜드에 속하는지 확인)을 위해 `.product-information` 내부의 안내 문단을
  실측했다. `Array.from(document.querySelector('.product-information')
  .querySelectorAll('p')).map(p => p.textContent)` 결과 `["Category: Women > Tops",
  "Availability: In Stock", "Condition: New", "Brand:  Polo"]` 4개 문단이 순서대로
  존재함을 확인했다. `id`/`data-qa`가 없고 클래스만으로는 4개 문단을 구분할 수 없어(모두
  형제 `<p>`), 텍스트 접두사(`"Category:"`, `"Brand:"`)를 조건으로 하는 상대 XPath(6.1절
  5순위)로 각각 고유하게 지정했다 - 다른 카테고리(예: Kids)에서 문단 순서가 달라지거나
  일부 상품에 "Brand" 문단이 없을 가능성(실측하지 않은 카테고리)에도 순서에 의존하지 않는
  안정적인 방식이다.
"""

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, DEFAULT_TIMEOUT
from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    """상품 상세 페이지(/product_details/{id})의 화면 조작/조회를 담당하는 Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), `BasePage`가 제공하는 공통 메서드
    (click/type_text/get_text/is_element_visible/find_element)만 사용해 요소를
    조작·조회한다. "Add to cart" 확인 모달은 `pages/add_to_cart_modal.py`의
    `AddToCartModal`을 재사용하며 이 클래스에서 다루지 않는다(위 파일 docstring 참고).
    """

    # 화면 구성요소 - Playwright MCP 실측 확인 완료(위 docstring 참고)
    IMAGE = (By.CSS_SELECTOR, ".view-product img")
    NAME = (By.CSS_SELECTOR, ".product-information h2")
    PRICE = (By.CSS_SELECTOR, ".product-information span span")

    # Quantity 입력란/Add to cart 버튼 - tests/test_cart.py에서 이미 실측 검증된 값과
    # 동일(위 docstring 참고, 중복 실측 대신 기존 근거 재사용)
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btn.btn-default.cart")

    # WRITE YOUR REVIEW 섹션 - Playwright MCP 실측 확인 완료(위 docstring 참고)
    REVIEW_NAME_INPUT = (By.ID, "name")
    REVIEW_EMAIL_INPUT = (By.ID, "email")
    REVIEW_TEXT_INPUT = (By.ID, "review")
    REVIEW_SUBMIT_BUTTON = (By.ID, "button-review")
    REVIEW_SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#review-section .alert-success span")

    # Category/Brand 안내 문단(Phase 7) - Playwright MCP 실측 확인 완료(위 docstring
    # "Phase 7 확장" 참고, 6.1절 5순위 텍스트 조건 기반 상대 XPath).
    # [2026-09-01 pytest 실행 중 재현·확인한 결함] 최초 구현은 `contains(text(), ...)`
    # (해당 요소의 "직계" 텍스트 노드만 검사)를 사용했는데, 실제 pytest(Selenium ChromeDriver)
    # 실행 중 이 사이트에 제3자 확장 프로그램/광고 네트워크로 추정되는 `class="google-anno"`
    # 주석(annotation) `<a>` 요소가 `<p>` 문단 내부에 실제로 주입되어 텍스트가 여러 노드로
    # 쪼개지는 현상이 재현되었다(`BRAND_TEXT`가 매번 Timeout으로 실패, 특히 "Brand:" 문단
    # 전체가 이 주석 요소로 감싸지는 경우가 있어 직계 텍스트 노드 매칭이 완전히 실패함).
    # 기존에 `pages/account_created_page.py`/`account_deleted_page.py` docstring은 이
    # "google-anno" 아티팩트를 Playwright MCP 브라우저 세션 전용 현상으로 추정했으나, 이번
    # 실측으로 실제 Selenium(ChromeDriver, 확장 프로그램 미설치 상태로 실행) 세션에서도
    # 동일하게 재현됨을 확인했다 - 사용자에게 보고가 필요한 사실로 판단한다(자세한 내용은
    # 자동화 구현 결과 보고 참고). `contains(text(), ...)`를 `contains(., ...)`(해당 요소의
    # 문자열 값 전체 - 자손 텍스트까지 포함)로 교체해 중첩 삽입 요소와 무관하게 안정적으로
    # 매칭되도록 수정했다(Full XPath가 아닌 상대 XPath 그대로 유지).
    CATEGORY_TEXT = (
        By.XPATH,
        "//div[@class='product-information']//p[contains(., 'Category:')]",
    )
    BRAND_TEXT = (
        By.XPATH,
        "//div[@class='product-information']//p[contains(., 'Brand:')]",
    )

    def navigate(self, product_id: int) -> None:
        """상품 상세 페이지(/product_details/{product_id})로 이동한다."""
        url = f"{BASE_URL.rstrip('/')}/product_details/{product_id}"
        self.driver.get(url)
        self.logger.info("상품 상세 페이지로 이동: %s", url)

    def is_image_visible(self) -> bool:
        """상품 이미지의 노출 여부를 반환한다."""
        return self.is_element_visible(self.IMAGE)

    def get_product_name(self) -> str:
        """상품명 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.NAME)

    def get_price_text(self) -> str:
        """가격 텍스트("Rs. {숫자}" 형식)를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.PRICE)

    def get_category_text(self) -> str:
        """카테고리 안내 문단(예: "Category: Women > Tops")을 조회해 반환한다(Phase 7,
        TC-PAGE-UI-029, Assertion 없음)."""
        return self.get_text(self.CATEGORY_TEXT)

    def get_brand_text(self) -> str:
        """브랜드 안내 문단(예: "Brand:  Polo")을 조회해 반환한다(Phase 7, TC-PAGE-UI-030,
        Assertion 없음)."""
        return self.get_text(self.BRAND_TEXT)

    def set_quantity(self, value: str) -> None:
        """Quantity 입력란의 기존 값을 지우고 지정한 값을 입력한다."""
        self.type_text(self.QUANTITY_INPUT, value)

    def get_quantity_value(self) -> str:
        """Quantity 입력란의 현재 값을 조회해 반환한다(Assertion 없음).

        `<input>` 요소는 `WebElement.text`가 항상 빈 문자열이므로 `BasePage.get_text()`
        (텍스트 노드 조회) 대신 `value` 속성을 직접 조회한다.
        """
        value = self.find_element(self.QUANTITY_INPUT).get_attribute("value")
        self.logger.debug("Quantity 입력란 값 조회 완료: %s", value)
        return value

    def click_quantity_spin_down(self, times: int = 1) -> None:
        """Quantity 입력란에 포커스한 뒤 `ArrowDown` 키를 지정한 횟수만큼 입력해 스피너
        아래(▼) 버튼 클릭과 동일하게 동작시킨다(TC-PRODUCT-DETAIL-016, 위 파일 docstring
        "Quantity 스피너 아래(▼) 버튼" 근거 참고).
        """
        self.click(self.QUANTITY_INPUT)
        quantity_input = self.find_element(self.QUANTITY_INPUT)
        for _ in range(times):
            quantity_input.send_keys(Keys.ARROW_DOWN)
        self.logger.info("Quantity 스피너 아래 버튼 대체 조작(ArrowDown) %s회 수행", times)

    def click_add_to_cart(self) -> None:
        """"Add to cart" 버튼을 클릭한다.

        클릭 성공 시 담기 확인 모달(`#cartModal`)이 노출되며, 모달 자체의 조작/조회는
        `pages/add_to_cart_modal.py`의 `AddToCartModal`을 사용한다(위 파일 docstring
        참고). 모달을 여는 버튼 클릭 자체는 페이지 전체 이동을 트리거하지 않으므로 일반
        `click()`을 사용한다(`AddToCartModal.CONTINUE_SHOPPING_BUTTON`과 동일한 판단
        근거).
        """
        self.click(self.ADD_TO_CART_BUTTON)

    def submit_review(self, name: str, email: str, review_text: str) -> None:
        """"WRITE YOUR REVIEW" 섹션에 값을 입력하고 Submit 버튼을 클릭한다."""
        self.type_text(self.REVIEW_NAME_INPUT, name)
        self.type_text(self.REVIEW_EMAIL_INPUT, email)
        self.type_text(self.REVIEW_TEXT_INPUT, review_text)
        self.click(self.REVIEW_SUBMIT_BUTTON)

    def get_review_success_message(self) -> str:
        """리뷰 제출 성공 메시지 텍스트를 조회해 반환한다(Assertion 없음)."""
        return self.get_text(self.REVIEW_SUCCESS_MESSAGE)

    def get_review_field_values(self) -> tuple[str, str, str]:
        """리뷰 입력 필드(Your Name, Email Address, 리뷰 내용)의 현재 값을 순서대로 조회해
        반환한다(Assertion 없음)."""
        name_value = self.find_element(self.REVIEW_NAME_INPUT).get_attribute("value")
        email_value = self.find_element(self.REVIEW_EMAIL_INPUT).get_attribute("value")
        review_value = self.find_element(self.REVIEW_TEXT_INPUT).get_attribute("value")
        return name_value, email_value, review_value

    def wait_for_review_fields_cleared(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        """리뷰 입력 필드 3개가 모두 빈 값으로 자동 초기화될 때까지 대기한다(Assertion 없음).

        REQ-PRODUCT-DETAIL-025("성공 메시지 노출 후 1~2초 경과 시 필드 자동 초기화")를
        고정 시간 대기(`time.sleep()`, 금지) 없이 확인하기 위해, `WebDriverWait` +
        커스텀 조건(3개 필드 `value` 속성이 모두 빈 문자열이 될 때까지 폴링)을 사용한다
        (`CartPage.wait_for_cart_row_count()`와 동일한 구현 패턴).
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(*self.REVIEW_NAME_INPUT).get_attribute("value") == ""
                and d.find_element(*self.REVIEW_EMAIL_INPUT).get_attribute("value") == ""
                and d.find_element(*self.REVIEW_TEXT_INPUT).get_attribute("value") == ""
            )
            self.logger.debug("리뷰 입력 필드가 지정된 시간 내에 자동 초기화됨")
        except TimeoutException:
            self.logger.error("리뷰 입력 필드가 지정된 시간 내에 자동 초기화되지 않음(Timeout)")
            raise
