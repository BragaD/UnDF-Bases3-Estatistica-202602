"""Formatação numérica no padrão brasileiro.

O `f"{x:,.1f}"` do Python usa o padrão americano (vírgula de milhar, ponto
decimal). Este livro é em português, então os números saem invertidos:
6.162.876,3 e não 6,162,876.3.
"""


def num(x, casas=1):
    """Formata um número no padrão brasileiro.

    >>> num(6162876.3)
    '6.162.876,3'
    >>> num(6162876.3, 0)
    '6.162.876'
    >>> num(4.4458, 4)
    '4,4458'
    """
    s = f"{x:,.{casas}f}"
    # troca os separadores usando um marcador intermediário, para não
    # sobrescrever o que acabou de ser trocado
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
