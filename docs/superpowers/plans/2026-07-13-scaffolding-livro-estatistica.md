# Scaffolding do Livro "Bases 3 — Estatística" — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar o repositório de um livro/site Quarto em Python para a disciplina Bases 3 — Estatística (UnDF), com ambiente containerizado e publicação automática no GitHub Pages.

**Architecture:** Livro Quarto (`type: book`, engine `jupyter`) cujo conteúdo espelha os capítulos 1–4 de *Practical Statistics for Data Scientists*. O ambiente é travado em duas camadas: `pyproject.toml` + `uv.lock` fixam as versões Python, e o `Dockerfile` consome esse lock (`uv sync --frozen`) por cima de um SO fixo com Quarto e locale `pt_BR`. O mesmo container renderiza localmente e no CI; a publicação em `gh-pages` acontece fora dele.

**Tech Stack:** Quarto 1.9.38 · Python 3.12 · uv · Docker + Compose · pandas/numpy/scipy/statsmodels/scikit-learn/matplotlib/seaborn · GitHub Actions · GHCR

**Spec:** `docs/superpowers/specs/2026-07-13-scaffolding-livro-estatistica-design.md`

## Global Constraints

- **Idioma do conteúdo:** português brasileiro. Código, nomes de variáveis e comentários nos chunks também em português (`estado`, `media_aparada`), exceto nomes de colunas dos CSVs, que são preservados do original (`Population`, `Murder.Rate`).
- **Escopo:** capítulos 1–4 do livro-texto. Nada de Classificação, ML Estatístico ou Clustering (caps. 5–7) — esses pertencem a *Bases 5 — Ciência de Dados*.
- **Registro obrigatório:** todo `.qmd` novo precisa entrar em `_quarto.yml` sob `book.chapters`. Arquivo não registrado não aparece no livro.
- **Caminhos de dados:** sempre relativos à raiz do projeto (`dados/state.csv`), nunca `../../dados/`. Isso é garantido por `project: execute-dir: project`.
- **Sementes:** todo chunk com RNG (bootstrap, permutação, amostragem) usa semente explícita — `np.random.default_rng(42)` ou `random_state=42`. Sem isso, cada render muda os números do livro e o `freeze` perde o sentido.
- **Nomes literais** (usados em `_quarto.yml`, CI e Docker):
  - Repositório: `BragaD/UnDF-Bases3-Estatistica-202602`
  - Site: `https://BragaD.github.io/UnDF-Bases3-Estatistica-202602`
  - Imagem GHCR: `ghcr.io/bragad/undf-bases3-estatistica-202602` — **minúsculas obrigatórias**; o GHCR rejeita maiúsculas, então o owner NÃO pode vir de `${{ github.repository_owner }}` (que resolveria para `BragaD`).
- **`_book/` e `_freeze/` são artefatos locais gitignorados.** `docs/` NÃO é gitignorado — guarda specs e planos.

---

## Estrutura de Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `pyproject.toml` | Dependências Python declaradas |
| `uv.lock` | Versões exatas travadas (gerado, versionado) |
| `.python-version` | Fixa Python 3.12 para o `uv` |
| `Dockerfile` | SO + locale pt_BR + Quarto + `uv sync --frozen` |
| `compose.yaml` | Preview local em `:4200` com bind mount |
| `Makefile` | Atalhos: `preview`, `render`, `build`, `shell`, `lock`, `check`, `clean` |
| `.devcontainer/devcontainer.json` | VS Code / GitHub Codespaces |
| `_quarto.yml` | Config mestre: capítulos, tema, engine, `execute-dir` |
| `index.qmd` | Página inicial do livro |
| `styles.css` | Classes `.conceito`, `.exemplo`, dark mode, spoiler |
| `spoiler.html` | JS do conteúdo protegido por senha |
| `references.bib` | Bibliografia |
| `images/logo-undf.png` | Logo (copiado do repo de referência) |
| `dados/*.csv` | 14 datasets dos caps. 1–4 |
| `content/capNN/index.qmd` | Visão geral + objetivos + tabela de seções |
| `content/capNN/NN-*.qmd` | Uma seção do livro por arquivo |
| `.github/workflows/quarto-render.yml` | Build da imagem → render no container → publish |
| `CLAUDE.md` / `AGENTS.md` | Instruções para agentes |
| `README.md` | Instruções para humanos |

---

## Task 1: Ambiente Python travado

**Files:**
- Create: `pyproject.toml`
- Create: `.python-version`
- Create: `.gitignore`
- Generate: `uv.lock`

**Interfaces:**
- Produces: `uv.lock` (consumido pelo `Dockerfile` na Task 2); ambiente com `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `matplotlib`, `seaborn`, `wquantiles`, `adjustText`, `pygam`, `dmba`, `jupyter`.

- [ ] **Step 1: Criar `.python-version`**

```
3.12
```

- [ ] **Step 2: Criar `pyproject.toml`**

Sem limites superiores de versão: o `uv.lock` é quem trava. Limites superiores aqui só criariam conflito de resolução sem ganho.

```toml
[project]
name = "bases3-estatistica"
version = "0.1.0"
description = "Livro Quarto — Bases 3: Estatística (UnDF)"
requires-python = ">=3.12"
dependencies = [
    "pandas",
    "numpy",
    "scipy",
    "statsmodels",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "wquantiles",
    "adjustText",
    "pygam",
    "dmba",
    "jupyter",
]

[tool.uv]
package = false
```

`jupyter` não é opcional: é o que o engine Jupyter do Quarto usa para executar os chunks (`ipykernel`, `nbclient`, `nbformat`).

- [ ] **Step 3: Criar `.gitignore`**

`docs/` fica **fora** desta lista de propósito — é onde moram specs e planos.

```gitignore
# Quarto
/.quarto/
/_book/
/_freeze/

# Python
.venv/
__pycache__/
*.py[cod]
.ipynb_checkpoints/
**/*.quarto_ipynb

# Ambiente
.env

# macOS
.DS_Store

# Editores
.vscode/

# Claude Code — preferências locais da máquina
.claude/settings.local.json
```

- [ ] **Step 4: Gerar o lock e verificar que resolve**

Run: `uv lock`
Expected: cria `uv.lock` sem erro. Se houver conflito de resolução (candidato mais provável: `pygam` ou `dmba` restringindo `numpy`/`scipy`), relaxe fixando o pacote conflitante a uma versão compatível no `pyproject.toml` e rode `uv lock` de novo — não invente `--resolution=lowest`.

- [ ] **Step 5: Sincronizar e verificar que todos os imports funcionam**

Run:
```bash
uv sync
uv run python -c "
import pandas, numpy, scipy, statsmodels, sklearn, matplotlib, seaborn, wquantiles, pygam, dmba, adjustText
from scipy.stats import trim_mean
print('todos os imports ok')
print('pandas', pandas.__version__, '| numpy', numpy.__version__, '| scipy', scipy.__version__)
"
```
Expected: imprime `todos os imports ok` seguido das versões. Nenhum `ModuleNotFoundError`.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml uv.lock .python-version .gitignore
git commit -m "build: ambiente Python travado com uv"
```

---

## Task 2: Container reprodutível

**Files:**
- Create: `Dockerfile`
- Create: `compose.yaml`
- Create: `Makefile`
- Create: `.devcontainer/devcontainer.json`

**Interfaces:**
- Consumes: `pyproject.toml` e `uv.lock` da Task 1.
- Produces: imagem local `bases3-estatistica:local`; comandos `make preview`, `make render`, `make shell`, `make check`.

- [ ] **Step 1: Criar `Dockerfile`**

Dois pontos não óbvios, ambos deliberados:

1. **`UV_PROJECT_ENVIRONMENT=/opt/venv`** — o venv NÃO pode ficar em `/livro/.venv`. O `compose.yaml` faz bind mount do projeto do host sobre `/livro`, o que esconderia qualquer coisa que a imagem tivesse criado ali. Em `/opt/venv` ele sobrevive ao mount.
2. **`ARG TARGETARCH`** — o Quarto publica `.deb` separados para `amd64` e `arm64`. O CI roda amd64; o Mac do autor é arm64. O BuildKit preenche `TARGETARCH` automaticamente com exatamente os nomes que o Quarto usa.

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG QUARTO_VERSION=1.9.38
ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    QUARTO_PYTHON=/opt/venv/bin/python \
    MPLBACKEND=Agg

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git locales \
    && sed -i '/^# *pt_BR.UTF-8/s/^# *//' /etc/locale.gen \
    && locale-gen \
    && curl -fsSL -o /tmp/quarto.deb \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${TARGETARCH}.deb" \
    && apt-get install -y --no-install-recommends /tmp/quarto.deb \
    && rm -f /tmp/quarto.deb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /livro

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen

EXPOSE 4200

CMD ["quarto", "preview", "--host", "0.0.0.0", "--port", "4200", "--no-browser"]
```

- [ ] **Step 2: Criar `compose.yaml`**

`build:` em vez de `image:` puxado do GHCR — assim o Mac arm64 constrói sua própria imagem nativa e não há incompatibilidade de arquitetura com a imagem amd64 do CI.

```yaml
services:
  livro:
    build:
      context: .
    image: bases3-estatistica:local
    ports:
      - "4200:4200"
    volumes:
      - .:/livro
```

- [ ] **Step 3: Criar `Makefile`**

Atenção: as receitas de Makefile precisam de **TAB**, não espaços.

```makefile
.DEFAULT_GOAL := help
COMPOSE := docker compose
RUN := $(COMPOSE) run --rm --no-deps livro

help: ## Mostra esta ajuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

build: ## Constrói a imagem Docker
	$(COMPOSE) build

preview: ## Preview com hot-reload em http://localhost:4200
	$(COMPOSE) up

render: ## Renderiza o livro para _book/
	$(RUN) quarto render

shell: ## Abre um shell dentro do container
	$(RUN) bash

check: ## Diagnóstico do Quarto dentro do container
	$(RUN) quarto check

lock: ## Regenera o uv.lock a partir do pyproject.toml
	uv lock

clean: ## Remove artefatos de render
	rm -rf _book _freeze .quarto

.PHONY: help build preview render shell check lock clean
```

- [ ] **Step 4: Criar `.devcontainer/devcontainer.json`**

```json
{
  "name": "Bases 3 — Estatística",
  "dockerComposeFile": "../compose.yaml",
  "service": "livro",
  "workspaceFolder": "/livro",
  "overrideCommand": true,
  "forwardPorts": [4200],
  "customizations": {
    "vscode": {
      "extensions": [
        "quarto.quarto",
        "ms-python.python",
        "ms-toolsai.jupyter"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/opt/venv/bin/python"
      }
    }
  }
}
```

- [ ] **Step 5: Construir a imagem**

Run: `DOCKER_BUILDKIT=1 make build`
Expected: build conclui sem erro. (BuildKit é necessário para `TARGETARCH`; o Compose v2 já o usa por padrão, a variável é cinto e suspensório para o Docker 20.10.)

Se falhar em `quarto.deb` com 404, confirme o nome do arquivo publicado:
`curl -sIL -o /dev/null -w "%{http_code}\n" https://github.com/quarto-dev/quarto-cli/releases/download/v1.9.38/quarto-1.9.38-linux-arm64.deb`

- [ ] **Step 6: Verificar que Quarto e Python coexistem no container**

Run:
```bash
docker compose run --rm --no-deps livro bash -lc '
  quarto --version
  which python
  python -c "import pandas, statsmodels, wquantiles; print(\"imports ok\")"
  locale | head -1
'
```
Expected:
```
1.9.38
/opt/venv/bin/python
imports ok
LANG=pt_BR.UTF-8
```

O `which python` apontando para `/opt/venv/bin/python` é a verificação que importa: prova que o venv sobreviveu ao bind mount.

- [ ] **Step 7: Commit**

```bash
git add Dockerfile compose.yaml Makefile .devcontainer/devcontainer.json
git commit -m "build: container reprodutivel com Quarto e Python"
```

---

## Task 3: Esqueleto Quarto renderizável

Esta task entrega o menor livro que renderiza de ponta a ponta — só a página inicial. Os capítulos entram nas Tasks 5 e 6. Separar assim significa que, se o render quebrar mais adiante, você sabe que a culpa é do conteúdo, não da configuração.

**Files:**
- Create: `_quarto.yml`
- Create: `index.qmd`
- Create: `styles.css`
- Create: `spoiler.html`
- Create: `references.bib`
- Create: `images/logo-undf.png` (cópia)

**Interfaces:**
- Produces: `_quarto.yml` com `book.chapters` contendo apenas `index.qmd` — as Tasks 5 e 6 acrescentam as partes dos capítulos. Classes CSS `.conceito` e `.exemplo`. Chave de citação `@bruce2020`.

- [ ] **Step 1: Copiar os ativos visuais do repo de referência**

`styles.css` e `spoiler.html` são reaproveitados sem alteração de comportamento (só o comentário de cabeçalho do CSS muda).

```bash
mkdir -p images
REF=../../202601/BasesIV_EngSoft_BD
cp "$REF/images/logo-undf.png" images/logo-undf.png
cp "$REF/spoiler.html" spoiler.html
cp "$REF/styles.css" styles.css
sed -i '' '1s|.*|/* ── Bases 3 — Estatística ── */|' styles.css
```

Verifique: `head -1 styles.css` deve imprimir `/* ── Bases 3 — Estatística ── */`, e `ls -la images/logo-undf.png` deve mostrar ~10 KB.

- [ ] **Step 2: Criar `_quarto.yml`**

`execute-dir` fica sob `project:`, **não** sob `execute:` — essa é a chave que faz `dados/state.csv` funcionar de dentro de `content/cap01/`.

```yaml
project:
  type: book
  output-dir: _book
  execute-dir: project

execute:
  freeze: auto

jupyter: python3

lang: pt

book:
  title: "Bases 3"
  subtitle: "Estatística"
  site-url: "https://BragaD.github.io/UnDF-Bases3-Estatistica-202602"
  repo-url: "https://github.com/BragaD/UnDF-Bases3-Estatistica-202602"
  repo-actions: [issue]
  navbar:
    logo: images/logo-undf.png
    logo-alt: "Logo UnDF"
    title: "Bases 3 — Estatística"
  date: today
  date-format: "DD/MM/YYYY"
  chapters:
    - text: "Início"
      href: index.qmd

page-navigation: true

page-footer:
  border: true
  left: "UnDF — Engenharia de Software e Sistemas de Informação — Estatística — 2026.2"
  right:
    - icon: github
      href: "https://github.com/BragaD/UnDF-Bases3-Estatistica-202602"

format:
  html:
    theme:
      light: cosmo
      dark: darkly
    css: styles.css
    number-sections: false
    include-after-body: spoiler.html
    toc: true
    toc-depth: 4
    toc-title: "Nesta página"
    link-external-icon: true
    link-external-newwindow: true
    code-copy: true
    code-overflow: wrap

bibliography: references.bib

editor: source
code-annotations: hover

author:
  - name: "Douglas Braga"
    email: "douglas.braga@undf.edu.br"
```

- [ ] **Step 3: Criar `references.bib`**

```bibtex
@book{bruce2020,
  author    = {Bruce, Peter and Bruce, Andrew and Gedeck, Peter},
  title     = {Practical Statistics for Data Scientists: 50+ Essential Concepts Using R and Python},
  edition   = {2nd},
  publisher = {O'Reilly Media},
  year      = {2020},
  isbn      = {978-1-492-07294-2}
}

@book{montgomery2018,
  author    = {Montgomery, Douglas C. and Runger, George C.},
  title     = {Applied Statistics and Probability for Engineers},
  edition   = {7th},
  publisher = {Wiley},
  year      = {2018},
  isbn      = {978-1-119-40036-3}
}

@book{wasserman2004,
  author    = {Wasserman, Larry},
  title     = {All of Statistics: A Concise Course in Statistical Inference},
  publisher = {Springer},
  year      = {2004},
  isbn      = {978-0-387-40272-7}
}

@book{efron1993,
  author    = {Efron, Bradley and Tibshirani, Robert J.},
  title     = {An Introduction to the Bootstrap},
  publisher = {Chapman and Hall/CRC},
  year      = {1993},
  isbn      = {978-0-412-04231-7}
}

@book{james2021,
  author    = {James, Gareth and Witten, Daniela and Hastie, Trevor and Tibshirani, Robert},
  title     = {An Introduction to Statistical Learning with Applications in R},
  edition   = {2nd},
  publisher = {Springer},
  year      = {2021},
  isbn      = {978-1-0716-1417-4}
}

@book{mckinney2022,
  author    = {McKinney, Wes},
  title     = {Python for Data Analysis},
  edition   = {3rd},
  publisher = {O'Reilly Media},
  year      = {2022},
  isbn      = {978-1-098-10403-0}
}
```

- [ ] **Step 4: Criar `index.qmd`**

```markdown
# Bem-vindo {.unnumbered}

Este é o material de apoio da disciplina **Bases 3 — Estatística**, oferecida aos cursos de **Engenharia de Software** e **Sistemas de Informação** da UnDF.

## Sobre a Disciplina

A disciplina apresenta a estatística do ponto de vista de quem constrói software e trabalha com dados: menos fórmulas decoradas, mais raciocínio sobre o que os dados dizem e o que eles não dizem. Todos os exemplos são em **Python**.

Os temas são:

- Análise exploratória de dados: estimativas de localização, variabilidade, distribuição e correlação
- Amostragem, distribuições amostrais, bootstrap e intervalos de confiança
- Experimentos estatísticos: testes A/B, testes de hipótese, valores-p, ANOVA e qui-quadrado
- Regressão e predição: regressão linear simples e múltipla, diagnóstico e splines

## Material Bibliográfico

O livro-texto da disciplina é:

> @bruce2020

O código e os conjuntos de dados originais estão em [github.com/gedeck/practical-statistics-for-data-scientists](https://github.com/gedeck/practical-statistics-for-data-scientists). Esta disciplina cobre os **capítulos 1 a 4**; os capítulos 5 a 7, sobre aprendizado de máquina, são tratados em *Bases 5 — Ciência de Dados*.

## Como Usar Este Material

Cada capítulo traz:

- Conceitos com exemplos executáveis em Python
- Código que roda sobre conjuntos de dados reais, incluídos no repositório
- Exercícios de fixação

O ambiente completo (Python, bibliotecas e Quarto) está empacotado em um container Docker — veja o `README.md` para rodar o livro na sua máquina.

## Licença {.unnumbered}

Material disponibilizado para fins educacionais. Os dados e exemplos originais são de autoria de Bruce, Bruce e Gedeck [@bruce2020].
```

- [ ] **Step 5: Renderizar o esqueleto**

Run: `make render`
Expected: termina sem erro e cria `_book/index.html`.

Verifique: `test -f _book/index.html && echo "index gerado"` → imprime `index gerado`.

- [ ] **Step 6: Verificar que o CSS e o logo entraram no build**

Run:
```bash
grep -c "conceito" _book/styles.css
test -f _book/images/logo-undf.png && echo "logo publicado"
```
Expected: contagem `>= 1` para `conceito`, e `logo publicado`.

- [ ] **Step 7: Commit**

```bash
git add _quarto.yml index.qmd styles.css spoiler.html references.bib images/logo-undf.png
git commit -m "feat: esqueleto do livro Quarto com tema e identidade da UnDF"
```

---

## Task 4: Conjuntos de dados

**Files:**
- Create: `dados/` (14 arquivos)
- Create: `dados/README.md`

**Interfaces:**
- Produces: `dados/state.csv` (consumido pela Task 5) e mais 13 arquivos consumidos pelas seções ainda a escrever. Nomes originais preservados para que o código do livro-texto rode literalmente.

- [ ] **Step 1: Baixar os 14 arquivos dos capítulos 1–4**

Os 5 arquivos restantes do repositório original (`loan_data.csv.gz`, `loan200.csv`, `loan3000.csv`, `full_train_set.csv.gz`, `housetasks.csv`) são exclusivos dos capítulos 5–7 e ficam de fora.

```bash
mkdir -p dados
BASE="https://raw.githubusercontent.com/gedeck/practical-statistics-for-data-scientists/master/data"
for f in state.csv dfw_airline.csv sp500_data.csv.gz sp500_sectors.csv \
         kc_tax.csv.gz lc_loans.csv airline_stats.csv loans_income.csv \
         web_page_data.csv four_sessions.csv click_rates.csv imanishi_data.csv \
         LungDisease.csv house_sales.csv; do
  curl -fsSL -o "dados/$f" "$BASE/$f" && echo "ok  $f"
done
```
Expected: 14 linhas `ok <arquivo>`, sem nenhum erro do curl.

- [ ] **Step 2: Verificar integridade — contagem e o conteúdo de `state.csv`**

Run:
```bash
ls dados | wc -l
du -sh dados
head -2 dados/state.csv
```
Expected:
```
14
 33M	dados        (aproximadamente)
"State","Population","Murder.Rate","Abbreviation"
"Alabama",4779736,5.7,"AL"
```

O cabeçalho de `state.csv` importa: a Task 5 depende das colunas `Population` e `Murder.Rate` (com ponto, não underscore).

- [ ] **Step 3: Criar `dados/README.md`**

````markdown
# Conjuntos de Dados

Os arquivos deste diretório vêm do repositório oficial do livro-texto:

**Bruce, Bruce & Gedeck — *Practical Statistics for Data Scientists*, 2ª ed. (O'Reilly, 2020)**
<https://github.com/gedeck/practical-statistics-for-data-scientists>

Os nomes originais foram preservados para que o código do livro rode sem adaptação.

Estão aqui apenas os 14 conjuntos usados pelos **capítulos 1–4**, que são o escopo desta
disciplina. Os demais (`loan_data.csv.gz`, `loan200.csv`, `loan3000.csv`,
`full_train_set.csv.gz`, `housetasks.csv`) pertencem aos capítulos 5–7 e não foram incluídos.

| Arquivo | Usado em |
|---|---|
| `state.csv` | 1.3 Estimativas de Localização, 1.4 Variabilidade, 1.5 Distribuição |
| `dfw_airline.csv` | 1.6 Dados Binários e Categóricos |
| `sp500_data.csv.gz` | 1.7 Correlação, 2.7 Caudas Longas |
| `sp500_sectors.csv` | 1.7 Correlação |
| `kc_tax.csv.gz` | 1.8 Duas ou Mais Variáveis |
| `lc_loans.csv` | 1.8 Duas ou Mais Variáveis |
| `airline_stats.csv` | 1.8 Duas ou Mais Variáveis |
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

```python
estado = pd.read_csv("dados/state.csv")
```

Nunca `../../dados/state.csv`.
````

- [ ] **Step 4: Commit**

```bash
git add dados/
git commit -m "data: conjuntos de dados dos capitulos 1-4"
```

---

## Task 5: Seção completa — prova da toolchain

Esta é a task que realmente verifica o scaffolding. Uma seção escrita por inteiro exercita a cadeia toda: leitura de dados pelo caminho de projeto, execução de chunk Python, gráfico matplotlib, cache do `freeze`, tudo dentro do container. Se ela renderiza com os números certos, a infraestrutura está provada.

**Files:**
- Create: `content/cap01/index.qmd`
- Create: `content/cap01/03-estimativas-localizacao.qmd`
- Modify: `_quarto.yml` (registrar a parte do Capítulo 1)

**Interfaces:**
- Consumes: `dados/state.csv` (Task 4); classes `.conceito`/`.exemplo` e `@bruce2020` (Task 3).
- Produces: o padrão de seção que as 37 restantes seguem — título `#`, `callout-note` citando a seção do livro, chunk `setup` com `include: false`, prosa e código intercalados.

- [ ] **Step 1: Criar `content/cap01/index.qmd`**

```markdown
# Análise Exploratória de Dados

::: {.callout-note}
Este capítulo é baseado no Capítulo 1 de @bruce2020.
:::

A estatística clássica nasceu preocupada com inferência: tirar conclusões sobre uma população grande a partir de uma amostra pequena. A análise exploratória de dados, proposta por John Tukey em 1962, inverte a ênfase — antes de testar qualquer hipótese, **olhe para os dados**.

Ao final deste capítulo, você será capaz de:

- Distinguir os tipos de dados estruturados e por que essa distinção importa para o software
- Resumir uma variável por estimativas de localização, sabendo quando a média engana e a mediana não
- Medir a dispersão dos dados e reconhecer a diferença entre desvio-padrão e desvio absoluto mediano
- Explorar a distribuição de uma variável com percentis, boxplots, histogramas e densidade
- Tratar dados binários e categóricos
- Medir e visualizar a correlação entre variáveis, e reconhecer suas armadilhas
- Explorar relações entre duas ou mais variáveis, numéricas e categóricas

## Seções

| Seção | Tópico |
|---|---|
| [1.1](01-dados-estruturados.qmd) | Elementos de Dados Estruturados |
| [1.2](02-dados-retangulares.qmd) | Dados Retangulares |
| [1.3](03-estimativas-localizacao.qmd) | Estimativas de Localização |
| [1.4](04-estimativas-variabilidade.qmd) | Estimativas de Variabilidade |
| [1.5](05-distribuicao-dados.qmd) | Explorando a Distribuição dos Dados |
| [1.6](06-dados-binarios-categoricos.qmd) | Explorando Dados Binários e Categóricos |
| [1.7](07-correlacao.qmd) | Correlação |
| [1.8](08-duas-ou-mais-variaveis.qmd) | Explorando Duas ou Mais Variáveis |
```

- [ ] **Step 2: Criar `content/cap01/03-estimativas-localizacao.qmd`**

````markdown
# Estimativas de Localização

::: {.callout-note}
Esta seção corresponde à seção 1.3 de @bruce2020.
:::

```{python}
#| label: setup
#| include: false
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import trim_mean
import wquantiles

plt.rcParams["figure.figsize"] = (7, 4)
```

Uma variável com centenas ou milhares de valores é impossível de compreender olhando linha a linha. O primeiro passo da exploração é resumi-la por um **valor típico**: uma estimativa de onde a maior parte dos dados está.

Isso parece trivial — "é só tirar a média" — e é exatamente por parecer trivial que dá errado tantas vezes.

## Os dados

Vamos usar população e taxa de homicídios (por 100.000 habitantes) dos 50 estados norte-americanos.

```{python}
#| label: carrega
estado = pd.read_csv("dados/state.csv")
estado.head()
```

::: {.conceito}
Note o caminho: `dados/state.csv`, e não `../../dados/state.csv`. O `_quarto.yml` define `execute-dir: project`, então o diretório de trabalho de todo chunk é a raiz do projeto, independentemente de onde o arquivo `.qmd` esteja.
:::

## Média

A **média** é a soma dos valores dividida pelo número de observações:

$$\bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$

```{python}
#| label: media
media = estado["Population"].mean()
print(f"Média: {media:,.1f}")
```

A média é sensível a valores extremos. A população da Califórnia (~37 milhões) e a do Wyoming (~564 mil) diferem por um fator de 66 — e a Califórnia puxa a média para cima sozinha.

## Média aparada

A **média aparada** descarta uma proporção fixa dos maiores e menores valores antes de calcular a média, o que a torna robusta a extremos:

$$\bar{x}_{\text{aparada}} = \frac{\sum_{i=p+1}^{n-p} x_{(i)}}{n - 2p}$$

```{python}
#| label: media-aparada
media_aparada = trim_mean(estado["Population"], 0.1)
print(f"Média aparada (10%): {media_aparada:,.1f}")
```

Aparar 10% de cada ponta remove os 5 estados mais populosos e os 5 menos populosos.

## Mediana

A **mediana** é o valor central dos dados ordenados. Ela depende apenas das observações do meio, então um valor extremo pode ser arbitrariamente grande sem movê-la.

```{python}
#| label: mediana
mediana = estado["Population"].median()
print(f"Mediana: {mediana:,.1f}")
```

::: {.exemplo}
A mediana é `{python} f"{mediana:,.0f}"` e a média é `{python} f"{media:,.0f}"` — a média é cerca de 39% maior. Essa diferença é a assinatura de uma distribuição assimétrica à direita, e é a razão pela qual reportar renda mediana e não renda média é a prática padrão.
:::

## Estimativas ponderadas

Nem toda observação merece o mesmo peso. Para a taxa de homicídios, tratar cada estado igualmente daria ao Wyoming a mesma influência que à Califórnia — mas eles representam números muito diferentes de pessoas.

A **média ponderada** corrige isso:

$$\bar{x}_w = \frac{\sum_{i=1}^{n} w_i x_i}{\sum_{i=1}^{n} w_i}$$

```{python}
#| label: ponderadas
media_pond = np.average(estado["Murder.Rate"], weights=estado["Population"])
mediana_pond = wquantiles.median(estado["Murder.Rate"], weights=estado["Population"])

print(f"Média simples     : {estado['Murder.Rate'].mean():.4f}")
print(f"Média ponderada   : {media_pond:.4f}")
print(f"Mediana ponderada : {mediana_pond:.4f}")
```

A média ponderada é a taxa de homicídios que uma pessoa média dos EUA enfrenta; a média simples é a taxa de um estado médio. São perguntas diferentes, com respostas diferentes.

## Comparando as estimativas

```{python}
#| label: fig-localizacao
#| fig-cap: "As três estimativas de localização sobre a distribuição de população dos estados."
fig, ax = plt.subplots()

ax.hist(estado["Population"] / 1e6, bins=20, color="#b0c4d8", edgecolor="white")
ax.axvline(media / 1e6, color="#c0392b", linestyle="-", linewidth=2, label=f"Média: {media/1e6:.1f}M")
ax.axvline(media_aparada / 1e6, color="#e67e22", linestyle="--", linewidth=2, label=f"Média aparada: {media_aparada/1e6:.1f}M")
ax.axvline(mediana / 1e6, color="#27ae60", linestyle=":", linewidth=2.5, label=f"Mediana: {mediana/1e6:.1f}M")

ax.set_xlabel("População (milhões)")
ax.set_ylabel("Número de estados")
ax.legend()
plt.tight_layout()
plt.show()
```

A média está à direita das outras duas, arrastada pela cauda de estados muito populosos. A média aparada e a mediana quase coincidem — é isso que "robusto a extremos" significa na prática.

## Resumo

| Estimativa | Valor | Robusta a extremos? |
|---|---|---|
| Média | `{python} f"{media:,.0f}"` | Não |
| Média aparada (10%) | `{python} f"{media_aparada:,.0f}"` | Sim |
| Mediana | `{python} f"{mediana:,.0f}"` | Sim |

::: {.conceito}
**Regra prática:** a média é o padrão, mas é frágil. Quando os dados têm cauda longa ou outliers plausíveis — renda, população, tempo de resposta de um servidor — a mediana ou a média aparada descrevem melhor o caso típico.
:::
````

- [ ] **Step 3: Registrar o Capítulo 1 no `_quarto.yml`**

Substitua o bloco `chapters:` (que hoje só tem `index.qmd`) por:

```yaml
  chapters:
    - text: "Início"
      href: index.qmd
    - part: "Capítulo 1: Análise Exploratória de Dados"
      chapters:
        - href: content/cap01/index.qmd
          text: "Visão Geral"
        - href: content/cap01/03-estimativas-localizacao.qmd
          text: "Estimativas de Localização"
```

As demais seções do Cap. 1 entram na Task 6, junto com os outros capítulos.

- [ ] **Step 4: Renderizar e conferir os números**

Run: `make render`
Expected: render conclui sem erro.

Run:
```bash
grep -o 'Média: [0-9,.]*' _book/content/cap01/03-estimativas-localizacao.html | head -1
grep -o 'Média aparada (10%): [0-9,.]*' _book/content/cap01/03-estimativas-localizacao.html | head -1
grep -o 'Mediana: [0-9,.]*' _book/content/cap01/03-estimativas-localizacao.html | head -1
```
Expected — estes são os valores reais de `state.csv`, conferidos contra o livro:
```
Média: 6,162,876.3
Média aparada (10%): 4,783,697.1
Mediana: 4,436,369.5
```

Se algum número divergir, **pare**: significa que o CSV não é o esperado ou que o `trim_mean` está sendo chamado errado. Não ajuste os valores esperados para caber no resultado.

- [ ] **Step 5: Verificar que o gráfico foi gerado e que o `freeze` funcionou**

Run:
```bash
grep -c "<img" _book/content/cap01/03-estimativas-localizacao.html
ls _freeze/content/cap01/
```
Expected: pelo menos 1 `<img>` (a figura), e um diretório `03-estimativas-localizacao` dentro de `_freeze/content/cap01/`.

Run `make render` de novo: deve terminar visivelmente mais rápido, sem reexecutar os chunks (é o cache do `freeze` agindo).

- [ ] **Step 6: Commit**

```bash
git add content/cap01/index.qmd content/cap01/03-estimativas-localizacao.qmd _quarto.yml
git commit -m "feat: capitulo 1 com a secao de estimativas de localizacao"
```

---

## Task 6: Estrutura completa dos capítulos

**Files:**
- Create: `scripts/gerar-stubs.sh`
- Create: 3 arquivos `content/capNN/index.qmd` (cap02, cap03, cap04)
- Create: 37 arquivos de seção em stub
- Modify: `_quarto.yml` (árvore completa)

**Interfaces:**
- Consumes: o padrão de seção estabelecido na Task 5.
- Produces: navegação completa do semestre; todos os 42 arquivos registrados no `_quarto.yml`.

- [ ] **Step 1: Criar os arquivos de seção em stub**

Cada stub tem título, o `callout-note` apontando a seção do livro, e um aviso de construção. O script abaixo gera os 37 (todos menos `cap01/03`, já escrito).

```bash
#!/usr/bin/env bash
set -euo pipefail

gerar_stub() {
  local caminho="$1" titulo="$2" secao="$3"
  cat > "$caminho" <<EOF
# ${titulo}

::: {.callout-note}
Esta seção corresponde à seção ${secao} de @bruce2020.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
EOF
  echo "ok  $caminho"
}

mkdir -p content/cap01 content/cap02 content/cap03 content/cap04

# Capítulo 1 — a seção 03 já existe e não é sobrescrita
gerar_stub content/cap01/01-dados-estruturados.qmd        "Elementos de Dados Estruturados"        "1.1"
gerar_stub content/cap01/02-dados-retangulares.qmd        "Dados Retangulares"                     "1.2"
gerar_stub content/cap01/04-estimativas-variabilidade.qmd "Estimativas de Variabilidade"           "1.4"
gerar_stub content/cap01/05-distribuicao-dados.qmd        "Explorando a Distribuição dos Dados"    "1.5"
gerar_stub content/cap01/06-dados-binarios-categoricos.qmd "Explorando Dados Binários e Categóricos" "1.6"
gerar_stub content/cap01/07-correlacao.qmd                "Correlação"                             "1.7"
gerar_stub content/cap01/08-duas-ou-mais-variaveis.qmd    "Explorando Duas ou Mais Variáveis"      "1.8"

# Capítulo 2
gerar_stub content/cap02/01-amostragem-aleatoria.qmd   "Amostragem Aleatória e Viés de Amostra"  "2.1"
gerar_stub content/cap02/02-vies-selecao.qmd           "Viés de Seleção"                         "2.2"
gerar_stub content/cap02/03-distribuicao-amostral.qmd  "Distribuição Amostral de uma Estatística" "2.3"
gerar_stub content/cap02/04-bootstrap.qmd              "Bootstrap"                               "2.4"
gerar_stub content/cap02/05-intervalos-confianca.qmd   "Intervalos de Confiança"                 "2.5"
gerar_stub content/cap02/06-distribuicao-normal.qmd    "Distribuição Normal"                     "2.6"
gerar_stub content/cap02/07-caudas-longas.qmd          "Distribuições de Cauda Longa"            "2.7"
gerar_stub content/cap02/08-distribuicao-t.qmd         "Distribuição t de Student"               "2.8"
gerar_stub content/cap02/09-distribuicao-binomial.qmd  "Distribuição Binomial"                   "2.9"
gerar_stub content/cap02/10-qui-quadrado.qmd           "Distribuição Qui-Quadrado"               "2.10"
gerar_stub content/cap02/11-distribuicao-f.qmd         "Distribuição F"                          "2.11"
gerar_stub content/cap02/12-poisson.qmd                "Distribuição de Poisson e Relacionadas"  "2.12"

# Capítulo 3
gerar_stub content/cap03/01-teste-ab.qmd               "Teste A/B"                               "3.1"
gerar_stub content/cap03/02-testes-hipotese.qmd        "Testes de Hipótese"                      "3.2"
gerar_stub content/cap03/03-reamostragem.qmd           "Reamostragem"                            "3.3"
gerar_stub content/cap03/04-significancia-valor-p.qmd  "Significância Estatística e Valores-p"   "3.4"
gerar_stub content/cap03/05-testes-t.qmd               "Testes t"                                "3.5"
gerar_stub content/cap03/06-testes-multiplos.qmd       "Testes Múltiplos"                        "3.6"
gerar_stub content/cap03/07-graus-liberdade.qmd        "Graus de Liberdade"                      "3.7"
gerar_stub content/cap03/08-anova.qmd                  "ANOVA"                                   "3.8"
gerar_stub content/cap03/09-teste-qui-quadrado.qmd     "Teste Qui-Quadrado"                      "3.9"
gerar_stub content/cap03/10-multi-armed-bandit.qmd     "Algoritmo Multi-Armed Bandit"            "3.10"
gerar_stub content/cap03/11-poder-tamanho-amostra.qmd  "Poder e Tamanho da Amostra"              "3.11"

# Capítulo 4
gerar_stub content/cap04/01-regressao-linear-simples.qmd  "Regressão Linear Simples"            "4.1"
gerar_stub content/cap04/02-regressao-linear-multipla.qmd "Regressão Linear Múltipla"           "4.2"
gerar_stub content/cap04/03-predicao.qmd                  "Predição com Regressão"              "4.3"
gerar_stub content/cap04/04-variaveis-fatoriais.qmd       "Variáveis Fatoriais na Regressão"    "4.4"
gerar_stub content/cap04/05-interpretando-equacao.qmd     "Interpretando a Equação de Regressão" "4.5"
gerar_stub content/cap04/06-diagnostico-regressao.qmd     "Diagnóstico de Regressão"            "4.6"
gerar_stub content/cap04/07-polinomial-splines.qmd        "Regressão Polinomial e Splines"      "4.7"

echo "---"
echo "stubs de seção criados: $(find content -name '*.qmd' ! -name 'index.qmd' | wc -l | tr -d ' ')"
```

Run: salve como `scripts/gerar-stubs.sh`, então `bash scripts/gerar-stubs.sh`
Expected: última linha imprime `stubs de seção criados: 38` (os 37 gerados + `cap01/03`, que já existia).

- [ ] **Step 2: Criar `content/cap02/index.qmd`**

```markdown
# Dados e Distribuições Amostrais

::: {.callout-note}
Este capítulo é baseado no Capítulo 2 de @bruce2020.
:::

Uma amostra nunca é a população. A pergunta central deste capítulo é: quanto do que vemos na amostra é sinal, e quanto é acidente do sorteio?

Ao final deste capítulo, você será capaz de:

- Reconhecer viés de amostra e viés de seleção, e por que amostras grandes não os corrigem
- Distinguir a distribuição dos **dados** da distribuição de uma **estatística**
- Explicar o Teorema Central do Limite e o erro padrão
- Usar o **bootstrap** para estimar a variabilidade de qualquer estatística, sem fórmula fechada
- Construir e interpretar intervalos de confiança
- Identificar as distribuições de referência — normal, t, binomial, qui-quadrado, F e Poisson — e quando cada uma aparece

## Seções

| Seção | Tópico |
|---|---|
| [2.1](01-amostragem-aleatoria.qmd) | Amostragem Aleatória e Viés de Amostra |
| [2.2](02-vies-selecao.qmd) | Viés de Seleção |
| [2.3](03-distribuicao-amostral.qmd) | Distribuição Amostral de uma Estatística |
| [2.4](04-bootstrap.qmd) | Bootstrap |
| [2.5](05-intervalos-confianca.qmd) | Intervalos de Confiança |
| [2.6](06-distribuicao-normal.qmd) | Distribuição Normal |
| [2.7](07-caudas-longas.qmd) | Distribuições de Cauda Longa |
| [2.8](08-distribuicao-t.qmd) | Distribuição t de Student |
| [2.9](09-distribuicao-binomial.qmd) | Distribuição Binomial |
| [2.10](10-qui-quadrado.qmd) | Distribuição Qui-Quadrado |
| [2.11](11-distribuicao-f.qmd) | Distribuição F |
| [2.12](12-poisson.qmd) | Distribuição de Poisson e Relacionadas |
```

- [ ] **Step 3: Criar `content/cap03/index.qmd`**

```markdown
# Experimentos Estatísticos e Testes de Significância

::: {.callout-note}
Este capítulo é baseado no Capítulo 3 de @bruce2020.
:::

O teste A/B é o experimento estatístico mais executado do mundo — e um dos mais mal interpretados. Este capítulo trata do desenho de experimentos e da pergunta que eles tentam responder: o efeito que eu vi é real, ou é ruído?

Ao final deste capítulo, você será capaz de:

- Desenhar um teste A/B e escolher a métrica antes de olhar o resultado
- Formular hipótese nula e alternativa, e decidir entre teste uni e bicaudal
- Usar **testes de permutação** para avaliar significância sem supor normalidade
- Interpretar corretamente um valor-p — e reconhecer as interpretações erradas mais comuns
- Aplicar testes t, ANOVA e qui-quadrado, sabendo qual cabe em qual situação
- Entender o problema dos **testes múltiplos** e por que ele produz descobertas falsas
- Calcular poder estatístico e tamanho de amostra necessário

## Seções

| Seção | Tópico |
|---|---|
| [3.1](01-teste-ab.qmd) | Teste A/B |
| [3.2](02-testes-hipotese.qmd) | Testes de Hipótese |
| [3.3](03-reamostragem.qmd) | Reamostragem |
| [3.4](04-significancia-valor-p.qmd) | Significância Estatística e Valores-p |
| [3.5](05-testes-t.qmd) | Testes t |
| [3.6](06-testes-multiplos.qmd) | Testes Múltiplos |
| [3.7](07-graus-liberdade.qmd) | Graus de Liberdade |
| [3.8](08-anova.qmd) | ANOVA |
| [3.9](09-teste-qui-quadrado.qmd) | Teste Qui-Quadrado |
| [3.10](10-multi-armed-bandit.qmd) | Algoritmo Multi-Armed Bandit |
| [3.11](11-poder-tamanho-amostra.qmd) | Poder e Tamanho da Amostra |
```

- [ ] **Step 4: Criar `content/cap04/index.qmd`**

```markdown
# Regressão e Predição

::: {.callout-note}
Este capítulo é baseado no Capítulo 4 de @bruce2020.
:::

A regressão é onde a estatística encontra a engenharia de software: é o primeiro modelo preditivo, e o alicerce de quase tudo que veio depois. Ela serve a dois propósitos que costumam ser confundidos — **explicar** uma relação e **prever** um valor.

Ao final deste capítulo, você será capaz de:

- Ajustar e interpretar uma regressão linear simples e múltipla
- Distinguir valores ajustados de resíduos, e usar ambos
- Selecionar variáveis com critérios como AIC, sem cair em sobreajuste
- Codificar variáveis categóricas (fatoriais) para entrar no modelo
- Interpretar coeficientes na presença de correlação entre preditores — e saber quando não interpretá-los
- Diagnosticar um modelo: outliers, pontos influentes, heterocedasticidade e não linearidade
- Estender a regressão com termos polinomiais e splines

## Seções

| Seção | Tópico |
|---|---|
| [4.1](01-regressao-linear-simples.qmd) | Regressão Linear Simples |
| [4.2](02-regressao-linear-multipla.qmd) | Regressão Linear Múltipla |
| [4.3](03-predicao.qmd) | Predição com Regressão |
| [4.4](04-variaveis-fatoriais.qmd) | Variáveis Fatoriais na Regressão |
| [4.5](05-interpretando-equacao.qmd) | Interpretando a Equação de Regressão |
| [4.6](06-diagnostico-regressao.qmd) | Diagnóstico de Regressão |
| [4.7](07-polinomial-splines.qmd) | Regressão Polinomial e Splines |
```

- [ ] **Step 5: Substituir o bloco `chapters:` do `_quarto.yml` pela árvore completa**

```yaml
  chapters:
    - text: "Início"
      href: index.qmd
    - part: "Capítulo 1: Análise Exploratória de Dados"
      chapters:
        - href: content/cap01/index.qmd
          text: "Visão Geral"
        - href: content/cap01/01-dados-estruturados.qmd
          text: "Elementos de Dados Estruturados"
        - href: content/cap01/02-dados-retangulares.qmd
          text: "Dados Retangulares"
        - href: content/cap01/03-estimativas-localizacao.qmd
          text: "Estimativas de Localização"
        - href: content/cap01/04-estimativas-variabilidade.qmd
          text: "Estimativas de Variabilidade"
        - href: content/cap01/05-distribuicao-dados.qmd
          text: "Explorando a Distribuição dos Dados"
        - href: content/cap01/06-dados-binarios-categoricos.qmd
          text: "Dados Binários e Categóricos"
        - href: content/cap01/07-correlacao.qmd
          text: "Correlação"
        - href: content/cap01/08-duas-ou-mais-variaveis.qmd
          text: "Duas ou Mais Variáveis"
    - part: "Capítulo 2: Dados e Distribuições Amostrais"
      chapters:
        - href: content/cap02/index.qmd
          text: "Visão Geral"
        - href: content/cap02/01-amostragem-aleatoria.qmd
          text: "Amostragem Aleatória e Viés"
        - href: content/cap02/02-vies-selecao.qmd
          text: "Viés de Seleção"
        - href: content/cap02/03-distribuicao-amostral.qmd
          text: "Distribuição Amostral"
        - href: content/cap02/04-bootstrap.qmd
          text: "Bootstrap"
        - href: content/cap02/05-intervalos-confianca.qmd
          text: "Intervalos de Confiança"
        - href: content/cap02/06-distribuicao-normal.qmd
          text: "Distribuição Normal"
        - href: content/cap02/07-caudas-longas.qmd
          text: "Distribuições de Cauda Longa"
        - href: content/cap02/08-distribuicao-t.qmd
          text: "Distribuição t de Student"
        - href: content/cap02/09-distribuicao-binomial.qmd
          text: "Distribuição Binomial"
        - href: content/cap02/10-qui-quadrado.qmd
          text: "Distribuição Qui-Quadrado"
        - href: content/cap02/11-distribuicao-f.qmd
          text: "Distribuição F"
        - href: content/cap02/12-poisson.qmd
          text: "Distribuição de Poisson"
    - part: "Capítulo 3: Experimentos Estatísticos e Testes de Significância"
      chapters:
        - href: content/cap03/index.qmd
          text: "Visão Geral"
        - href: content/cap03/01-teste-ab.qmd
          text: "Teste A/B"
        - href: content/cap03/02-testes-hipotese.qmd
          text: "Testes de Hipótese"
        - href: content/cap03/03-reamostragem.qmd
          text: "Reamostragem"
        - href: content/cap03/04-significancia-valor-p.qmd
          text: "Significância e Valores-p"
        - href: content/cap03/05-testes-t.qmd
          text: "Testes t"
        - href: content/cap03/06-testes-multiplos.qmd
          text: "Testes Múltiplos"
        - href: content/cap03/07-graus-liberdade.qmd
          text: "Graus de Liberdade"
        - href: content/cap03/08-anova.qmd
          text: "ANOVA"
        - href: content/cap03/09-teste-qui-quadrado.qmd
          text: "Teste Qui-Quadrado"
        - href: content/cap03/10-multi-armed-bandit.qmd
          text: "Multi-Armed Bandit"
        - href: content/cap03/11-poder-tamanho-amostra.qmd
          text: "Poder e Tamanho da Amostra"
    - part: "Capítulo 4: Regressão e Predição"
      chapters:
        - href: content/cap04/index.qmd
          text: "Visão Geral"
        - href: content/cap04/01-regressao-linear-simples.qmd
          text: "Regressão Linear Simples"
        - href: content/cap04/02-regressao-linear-multipla.qmd
          text: "Regressão Linear Múltipla"
        - href: content/cap04/03-predicao.qmd
          text: "Predição com Regressão"
        - href: content/cap04/04-variaveis-fatoriais.qmd
          text: "Variáveis Fatoriais"
        - href: content/cap04/05-interpretando-equacao.qmd
          text: "Interpretando a Equação"
        - href: content/cap04/06-diagnostico-regressao.qmd
          text: "Diagnóstico de Regressão"
        - href: content/cap04/07-polinomial-splines.qmd
          text: "Polinomial e Splines"
```

- [ ] **Step 6: Renderizar o livro completo**

Run: `make render`
Expected: conclui sem erro.

Run:
```bash
find _book/content -name '*.html' | wc -l
```
Expected: `42` (4 index de capítulo + 38 seções).

- [ ] **Step 7: Verificar que nenhum arquivo ficou órfão**

Todo `.qmd` de `content/` precisa estar em `_quarto.yml`. Este comando lista os que não estão — deve não imprimir nada:

```bash
for f in $(find content -name '*.qmd' | sort); do
  grep -q "$f" _quarto.yml || echo "ÓRFÃO (não registrado no _quarto.yml): $f"
done
echo "verificação concluída"
```
Expected: apenas `verificação concluída`, sem nenhuma linha `ÓRFÃO`.

- [ ] **Step 8: Commit**

```bash
git add content/ _quarto.yml scripts/gerar-stubs.sh
git commit -m "feat: estrutura completa dos capitulos 1-4"
```

---

## Task 7: CI/CD

**Files:**
- Create: `.github/workflows/quarto-render.yml`

**Interfaces:**
- Consumes: `Dockerfile` (Task 2), `_quarto.yml` com `output-dir: _book` (Task 3).
- Produces: publicação automática na branch `gh-pages` a cada push na `main`.

- [ ] **Step 1: Criar `.github/workflows/quarto-render.yml`**

Três decisões deliberadas neste arquivo:

1. **A imagem é escrita em minúsculas, literal.** Nada de `${{ github.repository_owner }}` — isso resolveria para `BragaD`, e o GHCR rejeita maiúsculas no nome da imagem.
2. **Um workflow, três jobs.** Se o build da imagem fosse um workflow separado, o primeiro push teria uma corrida: o job de render tentaria puxar uma imagem que ainda não existe. Com `needs:`, a ordem é garantida.
3. **O publish roda fora do container.** Ações de git dentro de imagem esbarram em `safe.directory` e em `git` ausente; renderizar dentro e publicar fora evita a classe inteira de problema.

```yaml
name: Render and Publish

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-image:
    name: Build da imagem
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login no GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build e push
        uses: docker/build-push-action@v6
        with:
          context: .
          platforms: linux/amd64
          push: true
          tags: ghcr.io/bragad/undf-bases3-estatistica-202602:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  render:
    name: Renderizar o livro
    needs: build-image
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read
    container:
      image: ghcr.io/bragad/undf-bases3-estatistica-202602:latest
      credentials:
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Marcar workspace como seguro para o git
        run: git config --global --add safe.directory "$GITHUB_WORKSPACE"

      - name: Render
        run: quarto render

      - name: Upload do livro renderizado
        uses: actions/upload-artifact@v4
        with:
          name: livro
          path: _book/
          retention-days: 7

  publish:
    name: Publicar no GitHub Pages
    needs: render
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download do livro renderizado
        uses: actions/download-artifact@v4
        with:
          name: livro
          path: _book

      - name: Publicar na branch gh-pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_book
          publish_branch: gh-pages
```

- [ ] **Step 2: Validar a sintaxe YAML**

Não há como executar o workflow localmente, então a verificação possível é sintática:

```bash
python3 -c "
import yaml, sys
wf = yaml.safe_load(open('.github/workflows/quarto-render.yml'))
jobs = wf['jobs']
assert list(jobs) == ['build-image', 'render', 'publish'], list(jobs)
assert jobs['render']['needs'] == 'build-image'
assert jobs['publish']['needs'] == 'render'
img = jobs['render']['container']['image']
assert img == img.lower(), f'imagem com maiúsculas: {img}'
print('workflow válido; imagem:', img)
"
```
Expected: `workflow válido; imagem: ghcr.io/bragad/undf-bases3-estatistica-202602:latest`

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/quarto-render.yml
git commit -m "ci: render no container e publish no gh-pages"
```

- [ ] **Step 4: Registrar as ações manuais pendentes**

Estas dependem do repositório existir no GitHub e **não podem ser feitas por script** aqui. Reporte-as ao usuário ao final:

1. Criar o repo `BragaD/UnDF-Bases3-Estatistica-202602` e dar `git push -u origin main`.
2. Em **Settings → Pages**, selecionar a branch `gh-pages` como fonte.
3. Em **Settings → Actions → General → Workflow permissions**, garantir *Read and write permissions*.
4. Após o primeiro build, o pacote GHCR nasce privado — isso é suficiente, pois o job `render` autentica com `GITHUB_TOKEN`. Torná-lo público é opcional.

---

## Task 8: Documentação

**Files:**
- Create: `CLAUDE.md`
- Create: `AGENTS.md`
- Create: `README.md`

**Interfaces:**
- Consumes: tudo das Tasks 1–7.

- [ ] **Step 1: Criar `CLAUDE.md`**

````markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Quarto book** (`type: book`) da disciplina *Bases 3 — Estatística*, oferecida aos cursos de Engenharia de Software e Sistemas de Informação da UnDF. Conteúdo em português brasileiro, **exemplos em Python**. Publicado no GitHub Pages a cada push na `main`.

Livro-texto: Bruce, Bruce & Gedeck — *Practical Statistics for Data Scientists*, 2ª ed. Código e dados originais: <https://github.com/gedeck/practical-statistics-for-data-scientists>

**Escopo: capítulos 1–4** (EDA, Distribuições Amostrais, Testes de Significância, Regressão). Os capítulos 5–7 do livro (Classificação, ML Estatístico, Aprendizado Não-Supervisionado) pertencem a *Bases 5 — Ciência de Dados* e **não** entram aqui.

## Comandos

Tudo roda dentro do container — não há Python instalado no host.

```bash
make preview   # hot-reload em http://localhost:4200
make render    # renderiza para _book/
make shell     # shell dentro do container
make check     # quarto check (diagnóstico)
make build     # reconstrói a imagem (após mudar Dockerfile ou uv.lock)
make lock      # regenera uv.lock após editar pyproject.toml
make clean     # remove _book/, _freeze/, .quarto/
```

Ao adicionar uma dependência Python: edite `pyproject.toml` → `make lock` → `make build`.

`execute: freeze: auto` está ativo: o Quarto só reexecuta chunks cujo fonte mudou. O cache fica em `_freeze/` (gitignorado). Se um chunk parecer "preso" com saída velha, `make clean`.

## Arquitetura

### Estrutura de conteúdo

Um diretório por capítulo, um `.qmd` por seção do livro:

```
content/
└── cap01/
    ├── index.qmd                      # Visão geral + objetivos + tabela de seções
    ├── 01-dados-estruturados.qmd      # Uma seção do livro por arquivo
    ├── 02-dados-retangulares.qmd
    └── ...
```

**Todo `.qmd` novo precisa ser registrado em `_quarto.yml` sob `book.chapters`.** O YAML define o sidebar e a ordem de navegação — arquivo não listado simplesmente não aparece no livro. A ordem vem do `_quarto.yml`, não do nome do arquivo; para reordenar, renomeie com `git mv` e atualize o YAML na mesma operação.

A maioria das seções ainda é **stub** (título + `callout-note` + aviso de construção). A seção completa que serve de modelo de estilo é `content/cap01/03-estimativas-localizacao.qmd`.

### Caminhos de dados

`_quarto.yml` define `project: execute-dir: project`, então o diretório de trabalho de **todo** chunk é a raiz do projeto, independentemente de onde o `.qmd` esteja:

```python
estado = pd.read_csv("dados/state.csv")   # ✓
estado = pd.read_csv("../../dados/state.csv")   # ✗ nunca
```

Os 14 CSVs em `dados/` mantêm os nomes originais do repositório do livro, para que o código do livro-texto rode sem adaptação. `dados/README.md` mapeia cada arquivo à seção que o usa.

### Sementes em chunks estocásticos — obrigatório

Boa parte do livro é bootstrap, permutação e amostragem. **Todo chunk com RNG usa semente explícita:**

```python
rng = np.random.default_rng(42)
amostra = dados.sample(1000, random_state=42)
```

Sem isso, cada `quarto render` produz números e gráficos diferentes: o `freeze` perde o sentido, o diff do site publicado vira ruído, e o material deixa de bater com o que o aluno vê na tela.

### Classes CSS

Definidas em `styles.css`, com suporte a dark mode:

```markdown
::: {.conceito}
Conceito importante (azul).
:::

::: {.exemplo}
Exemplo (verde).
:::
```

Para conteúdo protegido por senha (gabaritos), `spoiler.html` fornece o JS; use um div `.spoiler` com `data-password-hash` (SHA-256 hex) e `data-hint`.

### Ambiente

Duas camadas travadas: `pyproject.toml` + `uv.lock` fixam as versões Python; o `Dockerfile` consome esse lock (`uv sync --frozen`) sobre um SO fixo com Quarto e locale `pt_BR.UTF-8`. O mesmo container renderiza local e no CI.

Detalhe não óbvio: o venv fica em **`/opt/venv`**, não em `/livro/.venv`. O `compose.yaml` faz bind mount do projeto sobre `/livro`, o que apagaria um venv que estivesse ali.

### CI/CD

`.github/workflows/quarto-render.yml`, três jobs em cadeia a cada push na `main`:

1. `build-image` — constrói e envia `ghcr.io/bragad/undf-bases3-estatistica-202602:latest` (cache do BuildKit via GHA)
2. `render` — roda **dentro** dessa imagem, `quarto render` → `_book/`, sobe como artefato
3. `publish` — em runner limpo, publica `_book/` na branch `gh-pages`

O nome da imagem é minúsculo e literal: o GHCR rejeita maiúsculas, então não dá para usar `${{ github.repository_owner }}` (que resolveria para `BragaD`).

`_book/` e `_freeze/` são artefatos locais gitignorados. `docs/` **não** é gitignorado — guarda specs e planos.
````

- [ ] **Step 2: Criar `AGENTS.md`**

Mesmo conteúdo do `CLAUDE.md`, trocando apenas as 3 primeiras linhas (o cabeçalho) — é o que o repo de referência faz.

```bash
{
  printf '# AGENTS.md\n\nThis file provides guidance to coding agents (Codex, etc.) when working with code in this repository.\n'
  tail -n +4 CLAUDE.md
} > AGENTS.md

head -3 AGENTS.md
```
Expected:
```
# AGENTS.md

This file provides guidance to coding agents (Codex, etc.) when working with code in this repository.
```

- [ ] **Step 3: Criar `README.md`**

````markdown
# Bases 3 — Estatística

Material de apoio da disciplina **Bases 3 — Estatística**, dos cursos de Engenharia de Software e Sistemas de Informação da UnDF.

O site é publicado automaticamente em
**<https://BragaD.github.io/UnDF-Bases3-Estatistica-202602>**

Os exemplos são em **Python**. O livro-texto é Bruce, Bruce & Gedeck, *Practical Statistics for Data Scientists* (2ª ed.), e a disciplina cobre seus **capítulos 1 a 4**.

## Rodando localmente

O único pré-requisito é **Docker**. Python, Quarto e todas as bibliotecas vêm dentro do container — você não instala nada disso na sua máquina.

```bash
git clone https://github.com/BragaD/UnDF-Bases3-Estatistica-202602
cd UnDF-Bases3-Estatistica-202602
make preview
```

Abra <http://localhost:4200>. O preview recarrega sozinho quando você salva um `.qmd`.

Outros comandos:

```bash
make render   # gera o livro em _book/
make shell    # shell dentro do container
make check    # diagnóstico do Quarto
make build    # reconstrói a imagem (após mudar Dockerfile ou uv.lock)
make clean    # limpa artefatos de render
```

Alternativa sem instalar nada: abra o repositório no **GitHub Codespaces** ou no VS Code com a extensão Dev Containers — o `.devcontainer/` já está configurado.

## Estrutura

```
.
├── _quarto.yml           # Config mestre: capítulos, tema, engine
├── index.qmd             # Página inicial
├── content/capNN/        # Um diretório por capítulo, um .qmd por seção
├── dados/                # Conjuntos de dados do livro-texto (caps. 1–4)
├── images/               # Logo da UnDF
├── styles.css            # Classes .conceito e .exemplo, dark mode
├── references.bib        # Bibliografia
├── Dockerfile            # Quarto + Python (via uv.lock)
├── compose.yaml          # Preview local
├── pyproject.toml        # Dependências Python
├── uv.lock               # Versões travadas
└── .github/workflows/    # CI: build da imagem → render → gh-pages
```

Todo arquivo novo em `content/` precisa ser registrado em `_quarto.yml` para aparecer no livro.

## Dados

Os conjuntos em `dados/` vêm do [repositório oficial do livro](https://github.com/gedeck/practical-statistics-for-data-scientists), com os nomes originais preservados. Veja `dados/README.md`.

## Licença

Material disponibilizado para fins educacionais. Os dados e exemplos originais são de autoria de Bruce, Bruce e Gedeck.
````

- [ ] **Step 4: Verificar que os três arquivos existem e que o AGENTS espelha o CLAUDE**

Run:
```bash
wc -l CLAUDE.md AGENTS.md README.md
diff <(tail -n +4 CLAUDE.md) <(tail -n +4 AGENTS.md) && echo "AGENTS.md espelha CLAUDE.md a partir da linha 4"
```
Expected: os três arquivos têm conteúdo, e o `diff` não acusa diferença.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md AGENTS.md README.md
git commit -m "docs: instrucoes para agentes e para humanos"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean
make render
find _book/content -name '*.html' | wc -l
```
Expected: `42`, sem erro. Este é o teste que o CI vai rodar.

- [ ] **Nenhum arquivo órfão**

```bash
for f in $(find content -name '*.qmd' | sort); do
  grep -q "$f" _quarto.yml || echo "ÓRFÃO: $f"
done
echo ok
```
Expected: só `ok`.

- [ ] **Nenhum caminho de dados relativo ao arquivo**

```bash
grep -rn '\.\./\.\./dados' content/ && echo "ERRO: caminho relativo encontrado" || echo "caminhos de dados ok"
```
Expected: `caminhos de dados ok`.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
