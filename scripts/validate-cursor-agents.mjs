#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const dir = path.join(root, '.cursor', 'agents')
const allowed = new Set(['name', 'description', 'model', 'readonly'])
const errors = []

for (const entry of fs.readdirSync(dir).filter(f => f.endsWith('.md'))) {
  const file = path.join(dir, entry)
  const text = fs.readFileSync(file, 'utf8')
  const fm = text.match(/^---\n([\s\S]*?)\n---\n/)
  if (!fm) {
    errors.push(`${entry}: missing frontmatter`)
    continue
  }
  const keys = fm[1]
    .split('\n')
    .filter(Boolean)
    .map(line => line.split(':')[0].trim())

  for (const key of keys) {
    if (!allowed.has(key)) errors.push(`${entry}: unsupported key '${key}'`)
  }
  for (const req of ['name', 'description', 'model']) {
    if (!keys.includes(req)) errors.push(`${entry}: missing required key '${req}'`)
  }

  for (const forbidden of ['color:', 'tools:', 'disallowedTools:', 'memory:']) {
    if (fm[1].includes(forbidden)) errors.push(`${entry}: forbidden field '${forbidden}' found`)
  }
}

if (errors.length > 0) {
  console.error('Cursor agent validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log('Cursor agent validation passed.')
