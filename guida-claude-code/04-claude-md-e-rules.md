# 04 - CLAUDE.md e rules: le istruzioni permanenti

> Verificato il 15 luglio 2026 sulla doc ufficiale (v2.1.210).
> Esempio vivo: [`demo/CLAUDE.md`](demo/CLAUDE.md).

## Cos'è davvero

**Cos'è**: il CLAUDE.md è quello che Claude sa del tuo progetto *prima* che
tu scriva il primo prompt. L'analogia giusta è il documento di onboarding di
un collega nuovo, con la differenza che Claude è un collega nuovo *a ogni
sessione*: senza questo file riparte ogni volta da zero, riscopre i comandi,
ridà nomi sbagliati alle cose, rifà gli stessi errori.

**Dove sta**: è un normale file Markdown, `CLAUDE.md`, nella root del
progetto. Lo crei tu, oppure lo genera `/init`, che analizza il codebase e
ne produce uno di partenza (buono, ma da potare subito: vedi sotto).

**Come funziona**: all'avvio della sessione Claude Code lo cerca, lo carica
nel contesto e ce lo tiene per tutta la sessione: fa parte della "memoria"
che hai visto nella griglia di `/context` (cap. 03). Nessuna magia: è testo
che precede ogni tuo prompt. Da qui discendono le due regole del capitolo:
ogni riga costa contesto, e ogni riga viene letta sempre.

È il singolo file col miglior rapporto sforzo/resa di tutto il setup.

## Cosa metterci (e cosa no)

Il criterio: metti solo ciò che Claude **sbaglierebbe senza**:

- i comandi del progetto (`npm run test`, `npm run lint`) e quando lanciarli
- convenzioni non ovvie: "CSS modules, niente styled-components", "un
  componente per file", "test accanto al componente"
- i vincoli: "TypeScript strict, niente `any`"
- le trappole note: "il mock del router va importato prima del componente,
  altrimenti i test si rompono in modo criptico"

NON metterci ciò che Claude capisce da solo guardando il codice: l'albero
delle directory, l'elenco delle dipendenze, descrizioni generiche ("è
un'app React"). È zavorra che consuma contesto e diluisce le regole vere.

**Come si scrive**: guarda [`demo/CLAUDE.md`](demo/CLAUDE.md), il file reale
del progetto demo di questa guida: una riga di inquadramento, i comandi con
il *quando* usarli, le convenzioni. Un assaggio:

```markdown
# demo-app

SPA React + TypeScript (Vite). Componenti in `src/components/`, un file per
componente, stile con CSS modules (niente styled-components).

## Comandi

- `npm run test` — test (Vitest); lanciali prima di dichiarare finito un task

## Convenzioni

- TypeScript strict: niente `any`, preferisci type inference dove possibile.
- I test stanno accanto al componente: `Button.tsx` → `Button.test.tsx`.
```

Nota lo stile: frasi imperative e specifiche, niente prosa. Ogni riga è
un'istruzione che cambia un comportamento.

**Il test della riga**: per ogni riga chiediti "se la tolgo, Claude
sbaglierebbe qualcosa?". Se no, tagliala. Obiettivo: **sotto le ~200 righe**.
Il motivo non è estetico: i modelli seguono in modo affidabile un numero
limitato di istruzioni, e in un CLAUDE.md gonfio le regole importanti
annegano tra quelle inutili. Il file smette di funzionare proprio dove
serviva. Da v2.1.206, `/doctor` propone lui stesso i tagli.

## Il pattern che rende il file vivo: il log degli errori

Il CLAUDE.md migliore non si scrive in un pomeriggio: **cresce ogni volta che
Claude sbaglia**. Il ciclo è questo:

1. Claude sbaglia qualcosa (usa il comando deprecato, sbaglia il path degli
   asset).
2. Lo correggi in chat, ma la correzione vive solo in *questa* sessione.
3. La travasi nel CLAUDE.md come riga permanente: "usa X, non Y (deprecato)".
4. Da domani, nessuna sessione rifà quell'errore.

A fine sessione chiediti (o chiedi direttamente a Claude): "cosa hai imparato
oggi che domani non dovrai rispiegare?". Dopo un mese hai un file che vale
oro e che nessun `/init` potrebbe generare, perché codifica gli errori *del
tuo* progetto.

Per editarlo al volo senza uscire dalla sessione c'è `/memory`: elenca tutti
i file di istruzioni caricati (CLAUDE.md ai vari livelli, rules) e te li apre
nell'editor.

## I livelli (ripasso dal cap. 02, con le regole d'uso)

Non esiste un solo CLAUDE.md: all'avvio Claude Code li carica in ordine, dal
più generale al più specifico, e li somma. Ogni livello ha il suo mestiere:

| File | Per cosa |
|---|---|
| `~/.claude/CLAUDE.md` | le TUE preferenze, su tutti i progetti ("rispondi in italiano", "usa sempre pnpm") |
| `./CLAUDE.md` | le convenzioni del PROGETTO, committato: è lo standard del team |
| `./CLAUDE.local.md` | note tue su questo progetto, gitignorato ("il mio dev server gira sulla 3001") |
| `CLAUDE.md` di sottocartella | monorepo: NON viene caricato all'avvio, ma solo quando Claude lavora su file di quella cartella |

La riga di separazione pratica: se un collega clonando il repo trarrebbe
beneficio dalla regola → `./CLAUDE.md` (committato); se è una cosa tua o
della tua macchina → `CLAUDE.local.md` o il file utente.

**Gli import**: `@docs/convenzioni-css.md` a inizio riga include quel file
nel CLAUDE.md, come un `import` (ricorsivo, max 4 livelli). Serve a
modularizzare: il file principale resta corto e le sezioni corpose vivono in
file dedicati. Attenzione al caso speciale: se un import punta **fuori** dal
progetto, Claude Code si ferma e chiede conferma, perché un CLAUDE.md
malevolo in un repo di terzi potrebbe usare gli import per iniettarti
istruzioni. Il dialog è questo, e su repo che non conosci la risposta è no:

![Conferma per gli import esterni del CLAUDE.md](assets/04-import-dialog.svg)

## Rules: istruzioni con mira

**Cos'è**: una rule è un file di istruzioni con un *campo d'azione*
delimitato da glob sui path. Risolve un problema classico del CLAUDE.md: "le
regole sui test valgono solo per i file di test, perché devono stare sempre
nel contesto, anche quando lavoro sul CSS?"

**Dove stanno**: `.claude/rules/*.md` nel progetto (committabili, come il
CLAUDE.md) oppure `~/.claude/rules/` a livello utente. Un file per regola o
per area.

**Come si scrive**: Markdown con un frontmatter YAML che dichiara i path a
cui la regola si applica. Esempio completo:

```markdown
---
paths:
  - "src/**/*.test.ts"
---
# Regole per i test
- Usa Testing Library, mai enzyme.
- Ogni test ha un solo assert concettuale.
```

Il campo `paths:` accetta una lista di glob (`**` = qualunque sottocartella).
Il corpo è scritto come un CLAUDE.md: istruzioni brevi e imperative.

**Come funziona**: a differenza del CLAUDE.md, la rule NON è sempre nel
contesto. Entra in gioco **solo quando Claude tocca file che matchano i
glob**: finché lavori su `src/styles/`, la regola sui test non esiste; appena
apre `Button.test.ts`, si attiva. Contesto pulito e regole più seguite
(ricordi il limite sul numero di istruzioni?). È il posto giusto per le
convenzioni per-area nei progetti grandi.

## Un limite onesto

CLAUDE.md e rules sono *advisory*: Claude li segue quasi sempre, ma non è un
enforcement, sono istruzioni a un modello, non vincoli di sistema. Per le
cose che devono succedere **sempre e comunque** (formattare dopo ogni edit,
bloccare un comando) lo strumento giusto sono gli hook (cap. 07), che sono
deterministici. Regola pratica: preferenze e conoscenza → CLAUDE.md;
garanzie → hook.

---

**In sintesi**: parti da `/init`, pota col test della riga, tieni sotto 200
righe, e fai crescere il file a ogni errore di Claude. Con questo la Base è
completa: la prossima tappa del percorso è il Metodo, a partire dalla
verifica (cap. 11) — il capitolo più importante della guida. Skill e agenti
(cap. 05-06) arrivano subito dopo, e renderanno il doppio col metodo in
tasca.
