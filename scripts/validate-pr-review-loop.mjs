#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const skillRoot = path.join(
  root,
  'ai',
  'claude_code',
  'global',
  '.claude',
  'skills',
  'pr-review-loop'
)
const errors = []

function read(rel) {
  const abs = path.join(skillRoot, rel)
  if (!fs.existsSync(abs)) {
    errors.push(`missing: ${path.relative(root, abs)}`)
    return ''
  }
  return fs.readFileSync(abs, 'utf8')
}

const wrapper = read('SKILL.md')
const upstream = read('UPSTREAM.md')
const launcher = read('scripts/run-gh-pr-watch.py')
const officialSkill = read('vendor/openai-codex-babysit-pr/SKILL.md')
const officialWatcher = path.join(
  skillRoot,
  'vendor/openai-codex-babysit-pr/scripts/gh_pr_watch.py'
)
const officialTest = path.join(
  skillRoot,
  'vendor/openai-codex-babysit-pr/scripts/test_gh_pr_watch.py'
)

const PINNED_SHA = 'a770e5b8470d3320eb53a56a286ea4a0a70a1f59'

if (upstream && !upstream.includes(PINNED_SHA)) {
  errors.push('UPSTREAM.md must record the pinned openai/codex commit SHA')
}

if (
  officialSkill &&
  !officialSkill.includes('python3 .codex/skills/babysit-pr/scripts/gh_pr_watch.py')
) {
  errors.push('vendored babysit-pr SKILL.md looks patched (missing upstream path)')
}

if (wrapper) {
  const required = [
    'vendor/openai-codex-babysit-pr/SKILL.md',
    'scripts/run-gh-pr-watch.py',
    '一時的な `idle`',
    'review-clean と判定しない',
    '過去 HEAD の review 結果を新 HEAD へ流用しない',
    'branch 起因ならコードを直す',
    'merge可能。最終merge判断は人間。',
    '人間 reviewer のコメントへ返信せず',
    'gh workflow run',
    'retry_failed_checks',
    '@codex review',
  ]
  for (const item of required) {
    if (!wrapper.includes(item)) errors.push(`pr-review-loop SKILL.md missing policy: ${item}`)
  }
  if (
    wrapper.includes('python3 .codex/skills/babysit-pr/scripts/gh_pr_watch.py --pr auto --watch')
  ) {
    errors.push('wrapper must not tell agents to run the openai/codex-relative watcher path')
  }
  if (wrapper.split('\n').length > 500) {
    errors.push('pr-review-loop SKILL.md must be <= 500 lines')
  }
}

if (launcher) {
  if (!launcher.includes('os.execv')) {
    errors.push('launcher must exec the vendored watcher, not reimplement it')
  }
  if (launcher.includes('recommend_actions') || launcher.includes('fetch_new_review_items')) {
    errors.push('launcher must not reimplement watcher logic')
  }
}

if (!fs.existsSync(officialWatcher)) {
  errors.push('missing vendored gh_pr_watch.py')
}
if (!fs.existsSync(officialTest)) {
  errors.push('missing vendored test_gh_pr_watch.py')
}

const topLevelBabysit = path.join(
  root,
  'ai',
  'claude_code',
  'global',
  '.claude',
  'skills',
  'babysit-pr',
  'SKILL.md'
)
if (fs.existsSync(topLevelBabysit)) {
  errors.push('babysit-pr must not be a second top-level skill; keep a single vendored copy')
}

if (errors.length) {
  console.error('pr-review-loop validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log('pr-review-loop validation passed.')
