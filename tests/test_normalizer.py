"""
Unit tests for Normalizer class.

Tests configuration parameters (lowercase, handle_turkish_i) to ensure they are
properly applied by the Rust core.
"""

import pytest
from durak.normalizer import Normalizer


class TestNormalizerDefaults:
    """Test default behavior (lowercase=True, handle_turkish_i=True)"""
    
    def test_default_normalization(self):
        """Default: lowercase + Turkish I handling"""
        normalizer = Normalizer()
        
        # Should lowercase and handle Turkish I
        assert normalizer("İSTANBUL") == "istanbul"
        assert normalizer("ANKARA") == "ankara"
        assert normalizer("GELİYOR") == "geliyor"
    
    def test_turkish_i_conversion_default(self):
        """Default: İ → i, I → ı"""
        normalizer = Normalizer()
        
        # Turkish I conversion
        assert normalizer("İ") == "i"
        assert normalizer("I") == "ı"
        assert normalizer("İSTANBUL") == "istanbul"
        assert normalizer("IŞIK") == "ışık"


class TestNormalizerLowercaseFalse:
    """Test with lowercase=False"""
    
    def test_preserves_case_with_turkish_i(self):
        """lowercase=False: should preserve case but handle Turkish I"""
        normalizer = Normalizer(lowercase=False, handle_turkish_i=True)
        
        # Should NOT lowercase but should handle İ→i, I→ı
        result = normalizer("İSTANBUL")
        assert result == "iSTANBUL"  # İ→i, but rest stays uppercase
        
        result = normalizer("IŞIK")
        assert result == "ışıK"  # I→ı, but K stays uppercase
    
    def test_mixed_case_preserved(self):
        """lowercase=False: mixed case should be preserved"""
        normalizer = Normalizer(lowercase=False, handle_turkish_i=True)
        
        result = normalizer("GeliYorum")
        assert result == "GeliYorum"  # No Turkish I, case preserved
        
        result = normalizer("İstanbul")
        assert result == "istanbul"  # İ→i, rest already lowercase


class TestNormalizerTurkishIFalse:
    """Test with handle_turkish_i=False"""
    
    def test_no_turkish_i_conversion(self):
        """handle_turkish_i=False: should lowercase but NOT convert İ/I"""
        normalizer = Normalizer(lowercase=True, handle_turkish_i=False)
        
        # Should lowercase using standard Unicode rules, NOT Turkish rules
        result = normalizer("İSTANBUL")
        # Standard Unicode: İ → i + combining dot above (U+0069 U+0307)
        # or just İ → i depending on locale
        # In most cases, İ in Turkish context lowercases to i
        # But without Turkish handling, it should use default Unicode
        # For simplicity, we check it's NOT "istanbul" (which is Turkish-specific)
        assert result != "istanbul"
        
        result = normalizer("IŞIK")
        # Standard Unicode: I → i (not ı)
        # Without Turkish handling, I should become i (not ı)
        assert "ı" not in result  # Should NOT contain Turkish ı


class TestNormalizerBothFalse:
    """Test with both lowercase=False and handle_turkish_i=False"""
    
    def test_no_transformation(self):
        """Both False: text should be unchanged"""
        normalizer = Normalizer(lowercase=False, handle_turkish_i=False)
        
        # Should return input as-is
        assert normalizer("İSTANBUL") == "İSTANBUL"
        assert normalizer("GeliYorum") == "GeliYorum"
        assert normalizer("IŞIK") == "IŞIK"
        assert normalizer("istanbul") == "istanbul"


class TestNormalizerEdgeCases:
    """Test edge cases"""
    
    def test_empty_string(self):
        """Empty string should return empty"""
        normalizer = Normalizer()
        assert normalizer("") == ""
    
    def test_whitespace_only(self):
        """Whitespace should be preserved"""
        normalizer = Normalizer()
        assert normalizer("   ") == "   "
    
    def test_numbers_and_punctuation(self):
        """Numbers and punctuation should be unchanged"""
        normalizer = Normalizer()
        assert normalizer("123") == "123"
        assert normalizer("!@#$%") == "!@#$%"
        assert normalizer("2024 yılı!") == "2024 yılı!"
    
    def test_mixed_content(self):
        """Mixed content with Turkish characters"""
        normalizer = Normalizer()
        result = normalizer("İstanbul'da 2024 yılında!")
        assert result == "istanbul'da 2024 yılında!"


class TestNormalizerRepr:
    """Test string representation"""
    
    def test_repr_default(self):
        """Default normalizer repr"""
        normalizer = Normalizer()
        assert repr(normalizer) == "Normalizer(lowercase=True, handle_turkish_i=True)"
    
    def test_repr_custom(self):
        """Custom config repr"""
        normalizer = Normalizer(lowercase=False, handle_turkish_i=False)
        assert repr(normalizer) == "Normalizer(lowercase=False, handle_turkish_i=False)"
