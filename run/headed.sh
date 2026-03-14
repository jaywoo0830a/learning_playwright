#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# run/headed.sh  —  헤드 모드 (브라우저 직접 보면서) 테스트 실행
#
# 사용법:
#   bash run/headed.sh 1            # 1번 문제 헤드 모드
#   bash run/headed.sh automation/6 # 실전 6번 헤드 모드
#   bash run/headed.sh 3 --slowmo   # 3번 문제 슬로우 모션 (500ms)
#   bash run/headed.sh 3 --slowmo 1000  # 슬로우 모션 1000ms
# ─────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
cd "$ROOT"

# ── 가상환경 확인 ──────────────────────────────────────────
if [[ ! -f "$VENV/bin/python" ]]; then
    echo ""
    echo "❌ 가상환경이 없습니다. 먼저 초기화를 실행하세요:"
    echo "   bash run/init.sh"
    echo ""
    exit 1
fi

PYTHON="$VENV/bin/python"
PYTEST="$VENV/bin/pytest"

# ── .env 로드 ─────────────────────────────────────────────
HOST="127.0.0.1"
BASE_PORT=8100
ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
    while IFS='=' read -r key value; do
        [[ -z "$key" || "$key" == \#* ]] && continue
        key="${key// /}"; value="${value// /}"
        case "$key" in
            HOST)      HOST="$value" ;;
            BASE_PORT) BASE_PORT="$value" ;;
        esac
    done < "$ENV_FILE"
fi

# ── 인자 파싱 ─────────────────────────────────────────────
if [[ $# -eq 0 ]]; then
    echo ""
    echo "사용법: bash run/headed.sh <문제번호> [옵션]"
    echo ""
    echo "옵션:"
    echo "  --slowmo [ms]   슬로우 모션 (기본 500ms)"
    echo ""
    echo "예시:"
    echo "  bash run/headed.sh 1"
    echo "  bash run/headed.sh automation/6"
    echo "  bash run/headed.sh 3 --slowmo"
    echo "  bash run/headed.sh 3 --slowmo 1000"
    echo ""
    exit 1
fi

NUM="$1"
shift

# 슬로우 모션 옵션 파싱
SLOWMO_MS=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --slowmo)
            shift
            if [[ $# -gt 0 && "$1" =~ ^[0-9]+$ ]]; then
                SLOWMO_MS="$1"; shift
            else
                SLOWMO_MS="500"
            fi
            ;;
        *) shift ;;
    esac
done

# ── 포트 계산 ─────────────────────────────────────────────
if [[ "$NUM" == automation/* ]]; then
    SUB="${NUM#automation/}"
    PORT=$(( 8200 + SUB ))
else
    PORT=$(( BASE_PORT + NUM ))
fi

SAFE_NUM="${NUM//\//_}"
LOG_FILE="/tmp/pw_server_${SAFE_NUM}.log"
URL="http://${HOST}:${PORT}"

DIR="$ROOT/$NUM"
APP_DIR="$DIR/app"
TEST_FILE="$DIR/test_solution.py"

echo ""
echo "🎭 헤드 모드 실행"
echo "   문제: $NUM"
echo "   URL : $URL"
[[ -n "$SLOWMO_MS" ]] && echo "   슬로우 모션: ${SLOWMO_MS}ms"
echo ""

# ── 유효성 확인 ───────────────────────────────────────────
if [[ ! -f "$TEST_FILE" ]]; then
    echo "❌ test_solution.py 를 찾을 수 없습니다: $TEST_FILE"
    exit 1
fi

# ── 포트 충돌 정리 ────────────────────────────────────────
lsof -ti tcp:"$PORT" | xargs kill -9 2>/dev/null || true

# ── HTTP 서버 시작 ────────────────────────────────────────
"$PYTHON" -m http.server "$PORT" \
    --directory "$APP_DIR" \
    --bind "$HOST" \
    > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# 서버 준비 대기
READY=0
for i in $(seq 1 25); do
    if curl -s --max-time 1 "$URL/" > /dev/null 2>&1; then
        READY=1; break
    fi
    sleep 0.2
done

if [[ $READY -eq 0 ]]; then
    echo "❌ 서버 시작 실패 (포트 $PORT)"
    kill "$SERVER_PID" 2>/dev/null || true
    exit 1
fi

# ── pytest 헤드 모드 실행 ─────────────────────────────────
EXTRA_ARGS=""
if [[ -n "$SLOWMO_MS" ]]; then
    EXTRA_ARGS="--slowmo $SLOWMO_MS"
fi

echo "🌐 브라우저가 열립니다. 테스트 진행 상황을 직접 확인하세요."
echo ""

BASE_URL="$URL" "$PYTEST" "$TEST_FILE" \
    --headed \
    $EXTRA_ARGS \
    --tb=long \
    --no-header \
    -v \
    2>&1
EXIT_CODE=$?

# ── 서버 종료 ────────────────────────────────────────────
kill "$SERVER_PID" 2>/dev/null || true
wait "$SERVER_PID" 2>/dev/null || true

exit $EXIT_CODE
