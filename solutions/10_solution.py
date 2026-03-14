"""
문제 10 정답 — Heading & Link 탐색 종합
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    get_by_role("heading", level=1)
        → h1 만 찾는다. level= 생략 시 h1~h6 전체.

    get_by_role("navigation", name="주 내비게이션")
        → <nav aria-label="주 내비게이션"> 을 찾는다.
        → 이후 .get_by_role("link") 를 체이닝하면
          nav 안의 링크만 좁혀서 찾을 수 있다.

    locator.first / locator.last
        → 여러 요소 중 첫 번째 / 마지막 하나를 선택.

    to_contain_text("텍스트")
        → 전체 텍스트 중 부분 포함 검증.
        → to_have_text() 는 완전 일치.

◆ 범위 좁히기 패턴 (중요!)
    # ❌ 이렇게 하면 페이지 전체 링크를 세서 "더 읽기" 3개 + nav 3개 = 6개
    expect(page.get_by_role("link")).to_have_count(6)

    # ✅ nav 안의 링크만 세려면 부모 locator 먼저 잡기
    nav = page.get_by_role("navigation", name="주 내비게이션")
    expect(nav.get_by_role("link")).to_have_count(3)

◆ 흔한 실수
    ✗ get_by_role("heading") 으로 h2 개수를 셀 때
        h1 도 포함되므로 예상과 다른 숫자가 나올 수 있다.
    ✓ level=2 를 명시해서 h2 만 정확히 찾는다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_main_heading_level1(page: Page, base_url: str):
    page.goto(base_url)

    # level=1 로 h1 만 정확히 찾아 텍스트 검증
    expect(
        page.get_by_role("heading", level=1)
    ).to_have_text("기술 블로그")


def test_navigation_link_count(page: Page, base_url: str):
    page.goto(base_url)

    # nav 를 먼저 잡아 범위를 좁힌 뒤 그 안의 링크만 센다
    nav = page.get_by_role("navigation", name="주 내비게이션")
    expect(nav.get_by_role("link")).to_have_count(3)


def test_article_counts(page: Page, base_url: str):
    page.goto(base_url)

    # level=2 로 h2 만 찾는다 (h1 제외)
    # 포스트 3개 + 소개 + 연락처 = 총 5개
    expect(page.get_by_role("heading", level=2)).to_have_count(5)

    # name="더 읽기" 로 텍스트가 "더 읽기" 인 링크만 찾는다
    expect(page.get_by_role("link", name="더 읽기")).to_have_count(3)


def test_first_article_heading(page: Page, base_url: str):
    page.goto(base_url)

    headings = page.get_by_role("heading", level=2)

    # .first 로 h2 들 중 첫 번째만 선택
    # to_contain_text() 로 부분 포함 검증
    expect(headings.first).to_contain_text("Playwright로 E2E 테스트 시작하기")
