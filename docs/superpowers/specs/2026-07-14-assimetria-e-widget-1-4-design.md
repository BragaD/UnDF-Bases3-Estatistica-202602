# Widget de Dispersão (1.4) e Subseção de Assimetria (1.5)

**Data:** 2026-07-14
**Status:** Aprovado

## Objetivo

Duas adições ao Capítulo 1, independentes entre si:

1. Um **widget interativo na seção 1.4** (Estimativas de Variabilidade): histograma da taxa de homicídios com o desvio-padrão sob controle do aluno, média fixa e eixos travados.
2. Uma **subseção sobre assimetria dentro da seção 1.5** (Explorando a Distribuição dos Dados), com três conjuntos de 25 notas que têm a mesma média e a mesma variância, mas formas completamente diferentes.

## Decisões do autor

- A subseção de assimetria fica **dentro da 1.5**, não em arquivo novo. O livro-texto (Bruce/Gedeck) não tem seção de assimetria; criar uma exigiria renumerar quatro arquivos, e a 1.5 já é a seção que trata da **forma** da distribuição.
- O widget da 1.4 é o **do histograma com desvio ajustável**, substituindo a ideia inicial de "arrastar São Paulo e ver o desvio explodir".
- **Ambos os eixos do histograma ficam travados.** Um eixo que se reajusta mascara justamente o efeito que o widget existe para mostrar.
- Os três conjuntos de notas são um **cenário concreto** (três turmas), não vetores abstratos.

---

## Widget da 1.4 — o desvio-padrão como controle

### A transformação

O aluno move o desvio-padrão; a média não se mexe. Isso é conseguido pela padronização:

$$\text{taxa}' = \mu + z \cdot \sigma_{\text{novo}}, \qquad z = \frac{\text{taxa} - \mu}{\sigma_{\text{real}}}$$

A média permanece **exatamente** 22,74 para qualquer $\sigma_{\text{novo}}$, e o desvio passa a ser exatamente o do slider. Não é aproximação: é identidade algébrica.

### Parâmetros (medidos sobre os dados reais)

| | Valor |
|---|---|
| Média da taxa (fixa) | **22,74** |
| Desvio real | **8,61** — o valor inicial do slider |
| Faixa do slider | **4,0 a 11,8** (passo 0,1) |
| Eixo x (travado) | `[0, 45]` |
| Eixo y (travado) | `[0, 8]` |
| Largura do bin | 2,5 |

O valor inicial é o desvio **real**, para que o estado de partida do widget seja o dado que a página já imprime.

### Por que o slider para em 11,8

Não é escolha estética. O desvio crítico é

$$\sigma_{\text{crítico}} = \frac{\mu}{|z_{\min}|} = \frac{22{,}74}{1{,}926} = 11{,}81$$

Acima disso, São Paulo — que tem a **menor** taxa do país (6,16, ou $z = -1{,}93$) — passaria a ter taxa **negativa**. Taxa de homicídios negativa não existe.

Isso vira o ponto didático da seção: **o piso em zero limita quanta dispersão uma variável positiva pode ter, dada a sua média.** É por isso que variáveis positivas e limitadas por baixo — renda, população, tempo de espera — tendem a ser assimétricas à direita: elas têm muito mais espaço para crescer do que para cair. A prosa faz essa ponte, que também prepara a subseção de assimetria da 1.5.

### O que o aluno vê

```
desvio  4,0 : ······██████·····     concentrado
desvio  8,6 : ··██·██████████··     ← o desvio REAL
desvio 11,8 : █·████·█·████████     espalhado até o limite
```

Com o eixo-y travado em 8, o desvio real ocupa 57% da altura — visível sem desperdiçar espaço, e o achatamento ao aumentar a dispersão fica evidente.

---

## Subseção de assimetria (dentro da 1.5)

### As três turmas

25 alunos cada, notas de 0 a 100, **mesma média e mesma variância**:

| Turma | Média | Mediana | Variância | Assimetria | Faixa das notas |
|---|---|---|---|---|---|
| A — à direita | 65,0 | 61,1 | 144,0 | **+0,81** | 50,2 a 92,0 |
| B — à esquerda | 65,0 | 68,9 | 144,0 | **−0,81** | 38,0 a 79,8 |
| C — simétrica | 65,0 | 65,0 | 144,0 | **0,00** | 39,9 a 90,1 |

### Como são construídos (não sorteados até dar certo)

Três garantias, todas por construção — não por sorte:

1. **A padronização crava média e variância.** $x' = \frac{x - \bar{x}}{s} \cdot \sigma + \mu$ força média $\mu$ e desvio $\sigma$ exatos. A assimetria é invariante a transformação linear, então sobrevive intacta.
2. **O espelhamento dá assimetria exatamente oposta.** $x' = 2\mu - x$ preserva média e variância e inverte o sinal da assimetria. A turma B é o espelho da A.
3. **A turma C é simétrica por construção**, não por amostragem: 12 desvios, seus 12 espelhos, e o centro. Assimetria **exatamente** zero, não "próxima de zero".

Cada turma usa seu **próprio gerador semeado** (`default_rng(42)` e `default_rng(7)`), para que a ordem de consumo do RNG não altere um conjunto em silêncio quando outro mudar.

### Por que média 65 e desvio 12

A escolha é uma restrição, não um gosto. Com média 65 e desvio 15, a nota 100 fica a apenas 2,33 desvios — e um conjunto em forma de sino com 25 pontos **estoura isso com frequência**, produzindo notas acima de 100.

Com desvio **12**, a folga sobe para 2,92 desvios, e o conjunto simétrico cabe em [0, 100] para **199 de 200 sementes**. O exemplo não depende de eu ter tirado a semente certa — é robusto.

### O ponto

O gancho é o cotidiano de quem dá aula: dois relatórios idênticos — *"média 65, desvio 12"* — descrevendo turmas que não têm nada a ver uma com a outra. Média e variância resumem **onde** e **quão espalhados**; não dizem nada sobre a **forma**.

E a regra emerge sozinha da tabela, sem precisar ser decorada:

- Assimetria **positiva** → cauda à direita → **média > mediana**
- Assimetria **negativa** → cauda à esquerda → **média < mediana**
- Assimetria **zero** → **média = mediana**

### Fechamento com os dados reais

Aplicar o conceito ao dado que o aluno já conhece:

| Variável | Assimetria |
|---|---|
| População das UFs | **+2,96** — fortemente à direita (é São Paulo) |
| Taxa de homicídios | **−0,19** — quase simétrica |

Isso amarra o capítulo: a assimetria +2,96 da população é a mesma razão pela qual, na seção 1.3, a média era 90% maior que a mediana.

---

## Verificação

- Os três conjuntos têm média e variância **idênticas** (assert no chunk, não só no olho).
- A turma B tem assimetria **exatamente oposta** à da A; a turma C, exatamente zero.
- Todas as notas ficam em [0, 100].
- O widget da 1.4 mantém a média em 22,74 para qualquer posição do slider.
- Os eixos do histograma **não se movem** ao arrastar o slider — verificado no navegador.
- O teste Playwright (`scripts/verifica-widgets.py`) cobre o widget novo: existe, é reativo, a média não muda, e os eixos ficam parados.

## Fora de escopo

- Widget interativo na subseção de assimetria (um slider que morfa a forma continuamente). A tabela e os três histogramas já entregam a lição; um widget aqui é YAGNI.
- Curtose (o 4º momento). Fica para quem quiser puxar o fio.
- Seção autônoma de assimetria com renumeração dos arquivos 06–08.
