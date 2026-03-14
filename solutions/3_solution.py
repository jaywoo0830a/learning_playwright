"""
문제 3 정답 — 폼 입력 & 제출
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    get_by_label("라벨 텍스트")
        → <label> 과 연결된 input 을 찾는다.
        → for/id 연결, 감싸는 구조 모두 인식.

    fill("값")
        → 기존 값을 지우고 새 값을 입력.
        → input, textarea, contenteditable 에 사용 가능.

    get_by_text("텍스트")
        → div, p, span 같은 텍스트 요소 찾기에 적합.
        → 버튼/링크는 get_by_role() 을 우선 사용.

    not_to_be_visible()
        → 요소가 화면에 안 보이는지 검증.
        → 에러 케이스에서 성공 메시지가 "안 뜨는지" 확인할 때 필수.

◆ 흔한 실수
    ✗ get_by_label("이메일").fill() 후 바로 get_by_label("비밀번호")
        → fill() 은 포커스를 이동시키지 않는다. 다음 fill() 은 별도 요소.
    ✗ 성공 케이스만 테스트
        → 실무에서는 실패 케이스(not_to_be_visible) 도 반드시 검증해야 한다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_fill_email_input(page: Page, base_url: str):
    page.goto(base_url)

    # get_by_label() 로 label 에 연결된 input 을 찾아 값 입력
    page.get_by_label("이메일").fill("user@test.com")

    # to_have_value() 로 input 안에 실제로 들어간 값을 검증
    expect(page.get_by_label("이메일")).to_have_value("user@test.com")


def test_result_message_visible(page: Page, base_url: str):
    page.goto(base_url)

    # 올바른 자격증명 입력
    page.get_by_label("이메일").fill("user@test.com")
    page.get_by_label("비밀번호").fill("secret123")
    page.get_by_role("button", name="로그인").click()

    # get_by_text() 로 결과 메시지 텍스트를 찾아 보이는지 검증
    # auto-waiting: 클릭 후 메시지가 나타날 때까지 자동 대기
    expect(page.get_by_text("로그인 성공! 환영합니다.")).to_be_visible()


def test_login_success(page: Page, base_url: str):
    page.goto(base_url)

    # label 로 각 input 을 찾아 순서대로 채운다
    page.get_by_label("이메일").fill("user@test.com")
    page.get_by_label("비밀번호").fill("secret123")

    # 버튼 클릭
    page.get_by_role("button", name="로그인").click()

    # 성공 메시지 검증
    expect(page.get_by_text("로그인 성공! 환영합니다.")).to_be_visible()


def test_login_failure(page: Page, base_url: str):
    page.goto(base_url)

    page.get_by_label("이메일").fill("user@test.com")
    # 틀린 비밀번호 입력
    page.get_by_label("비밀번호").fill("wrongpassword")
    page.get_by_role("button", name="로그인").click()

    # 에러 메시지가 보여야 한다
    expect(
        page.get_by_text("이메일 또는 비밀번호가 틀렸습니다.")
    ).to_be_visible()

    # 성공 메시지는 절대 보이면 안 된다 ← 이 검증이 빠지면 불완전한 테스트!
    expect(page.get_by_text("로그인 성공")).not_to_be_visible()
