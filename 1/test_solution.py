"""
문제 1 — 페이지 타이틀 검증
==============================
학습 목표:
  - page.goto() 로 페이지 이동
  - expect(page).to_have_title() 로 타이틀 검증
  - re.compile() 로 정규식 부분 일치

README.md 를 읽고 아래 TODO 를 완성하세요.
"""
import re

import pytest
from playwright.sync_api import Page, expect


def test_exact_title(page: Page, base_url: str):
    """페이지 타이틀이 정확히 일치해야 한다."""
    # TODO: base_url 로 이동하세요
    # page.goto(???)

    # TODO: 타이틀이 "나의 첫 Playwright 앱" 과 정확히 일치하는지 검증하세요
    # expect(page).to_have_title(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_title_contains_playwright(page: Page, base_url: str):
    """페이지 타이틀에 'Playwright' 가 포함되어야 한다 (정규식)."""
    page.goto(base_url)

    # TODO: re.compile() 을 사용해 타이틀에 "Playwright" 가 포함되는지 검증하세요
    # expect(page).to_have_title(re.compile(???))
    raise NotImplementedError("TODO를 완성하세요")
