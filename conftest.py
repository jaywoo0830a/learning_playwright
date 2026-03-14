"""
conftest.py — 공통 pytest 설정

우선순위:
  1. 환경변수 BASE_URL          (test.sh 가 문제별로 자동 주입)
  2. 프로젝트 루트 .env 파일    (직접 pytest 실행 시 편의용)
  3. 기본값 http://127.0.0.1:8101

.env 예시 (직접 pytest 실행 시):
  HOST=127.0.0.1
  BASE_PORT=8100        # 실제 포트 = BASE_PORT + 문제번호
"""
import os
from pathlib import Path

import pytest

# ── .env 파일 로드 (환경변수가 없을 때만 보완) ─────────────────
_ENV_FILE = Path(__file__).parent / ".env"


def _load_env_file() -> dict:
    """Parse KEY=VALUE lines from .env, ignoring comments and blanks."""
    if not _ENV_FILE.exists():
        return {}
    result = {}
    for line in _ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result


_env_vars = _load_env_file()


def _get(key: str, default: str) -> str:
    """환경변수 우선, 없으면 .env, 없으면 default."""
    return os.environ.get(key) or _env_vars.get(key) or default


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "problem: learning_playwright problem number")


@pytest.fixture(scope="session")
def base_url() -> str:
    """
    Return the base URL for the current problem's dev server.

    test.sh 실행 시    → BASE_URL 환경변수로 자동 주입됨
    직접 pytest 실행 시 → .env 의 HOST / BASE_PORT 를 참고
    """
    url = _get("BASE_URL", "")
    if url:
        return url.rstrip("/")

    host      = _get("HOST", "127.0.0.1")
    base_port = _get("BASE_PORT", "8100")
    # 직접 실행 시 포트를 알 수 없으므로 BASE_PORT+1(문제 1)을 기본값으로
    return f"http://{host}:{int(base_port) + 1}"
