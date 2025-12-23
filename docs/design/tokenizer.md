# Tokenizer Design

Durak's tokenizer module should support multiple strategies while honouring Turkish morphology.

## Regex Tokenisation
- Base pattern: split on whitespace and punctuation but retain apostrophes used in proper noun suffixes (`Ankara'ya`).
- Preserve clitics (`-ki`, `-mi`, `-de`/`-da`) when attached with hyphens or apostrophes.
- Handle URLs/emails as single tokens to avoid accidental splitting.
- Numeric tokens: keep decimal separators (`,` and `.`) and range markers (`-`, `–`).

## Sentence Splitting
- Default approach: rule-based splitter identifying sentence enders (`.?!…`) while respecting abbreviations (`Dr.`, `Prof.`) and numeric contexts (`1.`, `3.14`).
- Provide hooks to plug in advanced segmenters later (e.g., spaCy, Stanza) via strategy objects.

## Subword Tokenizer Placeholder
- Define interface `SubwordTokenizer` with `tokenize(tokens: Sequence[str]) -> Sequence[str]`.
- Leave placeholder implementation raising `NotImplementedError`, allowing future adapters (BPE, WordPiece).

## API Sketch
- `tokenize(text: str | None, *, strategy: str = "regex", strip_punct: bool = False) -> list[str]`
- `tokenize_text(text: str | None, strategy: str = "regex", *, strip_punct: bool = False) -> list[str]` (backward-compatible wrapper)
- `split_sentences(text: str, strategy: str = "regex", **kwargs) -> list[str]`
- `normalize_tokens(tokens: Iterable[str], *, lower: bool = True, strip_punct: bool = False) -> list[str]`
- Strategy registry enabling custom tokenizers/splitters via callables.

## Rust Implementation (v0.4.0+)

The core tokenization logic is implemented in Rust (`src/lib.rs`) for performance:

- **`tokenize_with_offsets(text: &str) -> Vec<(String, usize, usize)>`**: Returns tokens with character-accurate offsets
- **Performance**: 3-5x faster than pure Python implementation
- **GIL Release**: Enables true multi-core parallelism for batch processing
- **Type Safety**: Complete `.pyi` type stubs for IDE support

## Testing Considerations

- Validate tokens from sample sentences keep diacritics and suffixal particles.
- Integration tests using the corpus validator suite to ensure tokenization maintains prior invariants.
- Regression cases for:
  - Apostrophe-separated suffixes (`Türkiye'ye`, `FB'li`).
  - Hyphenated compounds (`kapı-kilit`, numeric ranges).
  - Emoticons and URLs.
- Performance benchmarks comparing Rust vs Python implementations (`benchmarks/benchmark_rust_vs_python.py`).
