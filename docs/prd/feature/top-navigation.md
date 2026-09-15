---
문서유형: Feature PRD
상태: 승인완료   # 초안 | 승인완료
관련 Project PRD: project-prd.md
최초 작성일: 2026-08-21
최근 변경일: 2026-08-21
승인일: 2026-08-21
---

# Feature PRD - 상단 네비게이션

## 1. 개요

automationexercise.com 전체 페이지 상단에 고정적으로 노출되는 네비게이션 메뉴이다. 로그인
상태/로그아웃 상태에 따라 메뉴 구성이 달라지며(메뉴 구성 자체의 상세 내용은
`login-logout.md`, `signup-delete-account.md` 참조), 본 문서는 네비게이션 자체의 동작
— 각 메뉴 클릭 시 이동 URL, 페이지 간 이동 시 네비게이션 구성의 일관성, 활성(하이라이트)
표시, "Logged in as {유저명}" UI 요소 — 를 다룬다.

## 2. 관련 Project PRD 참조

- `/docs/prd/project-prd.md` (상태: 승인완료)
- Project PRD "5. 대상 Feature 목록" 중 "상단 네비게이션 (로그인 상태 / 로그아웃 상태에
  따라 메뉴 구성이 다름)" 항목에 해당
- Project PRD "7. Out of Scope" 중 "네비게이션 중 다음 메뉴의 상세 동작: Test Cases,
  API Testing, Video Tutorials, Contact us"와 연결됨 (본 문서 5절에서 이동 검증 여부까지
  포함해 범위를 명확히 확정함)

**관련 Feature PRD (중복 기술하지 않고 참조만 함)**

- `/docs/prd/feature/login-logout.md`
  - REQ-LOGIN-LOGOUT-004: 로그인 성공 시 로그인 상태 메뉴로 변경
  - REQ-LOGIN-LOGOUT-013, 014: Logout 클릭/URL 직접 접근 시 로그아웃 처리 및 로그아웃
    상태 메뉴로 변경
- `/docs/prd/feature/signup-delete-account.md`
  - REQ-SIGNUP-DELETE-ACCOUNT-006, 012: 회원가입/계정삭제 완료 페이지의 네비게이션이
    로그아웃 상태 메뉴로 표시됨
  - REQ-SIGNUP-DELETE-ACCOUNT-017: 로그아웃 상태에서 `/delete_account` 직접 접근 시
    나타나는 결함 의심 현상 (본 문서 6절에서 참조만 함)

## 3. 사용자 조작 시나리오

1. 로그인 상태와 로그아웃 상태 각각에서 상단 네비게이션의 Home, Products, Cart 메뉴를
   클릭하여 이동 URL을 확인한다.
2. 로그아웃 상태에서 Signup/Login 메뉴를 클릭하여 `/login`으로 이동하는지 확인한다.
3. Home, Products 등 서로 다른 페이지를 이동하면서 상단 네비게이션 메뉴 구성과
   "Logged in as {유저명}" 표시가 페이지마다 동일하게 유지되는지 확인한다.
4. 로그인 상태에서 특정 페이지(예: `/products`)에 위치했을 때 해당 메뉴 항목이 시각적으로
   활성(하이라이트) 표시되는지, 다른 메뉴에 마우스를 올렸을 때(hover)도 동일한 표시가
   나타나는지 확인한다.
5. "Logged in as {유저명}" 텍스트를 클릭해 별도 동작이 발생하는지 확인한다.
6. (참고, 결함 재확인 목적) 로그아웃 상태에서 `/delete_account` URL로 직접 접근했을 때
   네비게이션 자체의 메뉴 구성이 정상적인 로그아웃 상태 메뉴로 노출되는지 확인한다.

## 4. Requirements

### 4.1 확인된 요구사항

**메뉴 클릭 시 이동 URL**

- **REQ-TOP-NAVIGATION-001**: Home 메뉴 클릭 시 로그인/로그아웃 상태와 무관하게
  `https://automationexercise.com/`로 이동한다.
- **REQ-TOP-NAVIGATION-002**: Products 메뉴 클릭 시 로그인/로그아웃 상태와 무관하게
  `https://automationexercise.com/products`로 이동한다.
- **REQ-TOP-NAVIGATION-003**: Cart 메뉴 클릭 시 로그인/로그아웃 상태와 무관하게
  `https://automationexercise.com/view_cart`로 이동한다.
- **REQ-TOP-NAVIGATION-004**: 로그아웃 상태에서 Signup/Login 메뉴 클릭 시
  `https://automationexercise.com/login`으로 이동한다.

**네비게이션 일관성**

- **REQ-TOP-NAVIGATION-005**: Home, Products, Cart 등 서로 다른 페이지로 이동해도 상단
  네비게이션의 메뉴 구성과 "Logged in as {유저명}" 표시는 항상 동일하게 유지된다.
- **REQ-TOP-NAVIGATION-006**: "Logged in as {유저명}"의 유저명은 회원가입 시 사용자가
  입력한 Name 값이 그대로 노출된다.

**활성(하이라이트) 표시**

- **REQ-TOP-NAVIGATION-007**: 현재 위치한 페이지에 해당하는 메뉴 항목은 주황색으로
  활성 표시된다(예: `/products` 페이지에서 "Products" 메뉴가 주황색으로 하이라이트됨,
  스크린샷 확인).
- **REQ-TOP-NAVIGATION-008**: 모든 네비게이션 메뉴 항목은 마우스 오버(hover) 시에도
  동일하게 주황색으로 활성 표시된다.
- **REQ-TOP-NAVIGATION-009**: 현재 위치한 메뉴 항목은 마우스를 올리지 않아도(오버하지
  않아도) 활성 표시가 고정적으로 유지된다.
- **REQ-TOP-NAVIGATION-010**: 로그인 상태 메뉴 중 "Logout"과 "Delete Account" 두 항목은
  기본 상태에서도 다른 메뉴(회색/검정 계열)와 달리 빨간색 계열 텍스트/아이콘으로 표시된다
  (스크린샷 확인).

**"Logged in as {유저명}" UI 요소**

- **REQ-TOP-NAVIGATION-011**: "Logged in as {유저명}" 텍스트는 클릭해도 별도 동작이
  발생하지 않는다(링크가 아닌 단순 텍스트).

### 4.2 미확인 / 추가 확인 필요 항목

- 현재 없음 (Cart 메뉴 URL 재확인 완료 — REQ-TOP-NAVIGATION-003 참조)

## 5. Feature 단위 In Scope / Out of Scope

**In Scope**

- Home, Products, Cart, Signup/Login 메뉴 클릭 시 이동 URL 검증 (로그인/로그아웃 상태
  공통)
- 페이지 이동 간 상단 네비게이션 메뉴 구성 및 "Logged in as {유저명}" 표시의 일관성
- 현재 위치 메뉴의 활성(하이라이트) 표시, hover 시 활성 표시
- Logout / Delete Account 메뉴의 기본 스타일(빨간색 계열) 차이
- "Logged in as {유저명}" 텍스트의 클릭 동작 여부(단순 텍스트 확인)

**Out of Scope**

- Test Cases, API Testing, Video Tutorials, Contact us 메뉴: 클릭 시 정상 페이지 이동
  여부를 포함해 완전히 검증 대상에서 제외 (사용자 확정 사항)
- Logout, Delete Account 메뉴의 상세 처리 로직(로그아웃/계정삭제 자체의 동작) — 각각
  `login-logout.md`, `signup-delete-account.md` 범위이며 본 문서에서는 참조만 함
- 상단 네비게이션을 통해 진입한 이후 각 페이지 "내부"의 상세 기능 — Project PRD 원칙과
  일치
- 결제 기능, 이메일 인증, 성능 테스트 — Project PRD Out of Scope와 일치

## 6. 예외 / 에러 케이스

- 로그아웃 상태에서 `/delete_account` URL로 직접 접근 시 인증되지 않았음에도 "ACCOUNT
  DELETED!" 성공 페이지가 노출되는 현상은 `signup-delete-account.md`
  REQ-SIGNUP-DELETE-ACCOUNT-017에 이미 기술된 결함 의심 사항과 동일하며, 본 문서에서는
  새 Requirement로 발급하지 않는다. 다만 해당 페이지에서 상단 네비게이션 자체는
  정상적인 로그아웃 상태 메뉴 구성(Home, Products, Cart, Signup/Login, Test Cases,
  API Testing, Video Tutorials, Contact us)으로 노출되었음을 확인했으며(스크린샷 확인),
  이는 네비게이션 자체의 이상이 아니므로 본 문서 범위에서는 별도 이슈로 다루지 않는다.

## 7. 비고

- REQ-TOP-NAVIGATION-003(Cart 클릭 시 이동 URL)은 최초 관찰 시 `/products`로 보고되어
  4.2 미확인 항목으로 분류했으나, 재확인 결과 `https://automationexercise.com/view_cart`로
  확정되었다. 최초 관찰은 오탐이었던 것으로 정정한다.
- REQ-TOP-NAVIGATION-010(Logout/Delete Account 빨간색 스타일)은 스크린샷 근거로 확인된
  사실을 그대로 기재했으며, 이는 계정 관련 민감 동작(로그아웃/계정삭제)을 시각적으로
  구분하기 위한 디자인으로 추정되나, 추정 이유는 문서에 포함하지 않고 관찰된 사실만
  기록했다.
- Test Cases, API Testing, Video Tutorials, Contact us 4개 메뉴는 이동 여부를 포함해
  완전히 Out of Scope로 확정되었다(사용자 확정 사항, 2026-08-21).

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-21 | 최초 작성 (Draft) — 사용자 인터뷰(A/B/C 답변) 반영 | 초안 |
| 2026-08-21 | REQ-TOP-NAVIGATION-003 Cart 이동 URL 재확인 및 정정(`/products` → `/view_cart`), 4.2·7절 관련 서술 정리 | 초안 |
| 2026-08-21 | 사용자 최종 승인 | 승인완료 |
