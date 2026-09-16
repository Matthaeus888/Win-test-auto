# security_check

Git Push 전에 **사용자가 직접 확인**할 수 있는 형식으로 의존성 취약점 리포트를
생성하는 독립 스크립트입니다.

## 설계 원칙

- **Push 자동화 아님**: 이 스크립트는 Git 명령을 전혀 실행하지 않습니다.
  취약점 발견 여부와 관계없이 Commit/Push 승인은 항상 사용자가 직접 결정합니다
  (CLAUDE.md 14절/18절).
- **대상은 pip-audit만**: 이 프로젝트는 Python 전용(automation, scripts/*)이며
  `package.json`이 없어 `npm audit`은 적용 대상이 없습니다. 대상 파일은
  `automation/requirements.txt`, `scripts/notify_slack/requirements.txt`,
  `scripts/sheets_sync/requirements.txt`입니다.
- **사람이 읽을 수 있는 리포트**: 실행 결과를 콘솔에 출력하고, 동시에
  `scripts/security_check/reports/security_report_<timestamp>.md` 파일로 저장합니다.
  라이브러리별 취약점 ID, 수정 버전, 설명을 정리해 Push 전에 검토하기 쉬운 형태로 제공합니다.
- **판단은 사용자의 몫**: 취약점이 발견되면 종료 코드 1을 반환하지만, 이는 "주의가
  필요하다"는 신호일 뿐 스크립트가 임의로 조치를 취하거나 Push를 막지 않습니다.

## 사용 방법

```bash
python -m pip install -r scripts/security_check/requirements.txt
python scripts/security_check/run_security_check.py
```

실행 후 콘솔 출력과 `scripts/security_check/reports/` 안의 최신 Markdown 리포트를
검토한 뒤, 문제가 없다고 판단되면 평소대로 `git commit` / `git push`를 진행합니다.

## 언제 실행하나요

- **로컬**: QA 자동화 코드 구현이 끝나고 **Git Push를 사용자에게 승인받기 직전**에
  실행하는 것을 권장합니다.
- **CI**: `.github/workflows/ci.yml`의 `Run dependency security check (pip-audit)`
  스텝에서도 매 실행마다 동일한 스크립트를 돌립니다. `continue-on-error: true`로
  설정되어 있어 취약점이 발견돼도 CI Job 자체를 실패시키지 않으며, 리포트는
  `security-report` Artifact로 업로드됩니다. CI 결과의 Pass/Fail 판정에 반영할지는
  별도 요청 시 재검토합니다(CLAUDE.md 13절 — 실패를 임의로 PASS로 판단하지 않되,
  판정 기준 자체를 바꾸는 것도 임의로 하지 않음).
