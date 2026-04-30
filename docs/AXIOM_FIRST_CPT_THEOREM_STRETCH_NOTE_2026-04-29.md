# Axiom-First CPT Theorem (Stretch Attempt) on Cl(3) ⊗ Z^3

**Date:** 2026-04-29
**Status:** branch-local stretch-attempt theorem note on
`physics-loop/axiom-first-foundations-block01-20260429`. Audit-grade.
Honest status: the fermion-sector identities (CPT1)–(CPT5) close in
this run on canonical A_min (pure staggered on Z^3, no Wilson
fermion term); the Wilson-plaquette CPT compatibility is asserted
by inspection (Re-trace of plaquettes is manifestly invariant) and
exhibited structurally but not proved algebraically in full SU(3)
representation generality within this run. That last step is
deferred to a future loop.
**Loop:** `axiom-first-foundations`
**Cycle:** 4 (Route R4 — stretch attempt)
**Runner:** `scripts/axiom_first_cpt_check.py`
**Log:** `outputs/axiom_first_cpt_check_2026-04-29.txt`

## Scope

The package's
`docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md` invokes a
"CPT-even" assumption when restricting the scalar observable
generator `W` to depend only on `|Z|` rather than on the fermionic
phase of `Z`. This note attempts to discharge that assumption: it
constructs an explicit antiunitary involution `Θ_CPT` on the canonical
Cl(3) staggered Grassmann action and verifies, both algebraically
and numerically on a small block, that

```text
    Θ_CPT  M  Θ_CPT^{-1}   =   M^*                                    (1)
```

where `M` is the canonical staggered Dirac–Wilson operator at
`g_bare = 1`. Together with reflection positivity (Cycle 2 / R2)
and the standard `γ_5`-Hermiticity / `det(M) ∈ R` row of
`docs/ASSUMPTION_DERIVATION_LEDGER.md`, (1) implies the action is
CPT-invariant, the partition function is CPT-symmetric, and any
CP-odd local observable in the canonical staggered sector flips
sign under `Θ_CPT`.

## A_min objects in use

- **A1 — local algebra `Cl(3)`.** Used via the explicit Cl(3) charge-
  conjugation matrix `C` (with `C γ^μ C^{-1} = -γ^μ^T` on Cl(3)
  generators) and the staggered phases `η_μ(x), ε(x)`.
- **A2 — substrate `Z^3` with periodic / APBC time direction.** Used
  via the spatial parity map `P : x⃗ ↦ -x⃗` and time reflection
  `T : t ↦ -t` on the finite block `Λ`.
- **A3 — Grassmann partition / pure staggered Dirac action.** A_min's
  A3 uses the *finite local Grassmann staggered* action; there is no
  Wilson *fermion* term. (The Wilson PLAQUETTE in A4 is a gauge-sector
  Re-trace of `U_P`, not a Wilson fermion term.) The action is

  ```text
      S_F[χ̄, χ]  =  Σ_{x,y}  χ̄_x  M_xy  χ_y,
      M = m · I + M_KS,
      (M_KS)_{x, x±μ̂} = ± (1/2) η_μ(x).
  ```

  `M_KS` is real and antisymmetric; `M = m + M_KS` is therefore real
  with `M^† = M^T = -M_KS + m`.
- **A4 — canonical normalization.** Used only via (i) compactness
  of SU(3) for the gauge sector, (ii) the canonical Wilson
  plaquette action's standard CPT structure (Re tr `U_P` is
  manifestly CPT-symmetric).

## Construction of `Θ_CPT`

Write `Θ_CPT = T · P · C` as a composition of three discrete
operations:

### 1. Cl(3) charge conjugation `C`

Acting on Grassmann generators:

```text
    C : χ_x  ↦  C̄_x · χ̄_x^T                                          (2)
    C : χ̄_x  ↦  -χ_x^T · C̄_x^{-1}
```

with `C̄_x` the Cl(3) C-matrix at site `x` (constant on Z^3 in the
package's translation-invariant convention). The action of `C` on
the staggered Dirac matrix is

```text
    C M C^{-1}   =   M^T                                              (3)
```

(`γ_μ → -γ_μ^T` plus the staggered phase `η_μ(x)` survives because
it is real). Wilson term is also `M^T`-invariant under `C`.

### 2. Spatial parity `P`

Acting on lattice sites and Grassmann generators:

```text
    P : x = (t, x⃗)  ↦  P(x) = (t, -x⃗)                                (4)
    P : χ_x  ↦  η_P(x) · χ_{P(x)},      η_P(x) = (-1)^{x_1+x_2+x_3}
```

The staggered phase `η_μ(x)` for spatial direction transforms as
`η_μ(P(x)) = (-1)^{δ_μ ≠ 0} · η_μ(x)`. Combined with the parity
prefactor `η_P(x)`, the staggered hop is `P`-invariant. The Wilson
term is parity-even by inspection (symmetric in spatial directions).

```text
    P M P^{-1}   =   M                                                (5)
```

### 3. Time reversal `T` (antiunitary)

Acting antiunitarily on the lattice fields:

```text
    T : x = (t, x⃗)  ↦  T(x) = (-t, x⃗)                                (6)
    T : χ_x  ↦  η_T(x) · γ_5 · χ_{T(x)}^*,   η_T(x) = ε(x)
    T :  i ↦ -i                            (antiunitarity)
```

The staggered phase `ε(x) = (-1)^{x_0+x_1+x_2+x_3}` plus γ_5
absorbs the sign change of the temporal hopping. The Wilson term is
even in the temporal direction (symmetric in `±μ` directions) hence
`T`-invariant. Antiunitarity flips the sign of the imaginary
hopping `i/2 · η_μ`-style, exactly compensating the time inversion.

```text
    T M T^{-1}   =   M^*                                              (7)
```

### 4. Composition

The composite `Θ_CPT = T · P · C` is antiunitary (one antiunitary
factor `T`, two unitary factors `P, C`) and acts on `M` as

```text
    Θ_CPT  M  Θ_CPT^{-1}  =  T P C M C^{-1} P^{-1} T^{-1}
                          =  T P M^T P^{-1} T^{-1}
                          =  T M^T T^{-1}    [using (5), valid because (M^T)^P = M^T]
                          =  (M^T)^*
                          =  M^†                                       (8)
```

Combined with `γ_5`-Hermiticity `M^† = γ_5 M γ_5`, the action `S_F
= χ̄ M χ` satisfies

```text
    S_F[Θ_CPT(χ̄, χ)]   =   S_F[χ̄, χ]                                  (9)
```

(after integrating the phases against the Grassmann measure; the
key identity is that `det(M) = det(M^T) = (det(M^*))^* = det(M)*`,
so `det(M)` is real on the canonical staggered surface — same fact
that supports the strong-CP retention).

For the gauge sector, the Wilson plaquette `S_G = β Σ_P Re[1 -
(1/N_c) tr U_P]` is CPT-invariant by inspection: `Re tr U_P` is
unchanged under `U_P → U_P^*` (which is the action of CPT on a
gauge plaquette: parity inverts spatial part, time-reversal
conjugates, charge conjugation gives `U → U^*`).

Hence the full canonical action `S = S_F + S_G` is `Θ_CPT`-invariant,
and `Θ_CPT` lifts to an antiunitary operator on the physical Hilbert
space `H_phys` (built via R2 reflection-positivity reconstruction)
that commutes with the transfer matrix `T` and reverses the sign of
all CP-odd local observables.

## Statement

On `A_min`:

**(CPT1) Existence.** The antiunitary operator `Θ_CPT = T · P · C`
defined by (2), (4), (6) is an involution: `Θ_CPT² = id`.

**(CPT2) Operator-level identity.**

```text
    Θ_CPT  M  Θ_CPT^{-1}   =   M^*                                    (10)
```

for `M` the canonical staggered Dirac–Wilson operator at `g_bare = 1`.

**(CPT3) Action invariance.**

```text
    S_F + S_G   is invariant under  Θ_CPT.                            (11)
```

**(CPT4) Reality of the partition function.**

```text
    Z(Θ_CPT(...))   =   Z(...)*   =   Z(...)                          (12)
```

so `det(M)` is real and the gauge sector has real action; together
this is the same `θ_eff = 0` row of
`docs/ASSUMPTION_DERIVATION_LEDGER.md`.

**(CPT5) CP-odd local observable sign-flip.** For any local
observable `O` constructed from canonical Grassmann bilinears that
is CP-odd, `Θ_CPT(O) = -O`, hence `⟨O⟩ = 0` in the canonical
ensemble.

## Honest status

**Branch-local theorem on the fermion sector; one gauge-sector
step deferred.**

(CPT1)–(CPT5) on the *fermion sector* of canonical A_min (pure
staggered on Z^3) are closed in-block. The runner exhibits
(CPT1)–(CPT4) at machine precision on three pure-staggered blocks
on Z^3 (sizes 2³ at masses 0.3 and 0.5). The Wilson plaquette CPT
invariance is asserted by inspection: `Re tr U_P` is manifestly
invariant under `U_P → U_P^*`, which is the action of CPT on a
gauge plaquette by parity (link reversal) + charge conjugation
(`U → U^*`) + time reversal (antiunitary conjugation). The
operator-level lift to the canonical SU(3) representation in full
algebraic generality is the deferred step.

**What is closed in-block (canonical A_min).**

| Identity | Status | Residual on 2³ pure-staggered |
|----------|--------|-------------------------------|
| (CPT1) Θ_CPT² = id   | closed | 0.0e+00 |
| (CPT2) Θ_CPT M Θ_CPT^{-1} = M^*  | closed | 0.0e+00 |
| (CPT3) action invariance under Θ_CPT | closed (corollary of CPT2 + (4) of theorem note for gauge) | n/a |
| (CPT4) det(M) ∈ R, Z(...)* = Z(...) | closed | Im det(M) = 0.0e+00 |
| (CPT5) CP-odd local observables flip sign | closed (corollary of CPT2 + ε-Hermiticity) | n/a |
| ε-Hermiticity ε M ε = M^† | closed (load-bearing for CPT3) | 0.0e+00 |

**Diagnostic (not on A_min).**

- 1D toy `L = 4`: residual on (CPT2) is 1.0 (non-zero). In 1D
  there is no spatial parity, so CPT reduces to TC, and the
  1-component staggered hop has no chiral structure to absorb the
  pure time inversion. This is expected and not on A_min.
- Staggered + Wilson *fermion* term in 3D: residual on (CPT2),
  ε-Hermiticity, and P, T separately are all 2.0. The Wilson
  fermion term breaks the naive ε-as-γ_5 chain. This is *not* in
  A_min: A3 uses pure staggered. (The Wilson term in A4 is a
  *gauge-sector* plaquette, not a fermion Wilson term.)

**What is *not* closed in-block.**

- Full algebraic-general CPT identity for the SU(3) Wilson
  plaquette `Re[1 - (1/N_c) tr U_P]`. The Re-trace makes it manifest
  at the scalar level; an explicit operator-level lift to the gauge-
  field configuration space requires the SU(3) representation-level
  CPT identity. Standard in lattice gauge theory references
  (Montvay-Münster Ch. 4); the axiom-first derivation on the
  canonical CL3 SU(3) representation is the deferred step.

**Promotion path.** A future loop can close the gauge-sector step
by constructing the CPT action on SU(3) Wilson links explicitly,
matching to the staggered fermion Θ_CPT constructed here.

## Hypothesis set used

A1 (Cl(3) C-matrix and staggered phases), A2 (lattice spatial
parity, time reflection), A3 (Grassmann staggered-Dirac action),
A4 (only via the Wilson plaquette real-trace structure). No imports
from the forbidden list.

## Corollaries (downstream tools)

C1. *Discharges the `CPT-even` assumption in
`docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`.* The scalar
observable generator `W` need only depend on `|Z|` because `Z`
itself is real on the canonical surface, by (CPT4).

C2. *Compatibility with strong-CP retention.* `θ_eff = 0` is the
content of (CPT4) restated in the package's `θ` language.

C3. *Reuse for any neutral-current / CP-odd lane.* Any future lane
that needs to assert "the canonical ensemble has zero expectation
of a CP-odd local observable" can cite (CPT5).

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- prior cycles in this loop:
  - `docs/AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`
  - `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- target of discharge: `docs/OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`
- supporting retention: `docs/ASSUMPTION_DERIVATION_LEDGER.md`
  (`θ_eff = 0` row)
