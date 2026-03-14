"""
실전 문제 8 — SE ONE 복합 에디터 (제목+본문+블록+인라인툴바)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 이 문제가 다루는 실전 시나리오
    네이버 블로그, 티스토리, 브런치 같은
    실제 서비스의 에디터 E2E 자동화 테스트 패턴이다.

    ① 제목 input 은 iframe 밖 → 일반 fill()
    ② 본문은 iframe 안 contenteditable → press_sequentially()
    ③ 인라인 툴바는 텍스트 선택 시에만 나타남
    ④ + 블록 버튼으로 동적 컴포넌트 삽입
    ⑤ 자동저장 상태 텍스트 검증
    ⑥ 발행 후 결과 세 가지(제목/텍스트/HTML) 동시 검증

◆ 이 문제에서 배우는 것
    ① iframe 밖/안 혼합 입력        → fill() vs press_sequentially()
    ② select_text() + 인라인 툴바   → 선택 후 floating 버튼 클릭
    ③ + 블록 메뉴 클릭 → DOM 변화   → wait_for() 로 대기
    ④ 자동저장 상태 to_have_text()  → 타이밍 고려한 검증
    ⑤ 발행 결과 다중 필드 검증      → 여러 locator 연속 검증

나선형 학습 순서
    개념1(제목+본문 입력) → 개념2(블록 삽입) → 복합1(인라인툴바) → 복합2(발행 전체)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  제목(iframe 밖) + 본문(iframe 안) 입력   │
# └─────────────────────────────────────────────────────────┘
def test_title_and_body_input(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        제목(iframe 밖 input)은 fill(),
        본문(iframe 안 contenteditable)은 press_sequentially().
        두 입력 후 글자 수 카운터가 올라가는지 확인한다.

    ◆ HTML 구조
        <!-- iframe 밖 -->
        <input id="doc-title" data-testid="doc-title" placeholder="제목을 입력하세요" />

        <!-- iframe 안 -->
        <div id="body"
          contenteditable="true"
          data-testid="complex-editor-body"
          aria-label="본문 편집"
        ></div>

    ◆ 핵심 개념
        제목 input:
            page.get_by_test_id("doc-title").fill("제목 텍스트")
            → iframe 밖이므로 fill() 정상 동작.

        본문 contenteditable (iframe 안):
            frame = page.frame_locator("iframe#complex-frame")
            body  = frame.get_by_test_id("complex-editor-body")
            body.click()
            body.press_sequentially("본문 텍스트", delay=30)
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press-sequentially
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # STEP 1: 제목 input 에 "자동화 테스트 제목" 을 fill() 로 입력하세요
    # page.get_by_test_id("doc-title").fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: iframe 을 frame_locator 로 잡으세요
    # frame = page.frame_locator(???)

    # STEP 3: iframe 안 본문 에디터를 testid 로 찾아 텍스트 입력하세요
    # body = frame.get_by_test_id(???)
    # body.click()
    # body.press_sequentially("본문 내용입니다.", delay=30)

    # STEP 4: 글자 수 카운터 "#char-count" 가 "0자" 가 아닌지 검증하세요
    # expect(page.locator("#char-count")).not_to_have_text("0자")


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  블록 메뉴로 컴포넌트 삽입               │
# └─────────────────────────────────────────────────────────┘
def test_insert_block_component(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        + 버튼을 클릭해서 블록 메뉴를 열고
        인용(quote) 블록을 삽입한 후
        iframe 안에 blockquote 태그가 생겼는지 확인한다.

    ◆ HTML 구조 (iframe 밖)
        <div id="block-add-btn">+</div>
        <div id="block-menu">
          <button data-block="quote">❝ 인용</button>
          ...
        </div>

    ◆ 흐름
        ① 에디터 클릭 → + 버튼 보임
        ② + 버튼 클릭 → 블록 메뉴 팝업
        ③ 메뉴에서 "인용" 클릭
        ④ iframe 안에 blockquote.se-bq 생성 확인

    ◆ 힌트
        # + 버튼이 나타날 때까지 기다렸다가 클릭
        body.click()
        page.locator("#block-add-btn").wait_for()
        page.locator("#block-add-btn").click()

        # 메뉴에서 인용 클릭
        page.locator("[data-block='quote']").click()

        # iframe 안 blockquote 생성 검증
        frame.locator("blockquote").wait_for()
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-wait-for
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#complex-frame")
    body  = frame.get_by_test_id("complex-editor-body")

    # STEP 1: 에디터 클릭
    body.click()

    # STEP 2: + 버튼이 나타날 때까지 대기 후 클릭
    # page.locator("#block-add-btn").wait_for()
    # page.locator("#block-add-btn").click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 3: 블록 메뉴에서 "인용" 버튼 클릭
    # page.locator("[data-block='quote']").click()

    # STEP 4: iframe 안에 blockquote 가 생겼는지 검증
    # frame.locator("blockquote").wait_for()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  인라인 툴바로 서식 적용                  │
# └─────────────────────────────────────────────────────────┘
def test_inline_toolbar_bold(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        본문에 텍스트를 입력하고 Shift+Home 으로 한 줄 선택 후
        인라인 툴바의 Bold 버튼을 클릭해서 서식을 적용한다.

    ◆ 인라인 툴바 패턴
        SE ONE 은 텍스트를 선택했을 때만 인라인 툴바가 팝업된다.
        → mouseup 이벤트로 활성화 → position:fixed 로 표시

        Playwright 에서 텍스트 선택하는 법:
        방법 A: press_sequentially 후 Shift+Home (한 줄 선택)
        방법 B: select_text() — 요소 전체를 선택
        방법 C: mouse.move() + mouse.down() + mouse.move() + mouse.up()

    ◆ 힌트
        # 텍스트 입력 후 Shift+Home 으로 선택
        body.press_sequentially("서식 테스트 텍스트", delay=20)
        body.press("Shift+Home")

        # 인라인 툴바 등장 대기 후 Bold 클릭
        page.locator("#inline-toolbar").wait_for()
        page.locator("#itb-bold").click()

        # iframe 안에 <b> 또는 <strong> 생성 검증
        frame.locator("b, strong").wait_for()
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-press
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    frame = page.frame_locator("iframe#complex-frame")
    body  = frame.get_by_test_id("complex-editor-body")

    # STEP 1: 텍스트 입력
    body.click()
    body.press_sequentially("서식 테스트 텍스트", delay=20)

    # STEP 2: Shift+Home 으로 현재 줄 전체 선택
    # body.press("Shift+Home")
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 3: 인라인 툴바가 나타날 때까지 대기
    # page.locator("#inline-toolbar").wait_for()

    # STEP 4: 인라인 툴바의 Bold 버튼 클릭
    # page.locator("#itb-bold").click()

    # STEP 5: iframe 안에 b 또는 strong 태그 생성 검증
    # frame.locator("b, strong").wait_for()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  전체 발행 흐름 + 3개 필드 동시 검증     │
# └─────────────────────────────────────────────────────────┘
def test_full_publish_flow(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        제목 입력 → 본문 입력 → 발행 버튼 클릭 →
        발행 결과의 제목/본문텍스트/HTML 세 가지를 모두 검증한다.

    ◆ 발행 결과 구조
        <div id="final-result" class="show">
          <div id="final-title">자동화 테스트 제목</div>
          <div id="final-body">본문 내용입니다.</div>
          <div id="final-html"><p>본문 내용입니다.</p></div>
        </div>

    ◆ 힌트
        # 제목 입력 (iframe 밖)
        page.get_by_test_id("doc-title").fill("자동화 테스트 제목")

        # 본문 입력 (iframe 안)
        frame = page.frame_locator("iframe#complex-frame")
        body  = frame.get_by_test_id("complex-editor-body")
        body.click()
        body.press_sequentially("본문 내용입니다.", delay=20)

        # 발행 버튼
        page.locator("#btn-publish-complex").click()

        # 결과 세 가지 검증
        expect(page.locator("#final-title")).to_contain_text("자동화 테스트 제목")
        expect(page.locator("#final-body")).to_contain_text("본문 내용")
        expect(page.locator("#final-html")).not_to_have_text("(내용 없음)")
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-contain-text
    """
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # ── 제목 입력 (iframe 밖) ──
    # page.get_by_test_id("doc-title").fill("자동화 테스트 제목")
    raise NotImplementedError("TODO를 완성하세요")

    # ── 본문 입력 (iframe 안) ──
    # frame = page.frame_locator("iframe#complex-frame")
    # body  = frame.get_by_test_id("complex-editor-body")
    # body.click()
    # body.press_sequentially("본문 내용입니다.", delay=20)

    # ── 발행 버튼 클릭 ──
    # page.locator("#btn-publish-complex").click()

    # ── 결과 영역이 보이는지 검증 ──
    # expect(page.locator("#final-result")).to_be_visible()

    # ── 제목 검증 ──
    # expect(page.locator("#final-title")).to_contain_text("자동화 테스트 제목")

    # ── 본문 텍스트 검증 ──
    # expect(page.locator("#final-body")).to_contain_text("본문 내용")

    # ── 본문 HTML 이 비어있지 않은지 검증 ──
    # expect(page.locator("#final-html")).not_to_have_text("(내용 없음)")
