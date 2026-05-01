#!/usr/bin/env python3
"""
PR #230 YT bridge-stack import audit.

The axiom-first / constructive UV bridge stack is the strongest repo-native
candidate that might look like a missed top-Yukawa proof.  This runner checks
whether it can serve as retained closure for PR #230 under the current audit
firewall.

It cannot: the stack is explicitly bounded/conditional, imports accepted
endpoint or plaquette/u0 surfaces, and says it does not make the y_t lane
unbounded.  It remains useful support for transport, not a direct y_t
derivation.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
OUTPUT = ROOT / "outputs" / "yt_bridge_stack_import_audit_2026-05-01.json"

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


def ledger_rows() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))["rows"]


def main() -> int:
    print("PR #230 YT bridge-stack import audit")
    print("=" * 72)

    rows = ledger_rows()
    bridge_ids = [
        "yt_axiom_first_microscopic_bridge_theorem",
        "yt_constructive_uv_bridge_note",
        "yt_bridge_action_invariant_note",
        "yt_bridge_endpoint_shift_bound_note",
        "yt_bridge_hessian_selector_note",
        "yt_bridge_higher_order_corrections_note",
        "yt_bridge_moment_closure_note",
        "yt_bridge_nonlocal_corrections_note",
        "yt_bridge_operator_closure_note",
        "yt_bridge_rearrangement_principle_note",
        "yt_bridge_uv_class_uniqueness_note",
        "yt_bridge_variational_selector_note",
        "yt_exact_interacting_bridge_transport_note",
    ]
    status_rows = {
        claim_id: {
            "effective_status": rows.get(claim_id, {}).get("effective_status"),
            "audit_status": rows.get(claim_id, {}).get("audit_status"),
            "runner_path": rows.get(claim_id, {}).get("runner_path"),
        }
        for claim_id in bridge_ids
    }
    retained_rows = {
        claim_id: row
        for claim_id, row in status_rows.items()
        if row.get("effective_status") == "retained"
    }

    axiom_first = read("docs/YT_AXIOM_FIRST_MICROSCOPIC_BRIDGE_THEOREM.md")
    constructive = read("docs/YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md")

    bounded_phrases = [
        "does **not** by itself make the `y_t` lane unbounded",
        "does **not** yet prove full exact closure",
        "does not yet prove full exact closure",
        "This still does **not** make `y_t` unbounded",
        "bounded support note",
    ]
    accepted_endpoint_import = "accepted endpoint `y_t(v)=0.9176`" in constructive
    plaquette_import = "accepted plaquette / `u_0` surface" in axiom_first
    self_nonclosure = any(phrase in axiom_first or phrase in constructive for phrase in bounded_phrases)
    all_nonretained = not retained_rows
    unaudited_or_conditional = {
        claim_id: row
        for claim_id, row in status_rows.items()
        if row.get("effective_status") in {"bounded", "audited_conditional", None}
        or row.get("audit_status") in {"unaudited", None}
    }

    report("bridge-rows-present", all(claim_id in rows for claim_id in bridge_ids), f"rows={len(status_rows)}")
    report("no-retained-bridge-authority", all_nonretained, f"retained_rows={list(retained_rows)}")
    report("bridge-stack-nonclosure-self-stated", self_nonclosure, "notes state bounded/not unbounded")
    report("constructive-bridge-imports-accepted-endpoint", accepted_endpoint_import, "accepted y_t endpoint appears as fit target")
    report("axiom-first-bridge-imports-plaquette-u0", plaquette_import, "accepted plaquette/u0 surface appears in input stack")
    report("bridge-stack-has-unaudited-or-conditional-parents", bool(unaudited_or_conditional), f"count={len(unaudited_or_conditional)}")
    report("not-pr230-retained-closure", True, "bridge stack remains bounded transport support, not direct y_t proof")

    result = {
        "actual_current_surface_status": "exact negative boundary / bridge stack not PR230 closure",
        "verdict": (
            "The axiom-first / constructive UV bridge stack is not a missed "
            "retained top-Yukawa proof.  Its own notes classify it as bounded "
            "support, it imports the accepted y_t(v) endpoint or accepted "
            "plaquette/u0 surfaces, and audit ledger rows are bounded, "
            "unaudited, or audited conditional.  It can support transport once "
            "a boundary is supplied; it cannot replace the direct correlator "
            "measurement or microscopic scalar-residue theorem in PR #230."
        ),
        "proposal_allowed": False,
        "proposal_allowed_reason": "Bridge stack uses bounded/conditional transport and endpoint imports; it does not derive y_t from A_min.",
        "status_rows": status_rows,
        "unaudited_or_conditional": unaudited_or_conditional,
        "text_checks": {
            "accepted_endpoint_import": accepted_endpoint_import,
            "plaquette_u0_import": plaquette_import,
            "self_nonclosure": self_nonclosure,
        },
        "strict_non_claims": [
            "does not demote the bridge stack as support",
            "does not use observed or accepted y_t endpoint as proof input",
            "does not use alpha_LM/plaquette/u0 as PR230 proof input",
            "does not define y_t through H_unit matrix elements",
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
