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
| União, interseção, complementar | $A \cup B$ (Bussab: *reunião*), $A \cap B$, $A^c$, $\varnothing$ | `A | B`, `A & B`, `todos - A` em `set` | $\bar{A}$ ou $A'$ para complementar |
| Espaço amostral, ponto, evento | $\Omega$, $\omega$; evento $A \subseteq \Omega$ (não $\subset$) | $P(A) = \sum_{\omega \in A} P(\omega)$ no caso discreto | $S$ para espaço amostral |
| Ponto amostral em fórmula | parênteses duplos quando o ponto é um par | $P\big((C, C)\big)$ | $P(C, C)$, que parece conjunta |
| Condicional | $P(A \mid B) = P(A \cap B)/P(B)$, $P(B) > 0$ | — | $P(A/B)$ |
| Combinação | $\binom{n}{k}$ | `math.comb(n, k)` | $C_n^k$ sem definir |
| Binomial | $X \sim b(n, p)$; $P(X=k) = b(k; n, p)$ | — | $\mathrm{Bin}$ misturado com $b$ |
| Hipergeométrica | $X \sim \mathrm{hip}(N, r, n)$: população $N$, $r$ sucessos, amostra $n$ | — | letras da scipy no texto |
| Normal | $X \sim N(\mu, \sigma^2)$ — **variância** no 2º argumento | $Z \sim N(0, 1)$ | $N(\mu, \sigma)$ |
| Bernoulli, Poisson, uniforme, exponencial | $\mathrm{Ber}(p)$, $\mathrm{Pois}(\lambda)$, $u(\alpha, \beta)$, $\mathrm{Exp}(\beta)$ com $\beta$ = **média** (Bussab 7.4.3) | $X \sim \mathrm{Pois}(3)$ | $\mathrm{Exp}(\lambda)$ com taxa sem avisar |
| Binomial com parâmetros numéricos | $b(n, p)$ com vírgula e $p$ em fração, para não colidir com a vírgula decimal nem com a pmf $b(k; n, p)$ | $b(10, 1/10)$ | $b(10; 0{,}1)$ |
| Variável aleatória | $X$ em todas as seções de um capítulo (não reusar $N$, que é população na hipergeométrica) | $X \sim \mathrm{Pois}(\lambda)$ | $N \sim \mathrm{Pois}$ |
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
| 2.2 | Como combinar eventos? | $A \cup B$, $A \cap B$, $A^c$, $\varnothing$ | Bussab 5.2 (1ª metade) |
| 2.3 | Como contar sem listar? | $m/n$, $n!$, $\binom{n}{k}$; permutação sem símbolo próprio ($P(n,k)$ colide com probabilidade) | Bussab 5.2 (2ª metade) |
| 2.4–2.5 | Condicional e independência; Bayes | $P(A \mid B)$, partição | Bussab 5.3–5.4 |
| Cap. 3 | V.a. discretas: $E$, Var, FDA; uniforme, Bernoulli, binomial, hipergeométrica; Poisson (3.7, complementar) | $b(n,p)$, $\mathrm{hip}(N,r,n)$ | Bussab 6.1–6.3 (+ (6.4) e (6.5) da 6.4), 6.5, 6.6.1–6.6.4 |
| Cap. 4 | V.a. contínuas: densidade, $E$, Var ((7.8) incluída), FDA, inversa da FDA; uniforme, normal; exponencial (4.6, complementar) | $N(\mu,\sigma^2)$, $\Phi$, $u(\alpha,\beta)$ | Bussab 7.1–7.4.3 |

Escopo completo, por aula, no `CLAUDE.md`. Um capítulo do livro por capítulo do Bussab: Cap. 2 = Bussab 5, Cap. 3 = Bussab 6, Cap. 4 = Bussab 7. Remissões "no Capítulo 3/4" dentro do Cap. 2 estão corretas.

## Aplicações recorrentes

| Aplicação | Dataset | Seções | Para quê |
|---|---|---|---|
| Estados brasileiros | `dados/estados.csv` (n = 27) | 1.3–1.5 | mediana é observação real; SP é o outlier; média ponderada < simples |
| Aluguéis (BR) | gerado por `scripts/gerar-dados-alugueis.py` | "Agora é com você" da 1.3–1.5 | exercício no Colab |
| Estados brasileiros (sorteio) | `dados/estados.csv` | 2.1, 2.2 (A grande × B taxa acima da mediana: interseção = BA, união = 18) | $P$ equiprovável = frequência relativa; 13/27 acima da mediana; sortear UF × sortear pessoa (22,2% × 57,6%) |
| Builds de CI (passa/falha) | inline | 2.1, Cap. 3 | tradução do "bom/defeituoso" do Bussab 5.1 (Ex. 5.4) para software; vira binomial no Cap. 3 |
| PINs, suíte de testes, auditoria de PRs, Mega-Sena | inline | 2.3 | princípio multiplicativo; permutação × combinação; Ex. 5.8 (20 PRs, 5 com bug, 4 sorteados); Ex. 5.9 com preços da Caixa de 18/09/2026 (R\$ 6,00 a aposta simples, 6 a 20 números) |
| Lote de commits/casos de teste | inline | contagem, hipergeométrica | tradução de "lote de peças" do Bussab para software |

## Armadilhas de código ↔ teoria (verificadas)

| Armadilha | Impacto | Correção |
|---|---|---|
| Quantil do Bussab (3.20) usa $p_i = (i - 0{,}5)/n$ com interpolação linear = `numpy.quantile(method="hazen")`; o padrão do pandas é `linear` (tipo 7) | Ex. 3.5 do Bussab: hazen dá $q_1 = 4{,}5$, $q_3 = 11{,}25$; pandas dá $5$ e $11$ | Se o texto disser "segue (3.20)", o código tem de usar `hazen`; se usar o padrão, o texto deve dizer que é outra convenção |
| Variância na seção 3.2 do Bussab divide por $n$; pandas divide por $n-1$ | $\{3,5,5,7\}$: Bussab/`np.var` = 2; pandas = 2,667 | Citar o Bussab para a definição **e** o divisor usado |
| `scipy.stats.hypergeom(M, n, N)` × $\mathrm{hip}(N, r, n)$ | a ordem posicional coincide (população, sucessos, amostra), mas a letra $N$ é população no Bussab e amostra na scipy; `hypergeom(N=20, n=4, M=5)` com as letras do livro devolve `nan` sem erro. Trocar $r$ e $n$ dá a mesma distribuição (simetria), então esse erro nem aparece | usar os nomes da scipy (`M=`, `n=`, `N=`) com comentário da correspondência (a 3.6 faz) |
| `scipy.stats.norm(loc, scale)` recebe $\sigma$, Bussab escreve $\sigma^2$ | $N(0, 4)$ vira `norm(0, 2)` | nunca passar a variância em `scale` |
| `scipy.stats.uniform(loc, scale)`: `scale` é a **largura** | `uniform(10, 70)` é $u(10, 80)$ | `uniform(loc=α, scale=β-α)` |
| `scipy.stats.randint(a, b)` exclui `b` (ao contrário de `random.randint`) | `randint(1, 6)` é um dado de 5 faces; `pmf(6)` dá 0 sem aviso | `randint(1, 7)` |
| `scipy.stats.expon(scale=β)`: `scale` é a média; muitos textos usam a taxa | passar a taxa em `scale` troca média por taxa | `expon(scale=1/taxa)` |
| Saída de numpy 2 com `np.float64(...)` | poluição nas tuplas de saída | `np.set_printoptions(legacy="1.25")` no setup de cada seção e no notebook |
| Graphviz `{dot}` no modo escuro | texto e setas pretos sobre fundo escuro; SVG com 672 px inline | `bgcolor="transparent"` no dot; o `styles.css` tem `.quarto-dark svg g.graph` e `max-width: 100% !important` |
| Tabela de Resumo com fórmulas | estoura a página no celular | `::: {.table-responsive}` em volta (padrão nos Caps. 2–4) |
| `set` de strings em Python sai em ordem diferente a cada processo (hash aleatório) | a saída do chunk muda a cada render e o `freeze` perde o sentido | exibir com `sorted(...)` |
| Número de `{python} num(...)` dentro de `$...$` | a vírgula decimal vira `\,` (aparece como espaço); o ponto de milhar vira `\.` e a **barra aparece na tela** (`10 \. 000`); trocar por `{,}` também falha (o Quarto escapa as chaves) | **nenhum** `num(...)` com vírgula ou ponto dentro de `$...$`: fórmula com símbolos, número na prosa ("…$\binom{20}{4}$, ou 4.845"); inteiros abaixo de 1.000 podem ficar dentro |
| Tupla com resultado do numpy 2 na saída de um chunk | aparece `np.float64(0.217)` em vez de `0.217` | converter com `float(...)` antes de exibir |
| Probabilidades calculadas por dois caminhos comparadas com `==` | `sum([1/27]*21)` e `1 - 6/27` diferem na 16ª casa; `==` dá `False` | `math.isclose`; perto de zero, `abs_tol=1e-12` |
| Largura no celular (390 px, coluna de 339 px) | display com `\qquad`, inline longo, tabela com fórmula e até o ponto final de uma equação dentro de `.conceito` estouram a página | `aligned` em duas linhas; quebrar o inline; tabela dentro de `::: {.table-responsive}`; medir `scrollWidth` com Playwright |
| pandas 3: texto é `str`, não `object`; indexação de Series categóricas mudou | comparações erradas **sem exceção** (ver CLAUDE.md) | testar o resultado, não só a ausência de erro |

## Anti-padrões já vividos

| Anti-padrão | O que aconteceu | Correção |
|---|---|---|
| Citar a curtose como "vista no Cap. 1" | foi cortada em 2.2026 | a curtose não existe mais no livro |
| Corrigir `@bussab2023` para 2017 | invalidaria todas as citações | numeração das seções bate; manter 2023 |
| Resposta dependente de fato físico não dito no enunciado (relógio "elétrico" = contínuo, na 2.1) | o relógio de quartzo anda aos saltos; quem respondesse "discreto" estaria certo | a hipótese vai no enunciado, como faz o Bussab |
| Gabarito em `.spoiler` | o HTML publicado expõe tudo | gabarito só em `avaliacoes/` (gitignorado) |
