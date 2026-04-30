# Atomic Lane 2 Alpha(0) Running Bridge Boundary

**Date:** 2026-04-29
**Status:** no-go / conditional-support boundary for the current
`alpha(0)` bridge route; no Rydberg or hydrogen closure claim.
**Loop:** `.claude/science/physics-loops/impact-campaign-20260429/`
**Runner:** `scripts/frontier_atomic_lane2_alpha0_running_bridge_boundary.py`

```yaml
actual_current_surface_status: no-go
conditional_surface_status: conditional-support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "alpha_EM(M_Z) does not determine alpha(0) without charged-threshold, hadronic, and scheme-matched QED-running inputs"
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 1. Question

Lane 2 needs the atomic Coulomb coupling `alpha(0)` before the existing
hydrogen scaffold can become a framework-derived Rydberg calculation.

The repo already has a high-energy electroweak-scale value:

```text
1 / alpha_EM(M_Z) = 127.67
```

This block asks whether current repo content can transport that value to
`alpha(0)` without new threshold or low-energy inputs.

## 2. Boundary Theorem

**Theorem.** On the current repo surface, `alpha_EM(M_Z)` alone does not
determine the atomic Coulomb coupling `alpha(0)`.

The QED-running route is the right bridge type, but it remains conditional on
threshold masses, scheme choices, and hadronic vacuum-polarization treatment.

## 3. Proof

The hydrogen ground-state formula is:

```text
E_1 = -m_e alpha(0)^2 / 2
```

Using `alpha_EM(M_Z)` directly gives the known firewall failure:

```text
1 / alpha_EM(M_Z) = 127.67
1 / alpha(0)      = 137.035999084  (standard comparator)
```

The inverse-coupling gap is about `9.37`, and the direct substitution shifts
the Rydberg energy by more than ten percent. The gap is not notation; it is a
low-energy transport problem.

At one-loop, even the lepton part of the transport has threshold dependence:

```text
Delta(1/alpha) = (2 / 3 pi) sum_f log(M_Z / m_f)
```

The charged thresholds are load-bearing, and the lepton-only approximation
does not close the full gap to the atomic comparator. A hadronic or equivalent
low-energy vacuum-polarization treatment remains needed.

Therefore Lane 2 cannot close `alpha(0)` from the current high-energy value
alone.

## 4. Runner Witness

The runner checks:

- Lane 2 authority surfaces name `alpha(0)` / QED running as a required gate;
- direct `alpha_EM(M_Z)` substitution misses the Rydberg scale;
- one-loop threshold transport is sensitive to charged thresholds;
- lepton-only running leaves a remaining low-energy gap;
- current status remains no-go, with conditional support for a future
  scheme-matched bridge.

Checks:

```bash
set -o pipefail; python3 scripts/frontier_atomic_lane2_alpha0_running_bridge_boundary.py | tee outputs/frontier_atomic_lane2_alpha0_running_bridge_boundary_2026-04-29.txt
python3 -m py_compile scripts/frontier_atomic_lane2_alpha0_running_bridge_boundary.py
```

Expected runner result:

```text
SUMMARY: PASS=18 FAIL=0
```

## 5. What This Closes

This closes the narrow route:

```text
alpha_EM(M_Z) alone
  => alpha(0)
  => Rydberg scale
```

The implication fails. Low-energy QED transport is load-bearing.

## 6. What Remains Open

Lane 2 still needs:

- electron mass or charged-lepton activation law;
- `alpha(0)` or a scheme-matched QED-running bridge;
- physical-unit nonrelativistic Schrodinger/Coulomb limit.

This note addresses only the second gate.
