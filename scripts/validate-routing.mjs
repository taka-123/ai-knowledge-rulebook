#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const required = [
  'CLAUDE.md',
  '.claude/CLAUDE.md',
  '.cursor/rules/00-router.mdc',
  '.cursor/rules/10-skill-map.mdc',
  '.cursor/rules/20-scope-map.mdc',
  '.windsurf/rules/00-router.md',
  '.windsurf/rules/10-skill-map.md',
  '.windsurf/rules/20-scope-map.md',
]

const errors = []

for (const rel of required) {
  const full = path.join(root, rel)
  if (!fs.existsSync(full)) {
    errors.push(`${rel}: missing required routing file`)
  }
}

function collectFiles(dir, extPattern) {
  const full = path.join(root, dir)
  if (!fs.existsSync(full)) return []
  return fs
    .readdirSync(full)
    .filter(f => extPattern.test(f))
    .map(f => path.join(full, f))
}

const routeFiles = [
  path.join(root, 'CLAUDE.md'),
  path.join(root, '.claude', 'CLAUDE.md'),
  ...collectFiles('.cursor/rules', /\.mdc$/),
  ...collectFiles('.windsurf/rules', /\.md$/),
].filter(p => fs.existsSync(p))

for (const file of routeFiles) {
  const text = fs.readFileSync(file, 'utf8')
  if (!text.includes('.claude/skills')) {
    errors.push(`${path.relative(root, file)}: must reference .claude/skills`)
  }
}

for (const dir of ['.claude/skills', '.cursor/rules', '.windsurf/rules']) {
  const full = path.join(root, dir)
  if (!fs.existsSync(full)) continue
  for (const entry of fs.readdirSync(full)) {
    const target = path.join(full, entry)
    if (fs.lstatSync(target).isSymbolicLink()) {
      errors.push(`${path.relative(root, target)}: symlink is not allowed in canonical routing set`)
    }
  }
}

if (errors.length) {
  console.error('Routing validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log(`Routing validation passed (${routeFiles.length} files checked).`)
