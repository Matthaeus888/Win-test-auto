---
문서유형: Feature PRD
상태: 승인완료   # 초안 | 승인완료
관련 Project PRD: project-prd.md
최초 작성일: 2026-08-21
최근 변경일: 2026-08-22
승인일: 2026-08-21 (최초), 2026-08-21 (재승인), 2026-08-22 (재승인)
---

# Feature PRD - 각 페이지별 UI

## 1. 개요

automationexercise.com의 Home, Products, Cart, Signup/Login, Checkout 5개 페이지에 노출되는
화면 구성요소(레이아웃, 섹션, 표시 정보 등) 자체를 다룬다. 각 구성요소를 클릭/조작했을 때의
상세 동작(로그인/회원가입 폼 입력 검증, 계정삭제, 상단 네비게이션 자체 동작, 장바구니 담기/
수량 변경/삭제 동작, 주문/결제 처리 등)은 이 문서의 범위가 아니며, 해당 동작을 다루는 다른
Feature PRD 또는 "장바구니" Feature PRD(`cart.md`)를 참조한다.

**(2026-08-22 범위 확장)** 최초 작성 시에는 Checkout 페이지가 범위에 포함되지 않았으나,
"장바구니" Feature TC 작성 중 `/checkout` 페이지의 화면 구성요소 노출 여부를 확인하는 TC가
필요해졌고, 이는 성격상 cart의 "동작" 검증이 아니라 "화면 구성요소 존재 여부" 검증이라 본
문서 범위에 속해야 한다는 판단에 따라 사용자 요청으로 Checkout 페이지가 추가되었다(4.1
Checkout 페이지 절, 7. 비고 참조). Checkout 페이지에서도 주문/결제 "동작" 자체(Place Order
클릭 이후 처리 등)는 여전히 본 문서 범위가 아니며, 진입 시 노출되는 정적 화면 구성요소만
다룬다.

## 2. 관련 Project PRD 참조

- `/docs/prd/project-prd.md` (상태: 승인완료)
- Project PRD "5. 대상 Feature 목록" 및 "6. In Scope" 중 "각 페이지별 UI (Home, Products,
Cart, Signup/Login)" 항목에 해당
- Project PRD "8. 기타 제약사항 / 참고사항"의 "무작위 모달형 광고 노출 — 광고 관련 동작은
검증 대상에서 제외" 원칙을 그대로 따른다.
- **참고**: 2026-08-22 본 문서 범위에 Checkout 페이지가 추가되었으며, Project PRD "5. 대상
Feature 목록" / "6. In Scope"의 "각 페이지별 UI" 항목에도 Checkout이 함께 반영되어
"(Home, Products, Cart, Signup/Login, Checkout)"로 두 문서 간 표기가 일치한다(7. 비고 참조).
Project PRD "7. Out of Scope"의 "결제 기능"과는 별개로, 본 문서가 다루는 Checkout 페이지
범위는 어디까지나 정적 화면 구성요소 노출이며 결제/주문 처리 동작은 포함하지 않는다.

**관련 Feature PRD (중복 기술하지 않고 참조만 함)**

- `/docs/prd/feature/login-logout.md`
  - REQ-LOGIN-LOGOUT-001: 로그인 페이지의 "Login to your account" 영역과 "New User Signup!"
  영역이 "OR" 아이콘으로 구분되어 함께 노출되는 레이아웃 (본 문서에서는 재기술하지 않음)
- `/docs/prd/feature/signup-delete-account.md`
  - 회원가입 상세 정보 입력 페이지(`/signup`)의 필드 구성 등은 본 문서 범위(로그인 페이지
  자체)가 아니므로 다루지 않음
- `/docs/prd/feature/top-navigation.md`
  - 상단 네비게이션 메뉴 자체의 구성/동작(이동 URL, 활성 표시 등)은 본 문서에서 다루지 않음



## 3. 사용자 조작 시나리오

1. Home 페이지(`/`)에 진입해 최상단부터 하단 푸터까지 순서대로 화면 구성을 확인한다
  (배너/캐러셀 → CATEGORY → BRANDS → FEATURES ITEMS → RECOMMENDED ITEMS → SUBSCRIPTION →
   푸터).
2. Products 페이지(`/products`)로 이동해 동일한 방식으로 화면 구성을 확인한다
  (상단 배너 → 검색창 → 좌측 사이드바(CATEGORY/BRANDS) → ALL PRODUCTS → 푸터).
3. Cart 페이지(`/view_cart`)를 상품이 담기지 않은 상태와 담긴 상태 각각에서 확인한다.
4. Signup/Login 페이지(`/login`)의 전체 레이아웃을 확인한다(폼 자체의 입력 동작은 제외).
5. 로그인 상태에서 장바구니에 상품을 담고 "Proceed To Checkout" 버튼을 통해 `/checkout`
  페이지로 진입해 전체 레이아웃을 확인한다(Address Details → Review Your Order → 코멘트
  입력 영역 → Place Order 버튼 순서, 주문 완료/결제 자체 동작은 제외).
6. 각 페이지에서 관찰되는 요소 중 사이트 자체 UI가 아닌 것으로 판단되는 요소(광고 배너,
  브라우저 확장 프로그램으로 추정되는 오버레이 등)를 구분해 별도로 표시한다.



## 4. Requirements



### 4.1 확인된 요구사항

**Home 페이지 (**`/`**)**

- **REQ-PAGE-UI-001**: 최상단에 배너/캐러셀이 노출되며, 좌우 화살표(이전/다음)와 하단
점(dot) 인디케이터 3개가 함께 표시된다. 현재 슬라이드에 해당하는 dot은 주황색으로
표시된다. 약 3~4초 간격으로 자동 전환(폴링)되며, 좌우 화살표 클릭을 통한 수동 전환도
가능하다.
- **REQ-PAGE-UI-002**: "CATEGORY" 섹션에 WOMEN/MEN/KIDS 3개 카테고리가 아코디언(+ 아이콘)
형태로 노출된다.
- **REQ-PAGE-UI-003**: "BRANDS" 섹션에 브랜드명과 괄호 안 상품 개수가 함께 노출된다
(POLO(6), H&M(5), MADAME(5), MAST & HARBOUR(3), BABYHUG(4), ALLEN SOLLY JUNIOR(3),
KOOKIE KIDS(3), BIBA(5)).
- **REQ-PAGE-UI-004**: "FEATURES ITEMS" 섹션은 한 행에 3개씩 배치되는 상품 카드 그리드
형태이며, 각 카드에 상품 이미지, 가격(Rs. 단위), 상품명, "Add to cart" 버튼, "View
Product" 링크가 노출된다.
- **REQ-PAGE-UI-005**: "FEATURES ITEMS" 하단에 별도로 "RECOMMENDED ITEMS" 섹션이 존재하며,
좌우 화살표가 있는 캐러셀 형태로 상품이 노출된다(FEATURES ITEMS의 그리드 형태와 구분됨).
약 4~5초 간격으로 자동 전환되며, 좌우 화살표 클릭을 통한 수동 전환도 가능하다.
- **REQ-PAGE-UI-006**: 페이지 최하단에 "SUBSCRIPTION" 섹션(이메일 입력창, 제출 버튼,
안내 문구)이 노출된다.
- **REQ-PAGE-UI-007**: "SUBSCRIPTION" 섹션 아래 "Copyright © 2021 All rights reserved"
문구가 포함된 푸터가 노출된다.

**Products 페이지 (**`/products`**)**

- **REQ-PAGE-UI-008**: 최상단에 "SPECIAL OFFER BIG SALE UP TO 50% OFF" 배너 이미지가
노출된다(Home 페이지에는 없는, Products 페이지 고유 요소).
- **REQ-PAGE-UI-009**: 상단 배너 아래 "Search Product" placeholder를 가진 검색창과
돋보기 아이콘 버튼이 나란히 배치되어 노출된다.
- **REQ-PAGE-UI-010**: 좌측 사이드바에 "CATEGORY"(Women/Men/Kids), "BRANDS" 섹션이
Home 페이지의 REQ-PAGE-UI-002, REQ-PAGE-UI-003과 동일한 구성으로 노출된다.
- **REQ-PAGE-UI-011**: "ALL PRODUCTS" 섹션은 Home 페이지의 "FEATURES ITEMS"(REQ-PAGE-UI-004)와
동일한 카드 그리드 구조(이미지/가격/상품명/Add to cart/View Product)로 노출된다.
- **REQ-PAGE-UI-012**: 페이지 하단에 Home 페이지와 동일한 "SUBSCRIPTION" 섹션 및 Copyright
푸터(REQ-PAGE-UI-006, REQ-PAGE-UI-007)가 동일하게 노출된다.

**Cart 페이지 (**`/view_cart`**)**

- **REQ-PAGE-UI-013**: 상단 네비게이션 하단에 "Home > Shopping Cart" 형태의 브레드크럼이
노출된다. 상품이 담기지 않은 상태/담긴 상태 모두 동일하게 노출된다(다른 페이지에서는
관찰되지 않은 Cart 페이지 고유 요소).
- **REQ-PAGE-UI-014**: 장바구니가 비어있는 상태에서는 "Cart is empty! Click here to buy
products." 안내 문구와 "here" 링크가 노출된다.
- **REQ-PAGE-UI-015**: 장바구니에 상품이 담긴 상태에서는 화면 우측 상단에 "Proceed To
Checkout" 버튼(주황색)이 노출된다.
- **REQ-PAGE-UI-016**: 장바구니에 상품이 담긴 상태에서 상품 목록 표가 노출되며, 컬럼
구성은 "Item"(이미지), "Description"(상품명 + 카테고리 경로, 예: "Blue Top / Women >
Tops"), "Price", "Quantity"(숫자 값이 표시되는 입력란 형태), "Total"(가격 x 수량)이다.
각 행 맨 끝에는 삭제(x) 아이콘 버튼이 존재한다. (수량 입력란 값 변경 시 Total 재계산 등
실제 동작은 본 문서 범위가 아니며, 화면 구성요소로서 입력란/삭제 버튼의 "존재 여부"만
다룬다.)

**Signup/Login 페이지 (**`/login`**)**

- **REQ-PAGE-UI-017**: 로그인 폼/회원가입 폼 레이아웃 자체는 `login-logout.md`의
REQ-LOGIN-LOGOUT-001에 이미 기술되어 있어 본 문서에서는 재기술하지 않는다. 다만 이
페이지에는 Products 페이지의 "SPECIAL OFFER" 배너(REQ-PAGE-UI-008)와 같은 별도 배너
이미지가 노출되지 않는다는 점을 확인했다.

**CATEGORY / BRANDS 클릭 동작 (Home, Products 공통)**

- **REQ-PAGE-UI-018**: "CATEGORY" 아코디언은 WOMEN/MEN/KIDS 중 하나를 클릭하면 하위 메뉴가
펼쳐진다(예: WOMEN → DRESS, TOPS & SHIRTS, SAREE 등 / MEN → TSHIRTS, JEANS 등). 한 번에
하나의 카테고리만 펼쳐지며, 다른 카테고리를 클릭하면 이전에 열려 있던 카테고리는 닫힌다.
- **REQ-PAGE-UI-019**: CATEGORY 하위 메뉴(예: MEN > JEANS) 클릭 시 해당 카테고리 상품 목록
페이지(`/category_products/{id}`, 예: `/category_products/6`)로 이동하며, 이동한 페이지에는
"Products > Men > Jeans" 형태의 브레드크럼, "Men - Jeans PRODUCTS" 제목, 해당 카테고리
상품 그리드(REQ-PAGE-UI-004/011과 동일한 카드 구조: 이미지/가격/상품명/Add to cart/View
Product)가 노출된다.
- **REQ-PAGE-UI-020**: "BRANDS" 목록의 각 브랜드명 클릭 시 해당 브랜드 상품 목록 페이지
(`/brand_products/{브랜드명}`, 예: `/brand_products/H%26M`)로 이동하며, "Products > H&M"
형태의 브레드크럼, "BRAND - H&M PRODUCTS" 제목, 해당 브랜드 상품 그리드(동일 카드 구조)가
노출된다.

**FEATURES ITEMS 전체 상품 개수**

- **REQ-PAGE-UI-021**: Home 페이지 "FEATURES ITEMS" 섹션에는 전체 34개 상품이 노출되며,
별도의 페이지네이션 기능은 없고 스크롤을 통해 이어서 확인하는 방식이다.

**CATEGORY / BRANDS 필터링 정확성**

- **REQ-PAGE-UI-022**: "BRANDS" 섹션에 표시된 브랜드별 괄호 숫자(REQ-PAGE-UI-003 참조, 예:
POLO(6))는 해당 브랜드 상품 목록 페이지(`/brand_products/{브랜드명}`)에서 실제로 노출되는
상품 개수와 일치한다.
- **REQ-PAGE-UI-023**: CATEGORY/BRANDS 클릭 시 이동하는 상품 목록 페이지
(`/category_products/{id}`, `/brand_products/{브랜드명}`)에는 실제로 해당 카테고리/브랜드에
속하는 상품만 필터링되어 노출된다(무관한 상품이 섞여 노출되지 않음을 확인).
- **REQ-PAGE-UI-024**: 사용자가 확인한 범위 내에서 상품이 0개로 노출되는 카테고리/브랜드는
없었다(모든 카테고리/브랜드에 최소 1개 이상의 상품이 존재).



**Checkout 페이지 (**`/checkout`**)**

> 아래 REQ-PAGE-UI-025~031은 최초 "장바구니" Feature TC 작성 과정에서 관찰된 내용을 근거로
> 작성된 Draft였으나, 사용자가 실제 `/checkout` 페이지에서 직접 확인하여 아래 내용이
> 정확함을 확정했다(2026-08-22, 7. 비고 참조).

- **REQ-PAGE-UI-025**: 로그인 상태에서 장바구니에 상품이 담긴 채로 `/checkout` 페이지에
진입하면 "Address Details" 영역이 노출되며, 그 안에 "Your Delivery Address"와 "Your
Billing Address"가 함께 배치되어 노출된다.
- **REQ-PAGE-UI-026**: "Your Delivery Address"와 "Your Billing Address"에는 회원가입 시
입력한 이름/주소 정보가 자동으로 채워져 표시된다.
- **REQ-PAGE-UI-027**: Address Details 영역 아래에 "Review Your Order" 영역이 노출되며,
Cart 페이지(REQ-PAGE-UI-016)와 동일한 Item/Description/Price/Quantity/Total 컬럼 구성의
상품 목록 표가 표시된다.
- **REQ-PAGE-UI-028**: "Review Your Order" 표 하단에 Total Amount(합계 금액)가 노출된다.
- **REQ-PAGE-UI-029**: "Review Your Order" 영역 아래에 주문 관련 코멘트를 입력할 수 있는
텍스트 영역(textarea)이 노출된다.
- **REQ-PAGE-UI-030**: 페이지 하단에 "Place Order" 버튼이 노출된다.
- **REQ-PAGE-UI-031**: Address Details의 배송지/청구지 정보와 "Review Your Order" 표의
Quantity 값은 모두 수정/편집이 불가능한 표시 전용(read-only) 형태로 노출된다. 이는 Cart
페이지의 Quantity가 입력란 형태로 노출되는 것(REQ-PAGE-UI-016)과 구분되는 Checkout 페이지
고유 특성이다.

### 4.2 미확인 / 추가 확인 필요 항목

- 현재 없음. Checkout 페이지 REQ-PAGE-UI-025~031을 포함해 이전에 제기되었던 미확인 항목은
모두 사용자 확인이 완료되었다(4.1 Checkout 절 안내 문구, 7. 비고 참조).



## 5. Feature 단위 In Scope / Out of Scope

**In Scope**

- Home 페이지: 배너/캐러셀, CATEGORY, BRANDS, FEATURES ITEMS, RECOMMENDED ITEMS,
SUBSCRIPTION, 푸터 등 화면 구성요소의 노출 여부 및 구성
- Products 페이지: 상단 배너, 검색창, 좌측 사이드바(카테고리/브랜드), ALL PRODUCTS
그리드, 푸터 등 화면 구성요소의 노출 여부 및 구성
- Cart 페이지: 브레드크럼, 빈 카트 안내 문구, 상품 테이블 구성요소(수량 입력란/삭제
버튼 등의 "존재 여부"), Proceed To Checkout 버튼의 노출 여부
- Signup/Login 페이지: 페이지 레이아웃 배치 확인 수준 (폼 자체의 상세 동작은 `login-logout.md` 참조)
- Checkout 페이지: Address Details(배송지/청구지), Review Your Order(상품 목록 표, Total
Amount), 주문 코멘트 입력 영역, Place Order 버튼 등 화면 구성요소의 노출 여부 및 배치,
Address Details/Quantity의 표시 전용(read-only) 여부 (REQ-PAGE-UI-025~031, 사용자가 실제
`/checkout` 페이지에서 직접 확인해 정확함을 확정 — 7. 비고 참조)
- CATEGORY/BRANDS 클릭 시 이동한 상품 목록 페이지에서의 실제 필터링 동작: 브랜드별 표시
개수와 실제 노출 개수 일치 여부, 필터링 정확성(해당 카테고리/브랜드 상품만 노출되는지),
상품이 0개로 노출되는 카테고리/브랜드 존재 여부 (REQ-PAGE-UI-022~024, 7. 비고 참조)

**Out of Scope**

- Cart 페이지의 상품 담기, 수량 변경, 삭제 등 "동작" 자체 — 별도 "장바구니" Feature PRD
범위 (사용자 확정 사항)
- Checkout 페이지의 주문 완료/결제 처리 등 "동작" 자체(Place Order 클릭 이후 처리, 결제
수단 관련 화면 등) — Project PRD "7. Out of Scope"의 "결제 기능"에 해당하며 본 문서는
Checkout 페이지 진입 시 노출되는 정적 화면 구성요소만 다룬다
- 로그인/회원가입 폼의 입력 검증, 에러 케이스, 세션 유지 등 상세 동작 —
`login-logout.md`, `signup-delete-account.md` 범위
- 상단 네비게이션 자체의 동작(이동 URL, 활성 표시 등) — `top-navigation.md` 범위
- 광고 배너 및 브라우저 확장 프로그램으로 추정되는 오버레이 요소(파란 뱃지형 문구 등) —
사이트 고유 UI가 아닌 것으로 판단되어 검증 대상에서 완전히 제외 (Project PRD "기타
제약사항"의 광고 제외 원칙과 일치)
- Project PRD 대상 Feature 목록에 없는 그 밖의 페이지(예: 상품 상세 페이지는 "상품 상세"
Feature PRD 범위이며 본 문서 범위가 아님). Checkout 페이지는 2026-08-22 사용자 요청으로
본 문서 범위에 추가되었으나(위 In Scope 항목 참조), Project PRD "5. 대상 Feature 목록" /
"6. In Scope"의 "각 페이지별 UI" 항목 표기에는 아직 Checkout이 반영되지 않은 상태이다
(2. 관련 Project PRD 참조, 7. 비고 참조)
- Products 페이지 "Search Product" 검색창의 검색 동작 자체(키워드 검색 결과, 검색 결과
없음 케이스, 빈 검색어 케이스 등) — Project PRD 대상 Feature 목록의 "상품 검색" Feature PRD
(`/docs/prd/feature/product-search.md`) 범위로 판단(사용자 확정 사항). CATEGORY/BRANDS
클릭 필터링 관련 내용은 반대로 "상품 검색" Feature PRD가 아닌 본 문서 범위로 재조정되어
REQ-PAGE-UI-022~024로 반영되었다(7. 비고 참조).



## 6. 예외 / 에러 케이스

- Cart 페이지에 상품이 없을 때 "Cart is empty! Click here to buy products." 안내 문구가
노출되는 빈 상태(empty state) UI (REQ-PAGE-UI-014)



## 7. 비고

- Home, Products 페이지 모두에서 좌우 사이드/인라인 형태의 광고 배너("고려기프트",
"MOSNIER", "maplestory WORLDS", "inflearn", "Adobe Creative Cloud" 등)가 관찰되었으나,
이는 Project PRD "8. 기타 제약사항"의 광고 제외 원칙에 따라 Requirements에 포함하지
않았다.
- Home, Products 페이지의 상품명 인근에 파란색 뱃지 형태로 노출되는 "Quality Control &
Tracking", "Development Tools" 등의 문구는 사이트 고유 텍스트("Tshirt", "Dress" 등)에
덧씌워지는 패턴으로 관찰되어, automationexercise.com 자체 UI가 아니라 브라우저 확장
프로그램/광고 네트워크가 주입한 오버레이 요소로 추정된다. 사이트 UI로 보지 않아
Requirements에서 완전히 제외했다.
- Cart 페이지의 수량 입력란과 삭제 버튼은 이번 문서에서 "존재 여부"만 구성요소로 다루며,
값 변경/삭제 클릭 시 실제 동작(Total 재계산, 삭제 처리 등)에 대한 검증은 사용자 확정에
따라 별도 "장바구니" Feature PRD의 범위로 넘긴다.
- Products 페이지의 CATEGORY/BRANDS 섹션은 Home 페이지와 동일한 구성으로 관찰되어,
중복 기술 대신 REQ-PAGE-UI-002, 003을 참조하는 형태로 기술했다.
- Home 페이지 배너/캐러셀(REQ-PAGE-UI-001)과 RECOMMENDED ITEMS 캐러셀(REQ-PAGE-UI-005)의
자동 전환 여부는 최초 작성 시 4.2 미확인 항목이었으나, 이후 사용자가 직접 확인해 각각
약 3~4초, 약 4~5초 간격의 자동 전환과 좌우 화살표 클릭을 통한 수동 전환이 모두
가능함을 확정했다. 이에 따라 해당 내용은 4.2에서 제거하고 각 Requirement 본문에
반영했다.
- CATEGORY 아코디언 클릭 시 하위 메뉴 구성/동작(REQ-PAGE-UI-018)과 FEATURES ITEMS 전체
상품 개수/페이지네이션 여부(REQ-PAGE-UI-021)도 4.2 미확인 항목이었으나, 사용자가 직접
확인해 확정되었다.
- CATEGORY/BRANDS 클릭 시 필터링된 상품 목록 페이지(`/category_products/{id}`,
`/brand_products/{브랜드명}`)로 이동한다는 사실 자체(REQ-PAGE-UI-019, 020)는 "각 페이지별
UI" 구성요소 확인 수준으로 판단해 본 문서에 포함했다. 반면 그 이후 페이지에서의 정확한
필터링 로직, 그리고 Products 페이지 검색창(Search Product)의 실제 검색 동작은 Project
PRD의 "상품 검색" Feature 범위로 판단해 Out of Scope로 분류했다. 이 경계 판단은 아직
작성되지 않은 "상품 검색" Feature PRD와의 관계를 고려한 것으로, 해당 문서를 작성하는
시점에 이 경계가 적절한지 다시 검토가 필요할 수 있다.
- **CATEGORY/BRANDS 필터링 로직 범위 재조정 (2026-08-21)**: "상품 검색" Feature PRD
(`product-search.md`) 작성 과정에서 사용자가 해당 Feature의 범위를 "Products 페이지
검색창(키워드 검색)"으로만 한정하기로 확정했다. 이에 따라 본 문서의 5. Out of Scope에
있던 "CATEGORY/BRANDS 클릭 후 이동한 페이지에서의 실제 필터링 로직" 항목은 삭제하고,
대신 사용자가 직접 확인한 필터링 관련 사실(브랜드 표시 개수와 실제 노출 개수 일치,
필터링 정확성, 0개 노출 카테고리/브랜드 부재)을 REQ-PAGE-UI-022~024로 신규 반영해
In Scope로 이동했다. 검색창의 검색 동작 자체는 그대로 `product-search.md` 범위로
유지된다. 본 문서는 이미 승인완료 상태였으므로 이번 변경은 재승인 대상이며, 재승인은
사용자 본인의 직접 확인을 거쳐 별도로 처리된다.
- 이번 변경 작업 중 frontmatter(문서 상단 메타데이터) 구분자(`---`)가 누락되고 "문서유형"
앞에 의도치 않은 마크다운 heading 표기(`## `)가 붙어 있는 형식 손상이 발견되어, 내용은
그대로 두고 원래의 YAML frontmatter 형식(여는 `---` / 키:값 목록 / 닫는 `---`)으로 복구했다.
- **Checkout 페이지 범위 확장 (2026-08-22)**: "장바구니" Feature TC 작성 중 `/checkout`
페이지의 화면 구성요소 노출 여부를 확인하는 TC(TC-CART-012)가 필요해졌으나, 이는 cart의
"동작" 검증이 아닌 "화면 구성요소 존재 여부" 검증이라 본 문서(page-ui.md) 범위에 속해야
한다고 판단되어, 사용자 요청에 따라 Checkout 페이지를 본 문서 범위에 추가했다. 추가된
REQ-PAGE-UI-025~031(Address Details, Review Your Order, 주문 코멘트 입력 영역, Place
Order 버튼, 표시 전용 필드 여부)은 최초에는 cart TC 작성 중 관찰된 내용을 근거로 작성한
Draft였으나, 이후 사용자가 실제 `/checkout` 페이지에서 직접 확인해 정확함을 확정했다
(4.1 Checkout 페이지 절 참조). 아울러 Project PRD "5. 대상 Feature 목록" / "6. In Scope"의
"각 페이지별 UI" 표기에도 Checkout이 함께 반영되었다(2. 관련 Project PRD 참조 절 참조).
본 문서는 이미 승인완료 상태였으므로 이번 변경은 재승인 대상이다.



## 변경 이력


| 날짜         | 변경 사유                                                                                                                                                                                                   | 상태   |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| 2026-08-21 | 최초 작성 (Draft) — 사용자 실측(스크린샷) 결과 반영                                                                                                                                                                      | 초안   |
| 2026-08-21 | REQ-PAGE-UI-001, 005에 배너/캐러셀 자동 전환 주기(3~4초, 4~5초) 및 수동 전환(화살표 클릭) 내용 반영, 4.2에서 해당 미확인 항목 제거                                                                                                           | 초안   |
| 2026-08-21 | REQ-PAGE-UI-018~021 추가(CATEGORY 아코디언 동작, CATEGORY/BRANDS 클릭 시 이동 페이지, FEATURES ITEMS 전체 개수), 4.2 미확인 항목 모두 해소("현재 없음"으로 정리), Out of Scope/비고에 CATEGORY·BRANDS 필터링 로직 및 검색창 동작의 "상품 검색" Feature 위임 경계 기록 | 초안   |
| 2026-08-21 | 사용자 최종 승인 (CATEGORY/BRANDS 범위 경계 확인 포함)                                                                                                                                                                 | 승인완료 |
| 2026-08-21 | CATEGORY/BRANDS 필터링 로직 범위를 "상품 검색" Feature PRD에서 본 문서로 재조정, REQ-PAGE-UI-022~024 신규 추가(브랜드 표시 개수 일치, 필터링 정확성, 0개 노출 카테고리/브랜드 부재 확인), 5. Out of Scope 항목 수정, frontmatter 형식 손상 복구, 자동 전환 주기 물결표 중복 오타 수정 | 승인완료 (재승인 대기) |
| 2026-08-21 | 사용자 재승인 | 승인완료 |
| 2026-08-22 | cart Feature TC 작성 중 `/checkout` 페이지의 화면 구성요소 검증(TC-CART-012)이 본 문서 범위에 속해야 함이 확인되어, 사용자 요청에 따라 Checkout 페이지를 범위에 추가. REQ-PAGE-UI-025~031 신규 추가(Address Details, Review Your Order, 코멘트 입력 영역, Place Order 버튼, 표시 전용 필드 여부 — cart TC 작성 중 관찰 내용 기반 Draft, 사용자 재확인 필요), 1/2/3/5장에 Checkout 페이지 반영, Project PRD 표기 불일치 안내 추가. 미확인/재검증 필요 항목 존재 상태로 재승인 대기 | 승인완료 (재승인 대기) |
| 2026-08-22 | 사용자가 실제 `/checkout` 페이지에서 REQ-PAGE-UI-025~031 내용을 직접 확인해 정확함을 확정(4.1 Checkout 절, 4.2 갱신). frontmatter 상태 필드가 변경 이력과 불일치("승인완료"로만 표기)하던 것을 "승인완료 (재승인 대기)"로 수정 | 승인완료 (재승인 대기) |
| 2026-08-22 | 5. In Scope, 7. 비고 섹션에 남아있던 "REQ-PAGE-UI-025~031, 사용자 재확인 전 Draft 상태" 등 예전 문구를 4.1절과 일관되게 "사용자가 실제 확인해 정확함을 확정"으로 정리 | 승인완료 (재승인 대기) |
| 2026-08-22 | 사용자 최종 재승인 | 승인완료 |
| 2026-08-22 | Project PRD에 Checkout이 이미 반영되어 더 이상 유효하지 않은 불일치 안내 문구 정리 | 승인완료 |


