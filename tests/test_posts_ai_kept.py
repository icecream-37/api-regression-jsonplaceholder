"""Cases kept (or modified) from docs/ai-case-review.md after human review."""


def test_list_posts_filter_by_user_id(client, base_url):
    resp = client.get(f"{base_url}/posts", params={"userId": 1}, timeout=15)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) > 0
    assert all(item.get("userId") == 1 for item in data)


def test_get_post_comments_for_post_1(client, base_url):
    resp = client.get(f"{base_url}/posts/1/comments", timeout=15)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list) and len(data) > 0
    assert all(item.get("postId") == 1 for item in data)
    first = data[0]
    assert {"id", "name", "email", "body"}.issubset(first.keys())


def test_delete_post_does_not_500(client, base_url):
    """JSONPlaceholder often returns 200 on DELETE without durable removal; do not assume 404 after."""
    resp = client.delete(f"{base_url}/posts/1", timeout=15)
    assert resp.status_code < 500
