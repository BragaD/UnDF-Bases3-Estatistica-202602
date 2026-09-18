"""Captura uma página do livro renderizado em desktop, celular e dark mode.

Usado pela skill /visual-audit. Roda dentro da imagem do Playwright (a mesma do
verifica-widgets.py), com _book/ montado em /site e a pasta de saída em /out:

    docker run --rm -v "$PWD/_book:/site:ro" -v "$PWD/scripts:/scripts:ro" \
      -v "$PWD/quality_reports:/out" mcr.microsoft.com/playwright/python:v1.61.0-noble \
      bash -c "pip install --quiet playwright==1.61.0 && \
               python /scripts/captura-pagina.py content/cap01/05-distribuicao-dados.html"

Grava /out/capturas/<pagina>-{desktop,celular,escuro}.png.
"""

import functools
import http.server
import os
import sys
import threading

from playwright.sync_api import sync_playwright


class Quieto(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    if len(sys.argv) != 2:
        sys.exit("uso: captura-pagina.py content/capNN/MM-nome.html")
    pagina = sys.argv[1]
    base = os.path.splitext(os.path.basename(pagina))[0]

    servidor = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 8765), functools.partial(Quieto, directory="/site")
    )
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    os.makedirs("/out/capturas", exist_ok=True)

    with sync_playwright() as p:
        navegador = p.chromium.launch()
        for nome, largura, escuro in [
            ("desktop", 1280, False),
            ("celular", 390, False),
            ("escuro", 1280, True),
        ]:
            pg = navegador.new_page(viewport={"width": largura, "height": 900})
            if escuro:
                # O Quarto guarda o toggle de tema no localStorage; prefers-color-scheme não basta.
                pg.add_init_script("localStorage.setItem('quarto-color-scheme', 'alternate')")
            pg.goto(f"http://127.0.0.1:8765/{pagina}")
            pg.wait_for_timeout(1500)  # widgets OJS e MathJax
            if escuro and not pg.evaluate("document.body.classList.contains('quarto-dark')"):
                print("aviso: dark mode não ativou", file=sys.stderr)
            destino = f"/out/capturas/{base}-{nome}.png"
            pg.screenshot(path=destino, full_page=True)
            print(destino)
        navegador.close()


if __name__ == "__main__":
    main()
