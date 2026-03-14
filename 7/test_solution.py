"""
문제 7 — 이미지 alt 텍스트 & 갤러리 검증
==========================================
학습 목표:
  - get_by_alt_text() 로 alt 속성으로 이미지 찾기
  - to_have_count() 로 요소 개수 검증
  - to_have_attribute() 로 속성 값 검증
"""
from playwright.sync_api import Page, expect


def test_gallery_image_count(page: Page, base_url: str):
    """갤러리에 img 태그가 정확히 3개 있어야 한다."""
    page.goto(base_url)

    # TODO: "img" 태그 locator를 만들고 개수가 3개인지 검증하세요
    # expect(page.locator(???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_mountain_image_exists(page: Page, base_url: str):
    """alt='산 풍경' 이미지가 페이지에 존재해야 한다."""
    page.goto(base_url)

    # TODO: alt 텍스트 "산 풍경" 으로 이미지를 찾아 attribute를 검증하세요
    # img = page.get_by_alt_text(???)
    # expect(img).to_have_attribute("alt", ???)
    raise NotImplementedError("TODO를 완성하세요")


def test_all_alt_texts_exist(page: Page, base_url: str):
    """세 이미지의 alt 텍스트가 모두 페이지에 존재해야 한다."""
    page.goto(base_url)

    # TODO: "바다 풍경", "숲 풍경" alt 텍스트 이미지도 각각 존재하는지 검증하세요
    # expect(page.get_by_alt_text(???)).to_have_attribute("alt", ???)
    # expect(page.get_by_alt_text(???)).to_have_attribute("alt", ???)
    raise NotImplementedError("TODO를 완성하세요")


def test_figcaption_count(page: Page, base_url: str):
    """figcaption 요소가 정확히 3개 있어야 한다."""
    page.goto(base_url)

    # TODO: "figcaption" 태그 locator를 만들고 개수가 3개인지 검증하세요
    # expect(page.locator(???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")
