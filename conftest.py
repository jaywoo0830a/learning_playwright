"""
conftest.py — 공통 pytest 설정

BASE_URL 환경변수를 읽어 base_url fixture로 주입합니다.
test.sh 가 각 문제 서버 주소를 BASE_URL로 넘겨줍니다.
"""
import os
import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "problem: learning_playwright problem number")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the current problem's dev server."""
    url = os.environ.get("BASE_URL", "http://127.0.0.1:8101")
    return url.rstrip("/")
