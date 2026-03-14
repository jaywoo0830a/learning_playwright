"""
실전 문제 1 — contenteditable 리치 텍스트 에디터
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 왜 어려운가?
    일반 <input> 이나 <textarea> 가 아닌 <div contenteditable="true"> 이다.
    Notion, Confluence, 블로그 에디터, 이메일 작성 폼 등에서 자주 등장한다.

    문제점 1: fill() 이 안 되는 경우가 있다
        → contenteditable 은 표준 input 이벤트 외에 DOM mutation 으로 동작
        → press_sequentially() 나 evaluate() 로 우회해야 할 때가 있다

    문제점 2: 툴바 버튼 클릭 → 선택 영역 유지
        → 버튼 클릭 시 에디터 포커스가 날아가는 경우가 있음
        → 텍스트를 먼저 선택(select)한 뒤 버튼을 눌러야 서식 적용됨

    문제점 3: 내용 검증이 까다롭다
        → innerText vs innerHTML vs textContent 차이 이해 필요
        → evaluate() 로 JS를 직접 실행해 값을 꺼내야 할 때가 있다

◆ 이 문제에서 배우는 것
    ① get_by_role("textbox")     → contenteditable 접근
    ② fill() vs press_sequentially()  → 두 가지 입력 전략
    ③ evaluate()                 → JS 직접 실행으로 내부 상태 꺼내기
    ④ keyboard 단축키            → Ctrl+A, Ctrl+B 서식 적용

나선형 학습 순서
    개념1(에디터 찾고 입력) → 개념2(서식 버튼 클릭) → 복합1(입력+서식+저장) → 복합2(JS로 내용 검증)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  contenteditable 에 텍스트 입력하기       │
# └─────────────────────────────────────────────────────────┘
def test_type_into_editor(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        contenteditable 에디터에 텍스트를 입력하고
        글자 수 카운터가 올바르게 올라가는지 검사한다.

    ◆ HTML 구조
        <div
          id="editor"
          contenteditable="true"
          role="textbox"
          aria-label="본문 편집기"
        ></div>
        <span id="char-num">0</span> / 500자

    ◆ 핵심 개념
        contenteditable 요소의 role 은 "textbox" 이다.
        → get_by_role("textbox") 또는 get_by_label() 로 찾는다.

        fill() 은 contenteditable 에도 동작한다.
        → 단, 일부 에디터(ProseMirror, Slate.js 등)는 fill() 이 반응하지 않는다.
        → 그럴 때는 click() 으로 포커스 후 press_sequentially() 를 쓴다.
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press-sequentially

        전략 비교
        ┌────────────────────────┬──────────────────────────────────────────┐
        │ fill("텍스트")         │ 기존 내용 지우고 한 번에 입력. 빠름.     │
        │                        │ input 이벤트 1회 발생                    │
        ├────────────────────────┼──────────────────────────────────────────┤
        │ press_sequentially()   │ 한 글자씩 타이핑. 느리지만 JS 핸들러와  │
        │                        │ 잘 맞음. keydown/keyup 이벤트 발생       │
        └────────────────────────┴──────────────────────────────────────────┘

    ◆ 예시
        editor = page.get_by_role("textbox", name="본문 편집기")
        editor.click()           # 포커스
        editor.fill("Hello")     # 입력
        # 또는
        editor.press_sequentially("Hello", delay=30)  # 한 글자씩
    """
    page.goto(base_url)

    editor = page.get_by_role("textbox", name="본문 편집기")

    # STEP 1: 에디터를 클릭해 포커스를 맞추세요
    # editor.click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "Playwright 자동화 테스트" 텍스트를 입력하세요
    # editor.fill(???)

    # STEP 3: 글자 수 카운터 "#char-num" 이 0 보다 큰 숫자인지 검증하세요
    #          (정확한 숫자 대신 "0" 이 아닌지로 검증하면 됩니다)
    # expect(page.locator("#char-num")).not_to_have_text("0")


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  툴바 버튼으로 서식 적용하기              │
# └─────────────────────────────────────────────────────────┘
def test_apply_bold_formatting(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        텍스트를 입력한 뒤 Ctrl+A 로 전체 선택 후
        굵게(Bold) 버튼을 클릭하면 서식이 적용되는지 검사한다.

    ◆ HTML 구조
        <button id="btn-bold" data-cmd="bold" class="">B</button>
        <!-- 활성화 시 class="active" 로 바뀜 -->

    ◆ 핵심 개념
        키보드 단축키로 텍스트 전체 선택:
            editor.press("Control+a")   # Windows/Linux
            editor.press("Meta+a")      # macOS
        → 실무에서는 OS에 따라 달라지므로 주의!
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press

        서식 버튼 클릭 후 active 클래스 확인:
            expect(page.locator("#btn-bold")).to_have_class(re.compile("active"))
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-class

    ◆ 예시
        editor.fill("굵게 만들 텍스트")
        editor.press("Control+a")          # 전체 선택
        page.get_by_role("button", name="B").click()  # Bold 버튼
    """
    import re
    page.goto(base_url)

    editor = page.get_by_role("textbox", name="본문 편집기")
    editor.click()
    editor.fill("굵게 만들 텍스트")

    # STEP 1: Ctrl+A 로 텍스트 전체를 선택하세요
    # editor.press("Control+a")
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 툴바의 "B" 버튼을 클릭하세요
    # page.get_by_role("button", name=???).click()

    # STEP 3: "btn-bold" 버튼에 "active" 클래스가 붙었는지 검증하세요
    # expect(page.locator("#btn-bold")).to_have_class(re.compile(???))


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  입력 + 서식 + 저장 전체 흐름            │
# └─────────────────────────────────────────────────────────┘
def test_write_and_save(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        에디터에 내용을 입력하고 저장 버튼을 누르면
        저장된 텍스트 내용이 출력 영역에 나타나는지 검사한다.

    ◆ 전체 흐름
        ① 에디터 클릭 → ② 텍스트 입력 → ③ 저장 버튼 클릭
        → ④ "#output" 영역이 보이는지 검증
        → ⑤ "#output-text" 에 입력한 텍스트가 포함되는지 검증

    ◆ 힌트
        # 에디터 입력
        editor = page.get_by_role("textbox", name="본문 편집기")
        editor.click()
        editor.fill("자동화 테스트 내용입니다.")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill

        # 저장 버튼 클릭
        page.locator("#btn-save").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

        # 출력 영역 검증
        expect(page.locator("#output")).to_be_visible()
        expect(page.locator("#output-text")).to_contain_text("자동화 테스트")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-contain-text
    """
    page.goto(base_url)

    editor = page.get_by_role("textbox", name="본문 편집기")

    # STEP 1~2: 에디터에 "자동화 테스트 내용입니다." 를 입력하세요
    # editor.click()
    # editor.fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 3: 저장 버튼을 클릭하세요
    # page.locator(???).click()

    # STEP 4: 출력 영역 "#output" 이 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()

    # STEP 5: "#output-text" 에 "자동화 테스트" 텍스트가 포함되는지 검증하세요
    # expect(page.locator(???)).to_contain_text(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  evaluate() 로 에디터 내부 상태 꺼내기   │
# └─────────────────────────────────────────────────────────┘
def test_verify_content_with_evaluate(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        에디터에 입력한 후 evaluate() 로 브라우저 JS 를 직접 실행해
        innerHTML 과 innerText 를 각각 꺼내 Python 에서 검증한다.

    ◆ 왜 evaluate() 가 필요한가?
        to_contain_text() 는 화면에 렌더링된 텍스트를 검증한다.
        하지만 리치 에디터의 실제 HTML 구조(Bold 태그, 링크 태그 등)는
        to_contain_text() 로는 볼 수 없다.
        → evaluate() 로 직접 DOM 의 innerHTML 을 꺼내야 한다.
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-evaluate

    ◆ evaluate() 사용법
        # locator 기준으로 JS 실행
        result = page.locator("#editor").evaluate("el => el.innerHTML")
        # el 은 locator 가 가리키는 DOM 요소

        # page 기준으로 JS 실행
        result = page.evaluate("document.getElementById('editor').innerText")
        📖 공식문서: https://playwright.dev/python/docs/api/class-page#page-evaluate

    ◆ 예시
        editor.fill("테스트 내용")
        html = page.locator("#editor").evaluate("el => el.innerHTML")
        text = page.locator("#editor").evaluate("el => el.innerText")
        assert "테스트 내용" in text
    """
    page.goto(base_url)

    editor = page.get_by_role("textbox", name="본문 편집기")
    editor.click()
    editor.fill("평가 테스트 문장")

    # STEP 1: evaluate() 로 에디터의 innerText 를 꺼내세요
    # text = page.locator("#editor").evaluate(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 꺼낸 text 에 "평가 테스트" 가 포함되는지 Python assert 로 검증하세요
    # assert "평가 테스트" in text

    # STEP 3 (도전): evaluate() 로 innerHTML 도 꺼내
    #                 "p" 태그나 "div" 태그가 포함되어 있는지 확인해보세요
    # html = page.locator("#editor").evaluate("el => el.innerHTML")
    # assert len(html) > 0
