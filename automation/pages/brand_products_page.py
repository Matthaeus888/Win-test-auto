"""브랜드 상품 목록 페이지(/brand_products/{브랜드명})를 다루는 Page Object.

Source of Truth:
- docs/tc/page-ui.md (TC-PAGE-UI-026, 028, 030, 031)
- docs/prd/feature/page-ui.md REQ-PAGE-UI-020/022/023/024
- docs/automation/AUTOMATION_GUIDE.md 4.1절(Page Layer 책임), 6절(Locator 작성 원칙)

Locator 확정 근거(Playwright MCP 실측, 2026-09-01,
https://automationexercise.com/brand_products/Polo, 로그아웃 상태):
- 브레드크럼(`.breadcrumb`) 하위 `<li>`가 정확히 2개("Products"/href="/products", 활성
  브랜드명)임을 확인했다. **카테고리 페이지와의 차이점(중요)**: 카테고리 페이지의 활성 li는
  텍스트 자체에 ">" 구분자를 포함하지만(`category_products_page.py` 참고), 이 페이지의
  활성 li는 브랜드명만 담고 있고("Polo") ">" 구분자는 CSS `::before`로만 그려져 DOM/
  `.text`에는 나타나지 않는다(`document.querySelectorAll('.breadcrumb li').length === 2`,
  각 li 텍스트: `"Products"`, `"Polo"`).
- 상품 목록 상단 제목은 `.features_items h2.title`(페이지 전체 기준 1개)이며, 실제 DOM
  텍스트는 `"Brand -  Polo Products"` 형태임을 확인했다(단어 사이 이중 공백 포함, 카테고리
  페이지와 달리 선행 공백은 없음).
- 상품 카드 그리드는 `products_page.py`/`category_products_page.py`와 완전히 동일한 마크업
  (`.features_items .col-sm-4`)임을 재확인했다(`/brand_products/Polo`에서 카드 6개, Home
  페이지 BRANDS 섹션의 "POLO(6)" 표시와 정확히 일치 - TC-PAGE-UI-028 판정에 사용).
- 브랜드명에 `&`, 공백이 포함된 경우(예: "H&M", "Mast & Harbour") 실제 사이트 `<a>` 태그의
  `href` 속성 값 자체는 인코딩되지 않은 원문 그대로(`/brand_products/H&M`)이며, 실제로 이
  링크를 클릭해 이동한 뒤 `window.location.href`로 확인한 결과도 `%26`으로 인코딩되지 않고
  `&`이 그대로 유지된 `https://automationexercise.com/brand_products/H&M`이었다(TC 문서의
  "예: /brand_products/H%26M" 표기는 URI 인코딩 표기법으로 참고용 표현일 뿐, 실제 브라우저
  런타임 URL과는 인코딩 여부가 다름 - 문서 오류가 아니라 표기 관례 차이로 판단, Test Layer
  Assertion은 실측된 실제 URL 형식을 기준으로 한다). 이 Page Object의 `navigate()`는
  Selenium `driver.get()`으로 직접 URL을 구성해야 하므로, 공백은 `%20`으로 인코딩하되
  `&`는 인코딩하지 않는(`urllib.parse.quote(..., safe="&")`) 방식을 사용해 실제 사이트가
  기대하는 URL 형태와 일치시킨다.
"""

import re
from urllib.parse import quote

from selenium.webdriver.common.by import By

from config.settings import BASE_URL
from pages.base_page import BasePage


class BrandProductsPage(BasePage):
    """브랜드 상품 목록 페이지(/brand_products/{브랜드명})의 화면 조작/조회를 담당하는
    Page Object.

    Assertion은 수행하지 않으며(Test Layer 책임), `BasePage`가 제공하는 공통 메서드
    (get_text/find_element)만 사용해 요소를 조회한다. 화면 단위 1 Page 클래스 원칙에 따라
    `CategoryProductsPage`와 카드 마크업 패턴은 유사하지만 별도 클래스로 구현한다.
    """

    BREADCRUMB_LIS = (By.CSS_SELECTOR, ".breadcrumb li")
    TITLE = (By.CSS_SELECTOR, ".features_items h2.title")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".features_items .col-sm-4")
    PRODUCT_CARD_VIEW_PRODUCT = (By.CSS_SELECTOR, ".choose a")

    def navigate(self, brand_name: str) -> None:
        """브랜드 상품 목록 페이지(/brand_products/{brand_name})로 직접 이동한다.

        공백은 `%20`으로 인코딩하되 `&`는 인코딩하지 않는다(위 docstring 참고, 실제 사이트
        런타임 URL 형식과 일치시키기 위함).
        """
        encoded_brand_name = quote(brand_name, safe="&")
        url = f"{BASE_URL.rstrip('/')}/brand_products/{encoded_brand_name}"
        self.driver.get(url)
        self.logger.info("브랜드 상품 목록 페이지로 이동: %s", url)

    def get_breadcrumb_texts(self) -> list[str]:
        """브레드크럼 `<li>` 텍스트 목록을 순서대로 반환한다(Assertion 없음).

        예: `["Products", "Polo"]`(위 docstring 참고, 카테고리 페이지와 달리 활성 li에는
        ">" 구분자가 DOM 텍스트에 포함되지 않음).
        """
        self.find_element(self.BREADCRUMB_LIS)
        elements = self.driver.find_elements(*self.BREADCRUMB_LIS)
        texts = [element.text.strip() for element in elements]
        self.logger.debug("브랜드 페이지 브레드크럼 텍스트 조회 완료: %s", texts)
        return texts

    def get_title_text(self) -> str:
        """상품 목록 상단 제목(예: "Brand -  Polo Products")을 조회해 반환한다(Assertion
        없음)."""
        return self.get_text(self.TITLE)

    def get_product_card_count(self) -> int:
        """노출된 상품 카드 개수를 반환한다(Assertion 없음).

        `driver.find_elements()`(복수형)는 대상이 없으면 즉시 빈 리스트를 반환하고
        `WebDriverWait` 폴링을 하지 않으므로, 상품이 0개인 브랜드에서도 무한 대기 없이
        안전하게 0을 반환한다.
        """
        count = len(self.driver.find_elements(*self.PRODUCT_CARDS))
        self.logger.debug("브랜드 상품 카드 개수 조회 완료: %s", count)
        return count

    def get_product_detail_ids(self) -> list[int]:
        """노출된 상품 카드의 "View Product" 링크에서 상품 id 목록을 순서대로 추출해
        반환한다(Assertion 없음, `category_products_page.py`와 동일한 목적/구현 패턴 -
        TC-PAGE-UI-030 브랜드 필터링 정확성 확인에 사용)."""
        cards = self.driver.find_elements(*self.PRODUCT_CARDS)
        ids = []
        for card in cards:
            href = card.find_element(*self.PRODUCT_CARD_VIEW_PRODUCT).get_attribute("href")
            match = re.search(r"/product_details/(\d+)", href)
            if match:
                ids.append(int(match.group(1)))
            else:
                self.logger.warning("상품 상세 URL에서 id를 추출하지 못함: %s", href)
        self.logger.debug("브랜드 상품 id 목록 조회 완료: %s", ids)
        return ids
