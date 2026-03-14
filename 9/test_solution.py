"""
문제 9 — Select 옵션 선택 & 값 검증
======================================
학습 목표:
  - get_by_label() 로 select 찾기
  - select_option(value=...) 로 드롭다운 선택
  - to_have_value() 로 선택된 value 검증
"""
from playwright.sync_api import Page, expect


def test_select_delivery_by_value(page: Page, base_url: str):
    """'배송 방법' select 에서 value='express' 를 선택하면 검증돼야 한다."""
    page.goto(base_url)

    # TODO: 레이블 "배송 방법" 로 select를 찾아 value="express" 를 선택하세요
    # page.get_by_label(???).select_option(value=???)
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: 선택된 value 가 "express" 인지 검증하세요
    # expect(page.get_by_label(???)).to_have_value(???)


def test_select_quantity_by_value(page: Page, base_url: str):
    """'수량' select 에서 value='5' 를 선택하면 검증돼야 한다."""
    page.goto(base_url)

    # TODO: 레이블 "수량" 로 select를 찾아 value="5" 를 선택하고 검증하세요
    # page.get_by_label(???).select_option(value=???)
    # expect(page.get_by_label(???)).to_have_value(???)
    raise NotImplementedError("TODO를 완성하세요")


def test_delivery_summary(page: Page, base_url: str):
    """배송 방법과 수량 선택 후 확인하면 선택 결과가 보여야 한다."""
    page.goto(base_url)

    page.get_by_label("배송 방법").select_option(value="same-day")
    page.get_by_label("수량").select_option(value="3")

    # TODO: "확인" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: "당일 배송, 3개" 텍스트가 포함된 요소가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
