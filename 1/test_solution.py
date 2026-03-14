"""
문제 1 — 페이지 타이틀 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① page.goto()         → 브라우저가 주소로 이동
  ② to_have_title()    → 페이지 제목(<title>) 검증
  ③ re.compile()       → "정확히 일치" 대신 "포함 여부" 확인

나선형 학습 순서
  개념1 → 개념2 → 복합1 → 복합2
  (아래로 내려갈수록 두 개념을 동시에 써야 해요!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import re
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  page.goto() + to_have_title() 전체 일치  │
# └─────────────────────────────────────────────────────────┘
def test_exact_title(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        브라우저가 페이지를 열었을 때
        <title> 태그의 내용이 정확히 맞는지 검사한다.

    ◆ HTML 구조
        <title>나의 첫 Playwright 앱</title>

    ◆ 개념 설명
        page.goto(주소)
            → 브라우저를 그 주소로 이동시킨다.
              마치 주소창에 URL 을 직접 치는 것과 같다.
            → 페이지 로딩이 완전히 끝날 때까지 자동으로 기다린다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-page#page-goto

        expect(page).to_have_title("제목")
            → 현재 페이지의 <title> 이 문자열과 완전히 같은지 검증한다.
            → 글자 하나라도 다르면 테스트 실패!
            📖 공식문서: https://playwright.dev/python/docs/api/class-pageassertions#page-assertions-to-have-title

    ◆ 예시
        # <title>안녕하세요</title> 라면
        expect(page).to_have_title("안녕하세요")   # ✅ 통과
        expect(page).to_have_title("안녕")         # ❌ 실패 (전체가 달라서)
    """
    # STEP 1: base_url 주소로 이동하세요
    # page.goto(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 타이틀이 "나의 첫 Playwright 앱" 과 정확히 같은지 검증하세요
    # expect(page).to_have_title(???)


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  re.compile() 로 "포함" 여부 검증         │
# └─────────────────────────────────────────────────────────┘
def test_title_contains_playwright(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        타이틀에 "Playwright" 라는 단어가 들어있기만 하면 통과.

    ◆ HTML 구조
        <title>나의 첫 Playwright 앱</title>

    ◆ 개념 설명
        re.compile("찾을 단어")
            → 정규식(Regular Expression) 패턴 객체를 만든다.
            → Playwright 에 넘기면 "포함 여부" 검사로 바뀐다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-pageassertions#page-assertions-to-have-title

        문자열 vs re.compile() 차이
            to_have_title("Playwright")            # ❌ "Playwright" 와 완전히 같아야 함
            to_have_title(re.compile("Playwright")) # ✅ "Playwright" 가 어딘가 있으면 됨

        대소문자를 무시하고 싶다면?
            re.compile("playwright", re.IGNORECASE)
            → "PLAYWRIGHT", "Playwright", "playwright" 모두 통과

    ◆ 예시
        # <title>나의 첫 Playwright 앱</title>
        expect(page).to_have_title(re.compile("Playwright"))  # ✅ 포함되어 있으니 통과
        expect(page).to_have_title(re.compile("Vue"))         # ❌ 없으니 실패
    """
    page.goto(base_url)

    # TODO: re.compile() 을 사용해 타이틀에 "Playwright" 가 포함되는지 검증하세요
    # expect(page).to_have_title(re.compile(???))
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  goto + 전체일치 + 포함여부 동시에        │
# └─────────────────────────────────────────────────────────┘
def test_title_both_checks(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        하나의 테스트 안에서
        전체 일치 검증과 포함 여부 검증을 모두 수행한다.

    ◆ 도전 포인트
        goto() 는 한 번만 호출하고
        to_have_title() 을 두 가지 방식으로 각각 써야 한다.

    ◆ 힌트
        page.goto(주소)                                   # 이동 (한 번만)
        expect(page).to_have_title("전체 제목")           # 전체 일치
        expect(page).to_have_title(re.compile("단어"))    # 포함 여부
        📖 공식문서: https://playwright.dev/python/docs/writing-tests#assertions
    """
    # STEP 1: base_url 로 이동하세요
    # page.goto(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 타이틀이 "나의 첫 Playwright 앱" 과 정확히 같은지 검증하세요
    # expect(page).to_have_title(???)

    # STEP 3: re.compile() 로 "앱" 이라는 단어가 포함되는지 검증하세요
    # expect(page).to_have_title(re.compile(???))


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  대소문자 무시 옵션까지 활용              │
# └─────────────────────────────────────────────────────────┘
def test_title_case_insensitive(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        대소문자를 신경 쓰지 않고 "playwright" 가 포함되는지 확인한다.
        (실무에서 타이틀이 대소문자가 섞여 있을 때 유용하다!)

    ◆ 도전 포인트
        re.IGNORECASE 옵션을 추가해서
        "playwright" 소문자로 검색해도 통과시켜야 한다.

    ◆ 힌트
        re.compile("찾을단어", re.IGNORECASE)
            → 대소문자 무시 옵션
            → "PLAYWRIGHT", "Playwright", "playwright" 모두 매칭
        📖 공식문서: https://playwright.dev/python/docs/api/class-pageassertions#page-assertions-to-have-title
        📖 Python re 모듈: https://docs.python.org/3/library/re.html#re.IGNORECASE
    """
    page.goto(base_url)

    # TODO: re.IGNORECASE 옵션을 사용해서
    #       소문자 "playwright" 로 검색해도 타이틀에 포함되는지 검증하세요
    # expect(page).to_have_title(re.compile(???, ???))
    raise NotImplementedError("TODO를 완성하세요")
