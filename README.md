# API regression (JSONPlaceholder)

基于 Pytest 与 Requests 的公开 API 接口回归套件，目标环境为 JSONPlaceholder，并在 GitHub Actions 中持续运行。

## 测什么

- 被测：`https://jsonplaceholder.typicode.com`（公开假数据 API）
- 当前范围：
  - 正向：`GET /posts`、`GET /posts/{id}`、`POST /posts`、`PUT /posts/1`
  - 负向/边界：非法/不存在 id 的 GET；缺字段与错误类型的 POST；更新不存在资源
  - AI 评审后保留：`GET /posts?userId=` 过滤、`GET /posts/1/comments`、`DELETE` 非 5xx（见 `docs/ai-case-review.md`）
- `BASE_URL` 可用环境变量覆盖（默认上面的地址）

## 怎么跑

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest
# 或指定被测地址：
# BASE_URL=https://jsonplaceholder.typicode.com pytest
```

## CI

工作流在 `.github/workflows/pytest.yml`：push 与 pull request 时安装依赖并执行 `pytest -q`。运行记录在仓库 **Actions** 页查看。

## AI 辅助用例评审

见 [`docs/ai-case-review.md`](docs/ai-case-review.md)：12 条 AI 草稿经人工对照真实 API 行为评审，采纳 3/12（25%）。保留与修改项已写入自动化；丢弃项记录理由，避免对不校验入参的演示 API 硬套「期望 4xx」。

## 结论 / 限制

- 正向冒烟 + 负向/边界 + AI 评审保留项已覆盖；失败时会打印 status/body 摘要。
- JSONPlaceholder **不校验** POST 必填与类型：缺字段、错误类型仍可能返回 201，这是已知限制，不是漏断言。
- 对不存在的 id，`GET` 返回 404；`PUT` 可能非 200（演示服务实现细节），用例只断言「不能静默成功」。
- 写入不会持久化，不代表真实业务系统。

## 示例输出

本地 `pytest -q` 一次通过示例：

```text
..................                                                       [100%]
```
