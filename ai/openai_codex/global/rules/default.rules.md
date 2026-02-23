<!-- ## Codex（Global Rules）: `~/.codex/rules/default.rules` -->

```python
# Codex コマンド承認ルール（Starlark）

# 読み取り中心の安全なコマンド
prefix_rule(
    pattern = ["pwd"],
    decision = "allow",
)

prefix_rule(
    pattern = ["ls"],
    decision = "allow",
)

prefix_rule(
    pattern = ["cat"],
    decision = "allow",
)

prefix_rule(
    pattern = ["whoami"],
    decision = "allow",
)

prefix_rule(
    pattern = ["which"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "status"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "branch"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "diff"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "log"],
    decision = "allow",
)

prefix_rule(
    pattern = ["git", "show"],
    decision = "allow",
)

prefix_rule(
    pattern = [["rg", "grep"]],
    decision = "allow",
)

prefix_rule(
    pattern = ["trash"],
    decision = "allow",
)

prefix_rule(
    pattern = ["gomi"],
    decision = "allow",
)

# 変更・外部アクセスを伴うため確認が必要なコマンド
prefix_rule(
    pattern = [["rm", "mv", "cp"]],
    decision = "prompt",
    justification = "ファイル操作は破壊的変更につながる可能性があります。",
)

prefix_rule(
    pattern = ["git", "add"],
    decision = "prompt",
    justification = "ステージングで Git の状態が変化します。",
)

prefix_rule(
    pattern = ["git", ["checkout", "switch", "restore"]],
    decision = "prompt",
    justification = "ワークツリーの内容を上書きする可能性があります。",
)

prefix_rule(
    pattern = ["git", "commit"],
    decision = "prompt",
    justification = "コミットは履歴を更新します。",
)

prefix_rule(
    pattern = ["git", "push"],
    decision = "prompt",
    justification = "リモートや CI に影響するため事前確認が必要です。",
)

prefix_rule(
    pattern = [["curl", "wget"]],
    decision = "prompt",
    justification = "ネットワークアクセスを伴うため確認します。",
)

prefix_rule(
    pattern = ["gh"],
    decision = "prompt",
    justification = "認証情報やリモート状態にアクセスするため確認します。",
)

prefix_rule(
    pattern = [["npm", "pnpm", "yarn", "bun"], ["install", "add", "remove", "update"]],
    decision = "prompt",
    justification = "依存関係やロックファイルを変更する可能性があります。",
)

prefix_rule(
    pattern = ["pip", ["install", "uninstall"]],
    decision = "prompt",
    justification = "Python 環境の状態を変更します。",
)

prefix_rule(
    pattern = ["uv", ["add", "sync", "lock"]],
    decision = "prompt",
    justification = "依存関係や環境設定を変更する可能性があります。",
)

prefix_rule(
    pattern = ["poetry", ["add", "remove", "update"]],
    decision = "prompt",
    justification = "依存関係や lockfile を更新する可能性があります。",
)

prefix_rule(
    pattern = ["chmod"],
    decision = "prompt",
    justification = "ファイル権限を変更するため確認します。",
)

prefix_rule(
    pattern = ["psql"],
    decision = "prompt",
    justification = "DB への直接操作は影響範囲が大きいため確認します。",
)

prefix_rule(
    pattern = ["mysql"],
    decision = "prompt",
    justification = "DB への直接操作は影響範囲が大きいため確認します。",
)

prefix_rule(
    pattern = ["docker", "compose"],
    decision = "prompt",
    justification = "コンテナ構成や稼働状態に影響するため確認します。",
)

prefix_rule(
    pattern = ["docker-compose"],
    decision = "prompt",
    justification = "コンテナ構成や稼働状態に影響するため確認します。",
)

# 実行を禁止する高リスクコマンド
prefix_rule(
    pattern = ["sudo"],
    decision = "forbidden",
    justification = "権限昇格は許可しません。",
)

prefix_rule(
    pattern = ["rm", "-rf", "/"],
    decision = "forbidden",
    justification = "システム破壊につながるため禁止します。",
)

prefix_rule(
    pattern = ["dd"],
    decision = "forbidden",
    justification = "ディスクへ直接書き込む高リスク操作のため禁止します。",
)

prefix_rule(
    pattern = [["mkfs", "diskutil"]],
    decision = "forbidden",
    justification = "ディスク初期化やパーティション操作は禁止します。",
)

prefix_rule(
    pattern = ["ssh"],
    decision = "forbidden",
    justification = "外部環境への直接接続は本プロファイルでは禁止します。",
)

prefix_rule(
    pattern = ["scp"],
    decision = "forbidden",
    justification = "外部へのファイル転送は本プロファイルでは禁止します。",
)

prefix_rule(
    pattern = ["aws"],
    decision = "forbidden",
    justification = "クラウド資格情報や本番環境に影響しうるため禁止します。",
)

prefix_rule(
    pattern = ["terraform"],
    decision = "forbidden",
    justification = "インフラ変更の影響が大きいため禁止します。",
)

prefix_rule(
    pattern = ["kubectl"],
    decision = "forbidden",
    justification = "クラスタ操作の影響が大きいため禁止します。",
)

prefix_rule(
    pattern = ["git", "push", "--force"],
    decision = "forbidden",
    justification = "履歴破壊につながる force push は禁止します。",
)

prefix_rule(
    pattern = ["git", "push", "-f"],
    decision = "forbidden",
    justification = "履歴破壊につながる force push は禁止します。",
)

prefix_rule(
    pattern = ["git", "reset", "--hard"],
    decision = "forbidden",
    justification = "ローカル変更を失う可能性があるため禁止します。",
)

prefix_rule(
    pattern = ["git", "clean", "-fdx"],
    decision = "forbidden",
    justification = "未追跡ファイルを不可逆に削除するため禁止します。",
)
```
