"""
문제 8 — 목록 개수 & 내용 검증
================================
학습 목표:
  - get_by_test_id() 로 data-testid 요소 찾기
  - to_have_count() 로 개수 검증
  - to_have_text([...]) 로 목록 전체 텍스트 순서 검증
"""
from playwright.sync_api import Page, expect


def test_initial_item_count(page: Page, base_url: str):
    """초기 할 일 항목이 정확히 3개여야 한다."""
    page.goto(base_url)

    # TODO: data-testid="todo-item" 으로 요소들을 찾아 개수가 3개인지 검증하세요
    # items = page.get_by_test_id(???)
    # expect(items).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_item_texts(page: Page, base_url: str):
    """할 일 항목 텍스트가 순서대로 일치해야 한다."""
    page.goto(base_url)

    items = page.get_by_test_id("todo-item")

    # TODO: to_have_text() 에 리스트를 전달해 모든 항목 텍스트를 검증하세요
    # 각 li 안에는 텍스트 + "완료" 버튼이 있으므로 전체 텍스트를 고려하세요
    # expect(items).to_have_text([???, ???, ???])
    raise NotImplementedError("TODO를 완성하세요")


def test_add_item_increases_count(page: Page, base_url: str):
    """새 항목 추가 후 총 개수가 4개가 되어야 한다."""
    page.goto(base_url)

    # TODO: placeholder "새 할 일 입력" 으로 input을 찾아 "문서 작성하기" 를 입력하세요
    # page.get_by_placeholder(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "추가" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()

    # TODO: 항목이 4개가 되었는지 검증하세요
    # expect(page.get_by_test_id(???)).to_have_count(???)
