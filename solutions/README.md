# 정답 파일 안내

이 폴더에는 각 문제의 참고 정답이 있습니다.

## 사용 방법

막혔을 때 참고용으로만 활용하세요.  
직접 풀어보는 것이 가장 효과적인 학습입니다.

```
solutions/
  1_solution.py   # 문제 1 정답
  2_solution.py   # 문제 2 정답
  ...
  10_solution.py  # 문제 10 정답
```

## 정답으로 테스트 실행하기

특정 문제의 정답 파일을 직접 실행하고 싶다면:

```bash
# 예: 3번 정답 실행 (서버는 test.sh가 띄워줘야 함)
BASE_URL=http://127.0.0.1:8103 pytest solutions/3_solution.py -v
```

또는 test.sh 를 통해 검증:

```bash
bash run/test.sh 3
# → 3번 문제 서버를 띄우고, 3/test_solution.py 를 실행
```
