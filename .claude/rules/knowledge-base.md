---
paths:
  - "content/**/*.qmd"
  - "notebooks/**/*.ipynb"
  - "avaliacoes/**/*.qmd"
---

# Base de conhecimento do curso: Bases 3 — Estatística (UnDF)

Lida por `/create-lecture`, `/scaffold-exercises`, `/devils-advocate` e pelos agentes
`pedagogy-reviewer` e `domain-reviewer` **antes** de criar ou revisar conteúdo. O `CLAUDE.md`
continua sendo a fonte de verdade para escopo, estrutura e ambiente; este arquivo guarda o que
ele não guarda: **notação, progressão e armadilhas de conteúdo**.

## Registro de notação

A notação segue @bussab2023 sempre que ele define o objeto; onde ele é omisso, segue @bruce2020.

| Regra | Convenção | Exemplo | Anti-padrão |
|---|---|---|---|
| Estatísticas de ordem | parênteses no índice | $x_{(1)} \le \dots \le x_{(n)}$ | $x_1$ para "o menor valor" |
| Quantil | $q(p)$, $0 < p < 1$ | $q(0{,}25) = q_1$ | $Q_{25}$, $P_{25}$ como símbolo |
| Quartis | minúsculos, com índice | $q_1, q_2, q_3$; $q_2 = md$ | $Q1$ em fórmula |
| Distância interquartil | $d_q = q_3 - q_1$ (Bussab); "IQR" no texto (Bruce) | — | inventar um terceiro nome |
| Média amostral | $\bar{x}$ | $\bar{x} = \frac{1}{n}\sum x_i$ | $\mu$ para média de amostra |
| Desvio padrão amostral | $s$ (divisor $n-1$, como o pandas) | `std(ddof=1)` | $\sigma$ para dado amostral |
| Condicional | $P(A \mid B) = P(A \cap B)/P(B)$, $P(B) > 0$ | — | $P(A/B)$ |
| Combinação | $\binom{n}{k}$ | `math.comb(n, k)` | $C_n^k$ sem definir |
| Binomial | $X \sim b(n, p)$; $P(X=k) = b(k; n, p)$ | — | $\mathrm{Bin}$ misturado com $b$ |
| Hipergeométrica | $X \sim \mathrm{hip}(N, r, n)$: população $N$, $r$ sucessos, amostra $n$ | — | letras da scipy no texto |
| Normal | $X \sim N(\mu, \sigma^2)$ — **variância** no 2º argumento | $Z \sim N(0, 1)$ | $N(\mu, \sigma)$ |
| Números | vírgula decimal na prosa e nas tabelas renderizadas (`formato.num`) | $0{,}25$ em LaTeX | `0.25` na prosa |

## Progressão do livro

| Seção | Pergunta central | Notação-chave | Fonte |
|---|---|---|---|
| Intro | Por que estatística? Simpson | — | @weed |
| 1.1–1.2 | Que tipo de dado eu tenho? | — | Bruce 1 |
| 1.3 | Qual o valor típico? | $\bar{x}$, $md$, média aparada/ponderada | Bruce 1.3 |
| 1.4 | Quanto os dados se afastam? | $s^2$, $s$, $x_{(i)}$, $q_1, q_2, q_3$, $d_q$ | Bruce 1.4 + Bussab 3.3 |
| 1.5 | Qual a forma da distribuição? | $q(p)$, boxplot, histograma | Bruce 1.5 + Bussab 3.3 |
| 1.6–1.7 | Categóricos; correlação | $r$ | Bruce 1.6–1.7 |
| 1.8 | (leitura complementar, fora do notebook) | — | Bruce 1.8 |
| 2.1–2.2 | O que é probabilidade? Regras | $P(A)$, $A \cup B$, $A \cap B$ | @weed |
| 2.3 | Condicional e Bayes | $P(A \mid B)$, partição | Bussab 5.3–5.4 |
| 2.4 | Contagem | $n!$, $\binom{n}{k}$ | Bussab 5.2 |
| 2.5–2.7 | Binomial, hipergeométrica, normal | $b(n,p)$, $\mathrm{hip}(N,r,n)$, $N(\mu,\sigma^2)$ | Bruce 2 + Bussab 6.6.4 |
| 3.x | Amostragem, bootstrap, IC | — | Bruce 2 |
| 4.x, 5.x | Testes até t; regressão até predição (stubs) | — | Bruce 3–4 |

## Aplicações recorrentes

| Aplicação | Dataset | Seções | Para quê |
|---|---|---|---|
| Estados brasileiros | `dados/estados.csv` (n = 27) | 1.3–1.5 | mediana é observação real; SP é o outlier; média ponderada < simples |
| Aluguéis (BR) | gerado por `scripts/gerar-dados-alugueis.py` | "Agora é com você" da 1.3–1.5 | exercício no Colab |
| Lote de commits/casos de teste | inline | 2.4, 2.6 | tradução de "lote de peças" do Bussab para software |

## Armadilhas de código ↔ teoria (verificadas)

| Armadilha | Impacto | Correção |
|---|---|---|
| Quantil do Bussab (3.20) usa $p_i = (i - 0{,}5)/n$ com interpolação linear = `numpy.quantile(method="hazen")`; o padrão do pandas é `linear` (tipo 7) | Ex. 3.5 do Bussab: hazen dá $q_1 = 4{,}5$, $q_3 = 11{,}25$; pandas dá $5$ e $11$ | Se o texto disser "segue (3.20)", o código tem de usar `hazen`; se usar o padrão, o texto deve dizer que é outra convenção |
| Variância na seção 3.2 do Bussab divide por $n$; pandas divide por $n-1$ | $\{3,5,5,7\}$: Bussab/`np.var` = 2; pandas = 2,667 | Citar o Bussab para a definição **e** o divisor usado |
| `scipy.stats.hypergeom(M, n, N)` ≠ $\mathrm{hip}(N, r, n)$ | letras colidem trocadas | mapear no comentário do chunk (a 2.6 já faz) |
| `scipy.stats.norm(loc, scale)` recebe $\sigma$, Bussab escreve $\sigma^2$ | $N(0, 4)$ vira `norm(0, 2)` | nunca passar a variância em `scale` |
| pandas 3: texto é `str`, não `object`; indexação de Series categóricas mudou | comparações erradas **sem exceção** (ver CLAUDE.md) | testar o resultado, não só a ausência de erro |

## Anti-padrões já vividos

| Anti-padrão | O que aconteceu | Correção |
|---|---|---|
| Citar a curtose como "vista no Cap. 1" | foi cortada em 2.2026 | a curtose não existe mais no livro |
| Corrigir `@bussab2023` para 2017 | invalidaria todas as citações | numeração das seções bate; manter 2023 |
| Gabarito em `.spoiler` | o HTML publicado expõe tudo | gabarito só em `avaliacoes/` (gitignorado) |
