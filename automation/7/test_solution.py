"""
실전 문제 7 — SE ONE 스타일 에디터 (iframe + contenteditable)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ SE2 vs SE ONE 차이
    SE2:  iframe + document.designMode = 'on'
          → body 전체가 편집 영역
    SE ONE: iframe + <div contenteditable="true" id="se-editor">
          → 특정 div 만 편집 영역
          → data-testid, aria-label 속성 존재

◆ 왜 여전히 어려운가?
    문제점 1: fill() 여전히 무반응
        → contenteditable div 에 React 가 붙어있으면
           fill() 이 React state 를 업데이트하지 않는다.
        → click() + press_sequentially() 조합 필수.

    문제점 2: 인라인 툴바가 선택 이후에만 나타남
        → 텍스트를 마우스로 드래그 선택해야 툴바가 팝업됨.
        → Playwright 에서는 select_text() 또는
          shift+end 키로 선택하고 툴바를 클릭한다.

    문제점 3: data-testid 가 iframe 안에 있음
        → page.get_by_test_id() 로는 못 찾는다.
        → frame_locator().get_by_test_id() 로 찾아야 한다.

◆ 이 문제에서 배우는 것
    ① frame_locator + get_by_test_id   → iframe 안 testid 접근
    ② contenteditable fill vs press    → React 에디터 입력 전략
    ③ 선택 후 인라인 서식 적용         → select_text() 패턴
    ④ 툴바 블록 삽입 후 DOM 검증       → evaluate()

나선형 학습 순서
    개념1(testid로 에디터 찾기) → 개념2(입력 전략) → 복합1(서식 적용) → 복합2(발행 흐름)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  iframe 안 data-testid 로 에디터 찾기     │
# └─────────────────────────────────────────────────────────┘
def test_find_editor_in_iframe(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        SE ONE 의 contenteditable div 를
        frame_locator + get_by_test_id 조합으로 찾는다.

    ◆ HTML 구조 (iframe 안)
        <div
          id="se-editor"
          contenteditable="true"
          role="textbox"
          aria-label="SE ONE 본문"
          data-testid="se-one-editor"
        ></div>

    ◆ 핵심 개념
        frame_locator().get_by_test_id("값")
            → iframe 안의 data-testid 요소를 찾는다.
            → page.get_by_test_id() 는 iframe 밖만 탐색하므로 실패!

        frame_locator().get_by_role("textbox")
            → contenteditable div 의 role 은 textbox.
            → aria-label 이 있으면 name= 으로 더 정확히 특정.
        📖 공식문서: https://playwright.dev/python/docs/api/class-framelocator

    ◆ 예시
        frame  = page.frame_locator("iframe#se-one-frame")
        editor = frame.get_by_test_id("se-one-editor")
        expect(editor).to_be_visible()
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # STEP 1: iframe 을 frame_locator 로 잡으세요 (id="se-one-frame")
    # frame = page.frame_locator(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: iframe 안의 data-testid="se-one-editor" 요소를 찾으세요
    # editor = frame.get_by_test_id(???)

    # STEP 3: 에디터가 화면에 보이는지 검증하세요
    # expect(editor).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  contenteditable 에 텍스트 입력하기       │
# └─────────────────────────────────────────────────────────┘
def test_input_into_contenteditable(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        SE ONE 의 contenteditable div 에 텍스트를 입력하고
        글자 수 카운터("#word-count")가 업데이트 되는지 확인한다.

    ◆ SE ONE 입력 전략
        fill() → 많은 경우 React state 와 동기화 안 됨
        click() + press_sequentially() → 실제 키 이벤트 → React 반응
        click() + type()  (deprecated) → 내부적으로 press_sequentially 와 동일

    ◆ 힌트
        editor = frame.get_by_test_id("se-one-editor")
        editor.click()
        editor.press_sequentially("SE ONE 테스트 입력", delay=30)

        # 글자 수 카운터 검증 (iframe 밖)
        expect(page.locator("#word-count")).not_to_have_text("0자")
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press-sequentially
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame  = page.frame_locator("iframe#se-one-frame")
    editor = frame.get_by_test_id("se-one-editor")

    # STEP 1: 에디터를 클릭해서 포커스를 맞추세요
    # editor.click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: press_sequentially() 로 텍스트를 입력하세요
    # editor.press_sequentially("SE ONE 테스트 입력", delay=30)

    # STEP 3: 글자 수 카운터가 "0자" 가 아닌지 검증하세요
    # expect(page.locator("#word-count")).not_to_have_text("0자")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  H2 제목 블록 삽입 + DOM 검증            │
# └─────────────────────────────────────────────────────────┘
def test_insert_heading_block(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        H2 버튼(#tb-h2)을 클릭해서 제목 블록을 삽입하고
        iframe 안에 h2 태그가 생겼는지 검증한다.

    ◆ SE ONE 블록 삽입 패턴
        입력 → 커서 위치에서 toolbar 버튼 클릭 → DOM 변화 확인
        → 버튼은 iframe 밖 (page 컨텍스트)
        → 결과 DOM 은 iframe 안 (frame 컨텍스트)

    ◆ 힌트
        # 에디터에 포커스 후 H2 버튼 클릭
        editor.click()
        page.locator("#tb-h2").click()

        # iframe 안에 h2.se-heading 이 생겼는지 검증
        frame.locator("h2.se-heading").wait_for()
        또는
        expect(frame.locator("h2")).to_be_visible()
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-wait-for
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame  = page.frame_locator("iframe#se-one-frame")
    editor = frame.get_by_test_id("se-one-editor")

    # STEP 1: 에디터에 포커스
    editor.click()

    # STEP 2: H2 툴바 버튼 클릭 (iframe 밖)
    # page.locator("#tb-h2").click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 3: iframe 안에 h2 태그가 생겼는지 검증
    # frame.locator("h2").wait_for()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  전체 글쓰기 → 발행 → 결과 검증          │
# └─────────────────────────────────────────────────────────┘
def test_full_write_and_publish(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        SE ONE 에디터에 본문을 입력하고 발행 버튼을 눌렀을 때
        발행 결과 영역("#result-box")에 내용이 표시되는지 검증한다.

    ◆ 힌트
        # 에디터 입력
        editor.click()
        editor.press_sequentially("발행 테스트 본문입니다.", delay=20)

        # 발행 버튼 클릭 (iframe 밖)
        page.locator("#btn-publish").click()

        # 결과 영역 검증
        expect(page.locator("#result-box")).to_be_visible()
        expect(page.locator("#result-box")).to_contain_text("발행 테스트 본문")

        # evaluate() 로 에디터 내부 텍스트 추가 검증
        text = frame.get_by_test_id("se-one-editor").evaluate("el => el.innerText")
        assert "발행 테스트" in text
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-contain-text
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame  = page.frame_locator("iframe#se-one-frame")
    editor = frame.get_by_test_id("se-one-editor")

    # STEP 1: 에디터에 본문 입력
    # editor.click()
    # editor.press_sequentially("발행 테스트 본문입니다.", delay=20)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 발행 버튼 클릭
    # page.locator("#btn-publish").click()

    # STEP 3: 결과 박스가 보이는지 검증
    # expect(page.locator("#result-box")).to_be_visible()

    # STEP 4: 결과 박스에 입력한 텍스트가 포함되는지 검증
    # expect(page.locator("#result-box")).to_contain_text("발행 테스트 본문")

    # STEP 5 (도전): evaluate() 로 에디터 내부 텍스트도 직접 검증하세요
    # text = editor.evaluate("el => el.innerText")
    # assert "발행 테스트" in text
