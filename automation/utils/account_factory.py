"""회원가입 시나리오에서 사용할 동적 테스트 데이터 생성 Factory.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md 11.2절(동적 생성)
- 회원가입/계정삭제 TC(TC-SIGNUP-DELETE-ACCOUNT-001,002,004~007,010~014)는 매 실행마다
  신규(미가입) 계정이 필요하므로, uuid로 매번 고유한 이메일을 생성해 고정 계정
  (actest1~3)이 소모되는 사고와 Production 데이터 오염을 방지한다.

이 함수가 반환하는 값은 실제 개인정보가 아니라 테스트가 스스로 생성/사용하는 임시
더미 값이므로 .env 등 민감정보 관리 대상이 아니다(11.2절/12절 범위 밖). 화면과 무관한
순수 로직만 담당하므로 BasePage를 상속하지 않는다(config/accounts.py와 동일한 유틸
계층 패턴).

Country는 Playwright MCP 실측(2026-08-30, https://automationexercise.com/signup,
#country select 옵션 조회, 계정 생성 없이 페이지 구조만 조회)으로 확인된 유효 옵션
(India, United States, Canada, Australia, Israel, New Zealand, Singapore) 중
"United States"를 고정값으로 사용한다. SignupPage.select_country()가
Select.select_by_visible_text()를 사용하므로 유효하지 않은 옵션 텍스트를 넘기면
NoSuchElementException이 발생하기 때문에, 실측으로 확인된 값만 사용한다.
"""

import uuid


def generate_signup_data() -> dict:
    """매 호출마다 고유한 회원가입용 더미 데이터를 생성해 반환한다.

    Returns:
        SignupPage.fill_mandatory_fields()와 LoginPage.start_signup()에 필요한
        모든 필드를 담은 dict: name, email, password, first_name, last_name,
        address, country, state, city, zipcode, mobile_number.
    """
    unique_id = uuid.uuid4().hex[:8]

    return {
        "name": f"QA Test {unique_id}",
        "email": f"qa_test_{unique_id}@example.com",
        "password": f"QaTest!{unique_id}",
        "first_name": "QA",
        "last_name": f"Tester{unique_id}",
        "address": "123 QA Automation Street",
        "country": "United States",
        "state": "California",
        "city": "San Francisco",
        "zipcode": "94105",
        "mobile_number": "4155550100",
    }
