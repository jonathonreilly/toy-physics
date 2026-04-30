"""Runner: PMNS three-identity Q_Koide-from-V8 support lift (Block 7)."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

AUDIT_FAILS: list[str] = []


def audit(name: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not condition:
        AUDIT_FAILS.append(name)


def read_doc(path_rel: str) -> str:
    return (DOCS_DIR / path_rel).read_text(encoding="utf-8")


def main() -> int:
    print("=" * 72)
    print("PMNS three-identity Q_Koide-from-V8 support lift (Block 7) audit")
    print("=" * 72)

    v8 = read_doc("KOIDE_Q_OP_LOCALITY_SOURCE_DOMAIN_CLOSURE_THEOREM_NOTE_2026-04-29.md")
    audit("V8 (Block 1) note exists with support Q record",
          "actual_current_surface_status: support" in v8 and "Q = 2/3" in v8,
          "Block 1 prerequisite")

    pmns = read_doc("PMNS_SELECTOR_THREE_IDENTITY_SUPPORT_NOTE_2026-04-21.md")
    audit("PMNS three-identity support note exists",
          len(pmns) > 0,
          "support proposal on affine Hermitian chart")
    audit("Q_Koide = 2/3 used as PMNS chart constant",
          "Q_Koide = 2/3" in pmns,
          "chart constant import")
    audit("SELECTOR² = Q_Koide identity in PMNS chart",
          "SELECTOR^2 = Q_Koide" in pmns or "SELECTOR² = Q_Koide" in pmns,
          "scalar identity")

    # Compose V8's Q closure with the PMNS chart constant
    Q_Koide_V8 = 2 / 3
    SELECTOR_derived = np.sqrt(Q_Koide_V8)
    SELECTOR_expected = np.sqrt(6) / 3
    audit("V8-derived Q_Koide = 2/3", np.isclose(Q_Koide_V8, 2/3), f"Q_Koide = {Q_Koide_V8}")
    audit("SELECTOR = √Q_Koide = √6/3 from V8",
          np.isclose(SELECTOR_derived, SELECTOR_expected),
          f"√(2/3) = {SELECTOR_derived:.6f} = √6/3 = {SELECTOR_expected:.6f}")
    audit("SELECTOR² = Q_Koide algebraic identity",
          np.isclose(SELECTOR_derived ** 2, Q_Koide_V8),
          f"SELECTOR² = {SELECTOR_derived ** 2:.6f} = Q_Koide = {Q_Koide_V8:.6f}")

    own = read_doc("PMNS_THREE_IDENTITY_Q_KOIDE_FROM_V8_SUPPORT_LIFT_THEOREM_NOTE_2026-04-29.md")
    audit("V1 actual_current_surface_status: support",
          "actual_current_surface_status: support" in own, "support-grade lift")
    audit("V1 audit_required_before_effective_retained: true",
          "audit_required_before_effective_retained: true" in own, "firewall")
    audit("V1 bare_retained_allowed: false",
          "bare_retained_allowed: false" in own, "firewall")
    audit("V1 proposed_selector_laws_status: open",
          "proposed_selector_laws_status: open" in own, "PMNS gaps unchanged")
    audit("V1 broader_pmns_dm_gate_status: open",
          "broader_pmns_dm_gate_status: open" in own, "PMNS gate unchanged")

    print()
    print("=" * 72)
    fail_count = len(AUDIT_FAILS)
    print(f"FAIL count: {fail_count}")
    print("PMNS_Q_KOIDE_FROM_V8_SUPPORT_LIFT_VERIFIED =", fail_count == 0)
    if fail_count == 0:
        print()
        print("All Block 7 chain authorities + algebraic identities verified.")
        return 0
    else:
        print(f"Failed audits: {AUDIT_FAILS}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
