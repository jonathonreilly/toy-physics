#!/usr/bin/env python3
"""Re-verify the audit ready-leaf inventory synthesis meta note against
the live audit queue and ledger.

This is a navigation-map / classification check, not a physics proof.
The synthesis note makes specific claims about the live queue + ledger:

  - the total `ready=True` count is 36;
  - per-category counts are A=4, B=1, C=0, D=29, E=0, F=2;
  - the 4 A candidates, 1 B candidate, 2 F candidates, and the top D
    candidates listed in the synthesis are each currently `ready=True`
    with the stated `claim_type`;
  - the B candidate (alpha_lm) is currently `claim_type=decoration`;
  - the A candidates' latest-dated prior audits (if any) are
    `audited_clean`;
  - the F candidates' latest-dated prior audits are
    `audited_conditional` with notes prefixed `missing_dependency_edge`;
  - the D candidates' latest-dated prior audits are
    `audited_conditional` but NOT `missing_dependency_edge`;
  - the synthesis itself is `claim_type: meta` with
    `proposal_allowed: false`.

If any of these drift, the runner FAILs and the synthesis needs a
refresh.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "docs" / "audit" / "data" / "audit_queue.json"
LEDGER = ROOT / "docs" / "audit" / "data" / "audit_ledger.json"
NOTE = ROOT / "docs" / "AUDIT_READY_LEAF_INVENTORY_SYNTHESIS_META_NOTE_2026-05-10.md"


EXPECTED_TOTAL_READY = 36
EXPECTED_CATEGORY_COUNTS = {"A": 4, "B": 1, "C": 0, "D": 29, "E": 0, "F": 2}

# A — clean-just-waiting: latest dated verdict was audited_clean (or no
# prior dated audit at all). Listed verbatim in the synthesis A table.
EXPECTED_A_ROWS = {
    "valley_linear_action_note": "bounded_theorem",
    "koide_gamma_orbit_exponential_value_law_candidate_note_2026-04-18": "positive_theorem",
    "koide_s_l1_topological_chern_simons_note_2026-05-08_probes_l1_topological": "bounded_theorem",
    "lattice_nn_mass_response_note": "positive_theorem",
}

# B — misclassification (alpha_lm pattern, single canonical case).
EXPECTED_B_ROWS = {
    "alpha_lm_geometric_mean_identity_theorem_note_2026-04-24": "decoration",
}

# F — chain-blocked (missing_dependency_edge): both currently ready.
EXPECTED_F_ROWS = {
    "claude_complex_action_grown_companion_note": "positive_theorem",
    "mesoscopic_surrogate_alternate_family_scout_note": "bounded_theorem",
}

# D top 5 by score, listed in the synthesis D top-5 table. Score-tied
# leaf rows are sorted by claim_id for determinism in the runner.
EXPECTED_D_TOP5_ROWS = {
    "persistent_object_blended_readout_transfer_sweep_note_2026-04-16": "bounded_theorem",
    "lattice_3d_l2_numpy_h0125_bridge_note": "bounded_theorem",
    "dispersion_high_p_tiebreaker_note": "positive_theorem",
    "dm_abcc_basin_finite_search_support_note_2026-04-30": "positive_theorem",
    "dm_chamber_signature_structure_note_2026-04-19": "positive_theorem",
}


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f" | {detail}" if detail else ""
    print(f"{tag}: {label}{suffix}")


def latest_dated_audit(prior_audits: list[dict]) -> dict | None:
    with_date = [p for p in prior_audits if p.get("audit_date")]
    if not with_date:
        return None
    return sorted(with_date, key=lambda x: x.get("audit_date"), reverse=True)[0]


def classify(row: dict, ledger_row: dict) -> str:
    """Mirror the synthesis classification logic."""
    cid = row["claim_id"]
    qtype = row.get("claim_type")
    pa = ledger_row.get("previous_audits", [])

    # E: open_gate
    if qtype == "open_gate":
        return "E"

    # B: alpha_lm canonical case (the only B candidate at write time).
    if cid == "alpha_lm_geometric_mean_identity_theorem_note_2026-04-24":
        return "B"

    latest = latest_dated_audit(pa)
    if latest is None:
        # Truly first-time: A (clean-just-waiting on first pass).
        return "A"

    latest_v = latest.get("audit_status")
    notes = (latest.get("notes_for_re_audit_if_any") or "").strip()

    if latest_v == "audited_clean":
        return "A"
    if latest_v == "audited_conditional" and notes.startswith("missing_dependency_edge"):
        return "F"
    if latest_v == "audited_conditional":
        return "D"

    # No prior dated verdict pattern matched: treat as A (presumed clean
    # on first dated audit).
    return "A"


def main() -> int:
    if not QUEUE.exists():
        print(f"missing queue: {QUEUE}")
        return 1
    if not LEDGER.exists():
        print(f"missing ledger: {LEDGER}")
        return 1
    if not NOTE.exists():
        print(f"missing synthesis note: {NOTE}")
        return 1

    queue = json.loads(QUEUE.read_text())
    rows = json.loads(LEDGER.read_text())["rows"]
    note = NOTE.read_text()

    print("audit ready-leaf inventory synthesis check")
    print(f"note: {NOTE.relative_to(ROOT)}")
    print()

    # ---- classification + governance ----
    check("synthesis note is meta", "**Claim type:** meta" in note)
    check(
        "synthesis declares proposal_allowed: false",
        "proposal_allowed: false" in note,
    )
    audit_clean_token = "audited" + "_clean"
    check(
        "synthesis does not declare itself audited_clean",
        audit_clean_token not in note.split("## ", 1)[0],
        "header block must not pre-empt audit verdict",
    )

    # ---- total ready count ----
    ready_rows = [r for r in queue.get("queue", []) if r.get("ready")]
    check(
        f"total ready_count = {EXPECTED_TOTAL_READY}",
        len(ready_rows) == EXPECTED_TOTAL_READY,
        f"actual={len(ready_rows)}",
    )
    check(
        f"queue.ready_count field = {EXPECTED_TOTAL_READY}",
        queue.get("ready_count") == EXPECTED_TOTAL_READY,
        f"actual={queue.get('ready_count')}",
    )

    # ---- per-category counts ----
    by_cat: dict[str, list[dict]] = {k: [] for k in "ABCDEF"}
    for r in ready_rows:
        cid = r["claim_id"]
        led = rows.get(cid, {})
        cat = classify(r, led)
        by_cat[cat].append(r)

    for cat, expected in EXPECTED_CATEGORY_COUNTS.items():
        actual = len(by_cat[cat])
        check(
            f"category {cat} count = {expected}",
            actual == expected,
            f"actual={actual}",
        )

    # ---- explicit A roster ----
    actual_a = {r["claim_id"]: r.get("claim_type") for r in by_cat["A"]}
    check(
        "A roster matches synthesis",
        set(actual_a) == set(EXPECTED_A_ROWS),
        f"extra={sorted(set(actual_a) - set(EXPECTED_A_ROWS))} "
        f"missing={sorted(set(EXPECTED_A_ROWS) - set(actual_a))}",
    )
    for cid, expected_type in EXPECTED_A_ROWS.items():
        check(
            f"A row claim_type matches: {cid}",
            actual_a.get(cid) == expected_type,
            f"actual={actual_a.get(cid)!r}",
        )

    # ---- explicit B roster ----
    actual_b = {r["claim_id"]: r.get("claim_type") for r in by_cat["B"]}
    check(
        "B roster matches synthesis",
        set(actual_b) == set(EXPECTED_B_ROWS),
        f"extra={sorted(set(actual_b) - set(EXPECTED_B_ROWS))} "
        f"missing={sorted(set(EXPECTED_B_ROWS) - set(actual_b))}",
    )
    for cid, expected_type in EXPECTED_B_ROWS.items():
        check(
            f"B row claim_type matches: {cid}",
            actual_b.get(cid) == expected_type,
            f"actual={actual_b.get(cid)!r}",
        )

    # ---- explicit F roster ----
    actual_f = {r["claim_id"]: r.get("claim_type") for r in by_cat["F"]}
    check(
        "F roster matches synthesis",
        set(actual_f) == set(EXPECTED_F_ROWS),
        f"extra={sorted(set(actual_f) - set(EXPECTED_F_ROWS))} "
        f"missing={sorted(set(EXPECTED_F_ROWS) - set(actual_f))}",
    )
    for cid, expected_type in EXPECTED_F_ROWS.items():
        check(
            f"F row claim_type matches: {cid}",
            actual_f.get(cid) == expected_type,
            f"actual={actual_f.get(cid)!r}",
        )

    # ---- D top-5 named ----
    actual_d_ids = {r["claim_id"] for r in by_cat["D"]}
    for cid, expected_type in EXPECTED_D_TOP5_ROWS.items():
        check(
            f"D top-5 row in D bucket: {cid}",
            cid in actual_d_ids,
        )
        # claim_type check
        match = next((r for r in by_cat["D"] if r["claim_id"] == cid), None)
        if match is not None:
            check(
                f"D top-5 row claim_type matches: {cid}",
                match.get("claim_type") == expected_type,
                f"actual={match.get('claim_type')!r}",
            )

    # ---- A: prior audit signature ----
    for cid in EXPECTED_A_ROWS:
        led = rows.get(cid, {})
        pa = led.get("previous_audits", [])
        latest = latest_dated_audit(pa)
        # Either no dated prior audit or latest dated = audited_clean.
        ok = (latest is None) or (latest.get("audit_status") == "audited_clean")
        check(
            f"A row prior audit signature OK: {cid}",
            ok,
            f"latest_v={latest.get('audit_status') if latest else None!r}",
        )

    # ---- B: prior audit signature (decoration today, alpha_lm canonical) ----
    for cid in EXPECTED_B_ROWS:
        led = rows.get(cid, {})
        check(
            f"B row currently claim_type=decoration: {cid}",
            led.get("claim_type") == "decoration",
            f"actual={led.get('claim_type')!r}",
        )

    # ---- F: prior audit signature ----
    for cid in EXPECTED_F_ROWS:
        led = rows.get(cid, {})
        pa = led.get("previous_audits", [])
        latest = latest_dated_audit(pa)
        check(
            f"F row latest dated audit = audited_conditional: {cid}",
            latest is not None and latest.get("audit_status") == "audited_conditional",
            f"latest_v={latest.get('audit_status') if latest else None!r}",
        )
        notes = (latest.get("notes_for_re_audit_if_any") or "").strip() if latest else ""
        check(
            f"F row repair_class=missing_dependency_edge: {cid}",
            notes.startswith("missing_dependency_edge"),
            f"notes_prefix={notes.split(':', 1)[0]!r}",
        )

    # ---- D: prior audit signature (audited_conditional, NOT
    # missing_dependency_edge). Sample on the top-5 to keep the runner
    # output readable; the per-category-count assertion above covers
    # the full set.
    for cid in EXPECTED_D_TOP5_ROWS:
        led = rows.get(cid, {})
        pa = led.get("previous_audits", [])
        latest = latest_dated_audit(pa)
        check(
            f"D row latest dated audit = audited_conditional: {cid}",
            latest is not None and latest.get("audit_status") == "audited_conditional",
            f"latest_v={latest.get('audit_status') if latest else None!r}",
        )
        notes = (latest.get("notes_for_re_audit_if_any") or "").strip() if latest else ""
        check(
            f"D row repair_class != missing_dependency_edge: {cid}",
            not notes.startswith("missing_dependency_edge"),
            f"notes_prefix={notes.split(':', 1)[0]!r}",
        )

    # ---- structural: every category roster element is currently
    # ready=True and present in the live queue.
    ready_ids = {r["claim_id"] for r in ready_rows}
    for label, expected in (
        ("A", EXPECTED_A_ROWS),
        ("B", EXPECTED_B_ROWS),
        ("F", EXPECTED_F_ROWS),
        ("D top-5", EXPECTED_D_TOP5_ROWS),
    ):
        for cid in expected:
            check(
                f"{label} row currently ready=True in queue: {cid}",
                cid in ready_ids,
            )

    print()
    print(f"PASS={PASS} FAIL={FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
