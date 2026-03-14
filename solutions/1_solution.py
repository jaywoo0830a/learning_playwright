"""
문제 1 정답 — 페이지 타이틀 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    page.goto(url)
        → 브라우저를 해당 주소로 이동시킨다.
        → 페이지 load 이벤트가 끝날 때까지 자동으로 기다린다.

    expect(page).to_have_title("문자열")
        → <title> 태그 전체와 완전히 일치해야 한다.

    expect(page).to_have_title(re.compile("단어"))
        → <title> 어딘가에 해당 단어가 포함되면 통과.
        → 정규식이므로 re.IGNORECASE 등 옵션도 사용 가능.

◆ 흔한 실수
    ✗ to_have_title("Playwright")
        → "나의 첫 Playwright 앱" 과 다르므로 실패!
    ✓ to_have_title(re.compile("Playwright"))
        → 포함 여부만 검사하므로 통과.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import re
from playwright.sync_api import Page, expect


def test_exact_title(page: Page, base_url: str):
    # goto() 로 페이지 이동 — load 완료까지 자동 대기
    page.goto(base_url)

    # to_have_title() 에 문자열을 넘기면 <title> 과 완전히 일치해야 한다
    expect(page).to_have_title("나의 첫 Playwright 앱")


def test_title_contains_playwright(page: Page, base_url: str):
    page.goto(base_url)

    # re.compile() 을 넘기면 '포함' 여부만 검사
    # → "나의 첫 Playwright 앱" 안에 "Playwright" 가 있으므로 통과
    expect(page).to_have_title(re.compile("Playwright"))


def test_title_both_checks(page: Page, base_url: str):
    # goto() 는 한 번만 호출해도 두 번 검증 가능
    page.goto(base_url)

    # 검증 1: 전체 일치
    expect(page).to_have_title("나의 첫 Playwright 앱")

    # 검증 2: 부분 포함 — "앱" 이라는 단어가 들어있는지
    expect(page).to_have_title(re.compile("앱"))


def test_title_case_insensitive(page: Page, base_url: str):
    page.goto(base_url)

    # re.IGNORECASE 옵션: 대소문자 구분 없이 검색
    # → "playwright" 소문자로 검색해도 "Playwright" 와 매칭됨
    expect(page).to_have_title(re.compile("playwright", re.IGNORECASE))
