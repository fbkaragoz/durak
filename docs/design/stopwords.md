# Stopword Management Design

Objectives:

- Provide a curated Turkish stopword list sourced from permissive public datasets (e.g., Snowball/stopwords-iso) and manual curation.
- Allow projects to extend the list with domain-specific additions while preserving the base list for reuse.
- Support explicit keep-lists so critical terms remain even if they appear in the base list.
- Enable serialization and deserialization to share tailored stopword sets across projects.

Key APIs:

- `DEFAULT_STOPWORD_RESOURCE`: identifier for the curated Turkish base list (`"base/turkish"`).
- `BASE_STOPWORDS`: frozen set populated from the metadata-backed base resource.
- `load_stopword_resource(name, *, metadata_path=None, case_sensitive=False) -> set[str]`: resolve a named resource (with `extends` support) under `resources/tr/stopwords/`.
- `load_stopwords(path: Path | str) -> set[str]`: read stopwords from newline-delimited files (UTF-8) with optional case normalisation.
- `remove_stopwords(tokens, *, manager=None, base=None, additions=None, keep=None, case_sensitive=None) -> list[str]`: convenience helper that filters iterable tokens, optionally reusing a `StopwordManager`.
- `is_stopword(token, *, resource=None, metadata_path=None, case_sensitive=False) -> bool`: quick membership check against the base or a named resource.
- `list_stopwords(*, resource=None, metadata_path=None, case_sensitive=False, sort=True) -> list[str]`: introspection helper returning the stopword vocabulary for exploration or debugging.
- `process_text(text, *, remove_stopwords=False, rejoin_suffixes=False, ...) -> list[str]`: full-pipeline helper that chains cleaning, tokenization, suffix reattachment, and optional stopword removal.
- `StopwordManager`:
  - Initialization parameters: `base`, `additions`, `keep`, `case_sensitive`.
  - Constructors: `from_files(...)`, `from_resources(names, *, metadata_path=None, ...)`.
  - Methods: `is_stopword(token)`, `add(words)`, `remove(words)`, `export(path, format="txt")`, `to_dict()`.
  - Properties: `.stopwords` (read-only view), `.keep_words`.

Resource layout (v0.4.0+):

- Metadata lives in `resources/tr/stopwords/metadata.json` alongside the resource files.
- Each entry under `"sets"` must define:
  - `file`: path relative to `resources/tr/stopwords/`.
  - `description`: short human-readable summary.
  - `language`: ISO language tag (e.g. `"tr"`).
  - Optional `extends`: sequence of other resource identifiers to merge.
- Base lists reside in `resources/tr/stopwords/base/`, domain-specific additions under `resources/tr/stopwords/domains/`.
- **Rust Embedded Resources**: Stopwords are compiled into the binary at build time using `include_str!` for zero-overhead loading.
- **Dual Loading Strategy**: Python code can load from files (development) or from embedded Rust resources (production).
- Resources are loaded lazily and cached; paths are validated to remain inside the stopword data directory.
- Legacy identifiers prefixed with `"tr/"` remain as metadata aliases so existing integrations continue to resolve.

Testing scenarios:

- Default manager identifies base stopwords but honours keep words.
- Additional stopwords from files and iterables merge correctly; duplicates handled.
- `BASE_STOPWORDS` must stay in sync with the underlying `"base/turkish"` resource.
- Resource inheritance merges parent sets and detects circular `extends`.
- Case-insensitive mode normalises tokens via Turkish lowercasing from `cleaning.normalize_case`.
- Serialization roundtrip to temporary files retains stopwords and keeps duplicates suppressed.
- Ensure newline and whitespace trimming when loading files.
