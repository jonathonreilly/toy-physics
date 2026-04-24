#!/usr/bin/env python3
"""Verifier for the bare gravity-sector uniqueness attempt.

The verifier is intentionally conservative. It passes only if the note records
the conditional uniqueness reduction and refuses to mark B3 closed.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(rel: str) -> str:
    return (ROOT / rel).read_text()


def expect(name: str, cond: bool, detail: str) -> int:
    if cond:
        print(f"PASS: {name} - {detail}")
        return 1
    print(f"FAIL: {name} - {detail}")
    return 0


def main() -> int:
    note = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_UNIQUENESS_ATTEMPT_2026-04-24.md")
    status = read("docs/PLANCK_SCALE_BARE_GRAVITY_SECTOR_DERIVATION_STATUS_THEOREM_2026-04-23.md")
    program = read("docs/PLANCK_SCALE_BARE_CELL_ALONE_CLOSURE_PROGRAM_2026-04-23.md")
    same_surface = read("docs/PLANCK_SCALE_GRAVITY_SECTOR_SAME_SURFACE_CLOSURE_THEOREM_2026-04-23.md")

    passed = 0
    total = 0

    unsafe_claims = [
        "B3 status: CLOSED",
        "Bare Cl(3) / Z^3 alone forces the gravitational sector",
        "this proves gravity from bare algebra alone",
    ]

    total += 1
    passed += expect(
        "b3-refuses-closure",
        "`B3 status: OPEN`" in note
        and "not a B3 closure" in note
        and not any(claim in note for claim in unsafe_claims),
        "the attempt explicitly remains a reduction/no-go theorem",
    )

    total += 1
    passed += expect(
        "matches-prior-b3-status",
        "B3 is not closed" in status
        and "B3` is the remaining hard open theorem" in program,
        "new result is consistent with the existing B3 status",
    )

    total += 1
    passed += expect(
        "bare-data-inventory-present",
        "local primitive event algebra with `16` atomic event states" in note
        and "`Z^3` translation/adjacency algebra" in note
        and "time-locked `3+1` event frame" in note,
        "the retained algebraic inputs are stated before the attempted proof",
    )

    total += 1
    passed += expect(
        "many-symbols-no-go-present",
        "Bare Locality Gives Many Continuum Symbols" in note
        and "scalar conformal / breathing modes" in note
        and "vector or gauge-like plaquette modes" in note
        and "antisymmetric/torsion-like modes" in note,
        "the note gives explicit survivor classes without metricity",
    )

    total += 1
    passed += expect(
        "metricity-ward-criterion-named",
        "Soldered metricity / equivalence Ward identity" in note
        and "one soldered coframe" in note
        and "conserved symmetric source" in note,
        "the exact missing primitive is named rather than hidden",
    )

    total += 1
    passed += expect(
        "conditional-uniqueness-law-present",
        "`L = alpha sqrt(|g|) + beta sqrt(|g|) R + dB + topological_4D`" in note
        and "`beta != 0`" in note
        and "unique propagating metric action sector" in note,
        "the conditional metric-sector uniqueness reduction is explicit",
    )

    total += 1
    passed += expect(
        "boundary-action-recovered-conditionally",
        "well-posed glued-cell variational principle force" in note
        and "accepted Regge/GHY boundary/action family" in note
        and "`N_grav = P_A`" in same_surface,
        "boundary/action sector is recovered only after the gravity sector exists",
    )

    total += 1
    passed += expect(
        "three-equivalent-next-targets",
        "**Soldering form.**" in note
        and "**Ward form.**" in note
        and "**Spin-2 form.**" in note,
        "the remaining B3 target is exposed in three equivalent forms",
    )

    total += 1
    passed += expect(
        "no-hidden-einstein-regge-input",
        "If the phrase \"geometric action sector\" already means" in note
        and "the B3 load has been moved into that definition" in note,
        "the note detects when Einstein/Regge has been smuggled into terminology",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
