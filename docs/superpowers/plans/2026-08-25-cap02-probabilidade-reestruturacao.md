# Reestruturação de Probabilidade do Cap. 2 — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remover t/qui-quadrado/F/Poisson do Cap. 2 e adicionar probabilidade condicional e Bayes, contagem (permutação/combinação) e a distribuição hipergeométrica.

**Architecture:** Três fases. **Fase 1** move/renumera arquivos, cria stubs, conserta cross-refs e desacopla a cauda longa da t (render verde). **Fase 2** escreve as 3 seções novas. **Fase 3** atualiza cronograma/PID, regenera o notebook do Cap. 2 e o CLAUDE.md.

**Tech Stack:** Quarto (jupyter) · scipy.stats · numpy · math · `from formato import num` · `git mv`

**Spec:** `docs/superpowers/specs/2026-08-25-cap02-probabilidade-reestruturacao-design.md`

## Global Constraints

- **Render via container:** `make render` (Docker; sem Python no host). Se o render abortar no fim com stack do `quarto.js` (flake macOS bind-mount), rode `find . -name '*_files' -type d -not -path './.git/*' -not -path './_freeze/*' -exec rm -rf {} + ; find content -name '*.html' -delete ; rm -rf _book` e `make render` de novo (freeze quente).
- **Formato brasileiro:** `from formato import num`. Nunca `f"{x:,.1f}"`.
- **Semente obrigatória:** todo chunk com RNG usa `np.random.default_rng(42)` / `random_state=42`.
- **Caminho relativo à raiz:** `dados/...`, nunca `../../dados/`.
- **Callouts `de @bruce2020` (linha 4 das seções reaproveitadas) são IMUTÁVEIS.** Seções novas citam **@bussab2023**.
- **Modelo de voz:** `content/cap01/03-estimativas-localizacao.qmd`. Cada seção nova abre com `::: {.callout-note}`.
- Não mexer em `pyproject.toml`, `uv.lock`, `formato.py`, `dados/`.

## Números pré-computados no container (valores esperados não-negociáveis)

| Onde | Número |
|---|---|
| 2.3 Bayes falso-positivo | posterior = **0,0776** → impresso **7,8%** |
| 2.3 Bussab 5.15 | P(fraco\|aprovado) = **0,10** |
| 2.4 Contagem | 5! = **120**; P(5,3) = **60**; C(20,4) = **4845** |
| 2.4 Bussab 5.8 | P(2 defeituosas) = **0,217** |
| 2.6 Hipergeométrica | P(0 def) = **0,584**; P(≥1) = **0,416** |
| 2.6 Binomial-aprox | 0,9⁵ = **0,590** |

---

## Estrutura de arquivos (estado final do Cap. 2)

```
content/cap02/
├── index.qmd                                  (reescrito)
├── 01-o-que-e-probabilidade.qmd               (2.1, cross-ref na linha ~7)
├── 02-regras-probabilidade.qmd                (2.2, inalterado)
├── 03-probabilidade-condicional-bayes.qmd     (2.3, NOVO)
├── 04-contagem-permutacao-combinacao.qmd      (2.4, NOVO)
├── 05-distribuicao-binomial.qmd               (2.5, era 03)
├── 06-distribuicao-hipergeometrica.qmd        (2.6, NOVO)
├── 07-distribuicao-normal.qmd                 (2.7, era 05; abertura reescrita)
└── 08-caudas-longas.qmd                       (2.8, era 06; desacoplada da t)
```

---

## FASE 1 — Reestruturação e coerência

### Task 1: Mover/renumerar, stubs, `_quarto.yml`, `cap02/index.qmd`

**Files:**
- Remove/move: conforme os comandos abaixo
- Create (stubs): `03-probabilidade-condicional-bayes.qmd`, `04-contagem-permutacao-combinacao.qmd`, `06-distribuicao-hipergeometrica.qmd`
- Rewrite: `_quarto.yml`, `content/cap02/index.qmd`

- [ ] **Step 1: Remover e renumerar (nesta ordem)**

```bash
cd "$(git rev-parse --show-toplevel)"
git rm content/cap02/04-poisson.qmd content/cap02/07-distribuicao-t.qmd \
       content/cap02/08-qui-quadrado.qmd content/cap02/09-distribuicao-f.qmd
git mv content/cap02/06-caudas-longas.qmd        content/cap02/08-caudas-longas.qmd
git mv content/cap02/05-distribuicao-normal.qmd  content/cap02/07-distribuicao-normal.qmd
git mv content/cap02/03-distribuicao-binomial.qmd content/cap02/05-distribuicao-binomial.qmd
```

- [ ] **Step 2: Criar os 3 stubs (padrão do projeto)**

`content/cap02/03-probabilidade-condicional-bayes.qmd`:
```markdown
# Probabilidade Condicional e Teorema de Bayes

::: {.callout-note}
Esta seção se baseia nos capítulos 5.3 e 5.4 de @bussab2023.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
```

`content/cap02/04-contagem-permutacao-combinacao.qmd`:
```markdown
# Contagem: Permutação e Combinação

::: {.callout-note}
Esta seção se baseia na seção 5.2 de @bussab2023.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
```

`content/cap02/06-distribuicao-hipergeometrica.qmd`:
```markdown
# Distribuição Hipergeométrica

::: {.callout-note}
Esta seção se baseia na seção 6.6.4 de @bussab2023.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
```

- [ ] **Step 3: Reescrever o bloco `cap02` do `_quarto.yml`**

Substituir a lista de seções do Cap. 2 (o `part: "Capítulo 2: Probabilidade e Distribuições"`) por:
```yaml
    - part: "Capítulo 2: Probabilidade e Distribuições"
      chapters:
        - href: content/cap02/index.qmd
          text: "Visão Geral"
        - href: content/cap02/01-o-que-e-probabilidade.qmd
          text: "O que é Probabilidade"
        - href: content/cap02/02-regras-probabilidade.qmd
          text: "Regras de Probabilidade"
        - href: content/cap02/03-probabilidade-condicional-bayes.qmd
          text: "Probabilidade Condicional e Bayes"
        - href: content/cap02/04-contagem-permutacao-combinacao.qmd
          text: "Contagem: Permutação e Combinação"
        - href: content/cap02/05-distribuicao-binomial.qmd
          text: "Distribuição Binomial"
        - href: content/cap02/06-distribuicao-hipergeometrica.qmd
          text: "Distribuição Hipergeométrica"
        - href: content/cap02/07-distribuicao-normal.qmd
          text: "Distribuição Normal"
        - href: content/cap02/08-caudas-longas.qmd
          text: "Distribuições de Cauda Longa"
```

- [ ] **Step 4: Reescrever `content/cap02/index.qmd`**

Ler antes `content/cap01/index.qmd` para o padrão. O novo `cap02/index.qmd`: título "Probabilidade e Distribuições"; callout de fontes (Bruce + Weed + Bussab); intro; objetivos (entender probabilidade e suas regras; **probabilidade condicional e Bayes**; **contagem**; e as distribuições **binomial, hipergeométrica, normal e de cauda longa** — sem Poisson/t/qui²/F); tabela das 8 seções (2.1–2.8). Manter o link "Abrir no Colab" do `capitulo-02.ipynb` que já existe.

- [ ] **Step 5: Renderizar e verificar o esqueleto**

Run:
```bash
make clean && make render 2>&1 | tail -3
find _book/content/cap02 -name '*.html' | sort | sed 's#.*/cap02/##'
grep -rl 'Em construção' content/cap02 | sort
```
Expected: render sem erro; 9 htmls (index + 01–08, sem poisson/t/qui/f); os 3 stubs (03, 04, 06) aparecem em "Em construção".

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: cap2 — remove t/qui2/F/poisson, renumera, stubs de condicional/contagem/hipergeometrica"
```

---

### Task 2: Cross-refs, desacoplar cauda longa da t, aberturas

**Files:**
- Modify: `content/cap02/01-o-que-e-probabilidade.qmd`, `07-distribuicao-normal.qmd`, `08-caudas-longas.qmd`, `content/cap03/index.qmd`

- [ ] **Step 1: `cap02/01-o-que-e-probabilidade.qmd` (~linha 7)**

Onde a prosa enumera as distribuições do capítulo (hoje inclui Poisson e t), trocar pela nova lista: "a binomial, a hipergeométrica, a normal e as de cauda longa". Se a linha mencionar a próxima seção formalizar probabilidade condicional, manter (a 2.3 agora entrega isso).

- [ ] **Step 2: `cap02/07-distribuicao-normal.qmd` (abertura, ~linha 20)**

Trocar "Depois das duas distribuições discretas (binomial e Poisson), chega a mais importante das contínuas — a normal…" por "Depois das distribuições discretas (binomial e hipergeométrica), chega a mais importante das contínuas — a normal…".

- [ ] **Step 3: `cap02/08-caudas-longas.qmd` — desacoplar da t**

Ler a seção. Correções:
- Remissão "seção 2.6" (normal) → **2.7**.
- **Desacoplar da t:** a seção usa `stats.t.rvs(df=3, ...)` como amostra de cauda gorda. Manter o chunk (é só uma amostra pesada), mas reescrever a prosa que a chama de "distribuição t, o assunto da próxima seção" — não há seção t. Substituir por algo como "uma amostra de cauda gorda (gerada de uma distribuição de caudas pesadas)"; o fecho não deve prometer nenhuma seção t. A curtose já foi introduzida no Cap. 1, então pode-se remeter a ela. O callout linha 4 (`seção 2.7 de @bruce2020`) permanece.

- [ ] **Step 4: `cap03/index.qmd` (~linha 9)**

Reescrever a frase "As últimas distribuições do Capítulo 2 — qui-quadrado e F — apontaram para os testes de significância; mas, antes de testar…" para não citar qui²/F (removidas). Ex.: "Antes de testar hipóteses, é preciso entender como uma amostra se relaciona com a população que a gerou e como estimar a partir dela. É o que este capítulo cobre." Manter o resto.

- [ ] **Step 5: Integridade + render**

Run:
```bash
grep -rniE 'poisson|distribuição t\b|t de student|qui-quadrado|distribuição f\b' content/cap02 content/cap03 index.qmd --include='*.qmd' | grep -viE 'de @bruce2020' || echo "OK: sem menções órfãs"
make render 2>&1 | tail -3
```
Expected: `OK: sem menções órfãs` (ou só ocorrências legítimas em contexto histórico que você julgar aceitáveis); render sem erro.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "fix: cap2 — cross-refs pos-remocao e desacopla cauda longa da t"
```

---

### Task 3: `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Atualizar a nota do Cap. 2**

Onde o `CLAUDE.md` descreve as distribuições do Cap. 2 e a nota "Escopo reduzido" (que menciona remissões de qui²/F), atualizar: o Cap. 2 agora cobre probabilidade condicional e Bayes, contagem, e as distribuições binomial, hipergeométrica, normal e de cauda longa; t, qui-quadrado, F e Poisson **foram removidos**. Remover a frase sobre "as distribuições qui-quadrado e F seguem no Cap. 2, mas suas remissões…" (elas não seguem mais). Acrescentar que as seções de condicional/Bayes, contagem e hipergeométrica vêm de **@bussab2023**.

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: CLAUDE.md — atualiza escopo do cap2 (condicional/bayes, contagem, hipergeometrica)"
```

---

## FASE 2 — Conteúdo novo

### Task 4: 2.3 — Probabilidade condicional e Teorema de Bayes

**Files:**
- Modify: `content/cap02/03-probabilidade-condicional-bayes.qmd`

- [ ] **Step 1: Escrever a seção**

Manter `# Probabilidade Condicional e Teorema de Bayes` + callout @bussab2023. Setup oculto: `import numpy as np`, `from formato import num`.

Arco (prosa + chunks), na ordem: (1) probabilidade condicional $P(A\mid B)=P(A\cap B)/P(B)$, retomando a regra da multiplicação da 2.2, distinguindo **prior** de **posterior**; (2) independência revisitada $P(A\mid B)=P(A)$; (3) regra da probabilidade total (partição, árvore); (4) Bayes (2 eventos → geral), enquadrado como "inverter a condicional fácil na difícil"; (5) armadilha da taxa-base como fechamento.

Chunk do exemplo-âncora (detecção de anomalia; números verificados):
```{python}
#| label: bayes-falso-positivo
prevalencia, sensibilidade, falso_positivo = 0.01, 0.80, 0.096
posterior = (prevalencia * sensibilidade) / (
    prevalencia * sensibilidade + (1 - prevalencia) * falso_positivo)
print(f"P(evento real | alarme disparou) = {num(posterior * 100, 1)}%")
```
Saída verificada: **7,8%**. Prosa: o alarme acerta 80% dos eventos reais, mas, como o evento é raro (1%), a maioria dos alarmes é falso-positivo — só ~7,8% dos alarmes são evento real, contra a intuição de ~80%.

Chunk Monte Carlo (semente — segunda prova por frequências naturais):
```{python}
#| label: bayes-monte-carlo
rng = np.random.default_rng(42)
n = 1_000_000
tem_evento = rng.random(n) < prevalencia
alarme = np.where(tem_evento, rng.random(n) < sensibilidade, rng.random(n) < falso_positivo)
positivos = int(alarme.sum())
reais = int((alarme & tem_evento).sum())
print(f"De {num(positivos, 0)} alarmes, {num(reais, 0)} eram evento real: {num(100 * reais / positivos, 1)}%")
```
Saída: um valor ≈ **7,8%** (conferir no render; a semente trava). Prosa: a simulação confirma a conta.

Chunk Bayes com partição (Bussab 5.15):
```{python}
#| label: bayes-particao
prior = {"bom": 0.25, "médio": 0.50, "fraco": 0.25}
aprovado_dado = {"bom": 0.80, "médio": 0.50, "fraco": 0.20}
evidencia = sum(prior[c] * aprovado_dado[c] for c in prior)
posterior_fraco = prior["fraco"] * aprovado_dado["fraco"] / evidencia
print(f"P(candidato fraco | foi aprovado) = {num(posterior_fraco, 2)}")
```
Saída verificada: **0,10**. Prosa: dos aprovados, só 10% são fracos — Bayes atualiza a proporção de fracos (25% a priori) para 10% depois da evidência "foi aprovado".

Callout `.conceito` com a fórmula geral de Bayes e o aviso: hipóteses precisam formar **partição** (exclusivas e exaustivas). Links complementares (callout, sem recriar): 3Blue1Brown e Seeing Theory. **3 exercícios** em `callout-tip collapse`, sendo um o **Monty Hall** com simulação (`default_rng(42)`; trocar dá ~2/3).

- [ ] **Step 2: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|condicional-bayes' | head; echo "---"
H=_book/content/cap02/03-probabilidade-condicional-bayes.html
grep -oE '7,8%|0,10' "$H" | sort -u | tr '\n' ' '; echo
echo "exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
grep -nE 'default_rng|\.random\(' content/cap02/03-probabilidade-condicional-bayes.qmd | grep -v 'default_rng(42)' || echo "sementes ok"
```
Expected: `7,8%` e `0,10` presentes; exerc=3; stub=0; sementes ok.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/03-probabilidade-condicional-bayes.qmd
git commit -m "feat: cap2 2.3 — probabilidade condicional e teorema de bayes"
```

---

### Task 5: 2.4 — Contagem: permutação e combinação

**Files:**
- Modify: `content/cap02/04-contagem-permutacao-combinacao.qmd`

- [ ] **Step 1: Escrever a seção (curta)**

Manter `# Contagem: Permutação e Combinação` + callout @bussab2023. Setup oculto: `from math import factorial, perm, comb`, `from formato import num`.

Cobrir, curto: (1) princípio multiplicativo (um parágrafo, ex. senha de 2 dígitos); (2) permutação $P(n,k)=n!/(n-k)!$ — arranjos ordenados; (3) combinação $\binom{n}{k}=n!/(k!(n-k)!)$ — subconjuntos sem ordem; regra prática **"a ordem importa?"**. Parar aí (nada de arranjo com repetição/anagramas).

Chunk das fórmulas:
```{python}
#| label: contagem
print(f"5! = {factorial(5)}")                    # permutações de 5 elementos
print(f"P(5,3) = {perm(5, 3)}")                  # pódios ordenados de 3 entre 5
print(f"C(20,4) = {num(comb(20, 4), 0)}")        # amostras (sem ordem) de 4 entre 20
```
Saídas verificadas: `120`, `60`, `4.845`.

Chunk-ponte (Bussab 5.8 — proto-hipergeométrica):
```{python}
#| label: contagem-lote
p = comb(5, 2) * comb(15, 2) / comb(20, 4)
print(f"P(2 defeituosas entre as 4 sorteadas) = {num(p, 3)}")
```
Saída verificada: **0,217**. Prosa: num lote de 20 com 5 defeituosas, sorteando 4 sem ordem, a chance de sair exatamente 2 defeituosas — a conta é toda de combinações, e é exatamente a forma da hipergeométrica (próxima seção). 2 exercícios.

- [ ] **Step 2: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|contagem' | head; echo "---"
H=_book/content/cap02/04-contagem-permutacao-combinacao.html
grep -oE '5! = 120|P\(5,3\) = 60|4\.845|0,217' "$H" | sort -u
echo "exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
```
Expected: `120`, `60`, `4.845`, `0,217`; exerc=2; stub=0.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/04-contagem-permutacao-combinacao.qmd
git commit -m "feat: cap2 2.4 — contagem: permutacao e combinacao"
```

---

### Task 6: 2.6 — Distribuição hipergeométrica

**Files:**
- Modify: `content/cap02/06-distribuicao-hipergeometrica.qmd`

- [ ] **Step 1: Escrever a seção**

Manter `# Distribuição Hipergeométrica` + callout @bussab2023. Setup oculto: `import numpy as np`, `import matplotlib.pyplot as plt`, `from scipy.stats import hypergeom, binom`, `from formato import num`, `plt.rcParams["figure.figsize"] = (7, 4)`.

Cobrir: motivação (amostragem **sem reposição** de população finita — cada retirada muda a composição; contraste com a binomial, com reposição); fórmula $P(X=k)=\binom{r}{k}\binom{N-r}{n-k}/\binom{N}{n}$; exemplo de controle de qualidade transposto para software (amostrar casos de teste/bugs); nomenclatura do scipy; contraste com a binomial + regra dos 10%; aviso do suporte restrito de $k$; gancho para o Cap. 3 (correção de população finita).

Chunk principal (nomenclatura documentada; números verificados):
```{python}
#| label: hipergeometrica
# scipy: hypergeom(M, n, N) = (população, sucessos na população, tamanho da amostra)
# livro : N=100 (lote), r=10 (defeituosas), n=5 (amostra sem reposição)
lote = hypergeom(100, 10, 5)
print(f"P(0 defeituosas na amostra) = {num(float(lote.pmf(0)), 3)}")
print(f"P(ao menos 1 defeituosa)    = {num(float(1 - lote.cdf(0)), 3)}")
```
Saídas verificadas: **0,584** e **0,416**.

Chunk do contraste com a binomial (regra dos 10%):
```{python}
#| label: hiper-vs-binomial
print(f"Hipergeométrica (sem reposição): {num(float(lote.pmf(0)), 3)}")
print(f"Binomial (com reposição, p=0,1): {num(float(binom.pmf(0, 5, 0.1)), 3)}")
```
Saída verificada: 0,584 vs **0,590**. Prosa: como a amostra (5) é só 5% do lote (100), tirar sem reposição quase não muda a composição — a binomial já aproxima bem (diferença ~1%). Com amostra grande em relação à população, a aproximação falharia.

Figura (pmf discreta → barras):
```{python}
#| label: fig-hipergeometrica
#| fig-cap: "Distribuição hipergeométrica: probabilidade de cada número de defeituosas numa amostra de 5, de um lote de 100 com 10 defeituosas."
k = np.arange(0, 6)
fig, ax = plt.subplots()
ax.bar(k, lote.pmf(k), color="#b0c4d8", edgecolor="white")
ax.set_xlabel("Número de defeituosas na amostra")
ax.set_ylabel("Probabilidade")
plt.tight_layout()
plt.show()
```
2 exercícios em `callout-tip collapse` (um sobre quando usar hipergeométrica × binomial).

- [ ] **Step 2: Renderizar e verificar**

Run:
```bash
make render 2>&1 | grep -iE 'error|hipergeometrica' | head; echo "---"
H=_book/content/cap02/06-distribuicao-hipergeometrica.html
grep -oE '0,584|0,416|0,590' "$H" | sort -u | tr '\n' ' '; echo
echo "imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo) exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
```
Expected: `0,584 0,416 0,590`; imgs=1, exerc=2, stub=0.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/06-distribuicao-hipergeometrica.qmd
git commit -m "feat: cap2 2.6 — distribuicao hipergeometrica"
```

---

## FASE 3 — Downstream

### Task 7: Cronograma (home) + PID

**Files:**
- Modify: `index.qmd`, `docs/PID - Bases de Sistema de Informação 3 - Estatística e Probabilidade - 2.2026.xlsx`

- [ ] **Step 1: `index.qmd` — bullet "Sobre" + cronograma**

- No bullet de "Sobre a Disciplina" que lista "Probabilidade e distribuições: normal, binomial, Poisson, t, qui-quadrado e F", trocar por "Probabilidade: condicional, Bayes, contagem; e distribuições — binomial, hipergeométrica, normal e de cauda longa".
- No **cronograma**, re-mapear as aulas do Cap. 2 (hoje citam Poisson/t/qui²/F). Sugestão:
  - aula 6 (25/09): "2 — Probabilidade e Distribuições: probabilidade · regras · condicional e Bayes"
  - aula 7 (02/10): "2 — Contagem · binomial · hipergeométrica"
  - aula 8 (09/10): "2 — Normal · cauda longa · **revisão para a Prova 1**"

- [ ] **Step 2: PID — cronograma (rows 28–30)**

Ler os valores atuais das linhas 28–30 do PID (aulas 6–8, datas 25/09, 02/10, 09/10) e reescrever o conteúdo (coluna C) para bater com o novo cronograma da home. Usar o `.venv/bin/python` com openpyxl (já instalado):
```bash
cd "$(git rev-parse --show-toplevel)"
.venv/bin/python - <<'PY'
import openpyxl
out="docs/PID - Bases de Sistema de Informação 3 - Estatística e Probabilidade - 2.2026.xlsx"
wb=openpyxl.load_workbook(out); ws=wb[wb.sheetnames[0]]
ws["C28"]=("Capítulo 2 — Probabilidade e Distribuições: o que é probabilidade; regras de probabilidade; "
           "probabilidade condicional e Teorema de Bayes.")
ws["C29"]=("Capítulo 2 — Contagem (permutação e combinação); distribuição binomial; distribuição hipergeométrica.")
ws["C30"]=("Capítulo 2 — Distribuição normal; distribuições de cauda longa. Revisão para a Prova 1.")
wb.save(out); print("PID atualizado")
PY
```

- [ ] **Step 3: Render + commit**

```bash
make render 2>&1 | tail -3
grep -o 'condicional e Bayes\|hipergeométrica' _book/index.html | sort -u
git add index.qmd "docs/PID - Bases de Sistema de Informação 3 - Estatística e Probabilidade - 2.2026.xlsx"
git commit -m "docs: cronograma e PID — conteudo do cap2 (condicional/bayes, contagem, hipergeometrica)"
```

---

### Task 8: Regenerar o notebook do Cap. 2

**Files:**
- Modify: `notebooks/capitulo-02.ipynb`

**Interfaces:**
- Consome: os scripts de scratchpad `nb_tool.py` (manifesto/assemble) usados nos notebooks anteriores. Se não existirem mais, reconstruir a extração no mesmo padrão: código-only a partir dos `.qmd` do Cap. 2, com uma explicação autoral curta por célula (subagente), dados por URL raw, `curl formato.py` no setup, widgets/`ojs_define` pulados.

- [ ] **Step 1: Gerar o manifesto do Cap. 2**

Extrair as células de código das 8 seções do Cap. 2 (mesma lógica dos notebooks 1–3: só `{python}`, pular `{ojs}`/`ojs_define`, reescrever `dados/` → URL raw). O Cap. 2 novo usa `scipy.stats.hypergeom`, `math.comb/perm/factorial` — todos já no container e no Colab (nada de `pip install` novo além do que já havia).

- [ ] **Step 2: Explicações autorais (subagente)**

Dispatchar um subagente (sonnet) que lê os `.qmd` do Cap. 2 + o manifesto e escreve, para cada célula de código, uma explicação curta (1–2 frases, PT-BR, baseada no livro), gravando um JSON `índice → texto`. Mesmo prompt/estilo dos notebooks 1–3.

- [ ] **Step 3: Remontar e executar**

Remontar `notebooks/capitulo-02.ipynb` (setup com `curl formato.py`; por seção, cabeçalho + texto + código). Executar de ponta a ponta no container:
```bash
docker compose run --rm --no-deps livro bash -lc '
cd /livro && jupyter nbconvert --to notebook --execute --output /tmp/e.ipynb "notebooks/capitulo-02.ipynb" >/tmp/l 2>&1; echo exit=$?
python -c "import json;nb=json.load(open(\"/tmp/e.ipynb\"));print(\"erros=\",sum(1 for c in nb[\"cells\"] if c[\"cell_type\"]==\"code\" for o in c.get(\"outputs\",[]) if o.get(\"output_type\")==\"error\"))"'
```
Expected: `exit=0` e `erros= 0`.

- [ ] **Step 4: Commit**

```bash
git add notebooks/capitulo-02.ipynb
git commit -m "docs: regenera notebook do cap2 (condicional/bayes, contagem, hipergeometrica)"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean && make render 2>&1 | tail -3
```
Expected: sem erro.

- [ ] **Cap. 2 sem stubs; 8 seções**

```bash
grep -rl 'Em construção' content/cap02 && echo "AINDA HA STUB" || echo "cap2 completo (8 secoes)"
ls content/cap02/*.qmd | wc -l   # 9 (index + 8)
```
Expected: `cap2 completo (8 secoes)`; `9`.

- [ ] **Nenhuma menção órfã a t/qui²/F/Poisson**

```bash
grep -rniE 'poisson|distribuição t\b|t de student|qui-quadrado|distribuição f\b' content/cap02 content/cap03 index.qmd --include='*.qmd' | grep -viE 'de @bruce2020|cauda' || echo "OK"
```
Expected: `OK` (ou só ocorrências que você aprovou).

- [ ] **Números novos no HTML**

```bash
grep -o '7,8%' _book/content/cap02/03-probabilidade-condicional-bayes.html | head -1
grep -o '0,217' _book/content/cap02/04-contagem-permutacao-combinacao.html | head -1
grep -o '0,584' _book/content/cap02/06-distribuicao-hipergeometrica.html | head -1
```
Expected: cada um imprime o número.

- [ ] **Sementes**

```bash
grep -rnE 'default_rng|\.random\(|rvs\(' content/cap02/03-*.qmd content/cap02/06-*.qmd content/cap02/08-*.qmd | grep -vE 'default_rng\(42\)|random_state=42' && echo "ERRO" || echo "sementes ok"
```
Expected: `sementes ok`.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída (fora scratch gitignored).
