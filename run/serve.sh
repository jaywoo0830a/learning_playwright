#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# run/serve.sh  —  문제 앱 서버만 띄우기 (테스트 없이)
#
# 브라우저에서 직접 UI 를 보거나
# 수동으로 pytest 를 실행할 때 서버를 먼저 켜두는 용도.
#
# 사용법:
#   bash run/serve.sh 1            # 1번 앱 서버 실행 (Ctrl+C 로 종료)
#   bash run/serve.sh automation/6 # 실전 6번 앱 서버
# ─────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
cd "$ROOT"

if [[ ! -f "$VENV/bin/python" ]]; then
    echo "❌ 가상환경이 없습니다: bash run/init.sh"
    exit 1
fi

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

if [[ $# -eq 0 ]]; then
    echo ""
    echo "사용법: bash run/serve.sh <문제번호>"
    echo "예시:   bash run/serve.sh 1"
    echo "        bash run/serve.sh automation/6"
    echo ""
    exit 1
fi

NUM="$1"

if [[ "$NUM" == automation/* ]]; then
    SUB="${NUM#automation/}"
    PORT=$(( 8200 + SUB ))
else
    PORT=$(( BASE_PORT + NUM ))
fi

URL="http://${HOST}:${PORT}"
APP_DIR="$ROOT/$NUM/app"

if [[ ! -d "$APP_DIR" ]]; then
    echo "❌ 앱 폴더가 없습니다: $APP_DIR"
    exit 1
fi

# 포트 충돌 정리
lsof -ti tcp:"$PORT" | xargs kill -9 2>/dev/null || true

echo ""
echo "🌐 서버 시작: $URL"
echo "   앱 경로  : $APP_DIR"
echo ""
echo "   브라우저에서 $URL 을 열어보세요."
echo "   수동 테스트: BASE_URL=$URL .venv/bin/pytest $NUM/test_solution.py --headed -v"
echo ""
echo "   Ctrl+C 로 서버를 종료합니다."
echo ""

# 포그라운드 실행 — Ctrl+C 로 종료
"$VENV/bin/python" -m http.server "$PORT" \
    --directory "$APP_DIR" \
    --bind "$HOST"
