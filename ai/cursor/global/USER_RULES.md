# Cursor Settings > Rules & Memories > User Rules

[../../common/global/AGENTS.md](../../common/global/AGENTS.md)に記載のものを添付

## Global Reasoning Protocol

1. **Search Before Thought**: 複雑な依頼を受けた際、推論を開始する前に必ず `~/.cursor/` および `./.cursor/` 内の Subagents/Skills をスキャンせよ。
2. **Preference for Experts**: 該当する専門家がいる場合、メイン窓での長い推論を避け、即座に委任（Task）せよ。
3. **JIT Loading**: タスクに関連するスキルを発見したとき、およびスキル名に言及する際は、必ず当該 `SKILL.md` をロードして最新の制約を脳内に同期せよ。
   - CSS・Tailwind・UIコンポーネントの編集・追加時は、`ui-standardizer` の SKILL.md をロードしてから作業せよ。
   - 「バックログ用のmd記法で」等の依頼時は、`backlog-markdown-formatting` の SKILL.md をロードしてから整形せよ。
