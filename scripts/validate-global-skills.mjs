#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const skillsDir = path.join(root, 'ai', 'claude_code', 'global', 'skills')

function listSkillFiles(dir) {
  if (!fs.existsSync(dir)) return []
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => path.join(dir, d.name, 'SKILL.md'))
    .filter(p => fs.existsSync(p))
}

function parseFrontMatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/)
  if (!m) return null
  const body = m[1]
  const name = (body.match(/^name:\s*(.+)$/m) || [])[1]?.trim() ?? ''
  const hasDescription = /^description:\s*(.+)?$/m.test(body)
  return { name, hasDescription }
}

const headingChecks = [
  {
    label: 'When to use',
    regex: /^##\s+(When to use|いつ使うか)/m,
  },
  {
    label: 'When NOT to use',
    regex: /^##\s+(When NOT to use|Don['’]t use when)/m,
  },
  {
    label: 'Trigger Keywords',
    regex: /^##\s+(Trigger Keywords|Trigger Keywords?)/m,
  },
  {
    label: 'Procedure',
    regex: /^##\s+(Procedure|手順|生成プロトコル)/m,
  },
]

const files = listSkillFiles(skillsDir)
const errors = []

for (const file of files) {
  const text = fs.readFileSync(file, 'utf8')
  const rel = path.relative(root, file)
  const dirName = path.basename(path.dirname(file))
  const fm = parseFrontMatter(text)

  if (!fm) {
    errors.push(`${rel}: missing frontmatter`)
    continue
  }
  if (fm.name !== dirName) {
    errors.push(`${rel}: name must match directory (${dirName})`)
  }
  if (!fm.hasDescription) {
    errors.push(`${rel}: missing description`)
  }

  for (const check of headingChecks) {
    if (!check.regex.test(text)) {
      errors.push(`${rel}: missing heading '${check.label}'`)
    }
  }
}

if (errors.length) {
  console.error('Global skill validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log(`Global skill validation passed (${files.length} files).`)
