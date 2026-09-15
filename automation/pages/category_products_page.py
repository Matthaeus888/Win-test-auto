"""카테고리 상품 목록 페이지(/category_products/{id})를 다루는 Page Object.

Source of Truth:
- docs/tc/page-ui.md (TC-PAGE-UI-025, 029, 031)
- docs/prd/feature/page-ui.md REQ-PAGE-UI-019/023/024
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-09-01,
https://automationexercise.com/category_products/6, 로그아웃 상태):
- 브레드크럼(`.breadcrumb`) 하위 `<li>`가 정확히 2개("Products"/href="/products", 활성
  카테고리 경로)임을 확인했다. 활성 `<li class="active">`의 텍스트 자체가 이미
  "Men > Jeans"처럼 ">" 구분자를 포함하고 있음을 확인했다(브라우저 화면에서 보이는
  "Products > Men > Jeans"는 "Products"와 활성 li 사이의 ">" 구분자가 CSS `::before`로
  그려지고, 활성 li 텍스트 자체의 ">"는 DOM 텍스트임 - 두 가지가 합쳐져 보임).
  `document.querySelectorAll('.breadcrumb li').length === 2`로 고유 구조를 확인했다.
- 상품 목록 상단 제목은 `.features_items h2.title`(페이지 전체 기준 1개)이며, 실제 DOM
  텍스트는 앞뒤 공백과 단어 사이 이중 공백을 포함한 `" Men -  Jeans Products"`
  형태임을 확인했다(화면에는 CSS `text-transform: uppercase`로 대문자화되어 보이지만
  DOM 텍스트 자체는 대소문자 혼용). Assertion 시 공백 정규화 후 부분 문자열 비교를
  권장한다(Test Layer 책임).
- 상품 카드 그리드는 `products_page.py`가 실측한 `/products` 전체 목록과 완전히 동일한
  마크업(`.features_items .col-sm-4`)임을 재확인했다(`/category_products/6`에서 카드 3개,
  실제 Jeans 카테고리 상품 수와 일치).
"""

import re

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class CategoryProductsPage(BasePage):
    """카테고리 상품 목록 페이지(/category_products/{id})의 화면 조작/조회를 담당하는
    Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), `BasePage`가 제공하는 공통 메서드
    (get_text/find_element)만 사용해 요소를 조회한다. 화면 단위 1 Page 클래스 원칙에 따라
    `ProductsPage`와 카드 마크업 패턴은 유사하지만 별도 클래스로 구현한다.
    """

    BREADCRUMB_LIS = (By.CSS_SELECTOR, ".breadcrumb li")
    TITLE = (By.CSS_SELECTOR, ".features_items h2.title")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".features_items .col-sm-4")
    PRODUCT_CARD_VIEW_PRODUCT = (By.CSS_SELECTOR, ".choose a")

    def navigate(self, category_id: int) -> None:
        """카테고리 상품 목록 페이지(/category_products/{category_id})로 직접 이동한다."""
        url = f"{BASE_URL.rstrip('/')}/category_products/{category_id}"
        self.driver.get(url)
        self.logger.info("카테고리 상품 목록 페이지로 이동: %s", url)

    def get_breadcrumb_texts(self) -> list[str]:
        """브레드크럼 `<li>` 텍스트 목록을 순서대로 반환한다(Assertion 없음).

        예: `["Products", "Men > Jeans"]`(위 docstring 참고, 마지막 항목 자체에 ">" 포함).
        """
        self.find_element(self.BREADCRUMB_LIS)
        elements = self.driver.find_elements(*self.BREADCRUMB_LIS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("카테고리 페이지 브레드크럼 텍스트 조회 완료: %s", texts)
        return texts

    def get_title_text(self) -> str:
        """상품 목록 상단 제목(예: "Men -  Jeans Products")을 조회해 반환한다(Assertion
        없음)."""
        return self.get_text(self.TITLE)

    def get_product_card_count(self) -> int:
        """노출된 상품 카드 개수를 반환한다(Assertion 없음).

        `driver.find_elements()`(복수형)는 대상이 없으면 즉시 빈 리스트를 반환하고
        `WebDriverWait` 폴링을 하지 않으므로, 상품이 0개인 카테고리에서도 무한 대기 없이
        안전하게 0을 반환한다.
        """
        count = len(self.driver.find_elements(*self.PRODUCT_CARDS))
        self.logger.debug("카테고리 상품 카드 개수 조회 완료: %s", count)
        return count

    def get_product_detail_ids(self) -> list[int]:
        """노출된 상품 카드의 "View Product" 링크에서 상품 id 목록을 순서대로 추출해
        반환한다(Assertion 없음).

        TC-PAGE-UI-029(카테고리 필터링 정확성)처럼 각 상품의 실제 카테고리 정보를
        `ProductDetailPage`에서 확인해야 하는 시나리오에서, 카드 목록만으로는 카테고리 정보를
        알 수 없어(카드에는 이미지/가격/상품명만 노출) 상품 상세 페이지로 이동하기 위한 id를
        먼저 수집한다.
        """
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        ids = []
        for card in cards:
            href = card.find_element(*self.PRODUCT_CARD_VIEW_PRODUCT).get_attribute("href")
            match = re.search(r"/product_details/(\d+)", href)
            if match:
                ids.append(int(match.group(1)))
            else:
                self.logger.warning("상품 상세 URL에서 id를 추출하지 못함: %s", href)
        self.logger.debug("카테고리 상품 id 목록 조회 완료: %s", ids)
        return ids
