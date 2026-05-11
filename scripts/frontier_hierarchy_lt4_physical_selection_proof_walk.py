#!/usr/bin/env python3
"""Hierarchy L_t = 4 physical-selection proof-walk (bounded conditional).

This runner verifies the algebraic content of the proof-walk
recorded in
``docs/HIERARCHY_LT4_PHYSICAL_SELECTION_PROOF_WALK_BOUNDED_NOTE_2026-05-10.md``
and reads the live audit ledger to confirm that each of the three
named admission walls (A-W-A staggered-Dirac realization gate, A-W-B
scalar-additivity P1, A-W-C CPT-even phase blindness) is tied to an
existing audit row at the stated effective status.

Forbidden imports check: the algebraic content (T1-T5) is recomputed
using stdlib ``cmath`` and ``math`` only. No PDG values, no ``M_Pl``,
no ``alpha_LM``, no ``u_0``, and no framework numerical constant is
consumed.

Target: PASS=7, FAIL=0.
"""

from __future__ import annotations

import cmath
import json
import math
import pathlib
import sys

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    status = "PASS" if condition else "FAIL"
    if condition:
        PASS_COUNT += 1
    else:
        FAIL_COUNT += 1
    print(f"  [{status}] {name}")
    if detail:
        print(f"         {detail}")


def apbc_phases(Lt: int) -> list[complex]:
    return [cmath.exp(1j * (2 * n + 1) * math.pi / Lt) for n in range(Lt)]


def canon(z: complex) -> tuple[float, float]:
    return (round(z.real, 12), round(z.imag, 12))


def klein_four_orbit(z: complex) -> list[tuple[float, float]]:
    ops = [
        lambda w: w,
        lambda w: -w,
        lambda w: w.conjugate(),
        lambda w: -w.conjugate(),
    ]
    return sorted({canon(op(z)) for op in ops})


def phase_set(Lt: int) -> list[tuple[float, float]]:
    return sorted({canon(z) for z in apbc_phases(Lt)})


def orbit_partition(Lt: int) -> list[list[tuple[float, float]]]:
    phases = phase_set(Lt)
    seen: set[tuple[float, float]] = set()
    parts: list[list[tuple[float, float]]] = []
    for z in phases:
        if z in seen:
            continue
        orb = sorted(w for w in klein_four_orbit(complex(*z)) if w in phases)
        parts.append(orb)
        seen.update(orb)
    return parts


def sin2_at_phase(z: complex) -> float:
    angle = math.atan2(z.imag, z.real)
    return math.sin(angle) ** 2


def part1_klein_four_orbit_unique_at_lt4() -> None:
    print("\n" + "=" * 78)
    print("PART 1: Klein-four orbit decomposition on APBC phases")
    print("=" * 78)

    parts4 = orbit_partition(4)
    print(f"  L_t = 4 partition = {parts4}")
    check(
        "T1: L_t = 4 has one Klein-four orbit of size 4 (unique resolved orbit)",
        len(parts4) == 1 and len(parts4[0]) == 4,
        f"len(parts)={len(parts4)}, size={[len(p) for p in parts4]}",
    )


def part2_lt2_unresolved_sign_pair() -> None:
    print("\n" + "=" * 78)
    print("PART 2: L_t = 2 carries only the unresolved sign pair {+i, -i}")
    print("=" * 78)

    parts2 = orbit_partition(2)
    print(f"  L_t = 2 partition = {parts2}")
    check(
        "T2: L_t = 2 has one Klein-four orbit of size 2 (the unresolved sign pair)",
        len(parts2) == 1 and len(parts2[0]) == 2,
        f"len(parts)={len(parts2)}, size={[len(p) for p in parts2]}",
    )


def part3_lt_gt_4_splits() -> None:
    print("\n" + "=" * 78)
    print("PART 3: L_t > 4 splits into multiple Klein-four orbit sectors")
    print("=" * 78)

    parts6 = orbit_partition(6)
    parts8 = orbit_partition(8)
    print(f"  L_t = 6 partition = {parts6}")
    print(f"  L_t = 8 partition = {parts8}")
    check(
        "T3: L_t ∈ {6, 8} both split into multiple Klein-four orbits",
        len(parts6) > 1 and len(parts8) > 1,
        f"L_t=6: {len(parts6)} orbits, sizes={[len(p) for p in parts6]}; "
        f"L_t=8: {len(parts8)} orbits, sizes={[len(p) for p in parts8]}",
    )


def part4_sin2_uniform_at_lt4() -> None:
    print("\n" + "=" * 78)
    print("PART 4: sin^2((2n+1)pi/4) = 1/2 uniformly at L_t = 4")
    print("=" * 78)

    vals4 = [sin2_at_phase(z) for z in apbc_phases(4)]
    print(f"  sin^2 values at L_t = 4 = {vals4}")
    check(
        "T4: sin^2 is uniform 1/2 at L_t = 4",
        all(abs(v - 0.5) < 1e-12 for v in vals4),
        f"max deviation from 1/2 = {max(abs(v - 0.5) for v in vals4):.2e}",
    )


def part5_sin2_nonuniform_at_lt6() -> None:
    print("\n" + "=" * 78)
    print("PART 5: sin^2 is non-uniform at L_t = 6")
    print("=" * 78)

    vals6 = [sin2_at_phase(z) for z in apbc_phases(6)]
    distinct6 = sorted({round(v, 10) for v in vals6})
    print(f"  sin^2 values at L_t = 6 = {vals6}")
    print(f"  distinct values         = {distinct6}")
    check(
        "T5: sin^2 takes more than one distinct value at L_t = 6",
        len(distinct6) >= 2,
        f"distinct count = {len(distinct6)}",
    )


def part6_admission_walls_ledger_check() -> None:
    print("\n" + "=" * 78)
    print("PART 6: Admission-wall catalogue (live ledger check)")
    print("=" * 78)

    ledger_path = pathlib.Path(__file__).resolve().parent.parent / "docs" / "audit" / "data" / "audit_ledger.json"
    with ledger_path.open() as f:
        ledger = json.load(f)
    rows = ledger.get("rows", {})

    walls = [
        (
            "A-W-A staggered-Dirac realization gate",
            "staggered_dirac_realization_gate_note_2026-05-03",
            "open_gate",
        ),
        (
            "A-W-B scalar-additivity P1 admission",
            "observable_principle_from_axiom_note",
            "audited_conditional",
        ),
        (
            "A-W-C CPT-even phase blindness (CPT primitive)",
            "cpt_exact_note",
            "unaudited",
        ),
    ]

    all_match = True
    for label, row_id, expected_status in walls:
        row = rows.get(row_id, {})
        actual_status = row.get("effective_status", "<missing>")
        ok = actual_status == expected_status
        all_match = all_match and ok
        marker = "[OK]" if ok else "[MISMATCH]"
        print(f"  {marker} {label}")
        print(f"      row_id={row_id}")
        print(f"      expected={expected_status} actual={actual_status}")

    check(
        "T6: all three admission walls match the live-ledger effective_status",
        all_match,
        "If any mismatch is reported, update the proof-walk note or the runner so the "
        "conditional shape matches the live ledger.",
    )


def part7_forbidden_imports_check() -> None:
    print("\n" + "=" * 78)
    print("PART 7: Forbidden-imports self-check")
    print("=" * 78)

    # The algebraic content above uses cmath / math / json / pathlib only.
    # No PDG values, M_Pl, alpha_LM, u_0 constants, or framework numerical
    # constants are imported. We check actual import lines and module-level
    # numerical-constant uses, not narrative-string presence (a substring
    # match would self-match the forbidden list above).
    src_lines = pathlib.Path(__file__).read_text().splitlines()
    forbidden_import_substrings = [
        "from canonical_plaquette_surface",
        "import canonical_plaquette_surface",
        "from M_Pl",
        "import M_Pl",
    ]
    import_lines = [
        line.strip()
        for line in src_lines
        if line.strip().startswith(("import ", "from "))
    ]
    leaks = [
        s
        for s in forbidden_import_substrings
        if any(s in line for line in import_lines)
    ]
    allowed_imports = {
        "from __future__ import annotations",
        "import cmath",
        "import json",
        "import math",
        "import pathlib",
        "import sys",
    }
    unexpected_imports = [line for line in import_lines if line not in allowed_imports]
    check(
        "T7: forbidden numerical imports are absent from this runner",
        not leaks and not unexpected_imports,
        f"forbidden_import_leaks={leaks}; "
        f"unexpected_imports={unexpected_imports}; "
        f"allowed_imports={sorted(allowed_imports)}",
    )


def main() -> None:
    print("Hierarchy L_t = 4 physical-selection proof-walk")
    print("=" * 78)
    print(
        "Bounded conditional proof-walk: the algebraic L_t = 4 Klein-four orbit\n"
        "result (retained upstream) is bridged to the physical EWSB temporal\n"
        "block via three named admission walls A-W-A / A-W-B / A-W-C. This\n"
        "runner verifies the algebraic content and reads the live audit ledger\n"
        "to confirm each admission wall is tied to an existing audit row at\n"
        "the stated effective status."
    )

    part1_klein_four_orbit_unique_at_lt4()
    part2_lt2_unresolved_sign_pair()
    part3_lt_gt_4_splits()
    part4_sin2_uniform_at_lt4()
    part5_sin2_nonuniform_at_lt6()
    part6_admission_walls_ledger_check()
    part7_forbidden_imports_check()

    print("\n" + "=" * 78)
    print(f"TOTAL: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    print("=" * 78)
    if FAIL_COUNT == 0:
        print(
            "VERDICT: bounded conditional proof-walk passes; the algebraic\n"
            "L_t = 4 Klein-four orbit content is verified from primitives, and\n"
            "the three admission walls A-W-A / A-W-B / A-W-C are tied to live\n"
            "audit-ledger rows. The conditional shape is the load-bearing\n"
            "content."
        )
    sys.exit(1 if FAIL_COUNT else 0)


if __name__ == "__main__":
    main()
