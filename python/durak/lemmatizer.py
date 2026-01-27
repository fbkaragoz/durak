from __future__ import annotations

from typing import Literal

try:
    from durak._durak_core import lookup_lemma, strip_suffixes, strip_suffixes_validated
except ImportError:
    def lookup_lemma(word: str) -> str | None:
        raise ImportError("Rust extension not installed")
    def strip_suffixes(word: str) -> str:
        raise ImportError("Rust extension not installed")
    def strip_suffixes_validated(word: str, strict: bool = False, min_root_length: int = 2) -> str:
        raise ImportError("Rust extension not installed")

Strategy = Literal["lookup", "heuristic", "hybrid"]

class Lemmatizer:
    """
    Tiered Lemmatizer backed by Rust.
    
    Strategies:
    - lookup: Use only the exact dictionary 
      (fastest, high precision, low recall on OOV).
    - heuristic: Use only suffix stripping (fast, works on OOV, lower precision).
    - hybrid: Try lookup first, fallback to heuristic (default).
    
    Args:
        strategy: Lemmatization strategy (lookup, heuristic, hybrid)
        validate_roots: Enable root validity checking for heuristic mode
        strict_validation: Require roots to be in lemma dictionary
        min_root_length: Minimum acceptable root length (characters)
    """
    def __init__(
        self, 
        strategy: Strategy = "hybrid",
        validate_roots: bool = False,
        strict_validation: bool = False,
        min_root_length: int = 2,
    ):
        self.strategy = strategy
        self.validate_roots = validate_roots
        self.strict_validation = strict_validation
        self.min_root_length = min_root_length

    def __call__(self, word: str) -> str:
        if not word:
            return ""
            
        # Tier 1: Lookup
        if self.strategy in ("lookup", "hybrid"):
            lemma = lookup_lemma(word)
            if lemma is not None:
                return lemma
            if self.strategy == "lookup":
                return word  # Return as-is if not found

        # Tier 2: Heuristic (with optional root validation)
        if self.strategy in ("heuristic", "hybrid"):
            if self.validate_roots:
                return strip_suffixes_validated(
                    word,
                    strict=self.strict_validation,
                    min_root_length=self.min_root_length,
                )
            else:
                return strip_suffixes(word)
            
        return word

    def __repr__(self) -> str:
        parts = [f"strategy='{self.strategy}'"]
        if self.validate_roots:
            parts.append("validate_roots=True")
            if self.strict_validation:
                parts.append("strict_validation=True")
            if self.min_root_length != 2:
                parts.append(f"min_root_length={self.min_root_length}")
        return f"Lemmatizer({', '.join(parts)})"
