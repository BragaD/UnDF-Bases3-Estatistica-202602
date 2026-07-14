# Widgets Interativos na Seção 1.3 — Observable JS

**Data:** 2026-07-14
**Status:** Aprovado

## Objetivo

Acrescentar dois widgets interativos à seção 1.3 (Estimativas de Localização), para que o aluno **veja** a robustez da mediana e da média aparada em movimento, em vez de apenas ler sobre ela.

## A decisão de tecnologia, e por que não é Shinylive

O pedido original era Shinylive. Medi o custo antes de decidir, e ele mudou a escolha:

| Variante | Peso adicionado ao site publicado |
|---|---|
| Shinylive com `scipy` | **64 MB** |
| Shinylive só com `numpy` + `matplotlib` | **46 MB** |
| **Observable JS (`{ojs}`)** | **0 MB** |

O Shinylive embute o Pyodide (Python compilado para WebAssembly) e as *wheels* dos pacotes: o `scipy` sozinho pesa 13 MB, o runtime 9,7 MB, o matplotlib 6,5 MB. Além do peso no repositório, isso vira uma espera de download real para o aluno no primeiro acesso — o tipo de atrito que mata o uso em sala com wi-fi ruim.

O Observable JS é **nativo do Quarto** e roda no navegador sem runtime extra. Para o que estes widgets fazem — mover um slider, recalcular três estatísticas sobre 50 números, redesenhar um histograma — ele é instantâneo e gratuito.

**O critério que decidiu:** o código faz parte da lição? Aqui, não. A lição é a **intuição sobre robustez**; o código é o instrumento. Se o objetivo fosse o aluno ler e editar Python de verdade, os 46 MB do Shinylive se justificariam.

## Arquitetura

### Fonte única de dados

O chunk Python que **já existe** na seção 1.3 (`estado = pd.read_csv("dados/state.csv")`) passa a também alimentar os widgets, via a função `ojs_define()` que o Quarto injeta nos chunks Python:

```python
ojs_define(dados = estado)
```

Isso importa: os widgets **não** recarregam o CSV nem embutem uma cópia dos 50 valores. Eles leem o mesmo DataFrame que produziu os números impressos na página. Uma fonte, dois consumidores.

**Verificado antes de escrever este spec** (o risco declarado no design não se materializou): com pandas 3.0.3, o `ojs_define` serializa o DataFrame como um objeto orientado a colunas — 4 colunas × 50 linhas, com os valores corretos (Alabama = 4.779.736) — que é exatamente o formato que o `transpose()` do OJS consome. O plano B (passar `estado["Population"].tolist()`) fica disponível, mas não é necessário.

### O código dos widgets fica oculto

As células `{ojs}` levam `echo: false`. O código é **JavaScript**, num livro que ensina Python: exibi-lo sugeriria ao aluno que ele precisa aprendê-lo. O widget é apresentado como instrumento, e o Python segue sendo a única linguagem que o aluno **lê** no livro.

### Sem impacto no freeze nem no CI

O OJS roda no navegador do leitor, não no render. Não há chunk novo a executar, o cache do `freeze` não é afetado, e o CI não ganha nenhum passo.

## Os dois widgets

Ambos entram na seção 1.3, **depois** do conteúdo estático e **antes** dos exercícios.

### Widget A — O outlier

Um slider move a população da Califórnia de 1 a 300 milhões (o valor real é 37,3 M). As três estimativas são recalculadas ao vivo sobre os 50 estados, e o histograma redesenha.

O aluno vê a **média disparar** enquanto a média aparada e a mediana ficam praticamente paradas. É a demonstração de robustez em movimento — o mesmo ponto que a prosa faz, mas sentido em vez de lido.

### Widget B — O aparo

Um slider vai de 0% a 50%. Em 0% a média aparada **é** a média; em 50% ela **é** a mediana. O aluno vê a estimativa viajar continuamente de uma à outra.

Isto é literalmente a resposta do **exercício 1** da seção, que hoje pede ao aluno que imagine o que acontece "à medida que o aparo se aproxima de 50%". Com o widget, ele deixa de imaginar e passa a ver. A resposta do exercício ganha uma remissão ao widget.

## Ferramentas do OJS usadas

Todas já vêm no runtime do Quarto, sem import:

- `Inputs.range(...)` — os sliders
- `d3.mean`, `d3.median`, `d3.ascending` — as estatísticas e a ordenação
- `Plot` (Observable Plot) — os histogramas e as linhas de referência
- `transpose(...)` — converte o objeto orientado a colunas do `ojs_define` em array de registros

A média aparada é implementada em ~4 linhas (ordenar, cortar `k` de cada ponta, tirar a média do núcleo) — a mesma definição que o `scipy.stats.trim_mean` usa na seção.

## Verificação

Os checks estáticos de sempre (render sem erro, página gerada) **não bastam aqui**: uma célula `{ojs}` quebrada pode render sem erro e simplesmente não aparecer, ou aparecer e não responder ao slider. Por isso a verificação exige **abrir a página num navegador** e confirmar que:

1. Os dois sliders aparecem e são arrastáveis.
2. Mover o slider A muda os três números e redesenha o histograma.
3. Com o slider A no valor real da Califórnia (37,3 M), a média exibida bate com **6.162.876,3** — o número que a própria página imprime no chunk estático. Se divergir, o widget está lendo outra coisa.
4. Com o slider B em 0%, a média aparada exibida é igual à média (6.162.876,3); em 50%, é igual à mediana (4.436.369,5).

O item 3 é o que amarra o widget ao livro: ele prova que a fonte de dados é a mesma.

## Fora de escopo

- Widgets nos capítulos 2, 3 e 4. Se estes dois funcionarem bem em sala, o padrão se replica depois.
- Widgets para as demais seções do Capítulo 1.
- Qualquer uso de Shinylive ou Pyodide no repositório.
