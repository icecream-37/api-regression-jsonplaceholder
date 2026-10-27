import pytest


def test_list_posts_returns_200_and_non_empty(client, base_url):
    resp = client.get(f"{base_url}/posts", timeout=15)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) > 0
    assert {"userId", "id", "title", "body"}.issubset(data[0].keys())


def test_get_post_1_returns_200_and_expected_fields(client, base_url):
    resp = client.get(f"{base_url}/posts/1", timeout=15)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert "userId" in data
    assert isinstance(data["title"], str) and data["title"]
    assert isinstance(data["body"], str) and data["body"]


@pytest.mark.parametrize("post_id", [1, 2, 10])
def test_get_post_by_id_shape(client, base_url, post_id):
    resp = client.get(f"{base_url}/posts/{post_id}", timeout=15)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == post_id
    assert isinstance(data["title"], str)


def test_create_post_returns_201_and_echoes_fields(client, base_url):
    payload = {"title": "smoke create", "body": "hello", "userId": 1}
    resp = client.post(f"{base_url}/posts", json=payload, timeout=15)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data


def test_update_post_returns_200_and_echoes_title(client, base_url):
    payload = {"title": "smoke update", "body": "updated", "userId": 1}
    resp = client.put(f"{base_url}/posts/1", json=payload, timeout=15)
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
