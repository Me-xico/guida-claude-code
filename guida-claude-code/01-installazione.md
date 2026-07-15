# 01 — Installazione e primo avvio

> Verificato il 15 luglio 2026 sulla doc ufficiale, con Claude Code **2.1.210**.
> Se qualche comando non corrisponde, controlla i [docs di setup](https://code.claude.com/docs/en/setup).

In questo capitolo installiamo Claude Code, facciamo il login e diamo
un'occhiata a cosa succede al primo avvio. Alla fine avrai un `claude`
funzionante nel terminale e saprai dove mettere le mani se qualcosa non parte.

## Installazione

**Cos'è.** L'installer ufficiale è un semplice script che scarica un binario
nativo e lo mette nel tuo `PATH`. È il metodo raccomandato per un motivo
preciso: il binario installato così **si aggiorna da solo in background** —
come fa un browser moderno — quindi dopo l'installazione non dovrai più
pensarci.

**Come si installa.** Un comando, a seconda del sistema:

```bash
# macOS / Linux / WSL
curl -fsSL https://claude.ai/install.sh | bash
```

```powershell
# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex
```

**Dove finisce.** Il binario viene messo in `~/.local/bin/claude`. È un
eseguibile autonomo: **non serve Node.js**, né nessun altro runtime. Se hai
già visto in giro il pacchetto npm (`npm install -g @anthropic-ai/claude-code`)
sappi che è la via legacy: funziona ancora, ma anche lui non fa altro che
scaricare lo stesso binario nativo — non c'è motivo di preferirlo.

Se invece vuoi che sia il tuo package manager a governare gli aggiornamenti
(niente auto-update), esistono le alternative classiche: Homebrew
(`brew install --cask claude-code`), WinGet, e repository apt/dnf/apk firmati.

**Verifica.** Appena finito, controlla che il binario risponda:

```console
$ claude --version
2.1.210 (Claude Code)
```

Se il comando non viene trovato, quasi sempre il problema è che
`~/.local/bin` non è nel `PATH` della tua shell.

**Requisiti e note per piattaforma.** Serve macOS 13+ / Windows 10 1809+ /
Ubuntu 20.04+ / Debian 10+ e 4 GB di RAM — requisiti che qualunque macchina
da sviluppo soddisfa. Due note valgono la pena:

- **Windows nativo**: Git for Windows è opzionale, ma installa anche una
  bash — e questo abilita il tool Bash di Claude Code. Senza, Claude esegue
  i comandi via PowerShell. Funziona, ma gran parte degli esempi che trovi
  in giro (e in questa guida) assumono una shell POSIX.
- **WSL**: installa Claude Code *dentro* la distribuzione Linux (quindi con
  lo script `curl` da un terminale WSL), non da PowerShell. Deve vivere
  nello stesso mondo dei file su cui lavorerai.

## Login e piani

**Come funziona.** Alla prima esecuzione di `claude`, prima ancora di poter
scrivere qualcosa, parte il flusso di autenticazione: Claude Code apre il
browser, tu ti autentichi lì, e il terminale riceve le credenziali. Questa è
la schermata di scelta che ti accoglie:

![Schermata di scelta del metodo di login](assets/01-login.svg)

Le due opzioni corrispondono a due modi diversi di pagare:

- **Abbonamento claude.ai (Pro/Max)** — la via semplice per uso personale:
  OAuth via browser, nessuna API key da gestire, costo fisso mensile.
- **Claude Console (API)** — per billing a consumo o aziendale: paghi a
  token effettivamente usati, senza limiti orari.

| Piano | Costo | Claude Code |
|---|---|---|
| Free | 0 $ | ❌ non incluso |
| Pro | 20 $/mese | ✅ ~200 messaggi / 5 ore |
| Max 5x / 20x | 100 / 200 $/mese | ✅ limiti 5x / 20x rispetto a Pro |
| API | a token | ✅ senza limiti orari |

Come leggere la tabella: i piani in abbonamento hanno un budget di messaggi
che si rinnova ogni 5 ore. Per iniziare **Pro basta** — il limite si sente
solo con un uso intensivo. Se Claude Code diventa il tuo strumento
principale, Max 5x è l'upgrade naturale; l'API conviene quando serve un uso
senza tetti orari o fatturazione aziendale.

**Dove finiscono le credenziali.** Su Linux in
`~/.claude/.credentials.json`, con permessi `0600` (leggibile solo da te);
su macOS nel Keychain di sistema. Non devi toccarle mai a mano: per cambiare
account senza uscire dalla sessione c'è `/login`, per scollegarti `/logout`.

## Primo avvio

Finito il login ti trovi direttamente nel prompt interattivo. Niente wizard,
niente scelta del tema (quello si cambia dopo, con `/config`): Claude Code ti
mostra versione, modello attivo e piano, e aspetta il primo messaggio.

![Primo avvio: versione, modello, piano e prompt](assets/01-primo-avvio.svg)

Nota nella schermata i tre elementi in alto — versione, modello, piano —
sono la prima cosa da controllare quando qualcosa si comporta in modo
inatteso. Due comandi da conoscere subito:

- `/help` — l'elenco dei comandi disponibili.
- `/doctor` — la diagnostica completa: verifica installazione,
  configurazione, server MCP e stato degli aggiornamenti. Esiste anche
  fuori dalla sessione come `claude doctor`, utile proprio quando Claude
  non parte e non puoi usare lo slash command.

## Estensione VS Code (e le altre interfacce)

Per chi vive nell'editor esiste l'estensione ufficiale: cerca **"Claude
Code"** nel marketplace (publisher Anthropic, id `Anthropic.claude-code`,
richiede VS Code 1.98+). Rispetto alla CLI aggiunge un pannello di chat,
diff affiancati con commenti inline, checkpoint per riavvolgere il codice e
la gestione dei permessi direttamente dal prompt box.

Un dettaglio importante da capire: l'estensione include una **sua copia
della CLI**, ma **condivide la configurazione** — `~/.claude/settings.json`,
i CLAUDE.md, i server MCP, le skills. In pratica esiste una sola "identità"
di Claude Code sulla tua macchina: tutto quello che configuri nel terminale
(cap. 02) vale automaticamente anche nell'editor, e viceversa.

Esistono anche una **desktop app** (macOS/Windows/Linux) e **Claude Code on
web**: stessa sostanza, interfacce diverse. Questa guida usa la CLI, che è
dove vivono tutte le feature.

## Aggiornamenti

Con l'installer nativo la regola è: non fai nulla. Il binario controlla e
scarica gli aggiornamenti da solo, in background. Se vuoi forzare
l'aggiornamento a mano c'è `claude update`; per sapere com'è andato l'ultimo
tentativo, `claude doctor`.

L'unica scelta che puoi fare è **quale canale di rilascio** seguire. Si
configura in `settings.json` (il file di configurazione che vedremo in
dettaglio nel cap. 02 — per le impostazioni personali è
`~/.claude/settings.json`). Il file completo, nel caso minimo, è questo:

```json
{ "autoUpdatesChannel": "stable" }
```

I valori possibili sono due: `latest` (il default — ricevi le novità appena
escono) e `stable` (circa una settimana indietro, così le release con
regressioni vengono saltate prima che ti arrivino). Se hai installato con
Homebrew/WinGet/apt, invece, l'auto-update non c'è: aggiorni con il package
manager, come per qualunque altro pacchetto.

---

**In sintesi**: `curl | bash`, login col browser, `/doctor` se qualcosa non
torna. Prossimo capitolo: dove vive la configurazione e come piegarla al tuo
progetto.
