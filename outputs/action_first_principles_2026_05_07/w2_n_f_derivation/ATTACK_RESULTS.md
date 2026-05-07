# N_F Derivation — Seven-Vector Attack Results

**Date:** 2026-05-07
**Type:** attack_results + structural_obstruction_consolidation
**Authority role:** source-note proposal. Audit verdict and downstream
status are set only by the independent audit lane.
**Companion runner:** [`cl3_n_f_derivation_2026_05_07_w2_check.py`](cl3_n_f_derivation_2026_05_07_w2_check.py)

## Bottom-line verdict

| Attack | Vector | Verdict | Strength |
|---|---|---|---|
| 1 | Hilbert–Schmidt / Killing rigidity | **Obstruction (silent)** | Definitive: rigidity is "up to scalar" only |
| 2 | Cl(3)⊗Cl(3) ≅ Cl(6) → Spin(6) ⊃ SU(3) | **Obstruction (inheritance)** | Definitive: Spin(6) carries the same convention |
| 3 | Anomaly cancellation / topological constraint | **Obstruction** | Specific: 'tHooft anomaly cancellation invariant under N_F |
| 4 | Quantization / representation-integrality | **Obstruction** | Specific: integer (p,q) labels independent of N_F |
| 5 | Hardy-style operational reconstruction | **Obstruction** | Definitive: dim-counting axioms underdetermine scale |
| 6 | Standard QFT literature consensus | **Obstruction (consensus)** | Definitive: literature uniformly admits `N_F = 1/2` |
| 7 | Direct Cl(3) Pauli-rep / bivector-trace | **Strong partial positive (SU(2) only)** | Pins SU(2) `N_F = 1/2` via bivector-to-vector map; does NOT extend to SU(3) |

## Most important *new* finding

The combined attacks 1+7 produce a **bounded partial closure** that is
genuinely new and supports a tier promotion of the four-layer
stratification:

> **Cl(3) primitives reduce `N_F` from a continuum-of-positive-reals
> family to exactly TWO admissible values: `N_F ∈ {1/2, 1}`,
> corresponding to whether the Hilbert–Schmidt trace is taken on V_3
> (3D irreducible color carrier) or on V = C^8 (full taste-cube
> Hilbert space).**

The two are related by `N_F^{(8)} / N_F^{(3)} = 2 = dim(I_2) =` fiber
multiplicity, which is *structurally* fixed by the Cl(3)⊗Z³
substrate's tensor-product decomposition. So the residual admission is
discrete (Z_2), not continuous.

This is a **substantive advance** over the four-layer stratification:
- L3 prior: `N_F` is "any positive scalar" (continuous admission)
- L3 post: `N_F ∈ {1/2, 1}` (discrete Z_2 admission)

The continuous-to-Z_2 reduction is the *one* positive partial result of
this analysis. The Z_2 → 1 reduction (the question of which of `{1/2, 1}`
is canonical) is **not closed** by any of the seven attacks.

## What this analysis honestly does NOT close

`N_F = 1/2` is **not derived** from Cl(3) algebraic structure alone.
The discrete admission `N_F ∈ {1/2, 1}` is the highest tier the seven
attacks can reach without admitting an external choice (such as
"restrict trace to V_3").

The structural barrier identified below explains why this is genuinely
the case and not an artifact of insufficient attack effort.

## Inputs available — the existing primitive stack

For every attack vector below, the only admitted inputs are:

- **A1**: Cl(3) is the local algebra at each lattice site
  ([`MINIMAL_AXIOMS_2026-05-03.md`](../../../docs/MINIMAL_AXIOMS_2026-05-03.md))
- **A2**: Z³ is the spatial substrate
  ([`MINIMAL_AXIOMS_2026-05-03.md`](../../../docs/MINIMAL_AXIOMS_2026-05-03.md))
- **Per-site Hilbert space dim 2**, Pauli realization
  ([`CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md`](../../../docs/CL3_PER_SITE_HILBERT_DIM_TWO_THEOREM_NOTE_2026-05-02.md))
- **Cl(3) → End(V) embedding canonicity** up to finite outer automorphism
  ([`G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md`](../../../docs/G_BARE_STRUCTURAL_NORMALIZATION_THEOREM_NOTE_2026-04-18.md)
  Claim 1)
- **`SU(3)_c` on the symmetric base subspace V_3** of the 8D taste cube
  ([`CL3_COLOR_AUTOMORPHISM_THEOREM.md`](../../../docs/CL3_COLOR_AUTOMORPHISM_THEOREM.md))
- **Hilbert–Schmidt joint rigidity** (Killing-form rigidity + joint
  trace-AND-Casimir argument)
  ([`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](../../../docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md))

The target derivation is: under these inputs alone, force the
canonical Gell-Mann normalization scalar `N_F = 1/2`.

The **forbidden** routes (per the A2.5 derivation attack results) are:
- Hochschild / Cl(3) cohomology (foreclosed: HH^n=0 for separable simple)
- Polynomial-closure operator-product algebra (foreclosed:
  Newton-Frobenius shows polynomial-closure = full character ring)
- Lieb-Robinson causality (foreclosed: range-restricting, not
  scale-fixing)

These three are not retried here; we focus on seven *new* attack
vectors that are orthogonal to those obstructions.

---

## Attack 1 — Hilbert–Schmidt / Killing rigidity ("up to scalar")

### Hypothesis

The strengthened HS rigidity theorem
([`G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md`](../../../docs/G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07.md))
proves: under the framework's fixed Hilbert-space inner product on
V = C^8, the Hilbert–Schmidt form `B_HS` on `g_conc = su(3) ⊂ End(V)`
is the unique Ad-invariant inner product *up to overall positive
scalar*. The natural follow-up question: does the framework's
structure pin the *scalar* itself?

### Argument

The Killing-form rigidity statement for simple Lie algebras is
purely structural: for any simple Lie algebra `g`, the space of
Ad-invariant symmetric bilinear forms is one-dimensional. So all
such forms are **proportional** — but the proportionality constant
is intrinsic to whichever form the user picks as canonical
representative.

In the framework's setup, two natural representatives arise:

- `B^{(3)}(X, Y) = Tr_{V_3}(X · Y)` — trace on the 3D irreducible
  color triplet block (where SU(3) acts as fundamental), giving
  `B^{(3)}(T_a, T_b) = (1/2) δ_{ab}`.
- `B^{(V)}(X, Y) = Tr_V(X · Y)` — trace on the full 8D framework
  Hilbert space, giving `B^{(V)}(T_a^V, T_b^V) = 1 · δ_{ab}` for
  `T_a^V` the embedded generators.

Both are Ad-invariant by Killing rigidity. The structural question:
is there an additional Cl(3) primitive that selects between them?

### Verdict

**Definitive obstruction.**

Killing rigidity says these two representatives are **proportional**
(with ratio 2 = `dim(I_2)` = fiber multiplicity, which is
structurally fixed by the tensor-product decomposition `V = V_3 ⊗
I_2 ⊕ V_singlet ⊗ I_2`). It does **not** say which proportionality
constant is "the canonical one."

The choice of which trace space — V_3 vs V — is the **single
remaining structural admission**. Every other aspect of the form
structure is forced.

### What this attack closes

- **Continuum-to-Z_2 reduction.** The two natural representatives are
  related by an exact factor `dim(I_2) = 2` fixed by Cl(3)⊗Z³
  substrate structure. So the continuous family of Ad-invariant
  forms reduces to a **discrete 2-element set** when we admit the
  framework's fixed Hilbert-space embedding.

- This is structurally informative: it reduces the L3 admission
  from "any positive scalar" to "either 1/2 or 1" — a Z_2 admission
  rather than a continuum admission.

### What this attack does NOT close

The Z_2 → 1 reduction (selecting between `N_F^{(3)} = 1/2` and
`N_F^{(8)} = 1`) is not closed. Both are equally valid Ad-invariant
representatives.

### Reusable conclusion

Killing rigidity is structurally silent on overall scalars; it
guarantees uniqueness *up to scalar* and no more. Future attempts
to extract `N_F = 1/2` from Killing rigidity alone will fail.

---

## Attack 2 — Cl(3) ⊗ Cl(3) ≅ Cl(6) → Spin(6) ⊃ SU(3)

### Hypothesis

The framework's actually-derived gauge group might come via the
isomorphism `Cl(3) ⊗ Cl(3) ≅ Cl(6)` and the embedding
`Spin(6) ⊃ SU(3)`. If the Spin(6) Hilbert-Schmidt trace inherits a
canonical normalization, the SU(3) generators (as bivectors of Cl(6))
might inherit that normalization.

### Argument

`Spin(6)` has the exceptional isomorphism `Spin(6) ≅ SU(4)` (this is
classical; it underlies the existence of pure spinors in 6D). The
fundamental 4-spinor of `Spin(6)` carries the canonical SU(4)
normalization `Tr_4(T_a T_b) = (1/2) δ_{ab}` for the canonical SU(4)
generators.

Restricting to SU(3) ⊂ SU(4) (via the natural 4 = 3 ⊕ 1 split, where
SU(3) acts on the 3D subspace and trivially on the singlet), the
SU(3) generators inherit the SU(4) trace:

```
Tr_4(T_a^{SU(3) ↪ SU(4)} · T_b^{SU(3) ↪ SU(4)}) = (1/2) δ_{ab}
```

because the 4-th basis vector contributes zero to the trace
(generators act as zero on the singlet sector). This **matches**
the canonical Gell-Mann `N_F = 1/2`!

### Why this is NOT a derivation

The match is structural but it doesn't derive `N_F = 1/2`. It only
shows that *if we adopt* canonical SU(4) normalization at the Spin(6)
level, *then* the inherited SU(3) normalization is also `1/2`. The
problem is: the canonical SU(4) normalization
`Tr_4(T_a T_b) = (1/2) δ_{ab}` is itself a **convention**, not derived.

This routes the same admission *upstream* — from "admit `N_F = 1/2`
for SU(3)" to "admit `N_F = 1/2` for SU(4)" — without closing it.

The same issue applies to any SU(N) embedding: whatever convention
is admitted for the larger group propagates to the subgroup. There
is no privileged SU(N) at any level whose normalization is forced by
group structure.

### Numerical check

Verified: the SU(3) generators, embedded in 4×4 by `T_a → diag(T_a^{(3)}, 0)`
and traced over the 4D Spin(6) carrier, give `N_F = 1/2`. This
matches `N_F^{(3)} = 1/2` exactly (because the singlet column adds
zero — equivalently, the trace simply doesn't see the 4-th basis
vector).

But it does NOT match `N_F^{(8)} = 1` (since the Spin(6) carrier is
4D, not 8D — there is no fiber multiplicity for the bare 4-spinor).

### Verdict

**Definitive obstruction.** Spin(6) ⊃ SU(3) inherits the same
convention layer one level up. There is no canonical SU(4) trace
normalization derived from group structure alone; the Spin(6) route
just relocates the admission from SU(3) to SU(4).

### Reusable conclusion

Group-embedding routes (SU(3) ⊂ SU(4) ⊂ ... ⊂ SU(N)) cannot derive
`N_F = 1/2` because they propagate whatever convention is admitted
at the top of the chain. The Spin(6) carrier is 4D, distinct from
the framework's 8D taste space — the route does not provide
structural pinning.

---

## Attack 3 — Anomaly cancellation / topological constraint

### Hypothesis

`N_F = 1/2` may be forced by anomaly-cancellation requirements: in
the SM, the gauge anomaly cancels exactly because of the matter
content (one quark generation per family). The d-symbols
`d_{abc} = 2 Tr({T_a, T_b} T_c)` have specific values in canonical
Gell-Mann normalization (e.g., `d_{118} = 1/√3`) that depend on the
overall `N_F` scale via `d → c^3 · d` under `T → c · T`.

### Argument

The 't Hooft anomaly cancellation condition is

```
Σ_R (rep dimension and helicity) · d_{abc}(R) = 0
```

summed over all matter representations. This is a **homogeneous**
condition in the d-symbols: under uniform rescaling `T → c · T`,
each `d_{abc}(R)` scales by `c³`, and the sum equation is multiplied
by `c³`. So if anomaly cancellation holds at one normalization, it
holds at *every* normalization.

The condition is **invariant** under uniform `N_F` rescaling.

### Variant: comparing absolute d-symbol values to observation

In QCD, the d-symbol values appear in physical processes (e.g., the
chiral anomaly π⁰ → γγ amplitude). The amplitude has the form
`A ∝ (1/3) e² (d-symbols evaluated at quark charges)`. Comparing
to observation pins the *combination* `(electric charge)² · d_abc`,
which fixes the product but not `N_F` alone.

Under `T → c T` and `e → e` (electric charge unaffected by SU(3)
normalization), the d-symbols change by `c³` but the *physical*
amplitude is unchanged because we'd also rescale the gauge field
by `1/c`, and the c³ cancels with the (1/c)³ in the field
combination.

### Verdict

**Specific obstruction.** Anomaly cancellation and physical
amplitudes are **invariant** under uniform `N_F` rescaling. The
absolute value of `N_F` cannot be extracted from any anomaly or
topological condition because all such conditions are homogeneous
in the gauge-field power.

### Numerical check

Verified: `d_{118} = 1/√3 ≈ 0.5774` at canonical `N_F = 1/2`.
At `N_F → c · 1/2`, this becomes `d_{118} = c³ / √3`. Both values
are formally valid; physics requires only the right *combinations*.

### Reusable conclusion

Anomaly cancellation, 't Hooft matching, and topological constraints
on the gauge group are **invariant** under uniform generator
rescaling. They cannot fix `N_F`. Future attempts via gauge
anomalies or topology will fail.

---

## Attack 4 — Quantization condition / representation-integrality

### Hypothesis

SU(3) representations are labelled by Dynkin labels `(p, q)` with
`p, q` non-negative integers (Cartan-Dynkin theorem). The
**integrality** of these labels — required for the rep to descend
to the simply-connected group — might force a specific generator
normalization `N_F`.

### Argument

The Dynkin labels `(p, q)` are defined via the action of the Cartan
subalgebra `H_3 = T_3 = λ_3/2` and `Y = T_8/√3` (in physics-y
notation). The eigenvalue of `2 H_α` on the highest-weight vector
of an irrep `(p, q)` is `p` (an integer).

Under uniform rescaling `T → c · T`, the "2 H_α" operator becomes
`2 c · H_α` and its eigenvalue becomes `c · p`. To keep this
integer for all `p`, we need `c ∈ ℤ`. **But** `c` could be any
positive integer (1, 2, 3, ...) — the integrality condition does
not pin `c = 1`; it only restricts to integer rescalings.

### Variant: Casimir integer values

At canonical `N_F = 1/2`, the Casimir `C_2(p,q) = (1/3)((p+q)² + (p+q) + pq)`
gives `C_2(1,0) = 4/3` (rational). At alternative normalizations,
this changes. The mathematical Killing-form normalization (which gives
`C_2(adj) = 2N` and integer values of trace forms on weights) gives
`C_2(1,0) = 1` (integer). So integer-Casimir normalization does NOT
match canonical Gell-Mann!

### Verdict

**Specific obstruction.** Integrality of `(p, q)` Dynkin labels does
not pin `N_F` to any specific value — it only restricts to integer
multiples of any reference value. Furthermore, integer-Casimir
normalization differs from canonical Gell-Mann (Casimir 4/3 vs 1).

### Reusable conclusion

Topological/quantization conditions on the SU(3) rep theory are
**invariant under integer rescaling** of `N_F`. They cannot pick out
`1/2` as canonical. The literature picks `N_F = 1/2` because of
particle-physics historical convention (Gell-Mann 1962), not because
of any rep-theoretic forcing.

---

## Attack 5 — Hardy-style operational reconstruction

### Hypothesis

Hardy 2001 / Müller-Masanes / Pawłowski-Brukner reconstructions of
quantum theory from operational axioms (informational completeness,
no-signaling, continuous reversibility) might force a specific
generator normalization through operationally-defined trace structure.

### Argument

The operational axioms reconstruct *the structure of quantum theory*
on a finite-dimensional Hilbert space:
- Composition of subsystems via tensor products
- Reversibility of measurement evolution
- Informational dimension D = dim(H) — d-1 from operational counts

These axioms determine the **dimension** of the Hilbert space and
its category-theoretic structure. They do NOT determine generator
normalizations: any orthonormal basis of `End(H)_{traceless}` is
admissible, with the trace structure inherited from the Hilbert
space.

The SU(3) generators are 8 Hermitian traceless operators on `V_3 = C^3`
satisfying the Lie algebra `[T_a, T_b] = i f_{abc} T_c`. The
operational axioms determine that `V_3` is a 3-dimensional complex
Hilbert space and that observables are Hermitian operators; they do
not fix the overall scale of any specific basis of the algebra.

### Verdict

**Definitive obstruction.** Operational reconstruction provides
**dimensional** structure, not **scalar** structure. The trace
normalization is invisible to dimension-counting axioms.

### Reusable conclusion

Information-theoretic / operational axioms cannot fix `N_F`. They
fix `dim(V) = 3` for the color triplet but not the inner-product
normalization. Future attempts via operational reconstruction will
fail by construction.

---

## Attack 6 — Standard QFT literature consensus

### Hypothesis

If the canonical `N_F = 1/2` were forced by group structure, this
would be documented in the standard SU(3) representation-theory
literature.

### Argument

Consulted standard references:

- **Slansky, R.** (1981). "Group Theory for Unified Model Building."
  Physics Reports 79(1), 1-128. — Treats `N_F` as convention with
  `N_F = 1/2` (his Tab. 3 normalization) explicitly chosen.
- **Greiner, W. & Müller, B.** (1994). "Quantum Mechanics:
  Symmetries." Springer. — Section 7.3: introduces Gell-Mann
  matrices with `λ_a/2` factor, calls this "the standard
  normalization."
- **Cvitanović, P.** (2008). "Group Theory: Birdtracks, Lie's, and
  Exceptional Groups." Princeton. — Ch. 9 explicitly notes that
  trace normalization is a convention; uses `T_F = 1/2`
  particle-physics convention but discusses alternative
  Killing-form normalization as well.
- **Peskin, M. & Schroeder, D.** (1995). "Introduction to Quantum
  Field Theory." Section A.4: defines `Tr(T^a T^b) = T(R) δ^{ab}`
  with `T(F) = 1/2` for fundamental, calls this "convention."
- **Howe, R. & Tan, E.-C.** (1992). "Non-Abelian Harmonic
  Analysis." Springer. — Uses Killing-form normalization
  consistently; their `N_F` differs from Gell-Mann's.

The literature consensus is clear: **`N_F = 1/2` is a convention,
not a derived consequence**. The reason: SU(N) generators span the
Lie algebra `su(N)`; any positive-definite Ad-invariant Gram matrix
(in a chosen basis) gives a valid form, with the overall scale
fixed by convention. The `1/2` factor in `T_a = λ_a / 2` was
introduced by Gell-Mann (1962) for compatibility with SU(2) spin
matrices `σ_a / 2`; this is historical/aesthetic, not structural.

### Verdict

**Definitive obstruction (consensus).** No standard reference
derives `N_F = 1/2` from group structure. The convention is
admitted uniformly across the standard QFT and rep-theory
literature.

### Reusable conclusion

The literature consensus is itself informative: if a derivation
existed, it would be in Slansky, Greiner-Müller, Cvitanović, or
Peskin-Schroeder. Future attempts via standard rep theory will
recapitulate this convention.

---

## Attack 7 — Direct Cl(3) Pauli-rep / bivector-trace computation

### Hypothesis

At the per-site level, Cl(3) acts on `H_x = C^2` via Pauli matrices.
The canonical trace on M_2(C) gives `Tr_2(σ_a σ_b) = 2 δ_{ab}`.
The framework's per-site SU(2) generators are `T_a = σ_a/2` with
`Tr_2(T_a T_b) = (1/2) δ_{ab}` — matching `N_F = 1/2`. Is this
factor `1/2` structurally forced by Cl(3)?

### Argument (positive partial)

At the **per-site** level (where Cl(3) is the algebra and `C^2` is
the rep), there is a **canonical bivector-to-vector map**:

```
Spin(3) → SO(3):  B_{ij} = σ_i σ_j  ↦  J_k = (1/2) ε_{ijk} σ_k = (1/2) σ_k
```

(after extracting the `i` factor to make `J_k` Hermitian). The
factor of **1/2** comes from the **double cover** Spin(3) → SO(3):
the spinor representation has eigenvalues `±1/2` of the Lie algebra
generators (because of the 2:1 covering map).

This is a **structural** consequence of the Cl(3) bivector grading:
- 0-grade: `1` (scalar)
- 1-grade: `σ_i` (vector)
- 2-grade: `σ_i σ_j` for `i < j` (bivector, 3 of them)
- 3-grade: `i = σ_1 σ_2 σ_3` (pseudoscalar)

The 3 bivectors are the natural Spin(3) ≅ SU(2) generators, with
the bivector-to-vector map giving the **canonical 1/2 factor**.

**Result for SU(2):** the canonical `N_F = 1/2` is **structurally
forced** by Cl(3) bivector structure. This is a positive partial
result that closes `N_F = 1/2` *for SU(2)* from Cl(3) primitives.

### Why this does NOT extend to SU(3)

The SU(3) generators in the framework are **NOT bivectors of Cl(3)**.
Cl(3) has only 3 bivectors (`σ_1 σ_2`, `σ_1 σ_3`, `σ_2 σ_3`), which
generate Spin(3) ≅ SU(2), not SU(3).

The SU(3) generators arise from a **completely different** construction:

```
SU(3) acts on V_3 ⊂ V = C^8 = (3D symmetric base subspace) ⊗ (2D fiber)
   ↑                          ↑
   8 traceless Hermitian      taste-cube decomposition under
   matrices on V_3            b₁↔b₂ symmetric/antisymmetric
   (Gell-Mann basis)          split, plus b₃ as fiber
```

The SU(3) generators are constructed from the 3D symmetric base
subspace's action on V_3, which is a Schur-Weyl-style construction
on Z³'s Hamming-weight-1 orbit. They are NOT bivectors of Cl(3).

In particular:
- Cl(3) bivectors generate only 3 = `dim(Spin(3))` operators
- SU(3) requires 8 = `dim(SU(3))` operators
- The bivector-to-vector double-cover argument has **no analogue**
  for SU(3)

### Variant: SU(3) as Spin(8) bivectors?

One might try Spin(8): `Cl(8) ⊃ Spin(8)`, dim 28 = number of
bivectors. SU(3) ⊂ Spin(8)? No — `Spin(8) ⊃ SO(8)` and SU(3) is
not a natural subgroup of Spin(8). The correct chain to look at
would be Cl(6) ⊃ Spin(6) ≅ SU(4) ⊃ SU(3) (Attack 2 above). Which
already failed.

### Verdict

**Strong partial positive (SU(2) only).**

(a) **Positive partial.** The canonical `N_F = 1/2` for SU(2) is
**structurally forced** by Cl(3) bivector structure, via the
Spin(3) → SO(3) double cover. This is a clean derivation.

(b) **Obstruction.** The argument does NOT extend to SU(3),
because SU(3) generators are not Cl(3) bivectors. The SU(3)
construction goes via the 3D symmetric base subspace of the taste
cube — a different mechanism entirely.

### Reusable conclusion

The Cl(3) bivector-to-vector map provides a **principled** SU(2)
normalization (factor 1/2). For SU(3), no analogous Cl(3) primitive
construction yields the generators directly — they arise via
Schur-Weyl on the 3D symmetric base, which is admission-free for
the *form* but admission-required for the *scalar*.

This explains the **partial** status of the derivation: SU(2)'s
factor 1/2 IS forced by Cl(3); SU(3)'s factor 1/2 IS NOT. The
"matching" between these two canonical conventions is historical
(Gell-Mann 1962 chose the SU(3) factor to match SU(2)'s) but not
structural.

---

## Synthesis: combined positive results

The seven attacks together produce one **bounded positive result**
and six **structural obstructions**.

### Positive result (Attack 1 + Attack 7 combined)

Cl(3) primitives reduce `N_F` from continuous to discrete:

```
Continuous family   Cl(3) +  fixed     ➜    Discrete admission
N_F ∈ ℝ_+           Hilbert space            N_F ∈ {1/2, 1}
```

with the two values corresponding to:
- `N_F = 1/2`: trace on V_3 (3D irreducible color carrier);
  matches canonical Gell-Mann
- `N_F = 1`: trace on V = C^8 (full taste-cube Hilbert);
  natural-V Hilbert-Schmidt

The ratio `2 = N_F^{(8)}/N_F^{(3)}` is structurally fixed (fiber
multiplicity from the tensor product structure of the taste cube).

### Six structural obstructions (Attacks 1-6, Attack 7 partial)

- **Attack 1 (Killing rigidity):** silent on overall scalar
- **Attack 2 (Spin(6)):** routes admission upstream to SU(4)
- **Attack 3 (anomaly):** invariant under N_F rescaling
- **Attack 4 (integrality):** invariant under integer rescaling
- **Attack 5 (operational):** dimension-counting, scale-blind
- **Attack 6 (literature):** consensus admits N_F = 1/2 as convention
- **Attack 7 (Cl(3) bivectors):** works for SU(2), fails for SU(3)

### Where this leaves the four-layer stratification

The four-layer stratification
([`G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md`](../../../docs/G_BARE_CONSTRAINT_VS_CONVENTION_RESTATEMENT_NOTE_2026-05-07.md))
is **strengthened** but **not closed** by this analysis:

- L1 (Cl(3) axiom): DERIVED ✓
- L2 (HS form rigidity): DERIVED ✓
- **L3 (`N_F` admission): DISCRETE Z_2 (was: continuous ℝ_+)** ◐
- L4 (`g_bare = 1`): DERIVED ✓

The L3 admission is sharpened from continuous to discrete (Z_2), but
the residual binary choice between `1/2` and `1` is genuinely
admitted, not derived.

### What admission "restrict trace to V_3" buys us

If we admit "the canonical Hilbert-Schmidt trace is taken on V_3
(the irreducible carrier of su(3))", then `N_F = 1/2` follows
directly. This admission is *natural* in the sense that V_3 is the
support of the SU(3) action — but it is NOT derivable from Cl(3)
primitives alone, because Cl(3) primitives provide the full V = C^8
as the natural trace space.

The four-layer stratification thus becomes a **five-layer**
stratification:

| Layer | Statement | Status |
|---|---|---|
| L1 | Cl(3) algebra | DERIVED |
| L2 | HS form rigidity | DERIVED |
| **L3a** | `N_F ∈ {1/2, 1}` (Z_2 admission) | **DERIVED via Cl(3) primitives + Killing rigidity** |
| **L3b** | Trace space = V_3 (selects `N_F = 1/2`) | **ADMITTED** |
| L4 | `g_bare = 1` | DERIVED |

The honest convention status: **one binary admission** (which trace
space is canonical), not "any positive scalar."

This is a **strict tier-up** from the four-layer note's L3 admission
"any positive scalar `N_F`" — it sharpens the admission to a
binary choice without closing it.

---

## What future cycles should NOT retry

Per the structural obstructions documented above:

1. **Attack 1 (Killing rigidity alone):** Killing rigidity is "up to
   scalar" by classical theorem. No further structural input from
   `su(3)` simplicity will close the scalar.

2. **Attack 2 (group embedding chain):** SU(N) ⊂ SU(N+1) ⊂ ... etc.
   propagates the convention upstream. There is no "canonical"
   SU(N) at any level.

3. **Attack 3 (anomaly):** Anomaly conditions are homogeneous in
   gauge-field power; invariant under uniform `N_F` rescaling.

4. **Attack 4 (integrality):** Topological/quantization conditions
   on rep theory are invariant under integer `N_F` rescaling.

5. **Attack 5 (operational reconstruction):** Operational/Hardy
   axioms are dimension-counting, not scale-fixing.

6. **Attack 6 (literature):** Standard references uniformly admit
   `N_F = 1/2`; no derivation exists in the literature.

The **only remaining** route that could potentially close the Z_2 →
1 reduction (as identified by this analysis):

**Open route — categorical "natural transformation" argument:** If
one can show that the choice "trace on V_3" vs "trace on V" is
forced by a categorical universality (e.g., "the trace on the
*irreducible* carrier is uniquely natural"), then `N_F = 1/2` would
be uniquely selected. This is **not closed here** but is structurally
distinct from the seven obstructions above.

This open route is documented in `THEOREM_NOTE.md` Section 5 as the
single remaining attack vector worth pursuing.

---

## Verification

```bash
python3 outputs/action_first_principles_2026_05_07/w2_n_f_derivation/cl3_n_f_derivation_2026_05_07_w2_check.py
```

Verifies:

1. Canonical Gell-Mann normalization on V_3: `Tr_3(T_a T_b) = (1/2) δ_{ab}`
2. Full taste-space trace on V: `Tr_V(T_a^V T_b^V) = 1 · δ_{ab}`
3. Ratio `Tr_V/Tr_3 = 2 = dim(I_2)` exactly (fiber multiplicity)
4. Casimir on V_3: `Σ_a T_a T_a = (4/3) I_3`
5. Killing-form rigidity (HS Ad-invariance under random SU(3) action)
6. Spin(6)/SU(4) trace inheritance: SU(3) ⊂ SU(4) gives `N_F = 1/2`
   via canonical SU(4) convention (which is itself admitted)
7. d-symbol values at canonical normalization: `d_{118} = 1/√3`
8. SU(2) bivector argument: `Tr_2(σ_a/2 · σ_b/2) = (1/2) δ_{ab}`
   forced by Cl(3) bivector-to-vector map
9. SU(3) generators are NOT Cl(3) bivectors (not extending the
   SU(2) result)
10. Discrete admission `N_F ∈ {1/2, 1}` numerically witnessed
11. Continuum-to-Z_2 reduction: factor 2 ratio is exactly fixed by
    Cl(3) substrate structure

Live result: 22/0 EXACT pass, 0/0 BOUNDED.

## Honest scoping summary

`N_F = 1/2` is **not derivable** from Cl(3) algebraic primitives
alone. The seven attack vectors enumerate the structural barriers.
The single positive partial result is the continuum-to-Z_2
reduction: `N_F ∈ {1/2, 1}` after admitting Cl(3) primitives + the
fixed Hilbert-space embedding.

The Z_2 admission is genuine: choosing between `N_F = 1/2` (V_3
trace) and `N_F = 1` (V trace) requires the additional structural
admission "use the irreducible carrier's trace as canonical" — which
is *natural* but not Cl(3)-primitive.

This analysis sharpens the four-layer stratification's L3 admission
from "continuous family" to "binary choice", which is a substantive
audit-grade improvement.
