import re

import durak


def test_package_exposes_semantic_version() -> None:
    version = durak.__version__
    assert isinstance(version, str)
    assert re.match(r"^\d+\.\d+\.\d+(?:[+-][0-9A-Za-z.-]+)?$", version)


def test_quickstart_imports_available() -> None:
    assert callable(durak.clean_text)
    assert callable(durak.tokenize)
    tokens = durak.tokenize(durak.clean_text("Selam dünya!"))
    assert tokens[-1] == "!"
