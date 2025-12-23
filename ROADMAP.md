# Durak Roadmap

## 1. Completed (v0.1.0 - v0.4.0)
- [x] **Define package scope**: document core capabilities (tokenisation, normalization, lemmatization, stopword handling, text cleaning, frequency stats) in `docs/overview.md`.
- [x] **Project skeleton**: scaffold `pyproject.toml`, `python/durak/__init__.py`, `README.md`, `tests/`, and tooling configs (`ruff`, `black`, `pytest`, coverage).
- [x] **Core cleaning utilities**: implement `python/durak/cleaning.py` with language-agnostic utilities (artifact removal, unicode normalization, casing, punctuation stripping) and Turkish-specific patterns.
- [x] **Stopword management**: add `python/durak/stopwords.py` with curated Turkish base list, file loaders, `StopwordManager`, serialization helpers, and usage guidance in `docs/design/stopwords.md`.
- [x] **Tokenizer module**: build `python/durak/tokenizer.py` with Rust-backed regex tokenization, offset tracking, and sentence splitting.
- [x] **Rust Core Migration (v0.3.0)**: Move performance-critical operations to Rust via PyO3/Maturin.
- [x] **Industry-Standard Architecture (v0.4.0)**: Refactor to separate Rust (src/) from Python (python/) with embedded resources (resources/tr/).

## 2. Active Development (v0.5.0)
- **Lemmatization architecture**:
  - Ship thin adapters for multiple backends: Zemberek (preferred), spaCy `tr_core_news_lg`, Stanza `tr` model.
  - Design `LemmaEngine` interface so downstream tasks can call `lemmatize(tokens)` while swapping implementations.
  - Evaluate feasibility of rule-based fallback for environments without Java/large models.
- **Morphological metadata**: expose POS tags, morphological features (case, person, tense) when the backend supports them; define schema in `docs/api_reference.md`.
- **Pipeline orchestration**: introduce a `TextProcessor` class (in `pipeline.py`) chaining cleaning → tokenisation → lemmatization → stopword filtering, configurable through dataclasses or Pydantic models.
- **Frequency & n-gram analysis**: modularise frequency counters (`stats/frequencies.py`) supporting unigram/bigram/trigram computation on raw and lemma tokens, with stopword toggles and searchable outputs.
- **CLI utilities**: add `durak` entry point (Typer/Click) for running preprocessing pipelines, generating stopword reports, and exporting cleaned corpora.

## 3. Testing & Quality (Ongoing)
- **Unit tests**: cover each module (cleaning, stopwords, tokenizer, lemma adapters, pipeline) using curated text fixtures reflecting Turkish morphology challenges (suffix chains, apostrophes, abbreviations).
- **Corpus validation**: maintain `tests/data/corpus_validator.py` and shared fixtures to enforce diacritic preservation, particle boundaries, and stopword correctness on sample corpora.
- **Regression suites**: maintain snapshot tests for frequency outputs and lemmatisation results to detect model/version drift; store fixtures under `tests/data/`.
- **Continuous Integration**: GitHub Actions pipeline running lint, tests, and type-checks on Python 3.9–3.12 and multiple OS targets.
- **Benchmark harness**: optional script to measure throughput/latency of different lemma backends to guide users on performance trade-offs.

## 4. Documentation (v0.4.0+)
- **User guides**: document common workflows—preparing corpora, integrating with ML pipelines, extending stopwords, swapping lemma engines—in `docs/usage/`.
- **API reference**: auto-generate API docs via `mkdocs` or `sphinx` to describe public classes/functions.
- **Developer handbook**: provide contribution guidelines, coding standards, and instructions for adding new linguistic resources.
- **Morphology insights**: dedicate a section explaining Turkish-specific considerations (vowel harmony, agglutination, apostrophe handling) and how the toolkit addresses them.
- **Changelog**: maintain `CHANGELOG.md` following Keep a Changelog for transparent version history.

## 5. Packaging & Release (v0.4.0+)
- **Semantic versioning**: start at `0.1.0`; document stability guarantees for public APIs/backends.
- **Build tooling**: use `python -m build`; sign and upload with `twine`; supply hash-checked release workflow in GitHub Actions.
- **Artifact checks**: include README badge, metadata (`project.urls`, classifiers for Turkish language support) in `pyproject.toml`.
- **Community standards**: add `LICENSE` (e.g., MIT), `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, issue/PR templates.
- **Model/resource management**: clarify licensing and download instructions for third-party lemma models (Zemberek jars, spaCy models).

## 6. Future Explorations (v1.0.0+)
- **Embeddings integration**: adapters for fastText, Word2Vec, and SentenceTransformers tuned for Turkish.
- **Advanced morphology**: explore finite-state transducer integration or neural morphological disambiguation for higher accuracy.
- **Downstream tasks**: ship reference notebooks for sentiment classification, topic modelling, and named entity recognition using the toolkit.
- **Dataset connectors**: helpers to ingest popular Turkish corpora (news, social media, parliamentary proceedings) with reproducible preprocessing.
- **Web service layer**: optional FastAPI microservice exposing preprocessing and lemma endpoints for application integration.
