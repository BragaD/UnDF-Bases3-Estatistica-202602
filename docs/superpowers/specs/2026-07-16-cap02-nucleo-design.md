# Núcleo do Capítulo 2 — Seções 2.1 a 2.5

**Data:** 2026-07-16
**Status:** Aprovado

## Objetivo

Escrever as cinco seções que formam a espinha conceitual do Capítulo 2 (Dados e Distribuições Amostrais): amostragem e viés, viés de seleção, distribuição amostral, bootstrap e intervalos de confiança. As sete seções restantes (2.6–2.12, o catálogo de distribuições) ficam para um segundo ciclo.

Hoje as 12 seções do Capítulo 2 são stubs. Este spec preenche 5.

## Decisões (do brainstorming)

- **Escopo:** 2.1 a 2.5. O catálogo de distribuições (2.6–2.12) é outro ciclo.
- **Dados:** `loans_income.csv`, o mesmo do livro-texto. Foi considerada uma alternativa brasileira (5.571 municípios do IBGE) e **descartada pelo autor** — mantém-se fiel à fonte, sem pipeline novo.
- **Widget interativo na 2.3:** sim. Um slider para o tamanho da amostra *n*, mostrando a distribuição amostral estreitar e o erro padrão cair.

## Os dados

`dados/loans_income.csv` — 50.000 rendas de solicitantes de empréstimo (EUA). Coluna única, `x`.

Seguindo a convenção estabelecida nas seções 1.6–1.8, a coluna é traduzida **na leitura**, sem alterar o CSV:

```python
renda = pd.read_csv("dados/loans_income.csv").rename(columns={"x": "Renda"})["Renda"]
```

Os valores estão em **dólares** (dado americano) — a prosa registra isso, como a 1.8 faz com os pés².

**A população, medida:**

| | Valor |
|---|---|
| Tamanho | 50.000 |
| Média | 68.761 |
| Mediana | 62.000 |
| Desvio-padrão | 32.872 |

A média ser maior que a mediana já conecta com o Capítulo 1: renda é assimétrica à direita. Vale a remissão.

## A regra da semente — este é o capítulo que a cobra

O Capítulo 1 tinha um único chunk com gerador aleatório. Aqui **quase todo chunk sorteia**: amostras, reamostragens bootstrap, permutações. Sem semente explícita, cada `quarto render` publica números diferentes, o `freeze` perde o sentido e o material deixa de bater com o que o aluno vê.

**Todo chunk com RNG usa semente explícita** — `random_state=42`, `np.random.default_rng(42)`, ou um índice determinístico nos laços de reamostragem. A regra já está no `CLAUDE.md`; é aqui que ela paga o que custou.

## As cinco seções

Cada uma segue o padrão do Capítulo 1: `callout-note` citando a seção do livro, chunk `setup` oculto, prosa e código intercalados, callouts `.conceito`/`.exemplo`, tabela-resumo e **3 exercícios** com resposta em `::: {.callout-tip collapse="true"}`.

### 2.1 — Amostragem Aleatória e Viés de Amostra

População versus amostra; por que amostrar (custo, tempo, viabilidade); amostragem aleatória simples, com e sem reposição; **viés de amostra** — quando a amostra difere sistematicamente da população.

O ponto que não pode faltar: **uma amostra grande e enviesada é pior que uma pequena e aleatória**, porque o tamanho dá falsa confiança sem corrigir o viés. É o erro que faz pesquisas eleitorais falharem.

Código: sortear uma amostra de 100 rendas com `random_state=42` e comparar sua média com a da população.

### 2.2 — Viés de Seleção

Viés de seleção; *data snooping* (garimpar os dados até achar algo); o **efeito da busca vasta** — procurar em muitas hipóteses garante achar uma "significativa" por acaso; regressão à média.

Seção majoritariamente conceitual, como no livro. Um chunk pode demonstrar a busca vasta: sortear muitas séries puramente aleatórias e mostrar que a "melhor" delas parece impressionante — com semente fixa.

### 2.3 — Distribuição Amostral de uma Estatística

O coração do capítulo, e o conceito mais difícil: a distinção entre a **distribuição dos dados** e a **distribuição de uma estatística**.

Histogramas comparados: a população (n=1, ou seja, os dados brutos), as médias de amostras de n=5, e as de n=20 — 1.000 amostras cada. A distribuição das médias é mais estreita e mais simétrica que a dos dados, mesmo os dados sendo assimétricos: é o Teorema Central do Limite.

**O erro padrão e a raiz de n.** Os números medidos, que a seção exibe:

| n | Desvio das médias (medido) | σ/√n (teórico) |
|---|---|---|
| 1 | 32.456 | 32.872 |
| 5 | 14.625 | 14.701 |
| 20 | 7.009 | 7.350 |
| 100 | 3.213 | 3.287 |

O acordo entre as duas colunas é o ponto: a fórmula do erro padrão não é um artefato algébrico, é o que de fato acontece quando se amostra. E a consequência prática — para dividir o erro pela metade, é preciso **quadruplicar** a amostra.

**O widget** (ver seção própria, abaixo).

### 2.4 — Bootstrap

Reamostragem **com reposição** a partir da própria amostra, como substituto de repetir a coleta. A ideia central: tratar a amostra como se fosse a população e reamostrá-la.

Distribuição bootstrap da **mediana** (a estatística que não tem fórmula fechada de erro padrão — que é justamente por que o bootstrap importa). Erro padrão bootstrap medido: **235,51**. Viés.

O ponto honesto: o bootstrap não cria informação nova nem conserta uma amostra ruim. Se a amostra é enviesada, o bootstrap reproduz o viés fielmente.

### 2.5 — Intervalos de Confiança

Uma amostra de 20, bootstrap da média, percentis 5 e 95 → intervalo de 90%.

**A interpretação correta**, que é o erro mais comum da estatística aplicada: um IC de 90% **não** significa "90% de chance de o parâmetro estar neste intervalo". Significa que o *procedimento*, repetido muitas vezes, produz intervalos que contêm o parâmetro em 90% das vezes. O parâmetro é fixo; o intervalo é que é aleatório.

Nível de confiança versus largura: mais confiança exige intervalo mais largo. Não há almoço grátis.

## O widget da 2.3

Célula `{ojs}`, no padrão já estabelecido no Capítulo 1 (dados via `ojs_define`, código oculto com `//| echo: false`, sem `format` customizado no `Inputs.range`).

- **Slider:** tamanho da amostra *n*, de 1 a 100.
- **Ao vivo:** histograma das médias de 1.000 amostras de tamanho *n*, com o eixo X **travado** (senão o estreitamento — que é o efeito a mostrar — some no reajuste da escala).
- **Exibido:** o erro padrão medido e o teórico σ/√n, lado a lado, caindo juntos conforme *n* cresce.

**Ponto técnico a verificar na implementação, não a supor:** o widget precisa da população no navegador para reamostrar, e 50.000 números são ~350 KB de JSON na página. Não é proibitivo (o Shinylive recusado eram 46 MB), mas seria o maior ativo isolado do site. **Medir o impacto real na página renderizada.** Se pesar, o widget passa a usar uma subamostra da população, declarada como tal na prosa — decisão tomada com o número na mão.

A amostragem roda em JavaScript (a população vive no navegador). O sorteio do widget não precisa de semente: ele é exploratório e reamostra a cada interação, ao contrário dos chunks Python, cujos números vão impressos na página e **precisam** ser reprodutíveis.

## Verificação

- `make render` gera as 42 páginas sem erro.
- As cinco seções deixam de ser stub (nenhum "Em construção" em 2.1–2.5).
- Cada uma tem 3 exercícios (`callout-tip`).
- **Nenhum chunk com RNG sem semente** — verificação por `grep` sobre `content/cap02/`.
- Os números medidos aparecem nas páginas: o desvio das médias por *n* (2.3) e o erro padrão bootstrap 235,51 (2.4).
- O widget da 2.3 funciona **num navegador de verdade** (teste Playwright, como os do Capítulo 1): o slider existe, é reativo, o eixo X não se move, e o erro padrão exibido cai quando *n* cresce.
- Formato brasileiro em todo número impresso (`from formato import num`).

## Fora de escopo

- Seções 2.6 a 2.12 (o catálogo de distribuições: normal, cauda longa, t, binomial, qui-quadrado, F, Poisson). Próximo ciclo.
- Capítulos 3 e 4.
- Substituir o `loans_income` por dado brasileiro (avaliado e descartado nesta rodada).
