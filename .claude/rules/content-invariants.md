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
- **INV-2: Callout de atribuição.** Toda seção abre com um `callout-note` dizendo de onde vem — "Esta seção corresponde à seção 1.3 de @bruce2020", "se baseia na seção 6.6.4 de @bussab2023", "se inspira no Capítulo 10 de @weed" —, com o número **da fonte**, nunca o nosso (Bruce cap. 2 → nossos Caps. 2 e 3; Bruce cap. 3 → nosso Cap. 4; Bruce cap. 4 → nosso Cap. 5).
- **INV-3: Escopo.** Nada de t/qui-quadrado/F/Poisson no Cap. 2, de ANOVA/qui-quadrado/testes múltiplos/poder no Cap. 4, nem de variáveis fatoriais/diagnóstico/splines no Cap. 5. Curtose, violino, curva de densidade, valor esperado (1.6) e heatmap (1.7) foram cortados.
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
