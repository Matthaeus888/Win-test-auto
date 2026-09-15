# notify_slack

GitHub Actions CI(`.github/workflows/ci.yml`)에서 pytest 실행 결과(JUnit XML)를 파싱해
테스트가 실패했을 때만 Slack Incoming Webhook으로 알리는 독립 스크립트입니다.

## 설계 원칙

- **실패 시 전용 알림**: 실패한 테스트가 0건이면 아무 메시지도 보내지 않습니다
  (AUTOMATION_GUIDE.md 16절, CLAUDE.md 16절 — Slack은 CI 결과 알림 전용이며 Commit/Push
  승인 용도로 사용하지 않습니다).
- **최소 의존성**: XML 파싱은 `xml.etree.ElementTree`, HTTP 전송은 `urllib.request`만
  사용하며 3rd-party 패키지에 의존하지 않습니다.
- **인증정보 미포함**: Slack Webhook URL은 코드에 하드코딩하지 않고 환경변수
  `SLACK_WEBHOOK_URL`로만 전달받습니다(CLAUDE.md 17절).

## 사용 방법

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python3 scripts/notify_slack/notify.py automation/reports/results.xml
```

인자를 생략하면 기본값 `automation/reports/results.xml`을 사용합니다.

## GitHub Actions 연동

`SLACK_WEBHOOK_URL`을 저장소 Settings > Secrets and variables > Actions에 등록한 뒤,
워크플로우에서 테스트 실패 시(`if: failure()`)에만 이 스크립트를 실행하는 스텝을
추가합니다(`.github/workflows/ci.yml` 참고).
