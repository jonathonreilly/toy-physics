#!/usr/bin/env python3
"""
Exact link-channel compression for the Poissonized plaquette occupation law.

This runner takes the exact Poissonized occupation/intertwiner compression one
step further:

1. truncate plaquette occupations to Omega_K = {(m,n): m+n <= K}
2. the induced link data are finite count pairs (r,s) with r+s <= 4K
3. the exact local link tensor only needs the invariant channel space
      Inv(3^{⊗r} ⊗ 3bar^{⊗s})
4. that gives a finite exact link-channel alphabet for every K

The runner computes the exact invariant-space dimensions by SU(3) tensor-product
recursion and identifies the first special channels:
regular, X, and B.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


TRUNCATION_LEVELS = (8, 12, 16, 20)
MAX_LINK_TOTAL = 4 * max(TRUNCATION_LEVELS)
SHOW_CASES = ((0, 0), (1, 1), (2, 2), (3, 0), (0, 3), (4, 1), (4, 4), (6, 3))


@dataclass(frozen=True)
class Irrep:
    a: int
    b: int


def tensor_with_fundamental(counts: Counter[Irrep]) -> Counter[Irrep]:
    out: Counter[Irrep] = Counter()
    for rep, mult in counts.items():
        out[Irrep(rep.a + 1, rep.b)] += mult
        if rep.a > 0:
            out[Irrep(rep.a - 1, rep.b + 1)] += mult
        if rep.b > 0:
            out[Irrep(rep.a, rep.b - 1)] += mult
    return out


def tensor_with_antifundamental(counts: Counter[Irrep]) -> Counter[Irrep]:
    out: Counter[Irrep] = Counter()
    for rep, mult in counts.items():
        out[Irrep(rep.a, rep.b + 1)] += mult
        if rep.b > 0:
            out[Irrep(rep.a + 1, rep.b - 1)] += mult
        if rep.a > 0:
            out[Irrep(rep.a - 1, rep.b)] += mult
    return out


def build_tables(max_total: int = MAX_LINK_TOTAL) -> list[list[Counter[Irrep]]]:
    tables: list[list[Counter[Irrep]]] = [[Counter() for _ in range(max_total + 1)] for _ in range(max_total + 1)]
    tables[0][0][Irrep(0, 0)] = 1

    for r in range(max_total + 1):
        for s in range(max_total + 1):
            if r == 0 and s == 0:
                continue
            if r > 0 and s > 0:
                left = tensor_with_fundamental(tables[r - 1][s])
                down = tensor_with_antifundamental(tables[r][s - 1])
                if left != down:
                    raise ValueError(f"inconsistent SU(3) recursion at (r,s)=({r},{s})")
                tables[r][s] = left
            elif r > 0:
                tables[r][s] = tensor_with_fundamental(tables[r - 1][s])
            else:
                tables[r][s] = tensor_with_antifundamental(tables[r][s - 1])
    return tables


def inv_dim(tables: list[list[Counter[Irrep]]], r: int, s: int) -> int:
    return tables[r][s].get(Irrep(0, 0), 0)


def nonzero_support_pairs(tables: list[list[Counter[Irrep]]], link_total_cutoff: int) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for r in range(link_total_cutoff + 1):
        for s in range(link_total_cutoff + 1 - r):
            if inv_dim(tables, r, s) > 0:
                pairs.append((r, s))
    return pairs


def link_channel_totals(tables: list[list[Counter[Irrep]]], truncation_level: int) -> tuple[int, int, tuple[int, int], int]:
    link_total_cutoff = 4 * truncation_level
    support = 0
    channels = 0
    max_pair = (0, 0)
    max_dim = 0
    for r in range(link_total_cutoff + 1):
        for s in range(link_total_cutoff + 1 - r):
            dim = inv_dim(tables, r, s)
            channels += dim
            if dim > 0:
                support += 1
                if dim > max_dim:
                    max_dim = dim
                    max_pair = (r, s)
    return support, channels, max_pair, max_dim


def local_plaquette_alphabet_size(truncation_level: int) -> int:
    return (truncation_level + 1) * (truncation_level + 2) // 2


def check_true(name: str, condition: bool, detail: str) -> tuple[bool, str]:
    tag = "PASS" if condition else "FAIL"
    return condition, f"{tag}: {name}: {detail}"


def main() -> int:
    tables = build_tables()

    print("=" * 78)
    print("EXACT LINK-CHANNEL COMPRESSION FOR THE POISSONIZED PLAQUETTE LAW")
    print("=" * 78)
    print()
    print("Exact local truncation structure")
    print("  Plaquette truncation: Omega_K = {(m,n) in N^2 : m+n <= K}")
    print("  A link sees four incident plaquettes, so the induced link counts satisfy")
    print("    0 <= r,s and r+s <= 4K.")
    print("  The exact local link tensor then lives on the invariant channel space")
    print("    Inv(3^{⊗r} ⊗ 3bar^{⊗s}).")
    print()
    print("Exact first channels")
    for r, s in SHOW_CASES:
        print(f"  (r,s)=({r:2d},{s:2d})  dim Inv = {inv_dim(tables, r, s)}")
    print()
    print("  regular link sector:   dim Inv(1,1) = 1")
    print("  crossing X sector:     dim Inv(2,2) = 2")
    print("  baryon B sector:       dim Inv(3,0) = dim Inv(0,3) = 1")
    print()
    print("Truncation-level channel counts")
    for truncation_level in TRUNCATION_LEVELS:
        support, channels, max_pair, max_dim = link_channel_totals(tables, truncation_level)
        print(
            f"  K={truncation_level:2d}"
            f"  |Omega_K|={local_plaquette_alphabet_size(truncation_level):3d}"
            f"  nonzero (r,s) support={support:4d}"
            f"  total link channels Xi_K={channels}"
            f"  max at {max_pair} -> {max_dim}"
        )
    print()

    nonzero_pairs = nonzero_support_pairs(tables, 4 * max(TRUNCATION_LEVELS))
    checks = [
        check_true(
            "regular channel multiplicity",
            inv_dim(tables, 1, 1) == 1,
            f"dim Inv(1,1) = {inv_dim(tables, 1, 1)}",
        ),
        check_true(
            "crossing X channel multiplicity",
            inv_dim(tables, 2, 2) == 2,
            f"dim Inv(2,2) = {inv_dim(tables, 2, 2)}",
        ),
        check_true(
            "baryon B channel multiplicity",
            inv_dim(tables, 3, 0) == 1 and inv_dim(tables, 0, 3) == 1,
            f"dim Inv(3,0) = {inv_dim(tables, 3, 0)}, dim Inv(0,3) = {inv_dim(tables, 0, 3)}",
        ),
        check_true(
            "triality-zero support condition up to the audited window",
            all((r - s) % 3 == 0 for r, s in nonzero_pairs),
            "every nonzero invariant channel in the audited window has r-s == 0 mod 3",
        ),
        check_true(
            "no low-order support outside triality zero",
            all(inv_dim(tables, r, s) == 0 for r in range(9) for s in range(9) if (r - s) % 3 != 0),
            "all audited low-order nonzero channels sit on triality-zero pairs",
        ),
        check_true(
            "K=20 plaquette alphabet size",
            local_plaquette_alphabet_size(20) == 231,
            f"|Omega_20| = {local_plaquette_alphabet_size(20)}",
        ),
        check_true(
            "K=20 link-count support size",
            link_channel_totals(tables, 20)[0] == 1107,
            f"support = {link_channel_totals(tables, 20)[0]}",
        ),
        check_true(
            "K=20 total link-channel count",
            link_channel_totals(tables, 20)[1] == 5751651283997210283708144343174357,
            f"Xi_20 = {link_channel_totals(tables, 20)[1]}",
        ),
    ]

    print("Checks")
    passed = 0
    for ok, message in checks:
        print(" ", message)
        passed += int(ok)
    failed = len(checks) - passed
    print()
    print(f"SUMMARY: exact {passed} pass / {failed} fail")
    print()

    if failed:
        return 1

    print("Conclusion: after plaquette truncation to Omega_K, the exact evaluator")
    print("state space is a finite tensor network with plaquette occupation states")
    print("and finite link-channel alphabets. The first exact special channels are")
    print("the regular, X, and B sectors. The remaining evaluator problem is no")
    print("longer whether the local state space is finite, but how to compress or")
    print("contract the rapidly growing invariant-channel basis efficiently.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
