# Durak

<p align="center">
  <img src="docs/durak.svg" alt="Durak logo" width="200" />
</p>

Durak is a Turkish natural language processing toolkit focused on reliable preprocessing building blocks. It offers configurable cleaning, tokenisation, stopword management, lemmatisation adapters, and frequency statistics so projects can bootstrap robust text pipelines quickly.

- Personal homepage: [karagoz.io](https://karagoz.io)
- Source repository: [github.com/fbkaragoz/durak](https://github.com/fbkaragoz/durak)

## Getting Started

Durak is under active development. The first public release will provide:

- Unicode-aware cleaning functions tuned for Turkish data sources.
- Tokenisation strategies ranging from regex to pluggable subword engines.
- Stopword curation helpers with domain-specific override support.
- Pluggable lemmatisation interface with adapters for Zemberek, spaCy, and Stanza.
- Frequency statistics utilities for exploratory corpus analysis.

## Contributing

1. Create a virtual environment (`conda activate nlp.env` or `python -m venv .venv`).
2. Install development dependencies: `pip install -e .[dev]`.
3. Run the test suite: `pytest`.

Roadmap and task planning live in `ROADMAP.md`. Update the roadmap as you make progress if you want to contribute.
