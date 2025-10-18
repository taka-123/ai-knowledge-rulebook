This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Note: 本ファイルは `~/.claude/CLAUDE.md` の一般原則を継承し、競合する箇所のみを上書きします。

<language>Japanese</language>

<character_code>UTF-8</character_code>

<project_overview>
@README.md 参照
</project_overview>

<development_commands>

## フォーマット・検証

```bash
# 全ファイル整形（Prettier + Markdownlint + yamllint）
./format.sh fix

# 整形チェックのみ（CI と同じ）
./format.sh check
```

## npm scripts

```bash
# Lint チェック（整形確認のみ）
npm run lint

# 自動修正
npm run fix

# 個別実行
npm run lint:md    # Markdown Lint
npm run lint:yaml  # YAML Lint
npm run lint:json  # JSON Lint
npm run fix:md     # Markdown 自動修正
npm run fix:yaml   # YAML 自動整形
npm run fix:json   # JSON 自動整形

# JSON Schema 検証（AI プロファイル・ノート）
npm run schema:check
```

</development_commands>

<architecture_core>
@directorystructure.md 参照
</architecture_core>

<technology_stack>
@technologystack.md 参照
</technology_stack>

<development_rules>

## 基本ルール

### ブランチ運用

- `main` への直 push は禁止。必ずトピックブランチで作業する。
- PR には変更意図・検証内容・影響範囲を明記する。
- レビュー 1 名以上の承認と CI 成功後にマージする。

### ファイル形式と品質

- Markdown/JSON/YAML はすべて Prettier + 各種 Lint でフォーマット統一する。
- FrontMatter (`created` / `updated` / `tags`) は `notes/` 配下で必須。
- 参照リンク・引用元・取得日を明記する（特に `clips/`）。

### セキュリティ

- API キーや個人情報は絶対にコミットしない。
- Secret scanning / Push Protection が検出した場合は即座に修正する。
- `.env` 等の機密情報には触れず、必要時は利用者に依頼する。

</development_rules>

<security_note>

- パイプ（|）、リダイレクト（>、>>、<）、コマンド置換（$()、``）を使って deny リストのコマンドを回避することを禁止します。

</security_note>
