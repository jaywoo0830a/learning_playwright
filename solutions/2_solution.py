"""
문제 2 정답 — 버튼 클릭 & URL 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    get_by_role("button", name="텍스트")
        → role="button" 속성이 있는 요소를 찾는다.
        → <a> 태그라도 role="button" 이면 "button" 으로 찾는다.

    get_by_role("link", name="텍스트")
        → href 있는 <a> 태그의 기본 role 은 "link".

    get_by_role("heading", name="텍스트", level=1)
        → h1~h6 은 모두 role="heading".
        → level= 로 h1/h2/... 계층을 좁힐 수 있다.

    expect(page).to_have_url(re.compile("about.html"))
        → URL 에 "about.html" 이 포함되면 통과.
        → 클릭 후 페이지 이동을 자동으로 기다린다.

◆ 흔한 실수
    ✗ get_by_role("link", name="소개 페이지로 이동")
        → role="button" 속성이 있어서 "link" 로는 못 찾는다!
    ✓ get_by_role("button", name="소개 페이지로 이동")
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import re
from playwright.sync_api import Page, expect


def test_button_role_visible(page: Page, base_url: str):
    page.goto(base_url)

    # <a role="button"> 이므로 role="button" 으로 찾는다
    # name= 은 태그 안의 텍스트와 매칭
    expect(
        page.get_by_role("button", name="소개 페이지로 이동")
    ).to_be_visible()


def test_about_page_url(page: Page, base_url: str):
    # about.html 로 직접 이동
    page.goto(f"{base_url}/about.html")

    # re.compile() 로 URL 에 "about.html" 포함 여부만 검사
    # 전체 URL 을 쓰지 않아도 되므로 포트 번호 변경에 영향받지 않는다
    expect(page).to_have_url(re.compile("about.html"))


def test_click_button_and_check_url(page: Page, base_url: str):
    page.goto(base_url)

    # 버튼 클릭 — Playwright 가 페이지 이동 완료까지 자동 대기
    page.get_by_role("button", name="소개 페이지로 이동").click()

    # 이동 후 URL 에 "about.html" 이 포함되는지 검증
    expect(page).to_have_url(re.compile("about.html"))


def test_about_page_heading_and_back_link(page: Page, base_url: str):
    page.goto(f"{base_url}/about.html")

    # h1 은 role="heading", level=1 로 정확히 지정
    expect(
        page.get_by_role("heading", name="소개 페이지", level=1)
    ).to_be_visible()

    # href 있는 <a> 태그의 기본 role 은 "link"
    expect(
        page.get_by_role("link", name="← 메인으로")
    ).to_be_visible()
