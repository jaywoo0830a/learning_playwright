"""
문제 2 정답 — 버튼 클릭 & URL 검증
"""
import re

from playwright.sync_api import Page, expect


def test_click_button_and_check_url(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("button", name="소개 페이지로 이동").click()
    expect(page).to_have_url(re.compile(r"about\.html$"))


def test_about_page_heading(page: Page, base_url: str):
    page.goto(f"{base_url}/about.html")
    expect(page.get_by_role("heading", name="소개 페이지")).to_be_visible()
