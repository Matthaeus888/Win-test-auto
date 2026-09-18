# docs_sync

`prd-agent` / `roadmap-agent`가 Google Docs API를 직접 호출하지 않고, 이 독립 모듈을 통해서만
PRD/Roadmap을 Google Doc에 반영하도록 하기 위한 연동 모듈입니다. 서비스 계정 +
Google Docs API(google-api-python-client) 방식을 사용합니다.

`scripts/sheets_sync`(TC/Judge, 표 형태 데이터)와는 별도 모듈입니다. PRD/Roadmap은 서술형
Markdown 문서이므로, append/행 단위 동기화가 아니라 **Doc 본문 전체를 로컬 승인 문서 내용으로
덮어쓰는 단방향 동기화**로 동작합니다.

## 설계 원칙

- **단방향(로컬 → Doc)**: `docs/prd/*.md`, `docs/roadmap/ROADMAP.md`가 Source of Truth입니다.
  Doc에서 값을 읽어와 로컬 문서에 반영하는 기능은 없습니다 — Doc은 공유/열람용 사본입니다.
- **전체 교체**: 매 sync마다 Doc 본문 전체를 삭제하고 새로 삽입합니다. Doc에서 직접 편집한
  내용이 있다면 다음 sync 시 사라집니다.
- **최소 구현**: 마크다운을 Google Docs의 실제 서식(제목 스타일, 표 등)으로 변환하지 않고
  원문 텍스트를 그대로 삽입합니다. 서식이 필요하면 Doc을 연 뒤 수동으로 조정하거나, 이 모듈을
  확장해야 합니다.
- **인증정보 미포함**: 서비스 계정 키, Doc ID 등은 코드에 하드코딩하지 않고 환경변수로만
  전달받습니다. `.env`는 `.gitignore`에 포함되어 있어 커밋되지 않습니다.

## 설정 방법

### 1. Google Cloud 설정

1. Google Cloud Console에서 프로젝트를 선택(또는 생성)하고 **Google Docs API**를 활성화합니다
   (`scripts/sheets_sync`에서 이미 서비스 계정을 만들어 Sheets API를 활성화했다면, 같은
   프로젝트에서 Docs API만 추가로 활성화하면 됩니다).
2. 서비스 계정 키는 `scripts/sheets_sync`와 **공유**합니다(`GOOGLE_SERVICE_ACCOUNT_FILE` 동일).
   새로 만들 필요 없습니다.
3. PRD용 Google Doc, Roadmap용 Google Doc을 각각 새로 만들고, 두 문서 모두의 공유 설정에서
   서비스 계정 이메일을 **편집자**로 추가합니다.

### 2. 환경변수 설정

| 환경변수 | 필수 | 설명 |
|---|---|---|
| `GOOGLE_SERVICE_ACCOUNT_FILE` | 필수 | 서비스 계정 키 JSON 파일 경로 (sheets_sync와 공용) |
| `GOOGLE_PRD_DOC_ID` | 필수 (`prd-sync`용) | PRD를 반영할 Google Doc ID (URL의 `/d/{ID}/edit` 부분) |
| `GOOGLE_ROADMAP_DOC_ID` | 필수 (`roadmap-sync`용) | Roadmap을 반영할 Google Doc ID |

### 3. Python 의존성 설치

```bash
pip install -r scripts/docs_sync/requirements.txt
```

## 사용법

```bash
# 실제로 쓰지 않고 몇 글자가 반영될지만 미리 확인
python scripts/docs_sync/docs_sync.py prd-sync --input docs/prd/project-prd.md --dry-run

# 승인된 PRD로 Google Doc 본문 전체를 덮어쓴다
python scripts/docs_sync/docs_sync.py prd-sync --input docs/prd/project-prd.md

# 승인된 Roadmap으로 Google Doc 본문 전체를 덮어쓴다
python scripts/docs_sync/docs_sync.py roadmap-sync --input docs/roadmap/ROADMAP.md
```
