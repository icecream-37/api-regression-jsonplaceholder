import os

import pytest
import requests

DEFAULT_BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", DEFAULT_BASE_URL).rstrip("/")


class _LoggingSession(requests.Session):
    """Session that remembers the last response for failure summaries."""

    def __init__(self) -> None:
        super().__init__()
        self.last_response: requests.Response | None = None

    def request(self, *args, **kwargs):  # type: ignore[override]
        resp = super().request(*args, **kwargs)
        self.last_response = resp
        return resp


@pytest.fixture(scope="session")
def client() -> _LoggingSession:
    session = _LoggingSession()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    session = item.funcargs.get("client") if hasattr(item, "funcargs") else None
    resp = getattr(session, "last_response", None) if session is not None else None
    base = item.funcargs.get("base_url", DEFAULT_BASE_URL) if hasattr(item, "funcargs") else DEFAULT_BASE_URL
    print(f"\n[failure summary] BASE_URL={base}")
    print(f"[failure summary] test={item.nodeid}")
    if resp is not None:
        body = (resp.text or "")[:300].replace("\n", " ")
        print(f"[failure summary] status={resp.status_code} body={body}")
