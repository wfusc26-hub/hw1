#!/usr/bin/env python3
"""Word frequency analyzer.

Given a text block, return the top-k most frequent words and counts.
Capitalization and punctuation are ignored.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from typing import Iterable


WORD_PATTERN = re.compile(r"[A-Za-z0-9]+")


def extract_words(text: str) -> list[str]:
    """Extract lowercase words from input text."""
    return [match.group(0).lower() for match in WORD_PATTERN.finditer(text)]


def top_k_frequent_words(text: str, k: int = 10) -> list[tuple[str, int]]:
    """Return up to k (word, count) pairs sorted by count desc then word asc."""
    if k <= 0:
        return []

    counts = Counter(extract_words(text))
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return ordered[:k]


def format_results(results: Iterable[tuple[str, int]]) -> str:
    """Format analyzer results for display."""
    return "\n".join(f"{word} {count}" for word, count in results)


def main() -> None:
    """CLI entrypoint: read text from stdin and print top-k words."""
    if len(sys.argv) > 2:
        raise SystemExit("Usage: python word_frequency_analyzer.py [k]")

    k = 10
    if len(sys.argv) == 2:
        try:
            k = int(sys.argv[1])
        except ValueError as exc:
            raise SystemExit("k must be a non-negative integer.") from exc
        if k < 0:
            raise SystemExit("k must be a non-negative integer.")

    text = sys.stdin.read()
    results = top_k_frequent_words(text, k=k)
    if results:
        print(format_results(results))


if __name__ == "__main__":
    main()
