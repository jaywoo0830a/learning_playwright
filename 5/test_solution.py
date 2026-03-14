"""
문제 5 — 플레이스홀더 검색 & 키보드 입력
==========================================
학습 목표:
  - get_by_placeholder() 로 input 찾기
  - fill() + press("Enter") 조합
  - 동적 렌더링 결과 텍스트 검증
"""
from playwright.sync_api import Page, expect


def test_search_found(page: Page, base_url: str):
    """'노트북' 검색 시 '노트북 Pro' 결과가 보여야 한다."""
    page.goto(base_url)

    # TODO: placeholder "제품명을 검색하세요" 로 input을 찾아 "노트북" 을 입력하세요
    # search = page.get_by_placeholder(???)
    # search.fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "Enter" 키를 누르세요
    # search.press(???)

    # TODO: "노트북 Pro" 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


def test_search_keyboard(page: Page, base_url: str):
    """'키보드' 검색 시 '기계식 키보드' 결과가 보여야 한다."""
    page.goto(base_url)

    search = page.get_by_placeholder("제품명을 검색하세요")

    # TODO: "키보드" 를 입력하고 Enter 를 누르세요
    # search.fill(???)
    # search.press(???)
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "기계식 키보드" 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


def test_search_no_result(page: Page, base_url: str):
    """없는 제품 검색 시 '검색 결과가 없습니다.' 가 보여야 한다."""
    page.goto(base_url)

    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("없는제품xyz")

    # TODO: "Enter" 키를 누르세요
    # search.press(???)
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "검색 결과가 없습니다." 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
