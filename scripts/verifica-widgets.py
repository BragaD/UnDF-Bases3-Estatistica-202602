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

URL_DISPERSAO = "http://localhost:8000/content/cap01/04-estimativas-variabilidade.html"

# A média da taxa, que o widget da 1.4 NÃO pode mover — é o ponto da seção.
MEDIA_TAXA = "22,7"

URL_AMOSTRAL = "http://localhost:8000/content/cap02/03-distribuicao-amostral.html"


def verifica_dispersao(nav, falhas):
    """O widget da 1.4: mexer no desvio não move a média, e os eixos não se mexem."""
    page = nav.new_page()
    erros = []
    page.on("pageerror", lambda e: erros.append(str(e)))
    page.goto(URL_DISPERSAO, wait_until="networkidle")
    page.wait_for_selector('input[type="range"]', timeout=20000)

    slider = page.locator('input[type="range"]').first
    caixa = page.locator('input[type="number"]').first
    print(f"widget 1.4 — caixa do slider: {caixa.input_value()!r}")
    if not caixa.input_value():
        falhas.append("a caixa do slider da 1.4 está VAZIA — um `format` customizado?")

    def eixos_e_media():
        """Os rótulos do eixo x, os do eixo y, e o texto da média."""
        svg = page.locator("svg").last
        rotulos = svg.locator("text").all_inner_texts()
        corpo = page.inner_text("body")
        return rotulos, MEDIA_TAXA in corpo

    rot_ini, tem_media = eixos_e_media()
    if not tem_media:
        falhas.append(f"não achei a média ({MEDIA_TAXA}) na página da 1.4")

    # Mover o desvio de ponta a ponta NÃO pode mudar os eixos nem a média.
    for valor in ["4", "11.8"]:
        slider.fill(valor)
        slider.dispatch_event("input")
        page.wait_for_timeout(600)
        rot, tem_media = eixos_e_media()
        if rot != rot_ini:
            falhas.append(
                f"com desvio {valor}, os rótulos dos eixos MUDARAM — eles deveriam "
                f"estar travados, senão o gráfico mascara o efeito"
            )
        if not tem_media:
            falhas.append(f"com desvio {valor}, a média deixou de ser {MEDIA_TAXA} — "
                          f"a transformação deveria preservá-la")

    print("widget 1.4: eixos travados e média imóvel de ponta a ponta do slider")
    if erros:
        falhas.append(f"erros de JS na página 1.4: {erros[:2]}")
    page.close()


def verifica_distribuicao_amostral(nav, falhas):
    """O widget da 2.3: aumentar n estreita a distribuição (erro padrão cai) e
    o eixo X fica travado."""
    page = nav.new_page()
    erros = []
    page.on("pageerror", lambda e: erros.append(str(e)))
    page.goto(URL_AMOSTRAL, wait_until="networkidle")
    page.wait_for_selector('input[type="range"]', timeout=20000)

    slider = page.locator('input[type="range"]').first
    caixa = page.locator('input[type="number"]').first
    if not caixa.input_value():
        falhas.append("a caixa do slider da 2.3 está VAZIA — um `format` customizado?")

    def rotulos_x():
        # Escopo só no grupo do eixo X (aria-label do Observable Plot) — o eixo Y
        # não é travado (a frequência muda muito de forma com n) e um seletor
        # genérico por "svg text" pegaria os dois, dando falso positivo.
        # `all_text_contents()`, não `all_inner_texts()`: SVG <text> não implementa
        # `innerText` no Chromium (é uma API de HTMLElement), então `all_inner_texts()`
        # devolve só `None` para cada rótulo — comparar `None == None` sempre "bate",
        # mas por acidente, não porque os rótulos de fato coincidiram.
        return page.locator("svg").last.locator(
            'g[aria-label="x-axis tick label"] text'
        ).all_text_contents()

    rot0 = rotulos_x()

    slider.fill("5"); slider.dispatch_event("input"); page.wait_for_timeout(600)
    ep_baixo_n = page.inner_text("body")

    slider.fill("100"); slider.dispatch_event("input"); page.wait_for_timeout(600)
    ep_alto_n = page.inner_text("body")
    rot1 = rotulos_x()

    if not rot0 or rot1 != rot0:
        falhas.append("os rótulos do eixo X mudaram ao mexer no slider da 2.3 — o eixo deveria estar travado")

    # O erro padrão em n=100 deve ser MENOR que em n=5. A frase-âncora
    # "(o desvio das médias) é" é exclusiva do texto reativo do widget — a prosa
    # da seção usa "erro padrão" várias vezes antes dele (é o conceito da seção),
    # e um regex sem âncora captura a primeira ocorrência qualquer, inclusive
    # dígitos do CÓDIGO-FONTE exibido no chunk `erro-padrao` (ex.: o "1" de
    # `ddof=1`), sem relação nenhuma com o valor do widget.
    def ep(txt):
        m = re.search(r"erro padrão \(o desvio das médias\) é\s*([\d.]+)", txt)
        return int(m.group(1).replace(".", "")) if m else None
    e5, e100 = ep(ep_baixo_n), ep(ep_alto_n)
    print(f"widget 2.3: erro padrão n=5 → {e5}, n=100 → {e100}")
    if e5 is None or e100 is None:
        falhas.append("não consegui ler o erro padrão exibido no widget da 2.3")
    elif not (e100 < e5):
        falhas.append(f"o erro padrão NÃO caiu: n=5 deu {e5}, n=100 deu {e100} — o TCL não está sendo mostrado")

    if erros:
        falhas.append(f"erros de JS na página 2.3: {erros[:2]}")
    page.close()


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

            verifica_dispersao(nav, falhas)
            verifica_distribuicao_amostral(nav, falhas)

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
