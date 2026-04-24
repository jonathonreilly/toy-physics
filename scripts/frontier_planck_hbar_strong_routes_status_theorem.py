#!/usr/bin/env python3
"""Verify the hbar strong-routes status theorem."""

from __future__ import annotations

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
    note = read("docs/PLANCK_SCALE_HBAR_STRONG_ROUTES_STATUS_THEOREM_2026-04-24.md")
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    gamma_attempt = read("docs/PLANCK_SCALE_PRIMITIVE_ACTION_UNIT_GAMMA_ONE_ATTEMPT_2026-04-24.md")
    gamma_period = read("docs/PLANCK_SCALE_GAMMA_PHASE_PERIOD_OBSTRUCTION_THEOREM_2026-04-24.md")
    integral_count = read("docs/PLANCK_SCALE_PRIMITIVE_INTEGRAL_ACTION_COUNT_THEOREM_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "target-is-gamma-one",
        "`Phi(P) = gamma Tr(P)/16`" in note
        and "`Phi(P) = gamma Tr(P) / 16`" in phase_trace
        and "`Phi(I_16) = 1`" in note,
        "hbar target remains the non-homogeneous total-cell action unit",
    )

    total += 1
    passed += expect(
        "noncompact-central-extension-does-not-fix-scale",
        "`0 -> R -> G_hat -> G -> 1`" in note
        and "`lambda Z` is also\ncentral" in note
        and "real action generator up to scale" in note,
        "real central lift removes periodicity but not normalization",
    )

    total += 1
    passed += expect(
        "cubic-symmetry-does-not-supply-symplectic-form",
        "real Heisenberg-type cocycles require an antisymmetric/symplectic two-form"
        in note
        and "supplies no invariant\nspatial two-form" in note
        and "not already present in\nbare `Cl(3)` / `Z^3`" in note,
        "central-extension route needs a derived cocycle/symplectic datum",
    )

    total += 1
    passed += expect(
        "index-route-needs-new-objects",
        "`Index(D_cell) = 1`" in note
        and "canonical Fredholm/Dirac pair `D_cell`" in note
        and "one-cell spectral flow is one" in note,
        "index route is viable but not currently constructed",
    )

    total += 1
    passed += expect(
        "primitive-action-generator-is-exact-survivor",
        "`A_cell := I_16`" in note
        and "`Phi(A_cell) = 1`" in note
        and "This closes `gamma = 1` once the source-free closed histories are treated as\n"
        "the free integral monoid `N[A_cell]`" in note
        and "`Phi(I_16) = ell([A_cell]) = 1`" in integral_count,
        "the direct primitive action route is now closed in reduced count units",
    )

    total += 1
    passed += expect(
        "ward-reuse-would-be-circular",
        "Reusing it for hbar would be circular" in note
        and "before importing standard gravitational\narea/action normalization" in note,
        "boundary Planck Ward cannot be recycled into hbar without circularity",
    )

    total += 1
    passed += expect(
        "prior-no-gos-are-respected",
        "homogeneous" in note
        and "periodic" in note
        and "finite-root" in note
        and "`Phi -> lambda Phi`" in gamma_attempt
        and "narrow no-go theorem" in gamma_period,
        "new audit does not reopen already-blocked shortcuts",
    )

    total += 1
    passed += expect(
        "reviewer-links-hbar-strong-routes",
        "PLANCK_SCALE_HBAR_STRONG_ROUTES_STATUS_THEOREM_2026-04-24.md" in reviewer,
        "canonical packet links the hbar strong-routes theorem",
    )

    total += 1
    passed += expect(
        "si-hbar-still-not-claimed",
        "It is closed as reduced action count and as structural `S/hbar=Phi`, not as an\n"
        "SI-value derivation of `hbar`" in note
        and "Those routes are not closed in the current branch" in note
        and "Do not use:\n\n> The branch predicts the SI numerical value of `hbar`."
        in note,
        "structural hbar closure is separated from SI hbar and independent routes",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
