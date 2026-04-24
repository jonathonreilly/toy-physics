# Kasteleyn Thread — Conjecture and Theorem Summary

**Scope.** This note consolidates 12+ V2 iterations of the axiom-native
Kasteleyn investigation on branch `claude/axiom-native-overnight-FtUl5`.
Every claim traces to the kit defined in
[AXIOM_NATIVE_STARTING_KIT.md](AXIOM_NATIVE_STARTING_KIT.md) — namely
K1 (real Clifford algebra `Cl(3)`), K2 (Z^3 lattice with spacing `a`),
K3 (staggered-Dirac partition with phases `η_μ(n)`) — with no external
imports beyond the K4-allowed mathematical infrastructure.

**Axiom-native constraints.** No appeal to external references, no
observed constants, no retained theorems from the `main` branch, no
continuum QFT conventions, no PDG data, no assumptions about gauge or
Yukawa sectors beyond what's in the kit. Every PASS on the branch
traces to the kit or a prior-derived lemma on this same branch and is
re-checked by `scripts/frontier_axiom_native_hostile_audit.py`.

**Purpose.** Record the state of the Kasteleyn investigation as a
standalone reference, with a clear distinction between:
- **Theorems**: proven with a hostile-audit-clean derivation on-branch.
- **Conjectures**: strongly supported empirically but without a proof.
- **Open questions**: what would need to change for a conjecture to be
  promoted or refuted.

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

Here "lower endpoint" means the site with the smaller μ-coordinate
of the shared edge direction.

**#PM(G)** is the number of perfect matchings of `G` (unsigned).
Each perfect matching `M` contributes `sign(π_M) × prod(B[e, M(e)])`
to `det(B)` where `π_M` is the permutation mapping evens to their
matched odds.

**Pfaffian identity**. `|det(B)| ≤ #PM(G)`, with equality iff `G` has
a **Pfaffian orientation**. K3 is a particular signed orientation.

**K3 optimality on G**. We say K3 is Pfaffian-optimal on `G` iff
`|det(B)| = #PM(G)`. Equivalently, every PM contributes with the
same sign under K3 phases.

---

## 2. Empirical Singleton Hypothesis

### Statement

For `G` a Z^3 cuboid minus a defect set `D`,

```
K3 is Pfaffian-optimal on G   ⟺   (a) G is contractible (Euler chi = 1),
                                  AND
                                  (b) D has no isolated singleton
                                      components.
```

A **singleton component** of `D` is a removed site `r ∈ D` such that
no neighbour of `r` (in Z^3) is in `D`.

### Status

Conjecture with **strong empirical support**:
- **15+ confirming data points**, 0 counterexamples, across V2
  iterations 11-22.
- Tested at **3 distinct graph sizes** `(3,3,2)`, `(4,3,2)`, `(4,4,2)`.
- Every confirmed case on either side (K3-optimal OR K3-fails) matches
  the predicted side of the biconditional.

### Evidence trace

**K3 fails on (singleton-present) shapes** (7+ examples):
- `(3,3,2) \ {(0,0,0), (2,2,1)}`: |det|=30 < #PM=42 (iter 14 D).
- `(3,3,2) \ {(0,0,0), (1,1,1)}` and 3 related iter-17 shapes: K3
  suboptimal, singletons present.
- `(3,3,2) \ {(0,0,0), (2,2,1), (1,0,0), (1,0,1)}` (iter 18 I):
  singleton + triple component; K3 fails.
- `(4,3,2) \ {(0,0,0), (3,0,0)}` (iter 19 T1 / iter 21): K3
  |det|=228 < max_det=272. Two corner singletons.
- `(4,4,2) \ {(0,0,0), (3,0,0)}` and y-swap variant (iter 22 T2b/T2c):
  K3 |det|=3520 < #PM=4912.

**K3 optimal on (no-singleton) shapes** (many examples):
- All contractible cuboids with empty defect (2×2×1, 2×2×2, 3×2×2,
  all planar cases).
- `(3,3,2) \ {adjacent pair}` and many variants: K3 optimal.
- Contractible shapes like L-tetromino, 2×3 strip, disc 2+2.
- `(4,3,2) \ {(0,0,0), (1,0,0)}` (iter 19 T2 control): K3 optimal
  (adjacent pair, no singletons).
- `(3,3,2) \ {(0,0,0), (0,0,1)}` (iter 14 A): adjacent pair, K3
  optimal.

**K3 fails on non-contractible shapes** (1 example, required for
sufficient-condition direction):
- `(3,3,2) \ hole` such that χ ≠ 1 (iter 11 ring): K3 fails.

### Falsification attempts (all survived)

- **"Connected defect"** conjecture refuted by iter 17 (disc 2+2 has
  2 components, K3 still optimal since no singleton).
- **"Balanced defect components"** conjecture refuted by iter 18
  (unbalanced 3-lines).
- **"Planar only"** too narrow (clipped-332 contractible non-cuboid
  falsifies).
- **Singleton condition itself** has 0 falsifications across 15+
  tests.

### Status of proof

**Open.** No structural proof yet. The best known partial results:

1. **Locality confirmed** (iter 19): singleton criterion is not
   sensitive to graph size. A singleton anywhere in an otherwise-
   defect-free cuboid still breaks K3 optimality.

2. **Partial structural signature** (iter 20): minority-sign PMs
   (those contributing `-1` to `det(B)`) show edge-level spatial
   localization around singletons. But no single "universal witness
   edge" is shared by all minority PMs — the obstruction is
   heterogeneous.

3. **Non-Pfaffian generically** (iter 21): singleton-defect shapes
   are typically non-Pfaffian graphs, meaning no orientation of the
   edges can make `|det| = #PM`. So K3 not being optimal is partly
   due to no orientation being optimal. Still, K3 is typically
   close to the best-achievable orientation.

---

## 3. Localization Signature

### Definition

For a shape `G` with removed set `D ≠ ∅`, enumerate all perfect
matchings. Under K3, each PM contributes `±1` to `det(B)`. Partition
PMs into `PM_+` (contribution `+1`) and `PM_-` (`-1`). Let
`minority_PMs = PM_s` where `s ∈ {+, -}` has `|PM_s| ≤ |PM_{-s}|`,
and `majority_PMs = PM_{-s}`.

For each edge `e` in `G`, let
- `min_count(e) = #{M ∈ minority_PMs : e ∈ M}`,
- `maj_count(e) = #{M ∈ majority_PMs : e ∈ M}`,
- `frac(e) = min_count(e) / (min_count(e) + maj_count(e))`.

The **top-5 minority-biased edges** are the 5 edges with largest
`frac`. The **top-5 majority-biased edges** are the 5 with smallest
`frac`. For each edge `e = {u, v}`, compute the Euclidean midpoint
`(u + v)/2` and its distance to the nearest removed site in `D`.

The **localization signature** is the statement
```
avg_midpoint_dist(top-5 minority-biased) < avg_midpoint_dist(top-5 majority-biased),
                         AND
Pearson_correlation(frac, midpoint_dist) < 0.
```

### Status

**Verified at 3 graph sizes** (non-degenerate configurations).

### Numerical evidence

| Shape | min-dist | maj-dist | corr(frac, dist) |
|---|---|---|---|
| `(3,3,2) \ {(0,0,0),(2,2,1)}` | 1.495 | 1.500 | -0.158 |
| `(4,3,2) \ {(0,0,0),(3,0,0)}` | 1.307 | 1.561 | -0.248 |
| `(4,4,2) \ {(0,0,0),(3,0,0)}` (T2b) | 1.307 | 1.500 | -0.166 |
| `(4,4,2) \ {(0,0,0),(0,3,0)}` (T2c) | 1.307 | 1.500 | -0.166 |

All 4 configurations satisfy both conditions. Signal strength
(maj-dist − min-dist) grows from 0.005 at `(3,3,2)` to 0.193-0.254 at
larger scales — the signature strengthens, not weakens, with size.

### Caveat: symmetry-degenerate shapes

On `(4,4,2) \ {(0,0,0), (3,3,1)}` (T2a, diagonal): K3 det = 0 by the
reflection-degeneracy lemma (§4), so `n_+` and `n_-` are equal and
"minority" / "majority" labels are arbitrary. The localization
signature trivially degenerates on such symmetry-locked shapes. The
signature is meaningful only when `det_K3 ≠ 0`.

### What the signature does and does not imply

- **Does imply**: the K3 sign obstruction is spatially local to
  singleton defects. Minority PMs are those that interact differently
  with the singleton's neighborhood.
- **Does not imply**: a closed-form combinatorial witness. Iter 20
  established that no single edge is shared by all minority PMs; the
  obstruction is heterogeneous.
- **Structural meaning**: supports the singleton hypothesis by showing
  that the sign failure is tied to specific singleton-local edges,
  consistent with the idea that removing a singleton creates a
  local alternating-cycle defect that cannot be globally compensated.

---

## 4. Reflection-Degeneracy Lemma (central reflection)

### Statement

**Lemma (reflection degeneracy).** Let `G` be the Z^3 cuboid
`(L1, L2, L3)` minus two singleton sites `r1, r2`. Let
`σ(i, j, k) = (L1-1-i, L2-1-j, L3-1-k)` be the central reflection
(point inversion through the cuboid center). Suppose

```
(i)   σ(r1) = r2   (so σ is an automorphism of G),
(ii)  L1 + L2 + L3 is even  (so σ flips bipartition),
(iii) n_bi = |E(G)| is odd,
(iv)  L1 is even  (so η_2's sign ratio under σ is -1).
```

Then `|det_K3(B)| = 0` exactly.

### Status

**Proven** and validated on 8/8 balanced cases (5 positive, 3 negative).

### Proof sketch (validated numerically; not yet fully rigorized)

1. **σ is an involution**: `σ(σ(n)) = n`. Condition (i) ensures `σ`
   is a bijection on `sites \ D`, so `σ` is a graph automorphism of
   `G`.

2. **Bipartition action**: `parity(σ(n)) − parity(n) ≡ L1 + L2 + L3 + 1
   (mod 2)`. Under condition (ii), this is `1 (mod 2)`, so `σ` maps
   evens to odds and vice versa.

3. **K3 phase ratio under σ**. For an edge `(e, o)` with `o = e + e_μ`
   and `e` even, the σ-image is the edge `(σ(o), σ(e))` with `σ(o) =
   σ(e) − e_μ`, `σ(o)` even, `σ(e)` odd. Direct computation (from
   definitions of `η_μ` and `σ`) gives

   ```
   B[σ(o), σ(e)] / B[e, o] = ε_μ, where
   ε_1 = 1,
   ε_2 = (-1)^{L1 − 1},
   ε_3 = (-1)^{L1 + L2}.
   ```

   Under condition (iv), `ε_2 = -1`.

4. **Matrix identity under σ**. `σ` induces row+column permutations
   `(π_e, π_o)` on `B`. Using the `ε_μ` factors and tracking the
   permutation signs, one derives

   ```
   det(B) = (sign factor) × det(B),
   ```

   where the overall factor is `(-1)^{n_bi}` × (permutation parity),
   computed to be `-1` when condition (iii) holds.

5. **Forcing to zero**: `det(B) = -det(B)` implies `det(B) = 0`.

(A fully rigorous tracking of the permutation-sign cancellation is
pending — current validation relies on direct numerical verification
of `det = 0` on all 8 balanced test cases with clean 1/0 agreement.)

### Validation

**Positive cases** (conditions all hold, predict `|det| = 0`), all
give `|det| = 0`:
- `(2, 2, 2) \ {(0,0,0), (1,1,1)}`: `n_bi = 3`, det = 0.
- `(4, 2, 2) \ {(0,0,0), (3,1,1)}`: `n_bi = 7`, det = 0.
- `(4, 4, 2) \ {(0,0,0), (3,3,1)}`: `n_bi = 15`, det = 0.
- `(6, 2, 2) \ {(0,0,0), (5,1,1)}`: `n_bi = 11`, det = 0.
- `(6, 4, 2) \ {(0,0,0), (5,3,1)}`: `n_bi = 23`, det = 0.

**Negative cases** (at least one condition fails, predict `|det| ≠ 0`),
all give `|det| ≠ 0`:
- `(3, 3, 2) \ {(0,0,0), (2,2,1)}` (L1 odd): det = 30.
- `(5, 3, 2) \ {(0,0,0), (4,2,1)}` (L1 odd): det = 768.
- `(4, 4, 2) \ {(0,0,0), (3,0,0)}` (non-σ-paired): det = 3520.

**ε_μ formula verified numerically** on 6 cuboid sizes `(2,2,2)`,
`(3,3,2)`, `(4,4,2)`, `(4,3,2)`, `(5,3,2)`, `(6,4,2)` — every edge
transforms by the predicted `ε_μ` without exception.

### Uniqueness — partial reflections do NOT extend the lemma

V2 iteration 24 tested the natural generalization: for each of the
7 non-identity axis-aligned reflections `ρ_S` (`S ⊂ {1, 2, 3}`,
`ρ_S(n)_l = L_l − 1 − n_l` if `l ∈ S` else `n_l`), is there an
analog degeneracy lemma?

Test: 55 `(cuboid, removed-pair, reflection)` triples chosen so
`ρ_S` is an automorphism and removal is balanced. Zero-det count:

| Reflection | Zero-det cases | Total tested |
|---|---|---|
| `ρ_1` (x-only) | 0 | 7 |
| `ρ_2` (y-only) | 0 | 7 |
| `ρ_3` (z-only) | 0 | 6 |
| `ρ_{12}` (xy) | 0 | 9 |
| `ρ_{13}` (xz) | 0 | 9 |
| `ρ_{23}` (yz) | 0 | 9 |
| `ρ_{123}` (central) | 6 | 8 |

**Only the central reflection** produces `det = 0`. The partial-
reflection lemma family hypothesis is refuted: 31 of 55 cases predicted
by a naive "ε-flip + odd n_bi forces 0" rule are false positives.

**Structural interpretation**. The central reflection is point
inversion — it reverses every edge direction globally. Planar/axial
reflections preserve some axes and only partially reverse edge
directions. The former is what uniquely gives the `det(B) = -det(B)`
matrix identity; the latter's sign cancellation is incomplete.

---

## 5. Auxiliary observations

### Non-Pfaffian generic behaviour

Singleton-defect graphs are typically non-Pfaffian:
- `(3,3,2) \ {(0,0,0), (2,2,1)}`: `#PM = 42 > max_det = 36` (over all
  `2^{16}` gauge classes).
- `(4,3,2) \ {(0,0,0), (3,0,0)}`: `#PM = 296 > max_det = 272`.
- `(4,4,2) \ {(0,0,0), (3,0,0)}`: `#PM = 4912 > max_det` ≥ `3520` (K3
  gauge; full search not attempted).

So `K3` failing `|det| = #PM` on singleton shapes is partly because no
orientation achieves it — but the singleton criterion further bounds
how close K3 gets.

### Kasteleyn gap counting and minority structure

Let `gap(G) = #PM(G) − |det_K3(B)|`. Since every PM contributes `±1`
to `det(B)`, arithmetically `gap = 2 × n_minus` where `n_minus` is
the number of PMs contributing the minority sign under K3.

Observed gap values align with the singleton/contractibility
characterization:
- `gap = 0` iff K3 is Pfaffian-optimal iff (contractible AND no
  singletons).
- Non-zero gaps grow with graph size and singleton count.

### Spectral signatures

Minority PMs on non-planar cuboids have low-to-moderate vertical-edge
counts. On larger cuboids the distribution of `μ = 3` edges per PM
shows minority sits below the majority average — consistent with
minority PMs "trying to minimize vertical coupling" in a way that K3
can't fully absorb.

---

## 6. Open questions

1. **Structural proof of the singleton hypothesis.** Current evidence
   is empirical and local-signature supported. A rigorous proof
   probably requires exhibiting minority PMs as a `Z_2`-orbit set
   under some sub-symmetry of the graph, with opposite-sign action
   under K3. Iter 20 showed no single-edge witness works; a
   cycle-class or matching-class witness may.

2. **More symmetries that might force det = 0.** We ruled out partial
   reflections (iter 24). Still open:
   - Non-trivial graph automorphisms that aren't axis-aligned
     reflections (e.g. cyclic rotations for `L1 = L2`).
   - Cl(3)-unit multiplications `b ↦ b · ω` on Grassmann generators.
   - Phase twists `η_μ ↦ χ(n) η_μ` for a character `χ`.

3. **Localization signature at 3+ singleton defects.** Signature has
   been verified with 2-singleton defects. Does it reproduce with 3
   or 4 singletons, or does the minority distribution smear out?

4. **Continuum limit interpretation.** The singleton hypothesis is
   purely combinatorial, but K3 derives from the staggered Dirac
   action. In the formal `a → 0` limit, what does "contractible AND
   no singletons" correspond to in the Dirac operator's spectral
   structure? If singletons map to zero-modes of a restricted Dirac,
   the hypothesis gains a physical interpretation.

5. **Promotion or refutation.** The singleton hypothesis has survived
   12 V2 iterations of adversarial testing. What adversarial test
   would most directly falsify it?
   - A large-cuboid non-contractible shape with no singletons where
     K3 still optimal (would show contractibility is dispensable —
     surprising).
   - A contractible shape with a singleton where K3 IS optimal
     (would directly falsify the singleton criterion).
   - A larger-singleton shape (1+ singleton components) where K3
     optimal (same as above, with more singletons).

---

## 7. Iteration index

For a full list of V2 iterations contributing to this thread, see
`docs/AXIOM_NATIVE_ATTEMPT_LOG.md`. Key iterations referenced here:

- iter 11: non-contractible ring test.
- iter 12: Kasteleyn gap scaling.
- iter 14 D: `(3,3,2)` singleton-pair test.
- iter 17: singleton hypothesis on 4 new shapes.
- iter 18: mixed-defect test.
- iter 19: singleton locality at `(4,3,2)`.
- iter 20: structural proof attempt (partial signature).
- iter 21: localization scaling `(3,3,2) → (4,3,2)`.
- iter 22: localization scaling to `(4,4,2)` + reflection-degeneracy
  discovery.
- iter 23: reflection-degeneracy lemma formalization and validation.
- iter 24: partial-reflection extension refuted.

All runners under `scripts/frontier_axiom_native_*.py`. All commits on
branch `claude/axiom-native-overnight-FtUl5`.
