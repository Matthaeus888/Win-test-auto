---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정
대상 TC 문서: docs/tc/cart.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-08-22
관련 Feature PRD: feature/cart.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-08-24
최근 변경일: 2026-08-24
최근 Sheet 동기화일: 2026-08-24
확정일: 2026-08-24
---

# Automation Candidate 평가 - 장바구니 (상품 담기 포함)

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-CART-001 | 4 | 5 | 4 | 5 | 1 | 1 | 24 | Yes | 담기 확인 모달은 상품이 실제로 담겼음을 알리는 유일한 피드백이자 다른 Feature에서도 재사용되는 공유 컴포넌트의 최초 검증 지점(실패해도 담기 자체는 되므로 BC는 5가 아닌 4). 매 Release 반복 검증되는 핵심 경로이며 아이콘/문구/버튼 구성을 DOM으로 결정적으로 판정 가능하고 자동화/유지 비용이 매우 낮아 자동화 적극 권장. |
| TC-CART-002 | 2 | 3 | 5 | 5 | 1 | 1 | 21 | Hold | "Continue Shopping" 클릭 시 모달만 닫히는 단순 UX 동작으로 실패해도 페이지 이동/새로고침으로 복구 가능해 Business Criticality가 낮음(Skill 4.2 후순위 신호에 근접). 기술적으로는 자동화 비용이 매우 낮아 Score는 21(후보 구간)이나 비즈니스 영향이 낮아 ROI가 애매함 — 사용자 검토 필요. |
| TC-CART-003 | 2 | 3 | 5 | 5 | 1 | 1 | 21 | Hold | "View Cart" 링크 이동 확인으로, 실패해도 상단 네비게이션의 Cart 메뉴라는 대체 경로가 있어 Business Criticality가 낮음. TC-CART-002와 동일한 성격(단순 UI 이동 확인)으로 Score는 21이나 ROI 판단을 위해 사용자 검토 필요. |
| TC-CART-004 | 4 | 5 | 4 | 5 | 3 | 2 | 25 | Yes | Home/Products 등 서로 다른 진입 경로에서 담은 상품이 하나의 장바구니로 병합되지 않으면 결제 시 상품 누락(데이터 손실)으로 이어질 수 있는 핵심 데이터 정합성 시나리오. 매 Release 반복 검증되며 장바구니 목록으로 결정적 판정 가능해 자동화 권장. |
| TC-CART-005 | 5 | 5 | 4 | 5 | 4 | 3 | 26 | Yes | Quantity/Total 누적 계산은 최종 결제 금액에 직결되는 핵심 데이터 정합성 로직으로 실패 시 잘못된 금액으로 주문이 진행될 수 있음(BC 5). 7회 반복 클릭이라는 1회 수행 비용은 높지만(MC 4), 매 Release 반복 검증할 가치가 큰 핵심 회귀이며 값 검증이 결정적이라 자동화 적극 권장. |
| TC-CART-006 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 상세 페이지에서 지정한 수량이 장바구니에 잘못 반영되면 주문 금액 오류로 이어질 수 있는 시나리오. 리스트 페이지 고정값(TC-CART-005)과 별도 Risk Coverage(수량 지정 경로)를 검증하므로 중복이 아니며, 결정적 판정과 낮은 유지비용으로 자동화 권장. |
| TC-CART-007 | 2 | 2 | 5 | 5 | 1 | 1 | 20 | Hold | Quantity 칸 편집 불가 확인으로, 실패(편집 가능해짐)해도 사용자가 수량을 직접 조정할 수 있게 되는 정도로 영향이 제한적이며(PRD상 정상 동작을 재확인하는 Negative Case) 반복 검증 가치도 낮음. Score는 20(후보 구간)이나 정적 표시 요소 확인에 가까워(Skill 4.2) ROI 판단을 위해 사용자 검토 필요. |
| TC-CART-008 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 삭제가 실패하거나 엉뚱한 상품이 삭제되면 사용자가 원치 않는 상품을 그대로 결제하게 될 수 있는 핵심 회귀. 다건 중 특정 행 식별 로직이라 결함 발생 가능성도 있고, 목록 비교로 결정적 판정이 가능해 자동화 권장. |
| TC-CART-009 | 3 | 3 | 5 | 5 | 2 | 1 | 23 | Yes | 전체 삭제 시 빈 카트 상태로의 전환이라는 실제 조건부 렌더링 로직을 검증(안내 문구 자체는 page-ui.md에서 이미 검증되어 본 TC는 트리거 조건만 추가 확인). Business Criticality/Regression Frequency는 중간 수준이나 자동화/유지 비용이 낮고 결정적으로 판정 가능해 자동화 권장. |
| TC-CART-010 | 4 | 5 | 4 | 5 | 2 | 2 | 24 | Yes | 로그아웃 사용자의 체크아웃 진입을 막는 접근 제어 로직으로, 실패 시 비로그인 사용자가 결제 절차로 잘못 진입할 수 있어 영향이 큼. 로그인 상태 분기와 모달 렌더링이 결합되어 결함 발생 가능성이 있고 결정적 판정이 가능해 자동화 권장. |
| TC-CART-011 | 5 | 5 | 4 | 5 | 2 | 2 | 25 | Yes | 로그인 사용자가 결제 절차로 진입하는 유일한 경로이므로 실패 시 핵심 기능(결제 진입) 사용이 불가능해짐(BC 5). 매 Release 반복 검증되는 핵심 Flow이며 URL로 결정적 판정 가능해 자동화 적극 권장. |
| TC-CART-012 | 2 | 2 | 5 | 5 | 2 | 2 | 20 | Hold | `/checkout` Address Details 정보 편집 불가 확인으로, 실패(편집 가능해짐)해도 단순 정보 노출 영역의 표시 오류 수준이라 영향이 제한적임(PRD상 정상 동작 재확인 Negative Case). TC-CART-007과 유사한 정적 표시 요소 확인 성격으로 Score 20이나 ROI 판단을 위해 사용자 검토 필요. |
| TC-CART-013 | 2 | 2 | 5 | 5 | 2 | 2 | 20 | Hold | `/checkout` Review Your Order Quantity 편집 불가 확인으로, TC-CART-007(Cart 페이지 Quantity 편집 불가)과 동일한 요구사항(REQ-CART-005)을 다른 페이지(checkout)에서 재확인하는 성격이라 별도 Risk Coverage는 있으나(다른 컴포넌트) Business Criticality가 낮음. Score 20이나 ROI 판단을 위해 사용자 검토 필요. |
| TC-CART-014 | 4 | 3 | 4 | 5 | 3 | 2 | 23 | Yes | 계정에 실제로 담긴 상품이 있어도 로그아웃 상태에서는 항상 빈 카트로 보여야 하는 조건부 로직. 실패 시(로그아웃 상태에서 타 계정 데이터가 노출되는 형태로 나타나면) 데이터 노출 우려가 있어 Business Criticality를 4로 평가. 결정적 판정이 가능하고 자동화/유지 비용이 중간 수준이라 자동화 권장. |
| TC-CART-015 | 5 | 5 | 4 | 5 | 3 | 3 | 25 | Yes | 로그아웃 상태에서 담은 상품이 로그인 시 반영되지 않으면 사용자가 담았던 상품을 그대로 잃게 되는 심각한 데이터 손실(BC 5). 비로그인→로그인 데이터 병합이라는 다단계 시나리오로 유지비용은 중간이나(계정 상태 의존) 매 Release 검증 가치가 커 자동화 권장. |
| TC-CART-016 | 5 | 5 | 4 | 5 | 3 | 3 | 25 | Yes | 로그인 중 담아둔 상품이 재로그인 시 복원되지 않으면 마찬가지로 심각한 데이터 손실로 이어짐(BC 5). TC-CART-015와 반대 방향(로그인 상태 유지 후 재로그인)의 별도 Risk Coverage를 검증하므로 중복이 아니며 자동화 권장. |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-CART-001 | Approved | |
| TC-CART-002 | Approved | |
| TC-CART-003 | Approved | |
| TC-CART-004 | Approved | |
| TC-CART-005 | Approved | |
| TC-CART-006 | Approved | |
| TC-CART-007 | Rejected | |
| TC-CART-008 | Approved | |
| TC-CART-009 | Approved | |
| TC-CART-010 | Approved | |
| TC-CART-011 | Approved | |
| TC-CART-012 | Rejected | |
| TC-CART-013 | Rejected | |
| TC-CART-014 | Approved | |
| TC-CART-015 | Approved | |
| TC-CART-016 | Approved | |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다. 2026-08-24 재조회 결과를 반영했습니다(가공/재해석 없이 Sheet 값 그대로 옮김).

## Hard Rule 적용 / Validation 특이사항

- `cart.md`의 "결함 의심 항목" 섹션에 결함 의심으로 표시된 REQ가 없어(문서 51~56행 참조), 이번
  평가 대상 TC-CART-001~016 중 Skill 5절 Hard Rule(현재 발생 중인 결함을 정상 Expected
  Result처럼 고정한 TC)에 해당하는 항목은 없었습니다.
- TC-CART-007/012/013(Quantity, Address Details 등 편집 불가 확인)과 TC-CART-002/003
  (모달 버튼/링크 단순 이동)은 Automation Score는 후보 구간(20~21)이나 Business
  Criticality/Regression Frequency가 낮아 Candidate: Hold로 판정했습니다 — 자동화 자체가
  불가능해서가 아니라 ROI 판단을 위해 사용자 검토가 필요하다는 의미입니다.
- 2026-08-24 Sheet 재조회 및 확정 전 Validation 결과:
  - TC ID 유효성/중복: Sheet의 16개 TC ID 모두 `docs/tc/cart.md`에 실존, 중복 없음.
  - QA Decision 값 검증: 16건 모두 정확히 `Approved` 또는 `Rejected`(공백/오탈자/대소문자
    변형 없음). 미검토(빈 값) 0건, Hold 0건.
  - 원본 TC 문서 상태: `docs/tc/cart.md`는 여전히 `상태: 승인완료`.
  - TC 변경 여부: 평가 시점 기준 변경일(2026-08-22)과 현재 원본 TC 변경일(2026-08-22) 일치,
    평가 이후 변경 없음.
  - 결론: 4가지 Validation 모두 통과.
- AI 1차 판정과 사용자 QA Decision이 다른 항목(참고용, 사용자 Decision이 우선 적용됨):
  - TC-CART-002, TC-CART-003: AI Hold → 사용자 Approved
  - TC-CART-007, TC-CART-012, TC-CART-013: AI Hold → 사용자 Rejected

## Approved TC 목록 (자동화 대상 확정)

사용자가 채팅에서 직접 "네, 확정해줘"라고 명시적으로 확정 요청함에 따라(2026-08-24),
아래 13건을 최종 자동화 대상으로 확정합니다.

- TC-CART-001
- TC-CART-002
- TC-CART-003
- TC-CART-004
- TC-CART-005
- TC-CART-006
- TC-CART-008
- TC-CART-009
- TC-CART-010
- TC-CART-011
- TC-CART-014
- TC-CART-015
- TC-CART-016

자동화 제외(Rejected) 3건: TC-CART-007, TC-CART-012, TC-CART-013

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-24 | 승인완료된 TC 문서(`docs/tc/cart.md`, TC-CART-001~016)를 대상으로 automation-candidate Skill 6개 축 1차 평가 수행. Hard Rule 해당 항목 없음. Yes 11건 / Hold 5건. | 평가중 |
| 2026-08-24 | Google Sheet(Automation Candidates 워크시트)에 AI 작성 영역(16건 신규 추가) 동기화 완료. 이후 QA Decision/QA Comment 재조회(candidate-list) 수행 결과 TC-CART-001~016 전체 QA Decision이 아직 비어있음(미검토) 확인. Skill Workflow 8번에 따라 최초 재조회 수행으로 상태 전환 | 사용자검토완료 |
| 2026-08-24 | Google Sheet 재조회 결과 QA Decision 16건 전부 입력 완료(Approved 13 / Rejected 3 / Hold 0, 미검토 0) 확인. 확정 전 Validation(TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부) 4개 항목 모두 통과. 사용자가 채팅에서 직접 "네, 확정해줘"라고 명시적으로 확정 요청. Approved 13건을 최종 자동화 대상으로 확정하고 Rejected 3건은 자동화 제외로 확정. | 자동화대상확정 |
