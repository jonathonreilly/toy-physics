# Hadron Lane 1 B2 Dynamical Screening Boundary

**Date:** 2026-04-29
**Status:** no-go / bounded-support boundary for the current B2 route; no
`sqrt(sigma)` status upgrade and no hadron-mass claim.
**Loop:** `.claude/science/physics-loops/impact-campaign-20260429/`
**Runner:** `scripts/frontier_hadron_lane1_b2_dynamical_screening_boundary.py`

```yaml
actual_current_surface_status: no-go
conditional_surface_status: bounded-support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "B2 requires sea-fermion determinant data or an explicitly budgeted external comparator; current pure-gauge data do not determine the screening factor"
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 1. Question

Lane 1 identifies `(B2)` as the load-bearing numerical gap for the
`sqrt(sigma)` route:

```text
quenched SU(3) string tension at beta=6.0
  -> N_f=2+1 dynamical string tension
```

The current bounded derivation uses the quenched Method-2 payload and a rough
screening factor near `0.96`. This block asks whether the existing repo data
can close that factor without a new dynamical calculation.

## 2. Boundary Theorem

**Theorem.** On the current repo surface, the pure-gauge beta=6.0 payload does
not determine the `(B2)` dynamical screening factor.

Equivalently, B2 cannot be closed by reusing the existing pure-gauge
plaquette, Sommer-scale, Wilson-loop, or Creutz-ratio data alone.

## 3. Proof

The current Method-2 string-tension payload has the form:

```text
beta = 6.0
r0/a = 5.37
sigma a^2 = 0.0465
sqrt(sigma)_quenched ~= 484 MeV
```

The B2 correction is not another pure-gauge observable. It changes the path
measure from the Wilson gauge measure to a sea-fermion determinant measure:

```text
dmu_quenched(U)  proportional to exp(-S_g(U)) dU
dmu_dyn(U)       proportional to exp(-S_g(U))
                              det(D_u + m_u) det(D_d + m_d) det(D_s + m_s) dU
```

The screening factor compares string tensions extracted under these two
different measures. The determinant factors, the sea masses, and a large-volume
Creutz-ratio extraction are therefore load-bearing inputs.

The current repo has a useful pure-gauge consistency runner at `L=4`, but the
confinement note already marks that as qualitative: quantitative extraction
requires large Wilson loops and volumes at least of order `16^4`. The existing
runner also does not include the sea-fermion determinant.

Therefore a family of factors, for example `0.90`, `0.94`, `0.96`, and `1.00`,
leaves the same pure-gauge payload unchanged while producing different
`sqrt(sigma)` readouts. Pure-gauge data alone cannot select one member of that
family.

## 4. Runner Witness

The runner checks:

- current Lane 1 notes name B2 as the dominant numerical residual;
- the same pure-gauge payload is compatible with a family of screening factors;
- a toy determinant reweighting changes the measured observable and depends on
  the sea masses;
- the current `L=4` pure-gauge runner is not a large-volume dynamical
  extraction;
- the status firewall blocks a stronger branch-local status.

Checks:

```bash
set -o pipefail; python3 scripts/frontier_hadron_lane1_b2_dynamical_screening_boundary.py | tee outputs/frontier_hadron_lane1_b2_dynamical_screening_boundary_2026-04-29.txt
python3 -m py_compile scripts/frontier_hadron_lane1_b2_dynamical_screening_boundary.py
```

Expected runner result:

```text
SUMMARY: PASS=21 FAIL=0
```

## 5. What This Closes

This closes a narrow false route:

```text
current pure-gauge beta=6.0 data + rough factor 0.96
  => closed B2 dynamical screening budget
```

That implication fails. The current artifacts support only the bounded
`sqrt(sigma)` readout and the exact identification of what is missing.

## 6. What Remains Open

B2 can reopen only through one of these paths:

- a genuine `N_f=2+1` beta=6.0 determinant ensemble with controlled sea masses
  and large-volume Creutz ratios;
- a branch-local theorem deriving the determinant correction from framework
  structure;
- an explicitly budgeted external comparator, clearly marked as an admitted
  comparator rather than a framework-native derivation.

The note makes no pion, proton, neutron, spectroscopy, or form-factor claim.

## 7. Next Route

This is the second consecutive local no-go/boundary block in the campaign.
Per the long-running policy, the next science selection should force a stretch
attempt from minimal premises before more audit-only cycles.
