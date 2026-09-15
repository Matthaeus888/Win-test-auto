---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정
대상 TC 문서: docs/tc/signup-delete-account.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-08-22
관련 Feature PRD: feature/signup-delete-account.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-08-24
최근 변경일: 2026-08-27
최근 Sheet 동기화일: 2026-08-24
확정일: 2026-08-27
---

# Automation Candidate 평가 - 회원가입 / 계정삭제

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-SIGNUP-DELETE-ACCOUNT-001 | 5 | 5 | 5 | 5 | 1 | 1 | 26 | Yes | 회원가입 전체 퍼널의 진입점(로그인 페이지→상세정보 페이지 이동 + 입력값 자동 반영)으로 실패 시 회원가입 자체가 불가능해짐(login-logout.md TC-002/003과 동일 근거). 페이지 이동/입력값 반영을 URL/입력란 값으로 결정적 판정 가능하고 자동화·유지 비용이 매우 낮아 자동화 적극 권장. |
| TC-SIGNUP-DELETE-ACCOUNT-002 | 2 | 3 | 5 | 5 | 1 | 1 | 21 | Hold | 상세 정보 입력 페이지 3개 영역(상단/ADDRESS/하단) 노출 여부만 확인하는 단순 UI 레이아웃 검증(Skill 4.2 후순위 신호, login-logout.md TC-001과 동일 성격). Result Determinism/Automation Stability는 높고 자동화 비용도 매우 낮아 Score는 21(후보 구간)이나 비즈니스 영향이 낮아 ROI가 애매함 — 사용자 검토 필요. |
| TC-SIGNUP-DELETE-ACCOUNT-003 | 2 | 2 | 5 | 5 | 1 | 1 | 20 | Hold | "*" 필수 표기 여부만 확인하는 정적 텍스트 검증으로, 표기가 누락되어도 실제 필수값 검증(TC-004/008에서 별도 검증)에는 영향이 없어 Business Criticality가 낮음. Score 20이나 단순 UI 표기 확인(Skill 4.2)이라 ROI 판단을 위해 사용자 검토 필요. |
| TC-SIGNUP-DELETE-ACCOUNT-004 | 4 | 4 | 5 | 5 | 3 | 2 | 25 | Yes | 선택 필드를 비워도 가입이 가능해야 한다는 요구사항이 깨지면 다수 사용자가 가입 자체를 완료하지 못하게 되는 중요 시나리오(BC4). 완료 페이지 이동 여부로 결정적 판정 가능하고 요구사항 구조가 안정적이라 자동화 권장. |
| TC-SIGNUP-DELETE-ACCOUNT-005 | 5 | 5 | 4 | 5 | 3 | 2 | 26 | Yes | 회원가입 기능의 핵심 Happy Path(P0)로 완료 페이지 이동/안내 문구/버튼/네비게이션 전환을 함께 검증해야 하며, 실패 시 신규 계정 생성이 전면 불가능해짐(login-logout.md TC-004와 동일 근거). 최우선 자동화 대상. |
| TC-SIGNUP-DELETE-ACCOUNT-006 | 3 | 4 | 5 | 5 | 2 | 1 | 24 | Yes | 계정 생성 자체는 이전 단계에서 이미 완료된 상태라 실패해도 핵심 기능에는 영향이 없고 이후 페이지 이동 UX 문제에 그치나(BC3), 매 Release 반복 검증되는 단순 클릭 동작이며 자동화/유지 비용이 매우 낮아 자동화 권장. |
| TC-SIGNUP-DELETE-ACCOUNT-007 | 4 | 5 | 4 | 5 | 2 | 1 | 25 | Yes | 이미 가입된 이메일로 재가입 시도 시 에러 메시지 노출을 검증하는 핵심 Negative Case로, 실패 시 계정 데이터 유일성이 훼손되거나 사용자가 혼란을 겪을 수 있음. 에러 메시지 텍스트로 결정적 판정 가능하고 매 Release 반복 검증되어 자동화 권장. |
| TC-SIGNUP-DELETE-ACCOUNT-008 | 2 | 2 | 5 | 4 | 1 | 1 | 19 | No | 브라우저 native(HTML5) 필수 입력 검증 자체를 확인하는 TC로, `login-logout.md` TC-007~009와 동일한 성격(다만 폼/필드가 달라 완전한 중복은 아니며 별도 TC로 유지)이다. 기술적으로는 판정 가능하나(RD4) 애플리케이션 로직 변경에 의해 회귀할 가능성이 낮아(BC/RF 낮음) 반복 자동 회귀 검증 실익(Regression ROI)이 낮음(Skill 2.4/4.2/4.3 참조)해 자동화 후순위. |
| TC-SIGNUP-DELETE-ACCOUNT-009 | 2 | 2 | 5 | 5 | 3 | 2 | 21 | Hold | Mobile Number 형식 미검증이 유지되는지 재확인하는 목적의 TC로, PRD상 이미 확인된 사양(결함 아님)이 유지되는지 확인하는 성격이라 변경 가능성이 낮고 반복 검증 가치도 낮음(`login-logout.md` TC-012의 "정책 부재 재확인" 패턴과 유사, Skill 4.3 일회성 기능 신호에 근접). 다만 전체 회원가입 플로우를 거쳐야 해 1회 수행/유지 비용이 로그인 케이스보다 높아 자동화 비용 자체는 낮지 않음. Score 21이나 ROI가 애매해 사용자 검토 필요. |
| TC-SIGNUP-DELETE-ACCOUNT-010 | 5 | 4 | 5 | 5 | 4 | 3 | 26 | Yes | 계정삭제는 되돌릴 수 없는 핵심 동작이며, 확인 절차 없이 즉시 처리된다는 요구사항이 깨지면 사용자 신뢰와 데이터에 중대한 영향을 줌(BC5). 완료 페이지로의 즉시 이동 여부로 결정적 판정 가능. 삭제 전용 테스트 계정을 사전에 신규 가입해야 하는 절차상 비용(MTC4)과 테스트 데이터 준비/격리 필요성(MC3)이 있으나, 핵심 Risk 대비 자동화 실익이 커 최우선 자동화 대상. |
| TC-SIGNUP-DELETE-ACCOUNT-011 | 5 | 4 | 4 | 5 | 4 | 3 | 25 | Yes | 계정삭제가 실제로 완료되었음을 사용자에게 알리는 최종 확인 지점으로, 실패 시 삭제 여부를 사용자가 신뢰하기 어려워짐(BC5). 페이지 이동/안내 문구/버튼/네비게이션 전환을 함께 검증하는 복합 시나리오로 자동화 권장(사전 절차 비용은 TC-010과 동일하게 반영). |
| TC-SIGNUP-DELETE-ACCOUNT-012 | 3 | 4 | 5 | 5 | 3 | 2 | 24 | Yes | 계정삭제 자체는 이전 단계에서 이미 완료된 상태라 실패해도 핵심 동작(삭제)에는 영향이 없고 이후 페이지 이동 UX 문제에 그치나(BC3), 매 Release 반복 검증되는 단순 클릭 동작이며 결정적 판정이 가능해 자동화 권장. |
| TC-SIGNUP-DELETE-ACCOUNT-013 | 4 | 4 | 4 | 5 | 4 | 3 | 24 | Yes | 삭제된 계정으로 재로그인이 가능하면 계정 삭제가 실질적으로 이루어지지 않았다는 뜻이 되어 보안/데이터 정합성에 중대한 영향을 줌(BC4). 에러 메시지 텍스트는 `login-logout.md` TC-005/006과 동일하지만, 이 TC는 "삭제 처리가 실제 데이터에 반영되었는지"라는 별도 Risk Coverage(로그인 폼 자체의 검증 로직이 아니라 계정삭제 기능의 실효성)를 검증하므로 중복이 아니다(Skill 4.3). 가입→삭제까지 완료한 전용 계정이 필요해 비용은 다소 높으나(MTC4/MC3) 데이터 정합성 검증 가치가 커 자동화 권장. |
| TC-SIGNUP-DELETE-ACCOUNT-014 | 3 | 3 | 4 | 5 | 4 | 3 | 22 | Yes | 삭제된 계정 이메일이 재사용 가능한 상태로 해제되는지(회원가입-계정삭제 두 기능에 걸친 데이터 정합성)를 검증. 실패해도 재가입이 막히는 정도의 영향이라 BC/RF는 중간 수준이나(Score 22, 후보 구간), 완료 페이지 이동으로 결정적 판정 가능하고 데이터 정합성 회귀를 조기에 발견할 실익이 있어 자동화 권장. |
| TC-SIGNUP-DELETE-ACCOUNT-015 | 3 | 2 | 1 | 5 | 1 | 5 | 13 | No | [Hard Rule 적용] 현재 발생 중인 결함(회원가입 절차를 거치지 않고 `/account_created` URL에 직접 접근해도 "ACCOUNT CREATED!" 완료 페이지가 정상 가입 완료 시와 동일하게 노출됨)을 정상 Expected Result처럼 고정한 TC. `docs/tc/signup-delete-account.md` "결함 의심 항목" 섹션에 포함되어 있으며, Skill 5절 Hard Rule에 따라 점수(참고 13)와 무관하게 Candidate: No로 처리. 결함이 수정되고 TC/PRD가 정상 요구사항으로 재승인되면 재평가 가능. |
| TC-SIGNUP-DELETE-ACCOUNT-016 | 4 | 2 | 1 | 5 | 1 | 5 | 14 | No | [Hard Rule 적용] 현재 발생 중인 결함(로그아웃 상태/미인증 상태에서 `/delete_account` URL에 직접 접근해도 실제 삭제 처리 없이 "ACCOUNT DELETED!" 성공 페이지가 노출됨 — 인가 체크 부재 성격)을 정상 Expected Result처럼 고정한 TC. `login-logout.md`/`top-navigation.md`에서 본 Feature로 위임되었던 항목이며, `docs/tc/signup-delete-account.md` "결함 의심 항목" 섹션에 포함되어 있음. Skill 5절 Hard Rule에 따라 점수(참고 14)와 무관하게 Candidate: No로 처리. 결함이 수정되고 TC/PRD가 정상 요구사항으로 재승인되면 재평가 가능. |

## Cross-Feature 중복 검토 (Skill 4.3 TC 중복 여부)

사용자 요청에 따라, 이미 확정된 다른 Feature(login-logout 등)의 TC와 검증 목적이 실질적으로 동일한
항목이 있는지 별도로 확인했습니다(`page-ui.md` TC-040/041이 `cart.md` TC-012/013과 중복 판정된
사례와 동일한 관점의 점검).

- **TC-SIGNUP-DELETE-ACCOUNT-008 (브라우저 native 필수 입력 검증)**: `login-logout.md`
  TC-007~009(로그인 폼의 브라우저 native 검증)와 "브라우저 native 유효성 검사"라는 동일한 유형의
  동작을 다룬다는 점에서 판단 근거(Regression ROI 낮음)는 동일하다. 다만 검증 대상 폼/필드
  (로그인 폼의 Email/Password가 아니라 회원가입 상세 정보 페이지의 필수 필드)가 서로 다르고
  Test Steps도 다르므로, Skill 4.3의 "검증 목적이 실질적으로 동일한 중복"에는 해당하지 않는다고
  판단했습니다(완전한 중복 제외가 아니라 별도 TC로 유지하되, 동일한 판단 근거로 Candidate: No).
- **TC-SIGNUP-DELETE-ACCOUNT-013 (삭제된 계정 재로그인 시 에러 메시지)**: `login-logout.md`
  TC-005/006과 노출되는 에러 메시지 문구는 동일("Your email or password is incorrect!")하지만,
  이 TC는 "계정삭제 처리가 실제 데이터에 반영되었는지"라는 계정삭제 기능 고유의 Risk Coverage를
  검증하는 것이며 로그인 폼 자체의 검증 로직을 재검증하는 것이 아니다. 별도 Risk Coverage가
  존재하므로 중복으로 판단하지 않았습니다(Skill 4.3).
- **TC-SIGNUP-DELETE-ACCOUNT-016**: `login-logout.md` "7. 비고"와 `top-navigation.md` "결함
  의심 항목" 섹션에서 본 Feature로 위임하기로 명시된 항목입니다. 두 문서 모두 해당 항목을 자체
  TC로 보유하고 있지 않음(위임 완료 상태)을 확인했으며, `docs/tc/automation-candidates/` 하위에도
  `top-navigation.md`/`login-logout.md`에 중복 평가된 동일 항목이 없어 이번 평가에서만 1회
  평가했습니다.
- 그 외 TC-001~007, 009~012, 014, 015는 다른 확정 Feature(login-logout, cart, page-ui)의 TC와
  검증 대상 화면/로직이 겹치지 않아 중복 신호를 발견하지 못했습니다.

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-SIGNUP-DELETE-ACCOUNT-001 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-002 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-003 | Rejected | |
| TC-SIGNUP-DELETE-ACCOUNT-004 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-005 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-006 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-007 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-008 | Rejected | |
| TC-SIGNUP-DELETE-ACCOUNT-009 | Rejected | |
| TC-SIGNUP-DELETE-ACCOUNT-010 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-011 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-012 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-013 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-014 | Approved | |
| TC-SIGNUP-DELETE-ACCOUNT-015 | Rejected | |
| TC-SIGNUP-DELETE-ACCOUNT-016 | Rejected | |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다. 2026-08-27 재조회(candidate-list) 결과 TC-SIGNUP-DELETE-ACCOUNT-001~016
> 전체 QA Decision이 입력 완료되었음을 확인했습니다(Approved 11건, Rejected 5건, Hold 0건,
> 미검토 0건 — 가공/재해석 없이 Sheet 값 그대로 반영). QA Comment는 전 항목 공란입니다.

## Hard Rule 적용 / Validation 특이사항

- **TC-SIGNUP-DELETE-ACCOUNT-015**: `docs/tc/signup-delete-account.md`의 "결함 의심 항목"
  섹션에 포함된 TC로, 실제 회원가입 절차 없이 `/account_created` URL 직접 접근 시 정상 가입
  완료 페이지가 그대로 노출되는 현재 발생 중인 결함을 정상 Expected Result로 고정하고 있습니다.
  `automation-candidate` Skill 5절 Hard Rule에 따라 Automation Score와 무관하게 Candidate: No로
  처리했습니다.
- **TC-SIGNUP-DELETE-ACCOUNT-016**: 위와 동일하게 결함 의심 항목이며, 로그아웃(미인증) 상태에서
  `/delete_account` URL 직접 접근 시 실제 삭제 처리 없이 삭제 성공 페이지가 노출되는 현재 발생
  중인 결함(인가 체크 부재 성격)을 정상 Expected Result로 고정하고 있습니다. Skill 5절 Hard Rule에
  따라 Candidate: No로 처리했습니다. 두 항목 모두 결함이 수정되고 TC/PRD가 정상 요구사항 기준으로
  재승인되면 다시 일반 TC로 재평가할 수 있습니다.
- **자동화 대상 확정 시점 Validation 결과(2026-08-27, 사용자의 "QA 승인이 전부 되어있다면
  확정해주세요" 요청에 따른 재조회 및 확정 처리)**:
  1. TC ID 유효성/중복: Sheet의 TC-SIGNUP-DELETE-ACCOUNT-001~016(16건)이
     `docs/tc/signup-delete-account.md`에 실제로 존재하는 TC ID와 1:1로 정확히 일치하며, Sheet
     내 중복 없음을 확인.
  2. QA Decision 값 검증: 16건 전체가 정확히 `Approved`(11건) 또는 `Rejected`(5건)이며, `Hold`나
     미검토(빈 값), 그 외 잘못된 값(Validation Error)은 없음을 확인. Hard Rule 적용 대상인
     TC-015/016도 QA Decision이 `Rejected`로 입력되어 있어 AI 판정(Candidate: No)과 일치함.
  3. 원본 TC 문서 상태: `docs/tc/signup-delete-account.md`의 `상태`가 여전히 `승인완료`임을 확인.
  4. TC 변경 여부: 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-22)과 현재
     `docs/tc/signup-delete-account.md`의 `최근 변경일`(2026-08-22)이 동일해, 평가 이후 원본 TC
     문서가 변경되지 않았음을 확인.
  - 4개 항목 모두 통과하여 Approved 11건을 자동화 대상으로 확정함(Hold 0건, Rejected 5건).

## Approved TC 목록 (자동화 대상 확정)

2026-08-27 확정. QA Decision이 `Approved`인 아래 11건만 자동화 대상으로 확정합니다(Rejected
5건은 확정하지 않음, Hold는 이번 평가에서 0건). Hard Rule 적용 대상이었던 TC-015/016은
QA Decision도 `Rejected`로 일치해 확정 대상에서 제외됩니다.

| TC ID | Automation Score | Candidate (AI) | QA Decision |
|---|---|---|---|
| TC-SIGNUP-DELETE-ACCOUNT-001 | 26 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-002 | 21 | Hold | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-004 | 25 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-005 | 26 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-006 | 24 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-007 | 25 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-010 | 26 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-011 | 25 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-012 | 24 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-013 | 24 | Yes | Approved |
| TC-SIGNUP-DELETE-ACCOUNT-014 | 22 | Yes | Approved |

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-24 | 승인완료 상태의 `docs/tc/signup-delete-account.md`(TC-SIGNUP-DELETE-ACCOUNT-001~016) 최초 1차 자동화 후보 평가. Feature PRD(`docs/prd/feature/signup-delete-account.md`, 승인완료)를 맥락 참고. 사용자 요청에 따라 다른 확정 Feature(login-logout 등)와의 Cross-Feature 중복 여부를 별도 검토(중복 없음, TC-008/013은 유사 패턴이나 별도 Risk Coverage로 판단). TC-015/016은 Hard Rule 적용으로 Candidate: No. | 평가중 |
| 2026-08-27 | 사용자의 명시적 "자동화 대상 확정" 요청에 따라 Google Sheet 재조회(candidate-list) 수행. TC-SIGNUP-DELETE-ACCOUNT-001~016 전체 QA Decision이 입력 완료(Approved 11건, Rejected 5건, Hold 0건, 미검토 0건)됨을 확인. TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부 Validation을 모두 통과해 Approved 11건(001, 002, 004~007, 010~014)을 자동화 대상으로 확정(003, 008, 009, 015, 016은 Rejected로 제외). | 자동화대상확정 |
