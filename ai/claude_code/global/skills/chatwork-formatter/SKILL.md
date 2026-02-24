---
name: chatwork-formatter
description: Use when markdown content must be converted to ChatWork-readable format and presented as a copyable block in the conversation; When NOT to use: when the destination supports markdown rendering or when the task is not ChatWork-related; Trigger Keywords: [ChatWork, CW, チャットワーク, CW用, ChatWork用, CWで共有, CWの返信].
---

# chatwork-formatter

## When to use

- MarkdownテキストをChatWorkに貼り付けたい場合（mdが展開されないため変換が必要）。
- 「CWで共有したい」「CWの返信文を考えて」と依頼された場合。
- レポートや手順書をChatWorkで読みやすく送りたい場合。

## When NOT to use

- 送信先がGitHub/Notion/Slackなどmd展開が効く場合。
- すでにChatWork記法に変換済みの場合。

## Trigger Keywords

- ChatWork
- CW
- チャットワーク
- CW用
- CWで共有
- CWの返信

## Procedure

1. 変換対象のMarkdownを受け取る（ユーザーの入力・ファイル指定どちらも可）。
2. 下記「変換規則」に従い全文を変換する。
3. 構造（見出し・セクション）がある場合は `[info]...[/info]` で全体を囲む。
4. 「👇 CWにそのままコピーしてください」と1行出力する。
5. 変換済みテキストをコードブロックで囲んで続けて提示する。ファイルへの保存はしない。

## 変換規則

### タグの使用条件（重要）

- `[title]` は **`[info]` 内でのみ** 使用可。単独では使わない。
- `[info]` は単独で使用可。`[title]` を伴わなくても構わない。
- `[code]` `[hr]` は単独で使用可。

### 見出し変換

| 状況                    | Markdown | ChatWork                                   |
| ----------------------- | -------- | ------------------------------------------ |
| `[info]` で囲む場合     | `# H1`   | `[info][title]H1[/title]...内容...[/info]` |
| `[info]` を使わない場合 | `# H1`   | `【H1】`（前後に空行）                     |
| どちらでも              | `## H2`  | `▼ H2`（前後に空行）                       |
| どちらでも              | `### H3` | `■ H3`                                     |

### その他の変換

| Markdown                 | ChatWork                                   |
| ------------------------ | ------------------------------------------ |
| `- item` / `* item`      | `・item`                                   |
| `  - subitem`（ネスト）  | `　・subitem`（全角スペース+中点）         |
| `1. item`                | そのまま保持                               |
| `**bold**`               | `**` を除去、テキストのみ                  |
| `*italic*`               | `*` を除去、テキストのみ                   |
| `` `inline code` ``      | バッククォートを除去、テキストのみ         |
| ` ```コードブロック``` ` | `[code]...[/code]`                         |
| `---`（水平線）          | `[hr]`                                     |
| `[text](url)`            | `text ( url )`                             |
| `> 引用`                 | `　` +テキスト（全角スペースでインデント） |

## 優先ルール

- ChatWork で表示できない記法は削除・平文化する（崩れたまま渡さない）。
- 絵文字（`(bow)` `(roger)` `(cracker)` など）はユーザーから指示された場合のみ追加する。無指示では追加しない。
- `[info]` は構造があるときのみ使う。短い1〜2文ならプレーンテキストで十分。

## Output Contract

- 会話内に以下の形式で提示する（ファイル保存禁止）:

👇 CWにそのままコピーしてください

```
[変換済みテキスト]
```

- 変換の補足説明は出力ブロックの外に最小限（2行以内）で添える。
- 元の意味・構成は変えない。

## Examples

### Example 1

Input: ユーザーが「以下をCW用に変換して」と送ってきたMarkdown

```markdown
## 進捗報告

- 設計完了
- 実装中
  - APIレイヤー完了
  - DBレイヤー未着手

[詳細](https://example.com)
```

Output（会話内に提示）:

👇 CWにそのままコピーしてください

```
[info]
▼ 進捗報告

・設計完了
・実装中
　・APIレイヤー完了
　・DBレイヤー未着手

詳細 ( https://example.com )
[/info]
```

---

### Example 2

Input: 「CWの返信文を考えて。内容は：承認した旨と次のステップを伝える」

Output（会話内に提示）:

👇 CWにそのままコピーしてください

```
承認しました。

次のステップは以下の通りです。
・〇〇 の対応をお願いします。
・完了後にこちらのスレッドへご連絡ください。
```

---

### Example 3

Input: 「以下をCW用に」。内容はH1見出し＋番号付きリスト＋bashコードブロック2つを含むMarkdown

Output（会話内に提示）:

👇 CWにそのままコピーしてください

```
[info]
[title]セットアップ手順[/title]

1. 依存をインストール
[code]npm install[/code]

2. 起動
[code]npm run dev[/code]
[/info]
```
