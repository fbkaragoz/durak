# Changelog

All notable changes to Durak will be documented here. This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

- Planned enhancements to lemmatization adapters and pipeline orchestration.

## [0.2.4] - 2025-10-30

### Fixed
- Synced packaged stopword data with the expanded list so reattached tokens like "var" and "bi" are filtered consistently across installs.
- Added regression coverage ensuring stopword removal runs after suffix reattachment in the pipeline.
- Augmented the base stopword list with conversational tokens such as "öyle" highlighted by renewed corpus analysis.

### Changed
- Clarified README quickstart with explicit pipeline order, suffix reattachment guidance, and modular usage examples.

## [0.2.3] - 2025-10-29

### Added
- Introduced optional suffix reattachment in `process_text` (`rejoin_suffixes`) and exposed `attach_detached_suffixes` for manual pipelines to stabilise noisy corpora.

### Changed
- Expanded the base Turkish stopword list with apostrophe-prefixed and suffix-oriented variants to better capture colloquial usage.

## [0.2.2] - 2025-10-29

### Fixed
- Fixed CITATION.cff format for Zenodo DOI generation
- Added required `type: software` field
- Changed license format to "Other" for custom licenses
- Added keywords for better discoverability
- Standardized citation metadata structure

## [0.2.0] - 2025-10-29

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

[Unreleased]: https://github.com/fbkaragoz/durak/compare/v0.2.4...HEAD
[0.2.4]: https://github.com/fbkaragoz/durak/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/fbkaragoz/durak/compare/v0.2.2...v0.2.3
[0.2.0]: https://github.com/fbkaragoz/durak/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fbkaragoz/durak/releases/tag/v0.1.0
