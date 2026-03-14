# 문제 7 — 이미지 alt 텍스트 & 갤러리 검증

## 학습 목표
- `get_by_alt_text()` 로 alt 속성으로 이미지 찾기
- `get_by_title()` 로 title 속성으로 요소 찾기
- `to_have_count()` 로 요소 개수 검증

## HTML 구조
```html
<img alt="산 풍경" />
<img alt="바다 풍경" />
<img alt="숲 풍경" />
<figcaption>산 풍경</figcaption>
```

## 미션
1. 갤러리에 이미지가 총 3개 있는지 검증 (`img` 태그 기준)
2. alt 텍스트 "산 풍경", "바다 풍경", "숲 풍경" 이 각각 존재하는지 검증
3. figcaption 텍스트가 3개인지 검증

## 힌트
```python
# alt 텍스트로 이미지 찾기
page.get_by_alt_text("산 풍경")

# img 태그 전체 개수 검증
expect(page.locator("img")).to_have_count(3)

# 텍스트가 보이는지 검증
expect(page.get_by_alt_text("바다 풍경")).to_have_attribute("alt", "바다 풍경")
```

## 참고
- [Locators — locate by alt text](https://playwright.dev/python/docs/locators#locate-by-alt-text)
- [Assertions — to_have_count](https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-count)
