---
문서유형: Automation Candidate Evaluation
상태: 자동화대상확정   # 평가중 | 사용자검토완료 | 자동화대상확정
대상 TC 문서: docs/tc/product-search.md
대상 TC 문서 최근 변경일(평가 시점 기준): 2026-08-31
관련 Feature PRD: feature/product-search.md
Google Sheet 워크시트: Automation Candidates
최초 작성일: 2026-08-24
최근 변경일: 2026-08-31
최근 Sheet 동기화일: 2026-08-31
확정일: 2026-08-31
---

# Automation Candidate 평가 - 상품 검색

## AI 평가 결과 (AI 작성 영역 — Google Sheet와 동기화됨)

| TC ID | Business Criticality | Regression Frequency | Automation Stability | Result Determinism | Manual Test Cost | Maintenance Cost | Automation Score | Candidate (AI) | 선정/제외 사유 |
|---|---|---|---|---|---|---|---|---|---|
| TC-PRODUCT-SEARCH-001 | 4 | 4 | 3 | 5 | 2 | 3 | 21 | Yes | 검색 실행 시 URL 변경/섹션 제목 변경/매칭 필터링이 동시에 맞물려야 하는 검색 기능의 핵심 진입점이며 다른 검색 TC(002~010)의 전제가 되는 시나리오(BC4). 2026-08-31 REQ-PRODUCT-SEARCH-005 정정으로 매칭 판정 기준이 상품명뿐 아니라 하위 카테고리명까지 포함하도록 확장되어, 오매칭 판정 시 카테고리 taxonomy에 대한 의존성이 새로 생기고 요구사항이 이번에 한 차례 정정된 이력이 있어 Automation Stability(4→3)와 Maintenance Cost(2→3, 카테고리 데이터 의존성)를 하향 조정(Score 23→21, 재평가). 매 Release 반복 검증 가치가 크고(RF4) URL/제목/DOM으로 여전히 결정적 판정 가능(RD5)해 자동화 적극 권장은 유지. |
| TC-PRODUCT-SEARCH-002 | 4 | 3 | 4 | 4 | 2 | 2 | 21 | Yes | 검색 결과 카드(이미지/가격/상품명/Add to cart/View Product)는 핵심 상품 탐색·구매 진입 UI 요소로(BC4), `page-ui.md` TC-PAGE-UI-015(ALL PRODUCTS 그리드 카드 구성, Approved)와 검증 대상 컴포넌트는 동일하나 검색 결과 필터링 경로에서 카드가 누락 없이 렌더링되는지는 별도 Risk Coverage(Skill 4.3)로 판단해 중복 제외하지 않음. 다만 이미 검증된 컴포넌트 재사용이라는 점에서 Automation Score 산정 시 여러 축을 크게 낮추지는 않되 후순위로 고려될 여지가 있어 사유에 명시함. |
| TC-PRODUCT-SEARCH-003 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 매칭 결과 없을 때 별도 "결과 없음" 안내 문구 없이 빈 목록만 노출되는 PRD 확정 동작으로, 실패해도 영향은 제한적이나(BC2) 조건부 렌더링을 DOM으로 결정적 판정 가능(RD5)하고 자동화/유지 비용이 낮아(MTC2, MC2) 경계 케이스 회귀 가치가 있어 자동화 권장. |
| TC-PRODUCT-SEARCH-004 | 2 | 3 | 4 | 5 | 2 | 2 | 20 | Yes | 빈 검색어 실행 시 전체 상품 노출 및 `?search=` URL 유지라는 경계값(Boundary) 동작으로 영향은 제한적이나(BC2) URL 문자열로 결정적 판정 가능(RD5)하고 비용이 낮아(MTC2, MC2) 자동화 권장. |
| TC-PRODUCT-SEARCH-005 | 4 | 4 | 4 | 5 | 2 | 2 | 23 | Yes | 부분 일치(substring) 매칭은 검색 기능의 핵심 로직으로 실패 시 검색 결과 신뢰성이 크게 훼손됨(BC4). 매 Release 반복 검증 가치가 크고(RF4) 결과 목록으로 결정적 판정 가능(RD5), 자동화/유지 비용도 낮아(MTC2, MC2) 자동화 적극 권장. |
| TC-PRODUCT-SEARCH-006 | 3 | 3 | 3 | 5 | 3 | 3 | 20 | Yes | 검색어가 브랜드명(`biba`/`kookie`/`allen`/`babyhug`)과 완전 일치하더라도 브랜드명은 매칭 대상에서 항상 제외되어 검색 결과에 노출되지 않아야 한다는 검색 로직의 경계(scope) 확인. 2026-08-31 REQ-PRODUCT-SEARCH-005/008 2차 정정에 따라 검증 범위가 브랜드명 4건만으로 축소됨(기존 상위 카테고리명 women/men/kids 3건은 실제 Production 상품명에 리터럴로 포함되어 전제가 깨져 제거되었고, 해당 항목은 PRD 4.2 미확인 항목으로 이관됨). 검증 방식(브랜드명 substring 검색 후 0건 확인)과 수행 난이도는 변경 전과 동일해 6개 축 점수는 20점 그대로 유지(2차 재평가 결과 점수 변경 없음, 사유 텍스트만 갱신). 오매칭 시 검색 신뢰성이 훼손된다는 영향도(BC3)와 브랜드 키워드가 실제 상품명에 우연히 포함되지 않아야 한다는 테스트 데이터 의존성(AS3, MC3)은 기존과 동일 수준으로 판단. 결과는 DOM 목록으로 결정적 판정 가능(RD5)해 자동화 권장 유지. |
| TC-PRODUCT-SEARCH-010 | 4 | 4 | 4 | 5 | 2 | 3 | 22 | Yes | REQ-PRODUCT-SEARCH-005 정정(2026-08-31)을 촉발한 실제 프로덕션 관찰 사례(검색어 "shirt" → 상품명에 "shirt"가 없지만 하위 카테고리 "Tops"로 매칭되는 "Frozen Tops For Kids" 노출)를 검증하는 신규 회귀 방지 TC(신규 평가). 검색 결과 신뢰성에 직접 영향을 주는 핵심 매칭 로직이며 아직 회귀 검증이 전혀 없는 신규 로직으로 Risk Score 16(P0)에 해당(BC4, RF4). 특정 상품명이 목록에 노출되는지 DOM으로 결정적 판정 가능(RD5)하고 절차도 단순(MTC2)하나, 특정 상품·카테고리 매핑이라는 구체적 카탈로그 데이터에 의존해 카탈로그 변경 시 테스트가 깨질 수 있어 Maintenance Cost는 다소 높게 산정(MC3). TC-001/005와 동급의 핵심 회귀 방지 가치가 있어 자동화 적극 권장. |
| TC-PRODUCT-SEARCH-007 | 2 | 2 | 4 | 4 | 3 | 3 | 18 | Hold | 검색 결과가 페이지네이션 없이 스크롤로 노출되는지 확인하는 시나리오로, 실패해도 영향은 제한적이고(BC2) 반복 검증 우선순위도 낮음(RF2, P2). 동일 패턴을 검증하는 `page-ui.md` TC-PAGE-UI-027(Home FEATURES ITEMS 스크롤 노출)은 사용자가 이미 QA Decision: Rejected로 결정한 바 있어(BC/RF 낮음 사유 동일), 검색 결과라는 별도 Risk Coverage 자체는 인정하되 동일한 저ROI 판단이 반복될 가능성이 높아 사용자 검토를 위해 Hold로 제시함. 다수 상품 매칭 검색어 준비와 스크롤 시뮬레이션으로 수행/유지 비용도 다소 높음(MTC3, MC3). |
| TC-PRODUCT-SEARCH-008 | 3 | 3 | 4 | 5 | 2 | 2 | 21 | Yes | Enter 키 입력 시 검색이 실행되지 않아야 한다는 동작으로, 실패하면 사용자 기대와 다른 화면 전환이 발생하나 돋보기 클릭이라는 대체 경로가 있어 영향은 중간 수준(BC3). URL/제목 불변으로 결정적 판정 가능(RD5)하고 단일 키 입력 이벤트 확인이라 비용이 낮아(MTC2, MC2) 자동화 권장. |
| TC-PRODUCT-SEARCH-009 | 2 | 2 | 4 | 4 | 2 | 3 | 17 | Hold | 검색창에 길이/특수문자 제한이 없다는 PRD 확정 사실을 재확인하는 경계 테스트로, 영향은 제한적이고(BC2) 반복 검증 우선순위도 낮음(RF2). 특수문자가 URL 인코딩되어 나타나 판정 로직에 인코딩 처리가 필요해 유지비용이 다소 있고(MC3), Score도 Hold 구간 하한(17)이라 사용자 검토를 위해 Hold로 제시함. |

## QA Decision (Google Sheet에서 동기화됨 — 사용자 작성 영역, AI는 수정하지 않음)

| TC ID | QA Decision | QA Comment |
|---|---|---|
| TC-PRODUCT-SEARCH-001 | Approved | |
| TC-PRODUCT-SEARCH-002 | Approved | |
| TC-PRODUCT-SEARCH-003 | Approved | |
| TC-PRODUCT-SEARCH-004 | Approved | |
| TC-PRODUCT-SEARCH-005 | Approved | |
| TC-PRODUCT-SEARCH-006 | Approved | |
| TC-PRODUCT-SEARCH-010 | Approved | |
| TC-PRODUCT-SEARCH-007 | Rejected | |
| TC-PRODUCT-SEARCH-008 | Approved | |
| TC-PRODUCT-SEARCH-009 | Rejected | |

> 이 표는 Google Sheet의 QA Decision/QA Comment 컬럼을 그대로 옮겨온 참고용 스냅샷입니다.
> 실제 값의 Source of Truth는 항상 Google Sheet이며, 이 문서를 직접 수정해도 Sheet에는
> 반영되지 않습니다. 2026-08-27 재조회(candidate-list) 결과 TC-PRODUCT-SEARCH-001~009 전체
> QA Decision이 입력 완료되었음을 확인했습니다(Approved 7건, Rejected 2건, Hold 0건, 미검토
> 0건 — 가공/재해석 없이 Sheet 값 그대로 반영). QA Comment는 전 항목 공란입니다.
>
> **2026-08-31 재평가 관련 주의**: TC-PRODUCT-SEARCH-001/006은 AI 평가 결과가 갱신되었으므로
> 위 표의 Approved 값은 재평가 이전(2026-08-27) 시점의 스냅샷입니다. `candidate-sync`는 QA
> Decision/QA Comment 셀을 건드리지 않으므로 Sheet에는 기존 Approved 값이 그대로 남아 있을
> 수 있으나, 재평가된 내용을 사용자가 다시 검토해 QA Decision을 재확인/재입력해 주셔야 합니다.
> TC-PRODUCT-SEARCH-010은 이번에 신규 추가되어 아직 QA Decision이 입력되지 않았습니다(공란).
>
> **2026-08-31 candidate-sync 실제 반영 + candidate-list 재조회 결과(가공/재해석 없이 그대로
> 반영)**: 신규 추가 1건(TC-PRODUCT-SEARCH-010), AI 컬럼 갱신 9건(TC-PRODUCT-SEARCH-001~009)이
> Sheet에 정상 반영되었습니다. 재조회 결과 TC-PRODUCT-SEARCH-001의 QA Decision은 `Approved`로
> 유지되어 있고, TC-PRODUCT-SEARCH-006의 QA Decision도 `Approved`로 유지되어 있습니다(재평가로
> AI 점수/사유가 바뀌었더라도 도구 설계상 기존 QA Decision은 보존됨 — 다만 사용자가 재평가
> 내용을 확인한 뒤 그대로 유지할지 변경할지는 사용자 판단입니다). TC-PRODUCT-SEARCH-010의 QA
> Decision은 이 시점에는 아직 공란(미검토)이었습니다.
>
> **2026-08-31 재조회(candidate-list, 2차) 결과(가공/재해석 없이 그대로 반영)**: 사용자가
> Sheet에 TC-PRODUCT-SEARCH-010의 QA Decision을 직접 `Approved`로 입력했습니다. 재조회 결과
> TC-PRODUCT-SEARCH-001/006/010 세 TC 모두 QA Decision = `Approved`이며, 나머지 TC는 기존과
> 동일(002~006, 008 = Approved, 007/009 = Rejected)합니다. 전체 10건 모두 정확히
> `Approved`/`Rejected` 중 하나이며 Hold/미검토/잘못된 값은 없습니다. 위 QA Decision 표의
> TC-PRODUCT-SEARCH-010 값을 `Approved`로 갱신했습니다.
>
> **2026-08-31 TC-006 2차 재작성에 따른 주의(재확인 필요)**: `docs/tc/product-search.md`의
> TC-PRODUCT-SEARCH-006이 같은 날 다시 재승인되어(REQ-PRODUCT-SEARCH-005/008 2차 정정), 검증
> 범위가 "브랜드명 4건 + 상위 카테고리명 3건"에서 "브랜드명 4건만"으로 좁혀졌습니다. AI 평가
> 결과의 6개 축 점수/Score(20)/Candidate(Yes)는 변경되지 않았지만 "선정/제외 사유" 텍스트는 새
> 시나리오에 맞게 갱신했습니다. 위 표의 TC-PRODUCT-SEARCH-006 `Approved` 값은 **2차 정정 이전
> (구 시나리오: 브랜드+상위 카테고리 7건) 시점의 Sheet 스냅샷**이며, `candidate-sync`를 다시
> 실행하기 전까지는 Sheet의 값도 그대로일 수 있습니다. 새 시나리오(브랜드명 4건만)를 기준으로
> 사용자가 QA Decision을 재확인/재입력해 주셔야 합니다.
>
> **2026-08-31 candidate-sync 재반영 + candidate-list 재조회(3차) 결과(가공/재해석 없이 그대로
> 반영)**: `candidate-sync`가 다시 실행되어 신규 추가 0건, AI 컬럼 갱신 10건(TC-PRODUCT-SEARCH-
> 001~010, TC-006의 갱신된 "선정/제외 사유" 포함)이 Sheet에 반영되었고 QA Decision/QA Comment는
> 보존되었습니다. 이어서 `candidate-list`로 재조회한 결과 QA Decision은 기존과 동일하게
> 001~006/008/010 = `Approved`, 007/009 = `Rejected`이며(TC-006도 `Approved` 그대로 유지), Hold/
> 미검토/잘못된 값은 없습니다. 이는 Sheet 상 값 자체는 바뀌지 않았다는 뜻이며, TC-006의 새
> 시나리오(브랜드명 4건만)에 대한 재확인은 아래와 같이 사용자와의 직접 대화로 별도 확보했습니다:
> 사용자에게 "TC-006이 브랜드명 4건만 검증하는 새 시나리오로 바뀌었는데, 이 새 시나리오로 QA
> Decision Approved를 재확인하시겠습니까?"라고 질문했고, 사용자가 "재확인(Approved 유지)"으로
> 명확히 답변했습니다. 이로써 TC-006의 `Approved`는 새 시나리오(브랜드명 4건만) 기준으로도
> 유효한 QA Decision임이 확인되었습니다.

## Hard Rule 적용 / Validation 특이사항

- **Hard Rule(5절, 결함을 정상처럼 고정한 TC) 해당 항목 없음**: `product-search.md` 문서 자체가
  "결함 의심으로 표시된 REQ 항목이 없다"고 명시하고 있으며, 평가 과정에서도 현재 발생 중인 결함을
  정상 Expected Result로 고정한 TC는 발견되지 않았습니다.
- **2026-08-31 재평가 시 Hard Rule 재확인(TC-001/006/010)**: 자동화 구현 중 발견된 Production
  검색 결과 불일치(상품명에 검색어가 없는 상품이 노출되는 현상)는 한때 "결함이 의심되는 동작"으로
  보일 수 있었으나, Feature PRD의 REQ-PRODUCT-SEARCH-005가 이를 정상 요구사항(하위 카테고리명도
  매칭 대상)으로 정정·재승인(2026-08-31)했으므로 Skill 5절 "이 규칙은 영구적이지 않다" 예외에
  해당합니다. 즉 TC-001/006/010은 결함을 정상처럼 고정한 TC가 아니라 정정된 정상 요구사항을
  검증하는 TC이며, Hard Rule 적용 대상이 아닙니다.
- **TC-001 재평가 필요성 판단(단순 문구 동기화 아님)**: Expected Result가 "상품명만 매칭"에서
  "상품명 또는 하위 카테고리명 매칭"으로 실제 검증 로직 자체가 확장되어, Automation
  Stability/Maintenance Cost 재산정이 필요하다고 판단해 재평가함(Score 23→21, Candidate Yes 유지).
- **TC-006 재평가 필요성 판단**: Test Scenario/Preconditions/Test Steps/Expected Result가 전면
  재작성되어 검증 방향이 반대로 바뀜(기존: 하위 카테고리명(TOPS)도 매칭 안 됨 검증 → 현재: 하위
  카테고리명은 매칭되고 브랜드명·상위 카테고리명만 매칭 안 됨 검증)에 따라 재평가함. 재평가 결과
  6개 축의 자동화 특성(영향도/반복빈도/판정가능성/비용/유지보수)은 기존과 동일 수준으로 판단해
  점수(20점)는 변경하지 않았고, "선정/제외 사유" 텍스트만 새 시나리오에 맞게 갱신함.
- **TC-010 신규 평가**: 이번에 신규 추가된 TC로, Hard Rule 해당 없음(위 항목 참조). 6개 축 평가
  결과 Score 22, Candidate: Yes로 신규 판정함.
- **TC-006 2차 재평가 필요성 판단(2026-08-31, 같은 날 2차 정정)**: `docs/tc/product-search.md`의
  TC-PRODUCT-SEARCH-006이 REQ-PRODUCT-SEARCH-005/008 2차 정정에 따라 다시 재작성됨(자동화 구현/
  실행 결과 상위 카테고리명 women/men/kids 3건이 실제 상품명에 리터럴로 포함되어 매칭됨을 발견,
  브랜드명은 완전 일치 포함 항상 제외로 명확화하고 상위 카테고리명 매칭 여부는 PRD 4.2 미확인
  항목으로 이관, TC-006 검증 대상을 브랜드명 4건만으로 축소). 검증 범위는 7개 keyword에서 4개
  keyword로 좁아졌으나 검증 방식(브랜드명 substring 검색 후 0건 확인)과 수행 난이도는 동일하다고
  판단해 6개 축 점수(BC3/RF3/AS3/RD5/MTC3/MC3, Score 20)는 변경하지 않고 "선정/제외 사유"
  텍스트만 새 시나리오에 맞게 갱신함(Candidate: Yes 유지). 참고로 자동화 코드
  (`automation/tests/test_product_search.py::test_search_with_brand_keyword_shows_no_result`,
  parametrize 4건)가 이미 구현되어 pytest 실행 결과 4건 전건 PASSED로 확인된 상태이나, 이는
  구현 단계의 결과이며 이번 평가 축 재산정에는 반영하지 않음(평가는 자동화 적합성 판단이지 구현
  검증이 아님). TC-006의 Test Scenario/Expected Result 자체가 실질적으로 변경되었으므로, 점수
  변경 여부와 무관하게 "자동화대상확정 문서 재수정 시 처리" 절차에 따라 문서 상태를
  `자동화대상확정 → 사용자검토완료`로 되돌리고 TC-006에 대한 QA Decision을 다시 받아야 함(기존
  `Approved`는 구 시나리오 기준 스냅샷).
- **Cross-Feature 중복 검토 결과(사용자 요청에 따른 확인)**: `page-ui.md`의 CATEGORY/BRANDS
  필터링 관련 TC(TC-PAGE-UI-023~033 등, 사이드바에서 카테고리/브랜드 클릭 시 상품 목록 페이지로
  이동해 필터링되는 시나리오)와 `product-search.md`의 TC-PRODUCT-SEARCH-006(검색창에 카테고리/
  브랜드명 키워드를 입력해도 상품명에 없으면 매칭되지 않음을 확인)을 비교한 결과, **검증 목적이
  서로 다릅니다**: page-ui TC들은 "카테고리/브랜드 네비게이션 클릭 시 해당 카테고리/브랜드
  상품만 필터링되는지"를 검증하는 반면, TC-PRODUCT-SEARCH-006은 "검색창 텍스트 매칭이 상품명
  필드에만 적용되고 카테고리/브랜드 필드에는 적용되지 않는지"를 검증합니다. TC-PAGE-UI-040/041과
  cart.md TC-CART-012/013처럼 Test Steps가 사실상 동일한 수준의 중복은 아니라고 판단해
  TC-PRODUCT-SEARCH-006은 Cross-Feature 중복으로 표시하지 않았습니다.
- **부분적 컴포넌트 재사용 중복 검토**: TC-PRODUCT-SEARCH-002(검색 결과 카드 구성)는
  `page-ui.md` TC-PAGE-UI-015(ALL PRODUCTS 그리드 카드 구성, QA Decision: Approved)와 동일한
  카드 컴포넌트를 검증하지만, 검색 결과 필터링 경로에서의 렌더링을 확인한다는 별도 Risk
  Coverage가 있어 완전한 중복(Skill 4.3)으로는 보지 않았습니다. 다만 이미 검증된 컴포넌트
  재사용이라는 점은 위 표의 사유에 명시했으니 사용자 검토 시 참고 바랍니다.
- **동일 패턴 저ROI 선례 검토**: TC-PRODUCT-SEARCH-007(검색 결과 스크롤 노출)은 `page-ui.md`
  TC-PAGE-UI-027(Home FEATURES ITEMS 스크롤 노출)과 동일한 "페이지네이션 없이 스크롤로 노출"
  패턴을 검증하며, TC-PAGE-UI-027은 사용자가 이미 QA Decision: Rejected로 확정한 바 있습니다.
  완전한 중복은 아니라고 판단해 후보 표에는 포함했으나(Hold), 유사 선례가 있다는 점을 참고
  사항으로 기록합니다.
- 그 외 TC(001, 003, 004, 005, 008, 009)는 login-logout/cart/page-ui의 확정된 TC 목록과
  비교했을 때 검증 대상(검색 URL/제목/필터링 로직, 빈 검색어 처리, substring 매칭, Enter 키
  무시, 입력값 제한 없음)이 겹치지 않아 별도 중복 이슈는 발견되지 않았습니다.

- **자동화 대상 확정 시점 Validation 결과(2026-08-27, 사용자의 "QA 승인이 전부 되어있다면
  확정해주세요" 요청에 따른 재조회 및 확정 처리)**:
  1. TC ID 유효성/중복: Sheet의 TC-PRODUCT-SEARCH-001~009(9건)이 `docs/tc/product-search.md`에
     실제로 존재하는 TC ID와 1:1로 정확히 일치하며, Sheet 내 중복 없음을 확인.
  2. QA Decision 값 검증: 9건 전체가 정확히 `Approved`(7건) 또는 `Rejected`(2건)이며, `Hold`나
     미검토(빈 값), 그 외 잘못된 값(Validation Error)은 없음을 확인.
  3. 원본 TC 문서 상태: `docs/tc/product-search.md`의 `상태`가 여전히 `승인완료`임을 확인.
  4. TC 변경 여부: 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-22)과 현재
     `docs/tc/product-search.md`의 `최근 변경일`(2026-08-22)이 동일해, 평가 이후 원본 TC 문서가
     변경되지 않았음을 확인.
  - 4개 항목 모두 통과하여 Approved 7건을 자동화 대상으로 확정함(Hold 0건, Rejected 2건). 참고로
    TC-PRODUCT-SEARCH-007(Hold로 제시했던 TC)은 QA Decision이 `Rejected`로 결정되어 확정
    대상에서 제외됨.

- **자동화 대상 재확정 시점 Validation 결과(2026-08-31, 사용자의 명시적 "자동화 대상 확정"
  요청에 따른 재조회 및 확정 처리 — TC-001/006 재평가, TC-010 신규 평가 반영)**:
  1. TC ID 유효성/중복: Sheet의 TC-PRODUCT-SEARCH-001~010(10건)이 `docs/tc/product-search.md`에
     실제로 존재하는 TC ID와 1:1로 정확히 일치하며, Sheet 내 중복 없음을 확인.
  2. QA Decision 값 검증: 10건 전체가 정확히 `Approved`(8건: 001~006, 008, 010) 또는
     `Rejected`(2건: 007, 009)이며, `Hold`나 미검토(빈 값), 그 외 잘못된 값(Validation Error)은
     없음을 확인. TC-PRODUCT-SEARCH-010은 사용자가 Sheet에 직접 `Approved`를 입력함.
  3. 원본 TC 문서 상태: `docs/tc/product-search.md`의 `상태`가 여전히 `승인완료`임을 확인.
  4. TC 변경 여부: 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-31)과 현재
     `docs/tc/product-search.md`의 `최근 변경일`(2026-08-31)이 동일해, 이번 재평가(TC-001 수정/
     TC-006 재작성/TC-010 추가) 이후 원본 TC 문서가 추가로 변경되지 않았음을 확인.
  - 4개 항목 모두 통과하여 Approved 8건(001~006, 008, 010)을 자동화 대상으로 확정함(Hold 0건,
    Rejected 2건: 007, 009). 기존 확정 목록(001~006, 008, 7건) 대비 TC-010이 신규로 추가되어
    총 8건으로 확정됨.

- **자동화 대상 재확정 시점 Validation 결과(2026-08-31, TC-006 2차 재작성에 따른 재확정 —
  사용자의 명시적 "자동화 대상 확정" 요청에 따른 재조회 및 확정 처리)**:
  1. TC ID 유효성/중복: `candidate-list` 재조회 결과 Sheet의 TC-PRODUCT-SEARCH-001~010(10건)이
     `docs/tc/product-search.md`에 실제로 존재하는 TC ID와 1:1로 정확히 일치하며, Sheet 내
     중복 없음을 확인.
  2. QA Decision 값 검증: 10건 전체가 정확히 `Approved`(8건: 001~006, 008, 010) 또는
     `Rejected`(2건: 007, 009)이며, `Hold`나 미검토(빈 값), 그 외 잘못된 값(Validation Error)은
     없음을 확인. TC-PRODUCT-SEARCH-006의 `Approved`는 Sheet 상 기존 값이 그대로 유지된
     것이었으나, 새 시나리오(브랜드명 4건만)에 대해서도 유효한지 사용자에게 직접 질문했고
     사용자가 "재확인(Approved 유지)"으로 명확히 답변함을 확인.
  3. 원본 TC 문서 상태: `docs/tc/product-search.md`의 `상태`가 여전히 `승인완료`임을 확인.
  4. TC 변경 여부: 프런트매터의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(2026-08-31)과 현재
     `docs/tc/product-search.md`의 `최근 변경일`(2026-08-31)이 동일하며, 이번 TC-006 2차
     재평가(브랜드명 4건만으로 범위 축소)가 이미 AI 평가 결과에 반영되어 있어 원본 TC 문서와
     평가 내용 간 불일치가 없음을 확인.
  - 4개 항목 모두 통과하여 Approved 8건(001~006, 008, 010)을 자동화 대상으로 재확정함(Hold 0건,
    Rejected 2건: 007, 009). 확정 목록 자체(8건, TC ID 구성)는 이전과 동일하나, TC-006은 새
    시나리오(브랜드명 4건만) 기준으로 QA Decision이 재확인되었다는 점에서 의미가 갱신됨.

## Approved TC 목록 (자동화 대상 확정)

**2026-08-31 최종 재확정**: TC-PRODUCT-SEARCH-006이 2차로 재작성되어(검증 범위: 브랜드명 4건만)
일시적으로 `사용자검토완료`로 되돌아갔으나, 사용자가 새 시나리오 기준으로 QA Decision(Approved)을
직접 재확인함에 따라 재조회·Validation을 통과해 아래 8건이 자동화 대상으로 재확정되었습니다.

| TC ID | Automation Score | Candidate (AI) | QA Decision |
|---|---|---|---|
| TC-PRODUCT-SEARCH-001 | 21 | Yes | Approved |
| TC-PRODUCT-SEARCH-002 | 21 | Yes | Approved |
| TC-PRODUCT-SEARCH-003 | 20 | Yes | Approved |
| TC-PRODUCT-SEARCH-004 | 20 | Yes | Approved |
| TC-PRODUCT-SEARCH-005 | 23 | Yes | Approved |
| TC-PRODUCT-SEARCH-006 | 20 | Yes | Approved |
| TC-PRODUCT-SEARCH-008 | 21 | Yes | Approved |
| TC-PRODUCT-SEARCH-010 | 22 | Yes | Approved |

제외(미확정/Rejected):
- TC-PRODUCT-SEARCH-007 — QA Decision: Rejected (확정 대상 아님)
- TC-PRODUCT-SEARCH-009 — QA Decision: Rejected (확정 대상 아님)

> 참고(2026-08-27 1차 확정 이력): 당시 QA Decision이 `Approved`였던 TC-PRODUCT-SEARCH-001, 002,
> 003, 004, 005, 006, 008 (Score 23/21/20/20/23/20/21)이 자동화 대상으로 확정되었습니다. 이후
> 원본 TC 재승인에 따라 TC-001(Score 23→21)/TC-006(사유만 갱신, Score 20 유지)이 재평가되었고,
> TC-010(신규, Score 22)이 추가되어 이번 2026-08-31 재확정을 통해 총 8건으로 갱신되었습니다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-24 | 승인완료된 TC 문서(`docs/tc/product-search.md`, TC-PRODUCT-SEARCH-001~009)를 대상으로 automation-candidate Skill 6개 축 1차 평가 수행. Hard Rule 해당 항목 없음. Yes 7건 / Hold 2건 / No 0건. 사용자 요청에 따라 login-logout/cart/page-ui(특히 CATEGORY/BRANDS 필터링 TC)와의 Cross-Feature 중복 여부를 검토했으며, page-ui TC-PAGE-UI-040/041 수준의 완전한 중복은 발견되지 않았으나 TC-PRODUCT-SEARCH-002(카드 컴포넌트 재사용)와 TC-PRODUCT-SEARCH-007(스크롤 노출 패턴, page-ui TC-PAGE-UI-027 Rejected 선례 있음)에 부분적 중복/저ROI 참고사항을 기록함. | 평가중 |
| 2026-08-27 | 사용자의 명시적 "자동화 대상 확정" 요청에 따라 Google Sheet 재조회(candidate-list) 수행. TC-PRODUCT-SEARCH-001~009 전체 QA Decision이 입력 완료(Approved 7건, Rejected 2건, Hold 0건, 미검토 0건)됨을 확인. TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부 Validation을 모두 통과해 Approved 7건(001~006, 008)을 자동화 대상으로 확정(007, 009는 Rejected로 제외). | 자동화대상확정 |
| 2026-08-31 | 원본 TC 문서(`docs/tc/product-search.md`) 재승인(REQ-PRODUCT-SEARCH-005 정정)에 따라 "자동화대상확정 문서 재수정 시 처리" 절차 수행. TC-PRODUCT-SEARCH-001(Expected Result 확장 — 상품명 또는 하위 카테고리명 매칭)과 TC-PRODUCT-SEARCH-006(검증 방향 반전 — 하위 카테고리명은 매칭, 브랜드명·상위 카테고리명만 제외)을 재평가함(사용자 승인 후 진행). TC-001: AS 4→3, MC 2→3, Score 23→21로 조정(Candidate Yes 유지). TC-006: 6개 축 점수는 20점으로 변경 없음, 사유 텍스트만 새 시나리오에 맞게 갱신. 신규 TC-PRODUCT-SEARCH-010(하위 카테고리명 substring 매칭, P0)을 6개 축 기준 신규 평가(Score 22, Candidate: Yes)해 표에 추가. TC-002/003/004/005/007/008/009는 이번 변경과 무관해 그대로 유지. 영향받는 TC(001/006)와 신규 TC(010)는 QA Decision을 다시 받아야 하므로 문서 상태를 `자동화대상확정 → 사용자검토완료`로 되돌림(대상 TC 문서 최근 변경일도 2026-08-22→2026-08-31로 갱신). | 사용자검토완료 |
| 2026-08-31 | `candidate-sync --dry-run`(신규 1건 TC-010, AI 컬럼 갱신 9건 TC-001~009 확인) 이후 실제 `candidate-sync` 반영 완료(신규 추가 1건, AI 컬럼 갱신 9건, QA Decision/QA Comment 보존 확인). 이어서 `candidate-list`로 재조회한 결과 TC-PRODUCT-SEARCH-001 QA Decision=Approved(유지), TC-PRODUCT-SEARCH-006 QA Decision=Approved(유지), TC-PRODUCT-SEARCH-010 QA Decision=공란(미검토)을 확인해 위 QA Decision 표에 가공 없이 반영. TC-010의 QA Decision이 입력될 때까지 대기하며, 사용자가 명시적으로 "자동화 대상 확정"을 요청하기 전까지 문서 상태는 `사용자검토완료`로 유지(자동화대상확정으로 임의 전환하지 않음). | 사용자검토완료 |
| 2026-08-31 | 사용자가 Sheet에 TC-PRODUCT-SEARCH-010의 QA Decision을 `Approved`로 직접 입력함에 따라, 사용자의 명시적 "자동화 대상 확정" 요청을 받아 `candidate-list` 재조회(2차) 수행. TC-PRODUCT-SEARCH-001/006/010 세 TC 모두 QA Decision=Approved 확인(나머지 002~006/008=Approved, 007/009=Rejected는 기존과 동일). TC ID 유효성/중복, QA Decision 값(잘못된 값/미검토 없음), 원본 TC 승인완료 상태, TC 변경 여부(평가 시점 기준 최근 변경일 2026-08-31과 원본 최근 변경일 2026-08-31 일치) 4개 Validation을 모두 통과. TC-001 재평가(Score 23→21)/TC-006 재평가(사유 갱신, Score 20 유지)/TC-010 신규 승인을 반영해 Approved 8건(001~006, 008, 010)을 자동화 대상으로 최종 확정(Rejected 2건: 007, 009, Hold 0건). 문서 상태를 `사용자검토완료 → 자동화대상확정`으로 전환하고 확정일(2026-08-31)을 기록. | 자동화대상확정 |
| 2026-08-31 | `docs/tc/product-search.md` TC-PRODUCT-SEARCH-006이 같은 날 2차로 재작성됨(REQ-PRODUCT-SEARCH-005/008 2차 정정 — 브랜드명은 완전 일치 포함 항상 제외로 명확화, 상위 카테고리명 women/men/kids 3건은 실제 상품명에 리터럴 포함되어 전제 불성립으로 제거 및 PRD 4.2 미확인 항목 이관, 검증 범위를 브랜드명 4건만으로 축소)에 따라 "자동화대상확정 문서 재수정 시 처리" 절차 수행. TC-PRODUCT-SEARCH-006만 재평가함: 검증 방식(브랜드명 substring 검색 후 0건 확인)과 난이도가 변경 전과 동일하다고 판단해 6개 축 점수(BC3/RF3/AS3/RD5/MTC3/MC3, Score 20)는 유지하고 "선정/제외 사유" 텍스트만 새 시나리오(브랜드명 4건만)에 맞게 갱신(Candidate: Yes 유지). 참고로 자동화 코드(`test_search_with_brand_keyword_shows_no_result`, parametrize 4건)가 이미 구현되어 pytest 4건 전건 PASSED 확인됨(구현 결과는 참고 정보이며 평가 축 재산정에는 미반영). TC-002/003/004/005/007/008/009/010은 이번 변경과 무관해 그대로 유지. TC-006의 Test Scenario/Expected Result 자체가 실질적으로 변경되어 QA Decision을 새 시나리오 기준으로 다시 받아야 하므로, 문서 상태를 `자동화대상확정 → 사용자검토완료`로 되돌리고 확정일을 비움. 기존 "Approved TC 목록"은 이전 확정 이력(참고용, 재확정 필요)으로 표시. Google Sheet 동기화는 사용자 확인 후 별도 진행 예정. | 사용자검토완료 |
| 2026-08-31 | `candidate-sync` 재실행(신규 0건, AI 컬럼 갱신 10건 — TC-006의 갱신된 "선정/제외 사유" 반영, QA Decision/QA Comment 보존 확인) 및 `candidate-list` 재조회(3차, 직접 실행으로 독립 검증) 완료. QA Decision은 기존과 동일하게 001~006/008/010=Approved, 007/009=Rejected(Hold/미검토/잘못된 값 없음)이며, TC-006의 Approved 값은 Sheet 상 변경 없이 유지된 것이었음. 이에 대해 사용자에게 "TC-006이 브랜드명 4건만 검증하는 새 시나리오로 바뀌었는데 Approved를 재확인하시겠습니까?"를 직접 질의해 "재확인(Approved 유지)" 답변을 받아, TC-006의 QA Decision이 새 시나리오 기준으로도 유효함을 확보. TC ID 유효성/중복, QA Decision 값, 원본 TC 승인완료 상태, TC 변경 여부(원본 TC 최근 변경일과 평가 시점 기준 변경일 2026-08-31 일치, TC-006 2차 재평가 내용이 AI 평가 결과에 이미 반영됨) 4개 Validation을 모두 통과해 Approved 8건(001~006, 008, 010)을 자동화 대상으로 재확정(Rejected 2건: 007, 009, Hold 0건). 문서 상태를 `사용자검토완료 → 자동화대상확정`으로 전환하고 확정일(2026-08-31)을 기록. | 자동화대상확정 |
