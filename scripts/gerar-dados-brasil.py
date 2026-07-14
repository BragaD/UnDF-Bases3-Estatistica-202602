#!/usr/bin/env python3
"""Gera dados/estados.csv a partir de três fontes públicas.

RODA UMA ÚNICA VEZ. Não é um chunk do livro: o aluno não precisa ver a mecânica
de juntar três fontes para aprender o que é uma mediana, e um livro que faz duas
chamadas de rede a cada render é frágil e lento.

Fontes:
  - Taxa de homicídios 2024 — Atlas da Violência (Ipea/FBSP).
    O CSV bruto está versionado em dados/brutos/ porque a API do Atlas saiu do ar
    na reformulação do site (v3): /atlasviolencia/api/v1/... hoje devolve HTML.
  - População 2024 — IBGE, SIDRA tabela 6579, variável 9324.
  - Nome e sigla — IBGE, API de localidades.

Uso:  docker compose run --rm --no-deps livro python scripts/gerar-dados-brasil.py
"""
import csv
import gzip
import json
import urllib.request
from pathlib import Path

ANO = 2024
BRUTO = Path("dados/brutos/atlas-violencia-taxa-homicidios.csv")
SAIDA = Path("dados/estados.csv")

URL_POP = f"https://apisidra.ibge.gov.br/values/t/6579/n3/all/v/9324/p/{ANO}"
URL_UFS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"


def baixar_json(url):
    # A API do IBGE às vezes devolve o corpo comprimido em gzip mesmo quando o
    # urllib pede "Accept-Encoding: identity" (comportamento do servidor, não
    # do cliente) — sem isso o json.load falha com UnicodeDecodeError.
    with urllib.request.urlopen(url, timeout=60) as r:
        dados = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            dados = gzip.decompress(dados)
        return json.loads(dados)


def ler_taxas():
    """{codigo_ibge: taxa} para o ano alvo, do CSV do Atlas."""
    with BRUTO.open(encoding="utf-8-sig") as f:
        return {
            int(linha["Região ID"]): float(linha["Valor"])
            for linha in csv.DictReader(f)
            if linha["Período"].startswith(str(ANO))
        }


def ler_populacao():
    """{codigo_ibge: habitantes}. A primeira linha do SIDRA é cabeçalho."""
    return {int(r["D1C"]): int(r["V"]) for r in baixar_json(URL_POP)[1:]}


def ler_ufs():
    """{codigo_ibge: (nome, sigla)}."""
    return {uf["id"]: (uf["nome"], uf["sigla"]) for uf in baixar_json(URL_UFS)}


def main():
    taxas, populacao, ufs = ler_taxas(), ler_populacao(), ler_ufs()

    # Falhar alto, não silenciosamente: um estado faltante viraria um NaN no meio
    # de uma estatística do livro, e ninguém perceberia.
    if not (set(taxas) == set(populacao) == set(ufs)):
        raise SystemExit(
            "As três fontes não casam.\n"
            f"  taxas    : {len(taxas)} UFs\n"
            f"  população: {len(populacao)} UFs\n"
            f"  ufs      : {len(ufs)} UFs\n"
            f"  só nas taxas    : {sorted(set(taxas) - set(populacao) - set(ufs))}\n"
            f"  só na população : {sorted(set(populacao) - set(taxas))}\n"
            f"  só nas ufs      : {sorted(set(ufs) - set(taxas))}"
        )
    if len(ufs) != 27:
        raise SystemExit(f"Esperava 27 unidades federativas, encontrei {len(ufs)}.")

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f, ["Estado", "Populacao", "Taxa.Homicidios", "Sigla"],
            quoting=csv.QUOTE_NONNUMERIC,
        )
        w.writeheader()
        for codigo in sorted(ufs):
            nome, sigla = ufs[codigo]
            w.writerow({
                "Estado": nome,
                "Populacao": populacao[codigo],
                "Taxa.Homicidios": taxas[codigo],
                "Sigla": sigla,
            })

    print(f"{SAIDA}: {len(ufs)} unidades federativas, ano {ANO}")


if __name__ == "__main__":
    main()
