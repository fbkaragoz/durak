from __future__ import annotations

from typing import Any

try:
    from _durak_core import fast_normalize
except ImportError:
    # Fallback or initialization error handling
    def fast_normalize(text: str) -> str:
        raise ImportError("Durak Rust extension (_durak_core) is not installed/compiled.")

class Normalizer:
    """
    A configurable Normalizer module backed by Rust.
    
    Args:
        lowercase (bool): If True, lowercases the text (handling Turkish I/ı).
        handle_turkish_i (bool): If True, handles specific Turkish I/İ rules.
    """
    def __init__(self, lowercase: bool = True, handle_turkish_i: bool = True):
        self.lowercase = lowercase
        self.handle_turkish_i = handle_turkish_i

    def __call__(self, text: str) -> str:
        """
        Normalize the input text.
        
        Args:
            text (str): Input string.
            
        Returns:
            str: Normalized string.
        """
        if not text:
            return ""
        
        if self.lowercase and self.handle_turkish_i:
            return fast_normalize(text)
        
        # In the future, we can add more configuration options to the Rust core
        # and pass flags, but for now fast_normalize does both default behaviors.
        return fast_normalize(text)

    def __repr__(self) -> str:
        return f"Normalizer(lowercase={self.lowercase}, handle_turkish_i={self.handle_turkish_i})"
