"""
문제 2 — 버튼 클릭 & URL 검증
==============================
학습 목표:
  - get_by_role("button") 으로 버튼 찾기
  - click() 으로 클릭
  - expect(page).to_have_url() 로 이동 후 URL 검증
"""
import re

from playwright.sync_api import Page, expect


def test_click_button_and_check_url(page: Page, base_url: str):
    """버튼 클릭 후 about.html 로 이동해야 한다."""
    page.goto(base_url)

    # TODO: role="button" 이고 name="소개 페이지로 이동" 인 요소를 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: URL 에 "about.html" 이 포함되는지 정규식으로 검증하세요
    # expect(page).to_have_url(re.compile(???))


def test_about_page_heading(page: Page, base_url: str):
    """about.html 에 '소개 페이지' 제목이 보여야 한다."""
    page.goto(f"{base_url}/about.html")

    # TODO: role="heading" 이고 name="소개 페이지" 인 요소가 보이는지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")
