# Bifundamental Invariance U(2)_L × U(2)_R on the Active Doublet Block — Obstruction Theorem

**Date:** 2026-04-17
**Status:** **OBSTRUCTION THEOREM** (CASE 3). Five independent sole-axiom derivations converge: the retained atlas does **not** support independent `U(2)_L × U(2)_R` bifundamental invariance on the active-sheet doublet block `K_doublet`. The conditional closure gate that the U(2)-invariance+quartic-isotropy obstruction identified is therefore **not available**.
**Script:** `scripts/frontier_dm_neutrino_source_surface_bifundamental_invariance_obstruction_theorem.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

The U(2)-invariance+quartic-isotropy obstruction identified a conditional closure gate for the selector gate: IF independent
`U(2)_L × U(2)_R` unitary invariance were axiom-native on the doublet block,
THEN the Frobenius functional `F1 = ||K_doublet||_F^2 = Tr(K_doublet^† K_doublet)`
would be uniquely pinned among `U(2)`-invariant positive-definite quadratic
invariants, and F1 would promote to a sole-axiom selector for `(delta, q_+)`
with closure at

```
(delta_*, q_+*) = ( sqrt(6)/2 - sqrt(2)/18 , sqrt(6)/6 + sqrt(2)/18 )
  ≈ (1.1461774513, 0.4868157106)
```

This note asks the sole-axiom question: is the bifundamental gauge
axiom derivable from `Cl(3)` on `Z^3` via the retained atlas?

The honest answer is **NO**. This note produces the obstruction theorem
with **five independent converging derivations**, each of which rules out
bifundamental invariance from the retained structure. The DM flagship
gate for selector therefore remains OPEN, and the Frobenius-route conditional
gate is closed as unavailable.

## Principal structural input (retained)

The ingredient that decides the question is the **Hermiticity** of the
carrier itself. Every retained atlas ingredient feeding the doublet
block reduces to a Hermitian 3×3 carrier on a single `C^3`, not an
arbitrary complex Yukawa with distinct left/right index spaces.

1. **Hermitian bridge carrier** (retained,
 [DM_NEUTRINO_HERMITIAN_BRIDGE_CARRIER_NOTE_2026-04-15](./DM_NEUTRINO_HERMITIAN_BRIDGE_CARRIER_NOTE_2026-04-15.md)):
 the DM denominator object is a Hermitian 3×3 matrix `H` with the
 seven-coordinate grammar `(d1, d2, d3, r12, r23, r31, phi)`.
2. **Positive-polar section** (retained,
 [DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15](./DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md)):
 the right `U(3)` frame has been **gauge-fixed** to the positive
 polar representative `Y_+(H) = H^{1/2}`. `K_+(H) = Y_+^† Y_+ = H` on
 this section. The "right" `U(3)` gauge has already been used up.
3. **Intrinsic `Z_3` readout** (retained,
 [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)):
 `K_Z3(H) = U_Z3^† H U_Z3` with `U_Z3` unitary. Therefore `K_Z3` is
 Hermitian, and its principal submatrices are Hermitian. In
 particular, the doublet block `K_doublet = K_Z3[1:3, 1:3]` is a
 Hermitian 2×2 matrix.
4. **Shift-quotient bundle** (retained,
 [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md)):
 the **only** gauge direction tangent to the live source-oriented
 sheet is the 1-real common diagonal shift
 `(d1, d2, d3) → (d1 + λ, d2 + λ, d3 + λ)`, equivalently `H → H + λ I`.
 The gauge Lie algebra of the live sheet is one-dimensional abelian.
5. **Three-generation observable algebra** (retained,
 [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)):
 the retained generation algebra on `H_hw=1 ≅ C^3` is `<P_1, P_2, P_3, C_3[111]>`,
 which generates `M_3(C)` acting **irreducibly** on a **single** `C^3`.
 This is a one-sided (adjoint) action on the single retained carrier,
 not a bifundamental action on a two-sided index space.

## Theorem (Bifundamental Obstruction on the Active Doublet Block)

**Theorem.** Let the active-sheet `Z_3` doublet block be
`K_doublet = K_Z3(H)[1:3, 1:3]` with the retained closed forms
```
K_11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3)) (real)
K_22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3)) (real)
K_12 = (m - 4 sqrt(2)/9) + i (sqrt(3) delta - 4 sqrt(2)/3)
K_21 = (K_12)*     (Hermiticity-forced)
```
Assume only the retained atlas ingredients (i)-(v) above. Then:

1. `K_doublet` is Hermitian, `K_doublet^† = K_doublet`, with exactly
 **four real parameters** `(K_11, K_22, Re K_12, Im K_12)`.
2. The only action that preserves the retained structure
 `K → U K U^†` with `U ∈ U(2)` has **three** real group parameters
 and acts diagonally on the (left, right) index pair. This is the
 **single** unitary adjoint `U(2)` — a **diagonal embedding**
 `U(2) ↪ U(2)_L × U(2)_R`, `U ↦ (U, U)`.
3. The independent bifundamental action `K → U_L K U_R^†`
 with `U_L, U_R ∈ U(2)` **does not preserve Hermiticity** in general.
 It is therefore **not** a symmetry of the space on which
 `K_doublet` lives.
4. No right-acting extension of the retained generation algebra
 `<P_1, P_2, P_3, C_3[111]>` commutes with Hermiticity of the
 active-sheet carrier. Every such extension either coincides with
 the diagonal `U(2)` (which is already in the retained structure) or
 breaks Hermiticity and exits the retained sheet.

**Consequence.** The conditional closure gate identified in
[DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17](./DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17.md)
is **not axiom-native retained**. The Frobenius functional `F1` remains
one point in the 2-parameter `U(2)`-invariant positive-definite quadratic
cone `{(A, B) : B < 0, A > -B/4}`, and F1 is **not** uniquely pinned by
any sole-axiom gauge argument available in the retained atlas.

**Claim label.** *Retained-atlas-native obstruction theorem.* No new
axiom. Direct structural consequence of Hermiticity of the active
carrier, the polar-section gauge fixing, the 1-dimensional shift-quotient
gauge algebra, and irreducibility of the retained generation algebra on
a single carrier.

## Five independent converging derivations

The theorem is robust: each of the five attack lines specified in the
this specification produces an independent derivation of the same
obstruction.

### L1 — Polar decomposition route: gauge budget already spent

The retained polar section sets
`Y = H^{1/2} U_R` with `U_R ∈ U(3)`, and fixes `U_R = I` as the
positive representative. On this section, `K_+(H) = Y^† Y = H`. The
right `U(3)` freedom that could have provided a separate right-handed
doublet block gauge has been **explicitly consumed** by the positive
section. The carrier the doublet block is read from is `H` — a single
Hermitian object — not `(H_L, H_R)`.

Any attempt to re-inject a right `U(n)` action after the positive polar
section has been taken re-opens the right-frame obstruction theorem
(retained,
[DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15](./DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md)):
the unconditionally-available data are not invariant under right
rotations away from the positive polar representative. The positive
section is the unique intrinsic representative; there is no gauge
freedom left for `U_R`.

**L1 verdict: bifundamental invariance is NOT derivable. U(2)_R
has already been gauge-fixed.**

### L2 — Dirac bridge route: the retained local operator is Hermitian

The Dirac-bridge theorem (retained,
[DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md))
selects `M(phi) = Gamma_1` as the unique post-EWSB local Dirac
operator on `C^16`. `Gamma_1` is **Hermitian** (`M(phi)^† = M(phi)` and
`M(phi)^2 = |phi|^2 I`). The retained local Dirac lane is therefore
**not** the kind of object `Y_nu` that transforms bifundamentally
under independent `U(n)_L × U(n)_R`.

In Standard Model language: the retained atlas does not distinguish a
left-doublet flavor index from a right-singlet flavor index. The
generation indices on both sides are the **same** `hw=1` triplet —
identical carrier, identical `Z_3` grading — with `C_3[111]` cycling
both simultaneously. A bifundamental `U(n)_L × U(n)_R` distinguishes
two copies; the retained structure does not produce two copies.

**L2 verdict: bifundamental invariance is NOT derivable. The retained
Dirac surface has no separate L/R index spaces.**

### L3 — Carrier normal form + shift-quotient bundle: 1-dim gauge

The shift-quotient theorem (retained,
[DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md))
states explicitly that the gauge Lie algebra on the live source-oriented
sheet is **1-dimensional** — the common diagonal shift
`H → H + λ I`.

The bifundamental gauge algebra `u(2)_L ⊕ u(2)_R` on the doublet block
is `2 · (4) = 8`-dimensional, with independent left and right blocks.
Of these 8 generators, the retained sheet supports:

- **1 generator** (the `λ I` shift, which is the diagonal
 `(I, I) ∈ u(2)_L ⊕ u(2)_R` restricted to `λ · I_2` on the doublet block
 after quotienting by the singlet slot — itself a further restriction).
- **7 generators are absent** from the retained tangent space.

The retained gauge Lie algebra on the doublet block is therefore at
most `u(1)` (the common diagonal shift). Not `u(2)_L ⊕ u(2)_R` = 8D,
not `u(2)_L ⊕ u(1)` = 7D, not even `u(1)_L ⊕ u(1)_R` = 2D.

**L3 verdict: bifundamental invariance is NOT derivable. The retained
gauge has 1 generator; bifundamental needs 8.**

### L4 — Z_3 support trichotomy: one Higgs charge locks L and R together

The Z_3-support trichotomy (retained,
[NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE](./NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md))
constrains Dirac Yukawa entries by

```
q_L(i) + q_H + q_R(j) = 0 mod 3
```

with `q_L = (0, +1, -1)` and `q_R = (0, -1, +1) = -q_L` (conjugate
triplets). Fixing `q_H` pins each row and column to a single entry,
producing the three allowed supports {diagonal, forward cyclic,
backward cyclic}.

A candidate independent action `Y_nu → U_L Y_nu U_R^†` with independent
`U_L, U_R ∈ U(2)` on the doublet block `(i, j) ∈ {2, 3} × {2, 3}`
generically mixes rows across `Z_3`-charge levels (e.g. maps a
`q_L = +1` row to a linear combination of `q_L = +1` and `q_L = -1`
rows). But the Z_3-charge labels `q_L, q_R` are **retained** data —
they label the concrete `hw=1` eigensectors under the retained cyclic
`C_3[111]` operator.

Consequently the **only** independent left action `U_L` that preserves
the retained Z_3 structure is the one that preserves each charge level
separately — a **diagonal** `U(1)^3` on the three generations, i.e. a
torus `T^3_L`. Likewise `T^3_R` on the right. And `U_L × U_R` modulo
the `q_L + q_H + q_R = 0 mod 3` constraint locks to a **single** `T^2`,
not an independent `T^3_L × T^3_R = T^6`.

Restricted to the doublet block `(2, 3) × (2, 3)`, the preserved
independent abelian gauge on the Z_3-support doublet sector is at most
`U(1)_L × U(1)_R` modulo the charge constraint, which is **1-dimensional
abelian** — and only **phase** rotations, not full `U(2)` rotations.

**L4 verdict: bifundamental invariance is NOT derivable. The Z_3
charge constraint collapses `U(n)_L × U(n)_R` to at most a 1-dimensional
phase torus, modulo a single Higgs charge.**

### L5 — Observable-principle argument: scalar baseline forces single adjoint

The observable-principle generator
[OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
is `W[J] = log|det(D + J)| − log|det D|`. For a NON-Hermitian complex
`D`, `det(U_L D U_R^†) = det(U_L) det(U_R^†) det(D)` so
`W[J; D = D_0]` transforms covariantly (with a phase/volume factor)
under `D → U_L D U_R^†`, `J → U_L J U_R^†`. This is the usual
bifundamental structure on a flat Yukawa matrix.

But the retained atlas forces the **Schur-baseline** `D = m I_3`
(retained,
[DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)).
Under Schur's lemma on the irreducible retained `M_3(C)`-algebra on
`H_hw=1`, the only commuting operator with the full retained generation
algebra is a **scalar multiple of the identity**.

For the scalar baseline `D = m I`, the bifundamental orbit `U_L D U_R^†`
reduces to `m · U_L U_R^†`. The two independent unitaries collapse to
the **single** combined unitary `U_L U_R^†`, and `W[J; m I]` is
invariant only under the single adjoint
`J → U J U^†` with `U = U_L U_R^†`. The 8-dimensional `u(2)_L ⊕ u(2)_R`
has been collapsed to the **3-dimensional** diagonal embedding.

This is not an accident. On the retained chart where `D = m I_3` is
forced, the Yukawa-matrix index structure collapses: left and right
indices are identified by Schur, and the bifundamental action becomes
a single adjoint action. The single `U(2)` on the doublet block is
exactly what is already retained (the `U(2)`-invariant quadratic cone
of the U(2)-invariance+quartic-isotropy obstruction Line 1). There is no extra invariance to be pinned
down.

**L5 verdict: bifundamental invariance is NOT derivable. Schur's
lemma on the scalar baseline `D = m I` collapses `U_L × U_R` into a
single adjoint `U`.**

## Convergence table

| Line | Argument | Reduction |
|------|----------|-----------|
| L1 | Polar section already gauge-fixed `U_R` | `U(3)_R → {I}` |
| L2 | Retained Dirac is Hermitian (Gamma_1) | No separate L/R index space |
| L3 | Shift-quotient gauge is 1D | `u(2)_L ⊕ u(2)_R` (8D) → `u(1)` (1D) |
| L4 | Z_3 charge constraint locks L and R | `U(n)_L × U(n)_R` → 1D phase |
| L5 | Schur on scalar baseline collapses | `U_L U_R^†` → single adjoint `U` |

**All five lines converge on the same conclusion:** the retained atlas
supports at most a **single** `U(2)` adjoint action on the Hermitian
`K_doublet`, not independent `U(2)_L × U(2)_R` bifundamental action.

## Weaker invariances already in the retained atlas (flagged)

The discipline question from the mission brief: is `F1` uniquely pinned
by any weaker invariance already in the atlas? We check and answer NO:

- **Single diagonal `U(2)` adjoint** (retained): every U(2)-invariant
 PD quadratic is in the 2-parameter cone
 `F_{A,B}[K] = A (Tr K)^2 + B det K` with `B < 0, A > -B/4`. F1 is
 one point `(A, B) = (1, -2)` in this cone. *Not uniquely pinned.*
- **Retained `Z_3` cyclic `C_3[111]`** (retained): the Z_3-parity
 decomposition (
 [DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17](./DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md))
 sends any Z_3-parity-definite scalar to either a (δ)-only or (q_+)-only
 function; F1 is parity-mixing, so Z_3 cyclic invariance is consistent
 with F1 but also consistent with F2 = det K, F3 = traceless Frobenius,
 etc. *Not uniquely pinned.*
- **Common diagonal shift `H → H + λ I`** (retained): the shift acts
 trivially on the doublet block (since `K_11 + K_22` receives only a
 constant contribution from the shift that is `(δ, q_+)`-independent),
 so the shift cannot discriminate between F1 and any other quadratic.
 *Not uniquely pinned.*
- **CP involution `K → K*`** (from the real Majorana rotation): acts
 as `K_12 → K_12*` on the doublet block; all three of F1, F2, F3 are
 CP-invariant. *Not uniquely pinned.*

Conclusion: no weaker invariance already retained in the atlas pins
F1 uniquely. The only invariance that would pin F1 is exactly the
bifundamental invariance that this note proves unavailable.

## What this note newly closes

1. **Conditional gate is closed as unavailable.** The conditional
 closure path flagged in the U(2)-invariance+quartic-isotropy obstruction theorem
 [DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17](./DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17.md)
 ("IF `U(2)_L × U(2)_R` bifundamental invariance is axiom-native, THEN
 F1 is uniquely pinned and the selector gate closes at (sqrt(6)/2 − sqrt(2)/18,
 sqrt(6)/6 + sqrt(2)/18)") is settled: the IF-clause is **not**
 derivable from the retained atlas. The Frobenius-route candidate
 closure is therefore **not** a sole-axiom closure of the selector gate.
2. **Hermiticity of `K_doublet` is promoted to a theorem-grade
 structural fact.** Every attack line that assumes a non-Hermitian
 `K_doublet` is post-axiom: the retained chain
 `Y → H = Y Y^† → K_Z3 = U_Z3^† H U_Z3 → K_doublet = K_Z3[1:3, 1:3]`
 manifestly produces a Hermitian object at every stage. Hermiticity
 is not a choice; it is a theorem.
3. **Gauge-algebra dimension is a new retained invariant.** The gauge
 algebra on the active sheet has dimension 1 (the common diagonal
 shift). Any candidate symmetry argument that requires an
 `n > 1`-dimensional action must justify the extra generators from
 the retained structure; this note shows no retained object does.
4. **Schur-collapse lemma at scalar baseline.** On `D = m I`,
 `U_L D U_R^† = m U_L U_R^†`, which means the bifundamental action
 collapses to the single adjoint `U = U_L U_R^†`. This is a new
 structural lemma on the scalar-baseline chart.

## What this note does NOT do

- does not close selector (the flagship gate remains OPEN)
- does not rule out F1 as a **physical** candidate; it rules out the
 sole-axiom promotion of F1 via bifundamental invariance
- does not prevent Physics-Validation from cross-checking the F1
 candidate point via `eta / eta_obs = 1` (that is a separate
 physical-observable route)
- does not rule out that some **other** sole-axiom selection principle,
 not based on gauge invariance, could pin F1 (e.g., an
 entropy-minimization / variational / holonomy principle that still
 needs to be derived)
- does not introduce any new axiom

## Downstream implications

1. **Frobenius-route narrowed-gap classification consolidated.** The
 parity-mixing / F1 line is now categorized as "narrower-gap via
 functional-selection ambiguity, and the bifundamental-gauge route
 is unavailable". The five-candidate ledger stays intact; F1 is not
 promoted.
2. **Attention refocused to other retained structures.** The closure
 of the selector gate via sole-axiom must come from:
 (a) an info-geometric / entropy selector that solves the `(G-Var)`
 problem of the info-geometric selection obstruction, or
 (b) a higher-structure retained invariant (trace of `H^n` for `n > 4`,
 Pfaffian-like, Cartan-Killing pulled back through a retained
 representation), or
 (c) a physical-observable / Physics-Validation cross-check that
 picks one of the five candidate points empirically (followed
 by a retrospective sole-axiom explanation of why the other four
 miss).
3. **Bifundamental structure stays a marker of the SM input channel
 but not of the retained axiom.** Conversations that reach for the
 SM Yukawa-matrix bifundamental gauge to close retained atlas gates
 should be flagged: the retained atlas is **Hermitian-data-first** by
 construction (positive polar section, intrinsic Z_3 readout). The
 SM-style L/R decomposition is downstream and not a source of
 retained symmetry.

## Runner verification

The runner `scripts/frontier_dm_neutrino_source_surface_bifundamental_invariance_obstruction_theorem.py`
verifies, against the retained atlas:

A. **Hermiticity of K_doublet** on the active sheet for random
 `(m, delta, q_+)` points.
B. **Non-Hermitian transform** under generic bifundamental
 `K → U_L K U_R^†`: Hermiticity is broken.
C. **Hermitian transform preserved** under diagonal `K → U K U^†`:
 Hermiticity survives, confirming the single-adjoint `U(2)` is the
 correct retained gauge.
D. **Frobenius preserved under bifundamental action on the non-Hermitian
 linear space** (the U(2)-invariance+quartic-isotropy obstruction Line 1 re-verification): this is the
 mathematical fact that `F1` would be pinned IF the bifundamental
 gauge were axiom-native.
E. **Polar section uniqueness**: for random full-rank `H`, the positive
 polar representative `Y_+ = H^{1/2}` is unique and the right `U(3)`
 gauge is completely consumed.
F. **Shift-quotient gauge algebra dimension**: the retained tangent
 space of the live source-oriented sheet under common diagonal shift
 `λ I` is 1-dimensional; no additional `U(2)_L ⊕ U(2)_R` generators
 are tangent to the retained sheet.
G. **Schur-collapse**: for `D = m I`, the bifundamental orbit
 `U_L D U_R^†` reduces to `m U_L U_R^†`, confirming the
 single-adjoint collapse.
H. **Z_3-support trichotomy locks L and R**: independent 2×2 unitary
 actions on the doublet block `(i, j) ∈ {2, 3}` generically break
 the `q_L + q_H + q_R = 0 mod 3` support constraint.
I. **Weaker retained invariances do not pin F1**: each of single
 adjoint `U(2)`, Z_3 cyclic, shift, and CP independently admits the
 full 2-parameter PD cone.
J. **Conclusion: bifundamental invariance is NOT derivable from the
 retained atlas**: all five attack lines converge on obstruction.

Current expected harness counts: see runner output
(`PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_bifundamental_invariance_obstruction_theorem.py`).

## Atlas inputs used

All retained / theorem-grade on the integration branch:

- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md)
- [DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_POSITIVE_POLAR_H_CP_THEOREM_NOTE_2026-04-15.md)
- [DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md](./DM_NEUTRINO_POSTCANONICAL_POLAR_SECTION_NOTE_2026-04-15.md)
- [DM_NEUTRINO_HERMITIAN_BRIDGE_CARRIER_NOTE_2026-04-15.md](./DM_NEUTRINO_HERMITIAN_BRIDGE_CARRIER_NOTE_2026-04-15.md)
- [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- [NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md](./NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md)
- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_PARITY_SPLIT_THEOREM_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_PARITY_MIXING_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_PARITY_MIXING_SELECTION_OBSTRUCTION_NOTE_2026-04-17.md)
- [DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_QUARTIC_ISOTROPY_AND_U2_OBSTRUCTION_NOTE_2026-04-17.md)
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)

No new axioms are introduced.

## Narrowed-gap statement

**Before this note (after the U(2)-invariance+quartic-isotropy obstruction):**
```
Line 1 produced a CONDITIONAL closure gate: IF U(2)_L × U(2)_R bifundamental
invariance on the doublet block is axiom-native retained, THEN F1 is uniquely
pinned and the selector gate closes at (sqrt(6)/2 − sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18).
The gate's antecedent was not derived; the atlas status was "unretained,
pending sole-axiom derivation".
```

**After this note:**
```
The antecedent of the conditional gate is FALSIFIED by the retained atlas.
Five independent derivations (polar gauge-fixing, Hermitian-Dirac, 1D
shift-quotient, Z_3 charge-locking, Schur-collapse) show bifundamental
U(2)_L × U(2)_R invariance on the doublet block is NOT derivable from
Cl(3) on Z^3. The conditional gate is therefore unavailable, and F1 is
not promoted to a sole-axiom selector via this route. The five-candidate
ledger from the parity-mixing note remains open; closure must proceed
via another retained route (not Frobenius-bifundamental-gauge).
```

## Position on publication surface

Appropriate placement:

- atlas obstruction row in
 [DERIVATION_ATLAS.md](./publication/ci3_z3/DERIVATION_ATLAS.md) under
 the DM neutrino source-surface family, sibling to the info-geometric / Z_3-cubic / parity-split obstructions, the
 parity-mixing note, the observable-bank exhaustion theorem, and the quartic-isotropy+U(2) obstruction
- **do NOT** use for any publication-grade positive quantitative claim
- **do NOT** use to "support" the Schur-Q candidate — this note does
 not favor any one of the five candidate points; it rules out one
 specific closure-via-gauge route for F1

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_bifundamental_invariance_obstruction_theorem.py
```

## What this file must never say

- that selector is closed
- that the DM flagship gate is closed
- that F1 is uniquely pinned by any sole-axiom invariance
- that bifundamental invariance is axiom-native retained (the opposite
 is proven)
- that F1 has been promoted or demoted as a physical candidate;
 Physics-Validation via `eta / eta_obs = 1` is a separate cross-check
- that the other four candidates in the five-candidate ledger have been
 ruled in or out

If any future revision of this note tightens those boundaries, it must
cite a new source on the live retained/promoted surface. Until then, the
safe read is: **bifundamental gauge invariance is NOT derivable from
Cl(3)/Z^3 on the active doublet block (CASE 3 obstruction). The
Frobenius-route conditional closure gate is unavailable. selector remains
OPEN with five inequivalent candidate points now on record, none
promoted to theorem-grade.**
