"""
문제 9 정답 — Select 옵션 선택 & 값 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    select_option(value="값")
        → option 태그의 value 속성으로 선택.
        → HTML 코드 레벨의 값 (사용자에게 안 보이는 값).

    select_option(label="텍스트")
        → option 태그 안의 텍스트로 선택.
        → 사용자가 화면에서 보는 값.

    to_have_value("값")
        → select 의 현재 선택된 value 속성을 검증.

◆ 세 가지 선택 방법 비교
    select_option(value="express")          # value 속성으로 선택
    select_option(label="빠른 배송 (1~2일)") # 화면 텍스트로 선택
    select_option(index=2)                  # 0부터 시작하는 순서로 선택

◆ 언제 뭘 쓰나?
    value= → 코드를 보고 정확한 value 를 알 때. 가장 안정적.
    label= → 화면 텍스트 기준으로 테스트하고 싶을 때.
    index= → 거의 쓰지 않는다. DOM 변경에 취약.

◆ 흔한 실수
    ✗ select_option("빠른 배송") 처럼 따옴표만 쓰면
        → Playwright 가 value= 와 label= 둘 다 시도하지만
           정확한 텍스트와 달라서 실패할 수 있다.
    ✓ select_option(value="express") 또는
      select_option(label="빠른 배송 (1~2일)") 처럼 키워드 명시 권장.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_select_delivery_by_value(page: Page, base_url: str):
    page.goto(base_url)

    # get_by_label() 로 select 를 찾아 value 로 옵션 선택
    page.get_by_label("배송 방법").select_option(value="express")

    # 선택 후 실제 value 를 검증
    expect(page.get_by_label("배송 방법")).to_have_value("express")


def test_select_delivery_by_label(page: Page, base_url: str):
    page.goto(base_url)

    # label= 로 화면에 보이는 텍스트를 기준으로 선택
    page.get_by_label("배송 방법").select_option(label="일반 배송 (3~5일)")

    # 선택된 value 는 "standard"
    expect(page.get_by_label("배송 방법")).to_have_value("standard")


def test_select_both_options(page: Page, base_url: str):
    page.goto(base_url)

    # 배송 방법 선택 + 검증
    page.get_by_label("배송 방법").select_option(value="same-day")
    expect(page.get_by_label("배송 방법")).to_have_value("same-day")

    # 수량 선택 + 검증
    page.get_by_label("수량").select_option(value="5")
    expect(page.get_by_label("수량")).to_have_value("5")


def test_delivery_summary(page: Page, base_url: str):
    page.goto(base_url)

    page.get_by_label("배송 방법").select_option(value="same-day")
    page.get_by_label("수량").select_option(value="3")

    # 확인 버튼 클릭
    page.get_by_role("button", name="확인").click()

    # 결과 텍스트 부분 포함 검증
    # "선택: 당일 배송, 3개" 전체 텍스트 중 "당일 배송, 3개" 만 매칭해도 충분
    expect(page.get_by_text("당일 배송, 3개")).to_be_visible()
