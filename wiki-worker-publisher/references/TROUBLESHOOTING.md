# TROUBLESHOOTING.md — wiki-worker-publisher

## 1. Could not resolve "hono" or "common-worker-utils"

### 原因
`cf-workers` は npm workspaces 構造を採用しており、サブディレクトリ単独で実行した場合や依存関係がリンクされていない場合に esbuild がモジュールを見失う。

### 解決策
1. `cf-workers` のルートディレクトリに移動:
   ```bash
   cd /mnt/d/cf-workers
   ```
2. ルートで依存関係を解決:
   ```bash
   npm install
   ```
3. その後、再度 `wiki-worker` のデプロイを実行する。

---

## 2. Wrangler OAuth トークン失効・認証エラー

### 原因
Cloudflare OAuth トークンの有効期限切れ、またはログアウト状態。

### 解決策
1. ログイン状況を確認:
   ```bash
   npx wrangler whoami
   ```
2. 認証が切れている場合は再ログインを実行:
   ```bash
   npx wrangler login
   ```

---

## 3. 中間生成ファイル・スクリプトの保持方針

### 運用ルール
トラブル調査や次回再実行のため、作業中に生成されたスクリプト、ビルドログ、テストファイル等は**自動削除しない**。明示的に不要と判断された場合のみユーザー確認の上で対応する。
