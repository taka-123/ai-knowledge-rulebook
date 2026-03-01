---
description: Run a structured peer review with Codex CLI using repository snapshots and multi-round analysis
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(mkdir -p:*), Bash(rm /tmp/codex_discussion_*), Bash(bash -lc*), Bash(codex exec*), Bash(tee*), Bash(cat:*), Bash(ls /tmp*)
---

# discuss-with-codex

Leverage Codex CLI to perform a peer-style review on the current work. The command generates an auto-collected context brief, executes Codex with web search enabled, and captures iterative insights plus a final action plan.

## Prerequisites

- `codex` CLI is installed (`which codex`)
- 認証（`codex login`）および使用モデルの設定を済ませている
- Web Search を利用する場合は `codex exec --search ...` が許可されている
- 外部サービスに渡しても問題のない情報のみを含める（機密・未公開データの扱いに注意）

## Execution Steps

1. **Reset Temporary Files（任意）**

   ```bash
   !rm -f /tmp/codex_discussion_*.md /tmp/codex_context.md /tmp/codex_discussion_brief.md
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
   } > /tmp/codex_context.md'
   ```

3. **Build Discussion Brief**

   ```bash
   !cat <<'EOF' >/tmp/codex_discussion_brief.md
   # Repository Context (auto-collected)
   EOF
   !cat /tmp/codex_context.md >> /tmp/codex_discussion_brief.md
   !cat <<'EOF' >>/tmp/codex_discussion_brief.md

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

4. **Run Codex Analysis**

   ```bash
   !codex exec --search - </tmp/codex_discussion_brief.md | tee /tmp/codex_discussion_round1.md
   ```

5. **Iterative Follow-ups（必要に応じて）**
   - 追加論点がある場合は、`/tmp/codex_discussion_brief.md` に追記して再度 `codex exec` を実行
   - 各ラウンドの結果を `/tmp/codex_discussion_roundN.md` として保存し、意思決定の根拠を残す
   - モデルを切り替える場合は `codex exec -c model="gpt-5-codex"` などを追加

6. **Synthesize Action Plan**

   ```bash
   !mkdir -p .claude/discussion_logs
   !cat <<'EOF' > .claude/discussion_logs/codex_discussion_$(date +%Y%m%d_%H%M%S).md
   # Codex Discussion Summary

   ## Inputs
   - Brief: /tmp/codex_discussion_brief.md
   - Rounds: /tmp/codex_discussion_round*.md

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
   - `/tmp/codex_discussion_*` に残る情報を確認し、必要であれば削除
   - `.claude/discussion_logs/` のサマリを共有してレビュー・チケットに添付

## Usage Examples

- `/p-discuss-with-codex` – 変更全体の俯瞰
- `/p-discuss-with-codex API rate limiting redesign` – 特定トピックに焦点を当てる
- `/p-discuss-with-codex Focus on data privacy implications` – セキュリティ / プライバシー観点を強調
- `/p-discuss-with-codex --deep Investigate build-time regressions` – 複数ラウンドで継続調査

## Notes

- Codex の出力は一次情報（公式ドキュメント / リリースノート等）で再検証してから採用してください
- 長大な変更は `git diff` の対象をディレクトリ単位に絞ると分析しやすくなります
- CLI 実行が失敗する場合は、`codex exec` の権限やプロファイル設定、ネットワークポリシーを確認してください
