---
문서유형: Feature PRD
상태: 승인완료   # 초안 | 승인완료
관련 Project PRD: project-prd.md
최초 작성일: 2026-08-21
최근 변경일: 2026-08-21
승인일: 2026-08-21
---

# Feature PRD - 장바구니 (상품 담기 포함)

## 1. 개요

automationexercise.com에서 상품을 장바구니에 담는 동작(Home/Products 리스트 페이지 및 상품
상세 페이지에서의 "Add to cart"), 장바구니(`/view_cart`)에 담긴 상품에 대한 실제 조작(수량,
삭제), "Proceed To Checkout" 클릭 이후의 분기 동작, 그리고 로그인/로그아웃 상태에 따른 차이를
다룬다.

Cart 페이지의 화면 구성요소 자체(브레드크럼, 빈 카트 문구, 표 컬럼 구성 등 "존재 여부")는
`page-ui.md`에서 이미 다뤘으므로 본 문서에서는 재기술하지 않고, 그 구성요소를 조작했을 때의
실제 "동작"에 집중한다. 상품 상세 페이지 자체의 UI/기능은 향후 별도로 작성될 "상품 상세"
Feature PRD의 범위이며, 본 문서에서는 장바구니 담기 관점에서 확인된 사실(수량 지정 가능 여부)만
기록한다.

## 2. 관련 Project PRD 참조

- `/docs/prd/project-prd.md` (상태: 승인완료)
- Project PRD "5. 대상 Feature 목록" 및 "6. In Scope"의 "장바구니 (상품 담기 포함)" 항목에 해당
- Project PRD "7. Out of Scope"의 "결제 기능" 원칙에 따라, `/checkout` 페이지의 "Place Order"
  버튼 클릭 이후(실제 주문/결제 확정 절차)는 본 문서에서 다루지 않는다.
- Project PRD "8. 기타 제약사항 / 참고사항"의 "무작위 모달형 광고 노출 — 광고 관련 동작은 검증
  대상에서 제외" 원칙을 그대로 따른다.

**관련 Feature PRD (중복 기술하지 않고 참조만 함)**

- `/docs/prd/feature/page-ui.md` (승인완료)
  - REQ-PAGE-UI-013~016: Cart 페이지의 브레드크럼, 빈 카트 안내 문구, 상품 목록 표 컬럼 구성
    등 화면 구성요소의 "존재 여부"를 다룸. 본 문서는 이 구성요소들의 실제 "동작"만 다루며,
    구성요소 자체를 재기술하지 않는다. (7. 비고에 두 문서 간 관계를 별도로 설명)
- `/docs/prd/feature/login-logout.md`, `/docs/prd/feature/signup-delete-account.md`
  - 로그인/로그아웃/회원가입 절차 자체는 다루지 않으며, 본 문서에서는 "로그인 여부에 따른
    장바구니 동작 차이"만 다룬다.
- `/docs/prd/feature/top-navigation.md`
  - 상단 네비게이션 Cart 메뉴 자체의 동작(이동 URL 등)은 다루지 않는다.
- "상품 상세" Feature PRD (미작성, 향후 별도 작성 예정)
  - 상품 상세 페이지 자체의 UI/레이아웃/상세 기능은 다루지 않으며, 본 문서에서는 "상품 상세
    페이지에서는 담을 개수를 지정하여 담을 수 있다"는 사실만 장바구니 Feature 관점에서 기록한다.

## 3. 사용자 조작 시나리오

1. 로그아웃 상태에서 Home 페이지와 Products 페이지 각각의 상품 카드에서 "Add to cart" 버튼을
   클릭해 담기 동작과 확인 모달을 확인한다.
2. 동일 상품을 여러 번 담아 장바구니에서 수량이 어떻게 누적되는지, Home/Products 각 페이지에서
   담은 상품이 같은 장바구니에 함께 누적되는지 확인한다.
3. 상품 상세 페이지에서 담을 개수를 지정해 장바구니에 담고, 리스트 페이지에서 담을 때와의 차이를
   확인한다.
4. 장바구니 페이지(`/view_cart`)에서 담긴 상품의 Quantity 값 변경을 시도하고, 삭제(x) 버튼을
   클릭해 실제 삭제 동작을 확인한다. 모든 상품을 삭제했을 때의 화면 상태도 확인한다.
5. 로그아웃 상태와 로그인 상태 각각에서 "Proceed To Checkout" 버튼을 클릭해 나타나는 화면을
   비교한다. 로그인 상태에서는 이동한 `/checkout` 페이지의 구성을 확인한다.

## 4. Requirements

### 4.1 확인된 요구사항

**상품 담기 (Add to cart)**

- **REQ-CART-001**: Home/Products 리스트 페이지의 상품 카드에서 "Add to cart" 버튼을 클릭하면
  담기 확인 모달이 노출된다. 모달 구성은 초록색 체크 아이콘, "Added!" 제목, "Your product has
  been added to cart." 안내 문구, "View Cart" 링크(파란색 텍스트), 하단 초록색 "Continue
  Shopping" 버튼이다. 이 모달에서 "Continue Shopping" 버튼을 클릭하면 모달만 닫히고 담기를
  시도했던 페이지가 그대로 유지되어 노출되며, "View Cart" 링크를 클릭하면 장바구니(`/view_cart`)
  페이지로 이동한다.
- **REQ-CART-002**: Home 페이지에서 담은 상품과 Products 페이지에서 담은 상품은 동일한
  장바구니에 함께 누적된다.
- **REQ-CART-003**: Home/Products 리스트 페이지의 "Add to cart" 버튼으로는 담을 개수를 지정할
  수 없고 항상 1개씩만 담긴다. 동일 상품을 여러 번 담으면 장바구니에서 별도 행으로 추가되지
  않고 기존 행의 Quantity가 1씩 누적된다(예: "Sleeveless Dress" 상품을 7회 담은 결과 Quantity
  7, Total Rs. 7000(단가 Rs.1000 x 7)으로 표시됨을 확인).
- **REQ-CART-004**: 상품 상세 페이지에서는 (리스트 페이지의 "Add to cart"와 달리) 담을 개수를
  직접 지정해서 장바구니에 담을 수 있다(예: 한 번에 7개 지정해 담기). 상품 상세 페이지 자체의
  UI 구성(수량 입력란 위치 등)은 본 문서 범위가 아니며, 장바구니 Feature 관점에서 "수량 지정이
  가능하다"는 사실만 기록한다.

**장바구니 조작 (`/view_cart`)**

- **REQ-CART-005**: 장바구니 페이지의 Quantity 칸은 숫자가 박스 안에 표시되어 입력란처럼
  보이지만, 실제로는 값을 편집할 수 없는 표시 전용 요소이다. 특정 상품의 담긴 수량을 변경하는
  방법 자체가 존재하지 않는다.
- **REQ-CART-006**: 장바구니에서 특정 상품의 수량을 조정할 수는 없으며, 각 행의 삭제(x) 버튼을
  클릭해 해당 상품을 장바구니에서 완전히 삭제하는 것만 가능하다.
- **REQ-CART-007**: 장바구니에 담긴 상품을 모두 삭제하면 화면이 빈 카트 상태(`page-ui.md`
  REQ-PAGE-UI-014의 "Cart is empty! Click here to buy products." 안내 문구)로 전환된다.

**Proceed To Checkout**

- **REQ-CART-008**: 로그아웃 상태에서 "Proceed To Checkout" 버튼을 클릭하면 로그인/회원가입을
  요구하는 모달이 노출된다. 모달 구성은 사람 아이콘, "Checkout" 제목, "Register / Login account
  to proceed on checkout." 안내 문구, "Register / Login" 링크, 하단 초록색 "Continue On Cart"
  버튼이다.
- **REQ-CART-009**: 로그인 상태에서 "Proceed To Checkout" 버튼을 클릭하면 모달 없이 바로
  `https://automationexercise.com/checkout` 페이지로 이동한다.
- **REQ-CART-010**: `/checkout` 페이지에는 "Address Details" 영역(Your Delivery Address, Your
  Billing Address — 회원가입 시 입력한 이름/주소 정보가 자동으로 표시됨), "Review Your Order"
  영역(장바구니와 동일한 Item/Description/Price/Quantity/Total 표 및 Total Amount), 주문
  코멘트 입력용 텍스트 영역, 하단 "Place Order" 버튼이 노출된다. "Place Order" 버튼 클릭 이후의
  실제 주문/결제 확정 절차는 본 문서 범위에 포함하지 않는다(5. Out of Scope, 7. 비고 참조).
  Address Details의 배송지/청구지 정보와 Review Your Order 표의 Quantity는 모두 Cart 페이지와
  동일하게 수정/편집이 불가능한 단순 표시 요소이다.

**로그인 상태별 차이**

- **REQ-CART-011**: 상품을 장바구니에 담고 Cart 페이지에 진입하는 동작 자체는 로그인/로그아웃
  상태와 무관하게 가능하다. 다만 로그아웃 상태의 Cart 화면은 실제 계정에 연결된 장바구니 내역과
  무관하게 항상 비어있는 것처럼(빈 카트 상태로) 보인다.
- **REQ-CART-012**: 로그아웃 상태에서 상품을 담은 뒤 로그인하면, 로그인한 계정의 Cart에
  로그아웃 상태에서 담았던 상품이 반영되어 함께 노출된다(로그인 시점에 계정 Cart로 병합됨).
- **REQ-CART-013**: 로그인 상태에서 상품을 담은 채로 로그아웃하면 그 직후 Cart 화면은
  REQ-CART-011에 따라 비어있는 것처럼 보이지만, 이후 동일 계정으로 다시 로그인하면 이전에
  담아뒀던 상품이 다시 유지되어 노출된다. 즉 계정에 연결된 장바구니 내용 자체는 로그인 시점에
  유지/복원되는 것으로 관찰된다.
- **REQ-CART-014**: 로그인 여부에 따른 그 외의 차이는 "Proceed To Checkout" 클릭 시의 분기
  동작(REQ-CART-008 vs REQ-CART-009)뿐이다.

### 4.2 미확인 / 추가 확인 필요 항목

- 현재 없음 (이전에 제기되었던 미확인 항목 4건 모두 사용자 확인 완료됨)

## 5. Feature 단위 In Scope / Out of Scope

**In Scope**

- Home/Products 리스트 페이지에서의 "Add to cart" 동작(수량 미지정 담기, 담기 확인 모달 노출)
- 장바구니 내 상품 누적 방식(서로 다른 페이지에서 담은 상품의 통합 누적, 동일 상품 재담기 시
  수량 누적)
- 상품 상세 페이지의 "장바구니 담기 시 수량 지정 가능" 사실 (상세 페이지 자체 UI/기능 제외)
- Cart 페이지(`/view_cart`)에서의 실제 동작: Quantity 편집 불가 여부, 삭제(x) 버튼 동작, 전체
  삭제 시 빈 카트 상태 전환
- "Proceed To Checkout" 클릭 시 로그인 상태별 분기 동작(로그인 요구 모달 vs `/checkout` 이동)
- `/checkout` 페이지 진입 및 화면 구성 확인 (Address Details, Review Your Order, 주문 코멘트,
  Place Order 버튼의 노출 여부까지 — "Place Order" 클릭 이전까지)
- 로그인/로그아웃 상태에 따른 장바구니 담기·조회·체크아웃 진입 동작 차이(로그아웃 상태 Cart
  화면의 빈 카트 표시, 로그인 시점의 계정 Cart 병합/복원 동작 포함)

**Out of Scope**

- 상품 상세 페이지 자체의 UI/레이아웃/기타 기능 — 향후 별도 작성될 "상품 상세" Feature PRD
  범위 (사용자 확정 사항)
- Cart 페이지의 화면 구성요소 자체("존재 여부") — `page-ui.md` 범위 (7. 비고 참조)
- 로그인/회원가입/계정삭제 절차 자체 — `login-logout.md`, `signup-delete-account.md` 범위
- 상단 네비게이션 자체의 동작 — `top-navigation.md` 범위
- `/checkout` 페이지의 "Place Order" 버튼 클릭 이후 실제 주문/결제 확정 절차 — Project PRD
  "7. Out of Scope"의 결제 기능 제외 원칙에 해당하며, 사용자도 이 부분을 실측하지 않음
  (7. 비고 참조)
- 광고 배너 등 automationexercise.com 고유 UI가 아닌 요소 (Project PRD "8. 기타 제약사항"의
  광고 제외 원칙에 따름)

## 6. 예외 / 에러 케이스

- 로그아웃 상태에서 "Proceed To Checkout" 클릭 시 결제 진행 대신 로그인/회원가입을 요구하는
  모달이 노출되는 케이스 (REQ-CART-008)
- 장바구니 Quantity가 편집 불가능한 표시 전용 요소이므로, 수량 값에 대한 별도의 최소/최대치
  검증이나 숫자 외 입력 방지 등의 검증 케이스 자체가 존재하지 않음 (REQ-CART-005, REQ-CART-006)
- 장바구니에 담긴 상품을 모두 삭제했을 때 빈 카트 안내 상태로 전환되는 케이스 (REQ-CART-007)

## 7. 비고

- **page-ui.md와의 관계**: `page-ui.md`의 REQ-PAGE-UI-016은 Cart 페이지 상품 목록 표에 "수량
  입력란 형태"의 Quantity 칸이 "존재한다"는 사실만 다뤘으며, 실제 값 변경 가능 여부(동작)는
  명시적으로 본 문서로 위임되어 있었다(page-ui.md 4.1, 5. Out of Scope, 7. 비고 참조). 이번
  실측을 통해 해당 Quantity 칸이 실제로는 편집이 불가능한 표시 전용 요소임이 확인되었다
  (REQ-CART-005). 이는 page-ui.md의 "구성요소 존재 여부" 기술과 모순되는 것이 아니라, 이번
  문서가 다루는 "실제 동작" 정보로 그 구성요소를 보완하는 것이다. page-ui.md 본문은 수정하지
  않았다.
- **"Place Order" 이후를 Out of Scope로 처리한 근거**: `/checkout` 페이지 진입 및 화면 구성
  (Address Details, Review Your Order 등)까지는 사용자가 직접 관찰한 사실이므로 본 문서
  Requirements에 포함했다(REQ-CART-010). 다만 "Place Order" 버튼 클릭 이후의 실제 주문/결제
  확정 절차는 (1) 사용자가 실측하지 않았고, (2) Project PRD "7. Out of Scope"에 명시된 "결제
  기능" 제외 원칙에 정확히 해당하므로, 별도 확인 질문 없이 Out of Scope로 처리했다.
- **상품 상세 페이지 관련 경계**: 상품 상세 페이지의 존재와 "장바구니 담기 시 수량 지정 가능"
  사실(REQ-CART-004)만 장바구니 Feature 관점에서 기록했다. 해당 페이지 자체의 레이아웃, 다른
  기능(리뷰, 관련 상품 등)은 향후 작성될 "상품 상세" Feature PRD에서 다뤄야 할 범위로 판단해
  본 문서에 포함하지 않았다.
- 스크린샷에서 관찰된 "SUDDEN ATTACK", "Marriott Resort", "IPFoxy Proxies", "maplestory
  WORLDS", "고려기프트", "inflearn" 등의 광고 배너는 Project PRD "8. 기타 제약사항"의 광고 제외
  원칙에 따라 Requirements에 포함하지 않았다.
- **로그인 상태에 따른 장바구니 유지 동작(REQ-CART-011~013)**: 최초 작성 시 4.2 미확인
  항목이었으나, 사용자가 직접 확인해 로그아웃 상태의 Cart 화면은 항상 비어있는 것처럼 보이는
  반면, 실제 계정에 연결된 장바구니 내용은 로그인 시점에 병합/복원된다는 다소 복합적인 동작이
  확정되었다. 하나의 REQ로 뭉뚱그리지 않고 (1) 로그아웃 상태 Cart 화면의 표시 동작,
  (2) 로그아웃 중 담은 상품의 로그인 시 반영, (3) 로그인 중 담은 상품의 로그아웃 후 재로그인 시
  복원으로 나누어 각각 REQ-CART-011~013으로 분리 기술했다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-21 | 최초 작성 (Draft) — 사용자 실측(스크린샷) 결과 반영, REQ-CART-001~011 및 4.2 미확인 항목 4건 정리 | 초안 |
| 2026-08-21 | 4.2 미확인 항목 4건 모두 사용자 확인 완료 반영: REQ-CART-001에 모달 버튼("Continue Shopping"/"View Cart") 동작 추가, REQ-CART-010에 Address Details/Review Your Order Quantity 편집 불가 내용 추가, 로그인 상태별 장바구니 유지 동작을 REQ-CART-011~014로 확장/분리(로그아웃 시 빈 화면 표시, 로그인 시 계정 Cart 병합/복원 포함), 4.2를 "현재 없음"으로 정리 | 초안 |
| 2026-08-21 | 사용자 최종 승인 | 승인완료 |
