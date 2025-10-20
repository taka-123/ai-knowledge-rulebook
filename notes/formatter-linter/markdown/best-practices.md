# Markdown フォーマット・リント ベストプラクティス (2025年10月版)

最終更新: 2025-10-20

## 基本原則

**「フォーマット(見た目)はPrettierに、構文・品質チェックはmarkdownlintに完全に分離・特化させる」**

この設計は以下の公式ソースで推奨されています：

- [markdownlint 公式ドキュメント - Prettier との併用](https://github.com/DavidAnson/markdownlint/blob/main/doc/Prettier.md)
- [Joshua K. Goldberg (typescript-eslint メンテナー) のブログ](https://www.joshuakgoldberg.com/blog/configuring-markdownlint-alongside-prettier/)

## Prettier 3.4 の重要な変更点

### CJK スペーシングの挙動変更（2024年11月リリース）

**Prettier 3.3 以前:**

- CJK文字（日本語・中国語）と英数字の間に自動的にスペースを挿入
- `私はJavaScriptが好きです` → `私は JavaScript が好きです`
- `100円` → `100 円`

**Prettier 3.4 以降（現在の仕様）:**

- CJK文字と英数字の間にスペースを**挿入しない**
- `私はJavaScriptが好きです` → `私はJavaScriptが好きです`（変更なし）
- `100円` → `100円`（変更なし）

**変更理由:**

- CSS Text Module Level 3/4 の仕様に準拠
- ブラウザレンダリングとの整合性向上
- Markdown → HTML 変換時の不要な改行・スペース問題を解消

**参照:** [Prettier 3.4 リリースノート](https://prettier.io/blog/2024/11/26/3.4.0)

## 推奨設定

### 1. VSCode 設定 (`.vscode/settings.json`)

エディタのデフォルトフォーマッターをPrettierに統一：

```json
{
  // 🎨 全言語のデフォルトフォーマッターをPrettierに指定
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,

  // 📄 Markdown設定
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.wordWrap": "on",
    "editor.wordWrapColumn": 80
  },

  // 🗂️ YAML設定
  "[yaml]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[yml]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },

  // 📋 JSON設定
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[jsonc]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },

  // 🔧 Markdownlint設定（Linter として動作）
  "markdownlint.config": {
    "extends": "./.markdownlint.jsonc"
  }
}
```

### 2. Prettier 設定 (`.prettierrc.json`)

日本語可読性を優先し、`proseWrap: "preserve"` を使用：

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "singleQuote": true,
  "trailingComma": "es5",
  "endOfLine": "lf",

  "overrides": [
    {
      "files": "*.md",
      "options": {
        "printWidth": 80,
        "proseWrap": "preserve"
      }
    }
  ]
}
```

### 3. Markdownlint 設定 (`.markdownlint.jsonc`)

Prettier と競合するフォーマットルールを無効化：

```jsonc
{
  "extends": "markdownlint/style/prettier",
  "default": true,

  // プロジェクト固有の無効化ルール（必要に応じて調整）
  "MD013": false, // 行長制限
  "MD024": false, // 重複見出し
  "MD025": false, // 複数H1見出し
  "MD033": false, // インラインHTML
  "MD040": false, // コードブロック言語指定強制
  "MD041": false, // 最初の行が見出し強制
  "MD051": false, // アンカーリンク
}
```

**`extends: "markdownlint/style/prettier"`** により、以下のルールが自動的に無効化されます：

- フォーマット関連ルール（MD022, MD036, no-hard-tabs, no-trailing-spaces など）

### 4. YAMLLint 設定 (`.config/.yamllint.yml`)

Prettier と競合するフォーマットルールを無効化：

```yaml
extends: default

rules:
  # === Prettierと競合するため無効化 ===
  line-length: disable
  quotes: disable
  braces: disable
  brackets: disable
  colons: disable
  commas: disable

  # === Prettierと設定を合わせる ===
  indentation:
    spaces: 2 # Prettier の tabWidth と一致
    indent-sequences: consistent
    check-multi-line-strings: false

  # === YAMLの品質担保 ===
  key-duplicates: enable # 重複キー検出（最重要）
  trailing-spaces: enable
```

## 実行フロー

### 開発時（VSCode）

1. ファイル保存時に Prettier が自動フォーマット
2. markdownlint 拡張機能が品質チェック（リアルタイム）

### コマンドライン

```bash
# フォーマット
npm run format           # 全ファイルを Prettier でフォーマット
npm run format:check     # フォーマットチェックのみ

# Lint
npm run lint:md          # markdownlint で品質チェック
npm run lint:yaml        # yamllint で品質チェック

# 一括処理
./format.sh fix          # フォーマット + 修正
./format.sh check        # チェックのみ
```

### CI/CD

1. Prettier format check（フォーマット検証）
2. markdownlint（品質チェック）
3. yamllint（品質チェック）
4. JSON Schema 検証
5. Gitleaks（秘密情報スキャン）

## 役割分担まとめ

| ツール           | 役割                       | 対象                      |
| ---------------- | -------------------------- | ------------------------- |
| **Prettier**     | フォーマット（見た目）     | Markdown, YAML, JSON など |
| **markdownlint** | 品質チェック（構文・構造） | Markdown                  |
| **yamllint**     | 品質チェック（構文・構造） | YAML                      |

## トラブルシューティング

### Q1: Prettier が Markdown を整形しない

**A:** `.vscode/settings.json` で `"[markdown]"` の `defaultFormatter` が `esbenp.prettier-vscode` になっているか確認してください。

### Q2: markdownlint と Prettier が競合する

**A:** `.markdownlint.jsonc` に `"extends": "markdownlint/style/prettier"` を追加してください。

### Q3: CJK スペーシングが自動挿入されない

**A:** Prettier 3.4 以降では、これは**正常な動作**です。CJK スペーシングは挿入されなくなりました。古いバージョンでは挿入されていましたが、CSS 仕様準拠のため変更されました。

### Q4: 既存ファイルが大量にフォーマット変更される

**A:** 以下の手順で段階的に適用することを推奨：

1. まず設定ファイルのみ更新
2. 新規ファイルから適用開始
3. 既存ファイルは必要に応じて個別に整形
4. または、一括フォーマット後に Git で差分確認

## 参考リンク

- [Prettier 公式ドキュメント](https://prettier.io/docs/en/)
- [Prettier 3.4 リリースノート](https://prettier.io/blog/2024/11/26/3.4.0)
- [markdownlint ルール一覧](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- [markdownlint と Prettier の併用](https://github.com/DavidAnson/markdownlint/blob/main/doc/Prettier.md)
- [Configuring Markdownlint Alongside Prettier](https://www.joshuakgoldberg.com/blog/configuring-markdownlint-alongside-prettier/)
