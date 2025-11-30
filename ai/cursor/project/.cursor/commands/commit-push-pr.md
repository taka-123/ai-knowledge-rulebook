# コミット・プッシュ・PR作成（一括実行）

## 概要

現在のブランチに対して変更をコミットし、リモートへプッシュしたあと、Pull Request を作成するための一括実行コマンド例です。 
main/master への直接プッシュ禁止や、コミット前の品質チェック（lint / test / build など）、PR 作成フロー（AI/MCP を使うか、CLI を使うかなど）は、プロジェクトポリシーに合わせて調整してください。

## 前提条件

- 変更済みファイルが存在すること
- リモート `origin` が設定済みであること
- GitHub CLI (`gh`) がインストール済みであること（フォールバック用）
- 作業ブランチ（feature/_, fix/_ など）にいること

## 実行手順（対話なし）

1. ブランチ確認（main/master 直プッシュ防止）
2. 必要に応じて品質チェック（lint / test / build など）
3. 変更のステージング（`git add -A`）
4. コミット（引数または環境変数のメッセージ使用）
5. プッシュ（`git push -u origin <current-branch>`）
6. PR作成（MCP や CLI など環境に応じた方法で作成）

## 使い方

### A) 最小限の指定（推奨）

```bash
MSG="fix: 不要なデバッグログ出力を削除"

BRANCH=$(git branch --show-current) && \
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then \
  echo "⚠️ main/master への直接プッシュは禁止です"; exit 1; \
fi

# 任意の品質チェック（必要なら）
# ./scripts/lint.sh && ./scripts/test.sh && ./scripts/build.sh || exit 1

git add -A && \
git commit -m "$MSG" && \
git push -u origin "$BRANCH"

# ここで AI / MCP / gh などで PR を作成する
# - ブランチ名から目的を推測
# - git diff --name-status で変更ファイルを確認
# - PRタイトルと本文を自動生成
# - mcp_github_create_pull_request / gh pr create 等を呼ぶ
```

### B) 手動で PR タイトル・本文を指定

```bash
MSG="fix: 不要なデバッグログ出力を削除"
PR_TITLE="fix: 不要なデバッグログ出力を削除"
PR_BODY=$(cat <<'EOF'
## 概要
このPRでは、不要なデバッグログを削除し、ログ出力量を抑制します。

## 変更内容
- 冗長なデバッグログ出力を削除
- 必要なログレベルとメッセージのみを残す

## 技術的な詳細
- 影響範囲はログ出力のみで、ビジネスロジックに変更なし

## テスト内容
- ログ出力の有無と動作を手動確認

## 関連Issue
Refs #123
EOF
)

BRANCH=$(git branch --show-current) && \
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then \
  echo "⚠️ main/master への直接プッシュは禁止です"; exit 1; \
fi

# 任意の品質チェック（必要なら）
# ./scripts/quality-check.sh || exit 1

git add -A && \
git commit -m "$MSG" && \
git push -u origin "$BRANCH" && \
gh pr create --title "$PR_TITLE" --body "$PR_BODY" --base main
```

### C) ステップ実行（デバッグ用）

```bash
# 1) ブランチ確認
BRANCH=$(git branch --show-current)
echo "現在のブランチ: $BRANCH"
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "⚠️ main/master への直接プッシュは禁止です"; exit 1;
fi

# 2) 変更ファイルの確認
git status --short

# 3) 任意のローカル品質チェック（必要に応じて）
# ./scripts/lint.sh && ./scripts/test.sh && ./scripts/build.sh || exit 1

# 4) ステージング
git add -A
echo "ステージング完了"

# 5) コミット
MSG="fix: 不要なデバッグログ出力を削除"
git commit -m "$MSG"
echo "コミット完了"

# 6) プッシュ
git push -u origin "$BRANCH"
echo "プッシュ完了"

# 7) PR作成（AIや gh へ依頼）
# - ブランチ名: $BRANCH
# - 差分: git diff main...HEAD --name-status
# - コミット履歴: git log main..HEAD --oneline
```

## PR自動生成の情報源

AIがPRを作成する際に利用する情報例:

```bash
git branch --show-current
git merge-base origin/main HEAD
git diff --name-status $(git merge-base origin/main HEAD)...HEAD
git diff --stat $(git merge-base origin/main HEAD)...HEAD
git log origin/main..HEAD --oneline
```

## PRタイトルとメッセージのルール

- タイトル/本文のフォーマットは `.cursor/rules/pr-message-format.mdc` に従うこと。
- コミットメッセージ規約との意味的不整合を避ける。

## 注意事項

- コミットメッセージは `.cursor/rules/commit-message-format.mdc` に従う。
- `git status` や `git diff` で差分を確認してから実行する。

## トラブルシューティング

### プッシュ成功後に PR 作成だけ失敗した場合

```bash
gh pr create --title "タイトル" --body "メッセージ" --base main
# または GitHub UI でPRを作成
```

### ブランチ名から Prefix を推測

| ブランチ接頭辞 | Prefix   |
| -------------- | -------- |
| feature/       | feat     |
| fix/           | fix      |
| refactor/      | refactor |
| perf/          | perf     |
| test/          | test     |
| docs/          | docs     |
| build/         | build    |
| ci/            | ci       |
| chore/         | chore    |

## 関連ドキュメント

- コミットメッセージルール: `.cursor/rules/commit-message-format.mdc`
- PR メッセージルール: `.cursor/rules/pr-message-format.mdc`
- 開発フロー: プロジェクト固有の README / CONTRIBUTING / 開発ガイド等
