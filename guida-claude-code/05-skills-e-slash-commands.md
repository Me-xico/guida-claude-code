# 05 — Skill e slash command

> Verificato il 15 luglio 2026 sulla doc ufficiale (v2.1.210).

## Cos'è una skill, a che serve

Una skill è una **procedura confezionata**: una directory con dentro un file
`SKILL.md` che spiega a Claude, passo passo, come si fa una cosa specifica —
il check pre-release, il fix di una issue GitHub, qualunque routine che oggi
rispiegate a voce.

L'analogia che regge: una skill è una **ricetta in un ricettario**. Claude
tiene sempre sott'occhio l'indice (nome e una riga di descrizione per ogni
ricetta), ma apre la pagina solo quando deve cucinare quel piatto. È il
caricamento *lazy*: finché non la usi, una skill costa zero contesto.

Il problema che risolve lo riconosci al volo: stai incollando in chat le
stesse istruzioni per la terza volta, oppure il tuo CLAUDE.md (cap. 04) si
sta gonfiando di procedure lunghe che servono una volta su dieci. La regola
di ripartizione ufficiale:

- **fatti → CLAUDE.md**: sempre in contesto ("usiamo CSS modules", "i test
  stanno accanto al componente");
- **procedure → skill**: caricate on-demand, zero costo quando non le usi.

## Dove sta e chi la crea

Una skill è una directory che contiene almeno un `SKILL.md`:

| Scope | Path | Quando |
|---|---|---|
| Personale | `~/.claude/skills/<nome>/SKILL.md` | tue procedure, valide ovunque |
| Progetto | `.claude/skills/<nome>/SKILL.md` | committata: tutto il team la usa |
| Plugin | dentro il plugin (cap. 09) | distribuita con un plugin |
| Monorepo | `apps/web/.claude/skills/…` | si attiva lavorando lì, o con `/apps/web:deploy` |

La crei tu: a mano (è solo markdown) oppure — più comodo — chiedendo a Claude
di scrivertela (ci torniamo in fondo al capitolo). Non serve riavviare nulla:
**le modifiche sono live** — salvi il file e la skill è già aggiornata nella
sessione in corso.

Una skill non banale può avere anche materiale di supporto:

```
.claude/skills/release-check/
├── SKILL.md          # frontmatter + procedura (tienilo sotto ~500 righe)
├── references/       # doc di dettaglio, caricata solo se la skill la richiede
└── assets/           # script deterministici, template
```

`references/` e `assets/` sono opzionali: servono quando la procedura ha
dettagli lunghi che non vuoi dentro `SKILL.md`, o script di appoggio.

## Come si scrive

Un `SKILL.md` completo e minimale — frontmatter YAML tra i `---`, poi il
corpo in markdown:

```markdown
---
name: release-check
description: Verifica pre-release di una SPA: build pulita, test verdi,
  bundle size sotto soglia. Usala quando l'utente dice "siamo pronti al
  rilascio?", "release check", "posso deployare?".
---

Esegui in ordine, fermandoti al primo problema:

1. Lancia la build di produzione: deve chiudersi pulita.
2. Lancia la suite di test: tutti verdi.
3. Controlla la dimensione del bundle rispetto alla soglia.
4. Riporta il verdetto (pronto / non pronto) con i dettagli.
```

| Parte | A cosa serve |
|---|---|
| `name` | identifica la skill: è il nome della directory e diventa il comando `/release-check` |
| `description` | **il trigger**: l'unica cosa che Claude vede per decidere se attivarla |
| corpo | la ricetta: le istruzioni che Claude segue quando la skill si attiva |

Sulla description vale la pena fermarsi, perché è il punto dove le skill
falliscono. Claude non legge il corpo per decidere: legge *solo* la
description. Quindi scrivici dentro tre cose: **cosa fa** la skill, **le
frasi che devono attivarla** (letteralmente: "usala quando l'utente dice…"),
e — per le skill delicate — **quando NON attivarla**. Una description vaga
produce una skill che non parte mai, o che parte a sproposito.

## Come funziona, passo passo

1. **All'avvio della sessione** Claude carica l'indice delle skill
   disponibili: per ognuna solo `name` e `description`. I corpi restano su
   disco: costo in contesto quasi nullo.
2. **A ogni tua richiesta** Claude confronta quello che chiedi con le
   description. "Posso deployare?" matcha quella di `release-check` → la
   skill si attiva. In alternativa la attivi tu, digitando `/release-check`.
3. **All'attivazione** Claude legge l'intero `SKILL.md` e ne segue il corpo
   come se glielo avessi appena incollato in chat.
4. **Se il corpo rimanda a `references/`**, quei file vengono letti solo a
   quel punto: secondo livello di lazy loading.

Le skill compaiono anche nel menu `/` accanto ai comandi built-in — è lo
stesso menu che hai visto nel cap. 03 (`assets/03-slash-menu.svg`): digiti
`/` e le trovi lì, con la loro description come sottotitolo.

Due frontmatter di controllo regolano *chi* può invocarla:

- `disable-model-invocation: true` — solo tu puoi lanciarla, Claude non la
  attiva da solo. Giusto per azioni con effetti (deploy, commit).
- `user-invocable: false` — l'inverso: solo Claude, sparisce dal menu `/`.

## Argomenti e superpoteri del corpo

Una skill può ricevere argomenti ed eseguire comandi prima ancora che Claude
la legga. Esempio completo:

```markdown
---
name: fix-issue
description: Risolve una issue GitHub per numero
arguments: issue priority
argument-hint: [numero-issue] [priorità]
disable-model-invocation: true
---

Risolvi la issue #$issue con priorità $priority:

## Stato attuale
!`git status --short`

1. Leggi la issue, implementa il fix, aggiungi i test.
2. Commit: "fix: #$issue"
```

Invocazione: `/fix-issue 123 high`. Cosa succede, riga per riga:

| Elemento | Meccanica |
|---|---|
| `arguments: issue priority` | dichiara argomenti nominati: `123` finisce in `$issue`, `high` in `$priority` |
| `argument-hint` | il suggerimento che vedi nel menu `/` mentre digiti |
| `$issue`, `$priority` | sostituiti nel corpo prima che Claude lo legga (in alternativa: `$ARGUMENTS` per tutto, `$0`/`$1` per posizione) |
| `` !`git status --short` `` | **iniezione dinamica**: il comando viene eseguito *prima* che Claude legga la skill e il suo output incollato lì — la skill parte già col contesto giusto (diff, status, log) senza sprecare turni |

Altri frontmatter utili quando servono:

- `allowed-tools: Bash(git add *) …` — pre-approva quei tool per la durata
  della skill (niente richieste di permesso a metà procedura);
- `model:` / `effort:` — la fanno girare su un modello o sforzo diverso;
- `context: fork` — la esegue in un subagent, con contesto separato (cap. 06).

## E i vecchi slash command?

`.claude/commands/nome.md` funziona ancora: stesso frontmatter, stessa
invocazione `/nome`. Ma è il formato legacy — un file singolo, senza
`references/` né `assets/`. Se esistono entrambi con lo stesso nome, vince la
skill. Per cose nuove usa le skill; i command esistenti non vanno riscritti,
migrali solo quando ti serve la struttura in più.

## Skill di serie e come crearne di buone

Claude Code ne porta alcune built-in: `/code-review`, `/verify`, `/run`,
`/debug`, `/loop`, `/batch`. Aprirle e leggerle è il modo più rapido per
imparare lo stile.

Per crearne una tua, il flusso più pratico è: descrivi a Claude la procedura
a voce ("quando faccio il release check, prima lancio la build, poi…") e
chiedigli di scriverla come skill. Poi **affina la description** finché non
scatta sulle frasi giuste — è un piccolo lavoro iterativo. Esiste anche il
plugin ufficiale `skill-creator`
(`/plugin install skill-creator@claude-plugins-official`) che aggiunge test
case e A/B delle description.

Best practice ufficiali: SKILL.md corto e **imperativo** ("fai X", non "si
potrebbe fare X"), dettagli in `references/` caricati on-demand, script negli
`assets/` riferiti con `${CLAUDE_SKILL_DIR}` così funzionano da qualunque
directory.

---

**In sintesi**: ogni volta che ti accorgi di rispiegare una procedura, è una
skill che vuole nascere. Description = trigger, corpo = ricetta, lazy loading
= contesto pulito. Prossimo capitolo: gli agenti, ovvero a chi delegare.
