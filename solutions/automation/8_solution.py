"""
실전 8 정답 — SE ONE 복합 에디터 (제목+본문+블록+인라인툴바)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    제목(iframe 밖) → fill(), 본문(iframe 안) → press_sequentially().
    + 버튼 → wait_for() 대기 → 블록 메뉴 클릭 → DOM 변화 wait_for().
    Shift+Home 으로 한 줄 선택 → 인라인 툴바 팝업 → 서식 버튼 클릭.
    발행 후 제목/본문/HTML 세 결과 필드 동시 검증.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_title_and_body_input(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # 제목은 iframe 밖 → fill() 정상 동작
    page.get_by_test_id("doc-title").fill("자동화 테스트 제목")

    # 본문은 iframe 안 → press_sequentially()
    frame = page.frame_locator("iframe#complex-frame")
    body  = frame.get_by_test_id("complex-editor-body")
    body.click()
    body.press_sequentially("본문 내용입니다.", delay=30)

    expect(page.locator("#char-count")).not_to_have_text("0자")


def test_insert_block_component(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#complex-frame")
    body  = frame.get_by_test_id("complex-editor-body")
    body.click()

    # + 버튼 나타날 때까지 대기 후 클릭
    page.locator("#block-add-btn").wait_for()
    page.locator("#block-add-btn").click()

    # 메뉴에서 인용 블록 선택
    page.locator("[data-block='quote']").click()

    # iframe 안에 blockquote 생성 검증
    frame.locator("blockquote").wait_for()


def test_inline_toolbar_bold(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#complex-frame")
    body  = frame.get_by_test_id("complex-editor-body")
    body.click()
    body.press_sequentially("서식 테스트 텍스트", delay=20)

    # Shift+Home 으로 현재 줄 선택 → 인라인 툴바 팝업
    body.press("Shift+Home")
    page.locator("#inline-toolbar").wait_for()
    page.locator("#itb-bold").click()

    # iframe 안에 b 또는 strong 생성 확인
    frame.locator("b, strong").wait_for()


def test_full_publish_flow(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # 제목 입력 (iframe 밖)
    page.get_by_test_id("doc-title").fill("자동화 테스트 제목")

    # 본문 입력 (iframe 안)
    frame = page.frame_locator("iframe#complex-frame")
    body  = frame.get_by_test_id("complex-editor-body")
    body.click()
    body.press_sequentially("본문 내용입니다.", delay=20)

    # 발행 버튼 클릭
    page.locator("#btn-publish-complex").click()

    # 결과 세 가지 동시 검증
    expect(page.locator("#final-result")).to_be_visible()
    expect(page.locator("#final-title")).to_contain_text("자동화 테스트 제목")
    expect(page.locator("#final-body")).to_contain_text("본문 내용")
    expect(page.locator("#final-html")).not_to_have_text("(내용 없음)")
