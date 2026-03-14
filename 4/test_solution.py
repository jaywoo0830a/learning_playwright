"""
문제 4 — 동적 텍스트 & 가시성 검증
=====================================
학습 목표:
  - get_by_text() 로 텍스트 내용으로 요소 찾기
  - to_be_visible() / not_to_be_visible() 로 가시성 검증
  - Playwright auto-waiting 체험
"""
from playwright.sync_api import Page, expect


def test_success_toast_visible(page: Page, base_url: str):
    """'성공 알림' 버튼 클릭 후 성공 토스트가 보여야 한다."""
    page.goto(base_url)

    # TODO: "성공 알림" 버튼을 role로 찾아 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "저장이 완료되었습니다" 텍스트가 포함된 요소가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


def test_error_toast_visible(page: Page, base_url: str):
    """'에러 알림' 버튼 클릭 후 에러 토스트가 보여야 한다."""
    page.goto(base_url)

    # TODO: "에러 알림" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "오류가 발생했습니다" 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


def test_success_hides_error_toast(page: Page, base_url: str):
    """'성공 알림' 클릭 시 에러 토스트는 보이지 않아야 한다."""
    page.goto(base_url)
    page.get_by_role("button", name="성공 알림").click()

    # TODO: 에러 토스트 "오류가 발생했습니다" 가 보이지 않는지 검증하세요
    # expect(page.get_by_text(???)).not_to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")
