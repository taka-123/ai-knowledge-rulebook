# Project Constitution for Claude Code

作業開始前: `docs/ai/PROJECT_REALITY_MAP.md` → `docs/ai/AI_OPERATING_GUIDE.md` → 本ファイル。

## Canonical Source

- Skill 実体は `.claude/skills/<name>/SKILL.md` に限定する。
- ルーターや補助設定には Skill 本文を複製しない。

## Routing Policy

- 各 agent/skill の description 内の Trigger Keywords で自動マッチする。
- 同名資産がグローバルとプロジェクトに存在する場合、プロジェクト版が優先。
- 完了前に `format-lint-audit` で品質ゲートを確認する。

## Repository Commands

- `npm run format:check`
- `npm run schema:check`
- `npm run lint:md` / `npm run lint:yaml` / `npm run lint:json`

## 外部サービス

### AWS

- AWS へのアクセスは AWS MCP Server を使う。
- AWS CLI、AWS SDK、絶対パス・相対パスでの AWS CLI 実行、その他の迂回経路は使わない。
- リソースの作成・更新・削除・起動・停止・デプロイ・権限変更など状態変更は行わない。必要な変更は実行せずユーザーへ提示する。

### GitHub

- GitHub 操作には、公式 GitHub MCP Server または GitHub CLI（`gh`）を使用してよい。一方が利用できない場合は、可能であれば他方を試す。
- 明示依頼があれば自動で行ってよい: Issue / PR / CI の参照、Issue 作成・通常編集、Issue・PR へのコメント、PR 作成・通常編集、feature branch への通常 push。
- 明示依頼のない既存 Issue/PR の close・状態変更・大幅本文変更・base/reviewer 変更はしない。
- 禁止: PR merge、review 提出、main/master 直接 push、force push、Actions 手動起動・rerun、Ruleset/設定変更、認証情報の表示・変更。

詳細: `ai/EXTERNAL_SERVICES_SECURITY.md`
