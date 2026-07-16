# 14 - Must-have e costi: il setup dei primi 30 minuti

> Verificato il 15 luglio 2026. I prezzi cambiano: controlla claude.com/pricing.

## Il setup minimo che rende subito

Il problema che questo capitolo risolve: la guida ha 17 capitoli e non li
applicherai tutti il primo giorno. Quali cinque cose fare *subito*, nell'ordine
giusto, perché ripagano dal primo pomeriggio? Eccole:

1. **`/init` nel tuo progetto** → CLAUDE.md di partenza, poi potalo
   (cap. 04). Committalo: è documentazione per il team, non solo per te.
   Senza CLAUDE.md ogni sessione riparte da zero e rispieghi le stesse
   convenzioni ogni giorno.
2. **Deny sui segreti** in `.claude/settings.json`: `Read(.env)`,
   `Read(.env.*)`, `Bash(cat *.env*)` (cap. 02). Due minuti, per sempre:
   il giorno che Claude, esplorando per un bug, sta per aprire il file
   con le API key, il deny lo ferma senza che tu debba essere lì.
3. **Hook Prettier** su PostToolUse (cap. 07). Ogni file toccato esce già
   formattato: niente diff sporchi di soli spazi, niente "riformatta tutto"
   a fine sessione. Un frontend senza questo hook sta lasciando soldi sul
   tavolo.
4. **`/statusline`**: mettici contesto usato e modello, sono le due cose
   che vuoi vedere *sempre*. Il contesto che si riempie spiega metà dei
   comportamenti strani (cap. 13), e vederlo salire in tempo reale ti fa
   fare `/clear` al momento giusto invece che tre task troppo tardi.
5. **Allow per i comandi fidati**: `npm run test`, `npm run lint`, `git
   status/diff/log` in allow-list, così smetti di approvare l'ovvio. Ogni
   prompt di conferma su un comando innocuo è attrito che ti fa sorvegliare
   invece di lavorare.

E quando arriva il momento, la sesta mossa si aggiunge da sola: estensione
Chrome o Playwright MCP (cap. 10).

E poi, la regola più importante: **lascia che il resto cresca
just-in-time**. Skill alla seconda volta che rispieghi una procedura,
agente alla prima ricerca che ti sporca il contesto, hook alla prima regola
che Claude "dimentica". Costruire l'arsenale in anticipo è il modo più
sicuro di costruire quello sbagliato: il bisogno reale è un criterio di
progettazione migliore di qualunque previsione.

## Modello giusto per il task giusto

Il dolore da evitare è doppio: pagare il modello grosso per rinominare una
variabile, o far litigare il modello piccolo con un bug subdolo per
un'ora. La mappa:

- Il default (Sonnet) va bene per quasi tutto il lavoro quotidiano.
- **`/model opusplan`** è il trucco più citato: il modello grosso (Opus)
  pianifica, quello medio esegue: paghi il ragionamento dove rende (le
  decisioni) e risparmi dove non serve (la manovalanza di battitura).
- Modello piccolo (Haiku) per il lavoro meccanico, soprattutto negli agenti
  (`model: haiku` nel frontmatter, cap. 06): un agente che formatta o cerca
  stringhe non ha bisogno di ragionare.
- `Alt+T` (extended thinking) per i problemi davvero difficili, non di
  default: è potenza extra a costo extra, e sul task medio non si vede.

Nota onesta: la doc ufficiale a volte spinge nella direzione opposta ("usa il
modello grosso con thinking: meno correzioni = più veloce in totale").
Entrambe le posizioni sono vere in casi diversi: task ben specificato →
modello medio; task ambiguo e costoso da correggere → modello grosso. Il
discrimine è quanto è probabile che il primo tentativo vada male: se è
probabile, il modello grosso che ci azzecca subito costa *meno* di tre giri
col medio.

*Il segnale*: se ti accorgi che stai correggendo spesso il modello medio su
un certo tipo di task, quel tipo di task merita il grosso. Se il grosso non
sta mai facendo niente di intelligente, stai pagando ragionamento a vuoto.

## Le 5 abitudini di risparmio (ufficiali)

1. `/clear` tra un task e l'altro
2. modello proporzionato al task
3. riferisci i file per path (`@src/…`) invece di incollarli
4. CLAUDE.md sotto ~200 righe
5. piano prima delle modifiche grandi (meno tentativi = meno token)

Noterai che sono le stesse regole dei capitoli 3, 4 e 13: **quello che fa
lavorare meglio Claude è quello che costa meno**. Non è un caso: il nemico
comune è il contesto sprecato. Il token che paghi e il token che confonde
il modello sono lo stesso token: ottimizzare la qualità e ottimizzare il
costo, qui, sono lo stesso gesto.

## Monitorare

Quattro strumenti, dal più al meno frequente:

- la statusline: tutto quanto sotto, sempre sott'occhio, senza chiedere
- `/context`: quanto contesto stai usando (da guardare quando le risposte
  peggiorano, di solito la spiegazione è lì)
- `/usage`: dove sei coi limiti del piano (Pro/Max)
- `/cost`: spesa della sessione (utenti API)

Ordini di grandezza: la tabella completa dei piani è nel cap. 01; il punto
pratico è che se Claude Code diventa lo strumento principale, il limite del
Pro (~200 messaggi ogni 5 ore) si sente in fretta: sembrano tanti finché
non passi una giornata intera in sessione.

## Per andare oltre (cenni)

Tre direzioni per quando il flusso base ti sta stretto:

- **`claude -p "prompt"`**: modalità headless, Claude Code negli script e
  in CI (`--output-format json` per output strutturato). Il momento in cui
  serve: quando una cosa che fai in sessione vuoi che giri da sola.
- **GitHub Actions**: `anthropics/claude-code-action`, `@claude` nei
  commenti delle PR per review e fix automatici; rispetta il CLAUDE.md del
  repo, quindi le convenzioni che hai scritto valgono anche lì.
- **Git worktrees**: più sessioni in parallelo su branch diversi
  (`claude --worktree`); il collo di bottiglia diventa la tua capacità di
  fare review, non Claude. Da provare solo quando il flusso a sessione
  singola è già solido: parallelizzare il caos produce solo caos parallelo.

---

**In sintesi**: cinque mosse il primo giorno (init, deny, hook format,
statusline, allow-list), il resto quando serve davvero. E l'abitudine che
batte tutte: contesto pulito, evidenze sempre. Se dopo queste abitudini il
budget stringe ancora, il [cap. 15](15-risparmiare-token.md) presenta gli
strumenti che comprimono i token alla fonte, con numeri misurati, non
promessi.
