# Multi-Service Orchestrator (v2026.1)

Note: 本ファイルは親階層の司令塔です。全サービス共通のインフラ定義を参照します。

<routing_logic>

## サービス名言及時の即座解決 (MUST)

ユーザーが特定サービス名（例: `admin-dashboard`, `backend-api` 等）を言及した場合：

1. **即座に `{サービス名}/CLAUDE.md` を Read せよ。**
2. 探索（Glob/find）は禁止。パスを直接指定して読み込むこと。

</routing_logic>

<parent_context>

- System Overview: @README.md
- Global Architecture: @directorystructure.md
- Common Tech Stack: @technologystack.md

</parent_context>

<orchestration_rules>

## サービス横断規律

1. **コンテキストの優先順位**: 作業対象ディレクトリの `CLAUDE.md` が存在する場合、その個別ルールを本ルーターの設定より優先せよ。
2. **新規サービス追加**:
   - `[サービス名]/CLAUDE.md` および `@directorystructure.md` の作成を必須とする。
3. **自己認識（再帰トリガー）**:
   毎回の応答の冒頭に `#[n] (n=応答回数)` を表示せよ。これにより、現在どのサービスのコンテキストがロードされているかを再認識せよ。

</orchestration_rules>

<global_commands>

## [docker-compose up 等、全サービス共通の操作のみ追記]

</global_commands>
