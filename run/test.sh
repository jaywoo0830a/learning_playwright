#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# run/test.sh  —  문제별 테스트 실행
#
# 사용법:
#   bash run/test.sh 1        # 1번 문제만
#   bash run/test.sh 1 2 5    # 1, 2, 5번 문제
#   bash run/test.sh all      # 전체 (1~10)
# ─────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
cd "$ROOT"

# ══════════════════════════════════════════════════════════════
# ★ 서버 주소 설정 — 여기서만 바꾸면 됩니다
#
#   .env 파일이 있으면 거기서 읽어옵니다.
#   없으면 아래 기본값을 사용합니다.
#
HOST="127.0.0.1"   # 서버 호스트 (기본: 로컬호스트)
BASE_PORT=8100     # 기준 포트 — 실제 포트 = BASE_PORT + 문제번호
#                  #   문제 1 → 8101, 문제 2 → 8102, ...
# ══════════════════════════════════════════════════════════════

# .env 파일이 있으면 HOST / BASE_PORT 덮어쓰기
ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
    while IFS='=' read -r key value; do
        # 빈 줄·주석 무시
        [[ -z "$key" || "$key" == \#* ]] && continue
        key="${key// /}"      # 공백 제거
        value="${value// /}"
        case "$key" in
            HOST)      HOST="$value" ;;
            BASE_PORT) BASE_PORT="$value" ;;
        esac
    done < "$ENV_FILE"
fi

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
    local PORT=$(( BASE_PORT + NUM ))
    local URL="http://${HOST}:${PORT}"

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  📝 문제 $NUM  |  $URL"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    if [[ ! -d "$DIR" ]]; then
        echo "  ⚠️  $NUM 번 폴더가 없습니다. 건너뜁니다."
        ((SKIP++)) || true
        return
    fi

    if [[ ! -f "$TEST_FILE" ]]; then
        echo "  ⚠️  test_solution.py 가 없습니다."
        ((SKIP++)) || true
        return
    fi

    # HTTP 서버 시작
    "$PYTHON" -m http.server "$PORT" \
        --directory "$APP_DIR" \
        --bind "$HOST" \
        > /tmp/pw_server_$NUM.log 2>&1 &
    SERVER_PID=$!

    # 서버 준비 대기 (최대 3초)
    for i in $(seq 1 15); do
        if curl -s "$URL/" > /dev/null 2>&1; then break; fi
        sleep 0.2
    done

    # pytest 실행
    if BASE_URL="$URL" \
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

    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
}

# ── 실행 ───────────────────────────────────────────────────
echo ""
echo "🎭 Learning Playwright"
echo "   HOST      = $HOST"
echo "   BASE_PORT = $BASE_PORT  (문제 N → 포트 $((BASE_PORT+1))~$((BASE_PORT+10)))"
[[ -f "$ENV_FILE" ]] && echo "   설정 파일 = .env" || echo "   설정 파일 = 기본값 (없음)"

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
