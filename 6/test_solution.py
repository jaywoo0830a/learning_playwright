"""
문제 6 — 체크박스 & 상태 검증
================================
학습 목표:
  - get_by_role("checkbox", name=...) 로 체크박스 찾기
  - check() 로 체크, to_be_checked() 로 상태 검증
  - to_be_disabled() / to_be_enabled() 로 버튼 상태 검증
"""
from playwright.sync_api import Page, expect


def test_submit_button_initially_disabled(page: Page, base_url: str):
    """초기 상태에서 '가입하기' 버튼은 비활성화여야 한다."""
    page.goto(base_url)

    # TODO: "가입하기" 버튼이 비활성화 상태인지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_disabled()
    raise NotImplementedError("TODO를 완성하세요")


def test_required_checkboxes_enable_button(page: Page, base_url: str):
    """필수 체크박스 2개를 모두 체크하면 버튼이 활성화되어야 한다."""
    page.goto(base_url)

    # TODO: "이용약관에 동의합니다" 체크박스를 체크하세요
    # page.get_by_role("checkbox", name=???).check()
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "개인정보 처리방침에 동의합니다" 체크박스를 체크하세요
    # page.get_by_role("checkbox", name=???).check()

    # TODO: "가입하기" 버튼이 이제 활성화 상태인지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_enabled()


def test_full_signup_with_marketing(page: Page, base_url: str):
    """세 가지 체크박스 모두 체크 후 가입하면 마케팅 동의 완료 메시지가 보여야 한다."""
    page.goto(base_url)

    # 필수 항목 체크
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보 처리방침에 동의합니다 (필수)").check()

    # TODO: "마케팅 수신에 동의합니다" 체크박스를 체크하고 checked 상태를 검증하세요
    # marketing = page.get_by_role("checkbox", name=???)
    # marketing.check()
    # expect(marketing).to_be_checked()
    raise NotImplementedError("TODO를 완성하세요")

    # 가입하기 버튼 클릭
    page.get_by_role("button", name="가입하기").click()

    # TODO: "마케팅 수신에 동의하셨습니다" 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
