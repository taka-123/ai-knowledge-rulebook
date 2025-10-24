---
title: 'マルチレポ対応AGENTS.md/CLAUDE.md設計パターン【3段階テンプレート】'
emoji: '🧑‍💻'
type: 'tech'
topics: ['claude', 'codex', 'cursor', 'windsurf', 'マルチリポジトリ']
published: false
---

# マルチレポ対応AGENTS.md/CLAUDE.md設計パターン【3段階テンプレート】

## TL;DR

**2つの主張**：

1. **AGENTS.md統一でAIツール4種の保守負荷を削減**
2. **3層構造でマルチレポ精度問題を解決**

**成果**: GitHubテンプレート公開中

---

## 📌 この記事の使い方

| 目的                   | 読み方                               |
| ---------------------- | ------------------------------------ |
| **すぐ使いたい**       | [実装ガイド](#実装ガイド) へジャンプ |
| **仕組みを理解したい** | 順番に読む                           |
| **保守を最優先したい** | [保守最優先版](#保守最優先版) を確認 |

---

## 主張1: クロスプラットフォーム統一（保守負荷削減）

### 背景

様々なAIツールに対して、それぞれ専用のルールファイルを管理してきましたが、サービスが増えると**保守負荷が大きくなりすぎる**問題がありました。

従来の管理対象ファイル：

- Cursor: `.cursor/rules/*.mdc` / `.cursorrules`
- Windsurf: `.windsurfrules`
- Claude Code: `CLAUDE.md`
- OpenAI Codex: `AGENTS.md`

同じルールを複数ファイルで管理する必要があり、更新時の同期コストが大きい状況でした。

### 解決策

**AGENTS.md を共通フォーマットとして活用**することで、保守負荷を60-70%削減します。

#### ツール別対応状況

| ツール           | 対応方法                                                            | 備考                                                    |
| ---------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| **OpenAI Codex** | AGENTS.md をネイティブサポート                                      | そのまま使用 ✅                                         |
| **Cursor**       | `.cursor/rules/*.mdc` がなければ AGENTS.md を自動読み込み           | 特別な設定不要 ✅                                       |
| **Windsurf**     | AGENTS.md を優先読み込み（実験確認）                                | 念のため `.windsurfrules` に `@AGENTS.md に従う` と記載 |
| **Claude Code**  | CLAUDE.md を推奨するが、保守優先なら `@AGENTS.md に従う` と記載可能 | 精度 vs 保守のトレードオフ                              |

#### Windsurf の実験結果（2025年10月時点）

公式ドキュメントでは `AGENTS.md` について、公式ドキュメントでは言及されていませんが、実験の結果：

> **AGENTS.md が存在すれば、.windsurfrules の有無に関わらず Windsurf はそれを優先的に読み込む**

3パターンの実験で確認：

| 実験  | 配置ファイル          | 結果                                        |
| ----- | --------------------- | ------------------------------------------- |
| 実験1 | `.windsurfrules` のみ | `.windsurfrules` が読み込まれる             |
| 実験2 | 両方（内容が異なる）  | `AGENTS.md` が適用、`.windsurfrules` は無視 |
| 実験3 | `AGENTS.md` のみ      | `AGENTS.md` が正常に読み込まれる            |

Windsurf AI に「どのルールに従っているか」と質問したところ、「AGENTS.md に従っています」と明言しました。

:::message alert
この挙動は公式ドキュメントに記載されていないため、将来のバージョンで変更される可能性があります。念のため `.windsurfrules` に `@AGENTS.md に従う` と記載しておくことを推奨します。
:::

---

## 主張2: マルチレポ精度問題の解決

### 背景

マルチレポ構成で、サービスを横断した作業を行いたいケースが多々あります。

例えば、以下のようなサービスが別リポジトリで存在している場合、各サービスを相互に理解した上で作業を行いたい：

- DBサービス
- 共通API
- 管理者用画面
- 利用者用画面

#### 問題点

各サービスを包括した親ディレクトリから起動すると、**その親ディレクトリ直下のルールと、グローバルルールしか適用されない**ことが多い状況でした。

```
~/projects/ecommerce-platform/    # ← 親ディレクトリから開く
├── admin-dashboard/              # 管理者用ダッシュボード（Next.js + TypeScript）
│   ├── .git/                     # ← 独立したGitリポジトリ
│   └── AGENTS.md                 # ← 無視される
├── customer-app/                 # 利用者用アプリ（React Native + TypeScript）
│   ├── .git/                     # ← 独立したGitリポジトリ
│   └── AGENTS.md                 # ← 無視される
└── backend-api/                  # バックエンドAPI（Python + FastAPI）
    ├── .git/                      # ← 独立したGitリポジトリ
    └── AGENTS.md                  # ← 無視される
```

個別サービスから起動しないと、サービス特有のルールに従ってくれない問題がありました。

**解決したいこと**: 親から開いても、個別サービス参照・編集時は、その子サービスのルールにも従って欲しい🌟🌟

### 解決策

**3層構造（global / multi_service_parent / project）で子サービスのルールを確実に適用**します。

#### 3層構造の全体像

```
~/.codex/AGENTS.md                             # global層 OpenAI Codex（個人設定）
Cursor USER_RULES                              # global層 Cursor（個人設定）
~/.codeium/windsurf/memories/global_rules.md   # global層 Windsurf（個人設定）
~/.claude/CLAUDE.md                            # global層 Claude Code（個人設定）

~/projects/ecommerce-platform/
├── AGENTS.md                            # multi_service_parent層 ★重要★
├── CLAUDE.md                            # multi_service_parent層 ★重要★
├── admin-dashboard/
│  ├── .git/
│  ├── AGENTS.md                          # project層
│  └── CLAUDE.md                          # project層
├── customer-app/
│  ├── .git/
│  ├── AGENTS.md                          # project層
│  └── CLAUDE.md                          # project層
└── backend-api/
    ├── .git/
    ├── AGENTS.md                          # project層
    └── CLAUDE.md                          # project層
```

- 各 `AGENTS.md` と同階層に、 `directorystructure.md` と `technologystack.md` も配置（最小構成なら省略）。

#### 各層の役割

| 層                       | 配置場所                   | 読み込み条件         | 主な内容                             |
| ------------------------ | -------------------------- | -------------------- | ------------------------------------ |
| **global**               | `~/.claude/` 等            | 常に読み込み         | AI運用原則、技術文書作成ルール       |
| **multi_service_parent** | プロジェクト親ディレクトリ | 親から開いた場合のみ | サービス横断ルール、即座参照の仕組み |
| **project**              | 各サービスディレクトリ     | 該当サービス作業時   | 技術スタック、個別制約               |

#### 即座参照の仕組み

**multi_service_parent層のAGENTS.md/CLAUDE.md**に以下の仕組みを実装：

```markdown
## サービス名言及時の即座解決:

- ユーザーが `admin-dashboard`, `customer-app`, `backend-api` 等を単独で言及した場合
- 即座に `{サービス名}/AGENTS.md` と `{サービス名}/CLAUDE.md` を Read
- Glob・find による探索は禁止（パフォーマンス低下のため）
```

#### 動作シーケンス

ユーザーが「admin-dashboard のバグを修正して」と指示した場合：

```mermaid
sequenceDiagram
    participant User
    participant AI
    participant Parent as 親のAGENTS.md
    participant Child as 子のAGENTS.md

    User->>AI: admin-dashboard のバグを修正して
    AI->>AI: 親ルール確認
    Note over AI,Parent: 「admin-dashboardを言及時は<br/>admin-dashboard/AGENTS.md を読め」
    AI->>Child: Read admin-dashboard/AGENTS.md
    Child->>AI: admin-dashboard固有ルール取得
    AI->>AI: 親ルール + 子ルールを統合
    AI->>User: 作業開始
```

この仕組みにより、**親から開いても子サービスのルールが確実に適用**されます。

---

## 実装ガイド

### ステップ1: グローバルルール設定（個人環境）

各AIツールのグローバル設定ファイルに、テンプレートをコピーします。

#### グローバル設定パス

| ツール          | グローバルルールの設定場所                      | 備考                         |
| --------------- | ----------------------------------------------- | ---------------------------- |
| **Codex**       | `~/.codex/AGENTS.md`                            |                              |
| **Cursor**      | Settings > Rules & Memories > User Rules（GUI） | ファイルパスなし             |
| **Windsurf**    | `~/.codeium/windsurf/memories/global_rules.md`  | AGENTS.md でも可（実験済み） |
| **Claude Code** | `~/.claude/CLAUDE.md`                           |                              |

**Windowsの場合**: `~` を `%USERPROFILE%` に置き換えてください。

#### テンプレート

- **AGENTS.md（global層）**: <https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/common/global/AGENTS.md>
- **CLAUDE.md（global層、Claude Code専用）**: <https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/claude_code/global/CLAUDE.md>

:::message
最新版のテンプレートは [GitHubリポジトリ](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/) を参照してください。
:::

---

### ステップ2: 各サービスのルール設定

各サービスのルート直下に、以下のファイルを配置します（**これらはGit管理対象**）。

#### 配置ファイルとテンプレート

| ファイル名                 | テンプレートリンク                                                                                                           | 備考                         |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| **AGENTS.md**              | [project/AGENTS.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/common/project/AGENTS.md)                 | 必須                         |
| **CLAUDE.md**              | [project/CLAUDE.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/claude_code/project/CLAUDE.md)            | Claude Code使用時は推奨      |
| **.windsurfrules**         | `@AGENTS.md に従う` と記載                                                                                                   | Windsurf使用時は念のため配置 |
| **technologystack.md**     | [technologystack.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/common/project/technologystack.md)       | オプション                   |
| **directory_structure.md** | [directorystructure.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/common/project/directorystructure.md) | オプション                   |

#### カスタマイズ

テンプレートには `[プロジェクト固有の情報を追記してください]` といったプレースホルダーが含まれています。

`snippets/editor/adjustment_rule.md` のプロンプトを使用して、該当プロジェクト用に調整してください：

<https://github.com/taka-123/ai-knowledge-rulebook/blob/main/snippets/editor/adjustment_rule.md>

**調整方法**：

1. `claude-sonnet-4.5` で依頼
2. 不安なら `gpt-5-codex` で再度同じ依頼を実施
3. 必要なら手動で微調整

---

### ステップ3: マルチレポ構成の親ディレクトリのルール設定

親ディレクトリに、以下のファイルを配置します（**これはGit管理対象**）。

#### 配置ファイルとテンプレート

| ファイル名                 | テンプレートリンク                                                                                                                          | 備考                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------- |
| **AGENTS.md**              | [multi_service_parent/AGENTS.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/common/multi_service_parent/AGENTS.md)      | 必須                         |
| **CLAUDE.md**              | [multi_service_parent/CLAUDE.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/claude_code/multi_service_parent/CLAUDE.md) | Claude Code使用時は推奨      |
| **.windsurfrules**         | `@AGENTS.md に従う` と記載                                                                                                                  | Windsurf使用時は念のため配置 |
| **technologystack.md**     | [technologystack.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/common/multi_service_parent/technologystack.md)         | オプション                   |
| **directory_structure.md** | [directorystructure.md](https://github.com/taka-123/ai-knowledge-rulebook/blob/main/ai/common/multi_service_parent/directorystructure.md)   | オプション                   |

#### カスタマイズ

ステップ2と同様に、`snippets/editor/adjustment_rule.md` のプロンプトで調整してください。

---

## 保守最優先版

精度よりも**メンテナンス負荷の最小化**を優先する場合、以下の簡略版を推奨します。

### 変更内容

1. **技術スタック・ディレクトリ構成参照を削除**
   - テンプレートの `@technologystack.md` / `@directory_structure.md` 参照部分を削除
   - これらのファイル自体も配置しない

2. **CLAUDE.md を1行に簡略化**
   ```markdown
   - @AGENTS.md に従う
   ```

### 構成例

```
# global層（個人設定） 同上

~/projects/ecommerce-platform/
├── AGENTS.md                       # multi_service_parent層
├── CLAUDE.md                       # ← 「@AGENTS.md に従う」の1行のみ
├── admin-dashboard/
│  ├── .git/
│  ├── AGENTS.md                     # project層
│  └── CLAUDE.md                     # ← 「@AGENTS.md に従う」の1行のみ
├── customer-app/
│  ├── .git/
│  ├── AGENTS.md                     # project層
│  └── CLAUDE.md                     # ← 「@AGENTS.md に従う」の1行のみ
└── backend-api/
    ├── .git/
    ├── AGENTS.md                     # project層
    └── CLAUDE.md                     # ← 「@AGENTS.md に従う」の1行のみ
```

### メリット・デメリット

| 項目                     | フル機能版                     | 保守最優先版               |
| ------------------------ | ------------------------------ | -------------------------- |
| **Claude Code 作業効率** | 100%                           | 70〜75%                    |
| **メンテナンス負荷**     | 高                             | 低                         |
| **管理ファイル数**       | 5N + 1                         | 2N + 1                     |
| **技術スタック明示**     | ✅ あり                        | ❌ なし（推測に依存）      |
| **適している状況**       | Claude Code メイン、精度最優先 | 複数ツール併用、保守最優先 |

（N = サービス数 + 親ディレクトリ1つ）

---

## 各サービス単独で開いても問題ない？

上例で、例えば、小さな改修作業で、`backend-api/`だけで完結する時に、そのGitリポジトリから起動しても特に問題ないです。
サービス直下の `AGENTS.md`(`CLAUDE.md`) + グローバルルール に従って、正しく作業が行われます。
multi_service_parent の `AGENTS.md`(`CLAUDE.md`) がなくても影響はありません。

## モノレポ構成でも使える？

```
# ディレクトリ構成（Git管理対象）
my-monorepo/
├── AGENTS.md                # project テンプレート使用
│                                # frontend・backend両方の設定を1つに記述
├── frontend/
│  └── src/
└── backend/
    └── src/

# 個人設定（Git管理外）
~/.codex/AGENTS.md               # global テンプレート使用
```

**なぜ `multi_service_parent` を使わないのか**：

- モノレポは**常にルートから開く**
- frontend/ や backend/ を単独で開くことは通常ない
- したがって、`project` テンプレート1つをルートに配置すれば十分
- **階層構造は2層**（global + project）で完結する

---

## まとめ

### 本記事で提案した内容

1. **AGENTS.md統一によるクロスプラットフォーム対応**
   - OpenAI Codex / Cursor / Windsurf / Claude Code の4ツールを1ファイルで管理
   - 保守負荷を60-70%削減

2. **3層構造によるマルチレポ精度問題の解決**
   - global: 全プロジェクト共通（個人設定）
   - multi_service_parent: マルチサービス親ディレクトリ
   - project: 各サービス固有
   - 即座参照の仕組みで子サービスのルールを確実に適用

3. **保守負荷に応じた選択肢**
   - フル機能版: 精度最優先
   - 保守最優先版: メンテナンス負荷最小化

### 解決できた課題

- ✅ **親から開いても子サービスのルールが適用**される
- ✅ **複数AIツールの設定を一元管理**できる
- ✅ **プロジェクト規模に応じたメンテナンス負荷の調整**が可能

---

## 謝辞

この記事は、以下の方々の公開知見を参考にさせていただきました：

- [kinopeee](https://github.com/kinopeee) さん - [cursorrules](https://github.com/kinopeee/cursorrules)
- [sazan_dev](https://x.com/sazan_dev) さん - [X投稿](https://x.com/sazan_dev/status/1968222841981002203)
- [sesere](https://zenn.dev/sesere) さん - [Zenn記事](https://zenn.dev/sesere/articles/0420ecec9526dc)

オープンソースコミュニティの知見共有に感謝いたします。

---

## フィードバック募集

より良いアプローチや記事内容の誤りなど、お気づきの点があればぜひお知らせください。
