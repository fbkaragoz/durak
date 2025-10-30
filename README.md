# Durak

[![PyPI](https://img.shields.io/pypi/v/durak-nlp.svg)](https://pypi.org/project/durak-nlp/)
[![Python Versions](https://img.shields.io/pypi/pyversions/durak-nlp.svg)](https://pypi.org/project/durak-nlp/)
[![Tests](https://github.com/fbkaragoz/durak/actions/workflows/tests.yml/badge.svg)](https://github.com/fbkaragoz/durak/actions/workflows/tests.yml)
[![License](https://img.shields.io/badge/license-Durak%201.2-blue.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17477942.svg)](https://doi.org/10.5281/zenodo.17477942)

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
from durak import clean_text, process_text, tokenize, remove_stopwords

text = "Bu bir test. Durak kolaylaştırır."
tokens = tokenize(clean_text(text))
print(tokens)
# ['bu', 'bir', 'test', '.', 'durak', 'kolaylaştırır', '.']

filtered = remove_stopwords(tokens)
print(filtered)
# ['test', '.', 'durak', 'kolaylaştırır', '.']

processed = process_text(text, remove_stopwords=True)
print(processed)
# ['test', '.', 'durak', 'kolaylaştırır', '.']

# Repair detached suffix tokens (e.g., `Ankara ' da` → `ankara'da`) on demand:
suffix_fixed = process_text(
    "Ankara ' da kaldım ya",
    rejoin_suffixes=True,
    remove_stopwords=True,
)
print(suffix_fixed)
# ['ankara\'da', 'kaldım']
```

Need a quick lookup? `is_stopword("ve")` returns `True`, while `list_stopwords()[:5]` reveals the first few entries of the curated base set.

## Features

- Unicode-aware cleaning utilities tuned for Turkish content (social, news, informal text).
- Configurable stopword management with keep-lists, custom additions, `is_stopword`, and `list_stopwords` helpers.
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
- Topics: `turkish-nlp`, `nlp`, `tokenization`, `lemmatization`, `text-processing`, `pre-processing`, `python`

## License

Durak is distributed under the [Durak License v1.2](LICENSE). Commercial or institutional use requires explicit written permission from the author.
