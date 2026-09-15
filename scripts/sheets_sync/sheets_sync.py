"""Google Sheets 연동 모듈 (Sheets 연동 전용, TC 작성 규칙/Workflow는 담당하지 않음).

이 모듈은 tc-agent / automation-candidate-agent가 직접 Google Sheets API를 호출하지 않고,
이 스크립트를 통해서만 Spreadsheet를 읽고/쓰도록 하기 위한 독립 모듈이다.

설계 원칙 (qa-process 프로젝트 CLAUDE.md 17절 Security/Secret 관리 원칙과 일치):
- 인증정보(서비스 계정 키 등)는 코드에 하드코딩하지 않고 환경변수로만 받는다.
- TC 시트(list/append)는 append(추가)와 list(조회)만 제공하며, update/delete(수정/삭제) 기능은
  제공하지 않는다. 기존 TC를 임의로 덮어쓰거나 삭제하는 경로 자체를 코드 수준에서 만들지 않기
  위함이다.
- append 실행 전, 대상 시트에 이미 존재하는 TC ID와 충돌하는지 확인하고, 충돌 시 기본적으로
  추가를 거부한다(--force 플래그로만 우회 가능하게 하여 실수로 인한 중복 삽입을 방지한다).
- Candidate 시트(candidate-sync/candidate-list)는 automation-candidate-agent의 "AI 작성
  영역 / 사용자 작성 영역 분리" 요구를 충족하기 위한 예외적인 update 경로를 하나만 제공한다.
  이 update는 AI 작성 컬럼(TC ID, 6개 평가 점수, Automation Score, Candidate, 선정/제외 사유)
  범위로만 제한되며, 사용자 작성 컬럼(QA Decision, QA Comment)은 이 모듈의 어떤 명령으로도
  절대 쓰지 않는다(읽기만 가능).
- 이 스크립트는 사용자 승인 이후에만 Agent가 호출해야 한다. 승인 여부 판단은 이 모듈의
  책임이 아니다.

필요 환경변수:
- GOOGLE_SERVICE_ACCOUNT_FILE: 서비스 계정 키(JSON) 파일 경로 (TC/Candidate 공통)
- GOOGLE_SHEET_ID: TC를 기록할 대상 Google Spreadsheet의 ID (URL의 /d/{ID}/ 부분). list/append
  명령이 사용한다.
- GOOGLE_WORKSHEET_NAME: (선택) TC를 기록할 워크시트(탭) 이름. 기본값 "TC"
- GOOGLE_CANDIDATE_SHEET_ID: Automation Candidate 평가를 기록할 Google Spreadsheet의 ID.
  GOOGLE_SHEET_ID와는 **별개의 Spreadsheet 문서**를 가리켜야 한다(같은 문서의 다른 탭이
  아님). candidate-* 명령이 사용한다.
- GOOGLE_CANDIDATE_WORKSHEET_NAME: (선택) GOOGLE_CANDIDATE_SHEET_ID 안에서 Automation
  Candidate 평가를 기록할 워크시트(탭) 이름. 기본값 "Automation Candidates"

필요 라이브러리 (requirements.txt 참조): gspread, google-auth

사용 예시:
    # 기존 TC 조회 (중복 확인용)
    python sheets_sync.py list

    # docs/tc/{feature}.md의 TC 표를 파싱해 실제로 추가하지 않고 미리보기만
    python sheets_sync.py append --input ../../docs/tc/login-logout.md --dry-run

    # 실제로 Spreadsheet 맨 아래에 추가 (승인된 TC에 대해서만 실행)
    python sheets_sync.py append --input ../../docs/tc/login-logout.md

    # Automation Candidate 워크시트가 없을 때 최초 1회 생성
    python sheets_sync.py candidate-create-worksheet

    # Candidate 문서의 AI 작성 영역만 Sheet에 동기화 (QA Decision/QA Comment는 건드리지 않음)
    python sheets_sync.py candidate-sync --input ../../docs/tc/automation-candidates/login-logout.md

    # Candidate 워크시트 전체 조회 (QA Decision/QA Comment 포함, Validation/재조회용)
    python sheets_sync.py candidate-list

주의: 이 스크립트는 구조와 인터페이스를 제공하는 것이 목적이며, 실제 서비스 계정 인증정보가
설정되기 전까지는 --dry-run 없이 실행하면 인증 단계에서 명확한 에러 메시지와 함께 실패한다.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass

TC_COLUMNS = [
    "ID",
    "Requirement ID",
    "Feature",
    "Test Scenario",
    "Preconditions",
    "Test Steps",
    "Expected Result",
    "Priority",
    "Result",
]

# Automation Candidate 워크시트 컬럼. AI 작성 영역과 사용자(QA) 작성 영역을 명확히 분리한다.
# - AI 작성 영역: automation-candidate-agent가 automation-candidate Skill 기준으로 채우는
#   평가 결과. candidate-sync 명령은 이 범위(컬럼 1~10)만 쓴다.
# - 사용자 작성 영역: QA가 Google Sheet에서 직접 입력하는 최종 판단. 이 모듈의 어떤 명령도
#   이 두 컬럼에는 쓰지 않는다(읽기 전용).
CANDIDATE_AI_COLUMNS = [
    "TC ID",
    "Business Criticality",
    "Regression Frequency",
    "Automation Stability",
    "Result Determinism",
    "Manual Test Cost",
    "Maintenance Cost",
    "Automation Score",
    "Candidate (AI)",
    "선정/제외 사유",
]
CANDIDATE_USER_COLUMNS = ["QA Decision", "QA Comment"]
CANDIDATE_COLUMNS = CANDIDATE_AI_COLUMNS + CANDIDATE_USER_COLUMNS

# QA Decision 허용값: 정확히 "Approved" / "Rejected" / "Hold" 세 값만 유효하다(대소문자·공백까지
# 정확히 일치해야 함). 빈 값은 오류가 아니라 "미검토" 상태를 뜻한다. 이 값들에 대한 검증/보정 로직은
# 이 모듈이 아니라 automation-candidate-agent의 Validation 책임이다 — 이 모듈은 Sheet에 Dropdown
# (Data Validation)을 걸어 잘못된 값이 애초에 입력되지 않도록 돕는 역할만 한다.
QA_DECISION_VALUES = ["Approved", "Rejected", "Hold"]

DEFAULT_CANDIDATE_WORKSHEET_NAME = "Automation Candidates"


class SheetsSyncError(RuntimeError):
    """이 모듈에서 발생하는 예외를 명확히 구분하기 위한 최상위 예외 타입."""


@dataclass
class SheetsConfig:
    service_account_file: str
    sheet_id: str
    worksheet_name: str

    @classmethod
    def from_env(cls) -> "SheetsConfig":
        service_account_file = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
        sheet_id = os.environ.get("GOOGLE_SHEET_ID")
        worksheet_name = os.environ.get("GOOGLE_WORKSHEET_NAME", "TC")

        missing = [
            name
            for name, value in [
                ("GOOGLE_SERVICE_ACCOUNT_FILE", service_account_file),
                ("GOOGLE_SHEET_ID", sheet_id),
            ]
            if not value
        ]
        if missing:
            raise SheetsSyncError(
                "다음 환경변수가 설정되지 않았습니다: "
                + ", ".join(missing)
                + ". .env.example을 참고해 .env 파일을 준비하거나 환경변수를 export 하세요."
            )
        return cls(
            service_account_file=service_account_file,
            sheet_id=sheet_id,
            worksheet_name=worksheet_name,
        )

    @classmethod
    def from_candidate_env(cls) -> "SheetsConfig":
        """Automation Candidate 평가 전용 설정을 읽는다.

        GOOGLE_SHEET_ID(TC를 기록하는 기존 Spreadsheet)와는 별개의 Google Spreadsheet
        (GOOGLE_CANDIDATE_SHEET_ID)를 사용한다 — 같은 문서의 다른 탭이 아니라 완전히 다른
        Spreadsheet 문서에 연동하기 위함이다. 서비스 계정 키는 두 연동이 같은 값을 공유한다.
        """
        service_account_file = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
        sheet_id = os.environ.get("GOOGLE_CANDIDATE_SHEET_ID")
        worksheet_name = os.environ.get(
            "GOOGLE_CANDIDATE_WORKSHEET_NAME", DEFAULT_CANDIDATE_WORKSHEET_NAME
        )

        missing = [
            name
            for name, value in [
                ("GOOGLE_SERVICE_ACCOUNT_FILE", service_account_file),
                ("GOOGLE_CANDIDATE_SHEET_ID", sheet_id),
            ]
            if not value
        ]
        if missing:
            raise SheetsSyncError(
                "다음 환경변수가 설정되지 않았습니다: "
                + ", ".join(missing)
                + ". .env.example을 참고해 .env 파일을 준비하거나 환경변수를 export 하세요."
            )
        return cls(
            service_account_file=service_account_file,
            sheet_id=sheet_id,
            worksheet_name=worksheet_name,
        )


def _open_worksheet(config: SheetsConfig, worksheet_name: str | None = None):
    """gspread 클라이언트로 대상 워크시트를 연다. 실제 네트워크/인증 호출이 발생하는 지점.

    worksheet_name을 지정하지 않으면 config.worksheet_name(TC 워크시트)을 연다. Candidate
    워크시트 등 다른 탭을 열 때는 worksheet_name을 명시적으로 넘긴다.
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as exc:
        raise SheetsSyncError(
            "gspread / google-auth 패키지가 설치되어 있지 않습니다. "
            "requirements.txt를 참고해 `pip install -r requirements.txt`를 먼저 실행하세요."
        ) from exc

    if not os.path.isfile(config.service_account_file):
        raise SheetsSyncError(
            f"서비스 계정 키 파일을 찾을 수 없습니다: {config.service_account_file}"
        )

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials = Credentials.from_service_account_file(
        config.service_account_file, scopes=scopes
    )
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_key(config.sheet_id)

    name = worksheet_name or config.worksheet_name
    try:
        worksheet = spreadsheet.worksheet(name)
    except gspread.exceptions.WorksheetNotFound as exc:
        raise SheetsSyncError(
            f"워크시트 '{name}'을(를) 찾을 수 없습니다. "
            "GOOGLE_WORKSHEET_NAME/GOOGLE_CANDIDATE_WORKSHEET_NAME 환경변수 또는 실제 시트 탭 "
            "이름을 확인하세요. Candidate 워크시트가 아직 없다면 candidate-create-worksheet "
            "명령으로 먼저 생성해야 합니다."
        ) from exc

    return worksheet


def _ensure_header(worksheet, columns: list[str] = TC_COLUMNS) -> None:
    """워크시트 첫 행이 columns와 동일한 순서인지 확인한다.

    헤더가 없으면(빈 시트) 새로 기록하고, 헤더가 있는데 컬럼 구성이 다르면 에러로 중단한다
    (기존 데이터 구조를 임의로 바꾸지 않기 위함).
    """
    first_row = worksheet.row_values(1)
    if not first_row:
        worksheet.append_row(columns, value_input_option="RAW")
        return
    if first_row != columns:
        raise SheetsSyncError(
            "시트의 헤더 컬럼이 기대값과 다릅니다. "
            f"시트 헤더: {first_row} / 기대값: {columns}. "
            "컬럼 구성이 다른 시트에는 자동으로 쓰지 않습니다 — 시트 또는 컬럼 정의를 먼저 맞추세요."
        )


def _colnum_to_letter(n: int) -> str:
    """1부터 시작하는 컬럼 번호를 A1 표기 열 문자로 변환한다(1 -> A, 10 -> J)."""
    letters = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def list_existing_tcs(config: SheetsConfig) -> list[dict]:
    """기존 TC를 전부 읽어 dict 리스트로 반환한다. 중복 확인 등에 사용."""
    worksheet = _open_worksheet(config)
    _ensure_header(worksheet)
    records = worksheet.get_all_records(expected_headers=TC_COLUMNS)
    return records


def _open_spreadsheet(config: SheetsConfig):
    """워크시트(탭)가 아닌 Spreadsheet(문서) 자체를 연다. 탭 목록 조회/생성에 사용."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as exc:
        raise SheetsSyncError(
            "gspread / google-auth 패키지가 설치되어 있지 않습니다. "
            "requirements.txt를 참고해 `pip install -r requirements.txt`를 먼저 실행하세요."
        ) from exc

    if not os.path.isfile(config.service_account_file):
        raise SheetsSyncError(
            f"서비스 계정 키 파일을 찾을 수 없습니다: {config.service_account_file}"
        )

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file(
        config.service_account_file, scopes=scopes
    )
    client = gspread.authorize(credentials)
    return client.open_by_key(config.sheet_id)


def list_worksheets(config: SheetsConfig) -> list[str]:
    """Spreadsheet에 존재하는 워크시트(탭) 이름 전체를 반환한다."""
    spreadsheet = _open_spreadsheet(config)
    return [ws.title for ws in spreadsheet.worksheets()]


def create_worksheet(
    config: SheetsConfig,
    worksheet_name: str | None = None,
    columns: list[str] = TC_COLUMNS,
    dry_run: bool = False,
) -> str:
    """새 워크시트(탭)를 생성하고 헤더 행을 columns로 채운다.

    worksheet_name을 지정하지 않으면 config.worksheet_name(TC 워크시트)을 생성한다. Candidate
    워크시트를 생성할 때는 worksheet_name과 columns(CANDIDATE_COLUMNS)를 명시적으로 넘긴다.

    - 이미 동일한 이름의 탭이 존재하면 실수로 인한 중복 생성을 막기 위해 에러로 중단한다
      (기존 탭을 임의로 재사용/덮어쓰지 않기 위함).
    - 이 함수는 새 탭을 만들고 헤더만 기록할 뿐, 다른 탭의 데이터에는 전혀 접근하지 않는다.
    """
    name = worksheet_name or config.worksheet_name
    spreadsheet = _open_spreadsheet(config)
    existing_titles = {ws.title for ws in spreadsheet.worksheets()}
    if name in existing_titles:
        raise SheetsSyncError(
            f"워크시트 '{name}'이(가) 이미 존재합니다. "
            "기존 탭을 임의로 재사용하지 않도록 생성을 중단합니다. "
            "다른 이름을 쓰거나, 기존 탭에 쓰려는 것이었는지 확인하세요."
        )

    if dry_run:
        return name

    worksheet = spreadsheet.add_worksheet(title=name, rows=100, cols=len(columns))
    worksheet.append_row(columns, value_input_option="RAW")
    return name


def _parse_tc_markdown_table(markdown_text: str) -> list[dict]:
    """docs/tc/{feature}.md 안의 TC 마크다운 표를 파싱해 TC_COLUMNS 순서의 dict 리스트로 반환한다.

    기대하는 표 형식 (파이프 구분 마크다운 표):
        | ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
        |---|---|---|---|---|---|---|---|---|
        | TC-XXX-001 | REQ-XXX-001 | ... |

    `tc-writing` Skill 4.6 규칙에 따라 하나의 문서 안에 "## TC 목록"(정상 케이스)과
    "## 결함 의심 항목" 등 여러 개의 TC 표가 존재할 수 있다. 이 함수는 특정 섹션 제목에
    의존하지 않고, 헤더 컬럼 구성이 TC_COLUMNS와 정확히 일치하는 표를 문서 전체에서 순서대로
    모두 찾아 각 표의 데이터 행을 이어붙여 반환한다(발견 순서 = 문서에 등장하는 순서).
    표가 하나뿐인 기존 문서(예: page-ui.md)에서도 동일하게 동작한다(하위 호환).
    """
    def split_row(line: str) -> list[str]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        return cells

    def unescape_cell(text: str) -> str:
        """마크다운 표 셀 안에서 개행 대신 쓰인 <br>을 실제 줄바꿈으로 되돌린다.

        마크다운 파이프 표는 셀 안에 실제 개행 문자를 담을 수 없어 TC 문서에서 Test Steps 등
        여러 줄인 값을 <br>로 표기한다. Google Sheets 셀은 실제 개행 문자를 지원하므로, 여기서
        복원해두지 않으면 시트에 "<br>"라는 리터럴 문자열이 그대로 들어간다.
        """
        return re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    lines = [line.rstrip() for line in markdown_text.splitlines()]

    # 문서 안에는 TC 목록 표 외에 "변경 이력" 등 다른 표도 존재할 수 있고, TC 표 자체도
    # "## TC 목록" / "## 결함 의심 항목" 등 여러 섹션에 나뉘어 존재할 수 있다. 특정 섹션
    # 제목에 의존하지 않고, 헤더가 정확히 TC_COLUMNS와 일치하는 표를 모두 찾는다.
    header_idxs = [
        idx
        for idx, line in enumerate(lines)
        if line.strip().startswith("|") and split_row(line) == TC_COLUMNS
    ]

    if not header_idxs:
        raise SheetsSyncError(
            "입력 파일에서 TC 마크다운 표(헤더가 TC_COLUMNS와 일치하는 표)를 찾을 수 없습니다.\n"
            f"기대하는 헤더: {TC_COLUMNS}"
        )

    # 각 header_idx + 1은 구분선(---) 행이므로 건너뛰고, 그 다음부터 "|"로 시작하지 않는
    # 첫 줄(표가 끝나는 지점) 전까지만 해당 표의 데이터 행으로 수집한다. 여러 표에서 나온
    # 행을 문서에 등장한 순서대로 이어붙인다.
    rows = []
    for header_idx in header_idxs:
        for line in lines[header_idx + 2 :]:
            if not line.strip().startswith("|"):
                break
            cells = split_row(line)
            if len(cells) != len(TC_COLUMNS):
                raise SheetsSyncError(f"컬럼 개수가 맞지 않는 행이 있습니다: {line}")
            cells = [unescape_cell(cell) for cell in cells]
            rows.append(dict(zip(TC_COLUMNS, cells)))
    return rows


def append_tcs_from_markdown(
    config: SheetsConfig, input_path: str, dry_run: bool = False, force: bool = False
) -> list[dict]:
    """마크다운 TC 표를 읽어 Spreadsheet 맨 아래에 추가한다. 기존 행은 절대 덮어쓰지 않는다."""
    with open(input_path, encoding="utf-8") as f:
        markdown_text = f.read()

    new_rows = _parse_tc_markdown_table(markdown_text)
    if not new_rows:
        raise SheetsSyncError("추가할 TC가 없습니다 (표에 데이터 행이 없음).")

    # 문서 내에 "## TC 목록"과 "## 결함 의심 항목" 등 여러 표가 존재하는 경우, 표를 합치는
    # 과정에서 동일 ID가 중복 등장하지 않는지 먼저 확인한다(문서 내부 중복). 시트와의 중복
    # 여부와 별개로, 파일 자체의 정합성 문제이므로 --force 여부와 무관하게 항상 에러로 중단한다.
    seen_ids: dict[str, int] = {}
    for row in new_rows:
        seen_ids[row["ID"]] = seen_ids.get(row["ID"], 0) + 1
    internal_duplicates = sorted(id_ for id_, count in seen_ids.items() if count > 1)
    if internal_duplicates:
        raise SheetsSyncError(
            "입력 파일 내부에 중복된 TC ID가 있습니다: "
            + ", ".join(internal_duplicates)
            + ". 문서 내 여러 표(TC 목록 / 결함 의심 항목 등)에서 ID가 겹치지 않는지 확인하세요."
        )

    existing = list_existing_tcs(config)
    existing_ids = {row.get("ID", "").strip() for row in existing if row.get("ID")}

    conflicting = [row["ID"] for row in new_rows if row["ID"] in existing_ids]
    if conflicting and not force:
        raise SheetsSyncError(
            "다음 TC ID가 이미 시트에 존재합니다: "
            + ", ".join(conflicting)
            + ". 기존 TC를 덮어쓰지 않도록 기본적으로 추가를 중단합니다. "
            "의도한 것이 맞다면 ID를 바꾸거나 --force를 명시적으로 지정하세요 "
            "(--force도 기존 행을 수정하지 않고 별도 행으로만 추가합니다)."
        )

    if dry_run:
        return new_rows

    worksheet = _open_worksheet(config)
    _ensure_header(worksheet)
    for row in new_rows:
        worksheet.append_row(
            [row[col] for col in TC_COLUMNS], value_input_option="RAW"
        )
    return new_rows


def _parse_candidate_markdown_table(markdown_text: str) -> list[dict]:
    """Candidate 문서("## AI 평가 결과" 표)를 파싱해 CANDIDATE_AI_COLUMNS 순서의 dict 리스트로
    반환한다.

    QA Decision / QA Comment 표(사용자 작성 영역)는 헤더가 CANDIDATE_AI_COLUMNS와 다르므로 이
    함수가 찾는 대상이 아니다 — AI 작성 영역만 이 함수로 파싱하고 Sheet로 올린다.
    """

    def split_row(line: str) -> list[str]:
        return [cell.strip() for cell in line.strip().strip("|").split("|")]

    def unescape_cell(text: str) -> str:
        return re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    lines = [line.rstrip() for line in markdown_text.splitlines()]

    header_idxs = [
        idx
        for idx, line in enumerate(lines)
        if line.strip().startswith("|") and split_row(line) == CANDIDATE_AI_COLUMNS
    ]

    if not header_idxs:
        raise SheetsSyncError(
            "입력 파일에서 AI 평가 결과 표(헤더가 CANDIDATE_AI_COLUMNS와 일치하는 표)를 찾을 수 "
            f"없습니다.\n기대하는 헤더: {CANDIDATE_AI_COLUMNS}"
        )

    rows = []
    for header_idx in header_idxs:
        for line in lines[header_idx + 2 :]:
            if not line.strip().startswith("|"):
                break
            cells = split_row(line)
            if len(cells) != len(CANDIDATE_AI_COLUMNS):
                raise SheetsSyncError(f"컬럼 개수가 맞지 않는 행이 있습니다: {line}")
            cells = [unescape_cell(cell) for cell in cells]
            rows.append(dict(zip(CANDIDATE_AI_COLUMNS, cells)))
    return rows


def list_candidates(config: SheetsConfig, worksheet_name: str | None = None) -> list[dict]:
    """Candidate 워크시트 전체(AI 작성 영역 + 사용자 작성 영역 QA Decision/QA Comment)를 조회한다.

    사용자가 Sheet에 입력한 QA Decision/QA Comment를 다시 읽어오거나(사용자 QA Decision 입력
    반영), 자동화 대상 확정 전 Validation을 위해 최신 상태를 재조회하는 용도로 사용한다.
    """
    worksheet = _open_worksheet(config, worksheet_name=worksheet_name)
    _ensure_header(worksheet, columns=CANDIDATE_COLUMNS)
    return worksheet.get_all_records(expected_headers=CANDIDATE_COLUMNS)


def sync_candidates_from_markdown(
    config: SheetsConfig,
    input_path: str,
    worksheet_name: str | None = None,
    dry_run: bool = False,
) -> dict:
    """Candidate 문서의 AI 작성 영역만 Sheet에 반영한다(append 또는 AI 컬럼만 update).

    - 시트에 없는 TC ID는 새 행으로 추가하고, QA Decision/QA Comment는 빈 값으로 둔다(사용자가
      나중에 입력).
    - 시트에 이미 있는 TC ID는 AI 작성 컬럼(1~len(CANDIDATE_AI_COLUMNS)) 범위만 덮어쓴다. 이
      범위를 벗어난 QA Decision/QA Comment 셀은 절대 읽지도 쓰지도 않는다 — 재평가로 AI 점수가
      바뀌어도 사용자가 이미 입력한 결정/코멘트는 그대로 보존된다.
    """
    with open(input_path, encoding="utf-8") as f:
        markdown_text = f.read()

    new_rows = _parse_candidate_markdown_table(markdown_text)
    if not new_rows:
        raise SheetsSyncError("동기화할 Candidate 평가 결과가 없습니다 (표에 데이터 행이 없음).")

    seen_ids: dict[str, int] = {}
    for row in new_rows:
        seen_ids[row["TC ID"]] = seen_ids.get(row["TC ID"], 0) + 1
    internal_duplicates = sorted(id_ for id_, count in seen_ids.items() if count > 1)
    if internal_duplicates:
        raise SheetsSyncError(
            "입력 파일 내부에 중복된 TC ID가 있습니다: " + ", ".join(internal_duplicates)
        )

    worksheet = _open_worksheet(config, worksheet_name=worksheet_name)
    _ensure_header(worksheet, columns=CANDIDATE_COLUMNS)

    existing_values = worksheet.get_all_values()
    # 1행은 헤더이므로 2행부터 실제 데이터. TC ID(1번 컬럼) -> 시트 행 번호(1-based) 매핑.
    existing_row_idx = {
        row[0]: idx
        for idx, row in enumerate(existing_values[1:], start=2)
        if row and row[0]
    }

    appended: list[str] = []
    updated: list[str] = []
    updates: list[tuple[int, list[str]]] = []
    appends: list[list[str]] = []

    last_col_letter = _colnum_to_letter(len(CANDIDATE_AI_COLUMNS))
    for row in new_rows:
        tc_id = row["TC ID"]
        ai_values = [row[col] for col in CANDIDATE_AI_COLUMNS]
        if tc_id in existing_row_idx:
            updates.append((existing_row_idx[tc_id], ai_values))
            updated.append(tc_id)
        else:
            appends.append(ai_values + ["", ""])  # QA Decision, QA Comment는 빈 값으로 시작
            appended.append(tc_id)

    if dry_run:
        return {"appended": appended, "updated": updated}

    for row_idx, ai_values in updates:
        worksheet.update(
            f"A{row_idx}:{last_col_letter}{row_idx}",
            [ai_values],
            value_input_option="RAW",
        )
    for row_values in appends:
        worksheet.append_row(row_values, value_input_option="RAW")

    return {"appended": appended, "updated": updated}


def _cmd_list(args: argparse.Namespace) -> None:
    config = SheetsConfig.from_env()
    records = list_existing_tcs(config)
    if not records:
        print("(기존 TC 없음 — 시트가 비어있거나 헤더만 존재합니다)")
        return
    for row in records:
        print(" | ".join(str(row.get(col, "")) for col in TC_COLUMNS))
    print(f"\n총 {len(records)}건")


def _cmd_list_worksheets(args: argparse.Namespace) -> None:
    config = SheetsConfig.from_env()
    titles = list_worksheets(config)
    for title in titles:
        marker = " (현재 GOOGLE_WORKSHEET_NAME)" if title == config.worksheet_name else ""
        print(f"{title}{marker}")
    print(f"\n총 {len(titles)}개 워크시트(탭)")


def _cmd_create_worksheet(args: argparse.Namespace) -> None:
    config = SheetsConfig.from_env()
    name = create_worksheet(config, dry_run=args.dry_run)
    action = "미리보기 (--dry-run, 실제로 생성하지 않음)" if args.dry_run else "생성 완료"
    print(f"[{action}] 워크시트 '{name}' (헤더: {TC_COLUMNS})")


def _apply_qa_decision_validation(worksheet) -> bool:
    """QA Decision 컬럼에 QA_DECISION_VALUES만 선택 가능한 Dropdown(Data Validation)을 건다.

    gspread 버전에 따라 add_validation을 지원하지 않거나 API 호출이 실패할 수 있으므로
    best-effort로 동작한다 — 실패해도 워크시트 생성 자체는 계속 진행하며, 이 함수는 성공 여부만
    bool로 반환한다(성공하지 않아도 automation-candidate-agent의 Validation이 최종 방어선이다).
    """
    try:
        from gspread.utils import ValidationConditionType

        qa_decision_col = CANDIDATE_COLUMNS.index("QA Decision") + 1
        col_letter = _colnum_to_letter(qa_decision_col)
        worksheet.add_validation(
            f"{col_letter}2:{col_letter}{worksheet.row_count}",
            ValidationConditionType.one_of_list,
            QA_DECISION_VALUES,
            strict=True,
            showCustomUi=True,
        )
        return True
    except Exception:
        return False


def _cmd_candidate_create_worksheet(args: argparse.Namespace) -> None:
    config = SheetsConfig.from_candidate_env()
    result_name = create_worksheet(
        config, columns=CANDIDATE_COLUMNS, dry_run=args.dry_run
    )
    action = "미리보기 (--dry-run, 실제로 생성하지 않음)" if args.dry_run else "생성 완료"
    print(f"[{action}] Candidate 워크시트 '{result_name}' (헤더: {CANDIDATE_COLUMNS})")
    if not args.dry_run:
        worksheet = _open_worksheet(config, worksheet_name=result_name)
        if _apply_qa_decision_validation(worksheet):
            print(
                f"[Dropdown 적용 완료] QA Decision 컬럼에 {QA_DECISION_VALUES} 값만 선택 "
                "가능한 Data Validation을 적용했습니다."
            )
        else:
            print(
                "[Dropdown 미적용] QA Decision 컬럼에 Data Validation을 적용하지 못했습니다"
                "(gspread 버전 또는 API 제약일 수 있음). 워크시트 생성 자체는 정상 완료되었으며, "
                "필요하면 Google Sheet에서 데이터 확인 > 드롭다운을 수동으로 설정할 수 있습니다."
            )


def _cmd_candidate_sync(args: argparse.Namespace) -> None:
    config = SheetsConfig.from_candidate_env()
    result = sync_candidates_from_markdown(config, args.input, dry_run=args.dry_run)
    action = "미리보기 (--dry-run, 실제로 쓰지 않음)" if args.dry_run else "동기화 완료"
    print(
        f"[{action}] 신규 추가 {len(result['appended'])}건, "
        f"AI 컬럼 갱신 {len(result['updated'])}건 (QA Decision/QA Comment는 건드리지 않음)"
    )
    if result["appended"]:
        print("  신규 추가: " + ", ".join(result["appended"]))
    if result["updated"]:
        print("  AI 컬럼 갱신: " + ", ".join(result["updated"]))


def _cmd_candidate_list(args: argparse.Namespace) -> None:
    config = SheetsConfig.from_candidate_env()
    records = list_candidates(config)
    if not records:
        print("(Candidate 워크시트에 데이터 없음)")
        return
    for row in records:
        print(" | ".join(str(row.get(col, "")) for col in CANDIDATE_COLUMNS))
    print(f"\n총 {len(records)}건")


def _cmd_append(args: argparse.Namespace) -> None:
    config = SheetsConfig.from_env()
    rows = append_tcs_from_markdown(
        config, args.input, dry_run=args.dry_run, force=args.force
    )
    action = "미리보기 (--dry-run, 실제로 쓰지 않음)" if args.dry_run else "추가 완료"
    print(f"[{action}] {len(rows)}건")
    for row in rows:
        print(" | ".join(str(row.get(col, "")) for col in TC_COLUMNS))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="기존 TC 전체 조회")
    list_parser.set_defaults(func=_cmd_list)

    list_ws_parser = subparsers.add_parser(
        "list-worksheets", help="Spreadsheet에 존재하는 워크시트(탭) 이름 전체 조회"
    )
    list_ws_parser.set_defaults(func=_cmd_list_worksheets)

    create_ws_parser = subparsers.add_parser(
        "create-worksheet",
        help="GOOGLE_WORKSHEET_NAME으로 새 워크시트(탭)를 생성하고 헤더 행을 기록",
    )
    create_ws_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제로 생성하지 않고 어떤 이름으로 생성될지만 확인",
    )
    create_ws_parser.set_defaults(func=_cmd_create_worksheet)

    append_parser = subparsers.add_parser(
        "append", help="docs/tc/{feature}.md의 승인된 TC를 시트에 추가"
    )
    append_parser.add_argument(
        "--input", required=True, help="TC 마크다운 표가 담긴 파일 경로"
    )
    append_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제로 쓰지 않고 무엇이 추가될지만 출력",
    )
    append_parser.add_argument(
        "--force",
        action="store_true",
        help="ID가 이미 존재해도 중단하지 않고 별도 행으로 추가 (기존 행은 여전히 수정하지 않음)",
    )
    append_parser.set_defaults(func=_cmd_append)

    candidate_create_ws_parser = subparsers.add_parser(
        "candidate-create-worksheet",
        help="GOOGLE_CANDIDATE_SHEET_ID 문서에 GOOGLE_CANDIDATE_WORKSHEET_NAME 워크시트를 "
        "생성하고 헤더 행(AI 작성 컬럼 + QA Decision/QA Comment)을 기록",
    )
    candidate_create_ws_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제로 생성하지 않고 어떤 이름으로 생성될지만 확인",
    )
    candidate_create_ws_parser.set_defaults(func=_cmd_candidate_create_worksheet)

    candidate_sync_parser = subparsers.add_parser(
        "candidate-sync",
        help="Candidate 문서의 AI 작성 영역만 Sheet에 동기화 (QA Decision/QA Comment는 보존)",
    )
    candidate_sync_parser.add_argument(
        "--input", required=True, help="Candidate 평가 결과 마크다운 파일 경로"
    )
    candidate_sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="실제로 쓰지 않고 신규 추가/갱신 대상만 미리 확인",
    )
    candidate_sync_parser.set_defaults(func=_cmd_candidate_sync)

    candidate_list_parser = subparsers.add_parser(
        "candidate-list",
        help="Candidate 워크시트 전체 조회 (QA Decision/QA Comment 포함)",
    )
    candidate_list_parser.set_defaults(func=_cmd_candidate_list)

    args = parser.parse_args()
    try:
        args.func(args)
    except SheetsSyncError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
