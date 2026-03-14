# 문제 3 — 폼 입력 & 제출

## 학습 목표
- `get_by_label()` 로 label 연결 input 찾기
- `fill()` 로 값 입력
- 제출 후 결과 텍스트 검증

## HTML 구조
```html
<label for="email">이메일</label>
<input id="email" type="email" />

<label for="password">비밀번호</label>
<input id="password" type="password" />

<button type="submit">로그인</button>
<p id="result"><!-- 결과 메시지 --></p>
```

## 미션
1. **성공 케이스**: `user@test.com` / `secret123` 입력 → "로그인 성공! 환영합니다." 검증
2. **실패 케이스**: 틀린 비밀번호 입력 → "이메일 또는 비밀번호가 틀렸습니다." 검증

## 힌트
```python
# label 텍스트로 연결된 input 찾기
page.get_by_label("이메일").fill("user@test.com")

# 제출 버튼
page.get_by_role("button", name="로그인").click()

# 결과 텍스트 검증
expect(page.get_by_text("로그인 성공!")).to_be_visible()
```

## 참고
- [Locators — locate by label](https://playwright.dev/python/docs/locators#locate-by-label)
- [Actions — fill](https://playwright.dev/python/docs/input#text-input)
