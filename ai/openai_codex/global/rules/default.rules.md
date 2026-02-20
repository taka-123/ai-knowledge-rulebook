<!-- ## Codex（Global Rules）: `~/.codex/rules/default.rules` -->

```python
# Codex command approval rules (Starlark)

# Read-only / safe commands
prefix_rule(
    pattern = ["pwd"],
    decision = "allow",
    justification = "Working directory check is safe.",
    match = ["pwd"],
)

prefix_rule(
    pattern = ["ls"],
    decision = "allow",
    justification = "Listing files is safe.",
    match = ["ls", "ls -la"],
)

prefix_rule(
    pattern = ["cat"],
    decision = "allow",
    justification = "Viewing text files is read-only.",
    match = ["cat README.md"],
)

prefix_rule(
    pattern = ["whoami"],
    decision = "allow",
    justification = "Identity check is safe.",
    match = ["whoami"],
)

prefix_rule(
    pattern = ["which"],
    decision = "allow",
    justification = "Binary location check is safe.",
    match = ["which git", "which node"],
)

prefix_rule(
    pattern = ["git", "status"],
    decision = "allow",
    justification = "Repository status is read-only.",
    match = ["git status"],
)

prefix_rule(
    pattern = ["git", "branch"],
    decision = "allow",
    justification = "Branch list is read-only.",
    match = ["git branch", "git branch -a"],
)

prefix_rule(
    pattern = ["git", "diff"],
    decision = "allow",
    justification = "Diff is read-only.",
    match = ["git diff", "git diff --stat", "git diff --cached"],
)

prefix_rule(
    pattern = ["git", "log"],
    decision = "allow",
    justification = "Log is read-only.",
    match = ["git log -n 20", "git log --oneline -n 50"],
)

prefix_rule(
    pattern = ["git", "show"],
    decision = "allow",
    justification = "Show is read-only.",
    match = ["git show HEAD", "git show --name-only HEAD"],
)

prefix_rule(
    pattern = [["rg", "grep"]],
    decision = "allow",
    justification = "Search commands are read-only.",
    match = ["rg TODO .", "grep -R \"TODO\" ."],
)

# Mutating / network commands require explicit confirmation
prefix_rule(
    pattern = [["rm", "mv", "cp"]],
    decision = "prompt",
    justification = "File operations can be destructive.",
    match = ["rm file.txt", "mv a b", "cp a b"],
)

prefix_rule(
    pattern = ["git", "add"],
    decision = "prompt",
    justification = "Staging changes the index.",
    match = ["git add .", "git add path/to/file"],
)

prefix_rule(
    pattern = ["git", ["checkout", "switch", "restore"]],
    decision = "prompt",
    justification = "Can overwrite working tree.",
    match = ["git checkout main", "git switch -c feat", "git restore file.txt"],
)

prefix_rule(
    pattern = ["git", "commit"],
    decision = "prompt",
    justification = "Committing creates history.",
    match = ["git commit -m \"msg\""],
)

prefix_rule(
    pattern = ["git", "push"],
    decision = "prompt",
    justification = "Pushing can affect remotes and CI.",
    match = ["git push", "git push origin HEAD"],
)

prefix_rule(
    pattern = [["curl", "wget"]],
    decision = "prompt",
    justification = "Network access requires confirmation.",
    match = ["curl -I https://example.com", "wget https://example.com/index.html"],
)

prefix_rule(
    pattern = ["gh"],
    decision = "prompt",
    justification = "GitHub CLI can access credentials and remote state.",
    match = ["gh auth status", "gh pr view 1"],
)

prefix_rule(
    pattern = [["npm", "pnpm", "yarn", "bun"], ["install", "add", "remove", "update"]],
    decision = "prompt",
    justification = "Dependency operations can modify local and lockfile state.",
    match = ["npm install", "pnpm add zod", "yarn add react"],
)

prefix_rule(
    pattern = ["pip", ["install", "uninstall"]],
    decision = "prompt",
    justification = "Python package operations can modify environment.",
    match = ["pip install foo", "pip uninstall foo"],
)

prefix_rule(
    pattern = ["uv", ["add", "sync", "lock"]],
    decision = "prompt",
    justification = "uv can modify pyproject.toml and environment.",
    match = ["uv add requests", "uv sync"],
)

prefix_rule(
    pattern = ["poetry", ["add", "remove", "update"]],
    decision = "prompt",
    justification = "Poetry can modify pyproject.toml and lockfile.",
    match = ["poetry add requests", "poetry update"],
)

prefix_rule(
    pattern = ["chmod"],
    decision = "prompt",
    justification = "Changing file modes requires confirmation.",
    match = ["chmod +x script.sh"],
)

# Forbidden destructive commands
prefix_rule(
    pattern = ["sudo"],
    decision = "forbidden",
    justification = "Privilege escalation is forbidden.",
    match = ["sudo -n true"],
)

prefix_rule(
    pattern = ["rm", "-rf", "/"],
    decision = "forbidden",
    justification = "System-destroying command is forbidden.",
    match = ["rm -rf /"],
)

prefix_rule(
    pattern = ["dd"],
    decision = "forbidden",
    justification = "Raw disk write is forbidden.",
    match = ["dd if=/dev/zero of=/dev/sda"],
)

prefix_rule(
    pattern = [["mkfs", "diskutil"]],
    decision = "forbidden",
    justification = "Disk formatting and partitioning are forbidden.",
    match = ["diskutil eraseDisk APFS Foo /dev/diskX"],
)
```
