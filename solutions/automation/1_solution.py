"""
실전 1 정답 — contenteditable 리치 텍스트 에디터
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    fill() 은 contenteditable 에 동작하지만 일부 에디터에서 무시된다.
    → press_sequentially() 가 더 안전 (실제 키 이벤트 발생).

    evaluate("el => el.innerHTML") / ("el => el.innerText")
    → 에디터 내부 HTML/텍스트를 Python 으로 꺼내는 유일한 방법.
    → to_contain_text() 가 안 되는 상황에서 대안.

    Ctrl+A 로 전체 선택 후 서식 버튼 클릭
    → 서식 적용의 가장 안정적인 패턴.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_type_into_editor(page: Page, base_url: str):
    page.goto(base_url)
    editor = page.get_by_role("textbox", name="본문 편집기")
    editor.click()
    editor.fill("Playwright 자동화 테스트")
    expect(page.locator("#char-num")).not_to_have_text("0")


def test_apply_bold_formatting(page: Page, base_url: str):
    import re
    page.goto(base_url)
    editor = page.get_by_role("textbox", name="본문 편집기")
    editor.click()
    editor.fill("굵게 만들 텍스트")
    # 전체 선택 후 Bold 버튼 클릭
    editor.press("Control+a")
    page.get_by_role("button", name="B").click()
    # active 클래스가 붙었는지 확인
    expect(page.locator("#btn-bold")).to_have_class(re.compile("active"))


def test_write_and_save(page: Page, base_url: str):
    page.goto(base_url)
    editor = page.get_by_role("textbox", name="본문 편집기")
    editor.click()
    editor.fill("자동화 테스트 내용입니다.")
    page.locator("#btn-save").click()
    expect(page.locator("#output")).to_be_visible()
    expect(page.locator("#output-text")).to_contain_text("자동화 테스트")


def test_verify_content_with_evaluate(page: Page, base_url: str):
    page.goto(base_url)
    editor = page.get_by_role("textbox", name="본문 편집기")
    editor.click()
    editor.fill("평가 테스트 문장")
    # evaluate() 로 innerText 꺼내기
    text = page.locator("#editor").evaluate("el => el.innerText")
    assert "평가 테스트" in text
    # innerHTML 도 검증
    html = page.locator("#editor").evaluate("el => el.innerHTML")
    assert len(html) > 0
