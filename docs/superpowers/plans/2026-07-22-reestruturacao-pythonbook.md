# Reestruturação com Material do pythonbook — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reestruturar o livro incorporando material do pythonbook — nova Introdução motivacional, Cap. 1 enriquecido, e o antigo Cap. 2 dividido em dois (Probabilidade/Distribuições + Amostragem/Estimação) com renumeração em cascata —, seguida de dois revisores.

**Architecture:** Três fases. **Fase 1** move/renumera arquivos e conserta referências (o livro renderiza verde com o conteúdo só reordenado; slots novos entram como stubs). **Fase 2** escreve o conteúdo novo. **Fase 3** roda dois revisores e para na decisão do usuário.

**Tech Stack:** Quarto (jupyter) · scipy.stats · numpy · pandas · matplotlib · `git mv`

**Spec:** `docs/superpowers/specs/2026-07-22-reestruturacao-pythonbook-design.md`

## Global Constraints

- **Render sempre via container:** `make render`. Python avulso: `docker compose run --rm --no-deps livro python -c "…"`. Não há Python no host.
- **Formato brasileiro** em todo número impresso: `from formato import num`. Nunca `f"{x:,.1f}"`.
- **Semente obrigatória** em todo chunk com RNG: `np.random.default_rng(42)` / `random_state=42` / índice de laço.
- **Caminho relativo à raiz** nos `read_csv`: `dados/estados.csv`, nunca `../../dados/`.
- **Callouts `de @bruce2020` (linha 4 de cada seção reaproveitada) são IMUTÁVEIS** — citam o Bruce, cuja numeração não muda. Só a numeração do MEU livro (na prosa) remapeia.
- **Seções novas e enriquecimentos citam `@weed`** (a criar no `references.bib`).
- **Português brasileiro.** Seções novas abrem com `::: {.callout-note}`.
- **Modelo de voz:** `content/cap01/03-estimativas-localizacao.qmd`. Ler antes de escrever prosa.
- Não mexer em `pyproject.toml`, `uv.lock`, `formato.py`, `dados/`, `styles.css`, `modo-leitura.html`, `spoiler.html`.

## Números pré-computados no container (valores esperados não-negociáveis)

| Onde | Número |
|---|---|
| Cap. 1 curtose | Populacao = **8,78**; Taxa.Homicídios = **−0,88** |
| Cap. 1 z-score de SP | população **4,12**; taxa de homicídios **−1,93** |
| Cap. 1 moda (contínuo) | `estado["Populacao"]` tem **27 valores únicos em 27** → moda não informa |
| Cap. 1 moda (categórico) | causa modal em `dfw_airline` = **VooAnterior** (118.427,82 min) |
| Cap. 2 convergência frequentista (semente 42) | n=10 → **0,40**; n=100 → **0,52**; n=1000 → **0,509**; n=10000 → **0,494** |
| Intro Simpson | A: 93,1% / 73,0% / **total 78,0%**; B: 86,7% / 68,8% / **total 82,6%** (A vence cada segmento, B vence o total) |

---

## Estrutura de arquivos (estado final)

```
content/
├── intro/                          (novo)
│   ├── 01-por-que-estatistica.qmd  (novo — Fase 2)
│   └── 02-paradoxo-simpson.qmd     (novo — Fase 2)
├── cap01/  (8 seções + 4 subseções de enriquecimento)
├── cap02/  Probabilidade e Distribuições
│   ├── index.qmd                       (reescrito)
│   ├── 01-o-que-e-probabilidade.qmd    (novo)
│   ├── 02-regras-probabilidade.qmd     (novo)
│   ├── 03-distribuicao-binomial.qmd    (era 09)
│   ├── 04-poisson.qmd                  (era 12)
│   ├── 05-distribuicao-normal.qmd      (era 06)
│   ├── 06-caudas-longas.qmd            (era 07)
│   ├── 07-distribuicao-t.qmd           (era 08)
│   ├── 08-qui-quadrado.qmd             (era 10)
│   └── 09-distribuicao-f.qmd           (era 11)
├── cap03/  Amostragem e Estimação  (era cap02 01–05)
│   ├── index.qmd                       (reescrito)
│   ├── 01-amostragem-aleatoria.qmd
│   ├── 02-vies-selecao.qmd
│   ├── 03-distribuicao-amostral.qmd
│   ├── 04-bootstrap.qmd
│   └── 05-intervalos-confianca.qmd
├── cap04/  Significância  (era cap03, stubs)
└── cap05/  Regressão      (era cap04, stubs)
```

---

## FASE 1 — Reestruturação e coerência narrativa

### Task 1: Mover arquivos, criar stubs, reescrever `_quarto.yml` e os índices

Entrega o esqueleto completo da nova estrutura, renderizando verde. Conteúdo ainda reordenado só; slots novos como stubs.

**Files:**
- Move (git mv): árvore inteira conforme o mapa abaixo
- Create (stubs): `content/intro/01-por-que-estatistica.qmd`, `content/intro/02-paradoxo-simpson.qmd`, `content/cap02/01-o-que-e-probabilidade.qmd`, `content/cap02/02-regras-probabilidade.qmd`
- Rewrite: `_quarto.yml`, `content/cap02/index.qmd`, `content/cap03/index.qmd`, `content/cap04/index.qmd` (prosa), `content/cap05/index.qmd` (prosa)

- [ ] **Step 1: Mover e renumerar os arquivos (nesta ordem exata)**

```bash
cd "$(git rev-parse --show-toplevel)"
git mv content/cap04 content/cap05
git mv content/cap03 content/cap04
mkdir content/cap03
git mv content/cap02/index.qmd                    content/cap03/index.qmd
git mv content/cap02/01-amostragem-aleatoria.qmd  content/cap03/01-amostragem-aleatoria.qmd
git mv content/cap02/02-vies-selecao.qmd          content/cap03/02-vies-selecao.qmd
git mv content/cap02/03-distribuicao-amostral.qmd content/cap03/03-distribuicao-amostral.qmd
git mv content/cap02/04-bootstrap.qmd             content/cap03/04-bootstrap.qmd
git mv content/cap02/05-intervalos-confianca.qmd  content/cap03/05-intervalos-confianca.qmd
# Distribuições: renomear via nome temporário para evitar colisão de números
git mv content/cap02/06-distribuicao-normal.qmd   content/cap02/tmp-normal.qmd
git mv content/cap02/07-caudas-longas.qmd         content/cap02/tmp-caudas.qmd
git mv content/cap02/08-distribuicao-t.qmd        content/cap02/tmp-t.qmd
git mv content/cap02/09-distribuicao-binomial.qmd content/cap02/03-distribuicao-binomial.qmd
git mv content/cap02/10-qui-quadrado.qmd          content/cap02/08-qui-quadrado.qmd
git mv content/cap02/11-distribuicao-f.qmd        content/cap02/09-distribuicao-f.qmd
git mv content/cap02/12-poisson.qmd               content/cap02/04-poisson.qmd
git mv content/cap02/tmp-normal.qmd               content/cap02/05-distribuicao-normal.qmd
git mv content/cap02/tmp-caudas.qmd               content/cap02/06-caudas-longas.qmd
git mv content/cap02/tmp-t.qmd                    content/cap02/07-distribuicao-t.qmd
mkdir -p content/intro
```

- [ ] **Step 2: Verificar o resultado dos moves**

Run:
```bash
ls content/cap02 content/cap03 content/cap04 content/cap05 content/intro
```
Expected: `cap02` com `03-distribuicao-binomial … 09-distribuicao-f` (sem 01/02/index ainda); `cap03` com index + 01–05 de amostragem; `cap04` com os 11 stubs de significância; `cap05` com os 7 de regressão; `intro` vazio.

- [ ] **Step 3: Criar os 4 stubs (padrão do projeto — título + callout + "Em construção")**

`content/intro/01-por-que-estatistica.qmd`:
```markdown
# Por que Estatística?

::: {.callout-note}
Esta seção se inspira no Capítulo 1 de @weed.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
```

`content/intro/02-paradoxo-simpson.qmd`:
```markdown
# O Paradoxo de Simpson

::: {.callout-note}
Esta seção se inspira no Capítulo 1 de @weed.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
```

`content/cap02/01-o-que-e-probabilidade.qmd`:
```markdown
# O que é Probabilidade

::: {.callout-note}
Esta seção se inspira no Capítulo 10 de @weed.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
```

`content/cap02/02-regras-probabilidade.qmd`:
```markdown
# Regras de Probabilidade

::: {.callout-note}
Esta seção se inspira no Capítulo 10 de @weed.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
```

- [ ] **Step 4: Reescrever o bloco `chapters:` do `_quarto.yml`**

Substituir todo o bloco `chapters:` (linhas ~25–119) por:

```yaml
  chapters:
    - text: "Início"
      href: index.qmd
    - part: "Introdução"
      chapters:
        - href: content/intro/01-por-que-estatistica.qmd
          text: "Por que Estatística?"
        - href: content/intro/02-paradoxo-simpson.qmd
          text: "O Paradoxo de Simpson"
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
    - part: "Capítulo 2: Probabilidade e Distribuições"
      chapters:
        - href: content/cap02/index.qmd
          text: "Visão Geral"
        - href: content/cap02/01-o-que-e-probabilidade.qmd
          text: "O que é Probabilidade"
        - href: content/cap02/02-regras-probabilidade.qmd
          text: "Regras de Probabilidade"
        - href: content/cap02/03-distribuicao-binomial.qmd
          text: "Distribuição Binomial"
        - href: content/cap02/04-poisson.qmd
          text: "Distribuição de Poisson"
        - href: content/cap02/05-distribuicao-normal.qmd
          text: "Distribuição Normal"
        - href: content/cap02/06-caudas-longas.qmd
          text: "Distribuições de Cauda Longa"
        - href: content/cap02/07-distribuicao-t.qmd
          text: "Distribuição t de Student"
        - href: content/cap02/08-qui-quadrado.qmd
          text: "Distribuição Qui-Quadrado"
        - href: content/cap02/09-distribuicao-f.qmd
          text: "Distribuição F"
    - part: "Capítulo 3: Amostragem e Estimação"
      chapters:
        - href: content/cap03/index.qmd
          text: "Visão Geral"
        - href: content/cap03/01-amostragem-aleatoria.qmd
          text: "Amostragem Aleatória e Viés"
        - href: content/cap03/02-vies-selecao.qmd
          text: "Viés de Seleção"
        - href: content/cap03/03-distribuicao-amostral.qmd
          text: "Distribuição Amostral"
        - href: content/cap03/04-bootstrap.qmd
          text: "Bootstrap"
        - href: content/cap03/05-intervalos-confianca.qmd
          text: "Intervalos de Confiança"
    - part: "Capítulo 4: Experimentos Estatísticos e Testes de Significância"
      chapters:
        - href: content/cap04/index.qmd
          text: "Visão Geral"
        - href: content/cap04/01-teste-ab.qmd
          text: "Teste A/B"
        - href: content/cap04/02-testes-hipotese.qmd
          text: "Testes de Hipótese"
        - href: content/cap04/03-reamostragem.qmd
          text: "Reamostragem"
        - href: content/cap04/04-significancia-valor-p.qmd
          text: "Significância e Valores-p"
        - href: content/cap04/05-testes-t.qmd
          text: "Testes t"
        - href: content/cap04/06-testes-multiplos.qmd
          text: "Testes Múltiplos"
        - href: content/cap04/07-graus-liberdade.qmd
          text: "Graus de Liberdade"
        - href: content/cap04/08-anova.qmd
          text: "ANOVA"
        - href: content/cap04/09-teste-qui-quadrado.qmd
          text: "Teste Qui-Quadrado"
        - href: content/cap04/10-multi-armed-bandit.qmd
          text: "Multi-Armed Bandit"
        - href: content/cap04/11-poder-tamanho-amostra.qmd
          text: "Poder e Tamanho da Amostra"
    - part: "Capítulo 5: Regressão e Predição"
      chapters:
        - href: content/cap05/index.qmd
          text: "Visão Geral"
        - href: content/cap05/01-regressao-linear-simples.qmd
          text: "Regressão Linear Simples"
        - href: content/cap05/02-regressao-linear-multipla.qmd
          text: "Regressão Linear Múltipla"
        - href: content/cap05/03-predicao.qmd
          text: "Predição com Regressão"
        - href: content/cap05/04-variaveis-fatoriais.qmd
          text: "Variáveis Fatoriais"
        - href: content/cap05/05-interpretando-equacao.qmd
          text: "Interpretando a Equação"
        - href: content/cap05/06-diagnostico-regressao.qmd
          text: "Diagnóstico de Regressão"
        - href: content/cap05/07-polinomial-splines.qmd
          text: "Polinomial e Splines"
```

- [ ] **Step 5: Reescrever `content/cap02/index.qmd` (Visão Geral do novo Cap. 2)**

Ler antes o `content/cap01/index.qmd` para o padrão (título, callout de objetivos, tabela de seções). O novo `cap02/index.qmd`: título "Capítulo 2: Probabilidade e Distribuições"; objetivos (entender probabilidade, as regras, e o catálogo de distribuições); tabela das 9 seções (2 de probabilidade + 7 distribuições). Sem `Em construção`. Deve citar que o capítulo mistura Bruce (distribuições) e @weed (probabilidade).

- [ ] **Step 6: Reescrever `content/cap03/index.qmd` (Visão Geral do novo Cap. 3)**

Título "Capítulo 3: Amostragem e Estimação"; objetivos (amostra vs população, distribuição amostral/TCL, bootstrap, intervalo de confiança); tabela das 5 seções. Sem `Em construção`.

- [ ] **Step 7: Corrigir a prosa dos índices movidos (cap04 e cap05)**

Em `content/cap04/index.qmd`: trocar o número de capítulo na prosa e no título de "Capítulo 3" → "Capítulo 4" (é a Visão Geral da Significância, agora Cap. 4). Em `content/cap05/index.qmd`: "Capítulo 4" → "Capítulo 5".

Run (localizar as ocorrências a trocar):
```bash
grep -n 'Capítulo 3' content/cap04/index.qmd
grep -n 'Capítulo 4' content/cap05/index.qmd
```

- [ ] **Step 8: Renderizar e verificar o esqueleto**

Run:
```bash
make clean && make render 2>&1 | tail -5
echo "--- estrutura no HTML ---"
grep -c 'Probabilidade e Distribuições' _book/content/cap02/index.html
find _book/content -name '*.html' | sort | sed 's#_book/content/##'
```
Expected: render sem erro (`Output created: _book/index.html`); as páginas listam `intro/01`, `intro/02`, `cap02/01`–`09`, `cap03/01`–`05`, `cap04/01`–`11`, `cap05/01`–`07` e os cinco `index.html`.

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "refactor: reestrutura livro — intro, divide cap2, renumera em cascata"
```

---

### Task 2: Corrigir referências cruzadas e coerência narrativa

Depois do Task 1 o livro renderiza, mas a prosa ainda aponta para a numeração antiga e tem remissões de direção invertida. Este task conserta.

**Files:**
- Modify: `content/cap02/05-distribuicao-normal.qmd`, `06-caudas-longas.qmd`, `07-distribuicao-t.qmd`, `08-qui-quadrado.qmd`, `09-distribuicao-f.qmd`
- Modify: `content/cap03/01-amostragem-aleatoria.qmd`, `03-distribuicao-amostral.qmd`, `04-bootstrap.qmd`, `05-intervalos-confianca.qmd`

- [ ] **Step 1: Correções puras de número (não alteram sentido)**

Aplicar (a linha 4 `de @bruce2020` de cada arquivo NÃO muda):

- `cap02/06-caudas-longas.qmd`: `seção 2.6` → `seção 2.5` (referência à Normal).
- `cap02/05-distribuicao-normal.qmd`: `seção 2.7` (remissão a caudas longas) → `seção 2.6`.
- `cap02/08-qui-quadrado.qmd`: `Capítulo 3` → `Capítulo 4` (2 ocorrências); `seção 3.9` → `seção 4.9`.
- `cap02/09-distribuicao-f.qmd`: `Capítulo 3` → `Capítulo 4`; `seção 3.8` → `seção 4.8`.
- `cap03/01-amostragem-aleatoria.qmd`: `seção 2.3` → `seção 3.3` (2 ocorrências).
- `cap03/03-distribuicao-amostral.qmd`: `seção 2.1` → `seção 3.1` (2 ocorrências).
- `cap03/04-bootstrap.qmd`: `seção 2.3` → `seção 3.3` (2 ocorrências).
- `cap03/05-intervalos-confianca.qmd`: `seção 2.3` → `seção 3.3`.

- [ ] **Step 2: Reescritas de coerência narrativa (3 casos — mudam o sentido, não só o número)**

1. **`cap02/05-distribuicao-normal.qmd` — primeira aparição do `loans_income`.** O texto atual (`fig-qq-renda` e a prosa após) trata a renda como "as 50.000 rendas que este capítulo vem usando" e diz que a cauda longa "já vimos na seção 2.1". Na nova ordem, esta é a **primeira** vez que a renda aparece. Reescrever: (a) apresentar o dataset em uma frase no primeiro uso — "as 50.000 rendas de solicitantes de empréstimo do `loans_income` (em dólares), que o Capítulo 3 usará a fundo"; (b) trocar "a cauda longa à direita que já vimos na seção 2.1" por afirmação autossuficiente: "a cauda longa à direita da renda — um padrão que o Capítulo 3 retoma ao estudar amostragem". O chunk de código (`stats.probplot(renda, …)`) permanece; só a prosa muda.

2. **`cap02/07-distribuicao-t.qmd` — remissão a intervalos de confiança.** A prosa diz "Foi a distribuição por trás dos intervalos de confiança da seção 2.5, mesmo sem ter sido nomeada lá". IC agora é 3.5 e vem **depois**. Reescrever para remissão para frente: "É a distribuição por trás dos intervalos de confiança que o Capítulo 3 constrói (seção 3.5) — a que aparece quando se estima a média com amostra pequena."

3. **`cap03/01-amostragem-aleatoria.qmd` — remissão a cauda longa.** A prosa (na seção "Os dados") diz que a renda "é o exemplo clássico de distribuição de cauda longa à direita, e vai voltar quando o capítulo chegar lá". Cauda longa agora é 2.6, **anterior**. Reescrever para remissão para trás: "é o exemplo clássico de distribuição de cauda longa à direita, que o Capítulo 2 já tratou (seção 2.6)".

- [ ] **Step 3: Verificação de integridade das referências**

Run:
```bash
# Nenhuma referência de prosa deve apontar para número que não existe mais.
echo "=== refs a seções inexistentes do Cap.2 (2.10-2.12) fora da linha-4 Bruce ==="
grep -rnE 'seç(ão|ões) 2\.1[012]' content/cap02 content/cap03 | grep -v 'de @bruce2020' || echo "OK: nenhuma"
echo "=== refs a 'Capítulo 3' remanescentes nas distribuições (deveria ser Cap.4) ==="
grep -rn 'Capítulo 3' content/cap02 || echo "OK: nenhuma"
echo "=== sanidade: cada seção reaproveitada mantém seu callout Bruce na linha 4 ==="
for f in content/cap02/0[3-9]-*.qmd content/cap03/0[1-5]-*.qmd; do sed -n '4p' "$f"; done
```
Expected: as duas primeiras dão "OK: nenhuma"; a terceira lista 12 linhas `Esta seção corresponde à seção 2.X de @bruce2020` (com os números ORIGINAIS do Bruce: 2.9, 2.12, 2.6, 2.7, 2.8, 2.10, 2.11 para as distribuições e 2.1–2.5 para amostragem).

- [ ] **Step 4: Renderizar e commitar**

Run:
```bash
make render 2>&1 | tail -3
```
Expected: sem erro.

```bash
git add -A
git commit -m "fix: corrige referencias cruzadas e coerencia narrativa pos-reordenacao"
```

---

### Task 3: Atualizar o `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Atualizar as seções de escopo e estrutura**

Editar `CLAUDE.md`:
- Trocar "Escopo: capítulos 1–4" pela nova espinha: uma Introdução (motivacional) + **5 capítulos** (1 EDA, 2 Probabilidade e Distribuições, 3 Amostragem e Estimação, 4 Testes de Significância, 5 Regressão). Documentar o mapa Bruce↔meu-livro: **Bruce cap. 2** dividido entre **meus Cap. 2 e Cap. 3**; **Bruce cap. 3** → **meu Cap. 4**; **Bruce cap. 4** → **meu Cap. 5**. Isso explica por que os callouts `de @bruce2020` citam números "fora de fase" com os meus.
- No parágrafo do livro-texto, acrescentar o **pythonbook (Weed)** como segunda fonte — introdução, probabilidade, ordenação da Parte IV e enriquecimentos do Cap. 1 —, com a regra de atribuição (callouts `@bruce2020` para conteúdo Bruce; `@weed` para conteúdo pythonbook).
- Atualizar a árvore de diretórios em "Estrutura de conteúdo" para incluir `intro/` e `cap01`–`cap05`.

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: atualiza CLAUDE.md para a nova estrutura (intro + 5 capitulos)"
```

---

## FASE 2 — Conteúdo novo

### Task 4: `references.bib` (@weed) + Introdução §1 "Por que Estatística?"

**Files:**
- Modify: `references.bib`
- Modify: `content/intro/01-por-que-estatistica.qmd` (preenche o stub)

- [ ] **Step 1: Adicionar a entrada `@weed` ao `references.bib`**

Ler o `references.bib` para o estilo. Acrescentar (confirmar ano/autoria na fonte; se indeterminável, usar `year = {s.d.}`):
```bibtex
@book{weed,
  author    = {Weed, Ethan and Navarro, Danielle},
  title     = {Learning Statistics with {Python}},
  note      = {Adaptação em Python de \emph{Learning Statistics with R}, de Danielle Navarro},
  url       = {https://ethanweed.github.io/pythonbook/},
  year      = {2022}
}
```

- [ ] **Step 2: Escrever a seção "Por que Estatística?"**

Substituir o corpo do stub (mantendo o `# Por que Estatística?` e o `callout-note` citando @weed). Prosa motivacional, **despsicologizada** para Eng. de Software / dados. Cobrir, nesta ordem:
- A intuição humana falha em raciocínio estatístico — e por quê isso importa para quem vai analisar dados e construir software que decide com dados.
- **Viés de crença / confirmação:** tendemos a aceitar conclusões que confirmam o que já achávamos e a duvidar das que contrariam. A estatística é a disciplina que obriga os dados a responderem, independentemente do que gostaríamos que dissessem.
- Estatística no dia a dia de quem trabalha com dados: estimar sem medir tudo, decidir sob incerteza, distinguir sinal de ruído.
- Sem código pesado. No máximo uma frase ilustrativa. Sem exercícios (é seção motivacional) ou 1 pergunta de reflexão.

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|intro/01' | head
H=_book/content/intro/01-por-que-estatistica.html
echo "stub=$(grep -c 'Em construção' "$H")  weed=$(grep -c 'Weed\|pythonbook\|href.*ethanweed' "$H")"
```
Expected: render sem erro; `stub=0`; a citação a @weed resolve (bibliografia renderizada, `weed` ≥ 1).

- [ ] **Step 4: Commit**

```bash
git add references.bib content/intro/01-por-que-estatistica.qmd
git commit -m "feat: introducao — por que estatistica + entrada weed no bib"
```

---

### Task 5: Introdução §2 "O Paradoxo de Simpson"

**Files:**
- Modify: `content/intro/02-paradoxo-simpson.qmd` (preenche o stub)

**Interfaces:**
- Consome: `numpy`, `pandas`, `formato.num`.

- [ ] **Step 1: Escrever a seção com o exemplo numérico da inversão**

Manter `# O Paradoxo de Simpson` + callout @weed. Prosa: uma tendência agregada pode **se inverter** dentro de cada subgrupo; por isso agregar cegamente engana. Exemplo de dados/software (dois algoritmos A e B, dois segmentos de usuário — novos e recorrentes). Chunk (números verificados no container):

```{python}
#| label: simpson
import pandas as pd
from formato import num

# Sucessos / total por algoritmo e segmento (dados sintéticos)
dados = pd.DataFrame({
    "Segmento":   ["Novos", "Recorrentes"],
    "A_sucesso":  [81, 192],
    "A_total":    [87, 263],
    "B_sucesso":  [234, 55],
    "B_total":    [270, 80],
})

def taxa(s, t):
    return 100 * s / t

for _, r in dados.iterrows():
    print(f'{r.Segmento:>12}: A = {num(taxa(r.A_sucesso, r.A_total), 1)}%   '
          f'B = {num(taxa(r.B_sucesso, r.B_total), 1)}%')

a_tot = taxa(dados.A_sucesso.sum(), dados.A_total.sum())
b_tot = taxa(dados.B_sucesso.sum(), dados.B_total.sum())
print(f'{"TOTAL":>12}: A = {num(a_tot, 1)}%   B = {num(b_tot, 1)}%')
```

Saídas verificadas: Novos → A 93,1% / B 86,7%; Recorrentes → A 73,0% / B 68,8%; TOTAL → A **78,0%** / B **82,6%**. Prosa: A vence em **cada** segmento, mas B vence no **total** — porque os segmentos têm tamanhos e taxas-base diferentes (a mistura, não o mérito, decide o agregado). A lição: sempre pergunte se há um subgrupo escondido; conecta a confundidores que reaparecem no Cap. 3 (viés) e Cap. 4 (significância). 1 exercício em `callout-tip collapse`.

- [ ] **Step 2: Renderizar e verificar os números**

Run:
```bash
make render 2>&1 | grep -iE 'error|simpson' | head
H=_book/content/intro/02-paradoxo-simpson.html
grep -oE '93,1%|73,0%|78,0%|86,7%|68,8%|82,6%' "$H" | sort -u | tr '\n' ' '; echo
echo "stub=$(grep -c 'Em construção' "$H")  exerc=$(grep -c 'callout-tip' "$H")"
```
Expected: os seis percentuais aparecem; `stub=0`; `exerc=1`.

- [ ] **Step 3: Commit**

```bash
git add content/intro/02-paradoxo-simpson.qmd
git commit -m "feat: introducao — paradoxo de simpson"
```

---

### Task 6: Cap. 2 §1 "O que é Probabilidade"

**Files:**
- Modify: `content/cap02/01-o-que-e-probabilidade.qmd` (preenche o stub)

- [ ] **Step 1: Escrever a seção**

Manter `# O que é Probabilidade` + callout @weed. Cobrir:
- **Probabilidade vs estatística:** probabilidade parte do modelo para prever os dados (dedutivo); estatística parte dos dados para inferir o modelo (indutivo). Uma é o inverso da outra.
- **O que "probabilidade" significa:** a **visão frequentista** (a probabilidade de um evento é a frequência relativa dele no longo prazo, em repetições) vs a **visão bayesiana** (probabilidade como grau de crença). Qual a diferença, e por que importa aqui: os métodos do Cap. 4 (valores-p) são frequentistas.
- Simulação com semente mostrando a frequência relativa **convergindo** conforme as repetições crescem:

```{python}
#| label: convergencia-frequentista
import numpy as np
import matplotlib.pyplot as plt
from formato import num

plt.rcParams["figure.figsize"] = (7, 4)
rng = np.random.default_rng(42)
lancamentos = rng.integers(0, 2, 10000)          # 0 ou 1, moeda justa
proporcao = np.cumsum(lancamentos) / np.arange(1, 10001)

for n in [10, 100, 1000, 10000]:
    print(f"Após {n:>5} lançamentos: proporção de caras = {num(proporcao[n-1], 3)}")
```

Saídas verificadas: n=10 → **0,400**; n=100 → **0,520**; n=1000 → **0,509**; n=10000 → **0,494**. Gráfico da proporção acumulada convergindo para 0,5:

```{python}
#| label: fig-convergencia
#| fig-cap: "A proporção de caras oscila muito no começo e se estabiliza em torno de 0,5 conforme os lançamentos crescem. É a visão frequentista: probabilidade como frequência no longo prazo."
fig, ax = plt.subplots()
ax.plot(np.arange(1, 10001), proporcao, color="#2c3e50", linewidth=1)
ax.axhline(0.5, color="#c0392b", linestyle="--", linewidth=2)
ax.set_xscale("log")
ax.set_xlabel("Número de lançamentos (escala log)")
ax.set_ylabel("Proporção de caras")
plt.tight_layout()
plt.show()
```

Prosa: nos primeiros lançamentos a proporção pula (0,40 em 10); com 10.000 ela cola em 0,5. **Isso é** a definição frequentista em ação. 2 exercícios em `callout-tip collapse`.

- [ ] **Step 2: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|o-que-e-prob' | head
H=_book/content/cap02/01-o-que-e-probabilidade.html
grep -oE '0,400|0,520|0,509|0,494' "$H" | sort -u | tr '\n' ' '; echo
echo "imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo)  stub=$(grep -c 'Em construção' "$H")  exerc=$(grep -c 'callout-tip' "$H")"
grep -nE 'default_rng|integers|\.sample' content/cap02/01-o-que-e-probabilidade.qmd | grep -v 'default_rng(42)' || echo "sementes ok"
```
Expected: os quatro valores; `imgs=1`, `stub=0`, `exerc=2`; `sementes ok`.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/01-o-que-e-probabilidade.qmd
git commit -m "feat: cap2 — o que e probabilidade (frequentista vs bayesiano)"
```

---

### Task 7: Cap. 2 §2 "Regras de Probabilidade"

**Files:**
- Modify: `content/cap02/02-regras-probabilidade.qmd` (preenche o stub)

- [ ] **Step 1: Escrever a seção**

Manter `# Regras de Probabilidade` + callout @weed. Cobrir, com exemplos de dados/software:
- **Espaço amostral e evento;** probabilidade de um evento entre 0 e 1.
- **Complementar:** P(não A) = 1 − P(A). Exemplo: se a chance de uma requisição falhar é 0,02, a de **não** falhar é 0,98.
- **Regra da adição:** para eventos mutuamente exclusivos, P(A ou B) = P(A) + P(B); regra geral com a subtração da interseção.
- **Multiplicação e independência:** P(A e B) = P(A)·P(B) quando A e B são independentes. Exemplo: dois serviços independentes com 0,99 de disponibilidade cada → ambos no ar = 0,99² ≈ 0,98; **pelo menos um fora** = 1 − 0,99² (usando o complementar).
- **Distribuição de probabilidade:** a ideia de que uma variável aleatória tem uma probabilidade associada a cada valor possível — a ponte direta para as sete distribuições que seguem (a próxima seção, binomial, é a primeira).

Um chunk pequeno pode ilustrar o exemplo dos dois serviços:
```{python}
#| label: regras
from formato import num
p = 0.99
print(f"Ambos os serviços no ar:      {num(p**2, 4)}")
print(f"Pelo menos um fora do ar:     {num(1 - p**2, 4)}")
```
Saídas: 0,9801 e 0,0199 (aritmética simples; conferir no render). 2–3 exercícios em `callout-tip collapse`.

- [ ] **Step 2: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|regras-prob' | head
H=_book/content/cap02/02-regras-probabilidade.html
grep -oE '0,9801|0,0199' "$H" | sort -u | tr '\n' ' '; echo
echo "stub=$(grep -c 'Em construção' "$H")  exerc=$(grep -c 'callout-tip' "$H")"
```
Expected: `0,9801` e `0,0199`; `stub=0`; `exerc` ≥ 2.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/02-regras-probabilidade.qmd
git commit -m "feat: cap2 — regras de probabilidade"
```

---

### Task 8: Cap. 1 — enriquecimento "Moda" (seção 1.3)

**Files:**
- Modify: `content/cap01/03-estimativas-localizacao.qmd`

- [ ] **Step 1: Acrescentar a subseção "Moda" após "Mediana" (antes de "Estimativas ponderadas")**

Ler a seção primeiro (o setup dela já carrega `estado`). Nova subseção `## Moda` citando @weed numa nota. Conteúdo:
- A moda = o valor mais frequente. Diferente de média e mediana, ela também vale para dados **categóricos** (não exige ordem nem soma).
- **Lição honesta para contínuo:** na população dos estados, cada valor é único — a moda não informa nada:
```{python}
#| label: moda-continua
print(f"Valores únicos de população: {estado['Populacao'].nunique()} de {len(estado)}")
```
Saída verificada: **27 de 27**. Ou seja, moda inútil aqui.
- **Onde a moda brilha — categórico:** a causa modal de atraso de voo (o dataset da seção 1.6):
```{python}
#| label: moda-categorica
dfw = pd.read_csv("dados/dfw_airline.csv").rename(columns={
    "Carrier": "Companhia", "ATC": "ControleAereo", "Weather": "Clima",
    "Security": "Seguranca", "Inbound": "VooAnterior"})
print(f"Causa modal de atraso: {dfw.iloc[0].idxmax()}")
```
Saída verificada: **VooAnterior**. Prosa: para categórico, a moda é o resumo natural — não há média de "Clima" e "Segurança". Remissão para frente à seção 1.6. Acrescentar 1 exercício ao bloco de exercícios da seção sobre quando a moda é a medida certa.

- [ ] **Step 2: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|localizacao' | head
H=_book/content/cap01/03-estimativas-localizacao.html
grep -oE '27 de 27|VooAnterior' "$H" | sort -u | tr '\n' ' '; echo
grep -c 'Moda' "$H"
```
Expected: `27 de 27` e `VooAnterior` presentes; "Moda" ≥ 1.

- [ ] **Step 3: Commit**

```bash
git add content/cap01/03-estimativas-localizacao.qmd
git commit -m "feat: cap1 — moda como medida de localizacao"
```

---

### Task 9: Cap. 1 — enriquecimento "Escores-padrão (z-scores)" (seção 1.4)

**Files:**
- Modify: `content/cap01/04-estimativas-variabilidade.qmd`

- [ ] **Step 1: Acrescentar a subseção "Escores-padrão" antes de "Mexa no desvio-padrão"**

O widget desta seção **já usa** z-scores ("o truque por trás disso é o z-score"). A nova subseção `## Escores-padrão` formaliza o conceito que o widget explora — colocá-la **antes** do widget para que ele passe a apoiar-se num conceito já ensinado. Nota citando @weed. Conteúdo:
- Definição: $z = (x - \bar{x})/s$ — quantos desvios-padrão um valor está da média. Adimensional; permite comparar grandezas em escalas diferentes.
- Exemplo com os estados (o `estado` já está no setup):
```{python}
#| label: z-score
mu, sd = estado["Populacao"].mean(), estado["Populacao"].std(ddof=1)
sp = estado.loc[estado["Sigla"] == "SP", "Populacao"].iloc[0]
z_sp = (sp - mu) / sd
print(f"z-score da população de SP: {num(z_sp, 2)}")

mu_t, sd_t = estado["Taxa.Homicidios"].mean(), estado["Taxa.Homicidios"].std(ddof=1)
sp_t = estado.loc[estado["Sigla"] == "SP", "Taxa.Homicidios"].iloc[0]
print(f"z-score da taxa de homicídios de SP: {num((sp_t - mu_t) / sd_t, 2)}")
```
Saídas verificadas: população **4,12**; taxa **−1,93**. Prosa: SP está a 4 desvios acima da média em população (extremo raro) mas quase 2 desvios **abaixo** em taxa de homicídios — o mesmo estado, dois z-scores opostos, cada um em sua escala. É essa padronização que a Normal (Cap. 2, seção 2.5) usa como referência, e que o widget abaixo já emprega para mexer no desvio sem tocar na média. 1 exercício.

- [ ] **Step 2: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|variabilidade' | head
H=_book/content/cap01/04-estimativas-variabilidade.html
grep -oE 'z-score da população de SP: 4,12|-1,93' "$H" | sort -u
grep -c 'Escores-padrão' "$H"
```
Expected: `4,12` e `-1,93` presentes; "Escores-padrão" ≥ 1.

- [ ] **Step 3: Commit**

```bash
git add content/cap01/04-estimativas-variabilidade.qmd
git commit -m "feat: cap1 — escores-padrao (z-scores)"
```

---

### Task 10: Cap. 1 — enriquecimentos "Curtose" e "Gráfico de violino" (seção 1.5)

**Files:**
- Modify: `content/cap01/05-distribuicao-dados.qmd`

**Interfaces:**
- A seção já importa `scipy.stats` como `stats` e tem `estado` no setup.

- [ ] **Step 1: Acrescentar "Curtose" ao lado da assimetria existente**

A seção já trata **assimetria** (subseção "Assimetria"). Acrescentar um trecho sobre **curtose** — o número que mede o peso das caudas (quão frequentes são os extremos), complementando a assimetria (que mede o lado). Não reescrever a assimetria; adicionar depois do cálculo de `assimetria-real`:
```{python}
#| label: curtose-real
print(f"Curtose da população das UFs : {num(stats.kurtosis(estado['Populacao']), 2)}")
print(f"Curtose da taxa de homicídios: {num(stats.kurtosis(estado['Taxa.Homicidios']), 2)}")
```
Saídas verificadas: população **8,78**; taxa **−0,88**. Prosa: curtose positiva alta (8,78) = caudas pesadas, dominadas pelo extremo de SP; curtose negativa (−0,88) = caudas leves, distribuição mais "achatada" que a normal. Remissão para frente às caudas longas do Cap. 2 (seção 2.6), onde a curtose reaparece medindo cauda gorda.

- [ ] **Step 2: Acrescentar a subseção "Gráfico de violino" após o boxplot**

Nova subseção `## Gráfico de violino` (após a subseção do boxplot, antes de "Tabela de frequência"), citando @weed. O violino mostra a **densidade** estimada espelhada, não só os cinco números do boxplot:
```{python}
#| label: fig-violino
#| fig-cap: "Violino da população dos estados: a largura em cada altura reflete a densidade estimada de observações naquele valor."
fig, ax = plt.subplots(figsize=(4, 5))
ax.violinplot(estado["Populacao"] / 1e6, showmedians=True)
ax.set_ylabel("População (milhões)")
ax.set_xticks([])
plt.tight_layout()
plt.show()
```
Prosa: onde o boxplot mostra quartis, o violino mostra a forma inteira — útil para ver bimodalidade ou concentração. **Ressalva do pythonbook (@weed):** a densidade é uma **estimativa suavizada**; ela pode sugerir massa onde não há dado (a cauda do violino se estende além do maior e do menor valor reais, insinuando observações que não existem), e com poucos dados — como os 27 estados — essa suavização engana mais do que informa. Preferir o violino quando há muitas observações. 1 exercício sobre a diferença boxplot × violino.

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|distribuicao-dados' | head
H=_book/content/cap01/05-distribuicao-dados.html
grep -oE 'Curtose da população das UFs : 8,78|-0,88' "$H" | sort -u
echo "violino=$(grep -c 'violino\|Violino' "$H")  imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo)"
```
Expected: `8,78` e `-0,88` presentes; "violino" ≥ 1; a contagem de `imgs` aumentou em 1 em relação ao original (o violino é um `<img>` novo).

- [ ] **Step 4: Commit**

```bash
git add content/cap01/05-distribuicao-dados.qmd
git commit -m "feat: cap1 — curtose e grafico de violino"
```

---

## FASE 3 — Revisão

### Task 11: Dois revisores (estatística + didática) → relatório → decisão do usuário

Executar **como dois subagentes** (o usuário pediu explicitamente os revisores). Cobrem **todo o conteúdo escrito**: Introdução (2 seções), Cap. 1 (8 seções + enriquecimentos), Cap. 2 (9 seções), Cap. 3 (5 seções). **Não** cobrem Cap. 4/5 (stubs).

**Files:**
- Create (efêmeros, no scratchpad): `revisao-estatistica.md`, `revisao-didatica.md`

- [ ] **Step 1: Render limpo do zero (garantir que os revisores leem a versão atual)**

Run:
```bash
make clean && make render 2>&1 | tail -3
```
Expected: `Output created: _book/index.html`.

- [ ] **Step 2: Dispatch do revisor de ESTATÍSTICA**

Subagente (modelo capaz) com a instrução: revisar, quanto à **correção estatística**, os fontes `content/intro/*.qmd`, `content/cap01/*.qmd`, `content/cap02/*.qmd`, `content/cap03/*.qmd`. Procurar: erros conceituais, definições imprecisas ou fracas, fórmulas incorretas, uso indevido de termo técnico, e **números na prosa que não batem com a saída do código**. Não reescrever nada — produzir um relatório em `revisao-estatistica.md` com achados classificados por severidade (**Crítico / Importante / Menor**), cada um com arquivo, trecho e correção sugerida. Entregar apenas o caminho do relatório e um resumo de contagem por severidade.

- [ ] **Step 3: Dispatch do revisor de DIDÁTICA**

Subagente (modelo capaz) com a instrução: revisar, quanto ao **fluxo didático e clareza**, os mesmos fontes. Procurar: quebras na sequência lógica de ponta a ponta (um conceito usado antes de definido), **remissões quebradas** (para trás/para frente após a reordenação — em especial nas seções da Normal, t, e amostragem), saltos conceituais, e explicações confusas ou inadequadas ao público (Eng. de Software / Sistemas de Informação). Não reescrever nada — relatório em `revisao-didatica.md`, mesma classificação por severidade. Entregar caminho + resumo.

- [ ] **Step 4: Consolidar e apresentar ao usuário (PARADA)**

Ler os dois relatórios, consolidar num resumo único (agrupado por severidade, sem duplicatas), e **apresentar ao usuário**. **Não aplicar nenhuma correção.** A decisão do que corrigir é do usuário — este é o estado terminal do plano.

```bash
echo "Relatórios em: revisao-estatistica.md e revisao-didatica.md"
```

---

## Verificação Final (portão de conclusão da Fase 2, antes da Fase 3)

- [ ] **Render limpo do zero**

```bash
make clean && make render 2>&1 | tail -3
```
Expected: sem erro.

- [ ] **Nenhum stub no conteúdo em escopo**

```bash
grep -rl 'Em construção' content/intro content/cap02 2>/dev/null && echo "AINDA HA STUB" || echo "intro e cap2 completos"
```
Expected: `intro e cap2 completos`. (Cap. 4 e 5 permanecem stubs — fora de escopo.)

- [ ] **Integridade de referências cruzadas**

```bash
grep -rnE 'seç(ão|ões) 2\.1[012]' content/cap02 content/cap03 | grep -v 'de @bruce2020' || echo "OK refs"
grep -rn 'Capítulo 3' content/cap02 || echo "OK cap"
```
Expected: `OK refs` e `OK cap`.

- [ ] **Números novos presentes no HTML**

```bash
grep -o '82,6%' _book/content/intro/02-paradoxo-simpson.html | head -1
grep -o '0,494' _book/content/cap02/01-o-que-e-probabilidade.html | head -1
grep -o '4,12'  _book/content/cap01/04-estimativas-variabilidade.html | head -1
grep -o '8,78'  _book/content/cap01/05-distribuicao-dados.html | head -1
grep -o 'VooAnterior' _book/content/cap01/03-estimativas-localizacao.html | head -1
```
Expected: cada um imprime seu valor.

- [ ] **Sementes**

```bash
grep -rnE 'default_rng|integers\(|\.sample\(|rvs\(' content/intro content/cap02/01-*.qmd content/cap02/02-*.qmd | grep -vE 'default_rng\(42\)|random_state=42' && echo "ERRO semente" || echo "sementes ok"
```
Expected: `sementes ok`.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída (fora os relatórios de revisão no scratchpad, que não são versionados).
