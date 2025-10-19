# Durak

[![PyPI](https://img.shields.io/pypi/v/durak-nlp.svg)](https://pypi.org/project/durak-nlp/)
[![Python Versions](https://img.shields.io/pypi/pyversions/durak-nlp.svg)](https://pypi.org/project/durak-nlp/)
[![Tests](https://github.com/fbkaragoz/durak/actions/workflows/tests.yml/badge.svg)](https://github.com/fbkaragoz/durak/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-Durak%201.1-blue.svg)](LICENSE)

<p align="center">
  <img src="https://raw.githubusercontent.com/fbkaragoz/durak/main/docs/durak.svg" alt="Durak logo" width="200" />
</p>

Durak is a Turkish natural language processing toolkit focused on reliable preprocessing building blocks. It offers configurable cleaning, tokenisation, stopword management, lemmatisation adapters, and frequency statistics so projects can bootstrap robust text pipelines quickly.

- Homepage: [karagoz.io](https://karagoz.io)
- Repository: [github.com/fbkaragoz/durak](https://github.com/fbkaragoz/durak)
- Issue tracker: [github.com/fbkaragoz/durak/issues](https://github.com/fbkaragoz/durak/issues)

## Quickstart

Install from PyPI:

```bash
pip install durak-nlp
```

Clean and tokenize Turkish text in seconds:

```python
from durak import clean_text, tokenize

text = "Türkiye'de NLP zor mu? Durak kolaylaştırır."
tokens = tokenize(clean_text(text))
print(tokens)
# ['türkiye'de', 'nlp', 'zor', 'mu', '?', 'durak', 'kolaylaştırır', '.']
```

## Features

- Unicode-aware cleaning utilities tuned for Turkish content (social, news, informal text).
- Configurable stopword management with keep-lists, custom additions, and serialization.
- Regex-based tokenizer and sentence splitter with clitic and diacritic preservation.
- Lightweight corpus validator to guard Turkish-specific artefacts.
- Ready for extension with future lemmatization and subword adapters.

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

Before submitting changes, run:

```bash
ruff check .
mypy src
pytest
```

Refer to [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow, coding standards, and release process. The project roadmap lives in [ROADMAP.md](ROADMAP.md), and notable changes are tracked in [CHANGELOG.md](CHANGELOG.md).

## Community & Support

- Code of Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Citation guidance: [CITATION.cff](CITATION.cff)
- Topics: `turkish-nlp`, `nlp`, `tokenization`, `lemmatization`, `text-processing`, `python`

## License

Durak is distributed under the [Durak License v1.1](LICENSE). Commercial or institutional use requires explicit written permission from the author.
