---
문서유형: Test Case
상태: 승인완료   # 초안 | 승인완료
관련 Feature PRD: feature/signup-delete-account.md
최초 작성일: 2026-08-22
최근 변경일: 2026-08-30
승인일: 2026-08-22
---

# Test Case - 회원가입 / 계정삭제

## TC 목록

> 공통 Preconditions:
> - 사이트 진입 시 또는 일정 시간 경과 시 무작위로 노출될 수 있는 모달형 광고는 Project PRD "8.
>   기타 제약사항" 원칙에 따라 검증 대상이 아니므로, 모든 TC 수행 전 광고 모달이 노출된 경우 닫은
>   상태에서 진행한다(아래 표에는 반복 기재하지 않음).
> - 회원가입 TC(TC-SIGNUP-DELETE-ACCOUNT-001~009)는 매 회 새로운(미가입) Name/Email 값을
>   사용해야 하므로, 표에는 실제 값 대신 예시 placeholder(예: `newuser_{실행시각}@test.com`)로
>   표기한다. 실제 수행 시점에 고유한 값을 사용한다(`tc-writing` Skill 4.5, PRD에 정의되지 않은
>   구체적 테스트 데이터를 요구사항처럼 고정하지 않기 위함).
> - 계정삭제 TC(TC-SIGNUP-DELETE-ACCOUNT-010~014, TC-SIGNUP-DELETE-ACCOUNT-016)는 Project
>   PRD의 재사용 테스트 계정(actest1~3@test.com)을 삭제 대상으로 사용하지 않는다. 계정삭제는
>   되돌릴 수 없는 동작이므로, 사전에 회원가입 절차로 별도 생성한 "삭제 전용" 테스트 계정을
>   사용해 다른 Feature TC(로그인/로그아웃, 상단 네비게이션 등)에서 재사용 계정으로 검증하는
>   흐름과 데이터가 오염되지 않도록 한다(`tc-writing` Skill 4.5, Project PRD "11. Test Data 관리
>   원칙" 참조).
> - 계정 비밀번호 등 실제 인증정보는 표에 기록하지 않는다.

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-SIGNUP-DELETE-ACCOUNT-001 | REQ-SIGNUP-DELETE-ACCOUNT-001, REQ-SIGNUP-DELETE-ACCOUNT-002 | 회원가입 / 계정삭제 | 로그인 페이지에서 신규 Name/Email 입력 후 Signup 클릭 시 상세 정보 입력 페이지로 이동하고 입력한 Name/Email 값이 자동 반영되는지 확인 | 로그아웃 상태, 미가입 상태의 신규 Name/Email 값 준비(예: Name "Test User", Email `newuser_{실행시각}@test.com`) | 1. `/login` 페이지의 "New User Signup!" 영역에 준비한 Name, Email Address를 입력한다.<br>2. "Signup" 버튼을 클릭한다. | 상세 정보 입력 페이지(`/signup`, "ENTER ACCOUNT INFORMATION")로 이동하며, 1단계에서 입력한 Name/Email 값이 각각 해당 입력란에 동일하게 자동 반영되어 노출된다. | P1 | |
| TC-SIGNUP-DELETE-ACCOUNT-002 | REQ-SIGNUP-DELETE-ACCOUNT-003 | 회원가입 / 계정삭제 | 상세 정보 입력 페이지가 상단(Title/Name/Email/Password/DOB/체크박스 2종), ADDRESS INFORMATION, 하단(Mobile Number/Create Account 버튼) 구성으로 노출되는지 확인 | 로그아웃 상태에서 로그인 페이지의 "New User Signup!" 영역에 신규 Name/Email을 입력하고 "Signup"을 클릭해 상세 정보 입력 페이지(`/signup`)에 진입한 상태 | 1. 상단 영역(Title, Name, Email, Password, Date of Birth, "Sign up for our newsletter!" 체크박스, "Receive special offers from our partners!" 체크박스)을 확인한다.<br>2. ADDRESS INFORMATION 영역(First name, Last name, Company, Address, Address 2, Country, State, City, Zipcode)을 확인한다.<br>3. 하단 영역(Mobile Number, "Create Account" 버튼)을 확인한다. | 위 3개 영역의 모든 항목이 빠짐없이 노출된다. | P2 | |
| TC-SIGNUP-DELETE-ACCOUNT-003 | REQ-SIGNUP-DELETE-ACCOUNT-004 | 회원가입 / 계정삭제 | 상세 정보 입력 페이지에서 필수 입력 필드가 "*" 표기로 구분되는지 확인 | 상세 정보 입력 페이지(`/signup`)에 진입한 상태 | 1. 페이지 내 각 입력 필드 라벨을 확인해 "*" 표기가 있는 필드와 없는 필드를 구분한다. | Name, Email, Password, First name, Last name, Address, Country, State, City, Zipcode, Mobile Number 등 필수 필드에는 "*"가 표기되고, Title, Date of Birth, 체크박스 2종, Company, Address 2 등 선택 필드에는 "*"가 표기되지 않는다. | P2 | |
| TC-SIGNUP-DELETE-ACCOUNT-004 | REQ-SIGNUP-DELETE-ACCOUNT-005 | 회원가입 / 계정삭제 | 선택 필드(Title/Date of Birth/체크박스 2종/Company/Address 2)를 모두 비운 채 필수 필드만 입력해도 정상적으로 가입이 완료되는지 확인 | 상세 정보 입력 페이지(`/signup`)에 진입한 상태, 신규(미가입) Email 사용 | 1. Title, Date of Birth, "Sign up for our newsletter!" 체크박스, "Receive special offers from our partners!" 체크박스, Company, Address 2는 비워둔다.<br>2. 나머지 필수(*) 필드(Password, First name, Last name, Address, Country, State, City, Zipcode, Mobile Number)에만 유효한 값을 입력한다.<br>3. "Create Account" 버튼을 클릭한다. | 별도 에러 없이 "ACCOUNT CREATED!" 완료 페이지(`/account_created`)로 이동하며 가입이 정상적으로 완료된다. | P2 | |
| TC-SIGNUP-DELETE-ACCOUNT-005 | REQ-SIGNUP-DELETE-ACCOUNT-006 | 회원가입 / 계정삭제 | 상세 정보 입력 후 정상적으로 가입 완료 시 "ACCOUNT CREATED!" 페이지 이동, 안내 문구, "Continue" 버튼, 로그아웃 상태 네비게이션이 함께 노출되는지 확인 | 상세 정보 입력 페이지(`/signup`)에서 모든 필수 필드에 유효한 값 입력 완료 상태, 신규(미가입) Email 사용 | 1. "Create Account" 버튼을 클릭한다.<br>2. 이동한 페이지의 URL, 안내 문구, 버튼, 상단 네비게이션 상태를 확인한다. | `/account_created` 페이지로 이동하며 "Congratulations! Your new account has been successfully created!" 등의 안내 문구와 "Continue" 버튼이 노출된다. 상단 네비게이션은 로그아웃 상태 메뉴(Home, Products, Cart, Signup/Login, Test Cases, API Testing, Video Tutorials, Contact us)로 노출된다(자동 로그인되지 않음). | P0 | |
| TC-SIGNUP-DELETE-ACCOUNT-006 | REQ-SIGNUP-DELETE-ACCOUNT-007 | 회원가입 / 계정삭제 | "ACCOUNT CREATED!" 페이지에서 "Continue" 클릭 시 Home으로 랜딩되고 로그인 상태로 전환되는지 확인 | 회원가입 절차(1단계 Name/Email 입력 → 2단계 상세정보 입력 → Create Account)를 완료하여 "ACCOUNT CREATED!" 완료 페이지(`/account_created`)에 진입한 상태 | 1. "Continue" 버튼을 클릭한다.<br>2. 이동한 URL과 상단 네비게이션 상태를 확인한다. | `https://automationexercise.com/`(Home)으로 랜딩되며, 상단 네비게이션이 로그인 상태 메뉴로 전환된다(방금 생성한 계정으로 자동 로그인되어 "Logged in as {Name}" 텍스트가 노출됨). | P2 | |
| TC-SIGNUP-DELETE-ACCOUNT-007 | REQ-SIGNUP-DELETE-ACCOUNT-008 | 회원가입 / 계정삭제 | 이미 가입된 이메일로 재가입 시도 시 페이지 전환 없이 "Email Address already exist!" 에러 메시지가 노출되는지 확인 | 로그아웃 상태, 이미 가입되어 있는 이메일 주소 확인됨(예: 기존 테스트 계정 이메일) | 1. `/login` 페이지의 "New User Signup!" 영역에 이미 가입된 이메일 주소와 임의의 Name을 입력한다.<br>2. "Signup" 버튼을 클릭한다. | 상세 정보 입력 페이지로 전환되지 않고 로그인/가입 폼 화면이 그대로 유지되며, Email 입력란 하단에 "Email Address already exist!" 에러 메시지가 노출된다. | P1 | |
| TC-SIGNUP-DELETE-ACCOUNT-008 | REQ-SIGNUP-DELETE-ACCOUNT-009 | 회원가입 / 계정삭제 | 상세 정보 입력 페이지에서 필수(*) 필드를 비운 채 "Create Account" 클릭 시 브라우저 native 필수 입력 검증이 동작하는지 확인 | 상세 정보 입력 페이지(`/signup`)에 진입한 상태 | 1. 필수(*) 필드 중 일부(예: Password)를 비워둔다.<br>2. "Create Account" 버튼을 클릭한다. | 브라우저 자체(HTML5 native) 필수 입력 검증 팝업("이 입력란을 작성하세요.")이 노출되며 폼 제출이 차단된다. | P2 | |
| TC-SIGNUP-DELETE-ACCOUNT-009 | REQ-SIGNUP-DELETE-ACCOUNT-010 | 회원가입 / 계정삭제 | Mobile Number 입력란에 숫자가 아닌 값을 입력해도 별도 형식/길이 검증 없이 필수값만 충족하면 가입이 가능한지 확인 | 상세 정보 입력 페이지(`/signup`)에서 Mobile Number를 제외한 나머지 필수 필드에 유효한 값 입력 완료 상태, 신규(미가입) Email 사용 | 1. Mobile Number 입력란에 숫자가 아닌 값(예: "phone-number")을 입력한다.<br>2. "Create Account" 버튼을 클릭한다. | 별도 형식/길이 관련 에러 없이 "ACCOUNT CREATED!" 완료 페이지(`/account_created`)로 이동하며 가입이 정상적으로 완료된다. | P2 | |
| TC-SIGNUP-DELETE-ACCOUNT-010 | REQ-SIGNUP-DELETE-ACCOUNT-011 | 회원가입 / 계정삭제 | 로그인 상태에서 상단 네비게이션 "Delete Account" 클릭 시 별도 확인(컨펌) 절차 없이 즉시 삭제 처리되는지 확인 | 삭제 전용으로 사전에 신규 가입한 테스트 계정으로 로그인 완료 상태(Project PRD의 재사용 계정 actest1~3은 사용하지 않음) | 1. 로그인 상태에서 상단 네비게이션의 "Delete Account"를 클릭한다.<br>2. 클릭 직후 별도 확인 모달/팝업 노출 여부와 화면 전환 여부를 확인한다. | 삭제 여부를 묻는 별도 확인 모달이나 컨펌 절차 없이 즉시 "ACCOUNT DELETED!" 완료 페이지(`/delete_account`)로 이동한다. | P1 | |
| TC-SIGNUP-DELETE-ACCOUNT-011 | REQ-SIGNUP-DELETE-ACCOUNT-012 | 회원가입 / 계정삭제 | 계정삭제 처리 후 "ACCOUNT DELETED!" 완료 페이지 이동, 안내 문구, "Continue" 버튼, 로그아웃 상태 네비게이션이 함께 노출되는지 확인 | 계정삭제 절차(로그인 상태에서 상단 네비게이션 "Delete Account" 클릭)를 통해 "ACCOUNT DELETED!" 완료 페이지(`/delete_account`)에 진입한 상태 | 1. 이동한 페이지의 URL, 안내 문구, 버튼, 상단 네비게이션 상태를 확인한다. | `/delete_account` 페이지에 "Your account has been permanently deleted!" 등의 안내 문구와 "Continue" 버튼이 노출된다. 상단 네비게이션은 로그아웃 상태 메뉴로 노출된다. | P1 | |
| TC-SIGNUP-DELETE-ACCOUNT-012 | REQ-SIGNUP-DELETE-ACCOUNT-013 | 회원가입 / 계정삭제 | "ACCOUNT DELETED!" 페이지에서 "Continue" 클릭 시 로그아웃 상태로 Home으로 랜딩되는지 확인 | "ACCOUNT DELETED!" 완료 페이지(`/delete_account`)에 진입한 상태(TC-SIGNUP-DELETE-ACCOUNT-010~011 절차 참고) | 1. "Continue" 버튼을 클릭한다.<br>2. 이동한 URL과 상단 네비게이션 상태를 확인한다. | `https://automationexercise.com/`(Home)으로 랜딩되며, 상단 네비게이션이 로그아웃 상태 메뉴로 노출된다. | P2 | |
| TC-SIGNUP-DELETE-ACCOUNT-013 | REQ-SIGNUP-DELETE-ACCOUNT-014 | 회원가입 / 계정삭제 | 삭제된 계정의 이메일/비밀번호로 재로그인 시도 시 로그인되지 않고 에러 메시지가 노출되는지 확인 | 사전에 신규 가입 후 계정삭제까지 완료한 테스트 전용 계정의 이메일/비밀번호가 확인된 상태(비밀번호는 문서에 기록하지 않음) | 1. `/login` 페이지로 진입한다.<br>2. Email Address, Password 입력란에 삭제된 계정의 이메일/비밀번호를 입력한다.<br>3. "Login" 버튼을 클릭한다. | 로그인되지 않고 "Your email or password is incorrect!" 에러 메시지가 폼 하단에 노출되며, 로그인 폼 화면이 그대로 유지된다. | P1 | |
| TC-SIGNUP-DELETE-ACCOUNT-014 | REQ-SIGNUP-DELETE-ACCOUNT-015 | 회원가입 / 계정삭제 | 삭제된 계정의 이메일로 재가입 시도 시 "이미 존재하는 이메일" 에러 없이 정상적으로 신규 가입이 진행되는지 확인 | 사전에 신규 가입 후 계정삭제까지 완료한 테스트 전용 계정의 이메일이 확인된 상태 | 1. `/login` 페이지의 "New User Signup!" 영역에 삭제된 계정의 이메일 주소와 임의의 Name을 입력하고 "Signup" 버튼을 클릭한다.<br>2. 상세 정보 입력 페이지에서 필수 필드에 유효한 값을 입력하고 "Create Account" 버튼을 클릭한다. | "Email Address already exist!" 에러 없이 상세 정보 입력 페이지로 정상 이동하며, 최종적으로 "ACCOUNT CREATED!" 완료 페이지로 이동해 가입이 정상 완료된다. | P1 | |

## 결함 의심 항목

> `tc-writing` Skill 4.6에 따라, PRD상 "결함 의심"(비정상 동작이 관찰되었으나 정상/비정상 여부는
> 별도 판정하지 않고 사실만 기록)으로 표시된 REQ-SIGNUP-DELETE-ACCOUNT-016, 017에 대한 TC를 정상
> 케이스 TC 목록과 분리해 별도로 모았습니다. ID 넘버링은 위 정상 케이스 TC 목록(001~014)에 이어서
> 부여했으며, 컬럼 구조와 Requirement ID 매핑, Priority 산정 방식은 정상 케이스 TC와 동일합니다.
>
> 특히 TC-SIGNUP-DELETE-ACCOUNT-016(REQ-SIGNUP-DELETE-ACCOUNT-017)은 `login-logout.md`
> "7. 비고"에서 계정삭제 Feature PRD로 이관 예정이라고 메모되어 있던 사항이며,
> `top-navigation.md` "결함 의심 항목" 섹션에서도 본 문서로 위임한다고 명시했던 항목입니다
> (로그아웃 상태에서 `/delete_account` URL 직접 접근 시 미인증임에도 "ACCOUNT DELETED!" 성공
> 페이지가 노출되는 현상).

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-SIGNUP-DELETE-ACCOUNT-015 | REQ-SIGNUP-DELETE-ACCOUNT-016 | 회원가입 / 계정삭제 | 실제 회원가입 절차를 거치지 않고 URL(`/account_created`)에 직접 접근해도 "ACCOUNT CREATED!" 완료 페이지가 그대로 노출되는 비정상 동작 확인 (결함 의심, 로그인/로그아웃 상태 모두 재현) | 회원가입 절차를 거치지 않은 상태 | 1. 로그아웃 상태에서 브라우저 주소창에 `https://automationexercise.com/account_created`를 직접 입력하여 진입한다.<br>2. 노출되는 화면을 확인한다.<br>3. 유효한 테스트 계정으로 로그인한 뒤(예: actest1@test.com), 동일하게 `https://automationexercise.com/account_created`를 직접 입력하여 진입한다.<br>4. 노출되는 화면을 확인한다. | 실제로 회원가입 절차를 거치지 않았음에도, 로그인/로그아웃 상태 양쪽 모두에서 "ACCOUNT CREATED!" 완료 페이지("Congratulations! Your new account has been successfully created!" 문구, "Continue" 버튼 포함)가 정상 가입 완료 시와 동일하게 노출된다. | P1 | |
| TC-SIGNUP-DELETE-ACCOUNT-016 | REQ-SIGNUP-DELETE-ACCOUNT-017 | 회원가입 / 계정삭제 | 로그아웃 상태(미인증)에서 계정삭제 URL(`/delete_account`)에 직접 접근하면 실제 인증/삭제가 이루어지지 않았음에도 "ACCOUNT DELETED!" 성공 페이지가 노출되는 비정상 동작 확인 (결함 의심) | 로그아웃 상태(미인증) | 1. 로그아웃 상태에서 브라우저 주소창에 `https://automationexercise.com/delete_account`를 직접 입력하여 진입한다.<br>2. 노출되는 화면과 상단 네비게이션 상태를 확인한다. | 별도 인증 절차 없이도(로그인되어 있지 않고 삭제 대상 계정도 지정되지 않았음에도) "ACCOUNT DELETED!" 완료 페이지("Your account has been permanently deleted!" 문구, "Continue" 버튼 포함)가 정상 삭제 완료 시와 동일하게 노출되며, 상단 네비게이션도 로그아웃 상태 메뉴로 노출된다. | P1 | |

## Priority 산정 근거

- **TC-SIGNUP-DELETE-ACCOUNT-001**: Impact 5 / Likelihood 2 / Risk Score 10 — 회원가입 전체
  퍼널의 진입점으로, 실패 시 회원가입 자체가 불가능해진다(Impact 5). Name/Email 값이 다음 페이지로
  전달되는 흐름은 단순하지만 단일 클릭 동작이라 결함 발생 가능성 자체는 낮다(Likelihood 2).
- **TC-SIGNUP-DELETE-ACCOUNT-002**: Impact 3 / Likelihood 2 / Risk Score 6 — 개별 입력 필드의
  실제 동작(필수 여부, 값 검증 등)은 다른 TC에서 별도로 검증되므로, 이 TC 자체는 레이아웃 구성
  요소 노출 여부 확인에 해당해 영향이 제한적이다(Impact 3). 여러 영역/여러 필드를 한 번에 확인해야
  하는 정적 레이아웃 검증이라 결함 발생 가능성은 일반 수준이다(Likelihood 2).
- **TC-SIGNUP-DELETE-ACCOUNT-003**: Impact 2 / Likelihood 1 / Risk Score 2 — "*" 표기는 시각적
  안내 요소로, 표기가 누락되어도 실제 필수값 검증(REQ-009에서 별도 검증)에는 영향이 없어 영향이
  낮다(Impact 2). 정적 스타일/텍스트 확인이라 결함 발생 가능성은 매우 낮다(Likelihood 1).
- **TC-SIGNUP-DELETE-ACCOUNT-004**: Impact 4 / Likelihood 2 / Risk Score 8 — 선택 필드를 비워도
  가입이 가능해야 한다는 요구사항이 깨지면, 선택 항목을 채우지 않는 다수의 사용자가 가입 자체를
  완료하지 못하게 된다(Impact 4). 다만 필수/선택 필드 구분 로직 자체는 단순한 서버 측 검증이라
  결함 발생 가능성은 일반 수준이다(Likelihood 2).
- **TC-SIGNUP-DELETE-ACCOUNT-005**: Impact 5 / Likelihood 4 / Risk Score 20 — 회원가입 기능의
  핵심 Happy Path이며, 이 단계가 실패하면 신규 계정 생성이 전면 불가능해진다(Impact 5,
  `login-logout.md` TC-LOGIN-LOGOUT-004의 로그인 성공 시나리오와 동일한 근거). 완료 페이지 이동/
  안내 문구/버튼/네비게이션 전환이라는 여러 요소를 동시에 검증해야 하는 복합 시나리오라 결함 발생
  가능성도 상대적으로 높다(Likelihood 4).
- **TC-SIGNUP-DELETE-ACCOUNT-006**: Impact 3 / Likelihood 2 / Risk Score 6 — 계정 생성 자체는
  이미 이전 단계에서 완료된 상태이므로, 이 TC가 실패해도 핵심 기능(계정 생성)에는 영향이 없고
  이후 페이지 이동 UX 문제에 그친다(Impact 3). 단순 버튼 클릭에 의한 페이지 이동이라 결함 발생
  가능성은 낮다(Likelihood 2).
- **TC-SIGNUP-DELETE-ACCOUNT-007**: Impact 4 / Likelihood 3 / Risk Score 12 — 중복 이메일 검증이
  깨지면 계정 데이터 유일성이 훼손되거나 사용자가 혼란을 겪을 수 있는 중요 Negative
  Case이다(Impact 4). 서버 측 이메일 존재 여부 조회가 결합된 검증이라 결함 발생 가능성이 일반
  수준 이상이다(Likelihood 3).
- **TC-SIGNUP-DELETE-ACCOUNT-008**: Impact 2 / Likelihood 1 / Risk Score 2 — 브라우저 기본 제공
  (native) 기능으로 애플리케이션 로직에 의한 결함 가능성이 매우 낮다(`login-logout.md`
  TC-LOGIN-LOGOUT-007~009와 동일 근거).
- **TC-SIGNUP-DELETE-ACCOUNT-009**: Impact 2 / Likelihood 2 / Risk Score 4 — Mobile Number
  형식 미검증은 이미 PRD상 확인된 사양(결함이 아님)이며, 데이터 품질 이슈에 그쳐 영향이
  낮다(Impact 2). 형식/길이 제한이 없다는 부재 상태를 재확인하는 Boundary 테스트로 결함 발생
  가능성은 일반 수준이다(Likelihood 2).
- **TC-SIGNUP-DELETE-ACCOUNT-010**: Impact 5 / Likelihood 2 / Risk Score 10 — 계정삭제는 되돌릴
  수 없는 핵심 동작이며, 확인 절차 없이 즉시 처리된다는 요구사항이 깨지면(예: 의도치 않게 삭제되지
  않거나 반대로 확인 없이 처리되어야 할 상황에서 별도 확인이 끼어드는 등) 사용자 신뢰와 데이터에
  중대한 영향을 준다(Impact 5). 단일 메뉴 클릭 동작이라 결함 발생 가능성 자체는
  낮다(Likelihood 2).
- **TC-SIGNUP-DELETE-ACCOUNT-011**: Impact 5 / Likelihood 3 / Risk Score 15 — 계정삭제가
  실제로 완료되었음을 사용자에게 알리는 최종 확인 지점으로, 실패 시 삭제 여부를 사용자가 신뢰하기
  어려워진다(Impact 5). 페이지 이동/안내 문구/버튼/네비게이션 전환을 함께 검증해야 하는 복합
  시나리오라 결함 발생 가능성이 일반 수준 이상이다(Likelihood 3, 단 회원가입 완료 확인
  TC-SIGNUP-DELETE-ACCOUNT-005보다는 사전 단계의 입력값 검증이 없어 Likelihood를 4가 아닌
  3으로 평가함).
- **TC-SIGNUP-DELETE-ACCOUNT-012**: Impact 3 / Likelihood 2 / Risk Score 6 — 계정삭제 자체는
  이미 이전 단계에서 완료된 상태이므로, 이 TC가 실패해도 핵심 동작(삭제)에는 영향이 없고 이후
  페이지 이동 UX 문제에 그친다(Impact 3). 단순 버튼 클릭에 의한 페이지 이동이라 결함 발생
  가능성은 낮다(Likelihood 2).
- **TC-SIGNUP-DELETE-ACCOUNT-013**: Impact 4 / Likelihood 3 / Risk Score 12 — 삭제된 계정으로
  재로그인이 가능하다면 계정 삭제가 실질적으로 이루어지지 않았다는 뜻이 되어 보안/데이터 정합성에
  중대한 영향을 준다(Impact 4). 회원가입-삭제-로그인 여러 기능에 걸친 데이터 흐름을 검증해야 해
  결함 발생 가능성이 일반 수준 이상이다(Likelihood 3).
- **TC-SIGNUP-DELETE-ACCOUNT-014**: Impact 3 / Likelihood 3 / Risk Score 9 — 삭제된 이메일의
  재사용 가능 여부는 사용자 편의 기능으로, 실패해도 보안 문제로 이어지지는 않고 재가입이 막히는
  정도의 영향이다(Impact 3). 계정삭제-회원가입 두 기능에 걸친 데이터 흐름(이메일 잠금 해제 처리)을
  검증해야 해 결함 발생 가능성이 일반 수준 이상이다(Likelihood 3).
- **TC-SIGNUP-DELETE-ACCOUNT-015** (결함 의심): Impact 3 / Likelihood 3 / Risk Score 9 —
  실제 계정이 생성되지 않으므로 데이터 무결성 자체에 영향은 없으나, 인증/처리 여부와 무관하게
  완료 페이지가 노출되는 것은 사용자에게 잘못된 정보를 제공하는 문제이다(Impact 3). 이미 사용자
  실측을 통해 로그인/로그아웃 두 상태 모두에서 재현이 확인된 결함 의심 사항으로 발생 가능성이
  높다(Likelihood 3).
- **TC-SIGNUP-DELETE-ACCOUNT-016** (결함 의심): Impact 4 / Likelihood 3 / Risk Score 12 —
  미인증 상태에서도 "계정이 삭제되었다"는 성공 메시지가 노출되는 것은 실제 데이터 변경은 없지만
  사용자에게 실제 계정 상태를 오인하게 만들 수 있는 인가(authorization) 체크 부재 성격의 문제로,
  단순 정보 노출형 결함(TC-SIGNUP-DELETE-ACCOUNT-015)보다 영향이 크다고 판단했다(Impact 4).
  이미 사용자 실측을 통해 재현이 확인된 결함 의심 사항으로 발생 가능성이 높다(Likelihood 3).

## 사용자 확인 필요 사항

1. **TC-SIGNUP-DELETE-ACCOUNT-001 병합 설계**: REQ-SIGNUP-DELETE-ACCOUNT-001(상세 정보 페이지로
   이동)과 REQ-SIGNUP-DELETE-ACCOUNT-002(입력값 자동 반영)는 "Signup 클릭"이라는 동일한 단일
   동작에서 함께 관찰되는 두 가지 결과이므로, `login-logout.md` TC-LOGIN-LOGOUT-004(로그인 성공
   시 랜딩+메뉴 전환 병합)와 동일한 방식으로 하나의 TC로 병합했습니다. 이 설계가 적절한지 확인
   부탁드립니다.
   [확인 완료, 2026-08-22] 동의/적절함, 변경 없음
2. **계정삭제 TC의 테스트 데이터 정책**: 계정삭제(TC-SIGNUP-DELETE-ACCOUNT-010~014,
   TC-SIGNUP-DELETE-ACCOUNT-016)는 Project PRD의 재사용 테스트 계정(actest1~3@test.com)을
   대상으로 사용하지 않고, 별도로 신규 가입한 "삭제 전용" 테스트 계정을 사용하도록 Preconditions를
   설계했습니다. 이 원칙에 동의하시는지, 혹은 다른 방식(예: 재사용 계정 중 하나를 이번 기회에
   실제로 삭제 처리)을 의도하셨는지 확인 부탁드립니다.
   [확인 완료, 2026-08-22] 동의/적절함, 변경 없음
3. **TC-SIGNUP-DELETE-ACCOUNT-016(REQ-017) Test Steps 설계**: 로그아웃 상태에서 `/delete_account`
   URL에 직접 접근하는 것만 확인하고, 실제 다른 계정이 삭제되지 않았는지에 대한 별도 확인 절차는
   포함하지 않았습니다(URL 접근 시 세션이 없어 삭제 대상 계정 자체가 특정되지 않으므로, PRD에
   기술된 "실제로는 삭제되지 않았다"는 사실이 이 접근 경로 자체로 이미 성립한다고 판단했습니다).
   이 설계가 적절한지 확인 부탁드립니다.
   [확인 완료, 2026-08-22] 동의/적절함, 변경 없음
4. **Priority 산정값**: 위 "Priority 산정 근거"에 제시된 각 TC의 Impact/Likelihood 평가와 최종
   Priority(P0 1건 — TC-005, P1 8건, P2 7건)에 동의하시는지 확인 부탁드립니다.
   [확인 완료, 2026-08-22] 동의/적절함, 변경 없음
5. **결함 의심 항목 반영**: REQ-SIGNUP-DELETE-ACCOUNT-016, 017을 `tc-writing` Skill 4.6에 따라
   별도 "결함 의심 항목" 섹션(TC-SIGNUP-DELETE-ACCOUNT-015~016)으로 분리해 포함했습니다. 특히
   TC-SIGNUP-DELETE-ACCOUNT-016은 `login-logout.md`와 `top-navigation.md`에서 본 문서로
   위임하기로 했던 항목입니다. 이 반영 방식에 동의하시는지 확인 부탁드립니다.
   [확인 완료, 2026-08-22] 동의/적절함, 변경 없음

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-22 | 최초 작성 (승인완료된 Feature PRD `signup-delete-account.md`의 REQ-SIGNUP-DELETE-ACCOUNT-001~015 기반 정상 케이스 TC-SIGNUP-DELETE-ACCOUNT-001~014 초안 작성, REQ-016/017(결함 의심)은 `tc-writing` Skill 4.6에 따라 별도 "결함 의심 항목" 섹션에 TC-SIGNUP-DELETE-ACCOUNT-015~016으로 작성. REQ-017은 `login-logout.md`/`top-navigation.md`에서 위임된 사항을 반영) | 초안 |
| 2026-08-22 | 사용자 최종 승인 ("사용자 확인 필요 사항" 1~5번 전 항목 변경 없이 동의/적절함으로 확인) | 승인완료 |
| 2026-08-30 | Phase 2 Task 8(회원가입 완료 테스트) 자동화 테스트 실행 중 발견된 실제 사이트 동작과의 불일치를 사용자 확인 후 반영. TC-SIGNUP-DELETE-ACCOUNT-006의 Test Scenario/Expected Result를 "Continue 클릭 시 로그아웃 상태 유지"에서 "Continue 클릭 시 로그인 상태로 전환(방금 생성한 계정으로 자동 로그인됨, "Logged in as {Name}" 노출)"으로 수정. Selenium 기반 pytest 실행으로 3회 독립 재현(스크린샷 확인)해 실제 동작을 검증했으며, 사용자가 "제안한 내용으로 관련 문서 전부 업데이트"를 승인함. | 승인완료 |
