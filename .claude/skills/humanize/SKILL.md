---
name: humanize
description: Auditoria somente-leitura de sinais de "voz de IA" na prosa em português dos .qmd/.md do livro — conectivos de enchimento ("Além disso,", "Vale ressaltar que"), léxico-clichê ("mergulhar", "desvendar", "crucial"), travessões em excesso, antítese "não é X — é Y", parágrafos simétricos, tricolons, ressalvas empilhadas, "não apenas X, mas também Y", aberturas formulaicas. Gera relatório; NÃO reescreve. Use quando o professor disser "humanize", "isso soa como IA?", "procura sinais de IA", "tira a voz de IA".
argument-hint: "[arquivo(s) ou 'capNN' ou 'all'] [--severity baixa|media|alta] [--so-novo]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Bash", "Agent"]
disallowed-tools: ["Edit"]
---

# `/humanize` — auditoria de voz (detectar e apontar)

Lê o(s) arquivo(s), audita os sinais de voz de IA e escreve um relatório. **Não reescreve.** O
autor edita. Leia `.claude/rules/writing-with-ai.md`: um relatório limpo diz que a prosa lê
**bem**, não que lê **humana** — detectores neurais não são enganados por limpeza superficial.

## O que esta skill não é

- Não é revisão de texto (→ agente `proofreader`), de substância (→ `domain-reviewer`) nem de pedagogia (→ `pedagogy-reviewer`).
- Não tem modo `--rewrite`, de propósito: reescrita automática introduz novos sinais.

## Passos

1. **Arquivos:** um caminho; `capNN` = todos os `.qmd` de `content/capNN/`; `all` = `content/**/*.qmd` + `index.qmd`. Ignore `.bib`, `.py`, `.ipynb`, `scripts/`, `avaliacoes/` (a menos que pedido explicitamente).
2. **`--so-novo`:** audite só a prosa adicionada desde o último commit (`git diff -U0 HEAD -- <arquivo>`); o resto do arquivo fica de fora. É o modo certo depois de uma sessão de escrita assistida.
3. **Sem baseline da casa:** não calibre pelo texto existente do livro. Boa parte dele foi escrita com IA, e medir "o hábito do autor" ali mede a IA. **O travessão não é marca do autor; é sinal.** Só um `voice-profile.md` na raiz, escrito pelo professor, isenta um hábito. A auditoria de 2026-09-17 (`quality_reports/audits/humanize_cap01-04-05_report.md`) partiu da premissa errada e não deve ser usada como referência.
4. **Um agente `humanize-auditor` por arquivo**, em paralelo numa única mensagem, passando o limiar de severidade.
5. **Relatório** em `quality_reports/audits/humanize_<alvo>_report.md` (gitignorado), com: método; densidades (travessões, antíteses, conectivos por mil palavras); contagem por categoria (ALTA/MÉD/BAIXA); tabela de achados (`linha | cat | sev | trecho | sugestão`); os 3 parágrafos mais concentrados; recomendação (> 8 ALTA/1k: reescrever; 5–8: limpar; < 5: cosmético).
6. **Resumo na conversa:** totais por categoria, parágrafos mais concentrados, recomendação. **Nenhum arquivo-fonte editado.**

## Categorias (detalhe no agente)

1. Conectivos de enchimento · 2. Léxico-clichê · 3. Travessão e pontuação (travessões, antítese "não é X — é Y", ponto-e-vírgula empilhado) · 4. Parágrafos simétricos · 5. Tricolons · 6. Ressalvas empilhadas · 7. "Não apenas X, mas também Y" · 8. Aberturas formulaicas · 9. Pergunta-resposta retórica em série · 10. Autoelogio.

## Depois do relatório

O professor reescreve os trechos. Se um parágrafo concentra achados demais, a recomendação é
reescrevê-lo do zero — não remendar sinal por sinal.
