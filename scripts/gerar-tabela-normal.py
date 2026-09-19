"""Gera downloads/tabela-normal-padrao.pdf, a tabela da normal padrão usada no Cap. 4.

A tabela dá Phi(z) = P(Z <= z) para z de 0,00 a 3,49: a linha é o z até a primeira
casa decimal, e a coluna é a segunda casa. Roda uma vez; o PDF é commitado e servido
pelo site (project.resources no _quarto.yml).

    .venv/bin/python scripts/gerar-tabela-normal.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

SAIDA = Path(__file__).resolve().parent.parent / "downloads" / "tabela-normal-padrao.pdf"


def virgula(valor, casas):
    return f"{valor:.{casas}f}".replace(".", ",")


def main():
    linhas = np.round(np.arange(0.0, 3.5, 0.1), 1)
    colunas = np.round(np.arange(0.0, 0.1, 0.01), 2)
    celulas = [[virgula(stats.norm.cdf(z + c), 4) for c in colunas] for z in linhas]
    rotulos_linha = [virgula(z, 1) for z in linhas]
    rotulos_coluna = [virgula(c, 2) for c in colunas]

    fig = plt.figure(figsize=(8.27, 11.69))   # A4 em retrato

    # Título e desenho da área Phi(z)
    fig.text(0.5, 0.955, "Tabela da normal padrão", ha="center", fontsize=16, weight="bold")
    fig.text(0.5, 0.93, r"$\Phi(z) = P(Z \leq z)$, com $Z \sim N(0, 1)$", ha="center", fontsize=12)

    ax_curva = fig.add_axes([0.35, 0.80, 0.30, 0.11])
    x = np.linspace(-3.5, 3.5, 400)
    ax_curva.plot(x, stats.norm.pdf(x), color="black", linewidth=1)
    zona = x <= 1.0
    ax_curva.fill_between(x[zona], stats.norm.pdf(x[zona]), color="0.75")
    ax_curva.set_xticks([0, 1])
    ax_curva.set_xticklabels(["0", "z"])
    ax_curva.set_yticks([])
    for lado in ("top", "right", "left"):
        ax_curva.spines[lado].set_visible(False)

    # Tabela
    ax = fig.add_axes([0.11, 0.10, 0.83, 0.67])
    ax.axis("off")
    tabela = ax.table(
        cellText=celulas,
        rowLabels=rotulos_linha,
        colLabels=rotulos_coluna,
        loc="upper center",
        cellLoc="center",
    )
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8.5)
    tabela.scale(1, 1.18)
    for (linha, coluna), celula in tabela.get_celld().items():
        celula.set_linewidth(0.3)
        if linha == 0 or coluna == -1:
            celula.set_text_props(weight="bold")
            celula.set_facecolor("0.9")
        elif linha % 2 == 0:
            celula.set_facecolor("0.97")

    fig.text(
        0.08, 0.075,
        "Linha: z até a primeira casa decimal. Coluna: segunda casa decimal.\n"
        "Exemplo: z = 1,73 fica na linha 1,7 e na coluna 0,03, e dá Φ(1,73) = 0,9582.\n"
        "Para z negativo, use a simetria: Φ(−z) = 1 − Φ(z). Para z ≥ 3,5, Φ(z) é maior que 0,9997 (na prática, use 1).",
        fontsize=8.5, va="top",
    )
    fig.text(0.94, 0.015, "Bases 3: Estatística (UnDF)", ha="right", fontsize=7, color="0.4")

    SAIDA.parent.mkdir(exist_ok=True)
    fig.savefig(SAIDA)
    print(f"gravado: {SAIDA}")


if __name__ == "__main__":
    main()
