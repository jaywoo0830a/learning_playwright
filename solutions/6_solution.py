"""
문제 6 정답 — 체크박스 & 버튼 상태 검증
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
◆ 핵심 정리
    get_by_role("checkbox", name="라벨 텍스트")
        → checkbox 를 연결된 label 텍스트로 찾는다.

    check() / uncheck()
        → 체크박스를 체크 / 해제한다.
        → 이미 체크된 상태에서 check() 를 해도 안전하다 (멱등성).

    to_be_checked()
        → 체크된 상태인지 검증.

    to_be_disabled() / to_be_enabled()
        → 버튼이 비활성화 / 활성화 상태인지 검증.
        → disabled 속성 또는 aria-disabled="true" 를 인식.

◆ 테스트 설계 포인트
    ① 초기 상태 검증 (disabled)
    ② 조건 충족 후 상태 변화 검증 (enabled)
    ③ 액션 후 최종 결과 검증 (완료 메시지)
    → 세 단계를 모두 써야 의미 있는 테스트가 된다.

◆ 흔한 실수
    ✗ check() 만 하고 to_be_checked() 검증 생략
        → check() 가 실제로 동작했는지 확인 안 하면 의미가 없다.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


def test_checkbox_check_and_verify(page: Page, base_url: str):
    page.goto(base_url)

    chk = page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)")
    chk.check()

    # check() 후에는 반드시 to_be_checked() 로 실제 상태를 검증
    expect(chk).to_be_checked()


def test_submit_button_initially_disabled(page: Page, base_url: str):
    page.goto(base_url)

    # 초기 상태: 필수 체크박스가 없으므로 버튼은 disabled
    expect(
        page.get_by_role("button", name="가입하기")
    ).to_be_disabled()


def test_required_checkboxes_enable_button(page: Page, base_url: str):
    page.goto(base_url)

    # 필수 2개를 체크해야 버튼이 활성화됨
    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보 처리방침에 동의합니다 (필수)").check()

    # 두 개 모두 체크한 후에야 enabled 상태가 됨
    expect(
        page.get_by_role("button", name="가입하기")
    ).to_be_enabled()


def test_full_signup_with_marketing(page: Page, base_url: str):
    page.goto(base_url)

    page.get_by_role("checkbox", name="이용약관에 동의합니다 (필수)").check()
    page.get_by_role("checkbox", name="개인정보 처리방침에 동의합니다 (필수)").check()

    # 마케팅 체크박스를 변수에 저장해서 체크 + 상태 검증에 재사용
    marketing = page.get_by_role("checkbox", name="마케팅 수신에 동의합니다 (선택)")
    marketing.check()
    expect(marketing).to_be_checked()  # 체크됐는지 확인

    page.get_by_role("button", name="가입하기").click()

    # 최종 결과 메시지 검증
    expect(
        page.get_by_text("마케팅 수신에 동의하셨습니다")
    ).to_be_visible()
