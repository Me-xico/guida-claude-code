# 17 - Ricercare e progettare prima di implementare

> Verificato il 16 luglio 2026 sulla doc ufficiale. Claude Design e Ultraplan
> sono in research preview: comportamento e disponibilità possono cambiare.

## Il principio

Il capitolo 11 insegna a verificare il lavoro *fatto*. Questo capitolo
applica la stessa idea un passo prima: **il codice più costoso è quello
scritto sopra una decisione sbagliata**. Una libreria scelta male, un
approccio che non regge il caso d'uso, un requisito frainteso: nessun test
li cattura, perché il codice fa esattamente ciò che gli hai chiesto — è la
richiesta a essere sbagliata. La cura sono due attività che precedono
l'implementazione, ognuna col suo strumento: la **ricerca** (capire il
mondo prima di decidere) e la **progettazione** (decidere la forma prima di
costruire).

## Deep research: la ricerca con le prove

**Cos'è.** `/deep-research` è una skill di serie (da giugno 2026) che
trasforma una domanda in un'indagine strutturata. Non è "cerca sul web":
è un harness multi-agente che produce un report con le fonti citate.

**Come funziona**, in quattro fasi:

1. **Chiarimento**: prima di partire ti fa due o tre domande per
   restringere il campo — la stessa logica dell'intervista del cap. 12,
   applicata alla ricerca.
2. **Fan-out**: un agente guida coordina più worker che cercano in
   parallelo, ognuno da un angolo diverso.
3. **Verifica avversaria**: le affermazioni raccolte vengono messe alla
   prova prima di entrare nel report — è il cap. 11 applicato alle fonti,
   non al codice.
4. **Sintesi citata**: il report finale collega ogni affermazione alla sua
   fonte, così *tu* puoi verificare a campione invece di fidarti.

**Quando usarla.** Il segnale è una decisione difficile da invertire presa
su un terreno che non conosci: quale libreria adottare, dove hostare un
progetto, se uno strumento è maturo e mantenuto, come si comporta davvero
un servizio nei suoi piani gratuiti. Un esempio vissuto da questa guida: la
scelta di dove pubblicare il suo sito è uscita da una ricerca così, cinque
opzioni di hosting verificate sui documenti ufficiali, con i vincoli reali
dei piani gratuiti che le pagine di marketing non dicono. E gli strumenti del
cap. 15 sono entrati in guida solo dopo lo stesso trattamento: repo giusto,
manutenzione, numeri dichiarati contro numeri misurati.

**Il costo, onestamente.** Una deep research consuma una fetta seria del
tuo budget (usa i normali limiti del piano): non è per il dubbio da trenta
secondi. La soglia pratica: se sbagliare la decisione ti costerebbe più di
un'ora di rework, la ricerca si ripaga.

## Progettare: dalla scaletta al piano rivisto

Per la progettazione la guida ti ha già dato due gradini; qui li mettiamo
in scala e aggiungiamo il terzo:

1. **Plan mode** (cap. 03) — il gradino quotidiano: Claude esplora e
   propone, tu correggi dieci righe di piano invece di cento di codice.
2. **Intervista → SPEC** (cap. 12) — per le feature grandi: Claude ti
   intervista, i requisiti impliciti emergono, la spec scritta sopravvive
   alla sessione. È il pattern che la doc ufficiale chiama "la via più
   rapida a una buona spec".
3. **Ultraplan** (`/ultraplan <richiesta>`, research preview, piani
   Pro/Max) — quando il piano merita una revisione da documento, non da
   terminale: Claude lo scrive in cloud e tu lo rivedi **nel browser**, con
   commenti inline sulle sezioni come su una PR. Approvato il piano, scegli:
   esecuzione in cloud (arriva una PR) o "teleport" del piano nel tuo
   terminale per eseguirlo in locale. Nota di disponibilità: non funziona
   sui provider cloud aziendali (Bedrock, Vertex, Foundry).

La scala è la stessa del cap. 11: sali di gradino quando sale il costo
dell'errore.

## Claude Design: progettare l'interfaccia col tuo design system

**Cos'è.** [Claude Design](https://claude.ai/design) (research preview,
inclusa nei piani a pagamento) è il canvas visuale di claude.ai: descrivi
e ottieni design, prototipi interattivi, mockup — e li raffini
conversando, come in una sessione di Claude Code ma con la tela al posto
del terminale.

**Perché interessa a chi fa frontend**: può **importare il tuo design
system** — dal repo GitHub, dai file, dal codebase — e valida quello che
genera contro i tuoi componenti reali prima di mostrartelo. Il mockup che
esce non è "un'idea da rifare coi componenti veri": è già fatto coi
componenti veri.

**Il ponte con Claude Code** è la skill `/design-sync`: bidirezionale, porta
il design system del repo dentro Claude Design e rimanda sul canvas quello
che costruisci nel terminale. Il flusso completo per una feature UI diventa:

1. esplori le direzioni in Claude Design (canvas, iterazione visiva veloce);
2. scelta la direzione, il mockup è già conforme al design system;
3. implementi in Claude Code col ciclo screenshot-driven del cap. 10,
   usando il mockup come target di verifica.

**E il Figma MCP?** (cap. 10) Complementari, non alternativi: Claude Design
per l'ideazione e la prototipazione rapida quando il design nasce con te;
il Figma MCP quando il design vive già in Figma o serve il round-trip
codice → canvas Figma per il team di design.

## In sintesi

Il flusso completo di un lavoro ben fatto ha quattro tappe, ognuna con lo
strumento e la verifica giusti: **ricerca** (`/deep-research`, fonti
citate) → **decisione** → **piano** (plan mode → SPEC → Ultraplan, revisione
proporzionata alla posta) → **implementazione** (cap. 03 e 10, col criterio
di "finito" del cap. 11). Ogni tappa saltata si ripresenta più avanti, con
gli interessi. A chiudere il Metodo resta il capitolo sugli errori comuni
(cap. 13): la checklist dei sintomi, prima di passare agli attrezzi.
