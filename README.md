# Guida a Claude Code · A Claude Code Guide

🇮🇹 [Italiano](#italiano) · 🇬🇧 [English](#english)

**📖 Leggila online / Read it online: [me-xico.github.io/guida-claude-code](https://me-xico.github.io/guida-claude-code/)** · [English version](https://me-xico.github.io/guida-claude-code/en/)

---

## Italiano

Guida pratica a [Claude Code](https://code.claude.com/docs) per sviluppatori
che partono da zero: 15 capitoli dall'installazione al workflow frontend con
browser reale, passando per il metodo (verifica, prompt engineering, errori
comuni) e l'estensione dello strumento (skill, agenti, hook, MCP, plugin).

Scritta e verificata a **luglio 2026 (Claude Code 2.1.210)**: ogni comando è
stato eseguito davvero, le schermate sono catture reali della TUI e i fatti
sono stati controllati sulla documentazione ufficiale.

### Struttura del repo

| Percorso | Contenuto |
|---|---|
| [`guida-claude-code/`](guida-claude-code/) | i capitoli (it + en), gli screenshot SVG, il progetto demo |
| [`mkdocs.yml`](mkdocs.yml) | configurazione del sito (MkDocs Material, bilingue) |

### Costruire il sito in locale

```bash
uvx --from mkdocs-material --with mkdocs-static-i18n mkdocs serve
```

Le pagine inglesi sono i file `*.en.md` accanto agli originali italiani
(convenzione [mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n)).

### Da dove iniziare

Il [percorso di lettura](https://me-xico.github.io/guida-claude-code/) è sulla
home della guida. Se hai solo trenta secondi, leggi il capitolo
[Verifica](https://me-xico.github.io/guida-claude-code/11-verifica.html): se
ne leggi uno solo, è quello.

---

## English

A hands-on guide to [Claude Code](https://code.claude.com/docs) for
developers who have never touched it. Fifteen chapters take you from
installation to driving a real browser in your frontend workflow. Along the
way you get the part that actually matters — how to verify Claude's work,
how to ask for things so they get done, which mistakes everyone makes — and
the machinery to shape the tool around your own habits: skills, agents,
hooks, MCP, plugins.

Everything was written and checked in **July 2026 against Claude Code
2.1.210**. The commands were run for real, the screenshots come straight
from the TUI, and the facts were verified against the official docs.

### Repo layout

| Path | Contents |
|---|---|
| [`guida-claude-code/`](guida-claude-code/) | the chapters (it + en), SVG screenshots, the demo project |
| [`mkdocs.yml`](mkdocs.yml) | site configuration (MkDocs Material, bilingual) |

### Building the site locally

```bash
uvx --from mkdocs-material --with mkdocs-static-i18n mkdocs serve
```

English pages live in `*.en.md` files next to the Italian originals
(the [mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n) convention).

### Where to start

The [reading path](https://me-xico.github.io/guida-claude-code/en/) is on the
guide's home page. Got thirty seconds? Read the
[Verification](https://me-xico.github.io/guida-claude-code/en/11-verifica.html)
chapter — if you only read one, make it that one.
