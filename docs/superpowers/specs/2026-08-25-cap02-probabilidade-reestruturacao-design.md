# Reestruturação da Parte de Probabilidade do Cap. 2

**Data:** 2026-08-25
**Status:** Aprovado (design)

## Objetivo

Reestruturar a parte de probabilidade e distribuições do Capítulo 2: **remover** as distribuições t de Student, qui-quadrado, F e Poisson; **adicionar** probabilidade condicional e Teorema de Bayes, e a distribuição hipergeométrica, com uma seção curta de contagem (permutação e combinação) antes das distribuições. A seção de cauda longa é **mantida**, desacoplada da distribuição t.

## Decisões (do brainstorming + pesquisa online)

- **Remover:** Poisson, t de Student, qui-quadrado, F (integralmente — não migram para outro capítulo; o Cap. 4 já foi reduzido e não usa esses testes, e o Cap. 3 constrói IC por bootstrap).
- **Adicionar:** (2.3) Probabilidade condicional e Teorema de Bayes; (2.4) Contagem: permutação e combinação — **seção própria curta**; (2.6) Distribuição hipergeométrica.
- **Cauda longa:** **mantida**, desacoplada da t (usa a amostra de cauda gorda como ilustração, sem apontar para uma seção t).
- **Pesquisa online (subagentes):** concluída. Achado central: **Bussab & Morettin** (já bibliografia básica, `@bussab2023`) tem todo esse conteúdo em português, com os exemplos canônicos — é a fonte primária das seções novas.

## Nova estrutura (8 seções)

| # | Seção | Arquivo | Origem |
|---|---|---|---|
| 2.1 | O que é probabilidade | `01-o-que-e-probabilidade.qmd` | existente |
| 2.2 | Regras de probabilidade | `02-regras-probabilidade.qmd` | existente |
| 2.3 | Probabilidade condicional e Teorema de Bayes | `03-probabilidade-condicional-bayes.qmd` | **nova** |
| 2.4 | Contagem: permutação e combinação | `04-contagem-permutacao-combinacao.qmd` | **nova** |
| 2.5 | Distribuição binomial | `05-distribuicao-binomial.qmd` | existente (era 2.3) |
| 2.6 | Distribuição hipergeométrica | `06-distribuicao-hipergeometrica.qmd` | **nova** |
| 2.7 | Distribuição normal | `07-distribuicao-normal.qmd` | existente (era 2.5) |
| 2.8 | Distribuições de cauda longa | `08-caudas-longas.qmd` | existente (era 2.6) |

**Ordem lógica:** fundamentos (2.1→2.3, com Bayes estendendo a regra da multiplicação) → contagem (2.4, base da binomial e da hipergeométrica) → distribuições (2.5–2.8, discretas antes das contínuas).

## Mapa de arquivos (git, nesta ordem)

```
# 1. remover as 4 distribuições
git rm content/cap02/04-poisson.qmd content/cap02/07-distribuicao-t.qmd \
       content/cap02/08-qui-quadrado.qmd content/cap02/09-distribuicao-f.qmd
# 2. renumerar as reaproveitadas (08 e 07 livres; depois 05)
git mv content/cap02/06-caudas-longas.qmd     content/cap02/08-caudas-longas.qmd
git mv content/cap02/05-distribuicao-normal.qmd content/cap02/07-distribuicao-normal.qmd
git mv content/cap02/03-distribuicao-binomial.qmd content/cap02/05-distribuicao-binomial.qmd
# 3. criar as novas
#   content/cap02/03-probabilidade-condicional-bayes.qmd
#   content/cap02/04-contagem-permutacao-combinacao.qmd
#   content/cap02/06-distribuicao-hipergeometrica.qmd
```

Os callouts `de @bruce2020` das seções reaproveitadas **permanecem** (Bruce: binomial 2.9, normal 2.6, caudas 2.7 — números do Bruce, inalterados). As seções novas citam **@bussab2023** (Bruce não cobre condicional/Bayes, contagem nem hipergeométrica).

## Conteúdo das seções novas (números verificados no container)

### 2.3 — Probabilidade condicional e Teorema de Bayes

Arco (todo com callout `.conceito`/`.exemplo`, formato `num`, sementes `default_rng(42)`):
1. **Probabilidade condicional:** $P(A\mid B) = P(A\cap B)/P(B)$, motivada retomando a regra da multiplicação da 2.2 (que já era $P(A\cap B)=P(B)P(A\mid B)$ sem o nome). Distinguir **prior** $P(A)$ de **posterior** $P(A\mid B)$.
2. **Independência revisitada:** $P(A\mid B)=P(A)$; reforça (não contradiz) o callout existente da 2.2 sobre independência ≠ exclusividade mútua.
3. **Regra da probabilidade total:** partição $\{C_1,\dots,C_n\}$, $P(B)=\sum_i P(C_i)P(B\mid C_i)$ (diagrama de árvore).
4. **Teorema de Bayes:** forma de dois eventos e forma geral. Enquadramento: Bayes **inverte** uma condicional fácil ($P(\text{evidência}\mid\text{hipótese})$) na difícil ($P(\text{hipótese}\mid\text{evidência})$).
5. **Armadilha da taxa-base** como fechamento.

Exemplo-âncora (registro de software — detecção de anomalia/intrusão), números verificados:
- prevalência 1% (0,01), sensibilidade 80% (0,80), taxa de falso-positivo 9,6% (0,096) → **posterior P(evento | alarme) = 0,0776 ≈ 7,8%** (contra a intuição de ~80%).
- Segundo exemplo, em português e citável: Bussab Exemplo 5.15 — 25% bons, 50% médios, 25% fracos; P(aprovado|bom/médio/fraco)=0,80/0,50/0,20 → **P(fraco | aprovado) = 0,10**.

Python (sem scipy): (a) **cálculo direto da fórmula** (prior → verossimilhança → evidência → posterior, ex. com dict); (b) **simulação Monte Carlo** (frequências naturais) como segunda prova, com semente. **Monty Hall** como exercício com simulação (trocar dobra de 1/3 para 2/3).

Links complementares (callout): 3Blue1Brown (geometria de Bayes), Seeing Theory (widget interativo de teste médico) — apenas como links, não recriar em OJS.

Armadilhas a evitar (embutir na prosa): confundir $P(A\mid B)$ com $P(B\mid A)$; negligenciar a taxa-base; hipóteses precisam ser partição (exclusivas e exaustivas); prior é escolha, não fato.

### 2.4 — Contagem: permutação e combinação (curta)

Dose mínima (a mesma que Bussab e OpenStax usam):
1. **Princípio multiplicativo** — um parágrafo, exemplo trivial.
2. **Permutação** $P(n,k)=\dfrac{n!}{(n-k)!}$ — arranjos **ordenados** (pódio, senha). Verificado: $P(5,3)=60$, $5!=120$.
3. **Combinação** $\binom{n}{k}=\dfrac{n!}{k!\,(n-k)!}$ — subconjuntos **sem ordem** (amostra, comitê, lote). Regra prática: *"a ordem importa?"*. Verificado: $\binom{20}{4}=4845$.
4. Parar aí — **nada** de arranjo com repetição, permutação circular, anagramas.

Exemplo-ponte (Bussab 5.8): lote de 20 com 5 defeituosas, amostra de 4 → $\binom{5}{2}\binom{15}{2}/\binom{20}{4} = $ **0,217** (já é um proto-exercício de hipergeométrica). Python: `math.comb`, `math.perm`, `math.factorial`.

### 2.6 — Distribuição hipergeométrica

- **Motivação:** amostragem **sem reposição** de população finita; cada retirada muda a composição, então $p$ varia (tentativas dependentes) — o contraste direto com a binomial (com reposição).
- **Fórmula:** população $N$, $r$ com o atributo, amostra $n$ sem reposição; $P(X=k)=\dfrac{\binom{r}{k}\binom{N-r}{n-k}}{\binom{N}{n}}$, com $\max(0,n-N+r)\le k\le\min(r,n)$. Notação $X\sim\text{hip}(N,r,n)$.
- **Exemplo (controle de qualidade → software):** lote $N=100$, $r=10$ defeituosas, amostra $n=5$. Verificado: **P(0 defeituosas) = 0,584**, **P(≥1) = 0,416**. Transposição: amostrar casos de teste num release / bugs num backlog.
- **scipy.stats.hypergeom** com **nota de nomenclatura obrigatória**: `hypergeom(M, n, N)` do scipy = `(população, sucessos_na_população, tamanho_amostra)` — o `n` do scipy é o $r$ do livro, o `N` do scipy é o $n$. Comentário no primeiro chunk mapeando as letras.
- **Hipergeométrica × binomial + regra dos 10%:** com $n/N=5\%$, binomial $0{,}9^5=$ **0,590** ≈ hipergeométrica **0,584** (diferença ~1%). Segundo caso com $n/N$ grande (ex. `hypergeom(20,7,12)`, 60%) onde a binomial falharia — contraste pedagógico.
- **Suporte restrito de $k$:** avisar que `pmf` fora do suporte devolve 0 em silêncio (mesma classe de falha silenciosa da política de sementes/limites do projeto).
- **Gancho para o Cap. 3:** o fator de correção de população finita $\frac{N-n}{N-1}$ na variância — amostrar sem reposição de população pequena reduz variância.

### 2.8 — Cauda longa (desacoplar da t)

Manter o conceito (cauda gorda, curtose — já introduzida no Cap. 1). Trocar as remissões: a amostra `stats.t.rvs(df=3, ...)` pode continuar como **ilustração de cauda gorda**, mas a prosa **não** deve chamá-la de "distribuição t, o assunto da próxima seção" (não há seção t). Reescrever a abertura/fecho para não depender da t. O chunk que gera a amostra pode permanecer (é só uma amostra de cauda pesada) ou ser trocado por outra fonte de cauda gorda — decisão do plano, desde que a prosa não prometa uma seção t.

## Referências cruzadas a corrigir

- `cap02/01-o-que-e-probabilidade.qmd` (~linha 7): a enumeração das distribuições do capítulo cita Poisson e t — trocar pela nova lista (binomial, hipergeométrica, normal, cauda longa) e mencionar probabilidade condicional/Bayes.
- `cap02/07-distribuicao-normal.qmd` (abertura, ~linha 20): "Depois das duas distribuições discretas (binomial e Poisson)…" → "(binomial e hipergeométrica)".
- `cap02/08-caudas-longas.qmd`: remissão "seção 2.6" (normal) → **2.7**; desacoplar da t (ver 2.8 acima). Callout linha 4 (Bruce 2.7) permanece.
- `cap03/index.qmd` (~linha 9): "As últimas distribuições do Capítulo 2 — qui-quadrado e F — apontaram para os testes…" → reescrever sem citar qui²/F.
- `cap02/index.qmd`: reescrever por completo — prosa de visão geral, objetivos e tabela de seções (as 8 novas).
- `index.qmd`: bullet de "Sobre a Disciplina" (probabilidade e distribuições: trocar a lista) e as linhas do **cronograma** que citam Poisson/t/qui²/F.

## Mudanças mecânicas

- `_quarto.yml`: reescrever a lista de seções do Cap. 2.
- **Cronograma** (index.qmd) e **PID** (`docs/PID …xlsx`): re-mapear o conteúdo das aulas do Cap. 2 (sugestão: aula 6 = probabilidade · regras · condicional e Bayes; aula 7 = contagem · binomial · hipergeométrica; aula 8 = normal · cauda longa · revisão).
- **Notebook `notebooks/capitulo-02.ipynb`:** regenerar (novas seções entram no código; as removidas saem) — com o conversor já existente + as explicações autorais das células novas (subagente, como nos outros).
- **CLAUDE.md:** atualizar a nota de estrutura/escopo do Cap. 2 (lista de distribuições muda; a nota "Escopo reduzido" que menciona remissões de qui²/F precisa ser revista).

## Atribuição

- Seções novas (2.3, 2.4, 2.6): callout de abertura citando **@bussab2023** (e, onde couber, links complementares em nota — 3Blue1Brown, Seeing Theory, Think Bayes, scipy docs — sem virar bibliografia formal).
- Seções reaproveitadas (binomial, normal, cauda longa): callouts `@bruce2020` inalterados.

## Fontes (da pesquisa online)

- Bussab & Morettin, *Estatística Básica* — §5.2 (contagem), §5.3–5.4 (condicional/Bayes), §6.6.4 (hipergeométrica). Fonte primária, em PT-BR, já `@bussab2023`.
- OpenStax *Introductory Statistics 2e* §4.5 (hipergeométrica, CC BY): <https://openstax.org/books/introductory-statistics-2e/pages/4-5-hypergeometric-distribution>
- scipy `hypergeom`: <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html>
- Penn State STAT 414 (captura-recaptura); OnlineStatBook (cartas).
- 3Blue1Brown Bayes: <https://www.3blue1brown.com/lessons/bayes-theorem/>; Seeing Theory: <https://seeing-theory.brown.edu/bayesian-inference/index.html>; Think Bayes (Downey): <https://allendowney.github.io/ThinkBayes2/>; OpenIntro (heurística árvore-vs-fórmula).

## Verificação

- `make render` verde após a reestruturação.
- Nenhuma referência de prosa a Poisson / t / qui-quadrado / F fora de contexto histórico; `grep` de integridade (nenhuma remissão a seções inexistentes).
- Números novos no HTML: Bayes **7,8%** (0,0776); hipergeométrica **0,584** e **0,416**; binomial-aprox **0,590**; Bussab 5.15 **0,10**; combinatória ($\binom{20}{4}=4845$, $P(5,3)=60$).
- Sementes: todo chunk com RNG (Monte Carlo do Bayes, Monty Hall, amostra de cauda gorda) usa `default_rng(42)`.
- Cada seção nova com **exercícios** em `callout-tip collapse`.
- Notebook do Cap. 2 reexecuta sem erro (`nbconvert`).
- `_quarto.yml`, cronograma, PID e CLAUDE.md consistentes com as 8 seções.

## Fora de escopo

- Inferência bayesiana como método (prior contínuo, Beta-Binomial, MCMC) — só a regra de atualização discreta.
- Análise combinatória além de $P(n,k)$ e $\binom{n}{k}$.
- Reescrever binomial, normal e cauda longa além do necessário para os cross-refs e a desacoplagem da t.
- Recriar os widgets interativos (3Blue1Brown/Seeing Theory ficam como links).
- Capítulos 4 e 5 (stubs).
