# AGENTS.md マルチリポジトリ運用ガイド

**最終更新**: 2025-10-21
**ステータス**: 公式仕様・コミュニティ情報検証済み、実務投入可能、実証済みベストプラクティス追加
**対象読者**: マルチリポジトリ（モノレポ含む）環境でOpenAI CodexやCursorを運用する開発者・チーム

---

## 目次

1. [結論：2つの重要な質問](#結論2つの重要な質問)
2. [対処法：3パターン比較](#対処法3パターン比較)
3. [推奨構成：明示的読み込み方式](#推奨構成明示的読み込み方式)
4. [公式仕様の詳細](#公式仕様の詳細)
5. [FAQ](#faq)
6. [出典一覧](#出典一覧)

---

## 結論：2つの重要な質問

### 典型的な課題

企業開発では、以下のような3層構造のマルチリポジトリ環境が一般的です：

```
親リポジトリ（docker-compose統合）/
├── sub-repos/
│   ├── company-admin-app/
│   ├── facility-admin-app/
│   ├── facility-user-app/
│   ├── external-site-frontend/
│   ├── external-site-backend/
│   └── batch/
└── docker-compose.yml
```

各リポジトリには独自の`AGENTS.md`が配置され、IDEで親リポジトリを開き、ワークスペースに各子リポジトリを追加して作業します。

### Q1: 親から開いた場合、子リポジトリのAGENTS.mdは認識されるか？

**A1: いいえ、以下のツールで自動適用はされません**

| ツール       | 挙動                                       | 根拠の強度       | 確認日     |
| ------------ | ------------------------------------------ | ---------------- | ---------- |
| OpenAI Codex | 作業ディレクトリが子内にある場合のみ適用   | **公式仕様準拠** | 2025-10-17 |
| Cursor       | プロジェクト（起動ディレクトリ）単位で解釈 | **公式仕様準拠** | 2025-10-21 |

**注**: Cursor は 2025年10月時点でトークンクレジット制を採用しており、不要な y/n 確認を削減することでトークン消費を最適化できます。

#### 根拠

1. **OpenAI Codex**: 読み込み階層は `~/.codex/AGENTS.md` → リポジトリルートの `AGENTS.md` → 現在の作業ディレクトリの `AGENTS.md` の順でトップダウンマージ。作業ディレクトリが親の場合、子の `AGENTS.md` はマージ対象外。
2. **Cursor**: `AGENTS.md` はプロジェクト（`.cursor/rules` の簡易代替）スコープで解釈され、起動ディレクトリ基準の単一適用。
3. **agentsmd.io 仕様**: `AGENTS.md` のスコープは「そのファイルが存在するフォルダをルートとするディレクトリツリー全体」。より深い階層の `AGENTS.md` が競合時に優先されるが、起動ディレクトリが親の場合は子のスコープ外。

#### 結論

親から起動 = 親の `AGENTS.md` のみ有効。子リポジトリの `AGENTS.md` は**明示的に読み込む指示を親に記載しない限り**無視されます。

---

### Q2: AGENTS.mdの読み込み階層はどうなっているか？

**A2: ツールごとに以下の階層で読み込まれます**

#### OpenAI Codex（階層マージ型）

| 優先度      | ファイル         | パス                    | スコープ         | マージ方式         |
| ----------- | ---------------- | ----------------------- | ---------------- | ------------------ |
| 1（基底）   | ユーザー全体     | `~/.codex/AGENTS.md`    | 全プロジェクト   | トップダウンマージ |
| 2（上書き） | リポジトリルート | `<repo-root>/AGENTS.md` | 当該リポジトリ   | 1に追加・上書き    |
| 3（最優先） | 作業ディレクトリ | `<cwd>/AGENTS.md`       | 作業対象スコープ | 2に追加・上書き    |

**統合ルール**: より具体的（深い階層）な `AGENTS.md` が、より一般的な設定を上書き・補完します。

**重要**: 「作業ディレクトリ」は起動時の `cwd`。親で起動している限り、子の `AGENTS.md` は読み込まれません。

---

#### Cursor（プロジェクト単位型）

| 優先度                | ファイル             | パス                                                   | スコープ             |
| --------------------- | -------------------- | ------------------------------------------------------ | -------------------- |
| 1                     | プロジェクトルール   | `<project-root>/AGENTS.md` または `.cursor/rules/*.md` | プロジェクト全体     |
| 2（サブディレクトリ） | 子ディレクトリルール | `<sub-dir>/.cursor/rules/*.md`                         | サブディレクトリ以下 |

**重要**: Cursorでは `AGENTS.md` は `.cursor/rules` の簡易代替として扱われ、プロジェクト（起動ディレクトリ）スコープで解釈されます。親で起動した場合、子の `AGENTS.md` は自動適用されません。

**出典**:

- [Cursor Rules Documentation](https://docs.cursor.com/ja/context/rules) (2025-10-17確認)
- OpenAI Codex仕様（Microsoft Learn、コミュニティ検証済み）
- [agentsmd.io - AGENTS.md Specification](https://agentsmd.io/) (2025-10-17確認)

---

## 対処法：3パターン比較

### パターンA: 手動読み込み

**やり方**:

```bash
# Codex/Cursor起動時に明示的指示
codex "まず ./sub-repos/facility-user-app/AGENTS.md を読んでルールを確認してから、
       施設利用者画面の〇〇を修正してください"
```

| メリット                  | デメリット            |
| ------------------------- | --------------------- |
| ✅ 明示的で確実           | ❌ 毎回手動指示が必要 |
| ✅ シンプルで理解しやすい | ❌ 指示忘れのリスク   |

**推奨ケース**: 単発の修正、細かく制御したい場合

---

### パターンB: 親のAGENTS.mdに明示的読み込みルールを記載（推奨）

**やり方**: 親の `AGENTS.md` に各子リポジトリのルール読み込みを明記

````markdown
# 親リポジトリのAGENTS.md

## マルチリポジトリ運用ルール

### サブリポジトリ一覧

| リポジトリ名   | パス                                  | ルールファイル                                 |
| -------------- | ------------------------------------- | ---------------------------------------------- |
| 施設利用者画面 | `./sub-repos/facility-user-app/`      | `./sub-repos/facility-user-app/AGENTS.md`      |
| 施設管理者画面 | `./sub-repos/facility-admin-app/`     | `./sub-repos/facility-admin-app/AGENTS.md`     |
| 外部公開サイト | `./sub-repos/external-site-frontend/` | `./sub-repos/external-site-frontend/AGENTS.md` |
| バッチ処理     | `./sub-repos/batch/`                  | `./sub-repos/batch/AGENTS.md`                  |

### 🚨 サブリポジトリ修正時の必須手順

**作業対象ファイルが上記サブリポジトリ配下にある場合、以下を必ず実行**：

1. **該当サブリポジトリのルール確認**
   - 上記表の「ルールファイル」パスにある `AGENTS.md` を読み込む
   - 重複実装防止チェック（既存の類似機能、同名・類似名の要素を確認）

2. **ルールの厳密遵守**
   - 子リポジトリの `AGENTS.md` に記載されたコーディング規約・構造・命名規則に従う
   - 不明点がある場合は作業開始前に確認
   - 重要な判断が必要な場合は報告・承認を取得

3. **Git操作の注意**
   ```bash
   # 必ず子リポジトリ内で実行
   cd ./sub-repos/facility-user-app
   git status
   git add .
   git commit -m "..."
   ```
````

### 禁止事項

- 子リポジトリの `AGENTS.md` を読まずに修正を開始すること
- 親リポジトリの `.git/` で子リポジトリのコミットを実行すること
- 明示的に指示されていない変更を行うこと（必要な場合は提案として報告）

````

| メリット | デメリット |
|---------|-----------|
| ✅ チーム全体で統一運用 | ⚠️ エージェントの読解・遵守に一部依存 |
| ✅ Git管理可能（共有容易） | ❌ 初期セットアップが必要 |
| ✅ 明示的で追跡可能 | ❌ 親のAGENTS.mdが肥大化する可能性 |
| ✅ **実証済み**: 実際のマルチサービス環境で機能確認済み | |

**推奨ケース**: 継続的な開発、チーム全体で統一運用したい場合

**実証事例** (2025-10-21):
- `ai-knowledge-rulebook` のグローバル `AGENTS.md` に「🚨 作業開始前チェック」を明記
- `sc-docker-swimming-all` のようなマルチサービス構成（10+サービス）で運用成功
- 各サービス配下の `AGENTS.md` が確実に読み込まれることを確認

---

### パターンC: 個別起動（公式推奨）

**やり方**:

```bash
cd ./sub-repos/facility-user-app
codex
````

| メリット                           | デメリット                             |
| ---------------------------------- | -------------------------------------- |
| ✅ 子のAGENTS.mdが確実に有効       | ❌ 複数リポジトリ横断時に面倒          |
| ✅ Git操作も正しいリポジトリで実行 | ❌ IDEワークスペースの利便性が失われる |
| ✅ 最も公式仕様に沿った方法        | ❌ 起動切り替えが頻繁に必要            |

**推奨ケース**: 単一リポジトリに集中、Git操作の正確性を最優先

---

### 推奨アプローチ（ハイブリッド）

**B（明示的読み込み）+ C（個別起動）の併用**

- 単一リポジトリの修正: `cd`してから起動（C）
- 横断的な修正: 親から起動、親の`AGENTS.md`に従う（B）
- 緊急時・単発: 手動で子の`AGENTS.md`を読ませる（A）

---

## 推奨構成：明示的読み込み方式

### ディレクトリ構造

```
親リポジトリ/
├── AGENTS.md .......................... (1) マスタールール（子への参照明記）
└── sub-repos/
    ├── facility-user-app/
    │   └── AGENTS.md .................. (子のルール定義)
    ├── facility-admin-app/
    │   └── AGENTS.md .................. (子のルール定義)
    └── (以下略)
```

---

### (1) 親の`AGENTS.md`（完全版）

````markdown
# マルチリポジトリ開発 運用ルール

このリポジトリは、複数のサブリポジトリを統合する親リポジトリです。各サブリポジトリには独自のコーディング規約・構造・命名規則があり、作業時には該当サブリポジトリの `AGENTS.md` に従う必要があります。

## サブリポジトリ一覧

| リポジトリ名   | パス                                  | ルールファイル                                 | 技術スタック        |
| -------------- | ------------------------------------- | ---------------------------------------------- | ------------------- |
| 施設利用者画面 | `./sub-repos/facility-user-app/`      | `./sub-repos/facility-user-app/AGENTS.md`      | React, TypeScript   |
| 施設管理者画面 | `./sub-repos/facility-admin-app/`     | `./sub-repos/facility-admin-app/AGENTS.md`     | Next.js, TypeScript |
| 外部公開サイト | `./sub-repos/external-site-frontend/` | `./sub-repos/external-site-frontend/AGENTS.md` | Vue.js, TypeScript  |
| バッチ処理     | `./sub-repos/batch/`                  | `./sub-repos/batch/AGENTS.md`                  | Python              |

## 🚨 サブリポジトリ修正時の必須手順

### ステップ1: ルール読み込み

作業対象ファイルが上記サブリポジトリ配下にある場合、**必ず最初に**以下を実行：

1. 上記表の「ルールファイル」パスにある `AGENTS.md` を読み込む
2. そのファイルに記載されたすべてのルールを確認
3. コーディング規約・構造・命名規則・テスト方針を把握

**例**: `./sub-repos/facility-user-app/src/components/LoginForm.tsx` を修正する場合

```bash
# 最初にルールを読み込む
cat ./sub-repos/facility-user-app/AGENTS.md
```
````

### ステップ2: ルールの厳密遵守

以下を必ず守る：

- 子リポジトリの `AGENTS.md` に記載されたコーディング規約
- ファイル配置・命名規則
- コンポーネント構造・デザインパターン
- テスト記述方針

### ステップ3: Git操作

```bash
# ✅ 必ずサブリポジトリ内で実行
cd ./sub-repos/facility-user-app
git status
git add .
git commit -m "feat: パスワード再設定リンク追加"

# ❌ 親リポジトリでコミットしてはいけない
# cd <親リポジトリ>  # これはNG
# git add sub-repos/facility-user-app/  # これもNG
```

## 禁止事項

- ❌ 子リポジトリの `AGENTS.md` を読まずに修正を開始すること
- ❌ 親リポジトリの `.git/` で子リポジトリのコミットを実行すること
- ❌ 子リポジトリのコーディング規約を無視した修正
- ❌ 子リポジトリのファイル構造・命名規則を破壊する変更

## 横断的な修正の場合

全サブリポジトリに共通の変更を加える場合（例: `.gitignore` に `*.log` を追加）：

1. 各サブリポジトリの `AGENTS.md` を順番に読み込む
2. それぞれのルールに従って修正
3. 各サブリポジトリ内で個別にコミット

## トラブルシューティング

### 子リポジトリのルールを読み忘れた場合

1. 作業を中断
2. 該当サブリポジトリの `AGENTS.md` を読み込む
3. 既存の変更が子リポジトリのルールに準拠しているか確認
4. 準拠していない場合は修正

### どの子リポジトリに属するか不明な場合

```bash
# ファイルパスから判断
# 例: src/components/LoginForm.tsx
# → どのサブリポジトリの配下にあるか確認
find . -name "LoginForm.tsx" -type f
```

````

---

### (2) 子の`AGENTS.md`（例: facility-user-app）

```markdown
# 施設利用者画面 開発ルール

## 技術スタック

- React 18.2
- TypeScript 5.0
- Material-UI 5.x
- React Router v6
- Jest + React Testing Library

## ディレクトリ構造

````

facility-user-app/
├── src/
│ ├── components/ # 再利用可能なコンポーネント
│ ├── pages/ # ページコンポーネント
│ ├── hooks/ # カスタムフック
│ ├── services/ # API通信
│ ├── types/ # TypeScript型定義
│ └── utils/ # ユーティリティ関数
└── tests/

````

## コーディング規約

### コンポーネント命名

- PascalCase: `LoginForm.tsx`, `UserProfile.tsx`
- Hooksは `use` プレフィックス: `useAuth.ts`, `useFetch.ts`

### ファイル配置

- 1コンポーネント = 1ファイル
- テストファイルは `__tests__/` 配下または同階層に `*.test.tsx`

### スタイリング

- Material-UIの `styled` を優先
- インラインスタイルは禁止
- テーマ変数（`theme.palette.*`）を使用

### 状態管理

- ローカル状態: `useState`
- グローバル状態: Context API（Redux禁止）
- サーバー状態: React Query

### テスト

- すべてのコンポーネントにユニットテスト必須
- カバレッジ80%以上維持
- `data-testid` 属性を使用

## Git運用

- ブランチ: `feature/施設利用者-機能名`
- コミットメッセージ: Conventional Commits準拠
  - `feat:`, `fix:`, `refactor:`, `test:`, `docs:`

## 例

### 良い例

```tsx
// src/components/LoginForm.tsx
import { styled } from '@mui/material/styles';
import { Button, TextField } from '@mui/material';

const StyledForm = styled('form')(({ theme }) => ({
  padding: theme.spacing(2),
}));

export const LoginForm: React.FC = () => {
  // ...
};
````

### 悪い例

```tsx
// ❌ インラインスタイル使用
<div style={{ padding: '16px' }}>...</div>

// ❌ any型使用
const handleSubmit = (data: any) => { ... }

// ❌ テストなし
```

````

---

## 公式仕様の詳細

### 1. AGENTS.mdの読み込みルール

#### agentsmd.io 公式仕様（2025-10-17確認）

[agentsmd.io - AGENTS.md Specification](https://agentsmd.io/)より：

> **スコープ**: "The scope of an AGENTS.md file is the entire directory tree rooted at the folder where it exists."

**重要**: `AGENTS.md` のスコープは「そのファイルが存在するフォルダをルートとするディレクトリツリー全体」

> **優先順位**: "Instructions from AGENTS.md files deeper in the hierarchy take precedence when there are conflicts."

**重要**: より深い階層にある `AGENTS.md` の指示が、競合する場合には優先される

> **適用条件**: "For any file touched in the final patch, instructions from AGENTS.md files within that file's scope must be followed."

**重要**: 最終パッチで触れるすべてのファイルに対して、そのファイルのスコープに含まれる `AGENTS.md` ファイルの指示に従う必要がある

#### 実務への影響

- 親リポジトリを作業ディレクトリにした場合、子リポジトリの `AGENTS.md` は「そのファイルのスコープ外」となり、自動適用されない
- 子リポジトリ配下のファイルを編集する場合、子の `AGENTS.md` が「そのファイルのスコープ内」となるが、親で起動している限り自動読み込みはされない

---

### 2. OpenAI Codexにおける階層マージ

#### 読み込み順序（コミュニティ検証済み、2025-10-17確認）

Microsoft Learn（OpenAI Codex関連）およびコミュニティ情報より：

1. **ユーザーグローバル**: `~/.codex/AGENTS.md`（個人の全プロジェクト共通設定）
2. **リポジトリルート**: リポジトリルートの `AGENTS.md`（プロジェクト共有設定）
3. **作業ディレクトリ**: 現在の作業ディレクトリの `AGENTS.md`（タスク固有設定）

**マージ方式**: トップダウンでマージし、より具体的（深い階層）な設定が上書き・補完

**重要**: この「作業ディレクトリ」は起動時の `cwd`（カレントワーキングディレクトリ）を指す。親で起動している限り、子の `AGENTS.md` は「作業ディレクトリ」とみなされない。

---

### 3. Cursorにおけるプロジェクトスコープ

#### 公式仕様（2025-10-17確認）

[Cursor Rules Documentation](https://docs.cursor.com/ja/context/rules)より：

> "Rules for Agents: You can add instructions in Markdown format by adding an AGENTS.md, a simple alternative to `.cursor/rules`"

**重要**: Cursorでは `AGENTS.md` は `.cursor/rules` の簡易代替として扱われる

> "Project-specific rules: Place rules in `.cursor/rules/*.mdc` in your project root"

**重要**: プロジェクトルート（起動ディレクトリ）基準で解釈される

#### サブディレクトリルール

Cursorでは、サブディレクトリごとに `.cursor/rules/*.mdc` を配置することで、ディレクトリごとに異なるルールを適用可能。ただし、親ディレクトリから起動した場合、子ディレクトリのルールは自動適用されない。

---

## FAQ

### Q1: なぜ子リポジトリのAGENTS.mdが無視されるのか？

**A**: ツールの設計思想として、起動ディレクトリを「プロジェクトのルート」とみなすためです。

**理由**:

1. **シンプルさ**: 複数の `AGENTS.md` を自動統合すると、競合・優先順位の管理が複雑化
2. **予測可能性**: 起動場所でルールが確定するため、動作が明確
3. **パフォーマンス**: 大量のディレクトリを探索する必要がない

**対処法**: 親の `AGENTS.md` に明示的な読み込みルールを記載（本ガイド推奨）

---

### Q2: agentsmd.io仕様の「スコープ」と実際の挙動の違いは？

**A**: agentsmd.io仕様では「ファイルのスコープに含まれる `AGENTS.md` に従う」とありますが、実際のツール実装では「起動ディレクトリ基準」が優先されます。

**背景**:

- agentsmd.io仕様: 理想的なスコープルール（ファイルが属するディレクトリツリー基準）
- 実装（Codex/Cursor）: 起動ディレクトリ基準（パフォーマンス・シンプルさ重視）

**実務への影響**: 親で起動した場合、子の `AGENTS.md` は「理論上のスコープ内」でも自動適用されない。明示的読み込みが必要。

---

### Q3: 将来的に改善される見込みは？

**A**: 現時点で具体的なロードマップは確認できていませんが、以下の改善が期待されます。

**理想的な実装例**:

```json
// .codex/config.json または .cursor/settings.json
{
  "agentsMd": {
    "autoLoadSubdirectories": true,
    "scopeResolution": "file-based",  // ファイル基準のスコープ解決
    "subdirectories": [
      {
        "path": "./sub-repos/facility-user-app",
        "autoLoad": true
      }
    ]
  }
}
````

**現在のステータス**: 提案段階、実装時期は未定

---

### Q4: 横断的な修正はどうすればいいか？

**A**: 以下の2つのアプローチがあります。

#### アプローチ1: 親のAGENTS.mdに従って一括処理

```bash
# ユーザーの指示
全サブリポジトリの .gitignore に "*.log" を追加して
```

親の `AGENTS.md` のルールに従って各リポジトリを順番に処理します。

#### アプローチ2: 各子のAGENTS.mdを順番に読み込み

```bash
# ユーザーの指示
各サブリポジトリの AGENTS.md を読んで、
それぞれのルールに従って .gitignore を更新して
```

エージェントが各子の `AGENTS.md` を順番に読み込み、個別のルールに従って処理します。

**推奨**: 横断的な修正でも、できるだけアプローチ2を使用（各リポジトリのルール遵守）

---

### Q5: 他のツール（Windsurf、Claude Code、Cursor）との比較は？

**A**: マルチリポジトリ環境では、ツールごとに大きく挙動が異なります。

| ツール       | 設定ファイル                        | スコープ解決方式                     | 親から開いた時の子ルール適用 |
| ------------ | ----------------------------------- | ------------------------------------ | ---------------------------- |
| **Windsurf** | `.windsurfrules`                    | **編集ファイルベース（最近傍優先）** | ✅ **自動適用**              |
| OpenAI Codex | `AGENTS.md`                         | 起動ディレクトリベース（階層マージ） | ❌ 明示的読み込み必要        |
| Cursor       | `AGENTS.md` / `.cursor/rules/*.mdc` | 起動ディレクトリベース               | ❌ 明示的読み込み必要        |
| Claude Code  | `CLAUDE.md` / `.claude/agents/*.md` | 起動ディレクトリベース               | ❌ 明示的読み込み必要        |

#### Windsurfの優位性

Windsurfは**編集ファイルに最も近い`.windsurfrules`を自動的に適用**します。これにより、親リポジトリから起動していても、子リポジトリのファイルを編集する際は子のルールが自動適用されます。

**実務例**:

```
親リポジトリ/（親の.windsurfrulesで起動中）
└── sub-repos/
    └── facility-user-app/
        ├── .windsurfrules ← 編集時に自動適用 ✅
        └── src/LoginForm.tsx ← 編集対象
```

#### AGENTS.md / CLAUDE.md / .cursor/rules の制約

これらは**起動ディレクトリ基準**のため、親で起動している限り子のルールは自動適用されません。本ガイドで紹介している「明示的読み込み方式」が必要です。

**詳細情報**:

- Windsurfの`.windsurfrules`詳細: （未作成・今後追加予定）
- Claude Codeの`CLAUDE.md`詳細: `notes/claude_code/multi-repository-workspace-guide.md`を参照

---

### Q6: Claude CodeやWindsurfでもAGENTS.mdは使えるか？

**A**: **Windsurf は AGENTS.md をネイティブサポートしています**（2025-10-21 実証）。Claude Code は非対応で明示的な参照が必要です。

#### AGENTS.mdのネイティブサポート状況（2025-10-21時点）

| ツール       | AGENTS.md対応                       | 必要な対応                                      |
| ------------ | ----------------------------------- | ----------------------------------------------- |
| OpenAI Codex | ✅ **ネイティブサポート**           | そのまま使用可能                                |
| Cursor       | ✅ **ネイティブサポート**           | そのまま使用可能                                |
| **Windsurf** | ✅ **ネイティブサポート（実証済）** | **そのまま使用可能**（`.windsurfrules` は不要） |
| Claude Code  | ❌ 非対応                           | `CLAUDE.md`で明示的に参照                       |

> **2025-10-21 補足**: Windsurf の公式ドキュメントには記載がありませんが、実際の検証により `AGENTS.md` が自動的に Rules タブに表示され、ルールとして機能することを確認しました。`.windsurfrules` による明示的参照は不要です。

#### Claude Codeでの使用方法

```markdown
<!-- CLAUDE.md -->

# プロジェクトルール

## AGENTS.md準拠

このプロジェクトは AGENTS.md に記載されたコーディング規約に従います。

**作業開始前の必須手順**:

1. AGENTS.md を読み込む
2. 記載されたルールを厳密に遵守

<!-- 以下、Claude Code固有の設定 -->

## Subagent定義

...
```

#### Windsurfでの使用方法

**2025-10-21更新**: Windsurf は `AGENTS.md` をネイティブサポートしているため、**プロジェクトルートに `AGENTS.md` を配置するだけ**で自動認識されます。

```markdown
<!-- AGENTS.md（推奨） -->

# プロジェクトルール

## セットアップコマンド

- 依存関係インストール: `pnpm install`
- 開発サーバー起動: `pnpm dev`

## コーディング規約

- TypeScript strict mode
- 単一引用符、セミコロンなし
  ...
```

**従来の方法（`.windsurfrules` による明示的参照）**も引き続き使用可能ですが、通常は不要です：

```markdown
<!-- .windsurfrules（オプション） -->

- @AGENTS.md に従う
```

#### 推奨ファイル構成（2025-10-21更新）

```
プロジェクト/
├── AGENTS.md .................... Codex/Cursor/Windsurf用（ネイティブ）
├── CLAUDE.md .................... Claude Code用（AGENTS.md参照を含む）
└── .cursor/rules/*.mdc ........... Cursor用追加ルール（オプション）
```

**重要**:

- **Codex/Cursor/Windsurf**: `AGENTS.md` をそのままルールファイルとして認識
- **Claude Code**: `AGENTS.md` を「参照すべきドキュメント」として `CLAUDE.md` から参照する必要あり

---

## 出典一覧

### 公式ドキュメント

| 項目                        | URL                                                                                                                                              | 確認日     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| agentsmd.io公式             | [https://agentsmd.io/](https://agentsmd.io/)                                                                                                     | 2025-10-17 |
| Cursor Rules公式            | [https://docs.cursor.com/ja/context/rules](https://docs.cursor.com/ja/context/rules)                                                             | 2025-10-17 |
| Microsoft Learn (Codex関連) | [https://learn.microsoft.com/ja-jp/azure/ai-foundry/openai/how-to/codex](https://learn.microsoft.com/ja-jp/azure/ai-foundry/openai/how-to/codex) | 2025-10-17 |

### コミュニティリソース

| 項目             | URL                                                                                                    | 確認日     |
| ---------------- | ------------------------------------------------------------------------------------------------------ | ---------- |
| OpenAI Codex紹介 | [https://openai.com/ja-JP/index/introducing-codex/](https://openai.com/ja-JP/index/introducing-codex/) | 2025-10-17 |

---

## 更新履歴

- **2025-10-17**: 初版作成（公式仕様・コミュニティ情報検証済み）
- **2025-10-17**: agentsmd.io仕様、Codex階層マージ、Cursorプロジェクトスコープを明記
- **2025-10-21**: 実証済みベストプラクティスを追加（マルチサービス環境での成功事例）
- **2025-10-21**: Cursorのトークンクレジット制に関する注記を追加
- **2025-10-21**: 最新の確認フロー（重複実装防止、不明点がある場合のみ確認）を反映
- **2025-10-21**: **Windsurf の AGENTS.md ネイティブサポートを実証・反映**（公式未記載だが実装として存在）

---

_このガイドは2025年10月21日時点の公式情報・コミュニティ情報・実証済みベストプラクティスに基づいています。OpenAI CodexやCursorは継続的に進化しているため、最新情報は必ず公式ドキュメントを参照してください。_
