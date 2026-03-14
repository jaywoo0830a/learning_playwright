"""
문제 8 — 할 일 목록 개수 & 내용 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① get_by_test_id()   → data-testid 속성으로 요소 찾기
  ② to_have_count()    → 목록 개수 검증
  ③ to_have_text([])   → 목록 전체 텍스트를 한 번에 검증

나선형 학습 순서
  개념1(testid 찾기) → 개념2(텍스트 목록) → 복합1(추가 후 개수) → 복합2(전체 흐름)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  get_by_test_id() + to_have_count()      │
# └─────────────────────────────────────────────────────────┘
def test_initial_item_count(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        처음 페이지를 열었을 때 할 일 항목이 정확히 3개인지 검사한다.

    ◆ HTML 구조
        <li data-testid="todo-item">Playwright 설치하기 ...</li>
        <li data-testid="todo-item">첫 테스트 작성하기 ...</li>
        <li data-testid="todo-item">CI 연동하기 ...</li>

    ◆ 개념 설명
        page.get_by_test_id("testid 값")
            → data-testid="값" 속성을 가진 요소를 찾는다.
            → 텍스트나 역할이 바뀌어도 테스트가 깨지지 않아서 가장 안정적이다.
            → 개발자와 QA 가 함께 협의해서 정해두는 "테스트 전용 ID" 이다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-test-id

        expect(locator).to_have_count(숫자)
            → locator 가 매칭하는 요소의 개수를 검증한다.
            → 동적으로 항목이 추가/삭제되는 목록에 유용하다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count

    ◆ 예시
        # data-testid="todo-item" 인 요소가 3개인지 확인
        items = page.get_by_test_id("todo-item")
        expect(items).to_have_count(3)
    """
    page.goto(base_url)

    # STEP 1: data-testid="todo-item" 인 요소들을 찾아 변수에 저장하세요
    # items = page.get_by_test_id(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 항목 개수가 3개인지 검증하세요
    # expect(items).to_have_count(???)


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  to_have_text([]) 로 목록 전체 검증      │
# └─────────────────────────────────────────────────────────┘
def test_item_texts(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        3개 항목의 텍스트가 순서대로 정확히 맞는지 검사한다.

    ◆ HTML 구조
        <li data-testid="todo-item">Playwright 설치하기 <button>완료</button></li>
        <li data-testid="todo-item">첫 테스트 작성하기 <button>완료</button></li>
        <li data-testid="todo-item">CI 연동하기 <button>완료</button></li>
        ※ li 안에 텍스트 + "완료" 버튼이 함께 있음!

    ◆ 개념 설명
        expect(locator).to_have_text(["텍스트1", "텍스트2", ...])
            → locator 가 매칭하는 여러 요소의 텍스트를 리스트로 한 번에 검증한다.
            → 순서도 정확히 맞아야 한다.
            → 각 요소의 전체 텍스트(자식 요소 포함)를 비교한다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-text

    ◆ 예시
        # li 3개의 텍스트를 순서대로 검증
        expect(page.get_by_test_id("todo-item")).to_have_text([
            "첫 번째 항목 완료",
            "두 번째 항목 완료",
            "세 번째 항목 완료",
        ])
        # ※ "완료" 는 버튼 텍스트까지 포함된 전체 텍스트
    """
    page.goto(base_url)

    items = page.get_by_test_id("todo-item")

    # TODO: 3개 항목의 텍스트를 리스트로 한 번에 검증하세요
    #        각 li 의 전체 텍스트 (텍스트 + "완료" 포함) 를 써야 합니다
    # expect(items).to_have_text([???, ???, ???])
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  항목 추가 후 개수 변화 검증             │
# └─────────────────────────────────────────────────────────┘
def test_add_item_increases_count(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        새 항목을 추가하면 개수가 3 → 4개로 늘어나는지 검사한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 힌트
        # 먼저 입력창에 새 항목 입력
        page.get_by_placeholder("새 할 일 입력").fill("문서 작성하기")
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-placeholder

        # "추가" 버튼 클릭
        page.get_by_role("button", name="추가").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

        # 개수가 4개로 늘었는지 검증
        expect(page.get_by_test_id("todo-item")).to_have_count(4)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count
    """
    page.goto(base_url)

    # STEP 1: "새 할 일 입력" placeholder 로 input 을 찾아 "문서 작성하기" 를 입력하세요
    # page.get_by_placeholder(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "추가" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()

    # STEP 3: 항목 개수가 4개가 됐는지 검증하세요
    # expect(page.get_by_test_id(???)).to_have_count(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  추가 후 새 항목 텍스트까지 검증         │
# └─────────────────────────────────────────────────────────┘
def test_add_item_and_verify_text(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        새 항목 추가 후 그 항목의 텍스트가 목록 마지막에 있는지 검사한다.
        개수뿐만 아니라 추가된 내용도 검증하는 더 꼼꼼한 테스트!

    ◆ 도전 포인트
        .last 프로퍼티로 목록의 마지막 요소만 골라서 검증할 수 있다.

    ◆ 힌트
        items = page.get_by_test_id("todo-item")

        # 마지막 항목만 골라서 텍스트 검증
        expect(items.last).to_contain_text("문서 작성하기")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-last
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-contain-text
    """
    page.goto(base_url)

    page.get_by_placeholder("새 할 일 입력").fill("문서 작성하기")
    page.get_by_role("button", name="추가").click()

    items = page.get_by_test_id("todo-item")

    # STEP 1: 전체 개수가 4개인지 검증하세요
    # expect(items).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 마지막 항목(.last)의 텍스트에 "문서 작성하기" 가 포함되는지 검증하세요
    # expect(items.last).to_contain_text(???)
