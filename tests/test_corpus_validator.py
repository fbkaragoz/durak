from pathlib import Path

from tests.data.corpus_validator import validate_corpus


def test_corpus_validator_on_sample_sentences() -> None:
    sample_path = Path(__file__).parent / "data" / "sample_sentences.txt"
    sentences = sample_path.read_text(encoding="utf-8").splitlines()
    issues = validate_corpus(sentences)
    assert not issues, f"Corpus validation issues detected: {issues}"
