#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# run/test.sh  —  문제별 테스트 실행
#
# 사용법:
#   bash run/test.sh 1        # 1번 문제만
#   bash run/test.sh 1 2 5    # 1, 2, 5번 문제
#   bash run/test.sh all      # 전체 (1~10)
#
# 구조:
#   .venv 가상환경의 Python / pytest 를 사용합니다.
#   각 문제 폴더의 app/index.html 을 임시 HTTP 서버로 띄운 뒤
#   test_solution.py 를 pytest로 실행합니다.
#   테스트가 끝나면 서버를 자동으로 종료합니다.
# ─────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
cd "$ROOT"

# ── 가상환경 존재 확인 ─────────────────────────────────────
if [[ ! -f "$VENV/bin/python" ]]; then
    echo ""
    echo "❌ 가상환경이 없습니다. 먼저 초기화를 실행하세요:"
    echo "   bash run/init.sh"
    echo ""
    exit 1
fi

PYTHON="$VENV/bin/python"
PYTEST="$VENV/bin/pytest"

# ── 인자 처리 ──────────────────────────────────────────────
if [[ $# -eq 0 ]]; then
    echo "사용법: bash run/test.sh <문제번호|all>"
    echo "예시:   bash run/test.sh 1"
    echo "        bash run/test.sh all"
    exit 1
fi

if [[ "$1" == "all" ]]; then
    PROBLEMS=(1 2 3 4 5 6 7 8 9 10)
else
    PROBLEMS=("$@")
fi

# ── 결과 집계 ──────────────────────────────────────────────
PASS=0
FAIL=0
SKIP=0

# ── 문제별 실행 함수 ───────────────────────────────────────
run_problem() {
    local NUM=$1
    local DIR="$ROOT/$NUM"
    local APP_DIR="$DIR/app"
    local TEST_FILE="$DIR/test_solution.py"
    local PORT=$((8100 + NUM))

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  📝 문제 $NUM"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # 폴더 존재 확인
    if [[ ! -d "$DIR" ]]; then
        echo "  ⚠️  $NUM 번 폴더가 없습니다. 건너뜁니다."
        ((SKIP++)) || true
        return
    fi

    # 테스트 파일 존재 확인
    if [[ ! -f "$TEST_FILE" ]]; then
        echo "  ⚠️  test_solution.py 가 없습니다."
        ((SKIP++)) || true
        return
    fi

    # HTTP 서버 시작 — 가상환경 python 사용
    "$PYTHON" -m http.server "$PORT" \
        --directory "$APP_DIR" \
        --bind 127.0.0.1 \
        > /tmp/pw_server_$NUM.log 2>&1 &
    SERVER_PID=$!

    # 서버 준비 대기 (최대 3초)
    for i in $(seq 1 15); do
        if curl -s "http://127.0.0.1:$PORT/" > /dev/null 2>&1; then
            break
        fi
        sleep 0.2
    done

    # pytest 실행 — 가상환경 pytest 사용
    echo "  🌐 서버: http://127.0.0.1:$PORT"
    echo "  🐍 가상환경: $VENV"
    echo ""
    if BASE_URL="http://127.0.0.1:$PORT" \
       "$PYTEST" "$TEST_FILE" \
           --tb=short \
           --no-header \
           -q \
           2>&1; then
        ((PASS++)) || true
        echo "  ✅ 문제 $NUM — PASSED"
    else
        ((FAIL++)) || true
        echo "  ❌ 문제 $NUM — FAILED"
    fi

    # 서버 종료
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
}

# ── 실행 ───────────────────────────────────────────────────
for P in "${PROBLEMS[@]}"; do
    run_problem "$P"
done

# ── 최종 요약 ──────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 결과 요약"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ PASSED : $PASS"
echo "  ❌ FAILED : $FAIL"
echo "  ⚠️  SKIPPED: $SKIP"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
