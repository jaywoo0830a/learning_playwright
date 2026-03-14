"""
실전 문제 3 — 드래그 앤 드롭 (칸반 보드)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 왜 어려운가?
    HTML5 Drag & Drop API 는 Playwright 의 일반 drag_to() 로도 되지만
    React DnD, SortableJS, dnd-kit 같은 라이브러리는
    mousedown → mousemove → mouseup 시퀀스로만 반응한다.

    문제점 1: drag_to() 가 안 되는 경우
        → 일부 라이브러리는 포인터 이벤트(pointermove)를 써서
           Playwright 의 drag_to() 가 먹히지 않는다
        → mouse.move() + mouse.down() + mouse.up() 을 직접 조합해야 한다

    문제점 2: 드롭 후 DOM 변화 타이밍
        → 드롭 직후 즉시 검증하면 DOM 이 아직 업데이트 안 됐을 수 있다
        → expect() 의 auto-retry 를 활용하거나 wait_for 를 추가해야 한다

    문제점 3: 카드 위치 검증
        → "카드가 옮겨졌다" 는 것을 어떻게 검증하나?
        → 컬럼 안의 자식 요소 개수, 또는 특정 카드의 부모 확인

◆ 이 문제에서 배우는 것
    ① drag_to()                  → 기본 드래그 앤 드롭
    ② bounding_box() + mouse.*  → 좌표 기반 수동 드래그
    ③ filter(has=) 로 특정 카드  → 컬럼 안에서 카드 찾기
    ④ to_have_count()            → 컬럼 카드 수 변화 검증

나선형 학습 순서
    개념1(drag_to 기본) → 개념2(컬럼 내 카드 개수 검증) → 복합1(드래그+검증) → 복합2(연속 드래그)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  drag_to() 로 카드 이동하기               │
# └─────────────────────────────────────────────────────────┘
def test_drag_card_to_progress(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "할 일" 컬럼의 "로그인 기능 구현" 카드를
        "진행 중" 컬럼으로 드래그 앤 드롭하고
        이동 로그에 메시지가 나타나는지 검사한다.

    ◆ HTML 구조
        <div id="list-todo">          ← 드래그 출발 컬럼
          <div class="card" data-id="card-1">로그인 기능 구현</div>
        </div>
        <div id="list-progress">      ← 드롭 도착 컬럼
          ...
        </div>
        <div id="move-log">           ← 이동 로그

    ◆ 핵심 개념
        locator.drag_to(target)
            → locator 요소를 target 위치로 드래그 앤 드롭한다.
            → HTML5 Drag & Drop API 기반 앱에는 잘 동작한다.
            → React DnD, dnd-kit 같은 라이브러리는 안 될 수 있다.
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-drag-to

    ◆ 예시
        card = page.locator("[data-id='card-1']")
        target = page.locator("#list-progress")
        card.drag_to(target)
    """
    page.goto(base_url)

    # STEP 1: data-id="card-1" 카드를 locator 로 찾으세요
    # card = page.locator(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "#list-progress" 컬럼으로 drag_to() 하세요
    # card.drag_to(page.locator(???))

    # STEP 3: 이동 로그 "#move-log" 에 "로그인 기능 구현" 이 포함되는지 검증하세요
    # expect(page.locator(???)).to_contain_text(???)


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  컬럼 안의 카드 개수 검증                │
# └─────────────────────────────────────────────────────────┘
def test_column_card_counts(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        초기 상태에서 각 컬럼의 카드 개수가 맞는지 검사한다.
        (할 일: 3개, 진행 중: 1개, 완료: 1개)

    ◆ 핵심 개념
        컬럼 안의 카드만 찾으려면 범위를 좁혀야 한다:

        방법 A: 부모.locator(자식셀렉터)
            page.locator("#list-todo").locator(".card")
            → "#list-todo" 안의 ".card" 만 선택

        방법 B: filter(has=)
            page.locator(".card").filter(has=page.locator("#list-todo"))
            → 잘 안 쓰는 패턴. A 방법을 권장.
        📖 공식문서: https://playwright.dev/python/docs/locators#filtering-locators

    ◆ 예시
        todo_cards = page.locator("#list-todo .card")
        expect(todo_cards).to_have_count(3)
    """
    page.goto(base_url)

    # TODO: 각 컬럼의 카드 개수를 검증하세요
    # expect(page.locator(???)).to_have_count(3)  # 할 일
    # expect(page.locator(???)).to_have_count(1)  # 진행 중
    # expect(page.locator(???)).to_have_count(1)  # 완료
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  드래그 + 컬럼 카드 수 변화 검증         │
# └─────────────────────────────────────────────────────────┘
def test_drag_and_verify_counts(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        카드를 이동한 후 출발 컬럼과 도착 컬럼의
        카드 수가 모두 올바르게 변했는지 검사한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 예상 결과
        "로그인 기능 구현"(card-1) 을 할 일 → 진행 중 으로 이동하면
        할 일: 3개 → 2개
        진행 중: 1개 → 2개

    ◆ 힌트
        # 드래그
        page.locator("[data-id='card-1']").drag_to(page.locator("#list-progress"))
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-drag-to

        # 컬럼 카드 수 검증
        expect(page.locator("#list-todo .card")).to_have_count(2)
        expect(page.locator("#list-progress .card")).to_have_count(2)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count
    """
    page.goto(base_url)

    # STEP 1: card-1 을 "#list-progress" 로 드래그하세요
    # page.locator(???).drag_to(page.locator(???))
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 할 일 컬럼 카드 수가 2개로 줄었는지 검증하세요
    # expect(page.locator(???)).to_have_count(???)

    # STEP 3: 진행 중 컬럼 카드 수가 2개로 늘었는지 검증하세요
    # expect(page.locator(???)).to_have_count(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  수동 mouse 이벤트로 드래그 (고급 우회법) │
# └─────────────────────────────────────────────────────────┘
def test_drag_with_mouse_api(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        drag_to() 가 안 통하는 경우를 대비한
        bounding_box() + mouse 이벤트 직접 조합 방법을 실습한다.

    ◆ 왜 이 방법이 필요한가?
        React DnD, SortableJS, dnd-kit 같은 라이브러리는
        pointermove 이벤트를 사용하기 때문에
        drag_to() 가 동작하지 않는다.
        → bounding_box() 로 좌표를 구해서
           mouse.down() → mouse.move() → mouse.up() 을 수동으로 조합한다.

    ◆ bounding_box() 사용법
        box = locator.bounding_box()
        # box = {"x": 100, "y": 200, "width": 180, "height": 60}
        cx = box["x"] + box["width"] / 2   # 중심 X
        cy = box["y"] + box["height"] / 2  # 중심 Y
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-bounding-box

    ◆ mouse API 사용법
        page.mouse.move(x, y)   # 마우스 이동
        page.mouse.down()       # 마우스 버튼 누르기
        page.mouse.up()         # 마우스 버튼 놓기
        📖 공식문서: https://playwright.dev/python/docs/api/class-mouse

    ◆ 전체 드래그 패턴
        # 출발 요소 중심 좌표
        src_box = page.locator("[data-id='card-2']").bounding_box()
        sx = src_box["x"] + src_box["width"] / 2
        sy = src_box["y"] + src_box["height"] / 2

        # 도착 요소 중심 좌표
        dst_box = page.locator("#list-done").bounding_box()
        dx = dst_box["x"] + dst_box["width"] / 2
        dy = dst_box["y"] + dst_box["height"] / 2

        page.mouse.move(sx, sy)   # 카드로 이동
        page.mouse.down()         # 드래그 시작
        page.mouse.move(dx, dy, steps=10)  # 천천히 이동 (steps 로 smooth)
        page.mouse.up()           # 드롭
    """
    page.goto(base_url)

    # STEP 1: card-2 "대시보드 UI 개선" 의 bounding_box 를 구하세요
    # src_box = page.locator(???).bounding_box()
    # sx = src_box["x"] + src_box["width"] / 2
    # sy = src_box["y"] + src_box["height"] / 2
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "#list-done" 컬럼의 중심 좌표를 구하세요
    # dst_box = page.locator(???).bounding_box()
    # dx = dst_box["x"] + dst_box["width"] / 2
    # dy = dst_box["y"] + dst_box["height"] / 2

    # STEP 3: mouse API 로 드래그를 수행하세요
    # page.mouse.move(sx, sy)
    # page.mouse.down()
    # page.mouse.move(dx, dy, steps=10)
    # page.mouse.up()

    # STEP 4: 완료 컬럼의 카드가 2개가 됐는지 검증하세요
    # expect(page.locator(???)).to_have_count(???)
