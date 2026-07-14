# Widget de Dispersão (1.4) e Assimetria (1.5) — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Um widget na seção 1.4 que põe o desvio-padrão da taxa de homicídios sob controle do aluno (média fixa, eixos travados), e uma subseção sobre assimetria na 1.5 com três turmas de mesma média e mesma variância.

**Architecture:** O widget da 1.4 é uma célula `{ojs}` nativa do Quarto, alimentada pelo chunk Python da seção via `ojs_define`. A subseção de assimetria é Python puro (chunks + tabela + três histogramas), sem interatividade.

**Tech Stack:** Quarto OJS · Observable Plot · d3 · numpy · scipy.stats · matplotlib

**Spec:** `docs/superpowers/specs/2026-07-14-assimetria-e-widget-1-4-design.md`

## Global Constraints

- **Formato brasileiro em todo número impresso.** `from formato import num` nos chunks Python (`num(x, casas=1)` → `22,74`); `toLocaleString("pt-BR", ...)` no OJS. Nunca `f"{x:,.1f}"`.
- **Colunas do dataset:** `Estado`, `Populacao`, `Taxa.Homicidios`, `Sigla`. Caminho: `pd.read_csv("dados/estados.csv")`, nunca `../../dados/`.
- **Semente obrigatória em todo chunk com RNG.** A Task 2 usa `np.random.default_rng(42)` e `default_rng(7)` — **um gerador por conjunto**, para que a ordem de consumo do RNG não altere um conjunto em silêncio quando outro mudar.
- **Toda célula `{ojs}` leva `//| echo: false`.** É JavaScript num livro que ensina Python.
- **Português brasileiro.** Variáveis dos chunks em português.
- **Render sempre via container:** `make render`. Não há Quarto/Python confiáveis no host.
- **Não crie `AGENTS.md`.** Não mexa em `_quarto.yml`, `pyproject.toml`, `uv.lock`, `formato.py`, `dados/`.

## Duas armadilhas já verificadas neste projeto (não as redescubra)

1. **`ojs_define` NÃO emite dentro de um chunk com `include: false`.** Testei: o bloco `<script type="ojs-define">` simplesmente não aparece no HTML, e o widget carrega **vazio, sem erro nenhum**. Use `#| echo: false` + `#| output: false` — testei, e funciona (emite as 27 linhas, com o código oculto).

2. **O `Inputs.range` renderiza um `<input type="number">` ao lado do slider, que rejeita string não numérica.** Um `format` customizado devolvendo `"8,6 σ"` deixaria a caixa **vazia**, em silêncio. Não use `format` customizado — ponha a unidade no rótulo.

## Os números (todos medidos no container, sobre os dados reais)

**Widget da 1.4** — taxa de homicídios das 27 UFs:

| | Valor |
|---|---|
| Média (fixa, não se move) | **22,74** |
| Desvio real | **8,61** — valor inicial do slider |
| Faixa do slider | **4,0 a 11,8** (passo 0,01) |
| Desvio crítico | **11,81** = 22,74 ÷ 1,926 — acima disso, São Paulo teria taxa **negativa** |
| Eixo x (travado) | `[0, 45]` |
| Eixo y (travado) | `[0, 8]` (o pico em toda a faixa do slider é 7) |
| Largura do bin | 2,5 |

**Assimetria (1.5)** — três turmas de 25 alunos:

| Turma | Média | Mediana | Variância | Assimetria | Faixa |
|---|---|---|---|---|---|
| A — à direita | 65,0 | 61,1 | 144,0 | **0,81** | 50,2 a 92,0 |
| B — à esquerda | 65,0 | 68,9 | 144,0 | **-0,81** | 38,0 a 79,8 |
| C — simétrica | 65,0 | 65,0 | 144,0 | **0,00** | 39,9 a 90,1 |

**Dados reais:** assimetria da população das UFs = **2,96**; da taxa de homicídios = **-0,19**.

---

## Estrutura de Arquivos

| Arquivo | Task | O que muda |
|---|---|---|
| `content/cap01/04-estimativas-variabilidade.qmd` | 1 | chunk `ojs_define` + seção nova com o widget |
| `scripts/verifica-widgets.py` | 1 | passa a cobrir também a página 1.4 |
| `content/cap01/05-distribuicao-dados.qmd` | 2 | subseção `## Assimetria` + um exercício |

As duas tasks são **independentes** — nenhuma consome nada da outra.

---

## Task 1: Widget de dispersão na seção 1.4

**Files:**
- Modify: `content/cap01/04-estimativas-variabilidade.qmd`
- Modify: `scripts/verifica-widgets.py`

**Interfaces:**
- Produces: nada que a Task 2 consuma.
- **Sobre nomes OJS:** cada página do Quarto tem seu próprio módulo OJS. Os nomes `estados` e `fmt` já existem na página **1.3**, mas essa é outra página — não há colisão. Defina-os de novo aqui, uma vez cada.

- [ ] **Step 1: Exportar os dados para o OJS**

O chunk `setup` da seção tem `#| include: false`, e **`ojs_define` não emite nada dentro dele** (verificado). Crie um chunk **separado**, logo após o `setup`:

```python
#| label: exporta-ojs
#| echo: false
#| output: false
ojs_define(dados = estado)
```

Verifique depois do render que o bloco existe:
```bash
grep -c 'ojs-define' _book/content/cap01/04-estimativas-variabilidade.html
```
Expected: `1`. **Se der 0, o widget carregará vazio sem erro nenhum** — pare e corrija.

- [ ] **Step 2: Escrever a base OJS e o slider**

Insira uma seção nova, `## Mexa no desvio-padrão`, **depois** de `## Estimativas robustas: IQR e MAD` e **antes** de `## Resumo`. A prosa é sua, na voz da seção; o código abaixo é exato.

````markdown
```{ojs}
//| echo: false
estados = transpose(dados)

fmt = x => x.toLocaleString("pt-BR", {minimumFractionDigits: 1, maximumFractionDigits: 1})

// O z-score da taxa real, calculado UMA vez. É ele que permite mudar o desvio
// sem mexer na média: taxa' = μ + z × σ_novo devolve exatamente a média μ e
// exatamente o desvio σ_novo. Não é aproximação — é identidade algébrica.
// d3.deviation usa n−1, igual ao .std(ddof=1) do pandas.
base = {
  const taxas = estados.map(d => d["Taxa.Homicidios"]);
  const mu = d3.mean(taxas);
  const sd = d3.deviation(taxas);
  return {
    mu,
    sd,
    z: estados.map(d => ({sigla: d.Sigla, z: (d["Taxa.Homicidios"] - mu) / sd}))
  };
}
```

```{ojs}
//| echo: false
// Sem `format` customizado: a caixa <input type="number"> ao lado do slider
// rejeita string não numérica e ficaria vazia. A unidade vai no rótulo.
//
// O máximo é 11,8 e não é capricho: acima disso, São Paulo (a menor taxa do
// país) passaria a ter taxa NEGATIVA. Ver a prosa.
viewof desvio = Inputs.range([4, 11.8], {
  step: 0.01,
  value: 8.61,
  label: "Desvio-padrão da taxa:"
})
```

```{ojs}
//| echo: false
taxasAjustadas = base.z.map(d => ({sigla: d.sigla, taxa: base.mu + d.z * desvio}))

menor = taxasAjustadas.reduce((a, b) => (a.taxa < b.taxa ? a : b))
```
````

- [ ] **Step 3: O histograma de eixos travados**

Este é o coração do widget. **Os dois eixos têm `domain` fixo** — se qualquer um se reajustar, o gráfico "absorve" a mudança e o efeito que o widget existe para mostrar desaparece.

````markdown
```{ojs}
//| echo: false
Plot.plot({
  height: 300,
  marginLeft: 45,
  // Os DOIS eixos travados, de propósito: um eixo que se reajusta mascara
  // justamente o efeito que este widget existe para mostrar.
  x: {domain: [0, 45], label: "Taxa de homicídios (por 100 mil) →"},
  y: {domain: [0, 8], grid: true, label: "↑ Número de estados"},
  marks: [
    Plot.rectY(taxasAjustadas, Plot.binX({y: "count"}, {
      x: "taxa",
      thresholds: d3.range(0, 45.1, 2.5),
      fill: "#b0c4d8"
    })),
    Plot.ruleX([base.mu], {stroke: "#c0392b", strokeWidth: 2}),
    Plot.ruleY([0])
  ]
})
```

```{ojs}
//| echo: false
md`Média: **${fmt(base.mu)}** — a linha vermelha, que **não se move**.
Desvio-padrão: **${fmt(desvio)}** (o real é ${fmt(base.sd)}).

Menor taxa: **${fmt(menor.taxa)}** (${menor.sigla}) — Maior: **${fmt(d3.max(taxasAjustadas, d => d.taxa))}**`
```
````

- [ ] **Step 4: A prosa — e o motivo de o slider parar em 11,8**

A prosa que introduz o widget precisa fazer **dois** pontos:

**Primeiro:** média e desvio-padrão são independentes. O slider muda a dispersão e a linha vermelha da média **não sai do lugar** — porque a transformação é `taxa' = μ + z × σ_novo`, que devolve exatamente a média μ para qualquer σ.

**Segundo — e este é o ponto forte:** o slider **para em 11,8**, e não por capricho. O desvio crítico é

$$\sigma_{\text{crítico}} = \frac{\mu}{|z_{\min}|} = \frac{22{,}74}{1{,}926} = 11{,}81$$

Acima disso, São Paulo — que tem a **menor** taxa do país (6,16, ou z = −1,93) — passaria a ter taxa **negativa**. Taxa de homicídios negativa não existe.

Daí sai a lição: **o piso em zero limita quanta dispersão uma variável positiva pode ter, dada a sua média.** É por isso que variáveis positivas — renda, população, tempo de espera — tendem a ser assimétricas à direita: elas têm muito mais espaço para crescer do que para cair. (Arraste o slider até o fim e veja a menor taxa encostar em zero.)

Isso prepara o terreno para a subseção de assimetria da 1.5 — vale uma remissão.

- [ ] **Step 5: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap01/04-estimativas-variabilidade.html
grep -c 'ojs-define' "$H"
grep -c 'ojs-cell' "$H"
grep -oE 'Desvio-padrão: 9\.256\.155,8|IQR: 6\.443\.986,0|MAD: 4\.752\.396,9' "$H" | sort -u
```
Expected: `ojs-define` = 1; `ojs-cell` ≥ 4; e os três números do chunk Python **inalterados** (o widget não pode mexer neles).

- [ ] **Step 6: Estender o teste de navegador**

`scripts/verifica-widgets.py` hoje testa só a página 1.3. Ele precisa cobrir também a 1.4. **Um `grep` no HTML não basta**: uma célula `{ojs}` quebrada renderiza sem erro e simplesmente não aparece.

Acrescente uma função e chame-a no `main()`:

```python
URL_DISPERSAO = "http://localhost:8000/content/cap01/04-estimativas-variabilidade.html"

# A média da taxa, que o widget da 1.4 NÃO pode mover — é o ponto da seção.
MEDIA_TAXA = "22,7"


def verifica_dispersao(nav, falhas):
    """O widget da 1.4: mexer no desvio não move a média, e os eixos não se mexem."""
    page = nav.new_page()
    erros = []
    page.on("pageerror", lambda e: erros.append(str(e)))
    page.goto(URL_DISPERSAO, wait_until="networkidle")
    page.wait_for_selector('input[type="range"]', timeout=20000)

    slider = page.locator('input[type="range"]').first
    caixa = page.locator('input[type="number"]').first
    print(f"widget 1.4 — caixa do slider: {caixa.input_value()!r}")
    if not caixa.input_value():
        falhas.append("a caixa do slider da 1.4 está VAZIA — um `format` customizado?")

    def eixos_e_media():
        """Os rótulos do eixo x, os do eixo y, e o texto da média."""
        svg = page.locator("svg").last
        rotulos = svg.locator("text").all_inner_texts()
        corpo = page.inner_text("body")
        return rotulos, MEDIA_TAXA in corpo

    rot_ini, tem_media = eixos_e_media()
    if not tem_media:
        falhas.append(f"não achei a média ({MEDIA_TAXA}) na página da 1.4")

    # Mover o desvio de ponta a ponta NÃO pode mudar os eixos nem a média.
    for valor in ["4", "11.8"]:
        slider.fill(valor)
        slider.dispatch_event("input")
        page.wait_for_timeout(600)
        rot, tem_media = eixos_e_media()
        if rot != rot_ini:
            falhas.append(
                f"com desvio {valor}, os rótulos dos eixos MUDARAM — eles deveriam "
                f"estar travados, senão o gráfico mascara o efeito"
            )
        if not tem_media:
            falhas.append(f"com desvio {valor}, a média deixou de ser {MEDIA_TAXA} — "
                          f"a transformação deveria preservá-la")

    print("widget 1.4: eixos travados e média imóvel de ponta a ponta do slider")
    if erros:
        falhas.append(f"erros de JS na página 1.4: {erros[:2]}")
    page.close()
```

No `main()`, chame-a logo antes de `nav.close()`:

```python
            verifica_dispersao(nav, falhas)

            nav.close()
```

- [ ] **Step 7: Rodar o teste no navegador**

Run:
```bash
docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble \
  bash -c "pip install --quiet playwright==1.61.0 && python /scripts/verifica-widgets.py"
```
Expected: os testes da 1.3 seguem passando, mais:
```
widget 1.4 — caixa do slider: '8.61'
widget 1.4: eixos travados e média imóvel de ponta a ponta do slider

OK — os dois widgets carregam, são reativos e batem com os números do livro
```

**Se o teste acusar que os eixos mudaram, corrija o widget — não relaxe o teste.** Eixos travados é o requisito, não um detalhe.

- [ ] **Step 8: Commit**

```bash
git add content/cap01/04-estimativas-variabilidade.qmd scripts/verifica-widgets.py
git commit -m "feat: widget de dispersao na secao 1.4"
```

---

## Task 2: Subseção de assimetria na seção 1.5

**Files:**
- Modify: `content/cap01/05-distribuicao-dados.qmd`

**Interfaces:**
- Consumes: `dados/estados.csv` (já carregado no `setup` da seção, na variável `estado`).
- Produces: nada.

- [ ] **Step 1: Acrescentar os imports ao chunk `setup`**

O `setup` da seção (que tem `#| include: false`) precisa de:

```python
import numpy as np
from scipy import stats
```

Confira se já estão lá antes de duplicar.

- [ ] **Step 2: Gerar as três turmas**

Insira a subseção `## Assimetria` **depois** de `## Densidade` e **antes** de `## Resumo`.

O chunk abaixo é exato. Os três conjuntos são **construídos**, não sorteados até dar certo — e as garantias são `assert`, não "no olho":

```python
#| label: turmas
N, MEDIA, DESVIO = 25, 65.0, 12.0

def padroniza(x, media=MEDIA, desvio=DESVIO):
    """Crava média e desvio exatos, via z-score e reescala.

    A assimetria é invariante a transformação linear — ela sobrevive intacta.
    É isso que permite três conjuntos com a MESMA média e a MESMA variância,
    mas formas diferentes.
    """
    x = np.asarray(x, float)
    return (x - x.mean()) / x.std(ddof=1) * desvio + media

# Um gerador por turma: a ordem de consumo do RNG não pode alterar um conjunto
# em silêncio quando outro mudar.
turma_a = padroniza(np.random.default_rng(42).lognormal(0, 1.0, N))

# Espelho em torno da média: preserva média e variância, e inverte o SINAL da
# assimetria — exatamente, não aproximadamente.
turma_b = 2 * MEDIA - turma_a

# Simétrica POR CONSTRUÇÃO, não por amostragem: 12 desvios, seus 12 espelhos,
# e o centro. A assimetria é exatamente zero, não "próxima de zero".
desvios = np.abs(np.random.default_rng(7).normal(0, 1, (N - 1) // 2))
turma_c = padroniza(np.concatenate([-desvios, [0.0], desvios]))

turmas = {"A — à direita": turma_a, "B — à esquerda": turma_b, "C — simétrica": turma_c}

# As garantias são verificadas, não afirmadas.
assert np.allclose([t.mean() for t in turmas.values()], MEDIA)
assert np.allclose([t.var(ddof=1) for t in turmas.values()], DESVIO ** 2)
assert np.isclose(stats.skew(turma_a, bias=False), -stats.skew(turma_b, bias=False))
assert np.isclose(stats.skew(turma_c, bias=False), 0, atol=1e-12)
assert all(t.min() >= 0 and t.max() <= 100 for t in turmas.values())
```

**Por que média 65 e desvio 12, e não 70 e 15:** é uma restrição, não um gosto. Com desvio 15, a nota 100 fica a apenas 2,33 desvios da média, e um conjunto em forma de sino com 25 pontos **estoura isso com frequência** — produzindo notas acima de 100. Com desvio 12 a folga sobe para 2,92 desvios, e o conjunto simétrico cabe em [0, 100] para **199 de 200 sementes**. O `assert` da última linha guarda essa propriedade.

- [ ] **Step 3: A tabela — as quatro estatísticas**

```python
#| label: tabela-assimetria
resumo = pd.DataFrame(
    {
        "Média": [num(t.mean(), 1) for t in turmas.values()],
        "Mediana": [num(np.median(t), 1) for t in turmas.values()],
        "Variância": [num(t.var(ddof=1), 1) for t in turmas.values()],
        "Assimetria": [num(stats.skew(t, bias=False), 2) for t in turmas.values()],
    },
    index=list(turmas),
)
resumo
```

Saídas reais (confira depois do render):

| | Média | Mediana | Variância | Assimetria |
|---|---|---|---|---|
| A — à direita | 65,0 | 61,1 | 144,0 | 0,81 |
| B — à esquerda | 65,0 | 68,9 | 144,0 | -0,81 |
| C — simétrica | 65,0 | 65,0 | 144,0 | 0,00 |

- [ ] **Step 4: Os três histogramas**

```python
#| label: fig-assimetria
#| fig-cap: "Três turmas com a mesma média e a mesma variância — e formas completamente diferentes. A linha vermelha é a média; a verde tracejada, a mediana."
fig, eixos = plt.subplots(1, 3, figsize=(11, 3.3), sharey=True)

for ax, (nome, notas) in zip(eixos, turmas.items()):
    ax.hist(notas, bins=np.arange(30, 101, 7), color="#b0c4d8", edgecolor="white")
    ax.axvline(notas.mean(), color="#c0392b", linewidth=2)
    ax.axvline(np.median(notas), color="#27ae60", linestyle="--", linewidth=2)
    ax.set_title(nome, fontsize=10)
    ax.set_xlabel("Nota")

eixos[0].set_ylabel("Alunos")
plt.tight_layout()
plt.show()
```

O `sharey=True` importa: sem ele, cada painel escolheria sua própria escala e a comparação entre as três formas ficaria distorcida.

- [ ] **Step 5: A fórmula e a prosa**

A fórmula (obrigatória):

$$g_1 = \frac{\frac{1}{n}\sum_{i=1}^{n}(x_i - \bar{x})^3}{s^3}$$

O cubo é o que faz a assimetria funcionar: ele **preserva o sinal** do desvio. Desvios acima da média entram positivos, abaixo entram negativos, e eles se cancelam — a menos que uma das caudas seja mais longa. (No desvio-padrão, o quadrado destrói o sinal, e é por isso que ele nada diz sobre a forma.)

A prosa deve fazer **estes** pontos:

1. **O gancho:** dois relatórios idênticos — *"média 65, desvio 12"* — descrevendo turmas que não têm nada a ver uma com a outra. Média e variância dizem **onde** e **quão espalhado**; não dizem **nada** sobre a forma.
2. **A regra, que emerge sozinha da tabela** e não precisa ser decorada:
   - assimetria **positiva** → cauda à direita → **média > mediana** (65,0 > 61,1)
   - assimetria **negativa** → cauda à esquerda → **média < mediana** (65,0 < 68,9)
   - assimetria **zero** → **média = mediana** (65,0 = 65,0)
3. **Por que:** a cauda longa puxa a média (que soma todos os valores) e não move a mediana (que só olha o meio da fila). É a mesma fragilidade da média que a seção 1.3 mostrou — agora com um número que a mede.

Um callout `.conceito` com a regra dos três casos.

- [ ] **Step 6: Fechar com os dados reais**

```python
#| label: assimetria-real
print(f"População das UFs  : {num(stats.skew(estado['Populacao'], bias=False), 2)}")
print(f"Taxa de homicídios : {num(stats.skew(estado['Taxa.Homicidios'], bias=False), 2)}")
```
Saídas reais: `2,96` e `-0,19`.

A prosa amarra o capítulo: a assimetria de **2,96** da população é fortemente à direita — é São Paulo — e é **exatamente a mesma razão** pela qual, na seção 1.3, a média da população era 90% maior que a mediana. A taxa de homicídios, com **-0,19**, é quase simétrica: nela, média e mediana quase coincidem.

- [ ] **Step 7: Um exercício sobre assimetria**

A seção 1.5 tem três exercícios; toda seção do livro termina com exercícios. Acrescente um **quarto**, no formato dos existentes (resposta em `::: {.callout-tip collapse="true"}`):

> **4.** Um relatório informa que a renda média de um município é R\$ 4.200 e a mediana é R\$ 2.100. Sem ver os dados, o que você pode afirmar sobre a assimetria da distribuição de renda? E se média e mediana fossem iguais?

Resposta: a média é o dobro da mediana, então a assimetria é **positiva** (à direita) — há uma cauda de rendas altas puxando a média para cima, enquanto a mediana permanece onde está a maior parte das pessoas. É o padrão universal da renda, e a razão pela qual se reporta a mediana. Se média e mediana fossem iguais, a distribuição seria simétrica — o que, para renda, praticamente não acontece.

- [ ] **Step 8: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap01/05-distribuicao-dados.html
grep -oE '0,81|-0,81|0,00|144,0|65,0|61,1|68,9' "$H" | sort -u | tr '\n' ' '; echo
grep -oE 'População das UFs  : 2,96|Taxa de homicídios : -0,19' "$H"
grep -c '<img' "$H"
grep -c 'callout-tip' "$H"
```
Expected: os valores da tabela aparecem; as duas assimetrias reais (`2,96` e `-0,19`); `<img>` ≥ 4 (os 3 originais + o novo painel triplo); `callout-tip` = 4 (os 3 exercícios + o novo).

**Se os `assert` do chunk `turmas` falharem, o render quebra** — e é para isso que eles existem. Se isso acontecer, PARE e relate: significa que a construção não está entregando o que promete.

- [ ] **Step 9: Commit**

```bash
git add content/cap01/05-distribuicao-dados.qmd
git commit -m "feat: subsecao de assimetria na secao 1.5"
```

---

## Verificação Final

- [ ] **Render limpo do zero**

```bash
make clean && make render
find _book/content -name '*.html' | wc -l
```
Expected: `42`, sem erro.

- [ ] **Os números antigos das seções 1.4 e 1.5 sobreviveram**

```bash
grep -oE 'Desvio-padrão: 9\.256\.155,8|IQR: 6\.443\.986,0|MAD: 4\.752\.396,9' \
  _book/content/cap01/04-estimativas-variabilidade.html | sort -u
```
Expected: os três. As adições não podem ter mexido no que já estava certo.

- [ ] **Os widgets funcionam num navegador de verdade**

```bash
docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble \
  bash -c "pip install --quiet playwright==1.61.0 && python /scripts/verifica-widgets.py"
```
Expected: `OK — os dois widgets carregam, são reativos e batem com os números do livro`, incluindo as linhas do widget 1.4 (caixa preenchida, eixos travados, média imóvel).

- [ ] **Nenhum RNG sem semente**

```bash
grep -rnE 'default_rng\(|\.sample\(|np\.random\.' content/cap01/*.qmd \
  | grep -vE 'default_rng\(42\)|default_rng\(7\)|random_state=42|`sample' \
  && echo "ERRO: RNG sem semente" || echo "sementes ok"
```
Expected: `sementes ok`.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
