---
title: "Claude Skills の概要｜npaka"
source: "https://note.com/npaka/n/n6e221d209d90"
author:
  - "[[npaka]]"
published: 2025-10-17
created: 2025-10-19
description: "以下の記事が面白かったので、簡単にまとめました。   ・Introducing Claude Skills    1. Claude Skills の概要  「Skills」は、「Claude」が必要に応じて読み込むことができる「指示」「スクリプト」「リソース」を含むフォルダです。  「Claude」は、手元のタスクに関連する場合にのみ「Skills」にアクセスします。「Skills」を使用すると、Excel での作業や組織のブランドガイドラインの遵守といった特殊なタスクをより効率的に実行できるようになります。    Claudeアプリでは、スプレッドシートやプレゼンテーションなどのフ"
tags:
  - "clippings"
---
![見出し画像](https://assets.st-note.com/production/uploads/images/222820946/rectangle_large_type_2_9d262e23c5657b1f3c718f697bebf29f.png?width=1200)

## Claude Skills の概要

[npaka](https://note.com/npaka)

以下の記事が面白かったので、簡単にまとめました。

> **・** [**Introducing Claude Skills**](https://www.anthropic.com/news/skills)

## 1\. Claude Skills の概要

「 **Skills** 」は、 **「Claude」が必要に応じて読み込むことができる「指示」「スクリプト」「リソース」を含むフォルダ** です。

「Claude」は、手元のタスクに関連する場合にのみ「Skills」にアクセスします。「Skills」を使用すると、Excel での作業や組織のブランドガイドラインの遵守といった特殊なタスクをより効率的に実行できるようになります。

Claudeアプリでは、スプレッドシートやプレゼンテーションなどのファイルを作成するために「Skills」が使われているのを既に知っていると思います。これからは、独自の「Skills」を作成し、Claudeアプリ、Claude Code、APIで利用できるようになります。

## 2\. Claude Skills のしくみ

タスク処理中、「Claude」は利用可能な「Skills」をスキャンし、関連する「Skills」を探します。一致する「Skills」が見つかった場合、必要な最小限の情報とファイルのみが読み込まれるため、「Claude」は高速に動作しながら専門知識にアクセスすることができます。

スキルの特徴は、次のとおりです。

> **・構成可能**
> 「Skills」はスタック可能です。「Claude」は必要な「Skills」を自動的に識別し、その使用を調整します。
>
> **・移植性**
> 「Skills」はどこでも同じ形式を使用します。一度構築すれば、Claudeアプリ、Claude Code、API で使用できます。
>
> **・効率性**
> 必要なときに必要なものだけを読み込みます。
>
> **・強力**
> 「Skills」には、トークン生成よりも従来のプログラミングの方が信頼性の高いタスク用の実行コードを含めることができます。

「Skills」は、専門知識をパッケージ化できるカスタムオンボーディングマテリアルのようなもので、「Claude」をユーザーにとって最も重要な分野の専門家にすることができます。エージェントスキルの設計パターン、アーキテクチャ、開発のベストプラクティスに関する技術的な詳細については、 [エンジニアリングブログ](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) を参照してください。

## 3\. Claude製品での利用

### 3-1. Claudeアプリ

「Skills」はPro、Max、Team、Enterpriseユーザーが利用できます。ドキュメント作成などの一般的なタスク向けのスキル、カスタマイズ可能なサンプルSkills、そして独自のカスタムSkillsを作成する機能を用意しています。

![画像](https://assets.st-note.com/img/1760664737-26IX5QbhNtceszASYg0WvuoL.png?width=1200)

Claudeはタスクに基づいて関連するスキルを自動的に呼び出します。手動で選択する必要はありません。Claudeの思考回路にも、スキルが表示されます。

Skillsの作成は簡単です。「Skills作成」スキルがインタラクティブなガイダンスを提供します。Claudeはワークフローについて質問し、フォルダ構造を生成し、SKILL.mdファイルをフォーマットし、必要なリソースをバンドルします。手動でファイルを編集する必要はありません。

設定でSkillsを有効にしてください。TeamユーザーとEnterpriseユーザーの場合、管理者はまず組織全体でスキルを有効にする必要があります。

### 3-2. API

「Agent Skills」(以下、単にSkillsと呼びます）を「Messages API」リクエストに追加できるようになりました。新しい **/v1/skills** エンドポイントにより、開発者はカスタムスキルのバージョン管理と管理をプログラムで制御できます。Skillsを実行するには、「 [**Code Execution Tool**](https://docs.claude.com/en/docs/agents-and-tools/tool-use/code-execution-tool) 」 (ベータ版) が必要です。このツールは、Skillsの実行に必要な安全な環境を提供します。

Anthropicが作成したスキルを使用すると、Claudeで数式を含むプロフェッショナルなExcelスプレッドシート、PowerPointプレゼンテーション、Word文書、入力可能なPDFを読み取ったり生成したりできます。開発者はカスタムスキルを作成して、特定のユースケースに合わせてClaudeの機能を拡張できます。

開発者はClaudeコンソールからSkillsのバージョンを簡単に作成・表示・アップグレードすることもできます。

詳しくは、 [ドキュメント](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) または [Anthropic Academy](https://www.anthropic.com/learn/build-with-claude) を参照してください。

### 3-3. Claude Code

「Skills」は、チームの専門知識とワークフローを活用して「Claude Code」を拡張します。anthropics/skillsマーケットプレイスからプラグインを介してスキルをインストールします。「Claude」は、必要に応じてスキルを自動的に読み込みます。バージョン管理を通じてチームとスキルを共有できます。また、~/.claude/skillsに追加することで、手動でスキルをインストールすることもできます。「Claude Agent SDK」は、カスタムエージェントを構築するための「Agent Skills」と同様のサポートを提供します。

> **・Claude apps:**[User Guide](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills) & [Help Center](https://support.claude.com/en/articles/12512176-what-are-skills)
> **・API developers:**[Documentation](https://docs.claude.com/en/api/skills-guide)
> **・Claude Code:**[Documentation](https://docs.claude.com/en/docs/claude-code/skills)
> **・Example Skills to customize:**[GitHub repository](https://github.com/anthropics/skills)

[**ゼロから学ぶ MCP&A2Aプログラミング入門　AIエージェント時代を切り開く次世代プロトコル** *www.amazon.co.jp*](https://www.amazon.co.jp/dp/4839989826?tag=npaka-22&linkCode=ogi&th=1&psc=1)

[*3,520 円* (2025年10月17日 10:53時点 詳しくはこちら)](https://www.amazon.co.jp/dp/4839989826?tag=npaka-22&linkCode=ogi&th=1&psc=1)

[

Amazon.co.jpで購入する

](<https://www.amazon.co.jp/dp/4839989826?tag=npaka-22&linkCode=ogi&th=1&psc=1>)

## いいなと思ったら応援しよう

Claude Skills の概要｜npaka
