# Claude Code プロジェクトテンプレート

新規プロジェクトに Claude Code を導入する際のテンプレート。
グローバル設定（`ai/claude_code/global/`）と組み合わせて使う。

---

## 前提: グローバル設定の適用（一度だけ）

```bash
cp -r ai/claude_code/global/.claude/ ~/.claude/
```

`~/.claude/` に配置されたエージェント・スキル・フックは **CLI 専用**（Web 版 claude.ai では読み込まれない）。
Web 版でも使いたいエージェント・スキルは、後述のプロジェクト `.claude/` に配置する。

---

## プロジェクトへの適用

```bash
cp -r ai/claude_code/project/.claude/ /path/to/your-project/.claude/
cp ai/claude_code/project/CLAUDE.md   /path/to/your-project/CLAUDE.md
```

`.claude/` 一箇所をコピーするだけで完結する。

---

## `.claude/` の構成

```
.claude/
├── settings.json                   # 権限設定 + フック定義
├── hooks/
│   └── suggest-claude-md-hook.sh  # CLAUDE.md 自動提案フック
├── agents/                         # プロジェクト固有エージェント（後から追加）
└── skills/                         # プロジェクト固有スキル（後から追加）
```

### settings.json の主な設定

| 設定                             | 内容                                              |
| -------------------------------- | ------------------------------------------------- |
| `defaultMode: bypassPermissions` | Claude が都度確認なしに作業できる                 |
| `deny`                           | .env / secrets / pem / sudo / force push 等を禁止 |
| `ask`                            | git checkout / merge / DB 操作は確認を求める      |
| `allow`                          | node / npm / python / make 等を許可               |
| `SessionEnd` フック              | セッション終了時に CLAUDE.md 更新を提案           |
| `PreCompact` フック              | コンテキスト圧縮前に CLAUDE.md 更新を提案         |

---

## CLAUDE.md 自動提案フック

セッション終了時・コンテキスト圧縮前に会話履歴を自動分析し、`CLAUDE.md` への追記候補を新しいターミナルウィンドウで提示する。

### 検出する 3 パターン

1. **プロジェクト固有ルール** — 「A ではなく B を使ってください」が出現
2. **繰り返し修正指示** — 同種の修正が 2 回以上出現
3. **クロス整合性** — 複数箇所で統一を求める指示

### 手動実行

```
/suggest-claude-md
```

### ログ確認

```bash
cat /tmp/suggest-claude-md-{会話ID}-{タイムスタンプ}.log
```

### ワークフロー

1. Claude Code で開発作業
2. セッション終了 or コンテキスト圧縮時に自動分析
3. 新しいターミナルウィンドウに提案が表示される
4. 良いと思ったら「この内容を CLAUDE.md に追記して」と指示
5. コード変更と同じ PR に含めてレビュー

---

## プロジェクト固有のエージェント・スキルを追加する

グローバルの汎用エージェント・スキルだけでは補えない、プロジェクト固有の自動化を追加する場合は
`snippets/skill-agent-creator/` のプロンプトを順番に実行する。

### project/ （単一リポジトリ）

```
1. snippets/skill-agent-creator/project/1_scan.md       → プロジェクト分析・ギャップ特定
2. snippets/skill-agent-creator/project/2_blueprint.md  → 追加するエージェント/スキルを設計
3. snippets/skill-agent-creator/project/3_implement.md  → .claude/agents/, .claude/skills/ に生成
```

### multi_service_parent/ （複数リポジトリを束ねる親ディレクトリ）

```
1. snippets/skill-agent-creator/multi_service_parent/1_scan.md      → 横断分析
2. snippets/skill-agent-creator/multi_service_parent/2_implement.md → 横断エージェント/スキルを生成
```

### 生成されるもの

- `.claude/agents/*.md` — プロジェクトの作業フローに特化したエージェント
- `.claude/skills/*/SKILL.md` — プロジェクト固有コマンド・パスに対応したスキル
- `.work/AI_SCAN.md` / `.work/AI_BLUEPRINT.md` — 分析・設計の中間成果物

---

## グローバルで使えるエージェント・スキル（参考）

`~/.claude/` に配置される汎用資産。どのプロジェクトでも CLI から使用可能。

### エージェント（6個）

| 名前                | 役割                                       |
| ------------------- | ------------------------------------------ |
| `code-reviewer`     | コード差分の正しさ・安全性・保守性レビュー |
| `codebase-explorer` | コードベースの構造探索・地図作成           |
| `security-reviewer` | 脅威モデルに基づくセキュリティ監査         |
| `task-reviewer`     | タスク完了の品質・安全性・完遂確認         |
| `tech-researcher`   | 公式ドキュメント・一次情報に基づく技術調査 |
| `test-runner`       | テスト実行・失敗原因切り分け・最小修正     |

### スキル（12個）

| 名前                          | 役割                                               |
| ----------------------------- | -------------------------------------------------- |
| `agent-factory`               | 新しいエージェント/スキルの設計・生成              |
| `backlog-issue-planner`       | Backlog チケット起票（要件・実装計画・ブランチ名） |
| `backlog-markdown-formatting` | Backlog 向け Markdown 整形                         |
| `chatwork-formatter`          | ChatWork 向け Markdown 変換                        |
| `debug-strategist`            | 仮説駆動デバッグ                                   |
| `decide-tool`                 | Gemini/Cursor/Codex への外部委任判断               |
| `external-peer-review`        | Gemini/Codex を使った外部視点レビュー              |
| `git-helper`                  | コミット整理・ブランチ・PR 操作                    |
| `lint-fix`                    | lint/format 違反の最小差分修正                     |
| `skill-discoverer`            | 利用可能なエージェント/スキルの動的探索            |
| `task-planner`                | 実装を段階的に分解・計画                           |
| `ui-standardizer`             | UI/CSS の視覚規約・アクセシビリティ確認            |
