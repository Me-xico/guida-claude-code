# Guida a Claude Code

**📖 Leggila online: [me-xico.github.io/guida-claude-code](https://me-xico.github.io/guida-claude-code/)** · [English version](https://me-xico.github.io/guida-claude-code/en/)

Guida pratica a [Claude Code](https://code.claude.com/docs) per sviluppatori
che partono da zero: 15 capitoli dall'installazione al workflow frontend con
browser reale, passando per il metodo (verifica, prompt engineering, errori
comuni) e l'estensione dello strumento (skill, agenti, hook, MCP, plugin).

Scritta e verificata a **luglio 2026 (Claude Code 2.1.210)**: ogni comando è
stato eseguito davvero, ogni schermata è una cattura reale della TUI, ogni
fatto è controllato sulla documentazione ufficiale.

## Struttura del repo

| Percorso | Contenuto |
|---|---|
| [`guida-claude-code/`](guida-claude-code/) | i capitoli (it + en), gli screenshot SVG, il progetto demo |
| [`mkdocs.yml`](mkdocs.yml) | configurazione del sito (MkDocs Material, bilingue) |

## Costruire il sito in locale

```bash
uvx --from mkdocs-material --with mkdocs-static-i18n mkdocs serve
# oppure `mkdocs build` → sito statico in guida-claude-code-sito/
```

Le pagine inglesi sono i file `*.en.md` accanto agli originali italiani
(convenzione [mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n)).

## Da dove iniziare

Il [percorso di lettura](https://me-xico.github.io/guida-claude-code/) è sulla
home della guida. Se hai trenta secondi: capitolo
[Verifica](https://me-xico.github.io/guida-claude-code/11-verifica.html) — se
ne leggi uno solo, è quello.
