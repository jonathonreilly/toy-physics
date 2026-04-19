# G5 Variational Koide-Cone Note (Avenue H)

**Date:** 2026-04-17
**Status:** structural symbolic attempt on gap `G5` (charged-lepton mass
hierarchy) via a retained-variational-principle attack distinct from the
Agent 5 character-symmetry chain. Verdict:
`VARIATIONAL_KOIDE_DERIVED = PARTIAL`. One candidate (H-2,
real-irrep-block-democracy entropy) produces the Koide 45 deg cone as its
unique stationary point but relies on a weighting choice that is NOT
currently a retained authority. The three other candidates (H-1 CS
midpoint, H-3 Legendre midpoint of `log|det(D+J)|`, H-4 Fisher-Rao
midpoint on the mass simplex) each fail. The named missing primitive is
**real-irrep-block democracy** — a retained principle that weights the
1D trivial-character block and the 2D nontrivial-character block equally
(one entropy log per real-irrep block, independent of block dimension).
**Script:** [`scripts/frontier_g5_variational_koide_cone.py`](../scripts/frontier_g5_variational_koide_cone.py)
 — **22 PASS / 0 FAIL**.
**Authority role:** structural-attempt attack-surface note for gap `G5`,
Avenue H. Does not close G5. Distinct attack from Agent 5
(`OBSERVABLE_PRINCIPLE_CHARACTER_SYMMETRY_NOTE`) and Agent 10 v2
(`G5_GAMMA_1_SECOND_ORDER_RETURN_NOTE`).

## Safe statement

On the retained `Cl(3)/Z^3` framework surface, the Koide 45 deg cone on
the `hw=1` triplet `v in R^3_+` can be rewritten in the character-block
variables `p_+ = a_0^2` (1D trivial-character eigenspace power) and
`p_- = 2 |z|^2` (2D nontrivial-character eigenspace power) as the **equal-
block-power** condition

```
p_+ = p_-    <=>    a_0^2 = 2 |z|^2    <=>    Q_l = 2/3.
```

Equivalently, the Cauchy-Schwarz ratio
`sigma(v) = (sum v_i)^2 / (3 sum v_i^2) = a_0^2/|v|^2` takes the value
`sigma = 1/2` at Koide — the genuine midpoint of the CS range `[0, 1]`.

This is the Plancherel-level restatement of the original Agent 1 cone
equivalence. It is theorem-grade.

## Four variational candidates

### H-1 Cauchy-Schwarz midpoint stationarity

**Functional.** `S_sym(sigma) = sigma (1 - sigma)`. Unique maximum at
`sigma = 1/2`, which IS the Koide value.

**Derivability from retained authorities.** NO. The symmetric-quadratic
functional `sigma(1-sigma)` is not an output of the retained observable-
principle authority. The retained `log|det(D)| = log alpha + 2 log beta`
generator produces a *dimension-weighted* entropy whose stationary point
is `sigma = 2/3` (two units of weight on the 2D nontrivial block, one
unit on the 1D trivial block), NOT Koide.

**Koide match.** Coincidental at the sigma-value level only. No retained
pathway to this functional.

**Verdict:** NOT DERIVABLE FROM RETAINED.

### H-2 Maximum-entropy on C_3 character decomposition

**Functional.** `S(p_+, p_-) = log(p_+) + log(p_-)` at fixed
`p_+ + p_- = |v|^2`. Lagrangian stationary point

```
p_+^* = p_-^* = |v|^2 / 2,
```

which translates exactly to `a_0^2 = 2 |z|^2` — the Koide cone — with
`sigma = 1/2`. Hessian at the stationary point is negative-definite
(eigenvalues `-4/|v|^4` with multiplicity 2), so the stationary point is
a **unique maximum**.

**Derivability from retained authorities.** PARTIAL. The retained
observable-principle authority delivers `log|det(D)|` with D circulant,
decomposing as `log alpha + 2 log beta`. On the power variables
`(p_+, p_-)`, this corresponds to weights `(1, 2)` matching the COMPLEX
irrep dimensions. Maximising the weighted form `log(p_+) + 2 log(p_-)`
at fixed `p_+ + p_- = |v|^2` gives

```
p_+^{w*} = |v|^2 / 3,    p_-^{w*} = 2 |v|^2 / 3,
```

i.e., `a_0^2 = |v|^2/3`, `2 |z|^2 = 2 |v|^2/3` so `a_0^2 = |z|^2`. This
is `sigma = 1/3`, NOT Koide. The retained weighted form lands at the
"complex-irrep-democratic" direction, not the Koide midpoint.

**The Koide form requires EQUAL weighting across the two REAL-IRREP
blocks** — one log per block, independent of block dimension. This is
NOT the retained log|det| structure, which is intrinsically dimension-
weighted by the multiplicity of each eigenvalue in `det D`.

**Koide match.** YES if real-irrep-block democracy is assumed; NO
otherwise.

**Named missing primitive:** `REAL-IRREP-BLOCK DEMOCRACY` — a retained
variational principle that weights each real-irrep block of a
`C_3`-invariant 3-space by `1` regardless of block dimension, instead
of by the block's complex-multiplicity as in `log|det|`. Such a
principle would be a genuinely new retained object.

**Verdict:** DERIVABLE FROM RETAINED + real-irrep-block democracy.

### H-3 Partition-function Legendre midpoint

**Functional.** `F(v) = Legendre[W](v) = (1/2) v^T K^{-1} v + O(v^4)`,
where `K` is the Hessian of `W[J] = log|det(D + J)|` at `J = 0`. By
`C_3` invariance, `K = circ(a, b)` with eigenvalues `(alpha, beta, beta)`
where `alpha = a + 2b`, `beta = a - b`. Therefore

```
F(v) = (v . e_+)^2 / (2 alpha) + |v_perp|^2 / (2 beta).
```

Test: does `F` have a C_3-invariant stationary point on the Koide cone?

**Analysis.** Gradient zero only at `v = 0` (trivial). With Plancherel
constraint `a_0^2 + 2 |z|^2 = |v|^2`, the Lagrangian stationarity
`1/alpha = 1/beta` forces `alpha = beta`, i.e., `b = 0`. That IS exactly
the Agent 5 Candidate-B failure mode: on the retained minimal block,
`b = K_{12} = 0` kills cross-species propagator, and the Koide cone
collapses to the `b = 0` line, which the Agent 1 primary lane rejected
as the degenerate-species limit. Fixing the mean (trace) instead drives
`|z| -> 0`, the fully-degenerate direction (`m_e = m_mu = m_tau`).

**Derivability from retained authorities.** YES (full retained
observable-principle authority).

**Koide match.** NO. Legendre midpoint of the retained generator on the
minimal `C_3`-invariant block collapses to the b=0 null closed by
Agent 5.

**Verdict:** FALSE. Collapses to Agent 5 null.

### H-4 Information-geometric midpoint (Fisher-Rao)

**Functional.** Fisher-Rao distance on the mass-fraction simplex
`p_i = m_i / sum m_j`, induced from `q_i = 2 sqrt(p_i)` on the positive
octant of the 2-sphere of radius 2. Test: does the Koide cone coincide
with the FR midpoint between the uniform `p_u = (1/3, 1/3, 1/3)` and a
corner `p_c = (1, 0, 0)`, or with any other natural FR-geometric point?

**Numerical check.**
- `p_u = (1/3, 1/3, 1/3)`, `q_u = (2/sqrt(3)) * (1, 1, 1)`.
- `p_c = (1, 0, 0)`, `q_c = (2, 0, 0)`.
- Spherical midpoint (slerp at `t = 1/2`) gives
  `p_{FR-mid} = (0.789, 0.106, 0.106)`, at which
  `Q = 0.4226 ≠ 2/3`.
- Fisher-Rao arclength from `q_u` to a Koide-saturating point is
  `0.6155` rad ≈ `35.26 deg`, not a natural 45 deg angle.

**Derivability from retained authorities.** NO. The Fisher-Rao metric on
the 3-generation mass simplex is not a retained object; the retained
framework supplies the C_3-invariant `hw=1` algebra and the
observable-principle generator, neither of which carries a natural
information-geometric metric on the mass simplex.

**Koide match.** NO. The Koide 45 deg angle is a **Cartesian** half-angle
between `v_parallel = a_0 e_+` and `v_perp` in `R^3`, NOT a Fisher-Rao
geodesic angle on the mass-fraction simplex.

**Verdict:** FALSE. FR-metric not retained; FR-midpoint does not match
Koide.

## Aggregate verdict

```
VARIATIONAL_KOIDE_DERIVED = PARTIAL
```

One of four candidates (H-2 with real-irrep-block-democracy weighting)
selects the Koide cone as its unique stationary point, but the weighting
is NOT currently retained. Three candidates (H-1, H-3, H-4) either fail
outright or are restatements of the cone rather than derivations.

### PDG post-hoc comparison

Framework-native comparison is PDG-independent. For informational
post-hoc context only: observed charged-lepton Koide is
`Q_l^{PDG} = 0.666661...`, matching `2/3` to `|dev| < 6e-6`. At the H-2
stationary point `a_0^2 = 2 |z|^2`, reconstructing a C_3-invariant
sample vector `v_K = a_0 e_+ + 2 Re(z e_omega)` with `a_0 = sqrt(2/3)`,
`|z| = 1/sqrt(6)` gives `Q = 2/3` exactly (verified numerically to
machine precision in the runner).

## Named missing primitive

**`REAL-IRREP-BLOCK DEMOCRACY`:** a retained variational principle that
treats the 1D trivial-character eigenspace and the 2D nontrivial-
character eigenspace on EQUAL footing (one entropy log per real-irrep
block, independent of block dimension). If such a principle can be
derived from the retained Plancherel + observable-principle chain, H-2
closes G5 via Avenue H.

The retained authorities `log|det|` and the C_3 character decomposition
naturally produce DIMENSION-WEIGHTED entropies (one log per complex
irrep, weighted by complex-multiplicity), which stationary at
`sigma = 1/3` rather than Koide `sigma = 1/2`. A retained principle that
collapses the two complex-conjugate nontrivial-character copies into a
single "real-block" entry would close the gap.

## Honest interpretation

Avenue H demonstrates that the Koide 45 deg cone `a_0^2 = 2 |z|^2`
coincides with the UNIQUE stationary point of a particularly natural
character-block entropy — the "equal-power-per-real-irrep-block"
entropy `log(p_+) + log(p_-)` at fixed total power — but this entropy
is NOT the one naturally supplied by the retained observable-principle
generator `log|det(D + J)|`, which weights by complex-irrep dimension
and instead produces `sigma = 1/3`. The gap between the retained
dimension-weighted form and the Koide real-irrep-block-democratic form
is a specific combinatorial weighting choice (a factor of 2 on the
nontrivial-character block), structurally analogous to the residual
`S_2` ambiguity identified by Agent 10 v2 and the `b = 0` degeneracy
identified by Agent 5: all three obstructions trace to the same
retained-authority inability to distinguish complex-irrep structure
from real-irrep-block structure on the `hw=1` triplet. Avenue H does
not close G5, but it supplies a sharply labeled candidate successor
primitive (real-irrep-block democracy) in the same spirit as the
`S_2`-breaking primitive requested by Agent 10 v2. It is one specific
input away from a genuine retained derivation of Koide; whether that
input can be derived from deeper retained authorities (rather than
adopted as an axiom) is the open question.

## What this does not claim

- Koide `Q_l = 2/3` is NOT promoted to a retained framework theorem.
  Avenue H supplies a candidate variational functional whose stationary
  point is Koide, but the functional's weighting is not retained.
- The `log(p_+) + log(p_-)` entropy is NOT claimed to be a retained
  object. It is named as the **specific successor primitive** whose
  retention would close G5 via Avenue H.
- Avenue H is NOT claimed to supersede Agent 10 v2's `S_2`-breaking
  primitive lane. The two missing primitives are orthogonal candidates
  in the open G5 attack surface.

## Dependency contract

The runner depends on:
- Agent 1 algebraic cone equivalence: `Q_l = 2/3 <=> a_0^2 = 2 |z|^2`
  (re-derived symbolically in Part 0).
- C_3 character decomposition on `R^3` (retained).
- Plancherel identity `|v|^2 = a_0^2 + 2 |z|^2` (retained).
- Observable-principle generator `W[J] = log|det(D + J)|`
  (retained, via `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`).
- No PDG imports in the derivation.

## Atlas status

Structural attempt note. Candidate for a tool row in the
`DERIVATION_ATLAS.md` Section F (Flavor / Koide) alongside Agent 5's
character-symmetry note and Agent 10 v2's second-order-return note.
Does NOT close G5. Supplies one named missing primitive (real-irrep-
block democracy) to the open G5 candidate primitive list.
