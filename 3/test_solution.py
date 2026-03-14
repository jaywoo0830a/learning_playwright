"""
문제 3 — 폼 입력 & 제출
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
이 문제에서 배우는 것
  ① get_by_label()   → <label> 텍스트로 연결된 input 을 찾는다
  ② fill()           → input 에 값을 입력한다
  ③ get_by_text()    → 화면에 보이는 텍스트로 요소를 찾는다

나선형 학습 순서
  개념1(label로 찾기) → 개념2(텍스트 검증) → 복합1(성공 로그인) → 복합2(실패 로그인)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
from playwright.sync_api import Page, expect


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ①  get_by_label() + fill() 로 폼 입력      │
# └─────────────────────────────────────────────────────────┘
def test_fill_email_input(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        "이메일" 라벨에 연결된 input 을 찾아서
        값을 입력했을 때 그 값이 제대로 들어갔는지 검사한다.

    ◆ HTML 구조
        <label for="email">이메일</label>
        <input id="email" type="email" />

    ◆ 개념 설명
        page.get_by_label("라벨 텍스트")
            → <label> 의 텍스트와 연결된 input 을 찾는다.
            → for="id" 연결 방식과 감싸는 방식 모두 인식한다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-label

        locator.fill("입력할 값")
            → input 에 있던 기존 값을 지우고 새 값을 입력한다.
            → 마치 키보드로 직접 타이핑하는 것과 같다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-fill

        expect(locator).to_have_value("기대값")
            → input 에 현재 입력된 값이 맞는지 검증한다.
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-value

    ◆ 예시
        # <label for="name">이름</label><input id="name" />
        page.get_by_label("이름").fill("홍길동")
        expect(page.get_by_label("이름")).to_have_value("홍길동")
    """
    page.goto(base_url)

    # STEP 1: "이메일" 라벨로 input 을 찾아 "user@test.com" 을 입력하세요
    # page.get_by_label(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: 입력된 값이 "user@test.com" 인지 검증하세요
    # expect(page.get_by_label(???)).to_have_value(???)


# ┌─────────────────────────────────────────────────────────┐
# │  개념 문제 ②  get_by_text() + to_be_visible()          │
# └─────────────────────────────────────────────────────────┘
def test_result_message_visible(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        로그인 성공 후 화면에 나타나는 텍스트를
        get_by_text() 로 찾아 보이는지 검증한다.

    ◆ HTML 구조 (로그인 성공 후 나타남)
        <p id="result" class="success">로그인 성공! 환영합니다.</p>

    ◆ 개념 설명
        page.get_by_text("텍스트")
            → 화면에 보이는 텍스트 내용으로 요소를 찾는다.
            → 부분 일치도 가능하다. ("로그인 성공" 만 써도 찾는다)
            → 버튼, 링크 같은 인터랙티브 요소는 get_by_role() 을 우선 사용하고
               div, p, span 같은 텍스트 요소에는 get_by_text() 를 쓴다.
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-text

        expect(locator).to_be_visible()
            → 요소가 화면에 실제로 보이는지 검증한다.
            → display:none, visibility:hidden, opacity:0 이면 실패!
            → Playwright 가 요소가 나타날 때까지 자동으로 기다린다. (auto-waiting)
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible

    ◆ 예시
        # 로그인 성공 후 나타나는 메시지 확인
        expect(page.get_by_text("로그인 성공")).to_be_visible()   # 부분 일치 ✅
        expect(page.get_by_text("환영합니다", exact=True)).to_be_visible()  # 정확히 이 텍스트만
    """
    page.goto(base_url)

    # 올바른 정보로 로그인 (이 부분은 이미 완성됨)
    page.get_by_label("이메일").fill("user@test.com")
    page.get_by_label("비밀번호").fill("secret123")
    page.get_by_role("button", name="로그인").click()

    # TODO: "로그인 성공! 환영합니다." 텍스트가 화면에 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()
    raise NotImplementedError("TODO를 완성하세요")


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ①  폼 채우기 + 제출 + 성공 메시지 검증     │
# └─────────────────────────────────────────────────────────┘
def test_login_success(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        올바른 이메일/비밀번호를 입력하고 버튼을 클릭했을 때
        성공 메시지가 화면에 나타나는지 검사한다.
        (개념 문제 ① + ② 를 합친 문제!)

    ◆ 정답 자격증명
        이메일:    user@test.com
        비밀번호:  secret123

    ◆ 힌트
        # label 로 input 찾아 값 입력
        page.get_by_label("이메일").fill("user@test.com")
            📖 공식문서: https://playwright.dev/python/docs/locators#locate-by-label

        # 버튼 클릭
        page.get_by_role("button", name="로그인").click()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locator#locator-click

        # 결과 텍스트 검증
        expect(page.get_by_text("로그인 성공! 환영합니다.")).to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-visible
    """
    page.goto(base_url)

    # STEP 1: "이메일" 라벨로 input 을 찾아 "user@test.com" 을 입력하세요
    # page.get_by_label(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "비밀번호" 라벨로 input 을 찾아 "secret123" 을 입력하세요
    # page.get_by_label(???).fill(???)

    # STEP 3: "로그인" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()

    # STEP 4: "로그인 성공! 환영합니다." 텍스트가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()


# ┌─────────────────────────────────────────────────────────┐
# │  복합 문제 ②  틀린 비밀번호 → 에러 메시지 검증        │
# └─────────────────────────────────────────────────────────┘
def test_login_failure(page: Page, base_url: str):
    """
    ◆ 이 테스트가 확인하는 것
        틀린 비밀번호로 로그인하면 에러 메시지가 나와야 한다.
        그리고 성공 메시지는 절대 보이면 안 된다!

    ◆ 도전 포인트
        성공 메시지가 "보이지 않아야" 하는 것도 검증해야 한다.

    ◆ 힌트
        # 에러 메시지가 보이는지 검증
        expect(page.get_by_text("이메일 또는 비밀번호가 틀렸습니다.")).to_be_visible()

        # 성공 메시지가 보이지 않는지 검증  ← not_ 을 붙인다!
        expect(page.get_by_text("로그인 성공")).not_to_be_visible()
            📖 공식문서: https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-not-to-be-visible
    """
    page.goto(base_url)

    # STEP 1: 올바른 이메일, 틀린 비밀번호 "wrongpassword" 를 입력하세요
    # page.get_by_label(???).fill(???)
    # page.get_by_label(???).fill(???)
    raise NotImplementedError("TODO를 완성하세요")

    # STEP 2: "로그인" 버튼을 클릭하세요
    # page.get_by_role(???, name=???).click()

    # STEP 3: 에러 메시지 "이메일 또는 비밀번호가 틀렸습니다." 가 보이는지 검증하세요
    # expect(page.get_by_text(???)).to_be_visible()

    # STEP 4: 성공 메시지 "로그인 성공" 이 보이지 않는지 검증하세요
    # expect(page.get_by_text(???)).not_to_be_visible()
