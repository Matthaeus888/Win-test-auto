---
문서유형: Feature PRD
상태: 승인완료
관련 Project PRD: project-prd.md
최초 작성일: 2026-08-20
최근 변경일: 2026-08-20
승인일: 2026-08-20
---

# Feature PRD - 로그인/로그아웃

## 1. 개요

automationexercise.com에서 사전에 등록된 계정 정보(Email Address, Password)로 인증하여
로그인 상태로 전환하고, 로그인 상태를 해제(로그아웃)하는 기능이다. 로그인 상태 여부에 따라
상단 네비게이션 메뉴 구성이 달라진다.

## 2. 관련 Project PRD 참조

- `/docs/prd/project-prd.md` (상태: 승인완료)
- Project PRD "5. 대상 Feature 목록" 중 "로그인 / 로그아웃" 항목에 해당

## 3. 사용자 조작 시나리오

**로그인 시나리오**

1. 로그아웃 상태에서 상단 네비게이션의 "Signup/Login" 클릭 또는 URL(`/login`) 직접 진입으로
   로그인 페이지에 접근한다.
2. "Login to your account" 영역의 Email Address, Password 입력란에 값을 입력하고
   "Login" 버튼을 클릭한다.
3. 정상 계정 정보 입력 시 로그인 처리되어 루트 URL(`https://automationexercise.com/`, Home)로
   랜딩되며, 상단 네비게이션이 로그인 상태 메뉴로 전환된다.

**로그아웃 시나리오**

1. 로그인 상태에서 상단 네비게이션의 "Logout" 클릭 또는 URL(`/logout`) 직접 진입으로
   로그아웃을 수행한다.
2. 로그아웃 처리되어 로그인 페이지(`/login`)로 랜딩되며, 상단 네비게이션이 로그아웃 상태
   메뉴로 전환된다.

## 4. Requirements

### 4.1 확인된 요구사항

**로그인**

- **REQ-LOGIN-LOGOUT-001**: 로그인 페이지는 "Login to your account" 영역(Email Address 입력란,
  Password 입력란, Login 버튼)과 "New User Signup!" 영역이 "OR" 아이콘으로 구분되어 함께
  노출된다.
- **REQ-LOGIN-LOGOUT-002**: 로그인 페이지 진입 경로는 (a) 상단 네비게이션 "Signup/Login" 클릭,
  (b) URL(`/login`) 직접 진입 두 가지이다.
- **REQ-LOGIN-LOGOUT-003**: 정상적인 이메일/비밀번호로 로그인하면 `https://automationexercise.com/`
  (루트, Home)로 랜딩되며 로그인 상태로 전환된다.
- **REQ-LOGIN-LOGOUT-004**: 로그인 성공 시 상단 네비게이션 메뉴가 로그인 상태 메뉴(Home,
  Products, Cart, Logout, Delete Account, Test Cases, API Testing, Video Tutorials,
  Contact us, "Logged in as {유저명}")로 변경된다.
- **REQ-LOGIN-LOGOUT-005**: 존재하지 않는 이메일 또는 올바르지 않은 비밀번호로 로그인 시도 시,
  두 경우 모두 동일하게 "Your email or password is incorrect!" 에러 메시지가 폼 하단에
  노출되고 로그인 폼 화면이 그대로 유지된다(이메일 오류/비밀번호 오류를 구분하지 않음).
- **REQ-LOGIN-LOGOUT-006**: `@`가 포함되지 않는 등 형식이 올바르지 않은 이메일 입력 후 Login
  클릭 시, 브라우저 자체(HTML5 native) 유효성 검사 팝업이 노출되며 폼 제출이 되지 않는다.
- **REQ-LOGIN-LOGOUT-007**: Email Address 입력란을 비운 채 Login 클릭 시, 브라우저 자체 필수
  입력 검증 팝업("이 입력란을 작성하세요.")이 노출되며 폼 제출이 되지 않는다.
- **REQ-LOGIN-LOGOUT-008**: Password 입력란을 비운 채 Login 클릭 시에도 동일하게 브라우저 자체
  필수 입력 검증 팝업이 노출되며 폼 제출이 되지 않는다.
- **REQ-LOGIN-LOGOUT-009**: 이미 로그인된 상태에서 `/login` URL로 직접 재진입하면 로그인 폼이
  아닌 Home(루트)으로 리다이렉트된다.
- **REQ-LOGIN-LOGOUT-010**: 로그인 상태는 새로고침(F5) 후에도 유지된다.
- **REQ-LOGIN-LOGOUT-011**: 로그인 실패가 반복되어도 별도의 계정 잠금/제한 정책은 존재하지
  않는다.
- **REQ-LOGIN-LOGOUT-012**: 로그인 폼 입력값(이메일/비밀번호)에는 이메일 형식 검증(HTML5
  native) 외에 별도의 길이 제한, 특수문자 제한 등 클라이언트 측 검증 규칙이 존재하지 않는다.

**로그아웃**

- **REQ-LOGIN-LOGOUT-013**: 로그아웃 수행 경로는 (a) 상단 네비게이션 "Logout" 클릭, (b) 로그인
  상태에서 URL(`/logout`) 직접 진입 두 가지이다.
- **REQ-LOGIN-LOGOUT-014**: 로그아웃 처리 시 로그인 페이지(`/login`)로 랜딩되며, 상단 네비게이션
  메뉴가 로그아웃 상태 메뉴(Home, Products, Cart, Signup/Login, Test Cases, API Testing,
  Video Tutorials, Contact us)로 변경된다.

**발견된 이슈 (결함 의심)**

- **REQ-LOGIN-LOGOUT-015**: 이미 로그아웃된 상태에서 `/logout` URL로 직접 접근하면, 정상 페이지
  대신 Django 서버 에러 페이지(`KeyError at /logout`, Exception Value `'user_id'`, 상세
  Traceback, 서버 파일 경로, Python/Django 버전 등)가 그대로 노출된다.

### 4.2 미확인 / 추가 확인 필요 항목

- 현재 없음 (이전에 제기된 미확인 항목은 모두 확인 완료됨)

## 5. Feature 단위 In Scope / Out of Scope

**In Scope**

- 로그인 정상/실패 플로우 및 관련 에러 메시지, 브라우저 native 유효성 검사 동작
- 로그아웃 정상 플로우
- 로그인/로그아웃 상태에 따른 상단 네비게이션 메뉴 변경
- 로그인 상태에서의 `/login` 재진입, 새로고침 시 상태 유지 등 URL/세션 관련 동작
- 로그아웃 상태에서 `/logout`에 직접 접근했을 때 나타나는 동작(발견된 결함 포함)

**Out of Scope**

- 세션/로그인 유지 기간(토큰 만료 정책) 상세 검증 — Project PRD의 "계정 토큰 관련 검증 제외"
  원칙과 일치
- 회원가입 자체의 상세 동작 — 별도 Feature PRD 범위
- 계정삭제 기능 자체의 동작 (정상 플로우 및 로그아웃 상태에서의 `/delete_account` 접근 이상
  동작 포함) — 별도 "계정삭제" Feature PRD 범위
- 네트워크 연결 끊김 등 브라우저/OS 레벨 환경 요인에 의한 동작(오프라인 에러 페이지 등)
- 로그인/로그아웃 처리에 대한 지연시간(로딩) 관련 정책 검증 — 명시적 정책이 확인되지 않음

## 6. 예외 / 에러 케이스

- 존재하지 않는 이메일 / 잘못된 비밀번호: "Your email or password is incorrect!" 에러 메시지
  (REQ-LOGIN-LOGOUT-005)
- 이메일 형식 오류, 필수 입력 누락: 브라우저 native 유효성 검사 팝업, 폼 제출 차단
  (REQ-LOGIN-LOGOUT-006, 007, 008)
- [결함 의심] 로그아웃 상태에서 `/logout` 직접 접근 시 서버 에러(KeyError) 노출
  (REQ-LOGIN-LOGOUT-015)

## 7. 비고

- REQ-LOGIN-LOGOUT-015는 실제 Product 결함으로 추정되는 사항이며, 이 PRD에서는 발견된 사실만
  기록한다. 결함 자체의 수정이나 별도 이슈 트래킹은 이 문서의 범위가 아니다.
- 추후 TC 작성 단계에서 위 항목을 Negative TC로 다룰지, 별도 결함 리포트로 관리할지는 TC 작성
  단계 및 사용자 판단에 따른다.
- **[별도 발견 사항 메모]** 로그아웃 상태(미인증)에서 계정삭제 URL(`/delete_account`)에 직접
  접근하면, 실제로 인증되어 있지 않고 계정이 삭제되지 않았음에도 "계정이 성공적으로
  삭제되었습니다"라는 성공 페이지가 그대로 랜딩되는 결함을 발견했다. 이 항목은 본 Feature PRD의
  범위(로그인/로그아웃)가 아니므로 Requirement로 포함하지 않으며, 추후 작성될 "계정삭제"
  Feature PRD에 반영할 예정이다.
- 네트워크 연결이 끊긴 상태에서는 Chrome 자체의 오프라인 에러 페이지(`ERR_INTERNET_DISCONNECTED`)가
  노출되며, 이는 애플리케이션 동작이 아닌 브라우저/네트워크 환경 요인으로 판단되어 Out of Scope로
  처리한다. 로그인/로그아웃 처리에 대한 별도 지연시간(로딩) 정책도 확인되지 않아 검증 범위에서
  제외한다. 이 내용은 `feature/signup-delete-account.md` 작성 중 `/delete_account` 접근 시
  확인된 사항이며, 모든 페이지 랜딩 시 동일한 방식으로 API 호출이 발생하는 사이트 공통 특성이므로
  로그인/로그아웃 페이지에도 동일하게 적용된다고 판단해 반영한다. 로그인/로그아웃 화면에서
  별도로 재현 테스트를 수행한 것은 아니다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-20 | 최초 작성 (Draft) | 초안 |
| 2026-08-20 | 사용자 최종 승인 | 승인완료 |
| 2026-08-20 | 문서 관리 구조 변경에 따라 저장 위치/파일명 변경 (/docs/prd/feature-prd-login-logout.md → /docs/prd/feature/login-logout.md, 본문 내용 변경 없음) | 승인완료 |
| 2026-08-20 | 사이트 공통 특성(오프라인 환경/지연시간 정책 부재)을 signup-delete-account.md와 일관되게 반영하기 위한 재승인 | 승인완료 |
