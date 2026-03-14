"""
실전 6 정답 — SE2 스타일 에디터 (iframe + designMode)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    frame_locator("iframe#se2-frame") 로 SE2 iframe 진입.
    body.press_sequentially() 로 designMode 에디터에 키 입력.
    Ctrl+A → 외부 툴바 버튼 클릭 순서가 서식 적용의 핵심.
    evaluate("el => el.innerText") 로 iframe 내부 값 검증.

◆ 흔한 실수
    ✗ fill() 사용 — designMode 에서 input 이벤트 미발생으로 무시
    ✗ 툴바 클릭 전에 전체 선택 없이 → 서식이 빈 영역에 적용됨
    ✗ wait_for_load_state("networkidle") 생략 → iframe 미초기화
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_frame_locator_access(page: Page, base_url: str):
    page.goto(base_url)
    # iframe 초기화 완료 대기
    page.wait_for_load_state("networkidle")

    # title 속성으로 iframe 특정 — id 보다 안정적
    frame = page.frame_locator("iframe[title='본문 편집 영역']")
    expect(frame.locator("body")).to_be_visible()


def test_type_into_iframe_body(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#se2-frame")
    body  = frame.locator("body")
    body.click()
    # fill() 대신 press_sequentially() — designMode 키 이벤트 발생
    body.press_sequentially("SE2 에디터 입력 테스트", delay=30)
    expect(page.locator("#char-info")).not_to_have_text("0 글자")


def test_apply_bold_via_toolbar(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#se2-frame")
    body  = frame.locator("body")
    body.click()
    body.press_sequentially("굵게 처리할 텍스트", delay=20)

    # Ctrl+A 로 전체 선택 후 외부 Bold 버튼 클릭
    body.press("Control+a")
    page.locator("#tb-bold").click()

    # iframe 안에 <b> 또는 <strong> 태그 생성 확인
    frame.locator("b, strong").first.wait_for()


def test_full_write_and_submit(page: Page, base_url: str):
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#se2-frame")
    body  = frame.locator("body")
    body.click()
    body.press_sequentially("등록 테스트 내용", delay=20)

    # 등록 버튼은 iframe 밖
    page.locator("#btn-submit").click()

    # 결과 텍스트 영역 검증
    expect(page.locator("#result-text")).to_contain_text("등록 테스트 내용")

    # evaluate() 로 iframe body.innerText 직접 검증
    text = frame.locator("body").evaluate("el => el.innerText")
    assert "등록 테스트 내용" in text
