---
문서유형: Automation Development Roadmap
상태: 승인완료   # 초안 | 승인완료
관련 Project PRD: project-prd.md
관련 Feature PRD: [feature/login-logout.md, feature/signup-delete-account.md, feature/top-navigation.md, feature/product-search.md, feature/cart.md, feature/product-detail.md, feature/page-ui.md]
관련 Automation Candidate 문서: [tc/automation-candidates/login-logout.md, tc/automation-candidates/signup-delete-account.md, tc/automation-candidates/top-navigation.md, tc/automation-candidates/product-search.md, tc/automation-candidates/cart.md, tc/automation-candidates/product-detail.md, tc/automation-candidates/page-ui.md]
관련 Automation Guide: docs/automation/AUTOMATION_GUIDE.md
최초 작성일: 2026-08-27
최근 변경일: 2026-09-02 (진행 현황 갱신 - CI 스케줄 트리거 확장 검증 완료 반영)
승인일: 2026-08-27
---

# ROADMAP - Automation Exercise QA 자동화 개발 Roadmap

## 1. 개요 및 범위

이 문서는 `qa-process` 프로젝트에서 자동화 대상으로 확정된 Test Case를 기반으로,
개발팀이 순서대로 실행할 수 있는 자동화 코드 개발 실행 계획을 정의한다.

**대상 정의**: 아래 조건을 모두 만족하는 TC만 이 Roadmap의 구현 대상 범위로 삼는다.

```
Candidate 문서(docs/tc/automation-candidates/{slug}.md) 상태 = 자동화대상확정
AND
QA Decision = Approved
```

**대상 Feature 및 확정 TC 수 총계**: `docs/tc/automation-candidates/` 하위 7개 문서
전체(login-logout, cart, page-ui, product-detail, product-search,
signup-delete-account, top-navigation)를 재조회한 결과, 7개 Feature 모두
`상태: 자동화대상확정`이며 아래와 같이 총 **76건**의 TC가 최종 자동화 대상으로 확정되어
있다.

| Feature | 확정(Approved) TC 수 |
|---|---|
| login-logout | 11 |
| signup-delete-account | 11 |
| top-navigation | 6 |
| product-search | 8 |
| cart | 13 |
| product-detail | 6 |
| page-ui | 21 |
| **합계** | **76** |

이 수치 중 product-search를 제외한 6개 Feature는 `AUTOMATION_GUIDE.md` 0.1절의
2026-08-27 스냅샷(13/11/21/6/11/6)과 항목별로 정확히 일치한다. product-search만
2026-08-31 재확정(TC-PRODUCT-SEARCH-001/006 재평가, TC-010 신규 승인)에 따라 스냅샷
당시 7건에서 8건으로 증가했으며, 이는 스냅샷 갱신 누락이 아니라 원본 TC 문서 자체가
재승인되어 발생한 정당한 변경이다(상세는 8절 리스크 항목 참조). 이 Roadmap의 대상
확정 근거는 스냅샷 재사용이 아니라, 아래 "2. 입력 문서 스냅샷"과 "8. 리스크 및 확인
필요 사항"에 기록한 대로 각 Candidate 문서와 원본 TC 문서를 직접 재조회하여 별도로
검증한 결과다.

**Out of Scope(이 Roadmap이 다루지 않는 범위)**:
- Shrimp Task 생성 및 세부 작업 분해 (별도 단계, 이 Roadmap 승인 이후 진행)
- 실제 자동화 코드 구현 (별도 단계)
- 자동화 코드의 언어/프레임워크/네이밍 등 구체적 작성 방식 — Source of Truth는
  `docs/automation/AUTOMATION_GUIDE.md`이며 이 문서는 "무엇을 어떤 순서로 만들 것인가"만
  다룬다.

## 2. 입력 문서 스냅샷

| 문서 | 상태 | 최근 변경일 |
|---|---|---|
| prd/project-prd.md | 승인완료 | 2026-08-22 |
| prd/feature/login-logout.md | 승인완료 | 2026-08-20 |
| prd/feature/signup-delete-account.md | 승인완료 | 2026-08-20 |
| prd/feature/top-navigation.md | 승인완료 | 2026-08-21 |
| prd/feature/product-search.md | 승인완료 | 2026-08-31 (재승인) |
| prd/feature/cart.md | 승인완료 | 2026-08-21 |
| prd/feature/product-detail.md | 승인완료 | 2026-08-21 |
| prd/feature/page-ui.md | 승인완료 | 2026-08-22 |
| tc/login-logout.md | 승인완료 | 2026-08-22 |
| tc/signup-delete-account.md | 승인완료 | 2026-08-22 |
| tc/top-navigation.md | 승인완료 | 2026-08-22 |
| tc/product-search.md | 승인완료 | 2026-08-31 (재승인) |
| tc/cart.md | 승인완료 | 2026-08-22 |
| tc/product-detail.md | 승인완료 | 2026-08-22 |
| tc/page-ui.md | 승인완료 | 2026-08-22 |
| tc/automation-candidates/login-logout.md | 자동화대상확정 | 확정일 2026-08-24 |
| tc/automation-candidates/signup-delete-account.md | 자동화대상확정 | 확정일 2026-08-27 |
| tc/automation-candidates/top-navigation.md | 자동화대상확정 | 확정일 2026-08-27 |
| tc/automation-candidates/product-search.md | 자동화대상확정 | 확정일 2026-08-31 (재확정) |
| tc/automation-candidates/cart.md | 자동화대상확정 | 확정일 2026-08-24 |
| tc/automation-candidates/product-detail.md | 자동화대상확정 | 확정일 2026-08-27 |
| tc/automation-candidates/page-ui.md | 자동화대상확정 | 확정일 2026-08-24 |
| automation/AUTOMATION_GUIDE.md | 승인완료 | 2026-08-27 |

**재확인 결과(Workflow 2단계)**: 7개 Candidate 문서의 "Approved TC 목록(자동화 대상 확정)"에
기재된 TC ID 전건(75건)이 각 원본 TC 문서(`docs/tc/{slug}.md`)에 실제로 존재함을
grep으로 재확인했고, 7개 원본 TC 문서 모두 여전히 `상태: 승인완료`이며, 각 Candidate
문서의 "대상 TC 문서 최근 변경일(평가 시점 기준)"(전 Feature 공통 2026-08-22)이 현재
원본 TC 문서의 "최근 변경일"과 정확히 일치해 평가 이후 원본 TC가 변경된 사실이 없음을
확인했다. 불일치는 발견되지 않았다(상세는 8절 참조).

**2026-08-31 부분 개정 관련 추가 확인**: 위 "재확인 결과(Workflow 2단계)" 문단은 2026-08-27
시점 기준이며, product-search Feature는 이후 2026-08-31 REQ-PRODUCT-SEARCH-005 정정에
따라 TC-PRODUCT-SEARCH-001(Expected Result 수정)/006(재작성)/010(신규 추가)이
재승인·재확정되었다. 이번 부분 개정에서 product-search Candidate 문서와 원본 TC 문서를
다시 대조한 결과, Approved TC 8건(001~006, 008, 010) 전건이 `docs/tc/product-search.md`에
실제로 존재하고 해당 문서가 여전히 `상태: 승인완료`이며, Candidate 문서의 "대상 TC 문서
최근 변경일(평가 시점 기준)"(2026-08-31)이 원본 TC 문서의 "최근 변경일"(2026-08-31)과
정확히 일치함을 확인했다(불일치 없음). 다른 6개 Feature는 이번 변경과 무관하므로
재검증 대상이 아니다.

## 3. 기술 스택 및 아키텍처 (Reference)

`AUTOMATION_GUIDE.md` 1~4절 요약이며, 상세 규칙은 원본 문서를 기준으로 한다.

- 언어/도구: Python + Selenium WebDriver + pytest, 리포팅은 pytest-html(HTML) +
  JUnit XML(`--junitxml`) 병행. 브라우저는 Chrome(ChromeDriver). 대상 환경은 Production
  단일 환경(`https://automationexercise.com/`).
- 코딩 스타일: PEP8 예외 적용(4칸 들여쓰기, snake_case) — 전역 CLAUDE.md의 2칸/camelCase
  규칙에 대한 Python 자동화 코드 한정 예외(사용자 승인 완료).
- 아키텍처: Page Object Model(POM). 화면 단위 1 Page 클래스, 모든 Page는 `BasePage` 상속.
  Page Layer는 조작/조회만 담당(Assertion 없음), Test Layer가 Assertion을 전담.
- 디렉터리 구조(예정): `automation/pages`, `automation/tests`, `automation/utils`,
  `automation/config`, `automation/test_data`, `automation/screenshots`(git 미추적),
  `automation/reports`(git 미추적), `automation/conftest.py`, `automation/pytest.ini`,
  `automation/requirements.txt`.
- 테스트 데이터: 로그인 상태가 필요한 시나리오는 고정 계정 3개(`actest1~3@test.com`,
  이메일은 `test_data/accounts.json`, 비밀번호는 `.env`) 재사용. 회원가입/계정삭제처럼
  계정 자체를 생성·삭제하는 시나리오는 `utils`의 Factory 함수로 임의 이메일 동적 생성.

## 4. 구현 순서 결정 기준

**1순위: 기능적 의존성**
- 로그인 상태가 필요한 시나리오(장바구니 체크아웃 진입, 상단 네비게이션 로그인 상태
  메뉴, Checkout 페이지 UI 등)가 다수 존재하므로, 로그인/로그아웃(LoginPage 및 인증
  상태 확보)이 다른 모든 Feature의 전제 조건이 된다.
- 장바구니에 상품이 담긴 상태가 필요한 시나리오(Checkout 진입, page-ui의 Checkout/Cart
  비어있지 않은 상태 UI)가 있으므로, Cart의 핵심 담기/조회 메커니즘이 page-ui의 일부
  TC보다 먼저 준비되어야 한다.
- "Add to Cart" 확인 모달은 `cart.md`(REQ-CART-001)가 원 정의이며 `product-detail.md`가
  이를 참조·재사용한다고 PRD/Candidate 문서에 명시되어 있으므로, 공유 컴포넌트의 중복
  정의를 피하기 위해 cart를 product-detail보다 먼저 구현한다.
- 회원가입/계정삭제는 로그인 페이지(`/login`)의 "New User Signup!" 영역에서 시작되므로
  로그인/로그아웃과 동일한 화면(LoginPage)을 공유한다. 다른 Feature를 기능적으로 막지는
  않지만, Page Object 재사용 효율을 위해 로그인/로그아웃 바로 다음에 배치한다.

**2순위: Priority / Business Criticality / Automation Score**
- 기능적 의존관계가 동등한 Feature 사이에서는 Candidate 문서의 Business Criticality/
  Automation Score, 그리고 원본 TC의 Priority(P0 비중)를 참고해 순서를 정한다. 다만
  점수만으로 기계적으로 정하지 않고, Feature 간 결합도(공용 Page Object 재사용 가능성)를
  함께 고려한다.
- 상품 검색(product-search)은 로그인/장바구니 상태와 무관하게 독립적으로 수행 가능한
  Feature이며, Products 페이지 검색 결과 카드가 page-ui의 ALL PRODUCTS 그리드 카드 구조를
  참조하지만 이는 완전한 선행 조건은 아니므로(별도 Risk Coverage), 로그인 이후 이른
  시점에 독립적으로 배치한다.
- 각 페이지별 UI(page-ui)는 21건으로 대상 TC 수가 가장 많고 Home/Products/Cart/
  Signup-Login/Checkout 5개 화면을 모두 다루지만, 그중 다수(Checkout 관련 TC-025~039 등)가
  "로그인 + 장바구니에 상품이 담긴 상태"라는 다른 Feature의 산출물을 전제로 하므로 순서상
  가장 나중에 배치한다. 이렇게 하면 이전 Phase에서 이미 만들어진 HomePage/ProductsPage/
  CartPage/LoginPage/CheckoutPage Page Object를 그대로 확장해 재사용할 수 있다.

## 5. Phase별 Roadmap

### Phase 0: 공통 기반 구축 (Foundation)

- 산출물: `automation/` 디렉터리 구조 생성(pages/tests/utils/config/test_data/
  screenshots/reports), `BasePage`(공통 요소 탐색·클릭·입력·Wait 래핑 메서드),
  `conftest.py`(WebDriver fixture, function scope), `config/`(Base URL, 타임아웃 등),
  `test_data/accounts.json` 템플릿, `.env` 템플릿(비밀번호 등 민감정보 자리, 실제 값은
  커밋하지 않음), `requirements.txt`, `pytest.ini`.
- 근거: AUTOMATION_GUIDE 2, 3, 9, 11, 12절.
- 이 Phase가 끝나야 이후 모든 Feature Phase가 시작 가능하다(모든 Page 클래스가
  `BasePage`를 상속하고, 모든 테스트가 `driver` fixture를 사용).

### Phase 1: 로그인 / 로그아웃 (login-logout) 자동화 구현

- 대상 TC: 11건 (TC-LOGIN-LOGOUT-001, 002, 003, 004, 005, 006, 010, 011, 013, 014, 015)
- 필요 Page Object: `LoginPage`(로그인 폼 조작/에러 메시지 조회, "New User Signup!" 영역
  진입점 포함), `HomePage`(로그인 성공 후 랜딩 확인용 최소 골격)
- 선행 조건(의존 Feature): 없음 (Phase 0 완료 후 최우선 착수)
- 우선순위 근거: 장바구니 체크아웃 진입, 상단 네비게이션 로그인 상태 메뉴, page-ui의
  Checkout 화면 등 다른 다수 Feature의 TC가 "로그인 상태"를 전제 조건으로 요구하므로
  기능적 의존성상 최우선. Business Criticality도 최상위(다수 TC가 Score 25~26, P0 다수
  포함 — 로그인 Happy Path, 로그아웃 핵심 동작 등).

### Phase 2: 회원가입 / 계정삭제 (signup-delete-account) 자동화 구현

- 대상 TC: 11건 (TC-SIGNUP-DELETE-ACCOUNT-001, 002, 004, 005, 006, 007, 010, 011, 012,
  013, 014)
- 필요 Page Object: `SignupPage`(상세 정보 입력 페이지 `/signup`), `AccountCreatedPage`
  (`/account_created` 완료 화면), `AccountDeletedPage`(`/delete_account` 완료 화면),
  `LoginPage` 확장(Phase 1에서 만든 클래스의 "New User Signup!" 섹션 메서드 재사용/보강)
- 선행 조건(의존 Feature): login-logout — 같은 `/login` 화면(LoginPage)에서 회원가입
  플로우가 시작되고, 삭제된 계정 재로그인 검증(TC-SIGNUP-DELETE-ACCOUNT-013)이 Phase 1의
  로그인 에러 메시지 검증 로직을 재사용한다.
- 우선순위 근거: LoginPage를 공유하는 화면이라 Page Object 재사용 효율이 높고, 회원가입/
  계정삭제 Happy Path가 다수 P0(Score 25~26)로 Business Criticality가 매우 높다. 이후
  Phase에서 필요한 "동적 계정 생성" Factory 유틸리티(11.2절)도 이 Phase에서 함께 마련된다.
- **[Phase 1 인수 사항]** Phase 1에서 구현된 `LoginPage.click_new_user_signup()`(automation/pages/login_page.py)은
  "New User Signup!" 제목(h2) 영역을 클릭하는 구조로 구현되어 있으나, 실측 결과 해당 h2에는
  클릭 핸들러가 없어 클릭 자체가 실질적 효과가 없다(automation-developer-agent 2026-08-29
  보고, Playwright MCP 실측 기반). Phase 1의 Approved TC는 이 메서드를 요구하지 않아 Phase 1
  범위에서는 문제가 없었지만, 이 Phase(회원가입)는 실제로 Name/Email 입력 후 Signup 버튼을
  클릭해 `/signup`으로 진입해야 하므로, 이 메서드를 그대로 재사용하지 말고 signup-form의
  Name/Email 입력 필드와 Signup 버튼(Task 2 구현 시 확인된 data-qa 속성 후보: signup-name,
  signup-email, signup-button)을 사용하는 방식으로 재작업이 필요하다. 실제 재작업 여부와
  구체적 구현은 Phase 2 착수 시점에 automation-developer-agent가 재확인 후 진행한다.

### Phase 3: 상단 네비게이션 (top-navigation) 자동화 구현

- 대상 TC: 6건 (TC-TOP-NAVIGATION-001~006)
- 필요 Page Object: `HomePage`/`ProductsPage`/`CartPage`의 네비게이션 관련 메서드
  확장(메뉴 클릭, 이동 URL 확인, "Logged in as {유저명}" 조회, 활성 표시 조회)
- 선행 조건(의존 Feature): login-logout — 로그인 상태/로그아웃 상태 각각에서 메뉴 구성
  일관성(REQ-TOP-NAVIGATION-005)과 "Logged in as {유저명}" 표시(REQ-TOP-NAVIGATION-006)를
  검증하려면 Phase 1에서 확보한 로그인/로그아웃 상태 전환 메커니즘이 선행되어야 한다.
- 우선순위 근거: 기능적 의존성(로그인 상태 필요) 외에, 이 Phase에서 확장하는 HomePage/
  ProductsPage/CartPage의 기본 네비게이션 메서드는 이후 product-search/cart/product-detail/
  page-ui Phase에서 공통으로 재사용되므로 이른 시점에 배치해 결합도 높은 공용 Page Object를
  먼저 안정화한다.

### Phase 4: 상품 검색 (product-search) 자동화 구현

- 대상 TC: 8건 (TC-PRODUCT-SEARCH-001, 002, 003, 004, 005, 006, 008, 010) —
  **[2026-08-31 재승인 반영]** 기존 7건(001~006, 008)에서 TC-010(하위 카테고리명
  substring 매칭, P0)이 신규 추가되어 8건으로 확대. TC-001(Expected Result 확장 —
  상품명 또는 하위 카테고리명 매칭)과 TC-006(검증 방향 반전 — 하위 카테고리명은 매칭
  대상, 브랜드명·상위 카테고리명만 제외)도 시나리오가 변경되었으므로, 이미 작성된
  TC-001 테스트 코드는 새 Expected Result 기준으로 재작업이 필요하다(자동화 구현
  Agent 판단·처리 영역).
- 필요 Page Object: `ProductsPage` 확장(검색창 입력, 검색 실행, 검색 결과 카드/제목/URL
  조회). 신규 TC-010은 하위 카테고리명 매칭 결과 상품이 노출되는지 확인하는
  시나리오로, 기존에 정의된 검색 결과 카드 조회 메서드로 충분한지 또는 추가 조회
  메서드가 필요한지는 구현 단계(자동화 구현 Agent)에서 판단한다(이 Roadmap 문서는
  대상 범위만 갱신).
- 선행 조건(의존 Feature): 없음 (로그인/로그아웃 상태와 무관하게 수행 가능한 독립
  Feature). 다만 Phase 3에서 이미 만들어진 `ProductsPage` 기본 골격을 확장하는 형태로
  구현한다.
- 우선순위 근거: 기능적으로 다른 Feature를 막지 않는 독립 Feature이므로, 로그인 관련
  기반(Phase 1~3)이 갖춰진 직후 낮은 결합도의 Feature부터 처리한다. 검색 실행/URL 변경/
  매칭 로직 등 다수 TC가 결정적 판정이 가능하고 Score 20~23 수준으로 중요도가 있다.

### Phase 5: 장바구니 (cart, 상품 담기 포함) 자동화 구현

- 대상 TC: 13건 (TC-CART-001, 002, 003, 004, 005, 006, 008, 009, 010, 011, 014, 015, 016)
- 필요 Page Object: `CartPage`(장바구니 목록/삭제/빈 카트 상태), `AddToCartModal`
  (Home/Products 리스트 페이지 공용 담기 확인 모달 — 이후 product-detail Phase가 재사용할
  공유 컴포넌트로 이 Phase에서 최초 정의), `CheckoutPage`(로그인 요구 모달 및 `/checkout`
  기본 골격), `HomePage`/`ProductsPage`의 "Add to cart" 메서드 확장
- 선행 조건(의존 Feature): login-logout — "Proceed To Checkout" 클릭 시 로그인 상태별
  분기(REQ-CART-008/009), 로그인/로그아웃 상태에 따른 장바구니 병합·복원 동작
  (TC-CART-014~016) 검증에 Phase 1의 로그인/로그아웃 메커니즘이 필요하다.
- 우선순위 근거: Business Criticality가 매우 높은 TC(수량/합계 계산, 체크아웃 진입,
  로그인 상태별 데이터 정합성 등 다수 Score 24~26)가 다수 포함되어 있고, "Add to Cart"
  확인 모달의 원 정의를 담당하는 Feature이므로 이를 재사용하는 product-detail보다
  먼저 구현한다.

### Phase 6: 상품 상세 (product-detail) 자동화 구현

- 대상 TC: 6건 (TC-PRODUCT-DETAIL-001, 002, 008, 015, 016, 021)
- 필요 Page Object: `ProductDetailPage`(신규) — Quantity 입력/스피너, Add to cart 버튼,
  가격/카테고리 등 조회 메서드. "Add to cart" 확인 모달은 Phase 5에서 정의한
  `AddToCartModal`을 재사용(신규 정의하지 않음).
- 선행 조건(의존 Feature): cart — REQ-PRODUCT-DETAIL-016이 참조하는 담기 확인 모달은
  cart Feature(REQ-CART-001)가 원 정의이므로, Page Object 중복 정의를 피하려면 cart
  Phase 이후에 진행한다. login-logout에는 기능적으로 의존하지 않는다(비로그인 상태에서도
  상세 페이지 접근/담기 가능).
- 우선순위 근거: URL 패턴(진입점, Score 23), 정상 진입 스모크 테스트(Score 25), Add to
  cart 모달 재검증(Score 23) 등 중요도가 있으나, cart의 모달 정의에 의존하는 결합 관계상
  cart 다음으로 배치한다.

### Phase 7: 각 페이지별 UI (page-ui) 자동화 구현

- 대상 TC: 21건 (TC-PAGE-UI-006, 009, 015, 019, 020, 021, 023, 024, 025, 026, 028, 029,
  030, 031, 032, 033, 034, 035, 036, 037, 039)
- 필요 Page Object: `HomePage`/`ProductsPage`(배너·캐러셀, CATEGORY/BRANDS 아코디언,
  FEATURES ITEMS/ALL PRODUCTS 그리드, RECOMMENDED ITEMS 캐러셀 조회 메서드 확장),
  `CartPage`(빈 카트 안내, Proceed To Checkout 버튼, 상품 목록 표 컬럼 조회 확장),
  `CheckoutPage`(Address Details, Review Your Order, Total Amount, Place Order 버튼 조회
  확장 — Phase 5에서 만든 골격을 확장), `CategoryProductsPage`/`BrandProductsPage`(신규,
  카테고리/브랜드 필터링 결과 페이지)
- 선행 조건(의존 Feature): login-logout, cart — Checkout 관련 다수 TC(034~037, 039 등)는
  "로그인 상태 + 장바구니에 상품이 담긴 상태"에서 `/checkout` 페이지에 진입해야 확인
  가능하므로, 두 Feature의 Page Object/메커니즘이 이미 준비되어 있어야 효율적으로
  구현·재사용할 수 있다.
- 우선순위 근거: 대상 TC 수가 21건으로 가장 많지만, Home/Products/Cart/Signup-Login/
  Checkout 5개 화면을 모두 다루는 넓은 범위이며 다수 TC가 이미 다른 Phase에서 구축된
  Page Object의 확장으로 구현 가능하다. 따라서 공용 Page Object 재사용을 극대화하기 위해
  가장 마지막 Feature Phase로 배치한다.

### Phase Final: CI/CD 및 Slack 알림 연동

- 산출물: `.github/workflows/` 워크플로우(Push 시 자동화 테스트 실행 → 리포트 생성 →
  결과 판정), Slack 실패 알림 스크립트(JUnit XML 파싱, 실패 테스트명/사유 요약 포함)
- 근거: AUTOMATION_GUIDE 16절, CLAUDE.md 15/16절.
- 이 Phase는 Phase 1~7에서 생성된 자동화 테스트 스위트가 최소 1회 이상 로컬에서
  PASSED/FAILED로 실행 검증된 이후 착수한다.
- **[2026-08-31 명확화]** 이 검증은 AUTOMATION_GUIDE 20.1절이 정의하는 **전체
  통합테스트(Full Regression)**에 해당하며, Phase 1~7 전체를 통틀어 이 시점에 **1회만**
  수행한다. Phase 1~7 각각의 완료 시점(7절 Definition of Done)에는 해당 Phase 범위로
  한정한 테스트만 실행하며, 개별 Phase가 완료될 때마다 다른 Phase를 포함한 전체
  통합테스트를 반복 수행하지 않는다.

## 6. Feature별 상세 매핑표

| Feature | 확정 TC 수 | 대상 TC ID | 필요 Page Object | 의존 Feature | Phase |
|---|---|---|---|---|---|
| login-logout | 11 | TC-LOGIN-LOGOUT-001, 002, 003, 004, 005, 006, 010, 011, 013, 014, 015 | LoginPage, HomePage(골격) | 없음 | Phase 1 |
| signup-delete-account | 11 | TC-SIGNUP-DELETE-ACCOUNT-001, 002, 004, 005, 006, 007, 010, 011, 012, 013, 014 | SignupPage, AccountCreatedPage, AccountDeletedPage, LoginPage(확장) | login-logout | Phase 2 |
| top-navigation | 6 | TC-TOP-NAVIGATION-001~006 | HomePage/ProductsPage/CartPage(네비게이션 확장) | login-logout | Phase 3 |
| product-search | 8 | TC-PRODUCT-SEARCH-001, 002, 003, 004, 005, 006, 008, 010 | ProductsPage(검색 확장) | 없음 | Phase 4 |
| cart | 13 | TC-CART-001, 002, 003, 004, 005, 006, 008, 009, 010, 011, 014, 015, 016 | CartPage, AddToCartModal, CheckoutPage(골격), HomePage/ProductsPage(Add to cart 확장) | login-logout | Phase 5 |
| product-detail | 6 | TC-PRODUCT-DETAIL-001, 002, 008, 015, 016, 021 | ProductDetailPage(신규), AddToCartModal(재사용) | cart | Phase 6 |
| page-ui | 21 | TC-PAGE-UI-006, 009, 015, 019, 020, 021, 023, 024, 025, 026, 028, 029, 030, 031, 032, 033, 034, 035, 036, 037, 039 | HomePage/ProductsPage/CartPage/CheckoutPage(확장), CategoryProductsPage, BrandProductsPage(신규) | login-logout, cart | Phase 7 |

## 7. Definition of Done

각 Feature Phase는 다음을 모두 충족해야 완료로 간주한다.

- AUTOMATION_GUIDE 20.1절 기준으로, Phase 내부에서는 코드 작성 단위(Task)마다 관련
  테스트를 실행했고, Phase 코드 작성 완료 시점에는 **해당 Phase 범위로 한정한** pytest를
  실제로 실행해 PASSED/FAILED/ERROR 결과를 확인했는가 (실행 없이 "완료"로 간주하지 않음).
  다른 Phase를 포함한 전체 통합테스트는 각 Phase 완료 시점의 Definition of Done에
  포함되지 않으며, Phase Final 착수 직전에 1회만 수행한다(5절 Phase Final 참고).
- AUTOMATION_GUIDE 21절 Self Review 체크리스트(Explicit Wait 사용, Full XPath 미사용,
  Locator 상수화, Page Layer에 Assertion 없음, `BasePage` 상속, 테스트 독립성, 민감정보
  미하드코딩, `logging` 사용, 구체적 예외 처리, Naming Convention, 4칸 들여쓰기, 실패 시
  스크린샷 저장, 신규 Locator의 Playwright MCP 검증)를 모두 충족했는가.
- 코드 리뷰가 완료되었는가(CLAUDE.md 3절 워크플로우 7단계, Roadmap Agent의 책임 범위
  밖이며 후속 리뷰 단계에서 수행).
- 테스트 실패가 발생한 경우 원인을 Automation Code / Test Data / Test Environment / 실제
  Product 문제 중 하나로 구분하려 시도했으며, 불명확한 경우 추측으로 결론짓지 않고
  사용자에게 보고했는가.

## 8. 리스크 및 확인 필요 사항

**검증 결과 요약**: 7개 Candidate 문서와 7개 원본 TC 문서를 전수 재조회한 결과, 아래와
같이 **불일치나 결함은 발견되지 않았다.**

- TC ID 유효성: 75건의 Approved TC ID 전건이 각 원본 TC 문서에 실제로 존재함을 grep으로
  재확인했다.
- 원본 TC 문서 상태: 7개 문서 모두 여전히 `상태: 승인완료`이다.
- 원본 TC 변경 여부: 7개 Candidate 문서의 "대상 TC 문서 최근 변경일(평가 시점 기준)"이
  모두 2026-08-22이며, 현재 원본 TC 문서의 "최근 변경일"과 정확히 일치해 평가 이후 원본이
  변경된 사실이 없다.
- 관련 Feature PRD 7건 모두 `상태: 승인완료`이다.
- `AUTOMATION_GUIDE.md` 0.1절 스냅샷(13/11/21/6/7/11/6)과 이번 재조회 결과가 Feature별로
  정확히 일치해, 스냅샷 이후 자동화 대상 범위에 드리프트가 없음을 확인했다(단, 이 일치는
  스냅샷을 신뢰해 도출한 것이 아니라 별도 재조회로 검증한 결과다).

**사용자 확인이 필요한 판단 사항(이 Roadmap 초안에서 에이전트가 판단해 제안한 내용)**:

1. **Phase 순서 판단**: PRD/Candidate 문서에 "Feature 구현 순서" 자체가 명시적으로
   정의되어 있지 않으므로, 4절에 기술한 기능적 의존성(로그인 필요 여부, Add to Cart 모달
   공유 관계 등)과 Page Object 재사용 효율을 근거로 에이전트가 Phase 1~7 순서를
   판단했다. 특히 다음 두 가지는 PRD에 명시된 필수 순서가 아니라 에이전트의 구현 효율
   판단이므로 사용자 검토가 필요하다.
   - signup-delete-account를 top-navigation보다 먼저 배치(LoginPage 공유에 따른 재사용
     효율 근거, 기능적 강제 의존은 아님).
   - cart를 product-detail보다 먼저 배치(Add to Cart 모달의 원 정의 Feature를 먼저
     구현해 중복 정의를 피하려는 근거, 기능적 강제 의존은 아님 — product-detail 단독으로도
     구현 자체는 가능함).
2. **Cross-Feature 중복/참고 항목**: Candidate 문서 자체에 이미 기록되어 있던 사항이며
   이 Roadmap에서 새로 발견한 문제는 아니지만, 참고로 안내한다.
   - `page-ui.md` TC-PAGE-UI-040/041은 `cart.md` TC-CART-012/013과 검증 목적이 사실상
     동일해 두 문서 모두 QA Decision: Rejected로 일관되게 정리되어 있다(자동화 대상에서
     이미 제외됨, 조치 불필요).
   - `product-search.md` TC-PRODUCT-SEARCH-002(검색 결과 카드 구성)는 `page-ui.md`
     TC-PAGE-UI-015(ALL PRODUCTS 그리드 카드 구성)와 동일한 카드 컴포넌트를 검증하지만
     별도 Risk Coverage(검색 필터링 경로)로 판단되어 둘 다 Approved로 확정되어 있다.
     Page Object 관점에서는 두 TC가 동일한 상품 카드 Locator를 공유하게 되므로, 구현 단계
     (Shrimp Task 분해 이후)에서 중복 Locator 정의가 발생하지 않도록 유의가 필요하다는
     점만 참고로 남긴다(이 Roadmap 문서 자체의 범위 밖).
3. **[Phase 1 구현 중 발견, 2026-08-29 추가] LoginPage.click_new_user_signup() Phase 2 재작업
   필요 가능성**: Phase 1 Task 2(LoginPage 구현) 실측 결과 "New User Signup!" 클릭 메서드가
   실질적 효과가 없는 구조로 확인되었다. 5절 Phase 2 항목에 인수 사항으로 기록해두었으며,
   Phase 2 착수 시 실제 재작업 필요 여부를 다시 판단한다(현재는 사용자에게 미리 알리는
   목적의 예고 기록이며, 이 자체가 Roadmap의 Phase 순서나 범위를 변경하지는 않는다).

## 9. 진행 현황 (구현 단계)

이 절은 Roadmap 승인 이후 실제 구현 진행 상황을 사용자가 한눈에 확인할 수 있도록 기록하는
스냅샷이다. **Source of Truth는 항상 Repository Code와 Shrimp Task 상태이며(CLAUDE.md 8절),
이 표는 그 결과를 요약해 옮겨 적은 것일 뿐 판단 기준 자체가 아니다.** 실제 구현 상태와 이
표가 다르게 보이면 Repository Code를 기준으로 한다.

| Phase | Feature | 상태 | 비고 |
|---|---|---|---|
| Phase 0 | 공통 기반 구축 | 완료 | 2026-08-27, 커밋 `790ff26` |
| Phase 1 | login-logout | 완료 | Approved TC 11건 전건 pytest PASSED, 코드 리뷰 반영 완료, 커밋 `ae6ba0c`, `origin/master`(https://github.com/Matthaeus888/qa-process) push 완료 |
| Phase 2 | signup-delete-account | 완료 | Approved TC 11건 전건 pytest PASSED, 코드 리뷰 반영 완료(finding 4건 수정, 재검증 과정에서 발견한 자체 회귀 1건도 재수정), 커밋 `a4f0825`, `origin/master` push 완료. 구현 중 실제 사이트 동작이 TC-006 승인 내용과 달라(Continue 클릭 시 자동 로그인됨) 사용자 확인 후 TC/PRD 문서 갱신. Production 사이트의 제3자 광고 오버레이 방해 문제를 발견해 BasePage 방어 로직 추가 및 AUTOMATION_GUIDE 7.1절 신규 문서화(일부 극단적 클릭 차단 사례는 알려진 한계로 잔존, conftest.py 광고 도메인 차단은 사용자 결정으로 보류) |
| Phase 3 | top-navigation | 완료 | Approved TC 6건 전건 pytest PASSED, 코드 리뷰 반영 완료(finding 10건 중 correctness/견고성 4건 수정 — click_and_retry_if_vignette() 경쟁 조건 수정, 광고 방어 누락 3곳 보강, Locator 스코핑 일관성 정리, 미사용 죽은 코드 3개 제거), 커밋 `ece59d7`, `origin/master` push 완료. ProductsPage/CartPage 신규 구현 과정에서 페이지마다 로고/모달/브레드크럼으로 인한 중복 href를 실측으로 발견해 개별 대응. TC-006은 원본 TC의 외부 정보 의존(재사용 계정의 최초 가입 Name) 대신 Phase 2 회원가입 플로우 재사용으로 자기완결적으로 재설계. Phase 1+2+3 결합 회귀 28건 중 코드 자체의 진짜 실패는 0건이며, 제3자 광고발 브라우저 세션 크래시가 이례적으로 높은 빈도로 관측되어 사용자 확인 후 현재 코드로 완료 처리(AUTOMATION_GUIDE 7.1절 알려진 한계) |
| Phase 4 | product-search | 완료 | Approved TC 8건(001,002,003,004,005,006,008,010) 전건 pytest PASSED(TC-006은 브랜드명 4개 keyword parametrize, 총 실행 케이스 11개). **[2026-08-31 구현 중 PRD/TC 2차 재승인 발생]** 자동화 구현 중 실제 사이트 검색 매칭 로직이 승인된 PRD/TC와 달라 PRD(REQ-PRODUCT-SEARCH-001/005/008)를 2차례 재정정하고(① 하위 카테고리명 매칭 추가, ② 브랜드명은 완전 일치도 항상 제외로 명확화·상위 카테고리명은 4.2 미확인 항목으로 이관) TC-001 Expected Result 수정, TC-006을 브랜드명 4건만 검증하도록 재작성, TC-010(하위 카테고리명 매칭 회귀 테스트) 신규 추가 — 모두 사용자 직접 승인, Candidate 문서도 재확정 완료(Score 재산정 포함). TC-005는 assertion 방향이 반대로 작성된 코드 버그도 발견해 수정(승인 불필요, 코드 전용). Phase 1~4 전체 회귀(39건) 확인 중 Phase 4와 무관한 Phase 1 회귀 1건(TC-LOGIN-LOGOUT-015, `/logout` 직접 접근 시 Home으로 랜딩)을 발견해 AUTOMATION_GUIDE 22절에 알려진 Production 사이트 결함으로 문서화. 구현 커밋 `a457ce2` 완료 후 `/code-review`로 코드 리뷰를 실행해 finding 4건을 발견 — 경쟁 조건(URL 변경 대기 직후 상품 그리드 렌더링을 기다리지 않고 카드를 조회해 flaky 실패 가능성)과 동일 셀렉터 3회 중복 조회 2건은 `_wait_for_results_rendered()` 헬퍼 추가로 수정하고 재실행으로 회귀 없음(11건 PASSED) 확인, 커밋 `a81e9d3`. 나머지 2건(TC-001의 배제(exclusion) 조건 미검증, Enter 키 테스트의 비동기 반응 미대기)은 테스트 docstring에 이미 근거가 명시된 의도적 설계 결정으로 판단해 사용자 확인 후 알려진 제약사항으로 남기고 코드는 변경하지 않음. `origin/master` push 완료 확인(커밋 `a457ce2`, `a81e9d3`, `23bb387` 포함 `0f3fe24`까지 로컬/원격 일치) |
| Phase 5 | cart | 완료 | Approved TC 13건(001,002,003,004,005,006,008,009,010,011,014,015,016) 전건 pytest PASSED. CartPage 확장(목록/삭제/빈카트/Proceed To Checkout), AddToCartModal·CheckoutPage 신규(Phase 6 재사용 예정 공유 컴포넌트), HomePage/ProductsPage Add to cart 확장. `/code-review` 실행 결과 finding 7건 중 5건 수정(TC-011/014/015/016 `finally` 블록에서 cleanup 예외가 원래 assertion 실패를 가리던 문제, `base_page.py` click()/click_element() 클릭 재시도 로직 중복, 상품명 공백 정규화 로직 3중 중복(신규 `utils/text.py`로 통합), 장바구니 행 미발견 시 에러 로그용 DOM 재조회 1건), 2건은 검토 후 변경 보류(HomePage/ProductsPage 카드 Locator 중복 — Phase 1~3부터 이어진 "화면 단위 1 Page 클래스" 기존 설계와 일치해 유지, 리뷰어의 docstring 오독 1건은 실제로는 이미 정확히 기술되어 있어 수정 불필요). 수정 후 Phase 5 재실행 13/13 PASSED, `base_page.py` 공유 로직 변경 영향 확인을 위해 Phase 3(top-navigation) 6/6 PASSED spot-check도 재확인. 구현 커밋 `f3b7c6a`(코드 리뷰 반영 포함), push는 진행 중 |
| Phase 6 | product-detail | 완료 | Approved TC 6건(001,002,008,015,016,021) 전건 pytest PASSED. `ProductDetailPage` 신규 구현, `HomePage`에 View Product 링크 조작 추가, "Add to cart" 확인 모달은 `AddToCartModal`(Phase 5) 신규 정의 없이 재사용. `/code-review`(medium) 실행 결과 finding 2건 모두 수정 — `BasePage.click_and_retry_if_vignette()`가 신규 `click_and_retry_if_vignette_action()`과 로직이 중복돼 있던 것을 전자가 후자를 호출하도록 통합(AUTOMATION_GUIDE 19절 중복 코드 분리 원칙), `click_element()`가 광고 오버레이 제거로 인한 `StaleElementReferenceException`을 처리하지 않던 것을 명시적으로 로깅 후 재전파하도록 보강. 수정 후 Phase 6 재실행 6/6 PASSED, `base_page.py` 공유 로직 변경 영향 확인을 위해 Phase 2/3/5(로그인·회원가입·네비게이션·카트) 30건 spot-check도 재확인(전건 PASSED). TC-001 최초 구현 중 기존에 알려진 Google Vignette 광고 개입 패턴(AUTOMATION_GUIDE 7.1절)이 카드 index 기반 클릭에서도 재현되어 `BasePage`에 범용 재시도 헬퍼를 추가해 해결. 커밋 `ab652d6`, `origin/master` push 완료 확인(로컬/원격 일치) |
| Phase 7 | page-ui | 완료 | Approved TC 21건(006,009,015,019,020,021,023,024,025,026,028,029,030,031,032,033,034,035,036,037,039) 전건 pytest PASSED. `CategoryProductsPage`/`BrandProductsPage` 신규 구현, `HomePage`/`ProductsPage`(카드 상세/RECOMMENDED ITEMS 캐러셀/CATEGORY 아코디언)/`CartPage`(표 컬럼)/`CheckoutPage`(Address Details/Review Your Order/Total Amount/Place Order)/`ProductDetailPage`(카테고리/브랜드 텍스트 조회) 확장. TC-035(주소 자동 채움)는 고정 계정 대신 `utils/account_factory.py`로 자체 회원가입한 계정을 사용하는 자기완결적 방식으로 구현(Phase 3 TC-006 선례와 동일 논리). `/code-review`(medium) 실행 결과 finding 4건 모두 수정 — RECOMMENDED ITEMS 캐러셀 활성 상품명 비교 시 한쪽만 strip하던 비대칭 비교를 양쪽 다 strip하도록 통일(실측 결과 실제 DOM에 공백이 있어 처음 시도한 "양쪽 다 strip 안 함" 수정은 오히려 회귀를 유발해 재수정), `BasePage.wait_for_element_class_state()`가 class 속성이 없는 요소에서 크래시하던 문제를 방어 처리, HomePage/ProductsPage에 거의 동일하게 중복 구현돼 있던 CATEGORY 아코디언 클릭+재시도 로직(~90줄)을 `BasePage.click_and_wait_for_class_toggle()`로 통합하며 전용 타임아웃 상수(`CLASS_TOGGLE_TRANSITION_TIMEOUT`)로 분리(기존에는 의미가 다른 광고 오버레이 타임아웃을 재사용해 느린 환경에서 오탐 재클릭 위험이 있었음). 수정 후 Phase 7 재실행 21/21 PASSED, `base_page.py`/`home_page.py`/`products_page.py` 공유 로직 변경 영향 확인을 위해 Phase 1/3/5/6(로그인·네비게이션·카트·상품상세) 36건 spot-check도 재확인(전건 PASSED). 구현 중 Google Vignette 광고의 아코디언 토글 개입, `google-anno` 광고 주석 아티팩트가 Selenium 세션에서도 재현됨을 확인(기존 Playwright MCP 전용 추정이 틀렸음을 실측으로 확인), Checkout 표에 합계 행이 상품 행과 섞여 개수가 잘못 집계되던 문제, 고정 계정 장바구니 leftover 데이터 문제를 발견해 모두 수정. 커밋 `abd0b43`, `origin/master` push 완료 확인(로컬/원격 일치) |
| Phase Final | CI/CD 및 Slack 알림 연동 | Task 1~5 완료, CI 트리거 확장(스케줄+수동실행) 완료 | Shrimp Task 5건(9/1 계획) 전건 구현 완료. **Task 1** `automation/conftest.py`의 `driver` fixture에 `CI=true` 감지 시 headless(`--headless=new` 등) 분기 추가, headless/headed 각각 pytest 실행으로 회귀 없음 확인(headless 상태 `maximize_window()` 호출 시 800x600으로 축소되는 실측 결함을 발견해 CI 분기에서는 생략 처리). **Task 2** `.github/workflows/ci.yml` 신규 작성(master push 트리거, ubuntu-latest/Python 3.9, `pytest tests/` 실행 후 `always()`로 reports/screenshots를 upload-artifact) — automation-developer-agent가 "CI 연동은 담당 범위 밖"이라며 정당하게 반려(CLAUDE.md 6절 역할 분리)해 오케스트레이터가 직접 작성. **Task 3** `scripts/notify_slack/notify.py` 신규 작성(표준 라이브러리만 사용, JUnit XML 파싱 후 실패 시에만 Slack 전송). **Task 4** `ci.yml`에 Slack 알림 스텝 연결 — pseudocode의 `if: failure()`가 `run_tests`의 `continue-on-error: true`와 조합 시 절대 실행되지 않는 논리 오류가 됨을 발견해 `if: steps.run_tests.outcome == 'failure'`로 수정, GitHub Secret 4종(`ACTEST1_PASSWORD`/`ACTEST2_PASSWORD`/`ACTEST3_PASSWORD`/`SLACK_WEBHOOK_URL`) 등록 방법을 사용자에게 안내했고 2026-09-02 사용자가 4종 모두 등록 완료. **Task 5**: 사용자 승인 하에 Task 1~4 변경사항 커밋(`24c484d`) 및 push, 실제 GitHub Actions 실행(run `33597789576`)에서 79 passed/0 failed(328.43초, headless), Artifact(`test-reports`: `reports/results.xml`/`report.html`) 업로드까지 확인. Slack 알림 실전 검증을 위해 임시 실패 테스트를 추가해 커밋·push(run `33598394330`) → `Notify Slack on failure` 스텝 실행과 Slack Webhook HTTP 요청 성공(사용자가 실제 채널 도착도 확인) 확인. 이 과정에서 임시 테스트 외에 이미 문서화된 `/logout` 간헐적 결함(TC-LOGIN-LOGOUT-015)이 GitHub Actions headless 환경에서도 재현됨을 처음 확인해 `AUTOMATION_GUIDE.md` 22.1절에 사용자 승인 하에 기록. 사용자 요청으로 Slack 메시지에 실패 위치(파일:라인)를 명시하도록 `notify.py` 개선(커밋 `bc7921a`) 후 재검증(run `33599258272`)까지 완료. 임시 테스트 삭제 및 문서 갱신을 커밋(`f2165f8`)해 master 원상 복구. CI 트리거는 "master push만", 실행 범위는 "매 push마다 전체 실행"으로 확정했던 기존 결정에 더해, 2026-09-02 사용자 요청으로 "매일 KST 09:00 스케줄 + 수동 실행(workflow_dispatch)" 트리거를 추가(cron `0 0 * * *`는 UTC 기준, KST 09:00에 해당, 커밋 `9769f4a`). `workflow_dispatch`로 즉시 수동 실행(run `33600534407`)해 성공(7m25s)함으로써 신규 트리거 설정이 GitHub에 정상 등록·동작함을 확인했고, 같은 시점 push 트리거 실행(run `33600527284`)도 79 passed/0 failed로 성공해 임시 테스트 삭제 이후 회귀가 없음을 재확인. 실제 `schedule` 자동 실행은 다음날(2026-09-03) KST 09:00에 최초 발생 예정이며 이 세션에서는 직접 관측하지 못함(GitHub Actions 탭에서 추후 확인 가능) — 상세는 아래 변경 이력 참고 |

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-27 | 최초 작성. `docs/tc/automation-candidates/` 7개 문서 전체를 재조회하여 자동화대상확정 Feature 7개(login-logout, cart, page-ui, product-detail, product-search, signup-delete-account, top-navigation)를 확인하고, 원본 TC 문서와의 정합성(TC ID 존재, 승인완료 상태, 원본 변경 여부)을 재검증(불일치 없음). 관련 Feature PRD 7건 및 Project PRD를 확인해 기능적 의존성(로그인 필요 여부, Add to Cart 모달 공유 관계 등)을 근거로 Phase 1~7 순서를 판단해 초안 작성. 사용자 검토 대기 중. | 초안 |
| 2026-08-27 | 사용자가 8절에 기록된 판단 필요 사항 두 가지(1. signup-delete-account를 top-navigation보다 먼저 배치, 2. cart를 product-detail보다 먼저 배치)에 대해 "1,2번 승인"으로 동의. 이후 Roadmap 전체에 대한 최종 승인 여부를 별도로 재확인한 결과 사용자가 "네, 승인합니다"라고 명확한 최종 승인 의사를 밝힘. | 승인완료 |
| 2026-08-29 | 사용자 재승인에 따른 부분 갱신. Phase 1 Task 2(LoginPage 구현) 완료 후 automation-developer-agent가 보고한 리스크(`click_new_user_signup()`이 클릭 핸들러 없는 h2를 클릭하는 구조라 Phase 2에서 재작업이 필요할 수 있음)를 5절 Phase 2 항목과 8절 리스크 목록에 인수 사항으로 기록. Phase 순서/범위/Definition of Done 등 기존 내용은 변경하지 않음. | 승인완료 |
| 2026-08-30 | 사용자 요청에 따른 진행 현황 갱신. 9절 "진행 현황" 신규 추가 — Phase 0/1 완료(각각 커밋 `790ff26`/`ae6ba0c`, Phase 1은 GitHub `origin/master` push 완료 및 코드 리뷰 반영 포함)와 Phase 2~7 착수 전 상태를 기록. Phase Final(CI/CD)은 사용자 지시("모든 코드가 완성된 이후 진행")에 따라 보류로 명시. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-08-30 | 사용자 요청에 따른 진행 현황 갱신. Phase 2(signup-delete-account) 완료로 표시 — Approved TC 11건 전건 pytest PASSED, 코드 리뷰 반영, 커밋 `a4f0825` 및 `origin/master` push 완료. 구현 중 발견한 두 가지 특이사항(TC-006 실제 사이트 동작이 승인 내용과 달라 사용자 확인 후 TC/PRD 문서 갱신, Production 사이트 제3자 광고 오버레이 방해로 BasePage 방어 로직 추가 및 AUTOMATION_GUIDE 7.1절 신규 문서화)을 비고에 기록. Phase 3(top-navigation)을 다음 착수 대상으로 갱신. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-08-31 | 사용자 요청에 따른 진행 현황 갱신. Phase 3(top-navigation) 완료로 표시 — Approved TC 6건 전건 pytest PASSED, 코드 리뷰 반영(finding 10건 중 4건 수정: 경쟁 조건, 광고 방어 누락 3곳, Locator 스코핑 일관성, 미사용 코드 제거), 커밋 `ece59d7` 및 `origin/master` push 완료. 구현 중 발견한 특이사항(페이지별 중복 href 실측 대응, TC-006 자기완결적 재설계, 제3자 광고발 브라우저 크래시 빈도 상승을 사용자에게 보고 후 현재 코드로 완료 처리 승인받음)을 비고에 기록. Phase 4(product-search)를 다음 착수 대상으로 갱신. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-08-31 | (재승인) product-search Candidate 문서 재확정(TC-PRODUCT-SEARCH-001/006 재평가, TC-010 신규 승인)에 따른 부분 개정. 1절 대상 Feature 및 확정 TC 수 총계(product-search 7→8, 합계 75→76), 2절 입력 문서 스냅샷(product-search 관련 PRD/TC/Candidate 최근 변경일·확정일 2026-08-31 갱신), 5절 Phase 4 대상 TC(7건→8건, TC-010 추가) 및 시나리오 변경 사항 안내, 6절 매핑표(product-search 확정 TC 수/ID 목록 갱신), 9절 진행 현황 Phase 4 비고에 범위 변경 사실 기록. Phase 4는 아직 착수 전이므로 이미 작성된 TC-001 테스트 코드 재작업 필요성만 비고에 안내하고 실제 코드 수정은 자동화 구현 단계 몫으로 명시. 그 외 Phase 순서/Definition of Done 등 기존 계획은 변경하지 않음. | 승인완료(재승인) |
| 2026-08-31 | 사용자 요청에 따른 진행 현황 갱신. Phase 4(product-search) Approved TC 8건 전건 pytest PASSED로 갱신(TC-006은 브랜드명 4개 keyword parametrize). 구현 중 REQ-PRODUCT-SEARCH-005가 한 차례 더 재정정되어(브랜드명은 완전 일치도 항상 제외로 명확화, 상위 카테고리명 매칭 여부는 4.2 미확인 항목으로 이관) TC-006이 브랜드명 4건만 검증하도록 재작성되고 Candidate 문서도 재확정된 경위를 비고에 기록. TC-005의 assertion 방향 오류(배제↔포함) 코드 버그 수정 사실과, Phase 1~4 전체 회귀 확인 중 발견된 Phase 4와 무관한 Phase 1 회귀(TC-LOGIN-LOGOUT-015, 원인 조사 중)도 함께 기록. 코드 리뷰·Git Commit/Push는 아직 진행 전이라 Phase 4 상태를 "완료"가 아닌 "pytest 통과, 코드 리뷰·커밋 대기"로 정확히 표기. Phase 5(cart)는 Phase 4 코드 리뷰/커밋 완료 후 착수 예정으로 비고 추가. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-08-31 | 사용자 요청에 따른 진행 현황 갱신. Phase 4(product-search) 구현 커밋(`a457ce2`) 이후 `/code-review`로 코드 리뷰를 실행해 finding 4건을 발견한 경위를 비고에 기록 — 경쟁 조건(URL 변경 대기 직후 상품 그리드 렌더링을 기다리지 않고 카드를 조회해 flaky 실패 가능성)과 동일 셀렉터 3회 중복 조회 2건은 `_wait_for_results_rendered()` 헬퍼로 수정하고 재실행으로 회귀 없음(11건 PASSED) 확인 후 커밋(`a81e9d3`), 나머지 2건(TC-001 배제 조건 미검증, Enter 키 테스트 비동기 반응 미대기)은 테스트 docstring에 이미 근거가 명시된 의도적 설계 결정으로 판단해 사용자 확인 후 알려진 제약사항으로 남김. Phase 4 상태를 "코드 리뷰 반영 완료, push 대기"로 갱신하고 Phase 5(cart) 착수 조건도 "Phase 4 push 완료 후"로 정정. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-08-31 | 사용자 요청에 따른 진행 현황 갱신. `origin/master` 실제 상태를 재확인한 결과 로컬 `master`와 `origin/master`가 이미 완전히 일치함(커밋 `0f3fe24`까지 push 완료)을 확인해 Phase 4(product-search) 상태를 "코드 리뷰 반영 완료, push 대기"에서 "완료"로 갱신. Phase 5(cart)를 다음 착수 대상으로 표기. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-08-31 | 사용자 요청에 따라 AUTOMATION_GUIDE.md에 신설된 "20.1 테스트 실행 범위와 시점" 정책을 이 Roadmap에도 명시. 7절 Definition of Done을 "Phase 내부 Task 단위 테스트 실행 + Phase 완료 시 해당 Phase 범위로 한정한 pytest 실행"으로 구체화하고, 다른 Phase를 포함한 전체 통합테스트는 각 Phase Definition of Done에 포함되지 않음을 명시. 5절 Phase Final 항목에 "이 시점의 전체 스위트 실행이 AUTOMATION_GUIDE 20.1절의 전체 통합테스트(Full Regression)에 해당하며 Phase 1~7을 통틀어 1회만 수행한다"는 설명을 추가. Phase 순서/범위/기존 완료 Phase(0~4)의 진행 현황 기록은 변경하지 않음(소급 적용 없음, 향후 Phase 5 이후부터 적용). | 승인완료 |
| 2026-08-31 | 사용자 요청에 따른 진행 현황 갱신. Phase 5(cart) 완료로 표시 — Approved TC 13건 전건 pytest PASSED, `/code-review` finding 7건 중 5건 수정(finally 블록 cleanup 예외로 인한 assertion 마스킹, 클릭 재시도 로직 중복, 상품명 정규화 3중 중복, 에러 로그용 DOM 재조회 중복)/2건 보류(기존 설계 원칙과 일치하는 카드 Locator 중복은 유지, 리뷰어 오독 1건은 수정 불필요로 판단) 경위를 비고에 기록. 구현 커밋 `f3b7c6a`. Phase 6(product-detail)을 다음 착수 대상으로 갱신. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-01 | 사용자 요청에 따른 진행 현황 갱신. Phase 6(product-detail) 완료로 표시 — Approved TC 6건(001,002,008,015,016,021) 전건 pytest PASSED, `ProductDetailPage` 신규 구현, `HomePage`에 View Product 링크 조작 추가, "Add to cart" 확인 모달은 Phase 5의 `AddToCartModal`을 신규 정의 없이 재사용. `/code-review`(medium) finding 2건(`click_and_retry_if_vignette()`/`click_and_retry_if_vignette_action()` 로직 중복, `click_element()`의 `StaleElementReferenceException` 미처리) 모두 수정 후 Phase 6 재실행 6/6 PASSED 및 Phase 2/3/5 spot-check 30건 PASSED로 회귀 없음 확인. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-01 | 사용자가 Phase 6 구현 커밋(`ab652d6`) 및 `origin/master` push를 직접 완료. 로컬/원격 일치를 재확인해 9절 Phase 6 비고를 "커밋/push 승인 대기 중"에서 커밋 해시와 push 완료 확인으로 갱신. Phase 7(page-ui)을 다음 착수 대상으로 안내. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-01 | 사용자 요청에 따른 진행 현황 갱신. Phase 7(page-ui) 완료로 표시 — Approved TC 21건 전건 pytest PASSED, `CategoryProductsPage`/`BrandProductsPage` 신규 구현, HomePage/ProductsPage/CartPage/CheckoutPage/ProductDetailPage 확장. `/code-review`(medium) finding 4건(캐러셀 strip 비대칭 비교, class 속성 None 크래시, CATEGORY 아코디언 타임아웃 재사용 문제, HomePage/ProductsPage 간 ~90줄 중복 로직) 모두 수정 후 Phase 7 재실행 21/21 PASSED 및 Phase 1/3/5/6 spot-check 36건 PASSED로 회귀 없음 확인. 구현 중 발견한 특이사항(Google Vignette의 아코디언 개입, google-anno 광고 아티팩트의 Selenium 재현 확인, Checkout 표 합계 행 집계 오류, 고정 계정 leftover 데이터)을 비고에 기록. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-01 | 사용자가 Phase 7 구현 커밋(`abd0b43`) 및 `origin/master` push를 직접 완료. 로컬/원격 일치를 재확인해 9절 Phase 7 비고를 "커밋/push 승인 대기 중"에서 커밋 해시와 push 완료 확인으로 갱신. Feature Phase 1~7이 모두 완료·push되어 Phase Final(CI/CD 및 Slack 알림 연동) 착수 조건이 충족되었음을 참고로 안내(착수 여부는 사용자 결정 대기). Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-01 | 사용자 요청에 따른 진행 현황 갱신. Phase Final(CI/CD 및 Slack 알림 연동) 착수를 준비하던 중, AUTOMATION_GUIDE 20.1절이 요구하는 전체 통합테스트(Full Regression)가 실제로는 아직 수행되지 않았음을 발견 — 기존 `automation/reports/results_full.xml`(8/31 15:49 실행분)에는 test_login/test_signup/test_delete_account/test_top_navigation/test_product_search 5개 파일만 포함되어 있었고, 그 이후 완성된 test_cart.py(8/31 21:56 최종 수정)/test_product_detail.py(9/1 14:07)/test_page_ui.py(9/1 15:26)가 빠져 있어 76건 전체를 아우르지 못한 불완전한 실행이었음을 사용자에게 보고. 사용자가 "Full Regression 먼저 실행 후 계획"을 선택해 승인함에 따라 `automation/` 디렉터리에서 `pytest tests/ --html=reports/report_full_final.html --self-contained-html --junitxml=reports/results_full_final.xml`로 test_login.py/test_signup.py/test_delete_account.py/test_top_navigation.py/test_product_search.py/test_cart.py/test_product_detail.py/test_page_ui.py 8개 파일 전체를 재실행. 결과 79 passed, 0 failed, 0 error(923.62초 소요, 79건은 Approved TC 76건 기준 product-search TC-006 등 parametrize 확장 포함). 리포트는 `automation/reports/report_full_final.html`, `automation/reports/results_full_final.xml`에 저장. 9절 Phase Final 행을 "보류(사용자 결정)"에서 "착수 조건 충족(전체 통합테스트 완료)"으로 갱신하고 실행 결과와 리포트 경로를 비고에 기록. Phase Final의 실제 착수·구현 여부는 이번 갱신의 범위가 아니며 별도로 진행됨을 명시. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-02 | 사용자 요청에 따른 진행 현황 갱신. Phase Final Shrimp Task 1~4(headless Chrome 지원, `ci.yml` 작성, Slack 알림 스크립트, 알림 스텝 연결) 구현 완료 및 GitHub Secrets 4종(`ACTEST1_PASSWORD`/`ACTEST2_PASSWORD`/`ACTEST3_PASSWORD`/`SLACK_WEBHOOK_URL`) 사용자 등록 완료를 9절 Phase Final 비고에 기록. 구현 중 발견한 두 가지 논리적 문제(headless에서 `maximize_window()` 호출 시 800x600으로 축소되는 실측 결함, `if: failure()`가 `continue-on-error: true`와 조합 시 영원히 실행되지 않는 조건식 오류)를 수정한 경위도 함께 기록. CI 트리거는 "master push만", 실행 범위는 "매 push마다 전체 실행"으로 사용자 확정. 남은 Task 5(Commit/Push 승인 후 실제 GitHub Actions 실행 검증)는 사용자의 Commit/Push 승인이 선행되어야 진행 가능함을 명시(CLAUDE.md 18절). Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-02 | 사용자 승인에 따른 Task 5(Commit/Push 승인 후 실제 GitHub Actions 실행 검증) 완료 및 진행 현황 갱신. Task 1~4 변경사항을 커밋(`24c484d`)·push해 실제 GitHub Actions 실행(79 passed/0 failed, 328.43초, headless, Artifact 업로드 확인)으로 CI 파이프라인 동작을 검증. Slack 알림 실전 확인을 위해 임시 실패 테스트를 추가·push해 `Notify Slack on failure` 스텝 실행과 실제 Slack 채널 도착을 사용자가 직접 확인(이 과정에서 이미 문서화된 `/logout` 간헐적 결함이 GitHub Actions headless 환경에서도 재현됨을 처음 확인해 사용자 승인 하에 `AUTOMATION_GUIDE.md` 22.1절에 기록). 사용자 요청으로 Slack 메시지에 실패 위치(파일:라인)를 표시하도록 `notify.py`를 개선(커밋 `bc7921a`)하고 다시 실전 검증. 임시 테스트 삭제 및 문서 갱신 커밋(`f2165f8`)으로 master를 원상 복구. Shrimp Task 5건 전건 완료. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-02 | 사용자 요청에 따라 CI 트리거를 확장. 기존에 "master push만"으로 확정했던 트리거 범위에 "매일 한국시간(KST, UTC+9) 오전 9시 스케줄 실행(주 7일)"과 "수동 실행(workflow_dispatch)"을 추가하기로 사용자와 협의(GitHub Actions cron은 UTC만 지원하므로 `0 0 * * *`로 변환, 요일 범위는 매일로 확정). `.github/workflows/ci.yml`의 `on:` 블록에 `schedule`/`workflow_dispatch`를 추가했으며, job/step 내용(pytest 실행, Artifact 업로드, Slack 알림, 실패 처리)은 트리거 종류와 무관하게 동일하게 유지해 임의로 분기하지 않음. 9절 Phase Final 비고에 변경 사실을 기록. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
| 2026-09-02 | 사용자 요청에 따른 진행 현황 갱신. CI 트리거 확장 변경사항 커밋(`9769f4a`)·push 완료. `workflow_dispatch`로 즉시 수동 실행(run `33600534407`, 성공, 7m25s)해 신규 트리거 설정이 GitHub에 정상 등록됨을 확인했고, 동시에 발생한 push 트리거 실행(run `33600527284`)도 79 passed/0 failed로 성공해 임시 테스트 삭제 이후 회귀가 없음을 재확인. 9절 Phase Final 상태를 "완료"로 최종 정리하고, 실제 `schedule` 자동 실행(다음날 KST 09:00 최초 발생 예정)은 이 세션에서 직접 관측하지 못했음을 명시. Phase 순서/범위/Definition of Done 등 기존 계획 내용은 변경하지 않음. | 승인완료 |
