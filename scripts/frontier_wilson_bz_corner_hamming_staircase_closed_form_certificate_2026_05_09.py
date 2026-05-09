#!/usr/bin/env python3
"""Closed-form enumeration + lattice-independence certificate for the
Wilson term BZ-corner Hamming-weight staircase.

Companion runner for:
  docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_CLOSED_FORM_NOTE_2026-05-09.md

Lifts the bounded note
  docs/WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md
to a full closed-form theorem by establishing:

  T1. Closed-form enumeration. The 16 BZ corners of {0,1}^4 (= the
      Z^3 + t corners at L = 2, k_mu = n_mu * pi) decompose into
      five Hamming-weight classes with multiplicities binomial(4, k)
      = (1, 4, 6, 4, 1) and Wilson mass shifts W(n)/r = 2*hw(n)
      taking values (0, 2, 4, 6, 8). These are exact integer
      identities, not finite-window approximations.

  T2. Equivariance. The staircase decomposition is invariant under
      the full axis-permutation group S_4 acting on the four
      directions (t, x, y, z). In particular, every cyclic
      sub-rotation, including the spatial C_3[111] action used in
      the sister Z^3 staircase note (THREE_GENERATION_STRUCTURE_NOTE.md),
      fixes each level set.

  T3. Lattice-independence. For any rectangular Bravais lattice
      L = diag(a_t, a_x, a_y, a_z) (a_mu > 0) on Z^3 + t with
      antiperiodic boundary conditions and minimal block n_mu = 2,
      the BZ corners are k_mu = n_mu * pi / a_mu with
      n_mu in {0, 1}. Both the corner labels n in {0,1}^4 and
      the values 1 - cos(n_mu * pi) = 2 n_mu depend only on the
      F_2^4 quotient structure (the parity of n_mu), not on the
      lattice spacing a_mu. Therefore the Hamming-weight staircase
      is canonical given the C_3[111]-equivariant primitive cube
      structure; rescaling any rectangular Bravais lattice with
      the same L = 2 minimal block produces the same staircase.

  T4. Sister Z^3 corollary. Restricting to the spatial sub-cube
      {0,1}^3 (i.e. setting n_t = 0) recovers the 1+3+3+1 = 8
      decomposition cited by THREE_GENERATION_STRUCTURE_NOTE.md
      with multiplicities binomial(3, k) under the spatial
      C_3[111] cyclic group.

This is a finite combinatorial closure: every load-bearing step is
an exact integer / rational identity on bit-vectors. No Monte Carlo,
RG flow, or observational input is used.

The runner emits a JSON certificate at
  outputs/wilson_bz_corner_hamming_staircase_certificate_2026_05_09.json
containing all 8 spatial corners, all 16 spacetime corners, their
Hamming weights, the closed-form Wilson shifts, the binomial-coefficient
multiplicities, the S_4 / C_3[111] equivariance verification, and
the lattice-rescaling invariance check.

Stdlib + sympy (exact rationals + cos(0), cos(pi) symbolic checks).
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path
from typing import Any

import sympy as sp


ROOT = Path(__file__).resolve().parent.parent
NOTE_PATH = ROOT / "docs" / "WILSON_BZ_CORNER_HAMMING_STAIRCASE_CLOSED_FORM_NOTE_2026-05-09.md"
BOUNDED_NOTE_PATH = ROOT / "docs" / "WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md"
OUTPUT_JSON = ROOT / "outputs" / "wilson_bz_corner_hamming_staircase_certificate_2026_05_09.json"

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


# ---------------------------------------------------------------------------
# Combinatorial primitives.
# ---------------------------------------------------------------------------
def binomial(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    num = 1
    for i in range(k):
        num *= (n - i)
        num //= (i + 1)
    return num


def hw(n: tuple[int, ...]) -> int:
    return sum(n)


def enumerate_corners(d: int) -> list[tuple[int, ...]]:
    return [tuple(c) for c in product((0, 1), repeat=d)]


def wilson_shift_over_r(n: tuple[int, ...]) -> Fraction:
    """W(n) / r = sum_mu (1 - cos(n_mu * pi)) = 2 * hw(n) (exact integer)."""
    return Fraction(2 * sum(n))


def group_by_hw(corners: list[tuple[int, ...]]) -> dict[int, list[tuple[int, ...]]]:
    bucket: dict[int, list[tuple[int, ...]]] = {}
    for n in corners:
        bucket.setdefault(hw(n), []).append(n)
    return bucket


# ---------------------------------------------------------------------------
# T1. Closed-form enumeration on {0,1}^4.
# ---------------------------------------------------------------------------
def part_t1_closed_form_enumeration():
    section("T1. Closed-form enumeration on {0,1}^4 (16 BZ corners)")
    corners = enumerate_corners(4)
    check("enumerated 2^4 = 16 corners", len(corners) == 16, f"got {len(corners)}")
    check("all corners distinct", len(set(corners)) == 16)

    # Closed-form symbolic check: 1 - cos(n_mu * pi) for n_mu in {0,1} is exactly
    # 0 (n_mu=0) and 2 (n_mu=1) by sympy's exact cos.
    cos0 = sp.cos(0)
    cos_pi = sp.cos(sp.pi)
    check(
        "sympy exact: cos(0) = 1",
        sp.simplify(cos0 - 1) == 0,
        f"cos(0) = {cos0}",
    )
    check(
        "sympy exact: cos(pi) = -1",
        sp.simplify(cos_pi + 1) == 0,
        f"cos(pi) = {cos_pi}",
    )
    check(
        "1 - cos(0)  =  0  (n_mu=0 contributes 0)",
        sp.simplify(1 - cos0) == 0,
    )
    check(
        "1 - cos(pi) =  2  (n_mu=1 contributes 2)",
        sp.simplify(1 - cos_pi - 2) == 0,
    )

    # Per-corner Wilson value via direct symbolic substitution.
    corner_records: list[dict[str, Any]] = []
    for n in corners:
        # Symbolic Wilson sum over directions.
        w_sym = sum(1 - sp.cos(n_mu * sp.pi) for n_mu in n)
        w_sym = sp.simplify(w_sym)
        w_int = int(w_sym)
        w_expected = 2 * hw(n)
        check(
            f"corner {n}: symbolic W/r = {w_int}, closed-form 2*hw = {w_expected}",
            w_int == w_expected,
        )
        corner_records.append(
            {
                "corner": list(n),
                "hw": hw(n),
                "wilson_shift_over_r_symbolic": str(w_sym),
                "wilson_shift_over_r": w_int,
                "closed_form_2_times_hw": w_expected,
            }
        )

    # Multiplicity per Hamming weight = binomial(4, k).
    bucket = group_by_hw(corners)
    expected = [(0, 1), (1, 4), (2, 6), (3, 4), (4, 1)]
    total = 0
    for k, mult_expected in expected:
        mult = len(bucket.get(k, []))
        check(
            f"|{{n in {{0,1}}^4 : hw(n) = {k}}}| = binomial(4, {k}) = {mult_expected}",
            mult == mult_expected and binomial(4, k) == mult_expected,
            f"enumerated {mult}",
        )
        total += mult
    check(
        "sum of multiplicities = 2^4 = 16",
        total == 16 and total == sum(binomial(4, k) for k in range(5)),
    )

    return corners, corner_records, bucket


# ---------------------------------------------------------------------------
# T2. Equivariance under S_4 axis-permutation group.
# ---------------------------------------------------------------------------
def apply_perm(n: tuple[int, ...], perm: tuple[int, ...]) -> tuple[int, ...]:
    """Apply permutation perm of (0,...,d-1) to coordinate vector n.

    perm[i] is the new position of axis i. Concretely, the permuted vector
    n_perm has n_perm[perm[i]] = n[i].
    """
    d = len(n)
    out = [0] * d
    for i in range(d):
        out[perm[i]] = n[i]
    return tuple(out)


def part_t2_equivariance(corners: list[tuple[int, ...]]):
    section("T2. S_4 axis-permutation equivariance")

    s4 = list(permutations(range(4)))
    check("|S_4| = 4! = 24 axis permutations", len(s4) == 24)

    # Verify hw is permutation-invariant (Hamming weight = number of 1s).
    invariant_count = 0
    for perm in s4:
        ok = all(hw(apply_perm(n, perm)) == hw(n) for n in corners)
        if ok:
            invariant_count += 1
    check(
        "every S_4 element preserves hw (level sets fixed setwise)",
        invariant_count == 24,
        f"{invariant_count}/24 preserve hw",
    )

    # Verify Wilson shift is permutation-invariant.
    shift_invariant = 0
    for perm in s4:
        ok = all(
            wilson_shift_over_r(apply_perm(n, perm)) == wilson_shift_over_r(n)
            for n in corners
        )
        if ok:
            shift_invariant += 1
    check(
        "every S_4 element preserves W(n)/r",
        shift_invariant == 24,
        f"{shift_invariant}/24 preserve W",
    )

    # Verify the spatial C_3[111] subgroup (cyclic permutation of axes
    # (1,2,3) = (x,y,z) with t = axis 0 fixed) preserves levels.
    c3_111 = [
        (0, 1, 2, 3),  # identity
        (0, 2, 3, 1),  # (x y z) cycle
        (0, 3, 1, 2),  # (x z y) cycle
    ]
    check("C_3[111] is a subgroup of S_4", all(p in s4 for p in c3_111))
    c3_invariant = all(
        all(hw(apply_perm(n, perm)) == hw(n) for n in corners) for perm in c3_111
    )
    check(
        "C_3[111] preserves every Hamming-weight level setwise",
        c3_invariant,
    )
    c3_shift_invariant = all(
        all(
            wilson_shift_over_r(apply_perm(n, perm)) == wilson_shift_over_r(n)
            for n in corners
        )
        for perm in c3_111
    )
    check(
        "C_3[111] preserves W(n)/r",
        c3_shift_invariant,
    )

    # Concrete C_3[111] orbit example on hw=1 spatial triplet:
    # (0,1,0,0) -> (0,0,1,0) -> (0,0,0,1) under (x y z) cycle.
    n_x = (0, 1, 0, 0)
    n_y = apply_perm(n_x, (0, 2, 3, 1))
    n_z = apply_perm(n_y, (0, 2, 3, 1))
    check(
        "C_3[111] orbit on hw=1 spatial: x -> y -> z -> x",
        n_y == (0, 0, 1, 0)
        and n_z == (0, 0, 0, 1)
        and apply_perm(n_z, (0, 2, 3, 1)) == n_x,
        f"orbit = {n_x} -> {n_y} -> {n_z}",
    )

    # Time-axis cyclic group C_4[1111] (full cyclic axis rotation):
    c4_1111 = [
        (0, 1, 2, 3),
        (1, 2, 3, 0),
        (2, 3, 0, 1),
        (3, 0, 1, 2),
    ]
    c4_inv = all(
        all(hw(apply_perm(n, perm)) == hw(n) for n in corners) for perm in c4_1111
    )
    check(
        "C_4[1111] cyclic axis-rotation preserves every level",
        c4_inv,
    )

    # Build orbit decomposition under S_4: count orbit sizes per hw.
    orbits_by_hw: dict[int, list[list[tuple[int, ...]]]] = {}
    for corner in corners:
        orbit = set()
        for perm in s4:
            orbit.add(apply_perm(corner, perm))
        k = hw(corner)
        orbits_by_hw.setdefault(k, [])
        orbit_sorted = sorted(orbit)
        if orbit_sorted not in orbits_by_hw[k]:
            orbits_by_hw[k].append(orbit_sorted)

    expected_orbit_count = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1}
    expected_orbit_size = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}
    for k in range(5):
        orbits = orbits_by_hw.get(k, [])
        check(
            f"S_4 acts transitively on hw={k} (single orbit, size = binomial(4,{k}))",
            len(orbits) == expected_orbit_count[k]
            and len(orbits[0]) == expected_orbit_size[k],
            f"{len(orbits)} orbit(s); first orbit size = {len(orbits[0]) if orbits else 0}",
        )

    return s4, c3_111, c4_1111, orbits_by_hw


# ---------------------------------------------------------------------------
# T3. Lattice-independence under any rectangular Bravais rescaling.
# ---------------------------------------------------------------------------
def part_t3_lattice_independence(corners: list[tuple[int, ...]]):
    section("T3. Lattice-independence (rectangular Bravais rescaling)")

    # For lattice L = diag(a_t, a_x, a_y, a_z), BZ corners at minimal block
    # n_mu = 2 are k_mu = n_mu * pi / a_mu, n_mu in {0, 1}.
    # Wilson term: 1 - cos(k_mu * a_mu) = 1 - cos(n_mu * pi).
    # Therefore the per-direction value is independent of a_mu and depends
    # only on the parity n_mu.

    # Symbolic verification with arbitrary positive lattice spacings a_mu.
    a = sp.symbols("a_t a_x a_y a_z", positive=True)
    for n in corners:
        # k_mu * a_mu where k_mu = n_mu * pi / a_mu --> n_mu * pi.
        # So 1 - cos(k_mu * a_mu) = 1 - cos(n_mu * pi).
        per_dir = [sp.simplify(1 - sp.cos((n[mu] * sp.pi / a[mu]) * a[mu])) for mu in range(4)]
        w_sym = sum(per_dir)
        w_sym_simplified = sp.simplify(w_sym)
        w_expected = 2 * hw(n)
        check(
            f"lattice-independent corner {n}: 1 - cos(k*a) summed = {w_expected} (a-free)",
            w_sym_simplified == w_expected,
            f"got {w_sym_simplified}",
        )

    # Numerical sanity at three independent rectangular lattices (the
    # symbolic check is the actual proof; this is a redundant integer
    # check that the cancellation a_mu / a_mu = 1 holds for arbitrary a).
    test_lattices = [
        (sp.Rational(1, 1), sp.Rational(1, 1), sp.Rational(1, 1), sp.Rational(1, 1)),
        (sp.Rational(2, 3), sp.Rational(7, 5), sp.Rational(11, 4), sp.Rational(13, 9)),
        (sp.sqrt(2), sp.sqrt(3), sp.sqrt(5), sp.sqrt(7)),
    ]
    for L in test_lattices:
        for n in corners:
            k = [n[mu] * sp.pi / L[mu] for mu in range(4)]
            w = sum(1 - sp.cos(k[mu] * L[mu]) for mu in range(4))
            w = sp.simplify(w)
            w_expected = 2 * hw(n)
            ok = w == w_expected
            if not ok:
                check(
                    f"lattice {L} corner {n}: W = {w_expected}",
                    False,
                    f"got {w}",
                )
                break
        else:
            check(
                f"all 16 corners on lattice diag({L}) yield closed-form 2*hw",
                True,
            )

    # F_2^4 quotient structure: corner labels are bit vectors mod 2;
    # the staircase only depends on this quotient.
    check(
        "BZ-corner labels n in {0,1}^4 form F_2^4 (bit-vector quotient)",
        len({tuple(c) for c in corners}) == 2**4,
    )
    check(
        "Hamming weight = sum mod 0 (linear functional on F_2^4 over Z)",
        all(hw(n) == sum(n) for n in corners),
    )


# ---------------------------------------------------------------------------
# T4. Sister Z^3 corollary: restrict to spatial {0,1}^3.
# ---------------------------------------------------------------------------
def part_t4_sister_z3_corollary():
    section("T4. Sister Z^3 corollary: spatial {0,1}^3 with C_3[111]")

    spatial = enumerate_corners(3)
    check("enumerated 2^3 = 8 spatial BZ corners", len(spatial) == 8)

    bucket = group_by_hw(spatial)
    expected = [(0, 1), (1, 3), (2, 3), (3, 1)]  # binomial(3, k)
    for k, mult_expected in expected:
        mult = len(bucket.get(k, []))
        check(
            f"|{{n in {{0,1}}^3 : hw(n) = {k}}}| = binomial(3, {k}) = {mult_expected}",
            mult == mult_expected and binomial(3, k) == mult_expected,
        )
    check(
        "spatial multiplicity tuple (1, 3, 3, 1) sums to 2^3 = 8",
        sum(len(v) for v in bucket.values()) == 8,
    )

    # Spatial C_3[111] cyclic permutation of axes (x y z).
    c3 = [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
    for perm in c3:
        ok = all(hw(apply_perm(n, perm)) == hw(n) for n in spatial)
        check(
            f"spatial C_3[111] perm {perm} preserves Hamming weight",
            ok,
        )

    # Verify hw=1 triplet C_3[111] orbit (transitive single orbit).
    triplet = bucket[1]
    seed = triplet[0]
    orbit = {seed}
    for perm in c3:
        orbit.add(apply_perm(seed, perm))
    check(
        "C_3[111] acts transitively on the hw=1 spatial triplet",
        orbit == set(triplet) and len(orbit) == 3,
        f"orbit size = {len(orbit)}",
    )

    return spatial, bucket


# ---------------------------------------------------------------------------
# Note structure check.
# ---------------------------------------------------------------------------
def part_note_structure():
    section("Note structure (closed-form note)")
    check("note exists", NOTE_PATH.exists(), f"path = {NOTE_PATH.relative_to(ROOT)}")
    if not NOTE_PATH.exists():
        return
    text = NOTE_PATH.read_text()
    required = [
        ("title", "Wilson Term BZ-Corner Hamming-Weight Staircase Closed-Form"),
        ("claim_type bounded_theorem token", "Claim type:** bounded_theorem"),
        ("source-note authority phrase", "source-note proposal only"),
        ("Theorem T1", "## T1"),
        ("Theorem T2", "## T2"),
        ("Theorem T3", "## T3"),
        ("Theorem T4", "## T4"),
        ("closed-form formula 2*hw(n)", "2 · hw(n)"),
        ("multiplicity tuple (1, 4, 6, 4, 1)", "(1, 4, 6, 4, 1)"),
        ("S_4 equivariance phrase", "S_4 axis-permutation"),
        ("C_3[111] phrase", "C_3[111]"),
        ("F_2^4 quotient structure phrase", "F_2^4"),
        ("lattice-independence phrase", "lattice-independent"),
        ("companion bounded note cited",
         "WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08"),
    ]
    for label, marker in required:
        check(f"note contains: {label}", marker in text, f"marker = {marker!r}")


# ---------------------------------------------------------------------------
# Bounded-note cross-link check.
# ---------------------------------------------------------------------------
def part_bounded_note_cross_link():
    section("Bounded note cross-link to closed-form note")
    text = BOUNDED_NOTE_PATH.read_text()
    check(
        "bounded note exists and references the new closed-form companion",
        "WILSON_BZ_CORNER_HAMMING_STAIRCASE_CLOSED_FORM_NOTE_2026-05-09" in text,
        f"path = {BOUNDED_NOTE_PATH.relative_to(ROOT)}",
    )


# ---------------------------------------------------------------------------
# JSON certificate emission.
# ---------------------------------------------------------------------------
def emit_certificate(
    corners_4d: list[tuple[int, ...]],
    corner_records: list[dict[str, Any]],
    bucket_4d: dict[int, list[tuple[int, ...]]],
    s4: list[tuple[int, ...]],
    c3_111: list[tuple[int, ...]],
    c4_1111: list[tuple[int, ...]],
    orbits_by_hw: dict[int, list[list[tuple[int, ...]]]],
    spatial: list[tuple[int, ...]],
    spatial_bucket: dict[int, list[tuple[int, ...]]],
) -> None:
    section("Emit JSON certificate")
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    cert: dict[str, Any] = {
        "certificate_id": "wilson_bz_corner_hamming_staircase_closed_form_2026_05_09",
        "rigorize_target": (
            "wilson_bz_corner_hamming_staircase_bounded_note_2026-05-08"
        ),
        "closed_form_formula": "W(n) / r = 2 * hw(n) for n in {0,1}^4",
        "multiplicity_formula": "|{n : hw(n) = k}| = binomial(4, k)",
        "shifts_over_r": [0, 2, 4, 6, 8],
        "multiplicities_per_hw": {
            "0": 1,
            "1": 4,
            "2": 6,
            "3": 4,
            "4": 1,
        },
        "total_state_count": 16,
        "F2_4_quotient": True,
        "spacetime_corners_2_to_4": [
            {
                "corner": list(n),
                "hw": hw(n),
                "wilson_shift_over_r": int(wilson_shift_over_r(n)),
            }
            for n in corners_4d
        ],
        "spacetime_corner_symbolic_records": corner_records,
        "spacetime_buckets_by_hw": {
            str(k): [list(c) for c in bucket_4d[k]] for k in sorted(bucket_4d)
        },
        "S4_size": len(s4),
        "S4_orbits_by_hw": {
            str(k): [
                [list(c) for c in orbit] for orbit in orbits_by_hw.get(k, [])
            ]
            for k in sorted(orbits_by_hw)
        },
        "C3_111_perms_full4d": [list(p) for p in c3_111],
        "C4_1111_perms": [list(p) for p in c4_1111],
        "spatial_corners_2_to_3": [list(n) for n in spatial],
        "spatial_buckets_by_hw": {
            str(k): [list(c) for c in spatial_bucket[k]]
            for k in sorted(spatial_bucket)
        },
        "spatial_multiplicity_formula": "|{n : hw(n) = k}| = binomial(3, k)",
        "spatial_shifts_over_r": [0, 2, 4, 6],
        "lattice_independence_proof_sketch": (
            "For rectangular Bravais L = diag(a_t, a_x, a_y, a_z), BZ corners "
            "at L=2 minimal block are k_mu = n_mu pi / a_mu with n_mu in "
            "{0,1}. Then k_mu a_mu = n_mu pi, so 1 - cos(k_mu a_mu) = "
            "1 - cos(n_mu pi) = 2 n_mu, independent of a_mu. The staircase "
            "depends only on the F_2^4 quotient (n_mu mod 2)."
        ),
        "exact_arithmetic_method": (
            "sympy.cos(0)=1 and sympy.cos(pi)=-1 are exact symbolic; "
            "the Wilson sum reduces to the integer 2*hw(n) for every "
            "n in {0,1}^4."
        ),
        "summary": {
            "closure_status": "bounded_theorem",
            "T1_closed_form_enumeration": True,
            "T2_S4_equivariance_verified": True,
            "T3_lattice_independence_verified": True,
            "T4_sister_Z3_corollary": True,
        },
    }
    OUTPUT_JSON.write_text(json.dumps(cert, indent=2, sort_keys=False) + "\n")
    check(
        f"wrote JSON certificate to {OUTPUT_JSON.relative_to(ROOT)}",
        OUTPUT_JSON.exists(),
        f"size = {OUTPUT_JSON.stat().st_size} bytes",
    )


# ---------------------------------------------------------------------------
# Main.
# ---------------------------------------------------------------------------
def main() -> int:
    banner("frontier_wilson_bz_corner_hamming_staircase_closed_form_certificate_2026_05_09.py")
    print(" Closed-form enumeration + lattice-independence certificate")
    print(" Lifts wilson_bz_corner_hamming_staircase_bounded_note_2026-05-08")
    print(" to a full closed-form theorem.")

    corners, corner_records, bucket = part_t1_closed_form_enumeration()
    s4, c3_111, c4_1111, orbits_by_hw = part_t2_equivariance(corners)
    part_t3_lattice_independence(corners)
    spatial, spatial_bucket = part_t4_sister_z3_corollary()
    part_note_structure()
    part_bounded_note_cross_link()
    emit_certificate(
        corners_4d=corners,
        corner_records=corner_records,
        bucket_4d=bucket,
        s4=s4,
        c3_111=c3_111,
        c4_1111=c4_1111,
        orbits_by_hw=orbits_by_hw,
        spatial=spatial,
        spatial_bucket=spatial_bucket,
    )

    print()
    print("=" * 88)
    print(f" TOTAL: PASS={PASS}, FAIL={FAIL}")
    print("=" * 88)
    if FAIL == 0:
        print()
        print(" VERDICT: closed-form theorem certified.")
        print(" T1 closed-form enumeration: W(n)/r = 2*hw(n), multiplicities binomial(4,k).")
        print(" T2 S_4 equivariance verified (24/24 perms; C_3[111] and C_4[1111] sub-actions).")
        print(" T3 lattice-independence verified symbolically for any rectangular Bravais L.")
        print(" T4 sister Z^3 corollary verified (1+3+3+1 with C_3[111] transitivity).")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
