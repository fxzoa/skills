# setup-run-crawl4ai: Operation Guide

## 1. 会社PCや新端末での初回セットアップ
Docker が起動している環境で、以下の 1 コマンドを実行します：

```bash
# 例: 会社PCのプロジェクト設定ファイルに追記する場合
python3 scripts/setup_crawl4ai.py --env-file /path/to/your/project/.env
```
このコマンドにより：
1. 32バイトの暗号論的トークンが自動生成されます。
2. `unclecode/crawl4ai:latest` コンテナが `shm-size=1g` で起動します。
3. `/health` エンドポイントが応答するまで自動ポーリングされます。
4. 指定した `.env` に `CRAWL4AI_BASE_URL` と `CRAWL4AI_API_TOKEN` が自動書き込みされます。

---

## 2. 稼働状態の検証
```bash
python3 scripts/verify_crawl4ai.py --env-file /path/to/your/project/.env
```

---

## 3. Webスクレイピングの実行
```bash
# Markdown 形式で取得して標準出力
python3 scripts/crawl_url.py https://news.ycombinator.com/

# JSON 形式でファイルへ保存
python3 scripts/crawl_url.py https://example.com/ -o result.json --format json
```
