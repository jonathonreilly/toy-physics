# Z_3 Parity-Split Theorem — Microscopic Holonomy Selector Attempt

**Date:** 2026-04-17
**Status:** OBSTRUCTION + NARROWER-GAP + CROSS-CHECK-CANDIDATE
**Script:** `scripts/frontier_dm_neutrino_source_surface_z3_parity_split_theorem.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

This note records the outcome of a **direct microscopic** attempt to close
the right-sensitive 2-real selector law on the live DM-neutrino source-
oriented sheet: the `(delta, q_+)` pair in the `Z_3` doublet block. The
attempt deliberately bypasses any invented variational functional (the
info-geometric and cubic-variational routes). It seeks a sole-axiom
closure by a holonomy / transport / consistency condition using only
already-retained atlas objects.

The outcome is **not** a closure. It is:

- **two retained-atlas-native structural theorems** (Part 1 and Part 2),
- **one obstruction result** that rules out a whole class of candidate
 microscopic selectors (Z_3-parity-definite scalars), and
- **three cross-check-candidate results** showing that the natural mixed
 invariants (`det H`, `Tr(H^2)`, `K_12` character-matching) each give a
 `(delta, q_+)` that **disagrees** with the Schur-Q variational candidate
 `(sqrt(6)/3, sqrt(6)/3)`.

This note does not close the DM flagship lane or the selector gate.
Neither the Schur-Q variational candidate nor any microscopic candidate
is promoted to theorem-grade here. The integrated closure is the
downstream PMNS-as-f(H) closure.

## Theorem 1 (retained-atlas-native): Z_3-parity decomposition

**Statement.** On the live affine source-oriented sheet
`H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`, let
`sym(X) = (X + C_3 X C_3^{-1} + C_3^{-1} X C_3) / 3` denote the Z_3-cyclic
conjugation average and `anti(X) = X - sym(X)` denote the residual. Then:

```
sym(T_q) = T_q,  anti(T_q) = 0
sym(T_delta) = 0,  anti(T_delta) = T_delta
```

and `T_m` has nonzero components in both parity sectors.

**Proof.** Direct computation on the fixed retained generators. The
3x3 real matrices `T_q` and `T_delta` are verified by the runner at
machine precision:

- `z3_sym(T_q) - T_q` has zero norm
- `z3_anti(T_q)` has zero norm
- `z3_sym(T_delta)` has zero norm
- `z3_anti(T_delta) - T_delta` has zero norm

The orthogonality `<sym(X), anti(Y)> = 0` in the Hilbert-Schmidt trace
inner product holds for all pairs of retained generators to machine
precision, as expected from the projection-operator structure of `sym`.

**Claim label.** *Retained-atlas-native theorem.* No new axiom. Direct
algebraic fact about the fixed retained generators under the retained
`Z_3` symmetry.

## Theorem 2 (retained-atlas-native): Single-parity selector obstruction

**Statement.** Let `f: Herm(3, R) -> R` be any scalar function that
depends on `H` only through `sym(H)` (resp. only through `anti(H)`).
Then on the affine chart, `f(H(m, delta, q_+))` is a function of
`(m, q_+)` alone (resp. `(m, delta)` alone). Consequently, no single
Z_3-parity-definite scalar functional can fix the pair `(delta, q_+)`.

**Proof.** By Theorem 1, `sym(H) = sym(H_base) + m sym(T_m) + q_+ T_q`
does not contain any `delta`-dependent term. Likewise
`anti(H) = anti(H_base) + m anti(T_m) + delta T_delta` does not contain
any `q_+`-dependent term. Since `f` depends on `H` only through
`sym(H)` (resp. `anti(H)`), the claim follows.

The runner verifies the two constancy statements numerically:

- `||sym(H)[delta = v] - sym(H)[delta = 0]|| < 10^{-15}` for several `v`,
 at fixed `(m, q_+)`,
- `||anti(H)[q_+ = v] - anti(H)[q_+ = 0]|| < 10^{-15}` for several `v`,
 at fixed `(m, delta)`,
- `Tr(sym(H)^2)` is independent of `delta`,
- `Tr(anti(H)^2)` is independent of `q_+`.

**Claim label.** *Retained-atlas-native theorem.* No new axiom. Elementary
consequence of Theorem 1.

**Corollary (Z_3 parity-split structural obstruction).** Any microscopic
selector law for `(delta, q_+)` that is formulated via a single
Z_3-parity-definite scalar (circulant-only or anti-circulant-only
functional) **cannot close the gap**. It necessarily leaves one of the
two active coordinates free. any selector is therefore forced to use an
invariant that mixes both parity sectors.

## Cross-checks along mixed invariants

The natural mixed invariants that couple `delta` and `q_+` on the affine
sheet are tested in Part 3 of the runner. All three candidates are
retained-atlas-native scalars (no new axioms).

### (a) `det(H)` stationarity

Exhaustive solution of `grad det(H) = 0` on the 3-real affine chart (using
the analytic closed-form gradient) yields exactly **two** real critical
points. Exactly **one** lies inside the chamber `q_+ >= sqrt(8/3) - delta`:

```
(m_det, delta_det, q_det) ~= (0.613372, 0.964443, 1.552431)
```

with `det(H)_{crit} ~= 7.0765`. The other critical point
`(0.457, 1.227, -1.304)` lies outside the chamber (`q_+ < 0`).

### (b) `Tr(H^2)` stationarity

The global (unconstrained) minimum of `Tr(H^2)` lies outside the chamber.
Constraining to the chamber boundary `q_+ = sqrt(8/3) - delta` and
minimizing `Tr(H^2)(m, delta)` gives

```
(m_trH2, delta_trH2, q_trH2) ~= (0.385132, 1.267881, 0.365112).
```

### (c) `K_12 = -(a_* + b_*)` character-matching

The `Z_3` doublet-block entry `K_12 = m - 4 sqrt(2)/9 + i(sqrt(3) delta
- 4 sqrt(2)/3)` carries `Z_3`-weight `1`. The singlet-doublet slot sum
`a_* + b_* = 4 sqrt(2)/9 + i/2` also carries `Z_3`-weight `1` under the
natural embedding. The character-match `K_12 = -(a_* + b_*)` matches the
real part automatically (at `m = 0`, both equal `-4 sqrt(2)/9`) and forces

```
delta_char = (4 sqrt(2)/3 - 1/2) / sqrt(3) ~= 0.7999870.
```

This does **not** fix `q_+` (the condition is `q_+`-independent).

### Comparison with the Schur-Q variational candidate

```
Schur-Q variational candidate: (delta, q_+) = (sqrt(6)/3, sqrt(6)/3)
      ~= (0.816497, 0.816497)
(a) det(H) stationary: (delta, q_+) ~= (0.964443, 1.552431)
(b) Tr(H^2) on boundary: (delta, q_+) ~= (1.267881, 0.365112)
(c) K_12 char-match: delta ~= 0.799987 (q_+ free)
```

**All three microscopic candidates disagree with the Schur-Q variational
candidate.** No microscopic Z_3-parity-mixing invariant tested here
reproduces `(sqrt(6)/3, sqrt(6)/3)`.

This is a cross-check result, not an impossibility: a fourth, not-yet-
identified mixed invariant could still land on `sqrt(6)/3`. But the
obvious candidates do not.

## Narrowed gap statement

Before this note, the microscopic-holonomy direction was open and unexplored. After
this note:

**Negative results (hard):**

- Any Z_3-parity-definite microscopic scalar is ruled out as a the Z_3 parity-split theorem
 selector by Theorem 2.
- Among natural mixed microscopic scalars, `det(H)`, `Tr(H^2)`, and
 `K_12` character-match all fail to reproduce the Schur-Q minimum.

**Positive discipline (new):**

- Any future selector candidate for `(delta, q_+)` **must be checked
 against this cross-check ledger**. The question "does the candidate
 agree with `sqrt(6)/3`, or with one of `(a)/(b)/(c)`, or with a fourth
 point?" is now a standing discipline test.
- If a future selector lands at `sqrt(6)/3`, it must explain why the
 microscopic candidates above miss it.
- If a future selector lands at one of `(a)/(b)/(c)`, it must explain
 why the Schur-Q variational candidate is not the physical one.

## Position on publication surface

This note is explicitly **not** a flagship-grade theorem. It is a
narrower-gap + obstruction + cross-check note.

Appropriate placement:

- atlas obstruction row in
 `DERIVATION_ATLAS.md`
 under the DM neutrino source-surface family, sibling to the
 Schur-baseline partial closure
- do NOT use for any publication-grade positive quantitative claim
- do NOT use to "justify" the Schur-Q variational candidate — this
 note actively raises new questions for that candidate

## Is the det-critical-point the physically right `(delta, q_+)`?

The DM transport chain on the theorem-native radiation branch currently
gives `eta / eta_obs ~= 0.189` at the Schur-Q chamber minimum
(variational candidate). The PMNS-assisted route is required to reach
`eta / eta_obs = 1`.

A genuine closure via (a) (`det(H)` stationary) would predict a
significantly different `(delta, q_+)`. Evaluating the DM transport
chain at `(m_det, delta_det, q_det) ~= (0.613, 0.964, 1.552)` is the
natural next experiment: if `eta / eta_obs` lands closer to 1 at the
det critical point than at the Schur minimum, that would be a
compelling **new selector candidate** that deserves theorem-grade
pursuit in its own right. If it lands further from 1, the det-
stationarity candidate is ruled out on physical grounds and the Z_3 parity-split route is
simply obstructed.

This physical cross-check is recorded here as a **follow-up discipline
requirement** for any future selector work. It is not performed in this
runner (the transport chain is in a separate package; see
[DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md](./DM_LEPTOGENESIS_TRANSPORT_STATUS_NOTE_2026-04-16.md)).

## Atlas inputs used

All retained / theorem-grade on current `main`:

- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md)
 — exact affine chart `H(m, delta, q_+)` and exact active generators
 `T_m, T_delta, T_q`
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_HALF_PLANE_THEOREM_NOTE_2026-04-16.md)
 — exact chamber `q_+ >= sqrt(8/3) - delta`
- [DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_INTRINSIC_SLOT_THEOREM_NOTE_2026-04-16.md)
 — exact intrinsic slot pair `(a_*, b_*)`
- [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
 — exact `Z_3` doublet-block readout, including `K_12` formula
- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md)
 — Schur baseline `D = m I_3` and theorem-native `Q = 6(delta^2 + q_+^2)/m^2`

No new axioms are introduced in this note.

## What this file must never say

- that selector is closed
- that the DM flagship lane is closed
- that the Schur-Q variational candidate has been promoted to theorem-
 native by the Z_3 parity-split theorem (it has not; the Z_3 parity-split theorem cross-check actively
 disagrees)
- that the det-stationary point is the physical `(delta, q_+)` (it is a
 cross-check candidate, not a selector theorem)
- that the Z_3 parity-split theorem is definitively closed (it is obstructed only for Z_3-
 parity-definite scalars; Z_3-parity-mixing invariants remain an open
 design space, though the natural ones fail the cross-check)

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_z3_parity_split_theorem.py
```

Current expected: `PASS = 22, FAIL = 0`.
