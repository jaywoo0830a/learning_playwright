"""
문제 6 정답 — 체크박스 & 상태 검증
"""
from playwright.sync_api import Page, expect


def test_submit_button_initially_disabled(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_role("button", name="가입하기")).to_be_disabled()


def test_required_checkboxes_enable_button(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보 처리방침에 동의합니다 (필수)").check()
    expect(page.get_by_role("button", name="가입하기")).to_be_enabled()


def test_full_signup_with_marketing(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보 처리방침에 동의합니다 (필수)").check()
    marketing = page.get_by_role("checkbox", name="마케팅 수신에 동의합니다 (선택)")
    marketing.check()
    expect(marketing).to_be_checked()
    page.get_by_role("button", name="가입하기").click()
    expect(page.get_by_text("마케팅 수신에 동의하셨습니다")).to_be_visible()
