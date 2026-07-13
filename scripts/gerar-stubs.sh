#!/usr/bin/env bash
set -euo pipefail

gerar_stub() {
  local caminho="$1" titulo="$2" secao="$3"
  cat > "$caminho" <<EOF
# ${titulo}

::: {.callout-note}
Esta seção corresponde à seção ${secao} de @bruce2020.
:::

::: {.callout-warning}
## Em construção
O conteúdo desta seção ainda será escrito.
:::
EOF
  echo "ok  $caminho"
}

mkdir -p content/cap01 content/cap02 content/cap03 content/cap04

# Capítulo 1 — a seção 03 já existe e não é sobrescrita
gerar_stub content/cap01/01-dados-estruturados.qmd        "Elementos de Dados Estruturados"        "1.1"
gerar_stub content/cap01/02-dados-retangulares.qmd        "Dados Retangulares"                     "1.2"
gerar_stub content/cap01/04-estimativas-variabilidade.qmd "Estimativas de Variabilidade"           "1.4"
gerar_stub content/cap01/05-distribuicao-dados.qmd        "Explorando a Distribuição dos Dados"    "1.5"
gerar_stub content/cap01/06-dados-binarios-categoricos.qmd "Explorando Dados Binários e Categóricos" "1.6"
gerar_stub content/cap01/07-correlacao.qmd                "Correlação"                             "1.7"
gerar_stub content/cap01/08-duas-ou-mais-variaveis.qmd    "Explorando Duas ou Mais Variáveis"      "1.8"

# Capítulo 2
gerar_stub content/cap02/01-amostragem-aleatoria.qmd   "Amostragem Aleatória e Viés de Amostra"  "2.1"
gerar_stub content/cap02/02-vies-selecao.qmd           "Viés de Seleção"                         "2.2"
gerar_stub content/cap02/03-distribuicao-amostral.qmd  "Distribuição Amostral de uma Estatística" "2.3"
gerar_stub content/cap02/04-bootstrap.qmd              "Bootstrap"                               "2.4"
gerar_stub content/cap02/05-intervalos-confianca.qmd   "Intervalos de Confiança"                 "2.5"
gerar_stub content/cap02/06-distribuicao-normal.qmd    "Distribuição Normal"                     "2.6"
gerar_stub content/cap02/07-caudas-longas.qmd          "Distribuições de Cauda Longa"            "2.7"
gerar_stub content/cap02/08-distribuicao-t.qmd         "Distribuição t de Student"               "2.8"
gerar_stub content/cap02/09-distribuicao-binomial.qmd  "Distribuição Binomial"                   "2.9"
gerar_stub content/cap02/10-qui-quadrado.qmd           "Distribuição Qui-Quadrado"               "2.10"
gerar_stub content/cap02/11-distribuicao-f.qmd         "Distribuição F"                          "2.11"
gerar_stub content/cap02/12-poisson.qmd                "Distribuição de Poisson e Relacionadas"  "2.12"

# Capítulo 3
gerar_stub content/cap03/01-teste-ab.qmd               "Teste A/B"                               "3.1"
gerar_stub content/cap03/02-testes-hipotese.qmd        "Testes de Hipótese"                      "3.2"
gerar_stub content/cap03/03-reamostragem.qmd           "Reamostragem"                            "3.3"
gerar_stub content/cap03/04-significancia-valor-p.qmd  "Significância Estatística e Valores-p"   "3.4"
gerar_stub content/cap03/05-testes-t.qmd               "Testes t"                                "3.5"
gerar_stub content/cap03/06-testes-multiplos.qmd       "Testes Múltiplos"                        "3.6"
gerar_stub content/cap03/07-graus-liberdade.qmd        "Graus de Liberdade"                      "3.7"
gerar_stub content/cap03/08-anova.qmd                  "ANOVA"                                   "3.8"
gerar_stub content/cap03/09-teste-qui-quadrado.qmd     "Teste Qui-Quadrado"                      "3.9"
gerar_stub content/cap03/10-multi-armed-bandit.qmd     "Algoritmo Multi-Armed Bandit"            "3.10"
gerar_stub content/cap03/11-poder-tamanho-amostra.qmd  "Poder e Tamanho da Amostra"              "3.11"

# Capítulo 4
gerar_stub content/cap04/01-regressao-linear-simples.qmd  "Regressão Linear Simples"            "4.1"
gerar_stub content/cap04/02-regressao-linear-multipla.qmd "Regressão Linear Múltipla"           "4.2"
gerar_stub content/cap04/03-predicao.qmd                  "Predição com Regressão"              "4.3"
gerar_stub content/cap04/04-variaveis-fatoriais.qmd       "Variáveis Fatoriais na Regressão"    "4.4"
gerar_stub content/cap04/05-interpretando-equacao.qmd     "Interpretando a Equação de Regressão" "4.5"
gerar_stub content/cap04/06-diagnostico-regressao.qmd     "Diagnóstico de Regressão"            "4.6"
gerar_stub content/cap04/07-polinomial-splines.qmd        "Regressão Polinomial e Splines"      "4.7"

echo "---"
echo "stubs de seção criados: $(find content -name '*.qmd' ! -name 'index.qmd' | wc -l | tr -d ' ')"
