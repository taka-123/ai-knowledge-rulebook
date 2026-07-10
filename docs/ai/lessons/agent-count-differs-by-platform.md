Claude agent は 11 件、Cursor / Codex agent は各 9 件で、2 件は Claude 専用である。

## なぜ重要か

cross-platform 整合を前提に Cursor / Codex 側へ同じ agent を追加・参照すると、存在しない agent への参照や誤った同期期待が起きる。`codebase-explorer` と `tech-researcher` は `.codex/agents/` に無い。

## 何で確認したか

- 本セッション: `ls .claude/agents/*.md | wc -l` → 11
- 本セッション: `ls .cursor/agents/*.md | wc -l` → 9
- 本セッション: `ls .codex/agents/*.toml | wc -l` → 9
- `grep codebase-explorer .codex` → マッチなし

## いつ見直すか

- `.claude/agents/` に追加・削除したとき
- cross-platform-agent-sync スキル適用時
