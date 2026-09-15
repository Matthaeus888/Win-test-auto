---
문서유형: Feature PRD
상태: 승인완료   # 초안 | 승인완료
관련 Project PRD: project-prd.md
최초 작성일: 2026-08-21
최근 변경일: 2026-08-21
승인일: 2026-08-21
---

# Feature PRD - 상품 상세

## 1. 개요

automationexercise.com의 상품 상세 페이지(`/product_details/{id}`)를 다룬다. 상세 페이지 자체의
URL 패턴 및 상품 ID 파라미터 처리(존재/미존재 케이스 포함), 화면 구성요소(이미지, 상품명,
카테고리, 별점, 가격, Quantity 입력 UI, Add to cart 버튼, Availability/Condition/Brand 정보,
리뷰 작성 섹션 등)와 전체 레이아웃 구조, 그리고 상세 페이지에서 Quantity를 지정해 "Add to cart"를
클릭했을 때의 실제 반응(정상 값/비정상 값 각각)을 다룬다.

정상적인 수량으로 장바구니에 담았을 때 장바구니 페이지에 실제로 어떻게 반영되는지(수량 표시,
동일 상품 누적 등)의 "결과"는 `cart.md`의 범위이며(REQ-CART-004 참조), 본 문서에서는 재기술하지
않는다. 다만 Quantity 입력란 자체의 화면 구성(스피너 버튼 등)과, 비정상 입력값(문자, 음수, 0)으로
"Add to cart"를 클릭했을 때의 반응은 상세 페이지 고유의 관찰 사항이자 이번에 새로 발견된 결함
의심 사항이므로 본 문서에서 다룬다. 상세 페이지의 "Add to cart" 클릭 시 노출되는 확인 모달은
리스트 페이지(Home/Products)의 모달과 동일함을 확인한 수준에서만 언급하며, 모달 자체의 상세
구성은 `cart.md`(REQ-CART-001)를 참조한다.

## 2. 관련 Project PRD 참조

- `/docs/prd/project-prd.md` (상태: 승인완료)
- Project PRD "5. 대상 Feature 목록" 및 "6. In Scope"의 "상품 상세" 항목에 해당
- Project PRD "8. 기타 제약사항 / 참고사항"의 "무작위 모달형 광고 노출 — 광고 관련 동작은 검증
  대상에서 제외" 원칙을 그대로 따른다.

**관련 Feature PRD (중복 기술하지 않고 참조만 함)**

- `/docs/prd/feature/cart.md` (승인완료)
  - REQ-CART-001: "Add to cart" 클릭 시 노출되는 담기 확인 모달의 상세 구성(아이콘, 문구,
    "View Cart"/"Continue Shopping" 버튼 동작). 상세 페이지에서도 동일한 모달이 노출됨을
    확인했으며(4.1 참조), 모달 자체의 구성은 재기술하지 않는다.
  - REQ-CART-004: 상품 상세 페이지에서는 담을 개수를 직접 지정해서 장바구니에 담을 수 있다는
    사실. 정상 수량으로 담았을 때 장바구니에 실제로 반영되는 결과(수량 표시, 누적 등)는 본
    문서에서 다루지 않는다.
- `/docs/prd/feature/page-ui.md` (승인완료)
  - REQ-PAGE-UI-004/011: Home/Products 리스트 페이지 상품 카드의 "View Product" 링크를 통해
    상세 페이지로 이동한다는 구조. 리스트 페이지 카드 자체의 UI는 본 문서에서 다루지 않는다.
- `/docs/prd/feature/product-search.md` (승인완료)
  - REQ-PRODUCT-SEARCH-002: 검색 결과 카드의 "View Product" 링크를 통해서도 상세 페이지로
    이동한다는 구조. 검색 결과 화면 자체는 본 문서에서 다루지 않는다.

## 3. 사용자 조작 시나리오

1. Home/Products 등 상품 리스트에서 "View Product" 링크를 클릭해 상세 페이지로 이동하고, 이동한
   URL의 패턴(`/product_details/{id}`)을 확인한다.
2. 존재하는 상품 ID로 상세 페이지에 정상 진입해 화면이 정상적으로 노출되는지 확인한다.
3. 존재하지 않는 상품 ID(예: `/product_details/99`)로 URL에 직접 접근해 화면이 어떻게 노출되는지
   확인한다.
4. 정상 상품 기준으로 상세 페이지 최상단부터 하단까지 순서대로 화면 구성요소(이미지, 뱃지,
   상품명, 카테고리, 별점, 가격, Quantity 입력란, Add to cart 버튼, Availability/Condition/
   Brand 정보, WRITE YOUR REVIEW 섹션)를 확인한다.
5. Quantity 입력란에 기본값 그대로 둔 채 "Add to cart" 버튼을 클릭해 노출되는 모달을 확인한다.
6. Quantity 입력란의 스피너(위/아래 버튼)를 조작해 최솟값/최댓값 제한 여부를 확인한다.
7. Quantity 입력란에 문자만 입력, 숫자+문자 혼합 입력, 음수 입력, 0 입력 각각의 상태에서 "Add to
   cart" 버튼을 클릭해 반응을 확인한다.

## 4. Requirements

### 4.1 확인된 요구사항

**URL 패턴 및 상품 ID 처리**

- **REQ-PRODUCT-DETAIL-001**: 상품 상세 페이지의 URL은
  `https://automationexercise.com/product_details/{id}` 형태이며(예: `/product_details/1`), 마지막
  경로 파라미터가 상품 ID이다. 상품 ID 값 자체에 대한 별도의 형식 검증은 없는 것으로 확인된다.
- **REQ-PRODUCT-DETAIL-002**: 존재하는 상품 ID로 접근하면 상세 페이지가 정상적으로 노출된다.
- **REQ-PRODUCT-DETAIL-003 (결함 의심)**: 존재하지 않는 상품 ID(예: `/product_details/99`)로
  접근해도 별도의 404/에러 페이지 없이 상세 페이지 레이아웃이 그대로 렌더링된다. 다만 이미지
  영역에는 깨진 이미지 아이콘과 "ecommerce website products" alt 텍스트만 노출되고, Category/
  Brand 필드는 값 없이 빈 채로 노출된다. 반면 별점, Quantity 입력란, "Add to cart" 버튼,
  "Availability: In Stock", "Condition: New", "WRITE YOUR REVIEW" 섹션 등 나머지 레이아웃은
  정상 상품과 동일하게 그대로 노출된다. 존재하지 않는 상품 데이터에 대한 별도 처리 없이 페이지
  골격만 그대로 렌더링되는 비정상 동작으로, 결함 의심 사항으로 기록한다.

**화면 구성요소 (정상 상품 기준)**

- **REQ-PRODUCT-DETAIL-004**: 상품 이미지는 단일 이미지로 노출되며, 여러 장의 이미지나 썸네일
  전환 UI는 확인되지 않는다.
- **REQ-PRODUCT-DETAIL-005**: 상품 이미지 좌상단에 빨간색 "NEW" 배지가 노출된다.
- **REQ-PRODUCT-DETAIL-006**: 상품명이 텍스트로 노출된다(예: "Blue Top").
- **REQ-PRODUCT-DETAIL-007**: "Category: Women > Tops" 형태로 카테고리 경로 텍스트가 노출된다.
- **REQ-PRODUCT-DETAIL-008**: 주황색 별 아이콘으로 구성된 별점이 노출된다(예: 4.5개 채워진
  형태). 클릭할 수 없는 정적 표시 요소이다(REQ-PRODUCT-DETAIL-022 참조).
- **REQ-PRODUCT-DETAIL-009**: 가격이 Rs. 단위로 노출된다.
- **REQ-PRODUCT-DETAIL-010**: Quantity 입력란은 숫자를 직접 입력할 수 있고, 입력란 우측에
  위/아래 스피너 버튼이 함께 노출되는 네이티브 number input 형태이며, "Add to cart" 버튼 바로
  옆에 위치한다.
- **REQ-PRODUCT-DETAIL-011**: 주황색 "Add to cart" 버튼이 Quantity 입력란 옆에 노출된다.
- **REQ-PRODUCT-DETAIL-012**: "Availability: In Stock", "Condition: New", "Brand: {브랜드명}"
  (브랜드명은 링크 형태) 텍스트 정보가 노출된다.
- **REQ-PRODUCT-DETAIL-013**: 사이즈/색상을 선택하는 UI는 존재하지 않는다.
- **REQ-PRODUCT-DETAIL-014**: 하단에 "WRITE YOUR REVIEW" 섹션이 노출되며, Your Name 입력란,
  Email Address 입력란, "Add Review Here!" placeholder를 가진 텍스트 영역, Submit 버튼으로
  구성된다.
- **REQ-PRODUCT-DETAIL-015**: 페이지는 "Description" 등 별도 탭으로 전환되는 구조가 아니라,
  상품 이미지·카테고리·별점·가격·Quantity/Add to cart·Availability/Condition/Brand 정보·WRITE
  YOUR REVIEW 섹션이 순서대로 한 화면에 이어서 노출되는 단일 스크롤 레이아웃이다.

**Add to cart 동작 (상품 상세 페이지)**

- **REQ-PRODUCT-DETAIL-016**: 정상적인 수량 값을 지정한 상태에서 "Add to cart" 버튼을 클릭하면
  Home/Products 리스트 페이지에서와 동일한 확인 모달이 노출된다(초록 체크 아이콘, "Added!",
  "Your product has been added to cart.", "View Cart" 링크, 초록색 "Continue Shopping" 버튼 —
  `cart.md` REQ-CART-001과 동일, 모달 자체 구성은 재기술하지 않음).

**Quantity 입력 동작 및 결함 의심 사항**

- **REQ-PRODUCT-DETAIL-017**: Quantity 입력란의 스피너 버튼은 1 미만으로 내려가지 않는다(스피너
  조작 기준 최솟값은 1).
- **REQ-PRODUCT-DETAIL-018**: Quantity 입력란의 스피너 버튼에는 최댓값 제한이 없다.
- **REQ-PRODUCT-DETAIL-019 (결함 의심)**: Quantity 입력란에 문자만 입력한 상태에서 "Add to
  cart" 버튼을 클릭하면 장바구니에 담기지 않고 페이지도 그대로 유지되며, 별도의 에러 안내
  문구도 노출되지 않는다(조용히 실패). 숫자와 문자를 혼합해 입력한 경우에도 동일한 현상이
  나타난다.
- **REQ-PRODUCT-DETAIL-020 (결함 의심)**: 이미 동일 상품이 일정 수량 담겨 있는 상태에서
  Quantity 입력란에 음수를 입력하고 "Add to cart" 버튼을 클릭하면, 장바구니에 새로 담기는 것이
  아니라 기존에 담겨 있던 해당 상품의 수량에서 입력한 음수의 절댓값만큼 차감된다(예: 기존
  5개가 담긴 상태에서 -2를 입력해 클릭하면 3개로 감소).
- **REQ-PRODUCT-DETAIL-021 (결함 의심)**: Quantity 입력란에 0을 입력한 상태에서 "Add to cart"
  버튼을 클릭하면, 담기지 않거나 최소 1개로 처리되는 것이 아니라 장바구니에 수량 0으로 표기된
  채 그대로 담긴다.

**별점 및 리뷰 작성 (WRITE YOUR REVIEW)**

- **REQ-PRODUCT-DETAIL-022**: 별점(rating) 아이콘은 클릭할 수 없는 정적 표시 요소이다.
- **REQ-PRODUCT-DETAIL-023**: "WRITE YOUR REVIEW" 섹션의 Your Name, Email Address, 리뷰 내용
  (Add Review Here!) 3개 필드는 모두 필수값이다. 하나라도 비운 채 Submit 버튼을 클릭하면
  `login-logout.md`의 REQ-LOGIN-LOGOUT-007/008과 동일한 방식으로 브라우저 자체(HTML5 native)
  필수 입력 검증 팝업("이 입력란을 작성하세요.")이 비어있는 필드를 순서대로 가리키며 노출되고,
  폼 제출이 차단된다.
- **REQ-PRODUCT-DETAIL-024**: Email Address 필드는 이메일 형식에 대한 브라우저 자체(HTML5
  native) 유효성 검사도 동작한다. `login-logout.md`의 REQ-LOGIN-LOGOUT-006과 동일한 패턴으로,
  사이트 자체의 커스텀 검증이 아니라 `type="email"` input의 브라우저 기본 동작으로 보이며,
  입력 형식(예: `@` 누락, `@` 앞/뒷부분 누락 등)에 따라 상황에 맞는 브라우저 기본 안내 문구가
  노출된다.
- **REQ-PRODUCT-DETAIL-025**: 3개 필수값을 모두 올바르게 입력하고 Submit 버튼을 클릭하면 폼
  하단에 초록색 "Thank you for your review." 성공 메시지가 노출된다. 이 메시지가 노출된 후
  1~2초가 경과하면 입력 필드들(Your Name, Email Address, 리뷰 내용)이 자동으로 빈 값으로
  초기화된다.

**Related Products**

- **REQ-PRODUCT-DETAIL-026**: 상세 페이지에는 "Related Products"(연관 상품) 섹션이 존재하지
  않는다.

### 4.2 미확인 / 추가 확인 필요 항목

- 현재 없음 (이전에 제기되었던 미확인 항목 4건 모두 사용자 확인 완료됨)

## 5. Feature 단위 In Scope / Out of Scope

**In Scope**

- 상품 상세 페이지 URL 패턴(`/product_details/{id}`) 및 상품 ID 파라미터 처리(존재하는 ID로
  정상 접근하는 케이스와 존재하지 않는 ID로 접근했을 때의 비정상 렌더링 케이스 포함)
- 정상 상품 기준 화면 구성요소(이미지, NEW 배지, 상품명, 카테고리, 별점 표시, 가격, Quantity
  입력 UI, Add to cart 버튼, Availability/Condition/Brand 텍스트, 사이즈/색상 옵션 부재, WRITE
  YOUR REVIEW 섹션)와 단일 스크롤 레이아웃 구조
- 상세 페이지에서 "Add to cart" 클릭 시 확인 모달이 리스트 페이지와 동일하게 노출된다는 사실
  (모달 자체의 상세 구성은 `cart.md` 참조)
- Quantity 입력 UI의 스피너 최소/최대값 동작 및 비정상 입력값(문자, 문자+숫자 혼합, 음수, 0)
  상태에서 "Add to cart" 클릭 시의 실제 반응(결함 의심 사항 포함)
- 별점(rating) 아이콘의 클릭 가능 여부(정적 표시)
- "WRITE YOUR REVIEW" 섹션의 필수값 검증 동작(브라우저 네이티브 검증) 및 정상 제출 시 반응
  (성공 메시지 노출, 필드 자동 초기화)
- "Related Products"(연관 상품) 섹션의 존재 여부(미존재 확인)

**Out of Scope**

- 정상 수량으로 장바구니에 담았을 때 장바구니 페이지에 실제로 반영되는 결과(수량 표시, 동일
  상품 누적 등) — `cart.md`(REQ-CART-004) 범위
- Home/Products/검색결과/카테고리·브랜드 목록 페이지의 상품 카드 UI 자체 — `page-ui.md`,
  `product-search.md` 범위
- 결제/체크아웃 관련 절차 — Project PRD "7. Out of Scope"의 결제 기능 제외 원칙
- 광고 배너 등 automationexercise.com 고유 UI가 아닌 요소 — Project PRD "8. 기타 제약사항"의
  광고 제외 원칙에 따름

## 6. 예외 / 에러 케이스

- 존재하지 않는 상품 ID로 상세 페이지에 접근했을 때, 별도 에러 페이지 없이 이미지/카테고리/
  브랜드 데이터만 비어있는 채로 페이지 골격이 그대로 렌더링되는 케이스 (REQ-PRODUCT-DETAIL-003,
  결함 의심)
- Quantity 입력란에 문자만(또는 문자+숫자 혼합) 입력한 상태에서 "Add to cart"를 클릭했을 때
  아무 반응 없이 조용히 실패하는 케이스 (REQ-PRODUCT-DETAIL-019, 결함 의심)
- Quantity 입력란에 음수를 입력한 상태에서 "Add to cart"를 클릭했을 때, 담기는 것이 아니라
  기존 장바구니 수량에서 절댓값만큼 차감되는 케이스 (REQ-PRODUCT-DETAIL-020, 결함 의심)
- Quantity 입력란에 0을 입력한 상태에서 "Add to cart"를 클릭했을 때 수량 0으로 그대로 담기는
  케이스 (REQ-PRODUCT-DETAIL-021, 결함 의심)

## 7. 비고

- **결함 의심 사항에 대한 처리 원칙**: REQ-PRODUCT-DETAIL-003, 019, 020, 021은 사용자가 실제
  조작을 통해 관찰한 비정상 동작이며, 정상적으로 기대되는 동작과 다르게 보여 "결함 의심"으로
  표시했다. 본 문서는 발견된 사실을 있는 그대로 기록하는 것까지가 범위이며, 실제 결함 여부
  판정, 수정, 별도 이슈 트래킹은 본 문서의 범위 밖이다.
- **`cart.md`와의 경계**: Quantity 입력란 자체의 화면 구성(스피너 버튼 등)과, 그 입력란에
  비정상 값(문자, 음수, 0)을 넣고 "Add to cart"를 클릭했을 때의 반응은 상세 페이지 고유의
  관찰 사항이자 `cart.md` 작성 시점에는 다뤄지지 않았던 신규 발견이므로 본 문서에 기록했다.
  `cart.md`는 승인완료 상태의 문서이므로 본 문서 작성 과정에서 임의로 수정하지 않았으며,
  정상 수량으로 담았을 때 장바구니에 반영되는 결과(REQ-CART-004)만 참조로 연결했다.
- **`login-logout.md`와의 표현 일관성**: 리뷰 폼 필수값 검증(REQ-PRODUCT-DETAIL-023)과 이메일
  형식 검증(REQ-PRODUCT-DETAIL-024)은 `login-logout.md`의 REQ-LOGIN-LOGOUT-006~008과 동일하게
  브라우저 자체(HTML5 native) 유효성 검사임을 확인해 동일한 표현으로 기술했다.
- **Related Products**: 최초 작성 시 4.2 미확인 항목이었으나, 사용자가 페이지 하단까지 직접
  확인해 "Related Products"(연관 상품) 섹션이 존재하지 않음을 확정했다(REQ-PRODUCT-DETAIL-026).
- "고려기프트" 등 광고 배너가 스크린샷에서 관찰되었으나, Project PRD "8. 기타 제약사항"의
  광고 제외 원칙에 따라 Requirements에 포함하지 않았다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-21 | 최초 작성 (Draft) — 사용자 실측 결과 반영, REQ-PRODUCT-DETAIL-001~021 정리, 결함 의심 4건(003, 019, 020, 021) 포함, 4.2 미확인 항목 4건 정리 | 초안 |
| 2026-08-21 | 4.2 미확인 항목 4건 모두 사용자 확인 완료 반영: REQ-PRODUCT-DETAIL-022(별점 클릭 불가), 023(리뷰 3개 필드 필수, 네이티브 필수 입력 검증), 024(이메일 형식 네이티브 검증), 025(정상 제출 시 "Thank you for your review." 성공 메시지 및 1~2초 후 필드 자동 초기화), 026(Related Products 섹션 미존재 확정) 추가. 5. In/Out Scope 항목 이동(리뷰 검증·Related Products를 Out of Scope에서 In Scope로 이동), 4.2를 "현재 없음"으로 정리, REQ-PRODUCT-DETAIL-008의 오래된 미확인 문구 정리 | 초안 |
| 2026-08-21 | 사용자 최종 승인 | 승인완료 |
