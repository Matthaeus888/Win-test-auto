"""자동화 테스트 공통 환경 설정값.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md
- 1절 Technology Stack: 대상 환경은 Production 단일 환경(https://automationexercise.com/).
- 9절 Fixture 원칙 / 7절 Wait 처리 원칙: WebDriverWait 기본 타임아웃 값을 여기서 관리한다.
- 12절 환경변수 및 민감정보 관리: 비밀번호 등 민감정보는 이 파일에 두지 않고 .env로만 관리한다.
"""

# 테스트 대상 사이트의 기본 URL(Production 단일 환경)
BASE_URL = "https://automationexercise.com/"

# WebDriverWait의 기본 타임아웃(초 단위)
DEFAULT_TIMEOUT = 10
