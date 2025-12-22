from __future__ import annotations

from typing import Any

from durak.cleaning import clean_text
from durak.stopwords import remove_stopwords as remove_stopwords_func
from durak.suffixes import attach_detached_suffixes
from durak.tokenizer import tokenize


class Pipeline:
    """
    A sequential processing pipeline, similar to torch.nn.Sequential.
    
    Args:
        steps (list[Any]): A list of callable components (e.g. Normalizer).
    """
    def __init__(self, steps: list[Any]):
        self.steps = steps

    def __call__(self, text: str) -> Any:
        """
        Process a single document through the pipeline.
        
        Args:
            text (str): Input text.
            
        Returns:
            Any: The result of the final pipeline step.
        """
        doc = text
        for step in self.steps:
            doc = step(doc)
        return doc

    def pipe(self, texts: list[str], batch_size: int = 1000) -> list[Any]:
        """
        Process a stream of texts efficiently.
        
        Args:
            texts (list[str]): Input texts.
            batch_size (int): Size of batches (reserved for future Rust parallelization).
            
        Yields:
            Any: Processed documents.
        """
        # TODO: Implement Rust-based parallel batch processing here.
        # For now, we iterate in Python.
        for text in texts:
            yield self(text)

    def __repr__(self) -> str:
        step_names = [repr(step) for step in self.steps]
        return "Pipeline([\n  " + ",\n  ".join(step_names) + "\n])"

def process_text(
    text: str,
    *,
    remove_stopwords: bool = False,
    rejoin_suffixes: bool = False,
    # These params are kept for signature compatibility but might need implementation update
    **kwargs: Any
) -> list[str]:
    """
    Legacy wrapper for backward compatibility.
    
    This function mimics the old behavior using the new architecture or existing components.
    Since we haven't deleted the old cleaning/tokenizer modules yet, we can import them locally
    or assume they are available to replicate the old flow.
    """
    
    # Replicate original pipeline logic from Quickstart:
    # clean -> tokenize -> rejoin -> remove stopwords
    
    # 1. Clean (using default cleaning steps)
    cleaned = clean_text(text)
    
    # 2. Tokenize (using regex strategy)
    tokens = tokenize(cleaned)
    
    # 3. Rejoin suffixes if requested
    if rejoin_suffixes:
        tokens = attach_detached_suffixes(tokens)
        
    # 4. Remove stopwords if requested
    if remove_stopwords:
        tokens = remove_stopwords_func(tokens)
        
    return tokens
