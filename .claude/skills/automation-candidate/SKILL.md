---
name: automation-candidate
description: 자동화 대상 선정 평가 스킬 - 승인된 TC의 자동화 적합성을 Business Criticality/Regression Frequency/Automation Stability/Result Determinism/Manual Test Cost/Maintenance Cost 6개 축으로 평가하는 Automation Score 기준, 우선 선정/후순위 신호, Score와 무관한 Hard Rule, Candidate(Yes/No/Hold) 판정 기준을 정의합니다. 자동화 후보를 평가하는 모든 Agent가 이 Skill을 로드해서 따르며, 특정 프로젝트에 종속되지 않고 다른 QA 프로젝트에서도 재사용 가능합니다.
---

# Automation Candidate Skill

이 Skill은 **자동화 대상 선정 평가 기준(Automation Score 산정 방식, Candidate 판정 기준)**만
정의합니다. 평가 Workflow(TC 확인 → 평가 → Sheet 동기화 → 사용자 QA Decision 확인 등)는 이
Skill의 책임이 아니며, 이를 사용하는 Agent(예: `automation-candidate-agent`)가 담당합니다. 이
Skill은 특정 프로젝트명, 서비스명, TC 내용을 알지 못하는 상태를 전제로 작성되었으며, 어떤 QA
프로젝트에서도 동일하게 재사용할 수 있어야 합니다.

## 1. 평가 원칙

- **Priority만으로 자동화 여부를 결정하지 않는다.** P0 TC라도 육안 판단 의존도가 높거나 요구사항/
  UI 구조가 자주 바뀌면 자동화 부적합할 수 있고, P2 TC라도 매 Release마다 반복 수행되는 단순
  Regression이면 자동화 ROI가 높을 수 있다.
- **점수는 판단을 돕는 참고 지표이며, 기계적으로만 적용해 최종 결론을 내리지 않는다.** 아래 3절의
  Automation Score 구간은 "1차 판단 경향"일 뿐이다. 최종 Candidate는 TC의 실제 목적, 검증하는
  Risk의 성격, 실제 자동화 ROI(자동화 구현/유지보수 비용 대비 반복 실행으로 얻는 효과)를 함께
  고려해 판단한다. 점수 구간과 최종 Candidate가 다른 경우, 반드시 그 사유를 서술로 함께 제시한다.
- **동일한 원인으로 여러 축을 기계적으로 중복 감점하지 않는다.** 특히 Automation Stability(요구
  사항/UI 구조 자체의 변경 가능성)와 Maintenance Cost(구현 이후 유지 비용)는 서로 다른 질문이므로,
  하나의 관찰 사실이 어느 축에 해당하는 원인인지 구분해서 평가한다(2.3 / 2.6 참조). 마찬가지로
  Manual Test Cost(1회 수동 수행 비용)와 Regression Frequency(반복 빈도)도 서로 다른 질문이므로
  섞어서 평가하지 않는다(2.2 / 2.5 참조).
- **Score와 무관하게 항상 적용되는 규칙은 5절 Hard Rule을 따른다.**
- TC는 **개별 단위로 평가**한다. 같은 Feature 안에서도 TC별로 자동화 적합성이 다를 수 있으므로,
  Feature 전체를 일괄로 Yes/No 처리하지 않는다.

## 2. Automation Score 평가 기준 (6개 축)

각 축은 1~5점으로 평가한다. Business Criticality / Regression Frequency / Automation
Stability / Result Determinism / Manual Test Cost는 **5점이 자동화에 유리한 방향**이다.
**Maintenance Cost만 예외적으로 5점이 자동화에 불리한 방향(비용이 높음)이며**, 이는 원점수를
그대로 두고 3절의 최종 합산 공식에서 역산(`6 - Maintenance Cost`)해 방향을 맞춘다.

### 2.1 Business Criticality — TC 실패 시나리오의 사용자/비즈니스 영향도

이 축은 **Feature 전체의 중요도가 아니라, 이 TC가 검증하는 개별 실패(회귀) 시나리오가 실제로
발생했을 때의 영향도**를 평가한다. 같은 Feature에 속한 TC라도 검증하는 실패 시나리오에 따라
점수가 달라질 수 있다(예: 같은 "장바구니" Feature 안에서도 "결제 진입 차단"과 "안내 문구 오타"는
전혀 다른 점수를 받는다).

| 점수 | 기준 |
|---|---|
| 5 | 이 시나리오가 실패하면 핵심 사용자 Flow(로그인, 결제, 핵심 데이터 처리 등)를 사용할 수 없거나 데이터 손실/오류로 이어짐 |
| 4 | 실패 시 주요 기능 사용에 큰 지장을 주거나 서비스 결과의 신뢰성이 훼손됨 |
| 3 | 실패해도 기능은 사용 가능하나 일부 사용자 경험이 저하됨 |
| 2 | 실패해도 대체 경로가 있거나 영향이 제한적인 UI/부가 기능 수준 |
| 1 | 실패해도 사용자 영향이 매우 낮음 |

### 2.2 Regression Frequency — Release마다 반복 검증되는 정도

| 점수 | 기준 |
|---|---|
| 5 | 매 Release마다 예외 없이 반복 검증되는 핵심 Regression |
| 4 | 대부분의 Release에서 반복 검증됨 |
| 3 | 관련 기능 변경이 있을 때만 간헐적으로 검증 |
| 2 | 드물게만 재검증되는 기능 |
| 1 | 일회성 기능 또는 사실상 재검증되지 않음 |

### 2.3 Automation Stability — 기능/요구사항/UI 구조 자체의 변경 가능성

이 축은 **자동화 구현/유지에 드는 비용(Maintenance Cost, 2.6)과는 별개로, 검증 대상 기능의
요구사항이나 UI 구조 자체가 앞으로 얼마나 안정적으로 유지될 것으로 예상되는지**만 평가한다.
"바뀔 가능성이 있는가"에 대한 축이며, "바뀌었을 때(또는 실행할 때마다) 자동화를 유지하는 데
비용이 얼마나 드는가"는 2.6 Maintenance Cost에서 평가한다.

| 점수 | 기준 |
|---|---|
| 5 | 요구사항과 UI 구조가 매우 안정적이고 변경 계획이 없음 |
| 4 | 대체로 안정적, 변경이 있어도 영향 범위가 작음 |
| 3 | 보통 수준, 가끔 요구사항/UI 구조 변경 발생 |
| 2 | 요구사항 또는 UI 구조가 자주 바뀌는 편 |
| 1 | 요구사항 또는 UI 구조가 매우 자주 바뀜 |

### 2.4 Result Determinism — 결과의 자동 판정 가능성

| 점수 | 기준 |
|---|---|
| 5 | 값/상태/URL/DOM 속성 등으로 Pass/Fail을 명확하고 결정적으로 판정 가능 |
| 4 | 대부분 자동 판정 가능하나 일부 조건에서 보조 확인 필요 |
| 3 | 자동 판정이 가능하지만 판정 로직이 다소 복잡함 |
| 2 | 자동 판정이 까다롭고 육안 확인에 상당 부분 의존 |
| 1 | 실제 사용 예정 자동화 도구 기준으로 Pass/Fail을 판정할 방법이 없거나, 육안 판단(레이아웃 미세 차이, 디자인 감성 등)에 전적으로 의존함 |

**Browser Native 동작에 대한 주의**: 브라우저 기본 alert/confirm, 파일 다운로드 다이얼로그 등
Native 동작을 검증하는 TC를 자동화 불가능으로 단정하지 않는다. 실제 사용 예정 자동화 도구가 해당
동작을 제어/판정할 수 있는지(**기술적 가능성**)를 먼저 확인해 이 축의 점수를 매긴다. 기술적으로는
판정 가능하더라도 반복 회귀 검증으로서의 실익(**Regression ROI**)이 낮다고 판단되는 경우는 이
축을 낮추는 근거로 쓰지 않고, 4.3절 정성 분석과 최종 Candidate 판단에서 별도로 반영한다(기술적
가능성과 ROI를 같은 축에서 섞지 않는다).

### 2.5 Manual Test Cost — TC 1회 수동 수행 비용

이 축은 **반복 빈도를 포함하지 않고, 이 TC를 한 번 수동으로 수행하는 데 드는 비용(소요 시간,
사전 조건 준비 난이도, 수행 절차의 복잡도)만** 평가한다. 반복 빈도는 2.2 Regression Frequency에서
이미 평가하므로, 여기서 다시 반영하면 이중 계산이 된다.

| 점수 | 기준 |
|---|---|
| 5 | 1회 수행에도 사전 조건 준비와 수행 절차에 시간이 많이 들고 복잡함 |
| 4 | 1회 수행 비용이 높은 편 |
| 3 | 보통 수준의 1회 수행 비용 |
| 2 | 1회 수행이 짧고 간단함 |
| 1 | 수 초~수십 초 내 간단히 확인 가능함 |

### 2.6 Maintenance Cost — 자동화 구현 이후 유지 비용

이 축은 **자동화 구현 이후 자동화 코드/테스트 데이터/실행 환경/외부 의존성을 유지하는 데 드는
비용**을 평가한다. "기능 자체가 바뀔 가능성"은 2.3 Automation Stability에서 평가하므로, 여기서는
"실제로 자동화를 계속 통과시키기 위해 드는 비용"에 집중한다. 다음 요소를 포함해 평가한다.

- 자동화 코드/Selector의 복잡도
- 테스트 데이터 준비·정리(생성, 초기화, 격리)의 난이도
- 실행 환경(브라우저/디바이스/네트워크 등) 의존성
- 외부 시스템/타 서비스 연동 의존성(결제 PG, 알림 등)

**주의**: Automation Stability와 Maintenance Cost가 같은 관찰 사실(예: "UI가 자주 바뀐다")에서
비롯되었다고 해서 두 축을 기계적으로 함께 낮게 매기지 않는다. 원인이 "요구사항/구조 자체의 변경
가능성"이면 2.3에서만 반영하고, 원인이 "구현 이후 유지 비용(코드/데이터/환경/외부 의존성)"이면 이
축에서만 반영한다. 두 원인이 실질적으로 모두 존재하는 경우에만 각 축에 독립적으로 반영한다.

| 점수 | 기준 |
|---|---|
| 5 | 유지보수 비용이 매우 높아 자동화 효과를 상쇄하거나 초과할 가능성이 큼(복잡한 대기 조건, 불안정한 테스트 데이터, 다수의 외부 의존성 등) |
| 4 | 유지보수 비용이 높은 편 |
| 3 | 보통 수준의 유지보수 비용 |
| 2 | 유지보수 비용이 낮은 편 |
| 1 | 자동화 후 유지보수 비용이 매우 낮을 것으로 예상(안정적 구조, 단순한 로직, 의존성 적음) |

## 3. Automation Score 계산 및 1차 판단 구간

```
Automation Score = Business Criticality + Regression Frequency + Automation Stability
                  + Result Determinism + Manual Test Cost + (6 - Maintenance Cost)
```

Maintenance Cost는 점수가 높을수록 자동화에 불리하므로, 최종 합산 시 `(6 - Maintenance Cost)`로
역산해 다른 축과 방향을 맞춘다. 최대 점수는 30점이다(각 축 5점 만점 × 6개 축).

| Automation Score | 1차 판단 경향 (참고용) |
|---|---|
| 24 ~ 30 | 자동화 적극 추천 |
| 18 ~ 23 | 자동화 후보 또는 추가 검토 |
| 12 ~ 17 | Hold |
| 6 ~ 11 | 자동화 비추천 |

**주의**: 이 구간은 기계적 최종 판정이 아니라 1차 참고 지표다. **Automation Score만으로
Candidate 여부를 결정하지 않는다.** 점수 산정 후 4.3절의 추가 정성 분석 항목과 5절 Hard Rule,
TC 목적/ROI를 함께 검토한 뒤 최종 Candidate(Yes/No/Hold)를 결정하며, 점수 구간과 다르게 판단한
경우 그 사유를 반드시 남긴다.

## 4. 우선 선정 신호 / 후순위·제외 신호

### 4.1 우선 선정 고려 대상 (자동화 후보로 적극 고려)

- 핵심 사용자 Flow에서 실패 시 영향이 큰 시나리오 (Business Criticality 상)
- Release마다 반복되는 Regression (Regression Frequency 상)
- 결과가 명확하게 자동 판정 가능한 TC (Result Determinism 상)
- TC 1회 수동 수행 비용이 높고 반복 빈도도 높은 TC (Manual Test Cost 상 + Regression Frequency 상 조합)
- 요구사항과 UI 구조가 비교적 안정적인 기능 (Automation Stability 상)

### 4.2 후순위 또는 제외 고려 대상

- 단순 UI 노출 확인 (대체로 Business Criticality/Result Determinism이 낮고 자동화 ROI가 낮음)
- 브라우저 Native 동작 자체를 검증하는 TC 중, 실제 사용 예정 자동화 도구로 기술적으로 제어/판정이
  불가능하거나 Regression ROI가 낮다고 판단되는 경우(2.4 참고)
- 일회성 기능 (Regression Frequency 매우 낮음)
- 요구사항 또는 UI 구조 변경이 매우 잦은 기능 (Automation Stability 낮음)
- 육안 판단 의존도가 높은 TC (Result Determinism 낮음)
- 유지보수 비용이 자동화 효과보다 높은 TC (Maintenance Cost 높음 축이 전체 ROI를 상쇄)
- **현재 발생 중인 결함을 정상 Expected Result처럼 고정하는 TC** (5절 Hard Rule 참조 — 점수
  무관 무조건 제외, 별도 사용자 보고 필요)

### 4.3 추가 정성 분석 항목 (Automation Score 산정 이후 반드시 검토)

Automation Score를 계산한 뒤, 최종 Candidate(Yes/No/Hold)를 추천하기 전에 다음 항목을 추가로
검토한다. 이 항목들은 점수에 이미 반영되지 않은 맥락을 보완하기 위한 것으로, 점수가 높아도 아래
항목에서 문제가 발견되면 Candidate를 낮추거나 Hold로 조정할 수 있다.

- **TC 중복 여부**: 다른 TC 또는 이미 자동화된 TC와 검증 목적이 실질적으로 동일한지
- **다른 E2E Flow에서 이미 검증되는지**: 다른 자동화 대상 TC의 E2E Flow 안에서 동일한 동작이
  수행된다는 이유만으로 기계적으로 중복 판단하지 않는다. 이 TC가 별도의 Risk Coverage(다른
  Expected Result, 다른 조건, 다른 실패 가능 지점 등)를 검증하는지 확인하고, **별도 Risk
  Coverage가 없는 경우에만** 중복으로 판단해 자동화 실익이 낮다고 본다.
- **브라우저 Native 검증의 Regression ROI**: 2.4절에서 기술적으로는 판정 가능하다고 평가했더라도,
  실제로 반복 자동 회귀 검증할 실익이 낮다고 판단되면 여기서 반영한다.
- **일회성 기능 여부**: 반복 회귀 검증 가치가 낮은 일회성 기능을 검증하는 TC인지
- **유지보수 위험(Test Data / Environment Dependency 포함)**: 외부 의존성, 비결정적 대기 조건,
  테스트 데이터 준비/정리 난이도, 실행 환경(브라우저/디바이스/네트워크 등) 의존성 등으로 자동화
  이후 Flaky해지거나 유지보수 부담이 커질 위험이 있는지(2.6 Maintenance Cost 점수와 일관되게
  판단)

## 5. Score와 무관하게 적용되는 Hard Rule

아래 규칙은 Automation Score나 4절의 신호와 무관하게 항상 우선 적용된다.

- **현재 발생 중인 결함(비정상 동작)을 정상 Expected Result처럼 고정한 TC는 Candidate: No로
  처리한다.** (참고: `tc-writing` Skill 4.6에 따라 "결함 의심 항목" 섹션으로 분류된 TC가 여기
  해당할 가능성이 높다.) 이런 TC를 자동화하면 실제 결함을 회귀 검증 없이 정상으로 고정시키는
  결과가 되므로, 발견 시 점수 산정과 별개로 반드시 사용자에게 별도로 보고한다.
- **이 규칙은 영구적이지 않다.** 해당 TC의 근거가 된 PRD/TC가 이후 정상 요구사항으로 수정되어
  재승인되면(즉, 더 이상 "결함을 정상처럼 고정"하는 상태가 아니게 되면), 그 TC는 다시 일반 TC와
  동일한 절차로 재평가할 수 있다.

## 6. Candidate 판정

| Candidate | 의미 |
|---|---|
| Yes | 자동화 대상으로 적극 권장 |
| Hold | 아직 자동화 여부를 확정할 수 없음(정보 부족, 경계 사례, ROI 판단이 애매한 경우 등) — 사용자
        검토가 필요하며, 사용자가 검토 없이는 Approved/Rejected 어느 쪽으로도 자동 전환되지 않는다 |
| No | 자동화 대상에서 제외 권장 |

Candidate는 항상 Automation Score와 판정 사유(어떤 축이 결정적이었는지, 4절의 어떤 신호와 정성
분석 항목, 혹은 5절 Hard Rule에 해당하는지)를 함께 제시한다. 판정 사유가 부족해 사용자가 근거를
검토할 수 없는 경우 이 Skill의 목적(자동화 ROI에 대한 근거 있는 1차 판단 제공)에 부합하지 않는다.

**AI가 제시하는 Candidate는 어디까지나 추천이다.** 최종 자동화 대상은 이 평가 결과를 근거로
사용자가 검토하고 승인한 이후에만 확정되며, 이 Skill을 사용하는 Agent는 어떤 TC도 자체적으로
최종 확정하지 않는다.

## 7. 평가 시 준수사항

- Candidate 평가는 "자동화 대상으로 적합한지"만 판단하는 것이며, Automation TC 작성이나 자동화
  코드 구현을 의미하지 않는다. 실제 Automation TC/코드는 사용자가 최종 승인한 이후 별도 단계
  (다른 Agent/Skill)에서 진행한다.
- TC 자체(Test Scenario, Expected Result 등)를 수정하거나 재작성하지 않는다. 이 Skill은 평가만
  다루며, TC 작성 규칙은 `tc-writing` Skill의 책임이다.
- 최종 Candidate 판단 시 다음과 같은 질문을 함께 고려한다.
  - 이 TC가 실패(회귀)했을 때, 자동화가 없다면 얼마나 늦게 발견되는가?
  - 이 TC는 실제로 반복 실행될 가능성이 높은가, 아니면 한두 번 확인 후 다시 볼 일이 없는가?
  - 자동화 이후 예상되는 유지보수 비용이 장기적으로 자동화 효과를 초과할 가능성은 없는가?

## 8. 출력 포맷 가이드

TC별 평가 결과는 최소한 다음 4개 정보를 포함해야 한다.

`TC ID | Automation Score | Candidate | 선정/제외 사유`

이보다 상세한 정보(6개 축 개별 점수 등)를 함께 제시하는 것은 권장되며, 아래 컬럼 순서를 기본으로
사용한다.

| 순서 | 컬럼명 |
|---|---|
| 1 | TC ID |
| 2 | Business Criticality |
| 3 | Regression Frequency |
| 4 | Automation Stability |
| 5 | Result Determinism |
| 6 | Manual Test Cost |
| 7 | Maintenance Cost |
| 8 | Automation Score |
| 9 | Candidate (AI 판정) |
| 10 | 선정/제외 사유 |

실제 문서/Sheet 템플릿(QA Decision, QA Comment 등 사용자 작성 영역 포함)은 이 Skill을 사용하는
Agent가 정의한다.
