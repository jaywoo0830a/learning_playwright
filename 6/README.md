# 문제 6 — 체크박스 & 상태 검증

## 학습 목표
- `get_by_role("checkbox")` 로 체크박스 찾기
- `check()` / `uncheck()` 로 체크박스 조작
- `to_be_checked()` / `to_be_disabled()` / `to_be_enabled()` 상태 검증

## HTML 구조
```html
<input type="checkbox" id="chk-terms" />    이용약관 (필수)
<input type="checkbox" id="chk-privacy" />  개인정보 (필수)
<input type="checkbox" id="chk-marketing" /> 마케팅 (선택)

<!-- 필수 2개 모두 체크해야 활성화 -->
<button id="submit-btn" disabled>가입하기</button>
```

## 미션
1. 초기 상태에서 "가입하기" 버튼이 **비활성화** 되어 있는지 검증
2. 필수 체크박스 2개 체크 → 버튼이 **활성화** 되는지 검증
3. 마케팅 포함 전체 체크 후 가입 → 완료 메시지 검증

## 힌트
```python
# 체크박스 체크 / 해제
page.get_by_role("checkbox", name="이용약관").check()

# 체크 상태 검증
expect(checkbox).to_be_checked()

# 버튼 활성화/비활성화 검증
expect(page.get_by_role("button", name="가입하기")).to_be_disabled()
expect(page.get_by_role("button", name="가입하기")).to_be_enabled()
```

## 참고
- [Actions — checkboxes](https://playwright.dev/python/docs/input#checkboxes-and-radio-buttons)
- [Assertions — to_be_checked](https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-be-checked)
