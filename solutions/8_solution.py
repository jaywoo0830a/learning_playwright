"""
문제 8 정답 — 할 일 목록 개수 & 내용 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    get_by_test_id("값")
        → data-testid="값" 속성으로 요소를 찾는다.
        → 텍스트나 스타일이 바뀌어도 테스트가 깨지지 않아 가장 안정적.
        → 개발자와 QA 가 협의해서 미리 달아두는 "테스트 전용 ID".

    to_have_text(["텍스트1", "텍스트2", ...])
        → 여러 요소의 텍스트를 순서대로 한 번에 검증.
        → 각 요소의 전체 텍스트(자식 요소 포함)를 비교한다.
        → 개수와 순서가 모두 맞아야 통과.

    items.last
        → locator 가 찾는 여러 요소 중 마지막 요소.
        → items.first → 첫 번째, items.nth(n) → n번째 (0부터 시작).

    to_contain_text("텍스트")
        → 요소 텍스트에 해당 값이 "포함" 되는지 검증.
        → to_have_text() 는 전체 일치, to_contain_text() 는 부분 포함.

◆ to_have_text() 주의사항
    li 안에 버튼이 있으면 전체 텍스트에 버튼 텍스트도 포함된다.
    예: <li>Playwright 설치하기 <button>완료</button></li>
        → 전체 텍스트 = "Playwright 설치하기 완료"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_initial_item_count(page: Page, base_url: str):
    page.goto(base_url)

    # get_by_test_id() 로 data-testid="todo-item" 인 요소 전체를 가져온다
    items = page.get_by_test_id("todo-item")
    expect(items).to_have_count(3)


def test_item_texts(page: Page, base_url: str):
    page.goto(base_url)

    items = page.get_by_test_id("todo-item")

    # 리스트로 넘기면 순서대로 각 요소의 전체 텍스트를 비교
    # "완료" 는 버튼 텍스트까지 포함한 전체 텍스트
    expect(items).to_have_text([
        "Playwright 설치하기 완료",
        "첫 테스트 작성하기 완료",
        "CI 연동하기 완료",
    ])


def test_add_item_increases_count(page: Page, base_url: str):
    page.goto(base_url)

    page.get_by_placeholder("새 할 일 입력").fill("문서 작성하기")
    page.get_by_role("button", name="추가").click()

    # 추가 후 개수가 4개로 늘었는지 검증
    # auto-waiting: DOM 업데이트될 때까지 자동 대기
    expect(page.get_by_test_id("todo-item")).to_have_count(4)


def test_add_item_and_verify_text(page: Page, base_url: str):
    page.goto(base_url)

    page.get_by_placeholder("새 할 일 입력").fill("문서 작성하기")
    page.get_by_role("button", name="추가").click()

    items = page.get_by_test_id("todo-item")

    # 전체 개수 검증
    expect(items).to_have_count(4)

    # .last 로 마지막 항목만 골라서 텍스트 포함 여부 검증
    # to_contain_text() 는 "부분 포함" → "문서 작성하기 완료" 에서도 통과
    expect(items.last).to_contain_text("문서 작성하기")
