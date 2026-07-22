# Catálogo de Distribuições — Seções 2.6 a 2.12

**Data:** 2026-07-22
**Status:** Aprovado

## Objetivo

Escrever as sete seções que fecham o Capítulo 2 — o catálogo das distribuições que aparecem na estatística prática: normal, caudas longas, t de Student, binomial, qui-quadrado, F e Poisson. Diferente do núcleo (2.1–2.5, conceitos), estas são **seções de referência**: cada uma apresenta uma distribuição, sua forma, quando ela surge e o código mínimo para usá-la.

Com isto, o Capítulo 2 fica completo (12/12 seções).

## Decisões (do brainstorming)

- **Peso:** catálogo **compacto**. Cada seção ~70 linhas, com padrão uniforme (o que é → forma → quando aparece → código → 2 exercícios). Não o peso cheio das seções conceituais.
- **2 exercícios por seção** (não 3), condizente com o caráter de referência.
- **QQ-plots com dados:** o `loans_income` para a 2.6. Para a 2.7, **t(3) sintética**, não o S&P 500 (ver abaixo).

## Por que a 2.7 NÃO usa o S&P 500

O plano inicial era usar retornos de uma ação do `sp500_data.csv.gz` para ilustrar caudas gordas. **Medido e descartado:** o arquivo está corrompido para esse fim.

- As colunas são retornos diários, mas **228 de 3.284 (7%) são impossíveis** — valores como +132%, +166%, −101% num único dia.
- Removidos os impossíveis, a curtose do que sobra é **1,1** — praticamente normal. Retornos reais têm curtose 3–10+. Ou seja, mesmo limpo, o dado **não tem cauda gorda** para demonstrar.

(O mesmo arquivo serve à seção 1.7 porque correlação tolera ruído; a lição de cauda gorda, não.)

**No lugar:** uma amostra de uma distribuição **t de Student com 3 graus de liberdade** (`stats.t.rvs(df=3)`), curtose medida **6,8** — o exemplo canônico de cauda gorda. Vantagem dupla: é honesto (ilustra o que é cauda gorda) e **antecipa a 2.8**, que formaliza a própria distribuição t.

## As sete seções

Padrão comum: `callout-note` citando a seção do livro, chunk `setup` oculto, prosa compacta, **um gráfico** da forma (via `scipy.stats`), o código mínimo, e **2 exercícios** com resposta em `::: {.callout-tip collapse="true"}`. Formato brasileiro nos números (`from formato import num`).

### 2.6 — Distribuição Normal

A distribuição de referência: simétrica, definida por média e desvio. A regra 68–95–99,7. E o **QQ-plot** como teste visual de normalidade — pontos sobre a reta = normal; desvios nas pontas = não.

Dado real: QQ-plot do `loans_income` (`scipy.stats.probplot`). A renda tem assimetria **1,05** — o QQ curva para cima na ponta direita, revelando que **renda não é normal**. Lição honesta: a normal é útil, mas muitos dados reais não a seguem.

### 2.7 — Distribuições de Cauda Longa

Cauda mais gorda que a normal: eventos extremos acontecem com mais frequência do que a normal prevê. É por isso que "eventos de 6 sigma" ocorrem em finanças com frequência que a normal chamaria de impossível.

Amostra de `stats.t.rvs(df=3, random_state=42)` — curtose **6,8**. O QQ-plot contra a normal mostra a **curva em S** característica: as pontas se afastam da reta, para cima à direita e para baixo à esquerda, sinal de que os extremos são mais extremos que o normal previa. Remissão à 2.8: essa é a distribuição t, o assunto da próxima seção.

### 2.8 — Distribuição t de Student

Parecida com a normal, porém de caudas mais gordas — e as caudas afinam conforme os **graus de liberdade** crescem, até virar a normal. É a distribuição do erro de estimar a média com amostra pequena.

Números (`stats.t.sf`): a probabilidade de cair além de ±2 desvios —

| Distribuição | P(&#124;X&#124; > 2) |
|---|---|
| t(1) | 0,295 |
| t(5) | 0,102 |
| t(30) | 0,055 |
| Normal | 0,046 |

Com 30 gl a t já é quase a normal. É por isso que, com amostras grandes, usar a normal ou a t dá quase o mesmo — e por que, com amostras pequenas, a t (mais conservadora) é a correta.

### 2.9 — Distribuição Binomial

Contagem de sucessos em *n* tentativas independentes, cada uma com probabilidade *p*. O modelo do teste A/B: quantas conversões em *n* visitantes.

`stats.binom`: com n=5, p=0,1, a probabilidade de **exatamente** 2 sucessos é `pmf(2;5;0,1)` = **0,0729**; a de **até** 2 é `cdf(2;5;0,1)` = **0,9914**. Média = *np*, desvio = √(np(1−p)).

### 2.10 — Distribuição Qui-Quadrado

Soma de normais-padrão ao quadrado; assimétrica à direita, definida pelos graus de liberdade. Sua **média é igual aos graus de liberdade**.

`stats.chi2`: para gl=5, o valor acima do qual fica 5% da distribuição é **11,07** (o valor crítico dos testes). Seção majoritariamente conceitual, como no livro: apresenta a forma e diz que o aluno **reencontrará** o qui-quadrado no Capítulo 3 (testes de aderência e de independência).

### 2.11 — Distribuição F

Razão de duas variâncias. Aparece quando se comparam espalhamentos — o motor da **ANOVA**.

`stats.f`: o valor crítico 5% de F(5, 10) é **3,33**. Também conceitual e ponte para o Capítulo 3 (ANOVA, seção 3.8).

### 2.12 — Distribuição de Poisson e Relacionadas

Poisson: número de eventos raros num intervalo fixo, com taxa média λ. Chegadas a um servidor, ligações num call center, defeitos por lote.

`stats.poisson` (λ=2): P(0 eventos) = **0,135**; P(≥5) = **0,053**. E a **exponencial** como a irmã da Poisson: se os eventos ocorrem a 2 por hora, o **tempo de espera** entre eventos segue uma exponencial de média 30 minutos. (Menção à Weibull como a generalização com taxa variável — uma frase, sem código, como no livro.)

## Regra da semente

Só três chunks sorteiam: a amostra t(3) da 2.7, e eventuais amostras nos QQ-plots. **Todos com semente** (`random_state=42`). O QQ-plot do `loans_income` (2.6) usa o dataset inteiro — não sorteia, não precisa de semente.

## Verificação

- `make render` gera as 42 páginas sem erro.
- As sete seções deixam de ser stub (nenhum "Em construção" em 2.6–2.12).
- Cada uma tem **2 exercícios** (`callout-tip`) e **um gráfico** (`<img>`).
- Os números-chave aparecem: assimetria 1,05 (2.6), curtose 6,8 (2.7), a tabela da t (2.8), `0,0729`/`0,9914` (2.9), `11,07` (2.10), `3,33` (2.11), `0,135` (2.12).
- Nenhum chunk com RNG sem semente (`grep` sobre 2.6–2.12).
- **Capítulo 2 completo:** 12/12 seções sem stub.

## Fora de escopo

- Widgets interativos (o catálogo é de consulta; formas estáticas bastam).
- Retornos financeiros reais brasileiros para a 2.7 (avaliado; a t(3) sintética resolve sem projeto de dados).
- Derivações matemáticas das distribuições (é um catálogo de uso, não um curso de probabilidade).
- Capítulos 3 e 4.
