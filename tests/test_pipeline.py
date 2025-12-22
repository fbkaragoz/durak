import pytest
import durak
from durak.normalizer import Normalizer
from durak.pipeline import Pipeline

def test_normalizer_importable():
    norm = Normalizer()
    assert norm is not None

def test_pipeline_creation():
    pipe = Pipeline([
        Normalizer(),
    ])
    assert len(pipe.steps) == 1

def test_pipeline_execution():
    # If Rust extension is not built, this might fail or fallback.
    # We expect it to work if the environment is set up correctly.
    try:
        from _durak_core import fast_normalize
    except ImportError:
        pytest.skip("Rust extension not installed")

    pipe = Pipeline([
        Normalizer(),
    ])
    
    # Test valid Turkish input
    text = "İSTANBUL ve IĞDIR"
    # normalize should convert İ -> i, I -> ı, lower -> istanbul ve ığdır
    result = pipe(text)
    assert result == "istanbul ve ığdır"

def test_batch_processing():
    try:
        from _durak_core import fast_normalize
    except ImportError:
        pytest.skip("Rust extension not installed")
        
    pipe = Pipeline([Normalizer()])
    texts = ["İSTANBUL", "Ankara"]
    results = list(pipe.pipe(texts))
    assert results == ["istanbul", "ankara"]
