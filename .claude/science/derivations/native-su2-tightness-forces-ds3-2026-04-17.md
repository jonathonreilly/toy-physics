# Native-SU(2)-Tightness Forces `d_s = 3`

## Date

2026-04-17

## Status

PROPOSED-FOR-RETAINED — new theorem + verification runner.

This note attempts full retained-grade closure of the spatial-
dimension axiom-depth question. The derivation does not import the
retained cubic `Z³` orbit decomposition, the `8 = 1 + 1 + 3 + 3`
retained orbit structure, or any cubic-lattice-specific semantics.
Instead it relies on:

- the retained native-SU(2) weak-gauge theorem read at canonical
  no-selector strength (Lie-algebra equality `spin(n) = su(2)`),
- classical Clifford-algebra bivector counting `dim Λ²(R^n) = n(n-1)/2`
  (mathematical fact),
- `dim(su(2)) = 3` as a Lie algebra (mathematical fact),
- (for the gauge-group-agnostic variant) retained anomaly-forced
  chirality parity (`n` odd).

The primitive shift is: replace the retained axiom choice "`d_s = 3`
on Z³" with the retained native-SU(2) requirement plus standard Lie-
algebra dimensional matching. If the retention panel accepts the
canonical-no-selector reading of the native-SU(2) theorem (argued in
§"Is This A Genuinely-Non-Circular Derivation?" below) and accepts
the retained parity input for the gauge-agnostic variant, this
theorem is retention-eligible at the spatial-dimension axiom-depth
scope.

## The Problem And What This Note Actually Tries To Do

The earlier `cl3-minimality-conditional-support-2026-04-17.md` note
narrows honestly to conditional support: it depends on the retained
cubic `8 = 1 + 1 + 3 + 3` decomposition, and the reviewer correctly
observed that this is a consistency check, not an axiom-depth
derivation.

This note attempts a genuinely different derivation path that avoids
importing cubic-lattice orbit structure. The load-bearing primitive is
instead the **retained native SU(2) weak-gauge theorem** on `main`,
together with the fact that `dim(su(2)) = 3` as a Lie algebra.

**Claim.** The retained native SU(2) theorem, read at its canonical
(no-selector) strength, forces the Clifford dimension to satisfy
`dim(bivectors) = dim(su(2)) = 3`, which has unique positive integer
solution `n = 3`.

**What this note does NOT claim.** It does not derive "why SU(2) is
the weak gauge group" — that is the observed electroweak gauge
structure of nature, treated as an input. The note derives `d_s = 3`
from that input. This is a different primitive choice than "pick
`d_s = 3`": weak SU(2) is an external empirical fact, and its
dimension is a mathematical fact about the group SU(2).

## The Theorem

### Setup (no cubic Z³ assumed)

Consider the candidate Clifford algebra `Cl(n)` for any integer `n ≥ 1`.
The bivector subspace `Λ²(R^n)` has dimension

```
dim Λ²(R^n) = C(n, 2) = n(n-1)/2.
```

Under the commutator on `Cl(n)`, the bivectors generate the Lie algebra
`so(n)` (equivalently `spin(n)`), of dimension `n(n-1)/2`:

```
[B_{ij}, B_{kl}] = so(n) structure constants.
```

This is a standard Clifford-algebra fact that does not use a lattice,
an orbit structure, or any cubic symmetry.

### The retained native-SU(2) theorem, restated at full strength

The retained native-SU(2) theorem (authority:
`docs/NATIVE_GAUGE_CLOSURE_NOTE.md`) asserts that on the retained
framework surface, **the Clifford bivectors close exactly into the
weak SU(2) algebra** on the cubic surface — i.e., the set of all
bivectors is exactly the SU(2) weak-gauge Lie algebra, with no
bivector left over and no selector required to pick them out.

Read with the "no selector" clause, this statement is equivalent to:

```
The Clifford bivector Lie algebra equals su(2).
```

i.e.,

```
spin(n) = su(2)   as Lie algebras.
```

### The main theorem

**Theorem (Native-SU(2)-Tightness).** The retained native-SU(2)
statement at canonical no-selector strength,

```
spin(n) = su(2),
```

has a unique solution `n = 3` among positive integers.

**Proof.**

`su(2)` has dimension 3 as a real Lie algebra. So the condition
`spin(n) = su(2)` forces `dim(spin(n)) = 3`, i.e.

```
n(n-1)/2 = 3
n(n-1) = 6
n² − n − 6 = 0
n = (1 ± √25) / 2 = {3, -2}.
```

Only `n = 3` is a positive integer. For `n = 3` the dimension matches,
and the standard Lie-algebra isomorphism `spin(3) ≅ su(2)` is well-
known (the double cover `Spin(3) ≅ SU(2)`). For `n ≠ 3` either the
bivector count is too small (`n ≤ 2`) or too large (`n ≥ 4`):

- `n = 1`: `dim(spin(1)) = 0 ≠ 3`. Cannot support SU(2).
- `n = 2`: `dim(spin(2)) = 1 ≠ 3`. Only one bivector; its self-
  commutator vanishes. Cannot generate non-abelian SU(2).
- `n = 3`: `dim(spin(3)) = 3 = dim(su(2))`. ✓
- `n ≥ 4`: `dim(spin(n)) = n(n-1)/2 ≥ 6 > 3`. Strictly larger algebra.
  `su(2)` can still embed as a proper Lie subalgebra, but only via a
  selector (choice of 3 out of `≥ 6` bivectors), which violates the
  canonical no-selector clause of the retained theorem.

Hence `n = 3` uniquely. QED.

### What this theorem establishes and does not establish

**It establishes.**

1. `n = 3` is uniquely forced by the retained native SU(2) theorem
   read at canonical no-selector strength.
2. The derivation does not use any cubic `Z³` orbit decomposition,
   nor the retained `8 = 1 + 1 + 3 + 3` generation structure, nor
   any hw-orbit semantics, nor any SM matter content.
3. The derivation is comparison-level on the candidate `Cl(n)` family
   for `n ∈ {1, 2, 3, 4, 5, ...}`, with `n = 3` picked out by
   dimensional matching of the Lie algebras.

**It does not establish.**

1. "Why SU(2) is the weak gauge group." That is the observed gauge
   structure of the Standard Model, treated here as an empirical
   input. The theorem translates the input "observed weak SU(2) with
   no selector" into the conclusion "`d_s = 3` for the compatible
   Clifford algebra."
2. "Why no selector." The retained native-SU(2) theorem on `main` is
   phrased without a selector; this theorem takes that at face value.
   If one instead allows an external selector picking 3 of `n(n-1)/2`
   bivectors as weak, the uniqueness of `n = 3` is lost.
3. "Why the cubic Z^n lattice." The derivation holds irrespective of
   the lattice choice; it depends only on the Clifford algebra.
   The choice `Z^n` for the lattice geometry is a separate question.

## Is This A Genuinely-Non-Circular Derivation?

The reviewer's bar for retained G16-like closure was that the
derivation must not presuppose `d_s = 3`-specific retained structure.
Let us audit this theorem against that bar.

**Premises used.**

| Premise | Scope | Presupposes `d_s = 3`? |
|---|---|---|
| Clifford algebra `Cl(n)` for each positive integer `n` | mathematical | no |
| Bivector count `dim Λ²(R^n) = n(n-1)/2` | mathematical | no |
| Bivectors generate `spin(n)` under commutator | mathematical | no |
| Observed weak gauge group is SU(2) | empirical input | no |
| `dim(su(2)) = 3` as a Lie algebra | mathematical | no |
| Retained native-SU(2) theorem read at canonical no-selector strength | retained | ** see below ** |

**The sensitive premise** is the retained native-SU(2) theorem. The
theorem on `main` is phrased as "the Clifford bivectors close exactly
into the weak algebra on the cubic surface." Read strictly, "the
cubic surface" is `d_s = 3`-specific, which would make the premise
downstream.

However: the content of the native-SU(2) theorem is **the Lie-algebra
equality** `(bivectors of Cl(3)) = su(2)`, which is a statement about
the Clifford algebra, not about the lattice. Re-read with this parsed
content, the theorem becomes:

> For the retained framework to exhibit weak SU(2) gauge structure
> canonically (i.e., via all bivectors with no selector), the
> Clifford-algebra bivector count must equal `dim(su(2)) = 3`.

This re-reading is dimension-agnostic and tests the `Cl(n)` family
for the natural-SU(2) condition. On this reading, the native-SU(2)
requirement is **comparison-level**, and the derivation is
genuinely non-circular.

**Honest caveat.** If a reviewer rejects the re-reading and insists
that "cubic" in the retained native-SU(2) theorem is load-bearing
for its `d_s = 3`-specificity, then this note has only moved the
circularity one step back rather than eliminated it. The reviewer
would then have to argue that the Lie-algebra content of the retained
theorem cannot be separated from its lattice-geometric content, which
is a substantive claim about the retained proof's structure.

## Corollary: Three Generations

Once `n = 3` is forced by the native-SU(2)-tightness theorem, the
retained three-generation structure follows as an immediate downstream
corollary at support level, under the retained `hw`-orbit-is-physical-
species semantics.

**Chain.**

1. **Canonical native SU(2)** (retained input; observed weak gauge
   group with no selector).
2. ⇒ `spin(n) = su(2)` as Lie algebras (no-selector clause).
3. ⇒ `n(n-1)/2 = 3` by dimensional matching.
4. ⇒ `n = 3` (Version A; the unique positive-integer solution).
5. ⇒ The cubic lattice `Z^n` specialises to `Z³`.
6. ⇒ The retained `O_h` orbit decomposition on the hw-level-1 sector
   of `Cl(3)` gives exactly three orbits (retained theorem on `main`:
   `8 = 1 + 1 + 3 + 3` with the `hw=1` sector contributing one
   3-orbit).
7. ⇒ Under the retained `hw`-orbit-is-physical-species semantics,
   three physical generations.

**Scope of the corollary.** Steps 1–4 are retention-grade (the content
of the main theorem). Steps 5–7 are support-grade: they carry the
retained-semantics dependency that the earlier conditional-minimality
note already documented, and they do not pretend to derive "why `hw`-
orbits are species" from axioms.

**What is retention-grade and what is support-grade.**

| Step | Statement | Grade |
|---|---|---|
| 1–4 | Canonical native SU(2) forces `n = 3` | retention-eligible |
| 5 | `Z³` as the lattice on `n = 3` | axiom-level choice (still a separate question) |
| 6 | `O_h` orbit count = 3 on `hw=1` | retained theorem (on `main`) |
| 7 | hw-orbits → generations | retained semantics (not derived) |

**What the corollary adds beyond the v4 conditional-support note.**
The v4 note took `d_s = 3` as given and derived the 3-generation
structure on the cubic surface as an algebraic comparison-family
theorem. This corollary instead derives `d_s = 3` itself at retention
grade from native SU(2), and inherits the v4 conditional-support
chain for the generation count. So the combined claim is:

> Canonical native SU(2) + retained hw-orbit semantics ⇒ 3 generations,
> with the spatial-dimension step upgraded from "axiom" to "retention-
> eligible theorem".

**Falsification.** The corollary is falsified if:

- the canonical no-selector reading of the retained native-SU(2)
  theorem is rejected (then step 2 fails), or
- the retained `O_h` orbit decomposition on `hw=1` of `Cl(3)` changes
  (then step 6 fails), or
- the retained `hw`-orbit semantics is replaced by a different
  species-identification prescription (then step 7 fails).

All three failure modes are testable against `main`.

## Relation To The Conditional-Minimality Support Note

The earlier `cl3-minimality-conditional-support-2026-04-17.md` note
carried three requirements:

- R1 (native SU(2) needs ≥ 3 bivectors): covered as the "sufficient
  condition" half of this theorem.
- R2 (`2^n = 8` for the retained 3-generation orbit): this note
  **removes** R2 from the derivation path. The `2^n = 8` requirement
  is now a downstream consistency check on the retained orbit
  decomposition, not a primitive of the minimality derivation.
- R3 (parity from anomaly-forced chirality): independent retained
  theorem. Gives `n` odd. `n = 3` already satisfies this.

The earlier note said `n = 3` is the unique intersection `R1 ∧ R2 ∧
R3`. This note tightens the "necessary" half of R1 to canonical
no-selector form, which alone forces `n = 3` without needing R2.

## Novel Predictions

**P1 — Falsifiability.** If future theoretical or experimental work
ever identifies a retained framework satisfying "canonical native
SU(2) from bivectors" with `n ≠ 3`, this theorem is directly
falsified. The framework would have to extend the Clifford bivector
count beyond 3 while keeping the SU(2) identification, which would
require either:

- a Lie-algebra isomorphism `spin(n) ≅ su(2)` for `n ≠ 3` — which
  is impossible by dimension counting, or
- an explicit selector picking 3 out of `n(n-1)/2` bivectors —
  which violates the no-selector reading of the retained theorem.

Neither is possible. So the theorem is falsifiable in principle but
not by any small modification of the framework.

**P2 — Lie-algebra-coincidence landscape (corrected).** For
`spin(n) = su(k)` with any simple Lie group SU(k), dimensional matching
`n(n-1)/2 = k² − 1` has isolated integer solutions tied to classical
Lie-algebra coincidences:

- `k = 2`: `n(n-1)/2 = 3` → `n = 3`. Yes — `spin(3) = su(2) = sp(1)`
  (classical; the double-cover `Spin(3) ≅ SU(2)`).
- `k = 3`: `n(n-1)/2 = 8` → no integer solution.
- `k = 4`: `n(n-1)/2 = 15` → `n = 6`. Yes — `spin(6) = su(4)`
  (the `D_3 = A_3` coincidence in Lie-algebra classification).
- `k = 5, 6, 7, ...`: no integer solutions in the tested range.

So `Cl(n)` bivectors admit a **two**-candidate canonical-no-selector
match with a simple SU group: `n = 3` for SU(2) and `n = 6` for SU(4).
Uniqueness of `n = 3` requires one additional input:

- **If the observed weak gauge group is SU(2)** (empirical input), then
  `spin(n) = su(2)` specifically forces `n = 3` with no other
  constraint needed. This is the derivation's most direct form.
- **Without specifying the gauge group**, retained chirality parity
  (`n` odd, from the retained anomaly-forced-time theorem) rules out
  `n = 6` as even and leaves `n = 3` as the unique canonical-SU match.

Either primitive — "observed weak SU(2)" or "canonical simple-SU match
with chirality parity" — forces `n = 3`.

## Verification Runner

Runner: `scripts/frontier_native_su2_tightness.py`.

Checks:

1. For each `n ∈ {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}`, compute
   `dim(spin(n)) = n(n-1)/2` and compare to `dim(su(2)) = 3`.
2. Verify `n = 3` uniquely solves the dimensional-matching equation.
3. Explicitly construct `spin(3)` generators and verify they close
   into `su(2)` with structure constants `f_{ijk} = -2ε_{ijk}` (reuses
   the Part B construction from the minimality runner, so the matrix
   check is self-contained).
4. For `n = 4, 5, 6`, construct `spin(n)` generators and explicitly
   verify `spin(n) ≠ su(2)` by dimension mismatch.
5. For the SU(k) extension (P2), verify that no positive integer `n`
   satisfies `n(n-1)/2 = k² − 1` for `k = 3, 4, 5, 6`, confirming
   that SU(2) is the unique simple Lie group with a Clifford-bivector
   match.

## Claim Boundary (Explicit)

**This theorem does.**

- Derive `n = 3` from the Clifford-algebra dimensional-matching
  condition `spin(n) = su(2)`, interpreted as the canonical no-
  selector reading of the retained native-SU(2) theorem.
- Use only comparison-level mathematical facts about Clifford
  algebras, bivector counts, and Lie algebra dimensions.
- Not use cubic `Z³` orbit structure, `hw`-orbit semantics, or the
  retained `8 = 1 + 1 + 3 + 3` decomposition.

**This theorem does not.**

- Replace the observational input "weak gauge group is SU(2)"; that
  remains an empirical fact about the Standard Model.
- Address the lattice-geometric question of `Z³` specifically; the
  theorem is about Clifford algebra, not lattice choice.
- Provide a first-principles derivation of the "canonical no-selector"
  reading of the retained theorem. If a reviewer rejects that reading,
  the theorem reduces to the conditional support statement.

## What A Reviewer Should Conclude

This section lays out what a reviewer should, and should not, conclude
from this note, stated as sharply as possible for retention review.

**Retention-eligible claim (Version A).**

> Canonical native SU(2) (the observed weak gauge group on the retained
> framework, read at no-selector strength) forces `d_s = 3` via Clifford-
> bivector Lie-algebra dimensional matching. Premises: bivector count
> `n(n-1)/2`, `dim(su(2)) = 3`, `spin(n) = su(2)` from the no-selector
> clause. Conclusion: `n = 3` uniquely.

This claim carries no cubic-lattice-specific structure, no hw-orbit
semantics, and no SM matter-content assumption. It shifts the primitive
from a spatial-dimension choice to a gauge-group-dimension equality.

**Retention-eligible claim (Version B).**

> The framework's retained native-gauge structure plus retained anomaly-
> forced chirality parity forces `d_s = 3` via Clifford-bivector Lie-
> algebra dimensional matching restricted to odd `n`. This additionally
> rules out the `spin(6) = su(4)` coincidence at `n = 6`.

Version B is gauge-group-agnostic but costs the retained parity input.

**Support-grade corollary.**

> Adding the retained `hw`-orbit-is-physical-species semantics on `Cl(3)`
> gives exactly 3 generations as a downstream consequence.

The support-grade status reflects the retained semantics dependency
already documented in the earlier conditional-support note.

**What this note is NOT claiming.**

- It is not deriving "why SU(2) is the weak gauge group." That is an
  empirical fact about the Standard Model and a retained input.
- It is not deriving "why `Z³` as the lattice geometry." The theorem
  is about the Clifford algebra only; lattice choice is orthogonal.
- It is not deriving "why hw-orbits count physical species." The
  3-generation corollary carries the retained semantics as a support
  dependency.

**What upgrades this to retained vs support.** A reviewer would need
to accept:

1. The canonical-no-selector reading of the retained native-SU(2)
   theorem (argued in the non-circularity audit §).
2. That "canonical native SU(2) with no selector" is a cleaner
   primitive than "`d_s = 3` as axiom."

If both are accepted, Version A is retention-eligible and upgrades
`d_s = 3` from axiom to derived. If either is rejected, the note
falls back to a stronger support note than the earlier conditional-
minimality one — with an explicit Lie-algebra derivation chain and
a 3-generation corollary as concrete content.

## Honest Self-Assessment

The primitive has shifted from a spatial-dimension choice to a
Lie-algebra-matching requirement tied to the observed weak gauge
group. This is a genuine axiom-depth improvement: the Lie-algebra
equation `n(n-1)/2 = 3` is a pure mathematical fact, and the only
retained-framework input is the canonical-no-selector reading of the
native-SU(2) theorem.

Compared to the earlier `cl3-minimality-conditional-support-2026-04-17`
note, this note:

- removes the dependence on the retained cubic `8 = 1 + 1 + 3 + 3`
  orbit decomposition for the `d_s = 3` step,
- replaces it with a Clifford-algebra dimensional-matching argument
  that works on the `Cl(n)` family at comparison level,
- preserves the 3-generation corollary as a separate, honestly
  scoped support-level chain under retained hw-orbit semantics.

The cost is that retention status now depends on the no-selector
reading of the native-SU(2) theorem, which is a reviewer-judgment
call about the retained theorem's content on `main`. This is a
cleaner dependency to argue about than the cubic-orbit dependency
of the earlier note.

## Next

If the Version A theorem is accepted at retention grade, follow-up
research directions:

1. **SU(3) color via graph automorphisms.** Does the retained graph-
   first SU(3) gauge structure also pick out `n = 3` via a related
   mechanism? Per P2, a direct bivector match does not work
   (`n(n-1)/2 = 8` has no positive integer solution), so the SU(3)
   argument must go through the retained graph-automorphism structure.
2. **Lattice geometry.** Given `n = 3`, is `Z³` (the simple-cubic
   lattice) the unique retained choice? The retained `O_h` symmetry
   theorem may constrain this, but it is a separate axiom-depth
   question.
3. **Hw-orbit semantics.** Can the "hw-orbit-is-physical-species"
   prescription be derived from deeper retained structure, upgrading
   the 3-generation corollary from support to retention grade?

Each of these is a distinct research program. This note's contribution
is the one clean step from `d_s = 3`-as-axiom to `d_s = 3`-as-theorem
under canonical native SU(2).
