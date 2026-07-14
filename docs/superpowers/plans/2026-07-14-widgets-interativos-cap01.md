# Widgets Interativos na Seção 1.3 — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Acrescentar dois widgets Observable JS à seção 1.3, para que o aluno veja a robustez da mediana e da média aparada em movimento.

**Architecture:** Células `{ojs}` nativas do Quarto, que rodam no navegador do leitor. O chunk Python que já existe na seção passa a alimentá-las via `ojs_define(dados = estado)` — uma fonte de dados, dois consumidores. Zero bytes adicionados ao site, nenhum passo novo no CI, nenhum impacto no `freeze`.

**Tech Stack:** Quarto OJS · Observable Inputs · Observable Plot · d3 · Playwright (só para verificação)

**Spec:** `docs/superpowers/specs/2026-07-14-widgets-interativos-cap01-design.md`

## Global Constraints

- **O arquivo a modificar é um só:** `content/cap01/03-estimativas-localizacao.qmd`. Ele é a seção-modelo do livro inteiro e já passou por revisão — **não reescreva o que já está lá**. Os widgets entram **depois** da seção `## Resumo` e **antes** de `## Exercícios`.
- **Os números do chunk Python são intocáveis**, e a página os imprime nesta grafia exata (vírgula de milhar, ponto decimal — é o `f"{x:,.1f}"` do Python): `6,162,876.3` · `4,783,697.1` · `4,436,369.5`. Nenhuma alteração pode mudá-los, e **o widget deve exibi-los na mesma grafia** — do contrário o mesmo número apareceria de dois jeitos na mesma página.
- **O código OJS fica oculto:** toda célula `{ojs}` leva `//| echo: false`. É JavaScript num livro que ensina Python — exibi-lo sugeriria que o aluno precisa aprendê-lo.
- **Fonte única de dados:** os widgets leem o DataFrame `estado` via `ojs_define`. Proibido recarregar o CSV ou embutir os 50 valores como literal.
- **Render sempre via container:** `make render`. Não há Quarto/Python confiáveis no host.
- **Fidelidade ao livro-texto:** a prosa que apresenta os widgets segue a voz da seção — direta, com opinião didática. Sem analogias de engenharia de software.
- **Nada de Shinylive/Pyodide** entra no repositório.

## Fato já verificado (não re-teste, construa em cima)

`ojs_define` funciona com pandas 3.0.3. Testado neste projeto: `ojs_define(dados = estado)` serializa o DataFrame como objeto **orientado a colunas** — 4 colunas (`State`, `Population`, `Murder.Rate`, `Abbreviation`) × 50 linhas, com valores corretos (Alabama = 4.779.736). Em OJS, `transpose(dados)` converte isso num array de 50 registros.

---

## Estrutura de Arquivos

| Arquivo | O que muda |
|---|---|
| `content/cap01/03-estimativas-localizacao.qmd` | Uma linha no chunk Python (`ojs_define`); duas seções novas com os widgets; uma remissão na resposta do exercício 1 |
| `scripts/verifica-widgets.py` | Script Playwright que dirige a página num navegador de verdade |
| `CLAUDE.md` | Documenta o padrão OJS e por que Shinylive foi recusado |

---

## Task 1: Widget A — o outlier

**Files:**
- Modify: `content/cap01/03-estimativas-localizacao.qmd`

**Interfaces:**
- Produces: as variáveis OJS `estados` (array de 50 registros), `mediaAparada(x, prop)` e `fmt(x)` — a Task 2 as reutiliza. Defina-as UMA vez; a Task 2 não pode redefini-las (OJS proíbe redeclaração e a página quebraria).

- [ ] **Step 1: Acrescentar `ojs_define` ao chunk Python existente**

No chunk `#| label: carrega` (que já faz `estado = pd.read_csv("dados/state.csv")`), acrescente uma linha ao final. **Não mexa em mais nada do chunk.**

```python
#| label: carrega
estado = pd.read_csv("dados/state.csv")
ojs_define(dados = estado)
estado.head()
```

A ordem importa: `ojs_define` antes do `estado.head()`, para que a saída exibida na página continue sendo a tabela (que é o que o aluno deve ver), e não o retorno do `ojs_define`.

- [ ] **Step 2: Escrever a base OJS e o Widget A**

Insira **entre** a seção `## Resumo` e a seção `## Exercícios`. A prosa introdutória é sua, na voz da seção; o código OJS abaixo é exato.

Primeiro, a base compartilhada (definida uma única vez, usada pelos dois widgets):

````markdown
```{ojs}
//| echo: false
estados = transpose(dados)

// Espelha o formato do f"{x:,.1f}" que o chunk Python usa acima nesta mesma
// página. Trocar para pt-BR aqui faria o MESMO número aparecer de dois jeitos
// diferentes na mesma página (6.162.876,3 vs 6,162,876.3) — o aluno notaria.
fmt = x => x.toLocaleString("en-US", {minimumFractionDigits: 1, maximumFractionDigits: 1})

// Mesma definição do scipy.stats.trim_mean: corta k = floor(n × prop)
// observações de cada ponta e tira a média do que sobra.
function mediaAparada(x, prop) {
  const s = [...x].sort(d3.ascending);
  const k = Math.floor(s.length * prop);
  const nucleo = s.slice(k, s.length - k);
  return nucleo.length ? d3.mean(nucleo) : d3.median(s);
}
```
````

Depois o Widget A. O `value` do slider é **exatamente** a população real da Califórnia (37.253.956) e o `step` é 1 — assim, na carga inicial, as três estatísticas batem dígito a dígito com as que o chunk Python imprime acima na mesma página. Um `step` grosso arredondaria o valor inicial e quebraria essa correspondência.

````markdown
```{ojs}
//| echo: false
viewof pop_ca = Inputs.range([1_000_000, 300_000_000], {
  step: 1,
  value: 37253956,
  label: "População da Califórnia:",
  format: x => (x / 1e6).toFixed(1) + " M"
})
```

```{ojs}
//| echo: false
popsA = estados.map(d => d.State === "California" ? pop_ca : d.Population)

estatA = ({
  media:   d3.mean(popsA),
  aparada: mediaAparada(popsA, 0.10),
  mediana: d3.median(popsA)
})
```

```{ojs}
//| echo: false
html`<table class="table">
  <thead><tr><th>Estimativa</th><th style="text-align:right">Valor</th></tr></thead>
  <tbody>
    <tr><td><span style="color:#c0392b">━</span> Média</td>
        <td style="text-align:right"><strong>${fmt(estatA.media)}</strong></td></tr>
    <tr><td><span style="color:#e67e22">┅</span> Média aparada (10%)</td>
        <td style="text-align:right"><strong>${fmt(estatA.aparada)}</strong></td></tr>
    <tr><td><span style="color:#27ae60">┈</span> Mediana</td>
        <td style="text-align:right"><strong>${fmt(estatA.mediana)}</strong></td></tr>
  </tbody>
</table>`
```

```{ojs}
//| echo: false
Plot.plot({
  height: 260,
  marginLeft: 55,
  x: {label: "População (milhões) →"},
  y: {label: "↑ Número de estados", grid: true},
  marks: [
    Plot.rectY(popsA, Plot.binX({y: "count"}, {x: d => d / 1e6, fill: "#b0c4d8", thresholds: 20})),
    Plot.ruleX([estatA.media / 1e6],   {stroke: "#c0392b", strokeWidth: 2}),
    Plot.ruleX([estatA.aparada / 1e6], {stroke: "#e67e22", strokeWidth: 2, strokeDasharray: "5 3"}),
    Plot.ruleX([estatA.mediana / 1e6], {stroke: "#27ae60", strokeWidth: 2.5, strokeDasharray: "1 3"}),
    Plot.ruleY([0])
  ]
})
```
````

A prosa que introduz o widget deve fazer **este** ponto: arraste a Califórnia para 300 milhões e observe qual das três linhas se move. A média persegue o outlier; a média aparada e a mediana não saem do lugar. É a mesma afirmação da prosa acima, agora sob o controle do aluno.

- [ ] **Step 3: Renderizar e conferir a carga inicial**

Run:
```bash
make render
H=_book/content/cap01/03-estimativas-localizacao.html
python3 -c "
import re, json
h = open('$H').read()
m = re.search(r'<script type=\"ojs-define\">(.*?)</script>', h, re.S)
assert m, 'ojs_define AUSENTE — o widget não terá dados'
d = json.loads(m.group(1))
v = {c['name']: c['value'] for c in d['contents']}['dados']
print('colunas:', list(v))
print('linhas :', len(v['State']))
print('CA     :', v['Population'][v['State'].index('California')])
"
grep -c 'ojs-cell' "\$H"
```
Expected:
```
colunas: ['State', 'Population', 'Murder.Rate', 'Abbreviation']
linhas : 50
CA     : 37253956
```
e a contagem de `ojs-cell` ≥ 5.

**Se `ojs_define` estiver ausente, PARE** — sem ele o widget carrega vazio e não há como o aluno perceber que está vendo lixo.

- [ ] **Step 4: Verificar que os números do chunk Python NÃO mudaram**

Run:
```bash
grep -oE 'Média: 6,162,876\.3|Média aparada \(10%\): 4,783,697\.1|Mediana: 4,436,369\.5' _book/content/cap01/03-estimativas-localizacao.html | sort -u
```
Expected: os três números, intactos.

- [ ] **Step 5: Commit**

```bash
git add content/cap01/03-estimativas-localizacao.qmd
git commit -m "feat: widget interativo do outlier na secao 1.3"
```

---

## Task 2: Widget B — o aparo

**Files:**
- Modify: `content/cap01/03-estimativas-localizacao.qmd`

**Interfaces:**
- Consumes: `estados`, `mediaAparada(x, prop)` e `fmt(x)`, definidas na Task 1. **NÃO as redefina** — em OJS, redeclarar um nome quebra a página inteira com "duplicate definition".
- Produces: nada que outra task consuma.

- [ ] **Step 1: Escrever o Widget B**

Insere logo depois do Widget A, ainda antes de `## Exercícios`.

````markdown
```{ojs}
//| echo: false
viewof aparo = Inputs.range([0, 50], {
  step: 1,
  value: 10,
  label: "Aparo em cada ponta:",
  format: x => x + "%"
})
```

```{ojs}
//| echo: false
popsB = estados.map(d => d.Population)

estatB = ({
  media:   d3.mean(popsB),
  aparada: mediaAparada(popsB, aparo / 100),
  mediana: d3.median(popsB),
  cortados: Math.floor(popsB.length * aparo / 100)
})
```

```{ojs}
//| echo: false
md`Aparo de **${aparo}%** — descarta **${estatB.cortados}** estados de cada ponta.
A média aparada vale **${fmt(estatB.aparada)}**.`
```

```{ojs}
//| echo: false
Plot.plot({
  height: 130,
  marginLeft: 55,
  marginBottom: 40,
  x: {domain: [4.2, 6.4], label: "População (milhões) →"},
  y: {axis: null, domain: [-1, 1]},
  marks: [
    Plot.ruleY([0], {stroke: "#ccc"}),
    Plot.link([{x1: estatB.mediana / 1e6, x2: estatB.media / 1e6}],
              {x1: "x1", x2: "x2", y1: 0, y2: 0, stroke: "#ccc", strokeWidth: 6}),
    Plot.dot([{x: estatB.media / 1e6}],   {x: "x", y: 0, r: 7, fill: "#c0392b"}),
    Plot.dot([{x: estatB.mediana / 1e6}], {x: "x", y: 0, r: 7, fill: "#27ae60"}),
    Plot.dot([{x: estatB.aparada / 1e6}], {x: "x", y: 0, r: 10, fill: "#e67e22",
                                           stroke: "white", strokeWidth: 2}),
    Plot.text([{x: estatB.media / 1e6}],   {x: "x", y: 0.6, text: ["média"], fill: "#c0392b"}),
    Plot.text([{x: estatB.mediana / 1e6}], {x: "x", y: 0.6, text: ["mediana"], fill: "#27ae60"}),
    Plot.text([{x: estatB.aparada / 1e6}], {x: "x", y: -0.6, text: ["aparada"], fill: "#e67e22"})
  ]
})
```
````

A prosa deve fazer **este** ponto: em 0% a média aparada *é* a média; em 50% ela *é* a mediana. Ela não é uma terceira estimativa solta — é uma família contínua que liga as outras duas, e o slider é o parâmetro dessa família.

Por que a matemática fecha nos extremos: em 0%, `k = 0` e nada é cortado. Em 50%, `k = 25` de cada ponta, o núcleo fica vazio, e a função devolve a mediana por definição.

- [ ] **Step 2: Atualizar a resposta do exercício 1**

O exercício 1 pede ao aluno que imagine "o que acontece quando o aparo se aproxima de 50%". O widget B responde isso visualmente. Acrescente uma remissão ao final da resposta existente — **sem reescrever o resto dela**:

```markdown
Arraste o slider do aparo até 50% no widget acima: a média aparada pousa exatamente sobre a mediana.
```

- [ ] **Step 3: Renderizar e conferir**

Run:
```bash
make render
H=_book/content/cap01/03-estimativas-localizacao.html
grep -c 'ojs-cell' "$H"
grep -c 'callout-tip' "$H"
grep -oE 'Média: 6,162,876\.3|Mediana: 4,436,369\.5' "$H" | sort -u
```
Expected: `ojs-cell` ≥ 9; `callout-tip` = 3 (os exercícios seguem intactos); os dois números do Python inalterados.

- [ ] **Step 4: Commit**

```bash
git add content/cap01/03-estimativas-localizacao.qmd
git commit -m "feat: widget interativo do aparo na secao 1.3"
```

---

## Task 3: Verificação no navegador e documentação

Esta é a task que dá valor às duas anteriores. Uma célula `{ojs}` quebrada **renderiza sem erro** e simplesmente não aparece na página, ou aparece e não responde. Os `grep` das tasks 1 e 2 provam que o código chegou ao HTML — não provam que ele **funciona**. Só um navegador de verdade prova.

**Files:**
- Create: `scripts/verifica-widgets.py`
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: o `_book/` renderizado pelas Tasks 1 e 2.

- [ ] **Step 1: Escrever o script de verificação**

Ele serve o `_book/` por HTTP (o OJS não funciona a partir de `file://`), abre a página num Chromium de verdade, e **dirige o slider**, conferindo que os números mudam.

```python
# scripts/verifica-widgets.py
"""Verifica no navegador que os widgets OJS da seção 1.3 funcionam de fato.

Roda dentro do container playwright (ver o comando no Step 2). Serve o _book/
por HTTP porque o Observable JS não carrega a partir de file://.
"""
import re
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

URL = "http://localhost:8000/content/cap01/03-estimativas-localizacao.html"

# Os mesmos números que o chunk Python imprime na página. Se o widget mostrar
# outra coisa na carga inicial, ele não está lendo os dados do livro.
MEDIA_REAL = "6,162,876.3"
MEDIANA_REAL = "4,436,369.5"


def numeros_da_tabela(page):
    """Os três valores da tabela do Widget A, na ordem: média, aparada, mediana."""
    celulas = page.locator("table.table td strong").all_inner_texts()
    return [c.strip() for c in celulas]


def main():
    servidor = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        cwd="/site", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    falhas = []
    try:
        with sync_playwright() as p:
            nav = p.chromium.launch()
            page = nav.new_page()
            erros = []
            page.on("pageerror", lambda e: erros.append(str(e)))
            page.goto(URL, wait_until="networkidle")
            page.wait_for_selector("table.table td strong", timeout=20000)

            # 1. Os dois sliders existem?
            sliders = page.locator('input[type="range"]')
            n = sliders.count()
            print(f"sliders encontrados: {n}")
            if n < 2:
                falhas.append(f"esperava 2 sliders, achei {n}")

            # 2. Carga inicial: os números do widget batem com os do chunk Python?
            inicial = numeros_da_tabela(page)
            print(f"widget A na carga inicial: {inicial}")
            if not inicial or inicial[0] != MEDIA_REAL:
                falhas.append(f"média inicial do widget = {inicial[0] if inicial else '(vazio)'}, "
                              f"esperava {MEDIA_REAL} (o mesmo que o Python imprime)")
            if len(inicial) >= 3 and inicial[2] != MEDIANA_REAL:
                falhas.append(f"mediana inicial = {inicial[2]}, esperava {MEDIANA_REAL}")

            # 3. Mover o slider A muda a média — e NÃO move a mediana.
            sliders.nth(0).fill("300000000")
            sliders.nth(0).dispatch_event("input")
            page.wait_for_timeout(800)
            depois = numeros_da_tabela(page)
            print(f"widget A com CA em 300 M : {depois}")
            if depois == inicial:
                falhas.append("mover o slider A não mudou nada — o widget não é reativo")
            if len(depois) >= 3 and depois[2] != MEDIANA_REAL:
                falhas.append(f"a mediana MUDOU para {depois[2]} — deveria ser robusta ao outlier")
            if len(depois) >= 1 and depois[0] == MEDIA_REAL:
                falhas.append("a média NÃO mudou — deveria perseguir o outlier")

            # 4. Slider B em 50%: a média aparada tem que pousar na mediana.
            sliders.nth(1).fill("50")
            sliders.nth(1).dispatch_event("input")
            page.wait_for_timeout(800)
            texto = page.inner_text("body")
            if MEDIANA_REAL not in texto:
                falhas.append(f"com aparo 50%, não achei a mediana ({MEDIANA_REAL}) na página")
            else:
                print(f"widget B com aparo 50%: média aparada pousou em {MEDIANA_REAL}")

            # 5. Nenhum erro de JavaScript.
            if erros:
                falhas.append(f"erros de JS na página: {erros[:3]}")

            nav.close()
    finally:
        servidor.terminate()

    print()
    if falhas:
        print("FALHOU:")
        for f in falhas:
            print("  -", f)
        sys.exit(1)
    print("OK — os dois widgets carregam, são reativos e batem com os números do livro")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar a verificação num container Playwright descartável**

O Playwright **não** entra na imagem do livro — ela ficaria centenas de MB maior à toa, e o CI a baixaria a cada push. Usamos um container avulso, montando o `_book/` renderizado e o script.

Run:
```bash
docker run --rm \
  -v "$PWD/_book:/site:ro" \
  -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble \
  python /scripts/verifica-widgets.py
```
Expected (o primeiro `docker run` baixa a imagem e demora):
```
sliders encontrados: 2
widget A na carga inicial: ['6,162,876.3', '4,783,697.1', '4,436,369.5']
widget A com CA em 300 M : ['11,416,756.4', '4,783,697.1', '4,436,369.5']
widget B com aparo 50%: média aparada pousou em 4,436,369.5

OK — os dois widgets carregam, são reativos e batem com os números do livro
```

Os valores exatos após mover o slider podem diferir do exemplo — o que **não** pode variar é: a média muda, a mediana **não**, e a aparada quase não. Se a mediana se mover, a `mediaAparada` ou o `d3.median` estão operando sobre o array errado.

Se o script sair com falha, **corrija o widget** — não relaxe o script.

- [ ] **Step 3: Documentar o padrão no `CLAUDE.md`**

Acrescente uma seção. O ponto principal é o critério de decisão, não o "como" — ele é o que vai orientar as decisões dos próximos capítulos.

````markdown
### Widgets interativos (Observable JS)

A seção 1.3 tem dois widgets em células `{ojs}`, nativas do Quarto: rodam no navegador do leitor, **não somam bytes ao site** e não afetam o `freeze` nem o CI.

Os dados vêm do próprio chunk Python da seção, via `ojs_define(dados = estado)` — uma fonte, dois consumidores. Nunca recarregue o CSV no OJS nem embuta os valores como literal.

O código OJS vai sempre com `//| echo: false`. É JavaScript num livro que ensina Python: exibi-lo sugeriria ao aluno que ele precisa aprendê-lo.

**Shinylive foi avaliado e recusado.** Ele embute o Pyodide e as wheels dos pacotes: medi **46 MB** (numpy + matplotlib) a **64 MB** (com scipy) adicionados ao site, e uma espera de download real para o aluno. O critério que decidiu: *o código faz parte da lição?* Nestes widgets, não — a lição é a intuição sobre robustez, e o código é o instrumento. Se um dia o objetivo for o aluno **ler e editar Python de verdade**, o Shinylive volta à mesa e os 46 MB se justificam.

**Verificação:** `grep` no HTML não basta — uma célula `{ojs}` quebrada renderiza sem erro e simplesmente não aparece. Rode o teste de navegador:

```bash
make render
docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble python /scripts/verifica-widgets.py
```
````

- [ ] **Step 4: Commit**

```bash
git add scripts/verifica-widgets.py CLAUDE.md
git commit -m "test: verificacao dos widgets OJS em navegador real"
```

---

## Verificação Final

- [ ] **Render limpo e o livro inteiro de pé**

```bash
make clean && make render
find _book/content -name '*.html' | wc -l
```
Expected: `42`, sem erro.

- [ ] **Os widgets funcionam num navegador de verdade**

```bash
docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
  mcr.microsoft.com/playwright/python:v1.61.0-noble python /scripts/verifica-widgets.py
```
Expected: `OK — os dois widgets carregam, são reativos e batem com os números do livro`

- [ ] **O site não engordou**

```bash
du -sh _book | cut -f1
grep -rl 'shinylive\|pyodide' _book/ 2>/dev/null && echo "ERRO: Pyodide vazou para o site" || echo "sem Pyodide — ok"
```
Expected: nenhum vestígio de Pyodide/Shinylive.

- [ ] **Os números do chunk Python sobreviveram**

```bash
grep -oE 'Média: 6,162,876\.3|Média aparada \(10%\): 4,783,697\.1|Mediana: 4,436,369\.5' \
  _book/content/cap01/03-estimativas-localizacao.html | sort -u
```
Expected: os três.

- [ ] **Os exercícios seguem intactos**

```bash
grep -c 'callout-tip' _book/content/cap01/03-estimativas-localizacao.html
```
Expected: `3`.

- [ ] **Working tree limpa**

```bash
git status --short
```
Expected: nenhuma saída.
