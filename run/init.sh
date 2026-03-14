#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# run/init.sh  —  Learning Playwright 환경 초기화 (최초 1회 실행)
# ─────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo ""
echo "🎭 Learning Playwright — 환경 초기화"
echo "────────────────────────────────────"

# Python 버전 확인
PY=$(python3 --version 2>&1)
echo "✓ $PY 확인됨"

# pip 패키지 설치
echo ""
echo "📦 패키지 설치 중..."
python3 -m pip install --quiet pytest pytest-playwright

# Playwright 브라우저 설치
echo ""
echo "🌐 Playwright 브라우저 설치 중 (Chromium)..."
python3 -m playwright install chromium

echo ""
echo "✅ 초기화 완료!"
echo ""
echo "사용법:"
echo "  bash run/test.sh 1      # 1번 문제 테스트"
echo "  bash run/test.sh all    # 전체 테스트"
echo ""
