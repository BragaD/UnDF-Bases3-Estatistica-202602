# Colunas dos Datasets em Português — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Traduzir para português os nomes de coluna e os valores categóricos traduzíveis dos datasets usados nas seções 1.6, 1.7 e 1.8.

**Architecture:** A tradução acontece **na leitura** (`pd.read_csv(...).rename(columns=...)` e `.replace(...)` para valores). Os CSVs em `dados/` ficam intactos. Uma task por seção, porque cada seção usa datasets distintos e é renderizável/verificável isoladamente.

**Tech Stack:** pandas · Quarto (engine jupyter) · matplotlib/seaborn

**Spec:** `docs/superpowers/specs/2026-07-15-colunas-portugues-design.md`

## Global Constraints

- **Os CSVs em `dados/` NÃO são alterados.** A tradução vive nos chunks, via `.rename` / `.replace` na leitura.
- **Nenhum número pode mudar.** A tradução troca rótulos e nomes, não valores calculados. As proporções de atraso, as correlações, os totais do crosstab e as medianas por companhia têm de sair idênticos aos de hoje. Se algum mudar, um filtro foi quebrado — PARE.
- **A prosa também traduz.** Uma coluna traduzida no código mas ainda citada em inglês no texto é um defeito. Vale para os rótulos dos gráficos também.
- **Ficam em inglês** (identificadores / nomes próprios): tickers de ações (`T`, `VZ`, `SPY`…), nomes de companhias aéreas (`Alaska`, `American`, `Jet Blue`…), notas de risco `A`–`G`, e a sigla `etf`.
- **Formato brasileiro** nos números impressos: `from formato import num` (já em uso nas seções). Nunca `f"{x:,.1f}"`.
- **Convenção:** CamelCase para colunas de conceito único (`ValorVenal`, `Companhia`); snake_case para a família `pct_*` (`pct_atraso_companhia`).
- **Render sempre via container:** `make render`. Não há Quarto/Python confiáveis no host.
- **Não crie `AGENTS.md`.** Não mexa em `_quarto.yml`, `pyproject.toml`, `uv.lock`, `formato.py`, `dados/`.

---

## Estrutura de Arquivos

| Arquivo | Task | Datasets |
|---|---|---|
| `content/cap01/06-dados-binarios-categoricos.qmd` | 1 | `dfw_airline` |
| `content/cap01/07-correlacao.qmd` | 2 | `sp500_sectors`, `sp500_data` |
| `content/cap01/08-duas-ou-mais-variaveis.qmd` | 3 | `kc_tax`, `lc_loans`, `airline_stats` |

As três tasks são **independentes** — cada uma toca um arquivo, nenhuma depende da outra.

---

## Task 1: Seção 1.6 — `dfw_airline`

**Files:**
- Modify: `content/cap01/06-dados-binarios-categoricos.qmd`

**Interfaces:**
- Consumes: `dados/dfw_airline.csv` (colunas `Carrier`, `ATC`, `Weather`, `Security`, `Inbound`).

- [ ] **Step 1: Renomear as colunas na leitura**

O `dfw_airline.csv` tem uma linha e cinco colunas. Traduzir os nomes das colunas também troca os rótulos do gráfico de barras (a tabela é transposta). No chunk que lê o arquivo (`#| label: proporcoes`), acrescente o `.rename` logo após o `read_csv`:

```python
dfw = pd.read_csv("dados/dfw_airline.csv").rename(columns={
    "Carrier": "Companhia",
    "ATC": "ControleAereo",
    "Weather": "Clima",
    "Security": "Seguranca",
    "Inbound": "VooAnterior",
})
```

- [ ] **Step 2: Trocar as referências no código dos chunks**

Toda ocorrência das colunas antigas no código vira o nome novo. Os pontos conhecidos:
- O dicionário `custo` do chunk `valor-esperado` usa as chaves `"Carrier"`, `"ATC"`, `"Weather"`, `"Security"`, `"Inbound"` — todas viram os nomes em português.
- O chunk `moda` usa `.idxmax()` — a saída passa a ser `VooAnterior` (era `Inbound`).

Rode `grep -nE "Carrier|ATC|Weather|Security|Inbound" content/cap01/06-dados-binarios-categoricos.qmd` e migre cada uma.

- [ ] **Step 3: Trocar as referências na prosa**

A seção discute cada causa de atraso pelo nome. Toda menção no texto vira o termo em português: "Carrier" → "Companhia", "ATC" → "Controle Aéreo", "Weather" → "Clima", "Security" → "Segurança", "Inbound" → "Voo Anterior". A frase do callout `.exemplo` que hoje explica que `Inbound` é atraso herdado do voo anterior passa a falar de `VooAnterior` — e a explicação continua fazendo sentido (é o que o nome novo já diz).

- [ ] **Step 4: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap01/06-dados-binarios-categoricos.html
grep -ciE 'Carrier|Weather|Security|Inbound|\bATC\b' "$H"
grep -c "VooAnterior\|Voo Anterior" "$H"
```
Expected: **0** vestígios das colunas em inglês; `VooAnterior`/`Voo Anterior` ≥ 1.

- [ ] **Step 5: Conferir que os NÚMEROS não mudaram**

A moda continua sendo a maior causa (era `Inbound`, agora `VooAnterior`), e as proporções são idênticas.

Run:
```bash
grep -oE '42,43|30,40|23,02|4,03|0,12' "$H" | sort -u | tr '\n' ' '; echo
grep -oE 'R\$ 104,55' "$H"
```
Expected: as cinco proporções (`23,02`, `30,40`, `4,03`, `0,12`, `42,43`) e o valor esperado `R$ 104,55` — inalterados.

**Se algum número mudar, PARE.** A tradução não pode tocar nos valores.

- [ ] **Step 6: Commit**

```bash
git add content/cap01/06-dados-binarios-categoricos.qmd
git commit -m "docs: colunas do dfw_airline em portugues (secao 1.6)"
```

---

## Task 2: Seção 1.7 — `sp500`

**Files:**
- Modify: `content/cap01/07-correlacao.qmd`

**Interfaces:**
- Consumes: `dados/sp500_sectors.csv` (colunas `sector`, `symbol`), `dados/sp500_data.csv.gz` (colunas = tickers).

- [ ] **Step 1: Renomear as colunas e traduzir os valores de setor no `sp500_sectors`**

Os **tickers** (valores de `symbol`, e as colunas de `sp500_data`) **não** mudam — são identificadores. Só a coluna `sector`/`symbol` e os valores de `sector`.

No chunk que lê os setores (`#| label: carrega`), logo após o `read_csv`:

```python
SETORES = {
    "consumer_discretionary": "consumo_discricionario",
    "consumer_staples": "consumo_essencial",
    "energy": "energia",
    "etf": "etf",
    "financials": "financeiro",
    "health_care": "saude",
    "industrials": "industrial",
    "information_technology": "tecnologia_da_informacao",
    "materials": "materiais",
    "telecommunications_services": "telecomunicacoes",
    "utilities": "utilidade_publica",
}
setores = pd.read_csv("dados/sp500_sectors.csv").rename(
    columns={"sector": "Setor", "symbol": "Simbolo"}
)
setores["Setor"] = setores["Setor"].replace(SETORES)
```

- [ ] **Step 2: Atualizar os filtros no código**

O código filtra por setor. As referências mudam de nome de coluna **e** de valor:
- `setores[setores["sector"] == "telecommunications_services"]["symbol"]` → `setores[setores["Setor"] == "telecomunicacoes"]["Simbolo"]`
- `setores[setores["sector"] == "etf"]["symbol"]` → `setores[setores["Setor"] == "etf"]["Simbolo"]`

Confira com `grep -nE "sector|symbol|telecommunications" content/cap01/07-correlacao.qmd`.

- [ ] **Step 3: Prosa — o mínimo necessário**

A prosa da 1.7 fala de "telecomunicações" e "ETFs" já em português; ela raramente cita os nomes de coluna crus. Verifique se sobra alguma menção literal a `sector`/`symbol`/`telecommunications_services` no texto e traduza. Os tickers (`T`, `VZ`) **continuam** aparecendo na prosa — são identificadores e devem ficar.

- [ ] **Step 4: Renderizar e conferir os números (a correlação é o gate)**

Run:
```bash
make render
H=_book/content/cap01/07-correlacao.html
grep -c '0,678' "$H"
grep -ciE '\bsector\b|\bsymbol\b|telecommunications_services' "$H"
grep -c 'telecomunicacoes\|telecomunicações' "$H"
```
Expected: `0,678` (a correlação T×VZ) ≥ 1 — **inalterada**; **0** vestígios de `sector`/`symbol`/`telecommunications_services`; a menção a telecomunicações presente.

Os tickers devem sobreviver:
```bash
grep -oE "'T'|'VZ'|XLE|SPY" "$H" | sort -u | tr '\n' ' '; echo
```
Expected: os tickers continuam lá.

**Se `0,678` sumir, o filtro de setor foi quebrado — PARE.**

- [ ] **Step 5: Commit**

```bash
git add content/cap01/07-correlacao.qmd
git commit -m "docs: colunas do sp500 em portugues, tickers preservados (secao 1.7)"
```

---

## Task 3: Seção 1.8 — `kc_tax`, `lc_loans`, `airline_stats`

A maior das três: três datasets, e valores traduzíveis em `lc_loans`.

**Files:**
- Modify: `content/cap01/08-duas-ou-mais-variaveis.qmd`

**Interfaces:**
- Consumes: `dados/kc_tax.csv.gz`, `dados/lc_loans.csv`, `dados/airline_stats.csv`.

- [ ] **Step 1: `kc_tax` — renomear na leitura**

No chunk `carrega-kc`:

```python
kc = pd.read_csv("dados/kc_tax.csv.gz").rename(columns={
    "TaxAssessedValue": "ValorVenal",
    "SqFtTotLiving": "AreaConstruida",
    "ZipCode": "CEP",
})
```

Todas as referências seguintes (`kc.TaxAssessedValue`, `kc0.SqFtTotLiving`, `kc0.ZipCode`, os `x=`/`y=` dos gráficos, o filtro `.isin([...])` de CEPs) trocam para os nomes novos. Os valores de `AreaConstruida` continuam em **pés²** — os rótulos dos eixos e a prosa já dizem isso.

- [ ] **Step 2: `lc_loans` — renomear colunas E traduzir valores de situação**

No chunk `crosstab`:

```python
SITUACAO = {
    "Fully Paid": "Quitado",
    "Current": "Em dia",
    "Late": "Atrasado",
    "Charged Off": "Inadimplente",
}
lc = pd.read_csv("dados/lc_loans.csv").rename(columns={"status": "Situacao", "grade": "Nota"})
lc["Situacao"] = lc["Situacao"].replace(SITUACAO)
```

As notas `A`–`G` (valores de `Nota`) **ficam** como letras.

O `pivot_table` muda: `index="grade"` → `index="Nota"`, `columns="status"` → `columns="Situacao"`. As notas `A`–`G` (valores de `Nota`) **ficam** como letras.

**Ponto crítico — o slice de colunas do chunk `crosstab-pct` quebra.** Hoje a linha é:

```python
prop.loc[:, "Charged Off":"Late"] = prop.loc[:, "Charged Off":"Late"].div(prop["All"], axis=0)
```

Esse slice por rótulo (`"Charged Off":"Late"`) só funciona porque as colunas em inglês, na ordem do `pivot_table`, vão de `Charged Off` a `Late` com `All` no fim. Com os valores traduzidos, o `pivot_table` reordena as colunas alfabeticamente (`Atrasado`, `Em dia`, `Inadimplente`, `Quitado`, `All`) e os rótulos `"Charged Off"`/`"Late"` deixam de existir — o slice levanta `KeyError`.

Substitua por uma seleção **independente de ordem**: todas as colunas de situação são as que não são a margem `All`.

```python
situacoes = [c for c in prop.columns if c != "All"]
prop.loc[:, situacoes] = prop.loc[:, situacoes].div(prop["All"], axis=0)
```

O `index="A":"G"` do início do chunk (`prop = contagem.copy().loc["A":"G", :]`) **continua válido** — as notas seguem A–G.

- [ ] **Step 3: `airline_stats` — renomear na leitura**

No chunk `fig-boxplot-grupo`:

```python
voos = pd.read_csv("dados/airline_stats.csv").rename(columns={
    "pct_carrier_delay": "pct_atraso_companhia",
    "pct_atc_delay": "pct_atraso_controle",
    "pct_weather_delay": "pct_atraso_clima",
    "airline": "Companhia",
})
```

Os valores de `Companhia` (`Alaska`, `American`, …) **ficam** — nomes próprios. As referências `by="airline"`, `column="pct_carrier_delay"`, o `x="airline"`/`y="pct_carrier_delay"` do violin, trocam para os nomes novos.

- [ ] **Step 4: Trocar as referências na prosa**

A 1.8 cita `Charged Off`, `grade`, `status`, `TaxAssessedValue`, `SqFtTotLiving` no texto. Cada uma vira o termo em português: "Charged Off" → "Inadimplente", "grade" → "nota", os nomes de coluna pelos novos. O ponto pedagógico do crosstab — a taxa de `Inadimplente` crescer da nota A à G — se reescreve com os termos novos, sem mudar o argumento.

Os CEPs (98105, 98108, …) e os nomes das companhias continuam como estão.

- [ ] **Step 5: Renderizar e conferir os números (vários gates)**

Run:
```bash
make render
H=_book/content/cap01/08-duas-ou-mais-variaveis.html
echo "--- vestígios em inglês (esperado 0) ---"
grep -ciE 'TaxAssessedValue|SqFtTotLiving|ZipCode|pct_carrier_delay|pct_atc_delay|Charged Off|\bgrade\b|Fully Paid' "$H"
echo "--- os números não mudaram ---"
grep -oE '498\.249|432\.693|450\.961|72\.490|3\.241' "$H" | sort -u | tr '\n' ' '; echo
echo "--- os identificadores que ficam ---"
grep -oE 'Alaska|American|Jet Blue|98105|\bA\b' "$H" | sort -u | tr '\n' ' '; echo
```
Expected: **0** vestígios em inglês; os totais do `kc_tax` (`498.249` → `432.693`) e do crosstab (`450.961`, grade A `72.490`, grade G `3.241`) **inalterados**; os nomes de companhia, CEPs e a nota `A` presentes.

**Se `450.961` ou `432.693` mudarem, um `.rename`/`.replace` quebrou os dados — PARE.**

- [ ] **Step 6: Commit**

```bash
git add content/cap01/08-duas-ou-mais-variaveis.qmd
git commit -m "docs: colunas de kc_tax, lc_loans e airline_stats em portugues (secao 1.8)"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean && make render
find _book/content -name '*.html' | wc -l
```
Expected: `42`, sem erro.

- [ ] **Nenhum nome de coluna em inglês sobrou nas três seções**

```bash
grep -rciE 'Carrier|TaxAssessedValue|SqFtTotLiving|ZipCode|pct_carrier_delay|pct_atc_delay|pct_weather_delay|Charged Off|Fully Paid|\bsector\b|\bsymbol\b' \
  _book/content/cap01/06-dados-binarios-categoricos.html \
  _book/content/cap01/07-correlacao.html \
  _book/content/cap01/08-duas-ou-mais-variaveis.html
```
Expected: `0` em cada arquivo.

- [ ] **Os identificadores que devem ficar continuam lá**

```bash
grep -c "'T'\|'VZ'" _book/content/cap01/07-correlacao.html
grep -c 'Alaska\|American' _book/content/cap01/08-duas-ou-mais-variaveis.html
```
Expected: ambos ≥ 1 — tickers e nomes de companhias preservados.

- [ ] **Os números-chave sobreviveram (amostra transversal)**

```bash
grep -oE '0,678' _book/content/cap01/07-correlacao.html | head -1
grep -oE '450\.961|432\.693' _book/content/cap01/08-duas-ou-mais-variaveis.html | sort -u
grep -oE '42,43|R\$ 104,55' _book/content/cap01/06-dados-binarios-categoricos.html | sort -u
```
Expected: `0,678`; `432.693` e `450.961`; `42,43` e `R$ 104,55` — todos inalterados.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
