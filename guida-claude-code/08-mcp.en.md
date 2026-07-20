# 08 - MCP: giving Claude new eyes and hands

> Verified on July 15, 2026 against the official docs (v2.1.210).

## What it is and what it's for

The Model Context Protocol is the standard Claude Code uses to connect to
external tools: a browser, Figma, GitHub, your database. The right analogy
is a **power outlet**: an MCP server is a socket where Claude plugs in new
senses and new hands. Out of the box, Claude Code can read and write files
and run shell commands; every MCP server you connect adds capabilities it
doesn't have on its own.

Concretely, a server can bring three things:

- **tools**: new actions Claude can perform ("open this page in the
  browser", "list the GitHub issues");
- **resources**: data you can reference in chat as if they were files;
- **prompts**: ready-made commands the server makes available.

Tools are the part you'll use all the time; resources and prompts are
bonuses we'll get to later.

## How to add a server

The command is `claude mcp add`, from the terminal (not inside a session).
The form changes depending on *where the server runs*.

**Local server (stdio)**. A process that Claude Code starts on your machine
and talks to over stdin/stdout:

```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

Let's read it piece by piece: `playwright` is the **name** you give the
server (you'll see it everywhere: in permissions, in `/mcp`, in tool
names); the `--` is a **required separator**: everything to its right is
the command that starts the server, not options for `claude mcp`; `npx -y
@playwright/mcp@latest` is that command (the `-y` skips npx's interactive
confirmation, which would block the automatic startup).

**Remote server (HTTP)**. A service running elsewhere, typically operated
by the vendor; there's no process to start here, just a URL:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

`--transport http` tells Claude Code it should *connect* rather than
*execute*; `figma` is again a name of your choosing; the URL is the
service's endpoint.

**Management**: three commands worth knowing:

```bash
claude mcp list      # all configured servers, with connection status
claude mcp get name  # details of a server
claude mcp remove name
```

## How it works: what happens at startup

When a session starts, Claude Code reads the list of configured servers,
launches the stdio processes and connects to the HTTP endpoints. Each
server responds by declaring the tools it offers, and from that point on
those tools exist for Claude alongside the native ones (Read, Bash…). You
do nothing: you ask "open the homepage and tell me what you see" and Claude
picks the right server's tool, just as it would pick Read for a file.

Remote servers often require an OAuth login: after the add, "Needs
authentication" shows up. You resolve it in a session: `/mcp` → select the
server → Authenticate (the browser opens for the login), or from the CLI
with `claude mcp login name`.

The `/mcp` panel is also your control dashboard:

![The /mcp panel: local servers and claude.ai connectors, with status and tool count](assets/08-mcp-panel.svg)

What to notice in the screenshot: the panel has **two sections**. At the
top, the **Local MCPs**, i.e. the servers you configured on this machine:
for each one you see the **status** (connected or failed: the first thing
to check when "Claude can't see the browser") and the **number of tools**
it brings (here Playwright is connected with 24 tools). Below, the
**claude.ai connectors**: integrations tied to your account, which show up
in Claude Code without any local configuration.

## Scopes: where the configuration lives

`claude mcp add` writes the configuration to one of three places, chosen
with `--scope`. The question they answer is: *who should have this server?*

| Scope | Where | For whom |
|---|---|---|
| `local` (default) | personal config, for this project | you |
| `project` | **`.mcp.json` in the root, committed** | the whole team |
| `user` | personal config, all projects | you, everywhere |

`local` and `user` live in your personal config, outside the repo: they're
your business. `project`, on the other hand, writes an **`.mcp.json` file
in the project root**, meant to be committed: that's how you share the
stack with the team. Whoever clones the repo gets the servers already
configured.

!!! tip "The right scope is the lowest one that fits"
    `local` for your own experiments, `project` only when the server truly
    needs to be shared with the team, `user` only for what you use
    everywhere. The default (`local`) is already the cautious choice: raise
    it only when you need to.

Here's a complete `.mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

The structure mirrors the CLI command: `mcpServers` is the
name → definition map; `"type": "stdio"` says how to talk to the server;
`command` and `args` are the startup command, split into executable and
arguments (what sat to the right of the `--` on the terminal).

Two security mechanisms tied to this file. First: the first time you open
the project, Claude Code shows you the listed servers and **asks whether
you trust them**: these are processes that will run on your machine with
your permissions, and someone else wrote the file; trust is earned, not
automatic. Second: in the values you can use `${VAR}` or `${VAR:-default}`,
expanded from the environment at startup. API keys stay in each person's
environment variables, never committed in the JSON.

## How tools appear to Claude

Every MCP tool has a name with a fixed scheme: `mcp__server__tool`, e.g.
`mcp__github__list_issues` is the `list_issues` tool of the server you
named `github`. This scheme matters most in **permissions** (ch. 02),
where a wildcard lets you approve an entire server in one go:

```json
"allow": ["mcp__playwright__*"]
```

A fair question: don't ten servers with hundreds of tools clog the
context? Since 2026, no: tool schemas load **on demand** (tool search):
Claude sees the list of names, but a tool's full definition only enters
the context when it's actually needed.

And the two bonuses promised at the start, often overlooked:

- **resources** are referenced with `@server:protocol://path`, e.g.
  `@github:issue://123` brings that issue into the context, with the same
  `@` syntax you use for files (ch. 03);
- server **prompts** become slash commands:
  `/mcp__github__pr_review 456` runs the GitHub server's `pr_review`
  prompt with the argument `456`.

## Which servers, for a frontend dev

The four that matter are in chapter 10 (Playwright, the Chrome extension,
Chrome DevTools, Figma), with the full workflow. Here's the general rule, which
holds for any server: **every server is code running with your
permissions**. So: add what you use, remove what you don't (an occasional
`claude mcp list` as housekeeping), and only trust known sources. And if a
tool returns huge outputs (it happens, with web pages),
`MAX_MCP_OUTPUT_TOKENS` in the settings caps how much of it enters the
context.

!!! warning "Risk surface"
    An MCP server is code running on your machine with your permissions.
    The same caution as with hooks (ch. 07) applies: install only what you
    use, from sources you know, and clean up what you no longer need.

---

**In short**: `claude mcp add` for yourself, a committed `.mcp.json` for
the team, `/mcp` for status and authentication. MCP is the multiplier: on
its own Claude sees the filesystem, with MCP it sees your browser and your
design system. The next chapter shows how to package all of this; the one
after that is the actual frontend workflow.
