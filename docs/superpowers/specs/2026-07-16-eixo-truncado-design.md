# Eixo Y Truncado — Subseção "O eixo que mente" (1.6)

**Data:** 2026-07-16
**Status:** Aprovado

## Objetivo

Acrescentar à seção 1.6 uma subseção sobre o gráfico de barras enganoso: o mesmo dado desenhado com o eixo Y truncado (começando acima de zero) e com o eixo do zero, mostrando como o truncamento distorce a leitura. Um exemplo clássico de "como mentir com estatística" usando dados 100% verdadeiros — só o eixo mente.

## Decisões (do brainstorming)

- **Onde:** nova subseção na 1.6, logo após "Gráfico de barras não é histograma". A 1.6 já é a seção do gráfico de barras.
- **Dados:** os 9 estados do **Nordeste**, taxa de homicídios (Atlas 2024), de `dados/estados.csv`. O Nordeste foi escolhido em vez do Sudeste porque suas taxas são **altas e próximas entre si** (razão real de só 1,8×) — é o caso em que o truncamento mais engana. No Sudeste, ES é 4× SP, uma diferença real já grande, o que enfraqueceria o contraste.
- **Exercício:** acrescentar um 4º exercício à seção, sobre o eixo truncado.

## Os dados (Nordeste, Atlas 2024)

Ordenados por taxa:

| Estado | Sigla | Taxa |
|---|---|---|
| Piauí | PI | 20,47 |
| Sergipe | SE | 22,87 |
| Rio Grande do Norte | RN | 23,13 |
| Paraíba | PB | 25,45 |
| Maranhão | MA | 30,81 |
| Bahia | BA | 33,14 |
| Ceará | CE | 34,14 |
| Alagoas | AL | 35,65 |
| Pernambuco | PE | 36,78 |

Filtro: `estado["Sigla"].isin(["MA","PI","CE","RN","PB","PE","AL","SE","BA"])`.

## A distorção (números calculados no container)

| | Eixo truncado (começa em 20) | Realidade (eixo em 0) |
|---|---|---|
| PE parece vs PI | **~36×** maior (16,78 ÷ 0,47) | é **1,8×** maior (36,78 ÷ 20,47) |
| PI (o menor) | um fiapo — barra de altura 0,47 | 20,47 — uma taxa altíssima, longe de zero |

O contraste **36× contra 1,8×** é o coração da lição.

## Os dois gráficos

Lado a lado, num único `plt.subplots(1, 2)`, os mesmos 9 estados ordenados:

- **Esquerda — eixo truncado.** `ax.set_ylim(20, ...)`. Título deixa claro que é o "truncado". PI vira um fiapo; PE parece esmagador; o gradiente entre os estados parece enorme.
- **Direita — eixo do zero.** `ax.set_ylim(0, ...)`. A imagem honesta: todas as barras são visivelmente altas (todas acima de 20 por 100 mil), e as diferenças entre elas aparecem na proporção real — modestas.

Barras na cor do livro (`#b0c4d8`). Rótulos das UFs no eixo x. Título de cada painel indicando qual é qual.

## A discussão (por que engana)

O ponto técnico, preciso: num gráfico de **barras**, o olho lê a quantidade pelo **comprimento** da barra — e comprimento só tem significado medido **a partir do zero**. Truncar o eixo quebra essa codificação: o olho passa a ver a razão entre as **alturas desenhadas** (36×), não entre os **valores reais** (1,8×).

O que torna o truque insidioso: **todos os nove números são verdadeiros.** Não há dado falso, não há erro de cálculo — apenas um eixo que começa em 20 em vez de 0. É uma das formas mais comuns de enganar com uma base de dados honesta.

O alerta de uso honesto, para o aluno não sair achando que todo eixo truncado é fraude: a regra é específica de **barras**. Um gráfico de **linha** (evolução no tempo) às vezes *pode* truncar, porque ali o que carrega a informação é a **inclinação** da linha, não o comprimento de uma barra a partir do zero. Barras codificam magnitude por comprimento; por isso **começam no zero, sempre**.

Um callout `.conceito` fixa a regra: *gráfico de barras começa no zero.*

## O exercício (4º da seção)

No formato dos existentes (resposta em `::: {.callout-tip collapse="true"}`):

> Um jornal publica as taxas de homicídio de Pernambuco (36,78) e Piauí (20,47) num gráfico de barras com o eixo começando em 20. Quantas vezes maior a barra de Pernambuco *parece*? E qual é a razão *real* entre as duas taxas?

Resposta: a barra de PE parece **≈36×** a de PI — a altura desenhada é `(36,78 − 20) / (20,47 − 20) = 16,78 / 0,47 ≈ 36`. A razão real é `36,78 / 20,47 ≈ 1,8×`. O eixo truncado transformou uma diferença de 80% num abismo aparente de 36 para 1.

## Verificação

- `make render` gera as 42 páginas sem erro.
- A subseção tem os **dois** gráficos (o painel duplo conta como um `<img>`, mas são dois eixos).
- A seção passa a ter **4** exercícios (`callout-tip`).
- Os números da seção 1.6 que já existiam (proporções de atraso, `R$ 104,55`) **não mudam** — a subseção nova é aditiva.
- Formato brasileiro nos números (`from formato import num`, já no chunk setup).

## Fora de escopo

- Interatividade (um slider que move o piso do eixo). A comparação estática dos dois painéis já entrega a lição; um widget aqui é YAGNI.
- Outros tipos de gráfico enganoso (escala log sem aviso, eixo duplo). Fica para quem quiser puxar o fio.
