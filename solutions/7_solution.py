"""
문제 7 정답 — 이미지 alt 텍스트 & 갤러리 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 버그 수정 내역 (HTML 변경)
    기존: SVG 와 img 둘 다 같은 alt 텍스트를 가짐
        → get_by_alt_text("산 풍경") 이 두 요소를 동시에 찾음
        → Locator strict mode 위반 → 오류 발생!

    수정: SVG 를 제거하고 img 에 inline SVG data URI 를 src 로 사용
        → alt 텍스트가 img 하나에만 존재
        → get_by_alt_text() 가 정확히 하나만 찾음

◆ 핵심 정리
    get_by_alt_text("텍스트")
        → img 태그의 alt 속성으로 이미지를 찾는다.
        → alt 가 같은 요소가 여러 개면 strict 오류 발생!
          → 이런 경우 .first / .nth(n) 으로 특정하거나 HTML 을 수정해야 한다.

    to_have_attribute("속성명", "값")
        → 요소의 특정 HTML 속성이 기대한 값인지 검증.

    to_have_count(N)
        → locator 가 매칭하는 요소 수 검증.

◆ Locator strict mode 란?
    Playwright 의 locator 는 기본적으로 "엄격(strict)" 하다.
    → 조건에 맞는 요소가 2개 이상이면 오류를 낸다.
    → 의도치 않은 요소를 건드리는 사고를 예방하기 위한 안전장치.
    → 여러 개 중 하나를 골라야 할 때는 .first / .nth() / filter() 사용.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_mountain_image_visible(page: Page, base_url: str):
    page.goto(base_url)

    # alt 텍스트로 img 를 찾아 alt 속성 값 검증
    # HTML 수정으로 img 가 하나뿐이라 strict 오류 없음
    img = page.get_by_alt_text("산 풍경")
    expect(img).to_have_attribute("alt", "산 풍경")


def test_gallery_image_count(page: Page, base_url: str):
    page.goto(base_url)

    # page.locator("img") → 페이지의 모든 img 태그를 한 번에 찾는다
    # to_have_count(3) → 3개인지 검증
    expect(page.locator("img")).to_have_count(3)


def test_all_alt_texts_exist(page: Page, base_url: str):
    page.goto(base_url)

    # 3개 이미지 각각의 alt 속성을 검증
    # get_by_alt_text() 로 찾고 to_have_attribute() 로 속성 확인
    expect(
        page.get_by_alt_text("산 풍경")
    ).to_have_attribute("alt", "산 풍경")

    expect(
        page.get_by_alt_text("바다 풍경")
    ).to_have_attribute("alt", "바다 풍경")

    expect(
        page.get_by_alt_text("숲 풍경")
    ).to_have_attribute("alt", "숲 풍경")


def test_gallery_structure(page: Page, base_url: str):
    page.goto(base_url)

    # img 와 figcaption 이 각각 3개씩 있는지 한 테스트에서 모두 검증
    expect(page.locator("img")).to_have_count(3)
    expect(page.locator("figcaption")).to_have_count(3)
