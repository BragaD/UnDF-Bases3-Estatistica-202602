# Catálogo de Distribuições (2.6–2.12) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Escrever as sete seções de referência que fecham o Capítulo 2 — normal, caudas longas, t de Student, binomial, qui-quadrado, F e Poisson.

**Architecture:** Sete `.qmd` (hoje stubs), agrupados em 5 tasks por afinidade. Cada seção é compacta (~70 linhas): forma da distribuição via `scipy.stats`, quando aparece, código mínimo, 2 exercícios. Padrão de estilo herdado do Capítulo 1.

**Tech Stack:** Quarto (jupyter) · scipy.stats · numpy · pandas · matplotlib

**Spec:** `docs/superpowers/specs/2026-07-22-cap02-distribuicoes-design.md`

## Global Constraints

- **Catálogo compacto:** cada seção ~70 linhas, **2 exercícios** (não 3), resposta em `::: {.callout-tip collapse="true"}`.
- **Formato brasileiro** em todo número impresso: `from formato import num`. Nunca `f"{x:,.1f}"`.
- **Semente obrigatória** em todo chunk que sorteia (só a t(3) da 2.7 e QQ com amostra): `random_state=42`. O QQ do `loans_income` (2.6) usa o dataset inteiro, não sorteia.
- **Caminho relativo à raiz:** `dados/loans_income.csv`. Nunca `../../dados/`.
- **Português brasileiro.** Cada seção abre com `::: {.callout-note}` "Esta seção corresponde à seção 2.N de @bruce2020."
- **Um gráfico por seção** (a forma da distribuição, via scipy). Exceção: a **2.6** tem dois — a normal com as faixas 68–95–99,7 **e** o QQ-plot do `loans_income` —, porque a forma e o teste visual ensinam coisas diferentes.
- **Render sempre via container:** `make render`. Não crie `AGENTS.md`. Não mexa em `_quarto.yml`, `pyproject.toml`, `uv.lock`, `formato.py`, `dados/`.
- **Modelo de voz:** `content/cap01/03-estimativas-localizacao.qmd`. Leia antes de escrever.

## Os números (todos medidos no container)

| Seção | Números |
|---|---|
| 2.6 | assimetria do `loans_income` = **1,05** (renda não é normal) |
| 2.7 | curtose da t(3) = **6,8** (cauda gorda; normal = 0) |
| 2.8 | P(&#124;X&#124;>2): t(1)=**0,295**, t(5)=**0,102**, t(30)=**0,055**, normal=**0,046** |
| 2.9 | `binom.pmf(2;5;0,1)`=**0,0729**, `cdf(2;5;0,1)`=**0,9914** |
| 2.10 | média de χ²(k) = **k**; valor crítico 5% de χ²(5) = **11,07** |
| 2.11 | valor crítico 5% de F(5,10) = **3,33** |
| 2.12 | Poisson(λ=2): P(0)=**0,135**, P(≥5)=**0,053**; exponencial: 2/hora → **30 min** entre eventos |

---

## Estrutura de Arquivos

| Arquivo | Task |
|---|---|
| `content/cap02/06-distribuicao-normal.qmd` | 1 |
| `content/cap02/07-caudas-longas.qmd` | 1 |
| `content/cap02/08-distribuicao-t.qmd` | 2 |
| `content/cap02/09-distribuicao-binomial.qmd` | 3 |
| `content/cap02/10-qui-quadrado.qmd` | 4 |
| `content/cap02/11-distribuicao-f.qmd` | 4 |
| `content/cap02/12-poisson.qmd` | 5 |

---

## Task 1: 2.6 Normal + 2.7 Caudas Longas

As duas seções de QQ-plot, agrupadas porque compartilham a técnica (`scipy.stats.probplot`) e formam um par: a 2.6 mostra dado que **não** é normal, a 2.7 mostra o que é cauda gorda.

**Files:**
- Modify: `content/cap02/06-distribuicao-normal.qmd`, `content/cap02/07-caudas-longas.qmd`

**Interfaces:**
- Consumes: `dados/loans_income.csv` (2.6); `scipy.stats` (ambas).

- [ ] **Step 1: Escrever a 2.6 — Normal**

Pontos: a normal como referência (simétrica, média+desvio, regra 68–95–99,7); o QQ-plot como teste visual — pontos sobre a reta = normal, desvios nas pontas = não.

Chunk `setup` (oculto): `import numpy as np`, `import pandas as pd`, `import matplotlib.pyplot as plt`, `from scipy import stats`, `from formato import num`, e `renda = pd.read_csv("dados/loans_income.csv").rename(columns={"x": "Renda"})["Renda"]`.

A forma da normal:
```python
#| label: fig-normal
#| fig-cap: "A distribuição normal: simétrica, com 68% da massa a menos de 1 desvio da média, 95% a menos de 2, e 99,7% a menos de 3."
x = np.linspace(-4, 4, 200)
fig, ax = plt.subplots()
ax.plot(x, stats.norm.pdf(x), color="#2c3e50", linewidth=2)
for k, cor in [(1, "#27ae60"), (2, "#e67e22"), (3, "#c0392b")]:
    ax.axvline(k, color=cor, linestyle="--", alpha=0.6)
    ax.axvline(-k, color=cor, linestyle="--", alpha=0.6)
ax.set_xlabel("Desvios em relação à média")
ax.set_ylabel("Densidade")
plt.tight_layout()
plt.show()
```

O QQ-plot do dado real:
```python
#| label: fig-qq-renda
#| fig-cap: "QQ-plot da renda contra a normal. Se a renda fosse normal, os pontos seguiriam a reta. A curva para cima na ponta direita revela a cauda longa da renda."
fig, ax = plt.subplots()
stats.probplot(renda, dist="norm", plot=ax)
ax.set_title("")
ax.set_xlabel("Quantis teóricos (normal)")
ax.set_ylabel("Quantis da renda")
plt.tight_layout()
plt.show()
```

A assimetria que confirma:
```python
#| label: assimetria
print(f"Assimetria da renda: {num(stats.skew(renda), 2)}")
```
Saída real: `1,05`. Prosa: assimetria 0 seria normal; 1,05 é cauda à direita — a renda **não** é normal, e o QQ-plot mostra isso pela curvatura. Lição honesta: a normal é útil, mas muitos dados reais não a seguem.

**2 exercícios:**
1. Um QQ-plot tem os pontos quase sobre a reta, exceto os dois ou três das pontas, que se afastam. O que isso indica? *Resposta:* o corpo dos dados é aproximadamente normal, mas as caudas são mais pesadas (ou há outliers) — extremos mais frequentes do que a normal preveria. É o padrão de dados com cauda longa, tema da 2.7.
2. Por que a regra 68–95–99,7 é útil na prática? *Resposta:* dá uma referência rápida sem calcular nada: se um dado é aproximadamente normal, ~95% cai a menos de 2 desvios da média, então um valor a 3+ desvios é raro (menos de 0,3%) e merece atenção. É a base da detecção de outliers e do controle de qualidade.

- [ ] **Step 2: Escrever a 2.7 — Caudas Longas**

Pontos: cauda mais gorda que a normal = extremos mais frequentes do que a normal prevê. É por isso que "eventos de 6 sigma" ocorrem em finanças com frequência que a normal chamaria de impossível.

Chunk `setup` (oculto): numpy, matplotlib, `from scipy import stats`, `from formato import num`.

**Nota ao implementador — por que t(3) e não dado de ações:** o `sp500_data.csv.gz` foi medido e descartado (7% de retornos impossíveis, curtose ~1 sem cauda gorda real). A t(3) é o exemplo canônico de cauda gorda e antecipa a 2.8. NÃO use o sp500 aqui.

```python
#| label: cauda-gorda
amostra = stats.t.rvs(df=3, size=1000, random_state=42)
print(f"Curtose da amostra t(3): {num(stats.kurtosis(amostra), 1)}")
print(f"(Curtose de uma normal: 0)")
```
Saída real: `6,8`. Curtose alta = cauda gorda.

O QQ-plot que mostra a curva em S:
```python
#| label: fig-qq-cauda
#| fig-cap: "QQ-plot de uma amostra de cauda gorda contra a normal. As pontas se afastam da reta — para cima à direita, para baixo à esquerda: a curva em S dos extremos mais extremos que o normal previa."
fig, ax = plt.subplots()
stats.probplot(amostra, dist="norm", plot=ax)
ax.set_title("")
ax.set_xlabel("Quantis teóricos (normal)")
ax.set_ylabel("Quantis da amostra")
plt.tight_layout()
plt.show()
```

Prosa: enquanto a renda (2.6) curvava só de um lado (assimetria), aqui a curva é em **S** — as duas pontas se afastam, porque a cauda gorda é simétrica: valores extremos, para cima e para baixo, são mais comuns que a normal prevê. E a remissão: essa amostra veio de uma **distribuição t**, o assunto da próxima seção.

**2 exercícios:**
1. Por que modelar retornos financeiros com a normal subestima o risco? *Resposta:* retornos têm cauda gorda — quedas extremas acontecem com frequência muito maior do que a normal prevê. Um modelo normal chamaria a crise de "evento de 6 sigma, uma vez em milhões de anos"; na prática, crises ocorrem a cada década. Subestimar a cauda subestima a chance de perdas catastróficas.
2. No QQ-plot de cauda gorda, por que a curva é em S e não uma curvatura só de um lado? *Resposta:* cauda gorda é simétrica — os dois extremos são mais pesados que o normal. A ponta direita sobe (valores altos ainda mais altos que o esperado), a esquerda desce (valores baixos ainda mais baixos). Assimetria (como a renda) curva um lado só; cauda gorda curva os dois.

- [ ] **Step 3: Renderizar e conferir**

Run:
```bash
make render
grep -oE 'Assimetria da renda: 1,05' _book/content/cap02/06-distribuicao-normal.html
grep -oE 'Curtose da amostra t\(3\): 6,8' _book/content/cap02/07-caudas-longas.html
for f in 06-distribuicao-normal 07-caudas-longas; do
  H=_book/content/cap02/$f.html
  echo "$f: imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo) exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
done
```
Expected: `1,05` e `6,8` presentes; cada seção com imgs=2 (2.6: normal + QQ; 2.7: — só o QQ é `<img>`, então imgs=1), exerc=2, stub=0.

- [ ] **Step 4: Conferir a semente**

Run: `grep -nE 'rvs\(|sample\(|np\.random' content/cap02/0[67]-*.qmd | grep -v 'random_state=42'`
Expected: nenhuma saída.

- [ ] **Step 5: Commit**

```bash
git add content/cap02/06-distribuicao-normal.qmd content/cap02/07-caudas-longas.qmd
git commit -m "feat: secoes 2.6 normal e 2.7 caudas longas"
```

---

## Task 2: 2.8 — Distribuição t de Student

**Files:**
- Modify: `content/cap02/08-distribuicao-t.qmd`

**Interfaces:**
- Consumes: `scipy.stats`.

- [ ] **Step 1: Escrever a seção**

Pontos: a t parece a normal, mas com caudas mais gordas; as caudas afinam conforme os **graus de liberdade** crescem, até virar a normal. É a distribuição do erro de estimar a média com amostra pequena — a que a seção 2.5 usava implicitamente ao construir intervalos.

Chunk `setup` (oculto): numpy, matplotlib, `from scipy import stats`, `from formato import num`.

A forma, comparando t e normal:
```python
#| label: fig-t
#| fig-cap: "A distribuição t com poucos graus de liberdade tem caudas mais gordas que a normal. Conforme os graus de liberdade crescem, ela se aproxima da normal."
x = np.linspace(-4, 4, 200)
fig, ax = plt.subplots()
ax.plot(x, stats.norm.pdf(x), color="#2c3e50", linewidth=2, label="Normal")
for gl, cor in [(1, "#c0392b"), (5, "#e67e22")]:
    ax.plot(x, stats.t.pdf(x, gl), color=cor, linewidth=2, linestyle="--", label=f"t({gl})")
ax.set_xlabel("Valor")
ax.set_ylabel("Densidade")
ax.legend()
plt.tight_layout()
plt.show()
```

A convergência para a normal:
```python
#| label: convergencia
print(f"{'distribuição':>14}  {'P(|X| > 2)':>10}")
for gl in [1, 5, 30]:
    print(f"{'t(' + str(gl) + ')':>14}  {num(2 * stats.t.sf(2, gl), 3):>10}")
print(f"{'normal':>14}  {num(2 * stats.norm.sf(2), 3):>10}")
```
Saídas reais: t(1)=`0,295`, t(5)=`0,102`, t(30)=`0,055`, normal=`0,046`. Prosa: com 30 gl a t já é quase a normal — por isso, com amostra grande, tanto faz; com amostra pequena, a t (mais conservadora, caudas mais gordas) é a correta.

**Callout `.conceito`:** os graus de liberdade são, grosso modo, "quanta informação a amostra tem". Poucos gl → muita incerteza → caudas gordas → intervalos mais largos. Muitos gl → a t vira a normal.

**2 exercícios:**
1. Por que usar a t em vez da normal ao construir um intervalo de confiança de uma amostra de 10 observações? *Resposta:* com 10 observações há pouca informação, e o desvio-padrão da população é estimado (não conhecido). A t, de caudas mais gordas, compensa essa incerteza extra com um intervalo mais largo — mais honesto. Usar a normal com amostra pequena produz intervalos estreitos demais, que erram mais do que dizem.
2. A tabela mostra que t(30) e a normal são quase iguais. Que consequência prática isso tem? *Resposta:* com amostras de ~30 ou mais, a diferença entre usar a t ou a normal é desprezível. É a origem da "regra do 30" que muitos cursos citam — acima disso, a aproximação normal já serve.

- [ ] **Step 2: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap02/08-distribuicao-t.html
grep -oE '0,295|0,102|0,055|0,046' "$H" | sort -u | tr '\n' ' '; echo
echo "imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo) exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
```
Expected: os quatro valores; imgs=1, exerc=2, stub=0.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/08-distribuicao-t.qmd
git commit -m "feat: secao 2.8 distribuicao t de student"
```

---

## Task 3: 2.9 — Distribuição Binomial

**Files:**
- Modify: `content/cap02/09-distribuicao-binomial.qmd`

**Interfaces:**
- Consumes: `scipy.stats`.

- [ ] **Step 1: Escrever a seção**

Pontos: contagem de sucessos em *n* tentativas independentes, cada uma com probabilidade *p*. O modelo do teste A/B — quantas conversões em *n* visitantes. Média = *np*, desvio = √(np(1−p)).

Chunk `setup` (oculto): numpy, matplotlib, `from scipy import stats`, `from formato import num`.

A forma (a pmf é discreta → gráfico de barras):
```python
#| label: fig-binomial
#| fig-cap: "Distribuição binomial: a probabilidade de cada número de sucessos em 20 tentativas, com p=0,1. O pico fica perto de np = 2."
k = np.arange(0, 11)
fig, ax = plt.subplots()
ax.bar(k, stats.binom.pmf(k, 20, 0.1), color="#b0c4d8", edgecolor="white")
ax.set_xlabel("Número de sucessos")
ax.set_ylabel("Probabilidade")
plt.tight_layout()
plt.show()
```

O cálculo:
```python
#| label: binomial
print(f"P(exatamente 2 sucessos em 5, p=0,1): {num(stats.binom.pmf(2, 5, 0.1), 4)}")
print(f"P(até 2 sucessos em 5, p=0,1):        {num(stats.binom.cdf(2, 5, 0.1), 4)}")
```
Saídas reais: `0,0729` e `0,9914`. Prosa: `pmf` é a probabilidade de um valor exato; `cdf` acumula do zero até ele. A distância entre elas — 2 exatos é raro (7%), mas 2 **ou menos** é quase certo (99%) — mostra que os poucos sucessos se concentram embaixo.

**Callout `.exemplo`:** teste A/B — se a taxa de conversão real é 10% e chegam 5 visitantes, a chance de ver exatamente 2 conversões é 7%. É por isso que amostras pequenas de teste A/B enganam: o número de conversões varia muito por acaso.

**2 exercícios:**
1. Uma moeda justa é lançada 10 vezes. Qual a probabilidade de exatamente 5 caras — e por que não é a maioria esmagadora, já que 5 é "o esperado"? *Resposta:* é `binom.pmf(5, 10, 0.5)` ≈ 0,246 — só ~25%. O valor esperado (5) é o mais provável, mas divide a massa com 4, 6, e os vizinhos. "O esperado" não é "o quase certo"; é só o centro da distribuição.
2. Por que a binomial exige tentativas **independentes** e com **a mesma** probabilidade? *Resposta:* se as tentativas se influenciam (a segunda depende da primeira) ou se p muda entre elas, a contagem de sucessos deixa de seguir a binomial. É o pressuposto que justifica multiplicar probabilidades — e o que quebra quando, por exemplo, os visitantes de um site não são independentes (um compartilhou o link com o outro).

- [ ] **Step 2: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap02/09-distribuicao-binomial.html
grep -oE '0,0729|0,9914' "$H" | sort -u | tr '\n' ' '; echo
echo "imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo) exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
```
Expected: `0,0729` e `0,9914`; imgs=1, exerc=2, stub=0.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/09-distribuicao-binomial.qmd
git commit -m "feat: secao 2.9 distribuicao binomial"
```

---

## Task 4: 2.10 Qui-Quadrado + 2.11 F

As duas seções conceituais, agrupadas porque ambas apresentam a forma e servem de **ponte para o Capítulo 3** (testes de significância). Como no livro, são curtas.

**Files:**
- Modify: `content/cap02/10-qui-quadrado.qmd`, `content/cap02/11-distribuicao-f.qmd`

**Interfaces:**
- Consumes: `scipy.stats`.

- [ ] **Step 1: Escrever a 2.10 — Qui-Quadrado**

Pontos: soma de normais-padrão ao quadrado; assimétrica à direita; a **média é igual aos graus de liberdade**. Aparece nos testes de aderência (o dado bate com o esperado?) e de independência (duas categorias são relacionadas?).

Chunk `setup` (oculto): numpy, matplotlib, `from scipy import stats`, `from formato import num`.

A forma (para vários gl):
```python
#| label: fig-chi2
#| fig-cap: "A distribuição qui-quadrado para diferentes graus de liberdade. Assimétrica à direita; o pico se afasta do zero conforme os graus de liberdade crescem."
x = np.linspace(0, 20, 200)
fig, ax = plt.subplots()
for gl, cor in [(2, "#27ae60"), (5, "#e67e22"), (10, "#c0392b")]:
    ax.plot(x, stats.chi2.pdf(x, gl), color=cor, linewidth=2, label=f"k = {gl}")
ax.set_xlabel("Valor")
ax.set_ylabel("Densidade")
ax.legend()
plt.tight_layout()
plt.show()
```

O valor crítico:
```python
#| label: chi2
print(f"Média de χ²(5): {num(stats.chi2.mean(5), 0)}  (= graus de liberdade)")
print(f"Valor crítico 5% de χ²(5): {num(stats.chi2.ppf(0.95, 5), 2)}")
```
Saídas reais: média `5` e valor crítico `11,07`. Prosa: um χ² calculado acima de 11,07 (com 5 gl) tem menos de 5% de chance sob a hipótese de que tudo é acaso — o gancho do teste. **Remissão explícita ao Capítulo 3**, seção 3.9 (teste qui-quadrado).

**2 exercícios:**
1. Por que a distribuição qui-quadrado só assume valores positivos? *Resposta:* é uma soma de **quadrados** — cada normal ao quadrado é ≥ 0, e a soma também. Não há como uma soma de quadrados dar negativo, então a distribuição vive inteira à direita do zero.
2. A média de χ²(k) é k. O que isso diz sobre o valor esperado de um teste qui-quadrado quando a hipótese nula é verdadeira? *Resposta:* se não há efeito real (só acaso), o χ² calculado tende a ficar perto dos graus de liberdade do teste. Um valor muito acima disso é o sinal de que o desvio entre observado e esperado é grande demais para ser acaso.

- [ ] **Step 2: Escrever a 2.11 — F**

Pontos: razão de duas variâncias. Aparece quando se comparam espalhamentos — o motor da **ANOVA** (as médias de vários grupos diferem mais do que a variação dentro dos grupos justificaria?).

Chunk `setup` (oculto): numpy, matplotlib, `from scipy import stats`, `from formato import num`.

A forma:
```python
#| label: fig-f
#| fig-cap: "A distribuição F para diferentes pares de graus de liberdade. Assimétrica à direita, sempre positiva — é uma razão de variâncias."
x = np.linspace(0, 5, 200)
fig, ax = plt.subplots()
for (g1, g2), cor in [((5, 10), "#27ae60"), ((10, 30), "#e67e22")]:
    ax.plot(x, stats.f.pdf(x, g1, g2), color=cor, linewidth=2, label=f"F({g1}, {g2})")
ax.set_xlabel("Valor")
ax.set_ylabel("Densidade")
ax.legend()
plt.tight_layout()
plt.show()
```

O valor crítico:
```python
#| label: f-critico
print(f"Valor crítico 5% de F(5, 10): {num(stats.f.ppf(0.95, 5, 10), 2)}")
```
Saída real: `3,33`. Prosa: uma razão de variâncias maior que 3,33 (com esses gl) é improvável se as variâncias fossem de fato iguais — o gancho da ANOVA. **Remissão ao Capítulo 3**, seção 3.8 (ANOVA).

**2 exercícios:**
1. A distribuição F é a razão de duas variâncias. Por que ela é sempre positiva? *Resposta:* variância é uma média de quadrados, sempre ≥ 0, e a razão de dois números não-negativos também é ≥ 0. Como qui-quadrado, a F vive à direita do zero.
2. Numa ANOVA, um valor F próximo de 1 sugere o quê? *Resposta:* que a variação **entre** os grupos é parecida com a variação **dentro** deles — ou seja, os grupos não diferem mais do que o acaso já produziria. F perto de 1 = sem evidência de diferença entre as médias; F grande = as médias diferem mais do que a variação interna explica.

- [ ] **Step 3: Renderizar e conferir**

Run:
```bash
make render
grep -oE 'Média de χ²\(5\): 5|Valor crítico 5% de χ²\(5\): 11,07' _book/content/cap02/10-qui-quadrado.html
grep -oE 'Valor crítico 5% de F\(5, 10\): 3,33' _book/content/cap02/11-distribuicao-f.html
for f in 10-qui-quadrado 11-distribuicao-f; do
  H=_book/content/cap02/$f.html
  echo "$f: imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo) exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
done
```
Expected: os números `5`, `11,07`, `3,33`; cada seção imgs=1, exerc=2, stub=0.

- [ ] **Step 4: Commit**

```bash
git add content/cap02/10-qui-quadrado.qmd content/cap02/11-distribuicao-f.qmd
git commit -m "feat: secoes 2.10 qui-quadrado e 2.11 distribuicao f"
```

---

## Task 5: 2.12 — Poisson e Relacionadas

**Files:**
- Modify: `content/cap02/12-poisson.qmd`

**Interfaces:**
- Consumes: `scipy.stats`.

- [ ] **Step 1: Escrever a seção**

Pontos: Poisson = número de eventos raros num intervalo fixo, com taxa média λ (chegadas a um servidor, ligações num call center, defeitos por lote). A **exponencial** é a irmã da Poisson: o tempo de espera *entre* eventos. (Menção à Weibull como a generalização com taxa variável — uma frase, sem código.)

Chunk `setup` (oculto): numpy, matplotlib, `from scipy import stats`, `from formato import num`.

A forma da Poisson (discreta → barras):
```python
#| label: fig-poisson
#| fig-cap: "Distribuição de Poisson com λ=2: a probabilidade de observar cada número de eventos num intervalo. O pico fica em torno de λ."
k = np.arange(0, 11)
fig, ax = plt.subplots()
ax.bar(k, stats.poisson.pmf(k, 2), color="#b0c4d8", edgecolor="white")
ax.set_xlabel("Número de eventos no intervalo")
ax.set_ylabel("Probabilidade")
plt.tight_layout()
plt.show()
```

O cálculo:
```python
#| label: poisson
print(f"Poisson(λ=2): P(nenhum evento) = {num(stats.poisson.pmf(0, 2), 3)}")
print(f"Poisson(λ=2): P(5 ou mais)     = {num(stats.poisson.sf(4, 2), 3)}")
```
Saídas reais: `0,135` e `0,053`. Prosa: com taxa média 2 por intervalo, ver zero evento ainda tem 14% de chance, e ver 5 ou mais é raro (5%). A Poisson é o modelo de "quantas vezes algo raro acontece por unidade de tempo".

A exponencial, uma frase de código:
```python
#| label: exponencial
print(f"Se ocorrem 2 eventos por hora, o tempo médio entre eventos é {num(1 / 2 * 60, 0)} minutos.")
```
Saída real: `30` minutos. Prosa: Poisson conta **quantos** eventos num intervalo; a exponencial mede **quanto tempo** até o próximo. As duas descrevem o mesmo processo por ângulos diferentes. A **Weibull** generaliza a exponencial para quando a taxa não é constante — a chance de falha de uma peça que envelhece cresce com o tempo (uma menção, sem código).

**2 exercícios:**
1. Um call center recebe em média 3 ligações por minuto. A Poisson é um bom modelo para o número de ligações no próximo minuto? Que pressuposto ela exige? *Resposta:* sim, se as ligações são independentes e a taxa média é estável no período. A Poisson quebra se as chegadas se agrupam (uma promoção dispara uma onda) ou se a taxa varia muito ao longo do dia — aí o intervalo precisa ser curto o bastante para a taxa ser aproximadamente constante.
2. Se os eventos seguem uma Poisson, o tempo de espera entre eles segue uma exponencial. Por que o tempo de espera não é simplesmente constante (1/λ)? *Resposta:* porque os eventos chegam ao acaso, não em intervalos regulares. 1/λ é o tempo **médio** de espera, mas os intervalos individuais variam muito — alguns curtíssimos (dois eventos quase juntos), outros longos. A exponencial descreve exatamente essa variação, com muitos intervalos curtos e uma cauda de intervalos longos.

- [ ] **Step 2: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap02/12-poisson.html
grep -oE 'P\(nenhum evento\) = 0,135|P\(5 ou mais\)     = 0,053|é 30 minutos' "$H" | sort -u
echo "imgs=$(grep -oE '<img[^>]*>' "$H" | grep -civ logo) exerc=$(grep -c 'callout-tip' "$H") stub=$(grep -c 'Em construção' "$H")"
```
Expected: `0,135`, `0,053`, `30 minutos`; imgs=1, exerc=2, stub=0.

- [ ] **Step 3: Commit**

```bash
git add content/cap02/12-poisson.qmd
git commit -m "feat: secao 2.12 poisson e relacionadas"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean && make render
find _book/content -name '*.html' | wc -l
```
Expected: `42`, sem erro.

- [ ] **O Capítulo 2 está COMPLETO — nenhum stub**

```bash
grep -rl 'Em construção' content/cap02/ && echo "AINDA HÁ STUB" || echo "Capitulo 2 completo (12/12)"
```
Expected: `Capitulo 2 completo (12/12)`.

- [ ] **Cada seção 2.6–2.12 tem 2 exercícios e um gráfico**

```bash
for f in content/cap02/0[6789]-*.qmd content/cap02/1[012]-*.qmd; do
  n=$(grep -c 'callout-tip collapse' "$f")
  [ "$n" -eq 2 ] || echo "$(basename $f): $n exercícios (esperado 2)"
done
echo ok
```
Expected: só `ok`.

- [ ] **Nenhum chunk com RNG sem semente**

```bash
grep -rnE 'rvs\(|\.sample\(|np\.random' content/cap02/0[6789]-*.qmd content/cap02/1[012]-*.qmd \
  | grep -vE 'random_state=42|`sample|# ' \
  && echo "ERRO: RNG sem semente" || echo "sementes ok"
```
Expected: `sementes ok`.

- [ ] **Os números-chave do catálogo aparecem**

```bash
grep -o '1,05' _book/content/cap02/06-distribuicao-normal.html | head -1
grep -o '6,8'  _book/content/cap02/07-caudas-longas.html | head -1
grep -o '0,0729' _book/content/cap02/09-distribuicao-binomial.html | head -1
grep -o '11,07' _book/content/cap02/10-qui-quadrado.html | head -1
grep -o '3,33' _book/content/cap02/11-distribuicao-f.html | head -1
grep -o '0,135' _book/content/cap02/12-poisson.html | head -1
```
Expected: cada um imprime o número.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
