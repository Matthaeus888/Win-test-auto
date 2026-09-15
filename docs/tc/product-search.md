---
문서유형: Test Case
상태: 승인완료   # 초안 | 승인완료
관련 Feature PRD: feature/product-search.md
최초 작성일: 2026-08-22
최근 변경일: 2026-08-31
승인일: 2026-08-22
---

# Test Case - 상품 검색

## TC 목록

> 공통 Preconditions: 사이트 진입 시 또는 일정 시간 경과 시 무작위로 노출될 수 있는 모달형 광고는
> Project PRD "8. 기타 제약사항" 원칙에 따라 검증 대상이 아니므로, 모든 TC 수행 전 광고 모달이
> 노출된 경우 닫은 상태에서 진행한다(아래 표에는 반복 기재하지 않음). 별도 언급이 없는 한 로그인/
> 로그아웃 상태는 무관하다(Feature PRD에 로그인 필요 조건이 명시되지 않음).

| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-PRODUCT-SEARCH-001 | REQ-PRODUCT-SEARCH-001 | 상품 검색 | Products 페이지 검색창에 매칭되는 상품이 존재하는 검색어를 입력하고 검색 실행 시 URL 변경, 섹션 제목 변경, 매칭 상품만 노출되는지 확인 | Products 페이지(`/products`)에 진입해 있는 상태, 실제 상품명 또는 하위 카테고리명에 포함되는 검색어 확인됨(예: "shirt") | 1. Products 페이지의 "Search Product" 검색창에 실제 상품명과 매칭되는 검색어(예: "shirt")를 입력한다.<br>2. 돋보기 아이콘 버튼을 클릭한다.<br>3. 페이지 URL, 섹션 제목, 노출되는 상품 목록을 확인한다. | URL이 `https://automationexercise.com/products?search=shirt` 형태로 변경되고, 상품 목록 상단 섹션 제목이 "SEARCHED PRODUCTS"로 바뀌며, 입력한 검색어가 상품명 또는 하위 카테고리명(예: Tops, Dress, Tshirts, Jeans, Saree) 중 하나 이상에 부분 일치하는 상품만 노출된다(상품명과 하위 카테고리명 어디에도 검색어가 포함되지 않는 상품은 노출되지 않는다). | P0 | |
| TC-PRODUCT-SEARCH-002 | REQ-PRODUCT-SEARCH-002 | 상품 검색 | 검색 결과 상품 카드 구성(이미지/가격/상품명/Add to cart/View Product)이 ALL PRODUCTS 그리드와 동일한지 확인 | Products 페이지에서 매칭되는 검색어로 검색을 실행해 검색 결과가 노출된 상태(예: "shirt") | 1. 검색 결과에 노출된 임의의 상품 카드 하나를 확인한다. | 상품 카드에 이미지, 가격, 상품명, "Add to cart" 버튼, "View Product" 링크가 모두 노출되며, ALL PRODUCTS 목록의 카드 구성(`page-ui.md` REQ-PAGE-UI-011)과 동일한 레이아웃이다. | P2 | |
| TC-PRODUCT-SEARCH-003 | REQ-PRODUCT-SEARCH-003 | 상품 검색 | 매칭되는 상품이 없는 검색어로 검색 실행 시 상품 카드 없이 빈 목록 영역만 노출되고 별도 "결과 없음" 안내 문구가 노출되지 않는지 확인 | Products 페이지에 진입해 있는 상태, 어떤 상품명에도 매칭되지 않는 검색어 확인됨(예: "zzzzznonexistent") | 1. 검색창에 매칭되는 상품이 없을 것으로 예상되는 검색어(예: "zzzzznonexistent")를 입력한다.<br>2. 돋보기 아이콘 버튼을 클릭한다.<br>3. 노출되는 화면을 확인한다. | 섹션 제목은 "SEARCHED PRODUCTS"로 동일하게 노출되지만 그 아래에는 상품 카드가 하나도 노출되지 않고 빈 목록 영역만 남는다. "No result" 등 별도 결과 없음 안내 문구는 노출되지 않는다. | P2 | |
| TC-PRODUCT-SEARCH-004 | REQ-PRODUCT-SEARCH-004 | 상품 검색 | 검색어를 입력하지 않은 채(빈 문자열) 검색 실행 시 전체 상품이 노출되고 URL에는 `?search=` 형태가 남는지 확인 | Products 페이지에 진입해 있는 상태, 검색창이 빈 값인 상태 | 1. 검색창에 아무 값도 입력하지 않은 채 돋보기 아이콘 버튼을 클릭한다.<br>2. 노출되는 상품 목록과 URL을 확인한다. | Products 페이지 원본(ALL PRODUCTS)과 동일하게 전체 상품이 노출된다. URL은 `https://automationexercise.com/products?search=` 형태로 남아, 검색을 실행하지 않은 원본 Products 페이지 URL(`/products`)과 구분된다. | P2 | |
| TC-PRODUCT-SEARCH-005 | REQ-PRODUCT-SEARCH-005 | 상품 검색 | 검색어가 상품명의 일부 문자열(substring)과 일치할 때 부분 일치 매칭으로 해당 상품이 노출되는지 확인 | Products 페이지에 진입해 있는 상태, 특정 상품명의 일부에 해당하는 검색어 확인됨(예: 상품명이 "Blue Top"인 경우 "Top"만 입력) | 1. 검색창에 특정 상품명의 일부 문자열만 포함하는 검색어(예: "Top")를 입력한다.<br>2. 돋보기 아이콘 버튼을 클릭한다.<br>3. 노출되는 상품 목록을 확인한다. | 입력한 문자열이 상품명에 부분적으로라도 포함되는 모든 상품이 검색 결과에 노출된다(정확히 일치하지 않아도 매칭됨). | P1 | |
| TC-PRODUCT-SEARCH-006 | REQ-PRODUCT-SEARCH-005 | 상품 검색 | 검색어가 브랜드명과 일치(완전 일치 포함)하더라도 브랜드명은 매칭 대상에서 항상 제외되어 검색 결과에 노출되지 않는지 확인 | Products 페이지에 진입해 있는 상태, 브랜드명 keyword(`biba`, `kookie`, `allen`, `babyhug` — 실제 브랜드명 BIBA, KOOKIE KIDS, ALLEN SOLLY JUNIOR, BABYHUG에 대응)가 실제 상품명 및 하위 카테고리명 문자열에는 포함되지 않음이 확인됨 | 1. 검색창에 브랜드명 keyword(예: `biba`, `kookie`, `allen`, `babyhug`)를 검색어로 입력한다.<br>2. 돋보기 아이콘 버튼을 클릭한다.<br>3. 노출되는 상품 목록을 확인한다. | 해당 브랜드에 속한 상품이라도 검색 결과에 노출되지 않는다(브랜드명은 완전 일치·부분 일치 여부와 무관하게 매칭 대상에서 항상 제외되므로, 상품명·하위 카테고리명 문자열에 키워드가 포함되지 않는 한 결과에서 제외됨). | P2 | |
| TC-PRODUCT-SEARCH-010 | REQ-PRODUCT-SEARCH-005 | 상품 검색 | 검색어가 상품명에는 포함되지 않지만 하위 카테고리명과 일치할 때, 부분 일치 매칭으로 해당 상품이 노출되는지 확인 | Products 페이지에 진입해 있는 상태. 상품명에는 검색어가 포함되지 않지만 하위 카테고리명을 통해 매칭되는 것으로 이미 관찰된 상품·검색어 조합 확인됨(예: 검색어 "shirt", 상품 "Frozen Tops For Kids" — 상품명에 "shirt" 문자열 없음. `feature/product-search.md` 7. 비고 2026-08-31 기록 근거) | 1. 검색창에 "shirt"를 입력한다.<br>2. 돋보기 아이콘 버튼을 클릭한다.<br>3. 검색 결과에 "Frozen Tops For Kids"가 노출되는지 확인한다. | 상품명에 "shirt" 문자열이 포함되지 않는 "Frozen Tops For Kids"가 검색 결과에 노출된다(하위 카테고리명 부분 일치를 통해 매칭됨). | P0 | |
| TC-PRODUCT-SEARCH-007 | REQ-PRODUCT-SEARCH-006 | 상품 검색 | 검색 결과 상품 수가 많은 경우 별도 페이지네이션 없이 스크롤을 통해 이어서 노출되는지 확인 | Products 페이지에 진입해 있는 상태, 검색 결과가 한 화면에 다 노출되지 않을 만큼 많이 반환되는 검색어 확인됨(예: "shirt") | 1. 검색창에 다수의 상품이 매칭될 것으로 예상되는 검색어(예: "shirt")를 입력하고 돋보기 아이콘 버튼을 클릭한다.<br>2. 검색 결과 화면에서 페이지네이션 UI(페이지 번호, Next/Previous 버튼 등) 존재 여부를 확인한다.<br>3. 화면을 아래로 스크롤해 추가 상품이 이어서 노출되는지 확인한다. | 페이지네이션 UI가 노출되지 않으며, 스크롤을 통해 매칭된 모든 상품이 이어서 노출된다(`page-ui.md` REQ-PAGE-UI-021과 동일한 패턴). | P2 | |
| TC-PRODUCT-SEARCH-008 | REQ-PRODUCT-SEARCH-007 | 상품 검색 | 검색창에 검색어를 입력한 상태에서 Enter 키를 입력해도 검색이 실행되지 않는지 확인 | Products 페이지에 진입해 있는 상태 | 1. 검색창에 임의의 검색어(예: "shirt")를 입력한다.<br>2. 돋보기 아이콘 버튼을 클릭하지 않고 키보드의 Enter 키를 입력한다.<br>3. 화면과 URL의 변화 여부를 확인한다. | 검색이 실행되지 않는다. URL과 섹션 제목("ALL PRODUCTS")이 검색 실행 전 상태 그대로 유지되며, 상품 목록도 변화하지 않는다. | P2 | |
| TC-PRODUCT-SEARCH-009 | REQ-PRODUCT-SEARCH-008 | 상품 검색 | 검색창에 길이 제한 없이 긴 문자열과 특수문자를 입력해도 별도의 클라이언트 측 검증(길이 제한, 특수문자 제한) 없이 입력과 검색 실행이 가능한지 확인 | Products 페이지에 진입해 있는 상태 | 1. 검색창에 매우 긴 문자열과 특수문자를 포함한 값(예: 100자 이상의 임의 문자열 + "!@#$%^&*()")을 입력한다.<br>2. 돋보기 아이콘 버튼을 클릭한다.<br>3. 입력 과정과 검색 실행 결과를 확인한다. | 입력 과정에서 길이 제한이나 특수문자 제한으로 인한 경고/차단이 발생하지 않고 전체 값이 그대로 입력되며, 검색이 정상적으로 실행되어 URL이 `?search={입력값}` 형태로 변경된다(매칭되는 상품이 없어 결과가 빈 목록이더라도 REQ-PRODUCT-SEARCH-003과 동일하게 처리됨). | P2 | |

> 결함 의심 항목: `product-search.md` Feature PRD의 4.1/4.2/6절 전체를 확인한 결과, "결함
> 의심"(비정상 동작이 관찰되었으나 사실만 기록된 요구사항)으로 표시된 REQ 항목이 없어 `tc-writing`
> Skill 4.6에 따른 별도 "결함 의심 항목" 섹션은 이번 문서에 두지 않았습니다.

## Priority 산정 근거

- **TC-PRODUCT-SEARCH-001**: Impact 5 / Likelihood 4 / Risk Score 20 — 검색은 상품 탐색의 핵심 진입 경로 중 하나로 실패 시 핵심 기능 사용이 어려워지며(Impact 5), URL 변경/섹션 제목 변경/매칭 필터링이라는 세 가지 서로 다른 동작이 하나의 검색 실행 안에서 동시에 정확히 맞물려야 하는 복합 시나리오이자 다른 모든 검색 TC(TC-002~009)가 이 기본 동작이 정상임을 전제로 하는 진입점이라, 결함 발생 시 파급 범위와 발생 가능성이 모두 높다고 재평가함(Likelihood 4, 사용자 리뷰 반영). Risk Score 20으로 P0 기준(16~25)에 해당.
- **TC-PRODUCT-SEARCH-002**: Impact 3 / Likelihood 2 / Risk Score 6 — 카드 구성이 깨져도 상품 탐색·구매 자체는 가능해 영향은 제한적이며(Impact 3), `page-ui.md`에서 이미 검증된 공통 카드 컴포넌트를 재사용하는 구조라 결함 발생 가능성은 낮음(Likelihood 2).
- **TC-PRODUCT-SEARCH-003**: Impact 3 / Likelihood 2 / Risk Score 6 — PRD에 명시된 정상 동작(빈 목록만 노출)을 확인하는 것으로 잘못 동작해도 다른 상품을 잘못 노출하는 정도이며(Impact 3), 단순 조건부 렌더링이라 결함 발생 가능성은 낮음(Likelihood 2).
- **TC-PRODUCT-SEARCH-004**: Impact 2 / Likelihood 3 / Risk Score 6 — 전체 상품이 노출되는 것이 정상 동작(Fallback)이라 잘못되어도 사용자가 아예 상품을 못 보는 상황까지는 아니지만(Impact 2), 빈 문자열이라는 경계 조건에서 매칭 로직이 예외적으로 동작할 가능성이 있어(Likelihood 3) 경계값(Boundary) 테스트로 분류.
- **TC-PRODUCT-SEARCH-005**: Impact 4 / Likelihood 3 / Risk Score 12 — 부분 일치 매칭은 검색 기능의 핵심 로직으로, 정확히 동작하지 않으면 검색 결과 신뢰성이 크게 훼손되며(Impact 4), substring 매칭 로직 자체의 구현 복잡도로 결함 발생 가능성도 일반 수준 이상(Likelihood 3).
- **TC-PRODUCT-SEARCH-006**: Impact 4 / Likelihood 2 / Risk Score 8 — 브랜드명 오매칭 시 검색 결과 신뢰성이 훼손되어 영향은 여전히 크지만(Impact 4), 브랜드명 제외는 두 차례 REQ-PRODUCT-SEARCH-005 정정(2026-08-31 1차/2차)에도 흔들리지 않고 일관되게 확정된 규칙이라 발생 가능성은 낮게 판단(Likelihood 2). 2026-08-31(2차) 재검토 시 검증 범위를 브랜드명 4건(biba/kookie/allen/babyhug)으로 축소하고 상위 카테고리명(women/men/kids)은 제거했으나(상품명에 리터럴 포함되어 전제 불성립 + PRD 4.2 미확인 항목으로 남음) 점수는 그대로 유지 확정.
- **TC-PRODUCT-SEARCH-010**: Impact 4 / Likelihood 4 / Risk Score 16 — 검색 결과 신뢰성에 직접 영향을 주는 매칭 로직이며(Impact 4), 이번 REQ-PRODUCT-SEARCH-005 정정(2026-08-31)을 촉발한 실제 관찰 사례를 검증하는 TC로 아직 회귀 검증이 전혀 이루어지지 않은 신규 로직이라 결함 발생 가능성이 매우 높음(Likelihood 4). Risk Score 16으로 P0 기준(16~25)에 해당.
- **TC-PRODUCT-SEARCH-007**: Impact 2 / Likelihood 2 / Risk Score 4 — 페이지네이션 대신 스크롤로 노출되는 것은 UI/UX 방식의 문제로 영향은 제한적이며(Impact 2), `page-ui.md`에서 이미 검증된 동일 패턴(REQ-PAGE-UI-021)을 재사용하는 구조라 결함 발생 가능성도 낮음(Likelihood 2).
- **TC-PRODUCT-SEARCH-008**: Impact 3 / Likelihood 2 / Risk Score 6 — Enter 키로 검색이 실행되어 버리면 사용자 기대와 다른 화면 전환이 발생해 혼란을 줄 수 있으나 돋보기 아이콘 클릭이라는 대체 경로가 여전히 존재해 기능 자체는 사용 가능하며(Impact 3), 단일 키 입력 이벤트에 대한 단순한 조건 확인이라 결함 발생 가능성은 낮음(Likelihood 2).
- **TC-PRODUCT-SEARCH-009**: Impact 2 / Likelihood 2 / Risk Score 4 — 입력값 제한이 없다는 것은 이미 PRD상 확정된 사실을 재확인하는 성격이라 영향은 제한적이며(Impact 2), 단순 입력 필드 동작 확인 수준이라 결함 발생 가능성도 낮음(Likelihood 2).

## 사용자 확인 필요 사항

1. **TC-PRODUCT-SEARCH-006 테스트 데이터 선정 방식**: 카테고리명/브랜드명이면서 실제 상품명에는
   포함되지 않는 구체적인 키워드를 PRD에서 확정하지 않아, Preconditions/Test Steps에서 "실행 전
   실제 상품명 목록을 확인해 조건에 맞는 키워드를 선정한다"는 방식으로 작성했습니다. 이 방식이
   적절한지, 아니면 구체적인 키워드 예시를 미리 지정해 드리는 것이 나을지 확인 부탁드립니다.
   → **확인 완료(2026-08-22)**: 구체적 키워드로 확정됨 — 브랜드명 `biba`(BIBA), `kookie`(KOOKIE
   KIDS), `allen`(ALLEN SOLLY JUNIOR), `babyhug`(BABYHUG), 카테고리명 `TOPS`(Women > Tops).
   해당 키워드들을 TC-PRODUCT-SEARCH-006의 Preconditions/Test Steps에 구체적으로 명시하는 방식으로
   반영함(추상적 서술 제거).
2. **Priority 산정값 전반**: 위 "Priority 산정 근거"에 제시한 Impact/Likelihood 점수와 근거가
   적절한지 확인 부탁드립니다. 특히 TC-PRODUCT-SEARCH-001(P1, 검색 핵심 시나리오)과
   TC-PRODUCT-SEARCH-005(P1, 부분 일치 매칭 로직)의 P1 산정에 동의하시는지 확인 부탁드립니다.
   → **확인 완료(2026-08-22)**: TC-PRODUCT-SEARCH-001은 P0로 재산정 확정(Likelihood 3→4 상향,
   Risk Score 15→20). TC-PRODUCT-SEARCH-005는 기존 산정(Impact 4 / Likelihood 3 / Risk Score
   12 / P1) 그대로 적절함 확정 — 변경 없음.
3. **결함 의심 항목 섹션 부재**: `product-search.md` Feature PRD에는 "결함 의심"으로 표시된
   요구사항이 없어 별도 섹션을 두지 않았습니다. 이 판단이 맞는지 확인 부탁드립니다.
   → **확인 완료(2026-08-22)**: 판단이 맞음이 확정됨 — 변경 없음.
4. **REQ-PRODUCT-SEARCH-001/005/008 정정(2026-08-31)에 따른 TC-001/005/006 재검토**: 자동화
   구현 중 발견된 Production 사이트 검색 결과 불일치(상품명에 검색어가 없는 상품이 노출되는
   현상)를 사용자가 직접 재확인해 Feature PRD의 검색 매칭 규칙(REQ-PRODUCT-SEARCH-005)을
   "상품명 또는 하위 카테고리명 중 하나라도 일치하면 노출, 상위 카테고리명·브랜드명은 제외"로
   정정·재승인했습니다. 이에 따라 TC-PRODUCT-SEARCH-001의 Expected Result, TC-PRODUCT-SEARCH-006의
   Test Scenario/Preconditions/Test Steps/Expected Result 수정안과 신규 TC-PRODUCT-SEARCH-010
   (하위 카테고리명 substring 매칭, P0) 추가안을 제시했습니다.
   → **확인 완료(2026-08-31)**: 제시안 그대로 승인 — TC-001 Expected Result 수정, TC-006 재작성,
   TC-010(P0) 신규 추가 확정. TC-PRODUCT-SEARCH-005는 상품명 기준 substring 매칭 검증이라는
   기존 검증 목적이 여전히 유효해 변경 없음으로 확정.
5. **REQ-PRODUCT-SEARCH-005/008 2차 정정(2026-08-31)에 따른 TC-006 재검토**: TC-PRODUCT-SEARCH-006
   자동화 실행 결과 상위 카테고리명(women/men/kids) 3건이 실제로는 상품명에 리터럴로 포함되어
   있어 매칭됨을 발견, 사용자가 매칭 규칙을 다시 확인해 "브랜드명은 완전 일치·부분 일치 여부와
   무관하게 항상 매칭 대상에서 제외"로 명확화하고, 상위 카테고리명 매칭 여부는 PRD 4.2 미확인
   항목으로 남겼습니다. 이에 따라 TC-006을 브랜드명 4건(biba/kookie/allen/babyhug)만 검증하는
   것으로 재작성하는 수정안을 제시했습니다.
   → **확인 완료(2026-08-31)**: 제시안 그대로 승인 — TC-006을 브랜드명 4건만 검증하도록
   재작성(상위 카테고리명 3건 제거). TC-PRODUCT-SEARCH-001/005는 이번 2차 정정 대상이 아니며
   기존 서술과 모순 없어 변경 없음으로 재확인.
   **상위 카테고리명(Women/Men/Kids) 매칭 여부는 PRD `feature/product-search.md` 4.2절에
   미확인 항목으로 남아 있습니다.** 추후 이 항목이 REQ-PRODUCT-SEARCH-009 등으로 확정되면,
   확정된 내용에 따라 별도 TC 추가가 필요할 수 있습니다.

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-22 | 최초 작성 (승인완료된 Feature PRD `product-search.md`의 REQ-PRODUCT-SEARCH-001~008 기반 TC-PRODUCT-SEARCH-001~009 초안 작성) | 초안 |
| 2026-08-22 | 사용자 리뷰 피드백 반영 - TC-006 구체적 테스트 데이터 확정, TC-001 Priority P0 재산정, TC-005/결함 의심 섹션 부재 판단 확정 | 초안 |
| 2026-08-22 | 사용자 최종 승인 | 승인완료 |
| 2026-08-31 | 재승인 - Feature PRD REQ-PRODUCT-SEARCH-001/005/008 정정(검색 매칭 대상에 하위 카테고리명 추가, 브랜드명·상위 카테고리명만 제외)에 따라 TC-PRODUCT-SEARCH-001 Expected Result 수정, TC-PRODUCT-SEARCH-006 재작성(브랜드명·상위 카테고리명 제외 검증으로 범위 조정), TC-PRODUCT-SEARCH-010(하위 카테고리명 substring 매칭, P0) 신규 추가. TC-PRODUCT-SEARCH-005는 변경 없음 | 승인완료 |
| 2026-08-31 | 재승인(2차) - Feature PRD REQ-PRODUCT-SEARCH-005/008 재정정(브랜드명은 완전 일치 포함 항상 제외로 명확화, 상위 카테고리명 매칭 여부는 4.2 미확인 항목으로 이관)에 따라 TC-PRODUCT-SEARCH-006 테스트 데이터를 브랜드명 4개(biba/kookie/allen/babyhug)로 축소하고 Test Scenario/Expected Result를 브랜드명 제외 검증으로 조정. 상위 카테고리명(women/men/kids) 3건은 실제 사이트 데이터상 상품명에 리터럴 포함되어 전제가 성립하지 않고 REQ도 미확인으로 남겨 검증 근거가 없어 제거. TC-PRODUCT-SEARCH-001/005는 이번 2차 정정 대상(REQ-001 불변, REQ-005 일반화 표현이 기존 서술과 모순 없음)이 아니어서 변경 없음으로 재확인 | 승인완료 |
