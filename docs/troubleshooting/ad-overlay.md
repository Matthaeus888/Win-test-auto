# 트러블슈팅: 제3자 광고 오버레이로 인한 클릭/입력 가로채임

## 문제 상황

테스트 대상인 `automationexercise.com`은 실제 서비스 중인 사이트 자체가 아니라
**제3자(Google Ads) 네트워크가 페이지 진입 시 무작위로 전면 광고 오버레이**(Google
Vignette 등, 화면 전체를 덮고 "Close" 컨트롤이 있는 모달)를 주입한다. 이 광고는 QA
대상(Project PRD 기준 검증 대상 아님)이 아니지만, 실제 요소를 가리거나 클릭 이벤트를
가로채 자동화 테스트를 실패시켰다.

초기 구현에서는 아래와 같은 패턴으로 테스트가 실패했다.

```
selenium.common.exceptions.ElementClickInterceptedException:
Element <a href="/products">...</a> is not clickable at point (x, y).
Other element would receive the click: <iframe ...google_ads...>
```

## 원인 분석 과정

1. 최초에는 광고 오버레이가 "뷰포트의 80%를 덮는 iframe"일 때만 방어 로직을 태우도록
   구현했다(성능 비용을 줄이려는 의도).
2. 그러나 전체 회귀 테스트를 재실행하는 과정에서 실제 오버레이 크기가 매번 다르다는
   것이 확인되었다(실측 기준 뷰포트의 약 79%×65%인 사례 등) — 이 크기 기반 게이팅이
   실제 오버레이를 놓쳐 **5개 테스트가 연쇄 실패**하는 회귀를 유발했다.
3. 실패 스크린샷을 직접 검토해 원인을 좁혔고, 크기 기준 게이팅을 제거한 뒤 "Close"
   텍스트를 가진 요소가 DOM에 **존재하는지 자체**를 먼저 확인하는 방식으로 재설계했다.
4. `automationexercise.com` 자체 UI에는 정확히 "Close"라는 텍스트를 가진 요소가 없다는
   것을 수십 차례의 스크린샷 실측으로 확인해, 이 Locator가 사이트 자체의 정상 UI를
   오검지할 위험이 낮다고 판단했다.

## 해결 방법

`BasePage`에 두 단계 방어 로직을 구현했다([automation/pages/base_page.py](../../automation/pages/base_page.py)).

### 1) 진입 시 오버레이 선제 감지·해제

```python
def _dismiss_ad_overlay_if_present(self) -> None:
    # find_elements()(복수형)는 없으면 즉시 빈 리스트를 반환하며 폴링하지 않는다
    # → 오버레이가 없는 일반적인 경우 성능 저하가 없다.
    if not self.driver.find_elements(*self.AD_OVERLAY_CLOSE_BUTTON):
        return
    try:
        close_button = WebDriverWait(self.driver, self.AD_OVERLAY_DISMISS_TIMEOUT).until(
            EC.element_to_be_clickable(self.AD_OVERLAY_CLOSE_BUTTON)
        )
        close_button.click()
    except TimeoutException:
        pass  # Close 요소는 있었으나 클릭 가능한 상태가 아님 - 정상 진행
```

모든 `click()` / `type_text()` 호출 시작 시점에 자동 실행되며, `BasePage`를 상속하기만
하면 모든 Page Object가 별도 구현 없이 이 방어를 적용받는다.

### 2) 클릭이 가로채였을 때의 단계적 재시도

```python
try:
    element.click()
except ElementClickInterceptedException:
    # 1차: 화면 중앙으로 스크롤 후 재클릭
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except ElementClickInterceptedException:
        # 2차: 뷰포트 전체를 덮는 오버레이는 스크롤로도 회피 불가 →
        # JavaScript로 클릭 이벤트를 대상 DOM 요소에 직접 디스패치
        driver.execute_script("arguments[0].click();", element)
```

무한 재시도가 아니라 **최대 2회(스크롤 재클릭 → JS 클릭)** 로 재시도 횟수를 결정적으로
제한했다.

### 3) 클릭 이후 광고가 재개입하는 경우 (2차 방어)

"Continue" 버튼처럼 클릭이 실제 페이지 이동을 트리거하는 경우, 클릭 자체는
성공하더라도 그 직후 Google Vignette가 다시 개입해 URL 끝에 `#google_vignette`만
붙고 실제 이동은 되지 않는 현상도 발견했다. 이를 위해 클릭 후 URL을 짧게 관찰해
`google_vignette`가 나타나면 1회 더 재클릭하는 `click_and_retry_if_vignette()`를
추가했다.

## 배운 점

- **성능과 견고성은 트레이드오프**이며, 실측 없이 최적화(크기 기준 게이팅)를 먼저
  적용했다가 오히려 실패를 유발한 경험 — 추측이 아니라 스크린샷 등 **실측 증거로
  검증**한 뒤 로직을 확정해야 한다.
- 재시도는 "문제가 해결될 때까지"가 아니라 **결정적으로 횟수를 제한**해야 한다(무한
  재시도는 실제 결함을 가리는 결과를 낳는다).
- 광고처럼 자동화 대상이 아닌 요소라도, 검증 로직과 완전히 무관하게 둘 수는 없다 —
  공통 기반 클래스(`BasePage`)에 한 번만 구현해 모든 Page Object에 일관되게 적용하는
  것이 유지보수 관점에서 중요하다.
