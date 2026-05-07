# Route Portfolio — Bridge Gap New Physics

**Date:** 2026-05-06

## Block 01 candidate routes

### R1.A — Bi-invariant metric → Brownian time t (PRIMARY)

**Premise:** the canonical Cl(3) connection normalization
`Tr(T_a T_b) = δ_{ab}/2` induces a unique bi-invariant metric on SU(3)
(by Lie-algebra-rep argument: any Ad-invariant inner product on
the Lie algebra extends uniquely to a bi-invariant metric on the group).
Brownian motion on a compact Lie group with a bi-invariant metric has
a canonical generator (the Laplace-Beltrami operator), and the
Brownian time matching to the lattice gauge action is determined by
the metric coefficient.

**Method:**
1. Show: `Tr(T_a T_b) = δ_{ab}/2` defines an Ad-invariant inner product
   on su(3); by uniqueness up to scale, this is *the* canonical
   Lie-algebra inner product.
2. Show: bi-invariant metric on SU(3) extends with metric coefficient
   exactly fixed by the Tr-form normalization.
3. Show: Brownian-motion small-U expansion gives `dU ≈ i T_a dW^a`
   under standard Itô calculus.
4. Show: Wilson small-U expansion at coefficient β/N matches
   heat-kernel small-U at coefficient 1/(2t).
5. Match: at β=6, g_bare=1, N=3 → `t = N/β = 1/2`.

**Forbidden:** Bessel-determinant Wilson character coefficients as
motivation; only as definition.

**Deliverable:** `BRIDGE_GAP_HK_TIME_DERIVATION_NOTE_2026-05-06.md`,
exact-rational `t(β=6) = 1/2`, runner script verifying small-U
matching numerically + analytically.

**Promotion-value gate (V1-V5):**
- V1: closes the Block-01 step from the bridge gap new-physics opening — derives canonical t in the framework's primitive stack
- V2: new derivation chain (canonical Tr-form → bi-invariant metric → Brownian motion → small-U matching) not currently retained as a single artifact
- V3: audit lane could combine retained Tr-form + standard Menotti-Onofri matching, but has not done so; this loop does it
- V4: marginal content non-trivial — gives a specific framework-derived value `t = 1/2` that supersedes the imported Wilson formulation
- V5: not a one-step variant of any landed cycle — closest is `G_BARE_CANONICAL_CONVENTION_NARROW_THEOREM` which fixes Wilson β=6 from Tr-form, not HK t

**PASS the V1-V5 gate.**

### R1.B — Hilbert-Schmidt distance + Manton matching (ALTERNATIVE)

**Premise:** instead of Brownian motion, derive the action from the
Hilbert-Schmidt squared distance |U-I|²_HS = 2N(1 - (1/N)Re Tr U), which
is the natural Lie-group distance for the Cl(3) connection.

**Method:** small-U expansion of HS distance vs. bi-invariant geodesic
distance squared; identify which gives the framework's canonical action.

**Risk:** may give the same answer as R1.A (since both reduce to the
same small-U quadratic form at leading order). If yes: redundant.

**Status:** secondary; consider only if R1.A produces an inconclusive
answer.

### R1.C — Direct extraction from O(a²) Wilson improvement coefficients

**Premise:** at next-to-leading order in a, the Wilson action differs
from heat-kernel by O(a²·F²) terms. The framework's canonical
normalization may force a specific O(a²) improvement coefficient that
identifies one action over the other.

**Method:** Symanzik improvement program; compare O(a²) coefficients of
Wilson vs HK for SU(3) at canonical normalization.

**Risk:** known SU(N) calculation; may not give framework-specific output.

**Status:** secondary; useful for Block 04 (action-form uniqueness) but
not Block 01.

## Block 02 routes (after R1.A succeeds)

### R2.A — Single-plaquette closed form via retained C_2 (PRIMARY)

`⟨P⟩_HK,1plaq(t) = exp(-2t/3)` from the standard heat-kernel character
expectation for SU(3) using `C_2(1,0) = 4/3` retained. At t = 1/2
(from R1.A): `⟨P⟩_HK,1plaq(6) = exp(-1/3) = 0.7165313106...`

**Deliverable:** closed-form rational/transcendental expression.

### R2.B — Picard-Fuchs ODE for HK single-plaquette generating function

The HK partition function `Z_HK(t) = Σ_λ d_λ² exp(-t·C_2/2)` may satisfy
a holonomic ODE in t analogous to V=1 Wilson PF. If yes: useful structural
artifact.

**Risk:** Casimir-suppressed sum is not naturally holonomic in the same
sense as Bessel-determinant; may not give a finite-rank ODE.

## Block 03 routes (thermodynamic ⟨P⟩_HK(6))

### R3.A — Casimir-diagonal multi-plaquette character algebra (PRIMARY)

The HK lattice partition function:
```
Z_HK,Λ(t) = Σ_{λ on each link} (Π_links d_λ exp(-t·C_2/2)) × (Wigner-Racah graph)
```

Casimir factors per link and intertwiner contractions per vertex.
β-dependence factorizes over plaquettes — fundamentally different from
Wilson's Bessel-determinant case where β couples plaquettes through the
non-factorizing Bessel structure.

**Promise:** if the Casimir-diagonal structure makes the multi-plaquette
sum closed-form, the famous open lattice problem doesn't apply.

### R3.B — Schwinger-Dyson loop equation on HK Casimir basis

Migdal-Makeenko-style loop equations may close in closed form on the
Casimir basis (vs failing to close on Wilson's character basis).

## Block 04 routes (action-form uniqueness)

### R4.A — Continuum-limit action-form constraint

Show: as a → 0 (continuum limit), Wilson, HK, Manton, and Cl(3)-volume-form
all give `S → (1/2g²)∫Tr F²` to leading order. They differ at O(a²). The
framework's canonical normalization + Cl(3) tensor structure may fix the
O(a²) coefficient uniquely.

### R4.B — Cl(3) ⊗ Cl(3) tensor structure on adjacent sites

Cl(3) ⊗ Cl(3) ≅ M_2(C) ⊗ M_2(C) = M_4(C). The link-variable representation
on this 4-dim space has a natural action that may differ from Wilson and
HK both. **HIGH-VALUE EXPLORATORY: would derive both gauge group AND action
form from Cl(3) tensor structure.**

## Ranking by retained-positive probability

| Block | Route | Retained-positive prob | Runtime estimate | Risk |
|---|---|---|---|---|
| 01 | R1.A | HIGH | 60-90m | Low — well-established small-U matching |
| 02 | R2.A | HIGH (after R1.A) | 30-45m | Low — closed form |
| 03 | R3.A | MEDIUM | 90-120m | Medium — depends on Casimir-diagonal closure |
| 04 | R4.A | MEDIUM | 60-90m | Medium — uniqueness argument may not close |
| 04 | R4.B | LOW (high-EV speculative) | 90-120m | High — exploratory |

## Selection for execution

**Block 01 → R1.A (bi-invariant metric → t).** Highest retained-positive
probability, lowest risk, foundational for Blocks 02-04.
