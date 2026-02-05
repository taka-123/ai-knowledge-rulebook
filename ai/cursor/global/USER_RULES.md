# Cursor Settings > Rules & Memories > User Rules

[../../common/global/AGENTS.md](../../common/global/AGENTS.md)に記載のものを添付

## Global Reasoning Protocol

1. **Search Before Thought**: 複雑な依頼を受けた際、推論を開始する前に必ず `~/.cursor/` および `./.cursor/` 内の Subagents/Skills をスキャンせよ。
2. **Preference for Experts**: 該当する専門家がいる場合、メイン窓での長い推論を避け、即座に委任（Task）せよ。
3. **JIT Loading**: スキル名に言及する際は、必ず `SKILL.md` をロードして最新の制約を脳内に同期せよ。
