"""
문제 2 — 버튼 클릭 & URL 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① get_by_role()       → HTML 태그의 "역할(role)" 로 요소를 찾는다
  ② to_have_url()       → 페이지 이동 후 주소(URL) 가 맞는지 검증한다
  ③ to_be_visible()     → 요소가 화면에 실제로 보이는지 검증한다

나선형 학습 순서
  개념1(role 찾기) → 개념2(URL 검증) → 복합1(클릭+URL) → 복합2(이동+제목)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import re
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  get_by_role() 로 요소 찾기              │
# └─────────────────────────────────────────────────────────┘
def test_button_role_visible(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        페이지에 "소개 페이지로 이동" 버튼이 화면에 보이는지만 검사한다.
        (클릭은 아직 하지 않는다!)

    ◆ HTML 구조
        <a href="about.html" role="button">소개 페이지로 이동</a>

    ◆ 개념 설명
        HTML 태그마다 브라우저가 자동으로 "역할(role)" 을 부여한다.
        Playwright 는 이 역할을 이용해 요소를 찾는다.

        주요 태그 → role 대응표
        ┌──────────────────────────────┬─────────────┐
        │ HTML 태그                    │    role     │
        ├──────────────────────────────┼─────────────┤
        │ <button>                     │  "button"   │
        │ <a href="...">               │  "link"     │  ← href 있으면 link
        │ <a role="button">            │  "button"   │  ← role 속성으로 덮어쓰기
        │ <h1> ~ <h6>                  │  "heading"  │
        │ <input type="checkbox">      │  "checkbox" │
        │ <nav>                        │ "navigation"│
        │ <ul> / <ol>                  │  "list"     │
        │ <li>                         │  "listitem" │
        └──────────────────────────────┴─────────────┘

        page.get_by_role("role이름", name="태그 안의 텍스트")
            → role 이름과 텍스트가 일치하는 요소를 찾는다.
        📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-role

    ◆ 예시
        # <button>로그인</button>
        page.get_by_role("button", name="로그인")

        # <a href="...">홈으로</a>
        page.get_by_role("link", name="홈으로")

        # <a role="button">소개 페이지로 이동</a>  ← role 속성이 있으니 button 으로!
        page.get_by_role("button", name="소개 페이지로 이동")
    """
    page.goto(base_url)

    # TODO: role="button", name="소개 페이지로 이동" 인 요소가 보이는지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  to_have_url() 로 주소 검증              │
# └─────────────────────────────────────────────────────────┘
def test_about_page_url(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        about.html 로 직접 이동했을 때
        현재 URL 이 "about.html" 로 끝나는지 검사한다.

    ◆ 개념 설명
        expect(page).to_have_url("주소")
            → 현재 페이지 URL 이 주어진 값과 맞는지 검증한다.
            → 문자열을 넘기면 전체 일치,
               re.compile() 을 넘기면 포함 여부 검사.
            📖 공식문서: https://playwright.dev/python/docs/api/class-pageassertions#page-assertions-to-have-url

        비교 방식 차이
            to_have_url("http://127.0.0.1:8102/about.html")  # 전체 URL 이 완전히 같아야 함
            to_have_url(re.compile("about.html"))             # URL 에 "about.html" 만 포함되면 됨

        ※ re.compile("about\\.html") 에서 \\.  는
          정규식에서 점(.) 을 "진짜 점" 으로 취급한다는 표시이다.
          (정규식에서 . 는 "아무 글자" 라는 뜻이라 주의!)

    ◆ 예시
        page.goto(f"{base_url}/about.html")                  # about.html 로 이동
        expect(page).to_have_url(re.compile("about.html"))   # URL 확인
    """
    page.goto(f"{base_url}/about.html")

    # TODO: 현재 URL 에 "about.html" 이 포함되는지 re.compile() 로 검증하세요
    # expect(page).to_have_url(re.compile(???))
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  버튼 클릭 → URL 변경 검증               │
# └─────────────────────────────────────────────────────────┘
def test_click_button_and_check_url(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "소개 페이지로 이동" 버튼을 클릭하면
        URL 이 about.html 로 바뀌는지 검사한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ HTML 구조
        <a href="about.html" role="button">소개 페이지로 이동</a>

    ◆ 힌트
        # 버튼 찾아서 클릭
        page.get_by_role("button", name="...").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

        # URL 검증 (클릭 후 Playwright 가 자동으로 페이지 이동을 기다린다)
        expect(page).to_have_url(re.compile("about.html"))
            📖 공식문서: https://playwright.dev/python/docs/api/class-pageassertions#page-assertions-to-have-url
    """
    page.goto(base_url)

    # STEP 1: "소개 페이지로 이동" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: URL 에 "about.html" 이 포함되는지 검증하세요
    # expect(page).to_have_url(re.compile(???))


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  페이지 이동 후 제목 + 링크 동시 검증    │
# └─────────────────────────────────────────────────────────┘
def test_about_page_heading_and_back_link(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        about.html 에 두 가지가 동시에 존재해야 한다:
          1) "소개 페이지" 라는 h1 제목
          2) "← 메인으로" 라는 링크

    ◆ HTML 구조 (about.html)
        <h1>소개 페이지</h1>
        <a href="index.html">← 메인으로</a>

    ◆ 힌트
        # h1 ~ h6 은 모두 role="heading"
        # level= 로 계층을 좁힐 수 있다
        page.get_by_role("heading", name="소개 페이지", level=1)
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-role

        # href 있는 <a> 태그의 기본 role 은 "link"
        page.get_by_role("link", name="← 메인으로")
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-role

        # 두 요소 모두 to_be_visible() 로 검증
        expect(요소).to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(f"{base_url}/about.html")

    # STEP 1: "소개 페이지" h1 제목이 보이는지 검증하세요
    # expect(page.get_by_role(???, name=???, level=???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "← 메인으로" 링크가 보이는지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_visible()
