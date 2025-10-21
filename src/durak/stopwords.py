"""Stopword utilities for Durak."""

from __future__ import annotations

import json
from collections.abc import Iterable, MutableSet, Sequence
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, cast

from durak.cleaning import normalize_case

STOPWORD_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "stopwords"
DEFAULT_STOPWORD_RESOURCE = "tr/base"
STOPWORD_METADATA_PATH = STOPWORD_DATA_DIR / "metadata.json"

__all__ = [
    "BASE_STOPWORDS",
    "DEFAULT_STOPWORD_RESOURCE",
    "STOPWORD_METADATA_PATH",
    "StopwordMetadataError",
    "StopwordManager",
    "StopwordSnapshot",
    "load_stopword_resource",
    "load_stopword_resources",
    "load_stopwords",
]


class StopwordMetadataError(RuntimeError):
    """Raised when stopword metadata is missing or malformed."""


def _resolve_metadata_path(metadata_path: Path | str | None) -> Path:
    if metadata_path is None:
        return STOPWORD_METADATA_PATH
    return Path(metadata_path)


@lru_cache(maxsize=None)
def _read_stopword_metadata(resolved_metadata_path: str) -> dict[str, Any]:
    metadata_path = Path(resolved_metadata_path)
    try:
        raw = metadata_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise StopwordMetadataError(
            f"Stopword metadata file not found at '{metadata_path}'."
        ) from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise StopwordMetadataError(
            f"Stopword metadata at '{metadata_path}' is not valid JSON."
        ) from exc
    if not isinstance(data, dict):
        raise StopwordMetadataError("Stopword metadata must be a JSON object.")
    sets = data.get("sets")
    if not isinstance(sets, dict) or not sets:
        raise StopwordMetadataError("Stopword metadata 'sets' must be a non-empty map.")
    return data


def _resolve_resource_path(relative_path: str, *, base_dir: Path) -> Path:
    if not relative_path or not isinstance(relative_path, str):
        raise StopwordMetadataError("Stopword resource entry is missing its 'file'.")
    candidate = (base_dir / relative_path).resolve()
    base_dir_resolved = base_dir.resolve()
    try:
        candidate.relative_to(base_dir_resolved)
    except ValueError as exc:
        raise StopwordMetadataError(
            f"Stopword resource path '{relative_path}' escapes the data directory."
        ) from exc
    if not candidate.is_file():
        raise StopwordMetadataError(
            f"Stopword resource file '{relative_path}' not found under '{base_dir}'."
        )
    return candidate


def _ensure_sequence(value: Any, *, field: str) -> Sequence[str]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if not isinstance(value, Sequence):
        raise StopwordMetadataError(
            f"Stopword resource '{field}' must be a sequence of strings."
        )
    if not all(isinstance(item, str) for item in value):
        raise StopwordMetadataError(
            f"Stopword resource '{field}' must only contain strings."
        )
    return cast(Sequence[str], value)


def _collect_resource_words(
    resource_name: str,
    *,
    sets: dict[str, Any],
    base_dir: Path,
    case_sensitive: bool,
    stack: set[str],
    cache: dict[str, frozenset[str]],
) -> frozenset[str]:
    if resource_name in cache:
        return cache[resource_name]
    if resource_name in stack:
        cycle = " -> ".join((*stack, resource_name))
        raise StopwordMetadataError(f"Circular stopword resource extends chain: {cycle}")
    try:
        entry: dict[str, Any] = sets[resource_name]
    except KeyError as exc:
        raise StopwordMetadataError(f"Unknown stopword resource '{resource_name}'.") from exc

    stack.add(resource_name)
    try:
        words: set[str] = set()
        extends = _ensure_sequence(entry.get("extends"), field="extends")
        for parent in extends:
            parent_words = _collect_resource_words(
                parent,
                sets=sets,
                base_dir=base_dir,
                case_sensitive=case_sensitive,
                stack=stack,
                cache=cache,
            )
            words.update(parent_words)
        file_path = _resolve_resource_path(entry.get("file", ""), base_dir=base_dir)
        words.update(load_stopwords(file_path, case_sensitive=case_sensitive))
    finally:
        stack.remove(resource_name)

    frozen = frozenset(words)
    cache[resource_name] = frozen
    return frozen


@lru_cache(maxsize=None)
def _load_stopword_resource_cached(
    resolved_metadata_path: str, resource_name: str, case_sensitive: bool
) -> frozenset[str]:
    metadata = _read_stopword_metadata(resolved_metadata_path)
    sets = metadata["sets"]
    if not isinstance(sets, dict):
        raise StopwordMetadataError("Stopword metadata 'sets' must be a mapping.")
    base_dir = Path(resolved_metadata_path).parent
    cache: dict[str, frozenset[str]] = {}
    words = _collect_resource_words(
        resource_name,
        sets=sets,
        base_dir=base_dir,
        case_sensitive=case_sensitive,
        stack=set(),
        cache=cache,
    )
    return words


def load_stopword_resource(
    resource_name: str,
    *,
    metadata_path: Path | str | None = None,
    case_sensitive: bool = False,
) -> set[str]:
    """Load a stopword resource defined in metadata, applying inheritance."""
    metadata = _resolve_metadata_path(metadata_path).resolve()
    words = _load_stopword_resource_cached(
        str(metadata),
        resource_name,
        case_sensitive,
    )
    return set(words)


def load_stopword_resources(
    resource_names: Iterable[str],
    *,
    metadata_path: Path | str | None = None,
    case_sensitive: bool = False,
) -> set[str]:
    """Load and merge multiple stopword resources."""
    merged: set[str] = set()
    for name in resource_names:
        merged.update(
            load_stopword_resource(
                name,
                metadata_path=metadata_path,
                case_sensitive=case_sensitive,
            )
        )
    return merged


def _normalize(token: str, *, case_sensitive: bool) -> str:
    return token if case_sensitive else normalize_case(token, mode="lower")


def load_stopwords(path: Path | str, *, case_sensitive: bool = False) -> set[str]:
    """Load newline-delimited stopwords from a file."""
    entries: set[str] = set()
    raw_text = Path(path).read_text(encoding="utf-8")
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.add(_normalize(stripped, case_sensitive=case_sensitive))
    return entries


BASE_STOPWORDS: frozenset[str] = frozenset(
    load_stopword_resource(DEFAULT_STOPWORD_RESOURCE, case_sensitive=False)
)


@dataclass(frozen=True)
class StopwordSnapshot:
    stopwords: frozenset[str]
    keep_words: frozenset[str]
    case_sensitive: bool


class StopwordManager:
    """Manage stopword sets with extension and keep-list support."""

    def __init__(
        self,
        *,
        base: Iterable[str] | None = None,
        additions: Iterable[str] | None = None,
        keep: Iterable[str] | None = None,
        case_sensitive: bool = False,
    ) -> None:
        self.case_sensitive = case_sensitive
        base_words = set(base) if base is not None else set(BASE_STOPWORDS)
        normalized_base = {
            _normalize(word, case_sensitive=case_sensitive) for word in base_words
        }
        self._stopwords: MutableSet[str] = set(normalized_base)
        self._keep_words: MutableSet[str] = set()
        if additions:
            self.add(additions)
        if keep:
            self.add_keep_words(keep)

    @property
    def stopwords(self) -> frozenset[str]:
        return frozenset(self._stopwords)

    @property
    def keep_words(self) -> frozenset[str]:
        return frozenset(self._keep_words)

    def snapshot(self) -> StopwordSnapshot:
        return StopwordSnapshot(self.stopwords, self.keep_words, self.case_sensitive)

    def is_stopword(self, token: str | None) -> bool:
        if token is None:
            return False
        normalized = _normalize(token, case_sensitive=self.case_sensitive)
        if normalized in self._keep_words:
            return False
        return normalized in self._stopwords

    def add(self, words: Iterable[str]) -> None:
        for word in words:
            normalized = _normalize(word, case_sensitive=self.case_sensitive)
            if normalized and normalized not in self._keep_words:
                self._stopwords.add(normalized)

    def remove(self, words: Iterable[str]) -> None:
        for word in words:
            normalized = _normalize(word, case_sensitive=self.case_sensitive)
            self._stopwords.discard(normalized)

    def add_keep_words(self, words: Iterable[str]) -> None:
        for word in words:
            normalized = _normalize(word, case_sensitive=self.case_sensitive)
            if normalized:
                self._keep_words.add(normalized)
                self._stopwords.discard(normalized)

    def load_additions(self, path: Path | str) -> None:
        self.add(load_stopwords(path, case_sensitive=self.case_sensitive))

    def export(self, path: Path | str, *, fmt: str = "txt") -> None:
        dest = Path(path)
        words = sorted(self.stopwords)
        if fmt == "txt":
            dest.write_text("\n".join(words) + "\n", encoding="utf-8")
        elif fmt == "json":
            dest.write_text(
                json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        else:
            raise ValueError("Unsupported fmt; use 'txt' or 'json'.")

    def to_dict(self) -> dict[str, object]:
        return {
            "stopwords": sorted(self.stopwords),
            "keep_words": sorted(self.keep_words),
            "case_sensitive": self.case_sensitive,
        }

    @classmethod
    def from_files(
        cls,
        *,
        additions: Iterable[Path | str] = (),
        keep: Iterable[Path | str] = (),
        case_sensitive: bool = False,
    ) -> StopwordManager:
        manager = cls(case_sensitive=case_sensitive)
        for addition_path in additions:
            manager.load_additions(addition_path)
        for keep_path in keep:
            keep_words = load_stopwords(keep_path, case_sensitive=case_sensitive)
            manager.add_keep_words(keep_words)
        return manager

    @classmethod
    def from_resources(
        cls,
        resource_names: Iterable[str] | None = None,
        *,
        metadata_path: Path | str | None = None,
        additions: Iterable[str] | None = None,
        keep: Iterable[str] | None = None,
        case_sensitive: bool = False,
    ) -> StopwordManager:
        """Factory that loads base words from metadata-defined resources."""
        names = (
            tuple(resource_names)
            if resource_names
            else (DEFAULT_STOPWORD_RESOURCE,)
        )
        base_words = load_stopword_resources(
            names,
            metadata_path=metadata_path,
            case_sensitive=case_sensitive,
        )
        return cls(
            base=base_words,
            additions=additions,
            keep=keep,
            case_sensitive=case_sensitive,
        )
