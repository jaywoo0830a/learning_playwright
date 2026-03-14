# 문제 9 — Select 옵션 선택 & 값 검증

## 학습 목표
- `get_by_label()` 로 label 연결 select 찾기
- `select_option()` 으로 드롭다운 선택
- `to_have_value()` 로 선택된 value 속성 검증

## HTML 구조
```html
<label for="delivery">배송 방법</label>
<select id="delivery">
  <option value="">-- 선택하세요 --</option>
  <option value="standard">일반 배송 (3~5일)</option>
  <option value="express">빠른 배송 (1~2일)</option>
  <option value="same-day">당일 배송</option>
</select>

<label for="quantity">수량</label>
<select id="quantity">
  <option value="1">1개</option>  ...
</select>
```

## 미션
1. "배송 방법" select 에서 "빠른 배송" 을 선택하고 value가 `"express"` 인지 검증
2. "수량" select 에서 `"5"` 를 값으로 선택하고 검증
3. 두 값 선택 후 "확인" 클릭 → 결과 텍스트 검증

## 힌트
```python
# 레이블로 select 찾아 텍스트로 선택
page.get_by_label("배송 방법").select_option("빠른 배송 (1~2일)")

# 또는 value로 선택
page.get_by_label("배송 방법").select_option(value="express")

# 선택된 value 검증
expect(page.get_by_label("배송 방법")).to_have_value("express")
```

## 참고
- [Actions — select option](https://playwright.dev/python/docs/input#select-options)
- [Assertions — to_have_value](https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-value)
