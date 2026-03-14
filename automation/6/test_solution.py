"""
실전 문제 6 — SE2 스타일 에디터 (iframe + designMode)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 실제 사례
    네이버 스마트에디터 2.x, 그누보드 SE2,
    많은 국내 CMS 가 이 패턴을 사용한다.

◆ 왜 어려운가?
    에디터 본문이 <iframe> 안에 있고,
    그 iframe 의 document.designMode = 'on' 으로 동작한다.

    문제점 1: page.fill() 이 완전히 무시됨
        → designMode 는 표준 input 이벤트를 발생시키지 않는다.
        → iframe 안 document.body 에 직접 접근해야 한다.

    문제점 2: frame_locator() 체이닝 필수
        → page.get_by_role() 은 iframe 밖에서만 작동한다.
        → page.frame_locator("iframe") 으로 컨텍스트를 바꿔야 한다.

    문제점 3: 툴바는 iframe 밖, 본문은 iframe 안
        → 툴바 버튼: page.locator("#tb-bold").click()
        → 본문 입력: frame.locator("body") 또는 evaluate()

    문제점 4: 선택 영역 유지
        → 툴바 버튼을 클릭하면 iframe 포커스가 날아간다.
        → Ctrl+A 로 전체 선택 후 버튼을 누르는 것이 가장 안정적.

◆ 이 문제에서 배우는 것
    ① frame_locator()               → iframe 컨텍스트 진입
    ② iframe body 에 키 입력        → press_sequentially()
    ③ iframe 외부 툴바 클릭         → 포커스 이탈 주의
    ④ evaluate() 로 iframe 내부 값  → contentDocument.body.innerText

나선형 학습 순서
    개념1(frame_locator) → 개념2(iframe 내 입력) → 복합1(툴바 조작) → 복합2(전체 흐름)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  frame_locator() 로 iframe 진입           │
# └─────────────────────────────────────────────────────────┘
def test_frame_locator_access(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        frame_locator() 로 iframe 에 진입하고
        iframe 안의 body 가 접근 가능한지 확인한다.

    ◆ HTML 구조
        <!-- iframe 밖 (page 컨텍스트) -->
        <iframe id="se2-frame" title="본문 편집 영역"></iframe>

        <!-- iframe 안 (frame 컨텍스트) -->
        <body>  ← designMode='on' 상태

    ◆ 핵심 개념
        page.frame_locator("CSS셀렉터")
            → iframe 을 선택해서 그 안을 탐색하는 FrameLocator 반환.
            → 이후 .locator(), .get_by_role() 등을 체이닝.
        📖 공식문서: https://playwright.dev/python/docs/api/class-page#page-frame-locator

        frame_locator("iframe[title='본문 편집 영역']")
            → title 속성으로 iframe 특정 — id 보다 안정적.

    ◆ 예시
        frame = page.frame_locator("iframe#se2-frame")
        body  = frame.locator("body")
        expect(body).to_be_visible()
    """
    page.goto(base_url)
    # iframe 로딩 대기
    page.wait_for_load_state("networkidle")

    # STEP 1: title 속성으로 iframe 을 frame_locator 로 잡으세요
    # frame = page.frame_locator(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: iframe 안의 body 가 보이는지 검증하세요
    # expect(frame.locator("body")).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  iframe body 에 텍스트 입력하기           │
# └─────────────────────────────────────────────────────────┘
def test_type_into_iframe_body(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        designMode 로 동작하는 iframe body 에
        텍스트를 입력하고 글자 수 카운터가 올라가는지 확인한다.

    ◆ 핵심 개념
        designMode 에디터 입력 전략
        ┌──────────────────────────┬────────────────────────────────────────┐
        │ fill("텍스트")           │ ❌ 대부분 무시됨                        │
        │                          │   (input 이벤트 미발생)                │
        ├──────────────────────────┼────────────────────────────────────────┤
        │ click() + press_         │ ✅ 실제 키보드 이벤트 발생             │
        │ sequentially()           │   → designMode 에디터가 반응           │
        ├──────────────────────────┼────────────────────────────────────────┤
        │ evaluate()로 innerHTML   │ ✅ JS로 직접 DOM 조작                  │
        │ 직접 주입                │   → 가장 빠르지만 입력 이벤트 없음     │
        └──────────────────────────┴────────────────────────────────────────┘
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press-sequentially

    ◆ 예시
        frame = page.frame_locator("iframe#se2-frame")
        body  = frame.locator("body")
        body.click()
        body.press_sequentially("SE2 에디터 입력 테스트", delay=30)
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#se2-frame")
    body  = frame.locator("body")

    # STEP 1: body 를 클릭해서 포커스를 맞추세요
    # body.click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: press_sequentially() 로 텍스트를 입력하세요
    # body.press_sequentially("SE2 에디터 입력 테스트", delay=30)

    # STEP 3: 글자 수 카운터 "#char-info" 가 "0 글자" 가 아닌지 검증하세요
    # expect(page.locator("#char-info")).not_to_have_text("0 글자")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  툴바 Bold 버튼 클릭 후 서식 검증        │
# └─────────────────────────────────────────────────────────┘
def test_apply_bold_via_toolbar(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        iframe body 에 텍스트 입력 → Ctrl+A 전체 선택
        → 외부 툴바 Bold 버튼 클릭 → iframe 안에 <b> 태그 생성 확인.

    ◆ 핵심 포인트
        툴바(#tb-bold)는 page 컨텍스트, 본문은 frame 컨텍스트.
        Ctrl+A 로 iframe 안에서 전체 선택 후 외부 버튼을 클릭한다.
        → 버튼 클릭 시 JS가 iframe 에 execCommand('bold') 를 호출.

    ◆ 힌트
        # iframe 안 전체 선택
        body.press("Control+a")

        # 외부 툴바 버튼 클릭
        page.locator("#tb-bold").click()

        # iframe 안에 <b> 또는 <strong> 태그 생성 검증
        frame.locator("b, strong").first.wait_for()
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-wait-for
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#se2-frame")
    body  = frame.locator("body")

    # STEP 1: 텍스트 입력
    body.click()
    body.press_sequentially("굵게 처리할 텍스트", delay=20)

    # STEP 2: Ctrl+A 로 전체 선택
    # body.press("Control+a")
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 3: 외부 툴바 Bold 버튼 클릭
    # page.locator("#tb-bold").click()

    # STEP 4: iframe 안에 <b> 또는 <strong> 태그가 생겼는지 검증
    # frame.locator("b, strong").first.wait_for()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  입력 + 등록 + evaluate() 로 내용 검증   │
# └─────────────────────────────────────────────────────────┘
def test_full_write_and_submit(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        텍스트 입력 후 등록 버튼을 누르면
        저장된 텍스트가 화면에 나오는지, 그리고
        evaluate() 로 iframe 내부 innerText 도 직접 꺼내 검증한다.

    ◆ evaluate() 로 iframe 내부 DOM 접근하는 법
        # 방법 A: frame_locator 의 locator 에서 evaluate
        text = frame.locator("body").evaluate("el => el.innerText")

        # 방법 B: page.evaluate 로 JS 직접 실행
        text = page.evaluate(
            "document.getElementById('se2-frame').contentDocument.body.innerText"
        )
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-evaluate

    ◆ 힌트
        # 입력
        body.click()
        body.press_sequentially("등록 테스트 내용", delay=20)

        # 등록 버튼 (iframe 밖)
        page.locator("#btn-submit").click()

        # 결과 영역 검증
        expect(page.locator("#result-text")).to_contain_text("등록 테스트 내용")

        # evaluate() 로 iframe 내부 텍스트 직접 검증
        text = frame.locator("body").evaluate("el => el.innerText")
        assert "등록 테스트 내용" in text
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#se2-frame")
    body  = frame.locator("body")

    # STEP 1: 텍스트 입력
    # body.click()
    # body.press_sequentially("등록 테스트 내용", delay=20)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 등록 버튼 클릭
    # page.locator("#btn-submit").click()

    # STEP 3: 결과 텍스트 영역에 입력 내용이 포함되는지 검증
    # expect(page.locator("#result-text")).to_contain_text("등록 테스트 내용")

    # STEP 4: evaluate() 로 iframe body.innerText 를 꺼내 Python 에서 검증
    # text = frame.locator("body").evaluate("el => el.innerText")
    # assert "등록 테스트 내용" in text
