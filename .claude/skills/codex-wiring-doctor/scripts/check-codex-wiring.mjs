#!/usr/bin/env node
import fs from 'node:fs'
import path from 'node:path'

const AGENT_DIR = path.join(process.cwd(), '.codex', 'agents')
const CONFIG_GLOBS = [
  path.join(process.cwd(), '.codex', 'config.toml'),
  path.join(process.cwd(), '.codex', 'config.preset.review.toml'),
  path.join(process.cwd(), '.codex', 'config.preset.audit.toml'),
]

function listAgentFiles() {
  if (!fs.existsSync(AGENT_DIR)) return []
  return fs
    .readdirSync(AGENT_DIR)
    .filter(name => name.endsWith('.toml'))
    .sort()
}

function extractConfigRefs(filePath) {
  if (!fs.existsSync(filePath)) return []
  const text = fs.readFileSync(filePath, 'utf8')
  const refs = []
  const regex = /^config_file\s*=\s*"([^"]+)"/gm
  for (const match of text.matchAll(regex)) {
    refs.push(match[1])
  }
  return refs
}

const agents = listAgentFiles().map(name => `./.codex/agents/${name}`)
const refs = CONFIG_GLOBS.flatMap(extractConfigRefs)

const refSet = new Set(refs)
const agentSet = new Set(agents)

const orphan = agents.filter(agent => !refSet.has(agent))
const dangling = refs.filter(ref => !agentSet.has(ref))

const status = orphan.length === 0 && dangling.length === 0 ? 'PASS' : 'FAIL'

console.log(
  JSON.stringify(
    {
      status,
      agents,
      refs,
      orphan,
      dangling,
    },
    null,
    2
  )
)

if (status !== 'PASS') process.exit(1)
