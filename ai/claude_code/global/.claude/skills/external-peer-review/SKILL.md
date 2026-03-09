---
name: external-peer-review
description: "Use when the user explicitly asks to run a structured peer review or discussion using an external CLI tool (Gemini or Codex); When NOT to use: when Claude can perform the review directly without external perspective; Trigger Keywords: [discuss-with-gemini, discuss-with-codex, peer review, external review, second opinion]."
allowed-tools: Bash(gemini*), Bash(codex*), Bash(git *), Bash(bash -lc*), Bash(mkdir -p*), Bash(tee*), Bash(cat*), Bash(rm /tmp/*)
---

# external-peer-review

Structured multi-round peer review using external CLI tools (Gemini or Codex). Collects repository context automatically, runs external analysis, and synthesizes an action plan.

## When to use

- 現在の変更に外部視点からのレビューが欲しいとき。
- アーキテクチャ・パフォーマンス・セキュリティなど多角的な議論をしたいとき。
- `/discuss-with-gemini` または `/discuss-with-codex` を呼ばれたとき。

## When NOT to use

- Claude 単独でレビューが完結するとき。
- 外部 CLI がインストールされていない環境のとき。
- 機密情報を含む変更で外部 AI への共有が不適切なとき。

## Trigger Keywords

- discuss-with-gemini
- discuss-with-codex
- peer review
- external review
- second opinion

## Prerequisites

- **Gemini**: `gemini` CLI がインストール済み、`gcloud auth application-default login` で認証完了。
- **Codex**: `codex` CLI がインストール済み、`codex login` で認証完了。
- 外部サービスに渡して問題のない情報のみを含めること。

## Procedure

### 1. Reset Temporary Files

```bash
rm -f /tmp/{gemini,codex}_discussion_*.md /tmp/{gemini,codex}_context.md /tmp/{gemini,codex}_discussion_brief.md
```

### 2. Collect Repository Context

```bash
bash -lc '{
  echo "# Working Tree Status";
  git status --short || true;
  echo;
  echo "# Diffstat (staged)";
  git diff --stat --cached || true;
  echo;
  echo "# Diffstat (unstaged)";
  git diff --stat || true;
  echo;
  echo "# Recent Commits";
  git log --oneline -10 || true;
} > /tmp/${TOOL}_context.md'
```

`${TOOL}` は `gemini` または `codex`。

### 3. Build Discussion Brief

```bash
cat <<'EOF' >/tmp/${TOOL}_discussion_brief.md
# Repository Context (auto-collected)
EOF
cat /tmp/${TOOL}_context.md >> /tmp/${TOOL}_discussion_brief.md
cat <<'EOF' >>/tmp/${TOOL}_discussion_brief.md

# Discussion Goals
- Architecture / design implications
- Performance and scalability considerations
- Maintainability / code quality
- Security / privacy / compliance risks
- Testing and validation gaps

# Specific Questions
$ARGUMENTS
EOF
```

### 4. Run Analysis

| Tool   | Command                                                                                              |
| ------ | ---------------------------------------------------------------------------------------------------- |
| Gemini | `gemini -p "$(cat /tmp/gemini_discussion_brief.md)" -o text \| tee /tmp/gemini_discussion_round1.md` |
| Codex  | `codex exec "$(cat /tmp/codex_discussion_brief.md)" \| tee /tmp/codex_discussion_round1.md`          |

### 5. Iterative Follow-ups (optional)

追加論点がある場合、brief に追記して再実行。各ラウンドを `/tmp/${TOOL}_discussion_roundN.md` として保存。

### 6. Synthesize Action Plan

```bash
mkdir -p .claude/discussion_logs
cat <<'EOF' > .claude/discussion_logs/${TOOL}_discussion_$(date +%Y%m%d_%H%M%S).md
# ${TOOL} Discussion Summary

## Key Findings
- ...

## Action Items
- High: ...
- Medium: ...
- Low: ...

## Follow-up Checks
- Tests to run: ...
- Additional stakeholders to consult: ...
EOF
```

### 7. Cleanup (optional)

`/tmp/${TOOL}_discussion_*` を確認し、不要なら削除。

## Tool Selection

- **デフォルト**: Gemini（高速、コスト効率が良い）
- **精密分析**: Codex（構造化出力、深い分析向き）
- **指定なし**: ユーザーに確認するか、タスク特性で自動選択

## Output Contract

| Item         | Format                     |
| ------------ | -------------------------- |
| Tool Used    | `Gemini / Codex`           |
| Rounds       | 実行ラウンド数             |
| Key Findings | 箇条書き                   |
| Action Items | High / Medium / Low        |
| Log Path     | `.claude/discussion_logs/` |

### NG例

- 外部出力を検証なしにそのまま採用する（一次情報で再確認が必要）。
- 機密情報を brief に含める（セキュリティ違反）。
- ラウンド結果を保存せずに破棄する（検討過程の喪失）。

## Examples

### Example 1

Input: `/external-peer-review API rate limiting redesign`
Output: Gemini でリポジトリコンテキスト付きレビュー実行、アクションプラン生成。

### Example 2

Input: `/external-peer-review --codex セキュリティ観点でこの変更を評価して`
Output: Codex で精密分析、セキュリティリスクと対策を整理。

### Example 3

Input: `/external-peer-review --deep Performance bottlenecks in batch jobs`
Output: 複数ラウンドで継続的に検討、ラウンド間の知見蓄積。
