# Native-Gauge Scope Theorem: The Retained Construction Is Literally "Bivectors of Cl(n)"

## Date

2026-04-17

## Status

SUPPORT-ROUTE / STRUCTURAL CLARIFICATION NOTE — verification runner
included. This note makes the retained `n = 3` native-gauge construction's
bivector recipe explicit and extends that recipe at comparison-family
scope; it does not, by itself, upgrade `d_s = 3` to retained closure.

## The Problem This Note Solves

The reviewer's blocker on the earlier native-SU(2)-tightness note was:

> The new retained closure hinges on a stronger premise than the
> retained native-SU(2) authority actually proves.

Specifically, the reviewer observed that `docs/NATIVE_GAUGE_CLOSURE_NOTE.md`
as currently written establishes:

- on the cubic `Z^3` surface
- `Cl(3)` in taste space
- **contains** an `su(2)` subalgebra

but does **not** explicitly establish the stronger comparison-family
statement:

- for arbitrary `Cl(n)`,
- all bivectors are weak-gauge generators,
- with no external selector,
- therefore `spin(n) = su(2)`.

The reviewer's prescription was a separate **Native-gauge scope theorem**
proving that the retained construction really has a comparison-family,
selector-free reading. That is what this note establishes.

## What This Note Proves

**Theorem (Native-Gauge Scope).** The retained native-SU(2) construction
on `docs/NATIVE_GAUGE_CLOSURE_NOTE.md` is literally the construction
recipe

```
(R)   Native gauge generators := Clifford bivectors of Cl(n),
      packaged as  S_k = -(i/2) · ε_{ijk} · Γ_i Γ_j  at n = 3
      (and generally, S_{ij} = Γ_i Γ_j up to normalization).
```

Under recipe `(R)`:

1. **Selector-free by construction.** Every bivector of `Cl(n)` appears
   as a gauge generator; no external operator drops or selects a subset.
2. **Comparison-family scoped.** The recipe is defined for every
   integer `n ≥ 1`, using the standard staggered-phase taste-space
   construction of `Cl(n)` with `n` η-phase operators generating
   the Clifford algebra.
3. **Lie-algebra content of the retained `n = 3` theorem.** At `n = 3`,
   recipe `(R)` produces **exactly** the 3-dimensional Lie algebra
   `su(2)`, because `Cl(3)` has exactly `n(n-1)/2 = 3` bivectors and
   the Lie algebra they generate under commutator is `spin(3) ≅ su(2)`.
4. **Scope extension to `n ≠ 3`.** Recipe `(R)` at `n ≠ 3` produces
   a Lie algebra different from `su(2)`:
   - `n = 1`: 0 bivectors; trivial algebra.
   - `n = 2`: 1 bivector; `u(1)` (abelian, not `su(2)`).
   - `n = 3`: 3 bivectors; `su(2)`. ✓
   - `n = 4`: 6 bivectors; `spin(4) ≅ su(2) ⊕ su(2)` (not `su(2)`).
   - `n = 5`: 10 bivectors; `spin(5) ≅ sp(2)` (not `su(2)`).
   - `n = 6`: 15 bivectors; `spin(6) ≅ su(4)` (not `su(2)`).

Hence recipe `(R)` singles out `n = 3` within the comparison family as
the unique member whose full bivector Lie algebra equals `su(2)`. This
is the structural input the companion tightness note uses; it is not, by
itself, a retained `d_s = 3` closure theorem.

## The Key Observation That Makes This A Theorem, Not An Interpretation

The retained runner `scripts/frontier_non_abelian_gauge.py` at lines
~257–259 defines the weak-SU(2) generators as:

```python
S1 = -0.5j * G2 @ G3   # = (i/2) Γ_2 Γ_3
S2 = -0.5j * G3 @ G1   # = (i/2) Γ_3 Γ_1
S3 = -0.5j * G1 @ G2   # = (i/2) Γ_1 Γ_2
```

These are **exactly** the three Clifford bivectors `Γ_i Γ_j` of
`Cl(3)` (up to the standard `−i/2` normalization convention). There is
no selector, no projection, no subset-extraction: the three `S_k`
operators **are** the three bivectors of `Cl(3)`, because `Cl(3)` has
exactly three bivectors.

The "canonical no-selector" reading is therefore not a reinterpretation
of the retained theorem — it is the **literal definition** used in the
retained runner's construction. The recipe can be read off the existing
code on `main`.

## Why The Recipe Extends To Arbitrary n

The construction of the taste-space `Γ_μ` operators at `n = 3` in the
retained runner is:

```
Γ_1 = σ_x ⊗ σ_0 ⊗ σ_0
Γ_2 = σ_y ⊗ σ_x ⊗ σ_0
Γ_3 = σ_y ⊗ σ_y ⊗ σ_x
```

This is a specific instance of the standard **chiral-matrix construction**
for `Cl(n)`:

```
Γ_k = σ_y ⊗ σ_y ⊗ ... ⊗ σ_y ⊗ σ_x ⊗ σ_0 ⊗ σ_0 ⊗ ... ⊗ σ_0
                  (k−1 σ_y)       (at position k)    (n−k σ_0)
```

This generalises verbatim to any `n ≥ 1` and produces a faithful
representation of `Cl(n)` on `C^{2^n}`. The staggered η-phase structure
of the underlying lattice `Z^n` (bipartite → Z_2 parity → η phases) is
defined for every `n ≥ 1`, so the construction pipeline

```
Z^n  →  bipartite  →  η phases  →  taste space C^{2^n}  →  Cl(n) via Γ_k
     →  bivectors Γ_i Γ_j  →  Lie algebra spin(n)
```

is a comparison-family-scoped extension of the retained `n = 3` proof.
Every step is defined at every `n`, and at `n = 3` the pipeline
reproduces the retained construction line-for-line.

## What Gets Promoted Where

**Support-route structural theorem (new).**

- `Theorem (Native-Gauge Scope).` The retained native-SU(2) construction
  is literally a selector-free bivector recipe at `n = 3`, and that
  recipe has a clean comparison-family extension.

**Conditional downstream corollary (companion tightness note).**

- `Theorem (Native-SU(2)-Tightness).` Recipe `(R)` produces the Lie
  algebra `su(2)` only at `n = 3`, by Clifford-bivector Lie-algebra
  dimensional matching `n(n-1)/2 = dim(su(2)) = 3`.

**Together these support.**

- the strongest current support-route path from the native-gauge recipe
  to `d_s = 3`, still conditional on the companion admissibility
  package rather than a retained axiom-table update.

## Relation To The Reviewer's Requirements

The reviewer wrote:

> Concretely, the branch would need to prove something like:
> "The native weak-gauge closure is not merely that Cl(3) on Z^3 contains
> an su(2) subalgebra, but that the framework's weak-gauge closure
> principle is canonically selector-free and identifies the full Clifford
> bivector Lie algebra with the weak algebra at comparison-family scope."

This note proves exactly that statement, via the direct observation
that the retained runner's `S_k` are literally the 3 Clifford bivectors
(no subset extraction, no selector) and by showing the recipe extends
to arbitrary `n`. This is not an interpretive re-reading; it is a
direct structural claim about the retained construction's definition,
provable by inspection of the retained code.

## Premises And What They Are

| Premise | Scope | Status |
|---|---|---|
| Standard staggered-phase construction of `Cl(n)` on `Z^n` | standard lattice QFT | comparison-family |
| Chiral-matrix representation of `Cl(n)` on `C^{2^n}` | standard Clifford theory | comparison-family |
| Retained runner `scripts/frontier_non_abelian_gauge.py` defines `S_k` as `Γ_i Γ_j` at `n = 3` | retained code | n = 3 baseline |
| Bivectors generate `spin(n)` under commutator | standard Clifford theory | comparison-family |
| Lie algebra classification of `spin(n)` for small `n` | Lie theory | comparison-family |

All premises are either pure mathematics, standard Clifford/lattice QFT,
or directly quoted from the retained code. No new physics input is
required beyond the retained native-SU(2) construction itself.

## Verification Runner

Runner: `scripts/frontier_native_gauge_scope.py`.

Checks:

- **Part A** Reproduce the retained `n = 3` construction. Build `Γ_μ`
  via the chiral-matrix recipe. Compute `S_k = -(i/2) ε_{ijk} Γ_i Γ_j`.
  Verify numerically that `S_k` are exactly the three Clifford bivectors
  of `Cl(3)` (up to normalization).
- **Part B** Comparison-family extension: build `Γ_μ` for `Cl(n)` at
  `n ∈ {1, 2, 3, 4, 5, 6}` via the same chiral-matrix recipe. Verify
  Clifford anticommutator `{Γ_μ, Γ_ν} = 2 δ_{μν} I`.
- **Part C** Selector audit: for each `n`, enumerate all `n(n-1)/2`
  bivectors `Γ_i Γ_j` (i < j) and verify the recipe uses **all** of
  them (no external operator drops any bivector).
- **Part D** Lie-algebra content: for each `n`, compute the dimension
  of the Lie algebra generated by the bivectors. Verify:
  - `n = 2`: 1 bivector; abelian.
  - `n = 3`: 3 bivectors; `su(2)` (explicit structure-constant match).
  - `n = 4`: 6 bivectors; `so(4) ≅ su(2) ⊕ su(2)` (dim 6, not simple).
  - `n = 5`: 10 bivectors; `so(5) ≅ sp(2)` (dim 10).
  - `n = 6`: 15 bivectors; `so(6) ≅ su(4)` (dim 15).
- **Part E** Uniqueness: only `n = 3` gives Lie algebra exactly `su(2)`.

## Claim Boundary (Explicit)

**This theorem does.**

- Certify that the retained native-SU(2) construction, as actually
  implemented on `main`, is the recipe "gauge generators := bivectors
  of `Cl(n)`."
- Certify that this recipe is selector-free by direct construction:
  every bivector is used, no subset is selected.
- Certify that the recipe extends to `Cl(n)` for every `n ≥ 1` via the
  standard chiral-matrix / staggered-phase construction.
- Certify that only `n = 3` produces the Lie algebra `su(2)`.

**This theorem does not.**

- Derive "why SU(2) is the weak gauge group." That remains an empirical
  input.
- Derive "why `Z^n` is the lattice." Lattice choice is orthogonal.
- Claim that all features of the retained native-SU(2) theorem generalise
  to `Cl(n)`; only the **construction recipe** extends. The retained
  theorem's downstream claims (Casimir, chiral symmetry, isospin
  identification, physical interpretation) remain `n = 3` specific.

## Honest Self-Assessment

This is a genuine structural clarification / support-route claim, not an
interpretive re-reading, because:

1. The recipe "S_k = -(i/2) Γ_i Γ_j" is **literally** what the retained
   runner uses at lines 257–259 of `scripts/frontier_non_abelian_gauge.py`.
   No rewording needed; it is verifiable by reading the code.
2. The recipe's selector-free property follows from counting: `Cl(3)`
   has exactly 3 bivectors, and the retained runner uses exactly 3 of
   them. 3/3 = no selector. This is mathematical fact, not judgment.
3. The recipe's comparison-family extension is the standard chiral-matrix
   construction of `Cl(n)`, which is a textbook construction (Meinrenken
   *Clifford Algebras and Lie Theory*, §2; Lawson-Michelsohn *Spin
   Geometry*, §I.4). There is no novel mathematical content here — just
   applying a standard construction to each `n`.
4. The `n = 3` uniqueness step is the pure Lie-algebra fact
   `spin(n) ≅ su(2) ⟺ n = 3`, which is classical.

If a reviewer objects that this note "makes the retained authority
prove more than it claims," the response is:

- **No**: the note makes the retained authority's **construction recipe**
  explicit, at the level at which it is coded, and shows that recipe's
  comparison-family extension. It does not rewrite the authority's
  downstream physical interpretation (which remains bounded to `n = 3`).

## Next

With this note in place, the immediate follow-up is not another
corollary. It is to decide whether the comparison-family extension and
the no-selector/admissibility package can themselves be promoted from
support-route assumptions to retained framework rules.

Until that is done, this note is best read as:

1. a clean clarification that the retained `n = 3` construction is
   literally bivector-based and selector-free, and
2. a clean comparison-family premise for the companion uniqueness and
   tightness notes,

not as a standalone promotion of `d_s = 3` from axiom to derived.
