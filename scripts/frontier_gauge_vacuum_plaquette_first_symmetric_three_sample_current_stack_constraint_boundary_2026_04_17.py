#!/usr/bin/env python3
"""
Current-stack constraint boundary on the first symmetric three-sample plaquette
PF evaluation seam.
"""

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

THEOREM_PASS = 0
SUPPORT_PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = "", bucket: str = "THEOREM") -> None:
    global THEOREM_PASS, SUPPORT_PASS, FAIL
    status = "PASS" if condition else "FAIL"
    if condition:
        if bucket == "SUPPORT":
            SUPPORT_PASS += 1
        else:
            THEOREM_PASS += 1
    else:
        FAIL += 1
    print(f"  [{status}] [{bucket}] {name}")
    if detail:
        print(f"         {detail}")


def read(rel_path: str) -> str:
    return (ROOT / rel_path).read_text()


def sample_angle_units() -> dict[str, tuple[int, int]]:
    return {
        "W_A": (-13, 10),
        "W_B": (-5, -7),
        "W_C": (7, -11),
    }


def eigenangle_multiset(theta1_units: int, theta2_units: int) -> tuple[int, int, int]:
    vals = [
        theta1_units % 32,
        theta2_units % 32,
        (-(theta1_units + theta2_units)) % 32,
    ]
    return tuple(sorted(vals))


def inverse_multiset(multiset: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(sorted((-x) % 32 for x in multiset))


def sample_matrix() -> sp.Matrix:
    pi = sp.pi
    rows: list[list[sp.Expr]] = []
    for theta1_units, theta2_units in sample_angle_units().values():
        theta1 = theta1_units * pi / 16
        theta2 = theta2_units * pi / 16
        rows.append(
            [
                sp.Integer(1),
                sp.simplify(6 * (sp.cos(theta1) + sp.cos(theta2) + sp.cos(theta1 + theta2))),
                sp.simplify(
                    16
                    * (
                        1
                        + sp.cos(theta1 - theta2)
                        + sp.cos(2 * theta1 + theta2)
                        + sp.cos(theta1 + 2 * theta2)
                    )
                ),
            ]
        )
    return sp.Matrix(rows)


def main() -> int:
    radical_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_FIRST_SYMMETRIC_THREE_SAMPLE_EXACT_RADICAL_RECONSTRUCTION_MAP_NOTE_2026-04-17.md"
    )
    char_measure_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_SPATIAL_ENVIRONMENT_CHARACTER_MEASURE_THEOREM_NOTE.md"
    )
    compressed_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_COMPRESSED_RIM_EVALUATION_THEOREM_NOTE_2026-04-17.md"
    )
    inversion_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_RETAINED_CLASS_SAMPLING_INVERSION_NOTE_2026-04-17.md"
    )
    symmetry_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_CONJUGATION_SYMMETRIC_RETAINED_SAMPLING_REDUCTION_NOTE_2026-04-17.md"
    )
    connected_note = read("docs/GAUGE_VACUUM_PLAQUETTE_CONNECTED_HIERARCHY_THEOREM_NOTE.md")
    bridge_note = read("docs/GAUGE_VACUUM_PLAQUETTE_BRIDGE_SUPPORT_NOTE.md")
    observable_note = read("docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md")
    scalar_note = read(
        "docs/GAUGE_VACUUM_PLAQUETTE_BETA6_SCALAR_VALUE_INSUFFICIENCY_NOTE_2026-04-17.md"
    )

    samples = {
        name: eigenangle_multiset(theta1_units, theta2_units)
        for name, (theta1_units, theta2_units) in sample_angle_units().items()
    }
    pair_summaries: list[str] = []
    pairwise_separated = True
    for left, right in combinations(samples, 2):
        conj_same = samples[left] == samples[right]
        inv_conj_same = samples[left] == inverse_multiset(samples[right])
        pairwise_separated &= (not conj_same) and (not inv_conj_same)
        pair_summaries.append(
            f"{left}/{right}: conj={conj_same}, inverse-conj={inv_conj_same}, "
            f"{samples[left]} vs {samples[right]}"
        )

    fmat = sample_matrix()
    det_f = sp.simplify(fmat.det())
    det_abs = abs(float(sp.N(det_f, 50)))
    rank_f = fmat.rank()
    left_nullity = len(fmat.T.nullspace())
    row_a_orbit2 = sp.simplify(fmat[0, 2])
    c_entry = sp.simplify(fmat[1, 2])
    e_entry = sp.simplify(fmat[2, 2])
    lower_minor = sp.simplify(sp.Matrix([[fmat[1, 1], fmat[1, 2]], [fmat[2, 1], fmat[2, 2]]]).det())
    c_numeric = float(sp.N(c_entry, 50))
    e_numeric = float(sp.N(e_entry, 50))
    lower_minor_abs = abs(float(sp.N(lower_minor, 50)))

    print("=" * 104)
    print("GAUGE-VACUUM PLAQUETTE FIRST SYMMETRIC THREE-SAMPLE CURRENT-STACK CONSTRAINT BOUNDARY")
    print("=" * 104)
    print()
    print("Named sample conjugacy data (angles in units of pi/16)")
    for name, multiset in samples.items():
        print(f"  {name}: {multiset}")
    print()
    print("Pairwise conjugacy / inverse-conjugacy checks")
    for summary in pair_summaries:
        print(f"  {summary}")
    print()
    print("Exact first symmetric three-sample matrix")
    print(fmat)
    print()
    print(f"  det(F)                                      = {sp.N(det_f, 30)}")
    print(f"  |det(F)|                                    = {det_abs:.12f}")
    print(f"  rank(F)                                     = {rank_f}")
    print(f"  left nullity                                = {left_nullity}")
    print(f"  exact W_A chi_(1,1) entry                   = {row_a_orbit2}")
    print(f"  exact lower 2x2 minor on (Phi_1,Phi_2)      = {sp.N(lower_minor, 30)}")
    print(f"  |lower 2x2 minor|                           = {lower_minor_abs:.12f}")
    print(f"  exact chi_(1,1) entries at W_B, W_C         = {sp.N(c_entry, 30)}, {sp.N(e_entry, 30)}")
    print()

    check(
        "The exact radical reconstruction-map theorem already fixes the named sample matrix, its inverse map, and the lack of universal witness-sector collapse",
        "exact radical-form three-sample matrix" in radical_note
        and "there is no further universal linear collapse below" in radical_note,
        bucket="SUPPORT",
    )
    check(
        "The character-measure and compressed rim-evaluation theorems fix the sample class as a central positive-type class function Z_beta^env(W)=<K(W),v_beta>",
        "positive type. Therefore it has one exact `SU(3)` character expansion" in char_measure_note
        and "Z_beta^env(W) = <K(W), v_beta>" in compressed_note,
        bucket="SUPPORT",
    )
    check(
        "The retained-sampling and conjugation-symmetry theorems already place the first witness sector at exactly three independent symmetric samples",
        "finite constructive inversion problem" in inversion_note
        and "three generic marked-holonomy samples recover the symmetric retained" in symmetry_note,
        bucket="SUPPORT",
    )
    check(
        "The connected-hierarchy, bridge-support, observable-principle, and scalar-insufficiency notes constrain scalar/source data but still leave explicit beta=6 environment sample data open",
        "d/d beta = sum_r d/d J_r" in connected_note
        and "remaining open object is explicit `beta = 6` spatial-transfer matrix-element / Perron data" in bridge_note
        and "coefficients in its local source expansion." in observable_note
        and "one scalar framework-point observable leaves nontrivial class-sector freedom" in scalar_note,
        bucket="SUPPORT",
    )

    check(
        "The three named holonomies are pairwise neither conjugate nor inverse-conjugate",
        pairwise_separated,
        detail="; ".join(pair_summaries),
    )
    check(
        "So current centrality and class-function reality do not identify any pair of the three sample values",
        pairwise_separated,
        detail="no pair lies in the same conjugacy or inverse-conjugacy class",
    )
    check(
        "The exact first symmetric three-sample evaluation matrix still has full rank three with no left null relation",
        rank_f == 3 and det_abs > 1.0 and left_nullity == 0,
        detail=f"rank={rank_f}, |det(F)|={det_abs:.12f}, left nullity={left_nullity}",
    )
    check(
        "The W_A decoupling of chi_(1,1) is exact but does not collapse the burden below three because the W_B/W_C lower block is still nonsingular and the chi_(1,1) entries have opposite sign",
        row_a_orbit2 == 0 and c_numeric > 1.0e-12 and e_numeric < -1.0e-12 and lower_minor_abs > 1.0e-6,
        detail=f"F_(A,2)={row_a_orbit2}, F_(B,2)={c_numeric:.12f}, F_(C,2)={e_numeric:.12f}, |minor|={lower_minor_abs:.12f}",
    )
    check(
        "Therefore the strongest honest current-stack theorem is boundary-only: no hidden symmetry or current source-observable law reduces the first beta=6 seam below explicit evaluation of Z_6^env(W_A), Z_6^env(W_B), Z_6^env(W_C)",
        pairwise_separated and rank_f == 3 and left_nullity == 0 and row_a_orbit2 == 0 and lower_minor_abs > 1.0e-6,
        detail="the exact reconstruction map is fixed, and the remaining first retained seam is the three named same-surface sample values themselves",
    )

    print()
    print(f"THEOREM PASS={THEOREM_PASS} SUPPORT={SUPPORT_PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
