# Multi-Service Orchestrator

サービス横断の親ルール。

<routing_logic>

## サービス解決

- ユーザーが子サービス名を言及したら、即座に `{サービス名}/CLAUDE.md` を Read せよ。
- 直接パス指定を優先し、パス不明時のみ Glob で確認すること。

</routing_logic>

<parent_context>

<!-- テンプレート注記: `README.md` / `directorystructure.md` / `technologystack.md` の3項目のみ使用。不存在の行を削除し、3項目すべて不存在ならブロックごと削除 -->

- システム概要: `README.md`
- アーキテクチャ: `directorystructure.md`
- 技術スタック: `technologystack.md`

</parent_context>

<orchestration_rules>

## サービス横断規律

- 作業対象ディレクトリに `CLAUDE.md` がある場合、その個別ルールを本ファイルより優先せよ。

</orchestration_rules>

<global_commands>

## 全サービス共通コマンド

<!-- テンプレート注記: 任意欄。全サービス共通で毎ターン有益な操作のみ記載 -->

</global_commands>
