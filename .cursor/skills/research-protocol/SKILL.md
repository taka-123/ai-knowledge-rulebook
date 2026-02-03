---
name: research-protocol
description: Enforces citations and uncertainty notes for technical research before writing. Use when the user mentions 調査, 仕様, API, 公式ドキュメント, 出典, or when writing to notes/clips/ai/policy.
disable-model-invocation: true
---

# Research Protocol

## Quick Start

1. 技術的記述を抽出する。
2. 各記述に出典 URL と取得日が付与されているか確認する。
3. 不確実性がある記述に「未確認/推定」の注記を付与する。
4. 書き込み前に不足項目を列挙し、補完方針を示す。

## Source Priority

1. 公式 Spec / RFC
2. 公式 Docs
3. 公式 GitHub（Releases/Issues）
4. WebSearch（公式発表）

## Required Citation Format

```
**出典**: [ドキュメント名](URL)
**取得日**: YYYY-MM-DD
```

## Uncertainty Format

```
⚠️ **未確認**: [内容]（公式ドキュメントに明記なし）
```

## Decision Rules

- 出典がない技術的記述は書き込まない。
- 仕様が揺れる場合は複数ソースでクロスチェックし、差分を明記する。

## Output Format

対象:
必須出典:

- ...
  不足:
- ...
  補完方針:
- ...

## Verification

- 書き込み後に必要な監査コマンドが実行されることを確認する。
