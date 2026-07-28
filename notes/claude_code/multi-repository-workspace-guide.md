# Claude Code マルチリポジトリ運用ガイド

**最終更新**: 2025-10-21
**ステータス**: 公式仕様検証済み、実務投入可能
**対象読者**: マルチリポジトリ（モノレポ含む）環境でClaude Codeを運用する開発者・チーム

---

## 目次

1. [結論：2つの重要な質問](#結論2つの重要な質問)
2. [対処法：3パターン比較](#対処法3パターン比較)
3. [推奨構成：プロキシエージェント方式](#推奨構成プロキシエージェント方式)
4. [公式仕様の詳細](#公式仕様の詳細)
5. [サブエージェント推奨設定](#サブエージェント推奨設定)
6. [FAQ](#faq)
7. [出典一覧](#出典一覧)

---

## 結論：2つの重要な質問

### 典型的な課題

企業開発では、以下のような3層構造のマルチリポジトリ環境が一般的です：

```
親リポジトリ（docker-compose統合）/
├── sub-repos/
│   ├── company-admin-app/
│   ├── facility-admin-app/
│   ├── facility-user-app/
│   ├── external-site-frontend/
│   ├── external-site-backend/
│   └── batch/
└── docker-compose.yml
```

各リポジトリには独自の`CLAUDE.md`と`.claude/agents/*.md`が配置され、IDEで親リポジトリを開き、ワークスペースに各子リポジトリを追加して作業します。

### Q1: 親から開いた場合、子リポジトリの設定ファイルは認識されるか？

**A1: いいえ、以下の設定ファイル/ディレクトリはすべて無視されます**

| ファイル/ディレクトリ         | 根拠の強度                          | 確認日     |
| ----------------------------- | ----------------------------------- | ---------- |
| `CLAUDE.md`                   | **公式確認済み**                    | 2025-10-17 |
| `.claude/settings.json`       | **根拠強（公式仕様から推定）**      | 2025-10-17 |
| `.claude/settings.local.json` | **根拠強（公式仕様から推定）**      | 2025-10-17 |
| `.claude/agents/*.md`         | **根拠強（公式仕様から推定）**      | 2025-10-17 |
| `.claude/hooks/*`             | **根拠強（コミュニティ+構造類推）** | 2025-10-17 |
| `.claude/commands/*.md`       | 推定（詳細未確認）                  | 2025-10-17 |

#### 根拠

1. **公式仕様（CLAUDE.md）**: "Claude loads at startup"の「startup」は起動時のworking directoryを意味
2. **GitHub Issue #3146**: 「`--add-dir`で追加したディレクトリの`CLAUDE.md`は自動読み込みされない」と明記
3. **公式仕様（Settings）**: 設定ファイルは「working directoryから相対的に探す」形式
4. **公式仕様（Hooks）**: Project-level = `.claude/hooks/`、User-level = `~/.claude/hooks/` の2階層のみ
5. **構造の一貫性**: すべての`.claude/*`設定が同じ階層ルール（working directory基準）に従う設計

#### 結論

親から起動 = 親の`.claude/`配下のみ有効。子リポジトリの`.claude/`配下は単なるディレクトリとして扱われます。

### Q2: 設定ファイルの読み込み階層はどうなっているか？

**A2: 以下の階層で読み込まれます（優先度：高 → 低）**

| 優先度 | ファイル                | パス                                                                    | スコープ           |
| ------ | ----------------------- | ----------------------------------------------------------------------- | ------------------ |
| 1      | Enterprise managed      | `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS) | 企業全体           |
| 2      | CLI arguments           | `--add-dir`, `--model` 等                                               | コマンドライン     |
| 3      | Project local settings  | `.claude/settings.local.json`                                           | プロジェクト個人用 |
| 4      | Project shared settings | `.claude/settings.json`                                                 | プロジェクト共有   |
| 5      | User settings           | `~/.claude/settings.json`                                               | ユーザー全体       |

#### 統合ルール

公式仕様より：

> "Settings are **merged, with more specific settings adding to or overriding broader ones**"

**重要**: すべての`.claude/*`ファイルは「working directoryから相対的に探す」形式のため、`--add-dir`で追加した子リポジトリの設定は読み込まれません。

**出典**: [Claude Code Settings - Claude Docs](https://docs.claude.com/en/docs/claude-code/settings) (2025-10-17確認)

---

## 対処法：3パターン比較

### パターンA: 手動読み込み

**やり方**:

```bash
claude "まず ./sub-repos/facility-user-app/CLAUDE.md を読んでルールを確認してから、
       施設利用者画面の〇〇を修正してください"
```

| メリット                  | デメリット            |
| ------------------------- | --------------------- |
| ✅ 明示的で確実           | ❌ 毎回手動指示が必要 |
| ✅ シンプルで理解しやすい | ❌ 指示忘れのリスク   |

**推奨ケース**: 単発の修正、細かく制御したい場合

---

### パターンB: プロキシエージェント方式（推奨）

**やり方**: 親の`.claude/agents/`に各子リポジトリ用の専門エージェントを配置

```markdown
---
name: facility-user-specialist
description: 施設利用者画面の修正時に使用。USE PROACTIVELY when user requests changes to facility user app.
tools: Read, Edit, Write, Grep, Bash
---

あなたは施設利用者画面の修正専門エージェントです。

**作業開始前の必須手順**:

1. ./sub-repos/facility-user-app/CLAUDE.md を読み込む
2. ./sub-repos/facility-user-app/.claude/agents/ 配下の全mdファイルを確認
3. それらのルールに厳密に従って作業
```

| メリット                     | デメリット                                                           |
| ---------------------------- | -------------------------------------------------------------------- |
| ✅ 自動的にルールを認識      | ❌ 初期セットアップが必要                                            |
| ✅ チーム共有可能（Git管理） | ⚠️ グローバル CLAUDE.md で「作業開始前チェック」を定義することを推奨 |
| ✅ スケーラブル              | ❌ トークン消費が増える                                              |

**推奨ケース**: 継続的な開発、チーム全体で統一運用したい場合

---

### パターンC: 個別起動（公式推奨）

**やり方**:

```bash
cd ./sub-repos/facility-user-app
claude
```

| メリット                           | デメリット                            |
| ---------------------------------- | ------------------------------------- |
| ✅ 子の設定が確実に有効            | ❌ 複数リポジトリ横断時に面倒         |
| ✅ Git操作も正しいリポジトリで実行 | ❌ VSCode Workspaceの利便性が失われる |
| ✅ 最も公式仕様に沿った方法        | ❌ IDE統合が複雑化                    |

**推奨ケース**: 単一リポジトリに集中、Git操作の正確性を最優先

---

### 推奨アプローチ（ハイブリッド）

**B（プロキシエージェント）+ C（個別起動）の併用**

- 単一リポジトリの修正: `cd`してから起動（C）
- 横断的な修正: 親から起動、プロキシエージェントを活用（B）
- 緊急時・単発: 手動で`CLAUDE.md`を読ませる（A）

---

## 推奨構成：プロキシエージェント方式

### ディレクトリ構造

```
親リポジトリ/
├── CLAUDE.md .......................... (1) マスタールール
├── .claude/
│   ├── settings.json .................. (2) 共通権限設定
│   └── agents/
│       ├── facility-user-specialist.md
│       ├── facility-admin-specialist.md
│       ├── external-site-specialist.md
│       └── batch-specialist.md
└── sub-repos/
    ├── facility-user-app/
    │   ├── CLAUDE.md .................. (子のルール定義)
    │   └── .claude/agents/*.md ........ (子の専門エージェント)
    ├── facility-admin-app/
    │   └── (同上)
    └── (以下略)
```

---

### (1) 親の`CLAUDE.md`

````markdown
# マルチリポジトリ開発 運用ルール

## サブリポジトリ一覧

| リポジトリ名   | パス                                  | 担当エージェント            |
| -------------- | ------------------------------------- | --------------------------- |
| 施設利用者画面 | `./sub-repos/facility-user-app/`      | `facility-user-specialist`  |
| 施設管理者画面 | `./sub-repos/facility-admin-app/`     | `facility-admin-specialist` |
| 外部公開サイト | `./sub-repos/external-site-frontend/` | `external-site-specialist`  |
| バッチ処理     | `./sub-repos/batch/`                  | `batch-specialist`          |

## 🚨 サブリポジトリ修正時の必須手順

### ステップ1: 担当エージェントの起動

上記表の「担当エージェント」が自動起動します（手動指定も可能）

### ステップ2: ルール読み込み（エージェントが自動実行）

担当エージェントは以下を必ず実行：

1. 該当サブリポジトリの`CLAUDE.md`を読み込む
2. 該当サブリポジトリの`.claude/agents/*.md`を全て確認
3. それらのルールに厳密に従って作業

### ステップ3: Git操作

```bash
# ✅ 必ずサブリポジトリ内で実行
cd ./sub-repos/facility-user-app
git add .
git commit -m "..."
```
````

## 禁止事項

- サブリポジトリのルールを確認せずに修正すること
- 親リポジトリの`.git/`で子リポジトリのコミットを実行すること

````

---

### (2) 親の`.claude/settings.json`

```json
{
  "permissions": {
    "allow": [
      "Read(**/*)",
      "Grep(**/*)",
      "Bash(git status:*)",
      "Bash(git diff:*)"
    ],
    "ask": [
      "Edit(**/*)",
      "Bash(git commit:*)",
      "Bash(git push:*)"
    ],
    "deny": [
      "Read(.env)",
      "Read(.env.*)",
      "Bash(rm:-rf:*)",
      "Bash(sudo:*)"
    ]
  }
}
````

**ポイント**:

- `Read`は全許可（子リポジトリの`CLAUDE.md`読み込みに必須）
- `Edit`は`ask`（誤操作防止。書き込み系は `Edit(path)` に統合済み）
- `.env`系は完全拒否

---

### (3) 親の`.claude/agents/facility-user-specialist.md`

````markdown
---
name: facility-user-specialist
description: 施設利用者画面（./sub-repos/facility-user-app/）の修正時に必ず使用。USE PROACTIVELY when user requests changes to facility user app.
tools: Read, Edit, Write, Grep, Bash
model: inherit
---

あなたは施設利用者画面（`./sub-repos/facility-user-app/`）の修正専門エージェントです。

## 作業開始前の必須手順

**🚨 グローバル CLAUDE.md の「作業開始前チェック」に従い、以下を必ず実行**：

1. **サブリポジトリのルール確認**
   - ./sub-repos/facility-user-app/CLAUDE.md を読み込む
   - ./sub-repos/facility-user-app/.claude/agents/ 配下の全mdファイルを確認

2. **ルールの厳密遵守**
   - 子リポジトリの`CLAUDE.md`に記載されたコーディング規約に従う
   - 子リポジトリの`.claude/agents/`で定義された専門エージェントのルールを尊重

3. **Git操作の注意**
   ```bash
   # 必ず子リポジトリ内で実行
   cd ./sub-repos/facility-user-app
   git status
   git add .
   git commit -m "..."
   ```
````

## 制約事項

- 子リポジトリの`CLAUDE.md`を読まずに修正を開始すること
- 親リポジトリの`.git/`でコミットすること

## 報告形式

作業完了時、以下を必ず報告：

- ✅ 読み込んだルールファイル一覧
- ✅ 遵守したコーディング規約
- ✅ 実行したGitコマンド（どのディレクトリで実行したか含む）

````

**出典**:

- [Subagents - Claude Docs](https://docs.claude.com/en/docs/claude-code/sub-agents)
- コミュニティベストプラクティス（"USE PROACTIVELY"キーワード）

---

### 実践例

#### ケース1: 施設利用者画面の修正依頼

**ユーザーの指示**:

```text
施設利用者画面のログインフォームに「パスワード再設定」リンクを追加して
````

**Claude Codeの動作**（自動）:

1. `description`に「facility user app」が含まれる → `facility-user-specialist`が自動起動
2. エージェントが`./sub-repos/facility-user-app/CLAUDE.md`を読み込む
3. エージェントが`./sub-repos/facility-user-app/.claude/agents/*.md`を確認
4. 子リポジトリのルールに従って修正
5. `cd ./sub-repos/facility-user-app`してGit操作

---

### ケース2: 横断的な修正依頼

**ユーザーの指示**:

```text
全サブリポジトリの.gitignoreに「*.log」を追加して
```

**推奨アプローチ**:

```text
各サブリポジトリの担当エージェントを順番に呼び出して、
それぞれのルールに従って.gitignoreを更新して
```

これにより、Claude Codeが各プロキシエージェントを順番に起動し、個別のルールに従って処理します。

---

## 公式仕様の詳細

### 1. `CLAUDE.md`の読み込みルール

#### 公式仕様（2025-10-17確認）

[Claude Code Settings - Claude Docs](https://docs.claude.com/en/docs/claude-code/settings)より：

> "Memory files (CLAUDE.md) contain instructions and context that **Claude loads at startup**."

**重要**: Claude Codeは起動時のworking directoryにある`CLAUDE.md`のみを自動読み込み

#### `--add-dir`使用時の制限

[GitHub Issue #3146 - Configure Additional Directories](https://github.com/anthropics/claude-code/issues/3146)より：

> "CLAUDE.md files are **not automatically read from directories added via `--add-dir`**, which can be confusing"

**重要**: `--add-dir`で追加したディレクトリの`CLAUDE.md`は自動読み込みされない

#### Web検索結果（複数ソース一致、2025-10-17確認）

> "The primary CLAUDE.md file that gets loaded is the one in your **current working directory** where you launch Claude Code."

**出典**:

- [ClaudeLog - Working Directory FAQ](https://claudelog.com/faqs/what-is-working-directory-in-claude-code/)
- [Anthropic - Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

---

### 2. `.claude/agents/`の読み込みルール

#### エージェント配置場所の仕様（2025-10-17確認）

[Subagents - Claude Docs](https://docs.claude.com/en/docs/claude-code/sub-agents)より：

| 場所          | パス                | スコープ           | 優先度 |
| ------------- | ------------------- | ------------------ | ------ |
| Project-level | `.claude/agents/`   | 現在のプロジェクト | 最高   |
| User-level    | `~/.claude/agents/` | 全プロジェクト共通 | 低     |

優先順位：

> "When subagent names conflict, **project-level subagents take precedence** over user-level subagents."

**重要**: この「Project-level」は起動したworking directoryの`.claude/agents/`を指す

---

### 3. Settings.jsonの優先順位

[Claude Code Settings - Claude Docs](https://docs.claude.com/en/docs/claude-code/settings)より：

設定ファイルの読み込み順序（高 → 低）：

1. Enterprise managed policies (`managed-settings.json`)
2. Command line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

統合ルール：

> "Settings are **merged, with more specific settings adding to or overriding broader ones**"

**重要**: すべて「working directoryから相対的に探す」形式

#### 補足：`.claude/`配下のその他のファイル

以下のファイル/ディレクトリも同様にworking directory基準で読み込まれます：

| 項目     | パス                    | 用途                                          |
| -------- | ----------------------- | --------------------------------------------- |
| Hooks    | `.claude/hooks/*`       | フックスクリプト（PreToolUse, PostToolUse等） |
| Commands | `.claude/commands/*.md` | カスタムコマンド定義                          |

**出典**:

- [Get started with Claude Code hooks - Claude Docs](https://docs.claude.com/en/docs/claude-code/hooks-guide) (2025-10-17確認)
- コミュニティソース: Project-level = `.claude/hooks/`、User-level = `~/.claude/hooks/` の2階層構造

---

## サブエージェント推奨設定

### コミュニティで賞賛されている定番5エージェント

| エージェント     | 目的                             | 推奨理由                 |
| ---------------- | -------------------------------- | ------------------------ |
| code-reviewer    | コード品質・セキュリティレビュー | 自動レビューで品質向上   |
| debugger         | エラー解析・根本原因特定         | 問題解決の専門家         |
| test-runner      | テスト実行・失敗修正             | TDD推進・回帰防止        |
| spec-agent       | 最新仕様調査・技術選定           | 公式ドキュメント準拠確認 |
| security-auditor | 脆弱性監査                       | OWASP準拠チェック        |

**出典**:

- [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) (100+エージェント集)
- [eesel.ai - 7 powerful Claude Code subagents](https://www.eesel.ai/blog/claude-code-subagents) (2025年版推奨)

---

### 段階的導入アプローチ

**Phase 1（導入直後）**:

- code-reviewer
- debugger

**Phase 2（慣れてきたら）**:

- test-runner
- spec-agent

**Phase 3（プロジェクト特化）**:

- 言語特化エージェント（typescript-pro等）
- セキュリティ系（必要に応じて）

---

### 注意点

#### コスト面

- **20kトークンの固定オーバーヘッド**: サブエージェント1回の起動で最低20kトークン消費
- 例: 「LGTM」と返すだけでも20kトークンかかる

**出典**: [PubNub - Best practices for Claude Code subagents](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/)

#### ベストプラクティス

> **「単一責任の原則」**: 1エージェント = 1明確な役割
>
> **「Start small」**: 最初は2-3個から始め、必要に応じて追加

---

### 判断基準

- **✅ 入れるべき**: 週1回以上手動で同じ指示を出しているタスク
- **❌ 不要**: 「便利そう」だけで使用頻度が想像できないもの

---

## FAQ

### Q1: なぜ子リポジトリのCLAUDE.mdが無視されるのか？

**A**: Claude Codeの設計思想として、起動時のworking directoryを「プロジェクトのルート」とみなすためです。

**理由**:

1. **シンプルさ**: 複数のCLAUDE.mdを自動統合すると、競合・優先順位の管理が複雑化
2. **予測可能性**: 起動場所でルールが確定するため、動作が明確
3. **パフォーマンス**: 大量のディレクトリを探索する必要がない

**将来的な改善**: GitHub Issue #3146で改善が提案されています。

---

### Q2: シンボリックリンクを使う方法は有効か？

**A**: 技術的には可能ですが、推奨しません。

**方法例**:

```bash
# 親の .claude/agents/ から子のエージェントをリンク
ln -s ../../sub-repos/facility-user-app/.claude/agents/facility-user-specialist.md \
      .claude/agents/facility-user-specialist.md
```

**デメリット**:

- エージェント名の衝突リスク
- リンク管理が煩雑
- OS依存の互換性問題

**推奨代替案**: プロキシエージェント方式（本ガイド推奨）

---

### Q3: 将来的に改善される見込みは？

**A**: GitHub Issue #3146で以下の機能がリクエストされています（2025-10-17時点で未実装）。

**提案されている理想形**:

```json
{
  "additionalDirectories": [
    {
      "path": "./sub-repos/facility-user-app",
      "readClaudeMd": true,
      "loadAgents": true
    }
  ]
}
```

**現在のステータス**: Feature Request段階、実装時期は未定

**出典**: [GitHub Issue #3146](https://github.com/anthropics/claude-code/issues/3146)

---

### Q4: 横断的な修正はどうすればいいか？

**A**: 以下の2つのアプローチがあります。

#### アプローチ1: メインエージェントで一括処理

```bash
# ユーザーの指示
全サブリポジトリの package.json に "node": ">=20" を追加して
```

メインエージェント（親のルール）が各リポジトリを順番に処理します。

#### アプローチ2: 各担当エージェントを順番に呼び出し

```bash
# ユーザーの指示
各サブリポジトリの担当エージェントを使って、
それぞれのルールに従って package.json を更新して
```

Claude Codeが各プロキシエージェントを順番に起動し、個別のルールに従って処理します。

**推奨**: 横断的な修正でも、できるだけアプローチ2を使用（各リポジトリのルール遵守）

---

## 出典一覧

### 公式ドキュメント

| 項目           | URL                                                                                                                                  | 確認日     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| Settings公式   | [https://docs.claude.com/en/docs/claude-code/settings](https://docs.claude.com/en/docs/claude-code/settings)                         | 2025-10-17 |
| Subagents公式  | [https://docs.claude.com/en/docs/claude-code/sub-agents](https://docs.claude.com/en/docs/claude-code/sub-agents)                     | 2025-10-17 |
| Hooks公式      | [https://docs.claude.com/en/docs/claude-code/hooks-guide](https://docs.claude.com/en/docs/claude-code/hooks-guide)                   | 2025-10-17 |
| Best Practices | [https://www.anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices) | 2025-10-17 |

### GitHub Issues

| 項目        | URL                                                                                                            | 確認日     |
| ----------- | -------------------------------------------------------------------------------------------------------------- | ---------- |
| Issue #3146 | [https://github.com/anthropics/claude-code/issues/3146](https://github.com/anthropics/claude-code/issues/3146) | 2025-10-17 |

### コミュニティリソース

| 項目                  | URL                                                                                                                                              | 確認日     |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| VoltAgent Collection  | [https://github.com/VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)                         | 2025-10-17 |
| eesel.ai Guide        | [https://www.eesel.ai/blog/claude-code-subagents](https://www.eesel.ai/blog/claude-code-subagents)                                               | 2025-10-17 |
| PubNub Best Practices | [https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/](https://www.pubnub.com/blog/best-practices-for-claude-code-sub-agents/) | 2025-10-17 |
| ClaudeLog FAQ         | [https://claudelog.com/faqs/what-is-working-directory-in-claude-code/](https://claudelog.com/faqs/what-is-working-directory-in-claude-code/)     | 2025-10-17 |

---

## 更新履歴

- **2025-10-17**: 初版作成（公式仕様検証済み）
- **2025-10-17**: 全設定ファイル一覧を追加（`.claude/settings.json`, `.claude/hooks/`, `.claude/commands/`の読み込みルール明記）
- **2025-10-21**: 実証済みベストプラクティスを追加（グローバル CLAUDE.md の `<every_chat>` セクションに「作業開始前チェック」を配置することで、サブリポジトリの CLAUDE.md 読み込みを確実に実行できることを検証）

---

_このガイドは2025年10月21日時点の公式情報と実証済みベストプラクティスに基づいています。Claude Codeは継続的に進化しているため、最新情報は必ず公式ドキュメントを参照してください。_
