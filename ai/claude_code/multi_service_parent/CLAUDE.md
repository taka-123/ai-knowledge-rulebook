# Multi-Service Orchestrator

全サービス共通のインフラ定義を管理する親階層の司令塔。

<routing_logic>

## サービス解決

ユーザーがサービス名を言及した場合、即座に `{サービス名}/CLAUDE.md` を Read せよ。
パス不明時のみ Glob で確認すること。

</routing_logic>

<parent_context>

- システム概要: README.md
- アーキテクチャ: directorystructure.md
- 技術スタック: technologystack.md

</parent_context>

<orchestration_rules>

## サービス横断規律

1. 作業対象ディレクトリに `CLAUDE.md` がある場合、その個別ルールを本ファイルより優先せよ。
2. 新規サービス追加時は `[サービス名]/CLAUDE.md` と `directorystructure.md` を必ず作成せよ。

</orchestration_rules>

<global_commands>

## 全サービス共通コマンド

<!-- docker-compose up 等、全サービス共通の操作をここに追記 -->

</global_commands>
