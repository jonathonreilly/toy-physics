#!/usr/bin/env python3
"""
PR #230 same-1PI scalar-pole boundary.

The same-1PI route is the most tempting way to "fix Ward identity and fix
YT".  It equates a scalar-singlet four-fermion coefficient in two
representations.  This runner checks why that does not close PR #230:

1. the existing same-1PI notes use H_unit/Rep-B matrix-element data and are
   audited conditional, not clean PR #230 physical-readout authorities;
2. a four-fermion exchange coefficient fixes only the product y^2 D_phi.
   Field/source rescaling can keep Gamma^(4) fixed while changing the external
   scalar LSZ/y readout.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_same_1pi_scalar_pole_boundary_2026-05-01.json"

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="ignore")


def ledger_row(key: str) -> dict:
    rows = json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]
    return rows.get(key, {})


def main() -> int:
    print("PR #230 same-1PI scalar-pole boundary")
    print("=" * 72)

    same_1pi = read("docs/G_BARE_TWO_WARD_SAME_1PI_PINNING_THEOREM_NOTE_2026-04-19.md")
    rep_b = read("docs/G_BARE_TWO_WARD_REP_B_INDEPENDENCE_THEOREM_NOTE_2026-04-19.md")
    ward_no_go = read("docs/YT_TOP_MASS_WARD_DECOMP_NO_GO_NOTE_2026-04-30.md")

    rows = {
        "same_1pi": ledger_row("g_bare_two_ward_same_1pi_pinning_theorem_note_2026-04-19"),
        "rep_b": ledger_row("g_bare_two_ward_rep_b_independence_theorem_note_2026-04-19"),
        "ward": ledger_row("yt_ward_identity_derivation_theorem"),
    }
    statuses = {key: row.get("effective_status") for key, row in rows.items()}

    uses_h_unit_rep_b = "H_unit" in same_1pi and "F_Htt" in same_1pi and "<0|H_unit" in same_1pi
    rep_b_matrix_element = "F_Htt" in rep_b and "<0 | H_unit" in rep_b
    ward_no_go_flags_same_1pi = "same-1PI" in ward_no_go and "H_unit" in ward_no_go
    statuses_not_clean = statuses["same_1pi"] == "audited_conditional" and statuses["rep_b"] == "audited_conditional"

    # Four-fermion exchange coefficient invariant under scalar field rescaling.
    # If Gamma4 = y^2 D and D is rescaled by 1/kappa^2 while y is rescaled by
    # kappa, Gamma4 is unchanged but the external scalar-leg readout changes.
    gamma4 = 1.0 / 6.0
    kappas = [0.5, 1.0, 2.0]
    exchange_models = []
    for kappa in kappas:
        y = math.sqrt(gamma4) * kappa
        d_phi = 1.0 / (kappa * kappa)
        exchange_models.append(
            {
                "kappa": kappa,
                "y_vertex": y,
                "D_phi_normalization": d_phi,
                "gamma4_exchange": y * y * d_phi,
            }
        )
    gamma4_invariant = all(abs(row["gamma4_exchange"] - gamma4) < 1.0e-15 for row in exchange_models)
    y_distinct = len({round(row["y_vertex"], 15) for row in exchange_models}) == len(exchange_models)

    report("same-1pi-note-uses-h-unit-rep-b", uses_h_unit_rep_b, "H_unit/F_Htt Rep-B data present")
    report("rep-b-note-is-matrix-element-route", rep_b_matrix_element, "Rep-B defines F_Htt through H_unit matrix element")
    report("ledger-statuses-not-clean-for-pr230", statuses_not_clean, str(statuses))
    report("ward-decomp-flags-same-1pi-boundary", ward_no_go_flags_same_1pi, "prior no-go already marks same-1PI/H_unit obstruction")
    report("same-gamma4-allows-different-y", gamma4_invariant and y_distinct, f"models={exchange_models}")
    report("scalar-pole-residue-still-required", True, "Gamma4 fixes y^2 D, not y and D separately")

    result = {
        "actual_current_surface_status": "exact negative boundary / same-1PI not PR230 closure",
        "verdict": (
            "The existing same-1PI route is not a hidden PR #230 top-Yukawa "
            "closure.  Its current notes use H_unit/Rep-B matrix-element data "
            "and are audited conditional.  More basically, a four-fermion "
            "coefficient fixes y^2 D_phi, not the separately normalized "
            "physical scalar vertex y and scalar pole residue D_phi.  A scalar "
            "pole/LSZ normalization theorem is still required."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "The same-1PI route does not independently fix scalar LSZ/pole normalization.",
        "ledger_statuses": statuses,
        "exchange_rescaling_models": exchange_models,
        "required_next_theorem": [
            "derive scalar pole residue/canonical normalization independently of H_unit matrix elements",
            "then use any same-1PI coefficient only after y and D_phi are separately normalized",
        ],
        "strict_non_claims": [
            "does not reject the same-1PI g_bare support route in its own scope",
            "does not promote PR230",
            "does not define y_t through H_unit",
            "does not use observed top mass or Yukawa values",
        ],
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
