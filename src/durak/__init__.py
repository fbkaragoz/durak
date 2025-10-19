"""Durak Turkish NLP toolkit."""

from __future__ import annotations

from importlib import metadata

from .cleaning import clean_text, collapse_whitespace, normalize_case, normalize_unicode
from .tokenizer import normalize_tokens, split_sentences, tokenize_text

__all__ = [
    "__version__",
    "clean_text",
    "collapse_whitespace",
    "normalize_case",
    "normalize_unicode",
    "normalize_tokens",
    "split_sentences",
    "tokenize",
    "tokenize_text",
]

try:
    __version__ = metadata.version("durak-nlp")
except metadata.PackageNotFoundError:  # pragma: no cover - fallback during dev installs
    __version__ = "0.1.0"

tokenize = tokenize_text
