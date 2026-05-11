# Decoherence is Action-Independent

**Date:** 2026-04-04
**Status:** Confirmed on the frozen 3D `1/L^2` replay — exact numerical identity across actions
**Claim type:** bounded_theorem

**Audit-conditional perimeter (2026-05-10):**
The current generated audit ledger records this row `audited_conditional` with
`auditor_confidence = high`, `chain_closes = false`, and `claim_type =
bounded_theorem`. The audit chain-closure explanation is exact: "The
packet does not provide retained definitions of the two action laws
or the imported propagation harness needed to verify the zero-field
reduction. The runner also has no completed stdout, but the timeout
is not used as the terminal reason." This rigorization edit only
sharpens the boundary of the conditional perimeter; nothing here
promotes audit status. The supported content of this note is the
exact-identity table at h ∈ {1.0, 0.5, 0.25} reproduced verbatim from
the frozen 2026-04-04 log; the broader interpretation in §"Why" and
§"Implications" depends on the imported valley-linear and spent-delay
action definitions plus the propagation harness, which are not in the
restricted packet. The frozen log
[`logs/2026-04-04-decoherence-action-independence.txt`](../logs/2026-04-04-decoherence-action-independence.txt)
is the load-bearing artifact for the table; the runner
[`scripts/decoherence_action_independence.py`](../scripts/decoherence_action_independence.py)
is the registered re-derivation harness.

## Finding

On the frozen 3D `1/L^2` lattice replay, the decoherence observables
(d_TV, MI, CL bath purity, S_norm) are EXACTLY IDENTICAL for the
valley-linear and spent-delay actions at every tested lattice spacing.

Primary artifact:

- [`scripts/decoherence_action_independence.py`](/Users/jonreilly/Projects/Physics/scripts/decoherence_action_independence.py)
- [`logs/2026-04-04-decoherence-action-independence.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-04-decoherence-action-independence.txt)

| h | d_TV (both) | MI (both) | Decoh (both) | S_norm (both) |
|---|-------------|-----------|--------------|---------------|
| 1.0 | 0.627 | 0.414 | 30.2% | 0.390 |
| 0.5 | 0.786 | 0.588 | 49.4% | 0.701 |
| 0.25 | 0.830 | 0.647 | 49.9% | 0.807 |

## Why

The decoherence test uses zero field (no mass). Both actions reduce
to S = L × const at zero field. The amplitude magnitude at each node
depends only on the kernel (1/L^2) and the angular weight (exp(-βθ²)),
which are shared by both actions. The action only changes the PHASE
(via exp(ikS)), and the CL bath measurement depends on amplitude
MAGNITUDES at intermediate layers.

## Implications

The model cleanly separates:
- **Gravity**: action-dependent (valley-linear → Newtonian, spent-delay → sqrt)
- **Decoherence**: geometry-dependent (lattice structure + slits)
- **Born rule**: linearity-dependent (both actions are linear)

This means the action can be optimized for gravity without affecting
decoherence on the tested family. The valley-linear action gives Newtonian
gravity AND the same decoherence as spent-delay here, so there is no
gravity/decoherence trade-off on the frozen replay.

## Convergence

The decoherence converges as h → 0 on the tested family:
- d_TV: 0.63 → 0.79 → 0.83 (approaching 1.0)
- MI: 0.41 → 0.59 → 0.65 (approaching ~0.7?)
- Decoherence: 30% → 49% → 50% (converged to 50%)
- S_norm: 0.39 → 0.70 → 0.81 (approaching 1.0)

This convergence is a property of the LATTICE, not the action, on the
frozen 3D `1/L^2` branch.
