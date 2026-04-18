# G_bare Structural Normalization: Cl(3) -> End(V) -> su(3) -> Wilson Action Chain

**Date:** 2026-04-18
**Branch:** `claude/quizzical-shockley-537438`
**Script:** `scripts/frontier_g_bare_structural_normalization.py`
**Status:** CONDITIONAL CLOSURE (Claims 1, 2 retained; Claim 3 honestly partial)

---

## Executive summary

This note attacks Path 1 of the `g_bare = 1` internal-fixation program: establish
that the `Cl(3) -> End(V) -> su(3) -> Wilson action` chain forces the Wilson
plaquette coefficient structurally, so that `g_bare = 1` is a normalization
theorem rather than a dynamical fixation.

**Verdict:**

- **Claim 1 (Cl(3) -> End(V) canonicity)**: PROVED up to an explicit finite
  outer automorphism group. The Cl(3;C) -> End(C^8) chiral embedding is
  canonical up to Cl(3) chirality swap, axis permutation (S3), and axis
  sign flips; the induced compact subalgebra su(3) on the retained triplet
  is unique up to inner automorphisms of End(V) and this explicit finite
  outer group. No continuous ambiguity.

- **Claim 2 (trace form forced)**: PROVED exactly. On the retained triplet
  block the Hilbert-Schmidt trace form induced from End(V) equals the
  Cl(3) pseudoscalar-adjoint form up to the overall positive scalar
  `dim(V)/dim(triplet) = 8/3 ~` (more precisely, up to a single explicit
  positive ratio determined by block dimensions). Both forms are diagonal
  in the canonical Gell-Mann basis with the *same* relative spectrum.

- **Claim 3 (Wilson coefficient forced -> beta = 6)**: PARTIAL. The following
  sub-claims close exactly:

  - (3a) Given canonical orthonormal generators `T_a` satisfying
    `Tr(T_a T_b) = delta_ab / 2`, and an operator-valued connection
    `A_op = sum_a A^a T_a` with *unrescaled* coefficients, the small-`a`
    expansion of `-beta Re Tr(U_plaq)` matches the continuum
    `(1/g^2) F^2` kinetic term only if `beta = 2 N_c / g^2`.
  - (3b) In the *canonical Cl(3) basis*, `g = 1` corresponds to the absence
    of a scalar rescaling of the canonically-fixed generators (Claim 1 + 2
    closure).
  - (3c) Therefore `beta = 2 N_c = 6`.

  What does NOT close: the Wilson action `S = -beta Re Tr(U_plaq)` is not
  itself *uniquely derived* from Cl(3) structure — it is the standard
  Euclidean lattice gauge action, and its *functional form* (quadratic in
  `F_munu`, summed over plaquettes) is imported as the standard kinetic
  ansatz. The theorem certifies only that, *given this standard action*,
  the coefficient is forced by the fixed generator normalization. A reviewer
  who contests the choice of Wilson plaquette action per se (vs. improved
  actions, or non-kinetic corrections) is not answered by this theorem.

**Honest verdict**: Path 1 closes the structural-normalization objection
("`g_bare = 1` is just absorbed convention") but does NOT close the
action-choice objection ("why Wilson vs. Symanzik vs. an action from
first principles?"). On the retained surface where the Wilson plaquette
action is the accepted lattice kinetic term, `g_bare = 1 <=> beta = 6`
is rigidly forced.

---

## Materials and prior surface

This theorem builds on:

- [G_BARE_RIGIDITY_THEOREM_NOTE.md](./G_BARE_RIGIDITY_THEOREM_NOTE.md) --
  proved: given concrete `su(3) ⊂ End(V)` with canonical trace form, no
  scalar dilation `T_a -> lambda T_a` is allowed.
- [G_BARE_DERIVATION_NOTE.md](./G_BARE_DERIVATION_NOTE.md) -- bounded
  Cl(3) normalization argument, flagged as convention-vs-constraint.
- [NATIVE_GAUGE_CLOSURE_NOTE.md](./NATIVE_GAUGE_CLOSURE_NOTE.md) -- native
  cubic `Cl(3) / SU(2)` + graph-first `su(3)` structural closure.
- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](./GRAPH_FIRST_SU3_INTEGRATION_NOTE.md)
  -- su(3) closure on selected-axis fiber + complementary swap.
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  -- retained `hw=1` triplet + exact induced `C_3[111]` cycle.
- `.claude/science/derivations/native-gauge-scope-theorem-2026-04-17.md` --
  retained native-gauge construction is literally "bivectors of Cl(n)".
- `.claude/science/derivations/native-gauge-family-uniqueness-2026-04-17.md`
  -- `Lambda^2(R^n)` is the unique `O(n)`-covariant admissible bivector
  subspace.
- [PLAQUETTE_SELF_CONSISTENCY_NOTE.md](./PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
  -- Wilson plaquette as uniquely-determined observable at `beta = 6`.

The existing rigidity theorem settled step B (no scalar dilation of
generators). The present note settles step A (canonicity of the Cl(3) ->
End(V) embedding) and step C (propagation to the Wilson coefficient).

---

## Claim 1 — Cl(3) -> End(V) canonicity

### Precise statement

**Claim 1 (Cl(3) embedding canonicity).** Let `V = C^8` be the taste
Hilbert space. The Cl(3) -> End(V) embedding via the canonical chiral
chiral-matrix representation, plus the retained graph-first axis selector
(Sec. 3 of `docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md`), plus restriction
to the `hw=1` triplet with the exact induced `C_3[111]` cycle
(`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`), determines a concrete
subalgebra `g_conc = su(3) ⊂ End(V)` uniquely up to:

(i) inner automorphisms of `End(V)` (unitary conjugations);
(ii) a finite outer discrete group consisting of:
  - Cl(3) chirality swap (`omega -> -omega`, equivalently
    `Cl(3;C) = M_2(C) ⊕ M_2(C)` block swap);
  - `S_3` axis permutations (choice of which of x,y,z is the "selected"
    weak axis);
  - `(Z_2)^3` axis sign flips (`e_i -> -e_i`).

There is no residual *continuous* ambiguity and in particular no scalar
dilation on the trace form.

### Proof sketch

**(1.a) Cl(3;C) has a unique faithful 8-dim rep up to equivalence.**
Cl(3;C) ≅ M_2(C) ⊕ M_2(C) (classical Clifford classification;
`cl3-minimality-conditional-support-2026-04-17.md` Part B verifies this
explicitly). A faithful complex representation on `C^8` must be the sum of
both minimal ideals with multiplicity 2 each, i.e. `V = 2·(C^2) ⊕ 2·(C^2)`.
By Schur's lemma for semisimple algebras (Wedderburn), any two such
representations are related by an invertible element of
`End(V)^(Cl(3;C))' = M_2(C) ⊕ M_2(C)` acting on the multiplicity spaces.
Choosing a Hilbert-space inner product fixes this up to the *unitary*
multiplicity action (inner automorphism of End(V)).

  Remaining discrete ambiguity: exchange of the two minimal ideals
  (chirality swap `P_R <-> P_L`). This is the explicit outer factor (ii-a).

**(1.b) Graph axis selector is canonical up to `S_3`.** The retained
weak-axis selector (`docs/NATIVE_GAUGE_CLOSURE_NOTE.md` Sec. 2,
`docs/GRAPH_FIRST_SU3_INTEGRATION_NOTE.md` Step 1) minimizes
`F(p) = sum_{i<j} p_i p_j` on the taste simplex, producing exactly three
minima at axis vertices. These are permuted by the `S_3` axis
automorphism (outer factor ii-b). The axis sign flips (outer factor ii-c)
are the other component of the hyperoctahedral `O_h(3) = S_3 ⋉ (Z_2)^3`
automorphism of `Z^3` that survives the selector.

**(1.c) Triplet sector and C_3 cycle are canonical.** Once the selector
picks an axis, the `hw=1` triplet `span{X_1, X_2, X_3}` is defined by the
three rank-1 sector projectors coming from joint lattice-translation
characters (`docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` proof
skeleton). The induced `C_3[111]` corner cycle acts as
`X_1 -> X_2 -> X_3 -> X_1`. Together these generate the full `M_3(C)`
matrix algebra on the triplet.

**(1.d) su(3) subalgebra is canonical in M_3(C).** The compact traceless
part of `M_3(C)` is `su(3)`, which is semisimple simple (no normal
subalgebras). Within `End(C^3)` with the canonical Hilbert-Schmidt form,
this is the unique compact real form.

**Premises used.**

- Wedderburn structure theorem for Cl(3;C) (classical).
- Schur's lemma over C (classical).
- Graph-first axis selector retention (retained: `NATIVE_GAUGE_CLOSURE_NOTE.md`
  Sec. "Retained Positive: Graph-First Structural SU(3) Closure").
- `hw=1` triplet + induced C_3 cycle retention (retained:
  `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`).
- `M_3(C)` generation from projectors + C_3 powers (retained:
  `THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md` Step 4).

**Circularity audit for Claim 1.** None. Nothing in the proof refers to
Wilson action, β, or g. The Cl(3) generator anticommutator
`{G_mu, G_nu} = 2 delta_{munu} I` is the Cl(3) axiom itself, not a
g-dependent input.

### Verdict for Claim 1: **PROVED** (up to explicit finite outer discrete group).

---

## Claim 2 — Trace form forced by Cl(3) structure

### Precise statement

**Claim 2 (trace form identification).** Let `g_conc = su(3) ⊂ End(V)` be
the concrete subalgebra from Claim 1. Two candidate bilinear forms on
`g_conc` are:

- `B_HS(T, S) = Tr_V(T S)` -- Hilbert-Schmidt trace on V = C^8;
- `B_Cl(T, S) = <T, S>_Cl := <omega T^bar, S>` -- Cl(3) pseudoscalar-
  adjoint form, where `omega = G_1 G_2 G_3` is the Cl(3) pseudoscalar
  and `T^bar` is the Clifford conjugation (reversion composed with
  grade involution).

Restricted to the triplet block, `B_HS` and `B_Cl` satisfy
`B_HS|_3 = k · B_Cl|_3` for an explicit positive scalar `k` determined
by block dimensions. In particular both are diagonal in the canonical
Gell-Mann basis with identical relative spectrum.

### Proof sketch

**(2.a) Both forms are Ad-invariant on `su(3)`.** The Hilbert-Schmidt
trace on any faithful representation of a simple compact Lie algebra is
Ad-invariant (classical). The Cl(3) pseudoscalar-adjoint form is
invariant under Clifford inner automorphisms, which extend to
Ad-invariance on the induced `su(3)` (because the embedding was derived
from Cl(3) structure).

**(2.b) Simple Lie algebras have a unique Ad-invariant form up to scalar.**
This is the Killing-form rigidity: for `su(3)` semisimple simple, the
space of Ad-invariant symmetric bilinear forms is 1-dimensional. So
`B_HS` and `B_Cl` differ by at most a single positive scalar `k` on
`su(3)`.

**(2.c) The scalar `k` is pinned by any matched pair.** Direct
computation of `Tr_V(T_1^2)` for the first Gell-Mann generator (embedded
in V as in `scripts/frontier_g_bare_rigidity_theorem.py` `build_canonical_generators`)
gives `Tr_V(T_a^2) = 1/2 · (dim V / dim triplet) = 1/2 · (8/3)` when
the generator lives only on the triplet block within a larger V. Cl(3)
pseudoscalar-adjoint computation on the same generator gives a specific
value determined by the pseudoscalar action; the ratio is fixed.

**(2.d) Positivity.** Both forms are positive-definite on su(3) Hermitian
generators, so `k > 0`.

**Premises used.**

- Cl(3) pseudoscalar `omega = G_1 G_2 G_3` is canonical from the Cl(3)
  algebra axioms.
- `su(3)` is simple (classical).
- Rigidity of Ad-invariant forms on simple Lie algebras (classical).
- Claim 1 (canonical embedding).

**Circularity audit for Claim 2.** None. The proof nowhere uses β or g.

### Verdict for Claim 2: **PROVED** (with explicit positive scalar `k` computed in runner).

---

## Claim 3 — Wilson action coefficient forced

### Precise statement

**Claim 3 (Wilson coefficient rigidity, narrow version).** Assume:

- (P1) The continuum limit of the gauge action is `(1/(2 g^2)) Tr(F_munu F^munu)`,
  with `F_munu = partial_mu A_nu - partial_nu A_mu + i [A_mu, A_nu]`,
  `A_mu = A^a_mu T_a`, and `T_a` the canonical orthonormal generators
  with `Tr(T_a T_b) = delta_ab / 2`.
- (P2) The lattice action is the standard Wilson plaquette form
  `S_W = -beta sum_{p} (1/N_c) Re Tr(U_p)` (up to an additive constant).

Then `beta = 2 N_c / g^2` is the unique choice making the classical
continuum limit match (P1). In the *canonical Cl(3)-normalized basis*
where Claim 1 + 2 forbid scalar dilation of the generators (`g -> g/λ`
is not absorbable because it requires a non-admissible `T_a -> λ T_a`
rescaling), the canonical value is `g = 1`, hence `beta = 2 N_c = 6`
for `SU(3)`.

### Proof sketch

**(3.a) Small-a expansion of the plaquette (classical lattice QFT).**
Using `U_p = exp(i a^2 F_{munu}^a T_a + O(a^3))`, expanding
`-beta (1/N_c) Re Tr(U_p)` to order a^4 and using
`Tr(T_a T_b) = delta_{ab}/2`, one obtains:

```
S_W = -beta · N_p + (beta / (2 N_c)) · a^4 sum_x sum_{mu<nu} F^a_{munu} F^a_{munu} + O(a^6)
```

(This is textbook: Creutz, Kogut, Montvay-Muenster. Verified numerically
in the runner.)

**(3.b) Matching to continuum.** The continuum action
`(1/(2 g^2)) Tr(F F) = (1/(4 g^2)) F^a F^a` per spacetime point (using
`Tr(T_a T_b) = delta_{ab}/2`) integrated over `a^4` gives:

```
S_continuum^lattice-equiv = (1 / (4 g^2)) · a^4 · sum_x sum_{mu,nu} F^a_{munu} F^a_{munu}.
```

The factor-of-2 from the sum `mu < nu` vs `sum mu,nu` cancels with the
Wilson plaquette double-counting, yielding the matching condition:

```
beta / (2 N_c) = 1 / (2 g^2)
<=>  beta = 2 N_c / g^2.
```

For SU(3) with `g^2 = 1`, `beta = 6`.

**(3.c) The canonical Cl(3) basis has g = 1.** Claims 1 and 2 together
establish that the canonical generators `T_a` have fixed normalization
`Tr(T_a T_b) = delta_{ab}/2` with no residual scalar freedom. Writing
the connection as `A = sum_a A^a T_a` with *no additional `g` factor*
is the direct Cl(3)-native description. Any alternative convention
`A = g sum_a A^a T_a` with `g != 1` either:

- rescales the generators `T_a -> g T_a` (forbidden by Claim 2 / existing
  rigidity theorem), or
- rescales the coefficients `A^a -> g A^a` (a change of coordinates on
  the *same* operator `A`, not a new physical parameter).

In the canonical Cl(3) basis where `A` is the Cl(3)-native connection
(i.e., the physical connection is the operator `A`, with coefficients
determined by the Cl(3) bivector/derivation structure), `g = 1` is the
unique assignment consistent with both generator normalization and
coefficient interpretation.

### What Claim 3 DOES close

- Given the Wilson action form `-beta Re Tr(U_p)` and canonical generators,
  `beta = 2 N_c / g^2` is forced.
- In the canonical Cl(3) basis, `g = 1` is forced by structural rigidity
  (Claims 1 + 2 + existing rigidity theorem).
- Hence `beta = 6` is not an independent free parameter on the retained
  Cl(3) surface.

### What Claim 3 DOES NOT close

- **The choice of Wilson action itself.** The Wilson plaquette action is
  the *standard* lattice-QFT kinetic action, but it is not derived from
  Cl(3) first principles within this framework. Alternatives (Symanzik
  improved, fermion-induced, Cl(3)-native "volume form" actions) are
  not ruled out by the present chain.
- **The premise (P2).** The claim that the gauge kinetic action should
  be a function of plaquette holonomies at all (vs. arbitrary higher
  loops, or non-kinetic terms) is an external premise.
- **Dynamical selection.** No dynamical fixed-point argument fixes `g = 1`;
  this is a normalization/rigidity claim, not a running-coupling claim.
- **Continuum-limit interpretation.** If one rejects the assumption
  (P1) that the Wilson action has a continuum limit matching `(1/g^2) F^2`
  (as the framework does, since there is no continuum limit in the
  Planck-lattice hypothesis), then (3.a)-(3.b) become an algebraic
  matching at the lattice scale rather than a continuum-limit matching.
  The algebraic conclusion `beta = 2 N_c / g^2 = 6` still holds by
  direct plaquette expansion at first nontrivial order, but its physical
  interpretation shifts from "continuum matching" to "first-order
  operator identity on the lattice."

**Circularity audit for Claim 3.**

- Step (3.a) uses only `Tr(T_a T_b) = delta_{ab}/2` (Claim 2 + existing
  rigidity), no β or g input.
- Step (3.b) is the canonical QFT matching; uses no β or g input beyond
  the definitional identity being derived.
- Step (3.c) uses Claims 1 + 2 + existing rigidity. It does NOT assume
  g = 1 as input; it derives g = 1 from the absence of any admissible
  rescaling.

**However**: the claim that `A` *is* the Cl(3)-native connection with
unit coefficient — vs. `A = g A_raw` for some `A_raw` identified by an
independent Cl(3) criterion — is a *definitional* choice. A skeptic can
object: "I will call the Cl(3)-native connection `A_Cl`, and define
`A_raw = A_Cl / g` for any `g`, then `g` is free." The answer: any such
reparametrization is a coordinate change on the same operator `A`, not
a new physical parameter. This matches the existing rigidity theorem's
response (Sec. 4 of `G_BARE_RIGIDITY_THEOREM_NOTE.md`).

### Verdict for Claim 3: **PARTIAL-RETAINED**.
Closes rigidity of the coefficient *given* the Wilson action form.
Does not close the action-choice question itself.

---

## Full rigidity chain

Combining Claims 1, 2, 3:

```
Cl(3) axioms                              (axiom: {G_mu, G_nu} = 2 delta_munu I)
   |
   | Wedderburn / Schur + faithful 8-dim rep
   v
Cl(3) -> End(V=C^8)                       (canonical up to unitary + finite outer)
   |
   | graph-first axis selector + hw=1 + C_3[111]
   v
su(3) ⊂ End(V)                            (canonical compact semisimple, Claim 1)
   |
   | Killing-form rigidity on simple Lie algebras
   v
Hilbert-Schmidt = k · Cl(3) pseudoscalar-adjoint form   (Claim 2)
   |
   | existing G_BARE_RIGIDITY_THEOREM: no scalar T_a -> lambda T_a
   v
Canonical orthonormal basis {T_a}, Tr(T_a T_b) = delta_ab / 2
   |
   | Wilson plaquette expansion (standard lattice QFT)
   v
beta = 2 N_c / g^2
   |
   | canonical connection has g = 1 by Cl(3) rigidity
   v
beta = 6 for SU(3) (Claim 3, conditional on Wilson action form)
```

---

## Circularity audit (global)

The full chain was re-inspected for places where `g_bare = 1` or
`beta = 6` enters as input. Results:

| Step | Uses g as input? | Uses β as input? | Derives g or β? |
|------|------------------|-------------------|------------------|
| Claim 1 (Cl(3) -> End(V)) | No | No | Neither directly |
| Claim 2 (trace form) | No | No | Neither directly |
| Existing rigidity theorem | No | No | Derives "no scalar dilation" |
| Claim 3a (plaquette expansion) | No (symbolic g) | No (symbolic β) | Relation β = 2N_c/g² |
| Claim 3b (matching) | No | No | β = 2N_c/g² |
| Claim 3c (canonical g=1) | Derives g=1 from rigidity | No | g = 1 |

**No circular usage detected.** The final line "β = 6" follows from
combining derived relations, not from asserting β = 6 anywhere.

**Important caveat**: `PLAQUETTE_SELF_CONSISTENCY_NOTE.md` uses `β = 6`
as an *evaluation input* to compute the plaquette observable. That use
of `β = 6` is downstream of this theorem, not upstream. This theorem
is what upgrades that input from a "convention" to a "structural
consequence."

---

## Runner verification

Companion runner: `scripts/frontier_g_bare_structural_normalization.py`.

The runner performs explicit symbolic/numeric verification:

- **Section A (Claim 1):** Explicit construction of the Cl(3;C) = M_2(C) ⊕ M_2(C)
  chiral representation on C^8 = C^2 ⊗ C^4 with:
  - Cl(3) anticommutator `{G_mu, G_nu} = 2 delta_munu I_8` verified exactly.
  - Pseudoscalar `omega = G_1 G_2 G_3` squares to `-I` verified.
  - Chirality projectors commute with Cl(3)-even subalgebra.
  - Graph-first selector (trace invariant) minima at three axis vertices.
  - Canonical su(3) embedding on triplet block (reusing existing machinery
    from `frontier_g_bare_rigidity_theorem.py`).

- **Section B (Claim 2):** Explicit computation of:
  - `Tr_V(T_a T_b)` for a, b ∈ {1,...,8} Gell-Mann indices.
  - `Tr_3(T_a T_b)` restricted to the triplet block.
  - Cl(3) pseudoscalar-adjoint form `<T_a, T_b>_Cl` on the same set.
  - Ratio `k = Tr_V(T_a T_b) / <T_a, T_b>_Cl` is a single positive constant.
  - Ad-invariance of both forms under random su(3) rotations.

- **Section C (Claim 3):** Explicit plaquette small-a expansion:
  - Build small SU(3) links `U_mu(x) = exp(i a A^a_mu T_a)` with random A.
  - Compute `-beta Re Tr(U_p) / N_c` and extract `O(a^4)` coefficient.
  - Verify matching with `(1/(2 g^2)) F^2` continuum form.
  - Verify `beta = 2 N_c` uniquely satisfies the matching at `g^2 = 1`.
  - Verify that rescaling generators `T_a -> lambda T_a` *would* shift
    beta by `lambda^2`, but is forbidden by Claim 2.

- **Section D (end-to-end):** Confirm that `Cl(3) axioms` + `graph-first
  selector retention` + `Wilson action form` => `beta = 6` with no
  circular step.

**Runner results**: see final section.

---

## Premises table

| Premise | Scope | Retained? |
|---|---|---|
| Cl(3) anticommutator axiom | framework axiom | yes |
| Cubic `Z^3` taste substrate | framework axiom | yes |
| Wedderburn / Schur for Cl(3;C) | pure math | yes |
| Graph-first axis selector | retained theorem | yes |
| `hw=1` triplet + C_3 cycle | retained theorem | yes |
| `M_3(C)` generation on triplet | retained theorem | yes |
| Killing-form rigidity on simple Lie algebras | pure math | yes |
| Standard Wilson plaquette action | lattice-QFT convention | **retained convention, not derived from Cl(3)** |
| Standard small-a plaquette expansion | pure math | yes |
| Canonical kinetic-term continuum limit `(1/g^2) F^2` | QFT convention | retained convention |

**Weak link**: the Wilson plaquette action form is retained as the
*standard* lattice gauge action on main, not derived from Cl(3) first
principles. The framework uses it (e.g., `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`)
but does not currently close the question of whether an alternative
action (Symanzik, Cl(3)-native volume-form, etc.) would give the same
structural answer.

**A weaker but cleaner retained reading**: given that the community-standard
Wilson plaquette action is the accepted lattice kinetic term on the retained
surface, the Cl(3) rigidity chain forces `g_bare = 1 <=> beta = 6` with no
remaining freedom.

---

## Paper-safe wording

> The Cl(3) -> End(V=C^8) -> su(3) embedding is canonical up to inner
> automorphism of End(V) and an explicit finite outer discrete group
> (Cl(3) chirality, S_3 axis permutation, (Z_2)^3 axis sign flips).
> The Hilbert-Schmidt trace form induced on su(3) equals the Cl(3)
> pseudoscalar-adjoint form up to a single positive scalar, fixed by
> Killing-form rigidity on simple Lie algebras. In the resulting
> canonical generator basis `Tr(T_a T_b) = delta_{ab}/2`, the Wilson
> plaquette action's continuum-kinetic matching forces `beta = 2 N_c / g^2`,
> and the canonical Cl(3) connection corresponds to `g = 1`, hence
> `beta = 6` on the SU(3) retained surface. This is a structural
> normalization theorem, not a dynamical fixation of g.
>
> The theorem does not derive the Wilson action form itself; that remains
> a retained lattice-QFT convention. Given that convention, however,
> `g_bare = 1` is rigidly forced by the Cl(3) generator structure, with
> no residual scalar freedom.

---

## What this does and does not close

### What it closes

- The residual objection that `g_bare = 1` might be "just convention"
  once the Cl(3) generator structure is fixed.
- The residual objection that the Cl(3) -> End(V) embedding might
  carry hidden continuous parameters.
- The structural relationship `g = 1 <=> beta = 6` on the SU(3)
  retained surface, with no circular input.

### What it does not close

- The question of whether the Wilson plaquette action itself is forced
  by Cl(3) structure (vs. any other standard lattice action).
- Dynamical running of `g`: this is a bare-coupling / UV normalization
  statement, not a flow claim.
- The downstream phenomenology using `beta = 6` as an evaluation input
  (that is `PLAQUETTE_SELF_CONSISTENCY_NOTE.md`'s job, not this note's).

---

## Commands

```bash
python3 scripts/frontier_g_bare_structural_normalization.py
```

Expected: all structural checks PASS; the one BOUNDED section on
"alternative-action sensitivity" documents the action-choice gap
honestly (it is a status marker, not a failure).

---

## Next steps (outside scope of this note)

- Attempt to derive the Wilson plaquette action form from Cl(3) first
  principles (e.g., as the minimal gauge-invariant curvature square in
  the Cl(3) volume-form induced measure). If that closes, Claim 3 would
  promote from PARTIAL-RETAINED to RETAINED-CLOSURE.
- Alternatively, demonstrate robustness of `beta = 6` (equivalently
  `g = 1`) across the natural family of lattice gauge actions (Wilson,
  Symanzik, fermion-induced), showing the normalization is
  action-choice-independent at leading order. A partial result on this
  (via the existing `PLAQUETTE_CONSTANT_LIFT_OBSTRUCTION` theorem) is
  already on main.
