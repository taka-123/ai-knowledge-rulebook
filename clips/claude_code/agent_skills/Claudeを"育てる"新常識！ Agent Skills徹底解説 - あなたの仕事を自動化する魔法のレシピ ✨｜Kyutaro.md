---
title: "Claudeを\"育てる\"新常識！ Agent Skills徹底解説 - あなたの仕事を自動化する魔法のレシピ ✨｜Kyutaro"
source: "https://note.com/kyutaro15/n/nfcc15522626f"
author:
  - "[[Kyutaro]]"
published: 2025-10-17
created: 2025-10-19
description: "属人化をやめたい。品質を揃えたい。スピードは落とさない。 Agent Skillsは、現場のノウハウを「再現可能な資産」に変えます。プロンプトではなく標準手順×コードで積み上げるから、新人でもベテランと同じ結果に。それを実現するのが、Anthropicの画期的な機能、「Agent Skills」です。  この記事は、導入判断に必要な安全性・運用設計・環境別のリスクと効率、そして即導入できるサンプルまで一気通貫で解説し、あなたが今日からでも「AIを育てる」ための、実践的な設計図を提供します。    1. そもそもAgent Skillsって何？ - AIの新しい「引き出し」術 🗄️  A"
tags:
  - "clippings"
---
![見出し画像](https://assets.st-note.com/production/uploads/images/222783048/rectangle_large_type_2_a0a019bd0aacd23127f022921615c836.png?width=1200)

## Claudeを"育てる"新常識！ Agent Skills徹底解説 - あなたの仕事を自動化する魔法のレシピ ✨

[Kyutaro](https://note.com/kyutaro15)

---

属人化をやめたい。品質を揃えたい。スピードは落とさない。
**Agent Skills** は、現場のノウハウを「再現可能な資産」に変えます。プロンプトではなく **標準手順×コード** で積み上げるから、 **新人でもベテランと同じ結果** に。それを実現するのが、Anthropicの画期的な機能、「 **Agent Skills** 」です。

この記事は、導入判断に必要な **安全性・運用設計・環境別のリスクと効率** 、そして **即導入できるサンプル** まで一気通貫で解説し、あなたが今日からでも「 **AIを育てる** 」ための、実践的な設計図を提供します。

---

### 1\. そもそもAgent Skillsって何？ - AIの新しい「引き出し」術 🗄️

Agent Skillsとは、端的に言えば「 **AIに特定のタスクを教え込むための、手順書と道具箱をまとめたフォルダ** 」です。

構造はシンプルで、SKILL.mdという中心的な指示書ファイルと、それに関連する参考資料（Markdown）、データ、テンプレート、そして実行可能なPythonスクリプトで構成されます。

最大の特徴は、これをClaudeに登録しておくと、ユーザーが明示的に命令しなくても、 **Claude自身が会話の流れから「このタスクには、あのスキルが役立ちそうだ」と判断し、自律的にスキルを呼び出して実行してくれる** 点（モデル主導の起動）にあります。

---

### 2\. なぜ今、 Agent Skillsに注目すべきなのか？ - プロンプトのその先へ

Agent Skillsは、MCPが抱えていた課題（コンテクストの消費量が多過ぎるなど）を「 **段階的開示** （ **Progressive Disclosure** ）」という賢い仕組みで解決します。

**1.インデックス**: Claudeはまず、全スキルの **名前** と **説明文** （SKILL.mdのYAMLフロントマター）だけを読み込みます。

![画像](https://assets.st-note.com/img/1760649998-ye2zDvWTH9n870NsZuhpIacU.png?width=1200)

**2.起動**: 対話の中で関連性が高いと判断すると、初めてSKILL.md本体を読み込みます。

**3.深掘り**: さらに必要であれば、関連ファイルやスクリプトを読み込み、実行します。

![画像](https://assets.st-note.com/img/1760650025-PDrbaheLTnR84yCcQF0fUv73.png?width=1200)

これにより、常に最小限のコンテキストで動作しつつ、必要に応じて膨大な知識やツールを瞬時に引き出せる、驚異的な効率性を実現しています。

![画像](https://assets.st-note.com/img/1760650058-1JB9YZp6HW0aCwuInoPO5tqV.png?width=1200)

---

### 3\. Agent Skillsの核心ポイント - 再現性・無限コンテキスト・コード実行

Agent Skillsは、以下の3つの強力な特徴を持っています。

- **再現性と一貫性**: プロンプトのように属人化せず、「 **コード化された手順** 」として組織のノウハウをAIに移植し、誰でも同じ品質の成果を得られます。
![画像](https://assets.st-note.com/img/1760650169-dUPEYkTMlgvFG94JXetxSROu.png?width=1200)

- **事実上の「無限コンテキスト」**: スキルフォルダ内に膨大な資料を配置し、Claudeに必要な部分だけを読ませることで、コンテキスト長の制約を実質的に乗り越えます。
- **信頼性の高いコード実行**: LLMが苦手な厳密な処理をPythonスクリプトに任せることで、AIの創造性とコードの信頼性を両立させます。
![画像](https://assets.st-note.com/img/1760650126-DxtNbaGHoKneRIuE7LTh2wOc.png?width=1200)

---

### 4\. 重要: 3つの実行環境の違いを理解する (API vs Claude.ai vs ローカル) 🔬

コード実行を伴うスキルを扱う上で、実行環境は **3種類** あり、それぞれに決定的な違いがあります。タスクの目的に応じて最適な環境を選ぶ必要があるため、これらの特性を必ず理解しておきましょう。

**① API経由の実行環境** ☁️

**プロダクション（製品）環境での利用** を想定しており、セキュリティと再現性が最優先されます。

- **実行場所**: Anthropicの管理する安全なクラウド上のサンドボックス
- **ネットワーク**: **完全遮断** 。外部へのいかなる通信もできません。
- **パッケージ管理**: pip installは **不可** 。追加のライブラリはインストールできません。
- **利用可能なライブラリ**: pandas, numpy, openpyxl, pypdfなど、厳選されたライブラリのみが **プリインストール** されています。
- **主なユースケース**: 安全性が求められるアプリケーションへの組み込み、一貫した動作を保証したい定型タスクの自動化。

---

**② Claude.ai (Web UI) 経由の実行環境** 🌐

**実験やプロトタイピング** に適した、柔軟性の高い環境です。

- **実行場所**: Anthropicの管理するクラウド上のサンドボックス
- **ネットワーク**: **利用可能** 。外部のWebサイトやAPIにアクセスできます。
- **パッケージ管理**: **PyPIやnpm、GitHubリポジトリから動的にパッケージをインストール可能** です。
- **主なユースケース**: 最新のライブラリを試す、外部APIと連携するスキルを素早く開発する。

---

**③ Claude Code (ターミナル) によるローカル実行環境** 💻

**開発者の手元にあるマシン環境そのもの** を利用します。最もパワフルで制約がありません。

- **実行場所**: **あなた自身のPC（ローカルマシン）**
- **ネットワーク**: **あなたのPCのネットワーク設定に準拠** します。インターネットや社内ネットワークへのアクセスも自由です。
- **パッケージ管理**: **制限なし** 。あなたのPCにインストールされている **あらゆるツールやライブラリ** （git, docker, pip, npmなど）をスキルから直接利用できます。
- **主なユースケース**: ローカルファイルへのアクセス、バージョン管理システム（Git）との連携、ローカルの開発サーバーやデータベースの操作など、開発ワークフローに深く根差したタスク。

---

### 5\. 実践！スキルを作ってみよう - PDFフォーム解析スキルのハンズオン 🛠️

「 **PDFの入力フォームフィールドを抽出しJSONで出力する** 」スキルを作成します。pypdfはプリインストール済みなので、APIとclaude.aiの両方で動作します。

**ファイル構造**

```
pdf-fields/
├── SKILL.md
├── forms.md
└── extract_fields.py
```

**ファイル①: pdf-fields/SKILL.md**

```python
---
name: PDF form fields
description: Extract and inspect fillable text fields in a PDF, saving them to JSON. Use when asked to analyze or fill PDF forms.
---
# PDF Form Fields Skill
## クイックスタート
ユーザーがPDFフォームの調査を依頼してきた場合、以下のコマンドを実行してください:
\`\`\`bash
python ./extract_fields.py "<input.pdf>" "fields.json"
```

その後、\`fields.json\`を開き、フィールド名を確認します。
入力戦略などの詳細は\`forms.md\`を参照。

**ファイル②: pdf-fields/forms.md**

```javascript
**File: \`pdf-fields/forms.md\`**
\`\`\`markdown
# Filling strategy & edge cases

1) Prefer exact field names from \`fields.json\` when populating values.
2) If \`get_form_text_fields()\` returns empty but a form exists, fall back to \`get_fields()\`
   to include non-text widgets (checkboxes, dropdowns), then map them explicitly.
3) When keys are duplicated, \`pypdf\` may suffix them (e.g., \`.2\`, \`.3\`)—normalize keys before filling.
4) Confirm final PDF rendering by writing a filled copy and verifying values on each target page.
```

（内容はSKILL.mdを補足するもので、フォーム入力の戦略やエッジケースなどを詳細に記述します）

**ファイル③: pdf-fields/extract\_fields.py**

```python
#!/usr/bin/env python3
"""
Extract text form fields from a PDF and write them to JSON.

Usage:
  python extract_fields.py <input.pdf> <output.json>
"""

import sys, json
from pypdf import PdfReader

def main():
    if len(sys.argv) != 3:
        print("Usage: python extract_fields.py <input.pdf> <output.json>")
        sys.exit(1)

    input_pdf, output_json = sys.argv[1], sys.argv[2]

    reader = PdfReader(input_pdf)

    # Prefer text fields for a clean mapping; falls back if none found.
    fields = reader.get_form_text_fields()  # returns {name: value, ...} for text fields
    if not fields:
        # Broader (includes non-text widgets); returns richer objects
        # which you may want to post-process before JSON dumping.
        fields = reader.get_fields() or {}

        # Convert values to plain JSON-serializable forms where possible
        plain = {}
        for k, v in fields.items():
            # Many fields are dict-like; try to extract '/V' (value)
            try:
                plain[k] = getattr(v, "value", None) or v.get("/V", None) if hasattr(v, "get") else None
            except Exception:
                plain[k] = None
        fields = plain

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(fields, f, indent=2, ensure_ascii=False)

    print(f"Wrote {output_json} with {len(fields)} field(s).")

if __name__ == "__main__":
    main()
```

（pypdfライブラリを使用し、PDFからフォームフィールドを抽出してJSONファイルに書き出す、基本的なエラーハンドリングを備えたPythonスクリプトです）

---

### 6\. 作ったスキルをどう使う？ - ３つの実行環境を徹底解説

**1\. Claude.ai (Web UI)** 💻

pdf-fieldsフォルダを **zip圧縮** し、「 **設定** 」→「 **機能** 」→「 **スキル** 」からアップロードします。「 **コード実行とファイル作成** 」の有効化が必須です。

![画像](https://assets.st-note.com/img/1760684715-lVUntaINwg3ET2hOGJzW7R0P.png?width=1200)

Agent Skills は何もスキルをアップロードしなくても、有効化するだけで、既に沢山のスキルがデフォルトですぐに試せますので、是非有効にしてみてください！

**2\. Claude Code (ターミナル)** 🧑💻

pdf-fieldsフォルダを~/.claude/skills/（個人用）か./.claude/skills/（プロジェクト用）に配置すれば、claudeコマンドが自動で認識します。

**3\. Claude API** 🔌

アプリケーションに組み込むための、最もパワフルな方法です。

- **モデル指定**: Skillsと最新のコード実行ツールは、claude-sonnet-4-5-20250929のような **Claude 4.x系列のモデル** で利用する必要があります。
- **ベータヘッダ**: スキル、コード実行、そして多くの場合ファイルを扱うため、以下の **3つのベータ指定が推奨** されます。
- **制限事項**: 1リクエストに含められるカスタムスキルは **最大8個** 、スキルの合計サイズは **8MBまで** です。
- **バージョニング**: プロダクション環境では、version: "1"のように特定のバージョンに固定することで、安定した動作を保証できます。（開発中はversion: "latest"が便利です）

```python
# APIでスキルを利用するPythonコードの例
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    # Skills互換のモデルを指定
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    # ファイル操作も考慮し、必要なベータヘッダをすべて指定
    betas=["code-execution-2025-08-25", "skills-2025-10-02", "files-api-2025-04-14"],
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": "skill_xxxxxxxx",
                "version": "1" # プロダクションではバージョン固定を推奨
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "添付のPDFからフォームフィールドを抽出してください。"
        # ここにファイル添付の処理が入る
    }],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)

print(response.content)
```

Skillが作成したファイルは **Files API** でfile\_idを用いてダウンロードできます。

---

### 7\. 一流のスキル職人になるための「秘伝のタレ」

- **説明文はAIへの最高のプレゼン**: descriptionにスキルが「 **何をするか** 」「 **いつ使うべきか** 」を具体的に書きましょう。これが発見可能性の鍵です。
- **API向けには自己完結を意識**: APIコンテナにはネットワークがありません。必要なデータやライブラリはすべてスキル内に含めるか、プリインストールされたものを使いましょう。

---

### 8\. すぐに使える！Anthropic公式ビルトインスキル

カスタムスキルを作る前に、Anthropicが公式に提供している強力なビルトインスキルを試してみましょう。これらはAPIやclaude.aiでIDを指定するだけで利用できます。

[Get started with Agent Skills in the API - Claude Docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)

- **PowerPoint (pptx)**: データからプレゼンテーションを生成。
- **Excel (xlsx)**: 複雑なデータ分析やグラフ作成。
- **Word (docx)**: 長文のレポートや契約書の生成・編集。
- **PDF (pdf)**: PDFからの情報抽出や要約。

これらを活用するだけでも、多くの定型業務を自動化できるはずです。

---

### 9\. 安全なスキル活用のために - セキュリティの心得 🛡️

スキルは非常に強力ですが、その力を安全に使うための注意点があります。

- **未知のスキルは監査を**: 第三者が作成したスキルを利用する際は、必ずSKILL.mdやスクリプトの中身を確認し、意図しない動作（データの外部送信など）がないか監査してください。
- **サプライチェーンリスク**: claude.aiで外部パッケージをインストールする場合、そのパッケージ自体の信頼性にも注意が必要です。
- **プロンプトインジェクション**: SKILL.mdにユーザーからの入力をそのまま組み込むような設計は避けるべきです。悪意のある指示が実行されるリスクがあります。

---

### 10\. Agent Skillsが拓く、AIエージェントの未来 🚀

Agent Skillsは、AIが自らの能力を拡張していく未来への第一歩です。将来的には、複数のスキルが協調動作したり、さらにはAI自身が成功体験から新たなスキルを生成したりする世界が訪れるでしょう。これは、AI開発のパラダイムを根底から変える可能性を秘めています。

---

### 11\. まとめ：スキルで創る、あなただけの最強アシスタント

Agent Skillsは、AIとの関わり方を「 **お願いする** 」から「 **育てる・設計する** 」へと進化させる、パワフルなフレームワークです。

- 🎯 **ワークフローの体系化**: あなたのノウハウを、再利用可能な形でAIに教え込める。
- 🔬 **環境に応じた設計**: APIの堅牢性とclaude.aiの柔軟性を理解し、最適なスキルを開発できる。
- 🛡️ **安全な運用**: セキュリティを意識することで、強力な能力を安心して活用できる。

---

### 12\. Agent Skillsを系譜的にどう位置付けるべきか？\[2025/10/17 15:30追記\]

では、この技術は系譜的に見てどのように位置づけて見るべきでしょうか？大変参考になる2つのXの投稿をご紹介いたします。

これら Cursor Rules や MCP との比較、流れでAgent Skills の位置づけを見ると理解しやすいかと思います。
Cursor Rules も MCP も現在のコンテキストエンジニアリング技術の大きな潮流を作ってきました。
これらの弱点を克服して作られた Agent Skills がいかに重要な技術で、スコープの広い技術であるのかがお分かりいただけたかと思います。

※なお、上記は **Agent Skillsが Cursor Rules や MCPの上位互換になるという意味ではありません** 。それぞれに得手不得手があります。例えば、Cursor Rules はIDEをベースとしていますし、MCPにはAuthの仕組みがあります。あくまでこの系譜で見てみると理解しやすいという説明ですのでご注意ください。 \[2025/10/18 14:20追記\]

---

### あとがき

最後までお読みいただき、本当にありがとうございました。

Agent Skillsは、これまでのプロンプトエンジニアリングやコンテキストエンジニアリングの一つの到達点といえるものだと思います。勿論まだまだ改善されていくと思いますが、コンパクトで非常に柔軟な設計になっており、Claudeに限らずこの方式が今後普及していくのではないかと考えています。

この記事で得た知識を元に、ぜひあなた自身の手で、あなただけの「 **最強の相棒** 」を育ててみてください。その小さな一歩が、あなたの仕事やプロジェクトに、大きな変革をもたらすはずです！

「いいね」や「コメント」をいただけると嬉しいです！また、気になる点があればお気軽にコメントしてください。

### 参考リンク

[Equipping agents for the real world with Skills \\ Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

[Claude Skills: Customize AI for your workflows \\ Anthropic](https://www.anthropic.com/news/skills)

[Agent Skills - Claude Docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

[Skill authoring best practices - Claude Docs](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

[claude-cookbooks/skills at main · anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks/tree/main/skills)

---

## 著者プロフィール

AI技術の解説を行っている @kyutaro15 です。
以下の記事のように、重要な最新AI技術をほぼ最初期にできるだけ分かりやすく解説する活動を続けてきております。

### Cursor の紹介 \[2023年8月31日 00:34\]

コンテキストエンジニアリングの源流ともいえる Cursor。今では Cursor を使う人は非常に多いですが、当時、 Cursor を使う人はほぼ皆無でした。私は当時からCursorの可能性とその魅力にとりつかれており、いち早くCursorを紹介させていただきまた。

### RAG（Retrieval Augumented Generation）の紹介 \[2023年9月10日 23:59\]

今でこそAIに携わる方でRAGと言う言葉を知らない人はいませんが、まだ研究論文以外でRAGと言う言葉が一般的にほとんど知られていなかった時期に、RAGを解説する記事を書きました。

### 「Dify危険じゃないか？」と言う噂を検証して、DifyのCEOから直切感謝される\[2024年5月10日 20:08\]

今では世界中で広く使われているDifyですが、当時は「危ないのではないか？」と言う憶測がXで噂されていました。その噂を検証する記事を書き、DifyのLuyu Zhang CEOからnoteの記事に直接感謝のコメントをいただきました。Dify は 世界中で最も有名なAIツールの1つとなっております。

### MCP（Model Context Protocol）の世界初？の解説記事を書く\[2024年11月26日 02:24\]

本記事の源流の1つともいえるMCP技術が発表された時、その可能性に驚き、数十分という超特急で記事を書きました(笑)恐らく世界初のMCP解説記事ではないかと思います。
その応用範囲は広いけれども、MCPは基礎的（プロトコル）で理解するのが難しい技術だったため、非エンジニアにもできるだけ分かりやすいように解説記事を書きました。今では、MCPは世界中の誰もが使う、コンテキストエンジニアリングの基礎的な技術になりました。

### その他、重要なAI技術をいち早く紹介する記事を執筆

その他にも、AIに関する重要な技術をいち早く紹介しております。皆さまからたくさんのいいねを押していただき、本当にありがたいです。

もし気になっていただけたら、このアカウントをフォローしていただけるとありがたいです。

また、note以外でも、XでAIに関する独自の視点で様々な発信を行っておりますので、そちらもフォローしていただけると大変嬉しいです。

最近では、アジャイル開発とバイブコーディングに関する書籍の監修もしております。急速な時代の変化に流されにくい、より本質的な視点から書かれた骨太の本です。

[**アジャイル×バイブコーディングの未来: AI時代のソフトウェア開発と 時間を越えるポータブルスキル 概論編 ゴールファースト・テック (シンギュラリティ志向ライフ)** *amzn.asia*](https://amzn.asia/d/hX6QhEo)

[*800 円* (2025年10月18日 10:50時点](https://amzn.asia/d/hX6QhEo)

[

Amazon.co.jpで購入する

](<https://amzn.asia/d/hX6QhEo>)

今後とも、是非よろしくお願いいたします。

Claudeを"育てる"新常識！ Agent Skills徹底解説 - あなたの仕事を自動化する魔法のレシピ ✨｜Kyutaro
