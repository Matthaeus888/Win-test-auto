# 발견 결함 목록

자동화 테스트를 실행하는 과정에서 발견한, **자동화 코드가 아니라 실제 대상 서비스
(`automationexercise.com`)의 결함으로 판정된 항목**만 이 디렉터리에 정식 리포트로
기록합니다.

판정 기준은 [`CLAUDE.md` 13절](../../CLAUDE.md)의 "실패 원인 분류" 원칙(Automation
Code / Test Data / Test Environment / 실제 Product 문제)을 따르며, 아래 항목은 모두
**실제 Product 문제**로 분류된 것들입니다. 분류 근거와 재현 절차는 각 리포트에 상세히
기록되어 있습니다.

| ID | 제목 | 심각도 | 상태 | 관련 TC |
|---|---|---|---|---|
| [DEF-001](./DEF-001-logout-session-not-terminated.md) | `/logout` 접근 시 서버 세션이 종료되지 않고 로그인 상태로 Home에 랜딩 | High | 재현 확인(간헐적) | TC-LOGIN-LOGOUT-014, 015 |
| [DEF-002](./DEF-002-logout-server-error-disclosure.md) | 로그아웃 상태에서 `/logout` 접근 시 Django 디버그 에러 페이지 노출(정보 노출) | Medium | 재현 확인(간헐적) | TC-LOGIN-LOGOUT-016 |

## 왜 이 문서가 있는가

QA 자동화의 목적은 "테스트를 통과시키는 것"이 아니라 **실제 결함을 찾아내는 것**입니다.
이 프로젝트에서는 자동화 테스트 실행 중 두 차례 실제 결함을 발견했고, 발견 즉시
- 자동화 코드/테스트 데이터/환경 문제가 아님을 재현 절차로 검증하고
- Assertion을 완화하거나 실패를 우회 처리하지 않고 그대로 FAILED로 보고하며
- 근본 원인(서버 로그, HTTP 상태 코드)까지 추적한 뒤

정식 결함 리포트로 남겼습니다. 이 판단·기록 과정 자체가 이 프로젝트가 증명하려는
QA 역량입니다.
