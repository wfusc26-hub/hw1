#!/usr/bin/env python3
"""Group words that are anagrams of each other."""

from __future__ import annotations

import json
import sys
from collections import defaultdict

TEST_INPUT_LINES = [
    "listen silent enlist inlets google giggle rat tar art",
    "dusty study night thing cat act tac tacit attic tactic",
    "state taste tates seats asset teats teat set eats east",
]


def group_anagrams(words: list[str]) -> list[list[str]]:
    """Return groups of words that are anagrams.

    Words are grouped by their sorted-character signature.
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        signature = "".join(sorted(word))
        groups[signature].append(word)
    return list(groups.values())


def run_embedded_tests() -> None:
    """Run the bundled Problem 3 test inputs."""
    for idx, line in enumerate(TEST_INPUT_LINES, start=1):
        words = line.split()
        print(f"Input {idx}:")
        print(line)
        print("Output:")
        print(json.dumps(group_anagrams(words)))
        print()


def main() -> None:
    """CLI entrypoint.

    - With arguments: groups those words.
    - Without arguments: runs bundled test inputs.
    """
    words = sys.argv[1:]
    if not words:
        run_embedded_tests()
        return

    print(json.dumps(group_anagrams(words)))


if __name__ == "__main__":
    main()
