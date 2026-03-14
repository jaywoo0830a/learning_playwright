"""
문제 6 — 체크박스 & 버튼 상태 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① check() / to_be_checked()  → 체크박스 체크 & 상태 검증
  ② to_be_disabled()           → 버튼이 비활성화 상태인지 검증
  ③ to_be_enabled()            → 버튼이 활성화 상태인지 검증

나선형 학습 순서
  개념1(체크박스 상태) → 개념2(버튼 비활성화) → 복합1(체크→활성화) → 복합2(전체 흐름)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  check() + to_be_checked() 체크박스      │
# └─────────────────────────────────────────────────────────┘
def test_checkbox_check_and_verify(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "이용약관" 체크박스를 체크했을 때
        실제로 체크된 상태가 되는지 검사한다.

    ◆ HTML 구조
        <label>
            <input type="checkbox" name="terms" />
            이용약관에 동의합니다 (필수)
        </label>

    ◆ 개념 설명
        page.get_by_role("checkbox", name="라벨 텍스트")
            → type="checkbox" 인 input 을 라벨 텍스트로 찾는다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-role

        locator.check()
            → 체크박스를 체크한다.
            → 이미 체크된 상태라면 아무것도 하지 않는다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-check

        expect(locator).to_be_checked()
            → 체크박스가 체크된 상태인지 검증한다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-checked

    ◆ 예시
        chk = page.get_by_role("checkbox", name="동의합니다")
        chk.check()                    # 체크
        expect(chk).to_be_checked()   # 체크됐는지 검증
    """
    page.goto(base_url)

    # STEP 1: "이용약관에 동의합니다 (필수)" 체크박스를 찾아 체크하세요
    # chk = page.get_by_role(???, name=???)
    # chk.check()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 체크박스가 체크된 상태인지 검증하세요
    # expect(chk).to_be_checked()


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  to_be_disabled() 비활성화 상태 검증     │
# └─────────────────────────────────────────────────────────┘
def test_submit_button_initially_disabled(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        페이지를 처음 열었을 때
        "가입하기" 버튼이 비활성화 상태인지 검사한다.

    ◆ HTML 구조
        <button id="submit-btn" disabled>가입하기</button>
        ※ 필수 체크박스 2개를 모두 체크해야 활성화됨

    ◆ 개념 설명
        expect(locator).to_be_disabled()
            → 버튼이나 input 이 disabled 상태인지 검증한다.
            → disabled 속성이 있거나 aria-disabled="true" 이면 통과.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-disabled

        expect(locator).to_be_enabled()
            → 반대로 활성화 상태인지 검증한다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-enabled

    ◆ 예시
        btn = page.get_by_role("button", name="제출")
        expect(btn).to_be_disabled()   # 비활성화 ✅
        expect(btn).to_be_enabled()    # 활성화 ✅
    """
    page.goto(base_url)

    # TODO: "가입하기" 버튼이 처음에 비활성화 상태인지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_disabled()
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  필수 체크박스 2개 체크 → 버튼 활성화   │
# └─────────────────────────────────────────────────────────┘
def test_required_checkboxes_enable_button(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        필수 체크박스 2개를 모두 체크하면
        "가입하기" 버튼이 활성화되는지 검사한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 힌트
        # 체크박스 2개 체크
        page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
        page.get_by_role("checkbox", name="개인정보 처리방침에 동의합니다 (필수)").check()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-check

        # 버튼 활성화 검증
        expect(page.get_by_role("button", name="가입하기")).to_be_enabled()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-enabled
    """
    page.goto(base_url)

    # STEP 1: "이용약관에 동의합니다 (필수)" 체크박스를 체크하세요
    # page.get_by_role(???, name=???).check()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "개인정보 처리방침에 동의합니다 (필수)" 체크박스를 체크하세요
    # page.get_by_role(???, name=???).check()

    # STEP 3: "가입하기" 버튼이 활성화 상태인지 검증하세요
    # expect(page.get_by_role(???, name=???)).to_be_enabled()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  전체 체크 + 가입 + 완료 메시지          │
# └─────────────────────────────────────────────────────────┘
def test_full_signup_with_marketing(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        세 체크박스를 모두 체크하고 가입하면
        마케팅 동의 완료 메시지가 나와야 한다.
        마케팅 체크박스가 체크 상태인 것도 함께 검증한다.

    ◆ 전체 흐름
        ① 이용약관 체크  →  ② 개인정보 체크  →  ③ 마케팅 체크
        →  ④ 마케팅 체크박스 to_be_checked() 검증
        →  ⑤ "가입하기" 클릭
        →  ⑥ 완료 메시지 to_be_visible() 검증

    ◆ 힌트
        # 마케팅 체크박스 체크 후 상태 검증
        marketing = page.get_by_role("checkbox", name="마케팅 수신에 동의합니다 (선택)")
        marketing.check()
        expect(marketing).to_be_checked()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-checked

        # 가입 완료 메시지 검증
        expect(page.get_by_text("마케팅 수신에 동의하셨습니다")).to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(base_url)

    # STEP 1~2: 필수 체크박스 2개를 체크하세요 (복합 문제 ① 참고)
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보 처리방침에 동의합니다 (필수)").check()

    # STEP 3: 마케팅 체크박스를 찾아 변수에 저장하고 체크하세요
    # marketing = page.get_by_role(???, name=???)
    # marketing.check()
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 4: 마케팅 체크박스가 체크된 상태인지 검증하세요
    # expect(marketing).to_be_checked()

    # STEP 5: "가입하기" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()

    # STEP 6: "마케팅 수신에 동의하셨습니다" 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
