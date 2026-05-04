#!/usr/bin/env python3
"""Summarize auditor reliability across the ledger.

The audit lane has accumulated 800+ audited rows across multiple auditor
families. This script extracts auditor-reliability signals from the
existing data — without re-running any audits.

## How to read these metrics

Not all metrics are equally informative. Two of them are subject to
selection bias and need a careful read; two are unbiased and worth
acting on.

### 1. third_pass_overturn_rate (selection-biased — read with care)

What it measures: of the third-pass decisions where this auditor was a
participant, the fraction in which the third auditor sided with the
OTHER side.

Why selection bias matters: a third auditor is invoked ONLY when the
first two auditors disagreed. Disagreements arise on genuinely
ambiguous cases — the cases where two cold competent reviewers can read
the same evidence and reach different conclusions. In that population
the prior on "side A is correct" is ~50%, so a competent third auditor
will side against any given participant ~50% of the time.

A 50% overturn rate is therefore the EXPECTED value for a competent
auditor, not a problem signal. Only meaningful deviations (say, ≥70%
with N large enough to be statistically distinguishable from 50%)
suggest miscalibration. Even then, the direction matters more than the
magnitude — see `bias_direction_breakdown` below.

### 2. cross_confirmation_agreement_rate (unbiased — primary signal)

What it measures: among completed cross-confirmation pairs the auditor
participated in, the fraction where the first and second auditor
verdicts matched (so no third was needed).

Why unbiased: this is computed over EVERY cross-confirmed row the
auditor touched, not just disputed ones. High agreement rate = this
auditor reaches the same conclusion as another independent auditor on
typical cases. Low rate = this auditor's first-look judgment routinely
diverges from peers.

### 3. bias_direction_breakdown (unbiased — directional signal)

What it measures: when this auditor's verdict was overturned in a
third-pass decision, was their verdict cleaner or stricter than the
winning side?

  - more_lenient: auditor said "clean" / "renaming"; winner said "conditional" / "failed"
  - more_strict:  auditor said "conditional" / "failed"; winner said "clean" / "renaming"
  - same_severity: different verdict label, same severity tier

If a competent auditor's overturns split ~50/50 between more_lenient
and more_strict, that is consistent with random variation on hard
calls. A persistent skew toward more_lenient is a "rubber-stamp"
signal; persistent more_strict is a "gatekeeping" signal. This is the
metric to watch for actual miscalibration.

### 4. verdict_changed_after_re_audit (unbiased — independent overturn)

What it measures: count of rows where this auditor's prior verdict
sits in `previous_audits` with a different verdict than the row's
current audit_status. Captures cases where a re-audit (e.g. after note
hash drift, or a fresh-look pass) reached a different conclusion than
the auditor did originally.

Independent of cross-confirmation disputes — this is a real "did the
auditor miss something" signal.

## Pipeline placement

Pipeline order: AFTER compute_audit_queue.py and before audit_lint.py.
It does not write into the ledger itself. Output is informational only —
humans set audit-lane policy.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "docs" / "audit" / "data"
LEDGER_PATH = DATA_DIR / "audit_ledger.json"
OUTPUT_PATH = DATA_DIR / "auditor_reliability.json"

# Verdict severity rank for bias_direction analysis.
# Higher = more skeptical / restrictive verdict on the same evidence.
# audited_renaming and audited_decoration are tied at the same tier
# because both refuse to ratify a derivation but differ on why.
VERDICT_SEVERITY = {
    "audited_clean": 0,
    "audited_renaming": 1,
    "audited_decoration": 1,
    "audited_numerical_match": 2,
    "audited_conditional": 3,
    "audited_failed": 4,
}


def severity_compare(loser_verdict: str | None, winner_verdict: str | None) -> str:
    """Classify how the loser's verdict differs from the winner's verdict."""
    lr = VERDICT_SEVERITY.get(loser_verdict or "")
    wr = VERDICT_SEVERITY.get(winner_verdict or "")
    if lr is None or wr is None:
        return "unknown_severity"
    if lr < wr:
        return "more_lenient"
    if lr > wr:
        return "more_strict"
    return "same_severity"


def participant_families(*audits: dict) -> list[str]:
    """Return unique auditor families in first-seen order."""
    seen: dict[str, None] = {}
    for audit in audits:
        fam = audit.get("auditor_family")
        if fam:
            seen.setdefault(fam, None)
    return list(seen)


def main() -> int:
    if not LEDGER_PATH.exists():
        raise SystemExit("audit_ledger.json missing")
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows = ledger.get("rows", {})

    def empty_bucket():
        return {
            "total_audits": 0,
            "verdict_counts": Counter(),
            "criticality_counts": Counter(),
            "cross_confirmation_outcomes": Counter(),
            "overturned_by_third": 0,
            "ratified_by_third": 0,
            "judicial_third_pass_count": 0,
            "audits_with_runner_class": Counter(),
            "verdict_changed_after_re_audit": 0,
            # Unbiased signals
            "cross_confirmation_pairs_seen": 0,
            "cross_confirmation_pairs_agreed_first_try": 0,
            "bias_direction_breakdown": Counter(),
        }

    per_family: dict[str, dict] = defaultdict(empty_bucket)
    family_pair_disagreements: Counter = Counter()
    overall_completed_pairs = 0
    overall_agreed_pairs = 0

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
        first = cc.get("first_audit") or {}
        second = cc.get("second_audit") or {}
        third = cc.get("third_audit") or {}

        # Unbiased agreement-rate accounting: count every completed
        # cross-confirmation pair this auditor participated in, and
        # whether the first/second pair agreed without needing a third.
        completed_statuses = {
            "confirmed",
            "third_confirmed_first",
            "third_confirmed_second",
            "three_way_disagreement",
            "disagreement_irresolvable",
        }
        participants = participant_families(first, second)
        if cc_status:
            for side_fam in participants or [fam]:
                per_family[side_fam]["cross_confirmation_outcomes"][cc_status] += 1
        if cc_status in completed_statuses:
            overall_completed_pairs += 1
            if cc_status == "confirmed":
                overall_agreed_pairs += 1
            for side_fam in participants:
                per_family[side_fam]["cross_confirmation_pairs_seen"] += 1
                if cc_status == "confirmed":
                    per_family[side_fam]["cross_confirmation_pairs_agreed_first_try"] += 1

        if cc_status in ("third_confirmed_first", "third_confirmed_second"):
            winning_side = "first" if cc_status == "third_confirmed_first" else "second"
            winning_audit = first if winning_side == "first" else second
            losing_audit = second if winning_side == "first" else first
            wf = winning_audit.get("auditor_family")
            lf = losing_audit.get("auditor_family")
            if wf:
                per_family[wf]["ratified_by_third"] += 1
            if lf:
                per_family[lf]["overturned_by_third"] += 1
                # Bias direction: when the loser was overturned, was
                # their verdict more lenient or more strict than the
                # winner's?
                direction = severity_compare(
                    losing_audit.get("verdict"),
                    winning_audit.get("verdict"),
                )
                per_family[lf]["bias_direction_breakdown"][direction] += 1
            if wf and lf:
                family_pair_disagreements[(lf, wf)] += 1
            if third.get("auditor_family"):
                per_family[third["auditor_family"]]["judicial_third_pass_count"] += 1

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
                per_family[prior_fam]["verdict_changed_after_re_audit"] += 1

    # Convert Counters to plain dicts for JSON
    summary = {}
    for fam, bucket in per_family.items():
        out = dict(bucket)
        out["verdict_counts"] = dict(bucket["verdict_counts"])
        out["criticality_counts"] = dict(bucket["criticality_counts"])
        out["cross_confirmation_outcomes"] = dict(bucket["cross_confirmation_outcomes"])
        out["audits_with_runner_class"] = dict(bucket["audits_with_runner_class"])
        out["bias_direction_breakdown"] = dict(bucket["bias_direction_breakdown"])

        # Selection-biased metric: report it but flag the caveat.
        third_pass_decisions = bucket["overturned_by_third"] + bucket["ratified_by_third"]
        if third_pass_decisions:
            out["third_pass_overturn_rate"] = round(
                bucket["overturned_by_third"] / third_pass_decisions, 3
            )
            out["third_pass_decisions_n"] = third_pass_decisions
            out["third_pass_overturn_rate_caveat"] = (
                "Selection-biased: third auditor only runs on disputed cases. "
                "Expected value for a competent auditor is ~0.5. "
                "See script docstring."
            )

        # Unbiased agreement rate.
        pairs_seen = bucket["cross_confirmation_pairs_seen"]
        if pairs_seen:
            out["cross_confirmation_agreement_rate"] = round(
                bucket["cross_confirmation_pairs_agreed_first_try"] / pairs_seen, 3
            )
            out["cross_confirmation_pairs_n"] = pairs_seen

        summary[fam] = out

    pair_data = [
        {"loser": loser, "winner": winner, "count": n}
        for (loser, winner), n in family_pair_disagreements.most_common()
    ]

    # Overall agreement rate across cross-confirmation rows (informational).
    # This stays row-based, while per-family counters above count each
    # participating family once per completed pair.
    overall_pairs = overall_completed_pairs
    overall_agreed = overall_agreed_pairs
    overall_agreement_rate = (
        round(overall_agreed / overall_pairs, 3) if overall_pairs else None
    )

    output = {
        "policy": "auditor_reliability_v2",
        "policy_summary": (
            "Per-auditor-family verdict and cross-confirmation aggregate. "
            "Informational only — humans set audit-lane policy. "
            "PRIMARY SIGNALS (unbiased): "
            "cross_confirmation_agreement_rate (rate at which this auditor's "
            "first-look verdict matched the other independent auditor without "
            "needing a third), "
            "bias_direction_breakdown (when overturned, was the auditor "
            "more_lenient or more_strict?), "
            "verdict_changed_after_re_audit (independent re-audit produced a "
            "different verdict). "
            "DIAGNOSTIC ONLY (selection-biased): third_pass_overturn_rate is "
            "the fraction of disputed cases where the auditor was on the "
            "losing side; expected value for a competent auditor is ~0.5 "
            "because disputes arise on genuinely ambiguous cases. See script "
            "docstring for the full read-with-care guide."
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
            "total_cross_confirmation_pairs": overall_pairs,
            "total_cross_confirmation_family_participations": sum(
                b.get("cross_confirmation_pairs_seen", 0) for b in summary.values()
            ),
            "overall_agreement_rate": overall_agreement_rate,
        },
    }

    OUTPUT_PATH.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  auditor families observed: {output['totals']['auditor_families_observed']}")
    print(f"  total audits: {output['totals']['total_audits_recorded']}")
    print(f"  total third-pass decisions: {output['totals']['total_third_pass_decisions']}")
    print(f"  total cross-confirmation pairs: {output['totals']['total_cross_confirmation_pairs']}")
    if overall_agreement_rate is not None:
        print(f"  overall first-look agreement rate: {overall_agreement_rate}")
    if pair_data:
        print(f"  top family-pair disagreements:")
        for pair in pair_data[:5]:
            print(f"    {pair['loser']} -> {pair['winner']}: {pair['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
