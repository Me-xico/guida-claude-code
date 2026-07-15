# Guida a Claude Code

Guida pratica per sviluppatori che partono da zero con Claude Code.
Scritta e verificata a **luglio 2026 (Claude Code 2.1.210)**: ogni comando è
stato eseguito davvero e ogni fatto controllato sulla
[doc ufficiale](https://code.claude.com/docs) — che resta la fonte da
consultare quando questa guida invecchierà.

## Percorso di lettura

**Base (giorno 1):**

1. [Installazione e primo avvio](01-installazione.md)
2. [Setup e configurazione](02-setup-e-config.md)
3. [Uso quotidiano](03-uso-quotidiano.md)
4. [CLAUDE.md e rules](04-claude-md-e-rules.md)

**Metodo (quello che fa la differenza):**

5. [Verifica: il principio più importante](11-verifica.md) ← *se leggi un solo capitolo, questo*
6. [Prompt engineering](12-prompt-engineering.md)
7. [Errori comuni](13-errori-comuni.md)

**Potenza (quando le basi girano):**

8. [Skill e slash command](05-skills-e-slash-commands.md)
9. [Agenti](06-agenti.md)
10. [Hook](07-hooks.md)
11. [MCP](08-mcp.md)
12. [Plugin](09-plugins.md)
13. [Workflow frontend con browser](10-workflow-frontend.md) ← *per chi fa frontend*

**Riferimento:**

14. [Must-have e costi](14-must-have-e-costi.md) — il setup dei primi 30 minuti
15. [Risparmiare token: rtk, ponytail e caveman](15-risparmiare-token.md) — finestre di lavoro più lunghe sul piano Pro

## Materiale di supporto

- [`demo/`](demo/) — progetto demo con `CLAUDE.md` e `.claude/settings.json`
  reali, citati nei capitoli 02 e 04
- `slides.html` — le slide della guida, navigabili nel browser (offline)

## Il filo conduttore

Se dovessi comprimere tutto in tre regole:

1. **Il contesto è la risorsa scarsa**: `/clear` tra i task, delega le cose
   rumorose agli agenti, tieni il CLAUDE.md snello.
2. **Dai a Claude un modo di verificarsi**: test, build, screenshot — e
   chiedi evidenze, non asserzioni.
3. **Advisory vs deterministico**: le preferenze in CLAUDE.md, le garanzie
   negli hook.

Tutto il resto è dettaglio di queste tre.
