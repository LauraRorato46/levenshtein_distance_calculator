import unittest

from levenshtein_distance_calculator import levenshtein_distance, LevenshteinCalculator


class TestLevenshteinDistance(unittest.TestCase):

    def test_identical_strings(self):
        self.assertEqual(levenshtein_distance("abc", "abc"), 0)

    def test_empty_first(self):
        self.assertEqual(levenshtein_distance("", "abc"), 3)

    def test_empty_second(self):
        self.assertEqual(levenshtein_distance("abc", ""), 3)

    def test_both_empty(self):
        self.assertEqual(levenshtein_distance("", ""), 0)

    def test_single_substitution(self):
        self.assertEqual(levenshtein_distance("cat", "cot"), 1)

    def test_single_insertion(self):
        self.assertEqual(levenshtein_distance("ct", "cat"), 1)

    def test_single_deletion(self):
        self.assertEqual(levenshtein_distance("cat", "ct"), 1)

    def test_kitten_sitting(self):
        # classic textbook example: kitten -> sitting = 3
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)

    def test_saturday_sunday(self):
        # classic textbook example: Saturday -> Sunday = 3
        self.assertEqual(levenshtein_distance("Saturday", "Sunday"), 3)

    def test_order_invariance(self):
        a, b = "flaw", "lawn"
        self.assertEqual(levenshtein_distance(a, b), levenshtein_distance(b, a))

    def test_completely_different(self):
        self.assertEqual(levenshtein_distance("abc", "xyz"), 3)

    def test_unicode_runes(self):
        # operates on code points, not grapheme clusters. Each emoji here is
        # one code point, so the distance is 2 (two single-char substitutions).
        self.assertEqual(levenshtein_distance("\U0001F600", "\U0001F603"), 1)

    def test_repeated_chars(self):
        self.assertEqual(levenshtein_distance("aaaa", "aa"), 2)

    def test_non_string_first_raises(self):
        with self.assertRaises(TypeError):
            levenshtein_distance(123, "abc")

    def test_non_string_second_raises(self):
        with self.assertRaises(TypeError):
            levenshtein_distance("abc", None)

    def test_returns_int(self):
        result = levenshtein_distance("a", "b")
        self.assertIsInstance(result, int)


class TestLevenshteinCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = LevenshteinCalculator()

    def test_distance_method_matches_function(self):
        self.assertEqual(
            self.calc.distance("kitten", "sitting"),
            levenshtein_distance("kitten", "sitting"),
        )

    def test_distances_returns_list_in_order(self):
        result = self.calc.distances("cat", ["cat", "cot", "dog"])
        self.assertEqual(result, [0, 1, 3])

    def test_distances_with_empty_candidates(self):
        self.assertEqual(self.calc.distances("cat", []), [])

    def test_repr(self):
        self.assertEqual(repr(self.calc), "LevenshteinCalculator()")


if __name__ == "__main__":
    unittest.main()
