# Connes-Kreimer Partial-Sum Rota-Baxter on `B_4` — External Bounded Note

**Date:** 2026-05-10
**Type:** bounded_theorem
**Claim scope:** External mathematical theorem on the
Connes-Kreimer Hopf algebra of rooted trees `H_R` evaluated on a
complete-binary-tree generator `B_4` (16 leaves), with target a commutative
unital algebra `A_seq` of finite sequences under componentwise
multiplication and Rota-Baxter operator `P_strict` the strict
prefix-sum (weight `+1`). The algebraic Birkhoff factorization of a
character `phi: H_R -> A_seq` of weight `+1` (per
[`CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md))
exists. **No framework-native bridge from the regular part `phi_+`
evaluated on `B_4` to the framework's `alpha_LM^16` factor is closed
under this construction**: any character matching `B_4` to powers of
`alpha_LM` is an external structural choice (an import), and the
resulting `phi_+` readout is either tautological (e.g. zero Rota-Baxter
operator) or projector-dependent (non-idempotent Rota-Baxter
non-uniqueness, per Manchon arXiv:math/0408405).

**Status authority:** independent audit lane only. This source note
does not set or predict an audit outcome; later status is generated
by the audit pipeline after independent review.

**Source-note proposal disclaimer:** this note is a source-note proposal;
audit verdict and downstream status are set only by the independent
audit lane.

**Primary runner:** [`scripts/frontier_connes_kreimer_partial_sum_rb_b4_external_bounded.py`](../scripts/frontier_connes_kreimer_partial_sum_rb_b4_external_bounded.py)

---

## 1. Setup

### 1.1 The Hopf algebra `H_R` and the complete-binary-tree generator `B_4`

Let `H_R` be the Connes-Kreimer Hopf algebra of rooted trees, with
counit `epsilon`, coproduct `Delta`, antipode `S`, and convolution
product `*` on `Hom(H_R, A)` for any commutative unital algebra `A`,
as recorded in
[`CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md).

Let `B_4 in H_R` be a **complete binary rooted tree of depth 4**: one
root, two children of the root, four grandchildren, eight
great-grandchildren, sixteen leaves at depth 4. `B_4` has 31 nodes and
30 internal edges. The coproduct of `B_4` enumerates its admissible
cuts; the number of admissible cuts of a complete binary tree of
depth `d` is `2^(2^d - 1) - 1` for full cuts (excluding the empty and
full cuts), and many more counting the full poset of cut-sets. The
runner verifies the depth-1, depth-2, and depth-3 coproducts
explicitly to control the combinatorics.

### 1.2 Target algebra `A_seq` and Rota-Baxter operator `P_strict`

Let `A_seq = C^N` for some fixed `N >= 16`, with componentwise
multiplication

```text
(a * b)_n  =  a_n  *  b_n,                                            (1)
```

and identity `(1, 1, ..., 1)`. Define the **strict prefix-sum operator**

```text
P_strict(a)_n  =  a_1 + a_2 + ... + a_{n-1},     P_strict(a)_1 = 0.   (2)
```

`P_strict` is a Rota-Baxter operator of weight `+1` on `A_seq`:

```text
P_strict(a) * P_strict(b)  =  P_strict( P_strict(a) * b
                                       + a * P_strict(b)
                                       + 1 * a * b ).                 (3)
```

This is the standard textbook Rota-Baxter operator on a sequence
algebra. It is **not idempotent**: `P_strict(P_strict(a)) != P_strict(a)`
in general.

### 1.3 Algebraic Birkhoff factorization recursion

Given a character `phi: H_R -> A_seq`, the Connes-Kreimer-Manchon-
Ebrahimi-Fard recursion (per the cited external narrow retained
theorem) constructs `phi_-, phi_+` via

```text
prepared_phi(t)  =  phi(t)  +  sum_c  phi_-(P^c(t)) * phi(R^c(t)),    (4)
phi_-(t)         =  -P_strict( prepared_phi(t) ),                     (5)
phi_+(t)         =  ( id - P_strict )( prepared_phi(t) ),             (6)
```

where `c` runs over admissible cuts of `t`, `P^c(t)` is the pruned
forest, and `R^c(t)` is the rooted remainder.

When the Rota-Baxter operator is a **projector** (idempotent splitting
`A = A_- + A_+`), Birkhoff is unique (Manchon arXiv:math/0408405, end
of §II.5). When the Rota-Baxter operator is **not** a projector (as
for `P_strict` here), the Manchon Remark following Theorem II.5.1
records:

> "Rota-Baxter identity for R just guarantees that equation (**)
> gives a Birkhoff decomposition. When R is idempotent ... this
> decomposition is unique."

So `phi_-, phi_+` exist under (4)-(6) but are not the unique
splitting of `phi` into a `-` part and `+` part. They are the
specific recursion-produced output of (4)-(6).

---

## 2. Theorem (external)

**Theorem (Birkhoff recursion well-definedness).** Let `phi: H_R ->
A_seq` be any character of weight `+1`. Then the recursion (4)-(6),
with `P_strict` as in (2), defines maps `phi_-, phi_+: H_R -> A_seq`
satisfying

```text
phi  =  phi_-^{*-1}  *  phi_+,                                        (7)
```

with `phi_-(1) = phi_+(1) = 1 = (1, 1, ..., 1)`. The recursion is
deterministic on each tree depth.

**Proof sketch.** Existence: (4)-(6) is the Manchon-EFP-form Birkhoff
recursion, well-defined because `P_strict` is a Rota-Baxter operator
of weight `+1` on `A_seq` (verified by sympy in the runner).
Multiplicativity of `phi_-, phi_+` follows from the Rota-Baxter
identity and the Hopf-algebra structure (Manchon arXiv:math/0408405,
§II.5; Ebrahimi-Fard-Guo-Kreimer arXiv:hep-th/0407082). Uniqueness
fails in general because `P_strict` is not idempotent.  *Q.E.D.* (as
external theorem; the runner verifies the recursion on `B_1, B_2,
B_3`).

### 2.1 What this theorem does not prove

This external theorem proves the algebraic Birkhoff factorization is
well-defined on `B_4` with target `A_seq` and Rota-Baxter `P_strict`.
It does **not** prove:

- that any framework operator on the canonical staggered Wilson surface
  is a character on `H_R` valued in `A_seq`;
- that any framework rung-indexed sequence `(c_1, c_2, ..., c_16)`
  arises from a character on `H_R` evaluated on `B_4`;
- that the Birkhoff regular part `phi_+(B_4)` is interpretable as
  `alpha_LM^16` in any natural way;
- that the choice of `P_strict` (vs other Rota-Baxter operators on
  `A_seq`) is forced by the framework or by the staircase blocking
  step;
- that the `B_4` tree (rather than the Boolean lattice `2^[4]` or any
  other 16-element combinatorial structure) is forced by the
  framework's 16 = `2^4` BZ-corner derivation.

---

## 3. Why the four scaffolds do not close a framework-native bridge

This section is the bounded admissions block. It documents the four
specific obstructions to running the abstract Birkhoff theorem of §2
as a framework-native derivation of `alpha_LM^16`.

### 3.1 Admission A1 — Markopoulou (hep-th/0006199) Hopf algebra is on partitioned lattices, not on `H_R`

F. Markopoulou, *An algebraic approach to coarse graining*,
arXiv:hep-th/0006199 (2000), introduces a Hopf algebra on **partitioned
labeled lattices** with Boltzmann weights. The coproduct enumerates
sublattice / remainder pairs (Markopoulou eq. 8), and a "shrinking
antipode" `S_R` (Markopoulou eq. 42) implements the block-spin step
in place of the standard antipode `S` (Markopoulou eq. 15). Worked
examples: 2D `Z2` lattice gauge on irregular lattices, the 1D Ising
chain, and 1+1 spin foams.

This is the only published lattice / spin-system application of
Kreimer Hopf-algebraic renormalization the author has located in the
referenced literature search. It does not equip the framework's
canonical 4D `Z^3+t` staggered Wilson surface with a CK character on
`H_R`. Specifically:

1. Markopoulou's Hopf algebra is on **partitioned lattices**, not on
   `H_R` directly. The two are different Hopf algebras; one Hopf
   algebra is generated by partitioned lattices with the coproduct
   over sub-partition pairs, the other by rooted trees with the
   coproduct over admissible cuts.
2. Markopoulou's renormalization map `R` (eq. 39, eq. 46) is
   multiplicative on disjoint sublattices (eq. 41) but is **not
   claimed to satisfy the Rota-Baxter identity** in
   arXiv:hep-th/0006199. The shrinking antipode `S_R` is a modified
   antipode, not the Bogoliubov-Birkhoff `phi_-`.
3. Markopoulou's worked examples (2D `Z_2`, 1D Ising, 1+1 spin foam)
   do not include 4D staggered Wilson lattice gauge theory on
   `Z^3+t` APBC at `L = 2`.

**A1 admission.** Markopoulou's construction is an algebraic
analog motivating Hopf-style book-keeping of inhomogeneous block-spin
renormalization. It is not an existing instantiation of CK on `H_R`
applied to the framework's specific 4D staggered Wilson surface, nor
does it equip the surface with a Rota-Baxter projector. The published
work in [13] (Markopoulou) closes neither of these. Any framework-side
attempt to lift Markopoulou to `H_R` is itself a new construction
under the framework's no-new-axiom discipline.

### 3.2 Admission A2 — `B_4` complete binary tree vs Boolean lattice `2^[4]` (BZ corners)

The framework's BZ-corner derivation
(`WILSON_BZ_CORNER_HAMMING_STAIRCASE_CLOSED_FORM_NOTE_2026-05-09.md`,
plain-text context pointer, T1' therein) gives the 16 BZ corners
of `Z^3+t` APBC at `L = 2` as the elements of `{0,1}^4`, with
Hamming-weight classes of multiplicity `binomial(4, k)`, i.e. the
count tuple `(1, 4, 6, 4, 1)`. This is the structure of the
**Boolean lattice `2^[4]`**: the partial order of subsets of a
4-element set, with the `S_4` axis permutation as symmetry group
(per `WILSON_BZ_CORNER_HAMMING_STAIRCASE_CLOSED_FORM_NOTE_2026-05-09`
T2).

A **complete binary tree `B_4` of depth 4** has 16 leaves but is a
*different* combinatorial object: it imposes a strict left/right
ordering at each internal node and is acted on by an automorphism
group that breaks `S_4`. The cardinality match (both have 16
terminal vertices) is coincidental; the structural match is
explicitly broken at the level of automorphism group and admissible-
cut combinatorics.

**A2 admission.** The framework's "16 = `2^4`" derivation supports a
Boolean-lattice structure, not a complete binary tree. Any choice of
`B_4` is an external decoration. The Connes-Kreimer Hopf algebra
`H_R` is defined on rooted trees, not Boolean lattices, so the
"natural" framework-side substrate (the Boolean lattice `2^[4]`)
does not embed into `H_R` as a single CK generator. `B_4` is one
embedding choice; many other 16-leaf trees are equally consistent
with the cardinality but inequivalent structurally.

### 3.3 Admission A3 — Borinsky-Dunne trans-series does not define a CK character into a trans-series target with a Rota-Baxter operator

M. Borinsky and G. V. Dunne, *Non-perturbative completion of
Hopf-algebraic Dyson-Schwinger equations*, Nucl. Phys. B **957**,
115096 (2020), arXiv:2005.04265, applies resurgent asymptotic analysis
to extract trans-series solutions of the Hopf-algebraic
Dyson-Schwinger equation for the 4D Yukawa model. The Hopf algebra
structure organizes the **perturbative** input (the iterative
DSE expansion), and the trans-series is the **output** of the
resurgent completion of that perturbative series.

Borinsky-Dunne does not:

1. define an explicit Connes-Kreimer character `phi: H_R ->
   A_trans-series` whose target is a trans-series algebra equipped
   with a Rota-Baxter operator;
2. perform a Birkhoff factorization on the trans-series algebra;
3. identify the non-perturbative sectors `exp(-S_k / x)` as the
   image of a CK character.

The Hopf-algebraic structure persists in the sense that the
perturbative coefficients still have the iterative DSE form. It
does **not** equip the non-perturbative trans-series with a CK
character / target / Rota-Baxter triple.

**A3 admission.** The published Borinsky-Dunne construction does
not provide a CK character into a Rota-Baxter-equipped trans-series
algebra. Any framework-side attempt to define one is a new
construction, not an instantiation of the cited reference.

### 3.4 Admission A4 — Partial-sum `P_strict` is a Rota-Baxter operator, but its identification with the staircase RG is an import, and `phi_+(B_4)` is tautological under the simplest framework-natural character

`P_strict` of weight `+1` (eq. 2) is a Rota-Baxter operator on
`A_seq` (eq. 3, verified by sympy in the runner). Many natural
characters can be defined on `B_4` valued in `A_seq`. The simplest
framework-natural choice (the one suggested by the prompt scaffold)
assigns to each leaf of `B_4` the constant sequence
`(alpha_LM, alpha_LM, ..., alpha_LM)`, and extends multiplicatively
over the coproduct.

Under this character `phi_FW: H_R -> A_seq`:

```text
phi_FW(leaf)       =  (alpha_LM, alpha_LM, ..., alpha_LM),            (8)
phi_FW(B_4)        =  (alpha_LM^16, alpha_LM^16, ..., alpha_LM^16),   (9)
```

componentwise. The Birkhoff regular part `phi_+(B_4)` depends on
the recursion (4)-(6); for the leading constant-sequence value, an
explicit computation in the runner shows that `phi_+(B_4)_1 =
alpha_LM^16` is **the input character's value at the constant slot
`n = 1`** (since `P_strict(a)_1 = 0` by definition). The Birkhoff
machinery contributes nothing beyond identity in the `n = 1` slot.

For `n >= 2` slots, `phi_+(B_4)_n` is a non-trivial polynomial in
`alpha_LM` that depends on the full prefix-sum machinery, not on
`alpha_LM^16` alone.

**A4 admission (tautological readout).** The "`alpha_LM^16` is the
leading coefficient of `phi_+` at depth 4" claim **does** hold in
slot `n = 1` of `A_seq`, but only because `P_strict(a)_1 = 0`
trivially. The Birkhoff factorization contributes no derivation in
this slot. In other slots, `phi_+(B_4)_n` is a polynomial mixture
not equal to `alpha_LM^16`. This is the same tautological-readout
obstruction recorded as **O4** in
`CONNES_KREIMER_BRIDGE_16FOLD_BLOCKING_NO_GO_THEOREM_NOTE_2026-05-10.md`
(plain-text context pointer; the unaudited no-go from the prior round),
now lifted to the `B_4`
substrate and the `P_strict` Rota-Baxter.

---

## 4. What this bounded note claims, and what it does not

### 4.1 What is claimed (theorem-grade)

- **Theorem (§2).** The Connes-Kreimer-Manchon algebraic Birkhoff
  recursion (4)-(6) is well-defined for any character `phi: H_R ->
  A_seq` of weight `+1`. This is an instance of the external retained
  theorem in
  [`CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md)
  with target `A_seq` and Rota-Baxter `P_strict`.
- **Rota-Baxter check.** `P_strict` is a Rota-Baxter operator of
  weight `+1` on the sequence algebra under componentwise
  multiplication (verified deterministically in the runner).
- **Existence vs uniqueness.** Per Manchon arXiv:math/0408405
  Remark following Theorem II.5.1, the Birkhoff decomposition exists
  but is not unique because `P_strict` is not idempotent. The
  recursion-output `phi_+, phi_-` is well-defined; the splitting of
  `phi` is not unique.

### 4.2 What is not claimed (bounded admissions A1-A4)

- **Not claimed: framework-native derivation of `alpha_LM^16`.** Per
  admissions A1-A4 of §3, no framework-native bridge from the
  abstract theorem to the framework's `alpha_LM^16` factor is
  closed. The choice of `B_4`, the identification of `P_strict` with
  the framework's staircase RG step, the choice of constant-leaf
  character, and the readout slot `n = 1` are all external
  structural choices not forced by the framework's source stack.
- **Not claimed: invalidates `CONNES_KREIMER_BRIDGE_16FOLD_BLOCKING_NO_GO_THEOREM_NOTE_2026-05-10.md`.**
  The prior round's no-go obstructions O1-O4 are not refuted; they
  are sharpened. O3 (linear ladder collapse) is mitigated by the
  `B_4` substrate (admissible cuts of `B_4` are genuinely tree-like,
  not ladder-linear), but admission A2 records that `B_4` itself is
  an external decoration. O4 (tautological readout) survives in the
  sharpened form of admission A4. O1 (non-perturbative blocking) is
  unchanged by adopting the strict-prefix-sum Rota-Baxter, since
  `P_strict` is a structural operator on the rung-indexed sequence
  algebra, not a dim-reg pole projection. O2 (no Rota-Baxter
  projector) is partially relaxed: `P_strict` is a Rota-Baxter
  operator but is non-idempotent, so per Manchon the Birkhoff
  splitting exists but is non-unique.
- **Not claimed: new repo vocabulary.** The vocabulary used —
  Hopf algebra of rooted trees, Birkhoff factorization, character,
  coproduct, Rota-Baxter operator of weight `+1`, complete binary
  tree, BZ corner, partial-sum operator — is all canonical
  Connes-Kreimer / Hopf-algebraic / lattice-theoretic vocabulary.

---

## 5. Load-bearing step (class A / bounded)

The single load-bearing step is the recursion (4)-(6) applied
deterministically with `P_strict` as Rota-Baxter operator. The
recursion is cited from the external retained theorem
[`CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md);
the Rota-Baxter property of `P_strict` is a deterministic algebraic
identity verified by sympy in the runner. No PDG / observed input
is consumed.

This is load-bearing step class A / bounded: it consists of
deterministic algebraic identity checks on a finite-dimensional
sequence algebra `A_seq`, with no Monte Carlo, no observational
fit, and no same-surface family argument. The four admissions
A1-A4 are recorded as bounded admissions in §3, each with an
explicit obstruction structure.

---

## 6. Forbidden imports check

- No PDG observed values consumed.
- No literature numerical comparators consumed (only algebraic
  formulas).
- No fitted selectors consumed.
- No new framework axioms consumed. The repo baseline physical `Cl(3)`
  on `Z^3` is untouched; the abstract theorem is external.
- No same-surface family arguments employed.
- No new repo vocabulary introduced.

---

## 7. Validation (runner)

The runner
`scripts/frontier_connes_kreimer_partial_sum_rb_b4_external_bounded.py`
deterministically verifies the following:

- **T1.** Strict-prefix-sum `P_strict` is a Rota-Baxter operator
  of weight `+1` on `A_seq` for `N = 8` (sympy symbolic check on
  arbitrary symbolic sequences `a, b`).
- **T2.** `P_strict` is **not** idempotent (`P_strict(P_strict(a))
  != P_strict(a)` for generic `a`).
- **T3.** Construct `B_4` explicitly as a nested tuple; verify it
  has 16 leaves, 31 nodes, 30 internal edges.
- **T4.** CK coproduct on small subtrees `B_1, B_2, B_3` is enumerated
  explicitly; admissible-cut counts are verified.
- **T5.** Birkhoff recursion (4)-(6) is run on `B_1` and `B_2` for
  a constant-leaf character valued in `A_seq` (with `N = 4` for
  manageability); results are recorded explicitly.
- **T6.** The "leading slot" claim of A4: `phi_+(B_d)_1 =
  alpha_LM^(#leaves)` holds **only because** `P_strict(a)_1 = 0`
  trivially, not because of Birkhoff machinery. Verified symbolically
  for `B_1, B_2`.
- **T7.** Non-leading slots: `phi_+(B_2)_2` and `phi_+(B_2)_3` are
  explicit polynomials in `alpha_LM` not equal to `alpha_LM^4`.
- **T8.** Manchon non-uniqueness check: an alternative non-Rota-Baxter
  projector (the all-zeros operator `T = 0`) on `A_seq` gives a
  different Birkhoff decomposition with `phi_+ = phi_FW` itself,
  trivially. Documents the choice-dependence of `phi_+(B_4)`.
- **T9.** Cross-check vs the cited retained external theorem
  (T3 of `scripts/frontier_connes_kreimer_birkhoff_factorization_external_narrow.py`):
  on a separate fragment (the trees `t1, t2` of the retained note),
  the recursion (4)-(6) with Laurent-pole projection reproduces the
  retained result; with `P_strict` it does not (different Rota-Baxter,
  different Birkhoff output).
- **T10.** Note boundary check: this note carries claim type
  `bounded_theorem` and not `positive_theorem`; the four admissions
  A1-A4 are explicitly recorded.

Expected: `PASS >= 10`, `FAIL = 0`.

---

## 8. Cited authorities

### Retained framework source (load-bearing)

- [`CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md)
  — external narrow positive theorem (retained). Provides the
  Birkhoff recursion structure (4)-(6).

### Plain-text framework context (not load-bearing graph edges)

`WILSON_BZ_CORNER_HAMMING_STAIRCASE_CLOSED_FORM_NOTE_2026-05-09.md`
documents the `2^4 = 16` BZ-corner structure and the `S_4`
axis-permutation symmetry of the Boolean lattice substrate. The
admission A2 in §3.2 cites this note as plain-text context for the
Boolean lattice / `B_4` distinction; it is not a load-bearing
markdown-link edge in this note.

`CONNES_KREIMER_BRIDGE_16FOLD_BLOCKING_NO_GO_THEOREM_NOTE_2026-05-10.md`
is mentioned in §4.2 as the prior round's no-go note (currently
unaudited per the live ledger). This note sharpens admission O4
into A4; it does not cite the no-go note as a load-bearing edge,
hence the plain-text-only reference here.

### External mathematical literature (inline citations)

- A. Connes & D. Kreimer, *Renormalization in Quantum Field Theory
  and the Riemann-Hilbert Problem I*, Commun. Math. Phys. **210**,
  249-273 (2000), arXiv:hep-th/9912092.
- A. Connes & D. Kreimer, *Renormalization in Quantum Field Theory
  and the Riemann-Hilbert Problem II*, Commun. Math. Phys. **216**,
  215-241 (2001), arXiv:hep-th/0003188.
- D. Manchon, *Hopf algebras, from basics to applications to
  renormalization*, arXiv:math/0408405 (2004). Theorem II.5.1 and
  the Remark following it explicitly state the existence /
  uniqueness dichotomy for non-idempotent Rota-Baxter operators.
- K. Ebrahimi-Fard, L. Guo, D. Kreimer, *Spitzer's identity and
  the algebraic Birkhoff decomposition in pQFT*, J. Phys. A
  **37**, 11037-11052 (2004), arXiv:hep-th/0407082.
- L. Guo, *An Introduction to Rota-Baxter Algebra*, International
  Press / Higher Education Press (2012). Strict-prefix-sum
  operator on sequence algebras as a Rota-Baxter operator of weight
  `+1`.
- F. Markopoulou, *An algebraic approach to coarse graining*,
  arXiv:hep-th/0006199 (2000). Cited in admission A1 as the direct
  lattice / spin-system Hopf-algebraic precedent; the construction is
  on partitioned lattices, not on `H_R` directly.
- M. Borinsky & G. V. Dunne, *Non-perturbative completion of
  Hopf-algebraic Dyson-Schwinger equations*, Nucl. Phys. B **957**,
  115096 (2020), arXiv:2005.04265. Cited in admission A3; the
  Hopf algebra organizes the perturbative input, not a trans-series
  target.
- T. Krajewski & P. Martinetti, *Wilsonian renormalization,
  differential equations and Hopf algebras*, arXiv:0806.4309 (2008).
- C. Brouder, *Quantum field theory meets Hopf algebra*, Math. Nachr.
  **282**, 1664-1690 (2009), arXiv:hep-th/0510052.
- L. Foissy, *Les algèbres de Hopf des arbres enracinés décorés I,
  II*, Bull. Sci. Math. **126**, 193-239 and 249-288 (2002).
  Decorated planar rooted trees support `B_d` substrates with
  decoration, in a Hopf algebra `H_R^{dec}` related to but distinct
  from the un-decorated `H_R` of the retained external theorem.

---

## Status

**bounded_theorem proposal.** The Connes-Kreimer-Manchon algebraic
Birkhoff recursion (4)-(6) is well-defined on `H_R` with target
`A_seq` and the strict-prefix-sum Rota-Baxter operator `P_strict` of
weight `+1`. This instantiates the retained external theorem in
[`CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](CONNES_KREIMER_BIRKHOFF_FACTORIZATION_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md)
on a specific finite-dimensional target. **Four bounded admissions
A1-A4** are recorded:

- **A1** Markopoulou hep-th/0006199 uses a different Hopf algebra
  (partitioned lattices, not `H_R`).
- **A2** `B_4` complete binary tree is not forced by the framework's
  `2^4 = 16` BZ-corner Boolean lattice substrate.
- **A3** Borinsky-Dunne arXiv:2005.04265 organizes a perturbative
  expansion, not a CK character into a Rota-Baxter trans-series.
- **A4** The leading slot `phi_+(B_d)_1 = alpha_LM^(#leaves)` is a
  tautological readout (`P_strict(a)_1 = 0`); other slots are
  polynomial mixtures.

Independent audit will set effective status. This source-note proposal
does not predict that verdict.
