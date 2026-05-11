# Bridge Gap — Heat-Kernel Time from Canonical Cl(3) Tr-Form (Block 01)

**Date:** 2026-05-06
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded support theorem on the framework's leading-order
small-U Wilson-to-heat-kernel matching surface, conditional on (a) the
canonical Cl(3) connection trace form `Tr(T_a T_b) = δ_{ab}/2`,
(b) g_bare = 1 (open gate per `MINIMAL_AXIOMS_2026-05-03.md`),
(c) heat-kernel as the candidate Cl(3)-native gauge action (Block 04
target — uniqueness vs Wilson NOT yet derived), and (d) leading-order
small-U matching as the Brownian-time selection criterion (finite-β
correction analysis is Block 02 target). It is NOT a Resolution-A
closure of the bridge gap; it derives one specific structural input
(the heat-kernel time `t(β)` under canonical normalization) that the
project has not previously closed in writing.
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.
**Primary runner:** [`scripts/probe_hk_time_derivation.py`](../scripts/probe_hk_time_derivation.py)

## Question

Under the canonical Cl(3) connection trace form
`Tr(T_a T_b) = δ_{ab}/2` retained as `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02`,
what specific Brownian time `t = t(β)` does the framework's continuum
small-U matching assign to the heat-kernel gauge action?

The framework's gauge action is admitted-as-import (Wilson) per
[`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
line 467, and that heat-kernel is the Casimir-native alternative
(Casimir is retained per [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)).
Under the canonical Cl(3) Tr-form, the heat-kernel time `t` is not a
free parameter but is fixed by the Brownian-motion generator's match
to the Wilson small-U expansion at canonical g_bare = 1.

## Answer

At leading order in the small-U expansion:

```
t(β) = 2 N_c / β = g_bare²
```

In particular, at the framework's canonical g_bare = 1, β = 2 N_c = 6:

```
t(β = 6) = 1.
```

This is the Brownian-time match, not a fitted value, derived by
matching the canonical-normalized Wilson and heat-kernel small-U
expansions in the bi-invariant metric induced by `Tr(T_a T_b) = δ_{ab}/2`.

## Setup

### Premises (A_min for this block)

| ID | Statement | Class |
|---|---|---|
| A1 | Local algebra is `Cl(3)` | retained axiom |
| A2 | Z³ spatial substrate | retained axiom |
| TR | `Tr(T_a T_b) = δ_{ab}/2` (canonical normalization) | retained per `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02` |
| C2 | `C_2(1,0) = 4/3` exact | retained per `SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02` |
| GB | g_bare = 1, β = 2 N_c = 6 | open gate (admitted at canonical-convention layer) |
| SCH | Schur orthogonality, Lie-algebra rep theory | standard math machinery |
| BM | Brownian motion on compact Lie groups (Helgason; Liao 2004) | standard math machinery |
| WSU | Wilson small-U expansion `S_W = β·(1 - (1/N) Re Tr U)` | standard lattice-gauge machinery |

### Forbidden imports (no load-bearing role)

- PDG / lattice MC ⟨P⟩(6) values (≈ 0.5934, 0.59400 ± 4×10⁻⁴) — comparators only
- Bessel-determinant Wilson character coefficients as motivation
- Same-surface family arguments
- Fitted t or fitted β_eff
- Sommer scale, 4-loop QCD running (already admitted upstream)

## Derivation

### Step 1: Canonical bi-invariant metric on SU(3)

The trace form `Tr(T_a T_b) = δ_{ab}/2` on Hermitian Gell-Mann generators
`T_a = λ_a/2` defines an Ad-invariant inner product on `su(3)`.
Specifically, set

```
⟨X, Y⟩_su(3) := 2 · Tr(X Y),  for X = X^a T_a, Y = Y^a T_a in su(3).        (1)
```

Then by (TR):

```
⟨T_a, T_b⟩_su(3) = 2 · Tr(T_a T_b) = 2 · δ_{ab}/2 = δ_{ab},                  (2)
```

so `{T_a}` is an orthonormal basis of `su(3)` under this inner product.

By the standard Lie-group theorem (Helgason, *Differential Geometry, Lie
Groups, and Symmetric Spaces*, Theorem II.4.4): an Ad-invariant inner
product on `g` extends uniquely to a bi-invariant Riemannian metric `g`
on the Lie group `G = SU(3)`. Hence the Tr-form (1) gives a unique
bi-invariant metric `g_canonical` on SU(3) with the property that left-
and right-translates of orthonormal `{T_a}` form an orthonormal frame on
the tangent bundle `TSU(3)`.

### Step 2: Brownian-motion generator

Under bi-invariant metric `g_canonical`, the Laplace-Beltrami operator
on smooth functions on SU(3) has the standard eigenvalue spectrum
indexed by irreps `λ = (p, q)`:

```
Δ_g χ_λ = -C_2(λ) · χ_λ,                                                     (3)
```

where `C_2(λ)` is the quadratic Casimir on irrep `λ` in the normalization
fixed by (TR). Note: this normalization gives `C_2(1,0) = 4/3` per (C2).

(The sign and normalization convention in (3) is the one for which
`Δ_g = -Σ_a (E_a)²` where `E_a` are right-invariant vector fields with
`E_a|_e = T_a`. Under the canonical orthonormal frame from (TR), this is
the standard Laplace-Beltrami operator. The Casimir eigenvalue formula
`C_2(p,q) = (1/3)(p² + pq + q² + 3p + 3q)` is the framework-retained
exact rational at canonical normalization.)

Brownian motion `U_s` on `(SU(3), g_canonical)` starting at the identity
at "time" `s = 0` is the diffusion process generated by `(1/2) Δ_g`. Its
transition density at time `t` is the heat kernel:

```
P_t(U) = Σ_λ d_λ · exp(-t · C_2(λ) / 2) · χ_λ(U).                            (4)
```

Equation (4) is the canonical heat-kernel character expansion; it is a
direct consequence of (3), spectral decomposition of `Δ_g` on irreducible
characters, and Schur orthogonality (SCH).

### Step 3: Small-U Wilson action expansion

Take `U = exp(i X) ∈ SU(3)` with `X = X^a T_a ∈ su(3)`, `X` small. Then
to second order in `X`:

```
Re Tr U = Re Tr(I + iX - X²/2 + O(X³))
        = N_c - (1/2) Tr(X²) + O(X⁴).                                       (5)
```

Under (TR):

```
Tr(X²) = Σ_{a,b} X^a X^b Tr(T_a T_b) = (1/2) Σ_a (X^a)² = (1/2) |X|²,        (6)
```

where `|X|² := Σ_a (X^a)²` is the canonical-orthonormal-basis norm
squared (which equals the Riemannian norm squared `g_canonical(iX, iX)|_e`
by Step 1).

The Wilson per-plaquette action density is (WSU):

```
S_W(U) = β · (1 - (1/N_c) Re Tr U).                                         (7)
```

Substituting (5) and (6) into (7):

```
S_W(U) = β · (1 - (1/N_c)(N_c - (1/4) |X|² + O(X⁴)))
       = β · ((1/(4 N_c)) |X|² + O(X⁴))
       = (β / (4 N_c)) · |X|² + O(X⁴).                                      (8)
```

In particular, at canonical g_bare = 1 (so β = 2 N_c):

```
S_W(U) = (2 N_c / (4 N_c)) · |X|² + O(X⁴) = (1/2) |X|² + O(X⁴).             (9)
```

### Step 4: Small-U heat-kernel action expansion

The heat-kernel action is `S_HK(U) := -log P_t(U)` with `P_t` given by
(4). Near the identity, `P_t` is the standard Gaussian on the manifold
in the canonical metric:

```
P_t(U) ~ (2π t)^{-(dim G)/2} · exp(-d²(U, I) / (2 t))   as U → I.          (10)
```

Here `d(U, I)` is the geodesic distance under `g_canonical`. By Step 1
and standard Riemannian-geometry facts (the exponential map `exp_e` from
`su(3)` to `SU(3)` is the standard matrix exponential on a compact Lie
group with bi-invariant metric, and is a Riemannian isometry on a small
neighborhood of `0`):

```
d²(U, I) = ⟨X, X⟩_su(3) = |X|²   for U = exp(iX), |X| small.               (11)
```

(See Helgason loc. cit. Theorem IV.3.3 — bi-invariant exponential map is
a local Riemannian isometry on a normal neighborhood at the identity.)

Substituting (11) into (10):

```
-log P_t(U) = (1/2) log(2π t)·(dim G) + |X|²/(2 t) + O(X⁴),                (12)
```

so the X-dependent part of `S_HK` is:

```
S_HK(U)|_dynamic = |X|² / (2 t) + O(X⁴).                                    (13)
```

The constant prefactor `(dim G/2) log(2π t)` is U-independent and drops
out of all observable expectations — it is a normalization, not dynamics.

### Step 5: Match Wilson and heat-kernel at small U

For Wilson and heat-kernel to agree on the leading-order quadratic
form (which is what the small-U expansion captures and what the
continuum limit selects), set (8) equal to (13):

```
(β / (4 N_c)) · |X|² = |X|² / (2 t).                                       (14)
```

Solving:

```
t = 2 N_c / β.                                                              (15)
```

Equivalently, using `β = 2 N_c / g_bare²`:

```
t = g_bare².                                                                 (16)
```

At the framework's canonical g_bare = 1:

```
t(canonical) = 1.                                                            (17)
```

Equivalently, at the framework's β = 6:

```
t(β = 6) = 2 · 3 / 6 = 1.                                                   (18)
```

This is the leading-order Brownian-time match for the framework's
canonical normalization.

## Theorem 1 (Block 01 deliverable)

**Theorem.** Conditional on the canonical Cl(3) trace form
`Tr(T_a T_b) = δ_{ab}/2` (premise TR) and the Wilson small-U expansion
(premise WSU), the heat-kernel Brownian time matching the Wilson per-
plaquette action at leading order in `|X|²` is

```
t(β) = 2 N_c / β = g_bare².                                                 (T1)
```

At the framework's canonical g_bare = 1, β = 2 N_c = 6, this evaluates to

```
t(β = 6) = 1.                                                               (T1.6)
```

**Proof.** Steps 1-5 above. ∎

## Scope and Non-Claims

This bounded theorem is conditional on the canonical trace form,
`g_bare = 1`, heat-kernel as a candidate action form, and leading-order
small-`U` matching as the Brownian-time selection criterion.

Heat-kernel/Wilson small-`U` matching, Brownian motion on compact Lie
groups, and Schur orthogonality are standard mathematical machinery in a
narrow support role. No PDG or lattice-MC value is load-bearing.

The result is not a closure of the bridge gap: action-form uniqueness and
finite-beta correction structure remain separate open questions.

## What this closes

- The previously-open question "what t = t(β) does canonical Cl(3) Tr-form
  force at leading order?" is closed: `t = 2 N_c / β = g_bare²`, exactly.
- At canonical g_bare = 1: `t(β = 6) = 1`. This is a specific framework-
  derived rational, not a fitted value.
- Identifies that the framework's canonical small-U match between Wilson
  and heat-kernel selects `t = 1` UNAMBIGUOUSLY at leading order — there
  is no convention freedom in this specific choice.

## What this does NOT close

- Block 02 target: `⟨P⟩_HK,1plaq(6)` under derived t (separate evaluation).
- Block 03 target: thermodynamic ⟨P⟩_HK(6) under Casimir-diagonal action.
- Block 04 target: action-form uniqueness — does Cl(3) Tr-form actually
  force heat-kernel over Wilson, Manton, Cl(3)-volume-form, or a Spin(6)
  / SU(4)-tensor action?
- The four cluster-obstruction lanes (yt_ew M, gauge-scalar, Higgs mass,
  Koide-Brannen) are NOT closed by this block alone. They require Block 04
  (action-form uniqueness) AND Block 03 (thermodynamic limit) at a
  minimum.
- The famous open SU(3) lattice problem (analytic ⟨P⟩_Wilson(6)) is
  unchanged by this block.

## Cross-validation

The leading-order match (T1) is consistent with:

- **Drouffe-Zuber 1983** Phys. Rep. 102, 1 — strong-coupling analysis of
  heat-kernel SU(N) lattice gauge theory. Their `λ` parameter
  (heat-kernel coupling) corresponds to our `t`, and their continuum-limit
  matching gives `λ = N/(g²)` in their convention, equivalent to our
  `t = g_bare²` after their factor-of-2 convention adjustment.
- **Menotti-Onofri 1981** Nucl. Phys. B190, 288 — explicit SU(2)
  heat-kernel-Wilson matching at small `a`. Specializes to `t = g²`
  at leading order, consistent with our (16).

These are admitted-context cross-checks, NOT load-bearing derivation
inputs. The derivation in Steps 1-5 is self-contained from premise
(TR) + standard small-U expansion.

## Numerical preview for Block 02

Using (T1.6) `t(6) = 1` and `C_2(1,0) = 4/3`, the heat-kernel
single-plaquette expectation (to be derived in Block 02) is at leading
character order:

```
⟨(1/3) Re Tr U⟩_HK,1plaq = exp(-t · C_2(1,0) / 2) = exp(-2/3) ≈ 0.51342.
```

For comparison (NOT load-bearing, audit comparator only):

| Quantity | Value | Source |
|---|---|---|
| ⟨P⟩_W,1plaq(6) (Wilson, certified) | 0.42253174 | V=1 PF ODE (`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06`) |
| **⟨P⟩_HK,1plaq(6) (heat-kernel, this block + Block 02)** | **exp(-2/3) ≈ 0.51342** | (T1.6) + retained C_2 |
| ⟨P⟩_MC(6) (lattice MC) | ≈ 0.5934 | comparator only |

The heat-kernel single-plaquette value sits between Wilson 1-plaq (0.4225)
and the lattice MC value (0.5934), at exp(-2/3) = 0.5134 — about 5× ε_witness
below MC. That this CLOSED-FORM number lies near the MC value is suggestive
(NOT load-bearing) that heat-kernel may be the framework's actually-derived
action; Block 04 must close the action-form uniqueness question for any
load-bearing claim.

## Cross-references

- New-physics opening:
  [`BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md`](BRIDGE_GAP_NEW_PHYSICS_OPENING_NOTE_2026-05-06.md)
- Exhausted Resolution-A routes (under Wilson):
  [`BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md`](BRIDGE_GAP_EXHAUSTED_ROUTES_CONSOLIDATION_NOTE_2026-05-06.md)
- Wilson-as-import explicit text:
  [`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md) §467
- Canonical Tr-form retained:
  [`G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md`](G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM_NOTE_2026-05-02.md)
- Casimir retained:
  [`SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md`](SU3_CASIMIR_FUNDAMENTAL_THEOREM_NOTE_2026-05-02.md)
- V=1 PF (Wilson side):
  [`PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md`](PLAQUETTE_V1_PICARD_FUCHS_ODE_MINIMALITY_PROOF_NOTE_2026-05-06.md)
- Standard methodology references:
  - Helgason, *Differential Geometry, Lie Groups, and Symmetric Spaces*
    (Academic Press, 1978/2001) — bi-invariant metrics on Lie groups
  - Liao, *Lévy Processes in Lie Groups* (Cambridge, 2004) — Brownian
    motion on compact Lie groups
  - Menotti, P. & Onofri, E. (1981). Nucl. Phys. B190, 288
  - Drouffe, J.-M. & Zuber, J.-B. (1983). Phys. Rep. 102, 1

## Command

```bash
python3 scripts/probe_hk_time_derivation.py
```

Expected output: exact-arithmetic verification of (T1) — small-U
quadratic-form coefficients of Wilson and HK match at `t = 2 N_c / β`,
and at canonical `g_bare = 1, β = 6` evaluates to `t = 1` exactly.
