"""
문제 5 정답 — 플레이스홀더 검색 & 키보드 입력
"""
from playwright.sync_api import Page, expect


def test_search_found(page: Page, base_url: str):
    page.goto(base_url)
    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("노트북")
    search.press("Enter")
    expect(page.get_by_text("노트북 Pro")).to_be_visible()


def test_search_keyboard(page: Page, base_url: str):
    page.goto(base_url)
    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("키보드")
    search.press("Enter")
    expect(page.get_by_text("기계식 키보드")).to_be_visible()


def test_search_no_result(page: Page, base_url: str):
    page.goto(base_url)
    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("없는제품xyz")
    search.press("Enter")
    expect(page.get_by_text("검색 결과가 없습니다.")).to_be_visible()
