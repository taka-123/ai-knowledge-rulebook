![Prompting guide](https://developers.openai.com/images/codex/prompting_codex.webp)

Just like ChatGPT, Codex is only as effective as the instructions you give it. Here are some tips we find helpful when prompting Codex:

## Provide clear code pointers

Codex is good at locating relevant code, but it’s more efficient when the prompt narrows its search to a few files or packages. Whenever possible, use **greppable identifiers, full stack traces, or rich code snippets**.

## Include verification steps

Codex produces higher-quality outputs when it can verify its work. Provide **steps to reproduce an issue, validate a feature, and run any linter or pre-commit checks**. If additional packages or custom setups are needed, see [Environment configuration](https://developers.openai.com/codex/cloud/environments).

## Customize how Codex does its work

You can **tell Codex how to approach tasks or use its tools**. For example, ask it to use specific commits for reference, log failing commands, avoid certain executables, follow a template for PR messages, treat specific files as AGENTS.md, or draw ASCII art before finishing the work.

## Split large tasks

Like a human engineer, Codex handles really complex work better when it’s broken into smaller, focused steps. Smaller tasks are easier for Codex to test and for you to review. You can even ask Codex to help break tasks down.

## Leverage Codex for debugging

When you hit bugs or unexpected behaviors, try **pasting detailed logs or error traces into Codex as the first debugging step**. Codex can analyze issues in parallel and could help you identify root causes more quickly.

## Try open-ended prompts

Beyond targeted tasks, Codex often pleasantly surprises us with open-ended tasks. Try asking it to clean up code, find bugs, brainstorm ideas, break down tasks, write a detailed doc, etc.

Prompting guide
