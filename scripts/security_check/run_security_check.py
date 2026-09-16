"""
Git Push 전에 사용자가 직접 확인하는 의존성 보안 점검 스크립트.

이 프로젝트는 Python 전용(automation, scripts/*)이라 pip-audit만 대상이며,
Node/npm 매니페스트(package.json)가 없어 npm audit은 적용하지 않는다.

이 스크립트는 어떤 Git 명령도 실행하지 않는다. Commit/Push 승인은
CLAUDE.md 14/18절에 따라 항상 사용자가 직접 결정하며, 이 스크립트는 그
결정을 돕는 리포트만 생성한다.
"""

import datetime
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = Path(__file__).resolve().parent / "reports"

REQUIREMENTS_FILES = [
    "automation/requirements.txt",
    "scripts/notify_slack/requirements.txt",
    "scripts/sheets_sync/requirements.txt",
]


def run_pip_audit(requirements_path: Path) -> dict:
    """지정한 requirements.txt에 대해 pip-audit을 실행하고 JSON 결과를 반환한다."""
    result = subprocess.run(
        [sys.executable, "-m", "pip_audit", "-r", str(requirements_path), "-f", "json"],
        capture_output=True,
        text=True,
    )
    try:
        payload = json.loads(result.stdout) if result.stdout.strip() else {"dependencies": []}
    except json.JSONDecodeError:
        payload = {"dependencies": [], "raw_stdout": result.stdout, "raw_stderr": result.stderr}
    payload["_returncode"] = result.returncode
    payload["_stderr"] = result.stderr
    return payload


def format_report(results: dict[str, dict]) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "# 의존성 보안 점검 리포트 (pip-audit)",
        "",
        f"- 생성 시각: {now}",
        "- 실행 도구: pip-audit",
        "- 대상: " + ", ".join(REQUIREMENTS_FILES),
        "",
        "이 리포트는 Git Push 여부를 자동으로 결정하지 않습니다. "
        "취약점 발견 시 조치 여부와 Push 승인은 사용자가 직접 판단합니다 (CLAUDE.md 14/18절).",
        "",
    ]

    total_vulns = 0
    for req_file, payload in results.items():
        lines.append(f"## {req_file}")
        lines.append("")

        if payload.get("_stderr") and payload.get("_returncode") not in (0, 1):
            lines.append(f"⚠️ 실행 오류: `{payload['_stderr'].strip()}`")
            lines.append("")
            continue

        deps_with_vulns = [
            dep for dep in payload.get("dependencies", []) if dep.get("vulns")
        ]

        if not deps_with_vulns:
            lines.append("✅ 알려진 취약점이 발견되지 않았습니다.")
            lines.append("")
            continue

        for dep in deps_with_vulns:
            name = dep.get("name")
            version = dep.get("version")
            for vuln in dep.get("vulns", []):
                total_vulns += 1
                vuln_id = vuln.get("id", "UNKNOWN")
                fix_versions = ", ".join(vuln.get("fix_versions", [])) or "없음"
                description = (vuln.get("description") or "").strip().splitlines()[0] if vuln.get("description") else ""
                lines.append(f"- ❌ `{name}=={version}` — **{vuln_id}**")
                lines.append(f"  - 수정 버전: {fix_versions}")
                if description:
                    lines.append(f"  - 설명: {description}")
        lines.append("")

    lines.insert(6, f"- 발견된 취약점 수: {total_vulns}")
    lines.insert(7, "")

    return "\n".join(lines), total_vulns


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    results = {}
    for rel_path in REQUIREMENTS_FILES:
        abs_path = REPO_ROOT / rel_path
        if not abs_path.exists():
            continue
        print(f"[pip-audit] {rel_path} 점검 중...")
        results[rel_path] = run_pip_audit(abs_path)

    report_text, total_vulns = format_report(results)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"security_report_{timestamp}.md"
    report_path.write_text(report_text, encoding="utf-8")

    print("")
    print(report_text)
    print(f"\n리포트 저장 위치: {report_path.relative_to(REPO_ROOT)}")

    if total_vulns > 0:
        print(f"\n총 {total_vulns}건의 취약점이 발견되었습니다. Push 전에 리포트를 확인하세요.")
        return 1

    print("\n취약점이 발견되지 않았습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
