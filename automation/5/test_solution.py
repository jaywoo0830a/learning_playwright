"""
실전 문제 5 — 멀티스텝 폼 + 탭 + 아코디언
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 왜 어려운가?
    멀티스텝 폼은 화면에 한 스텝만 보이고 나머지는 display:none 이다.
    탭과 아코디언도 같은 패턴 — "숨겨진 상태" 와 "보이는 상태" 를 오간다.

    문제점 1: 다음 버튼 클릭 후 현재 패널 변화 대기
        → 스텝 전환 직후 새 패널이 아직 display:none 일 수 있다
        → expect().to_be_visible() 의 auto-retry 로 처리

    문제점 2: 유효성 검사 실패 시 버튼이 반응 없음
        → 빈칸 → 다음 클릭 → 에러 메시지만 뜨고 스텝 전환 안 됨
        → 에러 메시지가 보이는지 확인하는 네거티브 테스트 필요

    문제점 3: 탭 안의 숨겨진 컨텐츠
        → 탭을 클릭해야 해당 패널이 보임
        → 클릭 전에 to_be_visible() 하면 실패

    문제점 4: 아코디언 열기 전에 내용 검증 불가
        → 아코디언 헤더를 클릭해야 body 가 펼쳐짐

◆ 이 문제에서 배우는 것
    ① 스텝 인디케이터 상태 검증       → to_have_class() 로 active/done 확인
    ② 유효성 검사 에러 메시지 검증    → 에러 시 to_be_visible(), 성공 시 not_to_be_visible()
    ③ 탭 전환 + 숨김 패널 검증        → 클릭 후 to_be_visible()
    ④ 아코디언 열기 + 내용 검증

나선형 학습 순서
    개념1(스텝 전환) → 개념2(유효성 검사) → 복합1(전체 스텝 완주) → 복합2(탭+아코디언)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import re
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  스텝 전환 & 인디케이터 상태 검증        │
# └─────────────────────────────────────────────────────────┘
def test_step_navigation(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        스텝 1 에서 정보를 입력하고 "다음" 을 클릭하면
        스텝 2 패널이 활성화되고
        스텝 인디케이터의 클래스가 바뀌는지 검사한다.

    ◆ HTML 구조
        <div class="step active" id="step-ind-1">기본 정보</div>  ← 현재
        <div class="step" id="step-ind-2">약관 동의</div>
        <div class="panel active" id="panel-1">...</div>          ← 보이는 패널
        <div class="panel" id="panel-2">...</div>                  ← 숨겨진 패널

    ◆ 핵심 개념
        스텝 전환 후 인디케이터 클래스 확인:
            expect(page.locator("#step-ind-1")).to_have_class(re.compile("done"))
            expect(page.locator("#step-ind-2")).to_have_class(re.compile("active"))
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-class

        새 패널이 보이는지 확인:
            expect(page.locator("#panel-2")).to_be_visible()
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(base_url)

    # STEP 1: 이름과 이메일을 입력하세요 (유효성 통과 필요)
    # page.get_by_label(???).fill(???)
    # page.get_by_label(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "다음 →" 버튼을 클릭하세요
    # page.get_by_role("button", name=???).click()

    # STEP 3: 스텝 2 패널이 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()

    # STEP 4: 스텝 1 인디케이터가 "done" 클래스를 가지는지 검증하세요
    # expect(page.locator("#step-ind-1")).to_have_class(re.compile(???))

    # STEP 5: 스텝 2 인디케이터가 "active" 클래스를 가지는지 검증하세요
    # expect(page.locator("#step-ind-2")).to_have_class(re.compile(???))


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  유효성 검사 실패 → 에러 메시지 검증     │
# └─────────────────────────────────────────────────────────┘
def test_validation_error_messages(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        이름/이메일 없이 "다음" 을 클릭하면
        에러 메시지가 나타나고 스텝이 전환되지 않는지 검사한다.

    ◆ HTML 구조
        <div class="error-msg" id="err-name">이름을 입력해주세요.</div>
        <div class="error-msg" id="err-email">올바른 이메일을 입력해주세요.</div>
        ※ 초기에는 display:none → 유효성 실패 시 class="error-msg show"

    ◆ 핵심 개념
        에러 메시지가 보이는지 / 안 보이는지:
            expect(page.locator("#err-name")).to_be_visible()     # 에러 시
            expect(page.locator("#err-name")).not_to_be_visible() # 정상 시

        스텝 패널이 변하지 않았는지:
            expect(page.locator("#panel-1")).to_be_visible()   # 여전히 스텝 1
            expect(page.locator("#panel-2")).not_to_be_visible()  # 스텝 2 아직 안 보임
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(base_url)

    # STEP 1: 아무것도 입력하지 않고 "다음 →" 버튼을 클릭하세요
    # page.get_by_role("button", name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 이름 에러 메시지 "#err-name" 이 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()

    # STEP 3: 이메일 에러 메시지 "#err-email" 이 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()

    # STEP 4: 스텝 1 패널이 여전히 보이는지 (스텝 전환 안 됨) 검증하세요
    # expect(page.locator(???)).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  전체 3스텝 완주 + 가입 완료 검증        │
# └─────────────────────────────────────────────────────────┘
def test_complete_full_signup(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        스텝 1 → 스텝 2 → 스텝 3 을 모두 통과하고
        "가입 완료" 를 눌러 성공 화면이 나오는지 검사한다.
        (개념 문제 ① + ② 를 합친 전체 흐름!)

    ◆ 전체 흐름
        스텝 1: 이름, 이메일 입력 → 다음
        스텝 2: 약관 2개 체크 → 다음
        스텝 3: 기본값(무료) 유지 → 가입 완료
        → 성공 화면 "#success" 보임 + 이름 포함 메시지 검증

    ◆ 힌트
        # 스텝 1
        page.get_by_label("이름").fill("홍길동")
        page.get_by_label("이메일").fill("hong@test.com")
        page.get_by_role("button", name="다음 →").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill

        # 스텝 2 (아코디언은 열지 않아도 체크 가능)
        page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
        page.get_by_role("checkbox", name="개인정보처리방침에 동의합니다 (필수)").check()
        page.get_by_role("button", name="다음 →").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-check

        # 스텝 3 → 가입 완료
        page.get_by_role("button", name="가입 완료").click()

        # 성공 화면 검증
        expect(page.locator("#success")).to_be_visible()
        expect(page.locator("#success-detail")).to_contain_text("홍길동")
    """
    page.goto(base_url)

    # ── 스텝 1: 기본 정보 ──
    # page.get_by_label(???).fill(???)   # 이름
    # page.get_by_label(???).fill(???)   # 이메일
    # page.get_by_role("button", name=???).click()  # 다음
    raise NotImplementedError("TODO를 완성하세요")

    # ── 스텝 2: 약관 동의 ──
    # page.get_by_role("checkbox", name=???).check()   # 이용약관
    # page.get_by_role("checkbox", name=???).check()   # 개인정보
    # page.get_by_role("button", name=???).click()     # 다음

    # ── 스텝 3: 요금제 선택 (기본값 무료) ──
    # page.get_by_role("button", name=???).click()     # 가입 완료

    # ── 성공 화면 검증 ──
    # expect(page.locator(???)).to_be_visible()
    # expect(page.locator("#success-detail")).to_contain_text(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  아코디언 열기 + 탭 전환 + 요금제 검증  │
# └─────────────────────────────────────────────────────────┘
def test_accordion_and_tab_interactions(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        스텝 2에서 아코디언을 열어 내용을 확인하고,
        스텝 3에서 "프로" 탭을 클릭해서
        프로 플랜 내용이 보이고 select 값이 바뀌는지 검사한다.

    ◆ 아코디언 열기
        아코디언 헤더를 클릭하면 body 가 펼쳐짐:
            page.locator("#acc-terms .accordion-header").click()
            expect(page.locator("#acc-terms .accordion-body")).to_be_visible()
        📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

    ◆ 탭 전환
        탭 버튼 클릭 → 해당 패널이 보임:
            page.locator("[data-tab='pro']").click()
            expect(page.locator("#tab-pro")).to_be_visible()
            expect(page.locator("#tab-free")).not_to_be_visible()
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible

    ◆ select 값 변화 검증
        탭 클릭 시 select 의 value 도 함께 바뀜:
            expect(page.locator("#plan")).to_have_value("pro")
        📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-value
    """
    page.goto(base_url)

    # ── 스텝 1 통과 ──
    page.get_by_label("이름").fill("테스트")
    page.get_by_label("이메일").fill("test@test.com")
    page.get_by_role("button", name="다음 →").click()
    expect(page.locator("#panel-2")).to_be_visible()

    # ── 스텝 2: 아코디언 열기 ──
    # STEP 1: "#acc-terms" 의 accordion-header 를 클릭해서 펼치세요
    # page.locator(???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "#acc-terms" 의 accordion-body 가 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()

    # STEP 3: accordion-body 에 "이용약관" 텍스트가 포함되는지 검증하세요
    # expect(page.locator(???)).to_contain_text(???)

    # 약관 체크 후 다음으로 이동
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보처리방침에 동의합니다 (필수)").check()
    page.get_by_role("button", name="다음 →").click()
    expect(page.locator("#panel-3")).to_be_visible()

    # ── 스텝 3: 탭 전환 ──
    # STEP 4: "프로" 탭 버튼을 클릭하세요 (data-tab="pro")
    # page.locator(???).click()

    # STEP 5: 프로 플랜 패널 "#tab-pro" 이 보이는지 검증하세요
    # expect(page.locator(???)).to_be_visible()

    # STEP 6: 무료 패널 "#tab-free" 가 더 이상 안 보이는지 검증하세요
    # expect(page.locator(???)).not_to_be_visible()

    # STEP 7: select "#plan" 의 value 가 "pro" 로 바뀌었는지 검증하세요
    # expect(page.locator(???)).to_have_value(???)
