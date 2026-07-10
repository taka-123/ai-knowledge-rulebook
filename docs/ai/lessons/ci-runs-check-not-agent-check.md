CI は `npm run check` のみ実行し、`npm run agent:check` は実行しない。

## なぜ重要か

README と AGENTS.md は `agent:check` を推奨するが、main へのマージ時に Skill / Agent / Codex 配線の破損が CI で検知されない。ローカル検証を省略すると壊れた状態がマージされうる。

## 何で確認したか

- `.github/workflows/ci.yml` L27: `run: npm run check` のみ
- `package.json` L26: `agent:check` は別チェーン
- 本セッション `npm run agent:check` は exit 0（現状は健全）

## いつ見直すか

- CI ワークフロー変更時
- `agent:check` の構成変更時
