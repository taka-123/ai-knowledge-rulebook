---
name: frontend-design-project
description: Project-scoped overrides for frontend design to avoid AI-like aesthetics while aligning with this repository's brand choices
---

# Frontend Design Skill (Project Scope)

目的: グローバルスキル `frontend-design` を前提に、プロジェクト固有のブランド要素で上書きする。紫グラデや Inter への収束を避けつつ、ここで指定したフォント/カラー/モーション/背景を優先する。

読み込みタイミング: このリポジトリ内で UI/フロントエンド生成・改修を指示されたときに自動で併用する。

前提: グローバル (`ai/claude_code/global/skills/frontend-design/SKILL.md` 相当) を先に読み込み、その上で本ファイルの指針で強めに上書きする。

## 禁止事項（グローバルから継承＋追記）

- Inter, Roboto, Arial, Open Sans などの汎用サンセリフを使わない
- 紫〜青系の線形グラデーションを背景に使わない
- 予測可能なカードグリッドと中央寄せヒーローのテンプレ配置は避ける
- 影・モーションなしのフラットな UI を避ける

## タイポグラフィ（本プロジェクト優先）

- 見出し: Playfair Display / Crimson Pro / Spectral からローテーションして選択
- 本文: Source Serif Pro / Manrope / IBM Plex Sans を状況に応じて使い分け
- UI コンポーネント: DM Sans / Space Grotesk を優先（重複使用を避け、直近利用と被らないよう変化を付ける）
- サイズは 3 倍以上の階層差を付け、100/900 など極端なウェイトでメリハリを出す

## テーマとカラー

- 原則: 単一のプライマリ色を決め、その濃淡で構成する。アクセントは 10% 程度に抑える。
- 優先するプライマリ: Emerald (#10b981), Indigo (#4f46e5) ではなく Teal (#14b8a6) / Amber (#f59e0b) / Slate (#334155) を軸にローテーション
- 避ける組み合わせ: 667eea→764ba2 の紫グラデ、ec4899→a855f7 のピンク→パープルグラデ
- ニュートラルはやや暖色寄り (rgb(30,27,24) 系) を使い、純白/純黒は避ける

## モーション

- ページロード: セクションごとに 80–120ms のステップでフェードアップ、遅延をずらして重ねる
- ホバー/アクション: transform と opacity のみを 180–240ms、ease-out で変更
- スプリング使用時の推奨値: stiffness 380–420, damping 28–32（Framer Motion を使う場合）
- will-change は要所に限定し、パフォーマンスを優先

## 背景と質感

- グラデーション禁止。代わりにノイズテクスチャや控えめなドット/ラインパターンを使用
- 色温度を揃えた 2 層以上のレイヤー（例: 暗いメッシュ + ライトのスポット）で奥行きを出す
- 角丸は 10–14px を基準に統一。シャドウはレイヤードで弱く 2 段まで。

## 実装メモ

- CSS 変数でフォント・色を定義し、テーマ切替に備える: `--font-display`, `--font-body`, `--color-primary`, `--color-surface`
- React 生成時は Framer Motion を優先、静的 HTML の場合は CSS keyframes で分割遅延アニメーションを実装
- 背景用のノイズは data URI もしくは小サイズ PNG を Base64 で埋め込み、外部取得を避ける
