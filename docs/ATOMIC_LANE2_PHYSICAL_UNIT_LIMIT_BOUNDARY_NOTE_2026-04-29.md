# Atomic Lane 2 Physical-Unit Limit Boundary

**Date:** 2026-04-29
**Status:** no-go / conditional-support boundary for current Rydberg closure;
no atomic-scale numerical claim.
**Loop:** `.claude/science/physics-loops/impact-campaign-20260429/`
**Runner:** `scripts/frontier_atomic_lane2_physical_unit_limit_boundary.py`

```yaml
actual_current_surface_status: no-go
conditional_surface_status: conditional-support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "current dimensionless/scaffold hydrogen machinery fixes the 1/n^2 shape but not the physical eV scale"
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 1. Question

Lane 2 has a useful hydrogen scaffold and dimensionless Coulomb/bound-state
surfaces. This block asks whether those surfaces already fix the physical eV
Rydberg scale.

## 2. Boundary Theorem

**Theorem.** On the current repo surface, the dimensionless/scaffold hydrogen
machinery fixes the `1/n^2` spectral shape but not the physical eV scale.

The missing scale is exactly the Hartree factor:

```text
E_H = m_e alpha(0)^2
Rydberg = E_H / 2
```

## 3. Proof

The dimensionless Coulomb Hamiltonian has eigenvalues:

```text
epsilon_n = -1 / (2 n^2)
```

For any positive scale `S`, the physical-looking spectrum

```text
E_n = S * epsilon_n
```

has the same ratios `E_n/E_1 = 1/n^2`. Therefore the ratio structure does not
select the eV scale. Selecting the eV scale requires `S = m_e alpha(0)^2`.

Block 04 already showed `alpha(0)` is not closed from current
`alpha_EM(M_Z)` data. Lane 6 still blocks the electron mass. Therefore the
current hydrogen scaffold cannot be promoted into a framework-derived Rydberg
number.

## 4. Runner Witness

The runner checks:

- Lane 2 authority surfaces name the physical-unit Schrodinger/Coulomb limit
  as a required gate;
- multiple Hartree-scale choices preserve the same `1/n^2` ratios while
  producing different `E_1` values;
- the Hartree scale is exactly `m_e alpha(0)^2`;
- current status remains no-go, with conditional support for the solver once
  the physical-unit inputs land.

Checks:

```bash
set -o pipefail; python3 scripts/frontier_atomic_lane2_physical_unit_limit_boundary.py | tee outputs/frontier_atomic_lane2_physical_unit_limit_boundary_2026-04-29.txt
python3 -m py_compile scripts/frontier_atomic_lane2_physical_unit_limit_boundary.py
```

Expected runner result:

```text
SUMMARY: PASS=16 FAIL=0
```

## 5. What This Closes

This closes the narrow route:

```text
dimensionless hydrogen shape
  => physical eV Rydberg scale
```

The implication fails. The shape is useful downstream, but the scale remains
load-bearing.

## 6. What Remains Open

Lane 2 still needs:

- electron mass or charged-lepton activation law;
- `alpha(0)` or a scheme-matched QED-running bridge;
- physical-unit derivation of the one-body Schrodinger/Coulomb limit.
