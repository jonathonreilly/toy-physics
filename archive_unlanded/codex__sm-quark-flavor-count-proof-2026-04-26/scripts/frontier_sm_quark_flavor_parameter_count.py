#!/usr/bin/env python3
"""Verifier for the generic SM quark flavor parameter-count theorem.

The runner audits
SM_QUARK_FLAVOR_PARAMETER_COUNT_THEOREM_NOTE_2026-04-26.md using exact integer
and rational linear algebra. It deliberately does not claim numerical quark
masses, CKM entries, CKM phase values, rare-decay rates, PMNS values, or any
cosmology/dark-sector closure.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS_COUNT = 0
FAIL_COUNT = 0

Matrix = list[list[Fraction]]


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    suffix = f" -- {detail}" if detail else ""
    if condition:
        PASS_COUNT += 1
        print(f"PASS: {name}{suffix}")
    else:
        FAIL_COUNT += 1
        print(f"FAIL: {name}{suffix}")


def read_status(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Status:**"):
            return line
    return ""


def rank(matrix: Matrix) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    n_rows = len(rows)
    n_cols = len(rows[0])
    pivot_row = 0
    for col in range(n_cols):
        pivot = None
        for row in range(pivot_row, n_rows):
            if rows[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][col]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]
        for row in range(n_rows):
            if row == pivot_row:
                continue
            factor = rows[row][col]
            if factor:
                rows[row] = [
                    rows[row][idx] - factor * rows[pivot_row][idx]
                    for idx in range(n_cols)
                ]
        pivot_row += 1
        if pivot_row == n_rows:
            break
    return pivot_row


def ckm_rephasing_matrix(n: int) -> Matrix:
    """Rows are CKM entry phases; columns are alpha_u and beta_d phases.

    V_ab -> exp(-i alpha_a) V_ab exp(i beta_b), so each row has -1 in the
    corresponding up phase and +1 in the corresponding down phase.
    """
    out: Matrix = []
    for a in range(n):
        for b in range(n):
            row = [Fraction(0) for _ in range(2 * n)]
            row[a] = Fraction(-1)
            row[n + b] = Fraction(1)
            out.append(row)
    return out


def count_packet(n: int) -> dict[str, int]:
    raw_yukawa = 4 * n * n
    flavor_group = 3 * n * n
    baryon_stabilizer = 1
    physical = raw_yukawa - (flavor_group - baryon_stabilizer)
    masses = 2 * n
    unitary_dim = n * n
    effective_rephasings = 2 * n - 1
    ckm_physical = unitary_dim - effective_rephasings
    angles = n * (n - 1) // 2
    cp_phases = (n - 1) * (n - 2) // 2
    return {
        "raw_yukawa": raw_yukawa,
        "flavor_group": flavor_group,
        "baryon_stabilizer": baryon_stabilizer,
        "physical": physical,
        "masses": masses,
        "unitary_dim": unitary_dim,
        "effective_rephasings": effective_rephasings,
        "ckm_physical": ckm_physical,
        "angles": angles,
        "cp_phases": cp_phases,
    }


def main() -> int:
    theorem_note = DOCS / "SM_QUARK_FLAVOR_PARAMETER_COUNT_THEOREM_NOTE_2026-04-26.md"
    yukawa_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    ckm_moduli_note = DOCS / "CKM_MODULI_ONLY_UNITARITY_JARLSKOG_AREA_CERTIFICATE_THEOREM_NOTE_2026-04-26.md"

    check("theorem note exists", theorem_note.exists(), str(theorem_note.relative_to(ROOT)))
    check("one-Higgs Yukawa theorem exists", yukawa_note.exists(), str(yukawa_note.relative_to(ROOT)))
    check("CKM moduli certificate exists", ckm_moduli_note.exists(), str(ckm_moduli_note.relative_to(ROOT)))

    check("Yukawa theorem status is standalone positive", "standalone positive" in read_status(yukawa_note).lower())
    check("CKM moduli theorem status is standalone positive", "standalone positive" in read_status(ckm_moduli_note).lower())

    note_text = theorem_note.read_text(encoding="utf-8")
    note_lower = note_text.lower()
    check("note records primary runner", "frontier_sm_quark_flavor_parameter_count.py" in note_text)
    check("note states generic scope", "generic full-rank" in note_lower)
    check("note records ten physical parameters", "exactly ten physical real parameters" in note_lower)
    check("note avoids numerical CKM claim", "does not derive any numerical mass" in note_lower)
    check("note scopes out degeneracy strata", "exactly degenerate" in note_lower and "loses rank" in note_lower)
    check("note explains generic stabilizer", "generic stabilizer is only this one phase" in note_lower)

    packet = count_packet(3)
    check("two complex 3x3 Yukawas have 36 real parameters", packet["raw_yukawa"] == 36, str(packet))
    check("U(3)^3 flavor group has dimension 27", packet["flavor_group"] == 27, str(packet))
    check("generic stabilizer is one baryon-number dimension", packet["baryon_stabilizer"] == 1, str(packet))
    check("generic quotient dimension is ten", packet["physical"] == 10, str(packet))
    check("six quark masses are counted", packet["masses"] == 6, str(packet))
    check("physical CKM dimension is four", packet["ckm_physical"] == 4, str(packet))
    check("CKM splits into three angles plus one phase", packet["angles"] == 3 and packet["cp_phases"] == 1, str(packet))
    check("six masses plus four CKM parameters equals ten", packet["masses"] + packet["ckm_physical"] == packet["physical"])
    check(
        "six masses plus three angles plus one phase equals ten",
        packet["masses"] + packet["angles"] + packet["cp_phases"] == packet["physical"],
    )

    for n in range(1, 7):
        p = count_packet(n)
        expected_physical = n * n + 1
        expected_ckm = (n - 1) * (n - 1)
        expected_rephasing_rank = 2 * n - 1
        phase_rank = rank(ckm_rephasing_matrix(n))
        check(f"N={n}: quotient count is N^2+1", p["physical"] == expected_physical, str(p))
        check(f"N={n}: CKM physical count is (N-1)^2", p["ckm_physical"] == expected_ckm, str(p))
        check(f"N={n}: rephasing incidence rank is 2N-1", phase_rank == expected_rephasing_rank, str(phase_rank))
        check(
            f"N={n}: angle+phase split reconstructs CKM count",
            p["angles"] + p["cp_phases"] == p["ckm_physical"],
            str(p),
        )
        check(
            f"N={n}: mass+angle+phase split reconstructs full count",
            p["masses"] + p["angles"] + p["cp_phases"] == p["physical"],
            str(p),
        )

    check("N=1 has no mixing angle and no CP phase", count_packet(1)["angles"] == 0 and count_packet(1)["cp_phases"] == 0)
    check("N=2 has one angle and no CP phase", count_packet(2)["angles"] == 1 and count_packet(2)["cp_phases"] == 0)
    check("N=3 has one CP-odd CKM phase", count_packet(3)["cp_phases"] == 1)

    # The all-ones phase vector is the null direction of CKM rephasing:
    # alpha_a = beta_b for all a,b leaves every V_ab unchanged.
    m3 = ckm_rephasing_matrix(3)
    common_phase = [Fraction(1) for _ in range(6)]
    image = [sum(row[col] * common_phase[col] for col in range(6)) for row in m3]
    check("common baryon phase is inert on CKM entries", all(value == 0 for value in image), str(image))
    check("one CKM rephasing null direction remains", 6 - rank(m3) == 1, str(6 - rank(m3)))

    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
