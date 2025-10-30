import pytest

from durak import StopwordManager, process_text


def test_process_text_default_pipeline() -> None:
    tokens = process_text("Bu bir test!")
    assert tokens == ["bu", "bir", "test", "!"]


def test_process_text_with_stopword_removal() -> None:
    tokens = process_text("Bu bir test!", remove_stopwords=True)
    assert tokens == ["test", "!"]


def test_process_text_respects_stopword_manager() -> None:
    manager = StopwordManager(keep=["test"])
    tokens = process_text(
        "Bu bir test!", remove_stopwords=True, stopword_manager=manager
    )
    assert tokens == ["test", "!"]


def test_process_text_stopword_options_require_flag() -> None:
    with pytest.raises(ValueError):
        process_text("Bu bir test!", stopword_base=["custom"])


def test_process_text_rejoin_suffixes_with_apostrophe() -> None:
    tokens = process_text("Ankara ' da kaldım.", rejoin_suffixes=True)
    assert tokens[:2] == ["ankara'da", "kaldım"]


def test_process_text_rejoin_suffixes_without_apostrophe() -> None:
    tokens = process_text("Ankara da kaldım.", rejoin_suffixes=True)
    assert tokens[:2] == ["ankarada", "kaldım"]


def test_process_text_rejoin_suffixes_respects_flag() -> None:
    tokens = process_text("Ankara ' da kaldım.")
    assert tokens[:2] == ["ankara", "'"]


def test_process_text_rejoin_suffixes_requires_flag() -> None:
    with pytest.raises(ValueError):
        process_text("Ankara ' da kaldım.", rejoin_suffix_list=["da"])
