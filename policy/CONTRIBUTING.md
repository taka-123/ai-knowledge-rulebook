# Contributing Guide

## 1. 事前準備

- `main` を最新化し、トピックブランチ `feat/...` `fix/...` などを作成する。
- Node.js / Python が利用可能な環境で lint ツールを実行できるようにしておく。

## 2. コードスタイル

- インデントはスペース 2。`.editorconfig` に従う。
- Markdown は見出し→本文→箇条書きの順で簡潔に。FrontMatter を必須とするファイルでは `created` / `updated` を ISO8601 で記載する。

## 3. テスト

- 変更が Markdown/YAML/JSON の場合でも `npm uninstall` など不要な差分を入れない。
- `markdownlint-cli2` `yamllint` `check-jsonschema` がローカルで通ることを確認する。

## 4. PR 作成

1. 変更の目的と背景を先頭にまとめる。
2. 動作確認結果（スクリーンショット・コマンド出力など）を添付する。
3. TODO が残る場合は Issue 化してリンクする。

## 5. レビュー対応

- 指摘はブロック/任意を明確に分類し、解決したらレスポンスを残す。
- 大きな方針変更はドラフト PR で相談し、了解を得てから実装する。
