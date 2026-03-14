"""
문제 10 — Heading & Link 탐색 종합
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① get_by_role("heading", level=N)  → h1~h6 계층 구분해서 찾기
  ② 부모 locator 안에서 자식 찾기     → nav 안의 link 만 찾기
  ③ .first / .last                    → 여러 요소 중 첫/마지막만 선택
  ④ to_contain_text()                 → 텍스트를 "포함"하는지 검증

나선형 학습 순서
  개념1(heading level) → 개념2(범위 좁히기) → 복합1(개수+텍스트) → 복합2(전체 구조)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  heading level 로 계층 구분하기           │
# └─────────────────────────────────────────────────────────┘
def test_main_heading_level1(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        h1 제목이 "기술 블로그" 인지 검사한다.
        level=1 로 h1 만 정확히 찾는다.

    ◆ HTML 구조
        <h1>기술 블로그</h1>
        <h2>Playwright로 E2E 테스트 시작하기</h2>
        <h2>Python으로 자동화 테스트 작성하기</h2>
        ...

    ◆ 개념 설명
        page.get_by_role("heading")
            → h1 ~ h6 을 모두 찾는다.

        page.get_by_role("heading", level=1)
            → h1 만 찾는다. (h2 는 제외)

        page.get_by_role("heading", level=2)
            → h2 만 찾는다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-role

        expect(locator).to_have_text("텍스트")
            → 요소의 텍스트가 정확히 일치하는지 검증한다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-text

    ◆ 예시
        # h1 텍스트가 "기술 블로그" 인지 확인
        expect(page.get_by_role("heading", level=1)).to_have_text("기술 블로그")
    """
    page.goto(base_url)

    # TODO: level=1 로 h1 을 찾아 텍스트가 "기술 블로그" 인지 검증하세요
    # expect(page.get_by_role("heading", level=???)).to_have_text(???)
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  부모 요소 안에서 자식 요소만 찾기        │
# └─────────────────────────────────────────────────────────┘
def test_navigation_link_count(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        페이지의 모든 링크가 아니라
        nav 태그 안의 링크만 정확히 3개인지 검사한다.

    ◆ HTML 구조
        <nav aria-label="주 내비게이션">
            <a href="#posts">포스트</a>   ← nav 안의 링크
            <a href="#about">소개</a>     ← nav 안의 링크
            <a href="#contact">연락처</a> ← nav 안의 링크
        </nav>
        <a href="#" class="read-more">더 읽기</a>  ← nav 밖의 링크

    ◆ 개념 설명
        # 범위를 nav 로 먼저 좁히면 그 안에서만 탐색한다
        nav = page.get_by_role("navigation", name="주 내비게이션")
        nav.get_by_role("link")   # nav 안의 링크만!
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-role

        ※ 그냥 page.get_by_role("link") 를 쓰면
          "더 읽기" 링크까지 포함돼서 개수가 달라진다!

    ◆ 예시
        nav = page.get_by_role("navigation", name="주 내비게이션")
        expect(nav.get_by_role("link")).to_have_count(3)
    """
    page.goto(base_url)

    # STEP 1: aria-label="주 내비게이션" 인 nav 를 찾아 변수에 저장하세요
    # nav = page.get_by_role(???, name=???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: nav 안의 링크 개수가 3개인지 검증하세요
    # expect(nav.get_by_role(???)).to_have_count(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  h2 개수 + "더 읽기" 링크 개수 동시 검증 │
# └─────────────────────────────────────────────────────────┘
def test_article_counts(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        ① h2 제목이 총 5개 (포스트 3 + 소개 + 연락처) 인지
        ② "더 읽기" 링크가 3개인지
        두 가지를 동시에 검증한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 힌트
        # h2 개수 검증 (level=2)
        expect(page.get_by_role("heading", level=2)).to_have_count(5)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count

        # "더 읽기" 링크 개수 검증 (name= 으로 텍스트 필터링)
        expect(page.get_by_role("link", name="더 읽기")).to_have_count(3)
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-role
    """
    page.goto(base_url)

    # STEP 1: h2 제목의 개수가 5개인지 검증하세요
    # expect(page.get_by_role("heading", level=???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "더 읽기" 링크의 개수가 3개인지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_have_count(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  .first + to_contain_text() 로 첫 포스트  │
# └─────────────────────────────────────────────────────────┘
def test_first_article_heading(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        h2 제목 중 맨 첫 번째 것이
        "Playwright로 E2E 테스트 시작하기" 텍스트를 포함하는지 검사한다.

    ◆ 도전 포인트
        h2 가 5개나 있는데 첫 번째 것만 골라야 한다!
        .first 프로퍼티를 사용한다.

    ◆ 개념 설명
        locator.first
            → locator 가 매칭하는 여러 요소 중 첫 번째 요소만 가리킨다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-first

        locator.last
            → 마지막 요소를 가리킨다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-last

        expect(locator).to_contain_text("텍스트")
            → 요소의 텍스트에 주어진 값이 "포함" 되는지 검증한다.
            → to_have_text() 는 완전 일치, to_contain_text() 는 부분 포함.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-contain-text

    ◆ 예시
        headings = page.get_by_role("heading", level=2)
        expect(headings.first).to_contain_text("Playwright")  # 첫 번째 h2 에 "Playwright" 포함
        expect(headings.last).to_contain_text("연락처")       # 마지막 h2 에 "연락처" 포함
    """
    page.goto(base_url)

    # STEP 1: h2 heading 전체를 locator 로 찾아 변수에 저장하세요
    # headings = page.get_by_role(???, level=???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 첫 번째 h2(.first) 에 "Playwright로 E2E 테스트 시작하기" 가 포함되는지 검증하세요
    # expect(headings.first).to_contain_text(???)
