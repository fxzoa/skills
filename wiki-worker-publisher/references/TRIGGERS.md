# TRIGGERS.md — wiki-worker-publisher

## Positive Triggers (スキルを発動すべきプロンプト例)
- 「WIKI-WORKERへ上記HTMLを足して、デプロイして」
- 「作成したHTMLを wiki.btczoa.app に追加して公開してほしい」
- 「wiki-workerのllm-infraカテゴリにこの構成図をデプロイして」
- 「スタンドアロンHTML仕様書を社内Wikiポータルへ反映させて」
- 「wiki-worker に新しいアーキテクチャ図を追加して本番反映して」

## Negative Triggers (スキルを発動すべきでない例)
- 「静的HTMLをGitHub PagesやVercelに公開して」（→ 一般のWebホスティング）
- 「Kaggle Notebook をデプロイして」（→ `kaggle-notebook` / `kaggle-operator`）
- 「Google Colab で推論サーバーを立ち上げて」（→ `colab-operator` / `colab-notebook`）
- 「単にローカルでHTML図解を作成してほしい」（→ `architecture-diagram` / `diagram-design`）

## Smoke Test (スモークテスト手順)
1. 任意のテスト用HTMLを作成（例: `/tmp/test.html`）
2. `--skip-deploy` を付けてローカルビルド検証:
   ```bash
   python3 scripts/publish_doc.py --html /tmp/test.html --category llm-infra --skip-deploy
   ```
3. `dist/catalog.json` にテストHTMLが正しく登録されていることを確認。
