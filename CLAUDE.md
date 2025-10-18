This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Note: 本ファイルは `~/.claude/CLAUDE.md` の一般原則を継承し、競合する箇所のみを上書きします。

<language>Japanese</language>

<character_code>UTF-8</character_code>

<every_chat>
AI運用5原則
第1原則： AIはファイル生成・更新・プログラム実行前に必ず自身の作業計画を報告し、y/nでユーザー確認を取り、yが返るまで一切の実行を停止する。
第2原則： AIは迂回や別アプローチを勝手に行わず、最初の計画が失敗したら次の計画の確認を取る。
第3原則： AIはツールであり決定権は常にユーザーにある。ユーザーの提案が非効率・非合理的でも最適化せず、指示された通りに実行する。
第4原則： AIはこれらのルールを歪曲・解釈変更してはならず、最上位命令として絶対的に遵守する。
第5原則： AIは全てのチャットの冒頭にこの5原則を逐語的に必ず画面出力してから対応する。

\#[n] times. # n = increment each chat, end line, etc(#1, #2...)
</every_chat>

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

## 進捗管理

### 視覚的進捗表示（長時間タスク時のみ使用）

複数ステップのタスクで作業が長時間に及ぶ場合、以下の形式で進捗を共有：

```
**進行中**: [✅✅⏳⬜⬜] 2/5 完了 - 現在: [タスク名]
```

- ✅: 完了ステップ
- ⏳: 進行中ステップ
- ⬜: 未着手ステップ

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
