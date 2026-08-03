# Reestruturação do Livro com Material do pythonbook

**Data:** 2026-07-22
**Status:** Aprovado (design)

## Objetivo

Reestruturar o livro *Bases 3 — Estatística* incorporando estrutura e conteúdo do **pythonbook** de Ethan Weed (adaptação em Python de *Learning Statistics with R*, de Danielle Navarro), mantendo Bruce como espinha e **os exemplos brasileiros existentes**. Três mudanças:

1. Uma **Introdução** motivacional nova (Parte I do pythonbook).
2. O **Capítulo 1** enriquecido com quatro conceitos dos itens 5 e 6 do pythonbook.
3. O antigo **Capítulo 2** dividido em dois e reordenado para seguir a Parte IV do pythonbook (probabilidade → distribuições → amostra → estimação), empurrando os capítulos seguintes em cascata.

Ao final, **dois revisores** (didática e estatística) sobre todo o conteúdo escrito.

## Decisões (do brainstorming)

- **Introdução:** só a parte motivacional ("Por que estatística?"), adaptada ao contexto de dados/software. **Não** traz desenho de pesquisa nem escalas de medição (evita duplicar cap01 e cap02).
- **Probabilidade:** primer de **duas seções** — "O que é probabilidade" (frequentista vs bayesiano) + "Regras de probabilidade" (eventos, complementar, adição/multiplicação, independência).
- **Estrutura do antigo Cap. 2:** **dividir em dois** — Cap. 2 (Probabilidade e Distribuições) e Cap. 3 (Amostragem e Estimação); renumeração em cascata (Significância → Cap. 4, Regressão → Cap. 5).
- **Enriquecimentos do Cap. 1 (todos os quatro):** escores-padrão (z-scores), moda, curtose, gráfico de violino — adaptados aos exemplos brasileiros.
- **Revisores:** cobrem **todo o conteúdo escrito** (Intro + Cap. 1 + Cap. 2 + Cap. 3); **reportam por severidade** e decidimos juntos antes de aplicar correções.

## Nova estrutura do livro

| Parte (título no `_quarto.yml`) | Diretório | Seções |
|---|---|---|
| **Introdução** (sem número) | `content/intro/` | 2 (novas) |
| **Capítulo 1: Análise Exploratória de Dados** | `content/cap01/` | 8 (inalteradas) + 4 enriquecimentos (subseções) |
| **Capítulo 2: Probabilidade e Distribuições** | `content/cap02/` | 2 probabilidade (novas) + 7 distribuições (reaproveitadas) |
| **Capítulo 3: Amostragem e Estimação** | `content/cap03/` | 5 (reaproveitadas do cap02 atual) |
| **Capítulo 4: Experimentos Estatísticos e Testes de Significância** | `content/cap04/` | 11 stubs (era Cap. 3) |
| **Capítulo 5: Regressão e Predição** | `content/cap05/` | 7 stubs (era Cap. 4) |

Os enriquecimentos do Cap. 1 são **subseções** dentro dos `.qmd` existentes — **não** criam arquivos novos nem renumeram 1.1–1.8.

## Mapa de movimentação de arquivos (git mv, nesta ordem)

A ordem evita colisões de diretório.

```
# 1. Regressão: cap04 → cap05
git mv content/cap04 content/cap05

# 2. Significância: cap03 → cap04  (agora content/cap03 fica livre)
git mv content/cap03 content/cap04

# 3. Criar cap03 novo (Amostragem e Estimação) e mover as 5 seções de amostragem
mkdir content/cap03
git mv content/cap02/index.qmd            content/cap03/index.qmd   # será reescrito
git mv content/cap02/01-amostragem-aleatoria.qmd  content/cap03/01-amostragem-aleatoria.qmd
git mv content/cap02/02-vies-selecao.qmd          content/cap03/02-vies-selecao.qmd
git mv content/cap02/03-distribuicao-amostral.qmd content/cap03/03-distribuicao-amostral.qmd
git mv content/cap02/04-bootstrap.qmd             content/cap03/04-bootstrap.qmd
git mv content/cap02/05-intervalos-confianca.qmd  content/cap03/05-intervalos-confianca.qmd

# 4. Renumerar as distribuições dentro do cap02 (usar nomes temporários se necessário
#    para evitar colisão; a ordem final é a da tabela de remapeamento abaixo)
git mv content/cap02/09-distribuicao-binomial.qmd content/cap02/03-distribuicao-binomial.qmd
git mv content/cap02/12-poisson.qmd               content/cap02/04-poisson.qmd
git mv content/cap02/06-distribuicao-normal.qmd   content/cap02/05-distribuicao-normal.qmd
git mv content/cap02/07-caudas-longas.qmd         content/cap02/06-caudas-longas.qmd
git mv content/cap02/08-distribuicao-t.qmd        content/cap02/07-distribuicao-t.qmd
git mv content/cap02/10-qui-quadrado.qmd          content/cap02/08-qui-quadrado.qmd
git mv content/cap02/11-distribuicao-f.qmd        content/cap02/09-distribuicao-f.qmd

# 5. Criar os arquivos novos
#    content/cap02/01-o-que-e-probabilidade.qmd
#    content/cap02/02-regras-probabilidade.qmd
#    content/cap02/index.qmd  (novo, reescrito)
#    content/cap03/index.qmd  (reescrito)
#    content/intro/01-por-que-estatistica.qmd
#    content/intro/02-paradoxo-simpson.qmd
```

Observação sobre o `_freeze/`: renomear um `.qmd` invalida seu cache e o chunk reexecuta no próximo render. É esperado e correto (só mais lento). Nada a fazer.

## Remapeamento de seções (numeração DO MEU LIVRO)

Os callouts `corresponde à seção X de @bruce2020` (sempre a **linha 4** de cada seção) citam o **Bruce**, cuja numeração **não muda** — permanecem literais. Só as referências à numeração **do meu livro** (na prosa) remapeiam.

| Antigo (meu livro) | Novo | Arquivo |
|---|---|---|
| 2.9 Binomial | **2.3** | `cap02/03-distribuicao-binomial.qmd` |
| 2.12 Poisson | **2.4** | `cap02/04-poisson.qmd` |
| 2.6 Normal | **2.5** | `cap02/05-distribuicao-normal.qmd` |
| 2.7 Caudas longas | **2.6** | `cap02/06-caudas-longas.qmd` |
| 2.8 t de Student | **2.7** | `cap02/07-distribuicao-t.qmd` |
| 2.10 Qui-quadrado | **2.8** | `cap02/08-qui-quadrado.qmd` |
| 2.11 F | **2.9** | `cap02/09-distribuicao-f.qmd` |
| 2.1 Amostragem | **3.1** | `cap03/01-amostragem-aleatoria.qmd` |
| 2.2 Viés de seleção | **3.2** | `cap03/02-vies-selecao.qmd` |
| 2.3 Distribuição amostral | **3.3** | `cap03/03-distribuicao-amostral.qmd` |
| 2.4 Bootstrap | **3.4** | `cap03/04-bootstrap.qmd` |
| 2.5 Intervalos de confiança | **3.5** | `cap03/05-intervalos-confianca.qmd` |
| Cap. 3 (Significância) 3.1–3.11 | **Cap. 4** 4.1–4.11 | `cap04/*` |
| Cap. 4 (Regressão) 4.1–4.7 | **Cap. 5** 5.1–5.7 | `cap05/*` |

Novas seções do Cap. 2 (sem correspondência no Bruce cap. 2): **2.1** O que é probabilidade, **2.2** Regras de probabilidade.

## Inventário de referências cruzadas a corrigir

Levantado por `grep`. **Não** incluir as linhas-4 (`de @bruce2020`). Todas as referências abaixo são à numeração do meu livro.

**Nas distribuições (novo Cap. 2):**
- `05-distribuicao-normal.qmd`: `seção 2.1` → contexto de cauda longa/renda (ver "Coerência narrativa"); `seção 2.7` (remissão a caudas longas) → **2.6**.
- `06-caudas-longas.qmd`: `seção 2.6` (normal) → **2.5**.
- `07-distribuicao-t.qmd`: `seção 2.5` (intervalos de confiança) → **3.5** (ver "Coerência narrativa").
- `08-qui-quadrado.qmd`: `Capítulo 3` → **Capítulo 4** (2×, linhas ~18 e ~48); `seção 3.9` → **4.9**.
- `09-distribuicao-f.qmd`: `Capítulo 3` → **Capítulo 4**; `seção 3.8` → **4.8**.

**Na amostragem (novo Cap. 3):**
- `01-amostragem-aleatoria.qmd`: `seção 2.3` → **3.3** (2×); `Capítulo 1` permanece; referência à cauda longa como algo futuro → ver "Coerência narrativa".
- `03-distribuicao-amostral.qmd`: `seção 2.1` → **3.1** (2×); `Capítulo 1` permanece.
- `04-bootstrap.qmd`: `seção 2.3` → **3.3** (2×).
- `05-intervalos-confianca.qmd`: `seção 2.3` → **3.3**.

**Nos índices e stubs movidos:**
- `cap04/index.qmd`: prosa `Capítulo 3` → **Capítulo 4**. Os stubs de `cap04/*` mantêm seus callouts `seção 3.X de @bruce2020` (Bruce cap. 3 = A/B, testes — inalterado).
- `cap05/index.qmd`: prosa `Capítulo 4` → **Capítulo 5**. Stubs de `cap05/*` mantêm `seção 4.X de @bruce2020`.

**Verificação de integridade (fim da Fase 1):** um `grep` que garanta que nenhuma referência de prosa aponte para um número inexistente (ex.: buscar `seção 2.1[012]` — que não existe mais no Cap. 2 — deve dar vazio).

## Coerência narrativa (quebras de direção pela reordenação)

Mover as distribuições para **antes** da amostragem inverte a direção de referências que hoje são "para trás" e passam a ser "para frente" (ou vice-versa). Estas exigem **reescrita de prosa**, não só troca de número:

1. **Normal (2.5) usa `loans_income` primeiro.** Hoje o dataset é apresentado na amostragem (antiga 2.1). Na nova ordem, a Normal é a primeira aparição da renda. **Ação:** dar à Normal uma apresentação curta do dataset no primeiro uso ("as 50.000 rendas do `loans_income`…") e trocar "a cauda longa que já vimos na seção 2.1" por uma afirmação autossuficiente ou uma remissão para frente ao Cap. 3.
2. **t de Student (2.7) referencia intervalos de confiança como passado** ("foi a distribuição por trás dos IC da seção 2.5"). IC agora é 3.5, **posterior**. **Ação:** reescrever como remissão para frente ("será a distribuição por trás dos intervalos de confiança, no Cap. 3").
3. **Amostragem (3.1) referencia cauda longa como futuro** ("vai voltar quando o capítulo chegar lá"). Cauda longa agora é 2.6, **anterior**. **Ação:** reescrever como remissão para trás ("que o Capítulo 2 já tratou").

O **revisor de didática** é a rede de segurança para outras quebras de direção não listadas aqui.

## Conteúdo novo — Introdução (2 seções)

Voz motivacional, adaptada ao público de Engenharia de Software / Sistemas de Informação. Despsicologizada: os exemplos do pythonbook (silogismos, medição psicológica) viram exemplos de dados/software. Callout de abertura cita **@weed**.

- **`intro/01-por-que-estatistica.qmd`** — Por que a intuição falha e precisamos de estatística: viés de crença/confirmação (tendemos a aceitar conclusões que confirmam o que já achávamos e a duvidar das que não), a estatística como disciplina que obriga os dados a responder. Estatística no dia a dia (dados, software, decisões). Sem código pesado; no máximo uma ilustração simples.
- **`intro/02-paradoxo-simpson.qmd`** — A fábula de advertência do paradoxo de Simpson, num exemplo de **dados/A-B** (uma tendência agregada que se inverte dentro de cada subgrupo — ex.: uma variante que "vence" no total mas perde em todo segmento, ou taxa de sucesso por grupo). Um chunk pequeno com dados sintéticos (semente fixa) que exibe a inversão numérica. Conecta a confundidores/agregação que reaparecem adiante.

## Conteúdo novo — Probabilidade (2 seções, abrem o Cap. 2)

Callout de abertura cita **@weed**. Formato brasileiro nos números (`from formato import num`). Semente fixa em qualquer simulação.

- **`cap02/01-o-que-e-probabilidade.qmd`** — Diferença entre probabilidade e estatística (uma parte do processo é dedutiva, a outra indutiva). O que "probabilidade" significa: **visão frequentista** (frequência no longo prazo) vs **visão bayesiana** (grau de crença), qual a diferença e por que importa para o Cap. 4 (valores-p são frequentistas). Uma simulação com semente mostrando a frequência relativa convergindo para a probabilidade conforme o número de repetições cresce (eixo estabilizando).
- **`cap02/02-regras-probabilidade.qmd`** — Eventos e espaço amostral; probabilidade de um evento; **complementar** (P(não A) = 1 − P(A)); **adição** (eventos mutuamente exclusivos / regra geral); **multiplicação** e **independência** (P(A e B) = P(A)·P(B) quando independentes). A ideia de **distribuição de probabilidade** como ponte para as sete distribuições que seguem. Exemplos de dados/software (bug em um de N módulos, dois serviços independentes falharem juntos). 2–3 exercícios.

## Enriquecimentos do Cap. 1 (subseções)

Cada um no arquivo existente indicado, sem criar `.qmd` novos. Callout ou nota citando **@weed** onde o conceito vem do pythonbook. Exemplos brasileiros (estados, renda). Semente fixa se houver sorteio.

- **Moda** → `03-estimativas-localizacao.qmd`: nova subseção após média/mediana/aparada. A moda como valor mais frequente; útil sobretudo para **categóricos** (o estado/categoria mais comum), com ponte para a seção 1.6. Para a população contínua dos estados, discutir por que a moda é pouco informativa (cada valor é único) — a lição honesta.
- **Escores-padrão (z-scores)** → `04-estimativas-variabilidade.qmd`: nova subseção formalizando $z = (x - \bar{x})/s$ — quantos desvios um valor está da média. **Encaixe:** o widget desta seção já usa z-scores ("o truque por trás disso é o z-score"); a subseção transforma esse uso em conceito ensinado, e antecipa a padronização da Normal (2.5). Exemplo: o z-score de São Paulo na população, ou da taxa de homicídios.
- **Curtose** → `05-distribuicao-dados.qmd`: estender a discussão de forma (que já trata **assimetria**) com a **curtose** como o número que mede o peso das caudas. Conecta explicitamente com caudas longas (2.6). Não reescrever a assimetria existente — acrescentar ao lado.
- **Gráfico de violino** → `05-distribuicao-dados.qmd`: nova subseção após o boxplot, apresentando o violino como alternativa que mostra a **densidade** (não só os quartis), com a **ressalva do pythonbook** sobre quando ele engana (densidade estimada sugere massa onde não há dados; cauda suavizada além do mínimo/máximo reais).

## Atribuição de fontes

- Adicionar ao `references.bib` uma entrada para o pythonbook (Weed; adaptação em Python de *Learning Statistics with R* de Navarro), com URL `https://ethanweed.github.io/pythonbook/`. Chave: `@weed`. O ano/autoria a serem confirmados a partir da fonte no momento da implementação (não inventar; usar `s.d.` se indeterminável).
- Callouts `de @bruce2020` das seções reaproveitadas **permanecem** (números do Bruce inalterados).
- Seções novas (intro ×2, probabilidade ×2) e as subseções de enriquecimento citam **@weed**.
- O livro passa a se declarar híbrido: Bruce (espinha), Weed (introdução, probabilidade, ordenação, enriquecimentos), exemplos brasileiros próprios.

## Atualização do CLAUDE.md

O `CLAUDE.md` documenta a estrutura e precisa refletir a mudança:
- **Escopo:** de "capítulos 1–4" para a nova espinha (Introdução + 5 capítulos), com o mapa Bruce↔meu-livro (Bruce cap. 2 dividido entre meus Cap. 2 e Cap. 3; Bruce cap. 3 → meu Cap. 4; Bruce cap. 4 → meu Cap. 5).
- **Livro-texto:** acrescentar o pythonbook como segunda fonte (estrutura/introdução/probabilidade), com a regra de atribuição.
- **Estrutura de conteúdo:** a árvore de diretórios atualizada (`intro/`, `cap01`–`cap05`).

## Faseamento do plano

1. **Fase 1 — Reestruturação e coerência narrativa.** `git mv` na ordem acima; reescrever `_quarto.yml`; corrigir **todas** as referências cruzadas do inventário; aplicar as 3 reescritas de coerência narrativa; reescrever os `index.qmd` afetados; atualizar `CLAUDE.md`. **Portão:** `make render` verde (42 páginas → agora mais, com as movidas), `grep` de integridade de refs vazio, nenhum stub perdido. Nenhum conteúdo novo ainda.
2. **Fase 2 — Conteúdo novo.** Introdução ×2, probabilidade ×2, e os 4 enriquecimentos do Cap. 1. Cada `.qmd` renderiza; números conferidos no container; sementes conferidas. Entrada no `references.bib`.
3. **Fase 3 — Revisão.** Dois subagentes (estatística, didática) sobre Intro + Cap. 1 + Cap. 2 + Cap. 3. Relatório por severidade → consolidação → **decisão do usuário** antes de qualquer correção.

## Os dois revisores (Fase 3)

Executados como subagentes, cada um recebendo o conteúdo renderizado/fonte das quatro partes (Intro, Cap. 1, Cap. 2, Cap. 3):

- **Revisor de estatística:** erros conceituais, definições imprecisas ou fracas, fórmulas incorretas, números que não batem com o código, uso indevido de termo técnico. Foco em **correção**.
- **Revisor de didática:** sequência lógica de ponta a ponta, saltos conceituais (um conceito usado antes de definido), remissões quebradas (para trás/para frente), clareza e adequação ao público. Foco em **fluxo e clareza**.

Cada um entrega achados classificados por severidade (ex.: Crítico / Importante / Menor). Consolido os dois relatórios, apresento ao usuário, e as correções só são aplicadas **após decisão conjunta**.

## Verificação (global)

- `make render` verde após cada fase.
- `grep` de integridade: nenhuma referência de prosa a seção/capítulo inexistente.
- Cap. 2 (9 seções) e Cap. 3 (5 seções) sem stub; Intro (2 seções) sem stub.
- Enriquecimentos: cada conceito (moda, z-score, curtose, violino) presente no HTML da seção correspondente; um `<img>` novo para o violino.
- Números novos conferidos no container (probabilidade: convergência frequentista; Simpson: a inversão numérica).
- Sementes: nenhum chunk com RNG sem semente nas seções novas.
- `CLAUDE.md` e `references.bib` atualizados.
- Working tree limpa; commits atribuídos ao usuário.

## Fora de escopo

- Escrever o conteúdo dos Capítulos 4 e 5 (permanecem stubs).
- Desenho de pesquisa / escalas de medição / confiabilidade-validade (a introdução é só motivacional, por decisão).
- Aplicar as correções dos revisores nesta rodada (Fase 3 termina no relatório + decisão do usuário).
- Widgets interativos nas seções novas (probabilidade e intro são estáticas; o violino é gráfico estático).
- Reescrever exemplos brasileiros existentes do Cap. 1 (só acrescentar as subseções).
