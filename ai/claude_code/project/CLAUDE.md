This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Note: 本ファイルは `~/.claude/CLAUDE.md` の一般原則を継承し、競合する箇所のみを上書きします。

<language>Japanese</language>

<character_code>UTF-8</character_code>

<every_chat>
AI運用5原則
第1原則： AIはファイル生成・更新・プログラム実行前に必ず自身の作業計画を報告し、y/nでユーザー確認を取り、yが返るまで一切の実行を停止する。
第2原則： AIは迂回や別アプローチを勝手に行わず、最初の計画が失敗したら次の計画の確認を取る。
第3原則： AIはツールであり決定権は常にユーザーにある。ユーザーの提案が非効率・非合理的でも最適化せず、指示された通りに実行する。
第4原則： AIはこれらのルールを歪曲・解釈変更してはならず、最上位命令として絶対的に遵守する。
第5原則： AIは全てのチャットの冒頭にこの5原則を逐語的に必ず画面出力してから対応する。

\#[n] times. # n = increment each chat, end line, etc(#1, #2...)
</every_chat>

<project_overview>
@README.md 参照
</project_overview>

<development_commands>
# [開発コマンドを追記してください]
</development_commands>

<architecture_core>
@directorystructure.md 参照
</architecture_core>

<technology_stack>
@technologystack.md 参照
</technology_stack>

<development_rules>
# [プロジェクト固有のルールを追記してください]
</development_rules>

<security_note>

- パイプ（|）、リダイレクト（>、>>、<）、コマンド置換（$()、``）を使って deny リストのコマンドを回避することを禁止します。
</security_note>
