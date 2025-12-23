# Durak Resources

This directory contains static data files used by Durak for Turkish NLP processing. Resources are organized by language (`tr/` for Turkish) and compiled directly into the binary at build time using Rust's `include_str!` macro for zero-overhead, zero-I/O loading.

## Directory Structure

```
resources/
└── tr/                          # Turkish language resources
    ├── stopwords/               # Stopword lists
    │   ├── base/                # Base stopword sets
    │   │   └── turkish.txt      # Core Turkish stopwords
    │   ├── domains/             # Domain-specific stopwords
    │   │   └── social_media.txt # Social media stopwords
    │   └── metadata.json        # Stopword set definitions and inheritance
    ├── labels/                  # Linguistic labels
    │   └── DETACHED_SUFFIXES.txt # Turkish detached suffixes (da, de, etc.)
    └── config/                  # Configuration data
        ├── apostrophes.txt      # Turkish apostrophe characters
        └── lemma_suffixes.txt   # Turkish lemmatization suffixes
```

## Resource Types

### Stopwords (`stopwords/`)

**Format**: Newline-delimited text files, one word per line
- Lines starting with `#` are comments
- Empty lines are ignored
- Words are automatically normalized unless `case_sensitive=True`

**Example** (`base/turkish.txt`):
```
# Common Turkish stopwords
ve
veya
ama
fakat
```

**Metadata** (`metadata.json`):
Defines stopword sets with inheritance support:
```json
{
  "sets": {
    "base/turkish": {
      "file": "base/turkish.txt",
      "description": "Core Turkish stopwords"
    },
    "domains/social_media": {
      "file": "domains/social_media.txt",
      "extends": ["base/turkish"],
      "description": "Social media stopwords"
    }
  }
}
```

### Labels (`labels/`)

**Format**: Newline-delimited text files
- Used for linguistic labels and suffix lists
- One item per line

**Example** (`DETACHED_SUFFIXES.txt`):
```
da
de
ta
te
dan
den
```

### Configuration (`config/`)

**Format**: Newline-delimited or structured text
- Contains configuration values externalized from code
- Documented with inline comments

## Adding New Resources

### Adding a New Stopword Set

1. Create the file in appropriate directory:
   ```bash
   echo "yeni\nkelime" > resources/tr/stopwords/domains/medical.txt
   ```

2. Add entry to `metadata.json`:
   ```json
   {
     "sets": {
       "domains/medical": {
         "file": "domains/medical.txt",
         "extends": ["base/turkish"],
         "description": "Medical domain stopwords"
       }
     }
   }
   ```

3. (Optional) Embed in Rust for production use:
   ```rust
   // In src/lib.rs
   static STOPWORDS_MEDICAL_DATA: &str =
       include_str!("../resources/tr/stopwords/domains/medical.txt");

   #[pyfunction]
   fn get_stopwords_medical() -> Vec<String> {
       parse_lines(STOPWORDS_MEDICAL_DATA)
   }
   ```

4. Rebuild:
   ```bash
   maturin develop --release
   ```

### Adding a New Label List

1. Create the file:
   ```bash
   echo "yeni\nlabel" > resources/tr/labels/NEW_LABELS.txt
   ```

2. Load in Python:
   ```python
   from pathlib import Path

   labels_path = Path(__file__).parent.parent / "resources" / "tr" / "labels" / "NEW_LABELS.txt"
   labels = labels_path.read_text().strip().split('\n')
   ```

3. (Optional) Embed in Rust for better performance.

## Embedded vs File-Based Loading

### Embedded (Production)
- Resources compiled into binary at build time
- Zero file I/O, 100-1000x faster loading
- Used automatically when Rust extension is available
- Files referenced in `src/lib.rs` with `include_str!`

### File-Based (Development/Fallback)
- Resources loaded from disk at runtime
- Allows testing changes without rebuilding
- Automatic fallback if Rust extension unavailable
- Used in pure Python mode

## Best Practices

1. **Use UTF-8 encoding** for all text files
2. **One item per line** for list-based resources
3. **Add comments** with `#` prefix for documentation
4. **Keep files focused** - separate by domain/purpose
5. **Update metadata.json** when adding stopword sets
6. **Test both modes** - file-based and embedded
7. **Document custom additions** in comments

## Resource Guidelines

### Stopwords
- Include only high-frequency functional words
- Avoid domain-specific terms in base sets
- Use `extends` in metadata for domain specialization
- Provide clear descriptions

### Labels
- Use uppercase for label files (e.g., `DETACHED_SUFFIXES.txt`)
- Keep alphabetically sorted when order doesn't matter
- Document the source or rationale in comments

### Configuration
- Document each value with inline comments
- Keep format simple and parseable
- Version-control friendly (line-based)

## Performance Notes

Resources embedded at compile time provide significant benefits:
- **Loading time**: 100-1000x faster than file I/O
- **Memory**: Single allocation, no repeated parsing
- **Distribution**: No separate data files needed
- **Security**: Resources verified at build time

For development, file-based loading allows rapid iteration without rebuilds.

## Contributing Resources

When contributing new resources:

1. Ensure data quality and licensing
2. Document the source and curation process
3. Add tests to verify correctness
4. Update this README if adding new categories
5. Consider both embedded and file-based access

## Questions?

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines or open an issue at [github.com/fbkaragoz/durak/issues](https://github.com/fbkaragoz/durak/issues).
