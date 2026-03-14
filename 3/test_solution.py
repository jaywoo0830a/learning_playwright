"""
문제 3 — 폼 입력 & 제출
========================
학습 목표:
  - get_by_label() 로 label 연결 input 찾기
  - fill() 로 값 입력
  - get_by_role("button") 클릭 후 결과 검증
"""
from playwright.sync_api import Page, expect


def test_login_success(page: Page, base_url: str):
    """올바른 자격증명으로 로그인하면 성공 메시지가 보여야 한다."""
    page.goto(base_url)

    # TODO: label "이메일" 로 input을 찾아 "user@test.com" 을 입력하세요
    # page.get_by_label(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # TODO: label "비밀번호" 로 input을 찾아 "secret123" 을 입력하세요
    # page.get_by_label(???).fill(???)

    # TODO: "로그인" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()

    # TODO: "로그인 성공! 환영합니다." 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


def test_login_failure(page: Page, base_url: str):
    """틀린 비밀번호로 로그인하면 에러 메시지가 보여야 한다."""
    page.goto(base_url)

    page.get_by_label("이메일").fill("user@test.com")

    # TODO: 비밀번호에 틀린 값 "wrongpassword" 를 입력하세요
    # page.get_by_label(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    page.get_by_role("button", name="로그인").click()

    # TODO: "이메일 또는 비밀번호가 틀렸습니다." 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
