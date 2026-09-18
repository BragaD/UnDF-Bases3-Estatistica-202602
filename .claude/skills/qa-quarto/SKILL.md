---
name: qa-quarto
description: QA adversarial da renderização de uma seção do livro. Um agente crítico compara o .qmd com o HTML em _book/ (e com o notebook do capítulo) — chunks com erro, citações/refs não resolvidas, figuras ausentes, widgets OJS mudos, números da prosa divergentes; um agente consertador aplica o que é mecânico e re-renderiza; repete até convergir (máx. 5 rodadas). Use quando o professor disser "qa da seção", "confere o render", "o HTML bate com o qmd?", ou antes de dar push numa seção.
argument-hint: "[seção, ex.: 1.5, ou caminho do .qmd]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent"]
---

# QA adversarial: `.qmd` × página renderizada

**Filosofia:** o `.qmd` é o que o professor quis dizer; o HTML em `_book/` é o que o aluno vê.
Tudo o que se perde no caminho é defeito. (No workflow de origem esta skill comparava Quarto
com Beamer; aqui não há Beamer — a referência é o próprio fonte.)

```
Pré-voo → crítico (rodada 1) → consertador → crítico (rodada 2) → … até convergir
```

## Portões rígidos

| Portão | Condição |
|---|---|
| Execução | nenhum chunk com erro |
| Citações / refs | nada `?@...` no HTML |
| Figuras | todo chunk de gráfico gerou imagem |
| Widgets OJS | teste de navegador passa (seções com `{ojs}`) |
| Números | nenhum `{python}` literal; prosa = saída do código |
| Render fresco | HTML mais novo que o `.qmd` |

## Fase 0 — Pré-voo

1. Resolva a seção para `content/capNN/MM-*.qmd` e `_book/content/capNN/MM-*.html`.
2. Frescor: se o `.qmd` for mais novo que o HTML, rode `make render`. Docker parado → pare e avise (não audite HTML velho).
3. `{ojs}` na seção? → o teste de navegador do CLAUDE.md entra no portão.
4. Notebook do capítulo existe? → entra a dimensão de paridade livro ↔ notebook.
5. Teste o validador: `echo '[]' | python3 scripts/validate-findings.py`.
6. Ecoe o Relatório de Pré-Voo (arquivos, condições, rodadas máximas = 5).

## Fase 1 — Crítico

Agente `quarto-critic` com seção, rodada e condições. Relatório em
`quality_reports/<secao>_qa_critic_round1.md` + `.json`.

## Fase 2 — Consertos

Se não APROVADO: agente `quarto-fixer`. Ele aplica só `mechanical: true` e o que o crítico
especificou sem ambiguidade; o que toca definição, fórmula, número reportado ou escolha
pedagógica volta ao professor como **Bloqueado**.

## Fase 3 — Nova auditoria

Crítico de novo, **em contexto novo**, com o relatório anterior para deduplicar por `id`.

## Convergência

- Para quando uma rodada não traz nenhum `id` novo de `blocker`/`major`
  (`.claude/rules/orchestrator-protocol.md`).
- Teto: 5 rodadas → apresenta com pendências.
- **Duas vezes o mesmo `id`** (rodadas N e N+2) → escala ao professor em vez de remendar de novo.
- APROVADO ⇔ todos os portões passam.

## Relatório final

`quality_reports/<secao>_qa_final.md`: status dos portões, resumo por rodada, pendências e o
que ficou bloqueado para decisão do professor. Antes de apresentar, valide cada `.json` com
`python3 scripts/validate-findings.py`. Nunca faça commit.
