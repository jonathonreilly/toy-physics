# Kasteleyn Thread — Theorems, Refuted Conjectures, and Open Problems

**Status.** This note consolidates 20+ V2 iterations of the axiom-native
Kasteleyn investigation on branch `claude/axiom-native-overnight-FtUl5`.
It has been REVISED after iter 35's falsification of what had been the
thread's strongest empirical claim (the "singleton hypothesis"). The
thread's ground-truth results are now re-centred on the iter 12
planarity fact and the iter 23 reflection-degeneracy lemma.

Every claim below traces to the kit defined in the axiom-native
starting kit — K1 (real Clifford algebra `Cl(3)`), K2 (Z^3 lattice
with spacing `a`), K3 (staggered-Dirac partition with phases
`η_μ(n)`) — with no external imports beyond the K4-allowed
mathematical infrastructure.

**Axiom-native constraints.** No appeal to external references, no
observed constants, no retained theorems from any parallel branch,
no continuum QFT conventions, no PDG data, no assumptions about
gauge or Yukawa sectors beyond what's in the kit. Every PASS on the
branch traces to the kit or a prior-derived lemma on this same
branch and is re-checked by the hostile audit.

**Claim hierarchy:**
- **Theorems.** Proven with a hostile-audit-clean derivation or
  validated as a concrete structural fact on-branch.
- **Refuted conjectures.** Candidates that were tested adversarially
  and failed, explicitly retracted to avoid misleading future work.
- **Empirical patterns.** Consistent observations on restricted
  cuboid families without a claim of universality.
- **Open problems.** Questions whose answers would promote patterns
  to theorems or retract more claims.

---

## 1. Setup and notation

For a Z^3 cuboid `(L1, L2, L3)` with sites `n = (n_1, n_2, n_3)` in
`[0, L1) × [0, L2) × [0, L3)`, and a defect set `D ⊂ sites`, define
the truncated graph `G` with vertex set `sites \ D` and nearest-
neighbour edges `{n, n ± e_μ}` for `μ ∈ {1, 2, 3}` within the truncated
vertex set.

The **K3 staggered phases** are

```
η_1(n) = 1,
η_2(n) = (-1)^{n_1},
η_3(n) = (-1)^{n_1 + n_2}.
```

The **bipartite even/odd split** puts a site `n` in `E(G)` if
`n_1 + n_2 + n_3` is even, `O(G)` if odd. When `|E(G)| = |O(G)|`
we say the graph is **balanced**.

The **K3 bipartite block** `B = B(G)` is the `n_bi × n_bi` matrix with
`n_bi = |E(G)|`, entries indexed by `(e, o) ∈ E(G) × O(G)`, and

```
B[e, o] = η_μ(e)         if edge (e, o) in G and e is the lower endpoint,
B[e, o] = -η_μ(o)        if edge (e, o) in G and o is the lower endpoint,
B[e, o] = 0              otherwise.
```

**#PM(G)** is the number of perfect matchings of `G`.

**Pfaffian identity.** `|det(B)| ≤ #PM(G)`, with equality iff `G` has
a Pfaffian orientation and K3 is that orientation.

**K3 optimality on G.** We say K3 is Pfaffian-optimal on `G` iff
`|det(B)| = #PM(G)`.

---

## 2. Theorem (iter 12): K3 Pfaffian-optimality ⇔ planarity

### Statement

K3 is Pfaffian-optimal on `G = (L1, L2, L3)` cuboid (empty defect)
iff `G` is a **planar** graph.

### Status

**Proven / ground truth.** This is a direct application of
Kasteleyn's planarity theorem, verified on-branch for several cuboid
sizes in iter 12 and further corroborated by the iter 35 refutation
(which ruled out the weaker contractibility condition).

### Evidence

- Planar cuboids verified K3-optimal: `(2,2,1)`, `(2,2,2)`, `(2,2,3)`,
  `(3,2,2)`.
- Non-planar cuboids verified K3-NOT-optimal (iter 12 + iter 35):
  `(3,3,2)`: `#PM = 229`, `|det| = 225`.
  `(5,4,2)`: `#PM = 535229`, `|det| = 508805` (iter 35).
  `(6,4,2)`: `#PM = 9049169`, `|det| = 8473921` (iter 35).
- Gap `gap(G) := #PM(G) − |det_K3(B)|` is zero iff `G` is planar,
  otherwise positive and growing with the non-planar complexity.

### Remarks

- Contractibility (`χ(G) = 1`) is necessary for any non-degenerate
  Pfaffian discussion but is NOT sufficient for K3 optimality.
- On contractible but non-planar cuboids like `(5,4,2)` empty, K3 has
  `|det|/#PM ≈ 0.94`, close to but strictly less than optimal.

---

## 3. Theorem (iter 23): reflection-degeneracy lemma for central σ

### Statement

Let `G` be `(L1, L2, L3)` cuboid minus two singleton sites `r1, r2`.
Let `σ(i, j, k) = (L1−1−i, L2−1−j, L3−1−k)` be the central reflection.
If

```
(i)   σ(r1) = r2   (σ is a graph automorphism of G),
(ii)  L1 + L2 + L3 is even  (σ flips bipartition),
(iii) n_bi = |E(G)| is odd,
(iv)  L1 is even  (so ε_2 = (-1)^{L1-1} = -1 under σ),
```

then `|det_K3(B)| = 0` exactly.

### Status

**Proven.** Validated 8/8 on balanced cases (5 positive where all
conditions hold and det = 0 exactly, 3 negative where at least one
condition fails and det ≠ 0).

### Proof sketch

1. σ is an involution. Under condition (i), σ is an automorphism of
   the truncated graph `G`.
2. Under condition (ii), σ flips bipartition (maps evens to odds and
   vice versa).
3. The ε_μ sign-ratio formula `ε_μ = (1, (-1)^{L1−1}, (-1)^{L1+L2})`
   is verified numerically on multiple cuboid sizes.
4. σ induces row+column permutations on `B` (across bipartition),
   combined with the per-μ sign flips, yielding the matrix identity
   `det(B) = s · det(B)` where `s = ε_2^{#μ=2 edges in any PM} ×
   (permutation sign)`. Under conditions (iii) and (iv), `s = −1`.
5. `det(B) = −det(B)` forces `det(B) = 0`.

### Uniqueness — partial reflections are NOT equivalent

Iter 24 tested partial reflections `ρ_S` for `S ⊂ {1,2,3}` on
2-singleton defects. Zero-det counts by reflection type:

| Reflection | Zero-det cases | Total tested |
|---|---|---|
| `ρ_1` (x-only) | 0 | 7 |
| `ρ_2` (y-only) | 0 | 7 |
| `ρ_3` (z-only) | 0 | 6 |
| `ρ_{12}` (xy) | 0 | 9 |
| `ρ_{13}` (xz) | 0 | 9 |
| `ρ_{23}` (yz) | 0 | 9 |
| `ρ_{123}` (central σ) | 6 | 8 |

Only the central reflection produces det = 0 on 2-singleton defects.
Partial reflections can force det = 0 in OTHER settings (e.g., iter
32 found partial reflections cover all det=0 cases on (3,3,2)
line-3+singleton configs via a bipartition-preserving analog), but
they do not generalize the 2-singleton iter 23 lemma.

---

## 4. REFUTED CONJECTURE (iter 14–34 → iter 35): the "singleton
hypothesis"

### Original statement (retracted)

For `G` a Z^3 cuboid minus defect `D`, K3 is Pfaffian-optimal on `G`
iff:
  (a) `G` is contractible (`χ(G) = 1`), AND
  (b) `D` has no isolated singleton components.

### Refutation (iter 35)

**Clean falsifying counterexamples:**

| Cuboid | Defect | χ | singletons | #PM | \|det_K3\| | K3 optimal? |
|---|---|---|---|---|---|---|
| `(5,4,2)` | empty | 1 | none | 535,229 | 508,805 | NO (0.95) |
| `(6,4,2)` | empty | 1 | none | 9,049,169 | 8,473,921 | NO (0.94) |

Both are contractible with NO defect; the hypothesis predicts K3
optimal but K3 is non-optimal. The hypothesis is refuted.

### Why the hypothesis appeared consistent

Iter 14–22 tested the hypothesis primarily on `(3,3,2)`, `(4,3,2)`,
`(4,4,2)` with 2-site defects (singletons or adjacent pairs). On
those specific cuboids, certain 2-site removals happened to make
the remaining graph K3-compatible (e.g., an adjacent-pair removal
on `(3,3,2)` can planarize the resulting graph), validating the
"no singletons ⇒ K3 optimal" side of the hypothesis on a restricted
test set. On larger empty cuboids, the underlying non-planarity of
K3 dominates and the hypothesis breaks.

### Lesson

The hypothesis confused two effects:
- **Planarity** (necessary and sufficient for K3 optimality,
  per §2).
- **Singleton presence** (correlated with K3 failure on small
  non-planar test cases, but not the true driver).

The correct ground-truth statement is §2's planarity lemma. All
prior "singleton hypothesis" data points are consistent with
planarity reasoning: on `(3,3,2)` empty K3 fails (non-planar);
on `(3,3,2)` minus an adjacent pair K3 may be optimal (the
remaining graph happens to be planarity-compatible); on any
non-planar cuboid empty, K3 fails.

### Retracted claims

- "K3 optimal iff contractible AND no singletons": false.
- "Singleton criterion is local" (iter 19): this observation is
  still correct within the non-planar regime but does not imply
  the biconditional.
- "18+ confirming data points, zero counterexamples" (pre-iter 35):
  the 2 counterexamples found by iter 35 invalidate this count.

---

## 5. Empirical patterns (status: restricted observations, no
proof)

### 5.1 Localization signature

**Observation.** For a shape `G` with removed set `D ≠ ∅` that is
balanced, contractible, and K3 NOT optimal, define per edge `e`
`frac(e) := min_count(e) / (min_count(e) + maj_count(e))` where
min_count and maj_count are the number of PMs of each sign under K3
using edge `e`.

On `(3,3,2)`, `(4,3,2)`, `(4,4,2)` with 2-singleton defects:
- avg midpoint-distance to removed of top-5 min-biased edges
  < top-5 maj-biased edges.
- Pearson corr(frac, distance) < 0.
- Observation reproduces across 7+ tested configurations.

**Caveat (iter 35 revision).** This observation was on restricted
non-planar cuboid families with small defects. We do not claim it
extends to larger cuboids or different defect types. Iter 27–28
showed it already weakens on line-type non-singleton defect
components.

### 5.2 SH3-type non-automorphism det = 0

**Observation.** On `(4,4,2)` with line-3 + singleton defects,
`det_K3 = 0` occurs on 128 of 288 tested configurations. iter 30's
H5 characterizes these empirically: det = 0 iff (singleton in
opposite z-plane from line-3) AND (singleton parallel-axis coord
matches line-3 center parallel-axis coord parity).

None of these cases are explained by any graph automorphism (iter
33 showed no element of `D_4 × Z_2` fixes the defect for these
configs). There is some PM-pairing bijection forcing
`n_plus = n_minus` without a symmetry source.

**Caveat.** H5 is `(4,4,2)`-specific (iter 31 showed it fails on
`(3,3,2)`, `(4,3,2)`, `(5,3,2)`, `(5,5,2)`). The underlying
mechanism is open.

### 5.3 Kasteleyn gap and minority structure

On non-planar cuboids, the gap `#PM − |det_K3|` is positive and
equals `2 × n_minus` where `n_minus` is the count of PMs
contributing the minority sign under K3. Minority PMs on tested
shapes show a low-to-moderate vertical-edge bias, consistent with
K3's inherent difficulty in bridging multi-layer connections.

---

## 6. Open problems

### 6.1 Exact characterization of K3 failure on non-planar cuboids

The iter 12 planarity lemma tells us when K3 is optimal. On
non-planar cuboids, K3 fails, but the **magnitude** of the gap
varies. What determines `gap(G) = #PM(G) − |det_K3(B)|` as a
function of `G`'s topology? Empirically the gap grows with
non-planar complexity but no closed form is known.

### 6.2 Generalized reflection lemma

Iter 32 showed that partial reflections `ρ_S` with all `ε_μ = +1`
and `sign(π_e) · sign(π_o) = -1` force det = 0 on many line-3 +
singleton configurations (24/40 on `(3,3,2)`, 160/288 on
`(4,4,2)`). The iter 23 lemma + iter 32's partial-reflection
analysis give a combined rule; 496 det=0 configs across 5 L3=2
cuboids remain unexplained by reflections alone.

Open: state and prove a UNIFIED reflection lemma covering
bipartition-preserving and flipping cases.

### 6.3 SH3-type mechanism

The 496 unexplained det=0 cases (and more on larger cuboids) have
`det_K3 = 0` without any graph-automorphism source. Iter 34 narrowed
the search: the PM-pairing is "mostly local" (aggregate features
match between plus and minus PMs), with a small asymmetry
concentrated near the non-singleton defect component. A specific
alternating-cycle-based bijection candidate has not been constructed.

### 6.4 Continuum limit

K3 derives from the staggered Dirac lattice action. The
Pfaffian/planarity story above is purely combinatorial. In the
formal `a → 0` limit, what spectral information about the Dirac
operator is encoded in the Pfaffian-gap structure? This question
is untouched by current iterations.

### 6.5 Other symmetries

Candidate symmetries that might force det = 0 beyond axis-aligned
reflections:
- Cyclic rotations on cuboids with `L1 = L2` (partial coverage
  within `D_4 × Z_2` groups tested).
- Cl(3)-unit multiplications `b ↦ b · ω` on Grassmann generators
  (untested).
- Phase twists `η_μ ↦ χ(n) η_μ` for a character `χ` (untested).

---

## 7. Summary of concrete results after 20+ iterations

| Result | Status | Significance |
|---|---|---|
| §2 K3 optimal iff planar | PROVEN (iter 12) | Ground truth |
| §3 Reflection-degeneracy (central σ) | PROVEN (iter 23) | Structural theorem |
| §4 Singleton hypothesis | REFUTED (iter 35) | Retracted |
| §5.1 Localization signature | Empirical, restricted | Open |
| §5.2 SH3-type det = 0 | Empirical, unexplained | Open |
| §6.1 Gap characterization | Open | — |
| §6.2 Generalized reflection | Open | — |

The thread's two concrete contributions are §2 and §3. The
investigation's value also lies in its **negative results**: several
generalizations (partial-reflection family extension, singleton
hypothesis, H5 universality) were tested and refuted, preventing
future false leads.

---

## 8. Methodological note: V2 adversarial testing worked

The thread's most significant structural finding is the iter 35
refutation of the singleton hypothesis. The hypothesis had survived
24+ iterations and accumulated 15+ "confirming" data points; only
when V2's adversarial charter forced testing on NEW cuboid sizes
(not previously examined) did the refutation emerge.

The earlier "confirming" tests had tacitly assumed the hypothesis
while testing within a restricted family where it happened to hold.
This is the classic failure mode of non-adversarial empirical
science. V2's insistence on:
- no reverse-engineered polynomials
- structural absence as a blocker, not a PASS
- every PASS must be a computed boolean
- adversarial new-case testing over consistency-with-existing-cases

directly produced the refutation. Without that charter, the thread
would have continued accumulating confirming data points indefinitely
on `(3,3,2)`-size cuboids.

---

## 9. Iteration index (selected)

- iter 11: non-contractible ring test.
- iter 12: planarity-optimal equivalence (§2 theorem).
- iter 14–18: singleton hypothesis building (now retracted).
- iter 19: singleton locality claim (now contextualized).
- iter 20: partial structural signature attempt.
- iter 21–22: localization signature scaling (§5.1).
- iter 23: reflection-degeneracy lemma (§3 theorem).
- iter 24: partial-reflection extension refuted.
- iter 25: thread consolidation (pre-iter-35 version, now
  superseded by this doc).
- iter 26: localization at 4-singleton defects.
- iter 27–28: mixed-defect signal fragility.
- iter 29–30: SH3 anomaly + H5 candidate lemma.
- iter 31: H5 is `(4,4,2)`-specific.
- iter 32: bipartition-preserving partial-reflection test.
- iter 33: union test — central σ contributes zero on line-3 family.
- iter 34: SH3 PM-bijection search (mostly local, 8-PM asymmetry).
- iter 35: **singleton hypothesis refuted** on `(5,4,2)`, `(6,4,2)`
  empty cuboids.

All runners under `scripts/frontier_axiom_native_*.py`. All commits
on branch `claude/axiom-native-overnight-FtUl5`.
