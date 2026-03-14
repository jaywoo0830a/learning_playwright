"""
문제 9 — Select 옵션 선택 & 값 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① select_option()    → 드롭다운에서 옵션 선택
  ② to_have_value()    → 현재 선택된 값(value) 검증
  ③ 두 select 를 조합한 흐름

나선형 학습 순서
  개념1(value로 선택) → 개념2(텍스트로 선택) → 복합1(두 select 동시) → 복합2(결과 검증)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  select_option(value=) 으로 값으로 선택  │
# └─────────────────────────────────────────────────────────┘
def test_select_delivery_by_value(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "배송 방법" 드롭다운에서 value="express" 를 선택하고
        실제로 그 값이 선택됐는지 검사한다.

    ◆ HTML 구조
        <label for="delivery">배송 방법</label>
        <select id="delivery">
            <option value="">-- 선택하세요 --</option>
            <option value="standard">일반 배송 (3~5일)</option>
            <option value="express">빠른 배송 (1~2일)</option>
            <option value="same-day">당일 배송</option>
        </select>

    ◆ 개념 설명
        locator.select_option(value="값")
            → <select> 의 option 중 value 속성이 일치하는 것을 선택한다.
            → value= 말고 label= (화면에 보이는 텍스트) 로도 선택 가능하다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-select-option

        expect(locator).to_have_value("값")
            → <select> 의 현재 선택된 value 를 검증한다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-value

        선택 방법 3가지
            select_option(value="express")        # option 의 value 속성으로
            select_option(label="빠른 배송 (1~2일)") # 화면에 보이는 텍스트로
            select_option(index=2)                # 0부터 시작하는 순서로

    ◆ 예시
        page.get_by_label("배송 방법").select_option(value="express")
        expect(page.get_by_label("배송 방법")).to_have_value("express")
    """
    page.goto(base_url)

    # STEP 1: "배송 방법" label 로 select 를 찾아 value="express" 를 선택하세요
    # page.get_by_label(???).select_option(value=???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 선택된 value 가 "express" 인지 검증하세요
    # expect(page.get_by_label(???)).to_have_value(???)


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  select_option(label=) 으로 텍스트로 선택│
# └─────────────────────────────────────────────────────────┘
def test_select_delivery_by_label(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        value 가 아닌 화면에 보이는 텍스트(label) 로 옵션을 선택할 수 있다.

    ◆ 개념 설명
        select_option(label="화면에 보이는 텍스트")
            → option 태그 안의 텍스트로 선택한다.
            → 실제 사용자가 드롭다운을 보는 것과 동일한 방식!

        select_option(value=) vs select_option(label=)
            value=  → HTML 의 value 속성 (코드 레벨)
            label=  → 사용자에게 보이는 텍스트 (UI 레벨)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-select-option

    ◆ 예시
        # <option value="same-day">당일 배송</option>
        page.get_by_label("배송 방법").select_option(label="당일 배송")
        # → value 로는 "same-day" 가 선택됨
        expect(page.get_by_label("배송 방법")).to_have_value("same-day")
    """
    page.goto(base_url)

    # STEP 1: label= 방식으로 "일반 배송 (3~5일)" 텍스트의 option 을 선택하세요
    # page.get_by_label("배송 방법").select_option(label=???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 선택된 value 가 "standard" 인지 검증하세요
    # expect(page.get_by_label(???)).to_have_value(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  두 select 를 동시에 선택하고 검증       │
# └─────────────────────────────────────────────────────────┘
def test_select_both_options(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "배송 방법" 과 "수량" 두 개의 select 를 각각 선택하고
        두 값이 모두 정확한지 검사한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 힌트
        # 배송 방법 선택
        page.get_by_label("배송 방법").select_option(value="same-day")
        expect(page.get_by_label("배송 방법")).to_have_value("same-day")

        # 수량 선택
        page.get_by_label("수량").select_option(value="5")
        expect(page.get_by_label("수량")).to_have_value("5")
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-select-option
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-value
    """
    page.goto(base_url)

    # STEP 1: "배송 방법" 에서 value="same-day" 를 선택하고 검증하세요
    # page.get_by_label(???).select_option(value=???)
    # expect(page.get_by_label(???)).to_have_value(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "수량" 에서 value="5" 를 선택하고 검증하세요
    # page.get_by_label(???).select_option(value=???)
    # expect(page.get_by_label(???)).to_have_value(???)


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  선택 후 확인 버튼 → 결과 텍스트 검증   │
# └─────────────────────────────────────────────────────────┘
def test_delivery_summary(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        배송 방법과 수량을 선택하고 "확인" 을 누르면
        선택한 내용이 화면에 표시되는지 검사한다.

    ◆ 결과 예시
        배송 방법: 당일 배송, 수량: 3개
        → "선택: 당일 배송, 3개" 텍스트가 나타남

    ◆ 힌트
        # 선택 → 클릭 → 결과 검증 순서
        page.get_by_label("배송 방법").select_option(value="same-day")
        page.get_by_label("수량").select_option(value="3")
        page.get_by_role("button", name="확인").click()
        expect(page.get_by_text("당일 배송, 3개")).to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(base_url)

    # STEP 1: "배송 방법" 에서 "same-day" 를 선택하세요
    # page.get_by_label(???).select_option(value=???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "수량" 에서 "3" 을 선택하세요
    # page.get_by_label(???).select_option(value=???)

    # STEP 3: "확인" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()

    # STEP 4: "당일 배송, 3개" 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
