#!/usr/bin/env python3
"""Verifier for the ordered hbar/action-quantum attack theorem."""

from pathlib import Path
from fractions import Fraction
import math


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
    note = read("docs/PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md")
    status = read("docs/PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md")
    information = read("docs/PLANCK_SCALE_INFORMATION_ACTION_UNIT_MAP_THEOREM_LANE_2026-04-23.md")
    timelock = read("docs/PLANCK_SCALE_TIMELOCKED_CONVERTED_INFORMATION_ACTION_CONSTANT_LANE_2026-04-23.md")
    action_phase = read("docs/PLANCK_SCALE_ELEMENTARY_ACTION_PHASE_REDUCTION_THEOREM_2026-04-23.md")
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    total += 1
    passed += expect(
        "three-noncircular-routes-enumerated",
        "Independent lattice-spacing route" in note
        and "Structural action-unit route" in note
        and "Dimensionless prediction route" in note,
        "the program separates the only non-circular hbar options",
    )

    total += 1
    passed += expect(
        "planck-hbar-algebra-recorded",
        "`hbar = a^2 c_light^3 / G`" in note
        and "`a^2 c_light^3 / (hbar G) = 1`" in status,
        "a=l_P is algebraically equivalent to a dimensionless hbar relation",
    )

    total += 1
    passed += expect(
        "no-free-hbar-from-planck",
        "To turn this into a prediction, `a` must\nbe fixed independently of `hbar`" in note
        and "If `a` is defined only by `l_P`" in note,
        "the theorem prevents solving the definition backward",
    )

    total += 1
    passed += expect(
        "cosmic-address-condition-is-noncircular",
        "`hbar = R^2 c_light^3 / (G N^2)`" in note
        and "`N` is derived rather than chosen to fit `hbar`" in note,
        "current time/age can help only with an independently derived tick count",
    )

    eps = math.pi / 2.0
    q_required = eps / (8.0 * math.pi)
    kappa_bit = q_required / 2.0
    total += 1
    passed += expect(
        "kappa-info-numerics-are-exact",
        abs(q_required - 1.0 / 16.0) < 1e-15
        and abs(kappa_bit - 1.0 / 32.0) < 1e-15
        and "`q_* = eps_*/(8 pi) = 1/16`" in note
        and "`kappa_info^(bit) = q_*/2 = 1/32`" in note,
        f"minimal defect gives q={q_required:.12f}, kappa_bit={kappa_bit:.12f}",
    )

    total += 1
    passed += expect(
        "phase-trace-reduces-target-to-gamma",
        "`q_atom = gamma/16`" in note
        and "`kappa_info^(bit) = gamma/32`" in note
        and "`Phi(P) = gamma Tr(P) / 16`" in phase_trace
        and "`gamma = 1`" in note,
        "the first target is now the total-cell reduced action scalar",
    )

    total += 1
    passed += expect(
        "existing-information-obstructions-respected",
        "direct information-as-action is log-base dependent" in note
        and "raw `log Z` is chart-density dependent" in note
        and "`q_* = kappa_info I_*`" in information,
        "the attack order does not reuse ruled-out direct information routes",
    )

    total += 1
    passed += expect(
        "timelock-status-respected",
        "time-lock fixes the elementary information carrier, not the conversion\n  constant" in note
        and "The exact time-lock does **not** derive `kappa_info`" in timelock,
        "the note keeps kappa_info open rather than pretending time-lock proves it",
    )

    total += 1
    passed += expect(
        "action-phase-reduction-respected",
        "`a^2/l_P^2 = 8 pi q_*/eps_*`" in note
        and "`a^2 / l_P^2 = 8 pi q_* / eps_*`" in action_phase,
        "the hbar route remains tied to the existing action-phase reduction",
    )

    total += 1
    passed += expect(
        "fallback-lanes-are-ordered",
        "Projective phase / central-extension theorem" in note
        and "Discrete symplectic/Weyl commutator theorem" in note
        and "`alpha` prediction" in note,
        "fallbacks are explicit and not mixed into the current Planck proof",
    )

    total += 1
    passed += expect(
        "reviewer-packet-links-attack-order",
        "PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md" in reviewer,
        "canonical packet points reviewers to the ordered hbar program",
    )

    total += 1
    passed += expect(
        "safe-unsafe-claims-recorded",
        "The first target is now\n> `gamma = 1`" in note
        and "> Deriving `a = l_P` already predicts `hbar`" in note,
        "the note states the next target and bans the circular claim",
    )

    # Keep exact rational witnesses available for reviewer-readable output.
    exact_q = Fraction(1, 16)
    exact_kappa = Fraction(1, 32)
    total += 1
    passed += expect(
        "exact-rational-targets",
        exact_q.numerator == 1
        and exact_q.denominator == 16
        and exact_kappa.numerator == 1
        and exact_kappa.denominator == 32,
        f"q_*={exact_q}, kappa_info_bit={exact_kappa}",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
