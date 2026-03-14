"""
문제 4 정답 — 동적 텍스트 & 가시성 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    to_be_visible()
        → 요소가 화면에 실제로 보이는지 검증.
        → display:none, visibility:hidden, opacity:0 이면 실패.
        → 요소가 아직 없으면 나타날 때까지 자동 대기 (auto-waiting).

    not_to_be_visible()
        → 요소가 숨겨진 상태인지 검증.
        → DOM 에 존재하지만 display:none 인 경우도 통과.

◆ auto-waiting 이란?
    Playwright 는 expect() 를 실행할 때 기본 30초 동안
    조건이 충족될 때까지 계속 재시도한다.
    → sleep() 이나 wait() 를 직접 쓸 필요가 없다!
    → 토스트처럼 클릭 후 잠깐 뒤에 나타나는 요소도 자동으로 기다린다.

◆ 흔한 실수
    ✗ 성공 버튼 클릭 후 에러 토스트만 "안 보임" 검증 누락
        → 두 가지를 동시에 검증해야 완전한 테스트가 된다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_success_toast_visible(page: Page, base_url: str):
    page.goto(base_url)

    # 버튼 클릭 후 토스트가 나타날 때까지 Playwright 가 자동으로 기다린다
    page.get_by_role("button", name="성공 알림").click()
    expect(page.get_by_text("저장이 완료되었습니다")).to_be_visible()


def test_error_toast_initially_hidden(page: Page, base_url: str):
    page.goto(base_url)

    # 아무것도 클릭하지 않은 초기 상태
    # → 토스트는 display:none 이므로 not_to_be_visible() 통과
    expect(page.get_by_text("오류가 발생했습니다")).not_to_be_visible()


def test_error_toast_visible_after_click(page: Page, base_url: str):
    page.goto(base_url)

    page.get_by_role("button", name="에러 알림").click()
    expect(page.get_by_text("오류가 발생했습니다")).to_be_visible()


def test_only_one_toast_visible(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("button", name="성공 알림").click()

    # 성공 토스트는 보여야 한다
    expect(page.get_by_text("저장이 완료되었습니다")).to_be_visible()

    # 에러 토스트는 절대 보이면 안 된다
    # → 이 줄을 빠뜨리면 "성공 버튼이 에러도 띄우는" 버그를 못 잡는다
    expect(page.get_by_text("오류가 발생했습니다")).not_to_be_visible()
