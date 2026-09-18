"""Google Docs 연동 모듈 (Docs 연동 전용, PRD/Roadmap 작성 규칙/Workflow는 담당하지 않음).

이 모듈은 prd-agent / roadmap-agent가 직접 Google Docs API를 호출하지 않고, 이 스크립트를
통해서만 Google Doc을 읽고/쓰도록 하기 위한 독립 모듈이다.

설계 원칙 (qa-process 프로젝트 CLAUDE.md 17절 Security/Secret 관리 원칙과 일치):
- 인증정보(서비스 계정 키 등)는 코드에 하드코딩하지 않고 환경변수로만 받는다. 서비스 계정 키
  파일은 scripts/sheets_sync와 공용(GOOGLE_SERVICE_ACCOUNT_FILE).
- 로컬 승인 문서(docs/prd/*.md, docs/roadmap/ROADMAP.md)를 Source of Truth로 삼는다. 이
  모듈은 그 내용으로 Google Doc 본문 전체를 덮어쓰는 단방향(로컬 → Doc) 동기화만 제공하며,
  Doc에서 값을 읽어와 로컬 문서에 반영하는 기능은 없다 — Doc은 공유/열람용 사본일 뿐이다.
- **최소 구현**: 마크다운을 Google Docs의 실제 서식(제목 스타일, 표 등)으로 변환하지 않고,
  원문 텍스트를 그대로 삽입한다. 서식 변환이 필요해지면 별도로 확장한다.
- 이 스크립트는 사용자 승인 이후에만 Agent가 호출해야 한다. 승인 여부 판단은 이 모듈의 책임이
  아니다.

필요 환경변수:
- GOOGLE_SERVICE_ACCOUNT_FILE: 서비스 계정 키(JSON) 파일 경로 (sheets_sync와 공용)
- GOOGLE_PRD_DOC_ID: PRD를 동기화할 대상 Google Doc의 ID (URL의 /d/{ID}/edit 부분). prd-sync가
  사용한다.
- GOOGLE_ROADMAP_DOC_ID: Roadmap을 동기화할 대상 Google Doc의 ID. roadmap-sync가 사용한다.

필요 라이브러리 (requirements.txt 참조): google-api-python-client, google-auth

사용 예시:
    # 실제로 쓰지 않고 몇 글자가 반영될지만 미리 확인
    python docs_sync.py prd-sync --input ../../docs/prd/project-prd.md --dry-run

    # 승인된 PRD로 Google Doc 본문 전체를 덮어쓴다
    python docs_sync.py prd-sync --input ../../docs/prd/project-prd.md

    # 승인된 Roadmap으로 Google Doc 본문 전체를 덮어쓴다
    python docs_sync.py roadmap-sync --input ../../docs/roadmap/ROADMAP.md

주의: 서비스 계정 인증정보가 설정되기 전까지는 --dry-run 없이 실행하면 인증 단계에서 명확한
에러 메시지와 함께 실패한다.
"""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass


class DocsSyncError(RuntimeError):
    """이 모듈에서 발생하는 예외를 명확히 구분하기 위한 최상위 예외 타입."""


@dataclass
class DocConfig:
    service_account_file: str
    doc_id: str
    doc_id_env_name: str


def _config_from_env(doc_id_env_name: str) -> DocConfig:
    service_account_file = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE")
    doc_id = os.environ.get(doc_id_env_name)

    missing = [
        name
        for name, value in [
            ("GOOGLE_SERVICE_ACCOUNT_FILE", service_account_file),
            (doc_id_env_name, doc_id),
        ]
        if not value
    ]
    if missing:
        raise DocsSyncError(
            "다음 환경변수가 설정되지 않았습니다: "
            + ", ".join(missing)
            + ". .env.example을 참고해 .env 파일을 준비하거나 환경변수를 export 하세요."
        )
    return DocConfig(
        service_account_file=service_account_file,
        doc_id=doc_id,
        doc_id_env_name=doc_id_env_name,
    )


def _build_docs_service(service_account_file: str):
    """google-api-python-client로 Google Docs API 서비스 객체를 생성한다.

    실제 네트워크/인증 호출은 발생하지 않으며, 각 명령의 batchUpdate/get 호출 시점에 발생한다.
    """
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise DocsSyncError(
            "google-api-python-client / google-auth 패키지가 설치되어 있지 않습니다. "
            "requirements.txt를 참고해 `pip install -r requirements.txt`를 먼저 실행하세요."
        ) from exc

    if not os.path.isfile(service_account_file):
        raise DocsSyncError(f"서비스 계정 키 파일을 찾을 수 없습니다: {service_account_file}")

    scopes = ["https://www.googleapis.com/auth/documents"]
    credentials = Credentials.from_service_account_file(
        service_account_file, scopes=scopes
    )
    return build("docs", "v1", credentials=credentials, cache_discovery=False)


def _read_markdown(input_path: str) -> str:
    if not os.path.isfile(input_path):
        raise DocsSyncError(f"입력 파일을 찾을 수 없습니다: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        return f.read()


def sync_doc_from_markdown(
    config: DocConfig, input_path: str, dry_run: bool = False
) -> dict:
    """로컬 Markdown 파일 전체 내용으로 Google Doc 본문을 덮어쓴다(append가 아니라 전체 교체).

    기존 본문이 있으면 전부 삭제한 뒤 새 내용을 처음부터 삽입한다. Doc 쪽에서만 발생한 변경
    (예: 사용자가 Doc에서 직접 편집한 내용)은 이 sync로 인해 사라진다 — 이 모듈은 로컬 Markdown을
    Source of Truth로 간주하기 때문이다.
    """
    markdown_text = _read_markdown(input_path)
    if not markdown_text.strip():
        raise DocsSyncError("동기화할 문서 내용이 비어 있습니다 (입력 파일이 비어 있음).")

    if dry_run:
        return {
            "action": "dry-run",
            "doc_id": config.doc_id,
            "chars": len(markdown_text),
        }

    service = _build_docs_service(config.service_account_file)

    try:
        doc = service.documents().get(documentId=config.doc_id).execute()
    except Exception as exc:  # noqa: BLE001 - Google API 예외를 그대로 감싸서 재발생
        raise DocsSyncError(
            f"Google Doc(ID: {config.doc_id})을 열 수 없습니다: {exc}\n"
            f"{config.doc_id_env_name} 값과 서비스 계정 공유(편집자) 설정을 확인하세요."
        ) from exc

    content = doc.get("body", {}).get("content", [])
    end_index = content[-1].get("endIndex", 1) if content else 1

    requests: list[dict] = []
    # 본문에 삭제할 내용이 있을 때만 deleteContentRange를 추가한다(빈 range는 API 오류가 됨).
    if end_index > 2:
        requests.append(
            {"deleteContentRange": {"range": {"startIndex": 1, "endIndex": end_index - 1}}}
        )
    requests.append({"insertText": {"location": {"index": 1}, "text": markdown_text}})

    service.documents().batchUpdate(
        documentId=config.doc_id, body={"requests": requests}
    ).execute()

    return {"action": "synced", "doc_id": config.doc_id, "chars": len(markdown_text)}


def _cmd_prd_sync(args: argparse.Namespace) -> None:
    config = _config_from_env("GOOGLE_PRD_DOC_ID")
    result = sync_doc_from_markdown(config, args.input, dry_run=args.dry_run)
    print(f"[{result['action']}] PRD Doc({result['doc_id']}) - {result['chars']}자 반영")


def _cmd_roadmap_sync(args: argparse.Namespace) -> None:
    config = _config_from_env("GOOGLE_ROADMAP_DOC_ID")
    result = sync_doc_from_markdown(config, args.input, dry_run=args.dry_run)
    print(f"[{result['action']}] Roadmap Doc({result['doc_id']}) - {result['chars']}자 반영")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Google Docs 연동 (PRD/Roadmap 전용, sheets_sync와 별도 모듈)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prd_sync_parser = subparsers.add_parser(
        "prd-sync",
        help="승인된 PRD Markdown 전체로 GOOGLE_PRD_DOC_ID Doc 본문을 덮어쓴다",
    )
    prd_sync_parser.add_argument("--input", required=True, help="PRD Markdown 파일 경로")
    prd_sync_parser.add_argument(
        "--dry-run", action="store_true", help="실제로 쓰지 않고 반영될 글자 수만 확인"
    )
    prd_sync_parser.set_defaults(func=_cmd_prd_sync)

    roadmap_sync_parser = subparsers.add_parser(
        "roadmap-sync",
        help="승인된 Roadmap Markdown 전체로 GOOGLE_ROADMAP_DOC_ID Doc 본문을 덮어쓴다",
    )
    roadmap_sync_parser.add_argument(
        "--input", required=True, help="Roadmap Markdown 파일 경로"
    )
    roadmap_sync_parser.add_argument(
        "--dry-run", action="store_true", help="실제로 쓰지 않고 반영될 글자 수만 확인"
    )
    roadmap_sync_parser.set_defaults(func=_cmd_roadmap_sync)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except DocsSyncError as exc:
        print(f"에러: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
