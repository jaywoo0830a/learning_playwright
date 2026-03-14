"""
실전 3 정답 — 드래그 앤 드롭 칸반 보드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    drag_to() 는 HTML5 Drag API 기반 앱에서 동작.
    React DnD 등 pointer 이벤트 기반은 bounding_box + mouse API 사용.
    to_have_count() 로 컬럼 내 카드 수 변화를 검증.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_drag_card_to_progress(page: Page, base_url: str):
    page.goto(base_url)
    page.locator("[data-id='card-1']").drag_to(page.locator("#list-progress"))
    expect(page.locator("#move-log")).to_contain_text("로그인 기능 구현")


def test_column_card_counts(page: Page, base_url: str):
    page.goto(base_url)
    expect(page.locator("#list-todo .card")).to_have_count(3)
    expect(page.locator("#list-progress .card")).to_have_count(1)
    expect(page.locator("#list-done .card")).to_have_count(1)


def test_drag_and_verify_counts(page: Page, base_url: str):
    page.goto(base_url)
    page.locator("[data-id='card-1']").drag_to(page.locator("#list-progress"))
    expect(page.locator("#list-todo .card")).to_have_count(2)
    expect(page.locator("#list-progress .card")).to_have_count(2)


def test_drag_with_mouse_api(page: Page, base_url: str):
    page.goto(base_url)
    src_box = page.locator("[data-id='card-2']").bounding_box()
    sx = src_box["x"] + src_box["width"] / 2
    sy = src_box["y"] + src_box["height"] / 2
    dst_box = page.locator("#list-done").bounding_box()
    dx = dst_box["x"] + dst_box["width"] / 2
    dy = dst_box["y"] + dst_box["height"] / 2
    page.mouse.move(sx, sy)
    page.mouse.down()
    page.mouse.move(dx, dy, steps=10)
    page.mouse.up()
    expect(page.locator("#list-done .card")).to_have_count(2)
