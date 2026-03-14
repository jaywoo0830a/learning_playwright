#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# run/init.sh  —  Learning Playwright 환경 초기화 (최초 1회 실행)
#
# 프로젝트 루트에 .venv 가상환경을 생성하고
# pytest-playwright 및 Chromium 브라우저를 설치합니다.
# ─────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$ROOT/.venv"
cd "$ROOT"

echo ""
echo "🎭 Learning Playwright — 환경 초기화"
echo "────────────────────────────────────"

# ── Python 버전 확인 ───────────────────────────────────────
PY=$(python3 --version 2>&1)
echo "✓ $PY 확인됨"

# ── 가상환경 생성 ──────────────────────────────────────────
if [[ -d "$VENV" ]]; then
    echo "✓ 가상환경이 이미 존재합니다 (.venv)"
else
    echo ""
    echo "📁 가상환경 생성 중 (.venv)..."
    python3 -m venv "$VENV"
    echo "✓ 가상환경 생성 완료"
fi

# ── 가상환경 안의 pip / python 경로 ───────────────────────
PIP="$VENV/bin/pip"
PYTHON="$VENV/bin/python"
PLAYWRIGHT="$VENV/bin/playwright"

# ── 패키지 설치 ────────────────────────────────────────────
echo ""
echo "📦 패키지 설치 중 (가상환경)..."
"$PIP" install --quiet --upgrade pip
"$PIP" install --quiet pytest pytest-playwright

# ── Playwright 브라우저 설치 ───────────────────────────────
echo ""
echo "🌐 Playwright Chromium 브라우저 설치 중..."
"$PLAYWRIGHT" install chromium

echo ""
echo "✅ 초기화 완료!"
echo ""
echo "가상환경 위치 : $VENV"
echo ""
echo "사용법:"
echo "  bash run/test.sh 1      # 1번 문제 테스트"
echo "  bash run/test.sh all    # 전체 테스트"
echo ""
echo "가상환경을 직접 활성화하려면:"
echo "  source .venv/bin/activate        # macOS / Linux"
echo "  .venv\\Scripts\\activate           # Windows (Git Bash)"
echo ""
