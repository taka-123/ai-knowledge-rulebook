`~/.claude/skills/` を正典にして、他ツールから共通参照する。

1. 親ディレクトリを作成する。
2. 既存の「実ディレクトリ」(`~/.*/skills`) がある場合は退避する。
3. symlink を作成する。

```bash
mkdir -p ~/.agents ~/.cursor ~/.codeium/windsurf ~/.gemini/antigravity

for dst in \
  ~/.agents/skills \
  ~/.cursor/skills \
  ~/.codeium/windsurf/skills \
  ~/.gemini/antigravity/skills
do
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    mv "$dst" "${dst}.backup.$(date +%Y%m%d%H%M%S)"
  fi
  ln -sfn ~/.claude/skills "$dst"
done
```

確認:

```bash
ls -ld ~/.claude/skills ~/.agents/skills ~/.cursor/skills ~/.codeium/windsurf/skills ~/.gemini/antigravity/skills
```

Windows (PowerShell):

```powershell
$source = "$HOME/.claude/skills"
$parents = @(
  "$HOME/.agents",
  "$HOME/.cursor",
  "$HOME/.codeium/windsurf",
  "$HOME/.gemini/antigravity"
)
$targets = @(
  "$HOME/.agents/skills",
  "$HOME/.cursor/skills",
  "$HOME/.codeium/windsurf/skills",
  "$HOME/.gemini/antigravity/skills"
)

foreach ($p in $parents) {
  New-Item -ItemType Directory -Force -Path $p | Out-Null
}

foreach ($dst in $targets) {
  if (Test-Path $dst) {
    $item = Get-Item -Force $dst
    if (-not $item.LinkType) {
      Rename-Item $dst ($dst + ".backup." + (Get-Date -Format "yyyyMMddHHmmss"))
    } else {
      Remove-Item -Force $dst
    }
  }
  New-Item -ItemType SymbolicLink -Path $dst -Target $source | Out-Null
}
```

注記:

- Windows で symlink が作れない場合（権限/ポリシー制約）は、`$HOME/.claude/skills` から各ツールの `skills` 配下へコピー運用に切り替える。
