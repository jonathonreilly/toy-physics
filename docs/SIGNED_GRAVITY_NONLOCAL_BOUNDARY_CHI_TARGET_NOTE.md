# Signed Gravity Nonlocal / Boundary `chi_g` Target Note

**Date:** 2026-04-25
**Status:** theorem-target note only; no signed-gravity sector claim

This note defines the next theorem target after the two local P0 blocks:

- [`SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md`](SIGNED_GRAVITY_CHI_SELECTOR_THEOREM_OR_NOGO_NOTE.md)
  gives `NO_GO_STRICT_SELECTOR` for local Pauli-string taste-cell
  involutions.
- [`GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md`](GRAVITY_SIGNED_SOURCE_DENSITY_BOUNDARY_NOTE.md)
  gives `SOURCE_PRIMITIVE_BLOCKED_LOCAL` for the retained parity scalar
  source primitive.

The remaining admissible target is narrower:

> Find a nonlocal or boundary-hosted `Z_2` operator `Q_chi` whose eigenvalue
> supplies `chi_g = +/-1`, is conserved or superselected on a stated retained
> surface, locks the gravitational source sign and response sign, preserves
> positive inertial mass, and passes null/Born/norm controls.

This is not a negative-mass, shielding, propulsion, or reactionless-force
claim. It is a target specification for deciding whether the signed-response
consequence harness can be promoted beyond inserted signs.

## Common Gate

Every candidate below must pass the same gate before any phenomenology or
portability work is useful.

```text
Q_chi = Q_chi^dagger
Q_chi^2 = I
dim ker(Q_chi-I) > 0 and dim ker(Q_chi+I) > 0
[Q_chi, H_retained] = 0
```

or else a sharper superselection statement:

```text
P_- U_retained(t) P_+ = 0
```

on the explicitly stated surface. The theorem must also prove:

```text
rho_inertial = M_phys |psi|^2 >= 0
rho_active = chi_g M_phys |psi|^2
response sign = chi_g
```

The second and third lines are the source/response locking condition. A sign in
a response Hamiltonian alone is not enough. A signed boundary trace alone is
not enough. The same branch label must multiply the active source charge and
the test-body response.

If a candidate passes, the source-unit normalization theorem consumes the sign
only at the last step:

```text
C_signed = chi_g C_abs
M_inertial = C_abs > 0
q_bare = 4 pi C_signed = 4 pi chi_g M_inertial
G_Newton,lat = 1
```

This uses
[`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md).
It must not be reversed into a derivation of `chi_g`; the normalization theorem
only maps an already derived active charge into the bare Poisson source unit.

## Candidate A: Primitive Boundary Coframe Orientation

**Definition target.** On a selected primitive face, use the active boundary
block

```text
K = P_A H_cell,     dim K = 4,
E = span(t, n, tau_1, tau_2).
```

Under the metric-compatible Clifford/coframe response premise from
[`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`](PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md),
let

```text
Gamma_a = D(e_a),
Q_chi = Gamma_t Gamma_n Gamma_tau1 Gamma_tau2
```

up to the fixed phase convention that makes `Q_chi` Hermitian with
`Q_chi^2=I`.

**Conservation / superselection gate.** Prove that allowed boundary dynamics
are even in the primitive Clifford algebra:

```text
[H_boundary, Q_chi] = 0
```

and that bulk couplings induce only even boundary operators on `K`. If any
allowed coframe rotation or face-gluing term anticommutes with `Q_chi`, this
candidate fails.

**Source / response locking gate.** Prove that the same oriented coframe sign
enters both:

```text
C_signed = chi_g C_abs
response coupling = chi_g Phi
```

where `C_signed` is the exterior Gauss/asymptotic monopole coefficient. It is
not enough to show that `Q_chi` is the Clifford chirality of the active block;
the theorem must show that the gravitational source readout is the oriented
boundary flux/monopole, not the positive Born norm or the local parity scalar.

**Positive inertial mass gate.** The inertial readout must stay

```text
M_inertial = ||psi||^2 M_0 > 0
```

in both `Q_chi` sectors. The `Q_chi=-1` sector must not be implemented as
negative kinetic energy, negative norm, or negative rest mass.

**Null / Born / norm gates.**

- `Q_chi` sectors must not alter the Born three-slit identity on a fixed
  Hermitian branch Hamiltonian.
- Crank-Nicolson or exact unitary evolution must preserve norm separately in
  each sector.
- A zero exterior monopole, or an exactly paired `+/-` boundary source, must
  give zero far-field monopole.

**Failure conditions.**

- `Q_chi` is only the orientation of a chosen face convention and changes under
  allowed gauge/frame relabeling.
- The Clifford coframe premise supplies CAR/area-law structure but no signed
  exterior source.
- Boundary gluing or retained scalar/gauge terms mix the two sectors.
- The sign multiplies only the response side, reproducing the source-only /
  response-only action-reaction failure.

## Candidate B: APS / Spectral-Asymmetry Boundary Index

**Definition target.** For a compact source region `Omega` with boundary
`partial Omega`, define a boundary Dirac operator `D_partial` from the retained
Clifford/coframe structure and set

```text
Q_chi = sign(eta(D_partial))
```

or, if the signed integer is the natural invariant,

```text
chi_g = sign(Index_APS(D_Omega)).
```

The theorem must specify the regularization at `eta=0`; the zero-index sector
is a null/control sector, not a hidden third sign.

**Conservation / superselection gate.** Prove index stability under all allowed
local deformations that preserve the boundary gap:

```text
delta chi_g = 0
```

unless the boundary spectrum crosses zero. Crossings must be classified as
sector-changing defects, not as ordinary dynamics.

**Source / response locking gate.** Prove an APS/Wald/Gauss identity of the
form

```text
C_signed = chi_g C_abs
delta S_boundary / delta Phi = chi_g |psi|^2
```

on the candidate surface. This is the hard step. If the index only labels a
topological phase while the Poisson source remains `|psi|^2`, the candidate is
only a spectator charge.

**Positive inertial mass gate.** The absolute magnitude of the source region
must be an additive positive mass:

```text
M_inertial(Omega_1 union Omega_2)
  = M_inertial(Omega_1) + M_inertial(Omega_2) > 0.
```

The index sign may orient the active monopole only.

**Null / Born / norm gates.**

- `eta=0` or paired opposite-index boundaries must have zero signed monopole
  and positive total inertial mass.
- Boundary spectral flow may not introduce nonunitary bulk evolution.
- Born/norm controls must be unchanged away from explicit sector-crossing
  events.

**Failure conditions.**

- The boundary Dirac spectrum is gapless generically, making `chi_g`
  unstable.
- The sign is basis-dependent under boundary trivialization.
- The index is conserved but not coupled to the gravitational source.
- Mixed-index superpositions make the active mass basis-dependent.

## Candidate C: Nonlocal Projector-Difference Sector Charge

**Definition target.** Let `P_+` and `P_-` be nonlocal projectors onto two
orthogonal global sectors, for example a closed-boundary parity sector or a
global even/odd flux sector. Define

```text
Q_chi = P_+ - P_-
rho_active(x) = M_phys psi^dagger(x) Q_chi psi(x).
```

This candidate deliberately leaves the local taste-cell algebra. The projectors
must be defined by a global boundary condition or global constraint, not by a
local Pauli-string involution already blocked by the selector scan.

**Conservation / superselection gate.** Prove exact sector conservation:

```text
[P_+, H_retained] = [P_-, H_retained] = 0
```

for the retained dynamics. If the proof only gives approximate conservation,
the residual leakage must scale to zero under a stated limit and must be
bounded in the two-body harness.

**Source / response locking gate.** The source action must variationally expose
the projector-difference density:

```text
delta E / delta Phi(x) = M_phys psi^dagger(x) Q_chi psi(x),
```

not the local parity scalar `epsilon|psi|^2` and not the positive Born density.
For a pure sector packet this reduces to:

```text
rho_active = chi_g M_phys |psi|^2.
```

**Positive inertial mass gate.**

```text
rho_inertial(x) = M_phys |psi(x)|^2
```

must be independent of `Q_chi`. Sector populations add positively even when
active monopoles cancel.

**Null / Born / norm gates.**

- Same-point equal-norm `P_+` and `P_-` packets cancel the active monopole.
- The same pair has positive inertial mass equal to the sum of both norms.
- Sector projectors must commute with unitary evolution strongly enough that
  norm cannot leak into a hidden neutral sector.

**Failure conditions.**

- `P_+ - P_-` reduces to one of the blocked local neutral taste labels.
- The projectors depend on arbitrary basis choices or boundary gauge fixing.
- The variational derivative remains `epsilon|psi|^2`.
- The branch-projected source is inserted by hand rather than derived from an
  action.

## Candidate D: Boundary `Z_2` Holonomy / Flux Superselection

**Definition target.** If the retained boundary admits a gauge-invariant
noncontractible `Z_2` observable, define

```text
Q_chi = product_{ell in gamma_boundary} U_ell,
Q_chi = +/-1.
```

For an open finite patch, replace the loop by a gauge-invariant relative
boundary flux between two anchoring cuts. The definition must be independent of
local gauge choices.

**Conservation / superselection gate.** Prove the holonomy is a central
superselection label for the allowed local algebra:

```text
[Q_chi, A_local] = 0
[Q_chi, H_retained] = 0.
```

If local admissible defects can change the holonomy, they must be classified as
sector-changing boundary defects outside the theorem surface.

**Source / response locking gate.** Prove that the holonomy sign orients the
active Gauss charge:

```text
C_signed = Q_chi C_abs
```

and also orients the test response. A topological flux that affects only a
phase, lensing interference, or complex-action proxy is quarantined and is not
`chi_g`.

**Positive inertial mass gate.** The holonomy cannot alter the positive mass
readout:

```text
M_inertial = C_abs >= 0
```

after source-unit normalization fixes the physical monopole scale.

**Null / Born / norm gates.**

- Opposite holonomies with equal `C_abs` cancel the exterior monopole.
- Local Born probabilities are unchanged by pure gauge representatives of the
  same holonomy.
- Norm is conserved under the holonomy-preserving Hamiltonian.

**Failure conditions.**

- The lattice is simply connected or has no gauge-invariant `Z_2` boundary
  observable.
- The holonomy is a phase-only Aharonov-Bohm label with no active source
  coupling.
- It changes under allowed local moves, so it is not superselected.
- The sign survives only in lensing/proxy diagnostics rather than in two-body
  source/response closure.

## Recommended First Harness

If one candidate is chosen, start with Candidate A. It has the most existing
supporting infrastructure: the primitive boundary block `P_A H_cell`, the
conditional Clifford/coframe bridge, the primitive-CAR edge carrier, the
finite-boundary extension, and the source-unit normalization theorem.

The first harness should be algebraic and should not run new dynamics until
the branch/source theorem surface is explicit:

```text
scripts/frontier_signed_gravity_boundary_chi_candidate.py
```

Minimum output:

```text
candidate name
Q_chi Hermitian residual
Q_chi^2 residual
sector dimensions
[Q_chi, H_boundary] residual
P_- U P_+ leakage
frame/gauge relabel invariance check
source functional derivative identified as one of:
  chi_g |psi|^2
  epsilon |psi|^2
  |psi|^2
  spectator/topological only
positive inertial mass check
neutral +/- monopole cancellation
Born I3 control
norm drift
source-unit conversion:
  q_bare = 4 pi chi_g M_phys
FINAL_TAG
```

Allowed final tags:

```text
BOUNDARY_CHI_CANDIDATE_PASS
BOUNDARY_CHI_SOURCE_NOT_LOCKED
BOUNDARY_CHI_NOT_CONSERVED
BOUNDARY_CHI_GAUGE_RELABEL
BOUNDARY_CHI_NEGATIVE_INERTIAL_MASS
BOUNDARY_CHI_NULL_CONTROL_FAIL
BOUNDARY_CHI_NO_GO
```

The harness should treat `BOUNDARY_CHI_CANDIDATE_PASS` as a theorem target
readiness tag only. It is not a physical signed-gravity claim until a written
proof supplies the source/response locking theorem and the two-body
action-reaction consequence harness is rerun using the derived `Q_chi`.

## Candidate Priority

1. **Primitive boundary coframe orientation.** Best first target because it is
   closest to the retained boundary/Wald/Planck carrier surface, but it fails
   unless the coframe orientation is shown to source the exterior monopole.
2. **APS / spectral-asymmetry boundary index.** Strong conservation story if a
   boundary gap exists, but the source-locking bridge is harder.
3. **Boundary `Z_2` holonomy / flux superselection.** Clean superselection if
   the topology exists, but high risk of being only a phase/proxy label.
4. **Nonlocal projector-difference sector charge.** Useful as a formal
   fallback and no-go harness; lowest priority unless the projectors come from
   a native boundary constraint rather than an inserted sector split.

## Stop Conditions

Stop the signed-response promotion attempt and keep the lane as a control/no-go
packet if all concrete candidates hit one of these failures:

- no conserved or superselected `Q_chi`;
- conserved `Q_chi` exists but is source-neutral;
- signed source exists only by hand insertion;
- the sign also flips inertial mass or norm positivity;
- null `+/-` pairs leave a residual monopole;
- Born or norm controls fail on the branch-preserving surface;
- source-unit normalization is used to rename `G_kernel=1/(4 pi)` instead of
  consuming an already derived signed active charge.
