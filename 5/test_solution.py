"""
문제 5 — 플레이스홀더 검색 & 키보드 입력
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① get_by_placeholder()  → placeholder 속성으로 input 찾기
  ② press("Enter")        → 키보드 키 누르기
  ③ 둘을 조합한 검색 흐름

나선형 학습 순서
  개념1(placeholder 찾기) → 개념2(키 누르기) → 복합1(검색 성공) → 복합2(검색 실패)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  get_by_placeholder() 로 input 찾기      │
# └─────────────────────────────────────────────────────────┘
def test_search_input_exists(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        placeholder 가 "제품명을 검색하세요" 인 input 이
        화면에 존재하는지 검사한다.

    ◆ HTML 구조
        <input type="search" placeholder="제품명을 검색하세요" />

    ◆ 개념 설명
        page.get_by_placeholder("placeholder 텍스트")
            → input 태그의 placeholder 속성 값으로 요소를 찾는다.
            → label 이 없는 검색창, 필터 입력창에 주로 사용한다.
            → label 이 있다면 get_by_label() 을 우선 쓰는 것이 좋다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-placeholder

    ◆ 예시
        # <input placeholder="이름을 입력하세요" />
        page.get_by_placeholder("이름을 입력하세요")        # 찾기
        expect(page.get_by_placeholder("이름을 입력하세요")).to_be_visible()  # 보이는지 확인
    """
    page.goto(base_url)

    # TODO: placeholder "제품명을 검색하세요" 인 input 이 화면에 보이는지 검증하세요
    # expect(page.get_by_placeholder(???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  press() 로 키보드 키 누르기              │
# └─────────────────────────────────────────────────────────┘
def test_press_enter_shows_results(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        검색창에 값을 입력하고 Enter 를 눌렀을 때
        결과가 나타나는지 검사한다.

    ◆ HTML 구조
        <input placeholder="제품명을 검색하세요" />
        <!-- Enter 입력 시 결과 렌더링 -->
        <div class="result-item">노트북 Pro</div>

    ◆ 개념 설명
        locator.press("키이름")
            → 키보드의 특정 키를 누른다.
            → fill() 로 입력 후 press() 로 전송하는 패턴이 일반적이다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press

        자주 쓰는 키 이름
        ┌──────────────────┬────────────────┐
        │ 누를 키          │ 키 이름         │
        ├──────────────────┼────────────────┤
        │ 엔터             │ "Enter"        │
        │ 탭               │ "Tab"          │
        │ 위쪽 화살표      │ "ArrowUp"      │
        │ 아래쪽 화살표    │ "ArrowDown"    │
        │ Escape           │ "Escape"       │
        └──────────────────┴────────────────┘
        📖 전체 키 목록: https://playwright.dev/python/docs/api/class-keyboard

    ◆ 예시
        search = page.get_by_placeholder("검색어 입력")
        search.fill("노트북")    # 먼저 입력하고
        search.press("Enter")   # 그 다음 Enter 를 누른다
    """
    page.goto(base_url)

    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("노트북")

    # TODO: "Enter" 키를 눌러서 검색을 실행하세요
    # search.press(???)
    raise NotImplementedError("TODO를 완성하세요")

    # 결과가 나타나는지 확인 (이 부분은 완성됨)
    expect(page.get_by_text("노트북 Pro")).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  검색어 입력 + 엔터 + 결과 검증          │
# └─────────────────────────────────────────────────────────┘
def test_search_found(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "키보드" 를 검색하면 "기계식 키보드" 결과가 나와야 한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 힌트
        # placeholder 로 검색창 찾기
        search = page.get_by_placeholder("제품명을 검색하세요")
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-placeholder

        # 입력 + 엔터
        search.fill("키보드")
        search.press("Enter")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press

        # 결과 검증
        expect(page.get_by_text("기계식 키보드")).to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(base_url)

    # STEP 1: placeholder 로 검색창을 찾아 변수에 저장하세요
    # search = page.get_by_placeholder(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "키보드" 를 입력하세요
    # search.fill(???)

    # STEP 3: "Enter" 를 눌러 검색을 실행하세요
    # search.press(???)

    # STEP 4: "기계식 키보드" 결과가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  없는 제품 검색 → 안내 메시지 검증       │
# └─────────────────────────────────────────────────────────┘
def test_search_no_result(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        존재하지 않는 제품을 검색하면
        "검색 결과가 없습니다." 가 나와야 한다.
        그리고 실제 결과 아이템은 하나도 보이면 안 된다!

    ◆ 힌트
        # 없는 제품 검색
        search.fill("없는제품xyz")
        search.press("Enter")

        # 안내 메시지가 보이는지
        expect(page.get_by_text("검색 결과가 없습니다.")).to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible

        # 결과 아이템이 하나도 없는지 (개수가 0 인지)
        expect(page.locator(".result-item")).to_have_count(0)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count
    """
    page.goto(base_url)

    search = page.get_by_placeholder("제품명을 검색하세요")

    # STEP 1: "없는제품xyz" 를 입력하고 Enter 를 누르세요
    # search.fill(???)
    # search.press(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "검색 결과가 없습니다." 메시지가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()

    # STEP 3: ".result-item" 요소의 개수가 0 인지 검증하세요
    # expect(page.locator(???)).to_have_count(???)
