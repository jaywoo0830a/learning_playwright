"""
문제 9 정답 — Select 옵션 선택 & 값 검증
"""
from playwright.sync_api import Page, expect


def test_select_delivery_by_value(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("배송 방법").select_option(value="express")
    expect(page.get_by_label("배송 방법")).to_have_value("express")


def test_select_quantity_by_value(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("수량").select_option(value="5")
    expect(page.get_by_label("수량")).to_have_value("5")


def test_delivery_summary(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("배송 방법").select_option(value="same-day")
    page.get_by_label("수량").select_option(value="3")
    page.get_by_role("button", name="확인").click()
    expect(page.get_by_text("당일 배송, 3개")).to_be_visible()
