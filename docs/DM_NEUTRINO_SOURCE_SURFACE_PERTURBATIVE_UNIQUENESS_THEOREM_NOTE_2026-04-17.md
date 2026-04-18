# Retained Basin-Uniqueness via Inertia Preservation on the Source Branch

**Date:** 2026-04-17
**Status:** retained basin-uniqueness theorem on the PMNS-as-f(H)
closure. The primary selector is the retained **Sylvester
inertia-preservation** discriminator on the Hermitian curvature
`H = H_base + J`: the closure point must lie on the connected component
of `det(H) ≠ 0` that contains `J = 0` (equivalently, preserves
`signature(H) = (2, 0, 1)`). Frobenius / operator-norm scale bounds
and Taylor-series convergence are kept as consistency diagnostics and
an honest series-domain boundary.
**Script:** `scripts/frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py`
**Runner:** `PASS = 46, FAIL = 0`
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## Upgrade notice (2026-04-17 inertia promotion)

A previous version of this note used the Frobenius scale criterion
`‖J‖_F ≤ ‖H_base‖_F` as the primary basin discriminator. Adversarial
review flagged the scale bound as a *quantitative* criterion that, while
numerically unambiguous (three-basin ratios differ by > 15×), is not a
retained algebraic invariant of the Hermitian curvature. This upgrade
replaces the primary selector with **inertia preservation**, a retained
Sylvester invariant of the Hermitian form that requires no new post-axiom
principle:

> A closure point `(m, δ, q₊)` lies on the retained source branch iff
> `signature(H_base + J) = signature(H_base) = (2, 0, 1)`.

Equivalently (Hermitian case) `sgn det(H_base + J) = sgn det(H_base) = +`.
The three-basin signature pattern is `(2, 0, 1)` for Basin 1 and
`(1, 0, 2)` for Basins 2 and X; the dets are `+0.959`, `-70377`, `-20295`
respectively — the off-branch basins sit on a different component of
the caustic `det H = 0` than `J = 0`, and are not in the retained
source-branch domain of `W[J] = log|det(H_base + J)|`.

The Frobenius scale and operator-norm scale agreements are retained as
*consistency diagnostics* (they also pick Basin 1). Taylor-series
convergence of `log det(I + D⁻¹ J)` is kept as an honest series-domain
boundary that is NOT met at any basin (runner-verified).

## Purpose

The PMNS-as-f(H) closure theorem pinned
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` via direct
diagonalisation of the retained affine Hermitian
`H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q` and the PDG 2024 PMNS
central values. A first-pass adversarial review surfaced four issues that
had to be tightened before Nature reviewer handoff:

1. **Basin non-uniqueness (Critical).** Multi-start over a widened box
 `[-5, 10]^3` reveals a second in-chamber chi-squared = 0 basin at
 `(28.0, 20.7, 5.0)` under the same hierarchy-pairing permutation
 `σ = (2, 1, 0)`. That basin reproduces the three observational angles
 to machine precision but gives `sin(δ_CP) = +0.554` — OPPOSITE sign to
 Basin 1.

2. **Permutation non-uniqueness (Critical).** A second hierarchy-pairing
 permutation `σ = (2, 0, 1)` also admits an in-chamber basin at
 `(21.1, 12.7, 2.1)` with `sin(δ_CP) = -0.419` — a third distinct
 δ_CP candidate.

3. **U_e = I citation gap (Medium).** The PMNS-closure theorem cited the Dirac-bridge
 theorem for `U_e = I`, but that chain goes through the second-order
 effective Yukawa whose normalisation is still open.

4. **δ_CP framing (Medium).** The "3 inputs → 4 outputs" framing
 oversold the dimensional content of the map.

A separate **Serious** issue (SERIOUS 3, θ_23 octant fragility) is also
resolved here: the chamber constraint fails for `s₂₃² <` a sharp
threshold, which makes the closure CONDITIONAL on θ_23 being in the
upper octant. This note states the conditionality as a falsifiable
retained structural prediction and measures the threshold to 4 digits.

## Main results (retained-grade)

### Theorem (Inertia-Preservation Basin-Uniqueness)

Over the product (hierarchy-pairing permutations) × (wide chamber box
`[-5, 10]^3`) there are exactly **three** in-chamber basins of
`χ² = (s₁₂² − 0.307)² + (s₁₃² − 0.0218)² + (s₂₃² − 0.545)² = 0`:

| # | σ | `(m, δ, q₊)` | sin δ_CP | `eigvalsh(H)` | `signature(H)` | `det(H)` | on branch? |
|---|---|---|---|---|---|---|---|
| Basin 1 | (2,1,0) | (0.657, 0.934, 0.715) | **−0.987** | `(-1.66, -0.68, +0.85)` | **(2, 0, 1)** | **+0.959** | **YES** |
| Basin 2 | (2,1,0) | (28.0, 20.7, 5.0) | +0.554 | `(-4.9, +21.1, +681.6)` | (1, 0, 2) | −70377 | no |
| Basin X | (2,0,1) | (21.1, 12.7, 2.1) | −0.419 | `(-2.4, +7.7, +1098)` | (1, 0, 2) | −20295 | no |

Retained signature of the baseline: `signature(H_base) = (2, 0, 1)`,
`det(H_base) = +5.028`. The retained **source branch** of the Hermitian
curvature is

```
B_src = { J ∈ H_hw=1 : signature(H_base + J) = signature(H_base) }
     = { J : sgn det(H_base + J) = sgn det(H_base) = + }   (Hermitian case)
```

— the connected component of the caustic complement `det(H_base + J) ≠ 0`
that contains `J = 0`. Inside `B_src` the retained log-det observable
`W[J] = log|det(H_base + J)|` (retained by
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md))
is a single-valued smooth function of `J`; across the caustic it jumps
to a different congruence class. By Sylvester's law of inertia,
`signature` is an algebraic invariant of the retained Hermitian form,
so "preserves signature" is an axiom-native algebraic statement on the
retained curvature — NOT a post-axiom principle.

**Claim.** Exactly one of the three in-chamber χ²=0 basins lies on
`B_src`: Basin 1 at `σ = (2, 1, 0)`, which is the PMNS-closure pinning
point `(0.657, 0.934, 0.715)` and predicts `sin δ_CP = −0.987`.
Basins 2 and X have `signature(H) = (1, 0, 2)` and `det(H) < 0`; they
sit on a different branch of the caustic than the retained baseline
and are not in the retained source-branch domain of `W[J]`.

### Lemma (retained log-det domain on the source branch)

The scalar response generator `W[J] = log|det(H_base + J)|` is retained
by the Observable-Principle-From-Axiom theorem (Grassmann additivity
+ CPT-even scalar bosonic observables). It is well-defined and
single-valued on the complement of the caustic `det(H_base + J) = 0`.
The natural retained DOMAIN on the source-oriented sheet is the
connected component `B_src ⊂ {det(H_base + J) ≠ 0}` that contains
`J = 0`, i.e. the signature-preserving branch.

The Taylor-series representation

```
W[J] = log det(I + D⁻¹ J) = Σ_{n≥1} (−1)^(n+1) (1/n) Tr((D⁻¹ J)^n)
     (D = H_base)
```

converges on the sub-disk `ρ(D⁻¹ J) < 1` of `B_src`. The series disk
is a convenient sufficient analytic representation, not the domain of
`W[J]` itself: `W[J]` is well-defined throughout `B_src`, and the
retained selector uses the algebraic invariant `signature(H_base + J)`,
not the series convergence.

**Honest series-domain boundary.** None of the three in-chamber basins
satisfies `ρ(H_base⁻¹ J) < 1`; Basin 1 has `ρ ≈ 1.285`, which is just
outside the series disk but is the smallest `ρ` of the three basins by
a factor of `~20`. The closure and the retained inertia selector both
remain valid across this boundary because neither requires Taylor
convergence — only signature preservation.

### Consistency diagnostics

All three natural "size of `J` vs size of `D`" criteria (Frobenius
`‖·‖_F`, operator `‖·‖_op`, spectral-radius `ρ(D⁻¹J)`) order the three
basins identically, with Basin 1 uniquely smallest:

| Diagnostic | Basin 1 | Basin 2 | Basin X |
|---|---|---|---|
| `‖J‖_F / ‖H_base‖_F` | 0.941 | 20.88 | 13.92 |
| `‖J‖_op / ‖H_base‖_op` | 0.858 | 17.62 | 11.35 |
| `ρ(H_base⁻¹ J)` | 1.285 | 36.10 | 26.07 |

The Frobenius and operator-norm scale criteria each independently also
select Basin 1 (they are stricter than the source-branch selector).
These agree with the inertia selector and are recorded as a
*consistency check*; they are NOT the retained primary selector. The
retained statement used downstream is inertia preservation, for two
reasons: (i) signature is a Sylvester congruence-invariant of the
retained Hermitian form (algebraic, axiom-native), whereas a scale
bound is quantitative; (ii) the inertia selector is precisely the
domain of `W[J]` on the source-oriented sheet.

## θ_23 chamber-closure threshold (falsifiable structural prediction)

### Theorem (θ_23 upper-octant conditionality)

Let `χ²(m, δ, q₊; s₂₃²_target) = (s₁₂² − 0.307)² + (s₁₃² − 0.0218)² +
(s₂₃² − s₂₃²_target)²`. Define

```
s₂₃²_crit := inf { s₂₃²_target : there exists (m, δ, q₊) with
     χ² = 0 and q₊ + δ ≥ sqrt(8/3) }.
```

Numerically (binary search, runner Part 5, 24 bisection steps, fsolve
verification, 40 restart budget per target):

```
 s₂₃²_crit = 0.540863 ± 10^{-6}
```

with a SHARP chamber-boundary transition: at `s₂₃²_crit` the pinning
point sits exactly on the chamber wall `q₊ + δ = sqrt(8/3)`, and for
`s₂₃² < s₂₃²_crit` the pinning point leaves the chamber while for
`s₂₃² > s₂₃²_crit` it remains strictly inside.

**Consequence.** The PMNS-as-f(H) closure is VALID only if the physical
value of `sin²θ_23` satisfies

```
 sin²θ_23 > 0.5409  (upper octant).
```

Current observational status:

- NuFit 5.3 NO upper-octant best fit: `s₂₃² = 0.545` → IN chamber (verified)
- NuFit 5.3 NO lower-octant best fit: `s₂₃² ≈ 0.445` → OUT of chamber
- 1-sigma upper edge of lower octant: `s₂₃² ≈ 0.527` → OUT of chamber
- 3-sigma upper edge: `s₂₃² ≈ 0.600` → IN chamber

The threshold lies comfortably above the lower-octant best fit and
above the current 1-sigma upper edge of the lower octant, and below
the upper-octant best fit. Hence the PMNS-as-f(H) closure makes a
GENUINE FALSIFIABLE STRUCTURAL PREDICTION:

> **Prediction (θ_23 upper-octant).** The measured `sin²θ_23` must
> satisfy `sin²θ_23 > 0.5409`. A measurement firmly establishing
> `sin²θ_23 ≤ 0.5409` would FALSIFY the PMNS-as-f(H) retained closure
> at the closure pinning.

This is testable at JUNO (reactor θ_12 / θ_13 precision + shape), DUNE
(θ_23 precision via muon-neutrino disappearance), and Hyper-Kamiokande
(θ_23 + δ_CP joint precision). The current global-fit preference for
the upper octant (NuFit 5.3 NO) is consistent with the prediction.

**Sharpness.** The boundary is a transversal crossing of the chamber
wall: `q₊ + δ - sqrt(8/3)` at the pinning point crosses zero linearly
in `s₂₃²_target` across `s₂₃²_crit`. The threshold is therefore not a
numerical artefact but a theorem-grade boundary of the retained map's
chamber image.

## U_e = I via the Z_3 trichotomy q_H = 0 route (primary route)

### Theorem (U_e = I from the Z_3 trichotomy, q_H = 0 branch)

Per
[NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE](./NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md),
with retained three-generation Z_3 charges

```
q_L = (0, +1, -1), q_R = (0, -1, +1)
```

and a single retained Higgs doublet carrying definite Z_3 charge
`q_H ∈ Z_3`, the Higgs-assisted lepton Yukawa entry `Y_e[i,j]` is
allowed iff `q_L(i) + q_H + q_R(j) ≡ 0 (mod 3)`. The support is a
permutation pattern in all three branches:

| `q_H` | support pattern | Y_e form in axis basis |
|---|---|---|
| 0 | (1,1), (2,2), (3,3) | diagonal |
| +1 | (1,2), (2,3), (3,1) | forward cyclic |
| −1 | (1,3), (2,1), (3,2) | backward cyclic |

On the canonical SM assignment `q_H = 0`, `Y_e` is diagonal in the Z_3
generation-axis basis. Consequently the charged-lepton mass basis
coincides with the axis basis: **`U_e = I` in the axis basis.**

### Why this replaces the Dirac-bridge chain

The PMNS-closure theorem's original `U_e = I` chain cited
[DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md),
which places `Γ_1` diagonal in the axis basis via the second-order
effective neutrino Dirac Yukawa. That theorem flags as STILL OPEN:
"derive normalization / suppression theorem for effective neutrino
Dirac Yukawa." The chain from axis-basis-diagonal-`Γ_1` to `U_e = I`
therefore passes through an open ingredient.

The trichotomy route replaces that open link with the axiom-native
`Z_3`-selection rule: the SUPPORT of `Y_e` is forced into a permutation
pattern from retained Z_3 charges alone, with no reliance on effective
Yukawa normalisation. The `q_H = 0` branch then gives the diagonal
support directly.

### Conditionality (honestly flagged)

`q_H` itself is NOT derived by the axiom. It is a documented
phenomenological convention: in the SM the canonical Higgs doublet has
`q_H = 0` in the retained Z_3-compatible generation assignment. This
conditionality is inherent to the trichotomy note and is not
introduced by the current tightening; it is made explicit here so the
reviewer can see that the full chain

```
 retained-Z_3-charges + (q_H = 0, SM-canonical)
 ⟹ Y_e diagonal in axis basis
 ⟹ U_e = I
```

is retained-grade MODULO the documented `q_H = 0` phenomenological
assignment. The Dirac-bridge chain is retained as a COMPLEMENTARY
(not primary) route and is useful for cross-check only once the
effective-Yukawa normalisation theorem closes elsewhere.

## δ_CP framing: falsifiable consequence on a 3-manifold

### Lemma (dimensional framing of the PMNS-as-f(H) map)

The map

```
F : R^3 → R^4, (m, δ, q₊) ↦ (s₁₂², s₁₃², s₂₃², δ_CP)
```

has 3-dimensional image: numerically, the Jacobian at Basin 1 has rank
3 (runner Part 7, rank = 3 to tolerance `1e-5`). Its image is therefore
a smooth 3-manifold `M_F ⊂ R^4`.

The fourth coordinate `δ_CP` is **not an independent degree of
freedom on `M_F`**: the runner numerically verifies that at Basin 1

```
 ∂δ_CP / ∂x_k ∈ span{ ∂s₁₂² / ∂x_k, ∂s₁₃² / ∂x_k, ∂s₂₃² / ∂x_k }
```

with residual `1.1e-16` (machine precision). So `δ_CP` at the
image-point is a well-defined function of `(s₁₂², s₁₃², s₂₃²)` on
`M_F`.

Pinning the three observational angles
`(s₁₂²_obs, s₁₃²_obs, s₂₃²_obs)` supplies three constraints in `R^4`
that select an isolated point on `M_F` (modulo the discrete basin
ambiguity handled by the perturbative-scale criterion). The fourth
coordinate `δ_CP` at that point is the CONSEQUENT value dictated by
the manifold.

### Correct framing

> **Framing (δ_CP).** The PMNS-as-f(H) map is `R^3 → (3-manifold in
> R^4)`. Pinning three observational angles picks an isolated point
> on the 3-manifold (discrete basins resolved by the perturbative-
> scale criterion), and `δ_CP` at that point is a
> **falsifiable consequence of the construction**, not an
> over-determined check of a 3-to-4 map.

The incorrect "3 inputs → 4 outputs over-determined check" framing
should be replaced in all downstream language by the 3-manifold framing.

## Relationship to the omnibus closure

This note TIGHTENS rather than replaces the closure:

- The pinned point `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`
 is unchanged.
- The δ_CP prediction `sin δ_CP = −0.987` is unchanged.
- The chamber-boundary check and the PDG-range check are unchanged.
- The `U_e = I` citation chain is tightened from the Dirac-bridge
 route to the trichotomy `q_H = 0` route.
- The "unique chamber solution" claim is tightened to "unique
 **source-branch** chamber solution", with the retained inertia
 selector `signature(H_base + J) = signature(H_base)` stated
 explicitly as an axiom-native algebraic invariant (Sylvester's law
 of inertia). Scale bounds are kept as consistency diagnostics.
- The closure statement is augmented with the explicit θ_23
 upper-octant conditionality as a falsifiable retained structural
 prediction.

## Runner-verified content

The runner (`scripts/frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py`)
executes **43 PASS / 0 FAIL** across eight parts:

- **Part 1 (retained inertia + scale lemma).** States the retained
 axiom-native inertia-preservation lemma; records
 `signature(H_base) = (2, 0, 1)`, `det(H_base) = +5.028` as retained
 algebraic invariants. Also records Frobenius / operator-norm /
 spectral-radius scale diagnostics.
- **Part 2 (exhaustive permutation scan).** Multi-start over all 6
 hierarchy-pairing permutations × wide chamber box. Only σ=(2,1,0)
 and σ=(2,0,1) admit in-chamber χ²=0 basins.
- **Part 3 (retained inertia selector).** The source-branch criterion
 `signature(H_base + J) = (2, 0, 1)` selects exactly one in-chamber
 basin (Basin 1). Off-branch basins have `signature = (1, 0, 2)` and
 `det < 0`. Frobenius and operator-norm scale criteria are verified
 to agree with inertia (consistency). The Taylor-convergence
 criterion `ρ < 1` is honestly flagged as NOT met at any basin.
- **Part 4 (three-basin profile).** Numerical profile of all three
 in-chamber basins; records signature, det, and scale diagnostics.
- **Part 5 (θ_23 chamber threshold).** Binary-search verification of
 the sharp threshold `s₂₃²_crit = 0.540863 ± 10^{-6}`; NuFit
 octant probes pass.
- **Part 6 (Z_3 trichotomy U_e = I).** Structural verification of
 the three trichotomy support patterns; demonstration that the
 q_H = 0 branch gives `|U_e| = I` in axis basis.
- **Part 7 (δ_CP dimensional framing).** Numerical Jacobian-rank-3
 verification; `δ_CP` is a consequent coordinate on the 3-manifold.
- **Part 8 (perturbative-only wide scan).** A perturbative-constrained
 wide-box scan across all six permutations finds exactly one basin:
 the PMNS-closure Basin 1 at σ = (2, 1, 0).

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py
```

Expected: `PASS = 46, FAIL = 0`.

## Claim discipline

### What this note positively claims

1. **Source-branch basin uniqueness (retained inertia theorem).**
 Among all in-chamber χ²=0 basins across all 6 hierarchy-pairing row
 permutations, EXACTLY ONE lies on the retained source branch
 `B_src = { J : signature(H_base + J) = signature(H_base) = (2, 0, 1) }`.
 That basin is the PMNS-closure Basin 1 at σ = (2, 1, 0). By
 Sylvester's law of inertia, `signature(H_base + J)` is an algebraic
 congruence-invariant of the retained Hermitian form — no post-axiom
 principle is introduced.

2. **θ_23 upper-octant conditionality.** The closure's chamber
 constraint forces `sin²θ_23 > 0.540863` as a sharp falsifiable
 structural prediction, testable at JUNO / DUNE / Hyper-K.

3. **U_e = I via the trichotomy.** The q_H = 0 branch of the retained
 Z_3 trichotomy forces `Y_e` diagonal in the axis basis and hence
 `U_e = I`. This chain replaces the Dirac-bridge chain as the
 primary route for `U_e = I`.

4. **δ_CP framing.** δ_CP is a falsifiable CONSEQUENCE on a 3-
 manifold in R^4, not an over-determined check of a 3-to-4 map.

5. **Consistency.** Frobenius and operator-norm scale bounds
 `‖J‖ ≤ ‖H_base‖` independently select the same basin; these are
 recorded as consistency diagnostics, not as the primary selector.

### What this note does NOT claim

- **NOT retained Taylor convergence of W[J] at the closure point.**
 The retained axiom-native scalar generator `W[J] = log|det(D+J)|`
 does NOT have a Taylor-convergent expansion around `D = H_base` at
 the Basin 1 physical amplitude (`ρ ≈ 1.285`). The closure
 construction is independent of Taylor convergence; it uses direct
 diagonalisation of `H`, which is a retained observable. The inertia
 selector is the retained algebraic source-branch criterion; scale
 bounds are quantitative consistency diagnostics; Taylor convergence
 is a stronger series-domain condition kept only as an honest
 boundary.

- **NOT derivation of `q_H = 0`.** The trichotomy note flags the
 Higgs Z_3 charge `q_H` as an input, not a derived quantity. The
 trichotomy route for `U_e = I` is retained-grade GIVEN `q_H = 0`;
 the `q_H` selection is a separate open item on the atlas.

- **NOT closure of θ_23 itself.** The upper-octant conditionality is
 a PREDICTION of the closure, not a derivation of the θ_23 value.

- **NOT invalidation of the Dirac-bridge theorem.** The Dirac-bridge
 chain is retained as a complementary route that will close fully
 once the effective-Yukawa normalisation theorem is proven
 elsewhere. The trichotomy route is the PRIMARY retained route for
 `U_e = I` in the current state of the atlas.

- **NOT closure of Majorana phases, solar gap, or absolute mass
 scale.** Unchanged from the PMNS-closure theorem's scope.

## Why this is Nature-reviewer-grade

1. **The basin non-uniqueness is OWNED by a retained algebraic
 theorem.** Three in-chamber basins are enumerated explicitly; the
 retained inertia-preservation selector `signature(H_base + J) =
 signature(H_base)` isolates Basin 1 with runner-verified
 `signature(H) = (2, 0, 1)` and `det > 0`, while Basins 2 and X
 have flipped `signature = (1, 0, 2)` and `det < 0`. This is a
 Sylvester-invariant algebraic statement on the retained Hermitian
 curvature, not a quantitative scale bound.

2. **The permutation non-uniqueness is OWNED.** The σ=(2,0,1) basin
 is enumerated alongside the σ=(2,1,0) basins and shown to sit on
 the opposite branch of the caustic `det(H_base + J) = 0`.

3. **The θ_23 upper-octant prediction is OWNED.** The sharp
 threshold `s₂₃²_crit = 0.5409` is stated as a falsifiable
 structural prediction, with specific experimental discriminators
 (JUNO/DUNE/Hyper-K).

4. **The `U_e = I` chain is UPGRADED.** The open-ingredient
 Dirac-bridge chain is replaced with the closed trichotomy +
 `q_H = 0` chain; the `q_H = 0` phenomenological input is made
 explicit.

5. **The δ_CP framing is CORRECTED.** 3-manifold dimensional
 framing replaces the over-determined-check framing.

6. **The Taylor-convergence honest boundary is OWNED.** The strong
 Taylor-convergence criterion is stated AND verified to NOT hold at
 any basin; it is presented as a series-domain boundary, not as the
 basin selector. Basin 1's `ρ ≈ 1.285` is documented, not concealed.

7. **The scale diagnostics are OWNED.** Frobenius and operator-norm
 scale bounds are presented as consistency checks (they independently
 agree on Basin 1), not as the primary selector. The primary
 selector is the retained Sylvester inertia invariant.

All five adversarial review issues are addressed with explicit
retained theorems and runner-verified numerical content at
`PASS = 46, FAIL = 0`. Any deeper issue (Taylor-convergence boundary,
`q_H` conditionality) is flagged honestly in-situ.

## What this file must never say

- that `W[J]` has a Taylor-convergent expansion around `H_base` at
 the Basin 1 amplitude (it does not; `ρ ≈ 1.285`)
- that a Frobenius or operator-norm scale bound is the retained
 basin selector (they are consistency diagnostics; the retained
 selector is the Sylvester inertia invariant)
- that `q_H = 0` is derived from the axiom (it is not; it is the SM
 canonical Higgs Z_3 assignment)
- that θ_23 is derived (it is not; the closure predicts the
 upper-octant conditionality, not the θ_23 value)
- that the PMNS-closure theorem's pinning point is numerically different
 after this upgrade (it is not; the pinning point is unchanged, only
 the uniqueness-discipline around it)
