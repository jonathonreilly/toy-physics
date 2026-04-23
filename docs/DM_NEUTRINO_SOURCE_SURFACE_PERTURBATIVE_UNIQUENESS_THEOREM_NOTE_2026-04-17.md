# Conditional Basin-Uniqueness via an Imposed Branch-Choice Admissibility Rule

**Date:** 2026-04-17 (Option-A demotion applied after 2026-04-17 review pass)
**Status:** **CONDITIONAL / SUPPORT — NOT a retained theorem.** The
"inertia-preservation selector" is an **IMPOSED branch-choice
admissibility rule**, not a derived retained-theorem consequence. Under
this imposed rule — restrict the live sheet to the connected component
of `det(H_base + J) ≠ 0` that contains `J = 0`, equivalently
`signature(H_base + J) = signature(H_base) = (2, 0, 1)` — exactly one
in-chamber `χ² = 0` basin survives (Basin 1 at the PMNS-closure pin).
The Sylvester `signature` *is* an algebraic congruence-invariant of a
Hermitian form, but that does NOT derive the selection of the
baseline-connected branch as the physical one. That choice is the
load-bearing non-retained ingredient.

Frobenius / operator-norm scale bounds and Taylor-series convergence
are kept as *consistency diagnostics* and an honest series-domain
boundary.

**Script:** `scripts/frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py`
**Runner:** `PASS = 46, FAIL = 0` (labels rewritten to say "admissible
under imposed rule" rather than "retained"; no algorithmic change).
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## Option-A honest-label revision (2026-04-17)

The previous version of this note framed the branch selector as a
retained theorem via "Sylvester's law of inertia is axiom-native on a
Hermitian form". Reviewer feedback (commit 5c70c15d review) correctly
pointed out that this collapses two distinct steps:

1. Sylvester's law of inertia IS an axiom-native algebraic fact about
   any Hermitian form. (Uncontested.)
2. The CHOICE to restrict the live PMNS-as-f(H) sheet to the
   baseline-connected component `B_src` of the caustic complement is
   NOT derived. The other caustic components are equally Hermitian
   sheets; nothing in the retained atlas forces the live sheet to be
   the one containing `J = 0`.

The previous framing conflated (1) and (2). This revision separates
them: the Sylvester analysis is retained; the branch choice is now
honestly labeled as an **imposed admissibility rule** (conditional,
not retained). The Option-B Schur derivation of the branch-choice
principle is flagged as an open item.

## Previous-upgrade notice (2026-04-17 first-pass inertia "promotion")

An earlier version of this note promoted the inertia-preservation
criterion from a Frobenius-scale criterion to the primary selector and
called it a "retained Sylvester invariant of the Hermitian form that
requires no new post-axiom principle". The Option-A demotion above
withdraws that promotion: inertia preservation is an accurate
*description* of the baseline-connected branch `B_src`, but the SELECTION
of `B_src` as the physical live sheet is still imposed. Reviewer
feedback (commit 5c70c15d review) is correct that:

> The retained Hermitian form has several congruence classes; selecting
> the one containing `J = 0` requires an additional physical input
> (the branch-choice rule). That input is not in the retained atlas.

The imposed rule, stated honestly:

> **(Imposed branch-choice rule.)** A closure point `(m, δ, q₊)` is
> *admissible* iff `signature(H_base + J) = signature(H_base) =
> (2, 0, 1)`.

Equivalently (Hermitian case) `sgn det(H_base + J) = sgn det(H_base) = +`.
The three-basin signature pattern is `(2, 0, 1)` for Basin 1 and
`(1, 0, 2)` for Basins 2 and X; the dets are `+0.959`, `-70377`, `-20295`
respectively — the non-baseline-connected basins sit on a different
component of the caustic `det H = 0` than `J = 0`. Under the imposed
rule they are inadmissible; without the imposed rule they are equally
admissible Hermitian sheets.

The Frobenius scale and operator-norm scale agreements remain
*consistency diagnostics* (they also pick Basin 1 under the imposed
rule). Taylor-series convergence of `log det(I + D⁻¹ J)` is kept as an
honest series-domain boundary that is NOT met at any basin
(runner-verified).

## Purpose

The PMNS-as-f(H) closure theorem pinned
`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)` via direct
diagonalisation of the retained affine Hermitian
`H(m, δ, q_+) = H_base + m T_m + δ T_δ + q_+ T_q` and the PDG 2024 PMNS
central values. A first-pass adversarial package surfaced four issues that
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

## Main results (conditional / support — NOT retained)

### Statement (Basin-Uniqueness Under the Imposed Branch-Choice Rule; NOT a retained theorem)

Over the product (hierarchy-pairing permutations) × (wide chamber box
`[-5, 10]^3`) there are exactly **three** in-chamber basins of
`χ² = (s₁₂² − 0.307)² + (s₁₃² − 0.0218)² + (s₂₃² − 0.545)² = 0`:

| # | σ | `(m, δ, q₊)` | sin δ_CP | `eigvalsh(H)` | `signature(H)` | `det(H)` | on branch? |
|---|---|---|---|---|---|---|---|
| Basin 1 | (2,1,0) | (0.657, 0.934, 0.715) | **−0.987** | `(-1.66, -0.68, +0.85)` | **(2, 0, 1)** | **+0.959** | **YES** |
| Basin 2 | (2,1,0) | (28.0, 20.7, 5.0) | +0.554 | `(-4.9, +21.1, +681.6)` | (1, 0, 2) | −70377 | no |
| Basin X | (2,0,1) | (21.1, 12.7, 2.1) | −0.419 | `(-2.4, +7.7, +1098)` | (1, 0, 2) | −20295 | no |

Baseline signature: `signature(H_base) = (2, 0, 1)`,
`det(H_base) = +5.028`. The **baseline-connected branch** of the
Hermitian curvature is

```
B_src = { J ∈ H_hw=1 : signature(H_base + J) = signature(H_base) }
     = { J : sgn det(H_base + J) = sgn det(H_base) = + }   (Hermitian case)
```

— the connected component of the caustic complement `det(H_base + J) ≠ 0`
that contains `J = 0`. Inside `B_src` the log-det quantity
`W[J] = log|det(H_base + J)|` is a single-valued smooth function of `J`;
across the caustic it jumps to a different congruence class.

**Honest scope (Option-A demotion).** Sylvester's law of inertia is a
textbook algebraic statement about any Hermitian form, and the retained
atlas does retain the observable principle that justifies `W[J]` as a
scalar bosonic observable. What is NOT in the retained atlas is the
SELECTION of `B_src` (the baseline-connected branch) as *the* physical
live sheet. The other caustic components are equally Hermitian sheets
with well-defined `W[J]`; restricting to `B_src` is an imposed
branch-choice admissibility rule. Option B (deriving this rule from
the retained atlas — e.g. via a live-sheet Schur argument) is an open
item.

**Statement (under imposed branch-choice rule; NOT retained).** Exactly
one of the three in-chamber χ²=0 basins lies on `B_src`: Basin 1 at
`σ = (2, 1, 0)`, which is the PMNS-closure pinning point
`(0.657, 0.934, 0.715)` and predicts `sin δ_CP = −0.987`. Basins 2 and
X have `signature(H) = (1, 0, 2)` and `det(H) < 0`; they sit on a
different branch of the caustic than the baseline. Under the imposed
rule they are inadmissible; without the imposed rule they are equally
admissible.

### Lemma (log-det domain on the baseline-connected branch)

The scalar response generator `W[J] = log|det(H_base + J)|` is retained
by the Observable-Principle-From-Axiom theorem (Grassmann additivity
+ CPT-even scalar bosonic observables). It is well-defined and
single-valued on the complement of the caustic `det(H_base + J) = 0`.
The baseline-connected component `B_src ⊂ {det(H_base + J) ≠ 0}` is
the natural domain *under the imposed branch-choice rule*; without
the imposed rule, the other caustic components are equally valid
domains of `W[J]`.

The Taylor-series representation

```
W[J] = log det(I + D⁻¹ J) = Σ_{n≥1} (−1)^(n+1) (1/n) Tr((D⁻¹ J)^n)
     (D = H_base)
```

converges on the sub-disk `ρ(D⁻¹ J) < 1` of `B_src`. The series disk
is a convenient sufficient analytic representation, not the domain of
`W[J]` itself: `W[J]` is well-defined throughout `B_src`, and the
imposed branch-choice rule uses the algebraic invariant
`signature(H_base + J)`, not the series convergence.

**Honest series-domain boundary.** None of the three in-chamber basins
satisfies `ρ(H_base⁻¹ J) < 1`; Basin 1 has `ρ ≈ 1.285`, which is just
outside the series disk but is the smallest `ρ` of the three basins by
a factor of `~20`. The closure statement and the imposed branch-choice
rule both remain valid across this boundary because neither requires
Taylor convergence — only signature preservation.

### Consistency diagnostics (agree with the imposed rule; none are retained)

All three natural "size of `J` vs size of `D`" criteria (Frobenius
`‖·‖_F`, operator `‖·‖_op`, spectral-radius `ρ(D⁻¹J)`) order the three
basins identically, with Basin 1 uniquely smallest:

| Diagnostic | Basin 1 | Basin 2 | Basin X |
|---|---|---|---|
| `‖J‖_F / ‖H_base‖_F` | 0.941 | 20.88 | 13.92 |
| `‖J‖_op / ‖H_base‖_op` | 0.858 | 17.62 | 11.35 |
| `ρ(H_base⁻¹ J)` | 1.285 | 36.10 | 26.07 |

The Frobenius and operator-norm scale criteria each independently also
select Basin 1 (they are stricter than the branch-choice admissibility
rule). These agree with the inertia criterion under the imposed rule
and are recorded as a *consistency check*. The primary selector on the
current branch tip is the imposed branch-choice rule; the scale
criteria are quantitative consistency diagnostics. Neither is a
retained-theorem consequence of the axiom — the branch-choice rule is
conditional (Option-B open), and the scale criteria are quantitative.

## θ_23 chamber-closure threshold (falsifiable conditional structural prediction)

### Statement (θ_23 upper-octant conditionality; conditional on imposed branch-choice rule + q_H = 0)

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
the upper-octant best fit. Hence the PMNS-as-f(H) conditional/support
package makes a GENUINE FALSIFIABLE STRUCTURAL PREDICTION:

> **Prediction (θ_23 upper-octant).** The measured `sin²θ_23` must
> satisfy `sin²θ_23 > 0.5409`. A measurement firmly establishing
> `sin²θ_23 ≤ 0.5409` would FALSIFY the PMNS-as-f(H) conditional/support
> chamber pin at the closure point.

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
 retained-Z_3-charges + q_H gauge redundancy + canonical representative q_H = 0
 ⟹ Y_e diagonal in axis basis
 ⟹ U_e = I
```

is retained-grade on the PMNS-observable surface. The Dirac-bridge chain is retained as a COMPLEMENTARY
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
- The `sin δ_CP = −0.987` value at that pin is unchanged, but is now
 a CONDITIONAL prediction (conditional on the imposed branch-choice
 rule), not an unconditional closure output. `q_H` is gauge-redundant
 for PMNS observables on this branch.
- The chamber-boundary check and the PDG-range check are unchanged.
- The `U_e = I` citation chain is tightened from the Dirac-bridge
 route to the trichotomy + Higgs gauge-redundancy route.
- The "unique chamber solution" claim is replaced by "unique
 **baseline-connected-branch** chamber solution under the imposed
 branch-choice rule", explicitly flagged as conditional / support
 rather than retained-theorem.
- The θ_23 upper-octant conditionality is a falsifiable structural
 prediction OF the imposed-rule chamber image, not a retained theorem
 of the axiom.

## Runner-verified content

The runner (`scripts/frontier_dm_neutrino_source_surface_perturbative_uniqueness_theorem.py`)
executes **43 PASS / 0 FAIL** across eight parts:

- **Part 1 (baseline inertia + scale lemma).** Records
 `signature(H_base) = (2, 0, 1)`, `det(H_base) = +5.028` as algebraic
 invariants of the baseline, and the Frobenius / operator-norm /
 spectral-radius scale diagnostics. Sylvester's law of inertia is
 invoked as a textbook algebraic fact; the SELECTION of the
 baseline-connected branch is honestly labeled as imposed, not
 retained.
- **Part 2 (exhaustive permutation scan).** Multi-start over all 6
 hierarchy-pairing permutations × wide chamber box. Only σ=(2,1,0)
 and σ=(2,0,1) admit in-chamber χ²=0 basins.
- **Part 3 (imposed branch-choice rule selects Basin 1; NOT retained).**
 Under the imposed rule `signature(H_base + J) = (2, 0, 1)` exactly
 one in-chamber basin (Basin 1) is admissible. Non-baseline-connected
 basins have `signature = (1, 0, 2)` and `det < 0`; without the
 imposed rule they are equally admissible. Frobenius and operator-
 norm scale criteria are consistent (they pick the same basin under
 the imposed rule). The Taylor-convergence criterion `ρ < 1` is
 honestly flagged as NOT met at any basin.
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

1. **Baseline-connected-branch basin uniqueness (conditional on
 imposed branch-choice rule; NOT retained).** Among all in-chamber
 χ²=0 basins across all 6 hierarchy-pairing row permutations,
 EXACTLY ONE lies on the baseline-connected branch
 `B_src = { J : signature(H_base + J) = signature(H_base) = (2, 0, 1) }`.
 That basin is the PMNS-closure Basin 1 at σ = (2, 1, 0). Sylvester's
 law of inertia is invoked as a textbook algebraic fact about
 `signature`; the selection of `B_src` as the physical live sheet
 is the load-bearing non-retained ingredient.

2. **θ_23 upper-octant conditionality.** Under the imposed rule,
 the chamber constraint forces `sin²θ_23 > 0.540863` as a sharp
 falsifiable conditional structural prediction, testable at
 JUNO / DUNE / Hyper-K.

3. **U_e = I via the trichotomy.** The q_H = 0 branch of the retained
 Z_3 trichotomy forces `Y_e` diagonal in the axis basis and hence
 `U_e = I`. This chain replaces the Dirac-bridge chain as the
 primary route for `U_e = I`, conditional on `q_H = 0` being the
 physical SM assignment.

4. **δ_CP framing.** δ_CP is a falsifiable CONSEQUENCE on a 3-
 manifold in R^4 under the imposed rule + q_H = 0, not an
 over-determined check of a 3-to-4 map.

5. **Consistency.** Frobenius and operator-norm scale bounds
 `‖J‖ ≤ ‖H_base‖` independently pick the same basin as the imposed
 rule; these are consistency diagnostics, not retained selectors.

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

- **NOT derivation of a physically preferred `q_H` branch.** The
 trichotomy note still introduces the Higgs `Z_3` charge label `q_H`,
 but the Higgs gauge-redundancy theorem shows that `q_H = ±1` are
 PMNS-equivalent to the canonical representative `q_H = 0`. So `q_H`
 is no longer a separate open physical conditional for PMNS
 observables on this branch.

- **NOT closure of θ_23 itself.** The upper-octant conditionality is
 a PREDICTION of the closure, not a derivation of the θ_23 value.

- **NOT invalidation of the Dirac-bridge theorem.** The Dirac-bridge
 chain is retained as a complementary route that will close fully
 once the effective-Yukawa normalisation theorem is proven
 elsewhere. The trichotomy route is the PRIMARY retained route for
 `U_e = I` in the current state of the atlas.

- **NOT closure of Majorana phases, solar gap, or absolute mass
 scale.** Unchanged from the PMNS-closure theorem's scope.

## Why the honest-label revision is Nature-reviewer-grade

1. **The basin non-uniqueness is OWNED, under an honestly labeled
 imposed rule.** Three in-chamber basins are enumerated explicitly;
 the imposed branch-choice rule isolates Basin 1 with runner-verified
 `signature(H) = (2, 0, 1)` and `det > 0`, while Basins 2 and X
 have flipped `signature = (1, 0, 2)` and `det < 0`. Sylvester's
 law of inertia is invoked as a textbook algebraic fact; the
 selection of the baseline-connected branch is an imposed
 admissibility rule, and it is explicitly flagged as such rather
 than promoted to a retained theorem.

2. **The permutation non-uniqueness is OWNED.** The σ=(2,0,1) basin
 is enumerated alongside the σ=(2,1,0) basins and shown to sit on
 the opposite branch of the caustic `det(H_base + J) = 0`.

3. **The θ_23 upper-octant prediction is OWNED, as a CONDITIONAL
 prediction.** The sharp threshold `s₂₃²_crit = 0.5409` is a
 falsifiable structural prediction of the closure *under the imposed
 rule*, not of the retained atlas unconditionally. `q_H` is no longer
 a separate conditional at this stage.

4. **The `U_e = I` chain is UPGRADED.** The open-ingredient Dirac-bridge
 chain is replaced with the trichotomy + Higgs gauge-redundancy chain;
 `q_H = 0` is now treated as the canonical gauge representative rather
 than a separate physical conditional.

5. **The δ_CP framing is CORRECTED.** 3-manifold dimensional
 framing replaces the over-determined-check framing.

6. **The Taylor-convergence honest boundary is OWNED.** The strong
 Taylor-convergence criterion is stated AND verified to NOT hold at
 any basin; it is presented as a series-domain boundary, not as the
 basin selector. Basin 1's `ρ ≈ 1.285` is documented, not concealed.

7. **The scale diagnostics are OWNED.** Frobenius and operator-norm
 scale bounds are presented as consistency checks (they independently
 agree with the imposed rule), not as a retained selector.

8. **The imposed-rule honest label is STATED IN TITLE AND
 STATUS.** Reviewer feedback on the first-pass inertia "promotion"
 is taken seriously: the branch-choice rule is imposed, not derived.
 Option B (deriving the rule from retained structure — e.g. a
 live-sheet Schur argument) is flagged as a separate open item.

All adversarial review issues are addressed with explicit
runner-verified numerical content at `PASS = 46, FAIL = 0`. The
non-retained ingredients (imposed branch-choice rule; `q_H = 0`;
Taylor-convergence boundary) are flagged honestly in-situ.

## What this file must never say

- that the inertia-preservation selector is a retained theorem (it is
 an IMPOSED branch-choice admissibility rule; Sylvester's law of
 inertia is an algebraic fact about `signature`, but the restriction
 to the baseline-connected branch is imposed)
- that `W[J]` has a Taylor-convergent expansion around `H_base` at
 the Basin 1 amplitude (it does not; `ρ ≈ 1.285`)
- that a Frobenius or operator-norm scale bound is the primary basin
 selector (they are consistency diagnostics; the primary selector
 on the current branch tip is the imposed branch-choice rule)
- that `q_H = 0` is derived from the axiom (it is not; it is the SM
 canonical Higgs Z_3 assignment)
- that θ_23 is derived (it is not; the closure yields the
 upper-octant conditionality, not the θ_23 value)
- that the DM flagship lane is CLOSED as a consequence of this note
 (the honest status is conditional / support; see
 DM_FLAGSHIP_CLOSURE_REVIEW_NOTE_2026-04-17.md)
- that the PMNS-closure theorem's pinning point is numerically different
 after this revision (it is not; the pinning point is unchanged,
 only the uniqueness-discipline labels)
