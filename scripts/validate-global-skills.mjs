#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const skillsDir = path.join(root, 'ai', 'claude_code', 'global', '.claude', 'skills')

/** Rule-style skills applied on edit; no trigger description required */
const RULE_ONLY_SKILLS = new Set(['markdown-line-length'])

const procedureHeading = /^##\s+(Procedure|手順|進め方|いつ使うか|目的|振る舞い|生成プロトコル)/m

function listSkillFiles(dir) {
  if (!fs.existsSync(dir)) return []
  return fs
    .readdirSync(dir, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => path.join(dir, d.name, 'SKILL.md'))
    .filter(p => fs.existsSync(p))
    .sort()
}

function extractDescription(body) {
  if (/^description:\s*"/m.test(body)) {
    const m = body.match(/^description:\s*"([^"]*)"/m)
    return m ? m[1] : ''
  }
  if (/^description:\s*\|/m.test(body)) {
    const lines = body.split('\n')
    const start = lines.findIndex(l => l.startsWith('description:'))
    if (start === -1) return ''
    const content = []
    for (let i = start + 1; i < lines.length; i++) {
      const line = lines[i]
      if (/^[a-z][a-z0-9-]*:/i.test(line)) break
      content.push(line.replace(/^ {2}/, ''))
    }
    return content.join('\n').trim()
  }
  const m = body.match(/^description:\s*(.+)$/m)
  return m ? m[1].trim() : ''
}

function parseFrontMatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---\n/)
  if (!m) return null
  const body = m[1]
  const name = (body.match(/^name:\s*(.+)$/m) || [])[1]?.trim() ?? ''
  const description = extractDescription(body)
  const fields = body
    .split('\n')
    .filter(Boolean)
    .map(line => line.split(':')[0].trim())
  return { name, description, fields }
}

function hasThreeElementDescription(description) {
  const hasWhenNot = description.includes('When NOT to use')
  const hasKeywords = description.includes('Trigger Keywords')
  const hasUseWhen = /Use (proactively )?when/i.test(description)
  return hasWhenNot && hasKeywords && hasUseWhen
}

const files = listSkillFiles(skillsDir)
const errors = []
const relSkillsDir = path.relative(root, skillsDir)

if (files.length === 0) {
  errors.push(`${relSkillsDir}: no SKILL.md files found (check skills directory path)`)
}

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
  if (!fm.fields.includes('name') || !fm.fields.includes('description')) {
    errors.push(`${rel}: frontmatter must include name and description`)
  }
  if (!fm.description) {
    errors.push(`${rel}: missing description`)
  }

  if (!RULE_ONLY_SKILLS.has(fm.name)) {
    if (!hasThreeElementDescription(fm.description)) {
      errors.push(
        `${rel}: description must be 3-element format (Use when / When NOT to use / Trigger Keywords)`
      )
    }
    if (fm.description.length > 1024) {
      errors.push(`${rel}: description exceeds 1024 chars`)
    }
    if (!procedureHeading.test(text)) {
      errors.push(
        `${rel}: missing procedural heading (Procedure / 手順 / 進め方 / いつ使うか / 目的 / 振る舞い)`
      )
    }
  }

  if (!/^#\s+/m.test(text)) {
    errors.push(`${rel}: missing top-level heading`)
  }

  if (text.split('\n').length > 500) {
    errors.push(`${rel}: SKILL.md must be <= 500 lines`)
  }
}

if (errors.length) {
  console.error('Global skill validation failed:')
  for (const e of errors) console.error(`- ${e}`)
  process.exit(1)
}

console.log(`Global skill validation passed (${files.length} files).`)
