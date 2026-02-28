#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const ROOT = process.cwd()
const APPLY = process.argv.includes('--apply')

function readDescriptionFromMd(file) {
  if (!fs.existsSync(file)) return null
  const text = fs.readFileSync(file, 'utf8')
  const match = text.match(/^description:\s*(.+)$/m)
  return match ? match[1].trim() : null
}

function readDescriptionFromToml(file) {
  if (!fs.existsSync(file)) return null
  const text = fs.readFileSync(file, 'utf8')
  const match = text.match(/^description\s*=\s*"([\s\S]*?)"$/m)
  return match ? match[1].trim() : null
}

function writeDescriptionMd(file, desc) {
  const text = fs.readFileSync(file, 'utf8')
  const updated = text.replace(/^description:\s*.+$/m, `description: ${desc}`)
  fs.writeFileSync(file, updated)
}

function writeDescriptionToml(file, desc) {
  const text = fs.readFileSync(file, 'utf8')
  const updated = text.replace(/^description\s*=\s*"[\s\S]*?"$/m, `description = "${desc}"`)
  fs.writeFileSync(file, updated)
}

const claudeDir = path.join(ROOT, '.claude', 'agents')
const names = fs
  .readdirSync(claudeDir)
  .filter(name => name.endsWith('.md'))
  .map(name => name.replace(/\.md$/, ''))
  .sort()

const mismatches = []

for (const name of names) {
  const claudeFile = path.join(ROOT, '.claude', 'agents', `${name}.md`)
  const cursorFile = path.join(ROOT, '.cursor', 'agents', `${name}.md`)
  const codexFile = path.join(ROOT, '.codex', 'agents', `${name}.toml`)

  const source = readDescriptionFromMd(claudeFile)
  const cursor = readDescriptionFromMd(cursorFile)
  const codex = readDescriptionFromToml(codexFile)

  if (!source || !cursor || !codex) {
    mismatches.push({ name, reason: 'missing file or description' })
    continue
  }

  if (source !== cursor || source !== codex) {
    mismatches.push({ name, source, cursor, codex })
    if (APPLY) {
      writeDescriptionMd(cursorFile, source)
      writeDescriptionToml(codexFile, source)
    }
  }
}

console.log(JSON.stringify({ apply: APPLY, mismatches }, null, 2))
if (mismatches.length > 0 && !APPLY) process.exit(1)
