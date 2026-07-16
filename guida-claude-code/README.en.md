# A Guide to Claude Code

Claude Code is a **coding agent that lives in the terminal**: you describe
an outcome ("the login form doesn't validate the email: find out why and
fix it, with a test") and it reads the codebase, edits files, runs commands
and tests, and iterates until the task is done, asking your permission for
every action that matters. It's not a chat you copy code from, nor an
autocomplete: it's a collaborator working in your repo, and this guide
teaches you how to make it work **well**.

Everything was written and checked in **July 2026 against Claude Code
2.1.210**. The commands were run for real, the screenshots come straight
from the TUI, and the facts were verified against the
[official documentation](https://code.claude.com/docs) — still the place to
look once this guide starts to age.

## How to read it

**Basics - starting right (day 1):**

1. [Installation and first run](01-installazione.md) - from `curl` to your first prompt
2. [Setup and configuration](02-setup-e-config.md) - where config lives, permissions, deny rules for secrets
3. [Day-to-day use](03-uso-quotidiano.md) - the workflow, undo, session management
4. [CLAUDE.md and rules](04-claude-md-e-rules.md) - the project's permanent instructions

**Method - what makes the difference:**

5. [Verification](11-verifica.md) - *if you read only one chapter, make it this one*
6. [Prompt engineering](12-prompt-engineering.md) - asking for things in a way that works
7. [Common mistakes](13-errori-comuni.md) - recognizing them before you make them
8. [Research and design](17-ricerca-e-progettazione.md) - deep research, SPEC, Ultraplan and Claude Design: decide well before you build

**Power - once the basics are running:**

9. [Skills and slash commands](05-skills-e-slash-commands.md) - reusable procedures
10. [Agents](06-agenti.md) - who to delegate the noisy work to
11. [Hooks](07-hooks.md) - rules that always hold, not almost always
12. [MCP](08-mcp.md) - connecting browsers, Figma, GitHub
13. [Plugins](09-plugins.md) - your setup in a package
14. [Frontend workflow](10-workflow-frontend.md) - *for frontend devs: Claude with a real browser*

**Reference:**

15. [Must-haves and costs](14-must-have-e-costi.md) - the first 30 minutes of setup, the plans, the money-saving habits
16. [Saving tokens](15-risparmiare-token.md) - the tools for longer work windows on the Pro plan
17. [A real setup: global, per client, per repo](16-setup-a-tre-livelli.md) - how the author actually organizes it, three levels at a time

## What you need to follow along

A terminal, a Claude subscription (Pro is enough: ch. 01) and half an hour
for the Basics section. Chapters 02 and 04 use a small React/TS project as
their example; its files (`CLAUDE.md` and `.claude/settings.json`) are
shown in full within the chapters themselves: there's nothing to download.

## The promise

By the end of this guide you know how to: install and configure Claude
Code **safely** (your secrets stay yours), have it do real tasks **with a
method that holds up** (and notice right away when something goes wrong),
and **extend it** with automations and tools tailored to your work. Speed,
the one thing left, comes on its own with practice.
