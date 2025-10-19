"""Stopword utilities for Durak."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, FrozenSet, MutableSet, Set

from durak.cleaning import normalize_case

BASE_STOPWORDS: FrozenSet[str] = frozenset(
    {
        "acaba",
        "ama",
        "aslında",
        "az",
        "bazı",
        "belki",
        "ben",
        "beni",
        "benim",
        "beri",
        "biri",
        "birkaç",
        "birçok",
        "bir",
        "bin",
        "biz",
        "bizim",
        "bu",
        "çok",
        "çünkü",
        "da",
        "daha",
        "de",
        "defa",
        "diye",
        "eğer",
        "en",
        "gibi",
        "hem",
        "hep",
        "hepsi",
        "her",
        "hiç",
        "ile",
        "ise",
        "kez",
        "ki",
        "kim",
        "kimse",
        "mı",
        "mi",
        "mu",
        "mü",
        "nasıl",
        "ne",
        "neden",
        "nerde",
        "nerede",
        "niçin",
        "niye",
        "o",
        "olan",
        "olarak",
        "oldu",
        "oldun",
        "olduk",
        "olduğumuz",
        "olduğunu",
        "olmadı",
        "olmak",
        "olmaz",
        "olsa",
        "olsun",
        "onlar",
        "onu",
        "oysa",
        "pek",
        "sanki",
        "sen",
        "senin",
        "siz",
        "şey",
        "şu",
        "tüm",
        "ve",
        "veya",
        "ya",
        "yani",
        "yer",
        "yine",
        "yok",
        "zaten",
    }
)

__all__ = ["BASE_STOPWORDS", "StopwordManager", "StopwordSnapshot", "load_stopwords"]


def _normalize(token: str, *, case_sensitive: bool) -> str:
    return token if case_sensitive else normalize_case(token, mode="lower")


def load_stopwords(path: Path | str, *, case_sensitive: bool = False) -> Set[str]:
    """Load newline-delimited stopwords from a file."""
    entries: Set[str] = set()
    raw_text = Path(path).read_text(encoding="utf-8")
    for line in raw_text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.add(_normalize(stripped, case_sensitive=case_sensitive))
    return entries


@dataclass(frozen=True)
class StopwordSnapshot:
    stopwords: FrozenSet[str]
    keep_words: FrozenSet[str]
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
        normalized_base = {_normalize(word, case_sensitive=case_sensitive) for word in base_words}
        self._stopwords: MutableSet[str] = set(normalized_base)
        self._keep_words: MutableSet[str] = set()
        if additions:
            self.add(additions)
        if keep:
            self.add_keep_words(keep)

    @property
    def stopwords(self) -> FrozenSet[str]:
        return frozenset(self._stopwords)

    @property
    def keep_words(self) -> FrozenSet[str]:
        return frozenset(self._keep_words)

    def snapshot(self) -> StopwordSnapshot:
        return StopwordSnapshot(self.stopwords, self.keep_words, self.case_sensitive)

    def is_stopword(self, token: str) -> bool:
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

    def export(self, path: Path | str, *, format: str = "txt") -> None:
        dest = Path(path)
        words = sorted(self.stopwords)
        if format == "txt":
            dest.write_text("\n".join(words) + "\n", encoding="utf-8")
        elif format == "json":
            dest.write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            raise ValueError("Unsupported format; use 'txt' or 'json'.")

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
    ) -> "StopwordManager":
        manager = cls(case_sensitive=case_sensitive)
        for addition_path in additions:
            manager.load_additions(addition_path)
        for keep_path in keep:
            keep_words = load_stopwords(keep_path, case_sensitive=case_sensitive)
            manager.add_keep_words(keep_words)
        return manager
