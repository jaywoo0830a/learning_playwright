# 문제 5 — 플레이스홀더 검색 & 키보드 입력

## 학습 목표
- `get_by_placeholder()` 로 placeholder 텍스트로 input 찾기
- `fill()` 로 값 입력 후 `press("Enter")` 로 키 이벤트 발생
- 검색 결과 텍스트 검증

## HTML 구조
```html
<input type="search" placeholder="제품명을 검색하세요" />
<div id="results">
  <!-- Enter 입력 시 결과 동적 렌더링 -->
  <div class="result-item">노트북 Pro</div>
</div>
<p id="no-result">검색 결과가 없습니다.</p>
```

## 미션
1. "노트북" 검색 → "노트북 Pro" 결과가 보여야 한다
2. "키보드" 검색 → "기계식 키보드" 결과가 보여야 한다
3. "없는제품" 검색 → "검색 결과가 없습니다." 가 보여야 한다

## 힌트
```python
# placeholder 로 input 찾기
search = page.get_by_placeholder("제품명을 검색하세요")

# 입력 후 Enter 키 누르기
search.fill("노트북")
search.press("Enter")

# 결과 검증
expect(page.get_by_text("노트북 Pro")).to_be_visible()
```

## 참고
- [Locators — locate by placeholder](https://playwright.dev/python/docs/locators#locate-by-placeholder)
- [Actions — press key](https://playwright.dev/python/docs/input#keys-and-shortcuts)
