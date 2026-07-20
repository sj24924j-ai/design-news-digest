# デザインニュース ダイジェスト

乃村工藝社デザイナー職向けに、空間デザイン・建築・展示会/万博・サステナブル素材のニュースを毎朝まとめて確認できるWebアプリ。詳細な仕様は [requirements.md](requirements.md) を参照。

完全無料・サーバーレスで運用する（GitHub Actions + GitHub Pages）。投資助言ツールとは無関係の個人利用ツール。

## 構成

```
scripts/    ニュース収集バッチ（Python）。固定RSS + Google News キーワード検索RSSを取得しJSON化
frontend/   表示用の静的サイト（React + Vite + TypeScript）
  public/data/  日付ごとの記事JSON（バッチが生成）。フロントエンドはこれを読み込むだけ
.github/workflows/
  daily-news.yml    毎朝バッチを実行し、frontend/public/data を更新してコミット
  deploy-pages.yml  mainブランチへのpush時にビルドしGitHub Pagesへデプロイ
```

## セットアップ・開発コマンド

### ニュース収集バッチ (`scripts/`)

```bash
cd scripts
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python fetch_news.py     # frontend/public/data/ にJSONを生成・更新
```

購読メディア・キーワードは [scripts/feeds.py](scripts/feeds.py) で管理する。

### フロントエンド (`frontend/`)

```bash
cd frontend
npm install
npm run dev       # http://localhost:5173
npm run build      # tsc -b && vite build
npm run lint       # oxlint
```

## デプロイ

1. このリポジトリをGitHubへ作成しpush（Public。GitHub Pages無料プランの制約）
2. リポジトリ設定の Pages で「GitHub Actions」をソースに指定
3. `daily-news.yml` が毎朝ニュースデータを更新 → その push を `deploy-pages.yml` が検知して自動デプロイ

`vite.config.ts` の `base` はリポジトリ名 `design-news-digest` を前提にしている。リポジトリ名を変える場合はあわせて変更する。

## 既知の制約・今後の調整

- RSS未提供のメディア（乃村工藝社公式サイト等）はGoogle Newsキーワード検索で補完しているが、関連度が粗くノイズ記事が混ざることがある。`scripts/feeds.py` の `KEYWORD_QUERIES` を調整する。
- 要約は各フィードの見出し要約をそのまま使用（生成AIによる要約は行わない、無料方針）。
- 詳細な未決事項は [requirements.md](requirements.md) の13章を参照。
