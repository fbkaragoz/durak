import json
from pathlib import Path

import pytest

from durak.stopwords import BASE_STOPWORDS, StopwordManager, StopwordSnapshot, load_stopwords


def test_base_stopwords_contains_common_tokens() -> None:
    assert {"ve", "ama", "çünkü"} <= BASE_STOPWORDS


def test_load_stopwords_normalizes_entries(tmp_path: Path) -> None:
    source = tmp_path / "custom.txt"
    source.write_text("# comment\nServis\nveri\n", encoding="utf-8")
    loaded = load_stopwords(source)
    assert loaded == {"servis", "veri"}


def test_stopword_manager_respects_keep_words() -> None:
    manager = StopwordManager(keep=["ama"])
    assert manager.is_stopword("ve")
    assert not manager.is_stopword("ama")
    assert not manager.is_stopword("Ama")


def test_stopword_manager_additions_and_file_loading(tmp_path: Path, data_dir: Path) -> None:
    manager = StopwordManager(additions=["api"])
    assert manager.is_stopword("api")

    additions_path = data_dir / "extra_stopwords.txt"
    manager.load_additions(additions_path)
    assert all(manager.is_stopword(word) for word in ["uygulama", "servis", "sunucu"])


def test_case_sensitive_mode_differentiates_tokens() -> None:
    manager = StopwordManager(base=["Durak"], case_sensitive=True)
    assert manager.is_stopword("Durak")
    assert not manager.is_stopword("durak")


def test_export_and_snapshot_roundtrip(tmp_path: Path, data_dir: Path) -> None:
    manager = StopwordManager(additions=["veri"], keep=["ama"])
    manager.load_additions(data_dir / "extra_stopwords.txt")
    snapshot = manager.snapshot()
    assert isinstance(snapshot, StopwordSnapshot)
    assert "ama" in snapshot.keep_words

    txt_path = tmp_path / "stopwords.txt"
    json_path = tmp_path / "stopwords.json"
    manager.export(txt_path)
    manager.export(json_path, format="json")

    txt_contents = txt_path.read_text(encoding="utf-8").strip().splitlines()
    json_contents = json.loads(json_path.read_text(encoding="utf-8"))
    assert sorted(txt_contents) == sorted(json_contents)
    assert "ama" not in json_contents  # keep words should be excluded


@pytest.fixture
def data_dir() -> Path:
    return Path(__file__).parent / "data"
