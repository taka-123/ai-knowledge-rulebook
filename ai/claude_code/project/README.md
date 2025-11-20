# プロジェクト固有の Claude Code 設定

このテンプレートは、記事「[チームのCLAUDE.mdが勝手に育つ - Hook機能での自動化](https://zenn.dev/appbrew/articles/e2f38677f6a0ce)」の構成に合わせています。以下のように **プロジェクトルート直下に `bin/` と `.claude/` を配置** してください。

## 配置場所

```
your-project/
├── .claude/
│   ├── settings.json                 # Hook設定
│   └── commands/
│       └── suggest-claude-md.md      # スラッシュコマンド定義
├── bin/
│   └── suggest-claude-md-hook.sh     # Hook実行スクリプト
├── src/
└── ...
```

## CLAUDE.md 自動更新提案機能

会話履歴を自動分析して、CLAUDE.mdへの追記を提案する仕組みです。

### 構成ファイル

- [.claude/settings.json](.claude/settings.json) - Hook設定（SessionEnd/PreCompactで自動実行）
- [bin/suggest-claude-md-hook.sh](bin/suggest-claude-md-hook.sh) - Hook実行スクリプト
- [.claude/commands/suggest-claude-md.md](.claude/commands/suggest-claude-md.md) - スラッシュコマンド定義

### 動作タイミング

1. **SessionEnd** - Claude Codeを終了したとき
2. **PreCompact** - 会話履歴が圧縮される直前

### 手動実行

```bash
/suggest-claude-md
```

### ログ確認

分析結果は `/tmp/suggest-claude-md-{会話ID}-{タイムスタンプ}.log` に保存されます。

### 検出される3つのパターン

1. **プロジェクト独自のルール** - 「〜ではなく〜を使ってください」
2. **同じような修正指示の繰り返し** - 同種の修正が2回以上出現
3. **関連箇所で揃えるべきパターン** - 複数箇所での統一を指示

### ワークフロー

1. Claude Codeで開発作業
2. セッション終了時/コンテキスト圧縮前に自動分析
3. ターミナルに提案内容が表示される
4. 適切と判断したら「この内容をCLAUDE.mdに追記して」と指示
5. コード変更と同じPRに含めてレビュー

### 参考記事

- [これって書くべき？　チームでCLAUDE.mdや.cursor/rulesを育てる](https://zenn.dev/appbrew/articles/7eb12fff5738f4)
- [チームのCLAUDE.mdが勝手に育つ - Hook機能での自動化](https://zenn.dev/appbrew/articles/e2f38677f6a0ce)
