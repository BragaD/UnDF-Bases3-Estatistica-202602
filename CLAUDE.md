# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Quarto book** (`type: book`) da disciplina *Bases 3 — Estatística*, oferecida aos cursos de Engenharia de Software e Sistemas de Informação da UnDF. Conteúdo em português brasileiro, **exemplos em Python**. Publicado no GitHub Pages a cada push na `main`.

Livro-texto (espinha): Bruce, Bruce & Gedeck — *Practical Statistics for Data Scientists*, 2ª ed. Código e dados originais: <https://github.com/gedeck/practical-statistics-for-data-scientists>

Segunda fonte: o *pythonbook* de Ethan Weed contribui com a Introdução (motivacional) e enriquecimentos do Capítulo 1.

Terceira fonte: **Bussab & Morettin — *Estatística Básica*** entra onde o Bruce é raso demais para graduação: hoje, os quantis empíricos das seções 1.4 e 1.5 (seção 3.3 dele). O epub está em `livros/`, **gitignorado** — o repositório é público e o material tem direitos autorais.

**Armadilha da edição:** o epub é a impressão de 2017 da Saraiva, mas o `references.bib` cita a 10ª ed. (2023) como `@bussab2023`. A numeração de seções das duas bate (3.3 Quantis Empíricos, 5.2–5.4, 6.6.4 Hipergeométrica), então as citações estão corretas — **não "corrija" a bib para 2017**, isso invalidaria todas elas de uma vez.

Regra de atribuição: callouts `de @bruce2020` marcam conteúdo do livro-texto; `de @weed`, do pythonbook; `de @bussab2023`, do Bussab & Morettin. Como nos callouts do Bruce, o número citado é sempre o **da fonte**, não o nosso.

**Estrutura atual:** uma Introdução (motivacional, sem número), o Cap. 1 (Análise Exploratória de Dados), o Cap. 2 (Probabilidade, 2.1–2.5), o Cap. 3 (Variáveis Aleatórias Discretas, 3.1–3.7) e o Cap. 4 (Variáveis Aleatórias Contínuas, 4.1–4.6), todos escritos. As seções 3.7 (Poisson) e 4.6 (exponencial) são leitura complementar, com `callout-warning` como a 1.8, e ficam fora dos notebooks. Cada capítulo tem `notebooks/capitulo-NN.ipynb`.

O Cap. 1 corresponde ao **capítulo 1 de @bruce2020**. Como o número citado no callout é sempre o **da fonte**, e não o nosso, os dois coincidem no Cap. 1. No Cap. 2 já divergem: a seção 2.1 corresponde à 5.1 do Bussab.

**Os Capítulos 2 a 5 foram removidos do livro em 2.2026** — Probabilidade e Distribuições, Amostragem e Estimação, Experimentos Estatísticos e Testes de Significância, e Regressão e Predição. Os arquivos saíram de `content/`, as partes saíram do `_quarto.yml` e os notebooks `capitulo-02.ipynb` e `capitulo-03.ipynb` foram apagados. **Não recrie os capítulos antigos**: o conteúdo deles está no histórico do git, e a probabilidade está sendo reescrita a partir do Bussab (abaixo), com outra espinha. Os novos `content/cap02/`, `cap03/` e `cap04/` seguem o escopo abaixo, não o antigo.

**Capítulos de probabilidade (2 a 4).** A fonte é **@bussab2023, capítulos 5, 6 e 7**, e não mais o @bruce2020 nem o @weed. Não presuma o escopo do capítulo antigo: ele vinha do Bruce, tinha outra espinha e foi apagado. O escopo foi **definido pelo professor em 18/09/2026**, uma aula de 100 min por linha:

| Aula | Data | Seções de @bussab2023 |
|:-:|:-:|---|
| 6 | 09/10 | 5.1, 5.2 + revisão curta de contagem |
| 7 | 16/10 | 5.3, 5.4 |
| 8 | 30/10 | **Prova 1**: Cap. 1 + Cap. 5 |
| 9 | 06/11 | 6.1, 6.2, 6.3 (com E(aX+b) e Var(aX+b) da 6.4), 6.5 |
| 10 | 13/11 | 6.6.1 a 6.6.4 (uniforme discreta, Bernoulli, binomial, hipergeométrica) |
| 11 | 27/11 | 7.1, 7.2, 7.3 |
| 12 | 04/12 | 7.4.1, 7.4.2 (uniforme contínua, normal) |
| 13 | 11/12 | **Prova 2**: Caps. 6 e 7 |

Decisões que acompanham esse escopo:

- **Três capítulos no livro, um por capítulo do Bussab:** Cap. 2 Probabilidade (Bussab 5 + contagem), Cap. 3 Variáveis Aleatórias Discretas (Bussab 6), Cap. 4 Variáveis Aleatórias Contínuas (Bussab 7). A seção 2.1 (`content/cap02/01-modelos-probabilisticos.qmd`) corresponde à 5.1.
- **Suplementar, fora do cronograma:** 6.6.5 (Poisson) e 7.4.3 (exponencial), com `callout-warning` no topo como na 1.8, e fora do notebook do capítulo.
- **Fora do livro:** 5.5, 5.6, 6.4 (exceto os dois resultados abaixo), 6.7 em diante, 7.5 em diante.
- **Da 6.4 entram só E(aX+b) = aE(X)+b e Var(aX+b) = a²Var(X)**, como nota dentro da 6.3. A padronização da normal (7.4.2) depende deles.
- **Contagem:** revisão curta (princípio multiplicativo, permutação, combinação) junto da 5.2, porque o Bussab usa combinações na 5.2, na binomial e na hipergeométrica sem ter seção própria. O texto de partida é `content/cap02/04-contagem-permutacao-combinacao.qmd` no commit `bd099e5`, que tem travessões e cita "exercício 5.8": no Bussab é o **Exemplo 5.8**; corrigir ao recuperar.
- **Os alunos já viram integral:** 7.1 a 7.3 fazem as contas por integral, não só como área.
- **Não há aula de revisão antes das provas:** as Listas cumprem esse papel.
- **Aula 6 = seções 2.1, 2.2 e 2.3 do livro** (5.1 e 5.2 do Bussab, divididas em três arquivos). Por falta de tempo, ficam como leitura, fora da exposição em aula: espaço discreto × contínuo (2.1), os desvios sobre ponto flutuante/`isclose` (2.2), a simulação da auditoria e a tabela completa da Mega-Sena (2.3). O texto do site não muda por isso.

Ordem, profundidade e redação de cada seção continuam sendo combinadas com o professor, seção a seção, via `/create-lecture`.

**Cortes de 2.2026 no Cap. 1** (o semestre perdeu quatro sextas — 11/09 atestado, 02/10 e 23/10 eleições, 20/11 feriado): da 1.5 saíram as convenções `lower` e `higher` de quantil, o gráfico de violino, a curva de densidade e a curtose; da 1.6, o valor esperado; da 1.7, o heatmap. A **1.8 continua no site** como leitura complementar — tem um `callout-warning` no topo, está marcada na tabela do `content/cap01/index.qmd` e **não entra no `notebooks/capitulo-01.ipynb`**. A curtose **não existe mais no livro**; não a cite como "introduzida no Capítulo 1".

## Comandos

O render roda dentro do container. Mas se existir um `.venv/` na raiz (gitignorado, criado por `uv sync`), ele espelha o `uv.lock` e serve para executar chunks isoladamente sem subir o Docker — útil quando o daemon está parado. O `quarto render` continua sendo só no container.

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

Um diretório por capítulo (mais `intro/` para a Introdução, sem número), um `.qmd` por seção do livro:

```
content/
├── intro/
│   ├── 01-por-que-estatistica.qmd
│   └── 02-paradoxo-simpson.qmd
└── cap01/
    ├── index.qmd                      # Visão geral + objetivos + tabela de seções
    ├── 01-dados-estruturados.qmd      # Uma seção do livro por arquivo
    ├── 02-dados-retangulares.qmd
    └── ...
```

**Todo `.qmd` novo precisa ser registrado em `_quarto.yml` sob `book.chapters`.** O YAML define o sidebar e a ordem de navegação — arquivo não listado simplesmente não aparece no livro. A ordem vem do `_quarto.yml`, não do nome do arquivo; para reordenar, renomeie com `git mv` e atualize o YAML na mesma operação.

A Introdução e o Capítulo 1 estão completos, e são **todo** o livro hoje. A seção que serve de modelo de **estrutura** é `content/cap01/03-estimativas-localizacao.qmd` (não de voz: ela tem travessões demais).

### Caminhos de dados

`_quarto.yml` define `project: execute-dir: project`, então o diretório de trabalho de **todo** chunk é a raiz do projeto, independentemente de onde o `.qmd` esteja:

```python
estado = pd.read_csv("dados/estados.csv")   # ✓
estado = pd.read_csv("../../dados/estados.csv")   # ✗ nunca
```

Os 13 CSVs do livro-texto em `dados/` mantêm os nomes originais do repositório do livro, para que o código do livro-texto rode sem adaptação. `dados/README.md` mapeia cada arquivo à seção que o usa.

**O dado dos estados é brasileiro.** `dados/estados.csv` traz as 27 unidades federativas com população (IBGE, 2024) e taxa de homicídios (Atlas da Violência, 2024). Colunas em português: `Estado`, `Populacao`, `Taxa.Homicidios`, `Sigla`.

Ele é **gerado por nós**, não vem do livro-texto: `scripts/gerar-dados-brasil.py` junta três fontes e roda **uma única vez** (o CSV é commitado). O pipeline não é um chunk do livro — o aluno não precisa ver a mecânica de juntar três fontes para aprender o que é uma mediana, e um livro que faz chamadas de rede a cada render é frágil.

O CSV bruto do Atlas está versionado em `dados/brutos/` porque a API do Atlas saiu do ar na reformulação do site (v3) e hoje devolve HTML.

Três consequências que diferenciam o dado brasileiro do americano que ele substituiu, e que estão embutidas na prosa do Capítulo 1:

1. **n = 27 é ímpar** — a mediana é uma observação de verdade (é a população da Paraíba), não a média de duas. A seção 1.3 ensina os dois casos.
2. **A média ponderada da taxa é MENOR que a simples** (18,79 contra 22,74), ao contrário dos EUA. São Paulo tem a maior população do país e a menor taxa de homicídios — a violência letal se concentra nos estados menos populosos.
3. **São Paulo é o outlier populacional** (46 M contra 717 mil de Roraima, 64×), e é ele que os widgets da seção 1.3 movem.

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

`_book/` e `_freeze/` são artefatos locais gitignorados. `docs/superpowers/` é versionado — guarda os specs e planos das sessões. O resto de `docs/` **não**: os arquivos de PID (`docs/PID*`, `docs/ficha-PID.md`) e a grade de Rotinas (`docs/Rotinas*`, de terceiros) são documentos administrativos com dados de docente e ficam **locais**, pelo mesmo motivo que `avaliacoes/` e `livros/` — o repositório é público.

### Widgets interativos (Observable JS)

As seções 1.3 (dois widgets) e 1.4 têm células `{ojs}`, nativas do Quarto: rodam no navegador do leitor, **não somam bytes ao site** e não afetam o `freeze` nem o CI.

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

### Skills e agentes de revisão (`.claude/`)

Adaptados de [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow), que é feito para **slides Beamer + R**. Aqui "lecture/slide" significa **seção do livro** (`content/capNN/*.qmd`), o código é Python e a referência de render é o próprio `.qmd` (não há Beamer). Os nomes das skills foram mantidos para bater com o original.

- **Skills:** `/create-lecture` (nova seção ou stub), `/scaffold-exercises` (lista + gabarito em `avaliacoes/`), `/devils-advocate`, `/humanize`, `/visual-audit`, `/qa-quarto` (crítico ↔ consertador até convergir), `/slide-excellence` (fan-out de todas as lentes).
- **Agentes:** `domain-reviewer` (substância, calibrado pelo **Bussab**), `pedagogy-reviewer`, `proofreader`, `slide-auditor` (layout da página), `humanize-auditor`, `quarto-critic`, `quarto-fixer`, `verifier`.
- **Regras:** `.claude/rules/knowledge-base.md` guarda notação e **armadilhas código↔teoria verificadas** (quantil do Bussab = `method="hazen"`, não o padrão do pandas; variância do Bussab 3.2 divide por $n$; `hypergeom`/`norm` da scipy). `content-invariants.md` numera as regras deste arquivo (INV-1…12) para os revisores citarem.
- **Achados** são arrays JSON validados por `scripts/validate-findings.py` (`id = sha1(arquivo:linha:locus)`). Relatórios e capturas (`scripts/captura-pagina.py`) vão para `quality_reports/`, gitignorado.

#### Obrigatório: skills a cada escrita ou reescrita de conteúdo

Toda vez que escrever ou reescrever prosa, código ou exercício do livro (`content/`, `index.qmd`, `notebooks/`, `avaliacoes/`), **use as skills abaixo antes de dar o trabalho por concluído**, mesmo que ninguém peça. Rascunho de IA não revisado não vai para o livro.

| Situação | Antes | Depois de escrever |
|---|---|---|
| Seção nova ou stub preenchido | `/create-lecture` (Pré-Voo + lotes) | todos os itens da linha abaixo + `/devils-advocate` |
| Reescrita ou trecho novo numa seção | ler `.claude/rules/knowledge-base.md` e `content-invariants.md` | `/humanize <arquivo> --so-novo`; agente `domain-reviewer` se mexeu em fórmula, número, definição ou citação; agente `proofreader` |
| Mudança em gráfico, tabela, widget ou layout | — | `/visual-audit` |
| Lista, prova ou exercício | `/scaffold-exercises` | agente `domain-reviewer` no gabarito; `/humanize` no enunciado |
| Antes de commit/push (a `main` publica o site) | — | agente `verifier`; `/qa-quarto` nas seções alteradas |
| Revisão completa pedida pelo professor | — | `/slide-excellence` |

- **Achados de gravidade alta ou `blocker` são corrigidos antes de entregar**, ou apresentados ao professor quando exigem decisão dele (definição, número reportado, escolha pedagógica).
- Se uma skill não puder rodar (Docker parado, sem `.venv`), diga qual ficou de fora e por quê. Nunca omita.
- Ao escrever, **evite o travessão (—)**: ele não é estilo do professor e é o sinal de IA mais frequente no livro. Use vírgula, dois-pontos, parênteses ou ponto final. Também evite a antítese "não é X — é Y".
- Mudança só em infraestrutura (`Dockerfile`, `Makefile`, CI, `.claude/`) não precisa de `/humanize` nem de `domain-reviewer`; precisa do `verifier`.
