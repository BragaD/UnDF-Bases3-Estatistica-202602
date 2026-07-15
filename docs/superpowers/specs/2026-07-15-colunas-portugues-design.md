# Colunas dos Datasets em Português (seções 1.6, 1.7, 1.8)

**Data:** 2026-07-15
**Status:** Aprovado

## Objetivo

Traduzir para português os nomes de coluna — e os valores categóricos traduzíveis — dos datasets usados nas seções 1.6, 1.7 e 1.8, para que os exemplos sejam mais fáceis de entender. Os dados brasileiros da 1.1–1.5 (`estados.csv`) já estão em português; esta tarefa cobre os cinco datasets do livro-texto que sobraram.

## Decisões (do brainstorming)

- **Escopo:** nomes de coluna **e** valores categóricos traduzíveis.
- **Abordagem:** renomear **na leitura** (`pd.read_csv(...).rename(columns=...)` e, para valores, `.replace(...)`/`.map(...)`). Os CSVs em `dados/` ficam **intactos** — fiéis à fonte, como o `dados/README.md` promete. A tradução vive no livro, não nos arquivos.

## O que permanece em inglês, e por quê

Três categorias são identificadores ou nomes próprios, não texto:

- **Tickers de ações** (`T`, `VZ`, `SPY`, `XLE`, …) — códigos de negociação; são os nomes das colunas de `sp500_data.csv.gz` e os valores de `symbol`.
- **Nomes das companhias aéreas** (`Alaska`, `American`, `Delta`, `Jet Blue`, `Southwest`, `United`) — nomes próprios; valores de `airline`.
- **Notas de risco** (`A`–`G` em `lc_loans`) — graus, como rating de crédito; ficam como letras.
- **`etf`** — sigla (Exchange-Traded Fund); fica.

## Convenção de nomes

Segue o padrão do `estados.csv`: **CamelCase** para colunas de conceito único (`ValorVenal`, `AreaConstruida`, `Companhia`), e **snake_case** para a família de métricas `pct_*` (`pct_atraso_companhia`), que já era snake_case no original e lê melhor assim.

## O mapa de tradução

### 1.6 — `dfw_airline.csv`

As colunas são as causas de atraso; traduzi-las também troca os rótulos do gráfico de barras (é uma tabela de uma linha, transposta).

| Original | Português |
|---|---|
| `Carrier` | `Companhia` |
| `ATC` | `ControleAereo` |
| `Weather` | `Clima` |
| `Security` | `Seguranca` |
| `Inbound` | `VooAnterior` |

### 1.7 — `sp500_sectors.csv` e `sp500_data.csv.gz`

Colunas de `sp500_sectors`: `sector`→`Setor`, `symbol`→`Simbolo`.

Valores de `Setor` (traduzidos todos, para consistência):

| Original | Português |
|---|---|
| `consumer_discretionary` | `consumo_discricionario` |
| `consumer_staples` | `consumo_essencial` |
| `energy` | `energia` |
| `etf` | `etf` (sigla, fica) |
| `financials` | `financeiro` |
| `health_care` | `saude` |
| `industrials` | `industrial` |
| `information_technology` | `tecnologia_da_informacao` |
| `materials` | `materiais` |
| `telecommunications_services` | `telecomunicacoes` |
| `utilities` | `utilidade_publica` |

`sp500_data.csv.gz`: colunas são tickers → **não** mudam. Os valores de `symbol` (tickers) → **não** mudam.

### 1.8 — `kc_tax.csv.gz`

| Original | Português |
|---|---|
| `TaxAssessedValue` | `ValorVenal` |
| `SqFtTotLiving` | `AreaConstruida` |
| `ZipCode` | `CEP` |

Os valores de `AreaConstruida` continuam em **pés²** (é dado dos EUA) — a prosa da seção já registra a unidade.

### 1.8 — `lc_loans.csv`

Colunas: `status`→`Situacao`, `grade`→`Nota`.

Valores de `Situacao`:

| Original | Português |
|---|---|
| `Fully Paid` | `Quitado` |
| `Current` | `Em dia` |
| `Late` | `Atrasado` |
| `Charged Off` | `Inadimplente` |

Valores de `Nota` (`A`–`G`) → ficam como letras.

Nota sobre `Charged Off`→`Inadimplente`: "charged off" é tecnicamente mais forte (o banco baixou a dívida como prejuízo), mas "inadimplente" é o termo que o aluno reconhece e serve ao ponto da seção — que é a taxa de inadimplência crescer monotonicamente da nota A à G.

### 1.8 — `airline_stats.csv`

| Original | Português |
|---|---|
| `pct_carrier_delay` | `pct_atraso_companhia` |
| `pct_atc_delay` | `pct_atraso_controle` |
| `pct_weather_delay` | `pct_atraso_clima` |
| `airline` | `Companhia` |

Valores de `Companhia` (nomes próprios) → ficam.

## Raio de alcance

Os nomes aparecem no **código** e na **prosa** das três seções. Traduzir cada um exige:

1. O `.rename(columns=...)` (e `.replace(...)` para valores) logo após cada `pd.read_csv`.
2. Todas as referências no código dos chunks (`estado["Populacao"]`-style, filtros como `Setor == "telecomunicacoes"`, `crosstab`, etc.).
3. Todas as menções na **prosa** — a 1.6 discute cada causa de atraso pelo nome; a 1.8 cita `Charged Off`, `grade`, etc.

Uma coluna traduzida no código mas ainda citada em inglês na prosa é um defeito — a verificação precisa pegar isso.

## Verificação

- `make render` gera as 42 páginas sem erro.
- Os **números** das três seções não mudam — só rótulos e nomes. A tradução não pode alterar nenhum valor calculado (as proporções de atraso, as correlações, os totais do crosstab, as medianas por companhia).
- Nenhum vestígio dos nomes de coluna em inglês (`Carrier`, `TaxAssessedValue`, `pct_carrier_delay`, `Charged Off`, etc.) sobra nas páginas renderizadas das seções 1.6–1.8 — nem no código, nem na prosa, nem nos gráficos.
- Os identificadores que **devem** ficar (tickers, nomes de companhias, notas A–G) continuam lá.

## Fora de escopo

- Os CSVs em `dados/` não são alterados.
- As seções 1.1–1.5 (já em português) e os capítulos 2–4 (stubs) não são tocados.
- Unidades de medida (pés², dólares) não são convertidas — só os rótulos.
