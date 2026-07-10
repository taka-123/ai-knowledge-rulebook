gitignore された `.claude/suggestions/` が Prettier 対象のため、ローカルの `npm run check` が失敗しうる。

## なぜ重要か

`.claude/suggestions/` は Git 管理外だが `.prettierignore` に無い。ローカルに suggestions ファイルがあると `format.sh check` が exit 1 になり、CI（クリーン checkout）では再現しない不一致が起きる。

## 何で確認したか

- `.gitignore` L17: `.claude/suggestions/`
- `.prettierignore`: `suggestions/` パスなし（`clips/` `tmp/` のみ類似除外）
- 本セッション `npm run check`: `.claude/suggestions/*.md` ほかで Prettier warn、exit 1（suggestions は 9 件以上存在）

## いつ見直すか

- `.prettierignore` または `format.sh` の対象変更時
- suggestions の保存ポリシー変更時
