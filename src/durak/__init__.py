"""Durak Turkish NLP toolkit."""

from __future__ import annotations

from importlib import metadata

__all__ = ["__version__"]

try:
    __version__ = metadata.version("durak-nlp")
except metadata.PackageNotFoundError:  # pragma: no cover - fallback during dev installs
    __version__ = "0.1.0"
