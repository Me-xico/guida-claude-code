# 11 — Verifica: il principio più importante di tutta la guida

> Fonte: best practices ufficiali ("the single most impactful tip in this
> guide is verification") + doc su hook e /goal, luglio 2026.

## Il problema

Scenario che prima o poi capita a tutti: chiedi una modifica, Claude lavora
qualche minuto, conclude con un rassicurante "fatto, ora funziona", tu ti
fidi, mergi — e alle 18:30 scopri che il form di pagamento non invia più
nulla. Il codice *sembrava* giusto. Il messaggio *suonava* sicuro. Ma nessuno
aveva davvero verificato niente: né Claude, né tu.

La differenza tra una sessione che devi sorvegliare riga per riga e una da
cui puoi allontanarti è una sola: **Claude ha un modo per verificare da solo
il proprio lavoro?** Se sì, il loop diventa lavora → controlla → correggi →
ripeti finché passa, senza di te nel mezzo. Se no, il test runner sei tu — e
sei anche il collo di bottiglia.

## Come si applica: dai a Claude un criterio eseguibile

Per un frontend dev i "modi per verificare" sono concreti e quasi sempre già
nel progetto:

- i **test**: "scrivi prima i test (devono fallire), poi implementa finché
  passano" — il TDD si sposa con Claude meglio che con gli umani, perché il
  test fallito è un segnale che il modello può leggere e inseguire da solo
- l'**exit code della build**: `npm run build` che esce 0
- il **lint/typecheck**: `tsc --noEmit`
- lo **screenshot confrontato col mock**: "ecco il design; implementa, fai lo
  screenshot, confronta, elenca le differenze, correggi" (cap. 10)

Un prompt completo, per fissare la forma:

> "Aggiungi la validazione a `@src/components/CheckoutForm.tsx`: email
> obbligatoria e formato valido, CAP a 5 cifre. Prima scrivi i test Vitest
> per questi casi (devono fallire), poi implementa. Considera finito solo
> quando `npm test` passa e `tsc --noEmit` esce pulito."

Nota la struttura: cosa fare, come verificarlo, quando fermarsi. Il criterio
di verifica costa una riga in più e cambia tutto quello che viene prima.

## Perché funziona

Senza un criterio, "finito" è un giudizio del modello su sé stesso — e il
modello, come chiunque abbia appena scritto del codice, tende a crederci.
Con un criterio eseguibile, "finito" diventa un fatto osservabile: il test
passa o non passa. Claude può iterare contro quel fatto in autonomia, e ogni
iterazione consuma il *suo* tempo, non il tuo.

## Chiedi evidenze, non asserzioni

"Fatto, ora funziona" non è informazione: è una speranza. La contromossa è
sempre la stessa domanda, in tre varianti:

> "Mostrami l'output dei test."
> "Incolla l'exit code della build."
> "Fammi lo screenshot del componente com'è adesso."

Rivedere le **prove** è molto più veloce che ri-verificare tutto a mano. E
c'è un effetto secondario prezioso: Claude, sapendo che dovrà esibirle,
lavora meglio — esattamente come un junior che sa che il PR verrà letto
davvero.

*Il segnale che ti serve*: ti accorgi che stai per accettare un "fatto"
sulla parola. Fermati lì e chiedi l'evidenza.

## La scala della verifica

Quattro livelli, dal più leggero al più blindato. Il criterio per salire è
uno solo: **quanto costa l'errore se passa inosservato**.

1. **Nel prompt** — "…e considera finito solo quando `npm test` passa".
   Gratis, funziona quasi sempre. È il default: se non stai facendo almeno
   questo, parti da qui.
2. **`/goal`** — dichiari la condizione ("tutti i test passano e la build è
   verde") e un valutatore separato la ricontrolla a ogni turno, senza
   lasciar chiudere la sessione finché non è vera. Utile quando la sessione
   è lunga e temi che il criterio scritto nel prompt "sbiadisca" strada
   facendo.
3. **Stop hook** (cap. 07) — uno script che lancia i test quando Claude
   dichiara di aver finito, ed esce con `2` se falliscono: il "finito" viene
   respinto d'ufficio. È il livello **deterministico**: non dipende più
   dall'attenzione del modello, è codice che gira sempre.
4. **Subagent revisore** (cap. 06) — un agente a contesto fresco che giudica
   il lavoro senza il bias di chi l'ha scritto. Copre quello che i test non
   coprono: requisiti fraintesi, casi mancanti, scelte discutibili.

*Il segnale che devi salire di livello*: hai appena trovato in produzione
(o in review) un errore che il livello attuale avrebbe dovuto fermare.

## La review avversaria (con l'antidoto)

Il problema: chi ha scritto il codice — umano o modello — non vede più i
propri errori; il contesto della sessione contiene tutte le giustificazioni
delle scelte fatte, e quelle giustificazioni "convincono" anche il revisore
se è la stessa sessione. Il pattern: scrivi con una sessione, fai
revisionare a una **seconda** sessione (o al `/code-review` built-in) a
contesto pulito — chi non ha scritto il codice vede quello che l'autore non
vede più.

**Ma attenzione all'effetto collaterale documentato**: un reviewer istruito
a trovare problemi ne troverà *sempre* — è il suo mandato. Se ubbidisci a
ogni finding, dopo tre giri di review ti ritrovi con astrazioni, guard
clause e configurabilità che nessuno ha chiesto: l'over-engineering da
review. L'antidoto è limitare il mandato in partenza:

> "Fai la review di questo diff. Segnala **solo** bug reali e requisiti
> mancati rispetto a SPEC.md. Non proporre migliorie di stile, refactoring
> o astrazioni: se qualcosa funziona ed è nei requisiti, passa."

I suggerimenti extra che arrivano comunque: trattali come opzionali, non
come to-do.

## Il caso senza test

Codebase legacy senza test? È il caso in cui la verifica serve *di più*,
non di meno: stai per toccare codice di cui nessuno ricorda il
comportamento previsto. Non rinunciare — falla creare a Claude:

> "Prima di toccare qualsiasi cosa, scrivi un test di caratterizzazione che
> fotografa il comportamento **attuale** di `formatPrice` in
> `@src/utils/price.ts`: input tipici, zero, negativi, valute diverse.
> Deve passare così com'è. Poi, e solo poi, fai il refactor — il test deve
> continuare a passare."

Il test di caratterizzazione non dice che il codice è giusto: dice che il
refactor non ha cambiato nulla. Che è esattamente la garanzia che ti serve
sul legacy.

---

**In sintesi**: mai chiedere un lavoro senza chiederti "come farà a sapere
di averlo finito bene?". Un criterio verificabile nel prompt costa una riga
e cambia la qualità di tutto il resto. È il capitolo da rileggere quando gli
altri sembrano non funzionare — perché di solito è questo che manca.
