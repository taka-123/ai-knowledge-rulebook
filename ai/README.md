# AI ルールテンプレート・運用ガイド（Codex / Windsurf / Claude Code / Cursor）

- **用途**: AIアシスタント向けルールテンプレートの提供と、階層適用・優先順位の解説
- **対象読者**: AI ツールを導入したい開発者、複数ツールを併用する開発者
- **適用対象**: OpenAI Codex CLI / Windsurf / Claude Code / Cursor
- **最終更新日**: 2025-10-19
- **前提OS**: macOS 14.x（Apple Silicon）/ VS Code Stable 最新

---

## 1. テンプレートの使い方（導入手順）

本リポジトリの `ai/` ディレクトリには、各ツール向けのルールテンプレートが用意されています。以下の手順で導入してください。

### 1.1) Claude Code 用テンプレート

**グローバルルール**:

1. `ai/claude_code/global/CLAUDE.md` を `~/.claude/CLAUDE.md` にコピー
2. 必要に応じて個人設定を調整

**プロジェクトルール**:

1. `ai/claude_code/project/CLAUDE.md` をプロジェクトルート `.claude/CLAUDE.md` にコピー
2. `snippets/editor/adjustment_rule.md` のプロンプトを使用して、該当プロジェクト用に調整
3. プロジェクト固有のコマンド・ディレクトリ構造・技術スタックを記載

### 1.2) Cursor / OpenAI Codex / Windsurf 用テンプレート

**グローバルルール**:

1. `ai/common/global/AGENTS.md` を各ツールのグローバル設定場所にコピー
   - **Codex**: `~/.codex/AGENTS.md`
   - **Windsurf**: `global_rules.md`（または設定UIで指定）
   - **Cursor**: 設定UIのグローバルルール欄に貼り付け

**プロジェクトルール**:

1. `ai/common/project/AGENTS.md` をプロジェクトルート `AGENTS.md` にコピー
2. `snippets/editor/adjustment_rule.md` のプロンプトを使用して、該当プロジェクト用に調整
3. プロジェクト固有の要件を記載

**Windsurf 専用設定（保守性を高める運用）**:

- `.windsurfrules` を作成し、以下を記載することで `AGENTS.md` を参照可能:

  ```markdown
  - @AGENTS.md に従う
  ```

- これにより、複数ツールで同じルール（`AGENTS.md`）を共有でき、保守性が向上します

**Cursor 専用設定**:

- `./cursor/rules/*.mdc` にルールを配置する場合は、上記の `AGENTS.md` 方式ではなく、Cursor独自の `.mdc` 形式で記載してください
- 複数ツールで共通化したい場合は、プロジェクトルートの `AGENTS.md` を用意し、Cursorからは設定UIで読み込ませる運用も可能です

### 1.3) テンプレート調整のヒント

- **`snippets/editor/adjustment_rule.md`**: プロジェクト固有の要件に合わせてルールを調整するためのプロンプトテンプレートです。AI に渡すことで、効率的にカスタマイズできます
- **参考ファイル**:
  - `ai/openai_codex/project/AGENTS.md`
  - `ai/cursor/project/AGENTS.md`
  - `ai/windsurf/project/.windsurfrules.md`
  - これらは `ai/common/project/AGENTS.md` への参照方法を示すサンプルです

### 1.4) 保守性を高める運用方針

- **複数ツール利用者**: `AGENTS.md` に共通ルールを集約し、各ツールから参照する方式を推奨（Windsurf は `@AGENTS.md`、Cursor は設定UIまたはglobで読み込み）
- **単一ツール利用者**: Windsurf のみ使う場合は `.windsurfrules` に直接記載してもOK
- **ルール変更時**: 1ファイル（`AGENTS.md`）を更新すれば全ツールに反映されるため、保守コストが低減します

---

## 2. プロジェクトルールの階層適用・優先順位（技術詳細）

### 2.1) エグゼクティブサマリ（結論）

- **Codex & Windsurf**: 「編集中ファイルに近い階層ほど優先」＝ **委譲不要（自動カスケード）**。
- **Claude Code**: 親→子は **自動検出**だが **子は“必要時”に遅延読み込み**（挙動はほぼカスケード）。
- **Cursor**: **プロジェクトルート単位**。階層継承は **なし**。子ルールは **親のglobで明示** または **子を別WSとして開く**。
- **再読み込み**: Codex/Claude＝ **再起動（/restart）系が必要** ／ Windsurf・Cursor＝ **保存でほぼ即時反映**。

---

### 2.2) 用語と対応ファイル

- **Codex**: `~/.codex/AGENTS.md`（グローバル）, `<repo>/AGENTS.md`（ルート）, `<subdir>/AGENTS.md`（下位）
- **Windsurf**: `global_rules.md`（グローバル）, `.windsurfrules`（従来） or `.windsurf/rules/*.md`（推奨）
- **Claude Code**: `~/.claude/CLAUDE.md`（ユーザー）, `<repo>/CLAUDE.md`（ルート）, `<subdir>/CLAUDE.md`（モジュール）
- **Cursor**: 設定UIのグローバルルール + `<repo>/.cursor/rules/*.mdc`（プロジェクト）

---

### 2.3) 階層に同名/複数規約がある場合の **適用順**（上ほど先に読み、下ほど"近い・具体的"として実質優先）

| ツール | 読み込み順（上→下） | 親→子 自動委譲 | 備考 |
|---|---|---|---|
| **Codex** | グローバル → ルート → サブディレクトリ | **Yes** | すべて結合。近い階層が実質上書き。反映は再起動が必要。 |
| **Windsurf** | グローバル → ルート（.windsurf/rules） → サブ（.windsurf/rules） | **Yes** | Cascadeで自動収集。保存即反映。複数WSでも深い階層を優先表示。 |
| **Claude Code** | ユーザー → ルート → （**必要時**）サブ | **Yes（遅延）** | 子`CLAUDE.md`は該当サブツリー参照時に動的読込。編集後は再起動推奨。 |
| **Cursor** | グローバル設定 → ルート`.cursor/rules/*.mdc` | **No** | 子は自動継承なし。親のglob定義 or 子を別WSで開く。保存即反映。 |

---

### 2.4) A/B/C モノレポ例での最終適用（Aを開き、B/C配下を編集）

```
~/.codex/AGENTS.md（グローバル）
project/AGENTS.md（A: 親）
project/frontend/AGENTS.md（B）
project/backend/AGENTS.md（C）
```

- **Codex**: `グローバル → A → B(またはC)` で結合（B/Cが最も具体）。
- **Windsurf**: `global_rules → A/.windsurf/rules → B/.windsurf/rules（またはC）` とCascade（委譲不要）。
- **Claude Code**: 起動時 `ユーザー → A` 。B/Cのファイル参照時に `B（またはC）` を **追加読込**。
- **Cursor**: Aの`.cursor/rules/*.mdc`のみ適用。B/C独自ルールは **無視**（親にglobルールを作るか、B/Cを別WSで開く）。

---

### 2.5) 再読み込み・キャッシュ

- **Codex**: セッション起動時に読込。**変更反映はセッション再起動が必要**。
- **Windsurf**: **保存で即反映**（毎プロンプト時に最新収集）。
- **Claude Code**: 起動時に上位読込／**子はアクセス時に動的**。**編集反映は再起動（/restart）推奨**。
- **Cursor**: **保存で即反映**（ルール監視）。

---

### 2.6) 明示的な委譲・無効化・上書きの実務ヒント

- **Codex**: 自動結合。特定階層のみ無効化する公式フラグはなし。子`AGENTS.md`に「当フォルダではXを適用しない」等を明記して**実質上書き**。
- **Windsurf**: ルールはUIで **Always/Manual** 切替可。不要ならルール単位でオフ／削除。**複数ファイル分割**推奨。
- **Claude Code**: `CLAUDE.md`から`@path`で **インポート** 可。上位は土台、下位が詳細。編集時は`/restart`で確実反映。
- **Cursor**: 子ごとに`.mdc`を作る代わりに **親の`.cursor/rules`でglob割り当て**。Alwaysは最小限、Auto中心で文脈消費を抑制。

---

### 2.7) スニペット（テンプレ）

**Cursor（B配下だけに効かせる）**

```markdown
---
description: "Frontend rules"
globs: ["frontend/**"]
alwaysApply: false
---
- Reactは関数コンポーネントのみ
```

**Claude Code（ルートから分割読み込み）**

```markdown
# CLAUDE.md
See @frontend/CLAUDE.md for React rules
```

**Windsurf（分割ルール配置）**

```
A/.windsurf/rules/frontend.md
A/frontend/.windsurf/rules/testing.md
```

---

### 2.8) 最小再現手順（各3–6行）

- **Codex**: 3階層に`AGENTS.md`を置く → Codexを起動 → B内ファイルで生成 → Bの指示が反映 → `AGENTS.md`変更後は再起動。
- **Windsurf**: ルートとBに`.windsurf/rules`を置く → 保存 → B内でAI実行 → Rulesパネルで適用確認（即時反映）。
- **Claude Code**: `~/.claude/CLAUDE.md`と`A/CLAUDE.md`を用意 → VS Code起動 → B内ファイルで質問 → その時点で`B/CLAUDE.md`が効く → 変更時は`/restart`。
- **Cursor**: Aの`.cursor/rules`にB用`.mdc`を作り`globs: ["frontend/**"]` → B内でAI実行 → 反映確認（保存即時）。

---

### 2.9) ベストプラクティス（要点）

- **近い階層ほど具体**に：上位は方針、下位は実務ルール。
- **Always適用は最小限**（Windsurf/Cursor）：不要な文脈を増やさない。
- **変更後の反映手順をチームで統一**：Codex/Claudeは再起動ルールを周知。
- **モノレポ運用**：Cursorは親のglob設計が肝。Windsurf/Claude/Codexは子に置けば自動で効く。

---

### 2.10) 補足（Unknownの扱い）

- マルチWS時のCodex / Cursorの厳密な優先判定（内部実装）は **Unknown**。実務上は「編集中ファイルの属するプロジェクトの規約のみ」が使われる前提で運用。
