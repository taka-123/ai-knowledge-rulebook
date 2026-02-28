#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()
const DIR = path.join(ROOT, '.claude', 'agents')
const ALLOWED = new Set(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Cyan'])

const canonicalMap = new Map([
  ['red', 'Red'],
  ['blue', 'Blue'],
  ['green', 'Green'],
  ['yellow', 'Yellow'],
  ['purple', 'Purple'],
  ['orange', 'Orange'],
  ['pink', 'Pink'],
  ['cyan', 'Cyan'],
  ['magenta', 'Purple'],
])

const errors = []

for (const file of fs.readdirSync(DIR).filter(f => f.endsWith('.md'))) {
  const full = path.join(DIR, file)
  const text = fs.readFileSync(full, 'utf8')
  const colorMatch = text.match(/^color:\s*(.+)$/m)
  if (!colorMatch) {
    errors.push(`${file}: missing color`)
    continue
  }
  const current = colorMatch[1].trim()
  const mapped = canonicalMap.get(current.toLowerCase())
  if (!mapped || !ALLOWED.has(mapped)) {
    errors.push(`${file}: unsupported color '${current}'`)
    continue
  }
  if (current !== mapped) {
    const updated = text.replace(/^color:\s*.+$/m, `color: ${mapped}`)
    fs.writeFileSync(full, updated)
  }
}

if (errors.length > 0) {
  console.error('Color normalization failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log('Claude agent colors normalized.')
