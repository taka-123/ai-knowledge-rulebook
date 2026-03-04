# プロジェクト固有ガイドライン

> Motto: "既存アーキテクチャの絶対遵守と、意図せぬ変更のゼロ化"

## 1. 適用順序

- 作業対象から親へ遡ってツール固有ルールと `AGENTS.md` を読み、近い階層を優先する。

## 2. 実行ポリシー

- 計画: `rg` / `grep` で既存パターンを探索し、影響範囲（型/API/設定）を特定する。
- 実装: 既存の変換・エラー処理・非同期パターンを踏襲し、指示外変更は提案止まりにする。
- 承認必須: タスク範囲外の変更、復元困難な削除、外部契約に影響する変更、要件外リファクタ。

## 3. レビュー基準（`@codex review` / `/review`）

- P0: 誤動作、セキュリティ欠陥、アーキテクチャ違反。`マージ不可`
- P1: 命名規約違反、不適切なエラー処理、回帰リスク。`マージ不可`
- P2: 性能改善余地、重複コード、可読性改善。`フォローアップ可`
- P3: 軽微なタイポ、好みの提案。`任意`
- 判定は `可 / 不可` を明示し、指摘は重要度順に根拠と最小修正案を添える。

## 4. 検証と報告

- 既存テスト/検証コマンドを優先実行し、未実施・未検証範囲があれば明示する。
- 完了報告には、変更概要・検証結果・未実施事項（ある場合）を含める。

## 5. 作業前チェック

- [ ] 主要依存のバージョン表記と実マニフェストの整合を確認したか。
- [ ] 既存コードパターン探索と機密情報混入チェックを実施したか。
- [ ] 報告が global 層のタスク分類（🟢🟡🔴）に準拠しているか。

## Cursor Cloud specific instructions

This is a documentation/configuration management repository with no runtime services. The "application" is the lint, schema, and agent validation tooling.

### Services overview

There are no servers or databases. All verification is done via npm scripts defined in `package.json`.

### Key commands

Refer to `README.md` § セットアップ and § 検証コマンド for the full list. The three primary checks are:

- `npm run lint` — Prettier + markdownlint + yamllint (via `./format.sh check`)
- `npm run schema:check` — JSON Schema validation (uses `check-jsonschema`)
- `npm run agent:check` — Custom skill/agent/routing validators (Node.js `.mjs` scripts)

### Gotchas

- `yamllint` and `check-jsonschema` are Python packages installed with `pip install --user`. They land in `$HOME/.local/bin`, which must be on `PATH`. The VM snapshot persists `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc` so this is already set.
- `npm run schema:check` always exits 0 (trailing `; true`) even when schema mismatches exist — check stdout for actual errors.
- `npm run agent:check` exits non-zero on pre-existing validation failures in the repo (e.g. skill description pattern issues). These are not caused by environment setup.
- The sync scripts (`scripts/sync-*-to-home.sh`) require `rsync`. Install it with `sudo apt-get install -y rsync` if not already present.
- `npm run lint` (via `format.sh`) reports Prettier warnings on SKILL.md files — these are pre-existing formatting issues, not environment problems.
