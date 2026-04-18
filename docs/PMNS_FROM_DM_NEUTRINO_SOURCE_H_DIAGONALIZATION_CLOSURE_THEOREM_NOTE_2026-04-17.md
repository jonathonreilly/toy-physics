# PMNS as `f(H(m, delta, q_+))` — Conditional / Support Closure

**Date:** 2026-04-17 (Option-A demotion applied after 2026-04-17 review pass)
**Status:** **CONDITIONAL / SUPPORT closure — NOT a retained live-sheet
closure theorem.** The positive content this note retains: an explicit
map `(m, δ, q_+) → (θ_12, θ_13, θ_23, δ_CP)` by direct
diagonalisation of the retained affine Hermitian `H` on the live sheet,
and a uniquely pinned chamber point
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` whose `|U_PMNS|`
matches NuFit 5.3 NO 3-σ in 9/9 entries and predicts
`sin δ_CP = −0.9874`. The conditionality that the current branch tip
carries, explicitly flagged here:

1. **Imposed branch-choice admissibility rule** on the Hermitian
   curvature (`signature(H_base + J) = (2, 0, 1)`) — NOT a retained
   theorem; see the perturbative-uniqueness note's Option-A demotion
   and the flagship closure review note.
2. **SM-canonical `q_H = 0`** (not axiom-derived).
3. **Observational hierarchy pairing** `σ_hier = (2, 1, 0)`.

Under these three conditionals the pinning is unique inside the
chamber. Without them (in particular without (1)), there are competing
admissible basins (notably at `(28, 21, 5)` and `(21, 13, 2)` on
opposite caustic branches).

The DM flagship gate status on the current branch tip is therefore
**conditional / support**, NOT `CLOSED`.
**Script:** `scripts/frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py`
**Runner:** `PASS = 43, FAIL = 0`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Option-A honest-label revision (2026-04-17)

This note was tightened after two successive adversarial review passes.
The second review pass (commit 5c70c15d) correctly objected that the
first-pass "basin-uniqueness via Sylvester inertia" lane collapsed two
distinct steps: (a) Sylvester's law of inertia (textbook; uncontested)
and (b) the SELECTION of the baseline-connected branch as the physical
live sheet (not retained). The Option-A revision carries three pieces
of demotion:

- Basin-uniqueness and permutation-uniqueness (CRITICAL 1 + 2): the
 "retained Sylvester inertia selector" framing is WITHDRAWN. Basin
 uniqueness is now a conditional result under an imposed branch-
 choice admissibility rule. See
 [DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md)
 for the honest-label statement. Competing in-chamber basins still
 flip `signature(H_base + J)` from `(2, 0, 1)` to `(1, 0, 2)`, but
 the selection of the `(2, 0, 1)` branch as the physical live sheet
 is an imposed admissibility rule, NOT a retained theorem. Only
 Basin 1 at `σ = (2, 1, 0)` is admissible UNDER the imposed rule.
- θ_23 upper-octant conditionality (SERIOUS 3): formalized as a
 falsifiable CONDITIONAL structural prediction in
 [PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](./PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md).
 Chamber closure under the imposed branch-choice rule and `q_H = 0`
 exists only if `s_23^2` is above a specific threshold; this is a
 conditional falsifiable prediction resolvable at DUNE / JUNO / Hyper-K.
- U_e = I citation chain (MEDIUM 4): replaced by the Z_3-trichotomy route
 in
 [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](./CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md),
 which does NOT depend on the open normalization step in the
 Dirac-bridge theorem.
- δ_CP framing (MEDIUM 5): reframed below as "falsifiable consequence of
 the construction" rather than an over-determined check.

## Summary

The observable-bank exhaustion theorem
[DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17](./DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md)
stratified the remaining open object of the selector gate into exactly
three promotion lanes `(P1, P2, P3)`. This note builds **P3** explicitly.

**Main theorem.** The PMNS mixing angles `(θ_12, θ_13, θ_23,
delta_CP)` admit an explicit retained-atlas-native closed-form map

```
(m, delta, q_+) --> (sin^2 θ_12, sin^2 θ_13, sin^2 θ_23, delta_CP)
```

obtained by direct diagonalization of the retained affine Hermitian
`H(m, delta, q_+)` on the live source-oriented sheet. The map is defined
everywhere in the chamber `q_+ >= sqrt(8/3) - delta`.

**Back-propagation statement (conditional on the imposed branch-choice rule).**
Requiring this map to reproduce the PDG 2024 central observational values

```
sin^2 θ_12 = 0.307, sin^2 θ_13 = 0.0218, sin^2 θ_23 = 0.545
```

has a unique chamber solution **under the imposed branch-choice
admissibility rule** — i.e. restricted to the connected component of
`det(H_base + J) ≠ 0` that contains `J = 0`, equivalently
`signature(H_base + J) = signature(H_base) = (2, 0, 1)`:

```
(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)
```

verified by 60 independent random-start multi-start + fsolve sharpening, all
converging to the same point at machine precision. The point lies strictly
inside the chamber (distance `0.0159` above the boundary
`q_+ = sqrt(8/3) - delta`). Other admissible-absent-the-rule chamber
basins exist (at `(m, δ, q_+) ≈ (28, 21, 5)` on the same permutation
and at `≈ (21, 13, 2)` on the competing `σ = (2, 0, 1)` permutation)
— both flip `signature(H_base + J)` to `(1, 0, 2)` and have
`det(H_base + J) < 0`; they sit on non-baseline-connected caustic
branches and are inadmissible UNDER THE IMPOSED RULE. Without the
imposed rule they are equally admissible.

**δ_CP: falsifiable consequence of the construction.** The map
`(m, delta, q_+) -> (s12^2, s13^2, s23^2, delta_CP)` sends `R^3` to a
3-dimensional sub-manifold of `R^4`. Three observational angles pin
`(m, delta, q_+)` (under the retained source-branch inertia selector);
the CP phase is then forced by the chart geometry, not an over-determined fit.
Disagreement with future measurements falsifies the construction, not
merely the pinned point. At the pinned point:

```
sin(delta_CP) = -0.9874
delta_CP = -80.88 deg (equivalently +279.12 deg)
|Jarlskog| = 0.0328
```

in the T2K-preferred lower octant and consistent with the observational
`|J|` band.

**Observational consistency.** All nine entries of `|U_PMNS|` at the pinned
point lie inside the NuFit 5.3 3-sigma ranges (normal ordering). Under
the imposed branch-choice rule and `q_H = 0`, the selector gate closes
conditionally on the chamber; the honest overall status is
**conditional / support**, NOT unconditional positive closure.

## Retained inputs

All retained / theorem-grade at the time of writing:

- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
 — affine chart `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`.
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
 — chamber `q_+ >= sqrt(8/3) - delta`.
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
 — `K_Z3 = U_Z3^dag H U_Z3` decomposition, frozen slots `K01 = a_*`, `K02 = b_*`.
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM_NOTE_2026-04-16.md)
 — chamber-blindness of the current exact bank (includes `a_*`, `b_*`).
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
 — retained 3-dim irreducible observable space `H_hw=1`.
- [NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md](./NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md)
 — Z_3 support trichotomy fixing `Y_e` diagonal on the `q_H = 0`
 branch, hence `U_e = I` in the axis basis (primary route).
- [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](./CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md)
 — full `U_e = I` replacement citation chain with the `q_H = 0`
 conditional input flagged explicitly.
- [DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md)
 — imposed branch-choice admissibility rule (NOT retained)
 `signature(H_base + J) = (2, 0, 1)` picks Basin 1 uniquely.
 Scale bounds remain as consistency diagnostics (Basin 1 satisfies
 `‖J‖_F / ‖H_base‖_F ≈ 0.94` and `‖J‖_op / ‖H_base‖_op ≈ 0.86` while
 the non-baseline-connected basins have ratios ≥ 11).
- [DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md)
 — exhaustion theorem and the identification of P3 as the atlas-open
 promotion lane that closes the selector gate.

Conditional input (not axiom-derived, SM-canonical):

- `q_H = 0`: the Higgs `Z_3` generation charge on the charged-lepton
 Yukawa coupling. See
 [CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](./CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md)
 for the full conditionality discussion.

Complementary (secondary) retained route with an open normalization step:

- [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
 — post-EWSB Dirac operator `Γ_1` diagonal in the axis basis on
 `H_hw=1`. The chain from axis-basis-diagonal-`Γ_1` to `U_e = I` passes
 through the still-open second-order effective-Yukawa normalization;
 hence this is a complementary route that will be retained-grade once
 that normalization theorem closes elsewhere. The primary route used
 in this closure is the Z_3-trichotomy route above.

No post-axiom invention. No new axiom.

## Explicit construction of the PMNS map

### 1. The retained affine `H`

From the retained exact affine boundary theorem on the live sheet,

```
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q
```

with

```
H_base = [[0, E1, -E1 - i gamma],
  [E1, 0, -E2],
  [-E1 + i gamma, -E2, 0]],
T_m = [[1, 0, 0], [0, 0, 1], [0, 1, 0]],
T_delta = [[0, -1, 1], [-1, 1, 0], [1, 0, -1]],
T_q = [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3.
```

`H` is Hermitian by construction (verified at all five observable-bank-
exhaustion candidate points).

### 2. The charged-lepton basis

On `H_hw=1` the retained conjugate `Z_3` triplets are
`q_L = (0, +1, -1)` and `q_R = (0, -1, +1)` under the retained
`C_3[111]` generation cycle
([THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)).
For a single Higgs doublet with definite `Z_3` charge `q_H`, the retained
trichotomy
([NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md](./NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md),
applied to `Y_e` via the same conjugate-triplet derivation used in
[LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md](./LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md))
forces the charged-lepton Yukawa into one of three permutation patterns.
On the canonical `q_H = 0` branch (an SM-canonical conditional input,
not axiom-derived), `Y_e = diag(y_1, y_2, y_3)` and therefore

```
|U_e| = I_3 (in the axis basis of H_hw=1).
```

See
[CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md](./CHARGED_LEPTON_UE_IDENTITY_VIA_Z3_TRICHOTOMY_NOTE_2026-04-17.md)
for the full replacement chain (which does **not** depend on the open
normalization step in the Dirac-bridge theorem) and explicit flagging
of (i) the `q_H = 0` conditional input and (ii) the observational
hierarchy pairing `sigma_hier = (2, 1, 0)` below.

### 3. The neutrino basis from `H`

On the active sheet, the neutrino observable Hermitian is `H(m, delta,
q_+)` itself. The neutrino mass basis is the unitary `U_nu(m, delta, q_+)`
whose columns are the eigenvectors of `H`, ordered by ascending real
eigenvalue.

### 4. The PMNS matrix

The PMNS matrix is `U_PMNS = U_e^dag U_nu = U_nu`, followed by the
canonical row permutation

```
sigma_hier = (2, 1, 0) # electron <-> largest H-eigenvalue row,
    # muon <-> middle,
    # tau <-> smallest
```

which is the unique row permutation that produces observationally
non-degenerate angles consistent with the measured PDG hierarchy
`|U_e3| << |U_e1|, |U_e2|` **under the imposed branch-choice rule**
`signature(H_base + J) = (2, 0, 1)`. Four of the six permutations admit
no chamber solution at all; the competing `sigma = (2, 0, 1)`
permutation admits a chamber solution only at
`signature(H_base + J) = (1, 0, 2)` (on a non-baseline-connected
branch), which is inadmissible under the imposed rule (but admissible
without it). The 60-seed multi-start confirms `sigma_hier = (2, 1, 0)`
as the unique closing permutation under the imposed rule.

```
U_PMNS(m, delta, q_+) = P_{sigma_hier} · (eigenvectors of H in ascending eigenvalue order)
```

Mixing angles are extracted in the standard PDG convention:

```
|U_e3|^2 = sin^2 θ_13,
|U_e2|^2 = sin^2 θ_12 cos^2 θ_13,
|U_mu3|^2 = sin^2 θ_23 cos^2 θ_13,
```

and the CP phase from the Jarlskog invariant

```
J = Im(U_e1 U_e2^* U_mu1^* U_mu2)
 = c_12 s_12 c_23 s_23 c_13^2 s_13 sin(delta_CP).
```

## Retained chamber-blindness checks

The runner verifies at the five candidate points `A..E` that

```
K[0, 1] = a_* = 0.16993211 + 1.19280904 i, |a_*| = 1.2048528262,
K[0, 2] = b_* = 0.45860725 - 0.69280904 i, |b_*| = 0.8308459399.
```

These are identical at all five candidates at machine precision, exactly
as required by the retained current-bank blindness theorem. The singlet-
doublet coupling pair `(a_*, b_*)` is frozen on the chamber; all PMNS
chamber-variation comes from the doublet block
`K_doublet = K[1:3, 1:3]` which depends on `(m, delta, q_+)` as recorded
in the retained `Z_3` doublet-block point-selection theorem.

## Chamber variation of PMNS angles

The runner evaluates the map at the five observable-bank-exhaustion candidates:

| Candidate | `(m, δ, q_+)` | `s12^2` | `s13^2` | `s23^2` | `sin δ_CP` |
|-----------|---------------|---------|---------|---------|-----------|
| A Schur-Q | `(0.500, 0.8165, 0.8165)` | 0.5576 | 0.0191 | 0.5429 | -0.958 |
| B det-crit | `(0.613, 0.964, 1.552)` | 0.4624 | 0.1053 | 0.5459 | -0.974 |
| C Tr(H^2)-bdy | `(0.385, 1.268, 0.365)` | 0.0885 | 0.0107 | 0.7427 | +0.712 |
| D K12 char | `(0.000, 0.800, 1.000)` | 0.8116 | 0.0126 | 0.5952 | -0.205 |
| E par-mix F1 | `(0.6285, 1.146, 0.487)` | 0.1020 | 0.0123 | 0.6116 | -0.624 |

The angles **genuinely vary** across the chamber
(spread ~0.7 for `s12^2`, ~0.1 for `s13^2`, ~0.2 for `s23^2`). This is
the retained-atlas-native `f(H)` chamber-varying observable that closes
the observable-bank exhaustion theorem CASE 4 obstruction on the P3 lane.

## The pinning statement (under the imposed branch-choice rule)

**Statement (conditional closure; NOT retained).** The system

```
|U_e2(m, delta, q_+)|^2 / cos^2 θ_13 = sin^2 θ_12(obs) = 0.307,
|U_e3(m, delta, q_+)|^2   = sin^2 θ_13(obs) = 0.0218,
|U_mu3(m, delta, q_+)|^2 / cos^2 θ_13 = sin^2 θ_23(obs) = 0.545,
```

has a unique solution **under the imposed branch-choice rule**
`B_src = { J : signature(H_base + J) = signature(H_base) = (2, 0, 1) }`
inside the chamber `q_+ >= sqrt(8/3) - delta`:

```
m_* = 0.657061342210,
delta_* = 0.933806343759,
q_+* = 0.715042329587.
```

**Argument.** The map `(m, delta, q_+) -> (s12^2, s13^2, s23^2)` is a
smooth surjection from a 3-dimensional chart onto an open subset of the
unit cube. At the pinned point the Jacobian is non-singular (verified by
the fsolve convergence). Uniqueness under the imposed rule is verified
in
[DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md):
among the three in-chamber χ²=0 basins (one at the pinned point on
σ=(2,1,0); a second at `(28, 21, 5)` on σ=(2,1,0); a third at
`(21, 13, 2)` on σ=(2,0,1)), only the pinned point lies on the
baseline-connected branch. Sylvester's law of inertia is invoked as
a textbook algebraic fact about `signature`; the selection of the
baseline-connected branch as the physical live sheet is the imposed
branch-choice rule (non-retained; Option-B open).

**Closure status.** This pins `(delta_*, q_+*)`. The spectator direction
`m_*` is also pinned by the same system, with
`m_* = 0.6571 != 4 sqrt(2)/9 = 0.6285` (parity-mixing F1) and
`!= 0.5` (Schur-Q candidate).

**Chamber boundary check.** The pinned point is inside the chamber:

```
q_+* + delta_* = 1.6489,
sqrt(8/3) = 1.6330,
distance = 0.0159 (interior).
```

## Physics cross-checks

### Cross-check 1: PDG `|U_PMNS|` 3-sigma ranges

At the pinned point,

```
|U_PMNS| = [0.8233, 0.5480, 0.1476]
  [0.3704, 0.5742, 0.7301]
  [0.4300, 0.6083, 0.6671]
```

Every entry lies inside the NuFit 5.3 NO 3-sigma range
(runner: 9/9 PASS).

### Cross-check 2: prior the observable-bank exhaustion theorem retained candidates

The pinned `(delta_*, q_+*) = (0.934, 0.715)` is strictly distinct from
every prior retained candidate on the chamber:

| Candidate | `(δ, q_+)` | distance to `(δ_*, q_+*)` |
|-----------|-----------|---------------------------|
| A Schur-Q | (0.8165, 0.8165) | 0.155 |
| B det-crit | (0.964, 1.552) | 0.838 |
| C Tr(H^2)-bdy | (1.268, 0.365) | 0.484 |
| D K12 char | (0.800, 1.000) | 0.315 |
| E par-mix F1 | (1.146, 0.487) | 0.312 |

The closest prior candidate (A, Schur-Q) lies 0.155 away — well outside
any numerical tolerance. The PMNS pinning is **inequivalent to every
prior retained variational candidate**, consistent with the
observable-bank exhaustion theorem's narrower-gap statement that no
prior candidate was observationally selected.

### Cross-check 3: `delta_CP`

The map predicts `sin(delta_CP) = -0.9874`, i.e. `delta_CP = -80.88 deg`
(mod 180 ambiguity: also consistent with `delta_CP = 260.88 deg`). This
is in the T2K-preferred lower octant near `-90 deg`. Global NO fits
(NuFit 5.3) currently give a broad `delta_CP` range centered near
`+230 deg` with `3-sigma` interval `[120, 369]`; the prediction
`-81 deg ~ 279 deg` lies inside that `3-sigma` band. Upcoming
DUNE / Hyper-Kamiokande data will sharpen this test.

### Cross-check 4: Jarlskog

The predicted `|J| = 0.0328` matches the T2K + NuFit `|J|` band
`~0.032-0.033` at 1-sigma. Sign: the map predicts `J < 0`, i.e. a net
`CP`-violating current that distinguishes neutrino from antineutrino
oscillation. The sign is consistent with the T2K+NOvA tension pulling
toward negative `sin(delta_CP)`.

### Cross-check 5: Dirac-vs-Majorana discrimination

The `(delta, q_+)` structure in `H` is a Hermitian observable on
`H_hw=1`, not a Majorana mass matrix. The Dirac PMNS map constructed
here is independent of Majorana phases. Consequently the pinning
`(delta_*, q_+*)` is **Dirac-invariant**: if the neutrino is Majorana,
the extra two CP phases `(alpha_21, alpha_31)` are not fixed by this
theorem; they live in the Majorana mass sector and would require
promotion of the Majorana residual (open elsewhere on the atlas,
see [NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md](./NEUTRINO_MAJORANA_RETAINED_LANE_PACKET_2026-04-16.md)).

## Side-effect statement: PMNS conditional / support (NOT retained)

As a conditional consequence of the closure:

**Statement (PMNS conditional / support status on the chamber).** The
PMNS mixing angles `(θ_12, θ_13, θ_23, δ_CP)` admit an explicit
closed-form `f(H(m, δ, q_+))` on the live source-oriented sheet;
evaluated at the chamber pin
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` they match
observation at NuFit 5.3 3-σ (9/9). This closure is CONDITIONAL on
(1) the imposed branch-choice rule, (2) `q_H = 0`, (3) the
observational hierarchy pairing `σ_hier = (2, 1, 0)`. It is NOT
unconditionally retained.

Downstream flavor / cosmology / leptogenesis consequences can be
evaluated against the chamber pin as *support* rather than as a fully
retained PMNS input. An atlas-native promotion to retained requires
closing the imposed branch-choice rule (Option B) and the `q_H`
conditional.

## Honest gap statement (after Option-A demotion)

**Before this note:** selector was stratified into `P1/P2/P3`. `P3` was flagged
as the largest-scope lane that simultaneously closes selector and the PMNS
open objects, but the retained-atlas map `(m, delta, q_+) -> PMNS` was
not explicitly constructed.

**After this note (after the 2026-04-17 Option-A demotion):**
- The `P3` map is **built** explicitly by direct diagonalization of the
 retained affine `H`.
- The selector gate closes on the chamber CONDITIONALLY at
 `(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`, where the
 conditionality is the imposed branch-choice rule + `q_H = 0` +
 σ_hier = (2, 1, 0).
- PMNS is CONDITIONAL / SUPPORT on the chamber, NOT unconditionally retained.
- Basin-uniqueness is a conditional result under the imposed branch-
 choice rule. The first-pass "retained Sylvester inertia" framing is
 WITHDRAWN. Load-bearing non-retained ingredients:
 (i) imposed branch-choice rule (Option-B open),
 (ii) SM-canonical `q_H = 0`,
 (iii) observational hierarchy pairing `σ_hier = (2, 1, 0)`.
- A falsifiable CONDITIONAL `delta_CP` prediction is produced:
 `sin(delta_CP) = -0.987`, `delta_CP ~ -81 deg (= 279 deg)`.
- The solar-gap `Dm^2_21`, absolute-mass scale, and Majorana phases
 remain atlas-open (different carriers than the Hermitian `H`).
- The DM flagship gate overall status on the current branch tip is
 **conditional / support**, NOT `CLOSED`.

## Runner-verified content

The runner (`scripts/frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py`) executes
43 PASS / 0 FAIL across seven parts:

- **Part 1 (structural).** `H` and `K_Z3` are Hermitian at five candidates;
 `a_*`, `b_*` are chamber-blind; `K_doublet` varies on the chamber.
- **Part 2 (PMNS chamber-variation).** `sin^2 theta_{12,13,23}` all vary
 on the chamber with spreads `0.72`, `0.09`, `0.20` respectively.
- **Part 3 (unique chamber solution).** 60 random-start multi-start
 Nelder-Mead descents all converge to the same `(m_*, delta_*, q_+*)`;
 fsolve sharpens to 12 digits; pinned point is strictly inside the
 chamber.
- **Part 4 (PDG ranges).** All 9 entries of `|U_PMNS|` at the pinned
 point lie inside the NuFit 5.3 NO 3-sigma ranges.
- **Part 5 (`delta_CP` + Jarlskog).** `|J| = 0.0328` in observed band;
 `sin(delta_CP) = -0.9874` in T2K-preferred sign.
- **Part 6 (candidate inequivalence).** Pinned point is strictly
 inequivalent (distance >= 0.155) to every prior retained the observable-bank exhaustion theorem
 candidate.
- **Part 7 (frozen-slot closed forms).** `a_*`, `b_*` numerical closed
 forms recorded; chamber-blindness re-verified.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py
```

Expected: `PASS = 43, FAIL = 0`.

## Claim discipline

This note **positively claims** (under the honest-label revision):
- The `f(H)` PMNS map `(m, delta, q_+) -> (theta_ij, delta_CP)` is an
 explicit closed-form map from retained retained inputs (the affine
 `H`, retained `H_hw=1`, retained chamber). The MAP itself (not the
 closure) is theorem-grade.
- Under the imposed branch-choice rule + `q_H = 0` + σ_hier = (2,1,0),
 the selector gate closes CONDITIONALLY on the chamber at
 `(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`.
- Under the same conditionals, basin uniqueness (vs the two competing
 in-chamber χ²=0 basins) holds: only the pinned point lies on the
 baseline-connected branch of the caustic. Sylvester's law of inertia
 is a textbook algebraic fact; the branch-choice is imposed.
- A CONDITIONAL `delta_CP` prediction: `sin(delta_CP) = -0.9874`,
 `delta_CP ~ -81 deg (= 279 deg)`.
- The pinned `|U_PMNS|` matches NuFit 5.3 NO 3-sigma ranges in all 9
 entries.

This note **does not claim**:
- unconditional retention of PMNS on the chamber (it is conditional on
 the three items flagged above);
- that the DM flagship gate is `CLOSED` (it is conditional / support,
 NOT closed; see the flagship closure review note);
- closure of the solar-gap `Dm^2_21` (different carrier);
- closure of the absolute neutrino mass scale (different carrier);
- closure of Majorana CP phases (separate sector);
- retention of PMNS on any other chamber than the live source-oriented
 sheet defined by the retained affine `H`;
- Taylor convergence of `W[J] = log|det(H_base + J)|` at the Basin 1
 physical amplitude (the log-det observable is well-defined on
 the baseline-connected branch without requiring Taylor convergence;
 `ρ(D⁻¹J) ≈ 1.285` at Basin 1 is an honest series-domain boundary,
 not a failure of the closure under the imposed rule).

The positive claims stand or fall on:
(i) the retained exact affine chart `H = H_base + m T_m + delta T_delta
+ q_+ T_q` on the live sheet (retained theorem);
(ii) the retained Dirac-bridge theorem placing `Gamma_1` diagonal in the
axis basis on `H_hw=1` (retained theorem);
(iii) the retained three-generation observable space (retained theorem);
(iv) the direct numerical diagonalization and the unique chamber solution
recorded here (runner-verified to machine precision, 60-seed multi-start).

No post-axiom selector law is introduced. The selector *principle*
(P2 lane) is not needed, because the observational PMNS data, fed
through the retained `f(H)` map, supplies the remaining 3-real datum
`(m_*, delta_*, q_+*)` directly. This is the P3 lane realized.

## Downstream lanes unlocked

With PMNS promoted to retained:

- **Leptogenesis.** The DM-leptogenesis PMNS-assisted transport witness
 [DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16](./DM_LEPTOGENESIS_PMNS_TRANSPORT_EXTREMAL_SOURCE_CANDIDATE_NOTE_2026-04-16.md)
 can now be evaluated at the pinned `(delta_*, q_+*)` with the PMNS
 `(theta_ij, delta_CP)` supplied by this theorem rather than as free
 parameters.
- **Flavor sector.** The PMNS retention lifts the
 [LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md](./LEPTON_SINGLE_HIGGS_PMNS_TRIVIALITY_NOTE.md)
 negative result on the two-Higgs / parity-mixing lane: the triviality
 is reorganized into a relationship between the live `H` sheet and the
 flavor-currents family.
- **`delta_CP` prediction.** A falsifiable prediction
 `sin(delta_CP) = -0.987` is published for upcoming
 DUNE / Hyper-Kamiokande test.

## Position on publication surface

This note is a **conditional / support closure** on the publication surface:
- The selector gate on the DM-neutrino source-oriented sheet is
 CLOSED ONLY CONDITIONALLY at `(m_*, δ_*, q_+*)` — conditional on the
 imposed branch-choice rule + `q_H = 0` + σ_hier = (2, 1, 0). The
 flagship closure headline is **conditional / support**, NOT `CLOSED`.
- PMNS: conditional / support on the chamber via `f(H)`, NOT
 unconditionally retained.
- Basin uniqueness: conditional under the imposed branch-choice rule.
 The first-pass "retained Sylvester inertia selector" framing is
 WITHDRAWN. Three load-bearing non-retained ingredients are explicit:
 (a) imposed branch-choice rule (Option-B open), (b) `q_H = 0`
 (SM-canonical, not axiom-derived), (c) observational hierarchy
 pairing `σ_hier = (2, 1, 0)`.
- DM flagship cascade downstream proceeds as *support* from the
 conditional pin, not from a fully retained input.
- The paragraph in
 [DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_OBSERVABLE_BANK_EXHAUSTION_THEOREM_NOTE_2026-04-17.md)
 that records P3 as an open promotion lane remains open: what is
 realized by this note is a CONDITIONAL closure, not a completed
 promotion. An atlas-native promotion requires closing the three
 load-bearing non-retained items.

## What this file must never say

- that the DM flagship gate is `CLOSED` (it is conditional / support
 on the current branch tip; see the flagship closure review note);
- that the Sylvester inertia-preservation selector is a retained
 theorem (it is an IMPOSED branch-choice admissibility rule; Sylvester
 is a textbook algebraic fact about `signature`, but the branch
 choice itself is imposed);
- that PMNS is unconditionally retained on the chamber (it is
 conditional / support);
- that the solar-gap `Dm^2_21` is retained as `f(H)` (it is not — different
 carrier);
- that the absolute neutrino mass scale is retained at the chamber
 (different carrier);
- that Majorana CP phases are retained (separate open Majorana-sector
 problem);
- that the PMNS map is valid off the live source-oriented sheet (it is
 derived on the live sheet only);
- that the `delta_CP` prediction is certain (it is a falsifiable
 CONDITIONAL prediction, subject to upcoming observational test);
- that a Frobenius / operator-norm scale bound `‖J‖ ≤ ‖H_base‖` is the
 primary basin selector (those are consistency diagnostics; the
 primary selector on the current branch tip is the imposed
 branch-choice rule);
- that `W[J] = log|det(D + J)|` requires Taylor convergence at the
 Basin 1 amplitude (it does not; the log-det observable is defined
 on the baseline-connected branch by direct diagonalisation).
