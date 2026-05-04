#!/usr/bin/env python3
"""Summarize auditor reliability across the ledger.

The audit lane has accumulated 800+ audited rows across multiple auditor
families. This script extracts an auditor-reliability signal from the
existing data — without re-running any audits — by counting:

  - per auditor_family: total audits applied, breakdown by verdict
  - per auditor_family: cross_confirmation outcomes (confirmed,
    third_confirmed_first / _second, three_way_disagreement)
  - per auditor_family: rate of being overturned by a third auditor
    (third audit sided with the OTHER auditor)
  - judicial third-pass tiebreaker counts
  - rows where the auditor was overturned by an invalidate-and-reaudit
    path (an entry in previous_audits with a different verdict than current)

The output is data/auditor_reliability.json, which is informational only.
The audit lane does not auto-de-rank auditors — humans set policy. But
this surfaces the data needed to do so.

Pipeline order: AFTER compute_audit_queue.py and before audit_lint.py
(so lint can optionally consume the summary). It does not write into the
ledger itself.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
OUTPUT_PATH = DATA_DIR / "auditor_reliability.json"


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    # Per-family stats
    per_family: dict[str, dict] = defaultdict(
        lambda: {
            "total_audits": 0,
            "verdict_counts": Counter(),
            "criticality_counts": Counter(),
            "cross_confirmation_outcomes": Counter(),
            "overturned_by_third": 0,
            "ratified_by_third": 0,
            "judicial_third_pass_count": 0,
            "weak_clean_attempts_blocked": 0,
            "audits_with_runner_class": Counter(),
        }
    )
    family_pair_disagreements: Counter = Counter()

    for cid, row in rows.items():
        fam = row.get("auditor_family")
        verdict = row.get("audit_status")
        if not fam or verdict in (None, "unaudited", "audit_in_progress"):
            continue
        bucket = per_family[fam]
        bucket["total_audits"] += 1
        bucket["verdict_counts"][verdict] += 1
        bucket["criticality_counts"][row.get("criticality") or "leaf"] += 1
        if row.get("load_bearing_step_class"):
            bucket["audits_with_runner_class"][row["load_bearing_step_class"]] += 1

        cc = row.get("cross_confirmation") or {}
        if not isinstance(cc, dict):
            continue
        cc_status = cc.get("status")
        if cc_status:
            bucket["cross_confirmation_outcomes"][cc_status] += 1

        first = cc.get("first_audit") or {}
        second = cc.get("second_audit") or {}
        third = cc.get("third_audit") or {}
        if cc_status in ("third_confirmed_first", "third_confirmed_second"):
            winning_side = "first" if cc_status == "third_confirmed_first" else "second"
            losing_side = "second" if winning_side == "first" else "first"
            winning_audit = first if winning_side == "first" else second
            losing_audit = second if winning_side == "first" else first
            wf = winning_audit.get("auditor_family")
            lf = losing_audit.get("auditor_family")
            if wf:
                per_family[wf]["ratified_by_third"] += 1
            if lf:
                per_family[lf]["overturned_by_third"] += 1
            if wf and lf:
                family_pair_disagreements[(lf, wf)] += 1
            if third.get("auditor_family"):
                per_family[third["auditor_family"]]["judicial_third_pass_count"] += 1
        elif cc_status in ("three_way_disagreement", "disagreement"):
            for side, audit in (("first", first), ("second", second), ("third", third)):
                f = audit.get("auditor_family")
                if f:
                    per_family[f]["overturned_by_third"] += (
                        1 if cc_status == "three_way_disagreement" else 0
                    )

        # Internal-overturn detection: a previous_audits entry with a
        # different verdict than the current row.
        for prior in row.get("previous_audits", []) or []:
            prior_verdict = prior.get("audit_status")
            prior_fam = prior.get("auditor_family")
            if (
                prior_verdict
                and prior_fam
                and prior_verdict != verdict
                and prior_verdict not in (None, "unaudited", "audit_in_progress")
            ):
                per_family[prior_fam].setdefault("verdict_changed_after_re_audit", 0)
                per_family[prior_fam]["verdict_changed_after_re_audit"] += 1

    # Convert Counters to plain dicts for JSON
    summary = {}
    for fam, bucket in per_family.items():
        out = dict(bucket)
        out["verdict_counts"] = dict(bucket["verdict_counts"])
        out["criticality_counts"] = dict(bucket["criticality_counts"])
        out["cross_confirmation_outcomes"] = dict(bucket["cross_confirmation_outcomes"])
        out["audits_with_runner_class"] = dict(bucket["audits_with_runner_class"])
        if bucket["total_audits"]:
            denom = max(1, bucket["overturned_by_third"] + bucket["ratified_by_third"])
            out["third_pass_overturn_rate"] = round(
                bucket["overturned_by_third"] / denom, 3
            )
        summary[fam] = out

    pair_data = [
        {"loser": loser, "winner": winner, "count": n}
        for (loser, winner), n in family_pair_disagreements.most_common()
    ]

    output = {
        "policy": "auditor_reliability_v1",
        "policy_summary": (
            "Per-auditor-family verdict and cross-confirmation aggregate. "
            "Informational only — humans set audit-lane policy. Surfaced "
            "fields: total_audits, verdict_counts, cross_confirmation_outcomes, "
            "overturned_by_third (third auditor sided with other side), "
            "ratified_by_third, third_pass_overturn_rate."
        ),
        "auditor_family_summary": summary,
        "family_pair_disagreements": pair_data,
        "totals": {
            "auditor_families_observed": len(summary),
            "total_audits_recorded": sum(b["total_audits"] for b in summary.values()),
            "total_third_pass_decisions": sum(
                b.get("ratified_by_third", 0) + b.get("overturned_by_third", 0)
                for b in summary.values()
            ),
        },
    }

    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  auditor families observed: {output['totals']['auditor_families_observed']}")
    print(f"  total audits: {output['totals']['total_audits_recorded']}")
    print(f"  total third-pass decisions: {output['totals']['total_third_pass_decisions']}")
    if pair_data:
        print(f"  top family-pair disagreements:")
        for pair in pair_data[:5]:
            print(f"    {pair['loser']} -> {pair['winner']}: {pair['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
