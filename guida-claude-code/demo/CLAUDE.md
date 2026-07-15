# demo-app

SPA React + TypeScript (Vite). Componenti in `src/components/`, un file per
componente, stile con CSS modules (niente styled-components).

## Comandi

- `npm run dev` — dev server
- `npm run test` — test (Vitest); lanciali prima di dichiarare finito un task
- `npm run lint` — ESLint su src/

## Convenzioni

- TypeScript strict: niente `any`, preferisci type inference dove possibile.
- Componenti funzione + hooks, niente class components.
- I test stanno accanto al componente: `Button.tsx` → `Button.test.tsx`.
- Messaggi di commit in inglese, imperativi ("add login form") — override
  consapevole della regola globale "commit in italiano": è materiale didattico
  pensato per un pubblico generico.
