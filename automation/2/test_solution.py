"""
실전 문제 2 — CodeMirror / Monaco 스타일 코드 에디터
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 왜 어려운가?
    CodeMirror, Monaco Editor, Ace Editor 는 실제 텍스트를
    사용자에게 보이는 <div> 에 렌더링하고
    실제 입력은 숨겨진 <textarea> 나 별도 요소로 받는다.

    문제점 1: 보이는 요소(cm-content div)에는 fill() 이 안 된다
        → contenteditable="false" 이거나 pointer-events:none 처리됨
        → 숨겨진 <textarea> 를 찾아야 한다

    문제점 2: 에디터 클릭 → 숨겨진 textarea 활성화 순서가 있다
        → 에디터 wrapper 를 클릭해서 textarea 를 활성화시킨 뒤
           textarea 에 직접 fill() 해야 한다

    문제점 3: opacity:0 인 요소는 일반 click() 이 안 될 수 있다
        → locator.click(force=True) 또는 dispatch_event('click') 사용
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

◆ 이 문제에서 배우는 것
    ① 숨겨진 textarea 찾기              → aria-label 로 접근
    ② force=True / dispatch_event()    → 숨겨진 요소 강제 클릭
    ③ 줄 수 검증                        → evaluate() 로 값 꺼내기
    ④ 실행 결과 검증                    → to_contain_text()

나선형 학습 순서
    개념1(숨김 textarea 찾기) → 개념2(강제 활성화) → 복합1(코드 입력+실행) → 복합2(줄수+결과 검증)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  숨겨진 textarea 찾아서 입력하기          │
# └─────────────────────────────────────────────────────────┘
def test_find_hidden_textarea(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        눈에 보이지 않는 textarea(opacity:0)를 찾아서
        코드를 입력하고 줄 수 카운터가 변하는지 검사한다.

    ◆ HTML 구조
        <!-- 보이는 것: 클릭 대상 wrapper -->
        <div id="cm-editor">
            <!-- 숨겨진 실제 입력 요소 -->
            <textarea
              id="code-input"
              aria-label="코드 입력창"
              style="opacity:0; pointer-events:none"
            ></textarea>
            <!-- 시각적 표시용 (입력 불가) -->
            <div class="cm-content" contenteditable="false"></div>
        </div>
        <span id="line-count">0 줄</span>

    ◆ 핵심 개념
        opacity:0 / visibility:hidden 요소는 to_be_visible() 에서 실패하지만
        fill() 은 가능한 경우가 있다.
        → aria-label 로 찾으면 숨겨진 요소도 접근 가능하다.

        에디터 wrapper 를 먼저 클릭해야 textarea 가 활성화된다:
            page.locator("#cm-editor").click()   # wrapper 클릭 → textarea 활성화
            page.get_by_label("코드 입력창").fill(코드)
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill
    """
    page.goto(base_url)

    # STEP 1: 에디터 wrapper "#cm-editor" 를 클릭해서 textarea 를 활성화하세요
    # page.locator(???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: aria-label "코드 입력창" 으로 숨겨진 textarea 를 찾아 코드를 입력하세요
    code = "print('hello')\nprint('world')"
    # page.get_by_label(???).fill(???)

    # STEP 3: 줄 수 카운터 "#line-count" 가 "2 줄" 로 바뀌었는지 검증하세요
    # expect(page.locator(???)).to_have_text(???)


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  force=True 로 숨겨진 요소 강제 조작     │
# └─────────────────────────────────────────────────────────┘
def test_force_click_and_fill(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        pointer-events:none 인 요소에 force=True 로 강제 클릭해서
        코드를 입력하는 방법을 테스트한다.

    ◆ 핵심 개념
        Playwright 는 기본적으로 클릭 전에 요소가
        실제로 클릭 가능한지(actionability) 확인한다.
        숨겨진 요소는 이 검사에서 실패한다.

        force=True 옵션:
            → actionability 검사를 건너뛰고 강제로 이벤트 발생
            → 실제 사용자는 클릭 못 하지만 테스트에서만 사용
            → 남용하면 안 됨! 실제로 숨겨진 요소에만 사용
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

        dispatch_event() 대안:
            page.locator("#code-input").dispatch_event("click")
            → JS 이벤트를 직접 발생시킴 (force 와 유사)
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-dispatch-event

    ◆ 예시
        # 방법 A: wrapper 클릭으로 활성화 후 fill
        page.locator("#cm-editor").click()
        page.locator("#code-input").fill("코드")

        # 방법 B: force=True 로 직접 강제 클릭
        page.locator("#code-input").click(force=True)
        page.locator("#code-input").fill("코드")
    """
    page.goto(base_url)

    # STEP 1: force=True 옵션으로 숨겨진 "#code-input" textarea 를 강제 클릭하세요
    # page.locator(???).click(force=True)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 코드를 입력하세요
    code = "x = 10\ny = 20\nprint(x + y)"
    # page.locator("#code-input").fill(???)

    # STEP 3: 줄 수가 "3 줄" 인지 검증하세요
    # expect(page.locator("#line-count")).to_have_text(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  코드 입력 + 실행 + 출력 결과 검증       │
# └─────────────────────────────────────────────────────────┘
def test_run_code_and_check_output(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        에디터에 Python print() 코드를 입력하고
        실행 버튼을 누르면 출력 결과가 나오는지 검사한다.

    ◆ 힌트
        # wrapper 클릭 → textarea 활성화
        page.locator("#cm-editor").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

        # 코드 입력
        page.get_by_label("코드 입력창").fill("print('자동화 성공')")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill

        # 실행 버튼 클릭
        page.locator("#btn-run").click()

        # 출력 결과 검증
        expect(page.locator("#run-output")).to_be_visible()
        expect(page.locator("#run-output")).to_contain_text("자동화 성공")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-contain-text
    """
    page.goto(base_url)

    # STEP 1: wrapper 클릭으로 에디터 활성화
    # page.locator(???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: print('자동화 성공') 코드를 입력하세요
    # page.get_by_label(???).fill(???)

    # STEP 3: "실행" 버튼을 클릭하세요 (id="btn-run")
    # page.locator(???).click()

    # STEP 4: 출력 영역이 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()

    # STEP 5: 출력 영역에 "자동화 성공" 텍스트가 있는지 검증하세요
    # expect(page.locator(???)).to_contain_text(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  evaluate() 로 textarea 값 직접 검증     │
# └─────────────────────────────────────────────────────────┘
def test_verify_code_with_evaluate(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        입력한 코드가 실제 textarea.value 에 올바르게 들어갔는지
        evaluate() 로 DOM 을 직접 검사한다.

    ◆ 왜 evaluate() 가 필요한가?
        숨겨진 textarea 는 화면에 보이지 않아서
        to_contain_text() 로는 검증이 안 될 수 있다.
        → JS 로 textarea.value 를 직접 꺼내서 Python 에서 비교한다.

    ◆ 힌트
        # textarea 의 value 값 꺼내기
        value = page.locator("#code-input").evaluate("el => el.value")
        assert "print" in value
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-evaluate

        # textarea 의 줄 수 계산
        lines = page.locator("#code-input").evaluate(
            "el => el.value.split('\\n').length"
        )
        assert lines == 3
    """
    page.goto(base_url)

    page.locator("#cm-editor").click()
    code = "print('line1')\nprint('line2')\nprint('line3')"
    page.get_by_label("코드 입력창").fill(code)

    # STEP 1: evaluate() 로 textarea 의 value 값을 꺼내세요
    # value = page.locator("#code-input").evaluate(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 꺼낸 value 에 "print" 가 포함되는지 Python assert 로 검증하세요
    # assert "print" in value

    # STEP 3: evaluate() 로 줄 수를 계산해 3줄인지 검증하세요
    # lines = page.locator("#code-input").evaluate("el => el.value.split('\\n').length")
    # assert lines == 3
