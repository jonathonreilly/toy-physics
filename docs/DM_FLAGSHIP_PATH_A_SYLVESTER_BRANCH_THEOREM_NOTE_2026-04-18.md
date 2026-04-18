# Sylvester-Linear-Path Theorem for the P3 Branch-Choice Admissibility Rule — Candidate Retention Note

**Date:** 2026-04-18 (rev 2026-04-18b — first-round reviewer findings addressed)
**Status:** CANDIDATE THEOREM PROMOTION — awaiting review for retention
**Target:** retire the **pointwise signature** portion of the imposed
branch-choice admissibility rule in the P3 observational-promotion lane,
conditional on a separately-stated baseline-connected-component axiom
**Dedicated verifier:**
`scripts/frontier_dm_path_a_sylvester_linear_path.py`
**Relates to:**
`docs/PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md`,
`docs/DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md`,
`docs/DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`,
`docs/DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md`

## Reviewer-findings resolution (rev 2026-04-18b)

First-round reviewer raised two P1 blockers and one P2 blocker on `review.md`
(branch `review/path-a-sylvester-branch-theorem`):

1. **[P1 — scope overstatement]** Earlier revision claimed the theorem
   excludes Basins 2/X "by proof." It does not. The Sylvester argument
   shows signature is preserved along the *baseline-connected* linear
   segment; it does **not** derive that the baseline-connected component
   of `{det(H) ≠ 0}` is the physical live sheet. Basin-2/X exclusion
   therefore remains conditional on a separately-stated baseline-
   connected-component axiom (**A-BCC**, §"Remaining axiom" below).
2. **[P1 — sampled evidence]** Earlier revision certified interval-wide
   non-singularity of `H(t)` via 11 sampled `t`-values plus a 1107-point
   tube scan. Replaced in §Proof Step 2 below with an **exact 1D
   positivity argument** on the cubic `det(H(t))`: critical points from
   `p'(t) = 0` solved in closed form, minimum over `[0, 1]` taken on the
   finite extremum set.
3. **[P2 — no dedicated verifier]** Earlier revision shipped only the
   note. Added `scripts/frontier_dm_path_a_sylvester_linear_path.py`
   (11/11 PASS) which independently reproduces the cubic coefficients,
   solves `p'(t) = 0` symbolically, evaluates the exact extremum set,
   and cross-checks `signature(H_base) = signature(H_base + J_*) = (2, 0, 1)`
   via direct eigenvalue computation.

Control-plane promotion surfaces are **not** updated in this revision.
Per reviewer guidance, promotion-surface weaving is deferred until the
remaining A-BCC axiom is either discharged or formally accepted as a
retained primitive.

## Summary

On the retained affine chart, the 3×3 determinant
`p(t) ≡ det(H_base + t·J_*)` is an **exact cubic in `t`**, whose
coefficients are retained quantities derived symbolically from
`H_base`, `J_*`, and the retained affine generators. The critical points
of `p(t)` come from the quadratic `p'(t) = 0`, solved in closed form. The
minimum of `p` on the closed interval `[0, 1]` is therefore attained on
the explicit finite set `{0, 1} ∪ {critical points in (0, 1)}`, and equals
`+0.878309 > 0`. Sylvester's law of inertia then forces
`signature(H(t)) = signature(H(0))` for every `t ∈ [0, 1]`, and in
particular
```
signature(H_base + J_*) = signature(H_base) = (2, 0, 1).
```

**What this theorem establishes (unconditional):** at the P3 pin, the
selector-admissibility *signature* value `(2, 0, 1)` is a theorem, not
an imposition. The matching between `H_pin` and `H_base` is rigorously
derived by linear-path Sylvester continuation.

**What this theorem does not establish (axiom A-BCC, still imposed):**
that the baseline-connected component of `{det(H) ≠ 0}` is the physical
live sheet. Basin-2/X exclusion remains conditional on A-BCC.

**Consequence of combining this theorem with A-BCC accepted as primitive:**
the DM flagship gate's selector-admissibility conditional at the P3 pin
is discharged on the pointwise-signature side. Remaining conditionals:
(i) A-BCC itself (new, separately statable), and (ii) the `σ_hier = (2, 1, 0)`
hierarchy pairing (independent of this theorem; under separate
investigation — see the σ_hier-agent OBSERVATIONAL-INPUT verdict).

## Unit system and dimensional conventions

Natural units throughout; dimensionless on the retained 3-generation irreducible `H_{hw=1}`. Entries of `H(m, δ, q_+)` are dimensionless in the retained observable normalization of the `THREE_GENERATION_OBSERVABLE_THEOREM`. Specifically:

- `m, δ, q_+` — real dimensionless affine coordinates on the live source-oriented sheet
- `H_base, T_m, T_δ, T_q` — `3×3` Hermitian matrices on `H_{hw=1}`
- `J ≡ m·T_m + δ·T_δ + q_+·T_q` — the additive source operator
- `γ = 1/2, E_1 = √(8/3), E_2 = √8/3` — dimensionless real constants inside `H_base`
- `det(H)` has units [H]³

No PDG charged-lepton masses invoked.

## Retained preliminaries

### P1. Affine chart (retained, `ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY`)

The live source-oriented Hermitian sheet is parametrized by the affine chart:
```
H(m, δ, q_+) = H_base + m·T_m + δ·T_δ + q_+·T_q
```
with `H_base[0,1] = E_1`, `H_base[0,2] = −E_1 − iγ`, `H_base[1,2] = −E_2`, and `T_m, T_δ, T_q` the retained affine generators.

### P2. Source package (retained)

`γ = 1/2`, `E_1 = √(8/3)`, `E_2 = √8/3` — fixed by the retained source-package theorems (exact one-flavor branch `0.1888` and exact constructive sheet `1.0`).

### P3. Chamber boundary (retained)

Active affine chamber: `q_+ + δ ≥ √(8/3)` (intrinsic `Z_3` doublet-block point-selection theorem).

### P4. P3 observational pin (retained by observational promotion)

`(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`, matching 9/9 NuFit 5.3 NO 3σ PMNS bands.

### P5. Sylvester's law of inertia (textbook algebraic fact)

For a continuous family `H(t)` of `n × n` Hermitian matrices with `det(H(t)) ≠ 0` for all `t ∈ [0, 1]`, the signature is constant: `signature(H(t)) = signature(H(0))`.

## Theorem statement

**Theorem (Sylvester Linear-Path Admissibility at P3).** Let `J_* = m_* T_m + δ_* T_δ + q_+* T_q` with `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`. Then the Hermitian family
```
H(t) = H_base + t · J_*,   t ∈ [0, 1]
```
is non-singular along the entire closed segment. More precisely, the scalar
function `p(t) ≡ det(H(t))` is an **exact cubic polynomial in `t`** whose
minimum on `[0, 1]`, taken on the explicit finite extremum set
`{0, 1} ∪ {critical points of p in (0, 1)}`, equals
```
min_{t ∈ [0,1]} p(t) = +0.878309  >  0.
```
By Sylvester's law of inertia (P5), `signature(H(t))` is therefore constant
on `[0, 1]`, and in particular
```
signature(H_base + J_*) = signature(H_base) = (2, 0, 1).
```
The **pointwise signature value** in the imposed branch-choice admissibility
rule at `J_*` is therefore a retained theorem, not a pointwise imposition.

**Scope.** The theorem establishes only that `H_pin` lies on the same
connected component of `{det(H) ≠ 0}` as `H_base`, and hence shares its
signature. It does **not** derive that the baseline-connected component
is the physical live sheet (axiom **A-BCC**, §"Remaining axiom" below).

## Proof (exact 1D cubic argument)

### Step 1 — Closed-form det(H) on the affine chart

Symbolic expansion of the `3 × 3` determinant of `H(m, δ, q_+) = H_base + m T_m
+ δ T_δ + q_+ T_q` on the retained affine chart yields:
```
det(H) = − m³ − 2 m² q_+ + (4√2/3) m² + m q_+² + (4√2/3) m q_+ − (56/9) m
        + 2 q_+³ − (4√2/3) q_+² − (16/3) q_+
        − 3 δ² m − 6 δ² q_+ + (4√2/3) δ² + (8√6/3) δ m + (16√6/3) δ q_+
        − (32√3/9) δ − δ/4
        + 32√2/9
```

**Verification at `J = 0`:**
```
det(H_base) = 32√2/9 ≈ +5.028315
```
matching the retained atlas statement exactly (verified symbolically in the
dedicated runner, §"Reproduction"). Observable normalization preserved.

**Verification at P3 pin `(m_*, δ_*, q_+*) = (0.657061, 0.933806, 0.715042)`:**
The closed-form polynomial evaluates to
```
det(H_pin) = +0.959174
```
which the dedicated runner cross-checks against direct `det(H_base + J_*)`
eigen-computation (agreement to machine precision).

### Step 2 — Reduction to an exact univariate cubic

Substituting `(m, δ, q_+) = (t·m_*, t·δ_*, t·q_+*)` into the closed-form
determinant gives
```
p(t) ≡ det(H(t)) = A₀ + A₁ t + A₂ t² + A₃ t³
```
where every coefficient `Aₖ` is a retained algebraic quantity:

- `A₀ = 32√2/9 ≈ +5.028315` (atlas-identity, independent of `J_*`)
- `A₁ = −(56/9) m_* − (16/3) q_+* − (32√3/9 + 1/4) δ_* ≈ −13.886142`
- `A₂ = (4√2/3)(m_*² + m_* q_+* − q_+*² + δ_*²) + (8√6/3) δ_* m_* + (16√6/3) δ_* q_+* ≈ +15.110887`
- `A₃ = −m_*³ − 2 m_*² q_+* + m_* q_+*² + 2 q_+*³ − 3 δ_*² m_* − 6 δ_*² q_+* ≈ −5.293887`

The runner reproduces all four coefficients symbolically via sympy and cross-
checks `A₀` against `32√2/9` by exact simplification.

### Step 3 — Exact closed-form critical-point analysis

Because `p(t)` is a cubic, its derivative
```
p'(t) = A₁ + 2 A₂ t + 3 A₃ t²
```
is a **quadratic** whose roots are obtained in closed form:
```
t = [ −A₂ ± √(A₂² − 3 A₁ A₃) ] / (3 A₃)
```

The discriminant is `A₂² − 3 A₁ A₃ ≈ 228.339 − 220.478 = +7.861 > 0`, so
`p'(t) = 0` has two distinct real roots:
```
t₁ ≈ 0.775570   (inside [0, 1])
t₂ ≈ 1.127366   (outside [0, 1])
```
Since `A₃ < 0`, `p'(t)` is a downward parabola: `p'(t) > 0` on `(t₁, t₂)` and
`p'(t) < 0` outside. Hence `t₁` is a local minimum and `t₂` is a local maximum
of `p`. On `[0, 1]` only the local minimum `t₁` lies in the open interior.

### Step 4 — Theorem-grade minimum over `[0, 1]`

The minimum of a continuous function on a closed interval is attained on the
finite set `{boundary points} ∪ {interior critical points}`. For `p` on
`[0, 1]` this set is `{0, 1, t₁}`. Exact evaluation:
```
p(0)  = A₀                                           ≈ +5.028315
p(1)  = A₀ + A₁ + A₂ + A₃                            ≈ +0.959174
p(t₁) = (minimum; exact via Cardano's resolvent)     ≈ +0.878309
```

Therefore
```
min_{t ∈ [0,1]} p(t) = p(t₁) ≈ +0.878309 > 0.
```
This is an exact 1D argument: the minimum is taken on an **explicit finite
set of three points** of known analytic form, not sampled at 11 grid points
or tested within a 1107-point tube.

### Step 5 — Sylvester conclusion

`p(t) > 0` on `[0, 1]` ⟹ `det(H(t)) ≠ 0` on `[0, 1]` ⟹ `H(t)` is a
continuous family of non-singular Hermitian `3×3` matrices on `[0, 1]`. By
Sylvester's law of inertia (P5),
```
signature(H(1)) = signature(H(0))
signature(H_base + J_*) = signature(H_base).
```

**Direct eigenvalue check of the right-hand side.** On `H_base` the three
eigenvalues are
```
eigs(H_base) ≈ (−1.984570, −0.883438, +2.868007),
```
giving (in the retained atlas convention `(n_−, n_0, n_+)`) two negative,
zero zero, one positive eigenvalue:
```
signature(H_base) = (2, 0, 1).
```
At the pin, the direct eigenvalue computation independently gives
```
eigs(H_base + J_*) ≈ (−1.309094, −0.320434, +2.286589)  ⟹  (2, 0, 1),
```
consistent with the Sylvester conclusion.

Therefore `signature(H_base + J_*) = (2, 0, 1)`. **QED.** □

## Scope — what the theorem does and does not establish

The theorem is **pointwise at `J_*` on the baseline-connected linear
segment**, not chamber-wide, and is **silent on the physical-sheet
identification** of the baseline-connected component itself.

### Caustic structure of `det(H) = 0`

The zero locus `{det(H) = 0}` is a non-empty real 2-manifold inside the
chamber. Grid scans confirm non-trivial structure:
- 72 adjacent-grid sign changes along `q_+`-direction at fixed `m = m_*`
- 84 along `δ`-direction
- Nearest `det = 0` surface point to P3 pin: Euclidean distance `≈ 0.2561`
- Basin 2 `(28.0, 20.7, 5.0)`: `det = −70377` (opposite sign — different
  connected component of `{det ≠ 0}`)
- Basin X `(21.1, 12.7, 2.1)`: `det = −20295` (opposite sign — different
  connected component of `{det ≠ 0}`)

### Not every path works

Random two-segment (kinked) paths with an intermediate waypoint at
`(m_*/2, δ_*/2, q_+*/2) + N(0, 0.5)` crossed `det = 0` in 11 of 50 trials.
The connected component of `{det > 0}` containing `J = 0` and `J_*` is
therefore **non-convex** — the linear path succeeds, but not every path
does.

### Honest scope correction (rev 2026-04-18b)

Earlier revision language that the theorem "rules out Basins 2 and X by
proof" overstated what the Sylvester argument actually proves. The correct
decomposition is:

**Unconditional content of this theorem.** `H_pin` and `H_base` lie on the
**same connected component** of `{det(H) ≠ 0}` (call it **C_base**), and
share the signature `(2, 0, 1)`. Basins 2 and X carry `det < 0` and
therefore sit in a **different connected component** (call it **C_neg**)
of `{det ≠ 0}`.

**Remaining physical input (axiom A-BCC).** The identification
`live physical sheet  =  C_base` is **not** derived from Cl(3) on Z³, from
any retained source-surface theorem, or from the Sylvester argument. It is
a separately statable physical axiom: among the connected components of
`{det(H) ≠ 0}`, the physically realized PMNS sheet is the one containing
the baseline `J = 0` (equivalently, the `(2, 0, 1)`-signature component,
because `sign(det)` is a component invariant and agrees with `H_base`).

**Conditional exclusion of Basins 2/X.** Under A-BCC, Basins 2 and X are
structurally excluded because they sit in `C_neg`. Without A-BCC, the
Sylvester argument cannot by itself rule them out — it can only rule out
signature changes *along* the baseline-connected linear segment, not
between components.

**Why A-BCC is a reasonable axiom, but still an axiom.** Physically, the
baseline `J = 0` state is the unperturbed one-flavor source package with
no intrinsic slot or CP content. Continuous deformations away from this
baseline preserve signature under Sylvester. Jumping to a component where
`sign(det)` is reversed requires crossing `det = 0`, at which point the
Hermitian form becomes degenerate; the one-flavor-branch interpretation
breaks down there. So A-BCC is natural, but its elevation from "natural"
to "retained" is a separate derivation, not supplied here.

## Retained status changes (conditional on A-BCC)

Under this theorem **and** A-BCC accepted as a retained primitive, the
following items promote from conditional to retained (via the P3
observational-promotion lane):

| Item | Before | After Path A HIT (with A-BCC) |
|---|---|---|
| **Pointwise signature `(2, 0, 1)` at P3 pin** | IMPOSED rule | **RETAINED** (this theorem, A-BCC-free) |
| Baseline-connected component is the live sheet | IMPOSED | **IMPOSED (A-BCC)** — new named axiom, separately reviewable |
| Basin 1 selection vs Basin 2/X exclusion | IMPOSED | **RETAINED via (this theorem) + A-BCC** |
| PMNS angles `(θ_12, θ_13, θ_23)` | Conditional/support | **RETAINED** (9/9 NuFit 5.3 NO 3σ) once A-BCC accepted |
| `δ_CP ≈ −80.88°` (`sin δ_CP = −0.9874`) | Conditional forecast | **RETAINED prediction** once A-BCC accepted |
| `θ_23` upper octant (`sin²θ_23 ≥ 0.5409`) | Conditional prediction | **RETAINED falsifiable prediction** once A-BCC accepted |
| Jarlskog `|J_CP| = 0.0328` | Conditional | **RETAINED** once A-BCC accepted |
| DM flagship gate (overall) | CONDITIONAL/SUPPORT | **TWO NAMED AXIOMS REMAINING** (A-BCC, σ_hier) |

The net effect of this theorem, *without* A-BCC, is therefore to refactor
the prior imposed branch-choice rule into:

1. An unconditional **retained theorem** (pointwise signature at `J_*`
   equals pointwise signature at `J = 0`), and
2. A **smaller, sharper named axiom** (A-BCC: the baseline-connected
   component is the live sheet) that replaces the earlier generic
   "imposed branch-choice rule" language.

This is a strict refinement, not a closure, of the earlier imposed rule.

## Remaining conditionals

1. **A-BCC** — the baseline-connected-component identification axiom,
   newly named above. Separately reviewable; not addressed here.
2. **σ_hier = (2, 1, 0)** — the observational hierarchy pairing. An
   independent conditional in the P3 lane: which eigenvalue of
   `H(m_*, δ_*, q_+*)` corresponds to which neutrino mass slot in the
   ordered spectrum `m_1 < m_2 < m_3`. The σ_hier agent (ID
   `a331b5b13ca88b9c0`) returned OBSERVATIONAL-INPUT: σ_hier is a discrete
   S_3 involution (order 2), not derivable from the retained `C_3` order-3
   cycle; equivalent to observational NO preference.

If both A-BCC and σ_hier are accepted as retained primitives (or
discharged by further theorems), the DM flagship gate closes fully to
RETAINED on the P3 lane.

## What this theorem does NOT close

- Direct `dW_e^H = Schur_{E_e}(D_-)` derivation (Path B territory — remains open research problem; not required for gate closure via P3 lane)
- Chamber-wide signature rule (caustic is real; only pointwise form is theorem-grade)
- A-BCC (baseline-connected component = live sheet) — named separately above
- σ_hier pairing (independent conditional)
- Solar-gap `Δm²_21`, absolute neutrino mass scale, Majorana CP phases (separate carriers)

## Proposed status classification

**CANDIDATE THEOREM PROMOTION — AWAITING REVIEW**

The theorem is mathematically tight:
- Affine chart and `H_base` constants are retained (`DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY`).
- Closed-form `det(H)` derived symbolically and reproduced by the dedicated
  runner via `sympy`, with atlas cross-check `A₀ = 32√2/9` and direct-
  eigenvalue cross-check at the pin.
- Minimum over `[0, 1]` is **theorem-grade** via the exact extremum set
  `{0, 1, t₁}` with `t₁` given in closed form by the quadratic `p'(t) = 0`.
  No sampling or tube-scan is part of the proof.
- Sylvester's law of inertia is textbook.
- Conclusion `signature = (2, 0, 1)` follows rigorously.

The remaining subtlety — the baseline-connected-component identification
(A-BCC) — is now **honestly named as a separately statable axiom** rather
than folded into the theorem's content. This is a strict refinement of
the prior imposed branch-choice rule: what was previously one monolithic
imposition is now one retained theorem plus one smaller named axiom.

If retained (with A-BCC accepted):
- The P3 lane closes from "conditional/support" to "two-named-axioms-
  remaining" (A-BCC, σ_hier).
- All PMNS observables promote to retained.
- The DM flagship gate's closure path becomes: A-BCC + σ_hier + this theorem.

If retained (without A-BCC accepted):
- The imposed branch-choice rule is refactored into (this theorem) +
  (A-BCC). The reviewer-visible axiom count is **unchanged net** — we
  trade one imposition for one theorem plus one smaller axiom — but the
  pointwise signature at the pin is now theorem-grade.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_path_a_sylvester_linear_path.py
```

Expected output ends with `PASS=11 FAIL=0`. The runner:

1. Constructs `H(t)` symbolically from retained `H_base` and `T_m, T_δ, T_q`.
2. Verifies `H(t)` is Hermitian for all real `t`.
3. Computes `det(H(t))` as an exact cubic in `t`.
4. Cross-checks `A₀ = 32√2/9` against the retained atlas value.
5. Cross-checks `p(1)` against direct `det(H_base + J_*)` evaluation.
6. Solves `p'(t) = 0` symbolically (quadratic, closed form).
7. Certifies `min_{t ∈ [0,1]} p(t) = 0.878309 > 0` on the exact extremum
   set `{0, 1, t₁}`.
8. Cross-checks `min p ≈ 0.876` against the retained atlas statement.
9. Verifies `signature(H_base) = (2, 0, 1)` via direct numeric eigenvalues
   in the retained atlas convention `(n_−, n_0, n_+)`.
10. Verifies `signature(H_base + J_*) = (2, 0, 1)` via independent direct
    numeric eigenvalues at the pin.

## File references

- P3 primary closure: `PMNS_FROM_DM_NEUTRINO_SOURCE_H_DIAGONALIZATION_CLOSURE_THEOREM_NOTE_2026-04-17.md`
- Perturbative uniqueness (Option-A demotion): `DM_NEUTRINO_SOURCE_SURFACE_PERTURBATIVE_UNIQUENESS_THEOREM_NOTE_2026-04-17.md`
- Affine chart (source of `T_m, T_δ, T_q`, `H_base`, `γ`, `E₁`, `E₂`): `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
- Microscopic selector reduction: `DM_LEPTOGENESIS_PMNS_MICROSCOPIC_SELECTOR_REDUCTION_THEOREM_NOTE_2026-04-17.md`
- Chamber: `DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`
- Case 3 impossibility (for context, not used in proof): `DM_NEUTRINO_SOURCE_SURFACE_MICROSCOPIC_POLYNOMIAL_IMPOSSIBILITY_THEOREM_NOTE_2026-04-17.md`
- **Dedicated verifier for this theorem:** `scripts/frontier_dm_path_a_sylvester_linear_path.py`
- Other relevant runners (not part of this proof):
  - `scripts/frontier_dm_neutrino_source_surface_z3_parity_split_theorem.py` (symbolic gradient of det(H))
  - `scripts/frontier_dm_neutrino_source_surface_microscopic_polynomial_impossibility_theorem.py` (numerical det(H) probes)
  - `scripts/frontier_pmns_from_dm_neutrino_source_h_diagonalization_closure_theorem.py` (PMNS from H diagonalization)
