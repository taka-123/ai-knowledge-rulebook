# Codex project テンプレート

Local 向けの `.codex/`（config / rules / agents）と、Cloud でも効く方針の置き場を分ける。

| 資産                                                   | Local                   | Codex Cloud                      |
| ------------------------------------------------------ | ----------------------- | -------------------------------- |
| repo `AGENTS.md`（`ai/common/project/AGENTS.md` 由来） | 有効                    | **本線**                         |
| `.codex/config.toml`                                   | 有効（trusted project） | Cloud の安全装置としては扱わない |
| `.codex/rules/*.rules`                                 | 有効                    | 同上                             |

Cloud で AWS/GitHub 方針を効かせるなら、まず `AGENTS.md` を repo ルートに置く。
詳細: [`../EXTERNAL_SERVICES_SECURITY.md`](../EXTERNAL_SERVICES_SECURITY.md)
