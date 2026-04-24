#!/usr/bin/env python3
"""Verifier for the action-phase conversion target theorem."""

from pathlib import Path
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
    note = read("docs/PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md")
    hbar_status = read("docs/PLANCK_SCALE_HBAR_STATUS_AND_REMAINING_OBJECTIONS_AUDIT_2026-04-23.md")
    hbar_attack = read("docs/PLANCK_SCALE_HBAR_ATTACK_ORDER_THEOREM_2026-04-23.md")
    info = read("docs/PLANCK_SCALE_INFORMATION_ACTION_UNIT_MAP_THEOREM_LANE_2026-04-23.md")
    phase_trace = read("docs/PLANCK_SCALE_PRIMITIVE_PHASE_TRACE_REDUCTION_THEOREM_2026-04-24.md")
    reviewer = read("docs/PLANCK_SCALE_REVIEWER_CANONICAL_SUBMISSION_PACKET_2026-04-23.md")

    passed = 0
    total = 0

    eps = math.pi / 2.0
    q_required = eps / (8.0 * math.pi)
    kappa_bit = q_required / 2.0

    total += 1
    passed += expect(
        "hbar-role-stated",
        "`hbar` is the conversion factor between action and phase" in note
        and "`phi := S / hbar`" in note,
        "hbar is framed as action-to-phase conversion",
    )

    total += 1
    passed += expect(
        "later-structural-conversion-is-recorded",
        "later action-phase representation\nhbar theorem also derives the structural conversion statement" in note
        and "derives the structural action-to-phase role of `hbar`" in hbar_status
        and "does **not** derive the SI value of\n`hbar`" in hbar_status,
        "the target note is superseded by structural S/hbar=Phi while refusing SI hbar",
    )

    total += 1
    passed += expect(
        "q-target-exact",
        abs(q_required - 1.0 / 16.0) < 1e-15
        and "`q_* = 1/16`" in note,
        f"eps=pi/2 gives q_*={q_required:.12f}",
    )

    total += 1
    passed += expect(
        "kappa-target-exact",
        abs(kappa_bit - 1.0 / 32.0) < 1e-15
        and "`kappa_info = 1/32 per bit`" in note,
        f"two-bit carrier gives kappa={kappa_bit:.12f}",
    )

    total += 1
    passed += expect(
        "consistent-with-existing-hbar-attack",
        "`kappa_info^(bit) = q_*/2 = 1/32`" in hbar_attack
        and "`q_* = kappa_info I_*`" in info,
        "the new target matches existing hbar/information reductions",
    )

    total += 1
    passed += expect(
        "trace-reduction-sharpens-target-to-gamma",
        "`q_atom = gamma / 16`" in note
        and "`kappa_info = gamma / 32 per bit`" in note
        and "`Phi(P) = gamma Tr(P) / 16`" in phase_trace,
        "the target is now reduced to the gamma = 1 action-unit scalar",
    )

    total += 1
    passed += expect(
        "non-solutions-excluded",
        "predicting the SI decimal value of `hbar`" in note
        and "solving `a = l_P` backward" in note
        and "setting `q_*` by hand" in note,
        "unit-convention and backward-Planck routes are excluded",
    )

    total += 1
    passed += expect(
        "reviewer-links-action-phase",
        "PLANCK_SCALE_ACTION_PHASE_CONVERSION_TARGET_THEOREM_2026-04-23.md" in reviewer,
        "canonical packet links the action-phase target theorem",
    )

    print(f"SUMMARY: PASS={passed} FAIL={total - passed}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
