# Dados Brasileiros no Lugar dos Americanos

**Data:** 2026-07-14
**Status:** Aprovado

## Objetivo

Substituir o `dados/state.csv` (50 estados dos EUA, população 2010 e taxa de homicídios) por um conjunto equivalente do **Brasil**: 27 unidades federativas, população 2024 do IBGE e taxa de homicídios 2024 do Atlas da Violência.

Adaptar as cinco seções do Capítulo 1 que usam esses dados, mais os dois widgets interativos da seção 1.3.

O objetivo não é só trocar números: é que o aluno reconheça o país em que vive nos exemplos.

## Fontes

| Dado | Fonte | Acesso |
|---|---|---|
| Taxa de homicídios por UF, 2024 | Atlas da Violência (Ipea/FBSP) | CSV baixado manualmente do site |
| População por UF, 2024 | IBGE, SIDRA tabela 6579, variável 9324 | `https://apisidra.ibge.gov.br/values/t/6579/n3/all/v/9324/p/2024` |
| Nome e sigla por código IBGE | IBGE, API de localidades | `https://servicodados.ibge.gov.br/api/v1/localidades/estados` |

**Sobre o Atlas:** a API antiga (`/atlasviolencia/api/v1/...`) foi ao ar abaixo na reformulação do site (v3.0.0) e hoje devolve HTML. Não há endpoint público funcionando. O CSV bruto, portanto, vai **versionado** em `dados/brutos/atlas-violencia-taxa-homicidios.csv` — sem isso o pipeline deixa de ser reproduzível, e ninguém conseguiria auditar de onde vieram os números do livro.

**Sobre o `geobr`:** foi considerado e descartado. Ele baixa *shapefiles* — geometrias que não usamos — e arrastaria o `geopandas` para o projeto. A API de localidades do IBGE devolve a mesma informação (id, sigla, nome) num JSON de ~2 KB, sem dependência nova. Se um dia o livro tiver mapas, o `geobr` volta à mesa.

## Arquitetura

### O pipeline é one-off e fica fora do livro

`scripts/gerar-dados-brasil.py` roda **uma única vez**, gera o CSV, e o CSV é commitado. Ele **não** é um chunk do livro: o aluno não precisa ver a mecânica de juntar três fontes de dados para aprender o que é uma mediana, e um livro que executa três chamadas de rede a cada render é frágil e lento.

O script **valida e falha alto**: se as três fontes não casarem exatamente nas mesmas 27 UFs, ele levanta erro em vez de produzir um CSV com buraco. Um estado faltante viraria um `NaN` silencioso, e silêncio é exatamente o modo de falha que este projeto já sofreu duas vezes.

### O CSV gerado

`dados/estados.csv` — 27 linhas, colunas em **português**:

```
"Estado","Populacao","Taxa.Homicidios","Sigla"
"Rondônia",1746227,29.78,"RO"
"Acre",880631,19.65,"AC"
...
```

A regra do projeto de "preservar os nomes de coluna do original" existia para que o código do livro-texto rodasse literalmente sobre os CSVs do Gedeck. Este dado é **nosso** — a regra não se aplica, e um livro em português com cabeçalho em inglês seria incoerente.

`dados/state.csv` é **removido**. Depois da troca ele fica órfão, e mantê-lo convida um agente futuro a usá-lo por engano.

## Os números (calculados sobre os dados reais, antes de escrever este spec)

| Estatística | Valor |
|---|---|
| Média (população) | 7.873.472,2 |
| Média aparada 10% (k = 2 de cada ponta) | 6.250.792,8 |
| Mediana (população) | 4.145.040,0 |
| Média simples da taxa | 22,7389 |
| Média ponderada da taxa | 18,7907 |
| Desvio-padrão (população) | 9.256.155,8 |
| IQR (população) | 6.443.986,0 |
| Maior / menor população | São Paulo 45.973.194 / Roraima 716.793 → **64×** |

## As três mudanças que são de conteúdo, não de dados

Trocar o dataset não é uma operação mecânica. Três afirmações que o livro faz hoje **deixam de ser verdadeiras** com os dados brasileiros.

### 1. A mediana com n ímpar

O Brasil tem **27** UFs. A seção 1.3 hoje ensina, com todas as letras, que *"com número **par** de observações — como aqui, n = 50 — não existe um único valor central: a mediana é a média dos dois valores do meio... é por isso que o número calculado abaixo termina em `,5`"*. Com 27 estados isso é falso.

**Decisão:** ensinar a definição completa — com n ímpar a mediana é o valor central; com n par, é a média dos dois centrais.

E há um presente nos dados: a mediana da população brasileira, **4.145.040**, é exatamente a população da **Paraíba**. O aluno vê que a mediana não é um número que a conta inventou — é a observação que ficou no meio da fila. É um gancho melhor do que o `,5` do caso americano.

### 2. A conclusão da média ponderada se inverte

| | EUA | Brasil 2024 |
|---|---|---|
| Média simples da taxa | 4,07 | 22,74 |
| Média ponderada | 4,45 | **18,79** |
| Direção | ponderada **maior** | ponderada **menor** |

A prosa atual conclui que *"os estados mais populosos tendem a ter taxas de homicídio mais altas"*. No Brasil é o contrário: **São Paulo tem a maior população (46 milhões) e a menor taxa do país (6,16)**, e sozinho puxa a média ponderada para baixo. A violência letal se concentra nos estados menos populosos, no Norte e Nordeste.

A resposta do **exercício 2** da seção 1.3 inverte junto.

Isso não enfraquece a seção — fortalece. Mostra que a direção do efeito é um **fato empírico sobre o país**, não uma lei da estatística, e o contraste entre os dois países é ele próprio uma lição.

### 3. São Paulo substitui a Califórnia

Nos dois widgets da seção 1.3 e nas menções em 1.5. O paralelo se sustenta: São Paulo / Roraima = **64×**; Califórnia / Wyoming era 66×.

Detalhe do widget: o valor inicial do slider passa a ser **45.973.194** (população real de SP), com o mesmo cuidado de antes — `step: 1` em habitantes, para que os números do widget batam dígito a dígito com os que o chunk Python imprime na mesma página.

## Impacto no livro

| Seção | Usa | O que muda |
|---|---|---|
| 1.1 Dados Estruturados | `dtypes`, `astype("category")` | nomes de coluna, 27 categorias em vez de 50 |
| 1.2 Dados Retangulares | `shape`, `.loc`, índice | `(27, 4)`; o exemplo do `.loc["CA"]` vira `.loc["SP"]` |
| 1.3 Estimativas de Localização | tudo | números, mediana n ímpar, ponderada invertida, widgets |
| 1.4 Estimativas de Variabilidade | desvio, IQR, MAD | números |
| 1.5 Distribuição dos Dados | percentis, boxplot, `pd.cut`, densidade | números; os outliers do boxplot mudam |

Os widgets OJS da 1.3 leem os dados via `ojs_define`, então acompanham a troca — mas o `d.State === "California"` vira `d.Sigla === "SP"`, e o teste Playwright precisa dos novos valores esperados.

## Verificação

- O pipeline falha alto se as três fontes não casarem em 27 UFs.
- `dados/estados.csv` tem 27 linhas e as 4 colunas em português.
- `dados/state.csv` não existe mais, e nenhum `.qmd` o referencia.
- `make render` gera as 42 páginas sem erro.
- Os novos números aparecem nas páginas, em formato brasileiro.
- O teste Playwright (`scripts/verifica-widgets.py`) passa com os valores brasileiros: na carga inicial a média do widget é `7.873.472,2`, e ao arrastar São Paulo para o extremo a média muda enquanto a mediana **não**.

## Fora de escopo

- Os demais datasets do livro (`dfw_airline`, `sp500`, `kc_tax`, `lc_loans`, `airline_stats`) continuam americanos. Trocá-los é outro projeto — e as seções 1.6 a 1.8 não foram pedidas.
- Mapas do Brasil (que justificariam o `geobr`).
- Séries históricas do Atlas (o CSV bruto tem 2000–2024; o livro usa só 2024).
