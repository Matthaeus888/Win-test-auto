"""화면과 무관한 순수 문자열 처리 유틸리티.

Source of Truth: docs/automation/AUTOMATION_GUIDE.md 19절("utils: 화면과 무관한 순수
로직", "2회 이상 반복되는 코드는 공통 메서드로 분리")

화면과 무관한 순수 로직이므로 `config/accounts.py`, `utils/account_factory.py`와 동일한
유틸 계층 패턴으로 BasePage를 상속하지 않는다.
"""


def normalize_whitespace(text: str) -> str:
    """연속된 공백을 1칸으로 정규화해 반환한다.

    [2026-08-31 코드 리뷰 반영] 상품명 비교(장바구니 행 vs 상품 카드) 시 일부 상품명의
    DOM 텍스트에 연속 공백이 포함된 경우가 있어(예: "Sleeveless  Dress", TC-CART-005
    테스트 데이터) 비교 직전에 정규화가 필요하다. 이 로직이 `pages/cart_page.py`,
    `pages/products_page.py`, `tests/test_cart.py` 3곳에 동일하게 중복 구현되어 있던
    것을 이 함수로 통합했다(원본 텍스트 자체를 변형하는 것이 아니라 비교용 보조 함수).
    """
    return " ".join(text.split())
