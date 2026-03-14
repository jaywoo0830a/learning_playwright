"""
실전 문제 4 — 무한 스크롤 + 동적 렌더링 목록
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 왜 어려운가?
    무한 스크롤은 스크롤할 때마다 항목이 추가되므로
    "현재 몇 개인가" 가 동적으로 바뀐다.

    문제점 1: 스크롤 후 렌더링 대기
        → 스크롤 이벤트 → 네트워크/setTimeout → DOM 업데이트 순서
        → 스크롤 직후 바로 검증하면 항목이 아직 없다
        → expect() auto-retry 또는 wait_for_selector 필요

    문제점 2: 페이지 끝 감지
        → scrollHeight 가 계속 변하므로 "끝" 을 판단하기 어렵다
        → "모든 항목을 불러왔습니다" 텍스트가 나올 때까지 반복

    문제점 3: 필터 + 동적 목록 조합
        → 필터 버튼 클릭 → 기존 목록 제거 → 새 목록 로딩
        → 이전 항목이 사라질 때까지 기다려야 다음 검증 가능

◆ 이 문제에서 배우는 것
    ① evaluate() 로 스크롤 제어    → window.scrollTo(), scrollBy()
    ② wait_for_selector()          → 특정 요소가 나타날 때까지 대기
    ③ to_have_count() + retry      → 동적으로 증가하는 항목 수 검증
    ④ 필터 + 재로딩 패턴

나선형 학습 순서
    개념1(스크롤 제어) → 개념2(동적 대기) → 복합1(스크롤+카운트) → 복합2(필터+검증)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  evaluate() 로 스크롤 제어하기            │
# └─────────────────────────────────────────────────────────┘
def test_scroll_to_bottom(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        페이지 하단으로 스크롤하면
        추가 항목이 로드되어 피드 아이템이 늘어나는지 검사한다.

    ◆ HTML 구조
        <div id="feed">
          <div class="feed-item">...</div>  ← 스크롤할수록 추가됨
          ...
        </div>
        <div id="loader">불러오는 중...</div>

    ◆ 핵심 개념
        Playwright 에서 스크롤은 evaluate() 로 JS 를 직접 실행한다:
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            → 페이지 맨 아래로 이동

            page.evaluate("window.scrollBy(0, 500)")
            → 현재 위치에서 500px 아래로 이동
        📖 공식문서: https://playwright.dev/python/docs/api/class-page#page-evaluate

        스크롤 후 새 항목 로딩 대기:
            expect(page.locator(".feed-item")).to_have_count(10)
            → auto-retry 로 10개가 될 때까지 기다림
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count

    ◆ 예시
        # 초기 로드 (5개) 대기
        expect(page.locator(".feed-item")).to_have_count(5)

        # 스크롤 → 추가 5개 로드
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        expect(page.locator(".feed-item")).to_have_count(10)
    """
    page.goto(base_url)

    # STEP 1: 초기 피드 항목이 5개 로드될 때까지 대기하세요
    # expect(page.locator(???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: evaluate() 로 페이지 맨 아래로 스크롤하세요
    # page.evaluate(???)

    # STEP 3: 피드 항목이 10개로 늘어날 때까지 대기하세요
    # expect(page.locator(???)).to_have_count(???)


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  wait_for_selector 로 동적 요소 대기      │
# └─────────────────────────────────────────────────────────┘
def test_wait_for_end_message(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        모든 항목이 로드될 때까지 반복 스크롤하고
        "모든 항목을 불러왔습니다." 메시지가 나타나는지 검사한다.

    ◆ 핵심 개념
        page.wait_for_selector("셀렉터", state="visible")
            → 특정 요소가 나타날 때까지 기다린다.
            → expect().to_be_visible() 과 비슷하지만
               반복 루프 안에서 쓸 때 더 유연하다.
        📖 공식문서: https://playwright.dev/python/docs/api/class-page#page-wait-for-selector

        모든 항목 로드 패턴 (반복 스크롤):
            while True:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(600)  # 로딩 대기
                end = page.locator("#end-msg")
                if end.is_visible():
                    break
        📖 공식문서: https://playwright.dev/python/docs/api/class-page#page-wait-for-timeout

    ◆ 예시
        for _ in range(5):  # 최대 5번 스크롤
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(600)
        expect(page.locator("#end-msg")).to_be_visible()
    """
    page.goto(base_url)

    # TODO: 모든 항목이 로드될 때까지 반복 스크롤하고
    #        "#end-msg" 가 보일 때까지 기다리는 로직을 작성하세요
    for _ in range(5):
        # page.evaluate(???)
        # page.wait_for_timeout(???)
        pass
    raise NotImplementedError("TODO를 완성하세요")

    # 마지막으로 "#end-msg" 가 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  스크롤 + 피드 아이템 수 단계별 검증     │
# └─────────────────────────────────────────────────────────┘
def test_progressive_loading(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        스크롤할 때마다 아이템이 5개씩 늘어나는
        단계별 로딩이 정확한지 검사한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 예상 로딩 순서
        초기: 5개
        1번 스크롤: 10개
        2번 스크롤: 15개
        3번 스크롤: 20개 (전체) + 종료 메시지

    ◆ 힌트
        # 스크롤 후 일정 개수 대기 패턴
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        expect(page.locator(".feed-item")).to_have_count(10, timeout=5000)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count
    """
    page.goto(base_url)

    # STEP 1: 초기 5개 대기
    # expect(page.locator(???)).to_have_count(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 첫 번째 스크롤 후 10개 대기
    # page.evaluate(???)
    # expect(page.locator(???)).to_have_count(???)

    # STEP 3: 두 번째 스크롤 후 15개 대기
    # page.evaluate(???)
    # expect(page.locator(???)).to_have_count(???)

    # STEP 4: 세 번째 스크롤 후 20개 + 종료 메시지 검증
    # page.evaluate(???)
    # expect(page.locator(???)).to_have_count(???)
    # expect(page.locator("#end-msg")).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  필터 클릭 + 재로딩 + 타입별 아이템 검증 │
# └─────────────────────────────────────────────────────────┘
def test_filter_and_verify_types(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "알림" 필터 버튼을 클릭하면
        기존 항목이 사라지고 알림 타입 항목만 다시 로드되는지,
        그리고 로드된 항목이 모두 data-type="alert" 인지 검사한다.

    ◆ 도전 포인트
        필터 클릭 직후 기존 항목이 사라지고 새 항목이 로드되는 사이에
        검증하면 "0개" 상태를 잡을 수 있다.
        → 새 항목이 로드될 때까지 기다려야 한다.

    ◆ 힌트
        # 필터 버튼 클릭
        page.get_by_role("button", name="알림").click()

        # 새 항목 로드 대기
        expect(page.locator(".feed-item")).to_have_count(5, timeout=5000)

        # 로드된 항목이 모두 alert 타입인지 확인
        items = page.locator(".feed-item").all()
        for item in items:
            expect(item).to_have_attribute("data-type", "alert")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-attribute
    """
    page.goto(base_url)

    # STEP 1: 초기 로드 대기 (5개)
    expect(page.locator(".feed-item")).to_have_count(5, timeout=5000)

    # STEP 2: "알림" 필터 버튼을 클릭하세요
    # page.get_by_role("button", name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 3: 새 항목이 5개 로드될 때까지 대기하세요
    # expect(page.locator(???)).to_have_count(???, timeout=5000)

    # STEP 4: 로드된 모든 항목이 data-type="alert" 인지 검증하세요
    # items = page.locator(".feed-item").all()
    # for item in items:
    #     expect(item).to_have_attribute("data-type", ???)
