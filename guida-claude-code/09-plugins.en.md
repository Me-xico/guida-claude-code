# 09 - Plugins: your setup in a package

> Verified on July 15, 2026 (v2.1.210).

## What they are and what they're for

A plugin packages everything you saw in chapters 5–8 into a single
installable unit: **skills, agents, hooks and MCP servers** (plus optional
themes and commands). The analogy is the package manager: just as
`npm install` brings you a library with all its parts instead of files to
copy by hand, `/plugin install` brings you a complete Claude Code setup.
It's the difference between "copy these five files to the right places and
configure three keys" and a single command.

## Where it lives: the structure

A plugin is a directory (typically a Git repo) with a structure you'll
recognize immediately, because it mirrors the previous chapters:

```
my-plugin/
├── manifest.json     # name, version, description
├── skills/           # skills (ch. 05)
├── agents/           # agents (ch. 06)
├── hooks/hooks.json  # hooks (ch. 07)
└── .mcp.json         # MCP servers (ch. 08)
```

The `manifest.json` is the identity card (name, version, description); the
other directories contain exactly the files you were putting in `.claude/`
in chapters 5–8. Here they travel together, versioned as one thing. When
the plugin is installed, Claude Code loads those contents at session
startup as if they were yours: the skills show up among the slash
commands, the hooks attach to their events, the MCP servers start up.

## How to install and manage it

Everything happens in a session, starting from `/plugin`:

```
/plugin                              # browse marketplaces and installed plugins
/plugin install name@marketplace
/reload-plugins                      # reload after changes to plugin files
```

`/plugin` on its own opens the management panel:

![The /plugin panel: installed plugins and marketplaces to browse](assets/09-plugin-browser.svg)

From here you browse the marketplaces, see what's inside each plugin
**before** installing it, and manage the ones already installed. You
install from the panel or directly with `/plugin install
name@marketplace`, where the part after the `@` says which marketplace to
get the plugin from. `/reload-plugins` is for when you're developing a
plugin of your own: you edit the files and reload without restarting the
session.

## How it works underneath: settings and marketplaces

What does an installation actually write? Two keys in your
`settings.json`, worth knowing so you understand what's in your own
config:

```json
{
  "enabledPlugins": { "name@marketplace": true },
  "extraKnownMarketplaces": {
    "my-marketplace": { "source": { "source": "github", "repo": "user/repo" } }
  }
}
```

`enabledPlugins` is the list of what's active: the key is
`name@marketplace`, the `true`/`false` value turns the plugin on or off.
`extraKnownMarketplaces` registers third-party marketplaces: here's one
living on GitHub, specified with `"source": "github"` and the `repo` in
`user/repo` form.

And what is a marketplace? Little more than **a Git repo with an index**
of the plugins it contains. There's an official one,
`claude-plugins-official` (e.g. `/plugin install
skill-creator@claude-plugins-official`, mentioned in ch. 05), and you can
add third-party ones as above, including one of your own.

## When a plugin beats scattered config

- **For the team**: the company standard (format hook, review agent,
  deploy skill) becomes ONE versioned package that everyone installs and
  updates, instead of copied files that silently drift apart.
- **For you**: if you keep rebuilding the same setup on every machine or
  project, a personal plugin on a GitHub repo is your Claude Code
  "dotfiles".
- **From the community**: before building, look at what exists: browser
  automation, code intelligence, integrations; often there's already a
  plugin.

The same caution as with hooks (ch. 07): a plugin can bring hooks and MCP
servers, which means **code running with your credentials**. Install from
sources you trust, and read what's inside. That's exactly why the
`/plugin` panel shows it to you.

## A live example

This guide was written on a machine with a plugin installed from a
third-party GitHub marketplace: it brings a review persona ("lazy senior
dev") with its skills and a SessionStart hook that activates it in every
session. One `install`, and five skills plus a hook arrived together, and
with `/plugin uninstall` they'd leave just as much in one block. That's
the point of plugins.

---

**In short**: once your setup gets good, a plugin is how you share it
(with the team or with your future self). Next chapter: the frontend
workflow with a real browser.
