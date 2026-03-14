# 문제 8 — 목록 개수 & 내용 검증

## 학습 목표
- `get_by_test_id()` 로 data-testid 속성으로 요소 찾기
- `to_have_count()` 로 목록 개수 검증
- `to_have_text([...])` 로 목록 전체 내용을 한 번에 검증
- 동적으로 항목 추가 후 재검증

## HTML 구조
```html
<input placeholder="새 할 일 입력" />
<button id="add-btn">추가</button>

<li data-testid="todo-item">Playwright 설치하기 ...</li>
<li data-testid="todo-item">첫 테스트 작성하기 ...</li>
<li data-testid="todo-item">CI 연동하기 ...</li>
```

## 미션
1. 초기 항목이 정확히 **3개** 인지 검증
2. `to_have_text()` 로 각 항목의 텍스트가 맞는지 검증
3. 새 항목 추가 후 개수가 **4개** 로 늘었는지 검증

## 힌트
```python
items = page.get_by_test_id("todo-item")

# 개수 검증
expect(items).to_have_count(3)

# 텍스트 목록 검증 (순서 일치, 부분 포함)
expect(items).to_have_text([
    "Playwright 설치하기 완료",
    "첫 테스트 작성하기 완료",
    "CI 연동하기 완료",
])
```

## 참고
- [Locators — locate by test id](https://playwright.dev/python/docs/locators#locate-by-test-id)
- [Assertions — to_have_count](https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count)
- [Assertions — to_have_text](https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-text)
