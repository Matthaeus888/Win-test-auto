---
문서유형: Project PRD
상태: 승인완료
최초 작성일: 2026-08-20
최근 변경일: 2026-08-22
승인일: 2026-08-20 (최초), 2026-08-20 (재승인), 2026-08-21 (재승인), 2026-08-22 (재승인)
---

# Project PRD - Automation Exercise QA

## 1. 프로젝트 목적

대상 서비스(automationexercise.com)의 기능을 AI로 TC를 생성하고, 생성된 TC 기반으로
자동화 대상 영역을 선정하여 AI로 자동화용 TC 생성 및 자동화 코드를 생성하여 테스트
자동화를 진행한다.

## 2. 대상 서비스 개요

automationexercise.com은 테스트 자동화 연습을 위한 간단한 이커머스(전자상거래) 웹사이트이다.
주요 기능으로 회원가입, 로그인, 로그아웃, 상품 담기(장바구니), 계정 삭제(로그인 시에만 가능)
등이 존재한다.

## 3. 대상 URL / 환경

- Production: https://automationexercise.com/
- 별도 dev/staging 환경 없음 (프로덕션 URL만 대상)

## 4. 테스트 환경

- 브라우저: Chrome (v151.0.7922.169)
- OS: 웹 페이지 특성상 별도 지정 없음
- 테스트 계정: 사전 준비된 테스트 계정 3개 사용
  - actest1@test.com
  - actest2@test.com
  - actest3@test.com
  - (비밀번호 등 인증정보는 문서에 기록하지 않으며 별도 관리)

## 5. 대상 Feature 목록

- 상단 네비게이션 (로그인 상태 / 로그아웃 상태에 따라 메뉴 구성이 다름)
  - 로그인 상태: Home, Products, Cart, Logout, Delete Account, Test Cases, API Testing,
    Video Tutorials, Contact us, "Logged in as {유저명}" 표시
  - 로그아웃 상태: Home, Products, Cart, Signup/Login, Test Cases, API Testing,
    Video Tutorials, Contact us
- 로그인 / 로그아웃
- 회원가입 / 계정삭제
- 상품 검색
- 장바구니 (상품 담기 포함)
- 각 페이지별 UI (Home, Products, Cart, Signup/Login, Checkout)
- 상품 상세

## 6. In Scope

- 로그인 / 로그아웃
- 상단 네비게이션 동작 (로그인/로그아웃 상태별 메뉴 구성 차이 포함)
- 회원가입 / 계정삭제
- 상품 검색
- 상품 담기
- 장바구니
- 각 페이지별(Home, Products, Cart, Signup/Login, Checkout) UI
- 상품 상세

## 7. Out of Scope

- 결제 기능
- 네비게이션 중 다음 메뉴의 상세 동작: Test Cases, API Testing, Video Tutorials, Contact us
- 이메일 인증 (별도 인증 절차 없이 회원가입 및 로그인 가능)
- 성능 테스트

## 8. 기타 제약사항 / 참고사항

- 사이트 진입 시 또는 일정 시간 경과 시 무작위로 모달형 광고가 노출될 수 있음 —
  광고 관련 동작은 검증 대상에서 제외
- 프로젝트 일정은 미정 (추후 변경 가능)
- 계정 토큰(인증 토큰) 관련 정확한 처리 요건은 확인이 어려워 검증 대상에서 제외

## 변경 이력

| 날짜 | 변경 사유 | 상태 |
|---|---|---|
| 2026-08-20 | 최초 작성 | 초안 |
| 2026-08-20 | 사용자 최종 승인 | 승인완료 |
| 2026-08-20 | "1. 프로젝트 목적" 문구 수정 (AI 기반 TC/자동화 코드 생성 명시) - 재승인 | 승인완료 |
| 2026-08-21 | "상품 검색" Feature PRD 작업 중 상품 상세 페이지 존재가 확인되어, 대상 Feature 목록 및 In Scope에 "상품 상세" 추가 - 사용자 재승인 | 승인완료 |
| 2026-08-22 | page-ui Feature PRD의 Checkout 페이지 범위 확장에 맞춰 "각 페이지별 UI" 대상 Feature 표기(5. 대상 Feature 목록, 6. In Scope)에 Checkout 반영 - 사용자 요청, 재승인 대기 | 승인완료 (재승인 대기) |
| 2026-08-22 | 사용자 최종 재승인 | 승인완료 |
