# Changelog

All notable changes to Durak will be documented here. This project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

- Planned enhancements to lemmatization adapters and pipeline orchestration.

## [0.3.0] - 2025-12-23

### Added
- **Rust Core Engine ("Iron Core")**: Migrated performance-critical linguistic logic to Rust via PyO3/Maturin for significant speed improvements.
- **`Pipeline` class**: A modular, PyTorch-style component chaining system for building custom NLP pipelines.
- **`Normalizer` class**: Rust-backed Turkish text normalization with proper handling of İ/ı case transformations.
- **`Lemmatizer` class**: Multi-tier lemmatization with dictionary lookup and heuristic suffix stripping strategies.
- **`tokenize_with_offsets()`**: Character-accurate offset mapping for NER and span-based tasks.
- **Improved Tokenizer**: Rust-backed regex tokenization with configurable punctuation handling.

### Changed
- **License**: Switched to MIT license for broader compatibility.
- **Build System**: Now uses Maturin for building Rust+Python hybrid packages.
- **CI/CD**: Updated GitHub Actions workflows with proper Rust toolchain support and trusted publishing.

### Fixed
- Fixed GitHub Actions workflow using incorrect action name (`rust-action` → `rust-toolchain`).
- Fixed line-too-long linting errors in suffix handling.
- Fixed mypy type errors for optional Rust extension imports.

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

[Unreleased]: https://github.com/fbkaragoz/durak/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/fbkaragoz/durak/compare/v0.2.4...v0.3.0
[0.2.4]: https://github.com/fbkaragoz/durak/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/fbkaragoz/durak/compare/v0.2.2...v0.2.3
[0.2.0]: https://github.com/fbkaragoz/durak/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/fbkaragoz/durak/releases/tag/v0.1.0

