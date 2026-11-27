# References: TOOLS.md

## 1. 4分類ツールマトリクス (Tool Classification)

| 分類 | ツール名 / サービス | 実行コマンド / エンドポイント | 用途・役割 |
|:---|:---|:---|:---|
| **Command** | `uv` | `~/.local/bin/uv` | Python パッケージ・ツール高速管理 |
| **Command** | `node` | `node -v` | Node.js ランタイム実行 |
| **Command** | `npm` | `npm -v` | Node パッケージ管理 |
| **Command** | `wrangler` | `wrangler` | Cloudflare Workers / Pages 開発・デプロイ |
| **Command** | `gcloud` | `~/google-cloud-sdk/bin/gcloud` | Google Cloud Platform リソース管理 |
| **Command** | `colab` | `~/.local/bin/colab` | Google Colab VM / ノートブック実行 |
| **Command** | `kaggle` | `~/.local/bin/kaggle` | Kaggle コンペティション / データセット管理 |
| **Shell** | `nvm` | `\. "$NVM_DIR/nvm.sh"` | シェル関数型 Node.js バージョン切り替え |
| **MCP** | None (Local CLI only) | N/A | 本スキルはローカル CLI プロビジョニング用であり MCP サーバーは起動しません |
| **外部 API** | Google Cloud / Colab API | `https://*.googleapis.com` | gcloud / colab CLI によるリモート認証・セッション管理 |
| **外部 API** | Cloudflare API | `https://api.cloudflare.com/client/v4` | wrangler による Workers / DNS / Pages デプロイ |
| **外部 API** | Kaggle API | `https://www.kaggle.com/api/v1` | kaggle CLI によるデータセット取得・ノートブックプッシュ |

---

## 2. Authentication & Initial Setup

### gcloud
```bash
gcloud init
gcloud auth application-default login
```

### Wrangler (Cloudflare)
```bash
wrangler login
wrangler whoami
```

### Colab CLI
Requires GCP credentials or OAuth:
```bash
gcloud auth application-default login
colab --auth adc usage
```

### Kaggle CLI
Place API credentials in `~/.kaggle/kaggle.json`:
```bash
mkdir -p ~/.kaggle
chmod 600 ~/.kaggle/kaggle.json
# or interactive browser login:
kaggle auth login
```
