#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const dir = path.join(root, '.claude', 'agents')
const colors = new Set(['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'Pink', 'Cyan'])
const errors = []

for (const entry of fs.readdirSync(dir).filter(f => f.endsWith('.md'))) {
  const file = path.join(dir, entry)
  const text = fs.readFileSync(file, 'utf8')
  const fm = text.match(/^---\n([\s\S]*?)\n---\n/)
  if (!fm) {
    errors.push(`${entry}: missing frontmatter`)
    continue
  }

  const required = [
    'name:',
    'description:',
    'color:',
    'tools:',
    'disallowedTools:',
    'model:',
    'memory: project',
  ]
  for (const req of required) {
    if (!fm[1].includes(req)) errors.push(`${entry}: missing '${req}'`)
  }

  const colorMatch = fm[1].match(/^color:\s*(.+)$/m)
  if (!colorMatch || !colors.has(colorMatch[1].trim())) {
    errors.push(`${entry}: invalid color '${colorMatch ? colorMatch[1].trim() : ''}'`)
  }

  const descMatch = fm[1].match(/^description:\s*(.+)$/m)
  const desc = descMatch ? descMatch[1] : ''
  if (!desc.includes('When NOT to use') || !desc.includes('Trigger Keywords')) {
    errors.push(`${entry}: description is not 3-element format`)
  }

  for (const heading of ['## Workflow', '## Checklist', '## Output Format', '## Memory Strategy']) {
    if (!text.includes(heading)) errors.push(`${entry}: missing heading '${heading}'`)
  }
}

if (errors.length > 0) {
  console.error('Claude agent validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log('Claude agent validation passed.')
