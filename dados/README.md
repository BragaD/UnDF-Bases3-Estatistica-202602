# Conjuntos de Dados

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

## `alugueis.csv` — aluguéis em 5 cidades brasileiras (traduzido por nós)

10.692 imóveis para alugar em São Paulo, Rio de Janeiro, Belo Horizonte, Porto
Alegre e Campinas. É o dataset que atravessa o capítulo: a atividade **"Agora é
com você"** das seções 1.3 a 1.5, os dados categóricos e binários da 1.6, a
matriz de correlação da 1.7 e os quatro pares de tipos da 1.8.

Fonte: *Brazilian houses to rent* (v2), publicado no Kaggle por rubenssjr sob
**CC0** (domínio público). O CSV bruto está versionado em
`dados/brutos/houses_to_rent_v2.csv` (o Kaggle exige login para baixar).

Gerado por `scripts/gerar-dados-alugueis.py`, que roda **uma única vez**:

```bash
docker compose run --rm --no-deps livro python scripts/gerar-dados-alugueis.py
```

| Original | Aqui | Original | Aqui |
|---|---|---|---|
| `city` | `cidade` | `animal` (acept / not acept) | `aceita_animal` (sim / não) |
| `area` | `area_m2` | `furniture` (furnished / not furnished) | `mobiliado` (sim / não) |
| `rooms` | `quartos` | `hoa (R$)` | `condominio` |
| `bathroom` | `banheiros` | `rent amount (R$)` | `aluguel` |
| `parking spaces` | `vagas` | `property tax (R$)` | `iptu` |
| `floor` | `andar` | `fire insurance (R$)` | `seguro_incendio` |
| | | `total (R$)` | `total` |

**Só os nomes (e os dois binários) foram traduzidos — nada foi limpo, de
propósito.** A coluna `andar` traz `"-"` em 2.461 linhas (23%), o que faz o
pandas lê-la como texto: essa é a armadilha que a atividade pede ao aluno para
descobrir. Os outliers (área de 46.335 m², condomínio de R$ 1.117.000) também
ficaram — são o material de média × mediana × média aparada.

Os arquivos deste diretório vêm do repositório oficial do livro-texto:

**Bruce, Bruce & Gedeck — *Practical Statistics for Data Scientists*, 2ª ed. (O'Reilly, 2020)**
<https://github.com/gedeck/practical-statistics-for-data-scientists>

Os nomes originais foram preservados para que o código do livro rode sem adaptação.

**Nenhum conjunto do livro-texto está em uso hoje.** Em 20/09/2026 as seções 1.3, 1.6, 1.7 e
1.8 passaram a usar `alugueis.csv` e `estados.csv`, dado brasileiro, e seis arquivos saíram do
repositório: `dfw_airline.csv` e `airline_stats.csv` (causas de atraso e atrasos por companhia
aérea), `sp500_data.csv.gz` e `sp500_sectors.csv` (retornos de ações), `kc_tax.csv.gz`
(imóveis de King County) e `lc_loans.csv` (empréstimos do LendingClub). Eles continuam no
histórico do git e no repositório do livro-texto.

**Sem uso no momento.** Os capítulos que os consumiam saíram do site enquanto o material é
reconstruído. Os arquivos ficam aqui de propósito, e a numeração abaixo é a do **Bruce**, para
achar a seção de origem quando o conteúdo voltar.

| Arquivo | Seção do Bruce |
|---|---|
| `loans_income.csv` | 2.3 Distribuição Amostral, 2.4 Bootstrap, 2.5 Intervalos de Confiança |
| `web_page_data.csv` | 3.1 Teste A/B, 3.3 Reamostragem |
| `four_sessions.csv` | 3.8 ANOVA |
| `click_rates.csv` | 3.9 Teste Qui-Quadrado |
| `imanishi_data.csv` | 3.9 Teste Qui-Quadrado |
| `LungDisease.csv` | 4.1 Regressão Linear Simples |
| `house_sales.csv` | 4.2–4.7 Regressão Múltipla e diagnóstico |

## Como referenciar nos chunks

O `_quarto.yml` define `execute-dir: project`, então o diretório de trabalho de
qualquer chunk é a **raiz do projeto**, não a pasta do `.qmd`. Use sempre:

````python
estado = pd.read_csv("dados/estados.csv")
````

Nunca `../../dados/estados.csv`.
