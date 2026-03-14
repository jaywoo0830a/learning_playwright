"""
문제 10 — Heading & Link 탐색 종합
=====================================
학습 목표:
  - get_by_role("heading", level=N) 으로 제목 계층 찾기
  - get_by_role("navigation") 범위 안에서 링크 탐색
  - to_have_count(), to_have_text(), to_contain_text() 종합 활용
"""
from playwright.sync_api import Page, expect


def test_main_heading(page: Page, base_url: str):
    """h1 제목이 '기술 블로그' 여야 한다."""
    page.goto(base_url)

    # TODO: role="heading", level=1 로 h1을 찾아 텍스트가 "기술 블로그" 인지 검증하세요
    # expect(page.get_by_role("heading", level=???)).to_have_text(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_navigation_link_count(page: Page, base_url: str):
    """주 내비게이션 안에 링크가 정확히 3개여야 한다."""
    page.goto(base_url)

    # TODO: aria-label="주 내비게이션" 인 nav를 찾고
    #        그 안의 링크 개수가 3개인지 검증하세요
    # nav = page.get_by_role("navigation", name=???)
    # expect(nav.get_by_role(???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_article_heading_count(page: Page, base_url: str):
    """h2 제목이 페이지에 5개 있어야 한다 (포스트 3개 + 소개 + 연락처)."""
    page.goto(base_url)

    # TODO: role="heading", level=2 로 h2를 찾아 개수가 5개인지 검증하세요
    # expect(page.get_by_role("heading", level=???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_read_more_links(page: Page, base_url: str):
    """'더 읽기' 링크가 정확히 3개여야 한다."""
    page.goto(base_url)

    # TODO: name="더 읽기" 인 링크 role을 찾아 개수가 3개인지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_first_article_heading_text(page: Page, base_url: str):
    """첫 번째 h2 제목이 'Playwright로 E2E 테스트 시작하기' 를 포함해야 한다."""
    page.goto(base_url)

    # TODO: h2 중 첫 번째(.first) 요소가 해당 텍스트를 포함하는지 검증하세요
    # expect(page.get_by_role("heading", level=2).first).to_contain_text(???)
    raise NotImplementedError("TODO를 완성하세요")
