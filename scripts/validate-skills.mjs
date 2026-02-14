#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const skillsDir = path.join(root, '.claude', 'skills')
const firstPerson = /\b(i|me|my|mine|we|our|ours)\b/i

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
  const description = (body.match(/^description:\s*(.+)$/m) || [])[1]?.trim() ?? ''
  return { name, description }
}

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
  if (!/^[a-z-]+$/.test(fm.name)) {
    errors.push(`${rel}: name must match ^[a-z-]+$`)
  }
  if (fm.name.length > 64) {
    errors.push(`${rel}: name exceeds 64 chars`)
  }
  if (!fm.description.startsWith('Use when')) {
    errors.push(`${rel}: description must start with 'Use when'`)
  }
  if (fm.description.length > 1024) {
    errors.push(`${rel}: description exceeds 1024 chars`)
  }
  if (/[<>]/.test(fm.description)) {
    errors.push(`${rel}: description must not contain angle brackets`)
  }
  if (firstPerson.test(fm.description)) {
    errors.push(`${rel}: description must not contain first-person pronouns`)
  }

  const examplesSection = text.split(/\n## Examples\n/)[1] ?? ''
  const exampleCount = (examplesSection.match(/^### Example\s+\d+/gm) || []).length
  if (exampleCount < 3 || exampleCount > 5) {
    errors.push(`${rel}: examples must be between 3 and 5`)
  }
}

if (errors.length) {
  console.error('Skill validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log(`Skill validation passed (${files.length} files).`)
