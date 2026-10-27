import pytest


@pytest.mark.parametrize(
    "post_id",
    [0, -1, 99999, "abc"],
    ids=["zero", "negative", "missing", "non_numeric"],
)
def test_get_post_invalid_id_returns_404(client, base_url, post_id):
    resp = client.get(f"{base_url}/posts/{post_id}", timeout=15)
    assert resp.status_code == 404


def test_create_post_empty_body_still_201(client, base_url):
    """JSONPlaceholder does not validate required fields; document the real behavior."""
    resp = client.post(f"{base_url}/posts", json={}, timeout=15)
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data


def test_create_post_missing_title_still_201(client, base_url):
    payload = {"body": "no title", "userId": 1}
    resp = client.post(f"{base_url}/posts", json=payload, timeout=15)
    assert resp.status_code == 201
    data = resp.json()
    assert data.get("body") == payload["body"]
    assert "title" not in data or data.get("title") in (None, "")


def test_create_post_wrong_types_echoed(client, base_url):
    """Wrong types are accepted and echoed; useful as a known API limitation."""
    payload = {"title": 123, "body": True, "userId": "nope"}
    resp = client.post(f"{base_url}/posts", json=payload, timeout=15)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == 123
    assert data["body"] is True
    assert data["userId"] == "nope"


def test_update_nonexistent_post_does_not_return_200(client, base_url):
    """json-server may 500 on update of a missing id; we only assert it is not a silent success."""
    payload = {"title": "ghost", "body": "x", "userId": 1}
    resp = client.put(f"{base_url}/posts/99999", json=payload, timeout=15)
    assert resp.status_code != 200
