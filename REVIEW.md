# Review guidelines

## 目的

PR・差分レビューでは、変更によって新規発生または悪化した、実際に対応価値のある問題を見つける。

レビューの目的は、理論上考えられるすべての入力・Shell 構文・回避方法を列挙して、補助的な guardrail を突破不能にすることではない。

指摘の価値は、実害の具体性、現実的な発生経路、差分との因果関係、根拠または再現条件、修正コストとの見合いで判断する。
同じ root cause の表記違い・構文違いを、別問題として無限に再提示しない。

## 参照順序

PR・差分レビューでは、必要に応じて次を確認する。

1. `AGENTS.md`
2. `CLAUDE.md`
3. 本 `REVIEW.md`
4. 外部サービス・権限・Hooks に関する変更では `ai/EXTERNAL_SERVICES_SECURITY.md`
5. 対象コード、テスト、関連ドキュメント

上位の明示的な要件や security boundary を、本ファイルの一般論より優先する。

## コメント方針

- コメントは日本語で書く。
- 識別子、設定キー、コマンド、API 名、ログは原文を維持する。
- 差分で新規発生または悪化した問題を優先する。
- 指摘には可能な限り次を含める。
  - 何が起きるか
  - どの条件で起きるか
  - 実害
  - 根拠または再現条件
  - 必要なら最小修正案
- 未確認事項は `確認事項:` とする。
- 差分外の改善は `follow-up:` とし、原則 blocker にしない。
- 単なる好み、表現差、理論上可能というだけの問題を P0 / P1 にしない。

## 優先度

### P0

作業を直ちに止める必要がある問題。

例:

- 重大な認証・認可の破壊
- 機密情報の重大な漏えい
- 不可逆な大規模データ損失
- 本番環境に対する重大な破壊操作
- 明確な重大契約違反

### P1

merge 前に修正すべき、具体的かつ再現可能または現実的な問題。

例:

- 通常利用で発生し得る機能不具合・回帰
- 重要判定（review-clean、mergeability、CI 等）を誤って通す、または永久に通せなくする問題
- 実際の security boundary を破る問題
- 通常の Agent 操作で、明示的に禁止された重大操作が容易に実行される問題
- CI / build / runtime を壊す問題
- 明示された契約・仕様との不整合

### P2

非ブロッキングだが対応価値がある限定的な問題。

例:

- 発生条件が限定された不具合
- 保守性や観測性の不足
- 将来的に問題化し得るが、現在の変更を止めるほどではないもの

### P3

任意改善。

例:

- 可読性
- 軽微な整理
- 表現改善
- コードスタイル上の提案

P0 / P1 があれば `needs-fix`、P2 / P3 のみ、または指摘なしなら `ready` とする。

## Security review

### hard boundary と supplemental guardrail

次を本当の security boundary として扱う。

- AWS IAM / SCP
- GitHub Rulesets / Branch Protection
- GitHub credential permissions
- OS / container sandbox
- network policy
- MCP / tool capability restriction
- その他、実行側・サービス側で強制される制御

Hooks、Agent rules、command deny、`AGENTS.md` / `CLAUDE.md` 等は、原則として補助的な guardrail である。
目的は、通常の Agent が自然に生成しやすい典型的な危険操作や誤操作を止めることであり、敵対的な Shell 構文変形によるすべての bypass を防ぐことではない。

hard boundary が意図せず弱くなっている場合、または guardrail 上の通常形コマンドで容易に抜ける場合は厳しくレビューする。
「同じ操作を意図的に別表現へ変形すれば回避できる」というだけの指摘は、原則 blocker にしない。

guardrail の bypass を完全に禁止する必要がある場合は、regex の追加ではなく、credential、sandbox、Ruleset / Branch Protection、MCP allowlist 等のより強い境界へ責務を移す。

### guardrail 指摘を P1 にしてよい例外

- 通常の Agent が自然に生成する canonical なコマンドで簡単に抜ける
- ドキュメント上、hook 自体を「絶対的な security boundary」と明示している
- hook の欠陥によって実際の hard boundary まで破られる
- false positive により通常作業が実用上できない
- false negative が通常運用で高確率に発生する

## Root cause と非収束

同じ原因から派生する表記違い・構文違いを、新しい独立 P1 として無限に再提示しない。
root cause の方針が確定した後は、同一 threat model 上の syntax variant を新しい blocker にしない。

同一 root cause に対する blocking review は原則最大 3 round とする。
3 round を超えても同じ設計上の限界・threat model・回避カテゴリについて variant が続くだけなら、新しい P1 として継続せず、`確認事項:` / `follow-up:` / human decision へ移す。

別 root cause の新しい具体的 P0 / P1、hard boundary の破壊、通常利用でも発生する経路、修正による新しい regression が見つかった場合は、この上限に関係なく指摘してよい。

## 再確認モード

### 初回

対象差分全体を `full` review する。

### 修正後

局所修正であれば `targeted` review を優先する。

確認対象:

- 前回指摘の解消
- 変更した関数・処理
- 直接 caller / consumer
- 直接的な回帰
- 変更した boundary

次の場合だけ `full` に戻す。

- P0
- security boundary の変更
- 公開契約・権限境界・architecture の変更
- 修正範囲が大きく拡大した
- 後続差分を初回差分から安全に分離できない

再レビューのたびに新しい adversarial 入力を探索して、scope を無制限に広げない。
