---
name: skill-discoverer
description: Use when the user explicitly asks what skills or agents are available, or when uncertain which specialist to delegate to; When NOT to use: when the target skill is already known; Trigger Keywords: [スキル一覧, 何ができる, available skills, help, 委任先].
---

# skill-discoverer

## When to use

- 利用可能な skill/agent の一覧をユーザーが求めたとき。
- どの専門 agent に委任すべきか判断がつかないとき。
- `.claude/skills` や `.claude/agents` 更新後に動的発見結果を確認したいとき。

## When NOT to use

- 使うべき skill がすでに明確で探索不要なとき。
- 単純な単発作業で委任判断が不要なとき。
- 既存回答に一覧が含まれており再探索が不要なとき。

## Trigger Keywords

- スキル一覧
- 何ができる
- available skills
- help
- 委任先

## Procedure

1. `find .claude/agents -maxdepth 1 -type f -name '*.md' | sort` と `find .claude/skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort` を実行する。完了条件: 実体一覧を取得。
2. 各ファイルの frontmatter から `name` と `description` を抽出する。完了条件: 一覧データ作成。
3. 抽出結果を skills/agents 別に整形して提示する。完了条件: ユーザーが選択可能な一覧が完成。
4. ユーザー要求に最も適した候補を 1 件推薦し、代替候補を最大 2 件提示する。完了条件: 推薦理由が明示。
5. 次に実行する具体アクション（例: 該当 skill 適用）を 1 行で案内する。完了条件: 次アクションが明確。

## Output Contract

| セクション       | 形式                                                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Available Skills | `- lint-fix: Use when lint or format checks fail ...`                                                                            |
| Available Agents | `- code-reviewer: Use proactively when reviewing diffs under .claude/, .cursor/, .codex/, scripts/, package.json, or .work/ ...` |
| Recommended      | `1. repo-cartographer - 配線監査に最適`                                                                                          |
| Alternatives     | `- code-reviewer - 品質監査向け`（最大2件）                                                                                      |

### NG例

❌ 実体スキャンせず記憶だけで一覧を作る（実体不一致）。

❌ 一覧だけ返して推薦理由を書かない（意思決定不能）。

❌ 推薦候補を多数列挙して優先順位を付けない（選択困難）。

## Examples

### Example 1

Input: `find .claude/skills -mindepth 2 -maxdepth 2 -name SKILL.md | sort` の結果を使って「このリポジトリで使えるスキルを教えて」と依頼された。
Output: `.claude/skills/*/SKILL.md` から抽出した一覧表と推薦 1 件。

### Example 2

Input: `find .claude/agents -maxdepth 1 -type f -name '*.md' | sort` の結果を使って「配線監査に向く agent はどれ？」と依頼された。
Output: `.claude/agents/*.md` の description 一覧と `repo-cartographer` 推薦。

### Example 3

Input: `.work/AI_SCAN.md` を参照して「どの専門家に委任すべきかわからない」と依頼された。
Output: 目的に基づく推薦 1 件 + 代替 2 件 + 次アクション 1 行。
