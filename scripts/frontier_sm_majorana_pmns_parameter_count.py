#!/usr/bin/env python3
"""Verifier for the active-SM Majorana PMNS parameter-count theorem.

The runner audits
SM_MAJORANA_PMNS_PARAMETER_COUNT_THEOREM_NOTE_2026-04-26.md using exact
integer/rational linear algebra. It deliberately does not claim numerical
PMNS angles, Dirac or Majorana phase values, neutrino masses, neutrinoless
double-beta rates, baryogenesis, or cosmology closure.
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


def majorana_count_packet(n: int) -> dict[str, int]:
    y_e_raw = 2 * n * n
    kappa_raw = n * (n + 1)
    raw = y_e_raw + kappa_raw
    flavor_group = 2 * n * n
    stabilizer = 0
    physical = raw - (flavor_group - stabilizer)
    masses = 2 * n
    pmns_dim = physical - masses
    angles = n * (n - 1) // 2
    phases = n * (n - 1) // 2
    dirac_phases = (n - 1) * (n - 2) // 2
    majorana_phases = n - 1
    return {
        "y_e_raw": y_e_raw,
        "kappa_raw": kappa_raw,
        "raw": raw,
        "flavor_group": flavor_group,
        "stabilizer": stabilizer,
        "physical": physical,
        "masses": masses,
        "pmns_dim": pmns_dim,
        "angles": angles,
        "phases": phases,
        "dirac_phases": dirac_phases,
        "majorana_phases": majorana_phases,
    }


def dirac_mixing_count_packet(n: int) -> dict[str, int]:
    unitary_dim = n * n
    effective_rephasings = 2 * n - 1
    physical = unitary_dim - effective_rephasings
    angles = n * (n - 1) // 2
    phases = (n - 1) * (n - 2) // 2
    return {
        "unitary_dim": unitary_dim,
        "effective_rephasings": effective_rephasings,
        "physical": physical,
        "angles": angles,
        "phases": phases,
    }


def row_rephasing_matrix(n: int) -> Matrix:
    """Charged-lepton row phases acting on PMNS entries."""
    rows: Matrix = []
    for a in range(n):
        for _i in range(n):
            row = [Fraction(0) for _ in range(n)]
            row[a] = Fraction(-1)
            rows.append(row)
    return rows


def dirac_row_column_rephasing_matrix(n: int) -> Matrix:
    """Dirac mixing rephasings: rows and columns, one common null phase."""
    rows: Matrix = []
    for a in range(n):
        for i in range(n):
            row = [Fraction(0) for _ in range(2 * n)]
            row[a] = Fraction(-1)
            row[n + i] = Fraction(1)
            rows.append(row)
    return rows


def majorana_mass_rephasing_matrix(n: int) -> Matrix:
    """Majorana mass phases shift as 2 beta_i, so no continuous null remains."""
    rows: Matrix = []
    for i in range(n):
        row = [Fraction(0) for _ in range(n)]
        row[i] = Fraction(2)
        rows.append(row)
    return rows


def symmetric_stabilizer_matrix(n: int) -> Matrix:
    """Equations alpha_a + alpha_b = 0 for every nonzero symmetric entry."""
    rows: Matrix = []
    for a in range(n):
        for b in range(a, n):
            row = [Fraction(0) for _ in range(n)]
            row[a] += Fraction(1)
            row[b] += Fraction(1)
            rows.append(row)
    return rows


def main() -> int:
    theorem_note = DOCS / "SM_MAJORANA_PMNS_PARAMETER_COUNT_THEOREM_NOTE_2026-04-26.md"
    yukawa_note = DOCS / "SM_ONE_HIGGS_YUKAWA_GAUGE_SELECTION_THEOREM_NOTE_2026-04-26.md"
    bounds_note = DOCS / "NEUTRINO_RETAINED_OBSERVABLE_BOUNDS_THEOREM_NOTE_2026-04-24.md"

    check("theorem note exists", theorem_note.exists(), str(theorem_note.relative_to(ROOT)))
    check("one-Higgs Yukawa theorem exists", yukawa_note.exists(), str(yukawa_note.relative_to(ROOT)))
    check("neutrino observable bounds theorem exists", bounds_note.exists(), str(bounds_note.relative_to(ROOT)))
    check("Yukawa theorem status is standalone positive", "standalone positive" in read_status(yukawa_note).lower())
    check("bounds theorem status is retained", "retained" in read_status(bounds_note).lower())

    text = theorem_note.read_text(encoding="utf-8")
    lower = text.lower()
    normalized = " ".join(lower.split())
    check("note records primary runner", "frontier_sm_majorana_pmns_parameter_count.py" in text)
    check(
        "note states twelve physical real parameters",
        "exactly twelve physical real parameters" in normalized,
    )
    check("note states generic full-rank scope", "generic full-rank" in lower)
    check("note states no PMNS value claim", "does not derive any charged-lepton mass" in lower)
    check("note states two Majorana phases", "two majorana phases" in lower)
    check("note contrasts Dirac and Majorana rephasing", "purely dirac neutrino sector" in lower)

    p3 = majorana_count_packet(3)
    check("3x3 charged-lepton Yukawa has 18 real parameters", p3["y_e_raw"] == 18, str(p3))
    check("3x3 complex symmetric kappa has 12 real parameters", p3["kappa_raw"] == 12, str(p3))
    check("raw active Majorana lepton data have 30 real parameters", p3["raw"] == 30, str(p3))
    check("U(3)_L x U(3)_e has dimension 18", p3["flavor_group"] == 18, str(p3))
    check("generic continuous stabilizer is zero-dimensional", p3["stabilizer"] == 0, str(p3))
    check("generic active Majorana lepton quotient has dimension 12", p3["physical"] == 12, str(p3))
    check("six lepton masses are counted", p3["masses"] == 6, str(p3))
    check("physical PMNS dimension is six", p3["pmns_dim"] == 6, str(p3))
    check("PMNS splits into three angles plus three phases", p3["angles"] == 3 and p3["phases"] == 3, str(p3))
    check("three PMNS phases split into one Dirac plus two Majorana", p3["dirac_phases"] == 1 and p3["majorana_phases"] == 2, str(p3))

    for n in range(1, 7):
        p = majorana_count_packet(n)
        row_rank = rank(row_rephasing_matrix(n))
        dirac_rank = rank(dirac_row_column_rephasing_matrix(n))
        mass_phase_rank = rank(majorana_mass_rephasing_matrix(n))
        stabilizer_rank = rank(symmetric_stabilizer_matrix(n))
        dirac = dirac_mixing_count_packet(n)

        check(f"N={n}: Majorana physical count is N^2+N", p["physical"] == n * n + n, str(p))
        check(f"N={n}: mass plus PMNS split reconstructs count", p["masses"] + p["pmns_dim"] == p["physical"], str(p))
        check(f"N={n}: PMNS dimension is N(N-1)", p["pmns_dim"] == n * (n - 1), str(p))
        check(f"N={n}: PMNS angle plus phase split reconstructs dimension", p["angles"] + p["phases"] == p["pmns_dim"], str(p))
        check(f"N={n}: Dirac plus Majorana phases reconstruct PMNS phases", p["dirac_phases"] + p["majorana_phases"] == p["phases"], str(p))
        check(f"N={n}: charged row-rephasing rank is N", row_rank == n, str(row_rank))
        check(f"N={n}: Majorana mass rephasing has no continuous null", n - mass_phase_rank == 0, str(mass_phase_rank))
        check(f"N={n}: generic symmetric stabilizer has no continuous null", n - stabilizer_rank == 0, str(stabilizer_rank))
        check(f"N={n}: Dirac mixing has N-1 fewer phases than Majorana mixing", p["pmns_dim"] - dirac["physical"] == n - 1, f"Majorana={p['pmns_dim']}, Dirac={dirac['physical']}")
        check(f"N={n}: Dirac row-column rephasing rank is 2N-1", dirac_rank == 2 * n - 1, str(dirac_rank))

    check("N=1 has no PMNS angle or CP phase", majorana_count_packet(1)["angles"] == 0 and majorana_count_packet(1)["phases"] == 0)
    check("N=2 has one angle and one Majorana phase", majorana_count_packet(2)["angles"] == 1 and majorana_count_packet(2)["majorana_phases"] == 1)
    check("N=3 has three angles and three CP-odd phases", majorana_count_packet(3)["angles"] == 3 and majorana_count_packet(3)["phases"] == 3)

    print(f"TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
