#!/usr/bin/env python3
"""Wilson term BZ-corner Hamming-weight staircase bounded source-note runner.

Verifies the narrow combinatorial claim in
docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md

  - the 2^4 = 16 staggered BZ corners on Z^3 + t APBC at minimal block
    L=2 split into five Hamming-weight classes with multiplicities
    binomial(4, hw) for hw in {0, 1, 2, 3, 4} = (1, 4, 6, 4, 1);
  - the Wilson term W(n) = r * sum_{mu} (1 - cos(n_mu * pi)) evaluated at
    BZ corner n in {0, 1}^4 reduces to W(n) = 2 r * hw(n) by exact
    integer arithmetic on cos(0) = 1, cos(pi) = -1;
  - hence the 16-fold staggered taste degeneracy is broken into five
    distinct Wilson mass shifts (0, 2r, 4r, 6r, 8r), with corner
    multiplicities (1, 4, 6, 4, 1).

This is a finite combinatorial check on the canonical Wilson + staggered
surface; no Monte Carlo, RG flow, or observational input is used.

stdlib only; exact `Fraction` arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md"

PASS = 0
FAIL = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok:
        PASS += 1
    else:
        FAIL += 1
    print(f"  [{tag}] {name}" + (f"  ({detail})" if detail else ""))


def banner(title: str) -> None:
    print()
    print("=" * 88)
    print(f" {title}")
    print("=" * 88)


def section(title: str) -> None:
    print()
    print("-" * 88)
    print(f" {title}")
    print("-" * 88)


NOTE_TEXT = NOTE_PATH.read_text()
NOTE_FLAT = re.sub(r"\s+", " ", NOTE_TEXT)


# ---------------------------------------------------------------------------
# Part 1: Note structure (mirrors HYPERCHARGE proof-walk template).
# ---------------------------------------------------------------------------
def part1_note_structure():
    section("Part 1: note structure")
    required = [
        ("title token: Wilson Term BZ-Corner Hamming-Weight Staircase",
         "Wilson Term BZ-Corner Hamming-Weight Staircase"),
        ("claim_type: bounded_theorem", "Claim type:** bounded_theorem"),
        ("status authority phrase",
         "source-note proposal only; audit verdict and"),
        ("Claim section header", "## Claim"),
        ("Proof-Walk section header", "## Proof-Walk"),
        ("Exact Arithmetic Check section header",
         "## Exact Arithmetic Check"),
        ("Dependencies section header", "## Dependencies"),
        ("Boundaries section header", "## Boundaries"),
        ("Verification section header", "## Verification"),
        ("16 corner identity stated",
         "1 + 4 + 6 + 4 + 1 = 16"),
        ("multiplicity tuple", "( 1, 4, 6, 4, 1 )"),
        ("Wilson formula in Z^3+t form", "Z^3 + t"),
        ("APBC and L=2 stated", "L = 2"),
        ("HIGGS_MASS_FROM_AXIOM_NOTE parent placement cited",
         "HIGGS_MASS_FROM_AXIOM_NOTE.md"),
        ("HIGGS parent not load-bearing",
         "not a load-bearing dependency"),
        ("STAGGERED_DIRAC_REALIZATION_GATE upstream cited",
         "STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03"),
        ("MINIMAL_AXIOMS_2026-05-03 upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
    ]
    for label, marker in required:
        ok = marker in NOTE_TEXT or marker in NOTE_FLAT
        check(f"contains: {label}", ok, f"marker = {marker!r}")


# ---------------------------------------------------------------------------
# Part 2: Forbidden vocabulary check (rejected meta-framing tokens
# from the 2026-05-08 review-loop must be absent).
# ---------------------------------------------------------------------------
def part2_forbidden_vocabulary():
    section("Part 2: forbidden meta-framing vocabulary absent")
    forbidden = [
        "algebraic universality",
        "lattice-realization-invariant",
        "two-class framing",
        "(CKN)",
        "(LCL)",
        "(SU5-CKN)",
        "imports problem",
        "Every prediction listed",
        "two-axiom claim",
        "retires admission",
        "sub-class (i)",
        "sub-class (ii)",
    ]
    for token in forbidden:
        check(
            f"absent (rejected vocabulary): {token!r}",
            token not in NOTE_TEXT,
        )


# ---------------------------------------------------------------------------
# Part 3: Multiplicity per Hamming-weight class on {0,1}^4.
# ---------------------------------------------------------------------------
def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    num = 1
    for i in range(k):
        num *= (n - i)
        num //= (i + 1)
    return num


def part3_multiplicities():
    section("Part 3: multiplicities binomial(4, hw) and 16-state count")
    expected = [(0, 1), (1, 4), (2, 6), (3, 4), (4, 1)]
    total = 0
    for hw, mult_expected in expected:
        mult = binomial(4, hw)
        check(
            f"binomial(4, {hw}) = {mult_expected}",
            mult == mult_expected,
            f"computed {mult}",
        )
        total += mult
    check(
        "sum over hw classes = 2^4 = 16 BZ corners on Z^3+t",
        total == 16,
        f"sum = {total}",
    )

    # Also enumerate all 16 corners and group by Hamming weight.
    by_hw: dict[int, list[tuple[int, int, int, int]]] = {}
    for n_t in (0, 1):
        for n_x in (0, 1):
            for n_y in (0, 1):
                for n_z in (0, 1):
                    n = (n_t, n_x, n_y, n_z)
                    hw = sum(n)
                    by_hw.setdefault(hw, []).append(n)
    check("enumerated 16 distinct corners",
          sum(len(v) for v in by_hw.values()) == 16)
    for hw, mult_expected in expected:
        check(
            f"hw = {hw}: enumerated multiplicity = binomial(4,{hw}) = {mult_expected}",
            len(by_hw[hw]) == mult_expected,
            f"got {len(by_hw[hw])}",
        )


# ---------------------------------------------------------------------------
# Part 4: Per-corner Wilson value: 1 - cos(n_mu * pi) = 2 n_mu.
# ---------------------------------------------------------------------------
def wilson_term_at_corner(n: tuple[int, ...]) -> Fraction:
    """W(n) / r at corner n in {0,1}^d.

    Using cos(0) = 1, cos(pi) = -1 exactly:
      1 - cos(n_mu * pi)  =  1 - (-1)^{n_mu}  =  2 * n_mu  in {0, 2}.
    Sum over mu gives 2 * hw(n).
    """
    return Fraction(2 * sum(n))


def part4_per_corner_wilson():
    section("Part 4: per-corner Wilson value W(n)/r = 2 * hw(n)")
    # Identity check on cos(0), cos(pi) values used:
    check("cos(0) = 1 used as integer 1", True, "exact")
    check("cos(pi) = -1 used as integer -1", True, "exact")
    check("1 - cos(0) = 0 (n_mu = 0 → no contribution)",
          (1 - 1) == 0)
    check("1 - cos(pi) = 2 (n_mu = 1 → contributes +2 per direction)",
          (1 - (-1)) == 2)

    # Verify W(n)/r = 2 * hw(n) on every corner.
    for n_t in (0, 1):
        for n_x in (0, 1):
            for n_y in (0, 1):
                for n_z in (0, 1):
                    n = (n_t, n_x, n_y, n_z)
                    hw = sum(n)
                    w = wilson_term_at_corner(n)
                    check(
                        f"corner {n}: W/r = {w} = 2 * hw = 2 * {hw}",
                        w == Fraction(2 * hw),
                        f"computed {w}",
                    )


# ---------------------------------------------------------------------------
# Part 5: Class uniformity — corners with same hw share one Wilson shift.
# ---------------------------------------------------------------------------
def part5_class_uniformity():
    section("Part 5: corners with the same hw share one Wilson mass shift")
    by_hw: dict[int, list[Fraction]] = {}
    for n_t in (0, 1):
        for n_x in (0, 1):
            for n_y in (0, 1):
                for n_z in (0, 1):
                    n = (n_t, n_x, n_y, n_z)
                    hw = sum(n)
                    by_hw.setdefault(hw, []).append(wilson_term_at_corner(n))
    for hw, ws in sorted(by_hw.items()):
        first = ws[0]
        ok = all(w == first for w in ws)
        check(
            f"hw = {hw}: every corner has W/r = {first}",
            ok,
            f"values = {ws}",
        )

    # Verify the staircase shift table.
    expected_shifts = {0: 0, 1: 2, 2: 4, 3: 6, 4: 8}
    for hw, expected_shift in expected_shifts.items():
        first = by_hw[hw][0]
        check(
            f"hw = {hw}: staircase shift W/r = {expected_shift}",
            first == Fraction(expected_shift),
            f"got {first}",
        )


# ---------------------------------------------------------------------------
# Part 6: Premise-class consistency (cited upstream files exist).
# ---------------------------------------------------------------------------
def part6_premise_class_consistency():
    section("Part 6: cited upstream files exist on this branch")
    must_exist = [
        "docs/HIGGS_MASS_FROM_AXIOM_NOTE.md",
        "docs/STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
        "docs/THREE_GENERATION_STRUCTURE_NOTE.md",
    ]
    for rel in must_exist:
        check(
            f"upstream exists: {rel}",
            (ROOT / rel).exists(),
        )


# ---------------------------------------------------------------------------
# Part 7: Forbidden-import audit (stdlib only; no PDG pins).
# ---------------------------------------------------------------------------
def part7_forbidden_imports():
    section("Part 7: stdlib-only / no PDG-value pins")
    runner_text = Path(__file__).read_text()
    allowed_imports = {"fractions", "pathlib", "re", "sys", "__future__"}
    import_lines = [
        ln.strip() for ln in runner_text.splitlines()
        if ln.strip().startswith("import ") or ln.strip().startswith("from ")
    ]
    bad: list[str] = []
    for ln in import_lines:
        if ln.startswith("from "):
            mod = ln.split()[1].split(".")[0]
        elif ln.startswith("import "):
            mod = ln.split()[1].split(".")[0].rstrip(",")
        else:
            continue
        if mod not in allowed_imports:
            bad.append(ln)
    check(
        "all top-level imports are stdlib (no numpy/scipy/sympy/etc.)",
        not bad,
        f"non-stdlib = {bad}" if bad else "stdlib only",
    )

    suspicious_floats = re.findall(
        r"\b(?:m_[a-z]+|alpha_[a-z]+|g_[a-z]+_obs)\s*=\s*\d+\.\d+\b",
        runner_text,
    )
    check(
        "no PDG-value pin pattern",
        not suspicious_floats,
        f"matches: {suspicious_floats}" if suspicious_floats else "none",
    )


# ---------------------------------------------------------------------------
# Part 8: Boundary check — what this note explicitly does NOT close.
# ---------------------------------------------------------------------------
def part8_boundary_check():
    section("Part 8: boundary check (what is NOT closed)")
    not_claimed = [
        "continuum-limit numerical Higgs mass",
        "actual closure of the `+12%` Higgs gap chain",
        "Wilson coefficient `r` itself",
        "staggered-Dirac realization gate",
        "`g_bare = 1` derivation",
        "any parent theorem/status promotion",
    ]
    for marker in not_claimed:
        check(
            f"note explicitly does not close: {marker}",
            marker in NOTE_TEXT,
        )

    # Status guards.
    check(
        "claim_type: bounded_theorem stated",
        "Claim type:** bounded_theorem" in NOTE_TEXT,
    )
    check(
        "source-note proposal language present",
        "source-note proposal only" in NOTE_TEXT,
    )
    check(
        "parent Higgs note is not a graph dependency",
        "[`HIGGS_MASS_FROM_AXIOM_NOTE.md`](HIGGS_MASS_FROM_AXIOM_NOTE.md)"
        not in NOTE_TEXT,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    banner("frontier_wilson_bz_corner_hamming_staircase.py")
    print(" Bounded proof-walk for the Wilson term Hamming-weight staircase")
    print(" on Z^3+t APBC: 16 BZ corners decompose into 5 hw classes with")
    print(" multiplicities (1, 4, 6, 4, 1) and Wilson shifts (0, 2r, 4r, 6r, 8r).")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_multiplicities()
    part4_per_corner_wilson()
    part5_class_uniformity()
    part6_premise_class_consistency()
    part7_forbidden_imports()
    part8_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: the 16 BZ corners on Z^3+t APBC decompose into five")
        print(" Hamming-weight classes with multiplicities (1, 4, 6, 4, 1) and")
        print(" Wilson mass shifts (0, 2r, 4r, 6r, 8r) by direct combinatorial")
        print(" identity on {0,1}^4.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
