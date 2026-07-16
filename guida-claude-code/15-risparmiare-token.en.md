# 15 - Saving Tokens: rtk, ponytail and caveman

> Verified July 15, 2026: versions, install commands and numbers checked
> against GitHub and (for rtk) measured over months of real-world use.

## Why this chapter exists

If you're on a Pro plan, your budget is a window: ~200 messages every
5 hours (ch. 01). But the message isn't the unit that matters: **tokens**
are. And most of them aren't written by you: they're the *command outputs*
Claude runs (a `git log`, an `ls -la`, test output) and the *code and
prose* Claude generates. The 5 habits from ch. 14 cut behavioral waste;
the tools in this chapter cut waste **at the source, automatically**.
In plain terms: longer work windows on the same plan.

All three are third-party projects: the usual warning from ch. 07 and 09
applies: hooks and plugins run with your permissions, look at what you
install.

## rtk - compressing command outputs

**What it is**: a CLI proxy written in Rust ([rtk-ai/rtk](https://github.com/rtk-ai/rtk),
Apache 2.0) that sits between the commands and Claude: it runs the real
command and passes a **filtered, compressed** version of the output to the
context. A verbose `git status` becomes three dense lines; an `ls -la`
loses the permission bits Claude doesn't need. Claimed: 60–90% savings on
outputs.

**How to install it**:

```bash
brew install rtk        # or: curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
rtk init -g             # installs the hook for Claude Code + RTK.md, then restart Claude
```

**How it works**: `rtk init -g` adds a `PreToolUse` hook (ch. 07) that
transparently rewrites Claude's Bash commands into `rtk <command>`: Claude
asks for `git diff`, the system runs `rtk git diff`, and the compressed
output is what enters the context. You do nothing; Claude doesn't even
notice.

**What it actually saves**: from the counter (`rtk gain`) of a real
installation used over months of daily work:

```console
$ rtk gain
Total commands:    6812
Tokens saved:      2.1M (54.3%)
```

Half the tokens from command outputs, gone. On a Pro plan that's the
difference between a window that runs out mid-afternoon and one that lasts
until evening. It's the tool with the best benefit-to-risk ratio in this
chapter: it doesn't change *what* Claude does, only the size of what it
reads.

## ponytail - less generated code

**What it is**: a plugin ([DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail))
that installs a lazy senior dev "persona": shortest solution that works,
stdlib before dependencies, no speculative abstractions, minimal diff. The
token savings follow from the design: **less generated code = fewer output
tokens** (and often fewer bugs to review).

**How to install it** (it's the live example from ch. 09):

```bash
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail
```

**How it works**: a `SessionStart` hook injects the rules into every
session; three intensity levels (`/ponytail lite|full|ultra`); deliberate
shortcuts are marked with `ponytail:` comments so they stay tracked.

**What it saves** (the project's own benchmark, 3 models × 10 runs,
medians vs a no-plugin baseline): lines of code **46%**, tokens **78%**,
cost **80%**, time **73%** (with safety unchanged). That is: -22% tokens
and half the code to read. An honest warning: it shifts the code's *style*
toward minimalism; try it on a project of your own before adopting it:
either you'll like it, or it'll get on your nerves.

## caveman - terse replies (with an asterisk)

**What it is**: a plugin ([JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman))
that makes the agent's **prose replies** terse ("why use many token
when few token do trick"), leaving code, commands and errors untouched
byte for byte.

**How to install it**:

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

**The asterisk**: the project claims ~65% savings on *prose output*
tokens; but ponytail's independent benchmark (which uses it as a point of
comparison) measures it at **+7% total tokens** on coding tasks, because
on real tasks prose is a small slice, and the "caveman" style sometimes
makes the round-trip longer. The practical verdict: take it for
*readability* (replies you can scan in two seconds), not for savings.
For your budget, rtk and ponytail are what count.

## The right order for a Pro plan

1. **rtk**: right away, measured savings of ~50%+ on outputs, zero
   behavior changes, uninstalls without a trace.
2. **ponytail**: once you've made peace with the minimalist style, -22%
   tokens and much less code to review.
3. **caveman**: a matter of taste, not of budget.

And remember the biggest lever is still free: the 5 habits from ch. 14.
Method first, then tools.

---

**In short**: the token that never enters the context is the only one you
don't pay for and that doesn't confuse the model. rtk compresses what
Claude reads, ponytail cuts what Claude writes, caveman shortens what
Claude tells you. Only the first two, though, actually move the budget.
