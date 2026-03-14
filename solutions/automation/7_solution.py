"""
실전 7 정답 — SE ONE 스타일 에디터 (iframe + contenteditable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    frame_locator().get_by_test_id() 로 iframe 안 testid 접근.
    contenteditable div 도 press_sequentially() 가 안전.
    툴바 버튼(iframe 밖) 클릭 → iframe 안 DOM 변화 wait_for() 검증.

◆ SE2 vs SE ONE 차이
    SE2: frame.locator("body") — body 전체가 편집 영역
    SE ONE: frame.get_by_test_id("se-one-editor") — 특정 div
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_find_editor_in_iframe(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame  = page.frame_locator("iframe#se-one-frame")
    editor = frame.get_by_test_id("se-one-editor")
    expect(editor).to_be_visible()


def test_input_into_contenteditable(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame  = page.frame_locator("iframe#se-one-frame")
    editor = frame.get_by_test_id("se-one-editor")
    editor.click()
    # contenteditable 도 press_sequentially() 로 입력
    editor.press_sequentially("SE ONE 테스트 입력", delay=30)
    expect(page.locator("#word-count")).not_to_have_text("0자")


def test_insert_heading_block(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame  = page.frame_locator("iframe#se-one-frame")
    editor = frame.get_by_test_id("se-one-editor")
    editor.click()

    # H2 툴바 버튼은 iframe 밖
    page.locator("#tb-h2").click()
    # iframe 안에 h2 태그 생성 대기
    frame.locator("h2").wait_for()


def test_full_write_and_publish(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame  = page.frame_locator("iframe#se-one-frame")
    editor = frame.get_by_test_id("se-one-editor")
    editor.click()
    editor.press_sequentially("발행 테스트 본문입니다.", delay=20)

    # 발행 버튼은 iframe 밖
    page.locator("#btn-publish").click()

    expect(page.locator("#result-box")).to_be_visible()
    expect(page.locator("#result-box")).to_contain_text("발행 테스트 본문")

    # evaluate() 로 에디터 내부 텍스트 직접 검증
    text = editor.evaluate("el => el.innerText")
    assert "발행 테스트" in text
