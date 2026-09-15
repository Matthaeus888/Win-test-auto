---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정
대상 TC 문서: docs/tc/login-logout.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-08-22
관련 Feature PRD: feature/login-logout.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-08-23
최근 변경일: 2026-08-24
최근 Sheet 동기화일: 2026-08-23
확정일: 2026-08-24
---

# Automation Candidate 평가 - 로그인/로그아웃

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-LOGIN-LOGOUT-001 | 2 | 3 | 5 | 5 | 1 | 1 | 21 | Hold | 단순 UI 레이아웃 노출 확인(Skill 4.2 후순위 신호)으로 Business Criticality가 낮음(2). Result Determinism/Automation Stability는 높고 자동화 비용도 매우 낮아 Score는 21(후보 구간)이나, 비즈니스 영향이 낮아 자동화 ROI가 애매함 — 사용자 검토 필요. |
| TC-LOGIN-LOGOUT-002 | 5 | 5 | 5 | 5 | 1 | 1 | 26 | Yes | 로그인 기능 진입점(핵심 Flow)이며 매 Release 반복 검증되는 안정적 네비게이션 클릭 동작. 6개 축 모두 우수해 자동화 적극 권장. |
| TC-LOGIN-LOGOUT-003 | 5 | 5 | 5 | 5 | 1 | 1 | 26 | Yes | TC-002와 동일하게 로그인 진입점을 검증하되 URL 직접 접근이라는 별도 경로를 검증(별도 Risk Coverage, 중복 아님). 자동화 적극 권장. |
| TC-LOGIN-LOGOUT-004 | 5 | 5 | 4 | 5 | 3 | 2 | 26 | Yes | 로그인 핵심 Happy Path(P0). 랜딩 URL/세션/네비게이션 전환을 함께 검증하는 시나리오로 실패 시 핵심 기능 사용 불가. 최우선 자동화 대상. |
| TC-LOGIN-LOGOUT-005 | 4 | 5 | 4 | 5 | 2 | 1 | 25 | Yes | 존재하지 않는 이메일 로그인 시 에러 메시지 노출을 검증하는 핵심 Negative Case. 에러 메시지 텍스트로 deterministic 판정 가능하고 매 Release 반복 검증됨. |
| TC-LOGIN-LOGOUT-006 | 4 | 5 | 4 | 5 | 3 | 2 | 25 | Yes | TC-005와 유사하나 "이메일/비밀번호 오류를 구분하지 않는다"는 별도 요구사항(별도 Risk Coverage)을 검증하므로 중복 아님. 유효 계정 준비가 필요해 유지비용이 TC-005보다 약간 높으나 여전히 낮은 수준. |
| TC-LOGIN-LOGOUT-007 | 2 | 2 | 5 | 4 | 1 | 2 | 18 | No | 브라우저 native HTML5 유효성 검사 자체를 검증하는 TC로 애플리케이션 로직 변경에 의해 회귀할 가능성이 낮음(BC/RF 낮음). 기술적으로는 판정 가능하나(RD 4) 반복 자동 회귀 검증 실익(Regression ROI)이 낮음(Skill 4.2/4.3 참조)해 자동화 후순위로 판단. |
| TC-LOGIN-LOGOUT-008 | 2 | 2 | 5 | 4 | 1 | 1 | 19 | No | TC-007과 동일하게 브라우저 native 필수 입력 검증을 확인하는 TC로 Regression ROI가 낮아 자동화 후순위로 판단. |
| TC-LOGIN-LOGOUT-009 | 2 | 2 | 5 | 4 | 1 | 1 | 19 | No | TC-007/008과 동일 성격(브라우저 native 필수 입력 검증)의 TC로 동일 사유로 자동화 후순위. |
| TC-LOGIN-LOGOUT-010 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | 로그인 상태에서 `/login` 재진입 시 Home 리다이렉트되는 실제 route guard 로직을 검증. UX 저하 가능성이 있는 실제 애플리케이션 동작이며 URL로 deterministic 판정 가능. |
| TC-LOGIN-LOGOUT-011 | 4 | 4 | 4 | 5 | 2 | 2 | 23 | Yes | 새로고침 후 세션 유지 여부를 검증하는 세션 관리 핵심 로직. 실패 시 사용자가 반복 로그인해야 하는 주요 불편 발생. |
| TC-LOGIN-LOGOUT-012 | 2 | 2 | 5 | 5 | 3 | 2 | 21 | Hold | 계정 잠금 정책 "부재"가 유지되는지 재확인하는 목적의 TC로, 정책 변경 가능성이 낮아 반복 검증 가치(RF)가 낮고 Business Criticality도 낮음(Skill 4.3 일회성 기능 신호에 근접). 자동화 비용 자체는 낮으나(Score 21) ROI가 애매해 사용자 판단이 필요함. |
| TC-LOGIN-LOGOUT-013 | 2 | 2 | 4 | 5 | 2 | 1 | 20 | Yes | 긴 문자열/특수문자 입력 시 별도 클라이언트 제한이 없음을 확인하는 경계값 Negative Case. 에러 메시지로 deterministic 판정 가능하고 자동화/유지비용이 매우 낮아 기존 로그인 Negative Case 자동화 스위트에 낮은 추가비용으로 포함 가능. |
| TC-LOGIN-LOGOUT-014 | 5 | 5 | 5 | 5 | 2 | 2 | 26 | Yes | 로그아웃 핵심 동작(상단 메뉴 클릭). 실패 시 세션이 종료되지 않아 보안 영향이 있으며 매 Release 반복 검증되는 핵심 회귀. |
| TC-LOGIN-LOGOUT-015 | 5 | 4 | 5 | 5 | 2 | 2 | 25 | Yes | TC-014와 달리 URL 직접 접근이라는 별도 진입 경로로 로그아웃을 검증(별도 Risk Coverage, 중복 아님). |
| TC-LOGIN-LOGOUT-016 | 5 | 2 | 1 | 5 | 1 | 5 | 15 | No | [Hard Rule 적용] 현재 발생 중인 결함(로그아웃 상태에서 `/logout` 접근 시 Django 서버 에러 페이지 노출 — KeyError, Traceback 등 디버그 정보 노출)을 정상 Expected Result처럼 고정한 TC. Skill 5절 Hard Rule에 따라 점수(참고 15)와 무관하게 Candidate: No로 처리. 결함이 수정되고 TC/PRD가 정상 요구사항으로 재승인되면 재평가 가능. |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-LOGIN-LOGOUT-001 | Approved | 해당 화면은 변경가능성이 적은 부분이며, 사용자가 로그인시 필수적인 부분으로 자동화 대상 적용 |
| TC-LOGIN-LOGOUT-002 | Approved | |
| TC-LOGIN-LOGOUT-003 | Approved | |
| TC-LOGIN-LOGOUT-004 | Approved | |
| TC-LOGIN-LOGOUT-005 | Approved | |
| TC-LOGIN-LOGOUT-006 | Approved | |
| TC-LOGIN-LOGOUT-007 | Rejected | |
| TC-LOGIN-LOGOUT-008 | Rejected | |
| TC-LOGIN-LOGOUT-009 | Rejected | |
| TC-LOGIN-LOGOUT-010 | Approved | |
| TC-LOGIN-LOGOUT-011 | Approved | |
| TC-LOGIN-LOGOUT-012 | Rejected | 메뉴얼 테스트 비용이 3이지만 리그레이션 TC의 우선순위 P2이며, 정책 변경이 되지 않는 부분으로 자동화 제외 |
| TC-LOGIN-LOGOUT-013 | Approved | |
| TC-LOGIN-LOGOUT-014 | Approved | |
| TC-LOGIN-LOGOUT-015 | Approved | |
| TC-LOGIN-LOGOUT-016 | Rejected | |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다. 2026-08-24 재조회 결과를 반영했습니다(가공/재해석 없이 Sheet 값 그대로 옮김).

## Hard Rule 적용 / Validation 특이사항

- **TC-LOGIN-LOGOUT-016**: `docs/tc/login-logout.md`의 "결함 의심 항목" 섹션에 포함된 TC로,
  현재 발생 중인 결함(로그아웃 상태에서 `/logout` 직접 접근 시 Django 서버 에러 페이지가
  KeyError/Traceback 등 디버그 정보와 함께 그대로 노출됨)을 정상 Expected Result로 고정하고
  있습니다. `automation-candidate` Skill 5절 Hard Rule에 따라 Automation Score와 무관하게
  Candidate: No로 처리했습니다. 이 결함이 수정되고 TC/PRD가 정상 동작 기준으로 재승인되면
  다시 일반 TC로 재평가할 수 있습니다.
- 2026-08-24 Sheet 재조회 및 확정 전 Validation 결과(사전 점검, 아직 최종 확정 처리는
  수행하지 않음):
  - TC ID 유효성/중복: Sheet의 16개 TC ID(TC-LOGIN-LOGOUT-001~016) 모두 원본 TC 문서
    (`docs/tc/login-logout.md`, 결함 의심 항목 섹션의 016 포함)에 실제로 존재함을 확인했고,
    Sheet 내 중복 행은 없었습니다.
  - QA Decision 값 검증: 16건 모두 정확히 `Approved` 또는 `Rejected` 값이었습니다(공백/오탈자/
    대소문자 변형 없음). 미검토(빈 값) 0건, 잘못된 값(Validation Error) 0건, Hold 0건입니다.
  - 원본 TC 문서 상태: `docs/tc/login-logout.md`는 여전히 `상태: 승인완료`입니다.
  - TC 변경 여부: 이 문서 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-22)과
    현재 원본 TC 문서의 "최근 변경일"(2026-08-22)이 일치하여, 평가 이후 원본 TC가 변경된 사실이
    없습니다.
  - 결론: 4가지 Validation을 모두 통과했습니다. 다만 "자동화 대상 확정"은 사용자의 명시적 요청이
    있을 때만 수행하므로, 이번에는 결과 요약과 승인 요청까지만 진행하고 문서 상태를
    `자동화대상확정`으로 전환하지 않았습니다.

## Approved TC 목록 (자동화 대상 확정)

사용자가 채팅에서 직접 "네, 확정해줘"라고 명시적으로 확정 요청함에 따라(2026-08-24),
아래 11건을 최종 자동화 대상으로 확정합니다.

- TC-LOGIN-LOGOUT-001
- TC-LOGIN-LOGOUT-002
- TC-LOGIN-LOGOUT-003
- TC-LOGIN-LOGOUT-004
- TC-LOGIN-LOGOUT-005
- TC-LOGIN-LOGOUT-006
- TC-LOGIN-LOGOUT-010
- TC-LOGIN-LOGOUT-011
- TC-LOGIN-LOGOUT-013
- TC-LOGIN-LOGOUT-014
- TC-LOGIN-LOGOUT-015

자동화 제외(Rejected) 5건: TC-LOGIN-LOGOUT-007, 008, 009, 012, 016
(TC-016은 Hard Rule 적용 결과이며, 관련 결함이 수정되고 TC/PRD가 재승인되면 재평가 가능)

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-23 | 승인완료 상태의 `docs/tc/login-logout.md`(TC-LOGIN-LOGOUT-001~016) 최초 1차 자동화 후보 평가. Feature PRD(`docs/prd/feature/login-logout.md`, 승인완료)를 맥락 참고. TC-016은 Hard Rule 적용으로 Candidate: No. | 평가중 |
| 2026-08-24 | Google Sheet(Automation Candidates 워크시트) 최초 재조회. QA Decision 16건 전부 입력 완료(Approved 11 / Rejected 5 / Hold 0, 미검토 0). 확정 전 Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부) 4개 항목 모두 통과. 사용자의 명시적 "자동화 대상 확정" 요청 전이므로 상태는 자동확정 처리하지 않고 사용자검토완료로 전환. | 사용자검토완료 |
| 2026-08-24 | 사용자가 채팅에서 직접 "네, 확정해줘"라고 명시적으로 확정 요청. Approved 11건(TC-001,002,003,004,005,006,010,011,013,014,015)을 최종 자동화 대상으로 확정하고 Rejected 5건(TC-007,008,009,012,016)은 자동화 제외로 확정. | 자동화대상확정 |
