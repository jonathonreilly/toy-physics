# Axiom-First CPT Theorem (Stretch Attempt) on Cl(3) ⊗ Z^3

**Date:** 2026-04-29 (originally); 2026-05-10 (scope-split repair as
`audited_conditional`: separate the in-block fermion-sector CPT
identities from the deferred SU(3) Wilson-plaquette gauge-sector lift,
and rebase hypothesis set on
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) with the
staggered-Dirac realization gate named in
`admitted_context_inputs`).
**Status:** source-note proposal — author-declared `bounded_theorem`;
effective status set only by the independent audit lane.
**Claim type:** bounded_theorem
**Loop:** `axiom-first-foundations`
**Cycle:** 4 (Route R4 — stretch attempt)
**Runner:** [`scripts/axiom_first_cpt_check.py`](../scripts/axiom_first_cpt_check.py)
**Log:** `outputs/axiom_first_cpt_check_2026-04-29.txt`

## Authority disclaimer

This is a source-note proposal. Effective `effective_status` is generated
by the audit pipeline only after the independent audit lane reviews the
claim, dependency chain, and runner. The `claim_type`, scope, named
admissions, and bounded classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Scope-split repair (2026-05-10)

The 2026-05-10 audit verdict (`audited_conditional`) recorded
`scope_too_broad` and asked to either (a) split the clean
pure-staggered fermion-sector CPT identities from the deferred SU(3)
Wilson-plaquette extension, or (b) close the gauge-sector operator-level
lift directly. The note had also been written against the April-15
`A_min` framing (A1, A2, A3 = staggered/Grassmann, A4 = canonical
normalization) which has been superseded by
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).

This 2026-05-10 repair takes path (a) and rebases the hypothesis set:

- **(R1) Authority rebase.** The hypothesis set is rebased on
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md). Only
  `A1` (Cl(3) per-site algebra) and `A2` (`Z^3` substrate) are framework
  axioms here. The Grassmann staggered-Dirac action is admitted as a
  named open-gate input under `admitted_context_inputs`. The proof is a
  bounded fermion-sector CPT identity on the admitted staggered carrier.
- **(R2) Scope split.** The in-block result is split explicitly into
  - **(I) Fermion-sector identities (CPT1)–(CPT5) on the admitted
    staggered carrier**: closed in-block to machine precision on the
    `2³` pure-staggered runner blocks at masses `0.3` and `0.5` (runner
    `axiom_first_cpt_check.py`). This is the bounded fermion-sector
    theorem this note proposes for audit.
  - **(II) SU(3) Wilson-plaquette gauge-sector CPT lift**: explicitly
    **deferred** as an open derivation target. The argument by
    inspection (`Re tr U_P` invariant under `U_P → U_P^*`) is recorded
    as a structural observation, not as an in-note operator-level
    theorem. The SU(3) representation-level CPT identity for the Wilson
    plaquette is the open gate; closing it requires a separate axiom-
    first lift on the canonical SU(3) representation.
- **(R3) Action-invariance scope narrowing.** The action-invariance
  identity (CPT3) of the original note was stated for the full
  canonical action `S = S_F + S_G`. After the split it is restated for
  `S_F` only on the admitted staggered carrier; the `S_F + S_G`
  invariance is conditional on path (II) closing and is recorded in
  Honest status as an admitted-context corollary, not an in-block
  theorem.

## Scope (post-split, 2026-05-10)

The package's
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
invokes a "CPT-even" assumption when restricting the scalar observable
generator `W` to depend only on `|Z|` rather than on the fermionic phase
of `Z`. This note proposes a bounded fermion-sector identity that is
the natural in-block step toward discharging that assumption: it
constructs an explicit antiunitary involution `Θ_CPT` on the **admitted
canonical staggered Grassmann action** (named open gate per
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)) and
verifies, both algebraically and numerically on small pure-staggered
blocks, that

```text
    Θ_CPT  M  Θ_CPT^{-1}   =   M^*                                    (1)
```

where `M` is the staggered Dirac operator (no Wilson fermion term;
canonical normalization is admitted as a separate named input — see
"Hypothesis set used"). The in-block conclusion is then a bounded
fermion-sector CPT identity (CPT1)–(CPT5) on the admitted staggered
carrier.

**Out of scope (post-split).** Discharge of the OBSERVABLE_PRINCIPLE
"CPT-even" premise on the **full canonical action** `S_F + S_G` (i.e.
including the SU(3) Wilson-plaquette gauge sector at the operator level)
is **not** in scope on this note. That step requires the deferred
SU(3) Wilson-plaquette CPT lift named in (R2)(II); when that gate
closes, the discharge of the "CPT-even" premise lifts to the full
canonical action by composition.

## Hypothesis set used (post-split, 2026-05-10)

The proof uses the two repo baseline inputs recorded in
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md), plus
two **named admitted inputs** corresponding to open gates in that memo:

**Framework baseline inputs (current):**

- **physical `Cl(3)` local algebra** (legacy alias: `A1`). Used via the explicit Cl(3) charge-
  conjugation matrix `C` (with `C γ^μ C^{-1} = -γ^μ^T` on Cl(3)
  generators) and the staggered phases `η_μ(x), ε(x)`.
- **`Z^3` spatial substrate** (legacy alias: `A2`) with periodic / APBC time direction. Used
  via the spatial parity map `P : x⃗ ↦ -x⃗` and time reflection
  `T : t ↦ -t` on the finite block `Λ`.

**Admitted context inputs (open gates per current axiom memo):**

- **`staggered_dirac_realization_gate`.** The Grassmann partition with
  pure staggered Dirac action

  ```text
      S_F[χ̄, χ]  =  Σ_{x,y}  χ̄_x  M_xy  χ_y,
      M = m · I + M_KS,
      (M_KS)_{x, x±μ̂} = ± (1/2) η_μ(x).
  ```

  `M_KS` is real and antisymmetric; `M = m + M_KS` is therefore real
  with `M^† = M^T = -M_KS + m`. There is **no Wilson fermion term**.
  Per [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  line 162 (lanes that depend on the staggered-Dirac realization gate),
  this surface is admitted under named open-gate input until that gate
  closes.

- **`g_bare_canonical_normalization_gate`** (only for the Wilson
  plaquette structural observation; **not** load-bearing for the
  in-block fermion-sector identities (CPT1)–(CPT5)). Per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) line
  185 (lanes that depend on the g_bare gate). The in-block claim of
  this note is **independent** of this gate; the gate is named only for
  the deferred (R2)(II) Wilson-plaquette gauge-sector lift.

**Out-of-scope ingredients (deferred upstream gates):**

- **SU(3) Wilson plaquette operator-level CPT identity.** The Wilson
  plaquette `S_G = β Σ_P Re[1 - (1/N_c) tr U_P]` is structurally
  CPT-compatible by inspection on the Re-trace; the explicit operator-
  level lift to the canonical SU(3) representation is **not** closed in
  this note (see scope-split repair (R2)(II) above). The SU(3)
  Wilson-plaquette CPT lift is therefore a deferred open derivation
  target, not an in-block theorem of this note.

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

(`γ_μ → -γ_μ^T` plus the staggered phase `η_μ(x)` survives because it
is real). The admitted staggered carrier has no Wilson fermion term;
the diagnostic in "Honest status" below records the Wilson-fermion-term
residual `2.0` and confirms that surface is out of scope.

### 2. Spatial parity `P`

Acting on lattice sites and Grassmann generators:

```text
    P : x = (t, x⃗)  ↦  P(x) = (t, -x⃗)                                (4)
    P : χ_x  ↦  η_P(x) · χ_{P(x)},      η_P(x) = (-1)^{x_1+x_2+x_3}
```

The staggered phase `η_μ(x)` for spatial direction transforms as
`η_μ(P(x)) = (-1)^{δ_μ ≠ 0} · η_μ(x)`. Combined with the parity
prefactor `η_P(x)`, the staggered hop is `P`-invariant.

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
absorbs the sign change of the temporal hopping. Antiunitarity flips
the sign of the imaginary hopping `i/2 · η_μ`-style, exactly
compensating the time inversion.

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
(1/N_c) tr U_P]` is structurally CPT-compatible by inspection (`Re tr
U_P` is unchanged under `U_P → U_P^*`). The operator-level lift on the
canonical SU(3) representation is the **deferred** (R2)(II) gate
above; it is **not** closed in this note. The structural Re-trace
observation is recorded for orientation only and is not a load-bearing
step of any in-block theorem below.

Conditional on the deferred (R2)(II) gate closing, `Θ_CPT` lifts to an
antiunitary operator on the physical Hilbert space `H_phys` (built via
the reflection-positivity reconstruction sibling note) that commutes
with the transfer matrix `T` and reverses the sign of all CP-odd local
observables. This conditional corollary is **not** an in-block theorem
of this note.

## Statement (post-split, 2026-05-10)

Under the physical `Cl(3)` local algebra and `Z^3` spatial substrate
baseline (legacy aliases `A1`/`A2`) of
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md) plus the
named admitted `staggered_dirac_realization_gate` input (see
"Hypothesis set used"), the in-block bounded fermion-sector theorem is:

**(CPT1) Existence.** The antiunitary operator `Θ_CPT = T · P · C`
defined by (2), (4), (6) is an involution: `Θ_CPT² = id`.

**(CPT2) Operator-level identity.**

```text
    Θ_CPT  M  Θ_CPT^{-1}   =   M^*                                    (10)
```

for `M` the admitted staggered Dirac operator (no Wilson fermion term).

**(CPT3) Fermion-sector action invariance** (scope-narrowed, post-split).

```text
    S_F   is invariant under  Θ_CPT.                                  (11)
```

The full-action invariance `S_F + S_G is invariant under Θ_CPT` is
**not** asserted as an in-block theorem; it lifts conditionally on the
deferred (R2)(II) Wilson-plaquette gauge-sector CPT gate closing.

**(CPT4) Reality of the fermion-sector determinant.**

```text
    det(M) ∈ R                                                        (12)
```

so the fermion-sector contribution to the partition function is real.
The full-`Z` reality, including the gauge-sector measure, is
conditional on the deferred (R2)(II) gate.

**(CPT5) CP-odd fermion-sector local observable sign-flip.** For any
local observable `O` constructed from admitted-staggered Grassmann
bilinears that is CP-odd, `Θ_CPT(O) = -O`, hence `⟨O⟩_F = 0` in the
fermion-sector ensemble. The same statement on the full ensemble is
conditional on the deferred (R2)(II) gate.

## Honest status (post-split, 2026-05-10)

**Bounded fermion-sector theorem on the admitted staggered carrier;
SU(3) Wilson-plaquette gauge-sector lift deferred.**

(CPT1)–(CPT5) on the **fermion sector** of the admitted staggered
carrier (pure staggered on `Z^3`, no Wilson fermion term) are closed
in-block to machine precision on three pure-staggered runner blocks
(sizes `2³` at masses `0.3` and `0.5`). The runner exhibits these
identities directly; the runner-level table below is unchanged from
the original run.

**What is closed in-block (admitted staggered carrier).**

| Identity | Status | Residual on 2³ pure-staggered |
|----------|--------|-------------------------------|
| (CPT1) `Θ_CPT² = id`                                     | closed in-block | 0.0e+00 |
| (CPT2) `Θ_CPT M Θ_CPT^{-1} = M^*`                        | closed in-block | 0.0e+00 |
| (CPT3) `S_F` invariance under `Θ_CPT` (fermion-sector)   | closed in-block (from CPT2) | n/a |
| (CPT4) `det(M) ∈ R`                                      | closed in-block | `Im det(M) = 0.0e+00` |
| (CPT5) Fermion-sector CP-odd local observables flip sign | closed in-block (from CPT2 + ε-Hermiticity) | n/a |
| `ε`-Hermiticity `ε M ε = M^†`                            | closed in-block (load-bearing for CPT3 on `S_F`) | 0.0e+00 |

**Diagnostic (not in scope).**

- 1D toy `L = 4`: residual on (CPT2) is 1.0 (non-zero). In 1D there
  is no spatial parity, so CPT reduces to TC, and the 1-component
  staggered hop has no chiral structure to absorb the pure time
  inversion. This is expected and not in scope on this row.
- Staggered + Wilson *fermion* term in 3D: residual on (CPT2),
  `ε`-Hermiticity, and `P, T` separately are all 2.0. The Wilson
  fermion term breaks the naive `ε`-as-`γ_5` chain. This is **not**
  in scope: the admitted staggered-Dirac realization gate uses pure
  staggered. (The Wilson term in the deferred (R2)(II) gate is a
  gauge-sector plaquette, not a fermion Wilson term.)

**What is *not* closed in-block (deferred upstream gate).**

- **(R2)(II) SU(3) Wilson-plaquette operator-level CPT lift.** Full
  algebraic-general CPT identity for the SU(3) Wilson plaquette
  `Re[1 - (1/N_c) tr U_P]` at the operator level is the deferred
  upstream gate; it requires the SU(3) representation-level CPT
  identity. The structural Re-trace observation is recorded for
  orientation only and is not a load-bearing step of any in-block
  theorem above. The full-action invariance `S_F + S_G is invariant
  under Θ_CPT`, the full-`Z` reality, and the discharge of the
  OBSERVABLE_PRINCIPLE "CPT-even" premise on the full canonical
  action all lift conditionally on this gate closing.

**Promotion path.** When the deferred (R2)(II) Wilson-plaquette
gauge-sector CPT lift closes upstream and the named admitted
`staggered_dirac_realization_gate` closes per
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md), this
row becomes eligible for retagging by the independent audit lane.

## Corollaries (downstream tools)

C1. *Partial discharge of the `CPT-even` assumption in
[`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md).*
The fermion-sector contribution to the scalar observable generator
`W` need only depend on `|Z|` because the fermion-sector determinant
is real, by (CPT4). Discharge of the "CPT-even" premise on the full
canonical action (including the gauge-sector Wilson-plaquette
contribution) is conditional on the deferred (R2)(II) gate.

C2. *Fermion-sector compatibility with strong-CP retention.* The
content of (CPT4) restated in the `θ` language gives `θ_F^{eff} = 0`
on the fermion-sector determinant; the full `θ_eff = 0` row of the
package's strong-CP retention is conditional on the deferred (R2)(II)
gate.

C3. *Reuse for any fermion-sector neutral-current / CP-odd lane.*
Any future lane that needs to assert "the fermion-sector ensemble
on the admitted staggered carrier has zero expectation of a CP-odd
local observable" can cite (CPT5). The full-ensemble version is
conditional on (R2)(II).

## Citations

- Current axiom memo:
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  (supersedes the April-15 `A_min` framing the original note used).
- Prior cycles in this loop:
  - [`AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_SPIN_STATISTICS_THEOREM_NOTE_2026-04-29.md)
  - [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
  - [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
- Target of partial discharge:
  [`OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  (`audit_status: audited_conditional`, `claim_type: bounded_theorem`).
- Related assumption ledger: [`ASSUMPTION_DERIVATION_LEDGER.md`](ASSUMPTION_DERIVATION_LEDGER.md)
  (`θ_eff = 0` row), cited as related, not as in-note closure for the
  deferred (R2)(II) gate.
