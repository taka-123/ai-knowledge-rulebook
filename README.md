# AI ルール & 学習ノート リポジトリ

## 目的

- AI アシスタント向けルール・プロファイルと学習ノート/クリップ/スニペットを一元管理し、差分追跡と再利用性を高める。
- GitHub 上で閲覧・レビューしやすいプレーンテキスト形式（Markdown/JSON/YAML）を採用し、構成管理をシンプルに保つ。

## ディレクトリ構成

- @directorystructure.md 参照

## 技術スタック

- @technologystack.md 参照

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
- GitHub Pages + MkDocs によるブラウザ閲覧強化。

## 最初のセットアップ（手動作業）

- GitHub 上で `main` ブランチ保護（直 push 禁止・レビュー 1 名以上・必須ステータスチェック）を設定する。
- Secret scanning / Push Protection を有効化する。

## 謝辞

本プロジェクトのAIルールテンプレートは、以下の方々の公開情報を参考に作成しました。心より感謝申し上げます。

- [kinopeee](https://github.com/kinopeee) さん - [cursorrules](https://github.com/kinopeee/cursorrules)
- [sazan_dev](https://x.com/sazan_dev) さん - [X投稿](https://x.com/sazan_dev/status/1968222841981002203)
- [sesere](https://zenn.dev/sesere) さん - [Zenn記事](https://zenn.dev/sesere/articles/0420ecec9526dc)

その他、多くの方々のオープンな知見の共有に感謝いたします。
