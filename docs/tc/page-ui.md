---
문서유형: Test Case
상태: 승인완료   # 초안 | 승인완료
관련 Feature PRD: feature/page-ui.md
최초 작성일: 2026-08-22
최근 변경일: 2026-08-22
승인일: 2026-08-22
---

# Test Case - 각 페이지별 UI

## TC 목록

> 공통 Preconditions: 사이트 진입 시 또는 일정 시간 경과 시 무작위로 노출될 수 있는 모달형 광고는
> Project PRD "8. 기타 제약사항" 원칙에 따라 검증 대상이 아니므로, 모든 TC 수행 전 광고 모달이
> 노출된 경우 닫은 상태에서 진행한다(아래 표에는 반복 기재하지 않음).

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-PAGE-UI-001 | REQ-PAGE-UI-001 | 각 페이지별 UI | Home 페이지 최상단 배너/캐러셀의 좌우 화살표, dot 인디케이터, 활성 dot 색상 노출 확인 | 로그인/로그아웃 상태 무관 | 1. Home(`/`) 페이지로 진입한다.<br>2. 최상단 배너/캐러셀 영역의 좌우 화살표, 하단 dot 인디케이터 개수, 현재 슬라이드 dot 색상을 확인한다. | 좌우 화살표(이전/다음)가 노출되고, 하단에 dot 인디케이터 3개가 노출되며, 현재 슬라이드에 해당하는 dot이 주황색으로 표시된다. | P2 | |
| TC-PAGE-UI-002 | REQ-PAGE-UI-001 | 각 페이지별 UI | Home 페이지 배너/캐러셀의 자동 전환(약 3~4초 간격) 동작 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지로 진입해 현재 슬라이드(활성 dot 위치)를 확인한다.<br>2. 별도 조작 없이 약 4~5초간 대기한 후 슬라이드(활성 dot 위치)를 다시 확인한다. | 별도 조작 없이도 슬라이드가 자동으로 전환되어 활성 dot 위치가 변경된다. | P2 | |
| TC-PAGE-UI-003 | REQ-PAGE-UI-001 | 각 페이지별 UI | Home 페이지 배너/캐러셀의 좌우 화살표 클릭을 통한 수동 전환 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지로 진입해 현재 슬라이드(활성 dot 위치)를 확인한다.<br>2. 배너의 오른쪽(다음) 화살표를 클릭한다. | 클릭 즉시 다음 슬라이드로 전환되며 활성 dot 위치가 변경된다. | P2 | |
| TC-PAGE-UI-004 | REQ-PAGE-UI-002 | 각 페이지별 UI | Home 페이지 "CATEGORY" 섹션에 WOMEN/MEN/KIDS 3개 카테고리가 아코디언 형태로 노출되는지 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지로 진입한다.<br>2. "CATEGORY" 섹션을 확인한다. | "CATEGORY" 섹션에 WOMEN, MEN, KIDS 3개 카테고리가 각각 "+" 아이콘이 있는 아코디언 형태로 노출된다. | P2 | |
| TC-PAGE-UI-005 | REQ-PAGE-UI-003 | 각 페이지별 UI | Home 페이지 "BRANDS" 섹션에 브랜드명과 상품 개수가 함께 노출되는지 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지로 진입한다.<br>2. "BRANDS" 섹션의 브랜드 목록을 확인한다. | POLO(6), H&M(5), MADAME(5), MAST & HARBOUR(3), BABYHUG(4), ALLEN SOLLY JUNIOR(3), KOOKIE KIDS(3), BIBA(5) 형태로 브랜드명과 괄호 안 상품 개수가 함께 노출된다. | P2 | |
| TC-PAGE-UI-006 | REQ-PAGE-UI-004 | 각 페이지별 UI | Home 페이지 "FEATURES ITEMS" 섹션이 한 행 3개 카드 그리드 형태로 노출되고 각 카드 구성요소가 표시되는지 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지로 진입한다.<br>2. "FEATURES ITEMS" 섹션으로 스크롤해 카드 배치와 각 카드 구성요소를 확인한다. | 상품 카드가 한 행에 3개씩 배치된 그리드 형태로 노출되며, 각 카드에 상품 이미지, 가격(Rs. 단위), 상품명, "Add to cart" 버튼, "View Product" 링크가 모두 노출된다. | P1 | |
| TC-PAGE-UI-007 | REQ-PAGE-UI-005 | 각 페이지별 UI | "FEATURES ITEMS" 하단에 "RECOMMENDED ITEMS" 섹션이 별도 캐러셀 형태로 노출되는지 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지에서 "FEATURES ITEMS" 섹션 하단으로 스크롤한다.<br>2. "RECOMMENDED ITEMS" 섹션을 확인한다. | "RECOMMENDED ITEMS" 섹션이 "FEATURES ITEMS" 그리드와 별도로, 좌우 화살표가 있는 캐러셀 형태로 노출된다(그리드 형태와 구분됨). | P2 | |
| TC-PAGE-UI-008 | REQ-PAGE-UI-005 | 각 페이지별 UI | "RECOMMENDED ITEMS" 캐러셀의 자동 전환(약 4~5초 간격) 동작 확인 | "RECOMMENDED ITEMS" 섹션 노출 상태 | 1. "RECOMMENDED ITEMS" 섹션까지 스크롤해 현재 노출 상품을 확인한다.<br>2. 별도 조작 없이 약 5~6초간 대기한 후 노출 상품을 다시 확인한다. | 별도 조작 없이도 노출 상품이 자동으로 전환된다. | P2 | |
| TC-PAGE-UI-009 | REQ-PAGE-UI-005 | 각 페이지별 UI | "RECOMMENDED ITEMS" 캐러셀 좌우 화살표 클릭을 통한 수동 전환 확인 | "RECOMMENDED ITEMS" 섹션 노출 상태 | 1. "RECOMMENDED ITEMS" 섹션까지 스크롤해 현재 노출 상품을 확인한다.<br>2. 캐러셀의 오른쪽(다음) 화살표를 클릭한다. | 클릭 즉시 다음 상품(들)로 전환되어 노출 상품이 변경된다. | P2 | |
| TC-PAGE-UI-010 | REQ-PAGE-UI-006 | 각 페이지별 UI | Home 페이지 최하단에 "SUBSCRIPTION" 섹션이 노출되는지 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지 최하단까지 스크롤한다.<br>2. "SUBSCRIPTION" 섹션을 확인한다. | 이메일 입력창, 제출 버튼, 안내 문구로 구성된 "SUBSCRIPTION" 섹션이 노출된다. | P2 | |
| TC-PAGE-UI-011 | REQ-PAGE-UI-007 | 각 페이지별 UI | "SUBSCRIPTION" 섹션 아래에 Copyright 문구가 포함된 푸터가 노출되는지 확인 | Home 페이지 진입 상태 | 1. Home(`/`) 페이지 최하단까지 스크롤한다.<br>2. "SUBSCRIPTION" 섹션 아래 영역을 확인한다. | "Copyright © 2021 All rights reserved" 문구가 포함된 푸터가 노출된다. | P2 | |
| TC-PAGE-UI-012 | REQ-PAGE-UI-008 | 각 페이지별 UI | Products 페이지 최상단에 "SPECIAL OFFER BIG SALE UP TO 50% OFF" 배너 이미지가 노출되는지 확인 | 로그인/로그아웃 상태 무관 | 1. Products(`/products`) 페이지로 진입한다.<br>2. 페이지 최상단을 확인한다. | "SPECIAL OFFER BIG SALE UP TO 50% OFF" 문구가 포함된 배너 이미지가 최상단에 노출된다. | P2 | |
| TC-PAGE-UI-013 | REQ-PAGE-UI-009 | 각 페이지별 UI | Products 페이지 상단 배너 아래 "Search Product" placeholder 검색창과 돋보기 아이콘 버튼 노출 확인 | Products 페이지 진입 상태 | 1. Products(`/products`) 페이지로 진입한다.<br>2. 상단 배너 아래 영역을 확인한다. | "Search Product" placeholder를 가진 검색 입력창과 돋보기 아이콘 버튼이 나란히 배치되어 노출된다. | P2 | |
| TC-PAGE-UI-014 | REQ-PAGE-UI-010 | 각 페이지별 UI | Products 페이지 좌측 사이드바에 Home 페이지와 동일한 CATEGORY/BRANDS 섹션이 노출되는지 확인 | Products 페이지 진입 상태 | 1. Products(`/products`) 페이지로 진입한다.<br>2. 좌측 사이드바의 "CATEGORY", "BRANDS" 섹션을 확인한다. | Home 페이지와 동일하게 CATEGORY(WOMEN/MEN/KIDS 아코디언), BRANDS(브랜드명+개수) 섹션이 노출된다. | P2 | |
| TC-PAGE-UI-015 | REQ-PAGE-UI-011 | 각 페이지별 UI | Products 페이지 "ALL PRODUCTS" 섹션이 Home 페이지 FEATURES ITEMS와 동일한 카드 그리드 구조로 노출되는지 확인 | Products 페이지 진입 상태 | 1. Products(`/products`) 페이지로 진입한다.<br>2. "ALL PRODUCTS" 섹션을 확인한다. | 상품 이미지, 가격, 상품명, "Add to cart" 버튼, "View Product" 링크로 구성된 카드가 그리드 형태로 노출된다. | P1 | |
| TC-PAGE-UI-016 | REQ-PAGE-UI-012 | 각 페이지별 UI | Products 페이지 하단에 Home 페이지와 동일한 SUBSCRIPTION 섹션 및 Copyright 푸터가 노출되는지 확인 | Products 페이지 진입 상태 | 1. Products(`/products`) 페이지 최하단까지 스크롤한다.<br>2. SUBSCRIPTION 섹션 및 푸터를 확인한다. | Home 페이지와 동일한 SUBSCRIPTION 섹션(이메일 입력창, 제출 버튼, 안내 문구)과 "Copyright © 2021 All rights reserved" 문구가 포함된 푸터가 노출된다. | P2 | |
| TC-PAGE-UI-017 | REQ-PAGE-UI-013 | 각 페이지별 UI | 장바구니가 비어있는 상태에서 "Home > Shopping Cart" 브레드크럼 노출 확인 | 장바구니에 담긴 상품이 없는 상태 | 1. `/view_cart` 페이지로 진입한다.<br>2. 상단 네비게이션 하단 영역을 확인한다. | "Home > Shopping Cart" 형태의 브레드크럼이 노출된다. | P2 | |
| TC-PAGE-UI-018 | REQ-PAGE-UI-013 | 각 페이지별 UI | 장바구니에 상품이 담긴 상태에서도 동일하게 "Home > Shopping Cart" 브레드크럼이 노출되는지 확인 | 장바구니에 상품이 1개 이상 담긴 상태(사전 조작은 상품 담기 기능을 통해 준비) | 1. 상품이 담긴 상태로 `/view_cart` 페이지로 진입한다.<br>2. 상단 네비게이션 하단 영역을 확인한다. | 상품이 없는 상태(TC-PAGE-UI-017)와 동일하게 "Home > Shopping Cart" 브레드크럼이 노출된다. | P2 | |
| TC-PAGE-UI-019 | REQ-PAGE-UI-014 | 각 페이지별 UI | 장바구니가 비어있는 상태에서 안내 문구와 링크가 노출되는지 확인 | 장바구니에 담긴 상품이 없는 상태 | 1. `/view_cart` 페이지로 진입한다.<br>2. 페이지 중앙 영역을 확인한다. | "Cart is empty! Click here to buy products." 안내 문구와 "here" 링크가 노출된다. | P2 | |
| TC-PAGE-UI-020 | REQ-PAGE-UI-015 | 각 페이지별 UI | 장바구니에 상품이 담긴 상태에서 화면 우측 상단에 "Proceed To Checkout" 버튼이 노출되는지 확인 | 장바구니에 상품이 1개 이상 담긴 상태(사전 조작은 상품 담기 기능을 통해 준비) | 1. 상품이 담긴 상태로 `/view_cart` 페이지로 진입한다.<br>2. 화면 우측 상단 영역을 확인한다. | 주황색의 "Proceed To Checkout" 버튼이 화면 우측 상단에 노출된다. | P2 | |
| TC-PAGE-UI-021 | REQ-PAGE-UI-016 | 각 페이지별 UI | 장바구니에 상품이 담긴 상태에서 상품 목록 표의 컬럼 구성과 삭제 아이콘이 올바르게 노출되는지 확인 | 장바구니에 상품이 1개 이상 담긴 상태(사전 조작은 상품 담기 기능을 통해 준비) | 1. 상품이 담긴 상태로 `/view_cart` 페이지로 진입한다.<br>2. 상품 목록 표의 각 컬럼과 행 구성을 확인한다. | "Item"(이미지), "Description"(상품명+카테고리 경로, 예: "Blue Top / Women > Tops"), "Price", "Quantity"(입력란 형태), "Total"(가격×수량) 컬럼이 노출되고, 각 행 맨 끝에 삭제(x) 아이콘 버튼이 노출된다. | P1 | |
| TC-PAGE-UI-022 | REQ-PAGE-UI-017 | 각 페이지별 UI | Signup/Login 페이지에 Products 페이지의 "SPECIAL OFFER" 배너와 같은 별도 배너 이미지가 노출되지 않는지 확인 | 로그아웃 상태 | 1. `/login` 페이지로 진입한다.<br>2. 페이지 상단 영역을 확인한다. | Products 페이지의 "SPECIAL OFFER BIG SALE UP TO 50% OFF"와 같은 별도 배너 이미지가 노출되지 않는다. | P2 | |
| TC-PAGE-UI-023 | REQ-PAGE-UI-018 | 각 페이지별 UI | CATEGORY 아코디언에서 카테고리(예: WOMEN) 클릭 시 하위 메뉴가 펼쳐지는지 확인 | Home(`/`) 페이지 진입 상태 (Home/Products 공통 동작이므로 Home 기준으로 확인) | 1. Home(`/`) 페이지의 "CATEGORY" 섹션에서 "WOMEN"을 클릭한다.<br>2. 하위 메뉴 노출 여부를 확인한다. | "WOMEN" 하위에 DRESS, TOPS & SHIRTS, SAREE 등의 하위 메뉴가 펼쳐져 노출된다. | P1 | |
| TC-PAGE-UI-024 | REQ-PAGE-UI-018 | 각 페이지별 UI | CATEGORY 아코디언에서 다른 카테고리를 클릭하면 이전에 열려 있던 카테고리가 닫히는지 확인(단일 오픈) | Home(`/`) 페이지에서 하나의 카테고리(WOMEN)가 펼쳐져 있는 상태 | 1. "WOMEN" 카테고리를 클릭해 하위 메뉴를 펼친다.<br>2. 이어서 "MEN" 카테고리를 클릭한다. | "MEN" 하위 메뉴(TSHIRTS, JEANS 등)가 펼쳐지고, 동시에 이전에 열려 있던 "WOMEN"의 하위 메뉴는 닫힌다(한 번에 하나의 카테고리만 펼쳐짐). | P2 | |
| TC-PAGE-UI-025 | REQ-PAGE-UI-019 | 각 페이지별 UI | CATEGORY 하위 메뉴(예: MEN > JEANS) 클릭 시 해당 카테고리 상품 목록 페이지로 이동하는지 확인 | Home(`/`) 페이지에서 "MEN" 카테고리가 펼쳐진 상태 | 1. "MEN" 카테고리를 클릭해 하위 메뉴를 펼친다.<br>2. 하위 메뉴 중 "JEANS"를 클릭한다. | `/category_products/{id}` 형태의 상품 목록 페이지(예: `/category_products/6`)로 이동하며, "Products > Men > Jeans" 브레드크럼, "Men - Jeans PRODUCTS" 제목, 해당 카테고리 상품 그리드(이미지/가격/상품명/Add to cart/View Product 카드 구조)가 노출된다. | P1 | |
| TC-PAGE-UI-026 | REQ-PAGE-UI-020 | 각 페이지별 UI | "BRANDS" 목록의 브랜드명(예: H&M) 클릭 시 해당 브랜드 상품 목록 페이지로 이동하는지 확인 | Home(`/`) 페이지 진입 상태 | 1. "BRANDS" 섹션에서 "H&M"을 클릭한다. | `/brand_products/{브랜드명}` 형태의 상품 목록 페이지(예: `/brand_products/H%26M`)로 이동하며, "Products > H&M" 브레드크럼, "BRAND - H&M PRODUCTS" 제목, 해당 브랜드 상품 그리드(동일 카드 구조)가 노출된다. | P1 | |
| TC-PAGE-UI-027 | REQ-PAGE-UI-021 | 각 페이지별 UI | Home 페이지 "FEATURES ITEMS" 섹션에 전체 34개 상품이 페이지네이션 없이 스크롤로 노출되는지 확인 | Home(`/`) 페이지 진입 상태 | 1. Home(`/`) 페이지로 진입한다.<br>2. "FEATURES ITEMS" 섹션을 최하단까지 스크롤하며 노출되는 상품 개수와 페이지네이션 UI 존재 여부를 확인한다. | 별도의 페이지네이션 UI 없이 스크롤을 통해 전체 34개 상품이 이어서 노출된다. | P2 | |
| TC-PAGE-UI-028 | REQ-PAGE-UI-022 | 각 페이지별 UI | BRANDS 섹션에 표시된 브랜드별 괄호 숫자가 해당 브랜드 상품 목록 페이지의 실제 노출 개수와 일치하는지 확인 | Home(`/`) 페이지 진입 상태 | 1. Home(`/`) 페이지의 "BRANDS" 섹션에서 임의 브랜드(예: POLO(6))의 표시 개수를 확인한다.<br>2. 해당 브랜드명을 클릭해 `/brand_products/{브랜드명}` 페이지로 이동한다.<br>3. 이동한 페이지에서 실제로 노출되는 상품 개수를 확인한다. | BRANDS 섹션에 표시된 괄호 숫자(예: 6)와 브랜드 상품 목록 페이지에서 실제로 노출되는 상품 개수가 일치한다. | P1 | |
| TC-PAGE-UI-029 | REQ-PAGE-UI-023 | 각 페이지별 UI | CATEGORY 클릭으로 이동한 상품 목록 페이지에 해당 카테고리에 속하는 상품만 노출되는지 확인 | Home(`/`) 페이지 진입 상태 | 1. CATEGORY에서 임의 하위 카테고리(예: MEN > JEANS)를 클릭해 `/category_products/{id}` 페이지로 이동한다.<br>2. 노출되는 상품 목록의 각 상품 정보(카테고리 경로 등)를 확인한다. | 노출되는 모든 상품이 선택한 카테고리(Men > Jeans)에 속하며, 무관한 카테고리의 상품이 섞여 노출되지 않는다. | P1 | |
| TC-PAGE-UI-030 | REQ-PAGE-UI-023 | 각 페이지별 UI | BRANDS 클릭으로 이동한 상품 목록 페이지에 해당 브랜드 상품만 노출되는지 확인 | Home(`/`) 페이지 진입 상태 | 1. BRANDS에서 임의 브랜드(예: H&M)를 클릭해 `/brand_products/{브랜드명}` 페이지로 이동한다.<br>2. 노출되는 상품 목록의 각 상품 정보를 확인한다. | 노출되는 모든 상품이 선택한 브랜드(H&M)에 해당하며, 무관한 브랜드의 상품이 섞여 노출되지 않는다. | P1 | |
| TC-PAGE-UI-031 | REQ-PAGE-UI-024 | 각 페이지별 UI | 모든 CATEGORY/BRANDS 항목에 최소 1개 이상의 상품이 존재하며 0개로 노출되는 항목이 없는지 확인 | Home(`/`) 페이지 진입 상태 | 1. CATEGORY의 각 하위 카테고리와 BRANDS의 각 브랜드를 순회하며 클릭해 이동한 상품 목록 페이지의 상품 개수를 확인한다. | 모든 카테고리/브랜드 상품 목록 페이지에 최소 1개 이상의 상품이 노출되며, 상품이 0개로 노출되는 카테고리/브랜드가 없다. | P2 | |
| TC-PAGE-UI-032 | REQ-PAGE-UI-018 | 각 페이지별 UI | Products 페이지 좌측 사이드바 CATEGORY 아코디언에서 카테고리(예: WOMEN) 클릭 시 하위 메뉴가 펼쳐지는지 확인 | Products(`/products`) 페이지 진입 상태 | 1. Products(`/products`) 페이지 좌측 사이드바 "CATEGORY" 섹션에서 "WOMEN"을 클릭한다.<br>2. 하위 메뉴 노출 여부를 확인한다. | "WOMEN" 하위에 DRESS, TOPS & SHIRTS, SAREE 등의 하위 메뉴가 펼쳐져 노출된다. | P1 | |
| TC-PAGE-UI-033 | REQ-PAGE-UI-018 | 각 페이지별 UI | Products 페이지 좌측 사이드바 CATEGORY 아코디언에서 다른 카테고리를 클릭하면 이전에 열려 있던 카테고리가 닫히는지 확인(단일 오픈) | Products(`/products`) 페이지에서 하나의 카테고리(WOMEN)가 펼쳐져 있는 상태 | 1. Products(`/products`) 페이지 좌측 사이드바에서 "WOMEN" 카테고리를 클릭해 하위 메뉴를 펼친다.<br>2. 이어서 "MEN" 카테고리를 클릭한다. | "MEN" 하위 메뉴(TSHIRTS, JEANS 등)가 펼쳐지고, 동시에 이전에 열려 있던 "WOMEN"의 하위 메뉴는 닫힌다(한 번에 하나의 카테고리만 펼쳐짐). | P2 | |
| TC-PAGE-UI-034 | REQ-PAGE-UI-025 | 각 페이지별 UI | 로그인 상태로 장바구니에 상품이 담긴 채 `/checkout` 페이지 진입 시 "Address Details" 영역(Delivery/Billing Address) 노출 확인 | 로그인 상태이며 장바구니에 상품이 1개 이상 담긴 상태(사전 조작은 로그인 및 상품 담기 기능을 통해 준비) | 1. 로그인 상태로 상품을 장바구니에 담은 뒤 `/view_cart` 페이지에서 "Proceed To Checkout" 버튼을 클릭해 `/checkout` 페이지로 이동한다.<br>2. 페이지 상단의 "Address Details" 영역을 확인한다. | "Address Details" 영역이 노출되며, 그 안에 "Your Delivery Address"와 "Your Billing Address"가 함께 배치되어 노출된다. | P2 | |
| TC-PAGE-UI-035 | REQ-PAGE-UI-026 | 각 페이지별 UI | Address Details의 Delivery/Billing Address에 회원가입 시 입력한 이름/주소 정보가 자동으로 채워져 표시되는지 확인 | 기존 테스트 계정 재사용(예: actest1@test.com, 회원가입 시 입력했던 이름/주소 정보를 그대로 비교 기준으로 사용), 해당 계정으로 로그인한 상태이며 장바구니에 상품이 1개 이상 담긴 상태에서 `/checkout` 페이지에 진입한 상태 | 1. 기존 테스트 계정(예: actest1@test.com)이 회원가입 시 입력했던 이름/주소 정보를 비교 기준으로 미리 확인해 둔다.<br>2. `/checkout` 페이지의 "Your Delivery Address"와 "Your Billing Address" 영역에 표시된 이름/주소 정보를 확인한다. | Delivery Address와 Billing Address에 표시된 이름/주소 정보가 해당 계정이 회원가입 시 입력한 정보와 동일하게 자동으로 채워져 표시된다. | P1 | |
| TC-PAGE-UI-036 | REQ-PAGE-UI-027 | 각 페이지별 UI | Address Details 영역 아래 "Review Your Order" 영역에 Cart 페이지와 동일한 컬럼 구성의 상품 목록 표가 노출되는지 확인 | 로그인 상태이며 장바구니에 상품이 1개 이상 담긴 상태에서 `/checkout` 페이지에 진입한 상태 | 1. `/checkout` 페이지에서 "Address Details" 영역 아래로 스크롤한다.<br>2. "Review Your Order" 영역의 상품 목록 표 컬럼 구성을 확인한다. | "Review Your Order" 영역이 노출되며, Cart 페이지(TC-PAGE-UI-021)와 동일하게 "Item"(이미지), "Description"(상품명+카테고리 경로), "Price", "Quantity", "Total" 컬럼으로 구성된 상품 목록 표가 노출된다. | P1 | |
| TC-PAGE-UI-037 | REQ-PAGE-UI-028 | 각 페이지별 UI | "Review Your Order" 표 하단에 Total Amount(합계 금액)가 노출되는지 확인 | 로그인 상태이며 장바구니에 상품이 1개 이상 담긴 상태에서 `/checkout` 페이지에 진입한 상태 | 1. `/checkout` 페이지의 "Review Your Order" 표 하단 영역을 확인한다. | 상품 목록 표 하단에 Total Amount(합계 금액)가 노출된다. | P2 | |
| TC-PAGE-UI-038 | REQ-PAGE-UI-029 | 각 페이지별 UI | "Review Your Order" 영역 아래에 주문 관련 코멘트를 입력할 수 있는 textarea가 노출되는지 확인 | 로그인 상태이며 장바구니에 상품이 1개 이상 담긴 상태에서 `/checkout` 페이지에 진입한 상태 | 1. `/checkout` 페이지에서 "Review Your Order" 영역 아래를 확인한다. | 주문 관련 코멘트를 입력할 수 있는 textarea가 노출된다. | P2 | |
| TC-PAGE-UI-039 | REQ-PAGE-UI-030 | 각 페이지별 UI | `/checkout` 페이지 하단에 "Place Order" 버튼이 노출되는지 확인 | 로그인 상태이며 장바구니에 상품이 1개 이상 담긴 상태에서 `/checkout` 페이지에 진입한 상태 | 1. `/checkout` 페이지 최하단 영역을 확인한다. | "Place Order" 버튼이 페이지 하단에 노출된다. | P2 | |
| TC-PAGE-UI-040 | REQ-PAGE-UI-031 | 각 페이지별 UI | Address Details의 배송지/청구지 정보가 수정 불가능한 표시 전용(read-only) 형태로 노출되는지 확인 | 로그인 상태이며 장바구니에 상품이 1개 이상 담긴 상태에서 `/checkout` 페이지에 진입한 상태 | 1. `/checkout` 페이지의 "Your Delivery Address"/"Your Billing Address" 영역에 표시된 텍스트를 클릭하거나 수정을 시도한다. | 배송지/청구지 정보는 입력란(editable field)이 아닌 표시 전용 텍스트로 노출되어 클릭/수정이 불가능하다. | P2 | |
| TC-PAGE-UI-041 | REQ-PAGE-UI-031 | 각 페이지별 UI | "Review Your Order" 표의 Quantity 값이 Cart 페이지(TC-PAGE-UI-021)와 달리 수정 불가능한 표시 전용(read-only) 형태로 노출되는지 확인 | 로그인 상태이며 장바구니에 상품이 1개 이상 담긴 상태에서 `/checkout` 페이지에 진입한 상태 | 1. `/checkout` 페이지의 "Review Your Order" 표에서 Quantity 값을 클릭하거나 수정을 시도한다. | Quantity 값은 Cart 페이지의 입력란(editable) 형태와 달리 표시 전용 텍스트로 노출되어 클릭/수정이 불가능하다. | P1 | |

## Priority 산정 근거

- **TC-PAGE-UI-001**: Impact 2 / Likelihood 2 / Risk Score 4 — 정적 UI 요소(화살표, dot 색상) 확인으로 결함이 있어도 서비스 이용 자체에는 영향이 제한적이며 변경 가능성이 낮음.
- **TC-PAGE-UI-002**: Impact 2 / Likelihood 3 / Risk Score 6 — 타이머 기반 자동 전환은 JS 구현 특성상 정적 렌더링보다 결함 발생 가능성이 다소 높음.
- **TC-PAGE-UI-003**: Impact 2 / Likelihood 2 / Risk Score 4 — 단순 클릭 기반 전환으로 결함 발생 가능성과 영향 모두 제한적.
- **TC-PAGE-UI-004**: Impact 2 / Likelihood 2 / Risk Score 4 — 정적 아코디언 목록 노출 확인.
- **TC-PAGE-UI-005**: Impact 2 / Likelihood 2 / Risk Score 4 — 표시 여부만 확인(개수 정확성은 TC-028에서 별도 검증).
- **TC-PAGE-UI-006**: Impact 3 / Likelihood 3 / Risk Score 9 — 이커머스 핵심 상품 탐색 UI이며 여러 구성요소(이미지/가격/버튼/링크)를 동시에 검증해야 해 결함 발생 가능성도 일반 수준 이상.
- **TC-PAGE-UI-007**: Impact 2 / Likelihood 2 / Risk Score 4 — 섹션 존재 및 형태 확인 수준.
- **TC-PAGE-UI-008**: Impact 2 / Likelihood 3 / Risk Score 6 — TC-002와 동일 근거(타이머 기반 자동 전환).
- **TC-PAGE-UI-009**: Impact 2 / Likelihood 2 / Risk Score 4 — TC-003과 동일 근거.
- **TC-PAGE-UI-010**: Impact 2 / Likelihood 1 / Risk Score 2 — 정적 섹션으로 변경 가능성 낮음.
- **TC-PAGE-UI-011**: Impact 1 / Likelihood 1 / Risk Score 1 — 텍스트 문구 확인 수준으로 영향이 매우 낮음.
- **TC-PAGE-UI-012**: Impact 2 / Likelihood 1 / Risk Score 2 — 정적 배너 이미지 확인.
- **TC-PAGE-UI-013**: Impact 3 / Likelihood 2 / Risk Score 6 — "상품 검색" Feature의 진입점 UI이므로 영향은 있으나, 검증 대상은 검색 동작이 아닌 요소 노출 여부로 제한됨.
- **TC-PAGE-UI-014**: Impact 2 / Likelihood 2 / Risk Score 4 — Home과 동일 구조 재사용 요소로 결함 가능성 낮음.
- **TC-PAGE-UI-015**: Impact 3 / Likelihood 3 / Risk Score 9 — TC-006과 동일 근거(핵심 상품 탐색 UI, 다요소 검증).
- **TC-PAGE-UI-016**: Impact 1 / Likelihood 1 / Risk Score 1 — TC-010/011과 동일 근거.
- **TC-PAGE-UI-017**: Impact 2 / Likelihood 2 / Risk Score 4 — 정적 브레드크럼 확인.
- **TC-PAGE-UI-018**: Impact 2 / Likelihood 2 / Risk Score 4 — TC-017과 동일 근거이며, 상태(빈 카트/담긴 카트)에 따라 다르게 동작하지 않아야 한다는 요구사항을 별도로 검증.
- **TC-PAGE-UI-019**: Impact 3 / Likelihood 2 / Risk Score 6 — 빈 카트 상태에서 사용자를 구매로 유도하는 안내 UX 요소로 일정 수준 영향이 있음.
- **TC-PAGE-UI-020**: Impact 3 / Likelihood 2 / Risk Score 6 — 구매 퍼널 진입 버튼이나, 본 문서 범위는 결제 기능 자체가 아닌 버튼의 "노출 여부"로 한정됨(결제는 Project PRD Out of Scope).
- **TC-PAGE-UI-021**: Impact 3 / Likelihood 3 / Risk Score 9 — 여러 컬럼과 삭제 버튼이 동시에 존재해야 하는 복합 구성요소로 결함 발생 가능성이 일반 수준 이상.
- **TC-PAGE-UI-022**: Impact 1 / Likelihood 1 / Risk Score 1 — 배너 "미노출"을 확인하는 단순 Negative Case.
- **TC-PAGE-UI-023**: Impact 3 / Likelihood 3 / Risk Score 9 — 사용자가 실제로 조작하는 네비게이션 UX 요소이며 JS 인터랙션 특성상 결함 발생 가능성 존재.
- **TC-PAGE-UI-024**: Impact 2 / Likelihood 3 / Risk Score 6 — 단일 오픈 정책은 부가적인 UX 규칙으로 영향은 제한적이나, 상태 관리 로직이 있어 결함 발생 가능성은 있음.
- **TC-PAGE-UI-025**: Impact 4 / Likelihood 3 / Risk Score 12 — 상품 탐색의 핵심 이동 경로이며, URL/브레드크럼/제목/그리드 등 여러 요소를 함께 검증해야 함.
- **TC-PAGE-UI-026**: Impact 4 / Likelihood 3 / Risk Score 12 — TC-025와 동일 근거(다른 진입 경로).
- **TC-PAGE-UI-027**: Impact 2 / Likelihood 2 / Risk Score 4 — 고정된 상품 개수 확인으로 변경 가능성이 낮은 정적 데이터 확인.
- **TC-PAGE-UI-028**: Impact 4 / Likelihood 3 / Risk Score 12 — 표시 정보(개수)와 실제 데이터 간 불일치는 사용자 신뢰도에 영향을 미치는 데이터 정합성 이슈이며, 프론트/백엔드 데이터 연동 특성상 결함 발생 가능성도 존재.
- **TC-PAGE-UI-029**: Impact 4 / Likelihood 3 / Risk Score 12 — 필터링 정확성은 이커머스 상품 탐색의 핵심 신뢰성 요소이며 필터링 로직 결함 발생 가능성이 일반 수준 이상.
- **TC-PAGE-UI-030**: Impact 4 / Likelihood 3 / Risk Score 12 — TC-029와 동일 근거(브랜드 필터링).
- **TC-PAGE-UI-031**: Impact 2 / Likelihood 2 / Risk Score 4 — 데이터 완전성 확인 성격의 보조적 검증으로 영향이 제한적.
- **TC-PAGE-UI-032**: Impact 3 / Likelihood 3 / Risk Score 9 — TC-023과 동일 근거(사용자가 실제로 조작하는 네비게이션 UX 요소이며 JS 인터랙션 특성상 결함 발생 가능성 존재). Products 페이지에서도 동일한 REQ-PAGE-UI-018 동작을 별도로 검증하기 위해 Home 기준 TC-023과 동일한 점수를 적용함(사용자 요청에 따라 신규 추가).
- **TC-PAGE-UI-033**: Impact 2 / Likelihood 3 / Risk Score 6 — TC-024와 동일 근거(단일 오픈 정책은 부가적인 UX 규칙으로 영향은 제한적이나, 상태 관리 로직이 있어 결함 발생 가능성은 있음). Products 페이지에서도 동일한 REQ-PAGE-UI-018 동작을 별도로 검증하기 위해 Home 기준 TC-024와 동일한 점수를 적용함(사용자 요청에 따라 신규 추가).
- **TC-PAGE-UI-034** *(신규, 확인 필요)*: Impact 3 / Likelihood 2 / Risk Score 6 — Checkout 진입 시 Address Details 영역 노출 자체는 구매 여정에서 중요한 정적 구성요소이나, 본 TC는 존재/배치 확인 수준이고 렌더링 복잡도가 낮아 결함 발생 가능성은 제한적임.
- **TC-PAGE-UI-035** *(신규, 확인 필요)*: Impact 4 / Likelihood 3 / Risk Score 12 — 회원 개인 정보(이름/주소)를 자동으로 채워 보여주는 개인화 결과이므로 값이 틀리면 서비스 결과의 신뢰성이 크게 훼손됨(Impact 4). 프론트-백엔드 데이터 연동을 거쳐 표시되는 값이라 결함 발생 가능성도 일반 수준 이상(Likelihood 3).
- **TC-PAGE-UI-036** *(신규, 확인 필요)*: Impact 3 / Likelihood 3 / Risk Score 9 — TC-PAGE-UI-021(Cart 상품 목록 표)과 동일 근거. 여러 컬럼이 동시에 올바르게 구성되어야 하는 복합 요소로 결함 발생 가능성이 일반 수준 이상.
- **TC-PAGE-UI-037** *(신규, 확인 필요)*: Impact 3 / Likelihood 2 / Risk Score 6 — 금액 정보가 노출되어야 하는 요소로 일정 수준 영향이 있으나, 본 TC는 금액 계산의 정확성이 아닌 "노출 여부"로 범위가 한정됨(TC-PAGE-UI-020과 동일한 근거 구조).
- **TC-PAGE-UI-038** *(신규, 확인 필요)*: Impact 2 / Likelihood 2 / Risk Score 4 — 주문 코멘트 입력란은 부가적인 UX 요소로 영향이 제한적이며, 단순 정적 요소 노출 확인 수준.
- **TC-PAGE-UI-039** *(신규, 확인 필요)*: Impact 3 / Likelihood 2 / Risk Score 6 — TC-PAGE-UI-020(Proceed To Checkout 버튼 노출)과 동일 근거 구조. "Place Order"는 구매 퍼널의 마지막 CTA이나, 본 문서 범위는 클릭 이후 동작이 아닌 버튼의 "노출 여부"로 한정됨(결제는 Project PRD Out of Scope).
- **TC-PAGE-UI-040** *(신규, 확인 필요)*: Impact 3 / Likelihood 2 / Risk Score 6 — 배송지/청구지 정보가 편집 가능하면 잘못된 주문 정보로 이어질 수 있어 일정 수준 영향이 있으나(단, 실제 주문 제출/처리는 Out of Scope), read-only 속성 확인은 상대적으로 단순한 검증이라 결함 발생 가능성은 제한적.
- **TC-PAGE-UI-041** *(신규, 확인 필요)*: Impact 3 / Likelihood 3 / Risk Score 9 — TC-PAGE-UI-040과 영향 수준은 유사하나, Cart 페이지에서 동일하게 생긴 Quantity 컬럼이 입력 가능한 형태로 재사용되는 컴포넌트이므로 Checkout에서 실수로 편집 가능 상태로 남아있을 결함 발생 가능성이 더 높다고 판단함(Likelihood 3).

> 참고: 본 문서에서 산정된 TC 중 P0(Risk Score 16~25)는 없습니다. Feature PRD "각 페이지별 UI"가
> 화면 구성요소의 노출/배치 자체를 다루며, 로그인 성공/결제 등 핵심 트랜잭션 완료 여부를 다루지
> 않기 때문입니다(그런 핵심 기능은 `login-logout.md` 등 별도 Feature TC에서 P0로 다루어짐). 이
> 판단에 동의하시는지, 혹은 특정 TC를 P0로 재산정해야 한다고 보시는지 확인 부탁드립니다.
>
> 2026-08-22 추가: Checkout 페이지 REQ-PAGE-UI-025~031에 대응하는 신규 TC-PAGE-UI-034~041을
> 산정한 결과에서도 가장 높은 Risk Score는 12(TC-PAGE-UI-035, P1)로, P0에 해당하는 TC는 여전히
> 없습니다. 위 판단은 신규 TC 추가 이후에도 그대로 유지됩니다.

## 사용자 확인 필요 사항 (확인 완료 — 2026-08-22)

아래 4개 항목 모두 사용자 리뷰를 통해 답변이 확정되었습니다. 이력 추적을 위해 원래 질문과 확정된
결론을 함께 남깁니다.

1. **Priority 산정 방향**: 위 "참고" 문단과 같이 이 Feature에는 P0가 없는 것으로 산정했습니다. 동의하시는지 확인 부탁드립니다.
   - **결론**: 동의함. 변경 없음.
2. **REQ-PAGE-UI-018 (CATEGORY 아코디언 동작)의 검증 범위**: PRD상 "Home, Products 공통" 동작으로 기술되어 있어, TC-PAGE-UI-023/024를 Home 페이지 기준 1세트로만 작성했습니다. Products 페이지에서도 별도로 동일 TC를 중복 작성하는 것을 원하시면 알려주세요.
   - **결론**: Products 페이지용 TC 추가 요청. 이에 따라 TC-PAGE-UI-032(카테고리 클릭 시 하위 메뉴 펼침), TC-PAGE-UI-033(다른 카테고리 클릭 시 이전 카테고리 닫힘, 단일 오픈)을 TC-023/024와 동일한 검증 관점으로 신규 추가함(Requirement ID는 동일하게 REQ-PAGE-UI-018).
3. **Cart 상품 담긴 상태 Preconditions**: TC-PAGE-UI-018/020/021은 "장바구니에 상품이 1개 이상 담긴 상태"를 사전 조건으로 전제합니다. 실제 상품 담기 동작 자체는 Out of Scope(별도 장바구니 Feature)이므로, 이 사전 조건 설정 방식(Preconditions에만 명시하고 별도 TC로 담기 절차를 기술하지 않음)이 적절한지 확인 부탁드립니다.
   - **결론**: 승인함. 변경 없음.
4. **REQ-PAGE-UI-031 검증 범위**: TC-PAGE-UI-031은 "모든" 카테고리/브랜드를 순회하도록 기술되어 있어 실행 범위가 넓습니다. 전수 확인 대신 표본 확인으로 범위를 축소할지 여부를 확인 부탁드립니다.
   - **결론**: 전수 확인 유지로 결정됨. 현재 작성된 전수 순회 방식 그대로 유지, 변경 없음.

## 신규 추가 TC 확인 필요 사항 (확인 완료 — 2026-08-22)

Feature PRD `page-ui.md`의 Checkout 페이지 범위 확장(REQ-PAGE-UI-025~031, 재승인 완료)에 따라
아래 TC-PAGE-UI-034~041을 신규 추가했습니다. 아래 3개 항목 모두 사용자 리뷰를 통해 답변이
확정되었습니다. 이력 추적을 위해 원래 질문과 확정된 결론을 함께 남깁니다.

5. **신규 TC 034~041의 내용/Priority 산정**: TC-PAGE-UI-034(Address Details 영역 노출),
   035(주소 자동 채움), 036(Review Your Order 표 컬럼 구성), 037(Total Amount 노출), 038(주문
   코멘트 textarea 노출), 039(Place Order 버튼 노출), 040(Address Details read-only),
   041(Review Your Order Quantity read-only)의 Test Scenario/Steps/Expected Result 내용과,
   각각의 Priority(034 P2, 035 P1, 036 P1, 037 P2, 038 P2, 039 P2, 040 P2, 041 P1) 산정 근거에
   동의하시는지 확인 부탁드립니다.
   - **결론**: 동의함. 변경 없음.
6. **REQ-PAGE-UI-031의 TC 분리 방식**: REQ-PAGE-UI-031(Address Details와 Quantity 모두 read-only)을
   검증 목적이 서로 다른 두 요소(주소 정보 read-only / Quantity read-only)로 판단해
   TC-PAGE-UI-040, 041 두 개로 나눠 작성했습니다. 이 분리가 과도하다고 판단되시면 하나의 TC로
   통합할지 여부를 알려주세요.
   - **결론**: 적절함. 분리 유지로 확정, 변경 없음.
7. **TC-PAGE-UI-035 테스트 데이터**: 회원가입 시 입력한 이름/주소 정보와 Checkout에 자동 표시된
   값을 비교하는 방식으로 작성했습니다. 실제 비교에 사용할 계정/주소 정보(민감정보 제외)를
   테스트 수행 시점에 어떻게 준비할지(예: 신규 테스트 계정 생성 vs 기존 계정 재사용) 필요 시
   알려주시면 Preconditions에 더 구체화하겠습니다.
   - **결론**: 기존 테스트 계정 재사용으로 확정. TC-PAGE-UI-035의 Preconditions/Test Steps를
     "기존 테스트 계정 재사용(예: actest1@test.com, 회원가입 시 입력했던 이름/주소 정보를 그대로
     비교 기준으로 사용)" 형태로 구체화함(다른 TC 문서의 테스트 계정 표기 방식과 통일).

신규 TC 034~041에 대한 사용자 확인이 모두 완료되었습니다. 다만 Google Spreadsheet 반영은
사용자의 별도 최종 확인 후 진행합니다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-22 | 최초 작성 (승인완료된 Feature PRD `page-ui.md`의 REQ-PAGE-UI-001~024 기반 TC-PAGE-UI-001~031 초안 작성) | 초안 |
| 2026-08-22 | 사용자 리뷰 피드백 반영 - Products 페이지 아코디언 TC 추가(TC-PAGE-UI-032, 033, REQ-PAGE-UI-018 매핑), 나머지 항목(Priority 산정 방향, Cart Preconditions 방식, TC-031 전수 확인 범위) 승인 확정 | 초안 |
| 2026-08-22 | 사용자 최종 승인 | 승인완료 |
| 2026-08-22 | page-ui Feature PRD의 Checkout 페이지 범위 확장(REQ-PAGE-UI-025~031)에 따른 TC 신규 추가 (TC-PAGE-UI-034~041, Address Details 노출/자동 채움, Review Your Order 표/Total Amount, 주문 코멘트 textarea, Place Order 버튼, Address Details·Quantity read-only). 기존 TC-PAGE-UI-001~033은 변경하지 않음. 신규 TC는 사용자 확인 전이며 문서 상태는 승인완료 유지 | 승인완료 |
| 2026-08-22 | 신규 추가 TC-PAGE-UI-034~041 사용자 최종 확인 완료(내용/Priority 산정 동의, REQ-PAGE-UI-031 TC 분리 방식 유지 확정) 및 TC-PAGE-UI-035 테스트 데이터 구체화(기존 테스트 계정 재사용, 예: actest1@test.com 형태로 Preconditions/Test Steps 수정). Google Spreadsheet 반영은 미실시 | 승인완료 |
