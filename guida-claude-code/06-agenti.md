# 06 — Agenti (subagent): a chi delegare

> Verificato il 15 luglio 2026 sulla doc ufficiale (v2.1.210).

## Cos'è un subagent, a che serve

Un subagent è un **collaboratore usa-e-getta**: un'istanza di Claude che
parte con un suo ruolo, i suoi tool e — soprattutto — un suo **contesto
separato e pulito**. L'analogia: passi un task ben scritto a un collega, lui
lavora alla *sua* scrivania, e ti riporta solo la sintesi. Le carte sparse
restano da lui.

Il motivo profondo per cui esistono è il **contesto**: una ricerca nel
codebase o una suite di test verbosa possono bruciare metà della finestra di
contesto della tua sessione con output che non ti serve conservare. Il
subagent fa il lavoro sporco nel suo contesto e riporta indietro solo la
conclusione. Tu tieni la sintesi, non i log.

Secondo motivo: **restringere i poteri**. Un reviewer con soli tool di
lettura non può "aggiustare" le cose di sua iniziativa mentre giudica.

## Dove sta e chi lo crea

Un agente è un singolo file markdown:

| Scope | Path |
|---|---|
| Personale | `~/.claude/agents/<nome>.md` |
| Progetto | `.claude/agents/<nome>.md` (committato: tutto il team lo usa) |

Lo crei tu, e non c'è nessun wizard: o editi il file a mano, o chiedi a
Claude di fartelo ("crea un agente code-reviewer per questo progetto").
Le modifiche sono live: salvi il file e l'agente è già aggiornato in sessione.

## Come si scrive

Un esempio realistico e completo per un progetto frontend,
`.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Reviews code for quality, a11y and security. Use proactively
  after writing or modifying components.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior frontend reviewer. When invoked:
1. Look at the recent diff.
2. Check: correctness, accessibility (labels, focus, contrast),
   render performance (unnecessary re-renders), security (XSS, injections).
3. Return a checklist of findings (critical / warning / suggestion)
   with file:line references. You review, you do NOT edit.
```

| Campo | A cosa serve |
|---|---|
| `name` | il nome con cui l'agente viene invocato e mostrato |
| `description` | **il trigger**, come per le skill: il main agent la legge per decidere quando delegare. "Use proactively" incoraggia la delega automatica; scrivi anche cosa l'agente NON fa |
| `tools` | allowlist dei tool: dai solo il necessario (`Read, Grep, Glob, Bash` per un read-only) |
| `model` | `haiku` per lavoro meccanico (lint, esecuzione test), `sonnet` per review; ometti per ereditare dal main |
| corpo | il **system prompt** dell'agente: chi è, cosa fa quando viene invocato, in che formato risponde |

Nota il corpo dell'esempio: definisce il ruolo, i passi, il formato
dell'output e il confine ("you do NOT edit"). È il pattern da copiare.

Campi avanzati quando servono: `maxTurns` (tetto ai giri), `memory` (l'agente
accumula conoscenza tra sessioni), `isolation: worktree` (checkout git
separato: più agenti che *scrivono* in parallelo senza pestarsi),
`permissionMode`, `effort`.

## Come funziona, passo passo

1. Il main agent conosce gli agenti disponibili tramite le loro
   **description** (esattamente come per le skill: la description è il
   trigger della delega).
2. Quando decide di delegare — da solo, o perché glielo chiedi — scrive un
   **prompt di delega**: il task da svolgere.
3. Il subagent parte con un contesto **nuovo**: il suo system prompt (il
   corpo del file), il prompt di delega, CLAUDE.md e la memoria. Non vede la
   tua conversazione.
4. Lavora con i soli tool della sua allowlist; tutto l'output rumoroso
   (grep, log di test, file letti) resta nel *suo* contesto.
5. Alla fine restituisce il messaggio conclusivo — la sintesi — che è
   l'unica cosa che entra nella tua sessione.

Per invocarlo esplicitamente: nominalo nel prompt ("usa il code-reviewer sui
componenti nuovi") o garantisci la delega con la @-mention:
`@"code-reviewer (agent)"`.

### Foreground e background

Dal 2.1.198 i subagent girano in **background di default**: la tua sessione
continua mentre loro lavorano, e vieni notificato al termine. `/tasks` (o
`Ctrl+T`) mostra cosa sta girando; le richieste di permesso dei background
emergono comunque da te, non vengono auto-approvate.

## Cosa vede il subagent (e cosa no)

| Riceve | Non riceve |
|---|---|
| il prompt di delega | la storia della tua conversazione |
| il suo system prompt | i file che il main ha già letto |
| CLAUDE.md e memoria | le skill invocate dal main |

Conseguenza pratica, ed è l'errore classico: **il prompt di delega deve
essere autosufficiente** — path esatti, vincoli, formato dell'output atteso.
Dare per scontato che l'agente "sappia di cosa stavamo parlando" non
funziona: non lo sa, e lavorerà su ipotesi sue.

## Quelli di serie

- **Explore** — ricerche read-only nel codebase; usalo liberamente: è il modo
  standard di "capire dove sta X" senza sporcare il contesto.
- **Plan** — la ricognizione che alimenta il plan mode (cap. 03).
- **general-purpose** — tuttofare multi-step con tutti i tool.

## Quando NON usarli

- Modifica piccola e mirata: il giro di delega costa più del lavoro.
- Task che richiede botta e risposta con te: il subagent non ti vede.
- Fasi che condividono molto contesto: rispiegarlo a ogni agente costa più
  che tenerlo in sessione.

Esiste anche una modalità sperimentale a **team di agenti** che si parlano
tra loro (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`): sappi che c'è, ma per
iniziare i subagent bastano e avanzano.

---

**In sintesi**: delega agli agenti le cose rumorose (ricerche, test, review)
e resta proprietario del contesto. Description chiara, tool minimi, prompt di
delega autosufficiente. Prossimo capitolo: gli hook, dove le regole smettono
di essere consigli.
