"""
문제 7 — 이미지 alt 텍스트 & 갤러리 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① get_by_alt_text()   → alt 속성으로 이미지 찾기
  ② to_have_count()     → 요소 개수 검증
  ③ to_have_attribute() → 요소의 특정 속성 값 검증

나선형 학습 순서
  개념1(alt로 찾기) → 개념2(개수 세기) → 복합1(속성 검증) → 복합2(전체 갤러리)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  get_by_alt_text() 로 이미지 찾기        │
# └─────────────────────────────────────────────────────────┘
def test_mountain_image_visible(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        alt="산 풍경" 인 이미지가 페이지에 존재하는지 검사한다.

    ◆ HTML 구조
        <img src="" alt="산 풍경" />

    ◆ 개념 설명
        page.get_by_alt_text("alt 텍스트")
            → img 태그의 alt 속성 값으로 이미지를 찾는다.
            → alt 속성은 이미지가 안 보일 때 나타나는 대체 텍스트이고
               시각장애인을 위한 스크린리더도 이 값을 읽는다.
            → img, area 요소에만 사용 가능하다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-alt-text

        expect(locator).to_have_attribute("속성명", "기대값")
            → 요소의 특정 속성이 기대한 값인지 검증한다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-attribute

    ◆ 예시
        # <img alt="회사 로고" src="logo.png" />
        img = page.get_by_alt_text("회사 로고")
        expect(img).to_have_attribute("alt", "회사 로고")
    """
    page.goto(base_url)

    # TODO: alt 텍스트 "산 풍경" 으로 이미지를 찾아
    #        alt 속성이 "산 풍경" 인지 검증하세요
    # img = page.get_by_alt_text(???)
    # expect(img).to_have_attribute(???, ???)
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  to_have_count() 로 요소 개수 세기       │
# └─────────────────────────────────────────────────────────┘
def test_gallery_image_count(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        갤러리에 img 태그가 정확히 3개 있는지 검사한다.

    ◆ HTML 구조
        <img alt="산 풍경" />
        <img alt="바다 풍경" />
        <img alt="숲 풍경" />

    ◆ 개념 설명
        page.locator("CSS 셀렉터")
            → CSS 셀렉터로 요소를 찾는다.
            → 여러 개를 한 번에 찾을 수 있다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-css-or-xpath

        expect(locator).to_have_count(숫자)
            → locator 가 매칭하는 요소의 개수가 맞는지 검증한다.
            → 동적으로 렌더링되는 목록에서 특히 유용하다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count

    ◆ 예시
        # 페이지의 모든 li 개수가 5개인지 확인
        expect(page.locator("li")).to_have_count(5)

        # 페이지의 모든 img 개수가 3개인지 확인
        expect(page.locator("img")).to_have_count(3)
    """
    page.goto(base_url)

    # TODO: "img" 태그를 locator 로 찾아 개수가 3개인지 검증하세요
    # expect(page.locator(???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  alt 텍스트 3개 모두 존재하는지 검증     │
# └─────────────────────────────────────────────────────────┘
def test_all_alt_texts_exist(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        갤러리의 이미지 3개가 모두 올바른 alt 텍스트를 가지는지 검사한다.
        (개념 문제 ① 을 3번 반복하는 문제!)

    ◆ 힌트
        # alt 로 찾아서 속성 검증 (3번 반복)
        expect(page.get_by_alt_text("산 풍경")).to_have_attribute("alt", "산 풍경")
        expect(page.get_by_alt_text("바다 풍경")).to_have_attribute("alt", "바다 풍경")
        expect(page.get_by_alt_text("숲 풍경")).to_have_attribute("alt", "숲 풍경")
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-alt-text
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-attribute
    """
    page.goto(base_url)

    # TODO: "산 풍경" alt 이미지의 alt 속성이 "산 풍경" 인지 검증하세요
    # expect(page.get_by_alt_text(???)).to_have_attribute(???, ???)
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "바다 풍경", "숲 풍경" 도 각각 검증하세요
    # expect(page.get_by_alt_text(???)).to_have_attribute(???, ???)
    # expect(page.get_by_alt_text(???)).to_have_attribute(???, ???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  img 개수 + figcaption 개수 동시 검증    │
# └─────────────────────────────────────────────────────────┘
def test_gallery_structure(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        img 태그가 3개이고 figcaption 태그도 3개인지
        두 가지를 동시에 검증한다.
        (개념 문제 ② 를 두 번 응용하는 문제!)

    ◆ HTML 구조
        <figure>
            <img alt="산 풍경" />
            <figcaption>산 풍경</figcaption>
        </figure>
        ... (3개 반복)

    ◆ 힌트
        # img 개수 검증
        expect(page.locator("img")).to_have_count(3)

        # figcaption 개수 검증
        expect(page.locator("figcaption")).to_have_count(3)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count
    """
    page.goto(base_url)

    # STEP 1: "img" 태그의 개수가 3개인지 검증하세요
    # expect(page.locator(???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "figcaption" 태그의 개수도 3개인지 검증하세요
    # expect(page.locator(???)).to_have_count(???)
