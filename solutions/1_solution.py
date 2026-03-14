"""
문제 1 정답 — 페이지 타이틀 검증
"""
import re

from playwright.sync_api import Page, expect


def test_exact_title(page: Page, base_url: str):
    page.goto(base_url)
    expect(page).to_have_title("나의 첫 Playwright 앱")


def test_title_contains_playwright(page: Page, base_url: str):
    page.goto(base_url)
    expect(page).to_have_title(re.compile("Playwright"))
