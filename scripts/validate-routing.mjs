#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const required = [
  'CLAUDE.md',
  '.claude/CLAUDE.md',
]
const deprecatedRuleDirs = ['.cursor/rules', '.windsurf/rules']

const errors = []

for (const rel of required) {
  const full = path.join(root, rel)
  if (!fs.existsSync(full)) {
    errors.push(`${rel}: missing required routing file`)
  }
}

for (const dir of deprecatedRuleDirs) {
  const full = path.join(root, dir)
  if (!fs.existsSync(full)) continue

  const entries = fs.readdirSync(full)
  if (entries.length > 0) {
    errors.push(`${dir}: rule files are deprecated; use CLAUDE.md + .claude/skills shared source`)
  }
}

const routeFiles = [
  path.join(root, 'CLAUDE.md'),
  path.join(root, '.claude', 'CLAUDE.md'),
].filter(p => fs.existsSync(p))

for (const file of routeFiles) {
  const text = fs.readFileSync(file, 'utf8')
  if (!text.includes('.claude/skills')) {
    errors.push(`${path.relative(root, file)}: must reference .claude/skills`)
  }
}

for (const dir of ['.claude/skills']) {
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
