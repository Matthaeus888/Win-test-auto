# sheets_sync

`tc-agent`가 Google Spreadsheet를 직접 제어하지 않고, 이 독립 모듈을 통해서만 TC를 읽고
추가하도록 하기 위한 연동 모듈입니다. 서비스 계정 + Google Sheets API(gspread) 방식을
사용합니다.

## 설계 원칙

- **append-only**: 이 모듈은 조회(`list`)와 추가(`append`)만 제공합니다. 기존 행을 수정하거나
  삭제하는 기능은 의도적으로 구현하지 않았습니다.
- **인증정보 미포함**: 서비스 계정 키, Sheet ID 등은 코드에 하드코딩하지 않고 환경변수로만
  전달받습니다. `.env` 파일은 `.gitignore`에 포함되어 있어 커밋되지 않습니다.
- **중복 방지**: `append` 실행 시 시트에 이미 존재하는 TC ID와 충돌하면 기본적으로 추가를
  거부합니다.
- **현재 상태**: 이 모듈은 구조와 인터페이스만 구성된 상태이며, 실제 서비스 계정 인증정보는
  아직 연결되어 있지 않습니다. 실사용 전 아래 "설정 방법"을 따라 준비가 필요합니다.

## 설정 방법

### 1. Google Cloud 서비스 계정 준비

1. Google Cloud Console에서 프로젝트를 선택(또는 생성)하고 Google Sheets API를 활성화합니다.
2. 서비스 계정을 생성하고 JSON 키를 발급받습니다.
3. **최소 권한 원칙**: 이 서비스 계정에는 프로젝트 전체 권한이 아니라, TC를 기록할 대상
   Google Spreadsheet 문서 하나에 대해서만 "편집자" 권한으로 공유해야 합니다(Spreadsheet의
   공유 설정에서 서비스 계정 이메일 주소를 편집자로 추가).
4. 발급받은 JSON 키 파일은 이 저장소 바깥의 안전한 위치에 저장하거나, 저장소 내부에 두는 경우
   반드시 `.gitignore`에 포함되어 있는지 확인합니다(현재 프로젝트 루트 `.gitignore`에
   `*-credentials.json`, `service-account*.json` 패턴이 포함되어 있습니다).

### 2. 환경변수 설정

프로젝트 루트의 `.env.example`을 복사해 `.env`를 만들고 값을 채웁니다.

```bash
cp .env.example .env
```

| 환경변수 | 필수 | 설명 |
|---|---|---|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | 필수 | 서비스 계정 키 JSON 파일의 로컬 경로 (TC/Candidate 공통) |
| `GOOGLE_SHEET_ID` | 필수 (`list`/`append`용) | TC를 기록할 대상 Spreadsheet ID (URL의 `/d/{ID}/edit` 부분) |
| `GOOGLE_WORKSHEET_NAME` | 선택 (기본값 `TC`) | TC를 기록할 워크시트(탭) 이름 |
| `GOOGLE_CANDIDATE_SHEET_ID` | 필수 (`candidate-*`용) | Automation Candidate 평가를 기록할 Spreadsheet ID. **`GOOGLE_SHEET_ID`와는 별개의 Spreadsheet 문서**여야 합니다(같은 문서의 다른 탭이 아님) |
| `GOOGLE_CANDIDATE_WORKSHEET_NAME` | 선택 (기본값 `Automation Candidates`) | `GOOGLE_CANDIDATE_SHEET_ID` 안에서 Automation Candidate 평가를 기록할 워크시트(탭) 이름 |

`.env`는 셸에서 직접 로드하거나(`export $(grep -v '^#' .env | xargs)` 등), 프로젝트에서 사용 중인
방식에 맞춰 로드한 뒤 아래 명령을 실행합니다.

### 3. Python 의존성 설치

```bash
pip install -r scripts/sheets_sync/requirements.txt
```

## 사용법

```bash
# 기존 TC 전체 조회 (중복 확인용)
python scripts/sheets_sync/sheets_sync.py list

# docs/tc/{feature}.md의 TC 표를 실제로 쓰지 않고 미리보기
python scripts/sheets_sync/sheets_sync.py append --input docs/tc/login-logout.md --dry-run

# 사용자 승인을 받은 TC를 실제로 시트 맨 아래에 추가
python scripts/sheets_sync/sheets_sync.py append --input docs/tc/login-logout.md
```

`append`는 시트에 이미 존재하는 TC ID와 충돌하면 기본적으로 실패합니다. 의도된 상황이 아니라면
ID naming을 다시 확인하세요.

## Automation Candidate Spreadsheet

`automation-candidate-agent`가 사용하는 **별도 Google Spreadsheet 문서**입니다(`GOOGLE_SHEET_ID`
의 TC 시트와 같은 문서의 다른 탭이 아니라, `GOOGLE_CANDIDATE_SHEET_ID`로 지정하는 완전히 다른
문서). 이 문서/워크시트만 예외적으로 "AI 작성 컬럼(TC ID, 6개 평가 점수, Automation Score,
Candidate, 선정/제외 사유)"을 재평가 시 업데이트할 수 있는 `candidate-sync` 명령을 제공합니다.
이 update는 항상 AI 작성 컬럼 범위로만 제한되며, 사용자가 Sheet에서 직접 입력하는 `QA Decision`
/ `QA Comment` 컬럼은 이 모듈의 어떤 명령으로도 절대 쓰지 않습니다(조회만 가능).

TC 시트와 마찬가지로 이 Spreadsheet 문서도 서비스 계정에 "편집자" 권한으로 공유되어 있어야
합니다(위 "1. Google Cloud 서비스 계정 준비" 참조 — 대상 문서만 다를 뿐 설정 절차는 동일).

`QA Decision` 컬럼에 입력 가능한 값은 정확히 `Approved` / `Rejected` / `Hold` 세 가지뿐입니다
(대소문자·공백까지 정확히 일치해야 함). `candidate-create-worksheet`로 워크시트를 처음 생성할 때
이 세 값만 선택할 수 있는 Dropdown(Data Validation)을 QA Decision 컬럼에 자동으로 적용합니다
(gspread 버전에 따라 적용에 실패할 수 있으며, 실패해도 워크시트 생성 자체는 계속 진행됩니다 —
최종 검증은 `automation-candidate-agent`의 Validation이 담당합니다). 이 워크시트를 삭제 후 다시
만들지 않는 한 기존 워크시트에는 소급 적용되지 않습니다.

```bash
# 최초 1회, Candidate 워크시트가 없을 때만 생성 (이미 있으면 에러로 중단)
python scripts/sheets_sync/sheets_sync.py candidate-create-worksheet

# Candidate 문서의 AI 평가 결과 표만 파싱해 Sheet에 반영 (신규 TC는 추가, 기존 TC는 AI 컬럼만 갱신)
python scripts/sheets_sync/sheets_sync.py candidate-sync \
    --input docs/tc/automation-candidates/login-logout.md --dry-run

# 실제로 반영
python scripts/sheets_sync/sheets_sync.py candidate-sync \
    --input docs/tc/automation-candidates/login-logout.md

# QA Decision/QA Comment를 포함한 Candidate 워크시트 전체 조회 (사용자 입력 반영, 확정 전 Validation용)
python scripts/sheets_sync/sheets_sync.py candidate-list
```

## 입력 TC 파일 형식

`docs/tc/{feature}.md` 안에 아래와 같은 파이프 마크다운 표가 있어야 합니다(컬럼 순서 고정,
`tc-writing` Skill의 컬럼 정의와 동일).

```
| ID | Requirement ID | Feature | Test Scenario | Preconditions | Test Steps | Expected Result | Priority | Result |
|---|---|---|---|---|---|---|---|---|
| TC-LOGIN-LOGOUT-001 | REQ-LOGIN-LOGOUT-003 | 로그인/로그아웃 | ... | ... | ... | ... | P0 | |
```
