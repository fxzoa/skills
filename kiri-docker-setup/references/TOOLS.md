# TOOLS.md

## Tool Classification (4分類)

### 1. Command
* `scripts/install_kiri.py`: Kiri バイナリと Docker プラグインのダウンロードおよび展開
* `scripts/setup_service.py`: systemd サービスファイルの生成・登録と再起動
* `scripts/link_skills.py`: `/mnt/d/skills` から `.agents/skills` へのシンボリックリンク生成

### 2. Shell
* `docker context use kiri`: Docker 既定コンテキストの切り替え
* `systemctl status kiri.service`: Kiri サービスのヘルスチェック
* `docker run --rm alpine echo hello`: 疎通・コンテナ生成スモークテスト

### 3. MCP
* 該当なし（ローカル CLI および systemd 制御に特化）

### 4. 外部 API
* `https://github.com/libracoder/kiri/releases/download/v0.2.2/kiri_0.2.2_amd64.deb`: Kiri 公式 Debian パッケージのダウンロード
