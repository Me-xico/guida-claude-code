# 10 - Il workflow frontend: Claude con un browser vero

> Verificato il 15 luglio 2026. È IL capitolo per chi fa frontend: qui il
> loop di verifica (cap. 11) diventa visivo.

## Il salto di qualità

Senza browser, Claude scrive CSS alla cieca: lui modifica, tu guardi,
descrivi a parole cosa non va ("no, il padding è ancora troppo stretto"),
lui riprova. Sei tu il suo apparato visivo, ed è il collo di bottiglia.
Con un browser collegato, **Claude vede quello che vedi tu**: naviga la
pagina, legge la console, fa screenshot, confronta col design e si corregge
da solo. Il loop diventa chiuso. Tu esci dal giro delle iterazioni per
rientrare solo all'approvazione finale.

Le strade per collegare un browser sono due (più una terza freccia per il
debugging). Vediamole con lo stesso schema: cos'è, come si installa, come
funziona.

## Strada 1: Playwright MCP (gratuito, open source)

**Cos'è**: un server MCP (cap. 08) che dà a Claude un browser tutto suo,
headless o visibile, da pilotare: aprire pagine, cliccare, compilare
form, fare screenshot, leggere la console.

**Come si installa**: una riga, con la sintassi vista nel cap. 08 (nome del
server, `--`, comando di avvio):

```bash
claude mcp add playwright -- npx -y @playwright/mcp@latest
```

> **Testato dal vivo il 15 lug 2026**, due trappole reali incontrate:
> 1. di default il server cerca **Google Chrome**: se non ce l'hai (o
>    preferisci altro), scegli l'engine con `--browser firefox` o
>    `--browser chromium` in coda al comando;
> 2. al primo avvio può chiedere un browser che non hai in cache, si
>    risolve con `npx @playwright/mcp install-browser [firefox]`.
> Fatto questo, il test "apri example.com e dimmi titolo e h1" risponde
> correttamente con un browser vero (verificato qui su Firefox: lo user
> agent riportava proprio Gecko/Firefox).

**Come funziona**: da qui in poi, quando chiedi qualcosa che riguarda una
pagina, Claude usa i tool del server per pilotare il browser. Il punto
tecnico che lo rende potente: non ragiona (solo) sui pixel, ma
sull'**accessibility tree**, la rappresentazione strutturata della pagina
che il browser costruisce per gli screen reader. Sono dati deterministici
("c'è un bottone con label 'Salva'", "questo campo è required"), che Claude
legge con precisione dove uno screenshot lascerebbe ambiguità. Perfetto
per: verificare flussi, compilare form, leggere errori console, e come
base dei test e2e. Bonus non piccolo: se la tua UI è illeggibile per
l'accessibility tree, hai appena scoperto un problema di a11y, lo stesso
che avrebbe uno screen reader.

## Strada 2: l'estensione Chrome ufficiale (Anthropic, per gli abbonati)

**Cos'è**: Claude dentro il *tuo* Chrome, non in un browser a parte. La
differenza pratica: le tue sessioni già autenticate, il tuo stato reale,
niente da rifare login o ricostruire. E risposte più mirate: Playwright su
pagine complesse può restituire alberi da decine di migliaia di token,
l'estensione lavora in modo più selettivo.

**Come si ottiene**: è legata all'abbonamento, controlla la disponibilità
sul tuo piano su claude.ai. Se ce l'hai, è la strada più comoda per lo
sviluppo interattivo quotidiano; Playwright resta il cavallo di battaglia
per l'automazione e per chi parte da zero.

## Terza freccia: Chrome DevTools MCP

Per il debugging profondo c'è un terzo server:

```bash
claude mcp add chrome-devtools -- npx chrome-devtools-mcp@latest
```

Parla il protocollo DevTools di Chrome: network, performance, coverage,
le tab che apriresti tu in DevTools, lette da Claude. È complementare a
Playwright: quello pilota la pagina, questo la ausculta.

## Il ciclo screenshot-driven

Con il browser collegato si sblocca il pattern ufficiale per implementare
da design. Tre mosse:

1. **Dai il mock**: incolla lo screenshot del design (`Ctrl+V` in sessione)
   o collega Figma (sotto). Questo è il *target*: un'immagine, non una
   descrizione a parole.
2. **Chiedi il loop completo**, non solo l'implementazione: "implementa
   questo componente; poi avvia il dev server, apri la pagina, fai uno
   screenshot, confrontalo col mock, elenca le differenze e correggile.
   Ripeti finché non corrispondono." La frase chiave è *ripeti finché*: è
   quello che trasforma un tentativo unico in un ciclo.
3. Claude itera da solo: implementa → guarda (screenshot vero, dal browser
   vero) → confronta → corregge → riguarda.

Cosa aspettarsi: la prima iterazione sarà al 70%; la terza, quasi
indistinguibile dal mock. Il tuo lavoro si sposta da "descrivere le
differenze a parole" ad "approvare il risultato", che è esattamente il
mestiere che vuoi fare.

Lo stesso loop vale al contrario, per i bug visivi: incolla lo screenshot
del glitch e chiedi "riproduci, trova la causa, correggi, dimostra con uno
screenshot dopo". Lo screenshot finale è l'evidenza che il fix funziona.

## Figma

**Cos'è**: il server MCP ufficiale di Figma, che collega il design system
alla sessione. È un server remoto (HTTP, cap. 08): niente processi locali,
si aggiunge con l'URL e si autentica col tuo account Figma:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

**Come funziona**: Claude legge frame, componenti e design token
direttamente dal file Figma, non da uno screenshot, ma dai dati. "Usa i
token di spacing del design system, non valori a mano" smette di essere
una speranza: Claude i token li vede davvero. E dal 2026 l'integrazione
con Claude Code è bidirezionale, anche code → canvas.

## Il quadro completo

Con questo stack (Playwright o estensione + Figma + i test del cap. 11),
un task frontend suona così:

> "Implementa la card prodotto dal frame Figma 'ProductCard v2'. Componente
> in `src/components/`, CSS modules, dati mock. Poi: dev server, screenshot
> alla viewport 375px e 1280px, confronto col frame, correggi le differenze.
> Chiudi quando gli screenshot corrispondono e `npm run test` passa."

Nota i tre ruoli: il design come **input verificabile** (il frame Figma,
non una descrizione), il browser come **strumento di verifica** (gli
screenshot alle due viewport), i test come **cancello** (non si chiude
finché non passano). È il capitolo 11 applicato al frontend, ed è il
motivo per cui questo setup ripaga l'ora che costa metterlo in piedi.

---

**In sintesi**: Playwright MCP subito (una riga, gratis), l'estensione
Chrome se il tuo piano la include, Figma quando lavori da design. E da
domani, mai più "aggiusta il padding" a parole: screenshot, loop, evidenze.
Qui si chiude la Potenza; nel Riferimento trovi le cinque mosse dei primi
30 minuti e la mappa dei costi (cap. 14).
