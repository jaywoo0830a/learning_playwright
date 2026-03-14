"""
문제 4 정답 — 동적 텍스트 & 가시성 검증
"""
from playwright.sync_api import Page, expect


def test_success_toast_visible(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("button", name="성공 알림").click()
    expect(page.get_by_text("저장이 완료되었습니다")).to_be_visible()


def test_error_toast_visible(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("button", name="에러 알림").click()
    expect(page.get_by_text("오류가 발생했습니다")).to_be_visible()


def test_success_hides_error_toast(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("button", name="성공 알림").click()
    expect(page.get_by_text("오류가 발생했습니다")).not_to_be_visible()
