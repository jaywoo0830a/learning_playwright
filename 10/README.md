# 문제 10 — Heading & Link 탐색 종합

## 학습 목표
- `get_by_role("heading")` 으로 제목 요소 찾기
- `get_by_role("link")` 으로 링크 찾기
- `get_by_role("navigation")` 으로 nav 탐색
- `to_have_count()`, `to_contain_text()`, `to_be_visible()` 종합 활용

## HTML 구조
```html
<h1>기술 블로그</h1>
<nav aria-label="주 내비게이션">
  <a href="#posts">포스트</a>
  <a href="#about">소개</a>
  <a href="#contact">연락처</a>
</nav>
<h2>Playwright로 E2E 테스트 시작하기</h2>
<h2>Python으로 자동화 테스트 작성하기</h2>
<h2>CI/CD 파이프라인 구축 가이드</h2>
```

## 미션
1. `<h1>` 제목이 "기술 블로그" 인지 검증
2. 내비게이션 안에 링크가 정확히 **3개** 인지 검증
3. `<h2>` 제목이 페이지에 **4개** 인지 검증 (포스트 3개 + 소개/연락처 2개 = 5개)
4. "더 읽기" 링크가 **3개** 인지 검증

## 힌트
```python
# h1 검증
expect(page.get_by_role("heading", level=1)).to_have_text("기술 블로그")

# nav 안의 링크만 필터링
nav = page.get_by_role("navigation", name="주 내비게이션")
expect(nav.get_by_role("link")).to_have_count(3)

# h2 개수 검증
expect(page.get_by_role("heading", level=2)).to_have_count(5)
```

## 참고
- [Locators — locate by role](https://playwright.dev/python/docs/locators#locate-by-role)
- [Assertions — to_have_text](https://playwright.dev/python/docs/api/class-locatorassertions#locator-assertions-to-have-text)
