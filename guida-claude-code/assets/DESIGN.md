# Design system degli asset della guida

File interno (escluso dalla build, vedi `exclude_docs` in mkdocs.yml).
Regole per chiunque — umano o agente — produca o modifichi asset e layout.

## Due famiglie di asset, due mestieri

1. **Terminali Rich** (`NN-slug.svg`, ~15-21 KB): "cosa vedrai nella CLI".
   Generati con la libreria Python Rich (export SVG), font Fira Code 20px,
   chrome macOS (semafori rosso/ambra/verde), sfondo `#292929`, titolo
   centrato in italiano. NON disegnarli a mano: si generano da una sessione
   simulata. Contenuti sanitizzati per costruzione (policy in SANITIZE.md).
2. **Diagrammi flat** (`NN-slug.svg`, ~5-10 KB): "come è fatto il sistema".
   SVG scritti a mano, stile di riferimento: `18-flusso-agentico.svg`.

Ogni asset appartiene a UNA famiglia. Un capitolo può usarle entrambe:
il terminale mostra l'esperienza, il diagramma spiega la struttura.

## Diagrammi flat: convenzioni

- `viewBox` largo 960, altezza libera; font `system-ui, -apple-system,
  'Segoe UI', sans-serif`; nessun font esterno.
- Sfondo trasparente: i colori devono reggere sia il tema chiaro sia slate.
  Testo fuori dai box: SOLO il grigio neutro `#8A8FA3` (leggibile su
  entrambi). Testo dentro i box: bianco o tinta chiara della famiglia.
- Box: `rect` con `rx="9"`–`rx="12"`, fill pieno di palette, titolo bold
  14px, dettagli 11.5px nella tinta chiara.
- Fasce/raggruppamenti: bordo tratteggiato `#8A8FA3` (`stroke-dasharray="6 4"`),
  etichetta maiuscola 13px bold con `letter-spacing`.
- Frecce: marker triangolare `#8A8FA3`; ritorni/loop con tratteggio `4 4`.
- Legenda in alto a destra quando i colori codificano una dimensione.

## Palette semantica (coerente in TUTTA la guida)

| Colore | Hex | Significato | Tinta chiara testo |
|---|---|---|---|
| Viola | `#6D5BD0` | modello di punta / orchestratore / chi giudica | `#E8E4FA` |
| Blu | `#2E86AB` | modello medio / worker / esecuzione | `#D9EDF7` |
| Verde | `#4F9153` | modello piccolo / meccanico / esito positivo | `#DDEEDD` |
| Ambra | `#B0763B` | skill, procedure, orchestrazioni scritte | `#F7E8D5` |
| Grigio scuro | `#41465A` | l'utente, l'esterno, il neutro attivo | `#FFFFFF` |
| Grigio medio | `#8A8FA3` | etichette, frecce, contorni, testo su sfondo pagina | — |

Il significato è vincolante: non usare il viola per una skill o l'ambra per
un modello. Un diagramma che introduce una dimensione nuova sceglie UN
colore libero e lo dichiara in legenda.

## Naming e riuso

- `NN-slug.svg` dove NN = capitolo che lo usa; slug in kebab-case italiano.
- Asset condivisi tra le lingue: etichette in italiano, un solo file.
- Un asset = un capitolo (oggi nessun riuso; se un diagramma serve a due
  capitoli, vive nel capitolo che lo spiega e l'altro lo linka).

## Layout nel markdown (Material)

- Admonition per i richiami: `!!! tip` (pratica), `!!! warning` (trappola),
  `!!! note` (contesto). Titolo in italiano. Mai più di una ogni ~3 paragrafi.
- `??? note` (collassata) per gli approfondimenti opzionali.
- Tabs (`=== "macOS/Linux"`) per varianti di piattaforma o alternative.
- Code annotations (`# (1)!`) per spiegare i punti di uno snippet senza
  spezzarlo.
- Tabelle per elenchi confrontabili; prosa per il resto. Niente em-dash.
