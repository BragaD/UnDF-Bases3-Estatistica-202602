# Conteúdo do Capítulo 1 — Análise Exploratória de Dados

**Data:** 2026-07-13
**Status:** Aprovado

## Objetivo

Escrever o conteúdo das 7 seções restantes do Capítulo 1 do livro *Bases 3 — Estatística*, hoje em stub, e adequar a seção 1.3 (já escrita) ao padrão que este spec estabelece.

O scaffolding do repositório está completo e publicado: <https://BragaD.github.io/UnDF-Bases3-Estatistica-202602>. As 38 seções já estão registradas no `_quarto.yml` e navegáveis; 37 exibem "em construção". Este spec preenche 7 delas.

## Fonte

Capítulo 1 de Bruce, Bruce & Gedeck — *Practical Statistics for Data Scientists*, 2ª ed.
Código Python de referência: `python/code/Chapter 1 - Exploratory Data Analysis.py` em <https://github.com/gedeck/practical-statistics-for-data-scientists>

## Decisões do autor

Quatro decisões tomadas no brainstorming, que governam tudo abaixo:

1. **Profundidade:** cada seção tem o mesmo peso da 1.3 (~130 linhas) — auto-suficiente, com conceito, fórmula em LaTeX, código executado, gráfico, callouts e tabela-resumo. Uma aula por seção.
2. **Exercícios:** 2–3 ao fim de **cada** seção, sobre os mesmos datasets.
3. **Fidelidade ao livro:** sem analogias de engenharia de software. Os exemplos e o enquadramento são os do livro-texto.
4. **Respostas:** em callout recolhível nativo do Quarto (`::: {.callout-tip collapse="true"}`). Não usar `spoiler.html` — ele é ofuscação que se apresenta como senha, e o conteúdo vai em texto puro no HTML público.

## Retrofit da seção 1.3

A 1.3 foi escrita antes destas decisões e as viola em dois pontos. Sem corrigir, ela vira o ponto fora da curva do capítulo:

- **Remover a ponte para computação.** O callout final cita "renda, população, **tempo de resposta de um servidor**". A menção sai; ficam os exemplos do livro.
- **Acrescentar exercícios.** Hoje ela termina na tabela-resumo. Ganha a seção `## Exercícios` no mesmo formato das demais.

Nada mais muda nela: os números (média 6.162.876,3 / aparada 4.783.697,1 / mediana 4.436.369,5 / ponderadas 4,4458 e 4,4) e o código permanecem intactos.

## As 7 seções

Todas seguem o esqueleto da 1.3: título `#`, `callout-note` citando a seção do livro, chunk `setup` com `include: false`, prosa e código intercalados, callouts `.conceito`/`.exemplo`, tabela-resumo, e `## Exercícios` ao final.

### 1.1 — Elementos de Dados Estruturados
**Arquivo:** `content/cap01/01-dados-estruturados.qmd` · **Dados:** `state.csv`, `dfw_airline.csv`

Taxonomia dos tipos de dados: **numérico** (contínuo, discreto) e **categórico** (nominal, ordinal, binário). Por que a distinção importa: ela determina o tipo de gráfico, a análise cabível e como o software armazena e valida o dado.

O livro trata esta seção de forma quase inteiramente conceitual. Para alcançar o peso decidido, ela ganha código que **demonstra** a taxonomia em vez de apenas descrevê-la: `dtypes` do pandas, `astype("category")`, e categórico **ordenado** (`CategoricalDtype(ordered=True)`) mostrando que a ordem permite comparação (`<`) que o nominal não permite. Isso é fiel ao espírito do livro, que enfatiza a importância dos tipos para o software.

### 1.2 — Dados Retangulares
**Arquivo:** `content/cap01/02-dados-retangulares.qmd` · **Dados:** `state.csv`

O DataFrame como estrutura central. Vocabulário e seus sinônimos entre disciplinas: *feature* (variável, atributo, preditor, coluna) e *outcome* (resposta, variável dependente, alvo); registro (linha, caso, observação). Índice do DataFrame.

Dados **não** retangulares, e por que existem: séries temporais, dados espaciais e grafos.

### 1.4 — Estimativas de Variabilidade
**Arquivo:** `content/cap01/04-estimativas-variabilidade.qmd` · **Dados:** `state.csv`

Desvio-padrão, variância e desvio absoluto médio. Amplitude interquartil (IQR) como `quantile(0.75) - quantile(0.25)`. **Desvio absoluto mediano (MAD)** via `statsmodels.robust.scale.mad`, e a demonstração de que ele equivale a `median(|x - median(x)|) / 0.6745` — o fator que o calibra para ser comparável ao desvio-padrão numa distribuição normal.

O fio condutor é o mesmo da 1.3: as medidas robustas (IQR, MAD) versus as sensíveis a extremos (desvio-padrão).

Gráfico: comparação visual das medidas de dispersão sobre a distribuição de população.

### 1.5 — Explorando a Distribuição dos Dados
**Arquivo:** `content/cap01/05-distribuicao-dados.qmd` · **Dados:** `state.csv`

Percentis e quantis (`quantile([0.05, 0.25, 0.5, 0.75, 0.95])` sobre `Murder.Rate`). **Boxplot** da população. Tabela de frequência via `pd.cut` em 10 faixas, com os estados de cada faixa. **Histograma**. **Estimativa de densidade** — histograma com `density=True` sobreposto à curva de densidade da `Murder.Rate`.

### 1.6 — Explorando Dados Binários e Categóricos
**Arquivo:** `content/cap01/06-dados-binarios-categoricos.qmd` · **Dados:** `dfw_airline.csv`

Tabela de proporções das causas de atraso no aeroporto de Dallas/Fort Worth (`100 * dfw / dfw.values.sum()`). **Gráfico de barras** — e por que ele não é um histograma. **Moda**. **Valor esperado** como média ponderada pelas probabilidades. Probabilidade.

### 1.7 — Correlação
**Arquivo:** `content/cap01/07-correlacao.qmd` · **Dados:** `sp500_data.csv.gz`, `sp500_sectors.csv`

Coeficiente de correlação de Pearson e sua fórmula. Matriz de correlação das ações de telecomunicações (`sector == 'telecommunications_services'`, a partir de 2012-07-01). **Heatmap** das ETFs com `seaborn.heatmap` e paleta divergente. **Scatterplot** de T contra VZ.

As armadilhas, que são o ponto pedagógico da seção: correlação não implica causalidade; o coeficiente é sensível a outliers; e mede apenas relação **linear** — duas variáveis podem ter dependência forte e correlação zero.

### 1.8 — Explorando Duas ou Mais Variáveis
**Arquivo:** `content/cap01/08-duas-ou-mais-variaveis.qmd` · **Dados:** `kc_tax.csv.gz`, `lc_loans.csv`, `airline_stats.csv`

A seção mais longa: cobre os três pares de tipos.

- **Numérico × numérico** (`kc_tax`, filtrado para `TaxAssessedValue < 750000`, `100 < SqFtTotLiving < 3500`): por que o scatterplot falha com centenas de milhares de pontos, e as duas saídas — **hexbin** e **contorno KDE**.
- **Categórico × categórico** (`lc_loans`): **tabela de contingência** (`pivot_table`) de grade do empréstimo contra situação, em contagem e em proporção.
- **Categórico × numérico** (`airline_stats`): **boxplot agrupado** por companhia aérea e **violin plot**, e o que o violin mostra que o boxplot esconde (bimodalidade).
- **Múltiplas variáveis**: `FacetGrid` de hexbins por CEP.

## Regra da semente — primeiro caso real

O código do livro em 1.8 usa `kc_tax0.sample(10000)` para o KDE (a densidade 2-D sobre o dataset inteiro leva minutos). Isso é o **primeiro chunk com gerador aleatório do livro**, e é onde a regra do `CLAUDE.md` deixa de ser teórica:

```python
amostra = kc_tax0.sample(10000, random_state=42)
```

Sem `random_state`, o contorno muda a cada `quarto render`, o `freeze` deixa de ter sentido e cada push acumula um diff de ruído no `gh-pages`.

## Formato dos exercícios

```markdown
## Exercícios

**1.** Enunciado que exige raciocínio ou uma alteração no código da seção.

::: {.callout-tip collapse="true"}
## Resposta
Resposta comentada, com código quando couber.
:::
```

O `collapse="true"` fecha o callout por padrão. É ofuscação honesta: não se apresenta como senha, e o aluno sabe que basta clicar. Não usar `spoiler.html`.

## Custo de render

Medido no container, não estimado: ler `kc_tax.csv.gz` (498.249 linhas) leva **0,1 s**, e `sp500_data.csv.gz` (21 MB) é igualmente rápido. A leitura dos dados **não** é o gargalo.

O custo real está no **KDE 2-D** da seção 1.8: calculá-lo sobre os 432.693 imóveis filtrados levaria minutos, e é exatamente por isso que o livro amostra 10.000 pontos. Com a amostra, o gráfico sai em segundos. O `FacetGrid` de hexbins e o heatmap do S&P 500 também são rápidos.

Conclusão: o acréscimo ao tempo de render é modesto — dezenas de segundos, não minutos. O `freeze` cacheia depois do primeiro render.

## Verificação

Cada seção é verificável isoladamente:

- `make render` conclui sem erro.
- A página HTML da seção existe em `_book/content/cap01/` e contém pelo menos um `<img>` (o gráfico).
- A seção contém `## Exercícios` e ao menos um `callout-tip` com `collapse`.
- Os números da 1.3 permanecem intactos após o retrofit.
- Nenhum chunk com RNG sem `random_state`/semente explícita.

## Fora de escopo

- Capítulos 2, 3 e 4 (permanecem em stub).
- Ilustração do coeficiente de correlação por elipses (o livro a usa só para as figuras em tons de cinza da versão impressa; o site é colorido e o heatmap basta).
- Lista de exercícios consolidada em PDF (o repo de referência tem esse aparato com filtro Lua; aqui não existe e não entra agora).
