import re
from playwright.sync_api import Page, expect


# ═══════════════════════════════════════════════════════════════
# 개념 문제 1 — button role 로 요소 찾기
# ═══════════════════════════════════════════════════════════════

def test_button_role_exists(page: Page, base_url: str):
    """
    HTML:
        <a href="about.html" role="button">소개 페이지로 이동</a>

    role="button" 속성이 붙은 <a> 태그가 페이지에 존재해야 한다.
    클릭은 하지 않고 존재 여부만 검증한다.
    """
    page.goto(base_url)

    # ─────────────────────────────────────────────────────────
    # <a> 태그의 기본 role 은 "link" 이지만
    # role="button" 속성을 명시하면 "button" 으로 바뀐다.
    #
    # get_by_role("button", name="...")
    #   → name= 은 태그 안의 텍스트와 매칭
    #
    # TODO: "소개 페이지로 이동" 버튼이 보이는지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")


def test_heading_role_exists(page: Page, base_url: str):
    """
    HTML:
        <h1>메인 페이지</h1>

    <h1> 태그의 role 은 "heading" 이다.
    페이지에 "메인 페이지" 제목이 존재해야 한다.
    """
    page.goto(base_url)

    # ─────────────────────────────────────────────────────────
    # <h1> ~ <h6> 은 모두 role="heading"
    # level= 로 계층을 좁힐 수 있다.
    #
    #   get_by_role("heading", name="제목")            # h1~h6 전체
    #   get_by_role("heading", name="제목", level=1)   # h1 만
    #
    # TODO: "메인 페이지" 라는 h1 제목이 보이는지 검증하세요 (level=1)
    # expect(page.get_by_role(???, name=???, level=???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")


# ═══════════════════════════════════════════════════════════════
# 개념 문제 2 — link role 과 heading role 구분
# ═══════════════════════════════════════════════════════════════

def test_link_role_on_about_page(page: Page, base_url: str):
    """
    HTML (about.html):
        <a href="index.html">← 메인으로</a>

    role= 속성이 없는 <a href="..."> 의 기본 role 은 "link" 이다.
    about.html 에 "← 메인으로" 링크가 존재해야 한다.
    """
    page.goto(f"{base_url}/about.html")

    # ─────────────────────────────────────────────────────────
    # href 가 있는 <a> 태그  → role="link"   (기본)
    # href 가 없는 <a> 태그  → role="generic" (링크 아님)
    #
    # get_by_role("link", name="...")
    #   → name= 은 링크 안의 텍스트와 매칭
    #
    # TODO: "← 메인으로" 링크가 존재하는지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")


def test_about_page_heading_level(page: Page, base_url: str):
    """
    HTML (about.html):
        <h1>소개 페이지</h1>

    about.html 의 h1 제목이 정확히 "소개 페이지" 여야 한다.
    to_have_text() 로 텍스트 내용까지 검증한다.
    """
    page.goto(f"{base_url}/about.html")

    # ─────────────────────────────────────────────────────────
    # to_be_visible()  → 요소가 화면에 보이는지만 검증
    # to_have_text()   → 요소의 텍스트 내용까지 검증
    #
    # 더 엄격하게 검증하려면 to_have_text() 를 사용한다.
    #
    # TODO: h1 제목의 텍스트가 정확히 "소개 페이지" 인지 검증하세요
    # expect(page.get_by_role("heading", level=1)).to_have_text(???)
    raise NotImplementedError("TODO를 완성하세요")


# ═══════════════════════════════════════════════════════════════
# 복합 문제 1 — 버튼 클릭 → URL 변경 검증
# ═══════════════════════════════════════════════════════════════

def test_click_button_and_check_url(page: Page, base_url: str):
    """
    HTML (index.html):
        <a href="about.html" role="button">소개 페이지로 이동</a>

    버튼을 클릭하면 URL 이 about.html 로 바뀌어야 한다.
    클릭 액션 + URL 검증을 함께 수행한다.
    """
    page.goto(base_url)

    # ─────────────────────────────────────────────────────────
    # STEP 1: role="button" 요소를 찾아 클릭
    #
    # TODO: "소개 페이지로 이동" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # ─────────────────────────────────────────────────────────
    # STEP 2: URL 에 "about.html" 이 포함되는지 검증
    #
    #   to_have_url("전체URL")            → 완전 일치
    #   to_have_url(re.compile("부분"))   → 부분 포함
    #
    # TODO: URL 에 "about.html" 이 포함되는지 정규식으로 검증하세요
    # expect(page).to_have_url(re.compile(???))


# ═══════════════════════════════════════════════════════════════
# 복합 문제 2 — 페이지 이동 후 제목 + 링크 동시 검증
# ═══════════════════════════════════════════════════════════════

def test_about_page_heading_and_back_link(page: Page, base_url: str):
    """
    HTML (about.html):
        <h1>소개 페이지</h1>
        <a href="index.html">← 메인으로</a>

    about.html 에는 h1 제목과 메인으로 돌아가는 링크가
    동시에 존재해야 한다.
    """
    page.goto(f"{base_url}/about.html")

    # ─────────────────────────────────────────────────────────
    # STEP 1: h1 제목 검증
    #
    # TODO: "소개 페이지" h1 제목이 보이는지 검증하세요
    # expect(page.get_by_role(???, name=???, level=???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")

    # ─────────────────────────────────────────────────────────
    # STEP 2: 뒤로 가는 링크 검증
    #
    # TODO: "← 메인으로" 링크가 보이는지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_visible()