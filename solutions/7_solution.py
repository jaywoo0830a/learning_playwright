"""
문제 7 정답 — 이미지 alt 텍스트 & 갤러리 검증
"""
from playwright.sync_api import Page, expect


def test_gallery_image_count(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator("img")).to_have_count(3)


def test_mountain_image_exists(page: Page, base_url: str):
    page.goto(base_url)
    img = page.get_by_alt_text("산 풍경")
    expect(img).to_have_attribute("alt", "산 풍경")


def test_all_alt_texts_exist(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.get_by_alt_text("바다 풍경")).to_have_attribute("alt", "바다 풍경")
    expect(page.get_by_alt_text("숲 풍경")).to_have_attribute("alt", "숲 풍경")


def test_figcaption_count(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator("figcaption")).to_have_count(3)
