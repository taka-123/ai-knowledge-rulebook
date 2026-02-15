---
name: content-scaffold
description: Use when new markdown or rule files must be created from repository-specific templates with concrete commands and validation criteria; When NOT to use: modifications to already complete files that need no scaffolding; Trigger Keywords: 新規ファイル, scaffold, テンプレート, 雛形, 初期化.
---

# content-scaffold

## When to use

- 新規ドキュメントやルールを追加する。
- 既存規約に沿った雛形が必要。

## When NOT to use

- 既存ファイルの小修正のみ。
- 雛形不要な単発回答。

## Trigger Keywords

- 新規ファイル
- scaffold
- テンプレート
- 雛形
- 初期化

## Examples

### Example 1

Input: 新しい運用手順書を作るので骨組みを生成して。
Output: 見出し、入力条件、実行手順、検証項目を含む markdown 雛形を作成する。

### Example 2

Input: Cursor rule ファイルを追加するテンプレがほしい。
Output: frontmatter と trigger 節を持つ `.mdc` 雛形を生成する。

### Example 3

Input: 検証レポート用の標準フォーマットを作って。
Output: KPI、根拠、テスト結果、残課題の固定セクションを持つ雛形を出す。

---

## 1. Workflow

1. **Intake**: 生成するファイルの種別（Markdown ドキュメント / Cursor rule `.mdc` / Windsurf rule `.md` / AI profile JSON / SKILL.md / Agent `.md`）と配置先を確認する。
2. **Template Selection**: ファイル種別に応じたテンプレートを適用する。
   - Markdown: 見出し階層、FrontMatter（該当時）、検証項目セクション
   - Rule (.mdc/.md): frontmatter（name, description）、trigger keywords、examples
   - SKILL.md: frontmatter + When to use + When NOT to use + Trigger Keywords + Examples + 4-Section Body
   - Agent: Description + Tools + 4-Section Body
3. **Placeholder Fill**: テンプレートのプレースホルダーを具体的な内容で埋める。プロジェクト固有のコマンド（`npm run format:check` 等）を挿入する。
4. **Write**: Write ツールでファイルを生成する。
5. **Validate**: 生成ファイルに対し `npm run lint:md`（Markdown の場合）または該当する検証コマンドを実行し、構文を確認する。

## 2. Checklist

### Pre-flight

- [ ] ファイル種別と配置先パスが確定している
- [ ] 既存の類似ファイルのスタイルを確認済み
- [ ] 必要な FrontMatter フィールドを把握済み（該当時）

### Post-flight

- [ ] 生成ファイルがテンプレート構造に準拠している
- [ ] プレースホルダーが全て具体的内容に置換されている
- [ ] `npm run lint:md` が exit 0（Markdown の場合）
- [ ] 内部参照（`@` 参照、相対パス）が実在ファイルを指している

## 3. Output Format

```markdown
## content-scaffold Report

**Action**: CREATE
**Target**: <file path>
**Type**: Markdown | Rule (.mdc) | Rule (.md) | SKILL.md | Agent | JSON

### Generated Structure

- FrontMatter: <fields list>
- Sections: <section names>
- Validation commands: <applicable commands>

### Verification

| Check         | Command                | Result        |
| ------------- | ---------------------- | ------------- |
| Markdown Lint | `npm run lint:md`      | PASS          |
| Schema        | `npm run schema:check` | PASS (or N/A) |

### Next Steps

- Recommend `doc-validator` review on: <file path>
- Register in router: <router file path> (if Skill/Agent)
```

## 4. Memory Strategy

- **Persist**: ファイル種別ごとのテンプレート構造とプロジェクト固有のコマンドリストをキャッシュし、次回の生成を高速化する。
- **Invalidate**: テンプレート構造の規約（AGENTS.md の 4-Section Architecture 定義、SKILL.md の構造要件）が変更された場合にキャッシュを無効化する。
- **Share**: 生成したファイルパスを `doc-validator` Agent に提供し、品質検証の入力とする。Skill/Agent 生成時は `repo-cartographer` にパスを提供し、ルーター登録漏れの検出に活用する。
