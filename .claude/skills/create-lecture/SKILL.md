---
name: create-lecture
description: Cria uma nova seção (ou preenche um stub) do livro Quarto de Bases 3 — Estatística a partir das fontes (Bruce, Weed, Bussab), com checagem de notação, callout de atribuição, código Python com semente e registro no _quarto.yml. Use quando o professor disser "cria a seção X", "escreve a 1.9", "começa o capítulo de probabilidade", "nova seção sobre Y". Colaborativo e em lotes — não despeja a seção inteira de uma vez.
argument-hint: "[seção, ex.: 1.9 ou 'probabilidade condicional'] [--fonte bruce|bussab|weed]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Agent"]
---

# Criar uma seção do livro

Colaborativo e iterativo: **o professor conduz, o Claude é parceiro de raciocínio.** O modelo
de **estrutura** é `content/cap01/03-estimativas-localizacao.qmd` (não de voz: ele tem travessões
demais, e o travessão não é estilo do professor).

## Restrições (inegociáveis)

1. Ler `.claude/rules/knowledge-base.md` e `.claude/rules/content-invariants.md` **antes** de escrever.
2. Todo símbolo novo conferido contra o registro de notação.
3. Motivação antes da fórmula (INV-10); exemplo com dado real em até dois parágrafos de cada definição.
4. Callout de atribuição com o número **da fonte** (INV-2); escopo do CLAUDE.md respeitado (INV-3).
5. Python apenas; semente explícita (INV-5); caminhos a partir da raiz (INV-6); números da prosa ligados ao código com `` `{python} num(...)` `` (INV-8).
6. No máximo dois blocos coloridos seguidos (INV-11).
7. Toda citação resolve em `references.bib`.
8. **Lotes de uma subseção (`##`) por vez**, mostrando ao professor antes de seguir.

## Fase 0 — Pré-voo (obrigatório)

Leia: `CLAUDE.md`; `.claude/rules/knowledge-base.md`; o `index.qmd` do capítulo; a seção
anterior (fim) e a seguinte (começo); o stub, se existir; a fonte. Para o Bruce, o repositório
de código em <https://github.com/gedeck/practical-statistics-for-data-scientists>. Para o
Bussab, o epub em `livros/` (ver o bloco "Acesso ao Bussab" em
`.claude/agents/domain-reviewer.md`; **nunca** copie texto dele para o repositório).

Produza:

```markdown
## Relatório de Pré-Voo
**Seção:** N.M — <título> · arquivo: content/capNN/MM-nome.qmd (novo | stub)
**Fonte(s):** <Bruce x.y / Bussab x.y / Weed cap. z> — <o que cada uma contribui>
**Callout de atribuição:** "Esta seção <corresponde à | se baseia na> seção x.y de @chave."
**Notação:** novos: […] · reutilizados: […] (seção de origem) · conflitos: nenhum | […]
**Posição no arco:** a anterior terminou em … ; a próxima precisa de …
**Objetivo pedagógico:** <uma frase>
**Aplicação que atravessa a seção:** <dataset de dados/ ou exemplo de software>
**Dados:** <CSV existente em dados/ | precisa gerar (script em scripts/, roda uma vez)>
**Fora do escopo (INV-3):** <o que a fonte tem e não entra>
```

Confirme o objetivo com o professor antes da Fase 1.

## Fase 1 — Estrutura

Proponha os `##` da seção: pergunta de abertura → conceito → exemplo → código → armadilha →
(opcional) "Agora é com você". Liste gráficos, widgets OJS (só se a intuição depender de
mexer; ver critério do Shinylive no CLAUDE.md) e notação nova.
**PORTÃO: o professor aprova antes da Fase 2.**

## Fase 2 — Redação em lotes

Uma subseção por vez. Chunk de setup `include: false` como no modelo (`from formato import
num`). Atualize o `_quarto.yml` (INV-1) ao criar o arquivo. Se a seção substitui um stub,
remova o aviso de construção.

## Fase 3 — Código e figuras

Rode os chunks no `.venv` (se existir) para conferir números antes de escrevê-los na prosa;
depois `make render`. Widgets OJS consomem `ojs_define` e usam `//| echo: false` (INV-9).

## Fase 4 — Revisão

- `/humanize <arquivo> --so-novo` e corrigir os achados de gravidade alta.
- `/devils-advocate` na seção.
- Agente `domain-reviewer` (substância, referência Bussab).
- Agente `verifier` (render, citações, sementes, widgets).
- Atualize `.claude/rules/knowledge-base.md` com notação e armadilhas novas.
- Se o capítulo tem notebook (`notebooks/capitulo-NN.ipynb`), pergunte se a seção entra nele.

## Checklist final

```
[ ] Registrada no _quarto.yml e renderiza sem erro
[ ] Callout de atribuição com o número da fonte
[ ] Toda definição com motivação + exemplo
[ ] Sementes explícitas; caminhos a partir da raiz
[ ] Números da prosa ligados ao código
[ ] 2–3 perguntas ao leitor
[ ] ≤ 2 blocos coloridos seguidos
[ ] Nenhum meta-texto sobre o livro-fonte/o material (INV-13)
[ ] knowledge-base.md atualizada
[ ] humanize + devils-advocate + domain-reviewer + verifier rodados
```

## Ver também

`/scaffold-exercises` (lista para a seção) · `/qa-quarto` (renderização) · `/slide-excellence` (revisão completa).
