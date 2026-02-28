#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()
const DIR = path.join(ROOT, '.claude', 'skills')

const errors = []

for (const name of fs.readdirSync(DIR)) {
  const file = path.join(DIR, name, 'SKILL.md')
  if (!fs.existsSync(file)) continue

  const text = fs.readFileSync(file, 'utf8')
  const match = text.match(/^description:\s*(.+)$/m)
  if (!match) {
    errors.push(`${name}: missing description`)
    continue
  }
  const description = match[1]
  const hasPath = /\.[a-zA-Z0-9_\-]+\//.test(description) || /notes\//.test(description) || /ai\//.test(description)
  const proactive = description.startsWith('Use proactively when')
  const explicit = description.startsWith('Use when the user explicitly asks')

  if (proactive && !hasPath) {
    errors.push(`${name}: description condition lacks concrete path`)
  }
  if (!proactive && !explicit) {
    errors.push(`${name}: description must start with proactive or explicit pattern`)
  }
}

if (errors.length > 0) {
  console.error('Description condition enforcement failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log('Description condition enforcement passed.')
