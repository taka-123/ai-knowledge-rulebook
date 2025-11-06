---
description: Run a structured multi-round review with Gemini CLI using current repository context
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(mkdir -p:*), Bash(rm /tmp/gemini_discussion_*), Bash(bash -lc*), Bash(gemini*), Bash(tee*), Bash(cat:*), Bash(ls /tmp*)
---

# discuss-with-gemini

Use Gemini CLI to gather an external perspective on the current work. This command assembles live repository context, crafts a discussion brief, runs one or more Gemini rounds, and captures the resulting action plan.

## Prerequisites

- `gemini` CLI is installed and available on PATH
- `gcloud auth application-default login` などで Gemini CLI 認証を完了している
- 外部 AI へ共有して問題のない情報のみを扱う（機密情報が含まれる場合は事前に除外する）

## Execution Steps

1. **Reset Temporary Files（任意）**

   ```bash
   !rm -f /tmp/gemini_discussion_*.md /tmp/gemini_context.md /tmp/gemini_discussion_brief.md
   ```

2. **Collect Repository Context**

   ```bash
   !bash -lc '{
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
   } > /tmp/gemini_context.md'
   ```

3. **Build Discussion Brief**

   ```bash
   !cat <<'EOF' >/tmp/gemini_discussion_brief.md
   # Repository Context (auto-collected)
   EOF
   !cat /tmp/gemini_context.md >> /tmp/gemini_discussion_brief.md
   !cat <<'EOF' >>/tmp/gemini_discussion_brief.md

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

4. **Run Gemini Analysis**

   ```bash
   !gemini -p < /tmp/gemini_discussion_brief.md | tee /tmp/gemini_discussion_round1.md
   ```

5. **Iterative Follow-ups（必要に応じて）**
   - 追加で深掘りしたい論点があれば、`/tmp/gemini_discussion_brief.md` の末尾に追記して再度 `gemini -p` を実行
   - 各ラウンドの出力を `/tmp/gemini_discussion_roundN.md` として保存し、検討過程を残す
   - 例:

     ```bash
     !cat <<'EOF' >>/tmp/gemini_discussion_brief.md

     ## Follow-up Focus
     深掘りしたい論点: パフォーマンス回帰
     EOF
     !gemini -p < /tmp/gemini_discussion_brief.md | tee /tmp/gemini_discussion_round2.md
     ```

6. **Synthesize Action Plan**

   ```bash
   !mkdir -p .claude/discussion_logs
   !cat <<'EOF' > .claude/discussion_logs/gemini_discussion_$(date +%Y%m%d_%H%M%S).md
   # Gemini Discussion Summary

   ## Inputs
   - Brief: /tmp/gemini_discussion_brief.md
   - Rounds: /tmp/gemini_discussion_round*.md

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

7. **Review & Cleanup（任意）**
   - `/tmp/gemini_discussion_*` に残る機密情報を必要に応じて削除
   - `.claude/discussion_logs/` のサマリをチーム内で共有、またはチケットに添付

## Usage Examples

- `/p-discuss-with-gemini` – 現在の変更全体を俯瞰
- `/p-discuss-with-gemini API rate limiting redesign` – 特定トピックを “Specific Questions” に追加
- `/p-discuss-with-gemini Focus on post-merge testing gaps` – テスト観点に絞ったレビュー
- `/p-discuss-with-gemini --deep Performance bottlenecks in batch jobs` – 複数ラウンドで継続的に検討

## Notes

- Gemini 出力に含まれる提案・URL は一次情報で再確認してから採用してください
- 大規模リポジトリの場合は対象ディレクトリを絞るなど、プロンプトの粒度を調整すると効率的です
- CLI 実行が失敗する場合は、認証状態・プロキシ設定・ネットワークポリシーを確認してください
