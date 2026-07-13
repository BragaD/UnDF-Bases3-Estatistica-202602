# Conteúdo do Capítulo 1 — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Escrever as 7 seções restantes do Capítulo 1 (Análise Exploratória de Dados) e adequar a seção 1.3 ao mesmo padrão.

**Architecture:** Cada seção é um `.qmd` autocontido já registrado no `_quarto.yml`, seguindo o esqueleto de `content/cap01/03-estimativas-localizacao.qmd`: chunk `setup` oculto, prosa e código intercalados, callouts `.conceito`/`.exemplo`, tabela-resumo e `## Exercícios` com respostas em callout recolhível. Os chunks Python rodam sobre os CSVs versionados em `dados/`, executados pelo container no `make render`.

**Tech Stack:** Quarto (engine jupyter) · pandas · numpy · scipy · statsmodels · matplotlib · seaborn · wquantiles

**Spec:** `docs/superpowers/specs/2026-07-13-conteudo-cap01-design.md`

## Sobre este plano

Diferente de um plano de código, a **prosa didática é o trabalho** — não faz sentido transcrevê-la aqui para um implementador copiar. Este plano fixa o que não pode variar:

- **O código Python exato de cada chunk.** Rodei todos e conferi as saídas contra o livro-texto; os valores esperados abaixo são reais, não estimados.
- **Os números esperados.** Se o render produzir outros, algo está errado — **não ajuste o esperado para caber no obtido**.
- **Os pontos didáticos obrigatórios** de cada seção.
- **Os exercícios** (enunciado e o núcleo da resposta).

A redação da prosa fica com o implementador, tendo `content/cap01/03-estimativas-localizacao.qmd` como modelo de voz e estrutura. **Leia essa seção antes de escrever qualquer outra.**

## Global Constraints

- **Português brasileiro.** Variáveis dos chunks em português (`estado`, `media_aparada`). Nomes de coluna dos CSVs preservados do original: `Population`, `Murder.Rate` (com PONTO), `SqFtTotLiving`, `TaxAssessedValue`, `ZipCode`, `pct_carrier_delay`, `airline`, `grade`, `status`.
- **Fidelidade ao livro.** SEM analogias de engenharia de software. Os exemplos e o enquadramento são os do livro-texto. (A seção 1.3 hoje viola isso; a Task 1 corrige.)
- **Caminhos de dados relativos à raiz:** `pd.read_csv("dados/state.csv")`. NUNCA `../../dados/`. Garantido por `project: execute-dir: project` no `_quarto.yml`.
- **Semente obrigatória em todo chunk com RNG:** `random_state=42`. Aplica-se à Task 8 (`.sample()`).
- **Citação do livro:** `@bruce2020`. Cada seção abre com `::: {.callout-note}` dizendo "Esta seção corresponde à seção N.M de @bruce2020."
- **Classes CSS disponíveis:** `.conceito` (azul), `.exemplo` (verde).
- **Respostas dos exercícios:** `::: {.callout-tip collapse="true"}` com título `## Resposta`. **Nunca usar `spoiler.html`** — ele é ofuscação que se apresenta como senha e o conteúdo vai em texto puro no HTML público.
- **Todas as 8 seções já estão registradas no `_quarto.yml`.** Nenhuma task precisa mexer nele.
- **Render sempre via container:** `make render`. Não há Quarto/Python confiáveis no host.
- **Peso alvo:** ~130 linhas por seção, como a 1.3.

---

## Estrutura de Arquivos

| Arquivo | Task | Datasets |
|---|---|---|
| `content/cap01/03-estimativas-localizacao.qmd` | 1 (modificar) | `state.csv` |
| `content/cap01/01-dados-estruturados.qmd` | 2 | `state.csv`, `dfw_airline.csv` |
| `content/cap01/02-dados-retangulares.qmd` | 3 | `state.csv` |
| `content/cap01/04-estimativas-variabilidade.qmd` | 4 | `state.csv` |
| `content/cap01/05-distribuicao-dados.qmd` | 5 | `state.csv` |
| `content/cap01/06-dados-binarios-categoricos.qmd` | 6 | `dfw_airline.csv` |
| `content/cap01/07-correlacao.qmd` | 7 | `sp500_data.csv.gz`, `sp500_sectors.csv` |
| `content/cap01/08-duas-ou-mais-variaveis.qmd` | 8 | `kc_tax.csv.gz`, `lc_loans.csv`, `airline_stats.csv` |

A ordem das tasks (1.3 → 1.1 → 1.2 → 1.4 → …) é deliberada: a Task 1 estabelece o padrão de exercícios que todas as outras copiam.

---

## Verificação padrão de cada task

Todas as tasks 2–8 terminam com os mesmos quatro checks. Eles estão escritos por extenso em cada task, mas a lógica é esta:

1. `make render` conclui sem erro.
2. A página existe e contém os números esperados (grep no HTML).
3. A página contém `## Exercícios` e ao menos um callout recolhível.
4. Nenhum chunk com RNG sem semente.

---

## Task 1: Retrofit da seção 1.3

Estabelece o padrão de exercícios e alinha a 1.3 às decisões do spec.

**Files:**
- Modify: `content/cap01/03-estimativas-localizacao.qmd`

**Interfaces:**
- Produces: o formato de `## Exercícios` que as Tasks 2–8 replicam.

- [ ] **Step 1: Remover a analogia de engenharia de software**

No callout final (`.conceito`, "Regra prática"), o texto atual termina com:

> "...quando os dados têm cauda longa ou outliers plausíveis — renda, população, **tempo de resposta de um servidor** — a mediana ou a média aparada descrevem melhor o caso típico."

Remova `tempo de resposta de um servidor`. O spec decidiu fidelidade ao livro, sem pontes para computação. Substitua por um terceiro exemplo do domínio do livro (ex.: valor de imóveis) ou deixe apenas dois.

- [ ] **Step 2: Acrescentar a seção de exercícios ao final do arquivo**

Este é o formato canônico. As Tasks 2–8 o replicam.

````markdown
## Exercícios

**1.** A média aparada de 10% descartou os 5 estados mais populosos e os 5 menos populosos. Recalcule com aparo de 25%. O que acontece com a média aparada à medida que o aparo se aproxima de 50%?

::: {.callout-tip collapse="true"}
## Resposta

```python
trim_mean(estado["Population"], 0.25)
```

Com aparo de 50%, todas as observações são descartadas exceto a(s) central(is) — a média aparada **converge para a mediana**. A média aparada é, portanto, uma família contínua entre a média (aparo 0) e a mediana (aparo 0,5).
:::

**2.** A média ponderada da taxa de homicídios (4,45) é maior que a média simples (4,07). O que isso diz sobre a relação entre população e taxa de homicídios nos estados?

::: {.callout-tip collapse="true"}
## Resposta

Ponderar pela população **aumenta** a estimativa, então os estados mais populosos tendem a ter taxas de homicídio mais altas que os menos populosos. Se não houvesse relação alguma entre tamanho e taxa, as duas médias seriam próximas.
:::

**3.** Um relatório afirma que "a renda média das famílias do país subiu 8% no último ano, mas a renda mediana ficou estável". Como isso é possível?

::: {.callout-tip collapse="true"}
## Resposta

A média é sensível a extremos e a mediana não. Um ganho concentrado no topo da distribuição — os mais ricos ficando mais ricos — eleva a soma total (e portanto a média) sem mover o valor central. É exatamente o padrão de uma distribuição assimétrica à direita cuja cauda se alonga.
:::
````

- [ ] **Step 3: Renderizar**

Run: `make render`
Expected: conclui sem erro.

- [ ] **Step 4: Verificar que os números NÃO mudaram e que os exercícios entraram**

Run:
```bash
H=_book/content/cap01/03-estimativas-localizacao.html
grep -oE 'Média: 6,162,876\.3|Média aparada \(10%\): 4,783,697\.1|Mediana: 4,436,369\.5' "$H" | sort -u
grep -c 'callout-tip' "$H"
grep -c 'tempo de resposta' "$H"
```
Expected:
```
Média: 6,162,876.3
Média aparada (10%): 4,783,697.1
Mediana: 4,436,369.5
3          ← três respostas recolhíveis
0          ← a analogia foi removida
```

- [ ] **Step 5: Commit**

```bash
git add content/cap01/03-estimativas-localizacao.qmd
git commit -m "docs: exercicios na secao 1.3 e remocao de analogia fora do escopo"
```

---

## Task 2: Seção 1.1 — Elementos de Dados Estruturados

**Files:**
- Create: `content/cap01/01-dados-estruturados.qmd` (hoje é stub — substitua o conteúdo inteiro)

**Interfaces:**
- Consumes: `dados/state.csv`, `dados/dfw_airline.csv`; formato de exercícios da Task 1.

**Pontos didáticos obrigatórios:**

1. Dados brutos do mundo (sensores, cliques, texto) não são úteis até serem **estruturados**.
2. A taxonomia, com os dois ramos:
   - **Numérico**: *contínuo* (pode assumir qualquer valor num intervalo — velocidade do vento, duração) e *discreto* (apenas contagens inteiras — número de ocorrências).
   - **Categórico**: *nominal* (sem ordem — estados, tipos de tela), *ordinal* (com ordem — nota de 1 a 5), *binário* (caso especial com dois valores — 0/1, sim/não).
3. **Por que a distinção importa**, que é o ponto da seção: o tipo determina (a) o gráfico cabível, (b) a análise estatística cabível, e (c) como o software armazena, valida e otimiza o dado.

**Nota de escopo:** o livro trata esta seção de forma quase inteiramente conceitual. O spec decidiu dar-lhe o mesmo peso das demais, então ela ganha código que **demonstra** a taxonomia em vez de só descrevê-la. Isso é uma adição deliberada, fiel ao espírito do livro (que enfatiza a importância dos tipos para o software), não uma tradução literal.

- [ ] **Step 1: Escrever o arquivo**

Use exatamente estes chunks. O chunk `setup` vai com `include: false`.

```python
#| label: setup
#| include: false
import pandas as pd

pd.set_option("display.max_columns", None)
```

Chunk que mostra os tipos que o pandas infere:

```python
#| label: tipos
estado = pd.read_csv("dados/state.csv")
estado.dtypes
```

Saída real: `State` → `object` (string), `Population` → `int64`, `Murder.Rate` → `float64`, `Abbreviation` → `object`.

O ponto a extrair: o pandas inferiu `int64` para população (discreto, é contagem de pessoas) e `float64` para a taxa (contínuo). Mas ele NÃO sabe que `State` é categórico nominal — para ele é só texto.

Chunk que converte para categórico:

```python
#| label: categorico
estado["Abbreviation"] = estado["Abbreviation"].astype("category")
print(estado["Abbreviation"].dtype)
print("categorias:", len(estado["Abbreviation"].cat.categories))
```

Chunk do categórico **ordenado** — o coração da seção, porque mostra a consequência prática do tipo:

```python
#| label: ordinal
from pandas.api.types import CategoricalDtype

tamanho = CategoricalDtype(categories=["pequeno", "medio", "grande"], ordered=True)
s = pd.Series(["grande", "pequeno", "medio"], dtype=tamanho)

print(s.sort_values().tolist())
print("grande > pequeno ?", s[0] > s[1])
```

Saída real: `['pequeno', 'medio', 'grande']` e `True`.

Explique: com `ordered=True`, a comparação `>` funciona e a ordenação respeita a semântica, não o alfabeto. Num categórico nominal, `>` levantaria `TypeError` — e isso é uma **feature**, não uma limitação: o tipo impede uma operação que não faz sentido.

**Callout `.conceito` obrigatório:** declarar o tipo não é burocracia. É o que permite ao software rejeitar uma operação sem sentido (ordenar estados por "grandeza" alfabética), escolher o gráfico certo automaticamente e economizar memória (um `category` com 50 valores distintos guarda inteiros, não 50 strings repetidas).

**Tabela-resumo obrigatória:** os 5 tipos (contínuo, discreto, nominal, ordinal, binário), com um exemplo de cada e o gráfico típico.

- [ ] **Step 2: Escrever os exercícios**

Três exercícios, no formato da Task 1:

1. **Classifique** cada variável do `state.csv` (`State`, `Population`, `Murder.Rate`, `Abbreviation`) na taxonomia. *Resposta:* `State` e `Abbreviation` são categóricos nominais; `Population` é numérico discreto (contagem de pessoas); `Murder.Rate` é numérico contínuo.
2. Uma pesquisa registra satisfação como 1, 2, 3, 4, 5. O pandas lê como `int64`. **Por que tratar como numérico pode enganar?** *Resposta:* porque a distância entre 1 e 2 não é necessariamente igual à distância entre 4 e 5 — é ordinal, não intervalar. Calcular a média de notas de satisfação supõe que os intervalos são iguais, o que raramente é verdade. A mediana ou a moda são mais defensáveis.
3. O CEP (`ZipCode`) do `kc_tax` é lido como número. **É numérico?** *Resposta:* não. É categórico nominal codificado com dígitos. A média de dois CEPs não significa nada, e a proximidade numérica não implica proximidade geográfica. É um dos erros de tipo mais comuns na prática.

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render
H=_book/content/cap01/01-dados-estruturados.html
grep -c "pequeno" "$H"        # a saída do categórico ordenado
grep -c 'callout-tip' "$H"    # exercícios
grep -c "Em construção" "$H"  # o stub sumiu?
```
Expected: `pequeno` ≥ 1; `callout-tip` = 3; `Em construção` = 0.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/01-dados-estruturados.qmd
git commit -m "feat: secao 1.1 elementos de dados estruturados"
```

---

## Task 3: Seção 1.2 — Dados Retangulares

**Files:**
- Create: `content/cap01/02-dados-retangulares.qmd` (substitui o stub)

**Interfaces:**
- Consumes: `dados/state.csv`.

**Pontos didáticos obrigatórios:**

1. O **DataFrame** (matriz de dados, tabela) é a estrutura sobre a qual quase toda a estatística prática opera: linhas são registros, colunas são variáveis.
2. **Vocabulário e seus sinônimos** — este é um ponto real do livro, porque as disciplinas usam palavras diferentes para a mesma coisa e isso confunde:
   - Coluna preditora: *feature*, variável, atributo, preditor, entrada (input)
   - Coluna a prever: *outcome*, resposta, variável dependente, alvo (target), saída
   - Linha: registro, caso, observação, exemplo, instância
3. O **índice** do DataFrame, e que ele não é uma coluna de dados.
4. **Dados não retangulares** existem e não cabem nessa forma: séries temporais (a ordem carrega informação), dados espaciais (objetos e coordenadas) e grafos (relações entre nós — redes sociais, rotas).

- [ ] **Step 1: Escrever o arquivo**

```python
#| label: setup
#| include: false
import pandas as pd
```

```python
#| label: estrutura
estado = pd.read_csv("dados/state.csv")
print("linhas x colunas:", estado.shape)
estado.head()
```

Saída real: `(50, 4)`.

```python
#| label: info
estado.info()
```

```python
#| label: indice
print("índice padrão:", estado.index[:5].tolist())

# Um índice significativo torna a busca por rótulo natural
por_estado = estado.set_index("Abbreviation")
por_estado.loc["CA"]
```

Saída real de `por_estado.loc["CA"]`: State=California, Population=37253956, Murder.Rate=4.4.

**Callout `.conceito`:** o índice não é uma coluna de dados — é o rótulo das linhas. Confundir os dois é fonte comum de bug: `set_index` **remove** a coluna do corpo do DataFrame.

**Callout `.exemplo`:** montar a tabela de sinônimos (feature/outcome/registro) e dizer que, ao ler um artigo ou uma documentação, "preditor", "atributo" e "feature" são a mesma coisa.

**Seção sobre dados não retangulares:** prosa, sem código. Explicar os três casos (séries temporais, espaciais, grafos) e por que forçá-los numa tabela perde informação.

**Tabela-resumo:** o vocabulário, com as colunas "Termo usado neste livro | Sinônimos que você vai encontrar".

- [ ] **Step 2: Escrever os exercícios**

1. `estado.shape` retorna `(50, 4)`. **Qual é o significado de cada número, no vocabulário da seção?** *Resposta:* 50 registros (observações — os estados) e 4 features (variáveis).
2. Você quer prever a taxa de homicídios a partir da população. **Qual coluna é o *outcome* e quais são as *features*?** *Resposta:* `Murder.Rate` é o outcome; `Population` é a feature. `State` e `Abbreviation` são identificadores, não features úteis (usá-los como preditor seria memorizar cada linha).
3. Um log de servidor tem timestamp, IP e URL, uma linha por requisição. **É retangular? E se a pergunta for "qual a sequência típica de páginas antes de uma compra?"** *Resposta:* a tabela é retangular, mas a pergunta é sobre **sequência** — a ordem entre as linhas carrega a informação, e isso a forma retangular não representa. É um caso em que a estrutura tabular armazena o dado mas não o modela.

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render
H=_book/content/cap01/02-dados-retangulares.html
grep -c "California" "$H"     # a saída do .loc["CA"]
grep -c 'callout-tip' "$H"
grep -c "Em construção" "$H"
```
Expected: `California` ≥ 1; `callout-tip` = 3; `Em construção` = 0.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/02-dados-retangulares.qmd
git commit -m "feat: secao 1.2 dados retangulares"
```

---

## Task 4: Seção 1.4 — Estimativas de Variabilidade

**Files:**
- Create: `content/cap01/04-estimativas-variabilidade.qmd` (substitui o stub)

**Interfaces:**
- Consumes: `dados/state.csv`.

**Pontos didáticos obrigatórios:**

1. Localização (seção 1.3) é metade da história. A outra metade é **dispersão**: quão espalhados os dados estão em torno do valor típico.
2. **Desvio e variância.** Por que não se usa a média dos desvios (ela é sempre zero, por construção — os desvios positivos cancelam os negativos). As duas saídas: elevar ao quadrado (variância, desvio-padrão) ou tomar o valor absoluto (desvio absoluto médio).
3. O **desvio-padrão** é o mais usado porque tem a mesma unidade dos dados e porque a matemática dos quadrados é conveniente — não porque seja o mais robusto. Ele é ainda **mais** sensível a extremos que a média, porque o quadrado amplifica os desvios grandes.
4. **Estimativas robustas:** IQR (amplitude interquartil) e MAD (desvio absoluto mediano).
5. O fator **0,6745** do MAD: ele calibra o MAD para ser comparável ao desvio-padrão sob uma distribuição normal. Sem ele, os dois números não são comparáveis.

- [ ] **Step 1: Escrever o arquivo**

```python
#| label: setup
#| include: false
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels import robust

plt.rcParams["figure.figsize"] = (7, 4)
estado = pd.read_csv("dados/state.csv")
```

Fórmulas em LaTeX (obrigatórias):

$$s = \sqrt{\frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n-1}} \qquad \text{IQR} = Q_{75} - Q_{25}$$

$$\text{MAD} = \frac{\text{mediana}\big(|x_i - \text{mediana}(x)|\big)}{0{,}6745}$$

```python
#| label: desvio-padrao
desvio = estado["Population"].std()
print(f"Desvio-padrão: {desvio:,.1f}")
```
Saída real: `6,848,235.3`

```python
#| label: iqr
iqr = estado["Population"].quantile(0.75) - estado["Population"].quantile(0.25)
print(f"IQR: {iqr:,.1f}")
```
Saída real: `4,847,308.0`

```python
#| label: mad
mad = robust.scale.mad(estado["Population"])
print(f"MAD: {mad:,.1f}")

# O mesmo cálculo, explicitamente — para mostrar de onde vem o 0,6745
mad_manual = abs(estado["Population"] - estado["Population"].median()).median() / 0.6744897501960817
print(f"MAD (manual): {mad_manual:,.1f}")
```
Saída real: ambos `3,849,876.1` — idênticos. Faça o ponto de que a função da `statsmodels` está fazendo exatamente essa conta.

```python
#| label: fig-variabilidade
#| fig-cap: "As três medidas de dispersão sobre a distribuição de população dos estados."
mediana = estado["Population"].median()
fig, ax = plt.subplots()

ax.hist(estado["Population"] / 1e6, bins=20, color="#b0c4d8", edgecolor="white")
ax.axvline(mediana / 1e6, color="#2c3e50", linewidth=2, label=f"Mediana: {mediana/1e6:.1f}M")

for medida, valor, cor, estilo in [
    ("Desvio-padrão", desvio, "#c0392b", "-"),
    ("IQR", iqr, "#e67e22", "--"),
    ("MAD", mad, "#27ae60", ":"),
]:
    ax.axvline((mediana + valor) / 1e6, color=cor, linestyle=estilo, linewidth=2,
               label=f"{medida}: {valor/1e6:.1f}M")

ax.set_xlabel("População (milhões)")
ax.set_ylabel("Número de estados")
ax.legend()
plt.tight_layout()
plt.show()
```

**Callout `.conceito` obrigatório:** o desvio-padrão (6,8M) é quase o dobro do MAD (3,8M). Essa distância entre uma medida sensível e uma robusta é o mesmo sinal que a diferença entre média e mediana deu na seção 1.3: a distribuição tem cauda longa à direita.

**Tabela-resumo:** as três medidas, seus valores e se são robustas.

| Medida | Valor | Robusta? |
|---|---|---|
| Desvio-padrão | 6.848.235 | Não |
| IQR | 4.847.308 | Sim |
| MAD | 3.849.876 | Sim |

- [ ] **Step 2: Escrever os exercícios**

1. **Por que não se usa simplesmente a média dos desvios em relação à média?** *Resposta:* porque ela é sempre exatamente zero — é uma propriedade algébrica da média, não um fato sobre os dados. Os desvios positivos cancelam os negativos por construção. Daí a necessidade de eliminar o sinal, elevando ao quadrado ou tomando o módulo.
2. O desvio-padrão da população é 6,85M e o MAD é 3,85M — quase o dobro. **O que essa razão diz?** *Resposta:* que há observações extremas puxando o desvio-padrão. Sob uma distribuição normal, MAD e desvio-padrão seriam próximos (é para isso que serve o fator 0,6745). Uma razão desvio-padrão/MAD muito maior que 1 é um diagnóstico prático de cauda longa ou outliers.
3. **Se você multiplicar todas as populações por 1000, o que acontece com o desvio-padrão? E com o IQR?** *Resposta:* ambos são multiplicados por 1000. As medidas de dispersão têm a mesma unidade dos dados e escalam linearmente. (A variância, ao contrário, seria multiplicada por 1.000.000 — ela está em unidade ao quadrado, o que é justamente o inconveniente que motiva o desvio-padrão.)

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render
H=_book/content/cap01/04-estimativas-variabilidade.html
grep -oE 'Desvio-padrão: 6,848,235\.3|IQR: 4,847,308\.0|MAD: 3,849,876\.1' "$H" | sort -u
grep -c '<img' "$H"
grep -c 'callout-tip' "$H"
```
Expected: os três números batem exatamente; `<img>` ≥ 1; `callout-tip` = 3.

**Se algum número divergir, PARE.** Não ajuste o esperado.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/04-estimativas-variabilidade.qmd
git commit -m "feat: secao 1.4 estimativas de variabilidade"
```

---

## Task 5: Seção 1.5 — Explorando a Distribuição dos Dados

**Files:**
- Create: `content/cap01/05-distribuicao-dados.qmd` (substitui o stub)

**Interfaces:**
- Consumes: `dados/state.csv`.

**Pontos didáticos obrigatórios:**

1. Localização e dispersão resumem a distribuição em **dois números**. Esta seção olha a distribuição **inteira**.
2. **Percentis e quantis:** o percentil P é o valor abaixo do qual estão P% das observações. A mediana é o percentil 50.
3. **Boxplot:** a caixa vai do Q1 ao Q3 (o IQR da seção 1.4); a linha é a mediana; os bigodes se estendem até 1,5×IQR; os pontos além são desenhados individualmente. O boxplot é uma leitura visual direta dos percentis.
4. **Tabela de frequência e histograma:** dividir o intervalo em faixas iguais e contar. O histograma é a tabela de frequência desenhada; barras encostadas, porque o eixo é contínuo.
5. **Densidade:** uma versão suavizada do histograma. A área sob a curva é 1 — por isso o histograma precisa de `density=True` para ser comparável.

- [ ] **Step 1: Escrever o arquivo**

```python
#| label: setup
#| include: false
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (7, 4)
estado = pd.read_csv("dados/state.csv")
```

```python
#| label: percentis
percentis = [0.05, 0.25, 0.5, 0.75, 0.95]
tabela = pd.DataFrame(estado["Murder.Rate"].quantile(percentis))
tabela.index = [f"{p:.0%}" for p in percentis]
tabela.transpose()
```
Saídas reais: 5% → 1,600 · 25% → 2,425 · 50% → 4,000 · 75% → 5,550 · 95% → 6,510

```python
#| label: fig-boxplot
#| fig-cap: "Boxplot da população dos estados. Os pontos acima do bigode são os estados atipicamente populosos."
fig, ax = plt.subplots(figsize=(4, 5))
(estado["Population"] / 1e6).plot.box(ax=ax)
ax.set_ylabel("População (milhões)")
plt.tight_layout()
plt.show()
```

```python
#| label: freq
faixas = pd.cut(estado["Population"], 10)
faixas.value_counts().sort_index()
```

Ponto a fazer: as faixas são de **largura igual**, não de **contagem igual**. A primeira faixa concentra a maioria dos estados; as últimas têm um estado cada — a assinatura visual da cauda longa.

```python
#| label: fig-histograma
#| fig-cap: "Histograma da população. As barras se encostam porque o eixo é contínuo."
fig, ax = plt.subplots()
(estado["Population"] / 1e6).plot.hist(ax=ax, bins=10, edgecolor="white")
ax.set_xlabel("População (milhões)")
ax.set_ylabel("Número de estados")
plt.tight_layout()
plt.show()
```

```python
#| label: fig-densidade
#| fig-cap: "Histograma da taxa de homicídios com a curva de densidade sobreposta."
fig, ax = plt.subplots()
estado["Murder.Rate"].plot.hist(ax=ax, density=True, xlim=[0, 12],
                                bins=range(1, 12), edgecolor="white")
estado["Murder.Rate"].plot.density(ax=ax, linewidth=2)
ax.set_xlabel("Taxa de homicídios (por 100.000)")
plt.tight_layout()
plt.show()
```

**Callout `.conceito` obrigatório:** o `density=True` no histograma é o que torna as duas curvas comparáveis. Sem ele, o eixo Y do histograma é **contagem** e o da densidade é **densidade de probabilidade** — escalas diferentes, e a curva apareceria colada no eixo.

**Callout `.exemplo`:** ler o boxplot em voz alta — "metade dos estados tem entre 1,7 e 6,6 milhões de habitantes (a caixa); a mediana é 4,4 milhões; e os pontos isolados no topo são Califórnia, Texas, Nova York e Flórida."

- [ ] **Step 2: Escrever os exercícios**

1. **A mediana da taxa de homicídios é 4,0 e o percentil 95 é 6,51. Interprete o segundo número em uma frase.** *Resposta:* 95% dos estados têm taxa de homicídios igual ou inferior a 6,51 por 100.000 habitantes; apenas 5% (2 ou 3 estados) estão acima disso.
2. **No boxplot, por que os pontos acima do bigode são desenhados individualmente em vez de o bigode simplesmente se estender até eles?** *Resposta:* por convenção, o bigode vai até 1,5×IQR além do quartil. Pontos além disso são candidatos a outlier e são marcados individualmente justamente para chamar atenção — o objetivo é que você os **veja**, e não que eles sejam absorvidos pela escala.
3. **A tabela de frequência com `pd.cut` em 10 faixas colocou quase todos os estados nas primeiras faixas. Isso é um defeito do método?** *Resposta:* não — é um retrato fiel dos dados. `pd.cut` cria faixas de **largura** igual, e a distribuição é assimétrica. Se quiser faixas de **contagem** igual, use `pd.qcut` (que corta por quantis). São perguntas diferentes: uma mostra a forma da distribuição, a outra a divide em grupos do mesmo tamanho.

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render
H=_book/content/cap01/05-distribuicao-dados.html
grep -c '<img' "$H"           # boxplot + histograma + densidade
grep -c 'callout-tip' "$H"
grep -c "Em construção" "$H"
```
Expected: `<img>` ≥ 3; `callout-tip` = 3; `Em construção` = 0.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/05-distribuicao-dados.qmd
git commit -m "feat: secao 1.5 explorando a distribuicao dos dados"
```

---

## Task 6: Seção 1.6 — Explorando Dados Binários e Categóricos

**Files:**
- Create: `content/cap01/06-dados-binarios-categoricos.qmd` (substitui o stub)

**Interfaces:**
- Consumes: `dados/dfw_airline.csv`.

**Formato do dataset:** uma única linha, cinco colunas — `Carrier`, `ATC`, `Weather`, `Security`, `Inbound` — com a contagem de atrasos por causa no aeroporto de Dallas/Fort Worth.

**Pontos didáticos obrigatórios:**

1. Para dados categóricos, o resumo é simplesmente a **proporção** de cada categoria. Não há média a calcular.
2. **Gráfico de barras** — e a distinção que o livro faz questão de marcar: um gráfico de barras **não é um histograma**. No histograma o eixo X é numérico e contínuo (barras encostadas); no gráfico de barras o eixo X é categórico e sem ordem intrínseca (barras separadas).
3. **Moda:** a categoria mais frequente. É a única "medida de localização" que faz sentido para dado nominal.
4. **Valor esperado:** quando as categorias têm um valor numérico associado, o valor esperado é a média ponderada pelas probabilidades — $\text{VE} = \sum p_i \cdot v_i$. É a base de toda a estatística que vem depois.

- [ ] **Step 1: Escrever o arquivo**

```python
#| label: setup
#| include: false
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (7, 4)
```

```python
#| label: proporcoes
dfw = pd.read_csv("dados/dfw_airline.csv")
proporcoes = 100 * dfw / dfw.values.sum()
proporcoes.round(2)
```
Saídas reais (%): Carrier 23,02 · ATC 30,40 · Weather 4,03 · Security 0,12 · Inbound 42,43

```python
#| label: fig-barras
#| fig-cap: "Causas de atraso no aeroporto de Dallas/Fort Worth. As barras são separadas: o eixo é categórico, não contínuo."
fig, ax = plt.subplots()
dfw.transpose().plot.bar(ax=ax, legend=False, color="#4a90a4", edgecolor="white")
ax.set_xlabel("Causa do atraso")
ax.set_ylabel("Número de atrasos")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
```

```python
#| label: moda
moda = proporcoes.transpose().iloc[:, 0].idxmax()
print(f"Moda (causa mais frequente): {moda}")
```
Saída real: `Inbound`

Chunk do valor esperado — invente um exemplo no espírito do livro (o livro usa um webinar com dois níveis de serviço). Exemplo concreto e verificável:

```python
#| label: valor-esperado
# Uma companhia estima o custo médio de compensação por passageiro,
# conforme a causa do atraso.
custo = {"Carrier": 180, "ATC": 40, "Weather": 0, "Security": 25, "Inbound": 120}

p = (dfw / dfw.values.sum()).transpose().iloc[:, 0]   # probabilidade de cada causa
ve = sum(p[causa] * valor for causa, valor in custo.items())

print(f"Valor esperado do custo por atraso: R$ {ve:.2f}")
```

**Callout `.conceito` obrigatório:** a distinção histograma × gráfico de barras. Não é preciosismo: se você desenhar categorias nominais com barras encostadas, está sugerindo visualmente uma continuidade e uma ordem que não existem nos dados.

**Callout `.exemplo`:** a maior causa de atraso em Dallas/Fort Worth (42%) é `Inbound` — atrasos herdados de um voo anterior da mesma aeronave. Ou seja: a maior fonte de atraso não é uma causa local, é a propagação de atrasos pela malha.

**Tabela-resumo:** as 5 causas com contagem e proporção.

- [ ] **Step 2: Escrever os exercícios**

1. **A causa `Security` responde por 0,12% dos atrasos. Uma companhia deveria investir em reduzir atrasos de segurança?** *Resposta:* pela frequência, não — é a menor causa. Mas a frequência não é tudo: o valor esperado depende também do **custo** de cada evento. Uma categoria rara e catastrófica pode ter valor esperado maior que uma frequente e barata. A pergunta certa combina probabilidade e consequência.
2. **Por que a moda é a única medida de localização que faz sentido para `dfw`?** *Resposta:* porque as categorias são nominais — não há ordem nem distância entre "Weather" e "Security". Média e mediana exigem que os valores possam ser somados ou ordenados, e nenhuma das duas operações significa algo aqui.
3. **Recalcule o valor esperado supondo que o custo de `Weather` sobe de R$ 0 para R$ 200. O que muda, e por quê o efeito é pequeno?** *Resposta:* o VE sobe cerca de R$ 8 (0,0403 × 200). O efeito é pequeno porque `Weather` tem probabilidade baixa (4%) — no valor esperado, cada custo entra **ponderado** pela sua probabilidade. É exatamente por isso que o VE é a ferramenta certa: ele impede que um número grande, mas raro, domine a decisão.

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render
H=_book/content/cap01/06-dados-binarios-categoricos.html
grep -c "Inbound" "$H"        # a moda
grep -c '<img' "$H"
grep -c 'callout-tip' "$H"
```
Expected: `Inbound` ≥ 1; `<img>` ≥ 1; `callout-tip` = 3.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/06-dados-binarios-categoricos.qmd
git commit -m "feat: secao 1.6 dados binarios e categoricos"
```

---

## Task 7: Seção 1.7 — Correlação

**Files:**
- Create: `content/cap01/07-correlacao.qmd` (substitui o stub)

**Interfaces:**
- Consumes: `dados/sp500_data.csv.gz`, `dados/sp500_sectors.csv`.

**Pontos didáticos obrigatórios:**

1. **Coeficiente de correlação de Pearson:** mede a associação **linear** entre duas variáveis numéricas, numa escala de −1 a +1. É adimensional — não depende da unidade.
2. **Matriz de correlação:** a correlação de todos os pares. Simétrica, com 1 na diagonal.
3. **Heatmap:** quando há muitas variáveis, ler a matriz em números é impraticável. Uma paleta **divergente** (centrada em zero) é a escolha certa, porque zero é um ponto de referência com significado.
4. **As três armadilhas** — este é o ponto pedagógico da seção:
   - Correlação **não** implica causalidade.
   - O coeficiente é **sensível a outliers** — um único ponto extremo pode criar ou destruir uma correlação.
   - Ele mede apenas relação **linear**. Duas variáveis podem ter dependência determinística forte (ex.: $y = x^2$ em torno de zero) e correlação **zero**.

- [ ] **Step 1: Escrever o arquivo**

```python
#| label: setup
#| include: false
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["figure.figsize"] = (7, 4)
```

Fórmula em LaTeX (obrigatória):

$$r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{(n-1)\, s_x \, s_y}$$

```python
#| label: carrega
setores = pd.read_csv("dados/sp500_sectors.csv")
precos  = pd.read_csv("dados/sp500_data.csv.gz", index_col=0)

simbolos_telecom = setores[setores["sector"] == "telecommunications_services"]["symbol"]
telecom = precos.loc[precos.index >= "2012-07-01", simbolos_telecom]

print("dias x empresas:", telecom.shape)
telecom.head()
```
Saída real: `(754, 5)` — as empresas são T, CTL, FTR, VZ, LVLT.

```python
#| label: matriz
telecom.corr().round(3)
```
Saídas reais (confira estas): T×VZ = **0,678** (a mais alta), T×CTL = 0,475, T×FTR = 0,328, T×LVLT = 0,279, CTL×FTR = 0,420.

Ponto a fazer: T (AT&T) e VZ (Verizon) são as duas maiores operadoras dos EUA; são as mais correlacionadas do grupo. Elas respondem aos mesmos choques de mercado.

```python
#| label: fig-heatmap
#| fig-cap: "Correlação dos retornos diários entre fundos negociados em bolsa (ETFs)."
etfs = precos.loc[precos.index > "2012-07-01",
                  setores[setores["sector"] == "etf"]["symbol"]]

fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(etfs.corr(), vmin=-1, vmax=1,
            cmap=sns.diverging_palette(20, 220, as_cmap=True), ax=ax)
plt.tight_layout()
plt.show()
```
Os ETFs são 17: XLI, QQQ, SPY, DIA, GLD, VXX, USO, IWM, XLE, XLY, XLU, XLB, XTL, XLV, XLP, XLF, XLK.

Ponto a fazer no heatmap: SPY, DIA e IWM (índices amplos) são fortemente correlacionados entre si. **VXX** (volatilidade) é o bloco azul — correlação **negativa** com quase tudo: quando o mercado cai, a volatilidade sobe. É a leitura que justifica a paleta divergente.

```python
#| label: fig-scatter
#| fig-cap: "Retornos diários de AT&T (T) contra Verizon (VZ). A nuvem é alongada na diagonal — o sinal visual de correlação positiva."
fig, ax = plt.subplots(figsize=(5, 5))
ax.scatter(telecom["T"], telecom["VZ"], alpha=0.5, s=20, color="#2c7fb8")
ax.axhline(0, color="grey", linewidth=0.8)
ax.axvline(0, color="grey", linewidth=0.8)
ax.set_xlabel("Retorno diário — AT&T (T)")
ax.set_ylabel("Retorno diário — Verizon (VZ)")
plt.tight_layout()
plt.show()
```

Chunk que **demonstra** a terceira armadilha (não é do livro, mas é o modo honesto de provar a afirmação):

```python
#| label: nao-linear
x = np.linspace(-1, 1, 200)
y = x ** 2

print(f"Correlação entre x e x²: {np.corrcoef(x, y)[0, 1]:.10f}")
```
Saída real: essencialmente **0** (da ordem de 1e-17). Faça o ponto: y é uma função **determinística** de x — conhecendo x você sabe y com certeza absoluta — e ainda assim a correlação é zero. Correlação zero significa "sem relação **linear**", não "sem relação".

**Callout `.conceito` obrigatório:** as três armadilhas, enumeradas.

- [ ] **Step 2: Escrever os exercícios**

1. **A correlação entre T e VZ é 0,678. Isso significa que o preço da AT&T causa o preço da Verizon?** *Resposta:* não. As duas são grandes operadoras de telecomunicações expostas aos mesmos fatores — taxa de juros, regulação, ciclo econômico. A correlação vem de uma **causa comum**, não de uma causar a outra. Este é o erro mais frequente na leitura de correlações.
2. **No heatmap, o VXX aparece em azul (correlação negativa) contra quase todos os demais. Por quê?** *Resposta:* o VXX acompanha a volatilidade do mercado, que sobe quando os preços caem. É por isso que a paleta divergente importa: ela torna o sinal (negativo × positivo) visível de relance, e o zero é uma referência com significado real.
3. **O código mostrou que a correlação entre `x` e `x²` é zero, embora `y` seja determinado por `x`. Explique.** *Resposta:* Pearson mede associação **linear**. A parábola é simétrica em torno de zero: para cada x positivo que puxa a covariância para cima, existe um x negativo que a puxa para baixo, e os efeitos se cancelam. Uma correlação de zero descarta relação linear — não descarta relação.

- [ ] **Step 3: Renderizar e verificar**

Run:
```bash
make render
H=_book/content/cap01/07-correlacao.html
grep -c "0.678" "$H"          # a correlação T x VZ
grep -c '<img' "$H"           # heatmap + scatter
grep -c 'callout-tip' "$H"
```
Expected: `0.678` ≥ 1; `<img>` ≥ 2; `callout-tip` = 3.

**Se `0.678` não aparecer, PARE** — a matriz de correlação não é a esperada.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/07-correlacao.qmd
git commit -m "feat: secao 1.7 correlacao"
```

---

## Task 8: Seção 1.8 — Explorando Duas ou Mais Variáveis

A seção mais longa do capítulo, e a única com gerador aleatório.

**Files:**
- Create: `content/cap01/08-duas-ou-mais-variaveis.qmd` (substitui o stub)

**Interfaces:**
- Consumes: `dados/kc_tax.csv.gz`, `dados/lc_loans.csv`, `dados/airline_stats.csv`.

**Pontos didáticos obrigatórios:**

1. A estrutura da seção é dada pelos **três pares de tipos** possíveis: numérico×numérico, categórico×categórico, categórico×numérico.
2. **Num × num:** o scatterplot **falha** quando há centenas de milhares de pontos — vira uma mancha sólida, e a densidade fica invisível. As duas saídas: **hexbin** (agrupa em células hexagonais e colore por contagem) e **contorno KDE** (curvas de nível da densidade).
3. **Cat × cat:** a **tabela de contingência**. Em contagem, ela é dominada pelo tamanho dos grupos; em **proporção por linha**, revela o padrão.
4. **Cat × num:** **boxplot agrupado** e **violin plot**. O violin mostra a **forma** da distribuição (bimodalidade, concentrações) que o boxplot esconde atrás de cinco números.
5. **Múltiplas variáveis:** condicionar por uma terceira variável (`FacetGrid`).

- [ ] **Step 1: Escrever o arquivo — parte numérico × numérico**

```python
#| label: setup
#| include: false
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["figure.figsize"] = (7, 4)
```

```python
#| label: carrega-kc
kc = pd.read_csv("dados/kc_tax.csv.gz")
print(f"registros brutos: {len(kc):,}")

kc0 = kc.loc[(kc.TaxAssessedValue < 750000) &
             (kc.SqFtTotLiving > 100) &
             (kc.SqFtTotLiving < 3500), :]
print(f"após filtrar extremos: {len(kc0):,}")
```
Saídas reais: `498,249` brutos → `432,693` após o filtro. Explique o filtro: remove imóveis de valor extremo e áreas implausíveis, que comprimiriam a escala e esconderiam o grosso dos dados.

```python
#| label: fig-hexbin
#| fig-cap: "Valor venal contra área construída, em 432.693 imóveis de King County. Cada hexágono é colorido pela quantidade de imóveis que caem nele."
fig, ax = plt.subplots(figsize=(6, 5))
kc0.plot.hexbin(x="SqFtTotLiving", y="TaxAssessedValue",
                gridsize=30, sharex=False, ax=ax)
ax.set_xlabel("Área construída (pés²)")
ax.set_ylabel("Valor venal (US$)")
plt.tight_layout()
plt.show()
```

**Chunk com RNG — a semente é OBRIGATÓRIA.** O KDE 2-D sobre 432 mil pontos leva minutos; 10.000 pontos bastam para a forma. Sem `random_state=42`, o contorno muda a cada render e o `freeze` perde o sentido.

```python
#| label: fig-kde
#| fig-cap: "Curvas de nível da mesma relação. O KDE roda sobre uma amostra de 10.000 imóveis — com semente fixa, para o gráfico ser reprodutível."
amostra = kc0.sample(10000, random_state=42)

fig, ax = plt.subplots(figsize=(6, 5))
sns.kdeplot(data=amostra, x="SqFtTotLiving", y="TaxAssessedValue", ax=ax)
ax.set_xlabel("Área construída (pés²)")
ax.set_ylabel("Valor venal (US$)")
plt.tight_layout()
plt.show()
```

- [ ] **Step 2: Escrever a parte categórico × categórico**

```python
#| label: crosstab
lc = pd.read_csv("dados/lc_loans.csv")

contagem = lc.pivot_table(index="grade", columns="status",
                          aggfunc=lambda x: len(x), margins=True)
contagem
```
Saída real (confira o total): `All` × `All` = **450.961** empréstimos. Grade A: 72.490. Grade G: 3.241.

```python
#| label: crosstab-pct
prop = contagem.copy().loc["A":"G", :].astype(float)
prop.loc[:, "Charged Off":"Late"] = prop.loc[:, "Charged Off":"Late"].div(prop["All"], axis=0)
prop["All"] = prop["All"] / sum(prop["All"])
prop.round(3)
```

Ponto a fazer, que é o coração desta parte: na tabela de **contagem**, a grade B parece a pior (5.302 inadimplentes) simplesmente porque é a maior. Na tabela de **proporção**, o padrão real aparece: a taxa de `Charged Off` **cresce monotonicamente** de A para G — que é exatamente o que a grade deveria significar. A tabela de contagem escondia isso.

- [ ] **Step 3: Escrever a parte categórico × numérico**

```python
#| label: fig-boxplot-grupo
#| fig-cap: "Percentual diário de voos atrasados por causa da companhia, por companhia aérea."
voos = pd.read_csv("dados/airline_stats.csv")

fig, ax = plt.subplots(figsize=(7, 5))
voos.boxplot(by="airline", column="pct_carrier_delay", ax=ax)
ax.set_xlabel("")
ax.set_ylabel("% diário de voos atrasados")
ax.set_ylim(0, 50)
plt.suptitle("")
plt.title("")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()
```
Medianas reais (para conferir a leitura): Alaska 3,23 · American 8,43 · Delta 5,55 · Jet Blue 7,66 · Southwest 6,96 · United 6,45. A Alaska é a melhor; a American, a pior.

```python
#| label: fig-violin
#| fig-cap: "O mesmo dado em violin plot. A largura mostra a densidade — o que o boxplot resume em cinco números."
fig, ax = plt.subplots(figsize=(7, 5))
sns.violinplot(data=voos, x="airline", y="pct_carrier_delay",
               ax=ax, inner="quartile", color="#b0c4d8")
ax.set_xlabel("")
ax.set_ylabel("% diário de voos atrasados")
ax.set_ylim(0, 50)
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()
```

**Callout `.conceito` obrigatório:** o violin mostra a **forma** — concentrações e bimodalidade — que o boxplot comprime em cinco números. Duas distribuições muito diferentes podem ter boxplots quase idênticos.

- [ ] **Step 4: Escrever a parte de múltiplas variáveis**

```python
#| label: fig-facet
#| fig-cap: "A mesma relação, condicionada ao CEP. O padrão muda de bairro para bairro."
kc_ceps = kc0.loc[kc0.ZipCode.isin([98188, 98105, 98108, 98126]), :]

g = sns.FacetGrid(kc_ceps, col="ZipCode", col_wrap=2, height=3.2)
g.map_dataframe(plt.hexbin, "SqFtTotLiving", "TaxAssessedValue", gridsize=25, cmap="Blues")
g.set_axis_labels("Área construída (pés²)", "Valor venal (US$)")
plt.tight_layout()
plt.show()
```
Contagens reais por CEP: 98105 → 4.481 · 98108 → 5.535 · 98126 → 5.631 · 98188 → 4.043.

Ponto a fazer: a inclinação da relação área→valor **muda por CEP**. O 98105 (perto da universidade) tem valores mais altos para a mesma área. Condicionar por uma terceira variável revela o que a visão agregada mistura.

Se o `map_dataframe` com `plt.hexbin` der erro de assinatura, use uma função auxiliar (é o que o livro faz):

```python
def hexbin(x, y, color, **kwargs):
    cmap = sns.light_palette(color, as_cmap=True)
    plt.hexbin(x, y, gridsize=25, cmap=cmap, **kwargs)

g = sns.FacetGrid(kc_ceps, col="ZipCode", col_wrap=2, height=3.2)
g.map(hexbin, "SqFtTotLiving", "TaxAssessedValue", extent=[0, 3500, 0, 700000])
```

**Tabela-resumo obrigatória:** os três pares de tipos e a ferramenta de cada um.

| Par | Ferramenta |
|---|---|
| Numérico × numérico | Scatterplot; hexbin ou contorno KDE quando há muitos pontos |
| Categórico × categórico | Tabela de contingência (em proporção, não em contagem) |
| Categórico × numérico | Boxplot agrupado; violin plot quando a forma importa |

- [ ] **Step 5: Escrever os exercícios**

1. **Por que o scatterplot falha com 432 mil imóveis, e o hexbin não?** *Resposta:* com muitos pontos, eles se sobrepõem e a região densa vira uma mancha sólida — a informação de **quantos** pontos há em cada região se perde. O hexbin não desenha pontos: divide o plano em células e colore cada uma pela contagem, transformando densidade em cor. É legível justamente onde o scatterplot satura.
2. **Na tabela de contingência em contagem, a grade B tem mais empréstimos "Charged Off" (5.302) que a grade G (409). Isso significa que B é mais arriscada que G?** *Resposta:* não. B tem 132.370 empréstimos e G tem 3.241 — B tem mais de tudo, porque é maior. Em **proporção**, a taxa de inadimplência de G é muito maior. Comparar contagens brutas entre grupos de tamanhos diferentes é um erro clássico; é para isso que serve a normalização por linha.
3. **Se o chunk do KDE não tivesse `random_state=42`, o que aconteceria a cada `quarto render`?** *Resposta:* o `sample(10000)` sortearia 10.000 imóveis diferentes, e o contorno mudaria de forma sutilmente a cada render. O gráfico publicado nunca seria o mesmo duas vezes, o cache do `freeze` deixaria de fazer sentido, e cada push acumularia um diff de ruído no site. É por isso que todo chunk com gerador aleatório neste livro fixa a semente.

- [ ] **Step 6: Renderizar e verificar**

Run:
```bash
make render
H=_book/content/cap01/08-duas-ou-mais-variaveis.html
grep -cE '432,693|450961|450,961' "$H"   # o filtro do kc_tax e o total do crosstab
grep -c '<img' "$H"                       # hexbin, kde, boxplot, violin, facet
grep -c 'callout-tip' "$H"
```
Expected: os números aparecem; `<img>` ≥ 5; `callout-tip` = 3.

- [ ] **Step 7: Verificar a regra da semente — o chunk aleatório está semeado?**

Run:
```bash
grep -n 'sample(' content/cap01/08-duas-ou-mais-variaveis.qmd
```
Expected: toda chamada a `.sample(` contém `random_state=42`. Se alguma não contiver, **corrija antes do commit** — é a regra global do projeto.

- [ ] **Step 8: Commit**

```bash
git add content/cap01/08-duas-ou-mais-variaveis.qmd
git commit -m "feat: secao 1.8 explorando duas ou mais variaveis"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean
make render
find _book/content/cap01 -name '*.html' | wc -l
```
Expected: `9` (o index do capítulo + as 8 seções), sem erro.

- [ ] **Nenhum stub restou no Capítulo 1**

```bash
grep -rl "Em construção" content/cap01/ && echo "AINDA HÁ STUB" || echo "capítulo 1 completo"
```
Expected: `capítulo 1 completo`.

- [ ] **Toda seção tem exercícios**

```bash
for f in content/cap01/0*.qmd; do
  grep -q "## Exercícios" "$f" || echo "SEM EXERCÍCIOS: $f"
done
echo "verificação concluída"
```
Expected: apenas `verificação concluída`.

- [ ] **Nenhum chunk aleatório sem semente**

```bash
grep -rnE '\.sample\(|default_rng\(|np\.random\.' content/cap01/ \
  | grep -vE 'random_state=42|default_rng\(42\)' \
  && echo "ERRO: RNG sem semente" || echo "sementes ok"
```
Expected: `sementes ok`.

- [ ] **Nenhum caminho de dados relativo ao arquivo**

```bash
grep -rnE '(read_csv|read_table)\([^)]*\.\./\.\./dados' content/cap01/ \
  && echo "ERRO" || echo "caminhos ok"
```
Expected: `caminhos ok`.

- [ ] **Os números da 1.3 sobreviveram ao retrofit**

```bash
grep -oE 'Média: 6,162,876\.3|Mediana: 4,436,369\.5' _book/content/cap01/03-estimativas-localizacao.html | sort -u
```
Expected: os dois números.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
