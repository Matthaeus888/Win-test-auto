"""고정 계정(actest1~3) 자격증명 로딩 유틸.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md
- 11.1절: 로그인 상태가 필요한 시나리오는 사전 준비된 고정 계정 3개를 재사용한다.
  계정 이메일은 test_data/accounts.json, 비밀번호는 .env(환경변수)로만 관리한다.
- 12절: 비밀번호 등 민감정보는 코드에 절대 작성하지 않고 python-dotenv + .env로 관리한다.

이 파일은 화면과 무관한 순수 로직(자격증명 조합)만 담당하는 유틸이며 Page Object가
아니므로 BasePage를 상속하지 않는다.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv

# automation/.env를 로드한다(git 미추적, 로컬/CI 환경에서만 존재).
load_dotenv()

# automation/test_data/accounts.json 경로 (이 파일 기준 상위 디렉터리의 test_data)
_ACCOUNTS_FILE = Path(__file__).resolve().parent.parent / "test_data" / "accounts.json"


def get_account(name: str) -> dict:
    """계정명으로 이메일(test_data/accounts.json)과 비밀번호(.env)를 결합해 반환한다.

    Args:
        name: 계정명(예: "actest1"). accounts.json의 key와 동일해야 한다.

    Returns:
        {"email": str, "password": str} 형태의 자격증명 딕셔너리.

    Raises:
        KeyError: accounts.json에 등록되지 않은 계정명인 경우.
        RuntimeError: 대응하는 비밀번호 환경변수가 설정되지 않은 경우(.env 확인 필요).
    """
    with open(_ACCOUNTS_FILE, encoding="utf-8") as f:
        accounts = json.load(f)

    if name not in accounts:
        raise KeyError(f"등록되지 않은 계정명: {name}")

    email = accounts[name]["email"]
    password_env_key = f"{name.upper()}_PASSWORD"
    password = os.environ.get(password_env_key)

    if not password:
        raise RuntimeError(
            f"{password_env_key} 환경변수가 설정되지 않았습니다(.env 확인 필요)"
        )

    return {"email": email, "password": password}
