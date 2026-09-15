---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/product-detail.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-08-22
관련 Feature PRD: feature/product-detail.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-08-24
최근 변경일: 2026-08-27
최근 Sheet 동기화일: 2026-08-24
확정일: 2026-08-27
---

# Automation Candidate 평가 - 상품 상세

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-PRODUCT-DETAIL-001 | 4 | 4 | 4 | 5 | 1 | 1 | 23 | Yes | Home 카드의 "View Product" 링크가 실제로 `/product_details/{id}` 패턴으로 이동하는지 확인하는 TC로, 이후 다른 모든 상세 페이지 TC의 진입 경로가 되는 기초 계약(URL 구조)을 검증함(BC4). `page-ui.md` TC-PAGE-UI-006/015는 카드 안에 "View Product" 링크가 "노출"되는지만 확인하고 실제 클릭 후 이동 목적지(URL 패턴)는 검증하지 않아 별도 Risk Coverage로 중복이 아님. URL 문자열로 결정적 판정 가능하고 자동화 비용도 매우 낮아 자동화 권장. |
| TC-PRODUCT-DETAIL-002 | 5 | 5 | 4 | 4 | 2 | 1 | 25 | Yes | 존재하는 상품 ID로 상세 페이지가 정상 노출되는지 확인하는 것으로, 실패 시 상품 상세 Feature 전체 및 구매 퍼널 진입이 불가능해지는 핵심 스모크 테스트(BC5). 매 Release 예외 없이 반복 검증될 성격이며 여러 구성요소를 동시에 확인해 판정 로직이 다소 있으나(RD4) 자동화 실익이 커 적극 권장. |
| TC-PRODUCT-DETAIL-003 | 1 | 2 | 4 | 4 | 1 | 1 | 17 | No | 단일 이미지·썸네일 전환 UI 부재를 확인하는 정적 요소 확인으로 실패해도 사용자 영향이 매우 낮음(Skill 4.2 단순 UI 노출 확인 신호). 자동화 실익이 낮아 제외 권장. |
| TC-PRODUCT-DETAIL-004 | 1 | 1 | 5 | 5 | 1 | 1 | 18 | No | "NEW" 배지 노출 확인은 순수 장식 요소로 영향이 매우 낮음(BC1, RF1). Score는 18(후보 하한)이나 Skill 1절에 따라 점수만으로 결정하지 않고 TC 목적을 고려해 자동화 제외 권장. |
| TC-PRODUCT-DETAIL-005 | 2 | 2 | 5 | 5 | 1 | 1 | 21 | Hold | 상품명 텍스트 노출 확인으로 사용자 식별에 필요하나 정적 텍스트 렌더링 수준이라 BC가 낮음. Score는 21(후보 구간)이나 ROI 판단을 위해 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-006 | 2 | 1 | 5 | 5 | 1 | 1 | 19 | Hold | "Category: {대분류} > {소분류}" 텍스트 노출 확인으로 정적 요소이며 재검증 빈도도 낮아(RF1) BC/RF가 낮음. 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-007 | 1 | 1 | 5 | 4 | 1 | 1 | 17 | No | 별점 아이콘 노출 확인(클릭 동작은 TC-018에서 별도 검증)은 정적 표시 요소로 영향이 매우 낮아 자동화 제외 권장. |
| TC-PRODUCT-DETAIL-008 | 3 | 2 | 4 | 5 | 1 | 1 | 20 | Hold | 가격이 "Rs. {숫자}" 형식으로 노출되는지 확인하는 것으로, 구매 결정에 영향을 미치는 정보라 BC를 3으로 평가했으나 값의 정확성이 아닌 표기 형식만 다루는 정적 렌더링 검증이라 Score 20(후보 구간)에서 사용자 검토가 필요. |
| TC-PRODUCT-DETAIL-009 | 2 | 2 | 4 | 4 | 2 | 2 | 18 | Hold | Quantity 입력란이 네이티브 number input + 스피너 형태로 Add to cart 옆에 위치하는지 확인하는 구조 검증으로, 실제 담기 동작은 TC-015/016/017에서 별도 검증됨. 구조 자체의 실패 영향은 제한적(BC2)이라 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-010 | 2 | 2 | 5 | 5 | 1 | 1 | 20 | Hold | "Add to cart" 버튼이 Quantity 옆에 노출되는지(레이아웃 위치) 확인. 버튼 클릭 시 실제 동작은 TC-015에서 이미 검증되므로 본 TC는 배치 확인에 국한되어 BC가 낮음. 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-011 | 2 | 1 | 5 | 5 | 1 | 1 | 19 | Hold | Availability/Condition/Brand 텍스트 및 Brand 링크 형태 노출 확인으로 정적 요소이며 재검증 빈도가 낮음. 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-012 | 1 | 1 | 5 | 5 | 1 | 1 | 18 | No | 사이즈/색상 선택 UI 부재를 확인하는 단순 Negative Case로 영향이 매우 낮아 자동화 제외 권장. |
| TC-PRODUCT-DETAIL-013 | 2 | 2 | 4 | 4 | 2 | 2 | 18 | Hold | WRITE YOUR REVIEW 섹션의 3개 입력란+Submit 버튼 노출을 동시에 확인하는 복합 요소 검증이나, 노출 여부 확인 수준이라 BC가 낮음. 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-014 | 2 | 2 | 4 | 3 | 3 | 3 | 17 | Hold | 페이지 전체가 탭 전환 없이 단일 스크롤 레이아웃으로 이어지는지 순서를 확인하는 TC로, 여러 섹션의 DOM 순서를 비교해야 해 판정 로직이 다소 복잡하고(RD3) 셀렉터 다수 의존으로 유지비용도 있음(MC3). BC도 낮아 ROI 판단을 위해 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-015 | 4 | 4 | 4 | 5 | 2 | 2 | 23 | Yes | 정상 수량 지정 후 "Add to cart" 클릭 시 확인 모달이 노출되는지 확인하는 이 Feature의 유일한 P0 TC. `cart.md` TC-CART-001과 모달 구성 자체는 동일하지만, 본 TC는 (1) 상세 페이지 고유의 커스텀 Quantity 입력값 캡처, (2) 해당 값의 장바구니 반영, (3) 공유 모달 컴포넌트 렌더링까지 이 페이지 문맥에서 새롭게 결합되는 별도 Risk Coverage를 가지므로 중복이 아님(TC 자체의 Priority 산정 근거에도 동일하게 명시됨). 결정적 판정이 가능하고 자동화/유지 비용도 낮아 자동화 권장. |
| TC-PRODUCT-DETAIL-016 | 2 | 2 | 4 | 5 | 1 | 1 | 19 | Hold | Quantity 스피너 최솟값(1) 제한 확인. Boundary 로직이나 실패해도 영향이 제한적(BC2)이라 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-017 | 2 | 2 | 4 | 5 | 2 | 1 | 20 | Hold | Quantity 스피너 최댓값 미제한 확인. TC-016과 동일 근거(Boundary 확인, BC 낮음)이며 20회 반복 클릭으로 1회 수행 비용이 약간 있음. 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-018 | 1 | 1 | 5 | 5 | 1 | 1 | 18 | No | 별점 아이콘이 클릭 불가능한 정적 요소임을 확인하는 것으로 영향이 매우 낮아 자동화 제외 권장. |
| TC-PRODUCT-DETAIL-019 | 2 | 2 | 5 | 4 | 1 | 2 | 18 | No | WRITE YOUR REVIEW 3개 필드를 모두 비운 채 Submit 시 브라우저 자체(HTML5 native) 필수 입력 검증 팝업이 노출되는지 확인하는 TC로, `login-logout.md` TC-LOGIN-LOGOUT-007~009(동일 성격의 브라우저 네이티브 검증, Candidate: No 확정)와 동일한 근거를 적용함. 애플리케이션 로직이 아닌 브라우저 기본 동작이라 회귀 가능성이 낮고, 기술적으로는 판정 가능하나(RD4) 반복 자동 회귀 검증 실익(Regression ROI)이 낮아 자동화 후순위. |
| TC-PRODUCT-DETAIL-020 | 2 | 2 | 5 | 4 | 1 | 1 | 19 | No | Email 형식 오류 입력 시 브라우저 자체 이메일 형식 검증이 동작하는지 확인. TC-019와 동일 근거(`login-logout.md` 네이티브 검증 패턴, Regression ROI 낮음)로 자동화 후순위. |
| TC-PRODUCT-DETAIL-021 | 3 | 3 | 4 | 4 | 3 | 3 | 20 | Hold | 3개 필수값을 모두 올바르게 입력하고 Submit 시 성공 메시지가 노출되고 1~2초 후 필드가 자동 초기화되는지 확인. 브라우저 네이티브 검증(TC-019/020)과 달리 실제 애플리케이션 로직(피드백 메시지 + 타이머 기반 초기화)이라 회귀 검증 가치가 있으나(BC3), 타이밍 대기가 필요해 판정 로직이 다소 복잡하고(RD4) 대기 조건 특성상 유지보수 시 Flaky해질 위험이 있어(MC3) Score 20에서 사용자 검토 필요. |
| TC-PRODUCT-DETAIL-022 | 1 | 1 | 5 | 5 | 1 | 1 | 18 | No | "Related Products" 섹션이 존재하지 않음을 확인하는 단순 Negative Case로 영향이 매우 낮아 자동화 제외 권장. |
| TC-PRODUCT-DETAIL-023 | 3 | 3 | 2 | 4 | 2 | 3 | 17(참고) | No | **[Hard Rule 적용]** 존재하지 않는 상품 ID 접근 시 이미지/Category/Brand만 빈 값으로 노출되고 나머지 레이아웃은 정상 노출되는 현재 발생 중인 비정상 동작(결함 의심)을 정상 Expected Result처럼 고정한 TC. Skill 5절 Hard Rule에 따라 점수(참고 17)와 무관하게 Candidate: No로 처리. 결함이 수정되고 TC/PRD가 정상 요구사항으로 재승인되면 재평가 가능. |
| TC-PRODUCT-DETAIL-024 | 3 | 3 | 2 | 3 | 1 | 2 | 16(참고) | No | **[Hard Rule 적용]** Quantity에 문자만 입력 후 Add to cart 클릭 시 아무 안내 없이 조용히 실패하는 현재 발생 중인 결함을 정상 Expected Result처럼 고정한 TC. Hard Rule에 따라 점수(참고 16)와 무관하게 Candidate: No. 결함 수정 및 재승인 시 재평가 가능. |
| TC-PRODUCT-DETAIL-025 | 3 | 3 | 2 | 3 | 1 | 2 | 16(참고) | No | **[Hard Rule 적용]** TC-024와 동일 근거(숫자+문자 혼합 입력 조건에 대한 조용한 실패). 점수(참고 16)와 무관하게 Candidate: No. 결함 수정 및 재승인 시 재평가 가능. |
| TC-PRODUCT-DETAIL-026 | 4 | 2 | 2 | 4 | 3 | 3 | 18(참고) | No | **[Hard Rule 적용]** 음수 Quantity 입력 시 기존 장바구니 수량에서 절댓값만큼 차감되는 현재 발생 중인 데이터 무결성 결함을 정상 Expected Result처럼 고정한 TC. 점수(참고 18)와 무관하게 Candidate: No. 결함 수정 및 재승인 시 재평가 가능. |
| TC-PRODUCT-DETAIL-027 | 4 | 2 | 2 | 4 | 2 | 2 | 18(참고) | No | **[Hard Rule 적용]** Quantity 0 입력 시 수량 0으로 그대로 장바구니에 담기는 현재 발생 중인 결함을 정상 Expected Result처럼 고정한 TC. 점수(참고 18)와 무관하게 Candidate: No. 결함 수정 및 재승인 시 재평가 가능. |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-PRODUCT-DETAIL-001 | Approved | |
| TC-PRODUCT-DETAIL-002 | Approved | |
| TC-PRODUCT-DETAIL-003 | Rejected | |
| TC-PRODUCT-DETAIL-004 | Rejected | |
| TC-PRODUCT-DETAIL-005 | Rejected | |
| TC-PRODUCT-DETAIL-006 | Rejected | |
| TC-PRODUCT-DETAIL-007 | Rejected | |
| TC-PRODUCT-DETAIL-008 | Approved | |
| TC-PRODUCT-DETAIL-009 | Rejected | |
| TC-PRODUCT-DETAIL-010 | Rejected | |
| TC-PRODUCT-DETAIL-011 | Rejected | |
| TC-PRODUCT-DETAIL-012 | Rejected | |
| TC-PRODUCT-DETAIL-013 | Rejected | |
| TC-PRODUCT-DETAIL-014 | Rejected | |
| TC-PRODUCT-DETAIL-015 | Approved | |
| TC-PRODUCT-DETAIL-016 | Approved | |
| TC-PRODUCT-DETAIL-017 | Rejected | |
| TC-PRODUCT-DETAIL-018 | Rejected | |
| TC-PRODUCT-DETAIL-019 | Rejected | |
| TC-PRODUCT-DETAIL-020 | Rejected | |
| TC-PRODUCT-DETAIL-021 | Approved | |
| TC-PRODUCT-DETAIL-022 | Rejected | |
| TC-PRODUCT-DETAIL-023 | Rejected | |
| TC-PRODUCT-DETAIL-024 | Rejected | |
| TC-PRODUCT-DETAIL-025 | Rejected | |
| TC-PRODUCT-DETAIL-026 | Rejected | |
| TC-PRODUCT-DETAIL-027 | Rejected | |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다. 2026-08-27 재조회(candidate-list) 결과 TC-PRODUCT-DETAIL-001~027 전체
> QA Decision이 입력 완료되었음을 확인했습니다(Approved 6건, Rejected 21건, Hold 0건,
> 미검토 0건 — 가공/재해석 없이 Sheet 값 그대로 반영). QA Comment는 전 항목 공란입니다.

## Hard Rule 적용 / Validation 특이사항

- **Hard Rule 적용 대상(5건)**: `product-detail.md`의 "결함 의심 항목" 섹션에 포함된
  TC-PRODUCT-DETAIL-023~027은 모두 현재 발생 중인 결함(비정상 동작)을 정상 Expected Result처럼
  고정한 TC입니다. `automation-candidate` Skill 5절 Hard Rule에 따라 Automation Score와 무관하게
  전건 Candidate: No로 처리했습니다. 관련 결함이 수정되고 해당 TC/PRD가 정상 요구사항으로
  재승인되면 그때 다시 일반 TC와 동일한 절차로 재평가할 수 있습니다.
- **Cross-Feature TC 중복 여부 확인 결과 (login-logout / cart / page-ui 대상, Skill 4.3 참고)**:
  이번 평가에서는 page-ui.md ↔ cart.md 사례(TC-PAGE-UI-040/041 vs TC-CART-012/013)와 같은
  **완전한 중복(Test Steps까지 사실상 동일)** 은 발견되지 않았습니다. 다만 검증 대상이 겹치는
  것처럼 보일 수 있는 항목을 검토해 각각 별도 Risk Coverage가 있음을 확인했습니다.
  - **TC-PRODUCT-DETAIL-001 vs `page-ui.md` TC-PAGE-UI-006/015**: page-ui의 두 TC는 Home/
    Products 상품 카드 안에 "View Product" 링크가 "노출"되는지만 확인하고, 실제로 그 링크를
    클릭했을 때 이동하는 URL이 `/product_details/{id}` 패턴을 따르는지는 검증하지 않습니다.
    본 TC는 그 이동 목적지(URL 계약)를 검증하므로 별도 Risk Coverage로 판단해 중복 처리하지
    않았습니다.
  - **TC-PRODUCT-DETAIL-015 vs `cart.md` TC-CART-001**: 두 TC 모두 "Add to cart" 클릭 시
    노출되는 확인 모달을 다루지만, 모달 자체의 상세 구성(아이콘/문구/버튼)은 `cart.md`
    TC-CART-001의 책임이고(본 TC는 재기술하지 않음), 본 TC는 상세 페이지 고유의 Quantity
    입력값 캡처 → 장바구니 반영 → 공유 모달 렌더링이 이 페이지 문맥에서 새롭게 결합되는지를
    검증합니다. `product-detail.md` TC 목록의 Priority 산정 근거에도 이미 동일한 논리로
    별도 Risk Coverage임이 명시되어 있어 중복으로 판단하지 않았습니다.
  - **TC-PRODUCT-DETAIL-019/020 vs `login-logout.md` TC-LOGIN-LOGOUT-007~009**: 검증 대상
    페이지/폼이 서로 다르므로(로그인 폼 vs 리뷰 작성 폼) TC ID 수준의 중복은 아니지만, "브라우저
    자체(HTML5 native) 유효성 검사를 검증하는 TC는 Regression ROI가 낮다"는 동일한 평가 근거를
    일관되게 적용해 `login-logout.md`와 동일하게 Candidate: No로 판정했습니다(Skill 2.4/4.2
    참고, 기술적 판정 가능성과 회귀 검증 실익을 구분).
  - `login-logout.md`, `cart.md`, `page-ui.md`의 이미 확정(`상태: 자동화대상확정`)된 Approved TC
    목록을 함께 확인했으며, 그 외 나머지 TC-PRODUCT-DETAIL 항목에 대해서는 검증 목적이 실질적으로
    동일한 항목을 발견하지 못했습니다.
- Skill 1절에 따라 Automation Score만으로 기계적으로 결정하지 않고 TC 목적/ROI를 함께 고려한
  항목: TC-PRODUCT-DETAIL-004(Score 18이나 순수 장식 요소라 No), TC-PRODUCT-DETAIL-019/020
  (Score 18~19지만 브라우저 네이티브 검증의 Regression ROI가 낮아 No).
- **자동화 대상 확정 시점 Validation 결과(2026-08-27, 사용자의 "QA 승인이 전부 되어있다면
  확정해주세요" 요청에 따른 재조회 및 확정 처리)**:
  1. TC ID 유효성/중복: Sheet의 TC-PRODUCT-DETAIL-001~027(27건)이 `docs/tc/product-detail.md`에
     실제로 존재하는 TC ID와 1:1로 정확히 일치하며, Sheet 내 중복 없음을 확인.
  2. QA Decision 값 검증: 27건 전체가 정확히 `Approved`(6건) 또는 `Rejected`(21건)이며, `Hold`나
     미검토(빈 값), 그 외 잘못된 값(Validation Error)은 없음을 확인.
  3. 원본 TC 문서 상태: `docs/tc/product-detail.md`의 `상태`가 여전히 `승인완료`임을 확인.
  4. TC 변경 여부: 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-22)과 현재
     `docs/tc/product-detail.md`의 `최근 변경일`(2026-08-22)이 동일해, 평가 이후 원본 TC 문서가
     변경되지 않았음을 확인.
  - 4개 항목 모두 통과하여 Approved 6건을 자동화 대상으로 확정함(Hold 0건, Rejected 21건).

## Approved TC 목록 (자동화 대상 확정)

2026-08-27 확정. QA Decision이 `Approved`인 아래 6건만 자동화 대상으로 확정합니다(Rejected
21건은 확정하지 않음, Hold는 이번 평가에서 0건).

| TC ID | Automation Score | Candidate (AI) | QA Decision |
|---|---|---|---|
| TC-PRODUCT-DETAIL-001 | 23 | Yes | Approved |
| TC-PRODUCT-DETAIL-002 | 25 | Yes | Approved |
| TC-PRODUCT-DETAIL-008 | 20 | Hold | Approved |
| TC-PRODUCT-DETAIL-015 | 23 | Yes | Approved |
| TC-PRODUCT-DETAIL-016 | 19 | Hold | Approved |
| TC-PRODUCT-DETAIL-021 | 20 | Hold | Approved |

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-24 | 승인완료 상태의 `docs/tc/product-detail.md`(TC-PRODUCT-DETAIL-001~027, 결함 의심 항목 023~027 포함) 최초 1차 자동화 후보 평가 수행. Feature PRD(`docs/prd/feature/product-detail.md`, 승인완료)를 맥락 참고. 결함 의심 5건(023~027)은 Hard Rule 적용으로 전건 Candidate: No. login-logout/cart/page-ui 확정 문서 대상 Cross-Feature TC 중복 여부를 검토했으며 완전 중복은 발견되지 않음(TC-001/015/019/020은 검토 후 별도 Risk Coverage로 판단하거나 동일 평가 근거를 일관 적용). Yes 3건 / Hold 11건 / No 13건(Hard Rule 5건 포함). | 평가중 |
| 2026-08-24 | Google Sheet(Automation Candidates 워크시트)에 AI 작성 영역(27건 신규 추가) 동기화 완료. 이후 QA Decision/QA Comment 최초 재조회(candidate-list) 수행 결과 TC-PRODUCT-DETAIL-001~027 전체 QA Decision이 아직 비어있음(미검토) 확인. Skill Workflow 8번에 따라 최초 재조회 수행으로 상태 전환 | 사용자검토완료 |
| 2026-08-27 | 사용자의 명시적 "자동화 대상 확정" 요청에 따라 Google Sheet 재조회(candidate-list) 수행. TC-PRODUCT-DETAIL-001~027 전체 QA Decision이 입력 완료(Approved 6건, Rejected 21건, Hold 0건, 미검토 0건)됨을 확인. TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부 Validation을 모두 통과해 Approved 6건(001, 002, 008, 015, 016, 021)을 자동화 대상으로 확정. | 자동화대상확정 |
