#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()
const DIR = path.join(ROOT, '.cursor', 'agents')
const allowed = new Set(['name', 'description', 'model', 'readonly'])

const errors = []

for (const file of fs.readdirSync(DIR).filter(f => f.endsWith('.md'))) {
  const full = path.join(DIR, file)
  const text = fs.readFileSync(full, 'utf8')
  const fm = text.match(/^---\n([\s\S]*?)\n---\n/)
  if (!fm) {
    errors.push(`${file}: missing frontmatter`)
    continue
  }

  const lines = fm[1].split('\n').filter(Boolean)
  const keys = lines.map(line => line.split(':')[0].trim())
  for (const key of keys) {
    if (!allowed.has(key)) {
      errors.push(`${file}: unsupported frontmatter key '${key}'`)
    }
  }
  if (!keys.includes('name') || !keys.includes('description') || !keys.includes('model')) {
    errors.push(`${file}: missing required keys`)
  }
}

if (errors.length > 0) {
  console.error('Cursor agent frontmatter validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log('Cursor agent frontmatter validation passed.')
