# scripts/verifica-widgets.py
"""Verifica no navegador que os widgets OJS da seção 1.3 funcionam de fato.

Roda dentro do container playwright (ver o comando no Step 2). Serve o _book/
por HTTP porque o Observable JS não carrega a partir de file://.
"""
import re
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

URL = "http://localhost:8000/content/cap01/03-estimativas-localizacao.html"

# Os mesmos números que o chunk Python imprime na página. Se o widget mostrar
# outra coisa na carga inicial, ele não está lendo os dados do livro.
MEDIA_REAL = "7.873.472,2"
MEDIANA_REAL = "4.145.040,0"

# As 27 unidades federativas. O estado mediano é a Paraíba — e a lista do widget
# de aparo deve deixá-lo como único sobrevivente quando o aparo chega a 50%.
N_ESTADOS = 27
ESTADO_MEDIANO = "PB"


def numeros_da_tabela(page):
    """Os três valores da tabela do Widget A, na ordem: média, aparada, mediana."""
    celulas = page.locator("table.table td strong").all_inner_texts()
    return [c.strip() for c in celulas]


def main():
    servidor = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000"],
        cwd="/site", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    falhas = []
    try:
        with sync_playwright() as p:
            nav = p.chromium.launch()
            page = nav.new_page()
            erros = []
            page.on("pageerror", lambda e: erros.append(str(e)))
            page.goto(URL, wait_until="networkidle")
            page.wait_for_selector("table.table td strong", timeout=20000)

            # 1. Os dois sliders existem?
            sliders = page.locator('input[type="range"]')
            n = sliders.count()
            print(f"sliders encontrados: {n}")
            if n < 2:
                falhas.append(f"esperava 2 sliders, achei {n}")

            # 1b. As caixas numéricas ao lado dos sliders estão preenchidas?
            #
            # O Inputs.range renderiza um <input type="number"> ao lado do slider.
            # Ele REJEITA qualquer string não numérica: um `format` customizado que
            # devolva "37,3 M" ou "10%" deixa a caixa VAZIA — silenciosamente, sem
            # erro de render. Foi o que aconteceu na primeira versão destes widgets.
            caixas = page.locator('input[type="number"]')
            valores_caixas = [caixas.nth(i).input_value() for i in range(caixas.count())]
            print(f"caixas numéricas: {valores_caixas}")
            if caixas.count() < 2:
                falhas.append(f"esperava 2 caixas numéricas, achei {caixas.count()}")
            for i, v in enumerate(valores_caixas):
                if not v:
                    falhas.append(
                        f"a caixa numérica {i} está VAZIA — provavelmente um `format` "
                        f"customizado no Inputs.range devolvendo string não numérica"
                    )

            # 2. Carga inicial: os números do widget batem com os do chunk Python?
            inicial = numeros_da_tabela(page)
            print(f"widget A na carga inicial: {inicial}")
            if not inicial or inicial[0] != MEDIA_REAL:
                falhas.append(f"média inicial do widget = {inicial[0] if inicial else '(vazio)'}, "
                              f"esperava {MEDIA_REAL} (o mesmo que o Python imprime)")
            if len(inicial) >= 3 and inicial[2] != MEDIANA_REAL:
                falhas.append(f"mediana inicial = {inicial[2]}, esperava {MEDIANA_REAL}")

            # 3. Mover o slider A muda a média — e NÃO move a mediana.
            sliders.nth(0).fill("300000000")
            sliders.nth(0).dispatch_event("input")
            page.wait_for_timeout(800)
            depois = numeros_da_tabela(page)
            print(f"widget A com SP em 300 M : {depois}")
            if depois == inicial:
                falhas.append("mover o slider A não mudou nada — o widget não é reativo")
            if len(depois) >= 3 and depois[2] != MEDIANA_REAL:
                falhas.append(f"a mediana MUDOU para {depois[2]} — deveria ser robusta ao outlier")
            if len(depois) >= 1 and depois[0] == MEDIA_REAL:
                falhas.append("a média NÃO mudou — deveria perseguir o outlier")

            # 3b. A caixa numérica acompanhou o arrasto do slider?
            caixa_a = caixas.nth(0).input_value()
            print(f"caixa do slider A após arrastar: {caixa_a!r}")
            if caixa_a != "300000000":
                falhas.append(f"a caixa do slider A mostra {caixa_a!r}, esperava '300000000' "
                              f"— ela não está acompanhando o slider")

            # 4. A lista de estados do widget B: ordenada, e os cortados vêm das
            #    duas pontas. Com aparo 0% ninguém é cortado; com 10%, dois de
            #    cada ponta (int(27 × 0,1) = 2).
            itens = page.locator(".aparo-item")
            print(f"estados na lista do aparo: {itens.count()}")
            if itens.count() != N_ESTADOS:
                falhas.append(f"a lista tem {itens.count()} estados, esperava {N_ESTADOS}")

            siglas = [s.strip() for s in page.locator(".aparo-item .sigla").all_inner_texts()]
            if siglas and (siglas[0] != "RR" or siglas[-1] != "SP"):
                falhas.append(
                    f"a lista não está ordenada por população: começa em {siglas[0]} "
                    f"e termina em {siglas[-1]} — esperava RR (menor) ... SP (maior)"
                )

            for aparo, k in [(0, 0), (10, 2)]:
                sliders.nth(1).fill(str(aparo))
                sliders.nth(1).dispatch_event("input")
                page.wait_for_timeout(500)
                vermelhos = page.locator(".aparo-item.cortado").count()
                if vermelhos != 2 * k:
                    falhas.append(
                        f"com aparo {aparo}%, {vermelhos} estados em vermelho — esperava {2 * k}"
                    )

            # 5. Slider B em 50%: a média aparada tem que pousar na mediana, e na
            #    lista deve sobrar UM único estado — o mediano (a Paraíba). É a
            #    definição "aparar 50% = mediana" acontecendo na tela.
            sliders.nth(1).fill("50")
            sliders.nth(1).dispatch_event("input")
            page.wait_for_timeout(800)
            texto = page.inner_text("body")
            if MEDIANA_REAL not in texto:
                falhas.append(f"com aparo 50%, não achei a mediana ({MEDIANA_REAL}) na página")
            else:
                print(f"widget B com aparo 50%: média aparada pousou em {MEDIANA_REAL}")

            sobreviventes = [
                page.locator(".aparo-item .sigla").nth(i).inner_text().strip()
                for i in range(itens.count())
                if "cortado" not in (itens.nth(i).get_attribute("class") or "")
            ]
            print(f"com aparo 50%, sobrevive(m): {sobreviventes}")
            if sobreviventes != [ESTADO_MEDIANO]:
                falhas.append(
                    f"com aparo 50% sobrou {sobreviventes}, esperava só ['{ESTADO_MEDIANO}'] "
                    f"— aparar 50% descarta tudo menos o estado mediano"
                )

            # 6. Nenhum erro de JavaScript.
            if erros:
                falhas.append(f"erros de JS na página: {erros[:3]}")

            nav.close()
    finally:
        servidor.terminate()

    print()
    if falhas:
        print("FALHOU:")
        for f in falhas:
            print("  -", f)
        sys.exit(1)
    print("OK — os dois widgets carregam, são reativos e batem com os números do livro")


if __name__ == "__main__":
    main()
