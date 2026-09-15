---
문서유형: Test Case
상태: 승인완료   # 초안 | 승인완료
관련 Feature PRD: feature/cart.md
최초 작성일: 2026-08-22
최근 변경일: 2026-08-22
승인일: 2026-08-22
---

# Test Case - 장바구니 (상품 담기 포함)

## TC 목록

> 공통 Preconditions: 사이트 진입 시 또는 일정 시간 경과 시 무작위로 노출될 수 있는 모달형 광고는
> Project PRD "8. 기타 제약사항" 원칙에 따라 검증 대상이 아니므로, 모든 TC 수행 전 광고 모달이
> 노출된 경우 닫은 상태에서 진행한다(아래 표에는 반복 기재하지 않음).
>
> 본 문서는 Cart 페이지의 화면 구성요소 "존재 여부"(브레드크럼, 빈 카트 안내 문구, "Proceed To
> Checkout" 버튼, 상품 목록 표 컬럼 구성)는 다루지 않는다. 해당 내용은 `page-ui.md`
> TC-PAGE-UI-017~021에서 이미 검증되었으며, 필요한 경우 아래 TC에서 해당 TC ID를 참조로만
> 표기한다. 마찬가지로 `/checkout` 페이지의 화면 구성요소 "존재 여부"(Address Details,
> Review Your Order, 주문 코멘트 입력란, Place Order 버튼 등의 노출)도 `page-ui.md`
> TC-PAGE-UI-034~041에서 다루며, 본 문서에서는 별도로 다루지 않는다. 본 문서는 그 구성요소를
> 조작했을 때의 실제 "동작"(담기/누적/삭제/합계 계산/로그인 상태별 분기 등)에 집중한다.

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-CART-001 | REQ-CART-001 | 장바구니 | Home 페이지 상품 카드에서 "Add to cart" 클릭 시 담기 확인 모달이 규정된 구성요소와 함께 노출되는지 확인 | 로그인/로그아웃 상태 무관, Home(`/`) 페이지에 진입해 있는 상태 | 1. Home(`/`) 페이지의 임의 상품 카드에서 "Add to cart" 버튼을 클릭한다.<br>2. 노출되는 모달의 아이콘, 제목, 안내 문구, 링크, 버튼 구성을 확인한다. | 초록색 체크 아이콘, "Added!" 제목, "Your product has been added to cart." 안내 문구, 파란색 텍스트의 "View Cart" 링크, 하단 초록색 "Continue Shopping" 버튼으로 구성된 모달이 노출된다. | P0 | |
| TC-CART-002 | REQ-CART-001 | 장바구니 | 담기 확인 모달에서 "Continue Shopping" 버튼 클릭 시 모달만 닫히고 담기를 시도했던 페이지가 그대로 유지되는지 확인 | Home(`/`) 페이지에서 "Add to cart" 클릭 후 담기 확인 모달이 노출된 상태 | 1. 모달의 "Continue Shopping" 버튼을 클릭한다.<br>2. 화면 상태(모달 노출 여부, 페이지 URL)를 확인한다. | 모달이 닫히고 다른 페이지로 이동하지 않은 채, 담기를 시도했던 Home 페이지가 그대로 유지되어 노출된다. | P2 | |
| TC-CART-003 | REQ-CART-001 | 장바구니 | 담기 확인 모달에서 "View Cart" 링크 클릭 시 장바구니 페이지로 이동하는지 확인 | Home(`/`) 페이지에서 "Add to cart" 클릭 후 담기 확인 모달이 노출된 상태 | 1. 모달의 "View Cart" 링크를 클릭한다.<br>2. 이동한 페이지의 URL을 확인한다. | 장바구니(`https://automationexercise.com/view_cart`) 페이지로 이동한다. | P2 | |
| TC-CART-004 | REQ-CART-002 | 장바구니 | Home 페이지와 Products 페이지에서 각각 담은 상품이 동일한 하나의 장바구니에 함께 누적되는지 확인 | 장바구니가 비어있는 상태 | 1. Home(`/`) 페이지에서 임의 상품(상품 A)의 "Add to cart"를 클릭하고 모달의 "Continue Shopping"으로 닫는다.<br>2. Products(`/products`) 페이지로 이동해 상품 A와 다른 임의 상품(상품 B)의 "Add to cart"를 클릭한다.<br>3. 장바구니(`/view_cart`) 페이지로 이동해 상품 목록을 확인한다. | 상품 A와 상품 B가 별도의 장바구니로 분리되지 않고, 하나의 장바구니 목록에 함께 노출된다. | P1 | |
| TC-CART-005 | REQ-CART-003 | 장바구니 | 리스트 페이지 "Add to cart"는 담을 개수를 지정할 수 없이 항상 1개씩만 담기며, 동일 상품을 반복해서 담으면 별도 행이 아닌 기존 행의 Quantity가 누적되는지 확인 | 장바구니에 해당 상품이 담겨 있지 않은 상태, 단가를 알고 있는 임의 상품 확인됨(예: "Sleeveless Dress", 단가 Rs.1000) | 1. Home 또는 Products 페이지에서 해당 상품의 "Add to cart" 버튼을 7회 반복 클릭한다(매 클릭 후 모달의 "Continue Shopping"으로 닫고 동일 페이지에서 재클릭).<br>2. 장바구니(`/view_cart`) 페이지로 이동한다.<br>3. 해당 상품의 행 개수, Quantity, Total 값을 확인한다. | 해당 상품은 별도 행으로 추가되지 않고 1개 행만 유지되며, Quantity는 7, Total은 단가 x 7(예: Rs. 7000)로 표시된다. | P0 | |
| TC-CART-006 | REQ-CART-004 | 장바구니 | 상품 상세 페이지에서 담을 개수를 지정해 담았을 때 지정한 수량이 그대로 장바구니에 반영되는지 확인 | 장바구니에 해당 상품이 담겨 있지 않은 상태, 존재하는 상품 ID로 상세 페이지 진입 가능한 상태 | 1. 임의 상품의 상세 페이지(`/product_details/{id}`)로 진입한다.<br>2. Quantity 입력란에 1이 아닌 임의의 수량(예: 7)을 입력한다.<br>3. "Add to cart" 버튼을 클릭하고 모달의 "View Cart" 링크를 클릭한다.<br>4. 장바구니 페이지에서 해당 상품의 Quantity와 Total 값을 확인한다. | 리스트 페이지에서 1개씩만 담기는 것(TC-CART-005)과 달리, 상세 페이지에서 지정한 수량(7)이 그대로 반영되어 Quantity 7, Total은 단가 x 7로 표시된다. | P1 | |
| TC-CART-007 | REQ-CART-005 | 장바구니 | 장바구니 페이지의 Quantity 칸이 입력란처럼 보이지만 실제로는 값을 편집할 수 없는 표시 전용 요소인지 확인 | 장바구니에 상품이 1개 이상 담겨 있는 상태(사전 조작은 상품 담기 기능을 통해 준비, 표 컬럼 구성 자체는 `page-ui.md` TC-PAGE-UI-021 참조) | 1. 장바구니(`/view_cart`) 페이지에서 임의 상품 행의 Quantity 칸을 클릭한다.<br>2. 값을 직접 입력하거나 수정을 시도한다. | Quantity 칸의 값이 변경되지 않으며, 값을 편집할 수 있는 수단(입력 포커스, 스피너 등)이 동작하지 않는다. | P2 | |
| TC-CART-008 | REQ-CART-006 | 장바구니 | 장바구니에서 특정 상품 행의 삭제(x) 버튼 클릭 시 해당 상품만 장바구니에서 삭제되는지 확인 | 장바구니에 서로 다른 상품이 2개 이상 담겨 있는 상태 | 1. 장바구니(`/view_cart`) 페이지에서 삭제할 상품 행의 삭제(x) 버튼을 클릭한다.<br>2. 삭제 후 장바구니에 남아있는 상품 목록을 확인한다. | 클릭한 상품만 목록에서 삭제되고, 나머지 상품은 그대로 남아 노출된다. | P1 | |
| TC-CART-009 | REQ-CART-007 | 장바구니 | 장바구니에 담긴 모든 상품을 삭제하면 빈 카트 상태로 전환되는지 확인 | 장바구니에 상품이 1개 이상 담겨 있는 상태 | 1. 장바구니(`/view_cart`) 페이지에서 담긴 모든 상품의 삭제(x) 버튼을 순서대로 클릭해 전부 삭제한다.<br>2. 마지막 상품 삭제 직후 화면을 확인한다. | 상품 목록 표가 사라지고, 빈 카트 안내 상태("Cart is empty! Click here to buy products.", `page-ui.md` TC-PAGE-UI-019와 동일한 문구)로 전환된다. | P2 | |
| TC-CART-010 | REQ-CART-008 | 장바구니 | 로그아웃 상태에서 "Proceed To Checkout" 버튼 클릭 시 로그인/회원가입을 요구하는 모달이 노출되는지 확인 | 로그아웃 상태, 장바구니에 상품이 1개 이상 담겨 있는 상태(`page-ui.md` TC-PAGE-UI-020의 버튼 노출 확인 이후 단계) | 1. 로그아웃 상태로 장바구니(`/view_cart`) 페이지에 진입한다.<br>2. "Proceed To Checkout" 버튼을 클릭한다.<br>3. 노출되는 모달의 구성요소를 확인한다. | 사람 아이콘, "Checkout" 제목, "Register / Login account to proceed on checkout." 안내 문구, "Register / Login" 링크, 하단 초록색 "Continue On Cart" 버튼으로 구성된 모달이 노출되며, `/checkout` 페이지로 이동하지 않는다. | P1 | |
| TC-CART-011 | REQ-CART-009 | 장바구니 | 로그인 상태에서 "Proceed To Checkout" 버튼 클릭 시 모달 없이 바로 `/checkout` 페이지로 이동하는지 확인 | 로그인 상태(유효한 테스트 계정으로 로그인 완료, 예: actest1@test.com), 장바구니에 상품이 1개 이상 담겨 있는 상태 | 1. 로그인 상태로 장바구니(`/view_cart`) 페이지에 진입한다.<br>2. "Proceed To Checkout" 버튼을 클릭한다.<br>3. 모달 노출 여부와 이동한 페이지 URL을 확인한다. | 별도 모달 없이 `https://automationexercise.com/checkout` 페이지로 바로 이동한다. | P1 | |
| TC-CART-012 | REQ-CART-010 | 장바구니 | `/checkout` 페이지의 Address Details 영역 배송지/청구지 정보가 수정/편집이 불가능한 표시 요소인지 확인 | 로그인 상태, `/checkout` 페이지 진입 상태 | 1. Address Details 영역의 배송지(Your Delivery Address)/청구지(Your Billing Address) 정보 텍스트를 클릭해 수정을 시도한다. | 배송지/청구지 정보 텍스트가 변경되지 않으며, 편집할 수 있는 입력 수단(입력 포커스 등)이 동작하지 않는다. | P2 | |
| TC-CART-013 | REQ-CART-010 | 장바구니 | `/checkout` 페이지의 Review Your Order 표 Quantity가 수정/편집이 불가능한 표시 요소인지 확인 | 로그인 상태, `/checkout` 페이지 진입 상태(장바구니에 상품이 1개 이상 담긴 상태) | 1. Review Your Order 표의 임의 상품 행 Quantity 칸을 클릭해 값 수정을 시도한다. | Quantity 값이 변경되지 않으며, 편집할 수 있는 입력 수단이 동작하지 않는다(Cart 페이지 Quantity와 동일하게 단순 표시 요소로 동작, REQ-CART-005 참조). | P2 | |
| TC-CART-014 | REQ-CART-011 | 장바구니 | 계정에 담긴 상품 유무와 무관하게 로그아웃 상태의 Cart 화면은 항상 빈 카트 상태로 보이는지 확인 | 로그인 상태에서 상품을 장바구니에 담아둔 테스트 계정이 존재함(예: actest1@test.com), 현재는 로그아웃 상태 | 1. 로그아웃 상태로 장바구니(`/view_cart`) 페이지에 진입한다.<br>2. 화면 상태를 확인한다. | 해당 계정에 실제로 담긴 상품이 있음에도 불구하고, 빈 카트 안내 상태("Cart is empty! Click here to buy products.")로 노출된다. | P1 | |
| TC-CART-015 | REQ-CART-012 | 장바구니 | 로그아웃 상태에서 담은 상품이 이후 로그인하면 해당 계정의 장바구니에 반영되어 노출되는지 확인 | 로그아웃 상태, 유효한 테스트 계정 보유(예: actest1@test.com) | 1. 로그아웃 상태에서 임의 상품을 장바구니에 담는다.<br>2. 로그인 페이지로 이동해 해당 테스트 계정으로 로그인한다.<br>3. 장바구니(`/view_cart`) 페이지로 이동해 상품 목록을 확인한다. | 로그아웃 상태에서 담았던 상품이 로그인한 계정의 장바구니에 반영되어 함께 노출된다. | P0 | |
| TC-CART-016 | REQ-CART-013 | 장바구니 | 로그인 상태에서 담은 상품이 로그아웃 후 동일 계정으로 재로그인하면 다시 유지되어 노출되는지 확인 | 로그인 상태(유효한 테스트 계정으로 로그인 완료, 예: actest1@test.com) | 1. 로그인 상태에서 임의 상품을 장바구니에 담는다.<br>2. 로그아웃한다.<br>3. 동일 테스트 계정으로 다시 로그인한다.<br>4. 장바구니(`/view_cart`) 페이지로 이동해 상품 목록을 확인한다. | 로그아웃 이전에 담아뒀던 상품이 재로그인 후 그대로 유지되어 노출된다. | P0 | |

> **REQ-CART-014 관련**: "로그인 여부에 따른 그 외의 차이는 'Proceed To Checkout' 클릭 시의 분기
> 동작(REQ-CART-008 vs REQ-CART-009)뿐이다"라는 요약성 진술이며, 그 자체로 독립적인 관찰 가능한
> 동작을 새로 정의하지 않으므로 별도 TC를 생성하지 않았다. TC-CART-010, TC-CART-011이 각각
> REQ-CART-008, REQ-CART-009의 분기 동작을 검증하므로 REQ-CART-014의 내용은 두 TC의 조합으로
> 커버된다고 판단했다(이 판단이 적절한지는 하단 "사용자 확인 필요 사항" 참조).

## 결함 의심 항목

> `tc-writing` Skill 4.6에 따라 확인이 필요한 섹션입니다. `cart.md` Feature PRD의 4.1/4.2/6절을
> 확인한 결과, "결함 의심"(비정상 동작이 관찰되었으나 정상/비정상 여부는 판정하지 않고 사실만
> 기록한 요구사항)으로 표시된 REQ 항목이 없었습니다. 이에 따라 이번 문서에는 별도 "결함 의심
> 항목" TC를 두지 않았습니다.

## Priority 산정 근거

- **TC-CART-001**: Impact 5 / Likelihood 4 / Risk Score 20 — 담기 확인 모달은 상품이 실제로
  담겼음을 사용자에게 알리는 유일한 피드백이며, `product-detail.md` TC-PRODUCT-DETAIL-015 등
  다른 Feature에서도 재사용되는 공유 컴포넌트의 최초 검증 지점이라 결함 발생 시 파급 범위가
  크다(Impact 5). 아이콘/제목/안내 문구/두 종류의 액션(링크, 버튼)이 하나의 모달에서 동시에
  정확히 구성되어야 하는 복합 시나리오라 발생 가능성도 높다(Likelihood 4).
- **TC-CART-002**: Impact 3 / Likelihood 2 / Risk Score 6 — 실패해도 페이지 이동이나 새로고침
  등으로 복구 가능한 수준의 UX 문제이며(Impact 3), 단순 버튼 클릭에 의한 모달 닫힘 이벤트라 결함
  발생 가능성은 낮다(Likelihood 2).
- **TC-CART-003**: Impact 3 / Likelihood 2 / Risk Score 6 — 실패해도 상단 네비게이션의 Cart
  메뉴로 동일한 목적지에 도달할 수 있는 대체 경로가 존재하며(Impact 3), 단순 링크 이동이라 결함
  발생 가능성은 낮다(Likelihood 2).
- **TC-CART-004**: Impact 5 / Likelihood 3 / Risk Score 15 — 서로 다른 진입 경로에서 담은
  상품이 하나의 장바구니로 병합되지 않으면, 사용자가 실제로는 담았음에도 결제 시 상품이 누락되는
  심각한 데이터 손실로 이어진다(Impact 5). 서로 다른 페이지 컨텍스트의 담기 액션이 동일한
  세션/계정 상태로 귀결되어야 하는 구조적 특성상 결함 발생 가능성이 일반 수준 이상이다
  (Likelihood 3).
- **TC-CART-005**: Impact 5 / Likelihood 4 / Risk Score 20 — Quantity/Total 누적 계산은 최종
  결제 금액에 직결되는 핵심 데이터 정합성 로직으로, 오류 발생 시 잘못된 금액으로 주문이 진행될 수
  있다(Impact 5). 기존 행을 찾아 병합할지 새 행을 추가할지 판단하는 로직과 Quantity/Total
  재계산이 결합되어 있어 결함 발생 가능성이 매우 높다(Likelihood 4).
- **TC-CART-006**: Impact 4 / Likelihood 3 / Risk Score 12 — 상세 페이지에서 지정한 수량이
  장바구니에 잘못 반영되면 주문 금액 오류로 이어질 수 있어 영향이 크며(Impact 4), 서로 다른
  페이지(상세 → 장바구니) 간 수량 값 전달 로직이라 리스트 페이지의 고정값(1개) 담기보다 결함
  발생 가능성이 높다(Likelihood 3).
- **TC-CART-007**: Impact 2 / Likelihood 2 / Risk Score 4 — 편집 불가가 PRD상 정상 동작이며 이를
  확인하는 Negative Case로, 실패(즉 편집 가능해짐)하더라도 사용자가 수량을 직접 조정할 수 있게
  되는 정도라 영향은 제한적이고(Impact 2), 단순 정적 표시 요소 확인이라 결함 발생 가능성도
  낮다(Likelihood 2).
- **TC-CART-008**: Impact 4 / Likelihood 3 / Risk Score 12 — 삭제가 실패하거나 엉뚱한 상품이
  삭제되면 사용자가 원치 않는 상품을 그대로 결제하게 되는 문제로 이어질 수 있어 영향이
  크며(Impact 4), 다건의 상품 중 특정 행만 식별해 삭제하는 로직이라 결함 발생 가능성이 일반
  수준 이상이다(Likelihood 3).
- **TC-CART-009**: Impact 3 / Likelihood 2 / Risk Score 6 — 빈 카트 안내 문구 자체는
  `page-ui.md`에서 이미 검증되었고 본 TC는 전체 삭제라는 트리거 조건만 추가로 확인하는 것이라
  영향은 제한적이며(Impact 3), 단순 조건부 렌더링 전환이라 결함 발생 가능성도 낮다
  (Likelihood 2).
- **TC-CART-010**: Impact 4 / Likelihood 3 / Risk Score 12 — 로그아웃 사용자의 체크아웃 진입을
  막는 중요한 접근 제어 로직으로, 실패 시 비로그인 사용자가 결제 절차로 잘못 진입할 수 있어
  영향이 크며(Impact 4), 로그인 상태 분기와 모달 컴포넌트 렌더링이 결합되어 있어 결함 발생
  가능성이 일반 수준 이상이다(Likelihood 3).
- **TC-CART-011**: Impact 5 / Likelihood 3 / Risk Score 15 — 로그인 사용자가 결제 절차로 진입하는
  유일한 경로이므로 실패 시 핵심 기능 사용이 불가능해지며(Impact 5), 로그인 상태 분기에 따른
  단순 리다이렉션 로직이라 발생 가능성은 일반 수준으로 평가한다(Likelihood 3).
- **TC-CART-012**: Impact 2 / Likelihood 2 / Risk Score 4 — TC-CART-007과 동일하게 Address
  Details 배송지/청구지 정보의 편집 불가가 정상 동작인 Negative Case로, 실패(즉 편집 가능해짐)해도
  단순 정보 노출 영역의 표시 오류 수준이라 영향은 제한적이고(Impact 2), 단순 정적 표시 요소 확인이라
  결함 발생 가능성도 낮다(Likelihood 2).
- **TC-CART-013**: Impact 2 / Likelihood 2 / Risk Score 4 — TC-CART-007과 동일하게 Review Your
  Order 표 Quantity의 편집 불가가 정상 동작인 Negative Case로 영향과 발생 가능성 모두 낮다.
- **TC-CART-014**: Impact 3 / Likelihood 3 / Risk Score 9 — 실제 데이터가 삭제되는 것은 아니지만
  사용자가 로그아웃할 때마다 장바구니가 비어 보이는 특이한 UX로 혼란을 줄 수 있으며(Impact 3),
  로그인 여부와 무관하게 항상 빈 화면으로 렌더링해야 하는 조건부 로직이라 결함 발생 가능성이
  일반 수준 이상이다(Likelihood 3).
- **TC-CART-015**: Impact 5 / Likelihood 4 / Risk Score 20 — 로그아웃 상태에서 담은 상품이
  로그인 시 반영되지 않으면 사용자가 담았던 상품을 그대로 잃게 되는 심각한 데이터
  손실이며(Impact 5), 비로그인 세션의 장바구니 데이터를 로그인 시점에 계정 데이터로 병합하는
  로직은 여러 데이터 소스 간 동기화가 필요해 결함 발생 가능성이 매우 높다(Likelihood 4).
- **TC-CART-016**: Impact 5 / Likelihood 4 / Risk Score 20 — 로그인 중 담아둔 상품이 재로그인 시
  복원되지 않으면 마찬가지로 심각한 데이터 손실로 이어지며(Impact 5), 계정에 연결된 장바구니
  데이터의 영속성/복원 로직이라 결함 발생 가능성이 매우 높다(Likelihood 4).

## 사용자 확인 필요 사항

1. **REQ-CART-014에 대한 별도 TC 미생성**: "로그인 여부에 따른 그 외의 차이는 없다"는 요약성
   진술로 판단해 별도 TC를 만들지 않고, TC-CART-010(REQ-CART-008)과 TC-CART-011
   (REQ-CART-009)의 조합으로 커버된다고 간주했습니다. 이 판단이 적절한지 확인 부탁드립니다.
   → **[확인 완료, 2026-08-22]** 사용자가 해당 판단(별도 TC 미생성)을 승인했습니다. 변경 없음.
2. **TC-CART-005 테스트 데이터**: PRD에 명시된 예시값("Sleeveless Dress", 단가 Rs.1000, 7회 담기
   → Quantity 7 / Total Rs. 7000)을 그대로 사용했습니다. 실제 테스트 수행 시점에 해당 상품의
   재고나 가격이 달라졌을 수 있어, 예시값을 그대로 고정할지 "사전에 단가를 확인한 임의 상품"으로
   유연하게 표현할지 확인 부탁드립니다.
   → **[확인 완료, 2026-08-22]** 사용자가 PRD 예시값을 그대로 사용하는 현재 방식을 승인했습니다.
   변경 없음.
3. **Priority 산정값**: 특히 P0로 산정한 TC-CART-001(담기 확인 모달), TC-CART-005(리스트 담기
   누적 계산), TC-CART-015/016(로그인 상태별 장바구니 병합/복원)의 Impact/Likelihood 평가에
   동의하시는지 확인 부탁드립니다.
   → **[확인 완료, 2026-08-22]** 사용자가 P0 포함 전체 Priority 산정값을 승인했습니다(TC-CART-015,
   016은 재번호 부여로 TC-CART-016, 017로 변경되었으나 산정 근거와 값은 동일하게 유지). 변경 없음.
4. **TC-CART-013 범위**: `/checkout` 페이지의 Address Details 편집 불가 여부와 Review Your Order
   Quantity 편집 불가 여부를 하나의 TC로 묶어 작성했습니다(둘 다 REQ-CART-010에서 "동일하게
   편집 불가"로 함께 기술됨). 두 검증 포인트를 별도 TC로 분리하는 것이 나을지 확인 부탁드립니다.
   → **[확인 완료, 2026-08-22]** 사용자가 분리를 요청하여, 기존 TC-CART-013을
   TC-CART-013(Address Details 배송지/청구지 정보 편집 불가 확인)과 TC-CART-014(Review Your
   Order 표 Quantity 편집 불가 확인) 2개로 분리했습니다. Requirement ID는 둘 다 REQ-CART-010을
   유지하고, Priority는 기존과 동일한 근거(Impact 2 / Likelihood 2 / Risk 4 / P2)를 각각
   적용했습니다. 분리에 따라 이후 TC ID가 한 칸씩 밀려 전체 TC ID를 001~017로 재부여했습니다.
5. **`page-ui.md`와의 경계**: TC-PAGE-UI-017~021(브레드크럼, 빈 카트 안내 문구, "Proceed To
   Checkout" 버튼 노출, 상품 목록 표 컬럼 구성)은 재작성하지 않고 필요한 곳(TC-CART-007,
   TC-CART-009, TC-CART-010)에 참조만 표기했습니다. 이 경계 설정이 적절한지 확인 부탁드립니다.
   → **[확인 완료, 2026-08-22]** `page-ui.md` Feature PRD/TC의 Checkout 페이지 범위 확장이
   완료되어 TC-PAGE-UI-034~041(Address Details, Review Your Order, 주문 코멘트 입력란, Place
   Order 버튼 등의 노출 확인)이 신규 추가됨에 따라, 기존 TC-CART-012(`/checkout` 페이지 진입 시
   Address Details/Review Your Order/주문 코멘트 입력란/Place Order 버튼 노출 확인 — 순수 화면
   구성요소 존재 여부 확인으로 page-ui.md 범위와 중복)를 본 문서에서 제거하고, 해당 검증은
   `page-ui.md` TC-PAGE-UI-034/036/037/038/039로 이관했습니다. 제거에 따라 이후 TC ID를
   001~016으로 재부여했습니다(기존 013→012, 014→013, 015→014, 016→015, 017→016). Address
   Details/Review Your Order 표의 read-only 동작 검증(기존 TC-CART-013/014, 현재
   TC-CART-012/013)은 화면 구성요소의 "존재 여부"가 아닌 "동작"(편집 시도 시 반응)을 검증하는
   것이므로 본 문서 범위에 그대로 유지했습니다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-22 | 최초 작성 (승인완료된 Feature PRD `cart.md`의 REQ-CART-001~013 기반 TC-CART-001~016 초안 작성. REQ-CART-014는 요약성 진술로 판단해 별도 TC 미생성. `page-ui.md` TC-PAGE-UI-017~021과 중복되는 화면 구성요소 노출 확인은 재작성하지 않고 참조만 표기) | 초안 |
| 2026-08-22 | 사용자 리뷰 피드백 반영 - TC-CART-013을 2개 TC로 분리(Address Details 편집 불가 확인 / Review Your Order Quantity 편집 불가 확인), 분리에 따라 이후 TC ID를 001~017로 재부여. REQ-CART-014 별도 TC 미생성 판단, TC-CART-005 테스트 데이터, Priority 산정값(P0 포함 전체) 승인 확정. `page-ui.md` 경계 항목(5번)은 page-ui PRD 확장 작업 완료 후 별도 처리 예정으로 처리 대기 중 유지 | 초안 |
| 2026-08-22 | page-ui Feature PRD/TC의 Checkout 페이지 범위 확장에 따라 TC-CART-012(화면 구성요소 노출 확인)를 page-ui.md TC-PAGE-UI-034~041로 이관하고 문서에서 제거, TC ID 재부여 001~016. 상단 경계 안내 문단에 checkout 페이지 화면 구성요소 확인을 page-ui.md TC-PAGE-UI-034~041에서 다룬다는 내용 추가. 사용자 확인 필요 사항 5번(`page-ui.md`와의 경계) 확인 완료로 정리 | 초안 |
| 2026-08-22 | 사용자 최종 승인 | 승인완료 |
