# Lane 4D SR-2 Pfaffian / Scalar Two-Point Boundary

**Date:** 2026-04-29
**Status:** no-go / exact negative boundary for the SR-2 route; no
unconditional Dirac-global closure and no numerical neutrino-mass claim.
**Loop:** `.claude/science/physics-loops/impact-campaign-20260429/`
**Runner:** `scripts/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary.py`

```yaml
actual_current_surface_status: no-go
conditional_surface_status: conditional-support
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "SR-2 fails as a current-surface route; scalar two-point data are blind to the Pfaffian amplitude without a new typed coupling theorem"
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## 1. Question

The 2026-04-28 Lane 4 fan-out identified SR-2 as the cleanest next attack on
the open `(C2-X)` premise:

> Can the continuum-limit free-scalar two-point closure force every admissible
> Pfaffian extension to have trivial Majorana pairing amplitude `mu = 0`?

If yes, the conditional Dirac global lift would become much stronger. This
block tests that route against the current repo surface.

## 2. Boundary Theorem

**Theorem.** On the current repo surface, the continuum-limit free-scalar
two-point closure does not constrain the Majorana Pfaffian pairing amplitude
`mu`.

Equivalently, SR-2 cannot close `(C2-X)` unless a new typed theorem first
couples the neutrino charge-two Pfaffian primitive to the scalar two-point
surface.

## 3. Proof

The scalar two-point theorems state that the free-scalar Hamiltonian-lattice
two-point functions converge to Lorentz-scalar continuum forms depending only
on the invariant interval and mass:

```text
W_2D(s^2; m) = K_0(m sqrt(-s^2)) / (2 pi)
W_3D(s^2; m) = m K_1(m sqrt(-s^2)) / (4 pi^2 sqrt(-s^2))
```

The Pfaffian family in the neutrino Majorana lane is

```text
Delta(mu) = mu S_unique
```

where `S_unique` is the unique charge-two local channel isolated by the
Majorana current-stack notes.

The scalar two-point expressions have no `mu` input. Therefore the same
scalar two-point signature is compatible with both `mu = 0` and `mu != 0`.
The runner verifies this directly:

- the 1+1D and 3+1D scalar two-point values are identical across
  `mu in {0, 0.25, 1.0}`;
- the Pfaffian signatures differ across the same `mu` values;
- the normal determinant/source-response jet is also identical across `mu`;
- normal sources commute with fermion number, while the pairing seed carries
  charge `-2`.

This is a same-current-data witness against the implication:

```text
scalar two-point closure  =>  mu = 0
```

So SR-2 does not close `(C2-X)` on the current surface.

## 4. What This Closes

This closes one proposed continuation route from the Lane 4 fan-out:

- SR-2 cannot globalize the conditional Dirac theorem by reusing only the
  free-scalar two-point closure.
- The missing object remains a typed charge-two primitive exhaustion theorem,
  a Lorentz-onset theorem with a genuine Pfaffian coupling, or another new
  structural premise.

## 5. What This Does Not Close

This note does not prove:

- that all Pfaffian/Nambu extensions are impossible;
- that no future scalar-to-Pfaffian coupling theorem can be derived;
- that neutrinos are globally Dirac on every future admissible extension;
- any numerical neutrino mass, splitting, or cosmological mass sum.

The prior conditional-support theorem remains conditional. `(C2-X)` remains
open after SR-2.

## 6. Review Notes

Branch-local review disposition: pass.

Checks:

```bash
python3 scripts/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary.py
python3 -m py_compile scripts/frontier_neutrino_lane4_sr2_pfaffian_scalar_two_point_boundary.py
```

Expected runner result:

```text
SUMMARY: PASS=18 FAIL=0
```

## 7. Next Route

The queue should pivot. The nearest remaining Lane 4 options are:

- SR-1 Lorentz-onset incompatibility, but only if a genuine Pfaffian coupling
  to the Lorentz-onset surface is named first;
- SR-3 stronger anomaly cluster, though prior anomaly-exhaustion already
  failed for the gauge-singlet Majorana mass;
- a different lane from the refreshed campaign queue, especially Lane 1
  `sqrt(sigma)` `(B2)` if a narrow finite-volume audit can be made honest.
