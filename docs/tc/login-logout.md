---
문서유형: Test Case
상태: 승인완료
관련 Feature PRD: feature/login-logout.md
최초 작성일: 2026-08-21
최근 변경일: 2026-08-22
승인일: 2026-08-21
---

# Test Case - 로그인/로그아웃

## TC 목록

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-LOGIN-LOGOUT-001 | REQ-LOGIN-LOGOUT-001 | 로그인/로그아웃 | 로그인 페이지 진입 시 "Login to your account" 영역과 "New User Signup!" 영역이 OR 구분자와 함께 노출되는지 확인 | 로그아웃 상태 | 1. `/login` 페이지로 진입한다.<br>2. 페이지에 노출되는 영역을 확인한다. | "Login to your account" 영역(Email Address 입력란, Password 입력란, Login 버튼)과 "New User Signup!" 영역이 "OR" 아이콘으로 구분되어 함께 노출된다. | P2 | |
| TC-LOGIN-LOGOUT-002 | REQ-LOGIN-LOGOUT-002 | 로그인/로그아웃 | 상단 네비게이션 "Signup/Login" 클릭을 통한 로그인 페이지 접근 | 로그아웃 상태, Home 등 임의 페이지에 위치 | 1. 상단 네비게이션의 "Signup/Login" 메뉴를 클릭한다. | 로그인 페이지(`/login`)로 이동하며 "Login to your account" 영역이 노출된다. | P1 | |
| TC-LOGIN-LOGOUT-003 | REQ-LOGIN-LOGOUT-002 | 로그인/로그아웃 | URL(`/login`) 직접 진입을 통한 로그인 페이지 접근 | 로그아웃 상태 | 1. 브라우저 주소창에 `https://automationexercise.com/login`을 직접 입력하여 진입한다. | 로그인 페이지(`/login`)가 정상적으로 노출되며 "Login to your account" 영역이 표시된다. | P1 | |
| TC-LOGIN-LOGOUT-004 | REQ-LOGIN-LOGOUT-003, REQ-LOGIN-LOGOUT-004 | 로그인/로그아웃 | 정상적인 이메일/비밀번호로 로그인 시 Home 랜딩 및 로그인 상태 메뉴 전환 확인 | 로그아웃 상태, 유효한 테스트 계정 보유(예: actest1@test.com, 비밀번호는 별도 관리) | 1. `/login` 페이지로 진입한다.<br>2. Email Address, Password 입력란에 유효한 계정 정보를 입력한다.<br>3. "Login" 버튼을 클릭한다. | `https://automationexercise.com/`(Home)로 랜딩되고, 상단 네비게이션이 로그인 상태 메뉴(Home, Products, Cart, Logout, Delete Account, Test Cases, API Testing, Video Tutorials, Contact us, "Logged in as {유저명}")로 전환된다. | P0 | |
| TC-LOGIN-LOGOUT-005 | REQ-LOGIN-LOGOUT-005 | 로그인/로그아웃 | 존재하지 않는 이메일로 로그인 시도 시 에러 메시지 노출 확인 | 로그아웃 상태 | 1. `/login` 페이지로 진입한다.<br>2. Email Address에 존재하지 않는 이메일(예: notexist_qa_test@test.com)을 입력하고 Password에 임의 값을 입력한다.<br>3. "Login" 버튼을 클릭한다. | "Your email or password is incorrect!" 에러 메시지가 폼 하단에 노출되고, 로그인 폼 화면이 그대로 유지된다. | P1 | |
| TC-LOGIN-LOGOUT-006 | REQ-LOGIN-LOGOUT-005 | 로그인/로그아웃 | 존재하는 이메일에 잘못된 비밀번호로 로그인 시도 시 동일한 에러 메시지 노출 확인(이메일 오류와 구분되지 않음) | 로그아웃 상태, 유효한 테스트 계정 보유(예: actest1@test.com) | 1. `/login` 페이지로 진입한다.<br>2. Email Address에 유효한 테스트 계정 이메일을 입력하고 Password에 잘못된 값을 입력한다.<br>3. "Login" 버튼을 클릭한다. | TC-LOGIN-LOGOUT-005와 동일하게 "Your email or password is incorrect!" 에러 메시지가 폼 하단에 노출되고, 로그인 폼 화면이 그대로 유지된다(이메일 오류와 동일한 메시지로 구분되지 않음을 확인). | P1 | |
| TC-LOGIN-LOGOUT-007 | REQ-LOGIN-LOGOUT-006 | 로그인/로그아웃 | '@' 미포함 등 형식이 올바르지 않은 이메일 입력 시 브라우저 native 유효성 검사 동작 확인 | 로그아웃 상태 | 1. `/login` 페이지로 진입한다.<br>2. Email Address에 '@'가 없는 값(예: "invalidemail")을 입력하고 Password에 임의 값을 입력한다.<br>3. "Login" 버튼을 클릭한다. | 브라우저 자체(HTML5 native) 유효성 검사 팝업이 노출되며, 폼이 제출되지 않는다(에러 메시지 영역 미노출, 페이지 이동 없음). | P2 | |
| TC-LOGIN-LOGOUT-008 | REQ-LOGIN-LOGOUT-007 | 로그인/로그아웃 | Email Address 입력란을 비운 채 Login 클릭 시 브라우저 필수 입력 검증 동작 확인 | 로그아웃 상태 | 1. `/login` 페이지로 진입한다.<br>2. Email Address 입력란을 비워두고 Password에만 임의 값을 입력한다.<br>3. "Login" 버튼을 클릭한다. | 브라우저 자체 필수 입력 검증 팝업("이 입력란을 작성하세요.")이 노출되며, 폼이 제출되지 않는다. | P2 | |
| TC-LOGIN-LOGOUT-009 | REQ-LOGIN-LOGOUT-008 | 로그인/로그아웃 | Password 입력란을 비운 채 Login 클릭 시 브라우저 필수 입력 검증 동작 확인 | 로그아웃 상태 | 1. `/login` 페이지로 진입한다.<br>2. Email Address에만 형식이 올바른 임의 값을 입력하고 Password 입력란은 비워둔다.<br>3. "Login" 버튼을 클릭한다. | 브라우저 자체 필수 입력 검증 팝업이 노출되며, 폼이 제출되지 않는다. | P2 | |
| TC-LOGIN-LOGOUT-010 | REQ-LOGIN-LOGOUT-009 | 로그인/로그아웃 | 이미 로그인된 상태에서 `/login` URL로 직접 재진입 시 Home으로 리다이렉트되는지 확인 | 로그인 상태(유효한 테스트 계정으로 로그인 완료) | 1. 로그인 상태에서 브라우저 주소창에 `https://automationexercise.com/login`을 직접 입력하여 진입한다. | 로그인 폼이 노출되지 않고 Home(루트, `https://automationexercise.com/`)으로 리다이렉트된다. | P2 | |
| TC-LOGIN-LOGOUT-011 | REQ-LOGIN-LOGOUT-010 | 로그인/로그아웃 | 로그인 상태에서 새로고침(F5) 후에도 로그인 상태가 유지되는지 확인 | 로그인 상태(유효한 테스트 계정으로 로그인 완료) | 1. 로그인 상태에서 임의 페이지(예: Home)에 위치한다.<br>2. 브라우저 새로고침(F5)을 수행한다. | 새로고침 후에도 로그아웃되지 않고 상단 네비게이션이 로그인 상태 메뉴로 계속 유지된다. | P1 | |
| TC-LOGIN-LOGOUT-012 | REQ-LOGIN-LOGOUT-011 | 로그인/로그아웃 | 로그인 실패가 반복되어도 계정 잠금/제한 정책이 존재하지 않는지 확인 | 로그아웃 상태, 유효한 테스트 계정 보유(예: actest1@test.com) | 1. `/login` 페이지에서 유효한 테스트 계정 이메일에 잘못된 비밀번호를 입력하여 로그인을 5회 연속 시도한다.<br>2. 이후 동일 계정에 올바른 비밀번호로 다시 로그인을 시도한다. | 반복된 실패 시도 이후에도 계정 잠금이나 별도 제한 메시지 없이, 올바른 비밀번호 입력 시 정상적으로 로그인에 성공한다. | P2 | |
| TC-LOGIN-LOGOUT-013 | REQ-LOGIN-LOGOUT-012 | 로그인/로그아웃 | 이메일/비밀번호 입력값에 긴 문자열 및 특수문자 입력 시 이메일 형식 검증 외 별도 클라이언트 측 제한이 없는지 확인 | 로그아웃 상태 | 1. `/login` 페이지로 진입한다.<br>2. Email Address에 형식은 유효하지만 매우 긴 값(예: 로컬파트 100자 이상)을 입력하고, Password에 특수문자를 포함한 긴 문자열을 입력한다.<br>3. "Login" 버튼을 클릭한다. | 길이나 특수문자로 인한 별도의 브라우저 native 검증 팝업 없이 폼이 정상적으로 제출되며, "Your email or password is incorrect!" 에러 메시지가 노출된다(해당 계정이 존재하지 않는 것으로 처리됨). | P2 | |
| TC-LOGIN-LOGOUT-014 | REQ-LOGIN-LOGOUT-013, REQ-LOGIN-LOGOUT-014 | 로그인/로그아웃 | 상단 네비게이션 "Logout" 클릭을 통한 로그아웃 수행 및 결과 확인 | 로그인 상태(유효한 테스트 계정으로 로그인 완료) | 1. 로그인 상태에서 상단 네비게이션의 "Logout" 메뉴를 클릭한다. | 로그인 페이지(`/login`)로 랜딩되며, 상단 네비게이션이 로그아웃 상태 메뉴(Home, Products, Cart, Signup/Login, Test Cases, API Testing, Video Tutorials, Contact us)로 전환된다. | P1 | |
| TC-LOGIN-LOGOUT-015 | REQ-LOGIN-LOGOUT-013, REQ-LOGIN-LOGOUT-014 | 로그인/로그아웃 | URL(`/logout`) 직접 진입을 통한 로그아웃 수행 및 결과 확인(로그인 상태에서) | 로그인 상태(유효한 테스트 계정으로 로그인 완료) | 1. 로그인 상태에서 브라우저 주소창에 `https://automationexercise.com/logout`을 직접 입력하여 진입한다. | 로그인 페이지(`/login`)로 랜딩되며, 상단 네비게이션이 로그아웃 상태 메뉴로 전환된다. | P1 | |

## 결함 의심 항목

> `tc-writing` Skill 4.6 신규 규칙에 따른 소급 반영입니다. 과거(2026-08-21) 최초 승인 시에는
> REQ-LOGIN-LOGOUT-015(결함 의심)를 TC 목록에서 완전히 제외하고 별도 결함 리포트로만 관리하기로
> 했으나, 이후 확정된 신규 표준 규칙(정상 케이스와 섞지 않되 TC 문서에서 완전히 제외하지도 않음)에
> 따라 아래와 같이 별도 "결함 의심 항목" 섹션으로 재포함했습니다. 위 메인 TC 목록(TC-LOGIN-LOGOUT-001~015)의
> 기존 ID와 내용은 변경하지 않았으며, 신규 TC는 기존 마지막 번호(015) 다음부터 이어서 016을
> 부여했습니다.

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-LOGIN-LOGOUT-016 | REQ-LOGIN-LOGOUT-015 | 로그인/로그아웃 | 로그아웃 상태에서 URL(`/logout`) 직접 접근 시 정상 페이지 대신 Django 서버 에러 페이지가 그대로 노출되는 비정상 동작 확인 (결함 의심) | 로그아웃 상태 | 1. 로그아웃 상태에서 브라우저 주소창에 `https://automationexercise.com/logout`을 직접 입력하여 진입한다.<br>2. 노출되는 화면을 확인한다. | 로그인 페이지(`/login`) 랜딩이나 정상 처리 없이, Django 서버 에러 페이지(`KeyError at /logout`, Exception Value `'user_id'`, 상세 Traceback, 서버 파일 경로, Python/Django 버전 등 디버그 정보)가 그대로 노출된다. | P1 | |

## Priority 산정 근거

- **TC-LOGIN-LOGOUT-001**: Impact 3 / Likelihood 2 / Risk Score 6 — 정적 UI 레이아웃 확인으로, 문제가 있어도 로그인 기능 자체가 즉시 차단되지는 않으며 변경 가능성이 낮은 정적 화면.
- **TC-LOGIN-LOGOUT-002**: Impact 5 / Likelihood 2 / Risk Score 10 — 로그인 기능 전체의 진입점이라 실패 시 핵심 기능 사용 불가로 이어지지만, 단순 네비게이션 클릭 동작이라 결함 발생 가능성 자체는 낮음.
- **TC-LOGIN-LOGOUT-003**: Impact 5 / Likelihood 2 / Risk Score 10 — TC-002와 동일 근거, 다른 진입 경로(URL 직접 접근)에 대한 검증.
- **TC-LOGIN-LOGOUT-004**: Impact 5 / Likelihood 4 / Risk Score 20 — 로그인 기능의 핵심 Happy Path이며, 랜딩 URL/세션 확립/네비게이션 렌더링 등 여러 요소를 함께 검증해야 하는 복합 시나리오라 결함 발생 가능성도 상대적으로 높음.
- **TC-LOGIN-LOGOUT-005**: Impact 4 / Likelihood 3 / Risk Score 12 — 에러 처리가 잘못될 경우 사용자 혼란 및 보안 정보(계정 존재 여부) 노출 가능성이 있는 주요 Negative Case.
- **TC-LOGIN-LOGOUT-006**: Impact 4 / Likelihood 3 / Risk Score 12 — TC-005와 동일 근거이며, "이메일/비밀번호 오류를 구분하지 않는다"는 요구사항을 별도로 검증.
- **TC-LOGIN-LOGOUT-007**: Impact 2 / Likelihood 1 / Risk Score 2 — 브라우저 기본 제공(native) 기능으로 애플리케이션 로직에 의한 결함 가능성이 매우 낮음.
- **TC-LOGIN-LOGOUT-008**: Impact 2 / Likelihood 1 / Risk Score 2 — TC-007과 동일 근거.
- **TC-LOGIN-LOGOUT-009**: Impact 2 / Likelihood 1 / Risk Score 2 — TC-007/008과 동일 근거.
- **TC-LOGIN-LOGOUT-010**: Impact 3 / Likelihood 2 / Risk Score 6 — 잘못 동작해도 로그인 폼이 노출되는 정도이며 핵심 기능 자체가 차단되지는 않음.
- **TC-LOGIN-LOGOUT-011**: Impact 4 / Likelihood 3 / Risk Score 12 — 세션 유지 실패 시 사용자가 반복 로그인해야 하는 주요 불편이 발생하며, 쿠키/스토리지 등 세션 처리 특성상 결함 발생 가능성도 일반 수준 이상.
- **TC-LOGIN-LOGOUT-012**: Impact 2 / Likelihood 1 / Risk Score 2 — PRD상 정책 부재가 이미 확인된 사항으로, 해당 부재 상태가 유지되는지 재확인하는 목적이며 변경 가능성이 낮음.
- **TC-LOGIN-LOGOUT-013**: Impact 2 / Likelihood 2 / Risk Score 4 — 클라이언트 측 추가 검증 부재를 확인하는 경계값(Boundary) 테스트로 사용자 영향은 제한적.
- **TC-LOGIN-LOGOUT-014**: Impact 5 / Likelihood 2 / Risk Score 10 — 로그아웃 실패 시 세션이 종료되지 않아 보안상 영향이 있으나, 단순 클릭 동작이라 결함 발생 가능성 자체는 낮음.
- **TC-LOGIN-LOGOUT-015**: Impact 5 / Likelihood 2 / Risk Score 10 — TC-014와 동일 근거, 다른 진입 경로(URL 직접 접근)에 대한 검증.
- **TC-LOGIN-LOGOUT-016** (결함 의심): Impact 5 / Likelihood 3 / Risk Score 15 — 서버 에러 페이지에 상세 Traceback, 서버 파일 경로, Python/Django 버전 등 내부 구현 정보가 그대로 노출되는 정보 노출(Information Disclosure) 성격의 문제로, 단순 UX 결함보다 보안 영향이 크다고 판단해 Impact를 5로 평가함. 다만 "로그아웃 상태에서 `/logout`에 직접 접근"이라는 제한적이고 특정된 조건에서만 발생하므로 Impact 5 항목 중에서는 비교적 좁은 조건이나, 이미 사용자 실측을 통해 100% 재현이 확인된 결함 의심 사항이라 Likelihood는 3으로 평가함(Risk Score 15로 P1 상한).

## 사용자 확인 필요 사항

1. **TC-LOGIN-LOGOUT-016 신규 추가(결함 의심 항목 소급 반영)**: ✅ 확인 완료 — `tc-writing`
   Skill 4.6 신규 규칙에 따라 REQ-LOGIN-LOGOUT-015(결함 의심)를 기반으로 추가한
   TC-LOGIN-LOGOUT-016의 내용(Test Scenario/Expected Result)과 Priority 산정(Impact 5 /
   Likelihood 3 / Risk Score 15 / P1)이 적절하다고 최종 확인받았습니다.
2. **Google Spreadsheet 반영 필요**: ✅ 반영 완료 — TC-LOGIN-LOGOUT-016을 `sheets_sync.py
   append`로 Google Spreadsheet `Testcase_Login` 탭에 추가 반영했습니다(기존
   TC-LOGIN-LOGOUT-001~015에는 영향 없음, 총 16건).

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-21 | 최초 작성 (REQ-LOGIN-LOGOUT-001~014 기반 TC 초안, REQ-015는 처리 방식 확인 대기 중인 제안 행으로 포함) | 초안 |
| 2026-08-21 | 사용자 확인 결과 반영: (1) REQ-LOGIN-LOGOUT-015(결함 의심)는 TC 목록에서 제외하고 별도 결함 리포트로만 관리하기로 확정되어 TC-LOGIN-LOGOUT-016(안) 제거, (2) REQ-003+004→TC-004, REQ-013+014→TC-014/015 병합 설계 확정, (3) Requirement ID 복수 표기("REQ-A, REQ-B") 방식 확정. 최종 TC는 TC-LOGIN-LOGOUT-001~015 (15개) | 초안 |
| 2026-08-21 | 사용자 최종 승인 (Google Spreadsheet 반영은 서비스 계정 인증정보 설정 후 별도 진행 예정) | 승인완료 |
| 2026-08-22 | 신규 표준 규칙 소급 반영 - 결함 의심 항목 섹션 신설 및 REQ-LOGIN-LOGOUT-015 기반 TC-LOGIN-LOGOUT-016 추가(기존 TC-LOGIN-LOGOUT-001~015 ID/내용은 변경하지 않음, 이미 Google Spreadsheet에 반영된 정합성 유지). TC-016은 사용자 재확인 및 Spreadsheet 추가 반영 대기 중. | 승인완료 |
| 2026-08-22 | TC-LOGIN-LOGOUT-016 사용자 최종 확인 및 Google Spreadsheet Testcase_Login 탭 추가 반영: 내용/Priority(Impact 5 / Likelihood 3 / Risk Score 15 / P1)가 적절함을 최종 확인받고, `sheets_sync.py append`로 Testcase_Login 탭에 TC-016 1건을 추가 반영(기존 TC-LOGIN-LOGOUT-001~015는 그대로 유지, 반영 후 총 16건 확인). | 승인완료 |
