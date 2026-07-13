# Bases 3 — Estatística

Material de apoio da disciplina **Bases 3 — Estatística**, dos cursos de Engenharia de Software e Sistemas de Informação da UnDF.

O site é publicado automaticamente em
**<https://BragaD.github.io/UnDF-Bases3-Estatistica-202602>**

Os exemplos são em **Python**. O livro-texto é Bruce, Bruce & Gedeck, *Practical Statistics for Data Scientists* (2ª ed.), e a disciplina cobre seus **capítulos 1 a 4**.

## Rodando localmente

O único pré-requisito é **Docker**. Python, Quarto e todas as bibliotecas vêm dentro do container — você não instala nada disso na sua máquina.

```bash
git clone https://github.com/BragaD/UnDF-Bases3-Estatistica-202602
cd UnDF-Bases3-Estatistica-202602
make preview
```

Abra <http://localhost:4200>. O preview recarrega sozinho quando você salva um `.qmd`.

Outros comandos:

```bash
make render   # gera o livro em _book/
make shell    # shell dentro do container
make check    # diagnóstico do Quarto
make build    # reconstrói a imagem (após mudar Dockerfile ou uv.lock)
make clean    # limpa artefatos de render
```

Alternativa sem instalar nada: abra o repositório no **GitHub Codespaces** ou no VS Code com a extensão Dev Containers — o `.devcontainer/` já está configurado.

## Estrutura

```
.
├── _quarto.yml           # Config mestre: capítulos, tema, engine
├── index.qmd             # Página inicial
├── content/capNN/        # Um diretório por capítulo, um .qmd por seção
├── dados/                # Conjuntos de dados do livro-texto (caps. 1–4)
├── images/               # Logo da UnDF
├── styles.css            # Classes .conceito e .exemplo, dark mode
├── references.bib        # Bibliografia
├── Dockerfile            # Quarto + Python (via uv.lock)
├── compose.yaml          # Preview local
├── pyproject.toml        # Dependências Python
├── uv.lock               # Versões travadas
└── .github/workflows/    # CI: build da imagem → render → gh-pages
```

Todo arquivo novo em `content/` precisa ser registrado em `_quarto.yml` para aparecer no livro.

## Dados

Os conjuntos em `dados/` vêm do [repositório oficial do livro](https://github.com/gedeck/practical-statistics-for-data-scientists), com os nomes originais preservados. Veja `dados/README.md`.

## Licença

Material disponibilizado para fins educacionais. Os dados e exemplos originais são de autoria de Bruce, Bruce e Gedeck.
