# 15 — Risparmiare token: rtk, ponytail e caveman

> Verificato il 15 luglio 2026: versioni, comandi di installazione e numeri
> controllati su GitHub e (per rtk) misurati su un uso reale di mesi.

## Perché questo capitolo esiste

Se sei su un piano Pro, il tuo budget è una finestra: ~200 messaggi ogni
5 ore (cap. 01). Ma il messaggio non è l'unità che conta — lo sono i
**token**, e la maggior parte non li scrivi tu: sono gli *output dei
comandi* che Claude esegue (un `git log`, un `ls -la`, l'output dei test) e
il *codice e la prosa* che Claude genera. Le 5 abitudini del cap. 14 riducono
gli sprechi di comportamento; gli strumenti di questo capitolo riducono gli
sprechi **alla fonte, automaticamente**. Tradotto: finestre di lavoro più
lunghe con lo stesso piano.

Tutti e tre sono progetti di terze parti: vale il solito avviso dei cap. 07
e 09 — hook e plugin girano coi tuoi permessi, guarda cosa installi.

## rtk — comprimere gli output dei comandi

**Cos'è**: un proxy CLI in Rust ([rtk-ai/rtk](https://github.com/rtk-ai/rtk),
Apache 2.0) che si mette tra i comandi e Claude: esegue il comando vero e
passa al contesto una versione **filtrata e compressa** dell'output. Un
`git status` verboso diventa tre righe dense; un `ls -la` perde i permessi
che a Claude non servono. Dichiarato: 60–90% di risparmio sugli output.

**Come si installa**:

```bash
brew install rtk        # oppure: curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh
rtk init -g             # installa l'hook per Claude Code + RTK.md, poi riavvia Claude
```

**Come funziona**: `rtk init -g` aggiunge un hook `PreToolUse` (cap. 07) che
riscrive in trasparenza i comandi Bash di Claude in `rtk <comando>`: Claude
chiede `git diff`, il sistema esegue `rtk git diff`, e nel contesto entra
l'output compresso. Tu non fai niente; Claude nemmeno se ne accorge.

**Quanto rende davvero**: dal contatore (`rtk gain`) di un'installazione
reale usata per mesi di lavoro quotidiano:

```console
$ rtk gain
Total commands:    6812
Tokens saved:      2.1M (54.3%)
```

Metà dei token degli output di comando, spariti. Per un piano Pro è la
differenza tra una finestra che finisce a metà pomeriggio e una che arriva
a sera. È lo strumento col miglior rapporto beneficio/rischio del capitolo:
non cambia *cosa* fa Claude, solo quanto pesa quello che legge.

## ponytail — meno codice generato

**Cos'è**: un plugin ([DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail))
che installa una "persona" da senior dev pigro: soluzione più corta che
funziona, stdlib prima delle dipendenze, niente astrazioni speculative,
diff minimo. Il risparmio token è la conseguenza del design: **meno codice
generato = meno token di output** (e spesso meno bug da rivedere).

**Come si installa** (è l'esempio vivo del cap. 09):

```bash
claude plugin marketplace add DietrichGebert/ponytail
claude plugin install ponytail@ponytail
```

**Come funziona**: un hook `SessionStart` inietta le regole a ogni sessione;
tre intensità (`/ponytail lite|full|ultra`); le scorciatoie deliberate
vengono marcate con commenti `ponytail:` così restano tracciate.

**Quanto rende** (benchmark del progetto stesso, 3 modelli × 10 run,
mediane vs baseline senza plugin): righe di codice **46%**, token **78%**,
costo **80%**, tempo **73%** — a safety invariata. Cioè: -22% di token e
metà del codice da leggere. Avvertenza onesta: cambia lo *stile* del codice
verso il minimalismo; provalo su un progetto tuo prima di adottarlo — o ti
piace, o ti innervosisce.

## caveman — risposte terse (con un asterisco)

**Cos'è**: un plugin ([JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman))
che rende terse le **risposte in prosa** dell'agente ("why use many token
when few token do trick"), lasciando intatti byte-per-byte codice, comandi
ed errori.

**Come si installa**:

```bash
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

**L'asterisco**: il progetto dichiara ~65% di risparmio sui token di
*output in prosa*; ma il benchmark indipendente di ponytail (che lo usa come
termine di paragone) lo misura a **+7% di token totali** sui task di
coding — perché nei task veri la prosa è una fetta piccola, e lo stile
"caveman" a volte allunga il giro. Verdetto pratico: prendilo per la
*leggibilità* (risposte che si scorrono in due secondi), non per il
risparmio. Sul budget contano rtk e ponytail.

## L'ordine giusto per un piano Pro

1. **rtk** — subito: risparmio misurato ~50%+ sugli output, zero cambi di
   comportamento, si disinstalla senza lasciare traccia.
2. **ponytail** — quando hai fatto pace con lo stile minimalista: -22% di
   token e molto meno codice da rivedere.
3. **caveman** — questione di gusto, non di budget.

E ricorda che la leva più grande resta gratis: le 5 abitudini del cap. 14
(`/clear`, modello proporzionato, file per path, CLAUDE.md snello, piano
prima delle modifiche grandi). Prima il metodo, poi gli attrezzi.

---

**In sintesi**: il token che non entra nel contesto è l'unico che non paghi
e non confonde il modello. rtk comprime quello che Claude legge, ponytail
riduce quello che Claude scrive, caveman accorcia quello che Claude ti dice
— e solo i primi due spostano davvero il budget.
