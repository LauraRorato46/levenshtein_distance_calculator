"""Space-optimized Wagner-Fischer edit distance.

The classic Wagner-Fischer algorithm fills an (m+1) x (n+1) matrix to
compute Levenshtein distance. We keep only the current and previous row,
reducing space from O(m*n) to O(min(m,n)). This matters when the inputs are
large strings and is the whole reason this library exists instead of a
one-liner that builds the full matrix.

Design decisions, stated plainly so the tests cannot disagree with the
implementation:

* Only the pure Levenshtein metric is supported: insertions, deletions and
  substitutions, each costing 1. No transposition, no weighted costs, no
  case-folding. If you need Damerau-Levenshtein or weighted edits, this is
  not the right library.
* Inputs must be strings. Anything else raises TypeError eagerly, before
  any work is done, so the failure is easy to locate.
* The empty string is a valid input; distance from "" to s is len(s).
* The return type is a plain Python int.
* We iterate over the longer string as the "outer" loop so the row buffer
  stays the length of the shorter string. This is an internal optimization
  and does not change the result.
"""

from __future__ import annotations

from typing import Iterable

__all__ = ["levenshtein_distance", "LevenshteinCalculator"]


def levenshtein_distance(a: str, b: str) -> int:
    """Return the Levenshtein edit distance between two strings.

    Raises TypeError if either argument is not a str. Returns 0 for equal
    strings and len(s) for the distance between "" and s.
    """
    if not isinstance(a, str):
        raise TypeError(f"a must be str, got {type(a).__name__}")
    if not isinstance(b, str):
        raise TypeError(f"b must be str, got {type(b).__name__}")

    if a == b:
        return 0

    if len(a) < len(b):
        a, b = b, a

    if not b:
        return len(a)

    prev = list(range(len(b) + 1))
    cur = [0] * (len(b) + 1)

    for i in range(1, len(a) + 1):
        cur[0] = i
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            cost = 0 if ai == b[j - 1] else 1
            cur[j] = min(
                prev[j] + 1,
                cur[j - 1] + 1,
                prev[j - 1] + cost,
            )
        prev, cur = cur, prev

    return prev[-1]


class LevenshteinCalculator:
    """Stateless wrapper around :func:`levenshtein_distance`.

    Some callers prefer an object with a method over a free function so they
    can inject it as a dependency. The class holds no state; it exists purely
    to give that call site a stable object to hold onto.
    """

    __slots__ = ()

    def distance(self, a: str, b: str) -> int:
        """Return the Levenshtein distance between *a* and *b*."""
        return levenshtein_distance(a, b)

    def distances(self, reference: str, candidates: Iterable[str]) -> list[int]:
        """Return the distance from *reference* to each candidate, in order."""
        return [self.distance(reference, c) for c in candidates]

    def __repr__(self) -> str:
        return "LevenshteinCalculator()"
