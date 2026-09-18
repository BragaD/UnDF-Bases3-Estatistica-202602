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
| Espaço amostral, ponto, evento | $\Omega$, $\omega$; evento $A \subseteq \Omega$ (não $\subset$) | $P(A) = \sum_{\omega \in A} P(\omega)$ no caso discreto | $S$ para espaço amostral |
| Ponto amostral em fórmula | parênteses duplos quando o ponto é um par | $P\big((C, C)\big)$ | $P(C, C)$, que parece conjunta |
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
| 2.1 | O que é um modelo probabilístico? | $\Omega$, $\omega$, $A \subseteq \Omega$, $P(A)$ | Bussab 5.1 |
| 2.2–2.5 | Propriedades e contagem; condicional; Bayes (a escrever) | $A \cup B$, $A \cap B$, $A^c$, $\binom{n}{k}$, $P(A \mid B)$ | Bussab 5.2–5.4 |
| Cap. 3 | V.a. discretas: $E$, Var, FDA; uniforme, Bernoulli, binomial, hipergeométrica (a escrever) | $b(n,p)$, $\mathrm{hip}(N,r,n)$ | Bussab 6.1–6.3, 6.5, 6.6.1–6.6.4 |
| Cap. 4 | V.a. contínuas: densidade, $E$, Var, FDA; uniforme, normal (a escrever) | $N(\mu,\sigma^2)$ | Bussab 7.1–7.4.2 |

Escopo completo, por aula, no `CLAUDE.md`. Um capítulo do livro por capítulo do Bussab: Cap. 2 = Bussab 5, Cap. 3 = Bussab 6, Cap. 4 = Bussab 7. Remissões "no Capítulo 3/4" dentro do Cap. 2 estão corretas.

## Aplicações recorrentes

| Aplicação | Dataset | Seções | Para quê |
|---|---|---|---|
| Estados brasileiros | `dados/estados.csv` (n = 27) | 1.3–1.5 | mediana é observação real; SP é o outlier; média ponderada < simples |
| Aluguéis (BR) | gerado por `scripts/gerar-dados-alugueis.py` | "Agora é com você" da 1.3–1.5 | exercício no Colab |
| Estados brasileiros (sorteio) | `dados/estados.csv` | 2.1 | $P$ equiprovável = frequência relativa; 13/27 acima da mediana; sortear UF × sortear pessoa (22,2% × 57,6%) |
| Builds de CI (passa/falha) | inline | 2.1, Cap. 3 | tradução do "bom/defeituoso" do Bussab 5.1 (Ex. 5.4) para software; vira binomial no Cap. 3 |
| Lote de commits/casos de teste | inline | contagem, hipergeométrica | tradução de "lote de peças" do Bussab para software |

## Armadilhas de código ↔ teoria (verificadas)

| Armadilha | Impacto | Correção |
|---|---|---|
| Quantil do Bussab (3.20) usa $p_i = (i - 0{,}5)/n$ com interpolação linear = `numpy.quantile(method="hazen")`; o padrão do pandas é `linear` (tipo 7) | Ex. 3.5 do Bussab: hazen dá $q_1 = 4{,}5$, $q_3 = 11{,}25$; pandas dá $5$ e $11$ | Se o texto disser "segue (3.20)", o código tem de usar `hazen`; se usar o padrão, o texto deve dizer que é outra convenção |
| Variância na seção 3.2 do Bussab divide por $n$; pandas divide por $n-1$ | $\{3,5,5,7\}$: Bussab/`np.var` = 2; pandas = 2,667 | Citar o Bussab para a definição **e** o divisor usado |
| `scipy.stats.hypergeom(M, n, N)` ≠ $\mathrm{hip}(N, r, n)$ | letras colidem trocadas | mapear no comentário do chunk (a 2.6 já faz) |
| `scipy.stats.norm(loc, scale)` recebe $\sigma$, Bussab escreve $\sigma^2$ | $N(0, 4)$ vira `norm(0, 2)` | nunca passar a variância em `scale` |
| `set` de strings em Python sai em ordem diferente a cada processo (hash aleatório) | a saída do chunk muda a cada render e o `freeze` perde o sentido | exibir com `sorted(...)` |
| Número de `{python} num(...)` dentro de `$...$` | a vírgula decimal vira `\,` no MathJax e aparece como espaço | deixar o número fora do `$...$` |
| pandas 3: texto é `str`, não `object`; indexação de Series categóricas mudou | comparações erradas **sem exceção** (ver CLAUDE.md) | testar o resultado, não só a ausência de erro |

## Anti-padrões já vividos

| Anti-padrão | O que aconteceu | Correção |
|---|---|---|
| Citar a curtose como "vista no Cap. 1" | foi cortada em 2.2026 | a curtose não existe mais no livro |
| Corrigir `@bussab2023` para 2017 | invalidaria todas as citações | numeração das seções bate; manter 2023 |
| Resposta dependente de fato físico não dito no enunciado (relógio "elétrico" = contínuo, na 2.1) | o relógio de quartzo anda aos saltos; quem respondesse "discreto" estaria certo | a hipótese vai no enunciado, como faz o Bussab |
| Gabarito em `.spoiler` | o HTML publicado expõe tudo | gabarito só em `avaliacoes/` (gitignorado) |
