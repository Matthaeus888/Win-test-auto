"""Products 페이지(/products) 검색 기능의 기본 동작을 검증하는 테스트.

Source of Truth:
- docs/tc/product-search.md (TC-PRODUCT-SEARCH-001, 002, 003, 004, 005, 006, 008, 010)
- docs/automation/AUTOMATION_GUIDE.md 4.2절(Test Layer 책임), 8절(Assertion 원칙),
  10절(테스트 독립성)

이 파일은 TC-001(실제 상품명과 매칭되는 검색어 입력 후 검색 실행 시 URL 변경/섹션 제목
변경/매칭 상품만 노출), TC-002(검색 결과 상품 카드 하나에 이미지/가격/상품명/Add to
cart/View Product가 모두 노출), TC-003(매칭되는 상품이 없는 검색어로 검색 실행 시 섹션
제목은 유지되지만 상품 카드는 노출되지 않음), TC-004(검색어를 입력하지 않은 채 검색
실행 시 전체 상품이 노출되고 URL에는 `?search=` 형태가 남음), TC-005(상품명의 일부
문자열만 검색해도 부분 일치로 매칭됨), TC-006(브랜드명·상위 카테고리명 keyword로는
검색 결과가 노출되지 않음), TC-008(검색창에 검색어를 입력한 상태에서 Enter 키만
입력하고 돋보기 버튼을 클릭하지 않으면 검색이 실행되지 않아 URL/섹션 제목/상품 목록이
그대로 유지됨), TC-010(상품명에는 검색어가 없지만 하위 카테고리명 부분 일치로 매칭되는
상품이 노출됨)를 다룬다.

[TC-010 관련] TC-010은 REQ-PRODUCT-SEARCH-005 정정을 촉발한 실제 관찰 사례("shirt"로
검색 시 상품명에 "shirt"가 없는 "Frozen Tops For Kids"가 하위 카테고리명 "Tops" 부분
일치로 노출됨)를 그대로 회귀 테스트화한 것이다. 이 검증은 특정 상품명 하나가 결과 목록에
포함되는지만 확인하면 되므로, 카드별 하위 카테고리명을 별도로 조회하는 신규 Page Object
메서드 없이 기존 `search_product()`/`get_product_names()`만으로 충분하다고 판단했다
(Roadmap Phase 4 항목 "추가 조회 메서드가 필요한지는 구현 단계에서 판단"에 대한 결론).

모든 TC는 원본 TC 문서의 공통 Preconditions("별도 언급이 없는 한 로그인/로그아웃 상태는
무관함")에 따라 로그인 여부와 무관한 독립 Feature이므로, 로그인 절차 없이 로그아웃 상태
그대로 각 테스트가 스스로 Products 페이지 진입부터 셋업한다(AUTOMATION_GUIDE 10절 테스트
독립성).

Assertion은 Test Layer(이 파일)에서만 수행하며, Page 객체(ProductsPage)는 화면 조작/조회만
담당한다(Assertion 없음). 이 파일은 신규 Locator/메서드를 추가하지 않고
`automation/pages/products_page.py`(Phase 4 Task 1에서 이미 확장 완료)의 기존 메서드만
그대로 사용한다.

[2026-08-31 재작업 사유] REQ-PRODUCT-SEARCH-001/005/008 정정 재승인에 따라
TC-PRODUCT-SEARCH-001의 Expected Result가 "노출된 모든 상품명이 검색어를 포함해야 한다"에서
"상품명 또는 하위 카테고리명 중 하나 이상에 검색어가 부분 일치하는 상품만 노출된다"로
변경되었다(`docs/tc/product-search.md` TC-PRODUCT-SEARCH-001 참고). 실제 pytest 실행 결과
기존 assertion(모든 상품명이 "shirt"를 포함해야 함)은 "Tops" 하위 카테고리로 매칭된 4개
상품("Sleeves Printed Top - White" 등) 때문에 FAILED였다. 그런데 현재
`automation/pages/products_page.py`에는 카드별 하위 카테고리명을 조회하는 메서드가 없어
"상품명 또는 하위 카테고리명 어디에도 검색어가 없는 상품은 노출되면 안 된다"는 조건을 이
테스트에서 정확히 판정할 방법이 없다. 이에 따라 상품명 단독 포함 여부를 강제하던 assertion을
제거하고, URL 변경/섹션 제목 변경/검색 결과 1건 이상 노출이라는 결정적으로 판정 가능한
부분만 이 테스트가 검증하도록 범위를 조정했다. 하위 카테고리명 매칭 판정은 이를 전담하는
별도 TC-PRODUCT-SEARCH-010(자동화 구현은 별도 Task 범위)이 담당한다.
"""

import pytest

from config.settings import BASE_URL
from pages.products_page import ProductsPage


def test_search_with_matching_keyword_filters_products(driver):
    """TC-PRODUCT-SEARCH-001: 실제 상품명과 매칭되는 검색어("shirt")로 검색 실행 시 URL이
    `?search=shirt` 형태로 변경되고, 섹션 제목이 "SEARCHED PRODUCTS"로 바뀌며, 검색 결과
    카드가 1건 이상 노출된다.

    [2026-08-31 assertion 범위 조정] 원본 TC의 최신 Expected Result는 "상품명 또는 하위
    카테고리명 중 하나 이상에 검색어가 부분 일치하는 상품만 노출된다"이다. 그러나 현재
    `ProductsPage`에는 카드별 하위 카테고리명을 조회하는 메서드가 없어, "상품명에도
    하위 카테고리명에도 검색어가 없는 상품이 노출되면 안 된다"는 조건을 이 테스트에서 정확히
    판정할 수 없다. 이에 따라 상품명 단독 포함 여부를 강제하던 기존 assertion은 제거했다
    (실제 사이트는 하위 카테고리명으로도 매칭하므로 그 assertion은 결함이 아닌 정상 동작을
    실패로 오판정했다). 하위 카테고리명 매칭 검증은 TC-PRODUCT-SEARCH-010이 전담한다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.search_product("shirt")
    products_page.wait_for_url_contains("search=shirt")

    expected_url = f"{BASE_URL.rstrip('/')}/products?search=shirt"
    actual_url = driver.current_url
    assert actual_url == expected_url, (
        f"검색 실행 후 URL이 {expected_url!r}이어야 하지만 그렇지 않음 "
        f"(기대: {expected_url!r}, 실제: {actual_url!r})"
    )

    # [실측 확정] products_page.py 문서는 DOM raw 텍스트가 "Searched Products"(대소문자
    # 혼용)이고 화면 표시만 CSS text-transform으로 대문자화된다고 기록했으나, 실제 pytest
    # 실행 결과 Selenium의 element.text(BasePage.get_text() 내부 사용)는 브라우저 렌더링
    # 시점의 CSS text-transform이 적용된 값을 그대로 반환해 "SEARCHED PRODUCTS"로 조회됨을
    # 확인했다. TC-PRODUCT-SEARCH-001 원본 기대값과도 정확히 일치하는 값이라 이 값을
    # 채택한다.
    expected_title = "SEARCHED PRODUCTS"
    actual_title = products_page.get_section_title()
    assert actual_title == expected_title, (
        f"검색 실행 후 섹션 제목이 {expected_title!r}이어야 하지만 그렇지 않음 "
        f"(기대: {expected_title!r}, 실제: {actual_title!r})"
    )

    card_count = products_page.get_product_card_count()
    assert card_count > 0, (
        f"검색어 'shirt'에 매칭되는 상품 카드가 1개 이상 노출되어야 하지만 그렇지 않음 "
        f"(기대: 1개 이상, 실제: {card_count}개)"
    )


def test_search_result_card_shows_image_price_name_and_actions(driver):
    """TC-PRODUCT-SEARCH-002: 검색 결과에 노출된 임의의 상품 카드 하나(index 0)에 이미지,
    가격, 상품명, "Add to cart" 버튼, "View Product" 링크가 모두 노출된다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.search_product("shirt")
    products_page.wait_for_url_contains("search=shirt")

    card_count = products_page.get_product_card_count()
    assert card_count > 0, (
        f"카드 구성을 검증하려면 검색어 'shirt'에 매칭되는 상품 카드가 1개 이상 노출되어야 "
        f"하지만 그렇지 않음 (기대: 1개 이상, 실제: {card_count}개)"
    )

    target_index = 0

    actual_price = products_page.get_product_price_on_card(target_index)
    assert actual_price != "", (
        f"{target_index}번째 카드에 가격 텍스트가 노출되어야 하지만 빈 문자열임 "
        f"(기대: 빈 문자열이 아님, 실제: {actual_price!r})"
    )

    actual_name = products_page.get_product_names()[target_index]
    assert actual_name != "", (
        f"{target_index}번째 카드에 상품명 텍스트가 노출되어야 하지만 빈 문자열임 "
        f"(기대: 빈 문자열이 아님, 실제: {actual_name!r})"
    )

    is_image_visible = products_page.is_image_visible_on_card(target_index)
    assert is_image_visible is True, (
        f"{target_index}번째 카드에 상품 이미지가 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_image_visible})"
    )

    is_add_to_cart_visible = products_page.is_add_to_cart_visible_on_card(target_index)
    assert is_add_to_cart_visible is True, (
        f"{target_index}번째 카드에 'Add to cart' 버튼이 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_add_to_cart_visible})"
    )

    is_view_product_visible = products_page.is_view_product_visible_on_card(target_index)
    assert is_view_product_visible is True, (
        f"{target_index}번째 카드에 'View Product' 링크가 노출되어야 하지만 그렇지 않음 "
        f"(기대: True, 실제: {is_view_product_visible})"
    )


def test_search_with_no_matching_keyword_shows_empty_result(driver):
    """TC-PRODUCT-SEARCH-003: 매칭되는 상품이 없는 검색어("zzzzznonexistent")로 검색 실행
    시 섹션 제목은 "SEARCHED PRODUCTS"로 동일하게 노출되지만 상품 카드는 하나도 노출되지
    않는다. "No result" 등 별도 안내 문구 부재는 이 테스트에서 별도로 assert하지 않는다
    (PRD 확정 사실 재확인 목적, 과설계 방지)."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.search_product("zzzzznonexistent")
    products_page.wait_for_url_contains("search=zzzzznonexistent")

    expected_title = "SEARCHED PRODUCTS"
    actual_title = products_page.get_section_title()
    assert actual_title == expected_title, (
        f"매칭 결과가 없어도 섹션 제목이 {expected_title!r}이어야 하지만 그렇지 않음 "
        f"(기대: {expected_title!r}, 실제: {actual_title!r})"
    )

    card_count = products_page.get_product_card_count()
    assert card_count == 0, (
        f"매칭되는 상품이 없는 검색어로 검색 실행 시 상품 카드가 노출되지 않아야 하지만 "
        f"그렇지 않음 (기대: 0개, 실제: {card_count}개)"
    )


def test_search_with_empty_keyword_shows_all_products(driver):
    """TC-PRODUCT-SEARCH-004: 검색창에 아무 값도 입력하지 않은 채 돋보기 버튼을 클릭하면
    전체 상품이 노출되고, URL에는 `?search=` 형태가 남아 원본 `/products`와 구분된다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    total_product_count = products_page.get_product_card_count()

    products_page.search_product("")
    products_page.wait_for_url_contains("search=")

    actual_url = driver.current_url
    assert "search=" in actual_url, (
        f"검색어 없이 검색 실행 시 URL에 'search='가 포함되어야 하지만 그렇지 않음 "
        f"(기대: 'search=' 포함, 실제: {actual_url!r})"
    )

    original_url = f"{BASE_URL.rstrip('/')}/products"
    assert actual_url != original_url, (
        f"검색어 없이 검색 실행한 URL은 원본 Products 페이지 URL과 구분되어야 하지만 "
        f"동일함 (원본: {original_url!r}, 실제: {actual_url!r})"
    )

    searched_product_count = products_page.get_product_card_count()
    assert searched_product_count == total_product_count, (
        f"검색어 없이 검색 실행해도 전체 상품 개수가 그대로 노출되어야 하지만 그렇지 않음 "
        f"(기대: {total_product_count}개, 실제: {searched_product_count}개)"
    )


def test_search_with_partial_product_name_matches_substring(driver):
    """TC-PRODUCT-SEARCH-005: 특정 상품명의 일부 문자열("Top")만 검색해도 부분 일치
    매칭으로 해당 상품들이 검색 결과에 노출된다(예: 상품명 "Blue Top"은 "Top"으로도
    매칭됨).

    [2026-08-31 assertion 방향 수정] TC-005 Expected Result는 "상품명에 검색어가
    부분적으로라도 포함되는 모든 상품이 노출된다"는 포함(inclusion) 방향의 주장이며,
    "노출된 모든 상품명에 검색어가 포함되어야 한다"는 배제(exclusion) 방향은 주장하지
    않는다(REQ-PRODUCT-SEARCH-005 정정에 따라 하위 카테고리명으로도 매칭되므로,
    상품명에 "top"이 없는 상품도 정상적으로 결과에 포함될 수 있다 — TC-001 재작업과
    동일한 이유). 따라서 이 테스트는 (1) 검색 결과가 1건 이상이고 (2) 그중 적어도
    하나는 상품명에 "top"이 포함되어(대소문자 무시) substring 매칭이 실제로 동작함을
    확인하는 방식으로 검증한다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.search_product("Top")
    products_page.wait_for_url_contains("search=Top")

    card_count = products_page.get_product_card_count()
    assert card_count > 0, (
        f"검색어 'Top'에 부분 일치하는 상품 카드가 1개 이상 노출되어야 하지만 그렇지 않음 "
        f"(기대: 1개 이상, 실제: {card_count}개)"
    )

    product_names = products_page.get_product_names()
    assert any("top" in name.lower() for name in product_names), (
        f"검색어 'Top'으로 노출된 상품 중 적어도 하나는 상품명에 'top'이 포함되어야 하지만 "
        f"그렇지 않음 (기대: 상품명에 'top' 포함된 항목 1개 이상, 실제 상품명 목록: {product_names})"
    )


@pytest.mark.parametrize(
    "keyword",
    ["biba", "kookie", "allen", "babyhug"],
)
def test_search_with_brand_keyword_shows_no_result(driver, keyword):
    """TC-PRODUCT-SEARCH-006: 검색어가 브랜드명(biba, kookie, allen, babyhug)과 일치(완전
    일치 포함)하더라도 브랜드명은 매칭 대상에서 항상 제외되어 검색 결과에 노출되지 않는다
    (`docs/tc/product-search.md` TC-PRODUCT-SEARCH-006, 2026-08-31 2차 재작성 기준).

    [2026-08-31 2차 변경 사유] 최초 재작성(1차)에서는 상위 카테고리명(women/men/kids)도 함께
    검증했으나, 실제 pytest 실행 결과 이 3개 keyword는 상품명에 리터럴로 포함되어 있어
    ("Madame Top For Women", "Men Tshirt", "Frozen Tops For Kids" 등) FAILED였다. 원인 분석
    결과 사용자가 REQ-PRODUCT-SEARCH-005/008을 재정정해 "브랜드명은 완전 일치 포함 항상
    제외"를 명확히 하면서 상위 카테고리명 매칭 여부는 PRD 4.2 미확인 항목으로 남겼다. 이에
    따라 이 테스트는 브랜드명 4개만 검증하도록 범위를 좁혔다(keyword 목록은 원본 TC 문서
    2차 재작성분을 그대로 사용)."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.search_product(keyword)
    products_page.wait_for_url_contains(f"search={keyword}")

    card_count = products_page.get_product_card_count()
    assert card_count == 0, (
        f"브랜드명 keyword {keyword!r}로 검색 시 상품 카드가 노출되지 않아야 "
        f"하지만 그렇지 않음 (기대: 0개, 실제: {card_count}개)"
    )


def test_search_with_enter_key_does_not_execute_search(driver):
    """TC-PRODUCT-SEARCH-008: 검색창에 검색어를 입력한 상태에서 돋보기 버튼을 클릭하지
    않고 키보드의 Enter 키만 입력하면 검색이 실행되지 않는다. URL과 섹션 제목("ALL
    PRODUCTS")이 검색 실행 전 상태 그대로 유지되며, 상품 목록도 변화하지 않는다.

    `ProductsPage.search_and_press_enter()`(Phase 4 Task 1에서 이미 구현 완료, 돋보기
    버튼은 클릭하지 않고 Enter 키만 전송)를 그대로 사용하며, 이 테스트에서는 신규
    Locator/메서드를 추가하지 않는다.

    [Wait 관련] Enter 키 입력은 `send_keys()`로 처리되는 동기 WebDriver 명령이라, 만약
    사이트가 Enter 키에 반응해 검색을 실행했다면 그 반응(URL 변경 등)은 이 메서드가
    반환하는 시점에 이미 시작되었을 것이다. 이 TC는 "아무 일도 일어나지 않음"을
    검증하는 부정(negative) 시나리오라 기다려야 할 대상 조건 자체가 없으므로,
    `time.sleep()`이나 별도의 인위적 대기 없이 메서드 호출 직후 상태를 바로 비교한다."""
    products_page = ProductsPage(driver)
    products_page.navigate()

    initial_url = driver.current_url
    initial_title = products_page.get_section_title()
    expected_initial_title = "ALL PRODUCTS"
    assert initial_title == expected_initial_title, (
        f"검색 실행 전 섹션 제목이 {expected_initial_title!r}이어야 하지만 그렇지 않음 "
        f"(기대: {expected_initial_title!r}, 실제: {initial_title!r})"
    )

    products_page.search_and_press_enter("shirt")

    actual_url = driver.current_url
    assert actual_url == initial_url, (
        f"Enter 키만 입력했을 때 URL이 검색 실행 전 상태({initial_url!r})로 유지되어야 "
        f"하지만 변경됨 (기대: {initial_url!r}, 실제: {actual_url!r})"
    )

    actual_title = products_page.get_section_title()
    assert actual_title == initial_title, (
        f"Enter 키만 입력했을 때 섹션 제목이 검색 실행 전 상태({initial_title!r})로 "
        f"유지되어야 하지만 변경됨 (기대: {initial_title!r}, 실제: {actual_title!r})"
    )


def test_search_shirt_shows_product_matched_by_subcategory_name(driver):
    """TC-PRODUCT-SEARCH-010: 검색어 "shirt"로 검색 실행 시, 상품명에 "shirt" 문자열이
    포함되지 않는 "Frozen Tops For Kids"가 하위 카테고리명("Tops") 부분 일치를 통해 검색
    결과에 노출된다.

    이 TC는 REQ-PRODUCT-SEARCH-005 정정을 촉발한 실제 관찰 사례를 그대로 회귀 테스트화한
    것으로, 상품명 목록에 기대 상품명이 정확히 포함되는지만 확인하면 충분해 신규 Page
    Object 메서드 없이 기존 `search_product()`/`get_product_names()`만 사용한다."""
    products_page = ProductsPage(driver)
    products_page.navigate()
    products_page.search_product("shirt")
    products_page.wait_for_url_contains("search=shirt")

    expected_product_name = "Frozen Tops For Kids"
    actual_product_names = products_page.get_product_names()
    assert expected_product_name in actual_product_names, (
        f"검색어 'shirt'로 검색 실행 시 하위 카테고리명(Tops) 부분 일치를 통해 "
        f"{expected_product_name!r}가 검색 결과에 노출되어야 하지만 그렇지 않음 "
        f"(기대: {expected_product_name!r} 포함, 실제 상품명 목록: {actual_product_names})"
    )
