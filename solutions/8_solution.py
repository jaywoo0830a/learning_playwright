"""
문제 8 정답 — 목록 개수 & 내용 검증
"""
from playwright.sync_api import Page, expect


def test_initial_item_count(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_test_id("todo-item")).to_have_count(3)


def test_item_texts(page: Page, base_url: str):
    page.goto(base_url)
    items = page.get_by_test_id("todo-item")
    expect(items).to_have_text([
        "Playwright 설치하기 완료",
        "첫 테스트 작성하기 완료",
        "CI 연동하기 완료",
    ])


def test_add_item_increases_count(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_placeholder("새 할 일 입력").fill("문서 작성하기")
    page.get_by_role("button", name="추가").click()
    expect(page.get_by_test_id("todo-item")).to_have_count(4)
