#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()

const requiredFiles = [
  'CLAUDE.md',
  '.claude/CLAUDE.md',
  'CLAUDE.local.md',
  '.claude/commands/review-request.md',
  '.cursor/rules/review-routing.mdc',
  '.cursor/commands/review-request.md',
  '.codex/REVIEW_PLAYBOOK.md',
  '.codex/config.toml',
]

const errors = []

for (const rel of requiredFiles) {
  const full = path.join(root, rel)
  if (!fs.existsSync(full)) errors.push(`${rel}: missing required routing file`)
}

const scanFiles = [
  path.join(root, 'CLAUDE.local.md'),
  path.join(root, '.claude', 'commands', 'review-request.md'),
  path.join(root, '.cursor', 'rules', 'review-routing.mdc'),
  path.join(root, '.codex', 'REVIEW_PLAYBOOK.md'),
].filter(p => fs.existsSync(p))

for (const file of scanFiles) {
  const text = fs.readFileSync(file, 'utf8')
  if (!/レビューしてください/.test(text)) {
    errors.push(`${path.relative(root, file)}: must include natural-language review trigger`)
  }
  if (/git\s+--no\x2dstat/.test(text)) {
    errors.push(`${path.relative(root, file)}: must not use unsupported no-stat options`)
  }
}

if (errors.length) {
  console.error('Routing validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log(`Routing validation passed (${scanFiles.length} files checked).`)
