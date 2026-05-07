# C-iso Derivation — Per-Attack-Vector Results

**Date:** 2026-05-07
**Companion:** [`THEOREM_NOTE.md`](THEOREM_NOTE.md) (main note)
**Companion:** [`lieb_robinson_velocity_run.txt`](lieb_robinson_velocity_run.txt) (numerical log)
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.

This note records the per-attack-vector status for the six attack vectors
on Convention C-iso (`a_τ = a_s` plus Wilson-replace).

---

## Attack 1: Lieb-Robinson velocity sets the time discretization

### Hypothesis

Per [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](../../../docs/AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md),
the Lieb-Robinson velocity is `v_LR = 2 e r J` where `r = 1` (lattice unit
range) and `J = sup_z ‖h_z‖_op` is the maximum local-Hamiltonian-density
operator-norm.

The natural time scale is `a_τ,LR := a_s / v_LR`. If `v_LR = 1` in some
canonical-units, then `a_τ,LR = a_s` and Convention C-iso.i would follow.

### Derivation

The framework's natural Hamiltonian is

```
H_KS = (g²/(2 a_s)) Σ_e Ĉ_2(e) − (1/(g² a_s)) Σ_p (1/N_c) Re Tr_F(U_p)
```

with each local term `h_z` supported in a ball of radius `r = 1`.

Operator-norm bound on `h_z`:
- The link-Casimir term: `(g²/(2 a_s)) ‖Ĉ_2‖`. For SU(3) fundamental,
  `‖Ĉ_2‖|_{fundamental} = 4/3`. With multiple links per site (coordination
  6), proxy = `(g²/(2 a_s)) · (4/3) ≈ 0.667 g²/a_s`.
- The plaquette term: `(1/(g² a_s)) ‖(1/N_c) Re Tr_F U_p‖_op = 1/(g² a_s)`
  (since `|Tr_F U_p| ≤ N_c`).

Thus

```
J = max( g²/(2 a_s) · O(1), 1/(g² a_s) · O(1) )
```

is `g²`-dependent, with minimum at `g² = √2` and divergence at `g² → 0`
or `g² → ∞`.

### Result — NEGATIVE

Numerically, at canonical `g² = 1, a_s = 1`:

| Quantity | Value |
|---|---|
| `J` (proxy operator norm) | `1.0000` |
| `v_LR = 2 e r J` | `5.4366` (units: `a_s/time`) |
| `a_τ,LR = a_s/v_LR` | `0.1839 a_s` |
| `ξ_LR = a_s/a_τ,LR` | `5.4366` |

(Per [`lieb_robinson_velocity_run.txt`](lieb_robinson_velocity_run.txt) — verified
reproducible run.)

The **LR velocity does not equal 1** in canonical units. Instead, the LR
"natural anisotropy" is `ξ_LR ≈ 5.4` at canonical operating point,
**not** `ξ = 1`.

Furthermore, sweeping `g²`:

| `g²` | `J(g²)` | `v_LR` | `a_τ,LR/a_s` |
|---|---|---|---|
| 0.10 | 10.000 | 54.366 | 0.018 |
| 0.50 | 2.000 | 10.873 | 0.092 |
| 1.00 | 1.000 | 5.437 | 0.184 |
| 2.00 | 1.333 | 7.249 | 0.138 |
| 4.00 | 2.667 | 14.498 | 0.069 |

`v_LR` is **not** a `g²`-independent constant. There is no canonical-units
dimensionless value `v_LR = 1` derivable from primitives.

### Interpretation

The LR velocity is a **bound on signal propagation speed in lattice units
per unit time**. It is *not* the renormalized speed of light. The
renormalized speed of light = 1 is a **continuum-limit, all-orders**
statement (per [`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](../../../docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md)),
not a bare-lattice identity.

The bare-lattice anisotropy `ξ` is therefore **not pinned** by `v_LR`.

### Status

**Attack 1: NEGATIVE.** Cannot be used to derive `a_τ = a_s`.

---

## Attack 2: Single-clock causality forces `a_τ = a_s`

### Hypothesis

The single-clock structure
([`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](../../../docs/AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md))
fixes the form of evolution as a one-parameter unitary group `U(t) = exp(-itH)`
on `H_phys`. Could it also fix the discretization step `a_τ`?

### Derivation

The Single-Clock theorem (S1) states:

> The discrete-time iteration `U_n := T^n` extends, in the canonical
> continuum-time identification `t_phys = n · a_τ`, to a strongly-continuous
> one-parameter unitary group `U(t) := exp(-itH)`.

The mathematical content is **Stone's theorem**: a self-adjoint operator
`H` generates a unique strongly continuous one-parameter unitary group
`U(t) = exp(-itH)`. This pins:

- (a) the unitary group `U(t)` for `t ∈ ℝ`, given `H`;
- (b) the generator `H` is unique up to additive scalar (vacuum-energy
  subtraction).

It does **not** pin the value of `a_τ`. For any `a_τ > 0`, the transfer
matrix `T(a_τ) = exp(-a_τ H)` is a valid positive Hermitian operator on the
same `H_phys`.

### Result — NEGATIVE

The single-clock structure pins:
- *Form*: one-parameter unitary group with unique generator `H`.

It does NOT pin:
- *Step*: `a_τ`. Any positive value gives a valid transfer matrix.

This is consistent with the standard Trotter-expansion view:
`Z(T_phys) = Tr T(a_τ)^{N_τ}` for any `a_τ` and `N_τ = T_phys/a_τ`. The
Trotter remainder is `O(a_τ²)` per step, vanishing as `a_τ → 0` (Hamilton
limit).

### Interpretation

Single-clock fixes the **temporal-evolution algebra** (one generator),
not the **temporal-step granularity**. The latter is a discretization
choice.

This is parallel to the situation in any quantum-statistical-mechanics
calculation: the Hamiltonian determines dynamics, but the temporal mesh
size in a numerical simulation is a free parameter.

### Status

**Attack 2: NEGATIVE.** Cannot be used to derive `a_τ = a_s`.

---

## Attack 3: Continuum-limit consistency forces `ξ = 1`

### Hypothesis

The continuum limit `a → 0` requires both `a_s → 0` and `a_τ → 0`. The
continuum theory has a unique Lorentz/rotation structure (per
[`EMERGENT_LORENTZ_INVARIANCE_NOTE.md`](../../../docs/EMERGENT_LORENTZ_INVARIANCE_NOTE.md)).
Demand consistency: which anisotropy `ξ` makes the lattice theory match
the canonical Cl(3) trace form's induced metric?

### Derivation

The framework's continuum-limit emergent-Lorentz dispersion for fermionic
modes is:

```
E²(p) = p² − (a_s²/3) Σ_i p_i⁴ + O(a_s⁴ p⁶).
```

This is **isotropic** at leading order in `p` (Lorentz-invariant in the
sense of `E² = p²` continuum dispersion). The leading correction is
`O(a²p⁴)`, a CPT-even, parity-even, dimension-6 cubic-harmonic operator.

For an *anisotropic* lattice with bare `ξ ≠ 1`, the dispersion would be:

```
E²_aniso = (1/a_s²) Σ_i sin²(p_i a_s) · ξ + ...
        ≈ ξ · p² − (ξ a_s²/3) Σ_i p_i⁴ + ...
```

The renormalized speed of light `c_renorm := lim_{a→0, p→0} E/|p|` is
**1 for any value of bare `ξ`** in the continuum limit, after appropriate
renormalization of the temporal step.

What `ξ` distinguishes is the *finite-lattice-spacing* dispersion, not the
continuum-limit dispersion.

### Result — PARTIAL POSITIVE (but reframes, doesn't derive C-iso)

The continuum limit at fixed renormalized `c_renorm = 1` requires a
**Karsch-Klassen one-loop tuning** of `ξ_bare` as a function of `g²`:

```
ξ_bare(g², c_renorm = 1) = 1 + c_KK · g²/(8π²) + O(g⁴)
```

with `c_KK` a known one-loop constant. At canonical `g² = 1`, the bare
`ξ` differs from the renormalized `ξ = 1` by `O(g²/8π²) ≈ 1-3%`.

So:
- **Renormalized `ξ = 1`** is a continuum-limit *target*, not a bare-lattice
  primitive.
- **Bare `ξ = 1`** at canonical `g² = 1` differs from renormalized `ξ = 1`
  by a known one-loop correction.

Neither is a primitives-derived identity.

### Interpretation

The "continuum-limit consistency" argument tells us that **the framework's
prediction for any infrared observable does not depend on the bare `ξ`**
(by the Renormalization Group, all `ξ_bare` flow to the same continuum
fixed point at `c_renorm = 1`).

This *reframes* C-iso.i: the choice `a_τ = a_s` is a **bare-lattice
parameterization choice** with no infrared consequence, modulo finite-lattice
artifacts of order `O(g²)` (= the existing C-iso bound).

This is consistent with the `O(g²) ≈ 5-15%` C-iso admission characterized
in [`DICTIONARY_DERIVATION_RESULTS.md`](../DICTIONARY_DERIVATION_RESULTS.md).

### Status

**Attack 3: REFRAMES** — does not derive `ξ_bare = 1`, but explains why the
infrared physics is `ξ_bare`-independent. The C-iso bound is the lattice
artifact of fixing `ξ_bare` to a particular value.

This does not eliminate the C-iso admission, but it does explain why the
bound is the "right" magnitude (`O(g²)` finite-lattice artifact).

---

## Attack 4: Heat-kernel temporal as the framework's derived prediction

### Hypothesis

The framework's prediction for `⟨P⟩_KS(g²=1)` is in **heat-kernel-temporal**
language (= Theorem T-AT). The standard lattice-MC comparator
`⟨P⟩_W(β=6)` is in **Wilson-temporal** language. The difference is a
known `O(g²)` correction (= C-iso.ii).

So the right framing is:
- Framework prediction: anisotropic Wilson-spatial / heat-kernel-temporal.
- Comparator: 4D isotropic Wilson MC.
- Difference: one-loop anisotropy correction (C-iso.ii) plus the bare-`ξ`
  choice (C-iso.i).

The "Wilson-replace" step is then a **reinterpretation**, not a
derivation.

### Derivation

By Theorem T-AT [(DICTIONARY_DERIVED_THEOREM.md)](../DICTIONARY_DERIVED_THEOREM.md),
the framework's natural Euclidean partition function is:

```
Z = ∫ DU exp(-S_AT[U; ξ])
S_AT = -Σ_{spatial p} β_σ (1/N_c) Re Tr_F U_p^{(σ)}
     + Σ_{temporal p} [-ln K_{s_t}(U_p^{(τ)})]
```

with `β_σ = 1/(g²ξ)` and `s_t = g²/(2ξ)`. This is heat-kernel-temporal.

The framework's prediction for the *spatial* plaquette `⟨P_σ⟩` is computed
in this heat-kernel-temporal language, **not** by replacing the temporal
weight with Wilson form.

The "Wilson-replace" step is thus a *post-hoc choice* to compare to the
4D isotropic Wilson MC at `β = 6`. It is *not* what the framework
derives.

### Result — POSITIVE for honest scope

The right framing is:

> **Framework prediction** (theorem-grade): `⟨P_σ⟩` from `S_AT` at `ξ = 1, g² = 1`.
>
> **Comparator** (standard-physics): `⟨P_W⟩` from `S_W` at `β_W = 6`.
>
> **Bridge**: the two agree at leading order in `g²` and `1/ξ`, with
> explicit `O(g²)` correction.

Under this framing:

- Theorem T-AT *fully derives* the framework's lattice prediction (modulo
  the choice of `ξ`).
- The "Wilson-replace" step is *not* part of the framework's derivation.
  It is a **reinterpretation** for downstream comparison purposes.

This means C-iso.ii is **L3b parsimony, not L3 admission**: one chooses
to compare to Wilson-temporal MC instead of heat-kernel-temporal MC, and
the bound is the difference between the two within the continuum-equivalence
class (Theorem A2.5).

### Interpretation

This is a substantial *honest-scope improvement*. It removes "Wilson-replace"
from the genuine-admission list. The bridge gap then has only one genuine
admission (`a_τ = a_s` = C-iso.i) plus the existing continuum-equivalence-class
parsimony.

### Status

**Attack 4: POSITIVE** — successfully reframes C-iso.ii as L3b parsimony
(not a separate admission).

---

## Attack 5: Action-form continuum equivalence sharpening

### Hypothesis

Wilson and heat-kernel both give the same continuum action `Tr(F²)` at
leading order. The difference at finite β is Symanzik-irrelevant.
Quantify exactly what the difference is and whether it's bounded by
primitives.

### Derivation

The continuum-level theorem A2.5
([`A2_5_DERIVED_THEOREM.md`](../A2_5_DERIVED_THEOREM.md)) establishes
that under retained primitives (A1+A2 + canonical Tr-form + RP + locality
+ single-clock + Cl(3) color automorphism + standard Symanzik
power-counting), the continuum-level magnetic operator on each spatial
plaquette is uniquely

```
M̂_continuum(F_p) = α_eff · Tr(F_p²)
```

with `α_eff ≥ 0` determined by the Block B continuum-matching constraint.

Wilson, heat-kernel, Manton are different lattice representatives of the
**same continuum operator** with different higher-character coefficient
distributions. Their difference at finite β is `O(a²)` Symanzik
corrections, vanishing as `a → 0`.

For the temporal-plaquette weight, the explicit comparison
([`DICTIONARY_DERIVED_THEOREM.md`](../DICTIONARY_DERIVED_THEOREM.md)
Corollary T-AT.3) is:

| `s_t` | `ξ` (at `g²=1`) | rel.err Wilson-vs-HK |
|---|---|---|
| 0.01 | 50 | 0.35% |
| 0.05 | 10 | 0.32% |
| 0.50 | 1 | 8.55% |

This is `O(s_t)` at small `s_t`, with explicit Polyakov / Drouffe-Itzykson
heat-kernel asymptotic giving leading coefficient `N_c/s_t`.

### Result — POSITIVE

The Wilson-vs-heat-kernel difference is bounded by:
- `O(s_t) = O(g²/(2ξ))` near identity (Polyakov asymptotic).
- `O(a²)` Symanzik-irrelevant in the continuum limit.
- Numerically `~8.5%` at canonical `s_t = 0.5` (`ξ = 1, g² = 1`).

This is **the same bound** as the existing continuum-action-form parsimony
band (A2.5), now re-derived for the *temporal* sector specifically.

C-iso.ii is therefore absorbed into A2.5 parsimony: same equivalence class,
same `O(g²)` finite-`a` bound, no new admission.

### Interpretation

This is the most directly sharpening attack vector. It shows C-iso.ii is
*literally* the same admission as the existing A2.5-parsimony admission,
re-applied to the temporal sector.

### Status

**Attack 5: POSITIVE** — absorbs C-iso.ii into A2.5 parsimony bound.

---

## Attack 6: Reflection positivity in mixed-action lattice

### Hypothesis

The anisotropic mixed-action lattice (Wilson spatial + heat-kernel temporal)
inherits RP from `H_KS` via Trotter. If both temporal-action choices satisfy
RP, the framework can choose either. If only one does, that one is forced.

### Derivation

#### Heat-kernel temporal RP

Theorem T-AT directly inherits RP: `T(a_τ) = exp(-a_τ H_KS)` is the
RP-reconstructed transfer matrix
([`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)).
The Trotter expansion preserves RP at each step (positive operator
factorization). Therefore the mixed-action lattice with heat-kernel
temporal weight satisfies RP exactly.

#### Wilson temporal RP

The standard 4D isotropic Wilson action satisfies RP under
Osterwalder-Seiler / Sharatchandra-Thun-Weisz (cited in
[`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](../../../docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)).
The temporal Wilson plaquette factorizes as:

```
Re Tr_F U_p^{(τ)} = real part of a product of links across the reflection axis,
```

which gives an OS-type Cauchy-Schwarz factorization. Wilson temporal is
RP-positive.

#### Anisotropic mixed-action RP

For the anisotropic Wilson action with `β_σ ≠ β_τ` (both > 0), the OS
factorization works for both spatial and temporal plaquettes independently,
since each plaquette factorizes across the reflection axis identically.
RP holds for any positive `(β_σ, β_τ)`.

Both Wilson-temporal and heat-kernel-temporal are RP-positive on the
anisotropic 4D lattice.

### Result — NEGATIVE

RP does **not** select between Wilson-temporal and heat-kernel-temporal:
both are RP-compatible.

### Interpretation

This was the strongest hope for selecting one form over the other from
primitives. RP is a powerful primitive that pins many structural
properties (existence and positivity of `H`, spectrum condition, cluster
decomposition). But in the mixed-action lattice, **both** Wilson and
heat-kernel temporal forms preserve RP. The form selection is not a
primitives-derived identity.

This is consistent with A2.5: at the continuum level, both forms produce
the same `Tr(F²)`; the lattice-form selection is parsimony, not RP.

### Status

**Attack 6: NEGATIVE.** Cannot be used to select Wilson-temporal over
heat-kernel-temporal.

---

## Synthesis

| Attack | Status | What it achieves |
|---|---|---|
| A1. LR velocity | NEGATIVE | rules out `v_LR = 1` mechanism |
| A2. Single-clock | NEGATIVE | rules out single-clock as `a_τ` selector |
| A3. Continuum consistency | REFRAMES | explains why the C-iso bound is `O(g²)` (= finite-lattice artifact); does not eliminate |
| A4. Heat-kernel as derived | POSITIVE | reframes C-iso.ii as L3b parsimony |
| A5. Action-form sharpening | POSITIVE | absorbs C-iso.ii into A2.5 parsimony bound |
| A6. RP selection | NEGATIVE | both forms RP-compatible; RP doesn't select |

**Net:**

- C-iso.i (`a_τ = a_s`) cannot be derived from primitives. Documented
  structurally as L3a admission, parallel to `N_F = 1/2` in the `g_bare`
  chain.
- C-iso.ii (Wilson-replace) is absorbed into the existing
  continuum-equivalence-class parsimony (A2.5). It is **not** a separate
  admission.

The bridge admission count is reduced by 1 (Wilson-replace was previously
listed separately) and the remaining genuine admission is cleanly
characterized as L3a in a four-layer stratification.

This is a **bounded result** with structural-obstruction documentation.

---

## Cross-references

- Main note: [`THEOREM_NOTE.md`](THEOREM_NOTE.md)
- Numerical log: [`lieb_robinson_velocity_run.txt`](lieb_robinson_velocity_run.txt)
- Verification runner: [`scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py`](../../../scripts/cl3_c_iso_lieb_robinson_velocity_2026_05_07_w3_check.py)
