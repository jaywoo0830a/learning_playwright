"""
문제 10 정답 — Heading & Link 탐색 종합
"""
from playwright.sync_api import Page, expect


def test_main_heading(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_role("heading", level=1)).to_have_text("기술 블로그")


def test_navigation_link_count(page: Page, base_url: str):
    page.goto(base_url)
    nav = page.get_by_role("navigation", name="주 내비게이션")
    expect(nav.get_by_role("link")).to_have_count(3)


def test_article_heading_count(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_role("heading", level=2)).to_have_count(5)


def test_read_more_links(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_role("link", name="더 읽기")).to_have_count(3)


def test_first_article_heading_text(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_role("heading", level=2).first).to_contain_text(
        "Playwright로 E2E 테스트 시작하기"
    )
