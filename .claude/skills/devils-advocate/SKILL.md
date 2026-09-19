---
name: devils-advocate
description: Desafio adversarial de 5–7 perguntas às escolhas pedagógicas de uma seção ou capítulo do livro — ordem, pré-requisitos, carga cognitiva, motivação, notação, escolha do exemplo. Use quando o professor disser "advogado do diabo", "cutuca essa seção", "o que um aluno cético perguntaria?", "testa o desenho da seção". Somente leitura; mais leve que o pedagogy-reviewer.
argument-hint: "[arquivo .qmd ou seção, ex.: 2.6]"
allowed-tools: ["Read", "Grep", "Glob"]
disallowed-tools: ["Edit", "Write"]
---

# Advogado do diabo

Examine a seção criticamente e desafie o desenho com 5–7 perguntas pedagógicas específicas.
**Filosofia:** a melhor seção sai do diálogo ativo.

## Preparação

1. Leia o arquivo-alvo (resolva "1.6" para `content/cap01/06-*.qmd`).
2. Leia `.claude/rules/knowledge-base.md` (notação, progressão, armadilhas) e o `CLAUDE.md` (escopo e cortes).
3. Leia o fim da seção anterior e o começo da seguinte.

## Categorias de desafio

1. **Ordem** — "O aluno entenderia melhor se X viesse antes de Y?"
2. **Pré-requisito** — "Um aluno de ES/SI tem base para esta notação aqui?" (lembre o que foi cortado em 2.2026).
3. **Lacuna** — "Falta um exemplo intuitivo antes desta fórmula?"
4. **Apresentação alternativa** — "Duas outras formas de mostrar isto" (gráfico, simulação em Python, widget, analogia de software).
5. **Conflito de notação** — "Este símbolo colide com o uso em outra seção/no Bussab."
6. **Carga cognitiva** — "Símbolos ou funções novas demais de uma vez. Dividir?"
7. **Exemplo e dado** — "O dataset escolhido mostra o fenômeno, ou o esconde?" (ex.: n = 27 ímpar, SP outlier).
8. **Código** — "Este chunk ensina ou distrai? O aluno reproduz no Colab?"

## Saída

```markdown
# Advogado do diabo: <seção>

### Desafio 1: <Categoria> — <título curto>
**Pergunta:** …
**Por que importa:** …
**Sugestão:** …
**Onde:** linha N / subtítulo
**Severidade:** Alta / Média / Baixa

(5–7 desafios)

## Veredito
**Pontos fortes:** 2–3
**Mudanças críticas antes da aula:** 0–2
**Melhorias desejáveis:** 2–3
```

## Princípios

- Específico: cite subtítulo, linha, símbolo.
- Construtivo: todo desafio traz uma sugestão.
- Honesto: se a seção está boa, diga.
- Prioridade: conflito de notação e erro de pré-requisito > metáfora perdida.
- Pense como o aluno: onde ele se perde?
