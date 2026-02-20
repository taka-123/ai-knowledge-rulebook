<!--
OpenAI Codex CLI グローバル設定
- WSL2（公式推奨）: ~/.codex/AGENTS.md
  - 理由: 安定性・全機能保証・Unix環境での最適化
- Windows ネイティブ（実験的サポート）: C:\Users\<YourUsername>\.codex\AGENTS.md
  - 注意: WSL2推奨。ネイティブは実験的サポートで制限あり
- Mac: ~/.codex/AGENTS.md
-->

[../../common/global/AGENTS.md](../../common/global/AGENTS.md)に記載のものを添付

---

## Codex 固有アダプタ

### 探索対象

- Skills: `~/.agents/skills/<skill>/SKILL.md` / `.agents/skills/<skill>/SKILL.md`
- Agents: `~/.codex/config.toml` / `.codex/config.toml` の `[agents]` 定義

### 運用ルール

- タスク着手前に、関連する Skills と agent role の有無を確認する。
- スキル名が明示された場合は、該当 `SKILL.md` を JIT ロードする。
