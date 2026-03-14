"""
문제 3 정답 — 폼 입력 & 제출
"""
from playwright.sync_api import Page, expect


def test_login_success(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("이메일").fill("user@test.com")
    page.get_by_label("비밀번호").fill("secret123")
    page.get_by_role("button", name="로그인").click()
    expect(page.get_by_text("로그인 성공! 환영합니다.")).to_be_visible()


def test_login_failure(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("이메일").fill("user@test.com")
    page.get_by_label("비밀번호").fill("wrongpassword")
    page.get_by_role("button", name="로그인").click()
    expect(page.get_by_text("이메일 또는 비밀번호가 틀렸습니다.")).to_be_visible()
