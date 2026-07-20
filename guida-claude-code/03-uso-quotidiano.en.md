# 03 - Day-to-day use

> Verified on July 15, 2026 against the official docs (v2.1.210).

In chapter 02 you configured Claude Code; here we look at how you work with
it every day. First, though, one interface concept you'll use in every
section of this chapter: slash commands.

## Slash commands: the control panel

**What they are**: commands that start with `/` (`/clear`, `/rewind`,
`/compact`…). They aren't prompts for the model: they're orders to the
Claude Code *application*, think of VS Code's command palette, but textual.

**Where they are**: anywhere you can type a prompt. Type `/` as the first
character and a menu opens with all the available commands, each with its
description; keep typing to filter, arrow keys + Enter to pick one. No need
to memorize them: the menu is the index.

This is the menu that appears when you type `/`: note the descriptions next
to each command:

![The command menu that opens when you type /](assets/03-slash-menu.svg)

The menu also shows skills (ch. 05): commands you can define yourself.

## The workflow: Explore → Plan → Code → Commit

**What it is**: the official pattern for non-trivial tasks. The core idea:
separate the *understanding* from the *doing*, so you correct Claude on a
ten-line plan instead of on a hundred lines of already-written code.

The four phases in practice:

1. **Explore** (in plan mode): "read `src/auth` and explain how the login
   works". Claude reads, searches, summarizes, but modifies nothing.
2. **Plan**: "prepare a detailed implementation plan". Claude produces the
   plan; with ++ctrl+g++ you open it in your editor and fix it *before* a
   single line of code gets written: it's the moment when review is
   cheapest.
3. **Code**: you approve the plan and Claude implements. On approval it
   asks which mode to proceed in: auto, `acceptEdits`, or manual review of
   every edit (the permission modes from ch. 02).
4. **Commit**: "commit with a descriptive message".

**Plan mode, concretely**: it's one of the permission modes, Claude can
only read and explore, never write. You activate it by cycling with
++shift+tab++ (the same key cycles through all the modes) or at startup
with `claude --permission-mode plan`. You know you're in it because the
status bar under the prompt says so, like here:

![Plan mode active, shown in the bar under the prompt](assets/03-plan-mode.svg)

It's also a great way to explore a new codebase risk-free: "it
can't touch anything" is guaranteed by the permission system, not by the
model's good intentions.

!!! tip "When to skip the plan"
    If the diff can be described in one sentence (a typo, a rename, one log
    line), plan mode is pure overhead. Go direct.

## Checkpoints and /rewind: the safety net

**What it is**: Claude Code's undo. Every time Claude modifies a file, a
checkpoint is saved, a snapshot you can return to, like git restore points
but automatic and per-change.

**Where it is**: press ++esc++ ++esc++ (with an empty input) or type
`/rewind`. The restore menu opens with the list of checkpoints:

![The Rewind menu: every change is a restore point](assets/03-rewind-menu.svg)

**How to use it**: pick the point to go back to and *what* to restore.

- **code + conversation**: you go back all the way;
- **code only**: the files revert, but the conversation stays (useful for
  saying "do it again, but this time like this");
- **conversation only**: you keep the code, rewind the chat.
- "Summarize from here" / "up to here": doesn't restore, it compresses,
  half the session becomes a summary, the other half stays intact.

**How it changes the way you work**: you can let Claude *attempt* a risky
route ("rewrite the store with Zustand, let's see") knowing the way back
costs two keystrokes.

!!! warning "Two limits to know"
    It tracks **only the edits Claude makes**, not bash commands (`rm`,
    `mv`), not your manual changes, and it keeps the last 100 checkpoints.

## The 2-attempt rule

If you've corrected Claude twice on the same point and it's still getting
it wrong, **don't push for a third correction**. The reason is mechanical:
every failed attempt and every correction of yours stays in the context,
and by now Claude is reasoning inside a story full of false leads. Better
`/clear` and a prompt rewritten from scratch that folds in what you've
learned: "do X; note that Y doesn't work because Z". A clean session with a
better prompt almost always beats a long session full of accumulated
corrections.

## Sessions

Every conversation is a **session**, saved automatically: closing the
terminal loses nothing. The operations you actually need:

| What | How |
|---|---|
| Resume the last one | `claude --continue` |
| Pick from the picker | `claude --resume` (or `/resume` in session) |
| Name it | `claude -n name` at startup, `/rename name` in session |
| Resume by name | `claude --resume name` |
| Fork the session | `/branch [name]`, explore an alternative without losing the main thread |

`/branch` deserves a note: it creates a *fork* of the current session, like
a git branch of the conversation. You try a different direction and, if it
doesn't pan out, the main thread is still there.

## Context management

**What the context is**: the model's working memory, everything Claude
"sees" when generating the next response. It's a window of fixed capacity,
and it doesn't hold just the chat: it holds the system prompt, the tool
definitions, the memory files (CLAUDE.md, ch. 04), the skills, and then
every message of yours, every file read, every command output. A freshly
opened session already consumes part of it before you type a word.

**Where you see it**: the `/context` command shows the usage grid by
category: it's the session's X-ray. Look at it: each cell is a slice of the
window, the categories in the legend tell you who's occupying it, and the
free space is what's left for the actual work:

![Output of /context: the context usage grid by category](assets/03-context.svg)

!!! note "Why it matters to you"
    The context fills up as you work, and the fuller it gets the more
    performance degrades: Claude "forgets" the instructions given at the
    start, repeats mistakes already fixed. Almost every good habit in this
    guide stems from this.

The tools:

- `/clear`: empties the conversation. Use it **between one task and the
  next, always**: the new task doesn't need the previous one's history. No
  panic: the cleared session stays recoverable with `/resume`.
- `/compact [instructions]`: use it *inside* a long task, when the history
  is still needed but weighs too much: it replaces the conversation with a
  summary and picks up from there. The optional instructions say what to
  preserve: `/compact keep the file paths and the routing decisions`.
- `/context`: the periodic check described above (keep an eye on it in the
  statusline, ch. 14).
- `/btw question`: the side question ("what's the syntax for
  `grid-area`?") that does NOT enter the history: the answer shows in an
  overlay, context untouched. Small but a session-saver.

## Shortcuts and input tricks

The reference table, then the three tricks that deserve detail:

| Key | Effect |
|---|---|
| ++esc++ | interrupts Claude (your queued messages stay) |
| ++esc++ ++esc++ | input full: clears the line; input empty: opens `/rewind` |
| ++ctrl+c++ | first press: clears the input; second: exits |
| ++shift+tab++ | cycles the permission modes (ch. 02) |
| `!command` | shell mode: runs the command, output goes into the context |
| `@path` | reference a file (autocomplete) |
| ++ctrl+v++ | pastes an image from the clipboard (essential for frontend: screenshot → "reproduce this layout") |
| ++ctrl+o++ | detailed transcript (tool calls, timings, model) |
| ++ctrl+r++ | search the history |
| ++ctrl+b++ | sends the running command to the background |
| ++alt+t++ / ++option+t++ | toggles extended thinking (for the hard problems; on some models it's always on) |

**Shell mode (`!`)**: type `!` as the first character and the input changes
appearance, pink prompt, "! for shell mode" hint at the bottom: you're no
longer talking to the model, you're writing a command for your shell. The
command runs directly and the output lands in the context, where Claude
sees it. It's the fastest way to give it a fact from reality:
`! npm run test` and then "fix the failing tests". Here's what the input
looks like in shell mode:

![Input in shell mode: pink prompt and "! for shell mode" hint](assets/03-shell-mode.svg)

**Referencing files with `@`**: type `@` and autocomplete kicks in over the
project's files, keep typing to filter, Enter to insert the path. Claude
receives the *reference* and goes and reads the file itself: more precise
than "the button file" and cheaper than pasting its contents (ch. 14). This
is what the autocomplete looks like:

![File autocomplete when typing @](assets/03-at-file.svg)

**Message queue**: while Claude is working you can type and press Enter:
the message queues up for the next turn. No need to wait.

**Vim mode**: `/config` → Editor mode, for those who can't live without it.

## Switching models: /model

`/model` opens the picker: you choose the model and the *effort* level (how
much reasoning to invest). The default is fine for everyday work; which
model for which task, and what it costs, is the subject of ch. 14. The
picker:

![The /model picker: available models and effort level](assets/03-model-picker.svg)

## Two commands you don't expect

- `/recap`: a summary of the session. On Monday morning, after
  `claude --continue`, it answers the question "where were we?".
- `/goal condition`: you set a completion condition that Claude can't
  declare met until it's actually true (the mechanics are in ch. 11, where
  it's one rung of the verification ladder).

---

**In short**: plan mode for big tasks, ++esc++ ++esc++ as the universal
undo, `/clear` between tasks, and the 2-attempt rule when you get stuck. The next
chapter digs into the most important file in your setup: the CLAUDE.md.
