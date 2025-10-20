---
title: 'MCP セキュリティ評価レポート（改訂版）'
created: 2025-10-14
updated: 2025-10-14
tags:
  [
    'mcp',
    'security',
    'risk-assessment',
    'filesystem',
    'github',
    'playwright',
    'chrome-devtools',
    'context7',
    'notion',
    'serena',
  ]
source: ''
source_retrieved: 2025-10-14
---

# MCP セキュリティ評価レポート（改訂版）

**調査日**: 2025-10-14
**対象**: ai-knowledge-rulebook プロジェクトで使用中の MCP サーバー
**前提**: 一次情報（公式リポジトリ/公式ドキュメント/NVD）で裏取り。企業導入判断は**既定で保守的**。

---

## 📊 総合評価サマリー

| MCP サーバー       | リスクレベル                 | 企業導入          | 主な懸念事項                                                                                                   |
| ------------------ | ---------------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------- |
| serena             | 🔴 High                      | ❌ 非推奨（現状） | デフォルトでWebダッシュボード公開/認証なし、権限境界未整備（議論ベース） :contentReference[oaicite:0]{index=0} |
| filesystem         | 🟡 Medium → 🟢 Low (>=0.6.4) | ⚠️ 条件付き       | 0.6.3以前にCVE、**0.6.4で修正**。ディレクトリ封じ込め設定必須。                                                |
| github             | 🟡 Medium                    | ⚠️ 条件付き       | プロンプトインジェクション面・PAT権限設計。Fine-grained PAT推奨。                                              |
| playwright         | 🟡 Medium                    | ⚠️ 条件付き       | ブラウザ依存の脆弱性/更新頻度に依存。Docker隔離・定期更新。                                                    |
| chrome-devtools    | 🟡 Medium                    | ⚠️ 条件付き       | ブラウザ操作系ゆえ権限広め。公式発表を前提に隔離運用。                                                         |
| context7 (Upstash) | 🟢 Low                       | ✅ 推奨           | SOC2/GDPR表明。鍵管理の運用徹底。                                                                              |
| notion             | 🟢 Low                       | ✅ 推奨           | 公式提供・認証/コンプライアンス体制。                                                                          |

> 注: **serena のRCE/CVEは一次情報で確証なし**。ただし「ダッシュボード無認証/公開」の指摘・警告はコミュニティ議論で継続（High評価の根拠）。 :contentReference[oaicite:7]{index=7}

---

## 🔴 High: 企業導入非推奨（現状）

### serena

- **懸念**: デフォルトでWebダッシュボード（既定ポート例: 24282相当）を公開し、認証機構が無い/弱いという指摘が継続。IDE統合/CLI経由で**広範な操作面**が開くため、ネットワーク境界内でも**攻撃面が広い**。 :contentReference[oaicite:8]{index=8}
- **推奨運用（個人開発に限る）**
  - **ダッシュボード無効化**（フラグ/設定で明示的にOFF） :contentReference[oaicite:9]{index=9}
  - **ネットワーク分離**（ローカルのみ、ループバック限定/FW遮断）
  - **実行ユーザ最小権限**（非root/権限分離コンテナ）

> 企業導入: パッチ/認証/監査ログ/権限境界の一次情報整備までは**見送り**。

---

## 🟡 Medium → 🟢 Low（バージョン基準で低減）

### filesystem

- **事実**: `@modelcontextprotocol/server-filesystem` に **CVE-2025-53110 / CVE-2025-53109**。**v0.6.4**で修正。NVDは0.6.4を安全閾値として明示。
- **推奨**: **バージョン下限ピン**を設定（例）
  - `npx @modelcontextprotocol/server-filesystem@">=0.6.4 <1.0.0"`（予期せぬメジャー変更を抑止）
  - 許可ディレクトリは**最小限**（読み取りルートを限定）
- **追加ハードニング**: MCPのpermissions/allowで`Read`/`Write`を更に絞る。

---

## 🟡 Medium: 条件付きで可

### github

- **懸念**: コンテンツ由来のプロンプトインジェクション、PAT過剰権限。
- **推奨**: **Fine-grained PAT**で最小スコープ、**環境変数注入**、**90日ローテーション**。運用はDocker/コンテナで境界を維持。
- **例**:

  ```bash
  docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
  ```

### playwright / chrome-devtools

- **懸念**: ブラウザ依存のCVE露出、外部サイト操作面が広い。
- **推奨**: **Docker隔離**/**定期pull**でブラウザ更新、信頼サイトに限定。Chrome DevTools MCPは公式発表を前提に利用。

---

## 🟢 Low: 導入容易

### context7 (Upstash)

- **所感**: セキュリティ/コンプライアンス表明（SOC2/GDPR）。鍵管理・RBACは利用側運用に依存。

### notion

- **所感**: 公式提供・OAuth・企業向けセキュリティ体制。Integration権限は**最小**で付与。

---

## 🛠 推奨MCPグローバル設定（抜粋）

> **方針**: 「**最低限の固定** + **上限ガード**」で意図しない最新版事故を防ぐ

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem@>=0.6.4 <1.0.0",
        "/ABS/PATH/ALLOW1",
        "/ABS/PATH/ALLOW2"
      ]
    },
    "github": {
      "type": "stdio",
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ]
    },
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    },
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    },
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    },
    "notion": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": { "NOTION_TOKEN": "${NOTION_TOKEN}" }
    }
    /* serena は企業用途では推奨停止。個人用途で使う場合のみローカル/プロジェクト側に明示 */
  }
}
```

- **filesystem**は**下限>=0.6.4**（CVE修正済）を固定。
- **serena**はグローバル登録を避け、**プロジェクト局所**にし、ダッシュボード**無効化**/NW封鎖前提。 :contentReference[oaicite:17]{index=17}

---

## 🎯 企業導入の判断基準（更新）

- **即導入可**: context7 / notion（トークン運用を前提）。
- **条件付き**: filesystem(>=0.6.4) / github / playwright / chrome-devtools（隔離・最小権限・定期更新）。
- **見送り**: serena（現状はコミュニティ指摘の解消が一次情報で未確認）。 :contentReference[oaicite:20]{index=20}

---

## 📋 運用チェックリスト（再掲・更新）

**導入前**

- [ ] 公式/NVDで**既知脆弱性**と**修正バージョン**を確認（例: filesystem>=0.6.4）。
- [ ] トークンは**Fine-grained**/**最小スコープ**で作成。
- [ ] ブラウザ系は**Docker隔離**前提、定期pullで更新。

**運用中**

- [ ] 月次で各MCPの更新/リリースノート/NVDを確認
- [ ] 四半期でシークレット/トークンローテーション
- [ ] MCP許可パス/権限の棚卸し

**インシデント対応**

- [ ] 各MCPの**緊急停止手順**/ネットワーク遮断手順を整備
- [ ] ダッシュボード等の**公開面**は既定でOFF／ローカル限定（serena等） :contentReference[oaicite:24]{index=24}

---

## 🔗 参考（一次情報）

- NVD: CVE-2025-53110（fixed in 0.6.4）; CVE-2025-53109（fixed in 0.6.4）.
- Filesystem MCP README（許可パス/起動例）.
- Chrome DevTools MCP 公式ブログ（公開アナウンス）.
- Upstash / Context7 Security & Compliance.
- Notion Security.
- GitHub: Fine-grained personal access tokens（ドキュメント）.
- Serena: ダッシュボード/セキュリティ懸念に関する議論・記事（認証/公開の指摘）。 :contentReference[oaicite:31]{index=31}
