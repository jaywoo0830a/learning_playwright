# 🎭 Learning Playwright (Python)

Playwright 공식 문서 기반 실습 프로젝트입니다.  
각 문제마다 실제 HTML 앱이 있고, 테스트 코드를 완성하면 됩니다.

---

## 빠른 시작

```bash
# 1. 환경 초기화 (최초 1회)
bash run/init.sh

# 2. 특정 문제 테스트 실행
bash run/test.sh 1      # 1번 문제
bash run/test.sh 3      # 3번 문제
bash run/test.sh all    # 전체 문제
```

---

## 문제 목록 (Basic)

| # | 주제 | 핵심 개념 |
|---|------|-----------|
| 1 | 페이지 타이틀 검증 | `expect(page).to_have_title()`, `page.goto()` |
| 2 | 버튼 클릭 & URL 검증 | `get_by_role()`, `expect(page).to_have_url()` |
| 3 | 폼 입력 & 제출 | `get_by_label()`, `fill()`, `click()` |
| 4 | 텍스트 존재 검증 | `get_by_text()`, `to_be_visible()` |
| 5 | 플레이스홀더 입력 & 검색 | `get_by_placeholder()`, `press()` |
| 6 | 체크박스 & 상태 검증 | `get_by_role("checkbox")`, `check()`, `to_be_checked()` |
| 7 | 이미지 alt 텍스트 검증 | `get_by_alt_text()`, `to_be_visible()` |
| 8 | 목록 개수 & 내용 검증 | `to_have_count()`, `to_have_text()` |
| 9 | select 옵션 선택 | `select_option()`, `to_have_value()` |
| 10 | heading & 링크 탐색 | `get_by_role("heading")`, `get_by_role("link")` |

---

## 폴더 구조

```
learning_playwright/
├── README.md
├── run/
│   ├── init.sh          # 환경 설치 스크립트
│   └── test.sh          # 문제별 테스트 실행
├── conftest.py          # pytest 공통 설정 (server fixture)
└── {1~10}/
    ├── README.md        # 문제 설명 & 힌트
    ├── app/
    │   └── index.html   # 테스트 대상 HTML 앱
    └── test_solution.py # ← 여기에 테스트 코드를 작성하세요
```

---

## 참고 문서

- [Playwright Python 공식 문서](https://playwright.dev/python/docs/intro)
- [Locators 가이드](https://playwright.dev/python/docs/locators)
- [Assertions 가이드](https://playwright.dev/python/docs/test-assertions)
