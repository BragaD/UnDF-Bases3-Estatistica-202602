# Lista 1 (Prova 1) — Design

**Data:** 2026-08-28
**Autor:** Douglas Braga (com Claude Code)
**Status:** Design aprovado em brainstorming; aguardando revisão do spec.

## 1. Contexto e objetivo

A **Lista 1** é o instrumento avaliativo de estudo dirigido para a **Prova 1** (aula 9, 16/10/2026). Vale **15%** da nota e é **entregue até a data da prova**. A lista cobre os dois capítulos de conteúdo técnico:

- **Capítulo 1 — Análise Exploratória de Dados** (8 seções)
- **Capítulo 2 — Probabilidade e Distribuições** (8 seções)

A **Introdução** (motivacional — *Por que Estatística?*, *Paradoxo de Simpson*) entra na Prova 1 como leitura, mas **fica fora da lista**: é conceitual e não rende bom exercício manuscrito avaliável.

São **30 questões, 0,5 ponto cada** — total **15 pontos**, correspondendo aos 15% da nota. A lista funciona como estudo dirigido: resolvê-la *é* preparar-se para a prova, não uma tarefa empilhada sobre ela.

## 2. Decisões de design (fixadas no brainstorming)

| Eixo | Decisão |
|---|---|
| Formato de saída | **PDF** — folha do aluno **publicada no site e linkada no livro**; gabarito à parte |
| Motor | Quarto → **typst** (PDF sem LaTeX); gabarito é `.qmd` executável |
| Gabarito | Fica **no repositório** (público), mas **não linkado no livro** nem servido pelo site |
| Cobertura | **Capítulos 1 e 2** (Introdução fica fora) |
| Densidade | **30 questões**, ponderadas por peso do tema (15 do Cap. 1 + 15 do Cap. 2) |
| Pontuação | **0,5 ponto por questão** (uniforme) → 30 × 0,5 = **15 pontos = 15%** |
| Escopo dos exercícios | **Integrativos**: um exercício pode abranger várias seções |
| Entrega do aluno | **Manuscrita** — Python permitido como ferramenta, resposta escrita à mão |

## 3. Restrição manuscrita e suas consequências

O aluno resolve **à mão** e pode usar Python (no Colab) apenas para *chegar* ao número. O que se corrige é o manuscrito. Isso molda cada exercício:

1. **Dados pequenos e auto-contidos.** O enunciado traz os dados na própria folha (uma tabela de 6–10 valores, uma tabela de contingência 2×2 ou 2×3), computáveis à mão ou com o Python como calculadora. Evita-se "carregue um CSV de 50 mil linhas e cole a saída" — não sobra nada para escrever, e não dá para conferir o trabalho.
2. **Nenhum exercício do tipo "rode e reporte".** Mesmo quando o Python ajuda, a questão pede **valor + raciocínio/interpretação**. O grau é dado pelo caminho, não só pelo número final.
3. **Fechadas** pedem a **letra escolhida + uma justificativa curta** manuscrita (elimina o chute e revela o raciocínio).
4. **Abertas** pedem a **resolução completa** — fórmula, substituição, número, interpretação.
5. **Aritmética tratável.** Números escolhidos para fechar em contas de mão razoáveis; o Python é conferência, não muleta obrigatória.

## 4. Formato e cadeia de ferramentas

### Localização no repositório

Um projeto Quarto isolado em `avaliacoes/`, **separado do livro**:

```
avaliacoes/
├── _quarto.yml          # projeto próprio (type: default, format: typst); perfil padrão = lista
├── _quarto-gabarito.yml # perfil "gabarito" (só muda output-file e ativa as soluções)
├── lista-1.qmd          # FONTE ÚNICA: enunciados + soluções gated por profile
└── _extensions/         # (se necessário) template typst do cabeçalho
```

- **Não** é registrado no `_quarto.yml` do livro → nunca aparece no site nem no sidebar.
- `avaliacoes/_quarto.yml` usa `project: type: default` e `format: typst`, com `execute-dir: project` (cwd = `avaliacoes/`).
- **Caminhos de dados:** quando um exercício referenciar um dataset do livro, o caminho é `../dados/arquivo.csv` (a partir de `avaliacoes/`). A maioria dos exercícios é auto-contida e não carrega dataset.
- **Formatação numérica pt-BR:** reusa `from formato import num` — como `formato.py` está na raiz do repo e o cwd é `avaliacoes/`, o chunk de setup importa via `import sys; sys.path.insert(0, "..")`, sem duplicar o arquivo.

### Fonte única, dois PDFs (crítico para evitar divergência)

Enunciado e gabarito **não** são dois arquivos digitados em paralelo — isso convida a divergência (um número corrigido num, esquecido no outro). Há **um** arquivo, `lista-1.qmd`, e a solução de cada exercício vive num bloco condicionado ao **profile** do Quarto:

```markdown
**12.** [enunciado, dados na folha…]

::: {.content-visible when-profile="gabarito"}
### Resolução
[resolução manuscrita esperada + chunk Python que calcula o número]
:::
```

- **Perfil padrão (lista):** as soluções são omitidas → PDF do aluno.
- **Perfil `gabarito`:** as soluções aparecem → PDF do professor.

**Risco a validar na Fase 0:** `content-visible` esconde na saída, mas é preciso garantir que, no perfil "lista", o conteúdo da solução (inclusive o número calculado) **não vaza** para o PDF do aluno. A Fase 0 renderiza os dois perfis de um exercício-piloto e **confere no PDF do aluno que a resposta não está lá** (grep no texto extraído do PDF). Se o `content-visible` não isolar de forma confiável, o fallback é fragmentar em includes (`NN-enunciado.qmd` incluído nos dois; `NN-solucao.qmd` incluído só no gabarito) — mas o profile é a primeira opção por manter tudo num arquivo.

### Renderização

```bash
# dentro do container (serviço livro), a partir da raiz:
quarto render avaliacoes/lista-1.qmd                     # → avaliacoes/lista-1.pdf (aluno)
quarto render avaliacoes/lista-1.qmd --profile gabarito  # → avaliacoes/lista-1-gabarito.pdf (professor)
```

Alternativa registrada: **docx** via pandoc, caso se queira editar no Word. Recomendação mantida em **PDF** (integridade — aluno não altera; matemática limpa via typst).

## 5. Privacidade e versionamento

O repositório é PÚBLICO (`BragaD/UnDF-Bases3-Estatistica-202602`). A lista é **estudo guiado**: as respostas **podem ser públicas** — a nota premia a entrega manuscrita e o percurso, não o sigilo do gabarito. O que muda entre os dois artefatos é a **superfície de publicação**, não o segredo:

- **Folha do aluno** (`downloads/lista-1-prova-1.pdf`) — só os enunciados, para imprimir, resolver à mão e entregar. É declarada em `project.resources` do `_quarto.yml`, **servida pelo livro** no GitHub Pages e **linkada** no `index.qmd` (cronograma na aula 9; tabela de avaliação).
- **Gabarito** (`downloads/lista-1-prova-1-gabarito.pdf`) — resoluções + matriz de cobertura. Fica **commitado no repositório** (acessível via GitHub), mas **não** entra em `project.resources` e **não** é linkado no livro: não vira parte do site publicado nem é apresentado ao aluno pela navegação do livro. Serve de referência do professor e para quem for atrás dele no repo.

A distinção folha/gabarito é gerada pelo mesmo mecanismo de profile do Quarto (§4): render sem perfil → folha; `--profile gabarito` → gabarito.

- **Fonte fica local por conveniência:** `avaliacoes/lista-1.qmd` (e o freeze) permanece no **`.gitignore`** — o fonte único com blocos gated não é uma página do livro; o que se versiona são os dois PDFs renderizados. Manter o fonte fora do `_quarto.yml` evita que ele vire capítulo no sidebar.
- **Consequência para a execução:** a autoria **não** usa o fluxo SDD de "commit por tarefa"; usa dispatch de subagentes por bloco, conteúdo vivo na árvore de trabalho, verificado por render. O que é commitado: `.gitignore`, este spec + o plano, o `_quarto.yml`, o `index.qmd` e os **dois** PDFs em `downloads/` (só a folha do aluno é recurso do site; o gabarito só mora no repo).
- **Custo aceito:** os PDFs são artefatos gerados que precisam ser **re-renderizados e re-commitados** quando a lista muda (o fonte local é a fonte da verdade).

## 6. Estrutura da lista

Organizada em **dois blocos**, na ordem dos capítulos:

1. **Bloco 1 — Análise Exploratória de Dados** (15 questões)
2. **Bloco 2 — Probabilidade e Distribuições** (15 questões)

**Total: 30 questões**, ~55% fechadas / ~45% abertas. Distribuição-alvo:

| Bloco | Fechadas | Abertas | Total |
|---|:--:|:--:|:--:|
| 1 — Cap. 1 (Análise Exploratória) | 8 | 7 | 15 |
| 2 — Cap. 2 (Probabilidade e Distribuições) | 8 | 7 | 15 |
| **Total** | **16** | **14** | **30** |

Os pesos são um alvo, não uma cota rígida: um exercício integrativo forte pode substituir dois fracos, desde que o total feche em **30** (para os 0,5 pt × 30 = 15 pontos). As seções de cálculo (localização, variabilidade, distribuição, condicional/Bayes, contagem, binomial, hipergeométrica, normal) concentram as questões; as descritivas/conceituais recebem menos.

## 7. Tipos de exercício

### Fechada (múltipla escolha)

- **5 alternativas (a–e)**, exatamente uma correta.
- **Distratores por erro conceitual clássico** — cada alternativa errada corresponde a um engano típico, não a um número aleatório. Exemplos de erros a explorar:
  - média vs. mediana num conjunto com outlier;
  - confundir sensibilidade $P(+\mid D)$ com o posterior $P(D\mid +)$ (taxa-base);
  - trocar permutação por combinação (ordem importa ou não);
  - aplicar binomial onde é hipergeométrica (com/sem reposição);
  - ler correlação como causação;
  - inverter a regra empírica (68/95/99,7).
- O aluno escreve **a letra + justificativa curta**.
- O gabarito registra a letra correta **e por que cada distrator falha**.

### Aberta (dissertativa/computacional)

- Problema com dados no enunciado. Pede resolução completa: **fórmula → substituição → número → interpretação**.
- Onde fizer sentido, é **integrativo** (cobre mais de uma seção — ver §8).
- O gabarito traz a resolução passo a passo com o **número verificado** por chunk Python.

## 8. Exercícios integrativos — arquétipos

Exemplos do estilo (a autoria final acontece no plano; aqui ficam os arquétipos, sem respostas):

- **Resumo de um conjunto pequeno** — dada uma tabela de 8–9 valores com um extremo, calcular média, mediana, média aparada, desvio-padrão e IQR, e discutir qual estimativa é robusta ao extremo. *Cobre 1.3 + 1.4 + 1.5.*
- **Média ponderada vs. simples** — pequena tabela (grupos com pesos), comparar as duas médias e explicar a divergência. *Cobre 1.3.*
- **Tabela de contingência** — de uma 2×3, extrair probabilidades condicionais, testar independência e aplicar Bayes para inverter o condicionamento. *Cobre 2.2 + 2.3.*
- **Inversão na agregação** — de duas subtabelas por grupo, mostrar que a relação se inverte ao agregar (efeito Simpson) e explicar o confundidor via probabilidades condicionais. *Cobre 1.8 + 2.3 (integra Cap. 1 e Cap. 2).*
- **Escolha da distribuição** — um cenário de lote/amostra: decidir entre binomial e hipergeométrica, justificar (com/sem reposição) e calcular uma probabilidade, usando contagem. *Cobre 2.4 + 2.5 + 2.6.*
- **Padronização e caudas** — dada uma média e um desvio, padronizar valores (z), aplicar a regra empírica e contrastar com um cenário de cauda longa em que a intuição normal falha. *Cobre 2.7 + 2.8.*
- **Correlação de um conjunto pareado** — de 6–7 pares, estimar a correlação (à mão/Python) e discutir correlação vs. causação. *Cobre 1.7 + 1.8.*
- **Classificação de variáveis** — dada uma lista de variáveis de um sistema real, classificar cada uma (contínua/discreta, nominal/ordinal, binária). *Cobre 1.1 + 1.2.*

## 9. Matriz de cobertura

Garantia: **cada uma das 16 seções é tocada por ≥ 1 exercício**, mesmo que um exercício cubra várias. O gabarito manterá, no topo, uma matriz seção → exercícios que a cobrem, para conferência antes de fechar.

| Bloco | Seção | Coberta por (arquétipo) |
|---|---|---|
| 1 | 1.1 Dados Estruturados | classificação de variáveis |
| 1 | 1.2 Dados Retangulares | classificação de variáveis / leitura de tabela |
| 1 | 1.3 Estimativas de Localização | resumo de conjunto; ponderada vs. simples |
| 1 | 1.4 Estimativas de Variabilidade | resumo de conjunto (dp, IQR, MAD) |
| 1 | 1.5 Distribuição dos Dados | resumo de conjunto (percentis, boxplot); leitura de histograma |
| 1 | 1.6 Dados Binários e Categóricos | moda/proporção/valor esperado |
| 1 | 1.7 Correlação | correlação de conjunto pareado |
| 1 | 1.8 Duas ou Mais Variáveis | correlação/contingência por grupo; inversão na agregação |
| 2 | 2.1 O que é Probabilidade | interpretações + espaço amostral |
| 2 | 2.2 Regras de Probabilidade | contingência / regras |
| 2 | 2.3 Condicional e Bayes | contingência + Bayes; taxa-base; inversão na agregação |
| 2 | 2.4 Contagem | escolha da distribuição (permutação/combinação) |
| 2 | 2.5 Binomial | escolha da distribuição |
| 2 | 2.6 Hipergeométrica | escolha da distribuição |
| 2 | 2.7 Normal | padronização + regra empírica |
| 2 | 2.8 Caudas Longas | padronização vs. cauda longa |

(Distribuição de arquétipos por exercício é detalhada no plano; esta matriz garante que nenhuma seção fica órfã.)

## 10. Verificação

- **Todo número** do gabarito sai de um chunk Python executado no container (`scipy`/`numpy`/`pandas`/`math`), no padrão do livro. Nenhum número escrito à mão no gabarito.
- **Passe de fechamento:** renderizar `lista-1-gabarito.qmd` no container; conferir que todos os chunks rodam e a matriz de cobertura fecha.
- **Consistência enunciado↔gabarito:** garantida por construção — fonte única (`lista-1.qmd`), a solução é um bloco `content-visible when-profile="gabarito"` no mesmo arquivo (§4). Não há segunda cópia do enunciado para divergir.
- **Não-vazamento:** a Fase 0 confere, no PDF do aluno (perfil lista), que as respostas não aparecem (extração de texto + grep).

## 11. Layout do PDF (typst)

- **Cabeçalho:** disciplina, "Lista 1 — Prova 1", campos em branco para **Nome** e **Matrícula**, o **prazo de entrega** e a nota "**30 questões · 0,5 ponto cada · 15 pontos**".
- **Instruções:** entrega **manuscrita**; Python permitido como ferramenta de cálculo; mostrar o raciocínio nas abertas e justificar as fechadas.
- **Numeração contínua** (1…30) com marcação do bloco/tópico ao lado; cada questão indica **(0,5)**.
- **Espaço para resolver** nas abertas (quando impresso).
- Gabarito: mesmo layout, com a resolução e a matriz de cobertura no topo.

## 12. Fora de escopo

- **Introdução (motivacional).** Fica de fora da lista; entra na Prova 1 apenas como leitura.
- **Lista 2 / Prova 2.** Cap. 3–5 são outra lista, outro ciclo.
- **Publicação.** Só a **folha do aluno** é servida e linkada no livro (cronograma + avaliação). O **gabarito** fica no repositório, mas **não** é recurso do site nem é linkado. Ver §5.
- **Versionamento.** No repo: os dois PDFs em `downloads/` (só a folha do aluno é recurso do site). Local por conveniência: o fonte `avaliacoes/lista-1.qmd`.

## 13. Plano de execução (visão)

Três fases, com subagentes (sem commit — conteúdo local):

1. **Fase 0 — Andaime + prova do mecanismo.** Criar `avaliacoes/_quarto.yml`, `_quarto-gabarito.yml`, o cabeçalho typst, o chunk de setup (`sys.path`, imports), e a linha do `.gitignore`. Escrever **um** exercício-piloto (com solução gated) e renderizar os **dois** perfis no container. **Gate de saída:** o PDF do aluno não contém a resposta (verificado por extração de texto + grep); o do gabarito contém. Só se passa à Fase 1 com o mecanismo provado.
2. **Fase 1 — Autoria por bloco.** Um subagente por bloco (Cap. 1 e Cap. 2 — 15 questões cada) escreve os exercícios (enunciado + solução gated com chunks verificáveis), seguindo a densidade e os arquétipos. Podem correr em paralelo (blocos independentes). Numeração: Bloco 1 = 1…15, Bloco 2 = 16…30.
3. **Fase 2 — Verificação e fechamento.** Render dos dois perfis no container; conferir que todos os chunks rodam, que a matriz de cobertura fecha (16 seções), que o total é 30 questões, que o PDF do aluno não vaza respostas e que a numeração fecha. Render final dos dois PDFs.

O detalhamento (tarefas, arquétipos por exercício, código dos chunks) vai para o plano de implementação, via skill `writing-plans`.
