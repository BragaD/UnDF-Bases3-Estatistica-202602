---
name: scaffold-exercises
description: Monta uma lista de exercícios para seções do livro — conceituais, de cálculo e de código Python — com gabarito separado, no formato das listas em avaliacoes/ (Quarto → PDF via Typst, perfil "gabarito"). Use quando o professor disser "monta uma lista sobre X", "exercícios para a seção 2.5", "questões de fixação", "gera lista com gabarito". Enunciado e gabarito ficam em avaliacoes/ (gitignorado); nada vai para o repositório público.
argument-hint: "[seções ou tema] [--nivel intro|core|avancado] [--quantidade N] [--tipos conceitual,calculo,codigo] [--dataset caminho] [--sem-gabarito]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash"]
---

# `/scaffold-exercises` — lista de exercícios

Gera uma lista com enunciado e gabarito. O formato de referência é `avaliacoes/lista-1.qmd`:
um único `.qmd`, com o gabarito em `::: {.content-visible when-profile="gabarito"}` e dois
perfis (`_quarto.yml` e `_quarto-gabarito.yml`) que geram dois PDFs.

**Privacidade (INV-12):** `avaliacoes/` é gitignorado porque o repositório é público. Lista e
gabarito **nunca** vão para `content/`, nunca usam `.spoiler` e nunca entram num commit. O
que se distribui é o PDF.

## Tipos

| Tipo | O aluno | Gabarito |
|---|---|---|
| **conceitual** | explica, compara, identifica a hipótese violada | resposta curta + o erro comum |
| **cálculo** | resolve à mão (calculadora/Colab permitido) | passo a passo, com o número final formatado em pt-BR |
| **código** | escreve/lê Python (pandas, numpy, scipy) | código que **roda** + saída real |

Exercícios com dados usam os CSVs de `dados/` (estados, aluguéis…) ou uma simulação com
semente explícita (INV-5). Nunca invente números "de cabeça".

## Fase 0 — Pré-voo

Leia as seções-alvo, `.claude/rules/knowledge-base.md` e a lista existente em `avaliacoes/`
(para não repetir questões e manter a numeração/estilo). Produza:

```markdown
## Relatório de Pré-Voo — Lista
**Seções:** … · **Nível:** intro | core | avançado
**Tipos:** conceitual=N, cálculo=N, código=N (total N)
**Dados:** dados/<arquivo> | simulação com semente AAAAMMDD | nenhum
**Objetivos de aprendizagem:** 2–4
**Matriz de cobertura:** seção → questões
**Arquivo:** avaliacoes/<nome>.qmd
```

Tema vago demais para escrever objetivos → uma pergunta ao professor e para.

## Fase 1 — Questões

- **Motivação antes da mecânica:** uma frase dizendo por que a pergunta importa (de preferência um cenário de software/dados).
- **Notação da casa:** a mesma do livro (`knowledge-base.md`); nada que colida.
- **Calibração:** intro = um conceito; core = 2–3 passos encadeados; avançado = um insight não óbvio (ex.: por que a média ponderada fica abaixo da simples).
- **Autocontida:** cada questão diz suas hipóteses; nada de "como na aula".
- **Escopo:** só o que o livro cobre hoje — Introdução e Cap. 1, já descontados os cortes de 2.2026 (nada de curtose, violino, densidade, valor esperado ou heatmap).
- Questões fechadas: alternativas plausíveis, uma só correta, distratores que capturam erros reais (divisor $n$ × $n-1$, com × sem reposição, $\sigma$ × $\sigma^2$ na scipy).

## Fase 2 — Gabarito

Para cada questão: solução completa e uma linha de "por que importa". Código do gabarito
**executado** no `.venv` (ou via chunk `{python}` na própria lista, como a `lista-1.qmd` faz
com `from formato import num`); cole a saída real. Não executado → marque **RASCUNHO — NÃO
EXECUTADO**.

## Fase 3 — Arquivos

- `avaliacoes/<nome>.qmd` com enunciado + blocos `when-profile="gabarito"` (inclua a matriz de cobertura dentro do bloco de gabarito, como na lista 1).
- Reaproveite `avaliacoes/_quarto.yml` / `_quarto-gabarito.yml`; se o nome do PDF de gabarito precisar mudar, ajuste `output-file`.
- Render (comando indicado ao professor, a partir de `avaliacoes/`): `quarto render <nome>.qmd` e `quarto render <nome>.qmd --profile gabarito`.
- `--sem-gabarito`: só o enunciado.

## Saída

Caminhos absolutos dos arquivos, contagem por tipo, semente usada, quais códigos foram
executados. Confirme com `git check-ignore avaliacoes/<nome>.qmd` que o arquivo está ignorado.

## O que esta skill não faz

Não corrige respostas de alunos, não publica nada, não mexe em `content/` nem em `downloads/`
(copiar o PDF para `downloads/` é decisão do professor).
