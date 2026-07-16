# Guida a Claude Code

Claude Code è un **agente di coding che vive nel terminale**: gli descrivi un
risultato ("il form di login non valida l'email: trova il perché e sistemalo,
con un test") e lui legge il codebase, modifica i file, esegue comandi e test,
e itera finché il task non è fatto, chiedendoti il permesso a ogni azione che
conta. Non è una chat da cui copiare codice, né un autocomplete: è un
collaboratore che lavora nel tuo repo, e questa guida insegna a farlo
lavorare **bene**.

Scritta e verificata a **luglio 2026 (Claude Code 2.1.210)**: ogni comando è
stato eseguito davvero, ogni schermata è reale e ogni fatto è controllato
sulla [documentazione ufficiale](https://code.claude.com/docs), che resta la
fonte da consultare quando questa guida invecchierà.

## Come leggerla

Una nota sulla numerazione: il numero nel nome dei capitoli è un
identificatore stabile, non l'ordine di lettura — la guida cresce per
sezioni e i capitoli nuovi si accodano. L'ordine giusto è questo indice.

**Base - partire bene (giorno 1):**

1. [Installazione e primo avvio](01-installazione.md) - dal `curl` al primo prompt
2. [Setup e configurazione](02-setup-e-config.md) - dove vive la config, i permessi, il deny sui segreti
3. [Uso quotidiano](03-uso-quotidiano.md) - il flusso di lavoro, l'undo, la gestione delle sessioni
4. [CLAUDE.md e rules](04-claude-md-e-rules.md) - le istruzioni permanenti del progetto

**Metodo - quello che fa la differenza:**

5. [Verifica](11-verifica.md) - *se leggi un solo capitolo, questo*
6. [Prompt engineering](12-prompt-engineering.md) - chiedere le cose in modo che riescano
7. [Ricerca e progettazione](17-ricerca-e-progettazione.md) - deep research, SPEC, Ultraplan e Claude Design: decidere bene prima di costruire
8. [Errori comuni](13-errori-comuni.md) - riconoscerli prima di farli, la checklist che chiude il Metodo

**Potenza - quando le basi girano:**

9. [Skill e slash command](05-skills-e-slash-commands.md) - procedure riusabili
10. [Agenti](06-agenti.md) - a chi delegare il lavoro rumoroso
11. [Hook](07-hooks.md) - regole che valgono sempre, non quasi sempre
12. [MCP](08-mcp.md) - collegare browser, Figma, GitHub
13. [Plugin](09-plugins.md) - il setup in un pacchetto
14. [Workflow frontend](10-workflow-frontend.md) - *per chi fa frontend: Claude con un browser vero*

**Riferimento:**

15. [Must-have e costi](14-must-have-e-costi.md) - il setup dei primi 30 minuti, i piani, le abitudini di risparmio
16. [Risparmiare token](15-risparmiare-token.md) - gli strumenti per finestre di lavoro più lunghe sul piano Pro
17. [Un setup reale](16-setup-a-tre-livelli.md) - globale, per cliente, per repo: dove si può arrivare

## Cosa ti serve per seguirla

Un terminale, un abbonamento Claude (Pro basta: cap. 01) e mezz'ora per la
parte Base. I capitoli 02 e 04 usano come esempio un piccolo progetto
React/TS i cui file (`CLAUDE.md` e `.claude/settings.json`) sono mostrati
per intero nei capitoli stessi: non serve scaricare nulla.

## Perché esiste

Questa guida è prima di tutto il mio quaderno di bordo: scritta per
ricordare, verificata per potermi fidare. Se fa comodo anche a te, ne sono
felice.
