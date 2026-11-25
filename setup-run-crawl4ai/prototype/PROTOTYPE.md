# PROTOTYPE.md: プロトタイプ資産仕様書・流用/入替境界ガイド (setup-run-crawl4ai)

本ドキュメントは、`setup-run-crawl4ai` スキルにおけるプロトタイプ資産（Dockerコンテナ常駐環境）の構成を解説し、**別端末（会社PC等）へバッチ導入・流用する部分** と **環境固有で差し替える部分** の境界を明確に定義・分離したものです。

---

## 1. プロトタイプ収録資産の全体構造

```text
prototype/
├── docker-compose.yml          # Crawl4AI 実稼働コンテナ定義（shm-size=1g, 自動再起動）
└── sample_crawl.py             # 稼働テスト・動作検証スクリプト
```

---

## 2. 流用できる部分（汎用設計） vs 差し替える部分（環境固有要件）

会社PCや別端末、クラウド環境に導入する際は以下の境界線に従います。

| 構成要素 | 別端末でもそのまま「流用」できる部分（汎用資産） | 端末ごとに「差し替える」部分（固有要件） |
|:---|:---|:---|
| **コンテナ実行仕様<br>(`docker-compose.yml`)** | ・`unclecode/crawl4ai:latest` の公式イメージ<br>・Chromiumクラッシュ防止用の共有メモリ拡張（`shm_size: 1g`）<br>・内部待受ポート `11235`<br>・コンテナ健全性チェック定義（`healthcheck`） | ・ホスト側の待受ポート番号（他プロセスと競合する場合 `11235` 以外に変更）<br>・永続化ボリューム（必要に応じてログやプロファイルマウントを追加） |
| **認証トークン管理<br>(`CRAWL4AI_API_TOKEN`)** | ・暗号論的擬似乱数（32バイトhex/64文字）による自動生成ロジック<br>・指定 `.env` への追記・同期フォーマット（`CRAWL4AI_BASE_URL`, `CRAWL4AI_API_TOKEN`） | ・生成された具体的なトークン値（端末・環境ごとにユニーク）<br>・環境変数ファイルの保存先パス（`/mnt/d/conf/.env` や会社PCの任意パス） |
| **起動・検証フロー** | ・Dockerデーモン存在確認 → コンテナ起動 → `/health` ポーリング待機の決定論的フロー<br>・テスト用スクレイピングリクエスト（`sample_crawl.py`） | ・プロキシ環境（会社PCの社内HTTP_PROXY/HTTPS_PROXY設定の注入） |

---

## 3. 別端末（会社PC等）への導入チェックリスト

1. **Docker の稼働確認**: Docker Desktop または Docker Engine が起動していること。
2. **ワンクリックセットアップの実行**:
   ```bash
   python3 scripts/setup_crawl4ai.py --env-file /path/to/your/.env
   ```
3. **自動検証の合格確認**:
   ```bash
   python3 scripts/verify_crawl4ai.py --env-file /path/to/your/.env
   ```
