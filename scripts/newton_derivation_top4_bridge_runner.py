#!/usr/bin/env python3
"""Newton-derivation Principle-3 bridge runner on the top4 multistage compact object.

Scope
-----
This runner is the support artifact for ``docs/NEWTON_DERIVATION_TOP4_BRIDGE_NOTE.md``
and the open gate ``newton_derivation_note``. It re-extracts, from a *single*
fresh run of the audit-clean top4 multistage probe baseline case, the three
measurements that the Newton derivation chain relies on for Principle 3
("if the inertial quantity of a persistent pattern is an extensive quantity
attached to the same composition law as the field-source parameter ``s``,
then ``m proportional to s``"):

  1. ``stage_alpha``: the F~M exponent fitted across SOURCE_STRENGTHS on the
     multistage compact object. Principle 3 requires this to equal 1.
  2. ``max_kappa_drift``: the maximum stage-to-stage relative drift of the
     response coefficient ``kappa = delta / s``. Principle 3 requires this
     to be small (the same ``s`` controls the response across stages).
  3. ``stage_mean_overlap``: the mean update overlap of the persistent
     pattern. Principle 3 requires the pattern to remain a recognisable
     compact object across the multistage chain.

What this runner does *not* claim
---------------------------------
It does not claim a new persistent-pattern equivalence-principle theorem,
and it does not modify the audit-clean ``persistent_object_top4_multistage_transfer_sweep``
runner (which is still the primary admissibility certificate for the
top4 floor). It only re-extracts the Principle-3 numbers from the same
machinery so that the Newton-derivation bridge note has a *registered*
runner that names and prints exactly the measurements its conditional
theorem cites.

Audit boundary
--------------
* Same fixed family as the audit-clean top4 sweep: ``h=0.25``, ``blend=0.25``,
  ``top_keep=4``, three updates per segment, three chained segments,
  baseline source cluster ``(W=3, L=6, source_z=2.0)``.
* Single ``baseline`` case only. The full widened-pocket sweep stays in
  the existing audit-clean runner; this runner is intentionally narrower.
* Outputs are PASS/FAIL on Principle-3 thresholds only (``alpha in [0.95, 1.05]``,
  ``max_kappa_drift <= 0.10``, ``stage_mean_overlap >= 0.90``); no new
  equivalence-principle test, no two-body momentum claim, no inertial-mass
  closure.
"""

from __future__ import annotations


# Light-weight extraction runner — single ``baseline`` case from the
# top4 multistage probe. Should run well under the default 120-s ceiling,
# but bumping to 300 s for safety under audit-lane concurrency contention.
AUDIT_TIMEOUT_SEC = 300

import argparse
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.persistent_object_top3_multistage_probe import Case, _run_case  # noqa: E402
from scripts.persistent_object_compact_inertial_probe import (  # noqa: E402
    KAPPA_DRIFT_THRESHOLD,
)
from scripts.persistent_object_compact_shared import (  # noqa: E402
    ALPHA_BAND,
    OVERLAP_THRESHOLD,
)


TOP_KEEP = 4
BASELINE_CASE = Case("baseline", 6, 3, 2.0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--top-keep",
        type=int,
        default=TOP_KEEP,
        help="Compact object width to retain per update (default 4, matching the audit-clean top4 floor).",
    )
    args = parser.parse_args()

    t0 = time.time()
    print("=" * 100)
    print("NEWTON DERIVATION TOP4 BRIDGE RUNNER")
    print("  Principle-3 extensivity bridge on the audit-clean top4 multistage compact object")
    print("=" * 100)
    print(f"top_keep={args.top_keep}, case={BASELINE_CASE.label} (W={BASELINE_CASE.phys_w}, "
          f"L={BASELINE_CASE.phys_l}, source_z={BASELINE_CASE.source_z})")
    print(
        f"thresholds: alpha in [{ALPHA_BAND[0]:.2f}, {ALPHA_BAND[1]:.2f}], "
        f"max_kappa_drift <= {KAPPA_DRIFT_THRESHOLD:.2f}, mean_overlap >= {OVERLAP_THRESHOLD:.2f}"
    )
    print()

    row = _run_case(BASELINE_CASE, args.top_keep)

    overlap_str = "[" + ",".join(f"{val:.3f}" for val in row.stage_mean_overlap) + "]"
    alpha_str = "[" + ",".join(
        f"{alpha:.2f}" if alpha is not None else "n/a" for alpha in row.stage_alpha
    ) + "]"
    kappa_str = "[" + ",".join(f"{val:.6e}" for val in row.stage_kappa) + "]"

    print("PRINCIPLE-3 MEASUREMENTS")
    print(f"  stage_mean_overlap   = {overlap_str}")
    print(f"  stage_alpha          = {alpha_str}")
    print(f"  stage_kappa          = {kappa_str}")
    print(f"  max_kappa_drift      = {row.max_kappa_drift:.3%}")
    print()

    overlap_pass = all(val >= OVERLAP_THRESHOLD for val in row.stage_mean_overlap)
    alpha_pass = all(
        alpha is not None and ALPHA_BAND[0] <= alpha <= ALPHA_BAND[1]
        for alpha in row.stage_alpha
    )
    drift_pass = row.max_kappa_drift <= KAPPA_DRIFT_THRESHOLD

    print("PRINCIPLE-3 GATES")
    print(f"  PERSISTENCE  (mean_overlap >= {OVERLAP_THRESHOLD:.2f})           : "
          f"{'PASS' if overlap_pass else 'FAIL'}")
    print(f"  EXTENSIVITY  (alpha in [{ALPHA_BAND[0]:.2f}, {ALPHA_BAND[1]:.2f}])      : "
          f"{'PASS' if alpha_pass else 'FAIL'}")
    print(f"  STABILITY    (max_kappa_drift <= {KAPPA_DRIFT_THRESHOLD:.2f})        : "
          f"{'PASS' if drift_pass else 'FAIL'}")
    print()

    bridge_admissible = overlap_pass and alpha_pass and drift_pass

    print("SAFE READ")
    if bridge_admissible:
        print(
            "  - On the audit-clean top4 multistage baseline case, the persistent compact"
        )
        print(
            "    object satisfies the Principle-3 extensivity premise of the Newton-derivation"
        )
        print(
            "    chain operationally: alpha = 1, the response coefficient is stage-stable,"
        )
        print(
            "    and the same source-strength s is the only scalar parameter."
        )
        print(
            "  - This is a *bridge* result, not a new persistent-pattern equivalence-principle"
        )
        print(
            "    theorem. The remaining open question is the equivalence-principle test for"
        )
        print(
            "    different persistent compact-object widths under an external field, which"
        )
        print(
            "    matter_inertial_closure_note shows fails for free Gaussian packets."
        )
    else:
        print(
            "  - The Principle-3 extensivity bridge does not pass on the baseline case."
        )
        print(
            "  - The Newton derivation gate remains open and the support notes should not"
        )
        print(
            "    cite this run as evidence for Principle 3."
        )

    print()
    print(f"BRIDGE_ADMISSIBLE = {bridge_admissible}")
    print(f"Total runtime: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
