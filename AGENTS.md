# プロジェクト固有ガイドライン

## 1. 基本動作原則

- **指示理解**: ユーザー指示を精読し、範囲・制約・依存関係を確認する。不明点は即質問。
- **タスク分析**: 下記テンプレで目的から品質基準までを整理し、共有する。

```markdown
## タスク分析

- 目的: [最終目標]
- 技術要件: [利用技術・制約]
- 実装手順: [主要ステップ]
- リスク: [想定課題]
- 品質基準: [満たすべき指標]
```

- **プロセス選択**: タスク規模と影響から 🟢 / 🟡 / 🔴 を判定し、該当プロセスと報告テンプレを宣言する（`main` ブランチ保護下で PR 評価が必須）。
- **計画と実装**: 変更は最小単位で進め、既存スタイルと安全性を優先。進捗・判断をこまめに共有する。
- **確認要否の明示**: 承認や回答を待つときは応答の末尾に `【確認待ち】` セクションを置き、求めるアクションを 1 行で示す（例: `- 実装に進めてよいか確認をお願いします(y/n)`）。ユーザーから明示的に指示がある場合はそれに従う。

## 2. 実務フロー

- **初期分析**: 既存ドキュメント構造、参照整合性、命名規則を把握
- **実装**: 既存スタイル・フォーマットを踏襲し、変更範囲を最小化
- **検証**: Lint・Schema 検証・リンク確認を実施し、結果を共有（`npm run format:check` / `npm run schema:check` / `markdownlint-cli2` 実行ログを記載）
- **最終確認**: 要件、品質、ドキュメント、ロールバック手段を最終チェック（CI `ci` ワークフロー完走とレビュー承認を確認）

### 実装チェックリスト

```markdown
1. [Structure] ディレクトリ構成とファイル配置確認
2. [Content] Markdown/JSON/YAML の構文と内容検証
3. [Schema] JSON Schema 適合性確認
4. [Links] 内部参照の整合性確認
5. [Quality] Lint・Prettier 実行と CI パス確認
```

## 3. 品質・リスク管理

### テスト適用範囲

- 🟢 軽量: 構文・基本動作チェック（単一ファイル更新時は `npm run format:check` で Prettier / Markdownlint 結果を確認）
- 🟡 標準: ドキュメント内容・参照整合性・Schema 適合性の確認（`npm run schema:check` で `ai/`・`notes/` JSON を検証）
- 🔴 重要: 影響範囲分析・CI/CD 統合・セキュリティ検証（CI `ci` ワークフローの Gitleaks 含む全ジョブを想定）

### 運用チェックポイント

- 既存スタイル・フォーマット・命名規則を最優先
- 変更は小さく段階的に。ロールバック手段を維持
- API キーや個人情報等の機密は `.env.sample` 等で雛形のみ共有し、実ファイルはコミット禁止
- 追加依存（npm パッケージ）は最小限。不要になった依存は削除を検討
- Markdown/JSON/YAML は Prettier・Lint ルールに準拠
- `format.sh` スクリプトで整形・検証を行い、CI `ci` ワークフロー（Markdownlint / Yamllint / JSON Schema / Gitleaks）と整合させる
- 実ファイルに作業用コメントは残さない

### 禁止事項

- Markdown/JSON/YAML 構文エラーの放置
- 機密情報（API キー、個人情報）のコミット
- リンク切れ・参照不整合の放置

## 4. 報告とコンテキスト管理

### 軽量タスク報告

```markdown
**完了**: [対象] [タスク名] - 結果: [1 行要約]
```

### 標準タスク報告

```markdown
## 実行結果（対象機能）

**対象ファイル**: [変更したファイル一覧]
**変更内容**: [追加・修正・削除の概要]
**品質確認**: [Lint・Schema 検証結果]
**注意点**: [既知の制約・今後の対応]
```

### 重要タスク報告

```markdown
# 実行結果詳細

## 概要

[全体要約]

## 技術スタック影響

- ドキュメント構造: [影響]
- Lint・Schema 設定: [影響]

## 変更詳細

1. 構造変更: [ディレクトリ・ファイル配置]
2. 内容変更: [Markdown/JSON/YAML 更新]
3. 参照整合性: [リンク・参照の調整]
4. 品質保証: [Lint・Schema 検証結果]

## 影響範囲分析

- 既存ドキュメントへの影響: [確認結果]
- CI/CD への影響: [確認結果]
- AI プロファイルへの影響: [確認結果]

## 今後の保守注意事項

- [構造変更時の注意]
- [スキーマ変更時の影響]
```

### 進捗アップデート（任意）

```markdown
**進行中**: [✅✅⏳⬜⬜] 2/5 完了 - 現在: [タスク名]
**更新**: [✅✅✅⏳⬜] 3/5 完了 - 新規: [着手内容]
```

### 長時間タスク管理（推奨）

```markdown
## 30 分毎の進捗確認

- 完了項目: [リスト]
- 進行中: [現在の作業]
- 残り項目: [リスト]
- 予想残り時間: [X 分]
```

### 中断・再開サポート（必要時）

```markdown
## 中断ポイント記録

**完了**: ステップ 1-3
**進行中**: ステップ 4（60% 完了 - [詳細]）
**未着手**: ステップ 5-7
**環境状態**: [ブランチ名] / 依存関係: [状況]
**再開手順**: `git checkout [branch] && npm install` または `./format.sh check`
```

## 5. 今後の利用に向けたメモ

- 変更履歴を明確にし、承認プロセスを整備する
- 技術スタックや外部ツール（Lint/Schema 検証ツール等）の仕様変更時は、必要な承認とドキュメント更新を行う

## タスク分類・スラッシュコマンド補足

- **タスク分類**: タスクの種別（🟢 軽量 / 🟡 標準 / 🔴 重要）は、上位階層のルール（グローバルルールや親ディレクトリの `AGENTS.md`）で定義された方針を前提とし、このプロジェクト固有の例外や補足がある場合のみ本ファイルに明記する。
- **スラッシュコマンド**: スラッシュコマンド（例: `/review`, `/plan` 等）は、このプロジェクトで明示的に定義されたものだけを使用し、定義が見当たらないコマンド文字列は通常のテキストとして扱うか、ユーザーに意味を確認する。

## プロジェクト共通 Skill / Agent 一覧

Canonical Source: `.claude/skills/<name>/SKILL.md`

各ツール固有のルーティング設定は以下を参照：

- Claude Code: `CLAUDE.md` + `.claude/CLAUDE.md`
- Cursor: `.cursor/rules/*.mdc` + `.cursor/agents/*.md`
- Windsurf: `.windsurf/rules/*.md`

### Skills

| Skill                         | Category     |
| ----------------------------- | ------------ |
| `backlog-markdown-formatting` | Format       |
| `content-scaffold`            | Generator    |
| `context-compress-map`        | Context      |
| `debug-strategist`            | Debug        |
| `documentation-standards`     | Quality      |
| `docs-sync`                   | Sync         |
| `format-lint-audit`           | Quality Gate |
| `git-helper`                  | Git          |
| `lint-fix`                    | Fixer        |
| `research-protocol`           | Research     |
| `schema-guard`                | Validation   |
| `task-planner`                | Planning     |
| `ui-standardizer`             | UI/UX        |

### Agents

| Agent                    | Category | Read-only |
| ------------------------ | -------- | --------- |
| `content-writer`         | Fixer    | No        |
| `doc-validator`          | Reviewer | Yes       |
| `external-fact-guardian` | Reviewer | Yes       |
| `repo-cartographer`      | Explorer | Yes       |
| `repo-scaffolder`        | Fixer    | No        |
