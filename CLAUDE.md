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

**Toda dependência leva limite superior de versão.** Pacotes 1.x+ levam limite na major (`"pandas>=3,<4"`); pacotes **0.x levam limite no minor** (`"statsmodels>=0.14,<0.15"`), porque num 0.x é o minor que carrega mudanças incompatíveis — `<1` não protegeria nada.

O motivo é concreto, não teórico: o pandas 3 mudou o dtype padrão de texto (`object` → `str`) e a indexação de Series categóricas, e isso quebrou dois exemplos do Capítulo 1 **sem levantar exceção** — apenas devolvendo a resposta errada (`s[0] > s[1]` passou a comparar strings alfabeticamente e retornar `False` em silêncio). O `uv.lock` protege a reprodutibilidade de hoje, mas sem os limites um `make lock` futuro resolveria livremente e reintroduziria a mesma classe de falha silenciosa. Os limites transformam isso num conflito de resolução explícito.

Se um limite bloquear um upgrade que você quer, suba-o **deliberadamente** e re-renderize o livro conferindo os números — não o remova.

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

`spoiler.html` fornece o JS de um spoiler: um div `.spoiler` com `data-password-hash` (SHA-256 hex) e `data-hint`. **Isso é ofuscação, não proteção.** O conteúdo "protegido" viaja em texto puro no HTML publicado — o hash SHA-256 só alterna qual `<div>` fica visível; qualquer aluno lê tudo com Ctrl+U. **Nunca** use para gabaritos, provas ou qualquer coisa que o aluno não deva poder ver antes da hora. Serve só para "revelar a resposta depois de tentar" (ex.: resposta de um exercício de fixação) — algo que não tem problema estar visível no código-fonte.

### Ambiente

Duas camadas travadas: `pyproject.toml` + `uv.lock` fixam as versões Python; o `Dockerfile` consome esse lock (`uv sync --frozen`) sobre um SO fixo com Quarto e locale `pt_BR.UTF-8`. O mesmo container renderiza local e no CI.

Detalhe não óbvio: o venv fica em **`/opt/venv`**, não em `/livro/.venv`. O `compose.yaml` faz bind mount do projeto sobre `/livro`, o que apagaria um venv que estivesse ali.

Segundo detalhe não óbvio: o Dockerfile grava `/etc/profile.d/venv.sh` reexportando o `PATH` com `/opt/venv/bin` na frente. Isso existe porque um shell de **login** (`bash -l`, e é assim que alguns clientes abrem `docker exec`) recarrega `/etc/profile`, que reescreve o `PATH` e descartaria o `ENV PATH` fixado na imagem — fazendo `python` cair no interpretador do sistema em vez do venv. Se `make shell` ou o preview começarem a resolver o Python errado, esse é o primeiro lugar a checar.

### CI/CD

`.github/workflows/quarto-render.yml`, três jobs em cadeia a cada push na `main`:

1. `build-image` — constrói e envia `ghcr.io/bragad/undf-bases3-estatistica-202602:latest` (cache do BuildKit via GHA)
2. `render` — roda **dentro** dessa imagem, `quarto render` → `_book/`, sobe como artefato
3. `publish` — em runner limpo, publica `_book/` na branch `gh-pages`

O nome da imagem é minúsculo e literal: o GHCR rejeita maiúsculas, então não dá para usar `${{ github.repository_owner }}` (que resolveria para `BragaD`).

`_book/` e `_freeze/` são artefatos locais gitignorados. `docs/` **não** é gitignorado — guarda specs e planos.

### Widgets interativos (Observable JS)

A seção 1.3 tem dois widgets em células `{ojs}`, nativas do Quarto: rodam no navegador do leitor, **não somam bytes ao site** e não afetam o `freeze` nem o CI.

Os dados vêm do próprio chunk Python da seção, via `ojs_define(dados = estado)` — uma fonte, dois consumidores. Nunca recarregue o CSV no OJS nem embuta os valores como literal.

O código OJS vai sempre com `//| echo: false`. É JavaScript num livro que ensina Python: exibi-lo sugeriria ao aluno que ele precisa aprendê-lo.

**Shinylive foi avaliado e recusado.** Ele embute o Pyodide e as wheels dos pacotes: medi **46 MB** (numpy + matplotlib) a **64 MB** (com scipy) adicionados ao site, e uma espera de download real para o aluno. O critério que decidiu: *o código faz parte da lição?* Nestes widgets, não — a lição é a intuição sobre robustez, e o código é o instrumento. Se um dia o objetivo for o aluno **ler e editar Python de verdade**, o Shinylive volta à mesa e os 46 MB se justificam.

**Verificação:** `grep` no HTML não basta — uma célula `{ojs}` quebrada renderiza sem erro e simplesmente não aparece. Rode o teste de navegador:

```bash
make render
docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble \
  bash -c "pip install --quiet playwright==1.61.0 && python /scripts/verifica-widgets.py"
```

Detalhe não óbvio: apesar do nome, esta imagem **não** vem com o pacote Python `playwright` pré-instalado — só os binários dos navegadores, em `/ms-playwright`. O `pip install playwright==1.61.0` (mesma versão do tag da imagem) é obrigatório antes de importar `playwright.sync_api`, senão o script falha com `ModuleNotFoundError`. O Playwright em si **não** entra na imagem do livro: ela ficaria centenas de MB maior à toa, e o CI a baixaria a cada push.
