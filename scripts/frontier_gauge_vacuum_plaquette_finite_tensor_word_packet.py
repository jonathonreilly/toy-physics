#!/usr/bin/env python3
"""Gauge-vacuum plaquette finite tensor-word packet — bounded source-note runner.

Verifies docs/GAUGE_VACUUM_PLAQUETTE_FINITE_TENSOR_WORD_PACKET_BOUNDED_NOTE_2026-05-10.md
on the truncated NMAX = 4 weight box at MODE_MAX = 80 Wilson Bessel mode
sum, beta = 6:

  (P1) nonnegativity of tensor_word matrix entries
  (P2) conjugation-swap symmetry of tensor_word
  (P3) nonnegativity of boundary amplitude under unit-vector readout

Plus consistency check (derived corollary, not separate load-bearing):
  S · boundary0 = boundary0 exactly (since (0,0) is fixed by S),
  and therefore S · amp = amp follows from (P2) — verified numerically
  to confirm the chain composes consistently, not as a separate property.

The construction is:

  diag_c    = diag( c_(p,q)(6) / (d_(p,q) c_(0,0)(6)) ) on NMAX=4 box
  N_f       = SU(3) fundamental fusion-multiplicity matrix on the box
  N_fbar    = SU(3) anti-fundamental fusion-multiplicity matrix on the box
  tensor_word = diag_c · (N_f + N_fbar) · diag_c · (N_f + N_fbar)^T · diag_c

where c_(p,q)(6) is computed via Schur-Weyl Bessel-determinant truncated
to MODE_MAX = 80 modes (matching the Wilson-environment companion
GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09).

This is a split note following prior audit feedback on the parent
GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.
The bounded scope is ONLY (P1)-(P3); the parent's matrix-element identity
between the constructed matrix and actual spatial-environment boundary
amplitudes is NOT claimed here.

Imports: numpy + scipy.special.iv (family convention; matches the
Wilson-environment companion runner
frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.py).
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

import numpy as np
from scipy.special import iv

ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "GAUGE_VACUUM_PLAQUETTE_FINITE_TENSOR_WORD_PACKET_BOUNDED_NOTE_2026-05-10.md"

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


# Truncation parameters and physical inputs (match Wilson-environment companion)
BETA = 6.0
ARG = BETA / 3.0
MODE_MAX = 80
NMAX = 4

NOTE_TEXT = NOTE_PATH.read_text() if NOTE_PATH.exists() else ""
NOTE_FLAT = re.sub(r"\s+", " ", NOTE_TEXT)


# ---------------------------------------------------------------------------
# Canonical truncated local Wilson coefficient (Schur-Weyl Bessel determinant)
# Matches companion frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute
# ---------------------------------------------------------------------------
def dim_su3(p: int, q: int) -> int:
    """Standard SU(3) irrep dimension for (p, q) Dynkin label."""
    return (p + 1) * (q + 1) * (p + q + 2) // 2


def highest_weight_triple(p: int, q: int) -> list[int]:
    return [p + q, q, 0]


def coefficient_matrix(mode: int, lam: list[int]) -> np.ndarray:
    return np.array(
        [[iv(mode + lam[j] + i - j, ARG) for j in range(3)] for i in range(3)],
        dtype=float,
    )


def wilson_character_coefficient(p: int, q: int) -> float:
    """c_(p,q)(beta) via Schur-Weyl Bessel-determinant, truncated to MODE_MAX modes."""
    lam = highest_weight_triple(p, q)
    total = 0.0
    for mode in range(-MODE_MAX, MODE_MAX + 1):
        total += float(np.linalg.det(coefficient_matrix(mode, lam)))
    return total


def weights_box(nmax: int) -> list[tuple[int, int]]:
    return [(p, q) for p in range(nmax + 1) for q in range(nmax + 1)]


# ---------------------------------------------------------------------------
# SU(3) fundamental + anti-fundamental fusion multiplicities on the box
# ---------------------------------------------------------------------------
def build_mult_matrices(nmax: int):
    """Build N_f and N_fbar matrices on the NMAX weight box.

    Standard SU(3) tensoring with fundamental (1,0) and anti-fundamental (0,1)
    via the six-neighbor recurrence, restricted to (p, q) ∈ [0..nmax]² box.
    """
    weights = weights_box(nmax)
    index = {w: i for i, w in enumerate(weights)}
    nf = np.zeros((len(weights), len(weights)), dtype=int)
    nfb = np.zeros((len(weights), len(weights)), dtype=int)
    for p, q in weights:
        i = index[(p, q)]
        for a, b in [(p + 1, q), (p - 1, q + 1), (p, q - 1)]:
            if a >= 0 and b >= 0 and (a, b) in index:
                nf[index[(a, b)], i] += 1
        for a, b in [(p, q + 1), (p + 1, q - 1), (p - 1, q)]:
            if a >= 0 and b >= 0 and (a, b) in index:
                nfb[index[(a, b)], i] += 1
    return nf, nfb, weights, index


def conjugation_swap_matrix(weights, index) -> np.ndarray:
    """Permutation matrix swap[(p,q) → (q,p)] on the box."""
    swap = np.zeros((len(weights), len(weights)), dtype=int)
    for w in weights:
        swap[index[(w[1], w[0])], index[w]] = 1
    return swap


# ---------------------------------------------------------------------------
# Part 1: Note structure
# ---------------------------------------------------------------------------
def part1_note_structure():
    section("Part 1: note structure")
    required = [
        ("title token: Finite Tensor-Word Packet",
         "Finite Tensor-Word Packet"),
        ("claim_type: bounded_theorem",
         "Claim type:** bounded_theorem"),
        ("bounded status phrase",
         "finite truncated tensor-word packet only"),
        ("Claim section header", "## Claim"),
        ("Bounded admissions section header", "## Bounded admissions"),
        ("Proof-Walk section header", "## Proof-Walk"),
        ("Dependencies section header", "## Dependencies"),
        ("Boundaries section header", "## Boundaries"),
        ("Verification section header", "## Verification"),
        ("(P1) nonnegativity stated", "(P1) **Nonnegativity"),
        ("(P2) conjugation-swap stated", "(P2) **Conjugation-swap"),
        ("(P3) boundary nonneg stated", "(P3) **Nonnegative boundary amplitude"),
        ("(P3-corollary) S·boundary0=boundary0 derived from (P2)",
         "Derived corollary of (P2)"),
        ("BA-1 truncated Wilson coefficients stated",
         "(BA-1) **Canonical truncated local Wilson coefficients.**"),
        ("BA-2 fusion multiplicities stated",
         "(BA-2) **`SU(3)` fundamental and anti-fundamental fusion"),
        ("parent-note cite: GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER",
         "GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md"),
        ("Wilson-environment companion cited (rho_pq6)",
         "GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09"),
        ("MINIMAL_AXIOMS upstream cited",
         "MINIMAL_AXIOMS_2026-05-03"),
        ("explicit not-claimed: parent's matrix-element identity",
         "claim the parent note's structural matrix-element identity"),
        ("explicit not-claimed: full untruncated case",
         "close the full untruncated tensor-transfer construction"),
        ("split-note finite-packet framing",
         "split note for one finite tensor-word packet"),
    ]
    for label, marker in required:
        ok = marker in NOTE_TEXT or marker in NOTE_FLAT
        check(f"contains: {label}", ok, f"marker = {marker!r}")


# ---------------------------------------------------------------------------
# Part 2: Forbidden vocabulary
# ---------------------------------------------------------------------------
def part2_forbidden_vocabulary():
    section("Part 2: forbidden meta-framing vocabulary absent (note + runner docstring)")
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
        "Wilson asymptotic universality",
        "Bounded statement.",  # rejected in PR #887 review
        "post-2026-05-10 narrowing",  # rejected in PR #887 review
        "explicitly out of the bounded scope",  # rejected in PR #887 review
    ]
    runner_text = Path(__file__).read_text()
    docstring_match = re.match(r'^(?:#![^\n]*\n)?[^"]*"""(.*?)"""',
                               runner_text, re.DOTALL)
    runner_docstring = docstring_match.group(1) if docstring_match else ""
    for token in forbidden:
        check(
            f"absent in note (rejected vocabulary): {token!r}",
            token not in NOTE_TEXT,
        )
        check(
            f"absent in runner docstring (rejected vocabulary): {token!r}",
            token not in runner_docstring,
        )


# ---------------------------------------------------------------------------
# Part 3: Cited upstreams
# ---------------------------------------------------------------------------
def part3_cited_upstreams():
    section("Part 3: cited upstreams (all on origin/main)")
    must_exist = [
        "docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_TENSOR_TRANSFER_THEOREM_NOTE.md",
        "docs/GAUGE_VACUUM_PLAQUETTE_RHO_PQ6_WILSON_ENVIRONMENT_BOUNDED_NOTE_2026-05-09.md",
        "docs/MINIMAL_AXIOMS_2026-05-03.md",
    ]
    for rel in must_exist:
        check(f"upstream exists: {rel}", (ROOT / rel).exists())


# ---------------------------------------------------------------------------
# Part 4: Construct tensor_word and verify (P1), (P2), (P3.a), (P3.b)
# ---------------------------------------------------------------------------
def part4_construct_and_verify_packet():
    section("Part 4: construct tensor_word; verify (P1), (P2), (P3.a), (P3.b)")
    nf, nfb, weights, index = build_mult_matrices(NMAX)
    swap = conjugation_swap_matrix(weights, index)
    print(f"  truncation: NMAX = {NMAX} (weight box [0..{NMAX}]^2 = {len(weights)} states)")
    print(f"             MODE_MAX = {MODE_MAX} (Wilson Bessel mode sum)")
    print(f"             beta = {BETA}, beta/3 = {ARG}")
    print()

    # Compute Wilson character coefficients on the box
    coeffs = np.array(
        [wilson_character_coefficient(p, q) for p, q in weights], dtype=float
    )
    dims = np.array([dim_su3(p, q) for p, q in weights], dtype=float)
    c00 = coeffs[index[(0, 0)]]
    normalized = coeffs / (dims * c00)

    # (BA-2) sanity checks: N_f and N_fbar entries in {0, 1}
    nf_entries_ok = bool(np.min(nf) >= 0 and np.max(nf) <= 1)
    nfb_entries_ok = bool(np.min(nfb) >= 0 and np.max(nfb) <= 1)
    check("(BA-2) N_f entries in {0, 1}", nf_entries_ok)
    check("(BA-2) N_fbar entries in {0, 1}", nfb_entries_ok)

    # (BA-2) sanity checks: S · N_f = N_fbar · S (conjugation swap)
    nf_swap_diff = int(np.max(np.abs(swap @ nf - nfb @ swap)))
    nfb_swap_diff = int(np.max(np.abs(swap @ nfb - nf @ swap)))
    check(
        "(BA-2) S · N_f = N_fbar · S (fundamental ↔ anti-fundamental conjugation)",
        nf_swap_diff == 0,
        f"max |S·N_f - N_fbar·S| = {nf_swap_diff}",
    )
    check(
        "(BA-2) S · N_fbar = N_f · S (conjugation symmetry)",
        nfb_swap_diff == 0,
        f"max |S·N_fbar - N_f·S| = {nfb_swap_diff}",
    )

    # Local Wilson coefficient sanity: c_(0,0)(6) > 0, normalized[(0,0)] = 1
    c00_pos = bool(c00 > 0)
    norm_00_one = bool(abs(normalized[index[(0, 0)]] - 1.0) < 1e-12)
    check("(BA-1) c_(0,0)(6) > 0", c00_pos, f"c_(0,0)(6) = {c00:.6f}")
    check(
        "(BA-1) normalized[(0,0)] = 1 (definition)",
        norm_00_one,
        f"normalized[(0,0)] = {normalized[index[(0, 0)]]:.15f}",
    )

    # Local Wilson coefficient conjugation symmetry: normalized[(p,q)] = normalized[(q,p)]
    norm_swap_diff = float(
        np.max(np.abs(normalized - normalized[[index[(q, p)] for p, q in weights]]))
    )
    check(
        "(BA-1) c_(p,q)(6) = c_(q,p)(6) up to normalization (conjugation symmetry)",
        norm_swap_diff < 1e-12,
        f"max |normalized - swap·normalized| = {norm_swap_diff:.2e}",
    )

    # Construct tensor_word per eq. (3) of the bounded note
    diag_c = np.diag(normalized)
    tensor_word = diag_c @ (nf + nfb) @ diag_c @ (nf + nfb).T @ diag_c
    print()
    print(f"  tensor_word: {tensor_word.shape[0]} x {tensor_word.shape[1]} real matrix")
    print(f"               built from diag_c · (N_f+N_fbar) · diag_c · (N_f+N_fbar)^T · diag_c")
    print()

    # (P1) nonnegativity
    word_min = float(np.min(tensor_word))
    word_max = float(np.max(tensor_word))
    check(
        "(P1) min(tensor_word) ≥ 0 (nonnegativity of all matrix entries)",
        word_min >= 0.0,
        f"min = {word_min:.6e}, max = {word_max:.6e}",
    )

    # (P2) conjugation-swap symmetry
    word_swap_diff = float(np.max(np.abs(swap @ tensor_word - tensor_word @ swap)))
    check(
        "(P2) ‖S · tensor_word − tensor_word · S‖_∞ < 10⁻¹² (conjugation-swap symmetry)",
        word_swap_diff < 1e-12,
        f"max diff = {word_swap_diff:.2e}",
    )

    # (P3) nonneg boundary amplitude
    boundary0 = np.zeros(len(weights), dtype=float)
    boundary0[index[(0, 0)]] = 1.0
    amp = tensor_word @ boundary0
    amp_min = float(np.min(amp))
    amp_max = float(np.max(amp))
    check(
        "(P3) min(amp) ≥ 0 (nonneg boundary amplitude)",
        amp_min >= 0.0,
        f"min = {amp_min:.6e}, max = {amp_max:.6e}",
    )

    # (P3-corollary, derived from P2): the (0,0) state is fixed by S,
    # so S · boundary0 = boundary0 trivially. Combined with (P2):
    #   S · amp = S · tensor_word · boundary0
    #          = tensor_word · S · boundary0   [by (P2)]
    #          = tensor_word · boundary0
    #          = amp.
    # Verify the trivial S-fixed-point step explicitly, plus the
    # consistency S · amp = amp at numerical precision.
    s_b0_diff = int(np.max(np.abs(swap @ boundary0 - boundary0)))
    check(
        "(P3-corollary, EXACT) S · boundary0 = boundary0 (since (0,0) is "
        "S-fixed)",
        s_b0_diff == 0,
        f"max |S·boundary0 - boundary0| = {s_b0_diff}",
    )
    amp_swap_diff = float(np.max(np.abs(swap @ amp - amp)))
    check(
        "(P3-corollary, consistency) ‖S · amp − amp‖_∞ < 10⁻¹² "
        "(follows from (P2) + S·b0 = b0; consistency check, not separate load-bearing)",
        amp_swap_diff < 1e-12,
        f"max diff = {amp_swap_diff:.2e}",
    )

    # Print sample entries for diagnostic visibility
    print()
    print("  Sample tensor_word entries (boundary-projection diagonals):")
    for w in [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0)]:
        if w in index:
            i = index[w]
            print(f"    tensor_word[{w!s:>9}, (0,0)] = {tensor_word[i, index[(0, 0)]]:.6e}")
    print(f"  amp = tensor_word · e_{{(0,0)}}")
    for w in [(0, 0), (1, 0), (1, 1), (2, 0), (2, 2)]:
        if w in index:
            i = index[w]
            print(f"    amp[{w!s:>9}] = {amp[i]:.6e}")


# ---------------------------------------------------------------------------
# Part 5: Import boundary
# ---------------------------------------------------------------------------
def part5_import_boundary():
    section("Part 5: imports limited to family convention (numpy + scipy)")
    runner_text = Path(__file__).read_text()
    # numpy + scipy.special.iv is the family convention used by the companion
    # frontier_gauge_vacuum_plaquette_rho_pq_6_wilson_environment_compute.
    allowed = {
        "numpy", "scipy", "scipy.special",
        "pathlib", "re", "sys", "__future__",
    }
    bad = []
    for ln in runner_text.splitlines():
        ln = ln.strip()
        if ln.startswith("from "):
            mod = ln.split()[1].split(".")[0]
        elif ln.startswith("import "):
            mod = ln.split()[1].split(".")[0].rstrip(",")
        else:
            continue
        # Allow numpy, scipy, plus stdlib
        if mod not in {"numpy", "scipy", "pathlib", "re", "sys", "__future__"}:
            bad.append(ln)
    check(
        "imports limited to numpy + scipy + stdlib (family convention)",
        not bad,
        f"non-allowed = {bad}" if bad else "ok",
    )


# ---------------------------------------------------------------------------
# Part 6: Boundary check
# ---------------------------------------------------------------------------
def part6_boundary_check():
    section("Part 6: boundary check (what is NOT claimed)")
    not_claimed = [
        "claim the parent note's structural matrix-element identity",
        "close the full untruncated tensor-transfer construction",
        "close `analytic P(6)`",
        "change any parent or companion source row",
    ]
    for marker in not_claimed:
        check(
            f"note explicitly does not claim: {marker[:55]}",
            marker in NOTE_TEXT,
        )

    check(
        "claim_type: bounded_theorem stated",
        "Claim type:** bounded_theorem" in NOTE_TEXT,
    )
    check(
        "split-note finite-packet framing referenced",
        "split note for one finite tensor-word packet" in NOTE_TEXT,
    )
    check(
        "(BA-1) and (BA-2) admitted as bounded textbook inputs",
        "bounded inputs, not derived from the physical `Cl(3)`" in NOTE_TEXT,
    )


def main() -> int:
    banner("frontier_gauge_vacuum_plaquette_finite_tensor_word_packet.py")
    print(" Bounded source note: one explicit positive matrix tensor_word,")
    print(" constructed at NMAX = 4, MODE_MAX = 80, beta = 6 from canonical")
    print(" truncated Wilson coefficients and SU(3) fusion multiplicities.")
    print(" Verifies three load-bearing structural properties (P1)-(P3) at")
    print(" double precision, plus the (P3-corollary) consistency check that")
    print(" S·amp = amp follows from (P2) since S·boundary0 = boundary0.")
    print(" Follows prior audit feedback's split-note finite-packet path")
    print(" on parent gauge_vacuum_plaquette_spatial_environment_tensor_transfer_theorem_note.")

    part1_note_structure()
    part2_forbidden_vocabulary()
    part3_cited_upstreams()
    part4_construct_and_verify_packet()
    part5_import_boundary()
    part6_boundary_check()

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" RESULT: one explicit positive matrix tensor_word constructed from")
        print(" canonical truncated local Wilson coefficients (NMAX=4, MODE_MAX=80,")
        print(" beta=6) and SU(3) fusion multiplicities verifies three load-bearing")
        print(" structural properties at double precision: (P1) nonnegativity of")
        print(" matrix entries, (P2) conjugation-swap symmetry, (P3) nonnegative")
        print(" boundary amplitude under (0,0)-component unit-vector readout. The")
        print(" boundary-amplitude conjugation symmetry follows immediately from")
        print(" (P2) since (0,0) is fixed by the conjugation swap (consistency")
        print(" check, not a separate load-bearing property). The parent's broader")
        print(" matrix-element identity z_(p,q)^env = <chi, T^L eta> is NOT claimed")
        print(" here; this is a split-note bounded packet only.")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
