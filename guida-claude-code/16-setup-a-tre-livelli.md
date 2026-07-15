# 16 - Un setup reale: globale, per cliente, per repo

> Questo capitolo descrive il setup quotidiano dell'autore (luglio 2026),
> sanitizzato: niente nomi di clienti né dettagli di progetti di lavoro.
> È il "dove si può arrivare" dopo i capitoli 1-15, non il punto di partenza.

## Il problema che risolve

Se lavori per più clienti, un solo `~/.claude/` non basta: la memoria di un
cliente non deve inquinare le sessioni di un altro, le integrazioni (il Jira
di A, il GitLab di B) non devono nemmeno *esistere* nel contesto sbagliato, e
le tue preferenze personali devono valere ovunque senza copiarle dieci volte.
La risposta è organizzare il setup su tre livelli, ognuno col suo mestiere:

| Livello | Dove vive | Cosa ci metti |
|---|---|---|
| Globale | `~/.claude/` (condiviso tra i profili) | chi sei tu: preferenze, sicurezza, strumenti trasversali |
| Cliente | un profilo isolato per cliente | il contesto: memoria, permessi, integrazioni, skill di dominio |
| Repo | `.claude/` nel progetto | il codice: convenzioni, hook, agenti e mappe di quel codebase |

La regola per decidere dove va una cosa: **al livello più alto in cui è vera
per tutto ciò che sta sotto**. Vale sempre → globale. Vale per un cliente →
profilo. Vale per un repo → repo.

## Livello globale: chi sei tu

Nel mio `~/.claude/` vivono le cose che non cambiano mai, chiunque sia il
cliente del giorno:

- **CLAUDE.md snello** (una quarantina di righe): lingua, stile dei commit,
  tooling Python via `uv`, la regola "delega agli agenti come default" e la
  regola "agenti just-in-time" (se un ruolo ad hoc ricorre due volte, si
  persiste come agente — è così che è nata metà della lista qui sotto).
- **La deny-list sui segreti** (cap. 02): ogni percorso che contiene
  credenziali è illeggibile per qualunque sessione, sempre, comprese le
  varianti via shell.
- **L'hook salva-token** (cap. 15): rtk riscrive i comandi in trasparenza,
  su qualunque progetto.
- **Una quindicina di agenti advisory** che coprono i miei cappelli
  professionali (Python, IaC, data engineering, architettura, frontend,
  DevOps…), tutti col pattern "consiglia e non edita" e con la delimitazione
  esplicita verso gli agenti affini nella description.
- **Le skill trasversali**: la revisione di prosa (un revisore per lingua),
  la coppia traduzione+sincronizzazione con cui mantengo bilingue questa
  guida, le catture di schermo, il nucleo Playwright per pilotare browser.

Un dettaglio d'infrastruttura che ripaga: i profili cliente (sotto) non
copiano questa base, la **linkano**. Regole, agenti e skill globali sono
symlink dentro ogni profilo: si aggiorna un file, vale ovunque, niente copie
che divergono.

## Livello cliente: un profilo per contesto

Il meccanismo sotto è quello del cap. 02: `CLAUDE_CONFIG_DIR` sposta l'intera
configurazione. Io lo governo con [cloak](https://github.com/synth1s/cloak)
(`npm install -g @synth1s/cloak`): profili nominati da creare e indossare in
un comando — `cloak create cliente-a`, `cloak switch cliente-a` — con la
lista del "guardaroba" sempre a portata di `cloak ls`. Il principio comunque
funziona anche a mano, senza installare nulla:

```bash
CLAUDE_CONFIG_DIR=~/.profili/cliente-a claude
```

Ogni profilo è un mondo: la sua storia delle sessioni, la sua **memoria
persistente** (le lezioni imparate su un cliente non affiorano nelle sessioni
di un altro), i suoi server MCP e i suoi permessi. Gli effetti pratici che
me lo fanno amare:

- **Isolamento delle integrazioni**: il profilo del cliente A ha
  l'autenticazione al suo Jira; negli altri profili quel Jira non esiste
  proprio. Un'intera classe di incidenti ("ho scritto sul ticket sbagliato")
  diventa impossibile per costruzione.
- **Skill di dominio**: le procedure che valgono solo per un cliente (il suo
  flusso di consegna, i suoi screenshot di prodotto) vivono nel suo profilo
  e non affollano il menu `/` degli altri.
- **Documentazione instradata**: una skill di profilo scrive le note di
  progetto in un vault organizzato per cliente, così la conoscenza si
  accumula nel posto giusto senza deciderlo ogni volta.

## Livello repo: il codice davanti a te

Qui vale tutto il cap. 02 e 04 (CLAUDE.md di progetto, `settings.json`
committato), più i pezzi che nascono quando un repo diventa "di casa":

- **Hook di progetto**: l'autoformat su PostToolUse (cap. 07) tarato sul
  formatter del repo — nel mio caso, sul repo principale, un `make format`
  che tiene la CI sempre verde.
- **Agenti di progetto** (committati in `.claude/agents/`): un *gate-runner*
  su modello piccolo che esegue il build gate in contesto isolato e riporta
  solo il verdetto, e un *guardiano* read-only che rivede ogni diff sulle
  invarianti architetturali del repo. Sono il cap. 06 applicato: rumore fuori
  dalla sessione, poteri minimi.
- **Skill di scaffolding**: quando il repo ha componenti con un'anatomia
  fissa (N file sempre uguali, test di conformità), una skill le genera
  giuste al primo colpo.

## graphify: la mappa del codebase

L'ultimo arrivato nel setup, in fase di adozione pilota:
[graphify](https://github.com/Graphify-Labs/graphify) trasforma un codebase
in un **knowledge graph interrogabile** — `graphify query "chi implementa
questa interfaccia?"` al posto di tre giri di grep e cinque file letti. Il
parsing è locale (tree-sitter), e per gli agenti è un moltiplicatore: la
ricognizione che riempiva mezzo contesto (cap. 03) diventa una query.

È complementare a rtk: rtk comprime l'output dei comandi che lanci, graphify
evita di lanciarli. Le regole che mi sono dato per usarlo, dopo averlo
studiato:

1. **Solo per-repo, mai globale**: si installa nel `.claude/` del progetto
   (project-mode); il grafo è un artifact locale da `.gitignore`.
2. **Versione pinnata**: è pre-1.0 con release frequenti — e occhio al nome
   del pacchetto, `uv tool install graphifyy==<versione>` con la doppia *y*
   (il nome "pulito" su PyPI appartiene a un altro progetto).
3. **Dove rende**: codebase grossi che non hai letto tu — quelli di un
   cliente nuovo, o i tuoi progetti *vibe-coded* (il codice l'ha scritto
   l'agente: il prodotto lo conosci, il codice no). Cross-repo solo se i
   repo sono davvero un sistema unico (una piattaforma dati spalmata su
   dieci repo sì; una cartella di progetti scollegati no: otterresti isole
   disconnesse cucite da inferenze).
4. **Cosa non è**: non sostituisce la memoria persistente né il vault di
   note — quelli custodiscono il sapere *esperienziale* ("questo strumento
   l'ho già provato, ecco cosa ho imparato"), graphify estrae solo relazioni
   *strutturali* dal codice. Se una lezione non è scritta, nessun grafo la
   inventa; se è scritta, la trovi senza grafo.

## In sintesi

Tre livelli, tre domande: *è vero ovunque?* → globale; *è vero per questo
cliente?* → profilo; *è vero per questo codice?* → repo. Il setup cresce
just-in-time come tutto il resto della guida — nessuno dei pezzi qui sopra è
nato in un pomeriggio di configurazione: ognuno è arrivato quando il bisogno
l'ha chiesto due volte.
