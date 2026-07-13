FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ARG QUARTO_VERSION=1.9.38
ARG TARGETARCH

ENV DEBIAN_FRONTEND=noninteractive \
    LANG=pt_BR.UTF-8 \
    LC_ALL=pt_BR.UTF-8 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    QUARTO_PYTHON=/opt/venv/bin/python \
    MPLBACKEND=Agg

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git locales \
    && sed -i '/^# *pt_BR.UTF-8/s/^# *//' /etc/locale.gen \
    && locale-gen \
    && curl -fsSL -o /tmp/quarto.deb \
        "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-${TARGETARCH}.deb" \
    && apt-get install -y --no-install-recommends /tmp/quarto.deb \
    && rm -f /tmp/quarto.deb \
    && rm -rf /var/lib/apt/lists/*

# Um shell de login recarrega /etc/profile, que reescreve o PATH e descarta o
# ENV PATH acima — deixando `python` apontar para o interpretador do sistema em
# vez do venv. Isto garante o venv também em `bash -l` e `docker exec -it`.
RUN echo 'export PATH="/opt/venv/bin:$PATH"' > /etc/profile.d/venv.sh

WORKDIR /livro

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --frozen

EXPOSE 4200

CMD ["quarto", "preview", "--host", "0.0.0.0", "--port", "4200", "--no-browser"]
