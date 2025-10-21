This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Note: 本ファイルは CLAUDE.md の一般原則を継承し、競合する箇所のみを上書きします。
(macOS/Linux: ~/.claude/CLAUDE.md, Windows: %USERPROFILE%\.claude\CLAUDE.md)

<language>Japanese</language>

<character_code>UTF-8</character_code>

---

## 🚨 サービス別ルールの必須確認 🚨

### サービス固有 CLAUDE.md の必須読み込み

**このプロジェクトはマルチサービス構成です。**

各サービスディレクトリには独自の `CLAUDE.md` があり、**そのサービスのファイルを触る前に必ず Read ツールで読み込むこと。**

#### 📍 サービス別 CLAUDE.md の配置ルール

**パターン**: `[サービスディレクトリパス]/CLAUDE.md`

**例:**

- `services/service-a/` を触る → `services/service-a/CLAUDE.md` を読む
- `apps/frontend/` を触る → `apps/frontend/CLAUDE.md` を読む
- `backend/api/` を触る → `backend/api/CLAUDE.md` を読む

**これ以外のサービスも、ルールは同様です。**

#### ⚙️ 実行手順

1. **ファイルパスを確認** → どのサービスディレクトリ配下か判定
2. **即座に Read ツールを実行** → 例: `Read([プロジェクトパス]/services/service-a/CLAUDE.md)`
3. **読み込み完了を確認** → その内容を最優先ルールとして適用
4. **作業開始**

#### ⚠️ 絶対禁止事項

- サービス固有 `CLAUDE.md` を読まずに作業開始すること
- 「簡単な作業だから不要」と判断すること
- 読み込みを後回しにすること

#### 🔄 優先順位

1. **サービス固有 `CLAUDE.md`** （最優先）
2. プロジェクトルート `CLAUDE.md`（このファイル）
3. グローバル `~/.claude/CLAUDE.md`

競合時は上記の順で優先。

---

<project_overview>
@README.md 参照

</project_overview>

<development_commands>

## [プロジェクト固有の開発コマンドを追記してください]

### 例: コンテナ起動・停止

```bash
# 起動
$ docker-compose up -d

# 停止
$ docker-compose down
```

### 例: データベースマイグレーション

```bash
# マイグレーション実行
$ [マイグレーションコマンド]

# ステータス確認
$ [ステータス確認コマンド]
```

</development_commands>

<architecture_core>
@directorystructure.md 参照
</architecture_core>

<technology_stack>
@technologystack.md 参照
</technology_stack>

<development_rules>

### プロジェクト固有のルール

#### マイクロサービス構成

- 各サービスは `[サービスディレクトリパス]/` 配下に独立配置
- サービス固有の開発ルールは `[サービスディレクトリパス]/CLAUDE.md` を参照
- ディレクトリ構造は `[サービスディレクトリパス]/directorystructure.md` を参照（存在する場合）

#### データベース管理

- スキーマ変更は必ず [マイグレーション管理方法] を使用
- マイグレーション実行前に確認手順を実施
- [使用しているデータベース] を使用

#### 共通ライブラリ

- [共通処理のパス]: `[パス]`
- [共通スクリプトのパス]: `[パス]`

#### 新規サービス追加時

1. `[サービスディレクトリパス]/` にコード配置
2. `[コンテナ設定のパス]/` に設定ファイル配置（該当する場合）
3. `[統合設定ファイル]` にサービス定義追加
4. `[サービスディレクトリパス]/CLAUDE.md` を作成
5. `[サービスディレクトリパス]/directorystructure.md` を作成（推奨）

#### コード変更時の注意

- 各サービスの技術スタック・バージョン要件を確認
- 各サービスの依存関係を変更する前に該当サービスの `CLAUDE.md` を確認

</development_rules>

<error_classification>

### エラー対応の優先度

- 🟢 **軽度**: 記録しつつ継続（例: 警告ログ、非推奨 API）
- 🟡 **アプリケーション**: 自動リトライ後に報告（例: 解析失敗、フォーマット不一致）
- 🔴 **システム**: 即停止・承認待ち（例: タイムアウト、通信断）
- ⛔ **セキュリティ**: 全作業停止・緊急報告（例: 認証情報漏洩）
  </error_classification>

<security_note>

- パイプ（|）、リダイレクト（>、>>、<）、コマンド置換（$()、``）を使って deny リストのコマンドを回避することを禁止します。

</security_note>
