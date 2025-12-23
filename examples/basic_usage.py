"""Basic usage example demonstrating the Durak NLP toolkit.

This example shows how to use the core text processing features
including tokenization, normalization, stopword removal, and lemmatization.
"""

import durak


def main():
    # Sample Turkish text
    text = "Merhaba dünya! Bu bir Türkçe doğal dil işleme örneğidir."

    print("=" * 60)
    print("Durak NLP Basic Usage Example")
    print("=" * 60)

    # 1. Text Cleaning
    print("\n1. Text Cleaning")
    print(f"Original: {text}")
    cleaned = durak.clean_text(text)
    print(f"Cleaned:  {cleaned}")

    # 2. Tokenization
    print("\n2. Tokenization")
    tokens = durak.tokenize(cleaned)
    print(f"Tokens: {tokens}")

    # 3. Tokenization with offsets
    print("\n3. Tokenization with Offsets")
    tokens_with_offsets = durak.tokenize_with_offsets(cleaned)
    for token, start, end in tokens_with_offsets:
        print(f"  '{token}' at positions {start}-{end}")

    # 4. Stopword Removal
    print("\n4. Stopword Removal")
    print(f"Before: {tokens}")
    filtered = durak.remove_stopwords(tokens)
    print(f"After:  {filtered}")

    # 5. Using the Pipeline
    print("\n5. Using the Pipeline")
    result = durak.process_text(text)
    print(f"Pipeline result: {result}")

    # 6. Accessing embedded Rust resources (if Rust extension is available)
    print("\n6. Embedded Resources (Rust Extension)")
    try:
        from durak import _durak_core

        # Get embedded stopwords
        base_stopwords = _durak_core.get_stopwords_base()
        print(f"Loaded {len(base_stopwords)} base stopwords from Rust binary")
        print(f"First 10: {base_stopwords[:10]}")

        # Get embedded detached suffixes
        suffixes = _durak_core.get_detached_suffixes()
        print(f"\nLoaded {len(suffixes)} detached suffixes from Rust binary")
        print(f"Suffixes: {suffixes}")

        # Fast Rust normalization
        normalized = _durak_core.fast_normalize("İSTANBUL")
        print(f"\nRust fast_normalize('İSTANBUL') = '{normalized}'")

    except ImportError:
        print("Rust extension not available. Install with: maturin develop")

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
