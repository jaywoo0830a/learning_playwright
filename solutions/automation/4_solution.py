"""
실전 4 정답 — 무한 스크롤 + 동적 렌더링
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    page.evaluate("window.scrollTo(...)") 로 스크롤 제어.
    wait_for_timeout() 으로 비동기 로딩 대기.
    to_have_count() 의 auto-retry 로 동적 증가 항목 검증.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_scroll_to_bottom(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator(".feed-item")).to_have_count(5, timeout=5000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    expect(page.locator(".feed-item")).to_have_count(10, timeout=5000)


def test_wait_for_end_message(page: Page, base_url: str):
    page.goto(base_url)
    for _ in range(5):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(600)
    expect(page.locator("#end-msg")).to_be_visible()


def test_progressive_loading(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator(".feed-item")).to_have_count(5, timeout=5000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    expect(page.locator(".feed-item")).to_have_count(10, timeout=5000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    expect(page.locator(".feed-item")).to_have_count(15, timeout=5000)
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    expect(page.locator(".feed-item")).to_have_count(20, timeout=5000)
    expect(page.locator("#end-msg")).to_be_visible()


def test_filter_and_verify_types(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator(".feed-item")).to_have_count(5, timeout=5000)
    page.get_by_role("button", name="알림").click()
    expect(page.locator(".feed-item")).to_have_count(5, timeout=5000)
    items = page.locator(".feed-item").all()
    for item in items:
        expect(item).to_have_attribute("data-type", "alert")
