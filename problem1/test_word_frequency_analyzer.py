import unittest

from word_frequency_analyzer import top_k_frequent_words


class TestWordFrequencyAnalyzer(unittest.TestCase):
    def test_ignores_case_and_punctuation(self) -> None:
        text = "Hello, hello! HELLO... world; World?"
        self.assertEqual(
            top_k_frequent_words(text, k=10),
            [("hello", 3), ("world", 2)],
        )

    def test_breaks_ties_alphabetically(self) -> None:
        text = "banana apple cherry banana apple cherry"
        self.assertEqual(
            top_k_frequent_words(text, k=10),
            [("apple", 2), ("banana", 2), ("cherry", 2)],
        )

    def test_returns_exactly_k_items_when_possible(self) -> None:
        text = "z y x w v u t s r q p o"
        result = top_k_frequent_words(text, k=10)
        self.assertEqual(len(result), 10)
        self.assertEqual(result[0], ("o", 1))
        self.assertEqual(result[-1], ("x", 1))

    def test_returns_all_items_when_unique_words_less_than_k(self) -> None:
        text = "one two three"
        self.assertEqual(
            top_k_frequent_words(text, k=10),
            [("one", 1), ("three", 1), ("two", 1)],
        )

    def test_non_positive_k_returns_empty_list(self) -> None:
        text = "a a b"
        self.assertEqual(top_k_frequent_words(text, k=0), [])
        self.assertEqual(top_k_frequent_words(text, k=-1), [])


if __name__ == "__main__":
    unittest.main()
