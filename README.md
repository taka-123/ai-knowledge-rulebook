# AI ルール & 学習ノート リポジトリ

## 目的

- AI アシスタント向けルール・プロファイルと学習ノート/クリップ/スニペットを一元管理し、差分追跡と再利用性を高める。
- GitHub 上で閲覧・レビューしやすいプレーンテキスト形式（Markdown/JSON/YAML）を採用し、構成管理をシンプルに保つ。

## ディレクトリ構成（初期）

- `policy/`: リポジトリ運用指針とコントリビュート手順。
- `ai/`: Cursor・Windsurf・ChatGPT・Claude・Gemini 用プロファイル原本。
- `notes/`: 日次ログおよびテーマ別ノート。FrontMatter でメタデータを管理。
- `clips/`: 記事要約・引用を取得日付きで保存。
- `snippets/`: プロンプトや小スクリプトのメモ。
- `schemas/`: AI プロファイルやノートの JSON Schema 雛形。
- `tools/`: 生成補助・整形・同期スクリプト格納場所。
- `.config/`: Lint・検証設定（Markdownlint/Yamllint/JSONSchema）。
- `.github/`: Issue/PR テンプレートと CI ワークフロー。

## 運用フロー

1. 作業ブランチを切り、変更を加えたら PR を作成する。
2. PR では差分の意図と検証内容を先頭に明記する。
3. CI（Markdown/YAML/JSON 構文チェック・Secret Scan）がグリーンであることを確認する。
4. レビュー 1 名以上の承認後に `main` へマージする。

## セキュリティと注意事項

- API キーや個人情報など機密はコミットしない。必要に応じて `.env.sample` 等で雛形のみ共有する。
- GitHub の Secret scanning / Push Protection を有効化し、検出時は速やかに修正する。
- バイナリや大型ファイルは原則禁止。必要な場合は Git LFS を検討する。

## 今後の拡張例

- Obsidian Sync 連携によるモバイル編集効率化（任意）。
- `tools/` 配下へのノート整形スクリプト追加。
- GitHub Pages + MkDocs によるブラウザ閲覧強化。

## 最初のセットアップ（手動作業）

- GitHub 上で `main` ブランチ保護（直 push 禁止・レビュー 1 名以上・必須ステータスチェック）を設定する。
- Secret scanning / Push Protection を有効化する。
