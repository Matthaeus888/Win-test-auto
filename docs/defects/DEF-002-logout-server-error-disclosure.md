# DEF-002: 로그아웃 상태에서 `/logout` 접근 시 Django 디버그 에러 페이지 노출 (정보 노출)

| 항목 | 내용 |
|---|---|
| 심각도 | Medium (정보 노출 / Information Disclosure) |
| 발견일 | 2026-08-21 (실사용자 실측 제보), 2026-08-31 (Playwright MCP로 재확인) |
| 대상 | `https://automationexercise.com/logout` (로그아웃 상태에서 직접 접근) |
| 관련 TC | `TC-LOGIN-LOGOUT-016` (결함 의심 항목, [docs/tc/login-logout.md](../tc/login-logout.md)) |
| 분류 | 실제 Product 문제 — 정보 노출(Information Disclosure) |
| 재현성 | 간헐적 |

## 증상

**로그아웃된 상태**에서 `/logout` URL에 직접 접근하면, 정상적인 페이지(로그인 페이지
랜딩 등) 대신 **Django의 디버그 모드 에러 페이지**가 그대로 노출된다. 이 페이지에는
아래와 같은 서버 내부 정보가 포함되어 있다.

- 예외 종류/메시지: `KeyError at /logout`, Exception Value `'user_id'`
- 전체 Python Traceback (파일 경로, 라인 번호 포함)
- 서버 파일 시스템 경로 (`.../django/contrib/sessions/backends/base.py` 등)
- Python/Django 버전 정보

이런 정보는 프로덕션 환경에서 외부 사용자에게 노출되어서는 안 되는 내부 구현
세부사항이며, 공격자가 서버 스택/버전을 파악해 알려진 취약점을 노리는 정찰
(reconnaissance) 단계에 활용될 수 있다.

## 재현 절차

1. 로그아웃 상태(비로그인)를 확인한다.
2. 브라우저 주소창에 `https://automationexercise.com/logout`을 직접 입력해 접근한다.
3. 노출되는 화면을 확인한다.

## 기대 결과 vs 실제 결과

| 구분 | 기대 결과 | 실제 결과 |
|---|---|---|
| 응답 | 정상 페이지(로그인 페이지 랜딩 또는 최소한 일반 에러 페이지) | Django DEBUG 모드 상세 에러 페이지 |
| HTTP 상태 | 3xx/2xx | 500 |
| 노출 정보 | 없음 | Traceback, 서버 경로, 프레임워크/언어 버전 |

## 근본 원인

서버 측 `website/views.py`의 `logout` 뷰가 세션에서 `user_id` 키를 조건 없이
삭제하려고 시도하는 것으로 추정된다.

```python
del request.session['user_id']  # 이미 로그아웃 상태라 키가 없으면 KeyError
```

이미 로그아웃된 상태(키가 이미 없는 상태)에서 이 코드가 실행되면 `KeyError`가
발생하고, 프로덕션 서버가 `DEBUG=True`로 설정되어 있어 이 예외가 사용자에게 그대로
노출된다.

## 판정 근거

- 자동화 코드/Locator/Assertion 문제가 아님 — 클라이언트는 단순히 URL에 접근했을
  뿐이며, 서버가 500과 함께 디버그 정보를 반환하는 것을 그대로 관찰한 것이다.
- Test Data 문제가 아님 — 로그아웃 상태(계정 정보 자체가 관여하지 않는 시나리오)에서
  발생한다.
- Test Environment 문제가 아님 — 실사용자 최초 제보(브라우저 수동 조작)와 Playwright
  MCP 조회 전용 접근 양쪽에서 동일하게 재현되어 특정 자동화 도구/브라우저의 문제가
  아니다.
- → **실제 Product 문제**로 분류하며, 특히 프로덕션 환경에 디버그 모드가 켜져 있다는
  점에서 QA 관점의 기능 결함을 넘어 **보안 설정 결함**의 성격도 함께 갖는다.

## 대응 방침

- TC-LOGIN-LOGOUT-016으로 결함 의심 항목에 정식 등록해 회귀 시 계속 추적한다.
- 서버 측 조치(예외 처리 보강, `DEBUG=False` 설정)는 이 프로젝트의 범위 밖이며, 실제
  운영 조직이라면 아래 두 가지를 권고 사항으로 남긴다.
  1. `logout` 뷰에서 세션 키 삭제 전 존재 여부 확인(`request.session.pop('user_id',
     None)` 등)
  2. 프로덕션 환경의 Django `DEBUG` 설정을 `False`로 전환해 디버그 페이지 자체가
     노출되지 않도록 조치
