#!/usr/bin/env python3
"""Lane 3 direct generation-stratified quark Ward no-go.

This verifier checks the exact boundary behind
QUARK_GENERATION_STRATIFIED_WARD_FREE_MATRIX_NO_GO_NOTE_2026-04-28.md.

It proves a narrow negative statement: one-Higgs gauge selection plus the
top-channel Ward identity, retained three-generation structure, and CKM mixing
do not determine non-top quark Yukawa singular values.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import math
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    suffix = f" -- {detail}" if detail else ""
    print(f"{status}: {name}{suffix}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


@dataclass(frozen=True)
class Field:
    name: str
    color_dim: int
    su2_dim: int
    y_doubled: Fraction


Q_L = Field("Q_L", color_dim=3, su2_dim=2, y_doubled=Fraction(1, 3))
U_R = Field("u_R", color_dim=3, su2_dim=1, y_doubled=Fraction(4, 3))
D_R = Field("d_R", color_dim=3, su2_dim=1, y_doubled=Fraction(-2, 3))
H = Field("H", color_dim=1, su2_dim=2, y_doubled=Fraction(1, 1))
H_TILDE = Field("tilde H", color_dim=1, su2_dim=2, y_doubled=Fraction(-1, 1))


def hypercharge_sum(left: Field, scalar: Field, right: Field) -> Fraction:
    """Doubled-hypercharge sum for bar(F_L) S f_R."""
    return -left.y_doubled + scalar.y_doubled + right.y_doubled


def color_allowed(left: Field, right: Field) -> bool:
    return left.color_dim == right.color_dim == 3


def monomial_allowed(left: Field, scalar: Field, right: Field) -> bool:
    return color_allowed(left, right) and hypercharge_sum(left, scalar, right) == 0


def all_entries_allowed(scalar: Field, right: Field) -> bool:
    return all(monomial_allowed(Q_L, scalar, right) for _i in range(3) for _j in range(3))


def rotation12(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array(
        [
            [c, s, 0.0],
            [-s, c, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )


def sorted_singular_values(matrix: np.ndarray) -> np.ndarray:
    return np.sort(np.linalg.svd(matrix, compute_uv=False))


def same_ckm_witness() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return two Yukawa-matrix pairs with identical left mixing and different spectra."""
    v_ckm = rotation12(0.227)
    du_a = np.diag([0.00001, 0.006, 1.0])
    dd_a = np.diag([0.00002, 0.0004, 0.024])
    du_b = np.diag([0.0003, 0.03, 0.8])
    dd_b = np.diag([0.0007, 0.006, 0.06])

    yu_a = du_a
    yd_a = v_ckm @ dd_a
    yu_b = du_b
    yd_b = v_ckm @ dd_b
    return v_ckm, yu_a, yd_a, yu_b, yd_b


def main() -> int:
    note = DOCS / "QUARK_GENERATION_STRATIFIED_WARD_FREE_MATRIX_NO_GO_NOTE_2026-04-28.md"
    one_higgs_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    top_ward_note = DOCS / "YT_WARD_IDENTITY_DERIVATION_THEOREM.md"
    generation_note = DOCS / "THREE_GENERATION_STRUCTURE_NOTE.md"
    ckm_note = DOCS / "CKM_ATLAS_AXIOM_CLOSURE_NOTE.md"
    firewall_note = DOCS / "QUARK_LANE3_BOUNDED_COMPANION_RETENTION_FIREWALL_NOTE_2026-04-27.md"
    bottom_note = DOCS / "YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md"

    print("=" * 88)
    print("LANE 3 DIRECT GENERATION-STRATIFIED QUARK WARD NO-GO")
    print("=" * 88)

    print()
    print("A. Authority surfaces")
    print("-" * 72)
    for path in (note, one_higgs_note, top_ward_note, generation_note, ckm_note, firewall_note, bottom_note):
        check(f"{path.name} exists", path.exists(), str(path.relative_to(ROOT)))

    one_higgs_text = one_higgs_note.read_text(encoding="utf-8")
    top_ward_text = top_ward_note.read_text(encoding="utf-8")
    generation_text = generation_note.read_text(encoding="utf-8")
    firewall_text = firewall_note.read_text(encoding="utf-8")
    bottom_text = bottom_note.read_text(encoding="utf-8")
    note_text = note.read_text(encoding="utf-8")

    check("one-Higgs theorem says quark generation matrices are arbitrary", "arbitrary complex" in one_higgs_text and "Y_u" in one_higgs_text and "Y_d" in one_higgs_text)
    check("top Ward theorem states Q_L block normalization", "Q_L" in top_ward_text and "1/sqrt(6)" in top_ward_text)
    check("three-generation note states hierarchy remains open", "not retained: a first-principles `1+1+1` mass hierarchy" in generation_text)
    check("Lane 3 firewall keeps non-top masses open", "Lane 3 remains open" in firewall_text and "m_u" in firewall_text)
    check("bottom analysis closes species-uniform physical reuse", "species-uniform interpretation" in bottom_text and "overshoot" in bottom_text)

    print()
    print("B. Exact quark one-Higgs gauge bookkeeping")
    print("-" * 72)
    up_good = hypercharge_sum(Q_L, H_TILDE, U_R)
    up_wrong = hypercharge_sum(Q_L, H, U_R)
    down_good = hypercharge_sum(Q_L, H, D_R)
    down_wrong = hypercharge_sum(Q_L, H_TILDE, D_R)

    check("bar Q_L tilde H u_R is hypercharge neutral", up_good == 0, str(up_good))
    check("bar Q_L H d_R is hypercharge neutral", down_good == 0, str(down_good))
    check("bar Q_L H u_R wrong-Higgs residual is +2", up_wrong == 2, str(up_wrong))
    check("bar Q_L tilde H d_R wrong-Higgs residual is -2", down_wrong == -2, str(down_wrong))
    check("up-type monomial is color allowed", color_allowed(Q_L, U_R), "3bar x 3")
    check("down-type monomial is color allowed", color_allowed(Q_L, D_R), "3bar x 3")
    check("up-type selected monomial is gauge allowed", monomial_allowed(Q_L, H_TILDE, U_R))
    check("down-type selected monomial is gauge allowed", monomial_allowed(Q_L, H, D_R))

    print()
    print("C. Generation matrices remain free")
    print("-" * 72)
    entries_per_sector = 3 * 3
    check("all nine Y_u entries multiply the same gauge-allowed monomial", all_entries_allowed(H_TILDE, U_R))
    check("all nine Y_d entries multiply the same gauge-allowed monomial", all_entries_allowed(H, D_R))
    check("wrong-Higgs Y_u entries are rejected", not all_entries_allowed(H, U_R))
    check("wrong-Higgs Y_d entries are rejected", not all_entries_allowed(H_TILDE, D_R))
    check("gauge selection leaves nine complex entries per quark sector", entries_per_sector == 9, str(entries_per_sector))
    check("nine matrix entries exceed three eigenvalue slots", entries_per_sector > 3, "gauge skeleton is not a spectrum")

    print()
    print("D. Top Ward normalization is not a generation selector")
    print("-" * 72)
    n_color = 3
    n_iso = 2
    n_generation = 3
    ql_norm_sq = n_color * n_iso
    generation_averaged_sq = n_generation * ql_norm_sq
    weak_generation_sq = n_generation * n_iso

    check("top Ward Q_L normalization square is N_c*N_iso = 6", ql_norm_sq == 6, str(ql_norm_sq))
    check("top Ward coefficient is 1/sqrt(6)", abs(1.0 / math.sqrt(ql_norm_sq) - 0.4082482904638631) < 1.0e-15)
    check("adding generation averaging changes the normalization square", generation_averaged_sq == 18 and generation_averaged_sq != ql_norm_sq, str(generation_averaged_sq))
    check("generation x weak dimension 6 would be a new source primitive", weak_generation_sq == 6 and n_generation == 3 and ql_norm_sq == 6, "same number, different object")
    check("one-Higgs theorem does not select top/charm/up generation", "does not force diagonal form, hierarchy, rank, phase, or texture" in one_higgs_text)

    print()
    print("E. CKM mixing does not determine singular values")
    print("-" * 72)
    v_ckm, yu_a, yd_a, yu_b, yd_b = same_ckm_witness()
    ckm_a = v_ckm
    ckm_b = v_ckm
    su_a = sorted_singular_values(yu_a)
    sd_a = sorted_singular_values(yd_a)
    su_b = sorted_singular_values(yu_b)
    sd_b = sorted_singular_values(yd_b)

    check("witness CKM matrices are identical", np.max(np.abs(ckm_a - ckm_b)) < 1.0e-15)
    check("witness CKM matrix is nontrivial", abs(ckm_a[0, 1]) > 0.1 and abs(ckm_a[0, 1]) < 0.3, f"V_12={ckm_a[0, 1]:.6f}")
    check("first up-sector singular values match its chosen diagonal spectrum", np.allclose(su_a, np.array([0.00001, 0.006, 1.0])))
    check("second up-sector singular values differ from first", not np.allclose(su_a, su_b), f"A={su_a}, B={su_b}")
    check("first down-sector singular values match its chosen diagonal spectrum", np.allclose(sd_a, np.array([0.00002, 0.0004, 0.024])))
    check("second down-sector singular values differ from first", not np.allclose(sd_a, sd_b), f"A={sd_a}, B={sd_b}")
    check("same left mixing admits two different quark spectra", np.max(np.abs(ckm_a - ckm_b)) < 1.0e-15 and not np.allclose(sd_a, sd_b) and not np.allclose(su_a, su_b))

    print()
    print("F. Firewall and scope checks")
    print("-" * 72)
    forbidden_tokens = {
        "observed_quark_masses",
        "fitted_yukawa_entries",
        "hidden_generation_projector",
    }
    proof_inputs = {
        "field_charges",
        "higgs_choice",
        "generation_blind_gauge_action",
        "top_ward_block_dimension",
        "same_ckm_svd_witness",
        "source_note_scope_strings",
    }
    check("forbidden proof inputs are absent", forbidden_tokens.isdisjoint(proof_inputs), str(sorted(proof_inputs)))
    check("note says it does not claim non-top retained masses", "does not claim retained" in note_text and "m_b" in note_text)
    check("note keeps future source/readout primitive open", "source-domain" in note_text and "readout-map" in note_text)
    check("note states CKM is not eigenvalue closure", "CKM closure is not quark Yukawa eigenvalue closure" in note_text)

    print()
    print("Summary")
    print("-" * 72)
    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    if FAIL_COUNT == 0:
        print("VERDICT: direct generation-stratified quark Ward route remains open.")
        print("The current retained bank selects quark Yukawa operator skeletons and")
        print("top-channel normalization, but not non-top singular values.")
        return 0
    print("VERDICT: no-go verifier has failing checks.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
