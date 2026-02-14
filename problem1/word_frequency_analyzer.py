#!/usr/bin/env python3
"""Word frequency analyzer.

Given a text block, return the top-k most frequent words and counts.
Capitalization and punctuation are ignored.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from typing import Iterable


WORD_PATTERN = re.compile(r"[A-Za-z0-9]+")
SAMPLE_INPUTS = [
    (
        "Input 1",
        "The quick brown fox jumps over the lazy dog. The dog wasn\u2019t amused; the fox was.",
    ),
    (
        "Input 2",
        "Data, data, data! I can't make bricks without clay, said Sherlock. DATA drives decisions.",
    ),
    (
        "Input 3",
        "To be, or not to be\u2014that is the question:\nWhether 'tis nobler in the mind to suffer...",
    ),
]


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


def run_sample_inputs(k: int) -> None:
    """Run the analyzer against the built-in sample inputs."""
    print("Problem 1: Word Frequency Analyzer")
    for index, (label, text) in enumerate(SAMPLE_INPUTS):
        print(f"\n{label}")
        print(text)
        print("Output:")
        results = top_k_frequent_words(text, k=k)
        if results:
            print(format_results(results))
        else:
            print("(no words)")

        if index != len(SAMPLE_INPUTS) - 1:
            print()


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Analyze word frequency from stdin, or run built-in sample inputs "
            "with --samples."
        )
    )
    parser.add_argument("k", nargs="?", default=10, type=int, help="Number of top items.")
    parser.add_argument(
        "--samples",
        action="store_true",
        help="Run the three built-in sample inputs in this file.",
    )
    args = parser.parse_args(argv)
    if args.k < 0:
        parser.error("k must be a non-negative integer.")
    return args


def main() -> None:
    """CLI entrypoint."""
    args = parse_args(sys.argv[1:])
    if args.samples:
        run_sample_inputs(args.k)
        return

    text = sys.stdin.read()
    if not text.strip():
        run_sample_inputs(args.k)
        return

    results = top_k_frequent_words(text, k=args.k)
    if results:
        print(format_results(results))


if __name__ == "__main__":
    main()
