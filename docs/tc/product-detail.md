---
문서유형: Test Case
상태: 승인완료   # 초안 | 승인완료
관련 Feature PRD: feature/product-detail.md
최초 작성일: 2026-08-22
최근 변경일: 2026-08-22
승인일: 2026-08-22
---

# Test Case - 상품 상세

## TC 목록

> 공통 Preconditions: 사이트 진입 시 또는 일정 시간 경과 시 무작위로 노출될 수 있는 모달형 광고는
> Project PRD "8. 기타 제약사항" 원칙에 따라 검증 대상이 아니므로, 모든 TC 수행 전 광고 모달이
> 노출된 경우 닫은 상태에서 진행한다(아래 표에는 반복 기재하지 않음). 별도 언급이 없는 한 로그인/
> 로그아웃 상태는 무관하다(Feature PRD에 로그인 필요 조건이 명시되지 않음).

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-PRODUCT-DETAIL-001 | REQ-PRODUCT-DETAIL-001 | 상품 상세 | Home 페이지에서 "View Product" 링크 클릭 시 이동한 URL이 `/product_details/{id}` 패턴을 따르는지 확인 | Home(`/`) 페이지에 진입해 있는 상태 | 1. Home(`/`) 페이지의 임의 상품 카드에서 "View Product" 링크를 클릭한다.<br>2. 이동한 페이지의 URL을 확인한다. | URL이 `https://automationexercise.com/product_details/{id}` 형태(마지막 경로가 상품 ID)로 이동한다(예: `/product_details/1`). | P2 | |
| TC-PRODUCT-DETAIL-002 | REQ-PRODUCT-DETAIL-002 | 상품 상세 | 존재하는 상품 ID로 상세 페이지에 직접 URL 접근 시 페이지가 정상적으로 노출되는지 확인 | 존재하는 상품 ID 확인됨(예: 1) | 1. 브라우저 주소창에 `https://automationexercise.com/product_details/1`을 직접 입력하여 진입한다.<br>2. 페이지 노출 여부를 확인한다. | 별도 에러 없이 상세 페이지가 정상적으로 노출되며, 상품 이미지/상품명/가격 등 화면 구성요소가 표시된다. | P1 | |
| TC-PRODUCT-DETAIL-003 | REQ-PRODUCT-DETAIL-004 | 상품 상세 | 상품 이미지가 단일 이미지로만 노출되고 썸네일 전환 UI가 없는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태(예: `/product_details/1`) | 1. 상세 페이지 상단 이미지 영역을 확인한다. | 상품 이미지가 단일 이미지로 노출되며, 여러 장의 이미지를 전환할 수 있는 썸네일 목록이나 전환 UI는 노출되지 않는다. | P2 | |
| TC-PRODUCT-DETAIL-004 | REQ-PRODUCT-DETAIL-005 | 상품 상세 | 상품 이미지 좌상단에 빨간색 "NEW" 배지가 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 상세 페이지 상단 이미지 영역의 좌상단을 확인한다. | 이미지 좌상단에 빨간색 "NEW" 배지가 노출된다. | P2 | |
| TC-PRODUCT-DETAIL-005 | REQ-PRODUCT-DETAIL-006 | 상품 상세 | 상품명이 텍스트로 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태(예: "Blue Top" 상품) | 1. 상품 정보 영역의 상품명을 확인한다. | 상품명이 텍스트로 노출된다(예: "Blue Top"). | P2 | |
| TC-PRODUCT-DETAIL-006 | REQ-PRODUCT-DETAIL-007 | 상품 상세 | "Category: {대분류} > {소분류}" 형태로 카테고리 경로 텍스트가 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 상품 정보 영역에서 카테고리 텍스트를 확인한다. | "Category: Women > Tops"와 같이 "Category: {대분류} > {소분류}" 형태의 텍스트가 노출된다. | P2 | |
| TC-PRODUCT-DETAIL-007 | REQ-PRODUCT-DETAIL-008 | 상품 상세 | 주황색 별 아이콘으로 구성된 별점이 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 상품 정보 영역에서 별점 표시를 확인한다. | 주황색 별 아이콘으로 구성된 별점이 노출된다(예: 4.5개 채워진 형태). | P2 | |
| TC-PRODUCT-DETAIL-008 | REQ-PRODUCT-DETAIL-009 | 상품 상세 | 가격이 Rs. 단위로 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 상품 정보 영역에서 가격을 확인한다. | 가격이 "Rs. {숫자}" 형태로 Rs. 단위와 함께 노출된다. | P2 | |
| TC-PRODUCT-DETAIL-009 | REQ-PRODUCT-DETAIL-010 | 상품 상세 | Quantity 입력란이 숫자를 직접 입력할 수 있는 네이티브 number input이며, 위/아래 스피너 버튼과 함께 "Add to cart" 버튼 옆에 위치하는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 상품 정보 영역에서 Quantity 입력란을 확인한다.<br>2. 입력란에 숫자를 직접 입력해본다. | Quantity 입력란은 숫자를 직접 입력할 수 있고, 입력란 우측에 위/아래 스피너 버튼이 함께 노출되는 네이티브 number input 형태이며, "Add to cart" 버튼 바로 옆에 위치한다. | P2 | |
| TC-PRODUCT-DETAIL-010 | REQ-PRODUCT-DETAIL-011 | 상품 상세 | 주황색 "Add to cart" 버튼이 Quantity 입력란 옆에 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Quantity 입력란 옆 영역을 확인한다. | 주황색 "Add to cart" 버튼이 Quantity 입력란 옆에 노출된다. | P2 | |
| TC-PRODUCT-DETAIL-011 | REQ-PRODUCT-DETAIL-012 | 상품 상세 | Availability/Condition/Brand 텍스트 정보가 노출되고 Brand명이 링크 형태인지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 상품 정보 영역에서 Availability, Condition, Brand 텍스트를 확인한다. | "Availability: In Stock", "Condition: New", "Brand: {브랜드명}" 텍스트 정보가 노출되며, 브랜드명 부분은 링크 형태로 노출된다. | P2 | |
| TC-PRODUCT-DETAIL-012 | REQ-PRODUCT-DETAIL-013 | 상품 상세 | 상세 페이지에 사이즈/색상을 선택하는 UI가 존재하지 않는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 상세 페이지 전체 화면에서 사이즈/색상 선택 UI 존재 여부를 확인한다. | 사이즈 또는 색상을 선택할 수 있는 UI 요소가 존재하지 않는다. | P2 | |
| TC-PRODUCT-DETAIL-013 | REQ-PRODUCT-DETAIL-014 | 상품 상세 | 하단 "WRITE YOUR REVIEW" 섹션이 Your Name/Email Address/리뷰 내용 입력란과 Submit 버튼으로 구성되어 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 페이지 하단으로 스크롤해 "WRITE YOUR REVIEW" 섹션을 확인한다. | "WRITE YOUR REVIEW" 섹션에 Your Name 입력란, Email Address 입력란, "Add Review Here!" placeholder를 가진 텍스트 영역, Submit 버튼이 모두 노출된다. | P2 | |
| TC-PRODUCT-DETAIL-014 | REQ-PRODUCT-DETAIL-015 | 상품 상세 | 상세 페이지가 탭 전환 구조가 아니라 이미지부터 WRITE YOUR REVIEW까지 순서대로 이어지는 단일 스크롤 레이아웃인지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 페이지 최상단부터 최하단까지 순서대로 스크롤하며 구성요소 배치 순서와 탭 전환 UI 존재 여부를 확인한다. | 별도 탭으로 전환되는 구조 없이, 상품 이미지 → 카테고리 → 별점 → 가격 → Quantity/Add to cart → Availability/Condition/Brand 정보 → WRITE YOUR REVIEW 섹션이 순서대로 한 화면에 이어서 노출된다. | P2 | |
| TC-PRODUCT-DETAIL-015 | REQ-PRODUCT-DETAIL-016 | 상품 상세 | 정상적인 수량 값을 지정한 상태에서 "Add to cart" 버튼 클릭 시 리스트 페이지와 동일한 확인 모달이 노출되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Quantity 입력란에 정상적인 수량 값(예: 2)을 입력한다.<br>2. "Add to cart" 버튼을 클릭한다. | 초록 체크 아이콘, "Added!", "Your product has been added to cart." 문구, "View Cart" 링크, 초록색 "Continue Shopping" 버튼으로 구성된 확인 모달이 노출된다(Home/Products 리스트 페이지와 동일, `cart.md` REQ-CART-001 참조). | P0 | |
| TC-PRODUCT-DETAIL-016 | REQ-PRODUCT-DETAIL-017 | 상품 상세 | Quantity 입력란의 스피너 아래 버튼을 반복 클릭해도 1 미만으로 내려가지 않는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태, Quantity 입력란 기본값 1 | 1. Quantity 입력란의 스피너 아래(▼) 버튼을 여러 차례 클릭한다. | Quantity 값이 1 미만으로 내려가지 않고 1에서 멈춘다. | P2 | |
| TC-PRODUCT-DETAIL-017 | REQ-PRODUCT-DETAIL-018 | 상품 상세 | Quantity 입력란의 스피너 위 버튼을 다수 클릭해도 최댓값 제한이 없는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Quantity 입력란의 스피너 위(▲) 버튼을 다수(예: 20회) 클릭한다. | 클릭한 횟수만큼 Quantity 값이 계속 증가하며, 특정 값에서 증가가 멈추는 최댓값 제한이 나타나지 않는다. | P2 | |
| TC-PRODUCT-DETAIL-018 | REQ-PRODUCT-DETAIL-022 | 상품 상세 | 별점(rating) 아이콘이 클릭할 수 없는 정적 표시 요소인지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 별점 아이콘을 클릭한다. | 클릭해도 별점 값이나 표시 상태에 아무 변화가 없다(클릭 불가능한 정적 표시 요소). | P2 | |
| TC-PRODUCT-DETAIL-019 | REQ-PRODUCT-DETAIL-023 | 상품 상세 | WRITE YOUR REVIEW 섹션의 Your Name/Email Address/리뷰 내용 3개 필드를 모두 비운 채 Submit 클릭 시 브라우저 네이티브 필수 입력 검증이 동작하는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. "WRITE YOUR REVIEW" 섹션의 Your Name, Email Address, 리뷰 내용(Add Review Here!) 입력란을 모두 비워둔다.<br>2. Submit 버튼을 클릭한다. | 브라우저 자체(HTML5 native) 필수 입력 검증 팝업("이 입력란을 작성하세요.")이 비어있는 필드를 순서대로 가리키며 노출되고, 폼 제출이 차단된다. | P2 | |
| TC-PRODUCT-DETAIL-020 | REQ-PRODUCT-DETAIL-024 | 상품 상세 | Email Address 필드에 형식이 올바르지 않은 값을 입력한 상태에서 Submit 클릭 시 브라우저 네이티브 이메일 형식 검증이 동작하는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Your Name과 리뷰 내용 입력란에는 임의의 값을 입력한다.<br>2. Email Address 입력란에 '@'가 없는 값(예: "invalidemail")을 입력한다.<br>3. Submit 버튼을 클릭한다. | 브라우저 자체(HTML5 native) 이메일 형식 유효성 검사 팝업이 입력 형식에 맞는 안내 문구와 함께 노출되며, 폼 제출이 차단된다. | P2 | |
| TC-PRODUCT-DETAIL-021 | REQ-PRODUCT-DETAIL-025 | 상품 상세 | WRITE YOUR REVIEW 3개 필수값을 모두 올바르게 입력하고 Submit 클릭 시 성공 메시지가 노출되고 일정 시간 후 필드가 자동 초기화되는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Your Name, Email Address(올바른 형식), 리뷰 내용(Add Review Here!) 입력란에 모두 유효한 값을 입력한다.<br>2. Submit 버튼을 클릭한다.<br>3. 메시지 노출 직후와 1~2초 경과 후 각각 입력 필드 상태를 확인한다. | 폼 하단에 초록색 "Thank you for your review." 성공 메시지가 노출된다. 메시지 노출 후 1~2초가 경과하면 Your Name, Email Address, 리뷰 내용 입력 필드가 자동으로 빈 값으로 초기화된다. | P2 | |
| TC-PRODUCT-DETAIL-022 | REQ-PRODUCT-DETAIL-026 | 상품 상세 | 상세 페이지에 "Related Products"(연관 상품) 섹션이 존재하지 않는지 확인 | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. 페이지 최하단(WRITE YOUR REVIEW 섹션 이후)까지 스크롤한다.<br>2. "Related Products" 섹션 존재 여부를 확인한다. | "Related Products"(연관 상품) 섹션이 노출되지 않는다. | P2 | |

## 결함 의심 항목

> `tc-writing` Skill 4.6에 따라, PRD상 "결함 의심"(비정상 동작이 관찰되었으나 정상/비정상 여부는
> 별도 판정하지 않고 사실만 기록)으로 표시된 요구사항에 대한 TC를 정상 케이스 TC 목록과 분리해
> 별도로 모았습니다. ID 넘버링은 위 정상 케이스 TC 목록(001~022)에 이어서 부여했으며, 컬럼 구조와
> Requirement ID 매핑, Priority 산정 방식은 정상 케이스 TC와 동일합니다.

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-PRODUCT-DETAIL-023 | REQ-PRODUCT-DETAIL-003 | 상품 상세 | 존재하지 않는 상품 ID로 상세 페이지 접근 시 이미지/Category/Brand는 빈 값으로, 나머지 레이아웃은 정상 상품과 동일하게 노출되는 비정상 동작 확인 (결함 의심) | 존재하지 않는 상품 ID 확인됨(예: 99) | 1. 브라우저 주소창에 `https://automationexercise.com/product_details/99`를 직접 입력하여 진입한다.<br>2. 화면 전체 구성요소를 확인한다. | 별도의 404/에러 페이지 없이 상세 페이지 레이아웃이 그대로 렌더링된다. 이미지 영역에는 깨진 이미지 아이콘과 "ecommerce website products" alt 텍스트만 노출되고, Category/Brand 필드는 값 없이 빈 채로 노출된다. 반면 별점, Quantity 입력란, "Add to cart" 버튼, "Availability: In Stock", "Condition: New", "WRITE YOUR REVIEW" 섹션은 정상 상품과 동일하게 노출된다. | P1 | |
| TC-PRODUCT-DETAIL-024 | REQ-PRODUCT-DETAIL-019 | 상품 상세 | Quantity 입력란에 문자만 입력한 상태에서 "Add to cart" 클릭 시 조용히 실패하는 비정상 동작 확인 (결함 의심) | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Quantity 입력란의 기존 값을 지우고 문자만 입력한다(예: "abc").<br>2. "Add to cart" 버튼을 클릭한다. | 장바구니에 담기지 않고 페이지도 그대로 유지되며, 별도의 에러 안내 문구도 노출되지 않는다(확인 모달 미노출, 조용히 실패). | P1 | |
| TC-PRODUCT-DETAIL-025 | REQ-PRODUCT-DETAIL-019 | 상품 상세 | Quantity 입력란에 숫자와 문자를 혼합 입력한 상태에서 "Add to cart" 클릭 시에도 동일하게 조용히 실패하는지 확인 (결함 의심) | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Quantity 입력란의 기존 값을 지우고 숫자와 문자를 혼합해 입력한다(예: "2a").<br>2. "Add to cart" 버튼을 클릭한다. | TC-PRODUCT-DETAIL-024와 동일하게 장바구니에 담기지 않고 페이지도 그대로 유지되며, 별도의 에러 안내 문구도 노출되지 않는다. | P1 | |
| TC-PRODUCT-DETAIL-026 | REQ-PRODUCT-DETAIL-020 | 상품 상세 | 이미 동일 상품이 담겨 있는 상태에서 Quantity 입력란에 음수를 입력하고 "Add to cart" 클릭 시 기존 수량에서 절댓값만큼 차감되는 비정상 동작 확인 (결함 의심) | 상세 페이지의 동일 상품이 장바구니에 5개 담겨 있는 상태(사전 조작은 정상 수량으로 "Add to cart"를 반복 수행해 준비) | 1. 동일 상품의 상세 페이지에서 Quantity 입력란의 기존 값을 지우고 "-2"를 입력한다.<br>2. "Add to cart" 버튼을 클릭한다.<br>3. 장바구니(`/view_cart`)로 이동해 해당 상품의 수량을 확인한다. | 장바구니에 새로운 항목으로 담기지 않고, 기존에 담겨 있던 해당 상품의 수량이 입력한 음수의 절댓값만큼 차감된다(5개 → 3개로 감소). | P1 | |
| TC-PRODUCT-DETAIL-027 | REQ-PRODUCT-DETAIL-021 | 상품 상세 | Quantity 입력란에 0을 입력한 상태에서 "Add to cart" 클릭 시 수량 0으로 장바구니에 담기는 비정상 동작 확인 (결함 의심) | 존재하는 상품 ID로 상세 페이지 진입 상태 | 1. Quantity 입력란의 기존 값을 지우고 "0"을 입력한다.<br>2. "Add to cart" 버튼을 클릭한다.<br>3. 장바구니(`/view_cart`)로 이동해 해당 상품의 수량을 확인한다. | 담기지 않거나 최소 1개로 자동 보정되는 것이 아니라, 장바구니에 해당 상품이 수량 0으로 표기된 채 그대로 담긴다. | P1 | |

## Priority 산정 근거

- **TC-PRODUCT-DETAIL-001**: Impact 4 / Likelihood 2 / Risk Score 8 — URL 패턴이 어긋나면 상세 페이지 진입 자체가 실패할 수 있어 영향은 크지만, 단순 링크 클릭에 의한 이동이라 결함 발생 가능성은 낮음.
- **TC-PRODUCT-DETAIL-002**: Impact 5 / Likelihood 2 / Risk Score 10 — 존재하는 상품의 상세 페이지 노출은 상품 탐색·구매 퍼널 전체의 필수 진입점이라 실패 시 핵심 기능 사용이 불가능해지지만, 단순 페이지 렌더링이라 결함 발생 가능성 자체는 낮음. (사용자 확인 결과 현재 산정 유지, 변경 없음)
- **TC-PRODUCT-DETAIL-003**: Impact 2 / Likelihood 1 / Risk Score 2 — 정적 이미지 영역 노출 확인으로 영향과 결함 가능성 모두 낮음.
- **TC-PRODUCT-DETAIL-004**: Impact 1 / Likelihood 1 / Risk Score 1 — 단순 배지 노출 확인으로 영향이 매우 낮음.
- **TC-PRODUCT-DETAIL-005**: Impact 3 / Likelihood 1 / Risk Score 3 — 상품명이 노출되지 않으면 사용자가 어떤 상품인지 식별할 수 없어 영향은 있으나, 정적 텍스트 렌더링이라 결함 발생 가능성은 낮음.
- **TC-PRODUCT-DETAIL-006**: Impact 2 / Likelihood 1 / Risk Score 2 — 정적 카테고리 텍스트 노출 확인.
- **TC-PRODUCT-DETAIL-007**: Impact 2 / Likelihood 1 / Risk Score 2 — 정적 별점 표시 노출 확인(클릭 동작은 TC-PRODUCT-DETAIL-018에서 별도 검증).
- **TC-PRODUCT-DETAIL-008**: Impact 4 / Likelihood 2 / Risk Score 8 — 가격 정보 오류는 구매 결정에 직접적인 영향을 미치는 중요 정보이나, 상품별 데이터 렌더링 수준의 검증이라 결함 발생 가능성은 일반적인 수준.
- **TC-PRODUCT-DETAIL-009**: Impact 3 / Likelihood 2 / Risk Score 6 — 수량 입력 UI는 구매 액션(Add to cart)의 일부라 문제 발생 시 사용자 경험이 저하되며, 네이티브 input과 커스텀 스타일이 결합된 형태라 결함 발생 가능성이 다소 있음.
- **TC-PRODUCT-DETAIL-010**: Impact 3 / Likelihood 1 / Risk Score 3 — Add to cart 버튼의 노출 자체를 확인하는 것으로(클릭 시 동작은 TC-PRODUCT-DETAIL-015에서 별도 검증), 정적 렌더링 수준이라 결함 발생 가능성은 낮음.
- **TC-PRODUCT-DETAIL-011**: Impact 2 / Likelihood 1 / Risk Score 2 — 정적 텍스트 정보 노출 확인.
- **TC-PRODUCT-DETAIL-012**: Impact 1 / Likelihood 1 / Risk Score 1 — UI 부재를 확인하는 단순 Negative Case로 영향이 매우 낮음.
- **TC-PRODUCT-DETAIL-013**: Impact 2 / Likelihood 2 / Risk Score 4 — 여러 하위 구성요소(입력란 3종+버튼)를 함께 확인해야 해 단일 요소 확인보다는 결함 발생 가능성이 다소 있음.
- **TC-PRODUCT-DETAIL-014**: Impact 2 / Likelihood 2 / Risk Score 4 — 전체 레이아웃 순서 확인으로 여러 섹션을 함께 확인해야 함.
- **TC-PRODUCT-DETAIL-015**: **Impact 4 / Likelihood 4 / Risk Score 16 / P0** (사용자 최종 확인 완료로 재산정 확정, 2026-08-22). Impact를 4로 평가한 이유는, Add to cart가 구매 퍼널의 핵심 액션이지만 동일 기능이 Home/Products 리스트 페이지에서도 별도로 동작하므로(`cart.md` REQ-CART-001 참조) 상품 상세 페이지 경로에서만 결함이 발생해도 사이트 전체의 장바구니 담기 기능이 전면 차단되는 것은 아니라고 판단했기 때문입니다. Likelihood를 4로 평가한 이유는, 이 TC는 (1) 상세 페이지 고유의 커스텀 스타일 Quantity 입력값 캡처, (2) 해당 값의 장바구니 반영, (3) `cart.md`에서 이미 검증된 공유 모달 컴포넌트 렌더링까지 3단계가 이 페이지 문맥에서 새롭게 결합되어 동작해야 하므로, 단일 정적 요소 확인보다 결함 발생 가능성이 높다고 판단했기 때문입니다.
- **TC-PRODUCT-DETAIL-016**: Impact 2 / Likelihood 2 / Risk Score 4 — 스피너 최솟값 제한이라는 Boundary 로직으로 영향은 제한적이나 로직 오류 가능성은 존재.
- **TC-PRODUCT-DETAIL-017**: Impact 2 / Likelihood 2 / Risk Score 4 — TC-PRODUCT-DETAIL-016과 동일 근거(최댓값 미제한 Boundary 확인).
- **TC-PRODUCT-DETAIL-018**: Impact 1 / Likelihood 1 / Risk Score 1 — 클릭 불가(정적 요소)임을 확인하는 것으로 영향이 매우 낮음.
- **TC-PRODUCT-DETAIL-019**: Impact 2 / Likelihood 1 / Risk Score 2 — 브라우저 기본 제공(native) 기능으로 애플리케이션 로직에 의한 결함 가능성이 매우 낮음(`login-logout.md` TC-LOGIN-LOGOUT-007~009와 동일 근거).
- **TC-PRODUCT-DETAIL-020**: Impact 2 / Likelihood 1 / Risk Score 2 — TC-PRODUCT-DETAIL-019와 동일 근거(브라우저 네이티브 이메일 형식 검증).
- **TC-PRODUCT-DETAIL-021**: Impact 3 / Likelihood 2 / Risk Score 6 — 리뷰 제출 성공 여부를 사용자에게 알리는 피드백 UX이며, 메시지 노출과 1~2초 지연 후 필드 초기화라는 타이밍 로직이 결합되어 있어 결함 발생 가능성이 다소 있음.
- **TC-PRODUCT-DETAIL-022**: Impact 1 / Likelihood 1 / Risk Score 1 — 섹션 부재를 확인하는 단순 Negative Case로 영향이 매우 낮음.
- **TC-PRODUCT-DETAIL-023** (결함 의심): Impact 3 / Likelihood 3 / Risk Score 9 — 존재하지 않는 ID로 직접 접근하는 제한적 시나리오라 다수 사용자에게 미치는 영향은 크지 않지만, 사용자가 실측을 통해 이미 재현을 확인한 결함 의심 사항으로 발생 가능성은 높음.
- **TC-PRODUCT-DETAIL-024** (결함 의심): Impact 3 / Likelihood 3 / Risk Score 9 — 비정상 입력 시 아무 안내 없이 조용히 실패해 사용자가 원인을 알 수 없는 UX 문제이며, 이미 사용자 실측으로 재현이 확인된 결함 의심 사항.
- **TC-PRODUCT-DETAIL-025** (결함 의심): Impact 3 / Likelihood 3 / Risk Score 9 — TC-PRODUCT-DETAIL-024와 동일 근거(문자+숫자 혼합 입력 조건에 대한 재현 확인).
- **TC-PRODUCT-DETAIL-026** (결함 의심): Impact 4 / Likelihood 3 / Risk Score 12 — 사용자 의도와 다르게 장바구니 수량이 임의로 변경되는 데이터 무결성 문제로 영향이 크며, 이미 재현이 확인된 결함 의심 사항.
- **TC-PRODUCT-DETAIL-027** (결함 의심): Impact 4 / Likelihood 3 / Risk Score 12 — 수량 0인 상태로 장바구니에 담겨 이후 주문/결제 흐름에서 잘못된 데이터로 이어질 수 있는 문제이며, 이미 재현이 확인된 결함 의심 사항.

> 참고: 결함 의심 항목(TC-PRODUCT-DETAIL-023~027)을 제외한 정상 케이스 TC 중, 사용자 최종 확인을
> 거쳐 TC-PRODUCT-DETAIL-015(상품 상세 페이지 Add to cart 정상 동작)가 Risk Score 16 / P0로
> 재산정 확정되었습니다(위 해당 TC 산정 근거 참조). 그 외 정상 케이스 TC 중에는 Risk Score 16
> 이상(P0)에 해당하는 항목이 없다고 판단됩니다. `login-logout.md`의 로그인 성공
> (TC-LOGIN-LOGOUT-004, P0)과 마찬가지로, 여러 핵심 요소가 결합되어 결함 발생 가능성이 높은
> 시나리오로서 본 Feature 범위에서 TC-PRODUCT-DETAIL-015가 현재 유일한 P0 TC입니다.

## 사용자 확인 필요 사항

1. **결함 의심 사항(REQ-PRODUCT-DETAIL-003, 019, 020, 021)의 TC 처리 방식**: ✅ 확인 완료 —
   `tc-writing` Skill에 신설된 4.6 규칙에 따라, 정상 케이스 TC 목록에서 제외하지 않고 "결함 의심
   항목" 섹션(TC-PRODUCT-DETAIL-023~027)으로 분리해 문서 가장 밑에 포함했습니다.
2. **REQ-PRODUCT-DETAIL-019 TC 분리(TC-PRODUCT-DETAIL-024/025)**: ✅ 확인 완료 — 문자만 입력한
   경우와 숫자+문자 혼합 입력한 경우를 별도 TC로 분리한 현재 방식이 적절하다고 확인받아 변경 없이
   유지했습니다.
3. **TC-PRODUCT-DETAIL-026(舊 TC-021) Preconditions**: ✅ 확인 완료 — "장바구니에 동일 상품이
   5개 담겨 있는 상태"를 Preconditions에만 명시하고 별도 TC로 담기 절차를 기술하지 않는 현재
   방식이 적절하다고 확인받아 변경 없이 유지했습니다.
4. **TC-PRODUCT-DETAIL-002 Priority**: ✅ 확인 완료 — 현재 산정(Impact 5 / Likelihood 2 / Risk
   Score 10 / P1)이 적절하다고 확인받아 변경 없이 유지했습니다.
5. **TC-PRODUCT-DETAIL-015(舊 TC-016) Priority P0 재산정**: ✅ 확인 완료 — 제안한 재산정값
   (Impact 4 / Likelihood 4 / Risk Score 16 / P0)으로 최종 확정되었습니다. TC 목록 표의
   Priority 컬럼을 P1 → P0로 반영했습니다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-22 | 최초 작성 (승인완료된 Feature PRD `product-detail.md`의 REQ-PRODUCT-DETAIL-001~026 기반 TC-PRODUCT-DETAIL-001~027 초안 작성, REQ-019는 문자 입력/혼합 입력 조건별로 TC-019/020 2건으로 분리) | 초안 |
| 2026-08-22 | 사용자 리뷰 결과 반영: `tc-writing` Skill 4.6 신규 규칙에 따라 결함 의심 5건(舊 TC-PRODUCT-DETAIL-003/019/020/021/022, REQ-003/019(x2)/020/021)을 메인 TC 목록에서 분리해 "결함 의심 항목" 섹션으로 이동(신규 ID TC-PRODUCT-DETAIL-023~027 부여). 메인 TC 목록은 ID 001~022로 재부여(내용 변경 없음, ID만 재번호). REQ-019 TC 분리 방식, TC-021(신 026) Preconditions 처리 방식, TC-002 Priority 산정은 적절함을 확인받아 변경 없이 유지. TC-PRODUCT-DETAIL-016(신 015) Priority는 P0 재산정 필요성 검토 요청에 따라 재검토안(Impact 4/Likelihood 4/Risk 16/P0)을 제시했으며 최종 확정은 사용자 재확인 대기 중. Priority 산정 근거 섹션 전체 TC ID 재매핑. | 초안 |
| 2026-08-22 | TC-PRODUCT-DETAIL-015 Priority P0 재산정 확정: 사용자 최종 확인을 거쳐 Impact 4 / Likelihood 4 / Risk Score 16 / P0로 확정하고, TC 목록 표 Priority 컬럼(P1→P0), Priority 산정 근거, 사용자 확인 필요 사항, "이 Feature에 P0가 없다"는 취지의 참고 문단을 함께 갱신함. 문서 상태는 초안 유지(전체 문서 최종 승인은 별도 진행 예정). | 초안 |
| 2026-08-22 | 사용자 최종 승인 | 승인완료 |
