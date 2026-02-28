# Multi-Service Orchestrator

Note: 親階層の司令塔。全サービス共通インフラ定義を参照する。

<routing_logic>

## サービス名言及時の即座解決 (MUST)

ユーザーが特定サービス名（例: `admin-dashboard`, `backend-api`）を言及した場合：

1. **即座に `{サービス名}/CLAUDE.md` を Read せよ。**
2. パス不明時のみ Glob で確認し、直接パス指定を優先せよ。

</routing_logic>

<parent_context>

- システム概要: README.md
- 全体アーキテクチャ: directorystructure.md
- 共通技術スタック: technologystack.md

</parent_context>

<orchestration_rules>

## サービス横断規律

1. **コンテキスト優先**: 作業対象ディレクトリの `CLAUDE.md` が存在する場合、その個別ルールを本ルーターより優先せよ。
2. **新規サービス追加**: `[サービス名]/CLAUDE.md` と `directorystructure.md` の作成を必須とする。

</orchestration_rules>

<global_commands>

## 全サービス共通コマンド

<!-- docker-compose up 等、全サービス共通の操作をここに追記 -->

</global_commands>
