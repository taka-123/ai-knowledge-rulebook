# AI_OPERATING_GUIDE

モデル非依存の作業ルール。特定 AI の人格設定は含まない。

最終確認: 2026-07-07

## 作業開始時に読む順序

1. `docs/ai/PROJECT_REALITY_MAP.md` — 実態・境界・危険領域
2. `AGENTS.md`（Codex / Cursor 系）または `CLAUDE.md`（Claude Code）— 編集境界とハード制約
3. 依頼内容に応じた README:
   - テンプレート編集 → `ai/README.md`
   - 同期・配布 → `scripts/README.md`
   - 全体概要 → `README.md`
4. 変更対象の既存ファイルを **Read で実読** してから着手
5. 落とし穴は `docs/ai/lessons/` を確認

## 標準フロー（調査 → 計画 → 実装 → 検証 → 報告）

### 1. 調査

- README だけでなく `package.json`、対象ディレクトリ、検証スクリプトを確認する
- 編集対象が A / B / C のどれかを先に判定する（`PROJECT_REALITY_MAP.md` 参照）
- 横断 grep や大規模探索は subagent に委任し、結果を要約して取り込む

### 2. 計画

非自明な変更では短く整理する:

1. Goal — 何を変えるか
2. Scope — 触るファイル
3. Constraints — 互換性・検証・セキュリティ
4. Done when — 通る検証コマンド

### 3. 実装

- **最小差分**。依頼範囲外のリファクタ・整形・抽象化を混ぜない
- 既存パターン（Skill 構造、agent frontmatter、sync 退避規則）に合わせる
- Skill / Agent の `description` と Trigger Keywords は自動マッチに使われるため具体的に書く

### 4. 検証

変更種別に応じて **最小の `*:check` から** 実行し、必要なら広げる:

| 変更内容                        | 最低限                        | 広げる条件                                  |
| ------------------------------- | ----------------------------- | ------------------------------------------- |
| Markdown 一般                   | `npm run lint`                | 共有ルール・憲法変更                        |
| `ai/` JSON                      | `npm run schema:check`        | —                                           |
| `.claude/skills/`               | `npm run skills:check`        | description 変更時は `description:check` も |
| `ai/.../global/.claude/skills/` | `npm run global-skills:check` | —                                           |
| `.claude/agents/`               | `npm run claude-agents:check` | 色変更時は許可色セット確認                  |
| `.cursor/agents/`               | `npm run cursor-agents:check` | —                                           |
| `.codex/`                       | `npm run codex-wiring:check`  | —                                           |
| レビュールーティング            | `npm run routing:check`       | —                                           |
| 上記複数または不確実            | `npm run agent:check`         | —                                           |

**注意**: CI（`.github/workflows/ci.yml`）は `npm run check` のみ。`agent:check` はローカルで実行する。

### 5. 報告

完了報告に含めるもの:

- 変更内容と理由
- 実行した検証コマンドと **正確な結果**（失敗時は成功と報告しない）
- 未検証事項と残リスク
- 事実 / 推測 / 未確認の区別

## 実装前に確認すべき境界条件

- 編集対象は A（`ai/`）か B（ルート live 設定）か。B は **明示依頼がある場合のみ**
- C（`~/.claude/` 等）には書き込まない。反映はユーザーが sync スクリプトを実行
- 同期先契約・Agent 自動マッチ条件を変える場合は対応する `*:check` とドキュメント更新が必要
- MCP / 認証系は `--include-mcp` の扱いを理解した上でのみ触る
- グローバル配布資産（`ai/*/global/`、`ai/common/`）はツール中立を維持

## 変更してはいけない領域 / 慎重に扱う領域

| 領域                                                   | 扱い                                 | 根拠                   |
| ------------------------------------------------------ | ------------------------------------ | ---------------------- |
| `~/.claude/` 等ホーム配下（C）                         | 変更禁止（明示依頼・sync 以外）      | `AGENTS.md`            |
| 秘密情報・`.env*`                                      | 作成・コミット・出力禁止             | `CLAUDE.md` ハード制約 |
| `scripts/sync-*-to-home.sh` の退避・MCP デフォルト動作 | 破壊的変更は停止してトレードオフ提示 | `scripts/README.md`    |
| `node_modules/`、生成物                                | 直接編集しない                       | `AGENTS.md`            |
| lockfile                                               | 明示承認なしに変更しない             | `AGENTS.md`            |
| CI ワークフロー                                        | 明示依頼なしに変更しない             | プロジェクトルール     |
| git commit / push / rebase / force-push                | 明示依頼なしに実行しない             | プロジェクトルール     |

## テストが存在しない場合の確認方法

| 領域                         | 確認方法                                                                                                                                 |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| sync スクリプト              | 対象ファイルを読み、退避パターンとコピー元先を手動照合。実行はユーザー依頼時のみ                                                         |
| テンプレートのランタイム挙動 | 同期後に各 AI ツールで起動確認（人間）                                                                                                   |
| 文書の正確性                 | 実ディレクトリ・`package.json`・CI と突合                                                                                                |
| 自然言語ドキュメント品質     | `document-authoring` / AI 向け指示は `ai-instruction-authoring`（`ai/claude_code/global/.claude/skills/`、配布後は `~/.claude/skills/`） |

## AI が勝手に広げてはいけないスコープ

- 依頼外のリファクタ・一括整形・依存更新
- B / C 区分への書き込み（明示依頼なし）
- `sync-*-to-home.sh` の自律実行
- commit / PR 作成 / force-push
- 新しい検証スクリプトや抽象レイヤーの追加（依頼なし）
- 複数ツール間の agent 追加時の片方だけの更新（cross-platform 整合が必要）

## 事実と推測を区別した報告形式

```markdown
**事実**: `npm run agent:check` が exit 0（2026-07-07 実行）
**推論**: CI に agent:check が無いため、main へマージ後に配線破損が検知されない可能性
**未確認**: 次回 PR で CI が実際に agent:check なしで通過するか
```

## 未解決の知見を残す場所と更新規則

| 種別                         | 置き場                           | 規則                              |
| ---------------------------- | -------------------------------- | --------------------------------- |
| 確認済みの落とし穴・運用知見 | `docs/ai/lessons/*.md`           | 1 ファイル 1 知見。推測は書かない |
| 実態の地図                   | `docs/ai/PROJECT_REALITY_MAP.md` | 構造変更・検証変更時に更新        |
| 作業ルール                   | 本ファイル                       | フロー変更時に更新                |
| 一時的な作業メモ             | `.work/`（gitignore）            | 正本にしない                      |

誤りと分かった知見は lessons を更新または削除する。

## 人間確認が必要な操作

- `./scripts/sync-all-to-home.sh` および個別 sync（ホーム配下を上書き）
- `./scripts/sync-*-to-home.sh --include-mcp`（認証情報を含みうる）
- git commit / push / rebase / branch 削除 / PR 作成
- 依存パッケージの追加・更新・lockfile 変更
- CI ワークフロー変更
- 破壊的な sync スクリプト変更

## 外部送信・削除・課金・認証・データ更新前の確認規則

- API キー・トークン・個人情報をプロンプトやコミットに含めない
- MCP 経由の外部送信は、対象データに秘密情報が無いことを確認
- ホームディレクトリの削除・上書きは sync スクリプト経由のみとし、AI 単独で `rm` しない
- 課金が発生しうる外部 API 呼び出しはユーザー確認後
- `--include-mcp` は認証ファイルが配布先にコピーされることを理解した上でユーザーが実行

## クイックリファレンス

```bash
# セットアップ
npm install
pip install check-jsonschema yamllint

# 軽量チェック（CI と同等）
npm run check

# Agent / Skill 変更後
npm run agent:check

# ホームへ反映（ユーザーが実行）
./scripts/sync-all-to-home.sh
```
