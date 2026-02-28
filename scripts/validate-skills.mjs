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
    .sort()
}

function parseFrontMatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/)
  if (!m) return null
  const body = m[1]
  const fields = body
    .split('\n')
    .filter(Boolean)
    .map(line => line.split(':')[0].trim())
  const name = (body.match(/^name:\s*(.+)$/m) || [])[1]?.trim() ?? ''
  const description = (body.match(/^description:\s*(.+)$/m) || [])[1]?.trim() ?? ''
  return { fields, name, description }
}

function countBullets(text, section) {
  const m = text.match(new RegExp(`\\n## ${section}\\n([\\s\\S]*?)(\\n## |$)`))
  if (!m) return 0
  return (m[1].match(/^- /gm) || []).length
}

function countSteps(text) {
  const m = text.match(/\n## Procedure\n([\s\S]*?)(\n## |$)/)
  if (!m) return 0
  return (m[1].match(/^\d+\. /gm) || []).length
}

function countExamples(text) {
  const m = text.match(/\n## Examples\n([\s\S]*?)$/)
  if (!m) return 0
  return (m[1].match(/^### Example \d+/gm) || []).length
}

function countNgExamples(text) {
  const m = text.match(/\n### NG例\n([\s\S]*?)(\n## |$)/)
  if (!m) return 0
  return (m[1].match(/^❌ /gm) || []).length
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

  if (fm.name !== dirName) errors.push(`${rel}: name must match directory (${dirName})`)
  if (!/^[a-z-]+$/.test(fm.name)) errors.push(`${rel}: name must match ^[a-z-]+$`)
  if (fm.name.length > 64) errors.push(`${rel}: name exceeds 64 chars`)
  for (const bad of ['helper', 'utils', 'tools', 'documents']) {
    if (fm.name.includes(bad)) errors.push(`${rel}: name must not contain '${bad}'`)
  }

  if (fm.fields.length !== 2 || !fm.fields.includes('name') || !fm.fields.includes('description')) {
    errors.push(`${rel}: frontmatter must only include name and description`)
  }

  if (!fm.description.includes('When NOT to use') || !fm.description.includes('Trigger Keywords')) {
    errors.push(`${rel}: description must be 3-element format`)
  }
  if (!fm.description.startsWith('Use proactively when') && !fm.description.startsWith('Use when the user explicitly asks')) {
    errors.push(`${rel}: description must start with proactive or explicit pattern`)
  }
  if (fm.description.length > 1024) errors.push(`${rel}: description exceeds 1024 chars`)
  if (/[<>]/.test(fm.description)) errors.push(`${rel}: description must not contain angle brackets`)
  if (firstPerson.test(fm.description)) errors.push(`${rel}: description must not contain first-person pronouns`)

  const sectionChecks = [
    '# ',
    '## When to use',
    '## When NOT to use',
    '## Trigger Keywords',
    '## Procedure',
    '## Output Contract',
    '## Examples',
  ]
  for (const heading of sectionChecks) {
    if (!text.includes(heading)) errors.push(`${rel}: missing heading '${heading}'`)
  }

  const whenToUse = countBullets(text, 'When to use')
  const whenNot = countBullets(text, 'When NOT to use')
  const keywords = countBullets(text, 'Trigger Keywords')
  const steps = countSteps(text)
  const examples = countExamples(text)
  const ngExamples = countNgExamples(text)

  if (whenToUse < 2 || whenToUse > 3) errors.push(`${rel}: When to use bullets must be 2-3`)
  if (whenNot < 2 || whenNot > 3) errors.push(`${rel}: When NOT to use bullets must be 2-3`)
  if (keywords < 3 || keywords > 5) errors.push(`${rel}: Trigger Keywords must be 3-5`)
  if (steps < 4 || steps > 6) errors.push(`${rel}: Procedure steps must be 4-6`)
  if (examples !== 3) errors.push(`${rel}: Examples must be exactly 3`)
  if (ngExamples < 3 || ngExamples > 5) errors.push(`${rel}: NG examples must be 3-5`)

  if (!text.includes('Input:') || !text.includes('Output:')) {
    errors.push(`${rel}: Examples must contain Input/Output pairs`)
  }

  if (text.split('\n').length > 500) {
    errors.push(`${rel}: SKILL.md must be <= 500 lines`)
  }
}

if (errors.length) {
  console.error('Skill validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log(`Skill validation passed (${files.length} files).`)
