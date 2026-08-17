---
title: 'スニペット集'
created: 2025-09-27
updated: 2026-08-17
tags: ['snippets']
source: ''
---

## 利用ルール

- プロンプトや正規表現、小さなスクリプトを用途別に整理する。
- 使用例と注意点を併記し、実行に必要な前提条件があれば記録する。
- 使い捨てスニペットは削除せず、利用履歴や背景を残す。

## ディレクトリ構成

```
snippets/
├── README.md                    # 本ファイル
├── aws-github-safety-setup.md   # 他プロジェクトへ貼る AWS/GitHub 安全設定の一発指示
└── editor/                      # AI編集用プロンプトテンプレート
    ├── adjustment_rule.md       # テンプレート調整ルール
    └── compression_improvement.md # ファイル圧縮改良プロンプト
```

## 想定ファイル例

- **AI共通プロンプトテンプレート**: 複数のAIツールで再利用可能な汎用プロンプト
  - `aws-github-safety-setup.md`: 任意のソフトウェアリポジトリへ、AWS MCP 参照 + GitHub MCP 限定書き込み + IAM 手順を自己完結で入れる指示。対象プロジェクトの AI チャットに全文を貼る。他ファイルを読ませない。
  - 例: `prompt-code-review.md`, `prompt-refactoring.md`
- **正規表現パターン集**: 頻出する検索・置換パターン
  - 例: `regex-patterns.md`
- **使い捨てスクリプト**: 一時的な整形・変換スクリプト
  - 例: `quick-format.sh`, `convert-yaml-to-json.py`
- **エディタ補助プロンプト**: `editor/` 配下に配置済み
