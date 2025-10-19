# Stopword Management Design

Objectives:

- Provide a curated Turkish stopword list sourced from permissive public datasets (e.g., Snowball/stopwords-iso) and manual curation.
- Allow projects to extend the list with domain-specific additions while preserving the base list for reuse.
- Support explicit keep-lists so critical terms remain even if they appear in the base list.
- Enable serialization and deserialization to share tailored stopword sets across projects.

Key APIs:

- `BASE_STOPWORDS`: frozen set containing Durak's maintained list.
- `load_stopwords(path: Path | str) -> set[str]`: read stopwords from newline-delimited files (UTF-8).
- `StopwordManager`:
  - Initialization parameters: `base`, `additions`, `keep`, `case_sensitive`.
  - Methods: `is_stopword(token)`, `add(words)`, `remove(words)`, `export(path, format="txt")`, `to_dict()`.
  - Properties: `.stopwords` (read-only view), `.keep_words`.

Testing scenarios:

- Default manager identifies base stopwords but honours keep words.
- Additional stopwords from files and iterables merge correctly; duplicates handled.
- Case-insensitive mode normalises tokens via Turkish lowercasing from `cleaning.normalize_case`.
- Serialization roundtrip to temporary files retains stopwords and keeps duplicates suppressed.
- Ensure newline and whitespace trimming when loading files.
