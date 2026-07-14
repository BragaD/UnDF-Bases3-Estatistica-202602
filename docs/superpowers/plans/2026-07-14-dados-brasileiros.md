# Dados Brasileiros no Lugar dos Americanos — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Substituir os 50 estados americanos pelas 27 unidades federativas brasileiras (população IBGE 2024 + taxa de homicídios do Atlas da Violência 2024), e adaptar as 5 seções do Capítulo 1 que usam esses dados.

**Architecture:** Um pipeline one-off (`scripts/gerar-dados-brasil.py`) junta três fontes e gera `dados/estados.csv`, que é commitado. O pipeline **não** é um chunk do livro. As seções passam a ler o CSV brasileiro, com colunas em português.

**Tech Stack:** Python (pandas, requests/urllib) · APIs do IBGE (SIDRA + localidades) · CSV do Atlas da Violência

**Spec:** `docs/superpowers/specs/2026-07-14-dados-brasileiros-design.md`

## Global Constraints

- **Formato brasileiro em todo número impresso.** Use `from formato import num` nos chunks Python (`num(x, casas=1)` → `7.873.472,2`) e `toLocaleString("pt-BR", ...)` no OJS. Nunca `f"{x:,.1f}"`.
- **Colunas do novo CSV, em português:** `Estado`, `Populacao`, `Taxa.Homicidios`, `Sigla`. (A regra antiga de "preservar os nomes originais" valia para os CSVs do livro-texto; este dado é nosso.)
- **Caminho dos dados relativo à raiz:** `pd.read_csv("dados/estados.csv")`. Nunca `../../dados/`. Garantido por `project: execute-dir: project`.
- **Variáveis dos chunks em português.** A variável do DataFrame continua `estado`.
- **Render sempre via container:** `make render`. Não há Quarto/Python confiáveis no host.
- **Semente obrigatória** em todo chunk com RNG (`random_state=42`). Nenhuma das seções desta tarefa tem RNG, mas a regra vale.
- **O código OJS fica oculto** (`//| echo: false`) e nunca redefine um nome já definido (OJS quebra a página inteira com "duplicate definition", e o `quarto render` passa sem erro).
- **Não crie `AGENTS.md`.** Não mexa em `_quarto.yml`, `pyproject.toml`, `uv.lock`, `formato.py`.

## Os números (todos calculados no container, sobre os dados reais — não são estimativas)

**Estrutura:** n = 27 · `shape` = `(27, 4)` · `Sigla` tem 27 categorias · `.loc["SP"]` → São Paulo, 45973194, 6.16

**Seção 1.3:**

| | Valor |
|---|---|
| Média (população) | `7.873.472,2` |
| Média aparada 10% | `6.250.792,8` |
| Mediana | `4.145.040,0` — **a população real da Paraíba** |
| Média simples da taxa | `22,7389` |
| Média ponderada da taxa | `18,7907` — **MENOR** que a simples |
| Mediana ponderada | `16,4608` |
| Média ÷ mediana | 1,90 → a média é **90%** maior (nos EUA: 39%) |
| São Paulo ÷ Roraima | **64,1×** (nos EUA, CA÷WY = 66×) |
| k do aparo de 10% | `int(27 × 0,1)` = **2** de cada ponta (nos EUA: 5) |

**Seção 1.4:** desvio-padrão `9.256.155,8` · IQR `6.443.986,0` · MAD `4.752.396,9` · razão sd/MAD = **1,95** (nos EUA: 1,78)

**Seção 1.5:** quantis da `Taxa.Homicidios` — 5% `8,238` · 25% `16,165` · 50% `23,130` · 75% `30,295` · 95% `35,197`. Outliers do boxplot da população: **apenas MG e SP** (nos EUA eram 4: CA, TX, NY, FL). A primeira faixa do `pd.cut(..., 10)` contém **15 dos 27** estados.

---

## Estrutura de Arquivos

| Arquivo | Task | O que acontece |
|---|---|---|
| `dados/brutos/atlas-violencia-taxa-homicidios.csv` | 1 | criado (o CSV que o autor baixou; versionado para o pipeline ser reproduzível) |
| `scripts/gerar-dados-brasil.py` | 1 | criado (one-off, fora do livro) |
| `dados/estados.csv` | 1 | gerado e commitado |
| `dados/README.md` | 1 | documenta a nova fonte |
| `content/cap01/03-estimativas-localizacao.qmd` | 2 | chunks, prosa, exercícios, **e os dois widgets** |
| `scripts/verifica-widgets.py` | 2 | valores esperados brasileiros |
| `content/cap01/01-dados-estruturados.qmd` | 3 | chunks e prosa |
| `content/cap01/02-dados-retangulares.qmd` | 3 | chunks e prosa |
| `content/cap01/04-estimativas-variabilidade.qmd` | 4 | chunks e prosa |
| `content/cap01/05-distribuicao-dados.qmd` | 4 | chunks e prosa |
| `dados/state.csv` | 5 | **removido** |
| `CLAUDE.md` | 5 | documenta o dado brasileiro e o pipeline |

**Ordem deliberada:** o `state.csv` só é removido na Task 5. Até lá ele permanece, para que o livro renderize ao fim de **cada** task — se ele saísse na Task 1, as seções ainda não migradas quebrariam e nenhuma task intermediária seria verificável.

---

## Task 1: Pipeline e dados

**Files:**
- Create: `dados/brutos/atlas-violencia-taxa-homicidios.csv`
- Create: `scripts/gerar-dados-brasil.py`
- Create: `dados/estados.csv` (gerado pelo script)
- Modify: `dados/README.md`

**Interfaces:**
- Produces: `dados/estados.csv` com as colunas `Estado`, `Populacao`, `Taxa.Homicidios`, `Sigla` — consumido por todas as tasks seguintes.

- [ ] **Step 1: Versionar o CSV bruto do Atlas**

O autor baixou o arquivo do site do Atlas. A API antiga (`/atlasviolencia/api/v1/...`) foi ao ar abaixo na reformulação (v3) e hoje devolve HTML — **não há endpoint público funcionando**. Sem versionar o bruto, o pipeline deixa de ser reproduzível e ninguém consegue auditar de onde vieram os números do livro.

```bash
mkdir -p dados/brutos
cp "/Users/douglasbraga/.claude/uploads/9ace8a8a-7201-45bb-961e-0f655337a6cf/588ebdd9-Taxa_de_homic_dios_registrados_estados.csv" \
   dados/brutos/atlas-violencia-taxa-homicidios.csv
head -2 dados/brutos/atlas-violencia-taxa-homicidios.csv
wc -l dados/brutos/atlas-violencia-taxa-homicidios.csv
```
Expected:
```
Período,Região ID,Valor
2000-01-15T00:00:00.000Z,21,5.94
     675 dados/brutos/atlas-violencia-taxa-homicidios.csv
```
São 27 UFs × 25 anos (2000–2024). O livro usa só 2024.

- [ ] **Step 2: Escrever o pipeline**

Ele **valida e falha alto**: se as três fontes não casarem exatamente nas mesmas 27 UFs, levanta erro em vez de produzir um CSV com buraco. Um estado faltante viraria um `NaN` silencioso no meio de uma estatística do livro.

```python
#!/usr/bin/env python3
"""Gera dados/estados.csv a partir de três fontes públicas.

RODA UMA ÚNICA VEZ. Não é um chunk do livro: o aluno não precisa ver a mecânica
de juntar três fontes para aprender o que é uma mediana, e um livro que faz duas
chamadas de rede a cada render é frágil e lento.

Fontes:
  - Taxa de homicídios 2024 — Atlas da Violência (Ipea/FBSP).
    O CSV bruto está versionado em dados/brutos/ porque a API do Atlas saiu do ar
    na reformulação do site (v3): /atlasviolencia/api/v1/... hoje devolve HTML.
  - População 2024 — IBGE, SIDRA tabela 6579, variável 9324.
  - Nome e sigla — IBGE, API de localidades.

Uso:  docker compose run --rm --no-deps livro python scripts/gerar-dados-brasil.py
"""
import csv
import json
import urllib.request
from pathlib import Path

ANO = 2024
BRUTO = Path("dados/brutos/atlas-violencia-taxa-homicidios.csv")
SAIDA = Path("dados/estados.csv")

URL_POP = f"https://apisidra.ibge.gov.br/values/t/6579/n3/all/v/9324/p/{ANO}"
URL_UFS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"


def baixar_json(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)


def ler_taxas():
    """{codigo_ibge: taxa} para o ano alvo, do CSV do Atlas."""
    with BRUTO.open(encoding="utf-8-sig") as f:
        return {
            int(linha["Região ID"]): float(linha["Valor"])
            for linha in csv.DictReader(f)
            if linha["Período"].startswith(str(ANO))
        }


def ler_populacao():
    """{codigo_ibge: habitantes}. A primeira linha do SIDRA é cabeçalho."""
    return {int(r["D1C"]): int(r["V"]) for r in baixar_json(URL_POP)[1:]}


def ler_ufs():
    """{codigo_ibge: (nome, sigla)}."""
    return {uf["id"]: (uf["nome"], uf["sigla"]) for uf in baixar_json(URL_UFS)}


def main():
    taxas, populacao, ufs = ler_taxas(), ler_populacao(), ler_ufs()

    # Falhar alto, não silenciosamente: um estado faltante viraria um NaN no meio
    # de uma estatística do livro, e ninguém perceberia.
    if not (set(taxas) == set(populacao) == set(ufs)):
        raise SystemExit(
            "As três fontes não casam.\n"
            f"  taxas    : {len(taxas)} UFs\n"
            f"  população: {len(populacao)} UFs\n"
            f"  ufs      : {len(ufs)} UFs\n"
            f"  só nas taxas    : {sorted(set(taxas) - set(populacao) - set(ufs))}\n"
            f"  só na população : {sorted(set(populacao) - set(taxas))}\n"
            f"  só nas ufs      : {sorted(set(ufs) - set(taxas))}"
        )
    if len(ufs) != 27:
        raise SystemExit(f"Esperava 27 unidades federativas, encontrei {len(ufs)}.")

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, ["Estado", "Populacao", "Taxa.Homicidios", "Sigla"],
            quoting=csv.QUOTE_NONNUMERIC,
        )
        w.writeheader()
        for codigo in sorted(ufs):
            nome, sigla = ufs[codigo]
            w.writerow({
                "Estado": nome,
                "Populacao": populacao[codigo],
                "Taxa.Homicidios": taxas[codigo],
                "Sigla": sigla,
            })

    print(f"{SAIDA}: {len(ufs)} unidades federativas, ano {ANO}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Rodar o pipeline**

Run: `docker compose run --rm --no-deps livro python scripts/gerar-dados-brasil.py`
Expected: `dados/estados.csv: 27 unidades federativas, ano 2024`

- [ ] **Step 4: Conferir o CSV gerado**

Run:
```bash
head -3 dados/estados.csv
docker compose run --rm --no-deps livro python -c "
import pandas as pd
e = pd.read_csv('dados/estados.csv')
print('shape :', e.shape)
print('cols  :', list(e.columns))
sp = e.loc[e.Sigla == 'SP'].iloc[0]
print('SP    :', sp.Estado, int(sp.Populacao), sp['Taxa.Homicidios'])
print('menor :', e.loc[e.Populacao.idxmin(), 'Sigla'], int(e.Populacao.min()))
print('mediana da população:', int(e.Populacao.median()),
      '->', e.loc[e.Populacao == e.Populacao.median(), 'Estado'].iloc[0])
"
```
Expected:
```
"Estado","Populacao","Taxa.Homicidios","Sigla"
"Rondônia",1746227,29.78,"RO"
"Acre",880631,19.65,"AC"
shape : (27, 4)
cols  : ['Estado', 'Populacao', 'Taxa.Homicidios', 'Sigla']
SP    : São Paulo 45973194 6.16
menor : RR 716793
mediana da população: 4145040 -> Paraíba
```

**Se a mediana não for a população da Paraíba, PARE.** Todo o gancho didático da seção 1.3 depende disso.

- [ ] **Step 5: Documentar a fonte em `dados/README.md`**

Acrescente uma seção no topo (o README hoje só descreve os CSVs do livro-texto):

````markdown
## `estados.csv` — dado brasileiro (gerado por nós)

27 unidades federativas, com população e taxa de homicídios de **2024**.

| Coluna | Fonte |
|---|---|
| `Estado`, `Sigla` | IBGE — [API de localidades](https://servicodados.ibge.gov.br/api/v1/localidades/estados) |
| `Populacao` | IBGE — SIDRA, tabela 6579, variável 9324, ano 2024 |
| `Taxa.Homicidios` | Atlas da Violência (Ipea/FBSP), 2024 — por 100 mil habitantes |

Gerado por `scripts/gerar-dados-brasil.py`, que roda **uma única vez**:

```bash
docker compose run --rm --no-deps livro python scripts/gerar-dados-brasil.py
```

O CSV bruto do Atlas está versionado em `dados/brutos/`. A API do Atlas
(`/atlasviolencia/api/v1/...`) saiu do ar na reformulação do site (v3) e hoje
devolve HTML — sem o arquivo bruto, o pipeline não seria reproduzível.
````

- [ ] **Step 6: Commit**

O `state.csv` **permanece** por enquanto — as seções ainda o usam, e o livro precisa continuar renderizando ao fim de cada task. Ele sai na Task 5.

```bash
git add dados/brutos/ dados/estados.csv dados/README.md scripts/gerar-dados-brasil.py
git commit -m "data: 27 UFs com populacao IBGE e taxa de homicidios do Atlas (2024)"
```

---

## Task 2: Seção 1.3 — a seção-modelo

A maior task do plano, e a única com mudanças de **conteúdo**, não só de números. Ela inclui os dois widgets OJS, que vivem no mesmo arquivo: separá-los deixaria o widget lendo colunas que não existem mais, e uma célula `{ojs}` quebrada **renderiza sem erro**.

**Files:**
- Modify: `content/cap01/03-estimativas-localizacao.qmd`
- Modify: `scripts/verifica-widgets.py`

**Interfaces:**
- Consumes: `dados/estados.csv` (Task 1).
- Produces: o padrão de prosa e de chunk que as Tasks 3 e 4 replicam.

- [ ] **Step 1: Trocar a fonte de dados e os nomes de coluna nos chunks**

`estado["Population"]` → `estado["Populacao"]`; `estado["Murder.Rate"]` → `estado["Taxa.Homicidios"]`; `pd.read_csv("dados/state.csv")` → `pd.read_csv("dados/estados.csv")`.

O chunk que carrega os dados (o que também alimenta os widgets via `ojs_define`):

```python
#| label: carrega
estado = pd.read_csv("dados/estados.csv")
ojs_define(dados = estado)
estado.head()
```

- [ ] **Step 2: Reescrever a lição da mediana — n agora é ÍMPAR**

Este é o parágrafo que **deixou de ser verdadeiro**. Hoje ele diz:

> "Com número par de observações — como aqui, n = 50 —, não existe um único valor central: a mediana é a **média dos dois valores do meio**. É por isso que o número calculado abaixo termina em `,5`: não há meia pessoa, há uma média entre duas observações vizinhas."

Com 27 unidades federativas isso é falso. Reescreva para dar a **definição completa**, e use o presente que os dados trouxeram:

- Com **n ímpar** (como aqui, 27), a mediana é o valor que fica exatamente no meio da fila ordenada — o 14º. Ela **é uma observação de verdade**.
- Com **n par**, não há um único valor central: a mediana é a média dos dois do meio (e por isso pode terminar em meio).
- E o gancho: a mediana da população brasileira, **4.145.040**, é exatamente a população da **Paraíba**. A mediana não é um número que a conta inventou — é o estado que ficou no meio da fila.

Chunk esperado:

```python
#| label: mediana
mediana = estado["Populacao"].median()
print(f"Mediana: {num(mediana)}")

# Qual estado é a mediana? Com n ímpar, ela é uma observação de verdade.
estado_mediano = estado.loc[estado["Populacao"] == mediana, "Estado"].iloc[0]
print(f"É a população de: {estado_mediano}")
```
Saída real: `Mediana: 4.145.040,0` e `É a população de: Paraíba`

- [ ] **Step 3: Inverter a conclusão da média ponderada**

A prosa atual afirma:

> "Ponderar pela população **aumenta** a estimativa, então os estados mais populosos tendem a ter taxas de homicídio mais altas."

Nos dados brasileiros isso é **falso**, e o motivo é interessante:

| | Valor |
|---|---|
| Média simples da taxa | `22,7389` |
| Média ponderada | `18,7907` |

A ponderada é **menor**. **São Paulo tem a maior população do país (45.973.194) e a menor taxa de homicídios (6,16)** — sozinho, ele puxa a ponderada para baixo. A violência letal no Brasil se concentra nos estados **menos** populosos, no Norte e Nordeste.

A prosa deve dizer isso, e fazer o ponto maior: a **direção** do efeito é um fato empírico sobre o país, não uma lei da estatística. A média ponderada responde "qual taxa o brasileiro médio enfrenta" (18,79); a simples responde "qual a taxa do estado médio" (22,74). São perguntas diferentes, e no Brasil elas divergem no sentido oposto ao dos EUA.

Chunk:

```python
#| label: ponderadas
media_pond = np.average(estado["Taxa.Homicidios"], weights=estado["Populacao"])
mediana_pond = wquantiles.median(estado["Taxa.Homicidios"], weights=estado["Populacao"])

print(f"Média simples     : {num(estado['Taxa.Homicidios'].mean(), 4)}")
print(f"Média ponderada   : {num(media_pond, 4)}")
print(f"Mediana ponderada : {num(mediana_pond, 4)}")
```
Saídas reais: `22,7389` · `18,7907` · `16,4608`

- [ ] **Step 4: Atualizar os demais números e o exemplo do outlier**

- O aparo de 10% agora corta **2** de cada ponta (`int(27 × 0,1)` = 2), não 5. A prosa diz "os 5 mais populosos e os 5 menos"; passa a ser **2 e 2**.
- A média é **90%** maior que a mediana (nos EUA era 39%) — a distribuição brasileira é bem mais assimétrica. O callout `.exemplo` deve usar o número novo.
- O exemplo do fator: **São Paulo (45.973.194) e Roraima (716.793) diferem por 64×**. (O texto atual fala de Califórnia e Wyoming, 66×.)
- Saídas reais dos chunks: `Média: 7.873.472,2` · `Média aparada (10%): 6.250.792,8` · `Mediana: 4.145.040,0`
- A tabela-resumo e o gráfico `fig-localizacao` usam os valores novos; no gráfico, o eixo continua em milhões.

- [ ] **Step 5: Adaptar os widgets — São Paulo no lugar da Califórnia**

Os widgets leem os dados pelo `ojs_define`, então acompanham a troca — mas o **filtro do estado e o valor do slider** precisam mudar. A coluna também: `d.State` → `d.Sigla`, `d.Population` → `d.Populacao`.

```javascript
//| echo: false
// Sem `format` customizado, de propósito: o Inputs.range renderiza uma caixa
// <input type="number"> ao lado do slider, e ela rejeita qualquer string não
// numérica — um format que devolvesse "46,0 M" deixaria a caixa VAZIA.
//
// O slider está em habitantes, não em milhões, para que o valor inicial seja
// exatamente 45.973.194 — a população real de São Paulo. Em milhões, o Observable
// arredondaria o valor inicial para o step, e a média do widget deixaria de bater
// com a que o chunk Python imprime acima nesta mesma página.
viewof pop_sp = Inputs.range([1_000_000, 300_000_000], {
  step: 1,
  value: 45973194,
  label: "População de São Paulo (habitantes):"
})
```

```javascript
//| echo: false
md`São Paulo: **${fmt(pop_sp)}** habitantes — ${fmt(pop_sp / 1e6)} milhões.
${pop_sp === 45973194 ? "É o valor real." : "O valor real é 45.973.194."}`
```

```javascript
//| echo: false
popsA = estados.map(d => d.Sigla === "SP" ? pop_sp : d.Populacao)
```

E no Widget B: `popsB = estados.map(d => d.Populacao)`.

**Atenção:** `estados`, `fmt` e `mediaAparada` já estão definidos e **não podem ser redefinidos** — em OJS, redeclarar um nome quebra a página inteira, e o `quarto render` passa sem erro. A variável `pop_ca` some; entra `pop_sp`.

A prosa dos widgets troca "Califórnia" por "São Paulo".

- [ ] **Step 6: Atualizar os exercícios**

- **Exercício 1** (aparo de 25%): a resposta menciona os 5 estados de cada ponta; passa a ser **2**. O resto da resposta (a convergência para a mediana) continua válido.
- **Exercício 2** — este **inverte**. Hoje pergunta por que a ponderada (4,45) é *maior* que a simples (4,07) e responde "os estados mais populosos têm taxas mais altas". Agora a ponderada (`18,79`) é **menor** que a simples (`22,74`), e a resposta é o oposto: os estados mais populosos têm taxas **mais baixas** — São Paulo, o maior de todos, tem a menor taxa do país. Reescreva enunciado e resposta.
- **Exercício 3** (renda média × mediana) não usa os dados; **não mexa nele**.

- [ ] **Step 7: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap01/03-estimativas-localizacao.html
grep -oE 'Média: 7\.873\.472,2|Média aparada \(10%\): 6\.250\.792,8|Mediana: 4\.145\.040,0' "$H" | sort -u
grep -oE 'É a população de: Paraíba' "$H"
grep -oE 'Média simples     : 22,7389|Média ponderada   : 18,7907' "$H" | sort -u
grep -c 'California\|Califórnia' "$H"
grep -c 'callout-tip' "$H"
```
Expected:
```
Média: 7.873.472,2
Média aparada (10%): 6.250.792,8
Mediana: 4.145.040,0
É a população de: Paraíba
Média simples     : 22,7389
Média ponderada   : 18,7907
0          ← nenhuma menção à Califórnia sobrou
3          ← os três exercícios seguem
```

**Se algum número divergir, PARE.** Não ajuste o esperado para caber no obtido.

- [ ] **Step 8: Atualizar o teste dos widgets**

Em `scripts/verifica-widgets.py`, as constantes e o valor do arrasto:

```python
# Os mesmos números que o chunk Python imprime na página. Se o widget mostrar
# outra coisa na carga inicial, ele não está lendo os dados do livro.
MEDIA_REAL = "7.873.472,2"
MEDIANA_REAL = "4.145.040,0"
```

O slider de São Paulo tem valor inicial `45973194`; o teste continua arrastando para `300000000` e conferindo que a média muda e a mediana **não**. A checagem da caixa numérica após o arrasto continua esperando `"300000000"`.

Troque também a string do `print` que hoje diz `"widget A com CA em 300 M"` — o estado agora é **SP**, e um teste que fala de "CA" mente sobre o que está testando.

- [ ] **Step 9: Rodar o teste no navegador**

Run:
```bash
docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble \
  bash -c "pip install --quiet playwright==1.61.0 && python /scripts/verifica-widgets.py"
```
Expected:
```
sliders encontrados: 2
caixas numéricas: ['45973194', '10']
widget A na carga inicial: ['7.873.472,2', '6.250.792,8', '4.145.040,0']
widget A com SP em 300 M : [<média maior>, '6.250.792,8', '4.145.040,0']
caixa do slider A após arrastar: '300000000'
widget B com aparo 50%: média aparada pousou em 4.145.040,0

OK — os dois widgets carregam, são reativos e batem com os números do livro
```

A mediana **não pode mudar** ao arrastar o slider. Se mudar, o widget está calculando sobre o array errado.

- [ ] **Step 10: Commit**

```bash
git add content/cap01/03-estimativas-localizacao.qmd scripts/verifica-widgets.py
git commit -m "feat: secao 1.3 com dados brasileiros"
```

---

## Task 3: Seções 1.1 e 1.2

As duas mais leves — só nomes de coluna, números e o exemplo do estado.

**Files:**
- Modify: `content/cap01/01-dados-estruturados.qmd`
- Modify: `content/cap01/02-dados-retangulares.qmd`

**Interfaces:**
- Consumes: `dados/estados.csv` (Task 1); o padrão de prosa da Task 2.

- [ ] **Step 1: Seção 1.1 — Elementos de Dados Estruturados**

Troque a fonte (`dados/estados.csv`) e os nomes de coluna. Saídas reais:

```python
#| label: tipos
estado = pd.read_csv("dados/estados.csv")
estado.dtypes
```
`Estado` → `str` · `Populacao` → `int64` · `Taxa.Homicidios` → `float64` · `Sigla` → `str`

```python
#| label: categorico
estado["Sigla"] = estado["Sigla"].astype("category")
print(estado["Sigla"].dtype)
print("categorias:", len(estado["Sigla"].cat.categories))
```
Saída real: `category` e `categorias: 27` (eram 50).

A prosa que hoje fala de `Abbreviation` e dos estados americanos passa a falar de `Sigla` e das UFs. O exemplo do nominal (`"Alabama"` e `"AL"`) vira algo como `"São Paulo"` e `"SP"`. A tabela-resumo dos 5 tipos **não muda** — ela é conceitual.

Os chunks `ordinal` e `nominal-erro` (o categórico ordenado e o `TypeError`) **não usam o dataset**; não mexa neles.

- [ ] **Step 2: Seção 1.2 — Dados Retangulares**

```python
#| label: estrutura
estado = pd.read_csv("dados/estados.csv")
print("linhas x colunas:", estado.shape)
estado.head()
```
Saída real: `(27, 4)` (era `(50, 4)`).

```python
#| label: indice
print("índice padrão:", estado.index[:5].tolist())

por_estado = estado.set_index("Sigla")
por_estado.loc["SP"]
```
Saída real de `.loc["SP"]`: `Estado` = São Paulo · `Populacao` = 45973194 · `Taxa.Homicidios` = 6.16

A prosa e os exercícios trocam `"CA"`/California por `"SP"`/São Paulo, e `Abbreviation` por `Sigla`. O **exercício 1** diz "4 colunas — mas só `Population` e `Murder.Rate` são variáveis medidas"; os nomes viram `Populacao` e `Taxa.Homicidios`. O **exercício 3** (log de servidor) não usa o dataset; não mexa.

- [ ] **Step 3: Renderizar e conferir**

Run:
```bash
make render
grep -oE 'categorias: 27' _book/content/cap01/01-dados-estruturados.html
grep -oE '\(27, 4\)' _book/content/cap01/02-dados-retangulares.html
grep -c 'São Paulo' _book/content/cap01/02-dados-retangulares.html
grep -c 'California\|Califórnia\|Alabama' _book/content/cap01/01-dados-estruturados.html _book/content/cap01/02-dados-retangulares.html
```
Expected: `categorias: 27`; `(27, 4)`; `São Paulo` ≥ 1; **zero** menções a California/Califórnia/Alabama nas duas páginas.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/01-dados-estruturados.qmd content/cap01/02-dados-retangulares.qmd
git commit -m "feat: secoes 1.1 e 1.2 com dados brasileiros"
```

---

## Task 4: Seções 1.4 e 1.5

**Files:**
- Modify: `content/cap01/04-estimativas-variabilidade.qmd`
- Modify: `content/cap01/05-distribuicao-dados.qmd`

**Interfaces:**
- Consumes: `dados/estados.csv` (Task 1); o padrão de prosa da Task 2.

- [ ] **Step 1: Seção 1.4 — Estimativas de Variabilidade**

Troque a fonte e a coluna (`estado["Populacao"]`). Saídas reais:

| Chunk | Saída |
|---|---|
| `desvio-padrao` | `Desvio-padrão: 9.256.155,8` |
| `iqr` | `IQR: 6.443.986,0` |
| `mad` | `MAD: 4.752.396,9` (e o manual, idêntico) |

A prosa hoje diz que o desvio-padrão (6,8M) é "quase o dobro" do MAD (3,8M), razão 1,78. Nos dados brasileiros a razão é **1,95** — ainda mais próxima do dobro, e o argumento (cauda longa) fica **mais forte**, não mais fraco. Atualize os números e a tabela-resumo.

O **exercício 2** cita "6,85M e 3,85M — quase o dobro"; passa a citar `9,26M` e `4,75M`. Os exercícios 1 e 3 (por que não a média dos desvios; o que acontece ao multiplicar por 1000) são conceituais — **não mexa neles**.

- [ ] **Step 2: Seção 1.5 — Explorando a Distribuição dos Dados**

Troque a fonte e as colunas. Saídas reais:

Quantis da `Taxa.Homicidios`:

| | 5% | 25% | 50% | 75% | 95% |
|---|---|---|---|---|---|
| valor | `8,238` | `16,165` | `23,130` | `30,295` | `35,197` |

**O boxplot muda de forma:** com os dados americanos, quatro estados ficavam acima do bigode (CA, TX, NY, FL). Com os brasileiros, são **apenas dois: MG e SP**. O callout `.exemplo` que hoje lê o boxplot em voz alta ("os pontos isolados no topo são Califórnia, Texas, Nova York e Flórida") precisa ser reescrito com os valores e os estados novos.

A tabela de frequência (`pd.cut` em 10 faixas) põe **15 dos 27** estados na primeira faixa — a mesma assinatura de cauda longa, ainda mais concentrada.

Os três exercícios citam números (percentil 95 = 6,51; a leitura do boxplot; o `pd.cut`). Atualize os valores; a lógica das respostas continua válida.

- [ ] **Step 3: Renderizar e conferir**

Run:
```bash
make render
grep -oE 'Desvio-padrão: 9\.256\.155,8|IQR: 6\.443\.986,0|MAD: 4\.752\.396,9' \
  _book/content/cap01/04-estimativas-variabilidade.html | sort -u
grep -c '<img' _book/content/cap01/05-distribuicao-dados.html
grep -c 'Califórnia\|Texas\|Flórida' _book/content/cap01/05-distribuicao-dados.html
grep -c 'callout-tip' _book/content/cap01/04-estimativas-variabilidade.html
```
Expected: os três números de 1.4 exatos; `<img>` ≥ 3 em 1.5; **zero** menções a Califórnia/Texas/Flórida; `callout-tip` = 3.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/04-estimativas-variabilidade.qmd content/cap01/05-distribuicao-dados.qmd
git commit -m "feat: secoes 1.4 e 1.5 com dados brasileiros"
```

---

## Task 5: Remover o dado americano e documentar

**Files:**
- Delete: `dados/state.csv`
- Modify: `CLAUDE.md`
- Modify: `dados/README.md`

**Interfaces:**
- Consumes: tudo das Tasks 1–4.

- [ ] **Step 1: Confirmar que nada mais usa o `state.csv`**

Run:
```bash
grep -rn 'state\.csv' content/ scripts/ CLAUDE.md dados/README.md
```
Expected: **nenhuma saída**. Se aparecer alguma referência, ela precisa ser migrada antes de o arquivo sair.

- [ ] **Step 2: Remover**

```bash
git rm dados/state.csv
```

Ele fica órfão depois da migração, e mantê-lo convida um agente futuro a usá-lo por engano.

- [ ] **Step 3: Atualizar `dados/README.md`**

Remova a linha `| state.csv | 1.3 Estimativas de Localização, 1.4 Variabilidade, 1.5 Distribuição |` da tabela dos CSVs do livro-texto, e ajuste a contagem (a seção diz "os 14 conjuntos usados pelos capítulos 1–4"; passam a ser **13** do livro-texto, mais o `estados.csv`, que é nosso).

- [ ] **Step 4: Documentar no `CLAUDE.md`**

Na seção "Caminhos de dados", acrescente:

````markdown
**O dado dos estados é brasileiro.** `dados/estados.csv` traz as 27 unidades federativas com população (IBGE, 2024) e taxa de homicídios (Atlas da Violência, 2024). Colunas em português: `Estado`, `Populacao`, `Taxa.Homicidios`, `Sigla`.

Ele é **gerado por nós**, não vem do livro-texto: `scripts/gerar-dados-brasil.py` junta três fontes e roda **uma única vez** (o CSV é commitado). O pipeline não é um chunk do livro — o aluno não precisa ver a mecânica de juntar três fontes para aprender o que é uma mediana, e um livro que faz chamadas de rede a cada render é frágil.

O CSV bruto do Atlas está versionado em `dados/brutos/` porque a API do Atlas saiu do ar na reformulação do site (v3) e hoje devolve HTML.

Três consequências que diferenciam o dado brasileiro do americano que ele substituiu, e que estão embutidas na prosa do Capítulo 1:

1. **n = 27 é ímpar** — a mediana é uma observação de verdade (é a população da Paraíba), não a média de duas. A seção 1.3 ensina os dois casos.
2. **A média ponderada da taxa é MENOR que a simples** (18,79 contra 22,74), ao contrário dos EUA. São Paulo tem a maior população do país e a menor taxa de homicídios — a violência letal se concentra nos estados menos populosos.
3. **São Paulo é o outlier populacional** (46 M contra 717 mil de Roraima, 64×), e é ele que os widgets da seção 1.3 movem.
````

- [ ] **Step 5: Commit**

```bash
git add -A dados/ CLAUDE.md
git commit -m "chore: remove o dado americano e documenta o brasileiro"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean && make render
find _book/content -name '*.html' | wc -l
```
Expected: `42`, sem erro.

- [ ] **O `state.csv` sumiu e ninguém o procura**

```bash
test -e dados/state.csv && echo "ERRO: ainda existe" || echo "removido"
grep -rn 'state\.csv' content/ scripts/ CLAUDE.md && echo "ERRO: ainda referenciado" || echo "sem referências"
```
Expected: `removido` e `sem referências`.

- [ ] **Nenhum vestígio dos EUA nas 5 seções migradas**

```bash
grep -rniE 'california|califórnia|wyoming|alabama|murder\.rate|Population\b|Abbreviation' \
  content/cap01/0[12345]-*.qmd && echo "ERRO: sobrou dado americano" || echo "tudo brasileiro"
```
Expected: `tudo brasileiro`.

- [ ] **Os números brasileiros estão nas páginas**

```bash
grep -rohE '7\.873\.472,2|6\.250\.792,8|4\.145\.040,0|22,7389|18,7907|9\.256\.155,8|6\.443\.986,0|4\.752\.396,9' \
  _book/content/cap01/0*.html | sort -u
```
Expected: os 8 valores.

- [ ] **Os widgets funcionam num navegador de verdade**

```bash
docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble \
  bash -c "pip install --quiet playwright==1.61.0 && python /scripts/verifica-widgets.py"
```
Expected: `OK — os dois widgets carregam, são reativos e batem com os números do livro`

- [ ] **O pipeline é reproduzível**

```bash
docker compose run --rm --no-deps livro python scripts/gerar-dados-brasil.py
git diff --stat dados/estados.csv
```
Expected: `27 unidades federativas, ano 2024`, e **nenhuma diferença** no CSV — rodar de novo produz exatamente o mesmo arquivo.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
