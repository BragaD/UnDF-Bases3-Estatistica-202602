---
paths:
  - "content/**/*.qmd"
  - "_quarto.yml"
  - "styles.css"
  - "notebooks/**/*.ipynb"
---

# Invariantes de conteúdo (INV-1 a INV-12)

Regras numeradas e inegociáveis para o conteúdo deste livro. Críticos, revisores e auditores
citam o número ao apontar um problema ("viola INV-3") — e o campo `rule` de um `FINDING`
(ver `.claude/references/orchestration-schemas.md`) deve citar um destes invariantes, o
`CLAUDE.md` ou a `knowledge-base.md`. Cada invariante resume uma regra do `CLAUDE.md`; em caso
de conflito, o `CLAUDE.md` vence.

## Estrutura

- **INV-1: Registro no `_quarto.yml`.** Todo `.qmd` novo em `content/` é listado em `book.chapters`. Arquivo não listado não existe para o leitor.
- **INV-2: Callout de atribuição.** Toda seção abre com um `callout-note` dizendo de onde vem — "Esta seção corresponde à seção 1.3 de @bruce2020", "se baseia na seção 6.6.4 de @bussab2023", "se inspira no Capítulo 10 de @weed" —, com o número **da fonte**, nunca o nosso. Hoje o livro só tem o Cap. 1, que corresponde ao cap. 1 do Bruce, então os dois coincidem — mas a coincidência é temporária.
- **INV-3: Escopo.** O livro tem hoje **só a Introdução e o Cap. 1**; os Caps. 2 a 5 foram removidos em 2.2026. Do Cap. 1 foram cortados: curtose, violino, curva de densidade, convenções `lower`/`higher` de quantil, valor esperado (1.6) e heatmap (1.7); a 1.8 é leitura complementar, fora do cronograma e do notebook. O capítulo de **probabilidade** será reescrito a partir de @bussab2023 caps. 5–7, com **escopo ainda não definido** — pergunte antes de escrever.
- **INV-4: Bibliografia única.** Toda citação resolve em `references.bib`. `@bussab2023` **não** vira 2017.

## Código

- **INV-5: Semente explícita.** Todo chunk com aleatoriedade usa `np.random.default_rng(<semente>)` ou `random_state=<semente>`.
- **INV-6: Caminhos a partir da raiz.** `pd.read_csv("dados/...")`, nunca `../../dados/...` (`execute-dir: project`).
- **INV-7: Python, não R.** Todo exemplo executável é Python; dependência nova entra no `pyproject.toml` com limite superior de versão.
- **INV-8: Números da prosa vêm do código.** Valores que dependem dos dados entram por `` `{python} num(...)` `` ou são conferidos contra a saída do chunk. Um número digitado à mão que diverge da saída é erro.

## Widgets (OJS)

- **INV-9: OJS consome `ojs_define`.** Nunca recarrega o CSV nem embute valores literais; sempre `//| echo: false`. Verificação é pelo teste de navegador, não por `grep`.

## Pedagogia e apresentação

- **INV-10: Motivação antes da fórmula.** Toda definição é precedida por uma pergunta, um exemplo ou um dado que a torne necessária.
- **INV-11: No máximo dois blocos coloridos seguidos.** Callouts, `.conceito` e `.exemplo` empilhados diluem a ênfase; o terceiro vira prosa.
- **INV-12: Nada secreto no HTML.** `.spoiler` é ofuscação. Gabaritos e provas ficam em `avaliacoes/` (gitignorado); o repositório é público.
