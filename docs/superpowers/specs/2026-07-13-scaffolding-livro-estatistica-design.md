# Scaffolding — Livro Quarto "Bases 3 — Estatística"

**Data:** 2026-07-13
**Status:** Aprovado

## Objetivo

Criar o repositório de um site/livro Quarto para a disciplina **Bases 3 — Estatística**, atendendo aos cursos de Engenharia de Software e Sistemas de Informação da UnDF.

O repositório espelha a arquitetura de `../../202601/BasesIV_EngSoft_BD` (Quarto book, GitHub Actions, tema e logo da UnDF), com uma diferença central: **os exemplos são em Python, não em R**. Isso substitui toda a camada R (`renv`, `.Rprofile`, `setup-renv`, serviço PostgreSQL no CI) por uma camada Python containerizada.

## Livro-texto

Bruce, Bruce & Gedeck — *Practical Statistics for Data Scientists*, 2ª ed. (O'Reilly, 2020).
Código e dados: <https://github.com/gedeck/practical-statistics-for-data-scientists>

O livro-texto tem 7 capítulos. **O escopo desta disciplina são os capítulos 1–4** (núcleo estatístico). Os capítulos 5–7 (Classificação, ML Estatístico, Aprendizado Não-Supervisionado) ficam para *Bases 5 — Ciência de Dados*, disciplina irmã em `../bases_5_ciencia_de_dados`.

## Identidade

| Item | Valor |
|---|---|
| Repositório | `BragaD/UnDF-Bases3-Estatistica-202602` |
| Site | `https://BragaD.github.io/UnDF-Bases3-Estatistica-202602` |
| Imagem Docker | `ghcr.io/bragad/undf-bases3-estatistica-202602` |
| Título | "Bases 3" |
| Subtítulo | "Estatística" |
| Navbar | "Bases 3 — Estatística" |
| Rodapé | "UnDF — Engenharia de Software e Sistemas de Informação — Estatística — 2026.2" |
| Autor | Douglas Braga <douglas.braga@undf.edu.br> |
| Idioma | `pt` |

## Arquitetura

### Engine

`jupyter` (Python nativo), no lugar do `knitr` do repo de referência. `execute: freeze: auto` — o Quarto só re-executa chunks cujo fonte mudou; o cache vai para `_freeze/` (gitignorado).

### Diretório de trabalho dos chunks

`execute-dir: project` no `_quarto.yml` — sob o bloco `project:`, **não** sob `execute:`:

```yaml
project:
  type: book
  output-dir: _book
  execute-dir: project
```

Isto é uma **melhoria deliberada sobre o repo de referência**, onde o diretório de trabalho era o do *arquivo*, obrigando todo chunk a referenciar dados como `../../dados/arquivo.csv` — uma pegadinha que o CLAUDE.md de lá precisava documentar. Com `execute-dir: project`, qualquer chunk, em qualquer capítulo, usa o caminho uniforme `dados/state.csv`.

### Diretório de saída

`output-dir: _book` (padrão do Quarto para livros), gitignorado.

Isto também diverge do repo de referência, que usa `output-dir: docs` **e** gitignora `docs/` — vestígio de um setup "GitHub Pages serve a partir de /docs" que não é mais usado, já que a publicação é na branch `gh-pages`. Usar `_book` libera `docs/` para documentação real do projeto (incluindo este spec).

### Estrutura de conteúdo

Mesmo padrão do repo de referência: um diretório por capítulo, um `.qmd` por seção.

```
content/
├── cap01/   Análise Exploratória de Dados             index.qmd + 8 seções
├── cap02/   Dados e Distribuições Amostrais           index.qmd + 12 seções
├── cap03/   Experimentos Estatísticos e Significância index.qmd + 11 seções
└── cap04/   Regressão e Predição                      index.qmd + 7 seções
```

**Regra invariante:** todo arquivo novo precisa ser registrado em `_quarto.yml` sob `book.chapters`. O YAML define o sidebar e a ordem de navegação; arquivo não listado não aparece no livro. A ordem vem do `_quarto.yml`, não do nome do arquivo.

Cada `capXX/index.qmd` traz visão geral, objetivos de aprendizagem e uma tabela de seções — mesmo padrão de `content/cap01/index.qmd` do repo de referência.

As seções espelham fielmente as do livro-texto:

**Cap. 1 — Análise Exploratória de Dados**
1. Elementos de Dados Estruturados
2. Dados Retangulares
3. Estimativas de Localização
4. Estimativas de Variabilidade
5. Explorando a Distribuição dos Dados
6. Explorando Dados Binários e Categóricos
7. Correlação
8. Explorando Duas ou Mais Variáveis

**Cap. 2 — Dados e Distribuições Amostrais**
1. Amostragem Aleatória e Viés de Amostra
2. Viés de Seleção
3. Distribuição Amostral de uma Estatística
4. Bootstrap
5. Intervalos de Confiança
6. Distribuição Normal
7. Distribuições de Cauda Longa
8. Distribuição t de Student
9. Distribuição Binomial
10. Distribuição Qui-Quadrado
11. Distribuição F
12. Distribuição de Poisson e Relacionadas

**Cap. 3 — Experimentos Estatísticos e Testes de Significância**
1. Teste A/B
2. Testes de Hipótese
3. Reamostragem
4. Significância Estatística e Valores-p
5. Testes t
6. Testes Múltiplos
7. Graus de Liberdade
8. ANOVA
9. Teste Qui-Quadrado
10. Algoritmo Multi-Armed Bandit
11. Poder e Tamanho da Amostra

**Cap. 4 — Regressão e Predição**
1. Regressão Linear Simples
2. Regressão Linear Múltipla
3. Predição com Regressão
4. Variáveis Fatoriais na Regressão
5. Interpretando a Equação de Regressão
6. Diagnóstico de Regressão
7. Regressão Polinomial e Splines

### Estado inicial do conteúdo

São 38 seções ao todo (8 + 12 + 11 + 7), mais 4 `index.qmd` de capítulo.

**37 seções nascem como stubs:** título, um `callout-note` apontando a seção correspondente do livro-texto, e marcação de "em construção". Todas já registradas no `_quarto.yml`, entregando a navegação completa do semestre desde o primeiro commit; o conteúdo é preenchido incrementalmente.

**1 seção sai completa:** `content/cap01/03-estimativas-localizacao.qmd`, com carga de `state.csv`, média, média aparada, mediana, mediana ponderada e um gráfico. Ela existe para provar a toolchain inteira ponta a ponta: dados → chunk Python → plot → freeze → container → CI → gh-pages. Sem ela, o scaffolding seria estrutura não verificada.

## Dados

Os 14 CSVs usados pelos capítulos 1–4 são versionados em `dados/` (~34 MB), com os **nomes originais preservados**, para que o código Python do livro-texto rode literalmente.

| Arquivo | Usado em |
|---|---|
| `state.csv` | 1.3, 1.4, 1.5 |
| `dfw_airline.csv` | 1.6 |
| `sp500_data.csv.gz` | 1.7, 2.7 |
| `sp500_sectors.csv` | 1.7 |
| `kc_tax.csv.gz` | 1.8 |
| `lc_loans.csv` | 1.8 |
| `airline_stats.csv` | 1.8 |
| `loans_income.csv` | 2.3, 2.4, 2.5 |
| `web_page_data.csv` | 3.1, 3.3 |
| `four_sessions.csv` | 3.8 |
| `click_rates.csv` | 3.9 |
| `imanishi_data.csv` | 3.9 |
| `LungDisease.csv` | 4.1 |
| `house_sales.csv` | 4.2–4.7 |

Versionar (em vez de baixar sob demanda) garante preview offline e CI determinístico, sem dependência de rede. `dados/README.md` credita a fonte e a licença do repositório original.

## Ambiente — duas camadas travadas

```
pyproject.toml + uv.lock      ← fonte única das versões Python
        │ uv sync --frozen
        ▼
Dockerfile                    ← + SO, locale pt_BR.UTF-8, Quarto
        │
        ├── compose.yaml           preview local em :4200 (bind mount, hot reload)
        └── .devcontainer/         VS Code / GitHub Codespaces (um clique)
```

Docker sozinho **não** dá reprodutibilidade de dependências — um `pip install pandas` dentro do Dockerfile ainda flutua a cada rebuild. Por isso o container **consome** o lockfile (`uv sync --frozen`) em vez de substituí-lo. As duas camadas — SO e pacotes — ficam travadas, e existe uma única lista de dependências, sem risco de deriva entre local e CI.

Dependências (apenas o necessário para os caps. 1–4): `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`, `wquantiles`, `adjustText`, `pygam`, `dmba`, `jupyter`.

Ficam **de fora** `xgboost`, `imblearn`, `prince` e `pydotplus` — são exclusivos dos capítulos 5–7 e mantê-los fora deixa a imagem leve. Quando/se o escopo crescer, entram no `pyproject.toml`.

`jupyter` é requisito do engine Jupyter do Quarto (precisa de `ipykernel`, `nbclient`, `nbformat`).

Um `Makefile` expõe os atalhos: `make preview`, `make render`, `make lock`, `make build`.

## CI/CD

Um único workflow (`.github/workflows/quarto-render.yml`), dois jobs. Um workflow só — em vez de dois separados — elimina a corrida "a imagem ainda não existe no GHCR" no primeiro push.

```
job: build-image
  docker build (cache-from/to: type=gha)
  push → ghcr.io/bragad/undf-bases3-estatistica-202602:latest
  └─ cache hit típico: ~15s

job: render          (needs: build-image)
  container: ghcr.io/bragad/undf-bases3-estatistica-202602:latest
    └─ container.credentials com GITHUB_TOKEN (pacote GHCR é privado por padrão)
  quarto render → _book/
  upload-artifact

job: publish         (needs: render, runner limpo — fora do container)
  download-artifact
  publish _book/ → branch gh-pages
```

A publicação roda **fora** do container de propósito: as ações de git dentro de imagem esbarram no atrito conhecido de `safe.directory` e de `git` ausente. Renderizar no container e publicar no runner dá o melhor dos dois.

Permissões necessárias: `packages: write` (push GHCR) e `contents: write` (push gh-pages).

O locale `pt_BR.UTF-8` é definido **na imagem**, não no workflow — é propriedade do ambiente, não do CI.

## Regra: semear todo chunk estocástico

Boa parte do livro-texto é bootstrap, permutação e amostragem aleatória. Sem semente fixa, cada `quarto render` produz números e gráficos diferentes: o `freeze` perde o sentido, o diff do site publicado vira ruído e o material didático deixa de bater com o que o aluno vê.

**Todo chunk com RNG usa semente explícita** — `np.random.default_rng(42)`, `random_state=42`, `sample(..., random_state=42)`. Esta regra vai no CLAUDE.md.

## Documentação para agentes

Só `CLAUDE.md` — decisão explícita de não manter `AGENTS.md` espelhado; `CLAUDE.md` é fonte única de instruções para agentes. Cobre:

- Comandos: `uv sync`, `make preview`, `docker compose up`, `quarto render`
- Estrutura `content/capXX/` e a regra de registro obrigatório no `_quarto.yml`
- `execute-dir: project` → caminhos de dados uniformes (`dados/state.csv`)
- Regra das sementes nos chunks estocásticos
- Escopo caps. 1–4 e a fronteira com Bases 5
- Classes CSS `.conceito` / `.exemplo` e o uso do spoiler com senha
- Formato do CI e o fato de que `_book/` e `_freeze/` são artefatos locais gitignorados

## Ativos herdados do repo de referência

Copiados e adaptados: `styles.css` (classes `.conceito`, `.exemplo`, dark mode, spoiler), `spoiler.html` (conteúdo protegido por senha — útil para gabaritos), `images/logo-undf.png`, tema `cosmo`/`darkly`, `page-navigation`, TOC com `toc-depth: 4`.

`references.bib` é novo: `bruce2020` como referência principal, mais clássicos de apoio (Montgomery & Runger, Wasserman, Efron & Tibshirani, James et al.).

## Fora de escopo

- Conteúdo dos capítulos 5–7 (vai para Bases 5 — Ciência de Dados)
- Redação do conteúdo das 37 seções em stub (feita incrementalmente depois)
- Atividades, listas de exercícios e gabaritos (estrutura `atividades/` do repo de referência não é replicada agora; entra quando houver a primeira atividade)
