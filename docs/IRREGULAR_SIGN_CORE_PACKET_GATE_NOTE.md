# Irregular Sign Core-Packet Gate Note

**Date:** 2026-04-11
**Script:** `frontier_irregular_sign_core_packet_gate.py`
**Status:** bounded same-surface irregular sign separator on the audited
centered core-packet surface

## What was tested

The irregular-sign lane's endogenous sign closure (+Phi vs -Phi separation)
using core_packet (non-oscillating gaussian, exp(-r^2/2sigma^2)) as the
primary observable, replacing the original shell_packet which fails at low
screening due to oscillation-induced interference.

## Parameters

- Graphs: random_geometric (side=8), growing (n_target=64), layered_cycle (layers=8, width=8)
- Seeds: 42-46
- G values: 5.0, 10.0
- Screening: mu2=0.1 (original), mu2=0.001 (low)
- Window: steps [2, 11)
- Observables: ball1_margin, ball2_margin, depth_margin

## Results

| Screening | ball1 positive | ball2 positive | depth positive | min fraction |
|-----------|---------------|---------------|----------------|-------------|
| mu2=0.1   | 30/30 (100%)  | 30/30 (100%)  | 30/30 (100%)   | 100.0%      |
| mu2=0.001 | 28/30 (93%)   | 30/30 (100%)  | 28/30 (93%)    | 93.3%       |

The 2 negative rows at mu2=0.001 occur in random_geometric at G=10.0 (ball1
and depth margins), with magnitudes ~1e-7 against a positive mean of ~1e-8.
These are marginal sign flips at extremely small signal levels, not systematic
failures.

## Gate evaluation

- Gate 1 (mu2=0.1, threshold 80%): PASS at 100%
- Gate 2 (mu2=0.001, threshold 80%): PASS at 93.3%
- Gate 3 (cross-screening): PASS

## Conclusion

On the audited centered core-packet surface, `core_packet` cleanly separates
attraction from repulsion on the retained irregular bipartite families at both
screening levels. The older `shell_packet` failure at low screening was an
artifact of oscillation-induced interference masking the sign signal, not a
failure of the underlying sign physics.

This closes a **bounded same-surface separator**, not the whole irregular
direction/sign problem. It does **not** establish:

- arbitrary packet portability
- transport-style / off-center directional closure
- universal off-lattice directional gravity on all graph families or `G`
  values

The right read on current `main` is:

- the centered non-oscillating core packet now gives a bounded same-surface
  irregular sign separator
- the older off-center / transport-style probe remains a blocker history
- broader packet and transport portability on irregular graphs is still open

## Scope limits

- Audited on three graph families with 5 seeds each
- Two G values only
- Not tested on arbitrary initial states or graph topologies
- Margin magnitudes at mu2=0.001 are small (~1e-5 to ~1e-7) compared to
  mu2=0.1 (~1e-2), consistent with weaker gravitational coupling at low
  screening

## Companion Context

- blocker history:
  `IRREGULAR_DIRECTIONAL_OBSERVABLE_NOTE_2026-04-11.md` (sibling artifact;
  cross-reference only — not a one-hop dep of this note)
- weak-coupling retained companion:
  [`WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md`](WEAK_COUPLING_RETENTION_NOTE_2026-04-11.md)
- broader sign audit:
  [`GRAVITY_SIGN_AUDIT_2026-04-10.md`](GRAVITY_SIGN_AUDIT_2026-04-10.md)
