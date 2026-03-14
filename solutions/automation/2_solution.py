"""
실전 2 정답 — CodeMirror / Monaco 스타일 숨겨진 textarea
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    wrapper 클릭 → textarea 활성화 → fill() 순서가 필수.
    force=True 는 pointer-events:none 요소를 강제 클릭할 때 사용.
    evaluate("el => el.value") 로 숨겨진 textarea 값 검증.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_find_hidden_textarea(page: Page, base_url: str):
    page.goto(base_url)
    page.locator("#cm-editor").click()
    code = "print('hello')\nprint('world')"
    page.get_by_label("코드 입력창").fill(code)
    expect(page.locator("#line-count")).to_have_text("2 줄")


def test_force_click_and_fill(page: Page, base_url: str):
    page.goto(base_url)
    # force=True 로 숨겨진 textarea 강제 클릭
    page.locator("#code-input").click(force=True)
    code = "x = 10\ny = 20\nprint(x + y)"
    page.locator("#code-input").fill(code)
    expect(page.locator("#line-count")).to_have_text("3 줄")


def test_run_code_and_check_output(page: Page, base_url: str):
    page.goto(base_url)
    page.locator("#cm-editor").click()
    page.get_by_label("코드 입력창").fill("print('자동화 성공')")
    page.locator("#btn-run").click()
    expect(page.locator("#run-output")).to_be_visible()
    expect(page.locator("#run-output")).to_contain_text("자동화 성공")


def test_verify_code_with_evaluate(page: Page, base_url: str):
    page.goto(base_url)
    page.locator("#cm-editor").click()
    code = "print('line1')\nprint('line2')\nprint('line3')"
    page.get_by_label("코드 입력창").fill(code)
    value = page.locator("#code-input").evaluate("el => el.value")
    assert "print" in value
    lines = page.locator("#code-input").evaluate("el => el.value.split('\\n').length")
    assert lines == 3
