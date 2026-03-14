# 문제 4 — 동적 텍스트 & 가시성 검증

## 학습 목표
- `get_by_text()` 로 텍스트 내용으로 요소 찾기
- `to_be_visible()` / `not_to_be_visible()` 로 가시성 검증
- Playwright auto-waiting: 요소가 나타날 때까지 자동 대기

## HTML 구조
```html
<button onclick="showToast('success')">성공 알림</button>
<button onclick="showToast('error')">에러 알림</button>

<!-- 클릭 전에는 display:none, 클릭 후 display:block -->
<div id="toast-success" class="toast success">저장이 완료되었습니다! ✓</div>
<div id="toast-error"   class="toast error">오류가 발생했습니다...</div>
```

## 미션
1. "성공 알림" 버튼 클릭 → 성공 토스트 메시지가 **보여야** 한다
2. "에러 알림" 버튼 클릭 → 에러 토스트 메시지가 **보여야** 한다
3. 성공 알림 클릭 시 에러 토스트는 **보이지 않아야** 한다

## 힌트
```python
# 텍스트로 요소 찾기 (부분 일치)
page.get_by_text("저장이 완료")

# 보임 / 안 보임 검증
expect(locator).to_be_visible()
expect(locator).not_to_be_visible()
```

## 참고
- [Locators — locate by text](https://playwright.dev/python/docs/locators#locate-by-text)
- [Auto-waiting](https://playwright.dev/python/docs/actionability)
