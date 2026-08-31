#!/usr/bin/env node
import crypto from 'node:crypto'
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
const VENDOR_WATCHER_SHA256 = '9f9e992ec1f3e5a99546c79334ae2e0f810279edbd8b50fa894f2b275d644417'

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
    'final_review_clean_gate.py',
    'commit_id',
    'resolve_codex_threads.py',
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
} else {
  const hash = crypto.createHash('sha256').update(fs.readFileSync(officialWatcher)).digest('hex')
  if (hash !== VENDOR_WATCHER_SHA256) {
    errors.push('vendored gh_pr_watch.py must remain unmodified (SHA256 mismatch)')
  }
  const watcherText = fs.readFileSync(officialWatcher, 'utf8')
  if (
    !watcherText.includes('"kind": "review"') ||
    watcherText.includes('"commit_id": str(item.get("commit_id")')
  ) {
    errors.push('vendored normalize_reviews must stay upstream (no wrapper commit_id patch)')
  }
}
if (!fs.existsSync(officialTest)) {
  errors.push('missing vendored test_gh_pr_watch.py')
}

const gate = read('scripts/final_review_clean_gate.py')
if (gate) {
  if (
    gate.includes('gh_pr_watch') ||
    gate.includes('recommend_actions') ||
    gate.includes('fetch_new_review_items')
  ) {
    errors.push('final_review_clean_gate.py must not import or reimplement the vendored watcher')
  }
  if (!gate.includes('commit_id') || !gate.includes('original_commit_id')) {
    errors.push(
      'final_review_clean_gate.py must keep commit_id / original_commit_id for HEAD binding'
    )
  }
  if (!gate.includes('reviewThreads') || !gate.includes('"graphql"')) {
    errors.push('final_review_clean_gate.py must re-fetch published reviews and unresolved threads')
  }
  if (!gate.includes('codex_thumbs_up') || !gate.includes('is_codex_reviewer')) {
    errors.push('final_review_clean_gate.py must treat bound Codex thumbs-up as completion proof')
  }
  if (!gate.includes('extract_repo_from_pr_url')) {
    errors.push('final_review_clean_gate.py must target the PR URL base repository, not fork HEAD')
  }
  if (!gate.includes('does not match current PR HEAD')) {
    errors.push('final_review_clean_gate.py must reject --head that does not match live headRefOid')
  }
  if (!gate.includes('DISMISSED') || !gate.includes('VALID_PROOF_REVIEW_STATES')) {
    errors.push('final_review_clean_gate.py must not treat dismissed reviews as completion proof')
  }
  if (!gate.includes('pageInfo') || !gate.includes('hasNextPage') || !gate.includes('endCursor')) {
    errors.push('final_review_clean_gate.py must paginate reviewThreads with GraphQL cursors')
  }
  if (gate.includes('"codex" in lower') && gate.includes('"[bot]" in lower')) {
    errors.push('final_review_clean_gate.py must not treat partial *codex*[bot] logins as Codex')
  }
  if (!gate.includes('PR HEAD changed during gate fetch')) {
    errors.push('final_review_clean_gate.py must re-check PR HEAD after collecting review data')
  }
  if (!gate.includes('comment_ids') || !gate.includes('resolved_ids')) {
    errors.push(
      'final_review_clean_gate.py must drop REST comments that belong to resolved threads'
    )
  }
}

const resolver = read('scripts/resolve_codex_threads.py')
if (resolver) {
  if (
    !resolver.includes('eligible_codex_resolve_threads') ||
    !resolver.includes('resolveReviewThread')
  ) {
    errors.push('resolve_codex_threads.py must resolve only eligible Codex threads')
  }
  if (resolver.includes('pulls/') && resolver.includes('--approve')) {
    errors.push('resolve_codex_threads.py must not submit reviews')
  }
  if (resolver.includes('gh_pr_watch')) {
    errors.push('resolve_codex_threads.py must not import the vendored watcher')
  }
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
