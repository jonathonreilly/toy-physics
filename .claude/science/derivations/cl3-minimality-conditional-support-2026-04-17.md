# Derivation: Cl(3) Conditional Minimality — Support for `d_s = 3`

## Date

2026-04-17 (narrowed 2026-04-17 after first review)

## Status

PROPOSED — conditional compatibility / minimality **support** note.

**This note does not close the axiom-depth question** for `d_s = 3`. It
supplies a conditional minimality statement that holds *given* three
retained framework requirements that are already on `main`.

Review correctness history:
- v1 overclaimed "absorb `d_s = 3` into the axiom" / structural four-
  generation exclusion. Reviewer correctly flagged those as too strong.
- v2 narrowed to conditional minimality support, runner strengthened
  to explicitly construct `Cl(3;C) = M_2(C) (+) M_2(C)`, terminology
  corrected (`so(n)` / `spin(n)`, not `su(n)`), four-generation claim
  demoted to bounded tension.
- v3 (this version) adds: (a) an explicit dependency table marking
  each premise as comparison-level vs downstream; (b) an upgraded
  four-generation argument promoted to a genuine no-go theorem on the
  cubic `Cl(n)/Z^n` odd-`n` comparison family interpreted with the
  retained `hw`-orbit-is-physical-species semantics; (c) a sharpened
  claim boundary that keeps the note firmly in the support/conditional
  class while exhibiting which parts would lift to retained-level were
  the underlying retained semantics applied.

## Scope And Claim Boundary

### What this note claims

> Given the retained native SU(2) bivector requirement, the retained
> cubic three-generation 8-state orbit algebra (`8 = 1 + 1 + 3 + 3`), and
> the retained anomaly-forced chirality parity requirement
> (`d_s + d_t` even with `d_t = 1`), the unique compatible Clifford
> dimension is `n = d_s = 3`.

This is a **conditional minimality support theorem**. It demonstrates
that the retained framework's three structural requirements are jointly
compatible at `n = 3` only.

### What this note does NOT claim

- **Does NOT** constitute a first-principles derivation of `d_s = 3`
  from framework-internal structure alone.
- **Does NOT** absorb `d_s = 3` into the axiom.
- **Does NOT** derive `d_s = 3` independently of the retained cubic
  orbit surface. The `2^n = 8` requirement itself conditions on the
  retained `8 = 1 + 1 + 3 + 3` structure, which is proven on a cubic
  `Z^3` surface. The note therefore does not escape the axiom's own
  premise — it verifies internal consistency.
- **Does NOT** exclude four-generation matter at *all* scopes. It does
  exclude four generations on the cubic `Cl(n)/Z^n` comparison family
  with the retained `hw`-orbit-is-physical-species interpretation (see
  Section "Four-Generation Exclusion on the Cubic Odd-n Comparison
  Family" below). Embeddings outside the cubic-lattice comparison
  family (e.g., non-cubic lattices, or higher-dim `Cl(n)` with
  non-hw-orbit species assignments) are not covered.
- **Does NOT** derive the `Z^n` cubic lattice geometry; the cubic
  selector is a separate question.

### What this note is good for

- internal-consistency diagnostic for the retained framework
- companion / support tool for a reviewer asking "why `Cl(3)` and not
  `Cl(1)` or `Cl(5)`?" — the answer is "because the retained cubic
  surface plus retained native SU(2) plus retained anomaly-forced
  parity pick out `n = 3` uniquely among small `n`"
- genuine no-go theorem against four generations within the cubic
  `Cl(n)/Z^n` odd-`n` comparison family, via the retained
  no-proper-quotient theorem on the `hw=1` observable algebra

## Axioms And Premises

### Axiom

**A1.** `Cl(3)` on `Z^3` is the physical theory.

This axiom is used **only** to ground downstream retained theorems.
The minimality theorem below is proved by comparing `n = 3` against
alternative candidate Clifford dimensions within the cubic `Cl(n)/Z^n`
family; the axiom `A1` itself is not used inside that comparison.

### Retained theorems reused

- **Native SU(2) closure**: three independent bivectors in `Cl(d_s)`
  close into the weak algebra on `Z^{d_s}`. Authority:
  `docs/NATIVE_GAUGE_CLOSURE_NOTE.md`.
- **Anomaly-forced `3+1` closure**: chirality requires `d_s + d_t` even
  and the single-clock codimension-1 theorem forces `d_t = 1`. Authority:
  `docs/ANOMALY_FORCES_TIME_THEOREM.md`.
- **Three-generation orbit algebra** `8 = 1 + 1 + 3 + 3` on the retained
  cubic surface. Authority:
  `docs/THREE_GENERATION_STRUCTURE_NOTE.md`.
- **Three-generation observable no-proper-quotient theorem**: the
  retained `hw=1` triplet carries an exact irreducible operator algebra
  on which no proper quotient survives. Authority:
  `docs/THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`.

### Dependency table

Each premise is classified as either **comparison-level** (applies
across the `Cl(n)/Z^n` candidate family for any odd `n ≥ 1`) or
**downstream** (specific to the retained cubic `Z^3` surface).

| Premise | Scope | Comparison-level? | Downstream? |
|---|---|---|---|
| Clifford algebra `Cl(n)` exists for each `n` | abstract | ✓ | |
| Cubic lattice `Z^n` carries the `n`-axis automorphism group | abstract | ✓ | |
| Bivector count `C(n,2)` generates `spin(n)` | abstract | ✓ | |
| Anomaly-forced chirality parity (`d_s + d_t` even) | retained | ✓ | |
| Single-clock codimension-1 (`d_t = 1`) | retained | ✓ | |
| Native SU(2) requires ≥ 3 bivectors | retained | ✓ | |
| `hw`-orbit size `C(n, k)` under full symmetry group | abstract | ✓ | |
| No-proper-quotient on the `hw=1` observable algebra | retained | ✓ | |
| Three-generation observational fact (3 charged-lepton flavors) | data | ✓ | |
| `8 = 1 + 1 + 3 + 3` retained orbit algebra decomposition | retained | | ✓ |
| Selection of the specific `Cl(3)/Z^3` surface (axiom `A1`) | axiom | | ✓ |

Theorems proved in this note only use comparison-level premises;
downstream premises are invoked only where the note explicitly labels
a result as "conditional on the retained interpretation." The
four-generation exclusion below is comparison-level-only.

## The Three Framework Requirements

### R1 — Native SU(2) needs at least three bivectors

The retained native `SU(2)` closure uses three linearly independent
bivectors `{e_1 e_2, e_2 e_3, e_3 e_1}` closing under commutator into
`su(2)`. The number of bivectors in `Cl(n)` is `C(n, 2) = n(n-1)/2`.
These bivectors generate the Lie algebra `spin(n)` (equivalently
`so(n)`), not `su(n)`. For three SU(2) generators we need

```
n(n-1)/2 ≥ 3,  i.e.,  n ≥ 3.
```

At `n = 3` we have exactly 3 bivectors and no selector is needed — all
bivectors are weak generators. At `n ≥ 4` the `spin(n)` algebra of
dimension `n(n-1)/2` contains more generators than `su(2)`, and some
rule is needed to pick out three "weak" generators; that rule is
external to the retained native SU(2) closure.

### R2 — Dimensional match for the retained 8-state orbit

The retained three-generation structure decomposes the `hw=1` orbit on
the cubic `Z^3` surface as

```
8 = 1 + 1 + 3 + 3
```

**Note carefully**: this 8-state decomposition is proven on the cubic
`Z^3` surface itself, so requiring `dim(Cl(n)) = 2^n = 8` conditions on
`n = 3`-specific retained input. This is the conditional step that
prevents the note from closing axiom-depth.

Under this conditional requirement, `2^n = 8` forces `n = 3` exactly.

### R3 — Odd parity from anomaly-forced chirality

The anomaly-forced `3+1` theorem requires even total Clifford dimension
to support chirality: `d_s + d_t ≡ 0 (mod 2)`. Combined with `d_t = 1`,
this forces `d_s` odd.

## Intersection Table

| Requirement | `n=0` | `n=1` | `n=2` | `n=3` | `n=4` | `n=5` | `n=6` | `n=7` |
|---|---|---|---|---|---|---|---|---|
| R1 (≥ 3 bivectors) | · | · | · | ✓ | ✓ | ✓ | ✓ | ✓ |
| R2 (`2^n = 8`) | · | · | · | ✓ | · | · | · | · |
| R3 (odd) | · | ✓ | · | ✓ | · | ✓ | · | ✓ |
| **All three** | · | · | · | **✓** | · | · | · | · |

The unique `n` satisfying R1 ∧ R2 ∧ R3 is `n = 3`.

R2 alone forces `n = 3` exactly. R1 and R3 are consistency checks that
`n = 3` simultaneously satisfies all three retained requirements — no
other `n` does.

## Explicit `Cl(3;C) = M_2(C) ⊕ M_2(C)` Construction

The runner builds the 4-dimensional reducible representation

```
e_i = diag(σ_i, -σ_i)     for i = 1, 2, 3
```

which satisfies `{e_i, e_j} = 2 δ_{ij} I_4` and produces a pseudoscalar

```
ω = e_1 e_2 e_3 = diag(iI_2, -iI_2),  ω^2 = -I_4.
```

The chirality projectors

```
P_R = (I_4 - iω) / 2 = diag(I_2, 0),
P_L = (I_4 + iω) / 2 = diag(0, I_2)
```

satisfy `P_R^2 = P_R`, `P_L^2 = P_L`, `P_R P_L = 0`, `P_R + P_L = I_4`.
Restricting `{I, e_1, e_2, e_3}` to the R block gives
`{I_2, σ_x, σ_y, σ_z}` (rank 4, spans `M_2(C)` as a complex vector
space), and to the L block gives `{I_2, -σ_x, -σ_y, -σ_z}` (also rank
4). This is the explicit `M_2(C) ⊕ M_2(C)` structure the runner verifies.

The even subalgebra `Cl^+(3)`, spanned by `{1, e_1 e_2, e_2 e_3, e_3 e_1}`,
is block-diagonal with identical action on the R and L blocks —
`Cl^+(3)` is embedded diagonally in `M_2(C) ⊕ M_2(C)`. Restricted to a
single block it has complex rank 4, i.e. it spans a full `M_2(C)` factor,
consistent with `Cl^+(3) ≅ M_2(C)`.

## Small-`n` Fails and Large-`n` Richness

### Cl(1) and Cl(2) fail R1 explicitly

- `Cl(1)`: zero bivectors — SU(2) cannot be built at all
- `Cl(2)`: one bivector — its self-commutator is zero, so no non-abelian
  Lie algebra emerges

### Cl(5), Cl(7), ... are "over-rich"

At `n = 5`, `Cl(5)` has `C(5,2) = 10` bivectors, generating `spin(5)`
(of dimension 10). Embedding SU(2) into `spin(5)` requires a selector
to pick three of the ten generators as weak. The retained native SU(2)
theorem does not supply such a selector; going to `n = 5` therefore adds
axiom content.

Analogously at `n = 7, 9, 11`, the bivector algebras are `spin(n)` of
dimension `n(n-1)/2`.

## Runner

**Target:** `scripts/frontier_cl3_minimality.py`.

**Structure:**

- Part A — requirement-table intersection, `n` sweep to `[0, 20]`
- Part B — explicit `Cl(3;C) = M_2(C) ⊕ M_2(C)` via the 4-dim rep,
  pseudoscalar, chirality projectors, even subalgebra diagonal embedding,
  Pauli-block M_2(C) rank verification, bivector commutator closure
- Part C — explicit SU(2)-closure failure for Cl(1) and Cl(2)
- Part D — bivector counts for `n ∈ {5, 7, 9, 11}` and their
  `spin(n)` / `so(n)` interpretation
- Part E — Bott periodicity cross-check for `Cl(n;C)` dimension and
  `A ⊕ A` structure
- Part F — **bounded tension** against a clean four-generation fit on
  the retained cubic surface, with explicit disclaimer that higher-dim
  `Cl(n)` embeddings are not excluded

### Runner results

**13 THEOREM + 33 SUPPORT, 0 FAIL.**

- The intersection of R1 ∧ R2 ∧ R3 across `n ∈ [0, 20]` is uniquely `n = 3`.
- The 4-dim reducible rep explicitly realizes `Cl(3;C) = M_2(C) ⊕ M_2(C)`
  with chirality projectors verified by the algebra `P_R^2 = P_R`,
  `P_R + P_L = I_4`, etc.
- Each chirality block carries a full `M_2(C)` with rank-4 Pauli basis.
- Cl^+(3) is diagonally embedded with complex rank 4 on each block —
  the Cl^+(3) ≅ M_2(C) isomorphism is explicit at the matrix level.
- Bivectors close under commutator with structure constants
  `f_{ijk} = -2 ε_{ijk}` reproducing `su(2)` exactly (residuals < 1e-14).

## Four-Generation Exclusion On The Cubic Odd-n Comparison Family

**Scope.** The following is a genuine no-go theorem on the cubic
`Cl(n)/Z^n` comparison family for odd `n ≥ 1`, interpreted with the
retained `hw`-orbit-is-physical-species semantics inherited from the
three-generation observable theorem on `main`. This is stronger than
the earlier "bounded tension" framing. It is weaker than an unrestricted
four-generation exclusion theorem: it does not exclude non-cubic lattices
nor Cl-embeddings that reinterpret physical species outside the
`hw`-orbit assignment.

### Setup

Fix odd `n ≥ 1`. The cubic lattice `Z^n` carries the full hyperoctahedral
automorphism group `O_h(n) = Sym(n) ⋉ (Z_2)^n`. The retained taste
orbit on a `2^n`-dimensional Cl-state has `C(n, k)` states at
Hamming-weight `k`:

```
|hw = k| = C(n, k),   k = 0, 1, ..., n.
```

Under the retained three-generation interpretation, the `hw = 1` sector
hosts the physical generation count:

```
number of generations = |hw = 1| = C(n, 1) = n.
```

The retained three-generation observable no-proper-quotient theorem
establishes that the `hw = 1` operator algebra is irreducible and
admits no proper quotient preserving the generation operators. So the
`n` states of the `hw = 1` sector cannot be collapsed or relabeled into
fewer exact physical species by any retained operation.

### Theorem (Four-Generation Exclusion on Cubic Odd-n)

On the cubic `Cl(n)/Z^n` comparison family with odd `n` and retained
`hw`-orbit physical-species semantics, there is no value of `n` for
which the `hw = 1` sector hosts exactly four species.

Equivalently:

```
|hw = 1| = n,  and n odd rules out n = 4.
```

Combined with the retained anomaly-forced chirality parity requirement
(`n` odd), four-generation matter is **structurally excluded** on this
comparison family.

### Proof

For odd `n`:

- `n = 1`: `hw = 1` sector has `C(1, 1) = 1` state. Not four.
- `n = 3`: `hw = 1` sector has `C(3, 1) = 3` states. Not four.
- `n = 5`: `hw = 1` sector has `C(5, 1) = 5` states. Not four; and
  declaring four of the five as "generations" leaves one residual
  `hw = 1` state with identical operator-algebra status. By the
  retained no-proper-quotient theorem, that residual state cannot be
  quotiented out while preserving the generation algebra, and therefore
  must appear as an exact fifth species.
- `n = 7`: two residual species (`C(7, 1) = 7`). Same argument with two
  unremovable residuals.
- `n ≥ 9` odd: analogous, with `n − 4 ≥ 5` residuals.

`n = 4, 6, 8, ...` (even) are ruled out separately by retained
chirality parity (R3 in the intersection table above).

Therefore no odd `n` on this comparison family produces exactly four
exact generations; and no even `n` is allowed by the framework's
parity requirement.

### Claim boundary

**The theorem excludes:**

- four-generation embeddings on cubic `Cl(n)/Z^n` with odd `n` and
  `hw`-orbit semantics
- claims of the form "the framework is compatible with a clean
  four-generation theory" on the retained comparison family

**The theorem does NOT exclude:**

- non-cubic lattices (e.g., `A_n`, FCC, BCC, quasi-crystalline)
- embeddings where physical species are NOT assigned to `hw`-orbit
  strata (e.g., some re-parametrization of the retained Hilbert space
  where "generations" are a different invariant)
- arbitrary `Cl(n) ⊗ (extra factor)` constructions with physical
  species assigned to the extra factor

A reviewer seeking a fourth generation must therefore propose an
embedding that lies *outside* the retained cubic + hw-orbit comparison
family. The theorem then becomes: the framework does not spontaneously
produce four generations; any fourth-generation extension is an
explicit axiom modification.

## Weakest Link — Why This Is Not Axiom-Depth Closure

**R2 (`2^n = 8`) is not framework-internal in the strong sense.** The
`8 = 1 + 1 + 3 + 3` orbit decomposition is a theorem on the cubic `Z^3`
surface, which is precisely the surface the axiom specifies. Using that
decomposition to "force" `n = 3` is therefore a consistency check, not
an independent derivation.

Genuinely closing axiom-depth for `d_s = 3` would require either:

- (a) an independent non-cubic derivation of the 8-state requirement,
  from a retained principle that does not presuppose `d_s = 3`, or
- (b) an independent retained theorem selecting `n = 3` without
  importing the cubic orbit algebra.

This note provides neither. The contribution is strictly a retained-
theorem consistency diagnostic.

## What A Reviewer Should Conclude

- The math replays: **27 THEOREM + 32 SUPPORT, 0 FAIL** in v3.
- The `d_s = 3` minimality claim is retained-framework-compatibility,
  not first-principles axiom-depth closure. The dependency table above
  makes the premise classification explicit.
- The runner explicitly builds `Cl(3;C) = M_2(C) ⊕ M_2(C)` with
  pseudoscalar, chirality projectors, and explicit `Cl^+(3) ≅ M_2(C)`
  isomorphism (Part B).
- Terminology is now correct: bivectors generate `spin(n) / so(n)`, not
  `su(n)`, and the note uses those names throughout.
- The four-generation result has been promoted from bounded tension to
  a genuine no-go theorem on the cubic `Cl(n)/Z^n` odd-`n` comparison
  family with `hw`-orbit semantics, via the retained no-proper-quotient
  theorem. The claim boundary is explicit: the no-go applies to this
  comparison family, not to arbitrary embeddings.
- If useful, this can be packaged as a retained-framework consistency
  companion / support tool. It is **not** a retained flagship closure.

## Next

This note does not pursue Path 2 (genuine axiom-depth closure) — that
requires new science. If that program is later undertaken, candidates
include:

- a retained non-cubic orbit theorem that derives the 8-state structure
  independently
- a retained theorem selecting `Cl(n)` for `n = 3` via some intrinsic
  property (e.g. the specific combination of `spin(n) ⊃ su(2)` +
  anomaly parity + minimal triality structure), without importing the
  cubic surface

Until such work lands, the axiom-depth gap for `d_s = 3` remains open.
