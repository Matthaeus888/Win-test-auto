"""pytest 공통 fixture 및 hook 정의.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md 9절 Fixture 원칙, 14절 실패 시
Screenshot/Artifact 원칙
- WebDriver 생성/종료는 여기서 fixture로 관리하며, yield 패턴으로 테스트 종료 후
  리소스 정리(driver.quit())를 보장한다.
- 기본 scope는 function으로 설정해 테스트마다 새 WebDriver를 생성한다(10절 테스트 독립성).
- pytest_runtest_makereport hook으로 테스트 실패 시에만 자동으로 스크린샷을 캡처한다
  (14절, 15절 구체적 예외 처리·로깅 원칙 준수).
"""

import datetime
import logging
import os
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

# automation/screenshots (이 파일 conftest.py 위치 기준 - pytest를 어느 위치에서
# 실행하든 항상 동일한 경로에 저장되도록 절대경로로 계산한다)
_SCREENSHOTS_DIR = Path(__file__).resolve().parent / "screenshots"


@pytest.fixture(scope="function")
def driver():
    """테스트마다 새로 생성/종료되는 Chrome WebDriver fixture.

    GitHub Actions 등 CI 환경(디스플레이 없음)에서는 환경변수 CI=true가 자동으로
    설정되므로, 이 값을 감지해 headless 모드로 전환한다. 로컬(CI 미설정)에서는 기존과
    동일하게 headed로 동작한다.
    """
    options = Options()
    is_ci = os.environ.get("CI") == "true"
    if is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    if not is_ci:
        # headless 모드에서는 --window-size 인자로 뷰포트 크기를 이미 고정하므로
        # maximize_window()를 호출하지 않는다. 실측 결과 headless에서 maximize_window()를
        # 호출하면 오히려 800x600으로 축소되는 것을 확인했다(Shrimp Task 820a9890 검증).
        driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 실패 시(call 단계)에만 스크린샷을 자동 캡처하는 hook.

    AUTOMATION_GUIDE 14절 파일명 규칙({테스트_함수명}_{상태}_{YYYY-MM-DD_HH-MM-SS}.png)을
    따르며, automation/screenshots/(git 미추적)에 저장한다. 스크린샷 저장 자체가 실패해도
    원래 테스트 실패 보고를 막지 않되, AUTOMATION_GUIDE 15절에 따라 구체적 예외
    (WebDriverException/OSError)만 처리하고 반드시 logging으로 남긴다.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    driver_instance = item.funcargs.get("driver")
    if driver_instance is None:
        logger.warning(
            "테스트 %s가 실패했지만 driver fixture를 사용하지 않아 스크린샷을 캡처하지 않음",
            item.name,
        )
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{item.name}_failed_{timestamp}.png"
    filepath = _SCREENSHOTS_DIR / filename

    try:
        _SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        driver_instance.save_screenshot(str(filepath))
        logger.info("실패 스크린샷 저장 완료: %s", filepath)
    except WebDriverException:
        logger.error("실패 스크린샷 저장 중 WebDriver 오류 발생: %s", filepath, exc_info=True)
    except OSError:
        logger.error("실패 스크린샷 저장 중 파일 시스템 오류 발생: %s", filepath, exc_info=True)
