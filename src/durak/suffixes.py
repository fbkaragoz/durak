"""Utilities for handling detached Turkish suffix tokens."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

APOSTROPHE_TOKENS: tuple[str, ...] = ("'", "’")
DEFAULT_DETACHED_SUFFIXES: tuple[str, ...] = (
    "in",
    "ın",
    "un",
    "ün",
    "nin",
    "nın",
    "nun",
    "nün",
    "de",
    "da",
    "te",
    "ta",
    "ye",
    "ya",
)

__all__ = [
    "APOSTROPHE_TOKENS",
    "DEFAULT_DETACHED_SUFFIXES",
    "attach_detached_suffixes",
]


def _has_alpha(token: str | None) -> bool:
    return bool(token) and any(char.isalpha() for char in token)


def _matches_suffix(token: str | None, suffixes: set[str]) -> bool:
    if not token:
        return False
    normalized = token.lower()
    return normalized in suffixes


def attach_detached_suffixes(
    tokens: Sequence[str] | None,
    *,
    suffixes: Iterable[str] | None = None,
    allow_without_apostrophe: bool = True,
    apostrophes: Iterable[str] | None = None,
) -> list[str]:
    """Join detached suffix tokens with their preceding base token.

    Examples:
        >>> attach_detached_suffixes(["ankara", "'", "da"])
        ["ankara'da"]
        >>> attach_detached_suffixes(["ankara", "da"])
        ['ankarada']
    """
    if not tokens:
        return []

    suffix_set = {suffix.lower() for suffix in (suffixes or DEFAULT_DETACHED_SUFFIXES)}
    if apostrophes is not None:
        apostrophe_set = tuple(apostrophes)
    else:
        apostrophe_set = APOSTROPHE_TOKENS

    merged: list[str] = []
    index = 0

    while index < len(tokens):
        current = tokens[index]

        if not _has_alpha(current):
            merged.append(current)
            index += 1
            continue

        next_index = index + 1
        apostrophe_index = index + 2

        if (
            next_index < len(tokens)
            and tokens[next_index] in apostrophe_set
            and apostrophe_index < len(tokens)
            and _matches_suffix(tokens[apostrophe_index], suffix_set)
        ):
            combined = f"{current}{tokens[next_index]}{tokens[apostrophe_index]}"
            merged.append(combined)
            index += 3
            continue

        if (
            allow_without_apostrophe
            and next_index < len(tokens)
            and _matches_suffix(tokens[next_index], suffix_set)
        ):
            combined = f"{current}{tokens[next_index]}"
            merged.append(combined)
            index += 2
            continue

        merged.append(current)
        index += 1

    return merged
