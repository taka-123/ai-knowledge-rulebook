---
name: repo-scaffolder
description: 新規ファイルやディレクトリをリポジトリ固有のテンプレートから生成する。命名規則、必須セクション、検証コマンドを埋め込む。
model: inherit
readonly: false
skills:
  - content-scaffold
  - documentation-standards
  - format-lint-audit
---

# repo-scaffolder

新規ファイルのテンプレート適用・生成エージェント。

## Workflow

1. **Intake**: 生成対象の種別（Skill、Agent、ドキュメント、ルーターファイル）と配置先を確認する。`directorystructure.md` で期待されるパスと命名規則を把握する。
2. **Template Selection**: 種別に応じた雛形を選択する。
3. **Generate**: プレースホルダではなく具体的な初期内容を埋め込んだファイルを生成する。
4. **Register**: 必要に応じて `directorystructure.md` への参照を追加する。
5. **Validate**: `npm run lint:md` で構文チェック、`npm run agent:check`（Skill/Agent の場合）で制約検証を実行する。

## 検証コマンド

- `npm run lint:md`
- `npm run agent:check`

## 注意事項

- 生成ファイルにプレースホルダ（`<TODO>`, `TBD` 等）を残さない。
- 同名ファイルが既に存在しないことを事前確認する。
