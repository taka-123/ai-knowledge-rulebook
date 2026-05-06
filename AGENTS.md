# プロジェクト固有ガイドライン

> Motto: "既存アーキテクチャの絶対遵守と、意図せぬ変更のゼロ化"

## 1. 適用順序

- 作業対象から親へ遡ってツール固有ルールと `AGENTS.md` を読み、近い階層を優先する。

## 2. 実行ポリシー

### Shell Commands (CRITICAL!)

- **常に** Shell ツール使用時に `working_directory` を指定する。
  - ワークスペースルートまたは対象ディレクトリの絶対パスを用いる。
- コマンドに `cd` を含めない（ユーザーが明示した場合を除く）。
- 理由:
  - 一部環境でサンドボックス外とみなされる。
  - 承認待ちで止まる。

- 計画: `rg` / `grep` で既存パターンを探索し、影響範囲（型/API/設定）を特定する。
- 実装: 既存の変換・エラー処理・非同期パターンを踏襲し、指示外変更は提案止まりにする。
- 承認必須: タスク範囲外の変更、復元困難な削除、外部契約に影響する変更、要件外リファクタ。

## 3. 検証と報告

- 既存テスト/検証コマンドを優先実行し、未実施・未検証範囲があれば明示する。
- 完了報告には、変更概要・検証結果・未実施事項（ある場合）を含める。

## 4. 作業前チェック

- [ ] 主要依存のバージョン表記と実マニフェストの整合を確認したか。
- [ ] 既存コードパターン探索と機密情報混入チェックを実施したか。
- [ ] 報告が global 層のタスク分類（🟢🟡🔴）に準拠しているか。

## Cursor Cloud specific instructions

This is a documentation/configuration repository with no runtime services. The "application" is the set of lint, format, and validation scripts.

### Prerequisites

- Node.js >= 18 (installed via NodeSource)
- Python 3 with `yamllint` and `check-jsonschema` (pip)
- npm dependencies (see `package.json` devDependencies)

### Key commands (see README.md for full list)

| Task                   | Command                |
| ---------------------- | ---------------------- |
| Lint all               | `npm run lint`         |
| Auto-fix formatting    | `npm run format`       |
| Schema validation      | `npm run schema:check` |
| Agent/skill validation | `npm run agent:check`  |

### Gotchas

- `.claude/settings.json` defines PreToolUse hooks that log to `~/.claude/command_history.log`. The directory `~/.claude/` must exist or all Shell commands will be blocked by the hook. The update script creates it via `mkdir -p /root/.claude`.
- `npm run schema:check` ends with `; true` so it always exits 0, even when schema errors exist. Pre-existing schema mismatches (MCP config files validated against `ai_profile.schema.json`) are expected.
- `npm run agent:check` may report pre-existing skill validation failures (e.g., trigger keyword count). These are repo-level issues, not environment issues.
