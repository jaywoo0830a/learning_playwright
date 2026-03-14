# 문제 1 — 페이지 타이틀 검증

## 학습 목표
- `page.goto()` 로 페이지 이동
- `expect(page).to_have_title()` 로 타이틀 검증
- 정규식으로 부분 일치 검증

## HTML 구조
```html
<title>나의 첫 Playwright 앱</title>
<h1>환영합니다!</h1>
```

## 미션
`test_solution.py` 를 열고 `# TODO` 부분을 완성하세요.

1. 페이지로 이동
2. 타이틀이 `"나의 첫 Playwright 앱"` 과 정확히 일치하는지 검증
3. 타이틀에 `"Playwright"` 가 포함되는지 정규식으로 검증

## 힌트
```python
import re
from playwright.sync_api import Page, expect

# 전체 일치
expect(page).to_have_title("정확한 타이틀")

# 정규식으로 부분 일치
expect(page).to_have_title(re.compile("부분 문자열"))
```

## 참고
- [Writing Tests](https://playwright.dev/python/docs/writing-tests)
- [PageAssertions.to_have_title](https://playwright.dev/python/docs/api/class-pageassertions#page-assertions-to-have-title)
