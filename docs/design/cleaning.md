# Cleaning Utilities Design

Durak cleaning utilities should cover common Turkish corpus artefacts while remaining configurable. Initial scope:

- `normalize_unicode(text: str) -> str`: NFC normalization plus conversion of common visually-similar characters to canonical forms.
- `strip_html(text: str) -> str`: remove HTML tags and inline scripts/styles, retaining meaningful text segments.
- `collapse_whitespace(text: str) -> str`: replace consecutive whitespace (including newlines and tabs) with single spaces and trim edges.
- `normalize_case(text: str, mode: Literal["lower", "upper", "none"] = "lower") -> str`: apply Turkish-aware casing using `str.casefold` with special handling for dotted/undotted I; skip when `mode="none"`.
- `remove_urls(text: str) -> str`: strip common HTTP/HTTPS URLs and social media shortlinks.
- `remove_mentions_hashtags(text: str, keep_hash: bool = False) -> str`: drop `@handles` and optionally keep the hash symbol while removing hashtags.
- `remove_repeated_chars(text: str, max_repeats: int = 2) -> str`: limit elongated characters/emojis (`cooool`) to a configurable repeat threshold.
- `clean_text(text: str, *, steps: Iterable[Callable[[str], str]] = DEFAULT_CLEANING_STEPS) -> str`: orchestrate the default cleaning pipeline.

Testing strategies:

- Use fixtures verifying Turkish-specific casing (e.g., `İstanbul`, `IĞDIR`).
- Verify HTML stripping handles nested tags and scripts without clobbering text.
- Confirm URL removal leaves surrounding punctuation intact.
- Ensure repeated character normalization keeps meaningful punctuation like ellipses when `max_repeats >= 3`.
- Validate `clean_text` composes individual steps deterministically.
