"""
문제 4 — 동적 텍스트 & 가시성 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① to_be_visible()       → 요소가 지금 화면에 보이는가?
  ② not_to_be_visible()   → 요소가 지금 화면에 안 보이는가?
  ③ auto-waiting          → Playwright 가 알아서 기다려 준다!

나선형 학습 순서
  개념1(보임 검증) → 개념2(안 보임 검증) → 복합1(클릭→보임) → 복합2(하나만 보여야)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  to_be_visible() 로 요소가 보이는지 확인 │
# └─────────────────────────────────────────────────────────┘
def test_success_toast_visible(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "성공 알림" 버튼을 클릭하면
        성공 토스트 메시지가 화면에 나타나는지 검사한다.

    ◆ HTML 구조
        <button onclick="showToast('success')">성공 알림</button>
        <div id="toast-success" class="toast">저장이 완료되었습니다! ✓</div>
        ※ 토스트는 처음엔 display:none 상태 → 클릭하면 보임

    ◆ 개념 설명
        expect(locator).to_be_visible()
            → 요소가 화면에 실제로 보이는지 검증한다.
            → display:none 이거나 숨겨져 있으면 실패!
            → 핵심: Playwright 는 요소가 나타날 때까지 자동으로 기다린다.
               이것을 "auto-waiting" 이라고 한다.
               sleep() 같은 수동 대기를 쓸 필요가 없다!
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
            📖 auto-waiting: https://playwright.dev/python/docs/actionability

    ◆ 예시
        page.get_by_role("button", name="열기").click()
        # 클릭 후 팝업이 나타날 때까지 Playwright 가 알아서 기다림
        expect(page.get_by_text("팝업 내용")).to_be_visible()  # ✅ 기다렸다가 검증
    """
    page.goto(base_url)

    # STEP 1: "성공 알림" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "저장이 완료되었습니다" 텍스트가 화면에 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  not_to_be_visible() 로 숨김 상태 확인   │
# └─────────────────────────────────────────────────────────┘
def test_error_toast_initially_hidden(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        페이지를 처음 열었을 때 (아무 버튼도 클릭하지 않은 상태)
        에러 토스트가 화면에 보이지 않아야 한다.

    ◆ HTML 구조
        <div id="toast-error" class="toast" style="display:none">
            오류가 발생했습니다...
        </div>
        ※ 초기에는 숨겨진 상태!

    ◆ 개념 설명
        expect(locator).not_to_be_visible()
            → 요소가 화면에 보이지 않는 상태인지 검증한다.
            → to_be_visible() 의 반대!
            → DOM 에 존재하지만 숨겨진 경우도 "통과" 된다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-not-to-be-visible

        ※ 주의: not_to_be_visible() vs to_be_hidden()
            not_to_be_visible()  → 숨겨진 상태 OR DOM 에 없어도 통과
            to_be_hidden()       → 위와 동일 (같은 의미)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-hidden

    ◆ 예시
        # 아직 아무것도 클릭 안 한 초기 상태
        expect(page.get_by_text("오류 메시지")).not_to_be_visible()  # ✅ 숨겨져 있으니 통과
    """
    page.goto(base_url)

    # TODO: 페이지 초기 상태에서 "오류가 발생했습니다" 텍스트가 보이지 않는지 검증하세요
    # expect(page.get_by_text(???)).not_to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  버튼 클릭 후 에러 토스트 등장 검증      │
# └─────────────────────────────────────────────────────────┘
def test_error_toast_visible_after_click(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "에러 알림" 버튼을 클릭하면
        에러 토스트가 나타나야 한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 힌트
        # 버튼 클릭
        page.get_by_role("button", name="에러 알림").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

        # 에러 토스트 보임 검증
        expect(page.get_by_text("오류가 발생했습니다")).to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(base_url)

    # STEP 1: "에러 알림" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "오류가 발생했습니다" 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  한 토스트 클릭 시 다른 토스트는 숨겨짐  │
# └─────────────────────────────────────────────────────────┘
def test_only_one_toast_visible(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "성공 알림" 을 클릭하면
          ✅ 성공 토스트가 보여야 하고
          ❌ 에러 토스트는 보이면 안 된다!
        (두 가지 조건을 동시에 검증하는 문제!)

    ◆ 힌트
        # 성공 토스트 보임 검증
        expect(page.get_by_text("저장이 완료되었습니다")).to_be_visible()

        # 에러 토스트 안 보임 검증  ← not_ 을 붙인다!
        expect(page.get_by_text("오류가 발생했습니다")).not_to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-not-to-be-visible
    """
    page.goto(base_url)
    page.get_by_role("button", name="성공 알림").click()

    # STEP 1: 성공 토스트 "저장이 완료되었습니다" 가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 에러 토스트 "오류가 발생했습니다" 가 보이지 않는지 검증하세요
    # expect(page.get_by_text(???)).not_to_be_visible()
