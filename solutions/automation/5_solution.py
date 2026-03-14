"""
실전 5 정답 — 멀티스텝 폼 + 탭 + 아코디언
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    to_have_class(re.compile("active")) 로 스텝 인디케이터 상태 검증.
    아코디언 헤더 클릭 → body to_be_visible() 패턴.
    탭 클릭 → 활성 패널 to_be_visible() + 비활성 not_to_be_visible().
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
import re
from playwright.sync_api import Page, expect


def test_step_navigation(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("이름").fill("홍길동")
    page.get_by_label("이메일").fill("hong@test.com")
    page.get_by_role("button", name="다음 →").click()
    expect(page.locator("#panel-2")).to_be_visible()
    expect(page.locator("#step-ind-1")).to_have_class(re.compile("done"))
    expect(page.locator("#step-ind-2")).to_have_class(re.compile("active"))


def test_validation_error_messages(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_role("button", name="다음 →").click()
    expect(page.locator("#err-name")).to_be_visible()
    expect(page.locator("#err-email")).to_be_visible()
    expect(page.locator("#panel-1")).to_be_visible()


def test_complete_full_signup(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("이름").fill("홍길동")
    page.get_by_label("이메일").fill("hong@test.com")
    page.get_by_role("button", name="다음 →").click()
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보처리방침에 동의합니다 (필수)").check()
    page.get_by_role("button", name="다음 →").click()
    page.get_by_role("button", name="가입 완료").click()
    expect(page.locator("#success")).to_be_visible()
    expect(page.locator("#success-detail")).to_contain_text("홍길동")


def test_accordion_and_tab_interactions(page: Page, base_url: str):
    page.goto(base_url)
    page.get_by_label("이름").fill("테스트")
    page.get_by_label("이메일").fill("test@test.com")
    page.get_by_role("button", name="다음 →").click()
    expect(page.locator("#panel-2")).to_be_visible()
    # 아코디언 열기
    page.locator("#acc-terms .accordion-header").click()
    expect(page.locator("#acc-terms .accordion-body")).to_be_visible()
    expect(page.locator("#acc-terms .accordion-body")).to_contain_text("이용약관")
    # 체크 후 다음
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보처리방침에 동의합니다 (필수)").check()
    page.get_by_role("button", name="다음 →").click()
    expect(page.locator("#panel-3")).to_be_visible()
    # 탭 전환
    page.locator("[data-tab='pro']").click()
    expect(page.locator("#tab-pro")).to_be_visible()
    expect(page.locator("#tab-free")).not_to_be_visible()
    expect(page.locator("#plan")).to_have_value("pro")
