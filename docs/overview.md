# Durak Toolkit Overview

Durak provides modular Turkish NLP building blocks focused on preprocessing and lightweight analytics. The initial scope prioritises deterministic utilities with optional adapters for heavier linguistic backends.

## Core Capabilities
- **Text cleaning**: utilities for Unicode normalization, HTML/artifact removal, lowercasing policies, punctuation control, and Turkish-specific heuristics (e.g., `bkz.` patterns, repeated emojis, social media boilerplate).
- **Tokenisation**: configurable tokenizers including regex-based word tokenisation, sentence segmentation hooks, and extension points for subword strategies.
- **Stopword handling**: curated base list with merge/override facilities, serialization helpers, and keep-list logic for domain-specific retention.
- **Lemmatization interface**: pluggable adapters for engines such as Zemberek, spaCy `tr_core_news_lg`, and Stanza, wrapped behind a consistent `LemmaEngine` protocol.
- **Frequency statistics**: n-gram and frequency counters operating on raw or lemmatized tokens, with optional stopword filtering.

## Non-Goals (Initial Release)
- Training or hosting large language models.
- Providing end-to-end ML pipelines beyond preprocessing and descriptive statistics.
- Shipping proprietary linguistic resources—only open-source or user-provided assets.

## Design Principles
- **Composable**: prefer small, pure functions and classes that can be chained.
- **Embeddable**: work smoothly in larger Python pipelines (Pandas, scikit-learn, Spark).
- **Configurable**: expose ergonomic configuration objects or dataclasses instead of hard-coded global settings.
- **Observable**: include logging hooks and metrics-friendly outputs for pipeline runs.
- **Testable**: design APIs with deterministic behaviour and comprehensive fixtures targeting Turkish morphology edge cases.
