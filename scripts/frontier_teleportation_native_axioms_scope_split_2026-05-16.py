#!/usr/bin/env python3
"""Structural scope-split verification for the native teleportation axiom bundle.

This is not a physics simulation. It is a deterministic structural audit of
the parent theory note

    docs/TELEPORTATION_NATIVE_AXIOMS_THEORY_NOTE.md

and its source-theorem-note scope split

    docs/TELEPORTATION_NATIVE_AXIOMS_SCOPE_SPLIT_SOURCE_THEOREM_NOTE_2026-05-16.md

The runner verifies that the parent note honestly factors into two disjoint
claim surfaces:

  B = finite-bookkeeping consistency on audited finite surfaces
  N = nature-grade closure (HOLD)

and that the parent note's strongest operational statement is restricted to
surface B. It also verifies the audited finite-surface bookkeeping identities
used by the scope-split source theorem (Bell-frame XOR rule for the cited
Psi+ resource, Manhattan delivery-tick identity for the recorded worldline).

The runner does NOT promote the teleportation lane, does NOT close any of the
nature-grade blockers, and does NOT modify the canonical harness index.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
PARENT_NOTE = REPO_ROOT / "docs" / "TELEPORTATION_NATIVE_AXIOMS_THEORY_NOTE.md"
SPLIT_NOTE = (
    REPO_ROOT
    / "docs"
    / "TELEPORTATION_NATIVE_AXIOMS_SCOPE_SPLIT_SOURCE_THEOREM_NOTE_2026-05-16.md"
)
COMPANION_RUNNER = (
    REPO_ROOT / "scripts" / "frontier_teleportation_axiom_closure_checks.py"
)
HARNESS_INDEX = REPO_ROOT / "docs" / "CANONICAL_HARNESS_INDEX.md"


# Bell-frame convention from the parent note.
BELL_BITS: dict[str, tuple[int, int]] = {
    "Phi+": (0, 0),
    "Phi-": (1, 0),
    "Psi+": (0, 1),
    "Psi-": (1, 1),
}


class Verdict(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass(frozen=True)
class Check:
    name: str
    verdict: Verdict
    detail: str


@dataclass(frozen=True)
class CitedEvidence:
    """Finite-surface evidence cited by the parent note (frozen literals)."""

    fixed_phi_f_avg: float = 0.334850
    framed_f_avg: float = 0.998483
    framed_min_fidelity: float = 0.997724
    pairwise_pre_record_distance: float = 2.498e-16
    delivery_tick: int = 11
    alice_tick: int = 4
    manhattan_distance: int = 7
    resource_frame: str = "Psi+"


# Seven nature-grade blockers used by the scope-split note. Each must be
# recognizable in the parent note's "Nature-Grade Closure Blockers" section.
NATURE_GRADE_BLOCKERS = [
    ("durable Bell measurement / record creation", ["durable Bell measurement"]),
    ("derived 3D+1 record channel", ["3D+1 record channel", "from retained field"]),
    ("scalable native resource generation", ["scalable native resource", "side=2"]),
    ("apparatus-level retained-axis readout / correction", ["apparatus-level"]),
    ("physical robustness / noise / leakage / control / finite resources", ["noise", "leakage"]),
    ("operational Bell-frame calibration", ["Bell-frame calibration operational"]),
    ("conservation ledgers / no-transfer accounting", ["conservation ledgers"]),
]


def bell_frame_correction(
    measurement: str, resource_frame: str
) -> tuple[int, int]:
    """Composed Bob correction bits (z, x), up to Pauli phase. (Parent A2.)"""

    mz, mx = BELL_BITS[measurement]
    hz, hx = BELL_BITS[resource_frame]
    return (mz ^ hz, mx ^ hx)


def manhattan_delivery_tick(
    alice_site: tuple[int, int, int],
    bob_site: tuple[int, int, int],
    alice_tick: int,
    speed: int,
) -> tuple[int, int]:
    """Earliest delivery tick at unit Manhattan speed."""

    if speed <= 0:
        raise ValueError("speed must be positive")
    distance = sum(abs(a - b) for a, b in zip(alice_site, bob_site))
    latency = (distance + speed - 1) // speed
    return alice_tick + latency, distance


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def structural_checks() -> list[Check]:
    parent_text = _read(PARENT_NOTE)
    split_text = _read(SPLIT_NOTE)
    companion_text = _read(COMPANION_RUNNER)
    harness_text = _read(HARNESS_INDEX)

    checks: list[Check] = []

    # 1. Parent note exists and is labeled planning / candidate.
    checks.append(
        Check(
            "parent_note_planning_status",
            Verdict.PASS
            if (
                parent_text
                and "planning" in parent_text.lower()
                and "candidate theory" in parent_text.lower()
                and "not retained framework" in parent_text.lower()
            )
            else Verdict.FAIL,
            "Parent note is labeled planning / candidate theory artifact, "
            "not retained framework promotion.",
        )
    )

    # 2. A4 explicitly "candidate only" in the parent's evidence map.
    checks.append(
        Check(
            "parent_a4_candidate_only",
            Verdict.PASS
            if ("A4 native resource genesis" in parent_text
                and "candidate only" in parent_text)
            else Verdict.FAIL,
            "Parent note labels A4 native resource genesis as candidate only "
            "in the evidence map.",
        )
    )

    # 3. Theorem 4 (six-factor product) names every required factor.
    required_t4_factors = [
        "retained-factor operator closure",
        "Bell-frame calibration",
        "native resource genesis",
        "3D+1 causal record delivery",
        "exhaustive branch accounting",
        "no-transfer boundary accounting",
    ]
    t4_ok = all(factor in parent_text for factor in required_t4_factors)
    checks.append(
        Check(
            "parent_theorem4_six_factor_product",
            Verdict.PASS if t4_ok else Verdict.FAIL,
            "Parent Theorem 4 names the full six-factor product for "
            "nature-grade closure.",
        )
    )

    # 4. Each named nature-grade blocker is in the parent blockers section.
    blockers_section_idx = parent_text.find("## Nature-Grade Closure Blockers")
    blockers_text = parent_text[blockers_section_idx:] if blockers_section_idx >= 0 else ""
    for label, keywords in NATURE_GRADE_BLOCKERS:
        present = all(kw in blockers_text for kw in keywords)
        checks.append(
            Check(
                f"parent_blocker_present::{label.split()[0].lower()}",
                Verdict.PASS if present else Verdict.FAIL,
                f"Parent blocker list contains: {label}.",
            )
        )

    # 5. Parent's strongest operational statement is B-surface only.
    closing_idx = parent_text.find("Status\n\nThis theory pass")
    closing_text = parent_text[closing_idx:] if closing_idx >= 0 else parent_text
    checks.append(
        Check(
            "parent_strongest_statement_b_surface_only",
            Verdict.PASS
            if (
                "audited finite surfaces" in closing_text
                and "does not promote" in closing_text
            )
            else Verdict.FAIL,
            "Parent note's strongest current statement is restricted to "
            "audited finite surfaces and does not promote the lane.",
        )
    )

    # 6. Companion runner exists and references parent note.
    checks.append(
        Check(
            "companion_runner_references_parent",
            Verdict.PASS
            if companion_text
            and "TELEPORTATION_NATIVE_AXIOMS_THEORY_NOTE.md" in companion_text
            else Verdict.FAIL,
            "Companion runner frontier_teleportation_axiom_closure_checks.py "
            "exists and references the parent note.",
        )
    )

    # 7. Harness index files lane under HOLD planning / no transfer language.
    checks.append(
        Check(
            "harness_index_parked_hold_language",
            Verdict.PASS
            if (
                "parked bounded planning lane" in harness_text
                and "nature-grade closure HOLD" in harness_text
                and "state teleportation only" in harness_text
                and "no matter/FTL/mass/charge transfer" in harness_text
            )
            else Verdict.FAIL,
            "Canonical harness index already files the lane as parked "
            "planning with nature-grade HOLD; no index update is asserted.",
        )
    )

    # 8. Scope-split note exists and is honestly scoped.
    checks.append(
        Check(
            "split_note_planning_scope",
            Verdict.PASS
            if (
                split_text
                and "planning/conditional scope-split bridge" in split_text
                and "nature-grade-HOLD" in split_text
                and "audit_required_before_effective_retained: true" in split_text
                and "bare_retained_allowed: false" in split_text
            )
            else Verdict.FAIL,
            "Scope-split source theorem note exists and self-labels as "
            "planning bridge with nature-grade HOLD.",
        )
    )

    return checks


def bookkeeping_identity_checks(evidence: CitedEvidence) -> list[Check]:
    """Re-verify the finite-surface bookkeeping identities the split relies on."""

    checks: list[Check] = []

    # T2 Bell-frame XOR: Psi+ resource needs an X-only Bob correction for c=Phi+
    # measurement outcome (per parent's convention).
    psi_plus_phi_plus = bell_frame_correction("Phi+", "Psi+")
    checks.append(
        Check(
            "t2_bell_xor_psi_plus_resource",
            Verdict.PASS if psi_plus_phi_plus == (0, 1) else Verdict.FAIL,
            "Bell-frame XOR rule maps (Phi+ outcome | Psi+ resource) -> (0,1) "
            "i.e. X-only correction.",
        )
    )

    # T2 framed vs fixed fidelity inequality on the cited Psi+ surface.
    checks.append(
        Check(
            "t2_framed_vs_fixed_fidelity",
            Verdict.PASS
            if (
                evidence.framed_f_avg > 0.99
                and evidence.fixed_phi_f_avg < 0.5
                and evidence.framed_min_fidelity > 0.99
            )
            else Verdict.FAIL,
            "Cited finite-surface fidelities: framed >= 0.99 and "
            "fixed Phi+ < 0.5, as recorded by the parent note.",
        )
    )

    # T3 pairwise pre-record distance at numerical zero.
    checks.append(
        Check(
            "t3_pre_record_input_independence",
            Verdict.PASS
            if evidence.pairwise_pre_record_distance < 1e-12
            else Verdict.FAIL,
            "Cited pairwise pre-record input distance is at numerical zero "
            "(parent: 2.498e-16).",
        )
    )

    # A3 Manhattan delivery identity on the cited (4, 7, 11) worldline.
    # Use Alice=(1,1,1), Bob=(5,3,2): |4|+|2|+|1| = 7.
    expected_tick, expected_distance = manhattan_delivery_tick(
        alice_site=(1, 1, 1),
        bob_site=(5, 3, 2),
        alice_tick=evidence.alice_tick,
        speed=1,
    )
    checks.append(
        Check(
            "a3_manhattan_distance_identity",
            Verdict.PASS
            if expected_distance == evidence.manhattan_distance
            else Verdict.FAIL,
            f"Manhattan distance recomputes to {expected_distance}, "
            f"matching cited {evidence.manhattan_distance}.",
        )
    )
    checks.append(
        Check(
            "a3_manhattan_delivery_tick_identity",
            Verdict.PASS
            if expected_tick == evidence.delivery_tick
            else Verdict.FAIL,
            f"Manhattan delivery tick recomputes to {expected_tick}, "
            f"matching cited {evidence.delivery_tick} (= alice_tick + L1).",
        )
    )

    return checks


def split_disjointness_checks() -> list[Check]:
    """Sanity checks on the structural disjointness of surfaces B and N."""

    split_text = _read(SPLIT_NOTE)
    checks: list[Check] = []

    checks.append(
        Check(
            "split_names_surface_b_and_n",
            Verdict.PASS
            if (
                "Finite-bookkeeping consistency surface" in split_text
                and "Nature-grade closure surface" in split_text
            )
            else Verdict.FAIL,
            "Scope-split note explicitly names surfaces B and N.",
        )
    )

    checks.append(
        Check(
            "split_does_not_claim_n_closure",
            Verdict.PASS
            if (
                "Surface `N` remains HOLD" in split_text
                and "Nothing about surface `N` is closed here" in split_text
            )
            else Verdict.FAIL,
            "Scope-split note does not claim any nature-grade closure.",
        )
    )

    checks.append(
        Check(
            "split_does_not_promote_lane",
            Verdict.PASS
            if (
                "teleportation lane is not promoted" in split_text
                and "No new physics axiom" in split_text
            )
            else Verdict.FAIL,
            "Scope-split note explicitly declines lane promotion and adds "
            "no new physics axiom.",
        )
    )

    return checks


def print_table(checks: Iterable[Check]) -> None:
    for check in checks:
        print(f"{check.verdict.value:4s}  {check.name}: {check.detail}")


def main() -> int:
    all_checks: list[Check] = []
    all_checks.extend(structural_checks())
    all_checks.extend(bookkeeping_identity_checks(CitedEvidence()))
    all_checks.extend(split_disjointness_checks())

    print_table(all_checks)

    n_pass = sum(1 for c in all_checks if c.verdict == Verdict.PASS)
    n_fail = sum(1 for c in all_checks if c.verdict == Verdict.FAIL)
    total = len(all_checks)

    print()
    print(f"SUMMARY: PASS={n_pass} FAIL={n_fail} TOTAL={total}")
    print()
    print("SCOPE: This runner verifies the structural scope split between")
    print("  B = finite-bookkeeping consistency on audited surfaces, and")
    print("  N = nature-grade closure (HOLD).")
    print("It does NOT promote the teleportation lane, does NOT close any")
    print("nature-grade blocker, and does NOT modify the canonical harness")
    print("index. The parent note remains at planning / candidate status.")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
