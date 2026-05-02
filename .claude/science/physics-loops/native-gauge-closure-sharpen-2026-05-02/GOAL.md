# Goal: Sharpen native_gauge_closure_note bounded scope honestly

Iteration 4 of the 3plus1d-native-closure campaign. Iteration 1 (PR #392)
landed the lattice Wess-Zumino theorem closing admission (i) of
`anomaly_forces_time_theorem`, flipping that row to `positive_theorem`.

But `anomaly_forces_time_theorem` is not yet `effective_status: retained`
because dependency closure still needs the load-bearing inputs to be
retained-clean. One named blocker: `NATIVE_GAUGE_CLOSURE_NOTE` is
`retained_bounded`, used at the WZ note's W4 step ("the gauge sector on
the framework is exactly `SU(2)_L × SU(3)_C × U(1)_Y`-like").

## Two routes

**Route A — promote claim_type to positive_theorem.**
Requires upstream deps (graph_first_selector_derivation_note,
graph_first_su3_integration_note) to also be promoted to positive_theorem.
But both deps were just re-audited 2026-05-02 with claim_type_provenance
=`audited` (intentional bounded), confirmed cross-confirmation. The bounded
scope is genuine: the abelian factor in those notes is explicitly described
as "hypercharge-like" because the anomaly-complete U(1)_Y identification
belongs to a separate completion theorem. This is honest physics, not
inherited overcaution.

Route A would require either:
- a new positive_theorem note that anomaly-completes U(1)_Y on the
  bounded abelian eigenvalue surface (huge effort, OUT of scope here)
- splitting the deps' notes into separate positive theorem (algebra) and
  bounded support (physical-identification) parts (large rewrite, OUT of
  scope here)

**Route B (chosen) — document scope-intrinsic boundary cleanly.**
Add explicit marker to NATIVE_GAUGE_CLOSURE_NOTE that the bounded
scope is intrinsic and not deferred. Verify the WZ theorem's W4 use of
"U(1)_Y-like" gauge content is satisfied at the bounded scope (it is —
W4 only needs the gauge content existing, not anomaly-complete U(1)_Y;
that admission is internalized via Step 2's nu_R = 0 anomaly arithmetic
in the WZ note proper).

## Net effect

The WZ theorem stays `bounded_theorem` because of its own admitted bridges
(opposite-chirality singlet completion, Clifford-volume chirality
uniqueness, ultrahyperbolic obstruction). NATIVE_GAUGE_CLOSURE staying
`retained_bounded` is the right scope; it supplies the gauge content the
WZ theorem needs. The whole anomaly_forces_time ratification path remains
as a `bounded_theorem` end-state until upstream U(1)_Y anomaly-completion
becomes the next campaign target.

## Honest status

This iteration is a documentation tightening, not a claim_type promotion.
The narrow PR records the structural finding that the bounded scope is
genuine and that the campaign next-blocker for retained_bounded → retained
on this row is anomaly-complete U(1)_Y identification, which is itself a
separate audit lane.
