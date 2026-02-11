# Safety

- Keep changes minimal and reversible.
- Mark unknowns as `不明`; do not assert by guess.
- Require explicit approval before any destructive or external-impact operation:
  - `deploy`
  - `migrate`
  - `terraform apply`
  - `git push --force`
  - production config change
