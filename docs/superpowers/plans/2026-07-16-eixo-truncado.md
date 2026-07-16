# Subseção "O eixo que mente" (1.6) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Acrescentar à seção 1.6 uma subseção que mostra o mesmo gráfico de barras com eixo Y truncado e com eixo do zero, discutindo por que o truncamento engana.

**Architecture:** Uma subseção nova em `content/cap01/06-dados-binarios-categoricos.qmd`, com um chunk Python que desenha os dois painéis lado a lado (matplotlib), prosa de discussão, um callout `.conceito`, e um 4º exercício. Uma única task — é uma adição aditiva a um arquivo.

**Tech Stack:** Quarto (engine jupyter) · pandas · matplotlib

**Spec:** `docs/superpowers/specs/2026-07-16-eixo-truncado-design.md`

## Global Constraints

- **Formato brasileiro** nos números impressos: `from formato import num` (já está no chunk `setup` da seção). Nunca `f"{x:,.1f}"`.
- **Caminho dos dados relativo à raiz:** `pd.read_csv("dados/estados.csv")`. Nunca `../../dados/`.
- **Português brasileiro**; variável do DataFrame `estado`.
- **Render sempre via container:** `make render`. Não há Quarto/Python confiáveis no host.
- **A subseção é aditiva:** os números que a 1.6 já imprime (proporções de atraso, `R$ 104,55`) **não podem mudar**.
- **Não crie `AGENTS.md`.** Não mexa em `_quarto.yml`, `pyproject.toml`, `uv.lock`, `formato.py`, `dados/`, nem em outras seções.

## Os números (calculados no container, sobre os dados reais)

Os 9 estados do Nordeste, taxa de homicídios (Atlas 2024), ordenados:

`PI 20,47 · SE 22,87 · RN 23,13 · PB 25,45 · MA 30,81 · BA 33,14 · CE 34,14 · AL 35,65 · PE 36,78`

- Razão **real** PE/PI: `36,78 / 20,47` = **1,8×**
- Razão **visual** com eixo em 20: `(36,78 − 20) / (20,47 − 20)` = `16,78 / 0,47` = **≈36×**

---

## Task 1: A subseção do eixo truncado

**Files:**
- Modify: `content/cap01/06-dados-binarios-categoricos.qmd`

**Interfaces:**
- Consumes: `dados/estados.csv` (colunas `Estado`, `Populacao`, `Taxa.Homicidios`, `Sigla`). O chunk `setup` da seção **não** carrega esse arquivo (a seção usa `dfw`), então o chunk novo o carrega.

- [ ] **Step 1: Inserir a subseção**

Insira **entre** o fim de `## Gráfico de barras não é histograma` (logo após o callout `.conceito` que termina com "…perguntas de ordem.") e o início de `## A moda: a única "localização" possível`.

O conteúdo abaixo é exato. A prosa é sua a partir do esqueleto, na voz da seção (direta, com opinião didática); o **código do chunk é literal**.

````markdown
## O eixo que mente

Um gráfico de barras honesto sobre a mecânica — barras separadas, eixo categórico — ainda pode enganar de outra forma, e essa é uma das mais comuns em jornais e apresentações. O truque não está nos dados; está no eixo.

Abaixo, a taxa de homicídios dos nove estados do Nordeste (Atlas da Violência, 2024), desenhada de dois jeitos. Os números são **exatamente os mesmos** nos dois painéis. Só muda onde o eixo Y começa.

```{python}
#| label: fig-eixo-truncado
#| fig-cap: "A MESMA taxa de homicídios dos nove estados do Nordeste, desenhada de dois jeitos. À esquerda, o eixo começa em 20; à direita, no zero."
estado = pd.read_csv("dados/estados.csv")
nordeste = ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"]
ne = estado[estado["Sigla"].isin(nordeste)].sort_values("Taxa.Homicidios")

fig, (ax_trunc, ax_zero) = plt.subplots(1, 2, figsize=(10, 4))

for ax, base, titulo in [
    (ax_trunc, 20, "Eixo começando em 20 — enganoso"),
    (ax_zero, 0, "Eixo começando em 0 — honesto"),
]:
    ax.bar(ne["Sigla"], ne["Taxa.Homicidios"], color="#b0c4d8", edgecolor="white")
    ax.set_ylim(base, 38)
    ax.set_title(titulo, fontsize=10)
    ax.set_xlabel("Estado")

ax_trunc.set_ylabel("Taxa de homicídios (por 100 mil)")
plt.tight_layout()
plt.show()
```

[PROSA DA DISCUSSÃO — cobrir estes pontos:]

- No painel da esquerda, o Piauí (a menor taxa, 20,47) vira um fiapo e Pernambuco (36,78) parece esmagador. O olho lê Pernambuco como **cerca de 36 vezes** o Piauí.
- Mas essa razão é a das **alturas desenhadas**: `(36,78 − 20) / (20,47 − 20)`, que dá ≈36. A razão **real** entre as taxas é `36,78 / 20,47` = **1,8×**. Pernambuco tem uma taxa 80% maior que a do Piauí — não 36 vezes.
- Por que a barra engana: num gráfico de barras, o olho lê a quantidade pelo **comprimento** da barra, e comprimento só significa algo medido **a partir do zero**. Cortar o eixo em 20 quebra essa codificação.
- O que torna o truque insidioso: **todos os nove números são verdadeiros.** Não há dado falso nem erro de conta — só um eixo que começa em 20. É como se enganam pessoas com uma base de dados honesta.
- O painel da direita mostra a imagem real: todas as barras são altas (todos os nove estados têm taxa acima de 20 por 100 mil — o Nordeste inteiro é uma região de violência letal alta), e as diferenças entre elas aparecem na proporção verdadeira, modesta.

::: {.conceito}
**Regra prática:** um gráfico de barras começa no eixo zero, sempre. A barra codifica a magnitude pelo seu comprimento, e comprimento medido a partir de um ponto qualquer não é magnitude nenhuma. (A regra é específica de barras: um gráfico de **linha**, mostrando evolução no tempo, às vezes pode truncar o eixo — ali a informação está na **inclinação** da linha, não no comprimento de uma barra.)
:::
````

**Cuidado com a cerca de código:** o bloco de exemplo acima usa cercas de 4 crases (````` ```` `````) por fora porque contém um chunk de 3 crases dentro. No arquivo final, o que entra é: o cabeçalho `## O eixo que mente`, a prosa introdutória, o chunk `fig-eixo-truncado`, a prosa da discussão (os bullets viram parágrafos corridos), e o callout `.conceito` — nessa ordem.

- [ ] **Step 2: Acrescentar o 4º exercício**

A seção 1.6 tem três exercícios. Acrescente um quarto, no mesmo formato (resposta em `::: {.callout-tip collapse="true"}`), ao fim da lista:

````markdown
**4.** Um jornal publica as taxas de homicídio de Pernambuco (36,78) e Piauí (20,47) num gráfico de barras com o eixo Y começando em 20. Quantas vezes maior a barra de Pernambuco *parece*? E qual é a razão *real* entre as duas taxas?

::: {.callout-tip collapse="true"}
## Resposta

A barra de Pernambuco *parece* cerca de **36 vezes** a do Piauí: a altura desenhada de cada uma é o valor menos o piso do eixo, então a razão visual é `(36,78 − 20) / (20,47 − 20) = 16,78 / 0,47 ≈ 36`.

A razão **real** é `36,78 / 20,47 ≈ 1,8` — Pernambuco tem uma taxa 80% maior, não 36 vezes maior. O eixo truncado transformou uma diferença de 80% num abismo aparente de 36 para 1. É por isso que um gráfico de barras deve começar no zero: só assim o comprimento da barra corresponde ao valor.
:::
````

- [ ] **Step 3: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap01/06-dados-binarios-categoricos.html
grep -c '<img' "$H"
grep -c 'callout-tip' "$H"
grep -c 'O eixo que mente' "$H"
```
Expected: `<img>` = **2** (o gráfico de barras original + o novo painel duplo); `callout-tip` = **4** (os 3 exercícios + o novo); `O eixo que mente` ≥ 1.

- [ ] **Step 4: Conferir que os números antigos NÃO mudaram e que os novos estão certos**

Run:
```bash
H=_book/content/cap01/06-dados-binarios-categoricos.html
grep -oE '42,43|R\$ 104,55' "$H" | sort -u | tr '\n' ' '; echo
grep -oE '36 vezes|1,8|16,78|0,47' "$H" | sort -u | tr '\n' ' '; echo
```
Expected: `42,43` e `R$ 104,55` (os números antigos da seção, **intactos**); e os números da distorção (`36 vezes`, `1,8`, `16,78`, `0,47`) presentes na prosa/exercício.

**Se `42,43` ou `R$ 104,55` sumirem, a subseção nova mexeu no que não devia — PARE.**

- [ ] **Step 5: Conferir visualmente o gráfico (o eixo truncado precisa REALMENTE começar em 20)**

O ponto da subseção é o eixo. Confirme que o painel esquerdo começa em 20 e o direito em 0, rodando o mesmo cálculo que o chunk faz:

```bash
docker compose run --rm --no-deps livro python -c "
import pandas as pd
e = pd.read_csv('dados/estados.csv')
ne = e[e['Sigla'].isin(['MA','PI','CE','RN','PB','PE','AL','SE','BA'])]
print('menor taxa (PI):', ne['Taxa.Homicidios'].min())
print('maior taxa (PE):', ne['Taxa.Homicidios'].max())
print('9 estados?', len(ne) == 9)
"
```
Expected:
```
menor taxa (PI): 20.47
maior taxa (PE): 36.78
9 estados? True
```

Se a menor taxa não for 20,47, o filtro do Nordeste está errado e o eixo em 20 não produziria o "fiapo" esperado.

- [ ] **Step 6: Commit**

```bash
git add content/cap01/06-dados-binarios-categoricos.qmd
git commit -m "feat: subsecao do eixo Y truncado na secao 1.6"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean && make render
find _book/content -name '*.html' | wc -l
```
Expected: `42`, sem erro.

- [ ] **A subseção existe, com os dois gráficos e o exercício**

```bash
H=_book/content/cap01/06-dados-binarios-categoricos.html
grep -c 'O eixo que mente' "$H"
grep -c '<img' "$H"
grep -c 'callout-tip' "$H"
```
Expected: `O eixo que mente` ≥ 1; `<img>` = 2; `callout-tip` = 4.

- [ ] **Os números antigos da 1.6 sobreviveram**

```bash
grep -oE '23,02|30,40|42,43|R\$ 104,55' _book/content/cap01/06-dados-binarios-categoricos.html | sort -u
```
Expected: os quatro — a subseção nova não pode ter tocado no que já existia.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
