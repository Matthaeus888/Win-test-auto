---
문서유형: Feature PRD
상태: 승인완료
관련 Project PRD: project-prd.md
최초 작성일: 2026-08-20
최근 변경일: 2026-08-30
승인일: 2026-08-20
---

# Feature PRD - 회원가입 / 계정삭제

## 1. 개요

automationexercise.com에서 신규 사용자가 계정을 생성(회원가입)하고, 로그인 상태의 사용자가
자신의 계정을 삭제(계정삭제)하는 기능이다. 회원가입은 로그인 페이지에서 Name/Email을 먼저
입력한 뒤 별도 페이지에서 상세 정보를 입력하는 2단계 플로우로 구성되며, 계정삭제는 로그인
상태에서 상단 네비게이션을 통해 별도 확인 절차 없이 즉시 처리된다.

## 2. 관련 Project PRD 참조

- `/docs/prd/project-prd.md` (상태: 승인완료)
- Project PRD "5. 대상 Feature 목록" 중 "회원가입 / 계정삭제" 항목에 해당

## 3. 사용자 조작 시나리오

**회원가입 시나리오**

1. 로그아웃 상태에서 로그인 페이지(`/login`)의 "New User Signup!" 영역에 Name, Email Address를
   입력하고 "Signup" 버튼을 클릭한다.
2. 상세 정보 입력 페이지(`/signup`, "ENTER ACCOUNT INFORMATION")로 이동하며, 1단계에서 입력한
   Name/Email 값이 자동으로 반영되어 노출된다.
3. Password 등 필수 항목과 필요 시 선택 항목을 입력하고 "Create Account" 버튼을 클릭한다.
4. "ACCOUNT CREATED!" 완료 페이지(`/account_created`)로 이동한다. 이 페이지의 상단 네비게이션은
   로그아웃 상태 메뉴로 노출된다.
5. "Continue" 버튼을 클릭하면 방금 생성한 계정으로 자동 로그인되어 로그인 상태로 Home에 랜딩된다.

**계정삭제 시나리오**

1. 로그인 상태에서 상단 네비게이션의 "Delete Account"를 클릭한다.
2. 별도 확인 절차 없이 즉시 계정이 삭제 처리되고, "ACCOUNT DELETED!" 완료 페이지(`/delete_account`)로
   이동한다. 이 페이지의 상단 네비게이션도 로그아웃 상태 메뉴로 노출된다.
3. "Continue" 버튼을 클릭하면 로그아웃 상태로 Home으로 랜딩된다.

## 4. Requirements

### 4.1 확인된 요구사항

**회원가입**

- **REQ-SIGNUP-DELETE-ACCOUNT-001**: 로그인 페이지의 "New User Signup!" 영역에서 Name, Email
  Address 입력 후 "Signup" 클릭 시 상세 정보 입력 페이지(`/signup`, "ENTER ACCOUNT INFORMATION")로
  이동한다.
- **REQ-SIGNUP-DELETE-ACCOUNT-002**: 이전 단계에서 입력한 Name/Email 값이 상세 정보 입력
  페이지에도 자동으로 반영되어 노출된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-003**: 상세 정보 입력 페이지는 상단(Title, Name*, Email*,
  Password*, Date of Birth, "Sign up for our newsletter!" 체크박스, "Receive special offers
  from our partners!" 체크박스)과 ADDRESS INFORMATION(First name*, Last name*, Company,
  Address*, Address 2, Country*, State*, City*, Zipcode*), 하단(Mobile Number*, "Create
  Account" 버튼)으로 구성된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-004**: 필수 입력 필드는 페이지 내 "*" 로 표기된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-005**: 선택 필드(Title, Date of Birth, 체크박스 2종, Company,
  Address 2 등)를 입력하지 않아도 필수 필드만 충족하면 가입이 가능하다.
- **REQ-SIGNUP-DELETE-ACCOUNT-006**: 정상 가입 완료 시 "ACCOUNT CREATED!" 페이지
  (`/account_created`)로 이동하며, "Congratulations! Your new account has been successfully
  created!" 등의 안내 문구와 "Continue" 버튼이 노출된다. 이 페이지의 상단 네비게이션은 로그아웃
  상태 메뉴로 표시된다(자동 로그인되지 않음).
- **REQ-SIGNUP-DELETE-ACCOUNT-007**: "ACCOUNT CREATED!" 페이지에서 "Continue" 클릭 시, 방금
  생성한 계정으로 자동 로그인되어 로그인 상태로 Home으로 랜딩된다(상단 네비게이션이 "Logged in
  as {Name}" 등 로그인 상태 메뉴로 전환됨).
- **REQ-SIGNUP-DELETE-ACCOUNT-008**: 이미 가입된 이메일로 재가입 시도 시, 페이지 전환 없이
  로그인/가입 폼 화면이 그대로 유지되고 Email 입력란 하단에 "Email Address already exist!"
  에러 메시지가 노출된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-009**: 상세 정보 입력 페이지에서 필수(*) 필드를 비운 채 "Create
  Account" 클릭 시, 로그인 폼과 동일하게 브라우저 native(HTML5) 필수 입력 검증 팝업("이 입력란을
  작성하세요.")이 노출되며 폼 제출이 차단된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-010**: Mobile Number 입력란에는 숫자가 아닌 값도 입력 가능하며,
  별도의 형식/길이 제한 검증이 존재하지 않는다. 필수값만 충족하면 형식과 무관하게 가입이 가능하다.

**계정삭제**

- **REQ-SIGNUP-DELETE-ACCOUNT-011**: 로그인 상태에서 상단 네비게이션의 "Delete Account" 클릭 시,
  별도 확인(컨펌) 절차 없이 즉시 삭제 처리된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-012**: 삭제 처리 후 "ACCOUNT DELETED!" 완료 페이지
  (`/delete_account`)로 이동하며, "Your account has been permanently deleted!" 등의 안내
  문구와 "Continue" 버튼이 노출된다. 이 페이지의 상단 네비게이션도 로그아웃 상태 메뉴로 표시된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-013**: "ACCOUNT DELETED!" 페이지에서 "Continue" 클릭 시 로그아웃
  상태로 Home으로 랜딩된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-014**: 삭제된 계정의 이메일/비밀번호로 재로그인을 시도하면
  로그인되지 않으며, "Your email or password is incorrect!" 에러 메시지가 노출되고 로그인 폼
  화면이 유지된다(로그인/로그아웃 Feature PRD의 REQ-LOGIN-LOGOUT-005와 동일한 동작 패턴).
- **REQ-SIGNUP-DELETE-ACCOUNT-015**: 삭제된 계정의 이메일로 재가입을 시도하면 "이미 존재하는
  이메일" 에러 없이 정상적으로 신규 가입이 진행된다(계정 삭제 시 해당 이메일이 재사용 가능한
  상태로 해제됨).

**발견된 이슈 (결함 의심)**

- **REQ-SIGNUP-DELETE-ACCOUNT-016**: 실제 회원가입 절차를 거치지 않고 URL(`/account_created`)에
  직접 접근해도 "ACCOUNT CREATED!" 완료 페이지가 그대로 노출된다. 로그인 상태/로그아웃 상태
  양쪽 모두에서 재현된다.
- **REQ-SIGNUP-DELETE-ACCOUNT-017**: 로그아웃 상태(미인증)에서 계정삭제 URL(`/delete_account`)에
  직접 접근하면, 실제로 인증되어 있지 않고 계정이 삭제되지도 않았음에도 "ACCOUNT DELETED!"
  성공 페이지가 그대로 노출된다.

### 4.2 미확인 / 추가 확인 필요 항목

- 현재 없음 (이번 인터뷰를 통해 제기되었던 항목이 모두 확인 완료됨)

## 5. Feature 단위 In Scope / Out of Scope

**In Scope**

- 회원가입 정상 플로우(1차 Name/Email 입력 → 상세 정보 입력 → 계정 생성)와 관련 필드 구성/
  필수값 검증
- 회원가입 예외 케이스(중복 이메일, 필수 필드 미입력, Mobile Number 형식 미검증)
- 계정삭제 정상 플로우(확인 절차 없는 즉시 삭제) 및 완료 페이지 동작
- 삭제된 계정 이메일의 재사용 가능 여부(재로그인 실패, 재가입 가능)
- 회원가입/계정삭제 완료 후 상단 네비게이션 메뉴 표시 상태(로그아웃 상태 메뉴로 표시)
- 발견된 결함: `/account_created`, `/delete_account` URL 직접 접근 시 나타나는 비정상 동작

**Out of Scope**

- 로그인/로그아웃 자체의 상세 동작 — `feature/login-logout.md` 범위
- 네트워크 연결 끊김 등 브라우저/OS 레벨 환경 요인에 의한 동작(오프라인 에러 페이지 등)
- 계정삭제/가입 처리에 대한 지연시간(로딩) 관련 정책 검증 — 명시적 정책이 확인되지 않음
- 이메일 인증 절차 — Project PRD Out of Scope와 일치
- 결제 기능 — Project PRD Out of Scope와 일치

## 6. 예외 / 에러 케이스

- 이미 가입된 이메일로 재가입 시도: "Email Address already exist!" 에러
  (REQ-SIGNUP-DELETE-ACCOUNT-008)
- 상세 정보 입력 페이지 필수 필드 미입력: 브라우저 native 필수 입력 검증 팝업, 폼 제출 차단
  (REQ-SIGNUP-DELETE-ACCOUNT-009)
- 삭제된 계정 이메일로 재로그인 시도: "Your email or password is incorrect!" 에러
  (REQ-SIGNUP-DELETE-ACCOUNT-014)
- [결함 의심] `/account_created` 직접 접근 시 완료 페이지 비정상 노출
  (REQ-SIGNUP-DELETE-ACCOUNT-016)
- [결함 의심] 로그아웃 상태에서 `/delete_account` 직접 접근 시 삭제 성공 페이지 비정상 노출
  (REQ-SIGNUP-DELETE-ACCOUNT-017)

## 7. 비고

- REQ-SIGNUP-DELETE-ACCOUNT-016, REQ-SIGNUP-DELETE-ACCOUNT-017은 실제 Product 결함으로
  추정되는 사항이며, 이 PRD에서는 발견된 사실만 기록한다. 결함 자체의 수정이나 별도 이슈
  트래킹은 이 문서의 범위가 아니다.
- REQ-SIGNUP-DELETE-ACCOUNT-017은 `feature/login-logout.md` "7. 비고"에 "추후 계정삭제
  Feature PRD에 반영 예정"으로 메모되어 있던 사항을 이관하여 본 문서에서 정식 Requirement로
  다룬 것이다. `login-logout.md` 원본(승인완료 상태)은 수정하지 않았다.
- 네트워크 연결이 끊긴 상태에서 `/delete_account`에 접근 시 Chrome 자체의 오프라인 에러 페이지
  (`ERR_INTERNET_DISCONNECTED`)가 노출되는 것을 확인했으나, 이는 애플리케이션 동작이 아닌
  브라우저/네트워크 환경 요인으로 판단되어 Out of Scope로 처리했다.
- 추후 TC 작성 단계에서 REQ-SIGNUP-DELETE-ACCOUNT-016, 017을 Negative TC로 다룰지, 별도 결함
  리포트로 관리할지는 TC 작성 단계 및 사용자 판단에 따른다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-20 | 최초 작성 (Draft) | 초안 |
| 2026-08-20 | 사용자 최종 승인 | 승인완료 |
| 2026-08-30 | Phase 2 Task 8(회원가입 완료 테스트) 자동화 테스트 실행 중 발견된 실제 사이트 동작과의 불일치를 사용자 확인 후 반영. 3절 회원가입 시나리오 5단계와 REQ-SIGNUP-DELETE-ACCOUNT-007을 "Continue 클릭 시 로그아웃 상태 유지"에서 "Continue 클릭 시 방금 생성한 계정으로 자동 로그인되어 로그인 상태로 Home 랜딩"으로 수정. Selenium 기반 pytest 실행으로 3회 독립 재현(스크린샷 확인)해 실제 동작을 검증했으며, 사용자가 문서 갱신을 승인함. | 승인완료 |
