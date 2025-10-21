# Stopword Management Design

Objectives:

- Provide a curated Turkish stopword list sourced from permissive public datasets (e.g., Snowball/stopwords-iso) and manual curation.
- Allow projects to extend the list with domain-specific additions while preserving the base list for reuse.
- Support explicit keep-lists so critical terms remain even if they appear in the base list.
- Enable serialization and deserialization to share tailored stopword sets across projects.

Key APIs:

- `DEFAULT_STOPWORD_RESOURCE`: identifier for the curated Turkish base list (`"tr/base"`).
- `BASE_STOPWORDS`: frozen set populated from the metadata-backed base resource.
- `load_stopword_resource(name, *, metadata_path=None, case_sensitive=False) -> set[str]`: resolve a named resource (with `extends` support) under `data/stopwords/`.
- `load_stopwords(path: Path | str) -> set[str]`: read stopwords from newline-delimited files (UTF-8) with optional case normalisation.
- `StopwordManager`:
  - Initialization parameters: `base`, `additions`, `keep`, `case_sensitive`.
  - Constructors: `from_files(...)`, `from_resources(names, *, metadata_path=None, ...)`.
  - Methods: `is_stopword(token)`, `add(words)`, `remove(words)`, `export(path, format="txt")`, `to_dict()`.
  - Properties: `.stopwords` (read-only view), `.keep_words`.

Resource layout:

- Metadata lives in `data/stopwords/metadata.json` alongside the resource files.
- Each entry under `"sets"` must define:
  - `file`: path relative to `data/stopwords/`.
  - `description`: short human-readable summary.
  - `language`: ISO language tag (e.g. `"tr"`).
  - Optional `extends`: sequence of other resource identifiers to merge.
- Base lists reside in `data/stopwords/base/`, domain-specific additions under `data/stopwords/domains/`.
- Resources are loaded lazily and cached; paths are validated to remain inside the stopword data directory.

Testing scenarios:

- Default manager identifies base stopwords but honours keep words.
- Additional stopwords from files and iterables merge correctly; duplicates handled.
- `BASE_STOPWORDS` must stay in sync with the underlying `"tr/base"` resource.
- Resource inheritance merges parent sets and detects circular `extends`.
- Case-insensitive mode normalises tokens via Turkish lowercasing from `cleaning.normalize_case`.
- Serialization roundtrip to temporary files retains stopwords and keeps duplicates suppressed.
- Ensure newline and whitespace trimming when loading files.
