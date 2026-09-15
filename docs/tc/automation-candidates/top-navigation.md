---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/top-navigation.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-08-22
관련 Feature PRD: feature/top-navigation.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-08-24
최근 변경일: 2026-08-27
최근 Sheet 동기화일: 2026-08-24
확정일: 2026-08-27
---

# Automation Candidate 평가 - 상단 네비게이션

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-TOP-NAVIGATION-001 | 2 | 3 | 5 | 5 | 2 | 1 | 22 | Hold | Home 메뉴 이동은 브라우저 뒤로가기/URL 직접 입력 등 대체 수단이 있고 로그인/로그아웃 직후 자동 랜딩되는 경우가 많아 실패 영향이 제한적(BC2). 단순 정적 링크로 안정성/판정/유지비용은 모두 우수해 Score는 22(후보 구간)이나 비즈니스 영향이 낮아 ROI 판단을 위해 사용자 검토 필요. |
| TC-TOP-NAVIGATION-002 | 4 | 4 | 5 | 5 | 2 | 1 | 25 | Yes | 전체 상품 목록으로 이동하는 핵심 진입 경로로 PRD상 대체 경로가 제한적이라 실패 시 상품 탐색 자체가 어려워짐(BC4). 안정적인 정적 링크로 결정적 판정과 낮은 유지비용을 가져 자동화 적극 권장. |
| TC-TOP-NAVIGATION-003 | 2 | 3 | 5 | 5 | 2 | 1 | 22 | Hold | Cart 메뉴 이동은 담기 확인 모달의 "View Cart" 링크(`cart.md` TC-CART-003, 별도 진입 경로)라는 대체 경로가 이미 검증되어 있어 완전히 차단되지 않음(BC2). 자동화 비용 자체는 매우 낮으나(Score 22) 비즈니스 영향이 낮아 사용자 검토 필요. |
| TC-TOP-NAVIGATION-004 | 4 | 4 | 4 | 5 | 3 | 2 | 24 | Yes | 로그인 상태에서 3개 페이지를 순회하며 메뉴 구성과 "Logged in as {유저명}" 표시의 일관성을 함께 검증하는 복합 시나리오(P1). 불일치 시 사용자가 로그인 상태 자체를 신뢰하기 어려워지는 서비스 신뢰성 문제로 이어짐(BC4). 결정적 판정이 가능해 자동화 적극 권장. |
| TC-TOP-NAVIGATION-005 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Hold | TC-004(로그인 상태)와 동일 요구사항(REQ-TOP-NAVIGATION-005)의 로그아웃 상태 버전으로 별도 Risk Coverage(상태값)를 가져 중복은 아니나, "Logged in as" 같은 신뢰성 표시 요소가 없어 TC-004 대비 실패 영향이 상대적으로 작음(BC3). Score 21(후보 구간 중하단)로 사용자 검토 필요. |
| TC-TOP-NAVIGATION-006 | 4 | 3 | 4 | 4 | 3 | 2 | 22 | Yes | 회원가입 시 입력한 Name 값과 로그인 세션의 "Logged in as" 표시값을 비교하는 개인화 데이터 신뢰성 검증으로, 값이 틀리면 개인정보 표시 신뢰성이 크게 훼손됨(BC4, page-ui.md TC-035의 개인정보 표시 검증과 동일한 근거). 테스트 계정의 Name 값을 비교 기준으로 준비해야 해 1회 수행 비용은 다소 있으나(MTC3) 문자열 비교로 결정적 판정이 가능해 자동화 권장. |
| TC-TOP-NAVIGATION-007 | 2 | 3 | 4 | 4 | 1 | 2 | 18 | No | 현재 페이지 메뉴 항목의 주황색 활성 표시는 시각적 하이라이트로 기능 사용 자체에는 지장이 없는 단순 스타일 확인(BC2, Skill 4.2 단순 UI 노출/스타일 확인 신호). Score는 18(후보 구간 하한)이나 비즈니스 영향이 낮아 자동화 제외 권장. |
| TC-TOP-NAVIGATION-008 | 1 | 2 | 4 | 3 | 1 | 3 | 14 | No | 마우스 오버 시 시각 효과로 사용자 영향이 매우 낮고(BC1), hover 상태 시뮬레이션 및 hover 중 스타일 확인은 자동화 도구/브라우저 환경에 따라 판정이 다소 까다롭고(RD3) 유지비용도 있음(MC3, Skill 4.2 육안 판단/hover 의존 신호). Score 14(Hold 구간)이나 비즈니스 영향이 극히 낮아 자동화 제외 권장. |
| TC-TOP-NAVIGATION-009 | 2 | 2 | 4 | 4 | 1 | 2 | 17 | Hold | hover 없이도 활성 표시가 유지되는지 확인하는 상태 지속성 검증으로 TC-008보다는 결정적 판정이 쉬우나(hover 시뮬레이션 불필요) 여전히 시각적 스타일 확인 수준으로 비즈니스 영향이 낮음(BC2). Score 17(Hold 구간)로 사용자 검토 필요. |
| TC-TOP-NAVIGATION-010 | 2 | 2 | 4 | 4 | 1 | 2 | 17 | Hold | Logout/Delete Account의 빨간색 계열 표시는 다른 메뉴와의 시각적 구분을 위한 스타일 확인으로 기능 자체에는 영향이 없음(BC2). Score 17(Hold 구간)로 사용자 검토 필요. |
| TC-TOP-NAVIGATION-011 | 1 | 2 | 5 | 5 | 1 | 1 | 19 | No | "Logged in as" 텍스트 클릭 시 아무 동작도 없어야 하는 Negative Case로 안정적이고 결정적 판정이 가능하나(AS5, RD5), 실패(의도치 않은 동작 발생)하더라도 영향이 매우 낮은 요소임(BC1). Score는 19(후보 구간)이나 비즈니스 영향이 극히 낮아 자동화 제외 권장. |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-TOP-NAVIGATION-001 | Approved | |
| TC-TOP-NAVIGATION-002 | Approved | |
| TC-TOP-NAVIGATION-003 | Approved | |
| TC-TOP-NAVIGATION-004 | Approved | |
| TC-TOP-NAVIGATION-005 | Approved | |
| TC-TOP-NAVIGATION-006 | Approved | |
| TC-TOP-NAVIGATION-007 | Rejected | |
| TC-TOP-NAVIGATION-008 | Rejected | |
| TC-TOP-NAVIGATION-009 | Rejected | |
| TC-TOP-NAVIGATION-010 | Rejected | |
| TC-TOP-NAVIGATION-011 | Rejected | |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다. 2026-08-27 재조회(candidate-list) 결과 TC-TOP-NAVIGATION-001~011 전체
> QA Decision이 입력 완료되었음을 확인했습니다(Approved 6건, Rejected 5건, Hold 0건, 미검토
> 0건 — 가공/재해석 없이 Sheet 값 그대로 반영). QA Comment는 전 항목 공란입니다.

## Hard Rule 적용 / Validation 특이사항

- `docs/tc/top-navigation.md`의 "결함 의심 항목" 섹션에는 본 문서 범위에서 새로 발급된
  Requirement가 없으며(로그아웃 상태 `/delete_account` 직접 접근 관련 결함 의심은
  `signup-delete-account.md` 범위로 위임됨), 이번 평가 대상 TC-TOP-NAVIGATION-001~011 중
  Skill 5절 Hard Rule(현재 발생 중인 결함을 정상 Expected Result처럼 고정한 TC)에 해당하는
  항목은 없었습니다.
- **Cross-Feature TC 중복 확인 (요청에 따른 확인 결과)**: `docs/tc/page-ui.md`,
  `docs/tc/login-logout.md`를 대조 확인한 결과, 검증 목적이 실질적으로 동일한 신규 중복 TC는
  발견되지 않았습니다.
  - `docs/tc/top-navigation.md`는 문서 최상단 Precondition 설명 및 REQ-TOP-NAVIGATION-004 관련
    각주에서 이미 다음 두 가지 잠재적 중복을 **TC 설계 단계에서** 인지하고 처리해 두었습니다.
    - REQ-TOP-NAVIGATION-004(로그아웃 상태 Signup/Login 클릭 시 `/login` 이동)는
      `login-logout.md` TC-LOGIN-LOGOUT-002와 검증 목적(대상 메뉴, 클릭 동작, 기대 URL)이
      완전히 동일해 본 문서에 별도 TC를 생성하지 않음(사용자 확인 완료).
    - 로그인 성공/로그아웃 처리 시점의 메뉴 구성 "전환" 자체(로그인 직후 로그아웃→로그인 메뉴
      전환, 로그아웃 직후 역전환)는 `login-logout.md` TC-LOGIN-LOGOUT-004, 014, 015에서 이미
      검증되며, 본 문서 TC-TOP-NAVIGATION-004/005는 그 결과인 "이미 확립된 상태"에서의 메뉴
      동작(3개 페이지 순회 시 일관성)만 다루도록 범위가 분리되어 있어 중복이 아닙니다(별도 Risk
      Coverage: 페이지 이동 간 일관성 vs 상태 전환 그 자체).
  - `page-ui.md`의 검색창/CATEGORY 아코디언/브레드크럼 관련 TC(TC-PAGE-UI-013, 023~026,
    032~033 등)는 상단 네비게이션의 Home/Products/Cart/Logout 메뉴 자체의 이동 URL, 활성 표시,
    "Logged in as" 요소를 다루는 본 문서 TC와 검증 대상 UI 요소가 서로 달라 중복으로 보지
    않았습니다.
  - 결론: 이번 평가에서 새로 발견된 Cross-Feature 중복은 없으며, 기존에 알려진 중복은 이미 TC
    설계 단계에서 적절히 처리되어 있어 평가 대상에서 자연스럽게 제외되어 있었습니다.
- 단순 시각적 스타일/노출 확인이며 Business Criticality가 매우 낮은 TC(TC-TOP-NAVIGATION-007,
  008, 011)는 Automation Score가 후보 구간(14~19)으로 산정되었으나, Skill 1절에 따라 점수만으로
  기계적으로 결정하지 않고 TC 목적/ROI를 함께 고려해 Candidate: No로 판정했습니다(점수 구간과
  최종 판단이 다른 사유를 각 행에 명시).
- TC-TOP-NAVIGATION-003(Cart 메뉴 이동)은 `cart.md` TC-CART-003(담기 확인 모달의 "View Cart"
  링크)이라는 별도 진입 경로가 이미 검증되어 있어 완전한 실패로 이어지지 않는다는 점이 Business
  Criticality 점수에 반영되었을 뿐, 두 TC가 검증 목적·Test Steps 자체가 동일한 중복은 아닙니다
  (서로 다른 UI 요소 — 상단 네비게이션 메뉴 vs 모달 내 링크).

- **자동화 대상 확정 시점 Validation 결과(2026-08-27, 사용자의 "QA 승인이 전부 되어있다면
  확정해주세요" 요청에 따른 재조회 및 확정 처리)**:
  1. TC ID 유효성/중복: Sheet의 TC-TOP-NAVIGATION-001~011(11건)이 `docs/tc/top-navigation.md`에
     실제로 존재하는 TC ID와 1:1로 정확히 일치하며, Sheet 내 중복 없음을 확인.
  2. QA Decision 값 검증: 11건 전체가 정확히 `Approved`(6건) 또는 `Rejected`(5건)이며, `Hold`나
     미검토(빈 값), 그 외 잘못된 값(Validation Error)은 없음을 확인.
  3. 원본 TC 문서 상태: `docs/tc/top-navigation.md`의 `상태`가 여전히 `승인완료`임을 확인.
  4. TC 변경 여부: 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-22)과 현재
     `docs/tc/top-navigation.md`의 `최근 변경일`(2026-08-22)이 동일해, 평가 이후 원본 TC 문서가
     변경되지 않았음을 확인.
  - 4개 항목 모두 통과하여 Approved 6건을 자동화 대상으로 확정함(Hold 0건, Rejected 5건).

## Approved TC 목록 (자동화 대상 확정)

2026-08-27 확정. QA Decision이 `Approved`인 아래 6건만 자동화 대상으로 확정합니다(Rejected
5건은 확정하지 않음, Hold는 이번 평가에서 0건).

| TC ID | Automation Score | Candidate (AI) | QA Decision |
|---|---|---|---|
| TC-TOP-NAVIGATION-001 | 22 | Hold | Approved |
| TC-TOP-NAVIGATION-002 | 25 | Yes | Approved |
| TC-TOP-NAVIGATION-003 | 22 | Hold | Approved |
| TC-TOP-NAVIGATION-004 | 24 | Yes | Approved |
| TC-TOP-NAVIGATION-005 | 21 | Hold | Approved |
| TC-TOP-NAVIGATION-006 | 22 | Yes | Approved |

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-24 | 승인완료된 TC 문서(`docs/tc/top-navigation.md`, TC-TOP-NAVIGATION-001~011)를 대상으로 automation-candidate Skill 6개 축 1차 평가 수행. Feature PRD(`docs/prd/feature/top-navigation.md`, 승인완료)를 맥락 참고. Hard Rule 해당 항목 없음. Yes 3건(002, 004, 006) / Hold 5건(001, 003, 005, 009, 010) / No 3건(007, 008, 011). 사용자 요청에 따라 `page-ui.md`, `login-logout.md`와의 Cross-Feature 중복 여부를 확인했으며 신규 중복 없음(기존에 알려진 두 건은 TC 설계 단계에서 이미 처리됨)을 확인해 별도 기록. | 평가중 |
| 2026-08-24 | Google Sheet(Automation Candidates 워크시트)에 AI 작성 영역(11건 신규 추가) 동기화 완료(dry-run 확인 후 실제 반영). 이후 QA Decision/QA Comment 재조회(candidate-list) 수행 결과 TC-TOP-NAVIGATION-001~011 전체 QA Decision이 아직 비어있음(미검토) 확인. Skill Workflow 8번에 따라 최초 재조회 수행으로 상태 전환 | 사용자검토완료 |
| 2026-08-27 | 사용자의 명시적 "자동화 대상 확정" 요청에 따라 Google Sheet 재조회(candidate-list) 수행. TC-TOP-NAVIGATION-001~011 전체 QA Decision이 입력 완료(Approved 6건, Rejected 5건, Hold 0건, 미검토 0건)됨을 확인. TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부 Validation을 모두 통과해 Approved 6건(001~006)을 자동화 대상으로 확정. | 자동화대상확정 |
