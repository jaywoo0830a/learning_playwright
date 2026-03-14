#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# run/open.sh  —  Playwright codegen 으로 앱 열기
#                 (클릭하면 코드가 자동 생성됨)
#
# 사용법:
#   bash run/open.sh 1            # 1번 문제 앱을 codegen 으로 열기
#   bash run/open.sh automation/6 # 실전 6번 codegen
#   bash run/open.sh 1 --browser  # codegen 없이 브라우저만 열기
# ─────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
cd "$ROOT"

# ── 가상환경 확인 ──────────────────────────────────────────
if [[ ! -f "$VENV/bin/python" ]]; then
    echo ""
    echo "❌ 가상환경이 없습니다: bash run/init.sh"
    echo ""
    exit 1
fi

PLAYWRIGHT="$VENV/bin/playwright"

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
    echo "사용법: bash run/open.sh <문제번호> [--browser]"
    echo ""
    echo "옵션:"
    echo "  (기본값)   codegen 모드 — 클릭하면 Python 코드가 자동 생성됨"
    echo "  --browser  codegen 없이 브라우저만 열기"
    echo ""
    echo "예시:"
    echo "  bash run/open.sh 1"
    echo "  bash run/open.sh automation/6"
    echo "  bash run/open.sh 3 --browser"
    echo ""
    exit 1
fi

NUM="$1"
MODE="codegen"
[[ "$2" == "--browser" ]] && MODE="browser"

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

if [[ ! -d "$APP_DIR" ]]; then
    echo "❌ 앱 폴더가 없습니다: $APP_DIR"
    exit 1
fi

# ── 포트 충돌 정리 ────────────────────────────────────────
lsof -ti tcp:"$PORT" | xargs kill -9 2>/dev/null || true

# ── HTTP 서버 시작 ────────────────────────────────────────
"$VENV/bin/python" -m http.server "$PORT" \
    --directory "$APP_DIR" \
    --bind "$HOST" \
    > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# 서버 대기
for i in $(seq 1 25); do
    if curl -s --max-time 1 "$URL/" > /dev/null 2>&1; then break; fi
    sleep 0.2
done

echo ""

# ── 모드별 실행 ───────────────────────────────────────────
if [[ "$MODE" == "codegen" ]]; then
    echo "🎭 Codegen 모드 — 브라우저에서 클릭하면 Python 코드가 자동 생성됩니다."
    echo "   URL: $URL"
    echo "   생성된 코드를 복사해서 test_solution.py 에 붙여넣으세요."
    echo ""
    # codegen 은 브라우저가 닫힐 때까지 blocking
    "$PLAYWRIGHT" codegen \
        --target python \
        "$URL" \
        2>&1
else
    echo "🌐 브라우저 모드 — $URL 을 엽니다."
    echo "   (이 창은 Ctrl+C 로 종료하세요)"
    echo ""
    # chromium 으로 URL 열기
    "$PLAYWRIGHT" open "$URL" 2>&1
fi

# ── 서버 종료 ────────────────────────────────────────────
kill "$SERVER_PID" 2>/dev/null || true
wait "$SERVER_PID" 2>/dev/null || true
