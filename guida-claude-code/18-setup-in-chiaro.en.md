# 18 - The setup in plain sight: the files, line by line

> Ch. 16 covers the philosophy: three levels, what goes where. This
> chapter shows the **actual files** from my setup (July 2026), sanitized
> per the guide's policy: real structure and real rules, but the paths and
> names of client work projects are swapped for generic stand-ins (`acme`).
> It's not a template to copy wholesale: it's a working example to steal the
> pieces you need from.

## Permissions: allow, deny, ask

The `permissions` block in my global `~/.claude/settings.json` uses all
three lists, and each one does a different job:

```json
{
  "permissions": {
    "allow": [
      "Bash(rtk git status:*)",
      "Bash(rtk git diff:*)",
      "Bash(rtk git log:*)",
      "Bash(rtk git show:*)",
      "Bash(rtk git branch:*)",
      "Bash(rtk ls:*)",
      "Bash(rtk read:*)",
      "Bash(rtk grep:*)",
      "Bash(rtk rg:*)",
      "Bash(rtk wc:*)",
      "Bash(rtk git add:*)",
      "Bash(rtk git commit:*)",
      "Bash(rtk git push:*)",
      "WebSearch",
      "WebFetch(domain:github.com)",
      "WebFetch(domain:raw.githubusercontent.com)",
      "WebFetch(domain:www.npmjs.com)",
      "Bash(make check)",
      "mcp__atlassian__getJiraIssue",
      "mcp__atlassian__searchJiraIssuesUsingJql"
    ],
    "deny": [
      "Read(~/.config/acme/**)",
      "Read(**/.env)",
      "Read(**/.env.local)",
      "Read(**/credentials.json)",
      "Read(**/*.pem)",
      "Read(**/*.key)",
      "Read(~/.ssh/**)",
      "Read(~/.aws/credentials)",
      "Bash(*secrets.env*)",
      "Bash(*.config/acme*)",
      "Bash(*ACME_LLM_API_KEY*)",
      "Bash(*id_rsa*)",
      "Bash(*.ssh/*)"
    ],
    "ask": [
      "Bash(* .env*)",
      "Bash(*.pem*)",
      "Bash(*.key*)",
      "Bash(*credentials.json*)",
      "Bash(*~/.aws/*)"
    ]
  }
}
```

**Allow** holds only zero-risk operations I'd approve blindfolded a hundred
times a day: read-only git inspection (via rtk, ch. 15), reading files and
searching, the main repo's build gate, the documentation domains I consult
all the time, two read-only Jira tools. `git add`/`commit`/`push` look like
an exception to that principle, but they're covered elsewhere: the "never
commit without asking" rule lives in CLAUDE.md, and a hook (below) guards
the message content. Two limits I never cross: **never allowlist
interpreters** (`python`, `node`: that's arbitrary execution under another
name) and **never a generic `curl`** (it can POST, so it can exfiltrate
whatever it just read).

**Deny** protects secrets, and its history is a three-act lesson in syntax:

1. *Single-slash absolute paths don't work.* In file rules,
   `Read(/home/io/...)` is interpreted **relative to the settings file's
   directory**: my first deny-list blocked nothing at all. An absolute path
   is written `//path` (double slash) or, better, with `~/`.
2. *Don't enumerate commands, describe the sensitive string.* The first
   version had 32 rules (`cat`, `head`, `xxd`, `dd`, `strings`…) and still
   leaked: the list of ways to read a file is endless (`bash -c`, `perl`, a
   `<` redirect). Bash rules accept wildcards mid-pattern too, so
   `Bash(*secrets.env*)` denies **any** command that names that file, no
   matter which binary runs it. Three rules like that cover strictly more
   than the 32 before them.
3. *String matching is still gameable in principle* (indirect paths like
   `cat ~/.config/ac*/sec*`). The watertight version is the sandbox's
   `filesystem.denyRead`, which blocks reads at the kernel level for any
   child process. It's on my list of things to evaluate.

**Ask** is the most recent discovery: the missing middle ground. A pattern
as broad as "any command that touches a `.env`" in deny would cause real
damage: `cp .env.example .env` is a legitimate operation my fixtures do
routinely. With ask, the command pauses instead and asks: I deny suspicious
uses by hand, legitimate ones go through with a keystroke. The criterion I
distilled from this: **deny only where a false positive is nearly
impossible; ask where the pattern is broad**. There's no appeal with deny,
and a rule that fights you ends up deleted, which is worse than a rule that
asks.

## Hooks: the rules that always hold

Two global hooks and one project hook, all born from the same criterion
(ch. 07 and 16): if an "almost never" violation is still one too many, the
rule deserves a hook.

**PreToolUse on Bash, first hook: rtk.** One line, `rtk hook claude`, that
transparently rewrites commands into their compressed variant (ch. 15). No
semantics involved, just token savings on every project.

**PreToolUse on Bash, second hook: the commit guardian.** The file is
`~/.claude/hooks/block-ai-commit.sh`, and I'm quoting it in full because
it's my favorite example of a small hook done well:

```sh
#!/bin/sh
# PreToolUse hook (Bash): block git commit messages that mention AI assistance.
# Exit 2 = block the tool call and show stderr to the model.
cmd=$(jq -r '.tool_input.command // empty')
case "$cmd" in
  *"git commit"*) ;;
  *) exit 0 ;;
esac
# Narrow patterns on purpose — "anthropic" alone would block legitimate
# commits about Anthropic SDK code; widen only if something slips.
if printf '%s' "$cmd" | grep -qiE 'co-authored-by:[^"]*\b(claude|anthropic)|generated with|noreply@anthropic\.com|🤖'; then
  echo "Commit bloccato: il messaggio viola le regole del CLAUDE.md. Riscrivilo." >&2
  exit 2
fi
exit 0
```

The choices that matter: it exits immediately if the command isn't a commit
(zero cost on 99% of cases); exit code 2 blocks the tool **and** explains to
the model why, so it corrects itself on the next try; the patterns are
deliberately narrow (`anthropic` alone would block legitimate commits on
code that uses the Anthropic SDK), because a guardian that cries wolf on
false positives ends up disabled. The prose in CLAUDE.md explains the
intent; the hook *guarantees* it.

**Project-level PostToolUse: the autoformat.** In the main repo's
`.claude/settings.json`, on `Edit|Write`:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{ "type": "command",
                  "command": "make format >/dev/null 2>&1 || true" }]
    }]
  }
}
```

It lives at the repo level because it's *that repo's* formatter making the
call; the `|| true` is essential: a convenience hook must never block your
work if it fails.

## Agents: the standing team

Fifteen global agents in `~/.claude/agents/`, all born from the
just-in-time rule in ch. 16 (a role comes up twice → it gets persisted).
They split into two families, and the difference also governs the model:

- **Advisors** (they reason, they don't touch code): `architect`,
  `debugger`, `python-expert`, `web-fullstack`, `terraform-expert`,
  `cdk-python-expert`, `devops-hosting`, `data-engineer`, `data-scientist`,
  `data-analyst`, `cloud-ml-ai-engineer`. Common pattern: read-only tools
  (Read, Grep, Glob, Bash), "advise and sketch a diff, don't apply bulk
  edits", and a description that explicitly marks the boundary against
  neighboring agents ("NOT for Terraform → use terraform-expert"): that
  boundary is what lets the session pick the right agent without guessing
  wrong. No declared model: they inherit the session's, whichever is best
  available.
- **Executors** (they do one mechanical thing): `test-runner` (runs the
  suite in an isolated context, reports only the verdict: noise stays out
  of the session), `semantica-it`/`semantica-en` (prose reviewers, the only
  ones with Edit/Write) and `traduttore-it-en` (the `.en.md` twins of this
  guide). These do declare a model, small and pinned: whoever *thinks*
  inherits the best, whoever *executes* stays cheap.

At the repo level, specific ones get added. In the main repo: a
*gate-runner* that runs the build gate, and a read-only *guardian* that
reviews diffs against architectural invariants (ch. 16). Both are committed
under `.claude/agents/`, so they apply to anyone who clones the repo.

## Skills and slash commands: the procedures

Twelve global skills in `~/.claude/skills/`, grouped by job:

- **Prose and bilingualism**: `humanize` (orchestrates the semantica-*
  reviewers), `sync-en` (finds Italian chapters changed via git and gets
  the English twins retranslated: it's the skill that keeps this guide
  bilingual).
- **Screenshots**: `screenshot` (the user shows me something),
  `screenshot-autonomo` (I look at the screen on my own),
  `screenshot-recenti` (reuses shots already taken). Three separate skills
  because the *trigger* is different: lumping them together confused the
  choice.
- **Browser**: `playwright-browser`, the generic core other domain-specific
  skills (demos, visual documentation) build on.
- **Knowledge**: `documenta-progetto` (writes project notes into the right
  vault, routing between personal and work), `graphify` (ch. 16),
  `llm-council` (five advisors on different models for business decisions
  with real stakes).
- **Hygiene**: `clean-conversations` and `purge-project` (per-project
  history cleanup), `new-agent` (the scaffolding for the just-in-time rule:
  when a role recurs, this skill persists it).

Plus two slash commands in `~/.claude/commands/`: `/commit` (stage, logical
commits, branch and push per my conventions) and `/standup` (the "where was
I" on the current repo). The practical difference from skills: commands are
procedures *I* invoke, skills are procedures the session can also choose to
use on its own when it recognizes the case.

## MCP: few, and at the right level

The list of MCP servers is deliberately short, and *where* matters as much
as *what*:

- **Global** (`~/.claude/mcp.json`): just `tolaria`, the server for my
  notes app, the Markdown vault where project documentation ends up. It's
  global because there's only one vault, whatever the context.
- **Per client profile**: `atlassian` (Jira) lives in the profile of the
  client who uses it, with its own authentication. In every other profile
  that Jira simply doesn't exist: the "I posted on the wrong ticket"
  incident becomes impossible by construction, not by discipline (ch. 16).

The criterion is the same as the three levels: an MCP belongs **at the
lowest level where it's needed**. And every extra server is more context
and risk surface: a well-reasoned no (ch. 16, the web-search server I
passed on) is as much a part of the setup as the yeses.

## Everything else: plugin, statusline, model

Three lines round out the picture. A plugin (`ponytail`, an output style
that enforces the laziest solution that works, YAGNI as a permanent mode);
a custom statusline (`statusline.sh`: branch, model and remaining context
at a glance); the model pinned in settings with the extended context
window. Everything else is default: every setting you don't write is a
setting you don't have to maintain.

## In short

The most important file in this chapter isn't any of the JSON blocks: it's
the criterion behind each one. Allow gets measured against transcripts, not
imagined; deny gets written for sensitive strings, not lists of commands;
ask covers the gray zone. Rules with no exceptions become hooks; agents get
born when a role recurs, never before; MCP servers sit at the lowest level
that justifies them. If your setup applies these criteria, it'll look like
mine only where our jobs overlap, and that's exactly the point.
