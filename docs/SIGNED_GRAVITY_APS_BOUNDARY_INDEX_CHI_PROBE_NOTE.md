# Signed Gravity APS Boundary-Index `chi_g` Probe Note

**Date:** 2026-04-25
**Status:** first concrete APS/spectral-asymmetry candidate pass; source-locking
bridge still open
**Script:** [`../scripts/signed_gravity_aps_boundary_index_probe.py`](../scripts/signed_gravity_aps_boundary_index_probe.py)

This note makes Candidate B from
[`SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md`](SIGNED_GRAVITY_NONLOCAL_BOUNDARY_CHI_TARGET_NOTE.md)
concrete enough to test.  It does not make a negative-mass, shielding,
propulsion, physical antigravity, or reactionless-force claim.  The result is
a boundary-index candidate for a signed active-source label, not a derivation
that such a label is realized by the retained gravity surface.

Inputs already fixed by the signed-gravity audit:

- [`SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md`](SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md):
  local/taste-cell Pauli selectors are blocked.
- [`GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md`](GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md):
  the retained local scalar source is parity-signed but not a conserved
  branch-fixed monopole.
- [`SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md`](SIGNED_GRAVITY_SOURCE_ACTION_ESCAPE_HATCH_NOTE.md):
  any escape hatch must derive a native conserved signed active source while
  keeping positive inertial mass and source/response locking.

The APS route is the next admissible place to look because it is boundary
hosted, spectral, and deformation-stable when a boundary gap is protected.

## Candidate Definition

Let `Omega` be a compact source region with oriented boundary
`Y = partial Omega`.  A candidate retained boundary structure must supply:

```text
D_Y = D_Y^dagger
spec(D_Y) has a gap around 0 on the retained surface
D_Y is built from the retained boundary Clifford/coframe data
```

For a finite regulator or finite boundary discretization, define the regulated
eta count

```text
eta_delta(D_Y) =
  # {lambda in spec(D_Y): lambda > delta}
  - # {lambda in spec(D_Y): lambda < -delta}
```

and the zero-window count

```text
h_delta(D_Y) = # {lambda in spec(D_Y): |lambda| <= delta}.
```

The branch candidate is:

```text
Q_chi(Y) = sign(eta_delta(D_Y))
```

only when:

```text
h_delta(D_Y) = 0
eta_delta(D_Y) != 0
```

The null/control sector is:

```text
Q_chi(Y) = 0
```

when `eta_delta(D_Y) = 0` or `h_delta(D_Y) != 0`.  This is not a hidden third
active sign.  It is a rejection/control state where the signed-response
consequence harness is not allowed to claim a branch.

In a continuum theorem target, replace the finite count by the APS invariant:

```text
eta(D_Y, s) = sum_{lambda != 0} sign(lambda) |lambda|^{-s}
eta(D_Y) = analytic continuation to s = 0
Index_APS(D_Omega)
  = int_Omega A_hat(R) - (eta(D_Y) + h(D_Y))/2
```

The sign may be taken from `eta(D_Y)` or from the signed APS index only after
the theorem specifies which invariant is quantized on the retained boundary
surface.  The zero-index/zero-eta case remains a null/control sector.

## Conservation / Superselection Gate

The required theorem is not merely that `eta` can be computed.  It must show
that the retained boundary dynamics stay inside one gapped spectral sector:

```text
D_Y(t) = D_Y(0) + K(t)
gap_0(D_Y(t)) >= g > 0
delta Q_chi = 0
```

or else that the two signs are superselected:

```text
P_- U_retained(t) P_+ = 0.
```

Allowed local deformations may change eigenvectors and the metric/coframe
representative, but not the signed spectral flow unless an eigenvalue crosses
zero.  A zero crossing is a sector-changing boundary defect, not ordinary
dynamics.  If generic retained perturbations close the boundary gap, this APS
candidate fails.

## Source / Response Locking Gate

The hard missing theorem is a boundary source identity.  A pass requires an
APS/Wald/Gauss statement of the form:

```text
C_signed(Y) = Q_chi(Y) C_abs(Y)
delta S_boundary / delta Phi = Q_chi(Y) |psi|^2
response coupling = Q_chi(Y) Phi
```

with the same branch label in all three locations.  This must be a variational
or conserved-charge identity on the retained surface, not a later sign
insertion.  If the APS sign only labels a topological phase while the Poisson
source remains `|psi|^2`, then it is a spectator charge and the candidate
fails the signed-source gate.

## Positive Inertial Mass Gate

The APS sign may orient the active monopole only.  It must not change norm,
rest mass, kinetic energy sign, or Hilbert-space positivity:

```text
M_inertial(Omega) = C_abs(Y) > 0
rho_inertial = M_phys |psi|^2 >= 0
rho_active = Q_chi(Y) M_phys |psi|^2
```

For disjoint positive-mass source regions:

```text
M_inertial(Omega_1 union Omega_2)
  = M_inertial(Omega_1) + M_inertial(Omega_2) > 0.
```

The `Q_chi = -1` sector is therefore not negative inertial mass.  It is only a
candidate orientation of the active source coefficient, conditional on the
source/response locking theorem above.

## Null / Born / Norm / Source-Unit Controls

The APS candidate must pass these controls before any phenomenology:

| control | required result |
|---|---|
| `eta = 0` or `h != 0` | null/control sector; no signed branch claim |
| paired opposite-index boundaries | zero signed monopole and positive total inertial mass |
| unitary boundary-basis relabeling | identical spectrum, identical `eta_delta`, identical `Q_chi` |
| gap-preserving local deformation | unchanged `Q_chi` |
| zero crossing | explicit sector-changing defect |
| Born rule | unchanged on each fixed Hermitian branch Hamiltonian |
| norm | exact/unitary evolution preserves norm separately in each retained sector |
| source-unit normalization | may map `q_bare = 4 pi Q_chi M_phys` only after `Q_chi` is derived |

The source-unit theorem cannot derive `Q_chi`; it can only carry an already
derived signed active charge into the bare Poisson normalization.

## Finite-Matrix Probe

The executable probe uses a toy boundary spectrum:

```text
D_+ = diag(+g, +a_1, -a_1, ..., +a_n, -a_n)
D_- = diag(-g, +a_1, -a_1, ..., +a_n, -a_n)
D_0 = diag(+a_1, -a_1, ..., +a_n, -a_n)
```

The paired levels are bulk/control pairs.  The unpaired boundary level gives
`eta_delta = +/-1`.  This is only a finite regulator for the stability test;
it is not a proof that the retained physical boundary has such an unpaired
level.

The probe distinguishes two notions:

1. `eta_delta(D_Y)`, which is spectral and invariant under arbitrary unitary
   relabeling of the boundary basis.
2. a deliberately bad coordinate-local sign, which reads one chosen basis
   coordinate and can flip under a basis permutation while the spectrum is
   unchanged.

Command:

```bash
python3 scripts/signed_gravity_aps_boundary_index_probe.py
```

Current output:

```text
Signed-gravity APS boundary-index finite spectrum probe
  [PASS] eta sign gives both nonempty candidate sectors  (eta_plus=1, eta_minus=-1)
  [PASS] paired boundary spectrum is a null/control sector  (eta_null=0, zero_modes=0)
  [PASS] eta is invariant under arbitrary boundary-basis unitary relabeling  (eta=1, max_eig_err=2.22e-15)
  [PASS] basis-local sign can flip while eta and the spectrum do not  (artifact=1->-1, eta=1->1)
  [PASS] eta sign is stable under sampled gap-preserving boundary perturbations  (initial_gap=0.400, min_gap_after=0.372)
  [PASS] sector change is tied to an explicit boundary zero crossing  (chi_path=[1, 1, 1, 1, 0, -1, -1, -1, -1])
  [PASS] positive inertial mass is independent of eta sign  (M=2.75, active=2.75, response=+1)
  [PASS] paired +/- boundary sources are source-unit null controls  (active_sum=0.00, inertial_sum=5.50)
FINAL_TAG: APS_BOUNDARY_INDEX_PROBE_PASS_SOURCE_LOCKING_OPEN
```

The finite probe passes only the spectral-stability and basis-independence
preconditions.  The final tag deliberately leaves source locking open.

## Failure Conditions

This APS candidate fails if any of the following occur:

- `D_Y` is not naturally built from the retained boundary Clifford/coframe
  structure.
- the boundary spectrum is generically gapless, so `Q_chi` is unstable.
- `Q_chi` changes under a boundary-basis relabeling, trivialization choice, or
  packet-centering convention.
- spectral flow through zero is treated as ordinary dynamics instead of a
  classified sector-changing defect.
- the sign is conserved but the variational Poisson source remains the
  positive Born source `|psi|^2`.
- the sign is inserted only into the response Hamiltonian or only into the
  source, reproducing the source-only/response-only action-reaction failure.
- mixed-index superpositions make the active monopole basis-dependent.
- negative norm, negative kinetic energy, or negative inertial mass is used to
  implement the minus branch.

## Verdict

`Q_chi = sign(eta_delta(D_Y))` is now a precise APS/spectral-asymmetry boundary
candidate with a clean finite-matrix precondition test.  It passes the narrow
tests that a real candidate must pass first: basis relabeling does not change
the sign, gap-preserving deformations keep the sign fixed, null sectors are
explicit, and zero crossings are classified as sector-changing events.

It does not yet pass the physical signed-gravity gate.  The missing theorem is
the source/response locking bridge:

```text
C_signed = Q_chi C_abs
delta S_boundary / delta Phi = Q_chi |psi|^2
response coupling = Q_chi Phi.
```

Until that bridge is derived, the APS sign is a mathematically admissible
boundary selector candidate, not a physical signed active gravitational source.

## Follow-Up Bridge Audit

The missing bridge has now been audited in
`SIGNED_GRAVITY_APS_WALD_GAUSS_BRIDGE_AUDIT_NOTE.md`
(downstream consumer in same lane; cross-reference only — not a one-hop dep of this note)
with runner
[`../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py`](../scripts/signed_gravity_aps_wald_gauss_bridge_audit.py).

Result:

```text
FINAL_TAG: APS_WALD_GAUSS_BRIDGE_NOT_DERIVED
```

The audit keeps the eta sign as a clean boundary label, but finds that the
retained Wald/Gauss/source-unit stack supplies a positive unsigned source
scale. Gap-preserving variations leave eta source-neutral, and the locked
source/response table appears only after explicitly inserting `chi_eta` into
the source action.
