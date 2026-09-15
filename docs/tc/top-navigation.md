---
문서유형: Test Case
상태: 승인완료   # 초안 | 승인완료
관련 Feature PRD: feature/top-navigation.md
최초 작성일: 2026-08-22
최근 변경일: 2026-08-22
승인일: 2026-08-22
---

# Test Case - 상단 네비게이션

## TC 목록

> 공통 Preconditions: 사이트 진입 시 또는 일정 시간 경과 시 무작위로 노출될 수 있는 모달형 광고는
> Project PRD "8. 기타 제약사항" 원칙에 따라 검증 대상이 아니므로, 모든 TC 수행 전 광고 모달이
> 노출된 경우 닫은 상태에서 진행한다(아래 표에는 반복 기재하지 않음).
>
> 본 문서는 네비게이션 메뉴 자체의 이동 동작(이동 URL, 활성 표시, "Logged in as {유저명}" UI
> 요소)을 다룬다. 로그인 성공/로그아웃 처리 시점의 메뉴 구성 전환 자체(로그인 직후 로그아웃 상태
> 메뉴 → 로그인 상태 메뉴 전환, 로그아웃 직후의 역전환)는 `login-logout.md`
> TC-LOGIN-LOGOUT-004, 014, 015에서 이미 검증되며, 본 문서는 그 결과인 "이미 확립된 상태"에서의
> 메뉴 동작(클릭 시 이동 URL, 페이지 이동 간 일관성, 활성 표시)에 집중한다. 또한
> REQ-TOP-NAVIGATION-004(로그아웃 상태에서 Signup/Login 메뉴 클릭 시 `/login` 이동)는
> TC-LOGIN-LOGOUT-002("상단 네비게이션 'Signup/Login' 클릭을 통한 로그인 페이지 접근")에서 동일한
> 검증 목적으로 이미 다뤄지고 있어(`tc-writing` Skill 4.1 중복 방지 원칙), 본 문서에서 별도 TC를
> 생성하지 않고 TC-LOGIN-LOGOUT-002를 참조한다.

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-TOP-NAVIGATION-001 | REQ-TOP-NAVIGATION-001 | 상단 네비게이션 | 로그인 상태 여부와 무관하게 상단 네비게이션 "Home" 메뉴 클릭 시 이동 URL이 동일한지 확인 | 유효한 테스트 계정 보유(예: actest1@test.com), Home이 아닌 임의 페이지(예: Products)로 이동 가능한 상태 | 1. 로그아웃 상태로 Products(`/products`) 페이지에 진입해 상단 네비게이션의 "Home" 메뉴를 클릭하고 이동한 URL을 확인한다.<br>2. 유효한 테스트 계정으로 로그인한 뒤 Products(`/products`) 페이지로 이동해 상단 네비게이션의 "Home" 메뉴를 클릭하고 이동한 URL을 확인한다. | 로그인 상태 여부와 무관하게 `https://automationexercise.com/`(Home)으로 동일하게 이동한다. | P2 | |
| TC-TOP-NAVIGATION-002 | REQ-TOP-NAVIGATION-002 | 상단 네비게이션 | 로그인 상태 여부와 무관하게 상단 네비게이션 "Products" 메뉴 클릭 시 이동 URL이 동일한지 확인 | 유효한 테스트 계정 보유(예: actest1@test.com), Products가 아닌 임의 페이지(예: Home)로 이동 가능한 상태 | 1. 로그아웃 상태로 Home(`/`) 페이지에서 상단 네비게이션의 "Products" 메뉴를 클릭하고 이동한 URL을 확인한다.<br>2. 유효한 테스트 계정으로 로그인한 뒤 Home(`/`) 페이지로 이동해 상단 네비게이션의 "Products" 메뉴를 클릭하고 이동한 URL을 확인한다. | 로그인 상태 여부와 무관하게 `https://automationexercise.com/products`로 동일하게 이동한다. | P2 | |
| TC-TOP-NAVIGATION-003 | REQ-TOP-NAVIGATION-003 | 상단 네비게이션 | 로그인 상태 여부와 무관하게 상단 네비게이션 "Cart" 메뉴 클릭 시 이동 URL이 동일한지 확인 | 유효한 테스트 계정 보유(예: actest1@test.com), Cart가 아닌 임의 페이지(예: Home)로 이동 가능한 상태 | 1. 로그아웃 상태로 Home(`/`) 페이지에서 상단 네비게이션의 "Cart" 메뉴를 클릭하고 이동한 URL을 확인한다.<br>2. 유효한 테스트 계정으로 로그인한 뒤 Home(`/`) 페이지로 이동해 상단 네비게이션의 "Cart" 메뉴를 클릭하고 이동한 URL을 확인한다. | 로그인 상태 여부와 무관하게 `https://automationexercise.com/view_cart`로 동일하게 이동한다. | P2 | |
| TC-TOP-NAVIGATION-004 | REQ-TOP-NAVIGATION-005 | 상단 네비게이션 | 로그인 상태에서 Home/Products/Cart 페이지를 이동해도 상단 네비게이션 메뉴 구성과 "Logged in as {유저명}" 표시가 동일하게 유지되는지 확인 | 유효한 테스트 계정으로 로그인 완료(예: actest1@test.com) | 1. 로그인 상태로 Home(`/`) 페이지에 진입해 상단 네비게이션의 메뉴 구성과 "Logged in as {유저명}" 표시를 확인한다.<br>2. Products(`/products`) 페이지로 이동해 동일한 항목을 다시 확인한다.<br>3. Cart(`/view_cart`) 페이지로 이동해 동일한 항목을 다시 확인한다. | 세 페이지 모두에서 상단 네비게이션 메뉴 구성(Home, Products, Cart, Logout, Delete Account, Test Cases, API Testing, Video Tutorials, Contact us)과 "Logged in as {유저명}" 표시가 동일하게 유지된다. | P1 | |
| TC-TOP-NAVIGATION-005 | REQ-TOP-NAVIGATION-005 | 상단 네비게이션 | 로그아웃 상태에서 Home/Products/Cart 페이지를 이동해도 상단 네비게이션 메뉴 구성이 동일하게 유지되는지 확인 | 로그아웃 상태 | 1. 로그아웃 상태로 Home(`/`) 페이지에 진입해 상단 네비게이션의 메뉴 구성을 확인한다.<br>2. Products(`/products`) 페이지로 이동해 동일한 항목을 다시 확인한다.<br>3. Cart(`/view_cart`) 페이지로 이동해 동일한 항목을 다시 확인한다. | 세 페이지 모두에서 상단 네비게이션 메뉴 구성(Home, Products, Cart, Signup/Login, Test Cases, API Testing, Video Tutorials, Contact us)이 동일하게 유지된다. | P2 | |
| TC-TOP-NAVIGATION-006 | REQ-TOP-NAVIGATION-006 | 상단 네비게이션 | "Logged in as {유저명}"의 유저명이 회원가입 시 입력한 Name 값과 동일하게 노출되는지 확인 | 기존 테스트 계정 재사용(예: actest1@test.com, 회원가입 시 입력했던 Name 값을 비교 기준으로 미리 확인해 둠) | 1. 해당 테스트 계정이 회원가입 시 입력했던 Name 값을 비교 기준으로 확인해 둔다.<br>2. 해당 계정으로 로그인한 뒤 상단 네비게이션의 "Logged in as {유저명}" 표시를 확인한다. | "Logged in as" 뒤에 표시되는 유저명이 해당 계정이 회원가입 시 입력한 Name 값과 동일하다. | P1 | |
| TC-TOP-NAVIGATION-007 | REQ-TOP-NAVIGATION-007 | 상단 네비게이션 | 현재 위치한 페이지에 해당하는 메뉴 항목이 주황색으로 활성 표시되는지 확인 | 로그인/로그아웃 상태 무관 | 1. Products(`/products`) 페이지로 진입한다.<br>2. 상단 네비게이션의 "Products" 메뉴 항목 색상을 확인한다. | "Products" 메뉴 항목이 다른 메뉴 항목과 달리 주황색으로 활성 표시된다. | P2 | |
| TC-TOP-NAVIGATION-008 | REQ-TOP-NAVIGATION-008 | 상단 네비게이션 | 마우스 오버(hover) 시 모든 네비게이션 메뉴 항목이 동일하게 주황색으로 활성 표시되는지 확인 | 로그인/로그아웃 상태 무관, 현재 위치한 페이지에 해당하지 않는(비활성 상태인) 메뉴 항목이 존재하는 상태 | 1. Home(`/`) 페이지에 진입한 상태에서 현재 위치("Home")가 아닌 임의 메뉴 항목(예: "Products")에 마우스를 올린다(hover).<br>2. 해당 메뉴 항목의 색상을 확인한다. | hover한 메뉴 항목이 주황색으로 활성 표시된다. | P2 | |
| TC-TOP-NAVIGATION-009 | REQ-TOP-NAVIGATION-009 | 상단 네비게이션 | 현재 위치한 페이지의 메뉴 항목은 마우스를 올리지 않아도(hover하지 않아도) 활성 표시가 유지되는지 확인 | 로그인/로그아웃 상태 무관 | 1. Products(`/products`) 페이지에 진입한다.<br>2. 마우스를 "Products" 메뉴 항목이 아닌 다른 위치(예: 페이지 본문)에 둔 상태에서 "Products" 메뉴 항목의 색상을 확인한다. | 마우스를 올리지 않은 상태에서도 "Products" 메뉴 항목이 계속 주황색으로 활성 표시된다. | P2 | |
| TC-TOP-NAVIGATION-010 | REQ-TOP-NAVIGATION-010 | 상단 네비게이션 | 로그인 상태 메뉴 중 "Logout"과 "Delete Account" 항목이 기본 상태에서 다른 메뉴와 달리 빨간색 계열로 표시되는지 확인 | 로그인 상태(유효한 테스트 계정으로 로그인 완료, 예: actest1@test.com) | 1. 로그인 상태로 Home(`/`) 페이지에 진입한다.<br>2. 마우스를 올리지 않은 기본 상태에서 상단 네비게이션의 "Logout", "Delete Account" 메뉴 항목과 다른 메뉴 항목(예: "Home", "Products")의 텍스트/아이콘 색상을 비교한다. | "Logout"과 "Delete Account"는 빨간색 계열로 표시되고, 그 외 메뉴 항목은 회색/검정 계열로 표시되어 시각적으로 구분된다. | P2 | |
| TC-TOP-NAVIGATION-011 | REQ-TOP-NAVIGATION-011 | 상단 네비게이션 | "Logged in as {유저명}" 텍스트를 클릭해도 별도 동작이 발생하지 않는지 확인 | 로그인 상태(유효한 테스트 계정으로 로그인 완료, 예: actest1@test.com) | 1. 로그인 상태로 임의 페이지에 진입한다.<br>2. 상단 네비게이션의 "Logged in as {유저명}" 텍스트를 클릭한다.<br>3. 클릭 이후 화면 상태(URL, 페이지 이동 여부)를 확인한다. | 페이지 이동이나 별도 모달 노출 등 어떠한 동작도 발생하지 않고 현재 페이지가 그대로 유지된다. | P2 | |

> **REQ-TOP-NAVIGATION-004 관련**: "로그아웃 상태에서 Signup/Login 메뉴 클릭 시 `/login`으로
> 이동한다"는 요구사항은 `login-logout.md` TC-LOGIN-LOGOUT-002("상단 네비게이션 'Signup/Login'
> 클릭을 통한 로그인 페이지 접근")에서 동일한 검증 목적(대상 메뉴, 클릭 동작, 기대 이동 URL이
> 모두 동일)으로 이미 다뤄지고 있어, `tc-writing` Skill 4.1(중복 TC 방지) 기준에 따라 본 문서에
> 별도 TC를 생성하지 않았다. 이 판단이 적절한지는 하단 "사용자 확인 필요 사항" 참조.

## 결함 의심 항목

> `tc-writing` Skill 4.6에 따라 확인이 필요한 섹션입니다. Feature PRD `top-navigation.md`의
> 4.1/4.2/6절을 확인한 결과, 본 문서(상단 네비게이션 자체)에 대해 "결함 의심"으로 새로 발급된
> Requirement는 없습니다. PRD 6절에서 로그아웃 상태의 `/delete_account` URL 직접 접근 시
> "ACCOUNT DELETED!" 성공 페이지가 노출되는 현상을 언급하지만, 이는
> `signup-delete-account.md`의 REQ-SIGNUP-DELETE-ACCOUNT-017에 이미 기술된 결함 의심 사항과
> 동일한 것으로 PRD가 명시적으로 참조만 하고 있으며, 본 문서 범위에서 새 Requirement로 발급하지
> 않는다고 확정했습니다(해당 페이지에서 네비게이션 자체는 정상적인 로그아웃 상태 메뉴로 노출됨이
> 확인되어 네비게이션 자체의 결함으로 다루지 않음). 따라서 이번 문서에는 별도 "결함 의심 항목" TC를
> 두지 않았습니다. `signup-delete-account.md` Feature TC 작성 시 해당 결함 의심 사항이 별도로
> 다뤄질 예정입니다.

## Priority 산정 근거

- **TC-TOP-NAVIGATION-001**: Impact 3 / Likelihood 2 / Risk Score 6 — Home 이동 실패 시에도
  브라우저 뒤로가기, URL 직접 입력 등 대체 수단이 있고, 로그인/로그아웃 직후 자동으로 Home에
  랜딩되는 경우가 많아 상대적으로 사용 빈도가 낮다(Impact 3). 두 상태(로그인/로그아웃) 모두 동일한
  단순 정적 링크 클릭 동작이라 결함 발생 가능성은 낮다(Likelihood 2).
- **TC-TOP-NAVIGATION-002**: Impact 4 / Likelihood 2 / Risk Score 8 — 전체 상품 목록으로 이동하는
  핵심 진입 경로이며 PRD상 확인된 대체 경로가 제한적이라, 실패 시 상품 탐색 자체가 어려워질 수
  있다(Impact 4). 단순 정적 링크 클릭 동작이라 결함 발생 가능성은 낮다(Likelihood 2).
- **TC-TOP-NAVIGATION-003**: Impact 3 / Likelihood 2 / Risk Score 6 — 담기 확인 모달의 "View
  Cart" 링크(`cart.md` TC-CART-003)라는 대체 경로가 이미 검증되어 있어 완전히 차단되지는
  않는다(Impact 3). 단순 정적 링크 클릭 동작이라 결함 발생 가능성은 낮다(Likelihood 2).
- **TC-TOP-NAVIGATION-004**: Impact 4 / Likelihood 3 / Risk Score 12 — 페이지마다 메뉴 구성이나
  "Logged in as" 표시가 달라지면 사용자가 자신의 로그인 상태를 신뢰하기 어려워지는 등 서비스
  신뢰성에 영향을 준다(Impact 4). 여러 페이지를 순회하며 두 종류의 렌더링 조건(메뉴 구성,
  "Logged in as")을 함께 검증해야 하는 시나리오라 결함 발생 가능성이 일반 수준
  이상이다(Likelihood 3).
- **TC-TOP-NAVIGATION-005**: Impact 3 / Likelihood 2 / Risk Score 6 — 로그인 상태(TC-004) 대비
  검증할 표시 요소("Logged in as")가 없어 영향 범위가 상대적으로 작다(Impact 3). 단순 메뉴 구성
  비교로 결함 발생 가능성은 낮다(Likelihood 2).
- **TC-TOP-NAVIGATION-006**: Impact 4 / Likelihood 3 / Risk Score 12 — 잘못된 사용자명이 표시되면
  개인화 정보의 신뢰성이 크게 훼손된다(Impact 4). 회원가입 시 입력값과 로그인 세션의 표시값을
  연결하는 데이터 흐름이라 결함 발생 가능성이 일반 수준 이상이다(Likelihood 3).
- **TC-TOP-NAVIGATION-007**: Impact 2 / Likelihood 2 / Risk Score 4 — 시각적 하이라이트 표시로
  기능 자체 사용에는 지장이 없는 UI 요소이다(Impact 2). 단순 조건부 스타일 적용이라 결함 발생
  가능성은 낮다(Likelihood 2).
- **TC-TOP-NAVIGATION-008**: Impact 1 / Likelihood 2 / Risk Score 2 — 마우스 오버 시각 효과로
  사용자 영향이 매우 낮다(Impact 1). 일반적인 hover 스타일 구현이나 모든 메뉴 항목에 대한 일관
  적용 여부를 확인해야 해 약간의 결함 발생 가능성이 있다(Likelihood 2).
- **TC-TOP-NAVIGATION-009**: Impact 2 / Likelihood 2 / Risk Score 4 — TC-007과 동일하게 시각적 UI
  요소이다(Impact 2). 현재 페이지 상태 값에 따른 조건부 스타일 유지 로직이라 결함 발생 가능성은
  일반적 수준이다(Likelihood 2).
- **TC-TOP-NAVIGATION-010**: Impact 2 / Likelihood 1 / Risk Score 2 — 시각적 스타일 차이로 기능
  자체에는 영향이 없다(Impact 2). 정적 스타일 속성 확인이라 결함 발생 가능성은 매우
  낮다(Likelihood 1).
- **TC-TOP-NAVIGATION-011**: Impact 1 / Likelihood 1 / Risk Score 1 — 클릭해도 아무 동작이 없어야
  하는 Negative Case로, 실패(즉 의도치 않은 동작 발생)하더라도 영향이 낮다(Impact 1). 링크가 아닌
  단순 텍스트 요소로 결함 발생 가능성이 매우 낮다(Likelihood 1).

## 사용자 확인 필요 사항

1. **TC-TOP-NAVIGATION-001~003 상태 결합 설계**: Home/Products/Cart 메뉴는 PRD상 "로그인/로그아웃
   상태와 무관하게" 동일한 URL로 이동해야 한다는 단일 요구사항이므로, 로그인 상태와 로그아웃
   상태를 각각 별도 TC로 분리하지 않고 하나의 TC 안에서 2단계 Test Steps로 순차 검증하도록
   설계했습니다(`cart.md`, `page-ui.md`에서 상태별로 TC를 분리했던 사례와는 다른 방식입니다 — 그
   사례들은 상태에 따라 기대 결과 자체가 달랐던 반면, 이 3개 TC는 두 상태의 기대 결과가 완전히
   동일하기 때문입니다). 이 설계 방식이 적절한지, 혹은 다른 TC들과의 일관성을 위해 상태별로 TC를
   분리하는 것을 선호하시는지 확인 부탁드립니다.
   → **확인 완료(2026-08-22)**: 하나의 TC 안에서 두 상태를 순차 검증하는 설계는 유지하되,
   Test Scenario/Preconditions 문구를 "로그인 상태 여부와 무관하게 ... 동일한지 확인"과 같이
   TC-007 등에서 쓰는 "상태 무관" 표기 관례에 맞춰 수정하기로 확정. TC-001~003 Test Scenario를
   각각 "로그인 상태 여부와 무관하게 상단 네비게이션 'Home/Products/Cart' 메뉴 클릭 시 이동
   URL이 동일한지 확인"으로, Expected Result도 동일한 취지로 다듬어 반영함(Test Steps/Priority는
   변경 없음).
2. **REQ-TOP-NAVIGATION-004 별도 TC 미생성**: 위 TC 목록 하단 설명과 같이, 해당 요구사항은
   `login-logout.md` TC-LOGIN-LOGOUT-002가 이미 동일하게 검증하고 있다고 판단해 본 문서에 별도
   TC를 생성하지 않았습니다. 이 판단에 동의하시는지 확인 부탁드립니다.
   → **확인 완료(2026-08-22)**: 동의. 변경 없음.
3. **Priority 산정값**: 위 "Priority 산정 근거"에 제시된 각 TC의 Impact/Likelihood 평가와 최종
   Priority(P0 없음, P1 2건 — TC-004, TC-006, 나머지 P2)에 동의하시는지 확인 부탁드립니다.
   → **확인 완료(2026-08-22)**: 동의. 변경 없음.
4. **결함 의심 항목 부재**: 위 "결함 의심 항목" 섹션의 판단(본 문서 범위에서는 별도 TC를 두지
   않고, 관련 결함 의심 사항은 `signup-delete-account.md`에서 다룰 예정)에 동의하시는지 확인
   부탁드립니다.
   → **확인 완료(2026-08-22)**: 동의. 변경 없음.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-22 | 최초 작성 (승인완료된 Feature PRD `top-navigation.md`의 REQ-TOP-NAVIGATION-001~011 기반 TC-TOP-NAVIGATION-001~011 초안 작성. REQ-TOP-NAVIGATION-004는 `login-logout.md` TC-LOGIN-LOGOUT-002와 중복 검증 목적으로 판단해 별도 TC 미생성. PRD 6절 결함 의심 참조 사항은 새 Requirement 미발급 확정에 따라 결함 의심 항목 섹션에 TC 없이 사유만 기재) | 초안 |
| 2026-08-22 | 사용자 리뷰 피드백 반영 - TC-001~003 문구를 "로그인 상태 여부 무관" 표현으로 수정, 나머지 항목 승인 확정 | 초안 |
| 2026-08-22 | 사용자 최종 승인 | 승인완료 |
