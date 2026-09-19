---
paths:
  - "content/**/*.qmd"
  - "index.qmd"
  - "avaliacoes/**/*.qmd"
---

# Escrever com IA — o que torna a prosa legível

Dois problemas diferentes costumam ser confundidos:

| Problema | O que é | O que resolve |
|---|---|---|
| **Legibilidade** | a prosa é difícil de seguir, cheia de ressalvas, enchimento ou genérica | edição — vale a pena quem quer que tenha escrito |
| **Procedência** | a prosa *parece gerada por máquina* a um detector ou a um leitor desconfiado | **só reescrita humana de verdade**, mais transparência |

`/humanize` resolve o primeiro. **Não resolve o segundo.**

## O achado que motiva esta regra

No repositório de origem desta regra, um artigo passou por várias rodadas de "desIAzação"
superficial — menos travessões, sem "delve", conectivos variados — e um detector neural
(Pangram) o classificou como **100% escrito por IA**. Detectores classificam pela estatística
de tokens da geração, que sobrevive a qualquer transformação que o próprio modelo aplique.

> **Um modelo não consegue fazer a própria saída deixar de parecer saída de modelo.** Pedir
> ao Claude para "soar mais humano" produz texto diferentemente-LLM, não menos-LLM.

## O que fazer

1. **Decida o que o documento é.** Notas, planos e relatórios em `quality_reports/` são
   internos: rascunho de IA serve. O livro publicado, as listas e o PID são externos.
2. **No que é externo, o autor escreve as frases que carregam o argumento** — a abertura de
   cada seção, as interpretações dos números, os avisos de armadilha. O modelo ajuda na
   estrutura e no mecânico.
3. **Sinais superficiais são necessários, não suficientes.** Um relatório limpo do `/humanize`
   diz que a prosa lê **bem**, não que lê **humana**.
4. **Só detecção, por projeto.** `/humanize` não reescreve: a reescrita automática degrada a
   prosa e introduz novos sinais. O autor edita.

## Padrão para prosa externa

1. O leitor sabe o que a seção vai responder depois do primeiro parágrafo.
2. Frases carregam informação; corte a que sobrevive a ser apagada.
3. Ressalva ou é necessária ou some: "pode possivelmente sugerir" tem uma a mais.
4. A força da afirmação acompanha a evidência: ilustrado não é demonstrado.
5. Dá para ler em voz alta sem tropeçar.
