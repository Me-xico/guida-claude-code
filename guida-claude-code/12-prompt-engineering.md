# 12 - Prompt engineering per Claude Code

> Fonte: best practices ufficiali e pattern consolidati della community,
> luglio 2026.

## Il modello mentale giusto

Il problema di partenza è quasi sempre lo stesso: tratti Claude Code come un
motore di ricerca a cui strappare risposte, domanda secca, risposta secca,
delusione. Il modello mentale che funziona è un altro: è un **junior
brillante che gestisci**. Un junior con memoria azzerata a ogni sessione
(per questo esiste CLAUDE.md), velocissimo, che non si offende mai, ma
con una richiesta vaga produce un risultato vago, esattamente come farebbe
un junior vero con un ticket che dice solo "sistemare il login".

Tu sei il PM: più chiaro il brief, migliore la consegna. Tutto questo
capitolo è declinazione di questa frase.

## Specificità: criteri di successo, non aggettivi

Il dolore: chiedi "migliora questo componente", ottieni un refactor che
tocca venti righe che non c'entrano, e il problema vero, i re-render, è
ancora lì. Non è colpa del modello: "migliora" non dice *cosa* dev'essere
vero alla fine.

Debole: "migliora questo componente".
Forte:

> "Riduci i re-render di `ProductList`: memoizza le callback passate ai
> figli, sposta il filtro in un `useMemo`, e verifica con il Profiler che al
> cambio di `query` re-renderizzi solo la lista. Non cambiare l'API
> pubblica."

La differenza non è la lunghezza: è che il secondo ha **criteri
verificabili** (cap. 11, "verifica col Profiler che…") e **vincoli** (cosa
non toccare, "non cambiare l'API pubblica"). Aggettivi come "migliore",
"pulito", "moderno" non sono istruzioni: sono speranze. Il test rapido per
il tuo prompt: *un collega che non conosce il contesto saprebbe dire se il
lavoro è finito bene?* Se no, mancano i criteri.

*Il segnale che ti serve*: il risultato è "tecnicamente quello che ho
chiesto" ma non quello che volevi. Il problema era nel brief.

## Contesto e vincoli, non micro-istruzioni

L'errore opposto alla vaghezza: dettare *come* fare ogni passo, riga per
riga. Non serve: per quello c'è il modello, che il codice lo sa scrivere.
Serve invece dare ciò che il modello **non può sapere** guardando il repo:

- il *perché*: "questo form è il funnel di pagamento: la priorità è non
  rompere il tracking", cambia ogni decisione a valle
- i **vincoli**: "Node 18, niente dipendenze nuove"
- i **riferimenti**: "`@src/components/Form.tsx` è il pattern da seguire"

E il contesto passalo nella forma più ricca disponibile: riferisci i file
con `@` (invece di descriverli), incolla gli errori **interi** (lo stack
trace contiene la risposta più spesso di quanto pensi), allega screenshot
(`Ctrl+V`) quando il problema è visivo. Un prompt che mette insieme i pezzi:

> "Il tracking del funnel si è rotto dopo l'ultimo refactor. Questo form è
> il funnel di pagamento: priorità assoluta non perdere eventi. Errore in
> console: [incollato intero]. Il pattern corretto di invio eventi è in
> `@src/analytics/track.ts`. Vincolo: niente dipendenze nuove."

Perché funziona: il modello ragiona su quello che ha nel contesto. Perché,
vincoli e riferimenti sono esattamente le informazioni che non può dedurre
da solo: tutto il resto sì.

## Decomposizione: chiedi il primo passo, non il viaggio

L'errore più segnalato in assoluto (il "greed mistake"): chiedere in un
prompt solo una feature intera, "fammi il carrello con persistenza,
sconti, e la pagina checkout", e ottenere il 60% di otto cose diverse,
nessuna finita, con il contesto ormai saturo (cap. 13). Al contrario:

> "Costruiamo il carrello a passi. Step 1: solo il data-layer — hook
> `useCart` con aggiunta, rimozione, quantità, e i test Vitest. Niente UI,
> niente persistenza per ora. Poi ci vediamo qui e decidiamo lo step 2."

Ogni passo finito e verificato è un checkpoint (in senso letterale: cap. 03)
su cui costruire il successivo. Se lo step 2 va male, torni a un punto
solido invece di dover disfare una matassa.

Per le feature grandi, il pattern ufficiale è **farsi intervistare**, utile
proprio perché i requisiti che *credi* di avere chiari non lo sono:

> "Devo costruire X. Prima di scrivere codice, intervistami: fammi le domande
> che servono a chiarire requisiti e edge case, poi scrivi una spec in
> SPEC.md."

Le domande di Claude fanno emergere gli edge case a cui non avevi pensato
(cosa succede al carrello se l'utente fa logout? gli sconti si sommano?).
Rivedi la spec, `/clear`, e in una sessione fresca: "implementa SPEC.md,
step 1". La spec sostituisce cento correzioni in corsa, e la sessione che
implementa parte pulita, senza il rumore della discussione.

*Il segnale che ti serve*: stai scrivendo un prompt che contiene "e poi… e
anche…". Fermati alla prima "e".

## Iterare: feedback concreti, non ripetizioni

Il dolore: il risultato è sbagliato, tu rispieghi la stessa cosa con più
enfasi ("no, il bottone deve stare A DESTRA"), e va male di nuovo. Ripetere
più forte non aggiunge informazione. Dai invece **materiale nuovo**:
l'errore esatto, l'output del test, lo screenshot di cosa si vede davvero.
"Non funziona" non dà a Claude nulla su cui lavorare; uno stack trace sì:

> "Il fix non basta: al submit ora arriva questo — [stack trace intero].
> Ecco anche lo screenshot dello stato del form [Ctrl+V]. Nota che succede
> solo quando il campo email è vuoto."

E ricorda la regola dei 2 tentativi (cap. 03): al secondo giro andato male,
`/clear` e riformula da zero incorporando quello che hai imparato. Il
motivo è meccanico: ogni correzione fallita resta nel contesto e pesa sulle
risposte successive: le correzioni accumulate inquinano più di quanto
aiutino. Il terzo tentativo nella stessa sessione parte svantaggiato; lo
stesso prompt, riscritto meglio in una sessione pulita, parte avvantaggiato.

## Prima/dopo

| Debole | Forte |
|---|---|
| "fixa il bug del login" | "il login fallisce con 401 dopo il refresh del token — ecco il log: […]. Il flusso è in `@src/auth/`. Trova la causa, proponi il fix, e aggiungi un test che riproduca il caso" |
| "aggiungi i test" | "copri `useCart` con Vitest: aggiunta, rimozione, quantità a zero, carrello vuoto. Guarda `@src/hooks/useAuth.test.ts` per lo stile" |
| "rifai il css della navbar" | "la navbar deve diventare sticky con blur al scroll, come in questo screenshot [Ctrl+V]. Solo CSS modules, niente librerie. Poi screenshot del risultato" |

Nota il pattern comune delle versioni forti: fatto osservabile (log,
screenshot) + dove guardare (`@`) + criterio di fine (test, screenshot del
risultato). Sono sempre gli stessi tre ingredienti.

---

**In sintesi**: criteri verificabili + vincoli + contesto, un passo alla
volta, feedback fatti di prove. Il prompt perfetto non esiste; il prompt con
un criterio di successo verificabile sì, ed è quello che conta.
