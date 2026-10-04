# Levenshtein Distance Calculator

Computes the edit distance between two strings using a space-optimized
Wagner-Fischer algorithm that keeps only two rows of the DP matrix in memory
at a time.

## Usage

```python
from levenshtein_distance_calculator import levenshtein_distance, LevenshteinCalculator

levenshtein_distance("kitten", "sitting")  # -> 3

# Object form, useful for dependency injection:
calc = LevenshteinCalculator()
calc.distance("Saturday", "Sunday")          # -> 3
calc.distances("cat", ["cat", "cot", "dog"])  # -> [0, 1, 3]
```

## Why this exists

The textbook Wagner-Fischer algorithm builds a full `(m+1) x (n+1)` matrix,
which is wasteful: only the previous row is needed to compute the next one.
This library keeps two rows, dropping space from `O(m*n)` to `O(min(m,n))`.
That is the only reason it exists instead of pasting a one-liner from
Stack Overflow. The trade-off is that you cannot reconstruct the edit script
from it; if you need the actual edits, use a full-matrix implementation.

Only the pure metric is supported: insertions, deletions and substitutions,
each costing 1. No transposition (that is Damerau-Levenshtein), no weighted
costs, no case-folding. Inputs must be `str`; anything else raises
`TypeError`.

## The awkward edge

Distance is measured over Unicode **code points**, not grapheme clusters.
`levenshtein_distance("\u00e9", "e\u0301")` returns 2, not 0, even though both
render as the same glyph. Normalize your strings beforehand if you want
glyph-level comparison.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

