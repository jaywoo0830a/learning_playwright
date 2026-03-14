# 문제 2 — 버튼 클릭 & URL 검증

## 학습 목표
- `get_by_role("button")` 으로 버튼/링크 찾기
- `click()` 으로 클릭 액션
- `expect(page).to_have_url()` 로 URL 검증

## HTML 구조
```html
<!-- index.html -->
<a href="about.html" role="button" id="go-btn">소개 페이지로 이동</a>

<!-- about.html -->
<h1>소개 페이지</h1>
```

## 미션
1. 메인 페이지에서 "소개 페이지로 이동" 버튼을 클릭
2. URL이 `about.html` 로 끝나는지 검증
3. `<h1>` 에 "소개 페이지" 가 보이는지 검증

## 힌트
```python
# role="button" 속성을 가진 a 태그도 button role로 찾을 수 있습니다
page.get_by_role("button", name="버튼 텍스트").click()

# URL 검증: 정규식도 가능
expect(page).to_have_url(re.compile(r"about\.html$"))
```

## 참고
- [Locators — locate by role](https://playwright.dev/python/docs/locators#locate-by-role)
- [PageAssertions.to_have_url](https://playwright.dev/python/docs/api/class-pageassertions#page-assertions-to-have-url)
