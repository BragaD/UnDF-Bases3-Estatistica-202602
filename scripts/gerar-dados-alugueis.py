#!/usr/bin/env python3
"""Gera dados/alugueis.csv a partir do dataset "Brazilian houses to rent".

RODA UMA ÚNICA VEZ. Não é um chunk do livro: o aluno recebe o CSV pronto, em
português, e a mecânica de traduzir cabeçalhos não faz parte da lição.

Fonte:
  - "Brazilian houses to rent" (v2), publicado no Kaggle por rubenssjr, sob
    licença CC0 (domínio público). 10.692 imóveis para alugar em São Paulo,
    Rio de Janeiro, Belo Horizonte, Porto Alegre e Campinas.
    O CSV bruto está versionado em dados/brutos/houses_to_rent_v2.csv (o Kaggle
    exige login para baixar; sem o arquivo bruto, o pipeline não seria
    reproduzível).

O que este script faz — e o que ele NÃO faz de propósito:
  - Traduz os nomes das colunas e os valores das duas colunas binárias
    (acept/not acept → sim/não; furnished/not furnished → sim/não).
  - NÃO limpa a coluna `andar`: 23% das linhas trazem "-" (imóvel térreo ou
    casa sem andar), e é exatamente isso que faz o pandas ler a coluna inteira
    como texto. Essa "armadilha" é o objeto da atividade "Agora é com você" da
    seção 1.3 — o aluno precisa descobri-la, não recebê-la resolvida.
  - NÃO remove outliers (área de 46.335 m², condomínio de R$ 1.117.000): eles
    são o material de aula para média × mediana × média aparada.

Uso:  docker compose run --rm --no-deps livro python scripts/gerar-dados-alugueis.py
"""
import csv
from pathlib import Path

BRUTO = Path("dados/brutos/houses_to_rent_v2.csv")
SAIDA = Path("dados/alugueis.csv")

# Ordem original preservada. Nomes sem acento para não atrapalhar o pandas.
COLUNAS = {
    "city": "cidade",
    "area": "area_m2",
    "rooms": "quartos",
    "bathroom": "banheiros",
    "parking spaces": "vagas",
    "floor": "andar",
    "animal": "aceita_animal",
    "furniture": "mobiliado",
    "hoa (R$)": "condominio",
    "rent amount (R$)": "aluguel",
    "property tax (R$)": "iptu",
    "fire insurance (R$)": "seguro_incendio",
    "total (R$)": "total",
}

# Só as duas binárias têm valores traduzidos; o resto vai como está.
VALORES = {
    "aceita_animal": {"acept": "sim", "not acept": "não"},
    "mobiliado": {"furnished": "sim", "not furnished": "não"},
}


def traduzir(linha):
    nova = {novo: linha[antigo] for antigo, novo in COLUNAS.items()}
    for coluna, mapa in VALORES.items():
        nova[coluna] = mapa[nova[coluna]]  # KeyError = valor inesperado na fonte
    return nova


def main():
    with BRUTO.open(encoding="utf-8") as f:
        linhas = [traduzir(l) for l in csv.DictReader(f)]

    # Sanidade: os números que a seção 1.3 cita têm que bater com o bruto.
    assert len(linhas) == 10_692, len(linhas)
    assert sum(l["andar"] == "-" for l in linhas) == 2_461
    assert {l["aceita_animal"] for l in linhas} == {"sim", "não"}
    assert {l["mobiliado"] for l in linhas} == {"sim", "não"}

    with SAIDA.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(COLUNAS.values()))
        w.writeheader()
        w.writerows(linhas)
    print(f"{SAIDA}: {len(linhas)} linhas, {len(COLUNAS)} colunas")


if __name__ == "__main__":
    main()
