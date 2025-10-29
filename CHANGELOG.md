# Changelog

All notable changes to Durak will be documented here. This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

- Planned enhancements to lemmatization adapters and pipeline orchestration.

## [0.2.0] - 2025-10-26

- Promoted stopword utilities to the top-level API, including `remove_stopwords`,
  new `is_stopword` and `list_stopwords` helpers, and clearer metadata resource naming.
- Added `process_text` for an end-to-end clean → tokenize → stopword removal pipeline,
  plus `tokenize(..., strip_punct=True)` for punctuation-free token streams.
- Documented usage examples in key docstrings and README quickstart for faster adoption.
- Updated licensing to Durak License v1.2 and bumped package metadata to version 0.2.0.

## [0.1.0] - 2025-10-19

- Initial public release of the Durak NLP toolkit.
- Added text cleaning utilities with Turkish-specific heuristics.
- Shipped configurable stopword management and serialization helpers.
- Introduced regex-based tokenizer, sentence splitting, and corpus validator integration.
- Provided development tooling (pytest, ruff, mypy configs) and packaging metadata for TestPyPI/PyPI releases.

[Unreleased]: https://github.com/fbkaragoz/durak/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/fbkaragoz/durak/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fbkaragoz/durak/releases/tag/v0.1.0
