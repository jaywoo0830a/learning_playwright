"""
문제 5 정답 — 플레이스홀더 검색 & 키보드 입력
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    get_by_placeholder("텍스트")
        → input 의 placeholder 속성 값으로 요소를 찾는다.
        → label 이 없는 검색창에 사용하는 두 번째 선택지.
          (label 있으면 get_by_label() 을 우선 사용)

    press("Enter")
        → 키보드 Enter 키를 누른다.
        → fill() 로 입력 후 press() 로 전송하는 것이 검색 폼의 일반 패턴.

    to_have_count(0)
        → 요소가 하나도 없는지 검증.
        → "검색 결과 없음" 상태를 확인할 때 유용.

◆ fill() + press() 패턴
    search = page.get_by_placeholder("검색어 입력")
    search.fill("키워드")   # 입력
    search.press("Enter")  # 전송

◆ 흔한 실수
    ✗ fill() 만 하고 press("Enter") 안 함
        → 이 앱은 Enter 키 이벤트에만 반응하므로 결과가 안 나온다!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_search_input_exists(page: Page, base_url: str):
    page.goto(base_url)

    # placeholder 텍스트로 input 을 찾아 화면에 보이는지만 확인
    expect(
        page.get_by_placeholder("제품명을 검색하세요")
    ).to_be_visible()


def test_press_enter_shows_results(page: Page, base_url: str):
    page.goto(base_url)

    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("노트북")

    # Enter 키를 눌러야 검색 이벤트가 발생한다
    search.press("Enter")

    expect(page.get_by_text("노트북 Pro")).to_be_visible()


def test_search_found(page: Page, base_url: str):
    page.goto(base_url)

    # locator 를 변수에 저장하면 재사용 가능
    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("키보드")
    search.press("Enter")

    expect(page.get_by_text("기계식 키보드")).to_be_visible()


def test_search_no_result(page: Page, base_url: str):
    page.goto(base_url)

    search = page.get_by_placeholder("제품명을 검색하세요")
    search.fill("없는제품xyz")
    search.press("Enter")

    # 안내 메시지가 보여야 한다
    expect(page.get_by_text("검색 결과가 없습니다.")).to_be_visible()

    # 결과 아이템이 0개여야 한다
    # → to_have_count(0) 은 "요소가 없음" 을 검증하는 관용 패턴
    expect(page.locator(".result-item")).to_have_count(0)
