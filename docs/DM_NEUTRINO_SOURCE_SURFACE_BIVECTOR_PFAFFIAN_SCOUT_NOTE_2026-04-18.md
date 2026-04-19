# DM Neutrino Source-Surface Bivector / Pfaffian Scout Note

**Date:** 2026-04-18
**Lane:** DM Blocker 3 Lane B — Pfaffian / bivector-grade scalar attack
**Verdict:** DEAD (with one partial channel flagged below)
**Axiom:** Cl(3) on Z^3 (single framework axiom; no retained physics as input)
**Units:** dimensionless Hermitian generators on H_hw=1 (natural units throughout)
**Script:** `scripts/frontier_dm_neutrino_source_surface_bivector_pfaffian_scout.py`

## Question

Case 3 Microscopic Polynomial Impossibility Theorem proves that no
retained local-polynomial functional on `H_hw=1` can pin `(delta_*, q_+*)`
because every such functional factors through `(delta^2, q_+)`. The
proof relies on assumption **A2.4**: `W[J] = log|det(D+J)|` is *the*
canonical retained scalar generator (forced by Grassmann-additivity
plus CPT-even scalarity).

Lane B drops A2.4 and asks: does the Cl(3) bivector grade (or a
Pfaffian-type scalar on chirality-split / staggered Dirac blocks)
supply an axiom-native `Z_3`-invariant polynomial scalar on `H_src` that
is `delta`-ODD, thus escaping the Case 3 trap?

## Bottom line

**DEAD at the strictness demanded by the theorem framing, with one PARTIAL channel.**

Inside `H_hw=1`, the natural `Z_3`-doublet bilinear

```
K_12(H_src) := v_2^T H_src v_2,    v_2 = (1, omega^2, omega)/sqrt(3)
```

evaluates in closed form to

```
K_12 = m + i sqrt(3) delta         (q_+ drops out: v_2^T T_q v_2 = 0)
```

so `K_12^3 = (m + i sqrt(3) delta)^3`, and

```
Im(K_12^3) = 3 sqrt(3) delta (m^2 - delta^2).
```

This IS a polynomial, `Z_3`-invariant, `delta`-ODD scalar on `H_src`.
Naively it breaks `delta`-evenness and gives a PARTIAL pinning of
`delta` (up to the ambiguity `delta = 0` or `delta^2 = m^2`).

However the scalar has three killer defects:

1. **Phase-gauge dependence (fatal).** The scalar uses the complex
   `C_3`-eigenvector `v_2`. Under the gauge `v_2 -> e^{i phi} v_2`, the
   pair `(Re K_12^3, Im K_12^3)` rotates by `6 phi`. The axiom-native
   `C_3[111]` action on `H_hw=1` forces only the eigenvalue equation
   `C_3 v_2 = omega v_2`, not the phase of `v_2`. The retained
   axiom-native atlas does not supply a preferred phase. A generic phase
   rotates `Im(K_12^3)` into `Re(K_12^3)` continuously, destroying
   `delta`-parity.

2. **`q_+`-blindness.** `v_2^T T_q v_2 = 0` identically. So this scalar
   does not even see `q_+`. The joint `(delta_*, q_+*)` selector needs
   at least two independent equations, and this one contributes zero
   information about `q_+`.

3. **Not in the axiom-native W[J] family.** `Im(K_12^3)` is a
   complex-BILINEAR contraction `v^T H v`, not a sesquilinear
   `v^dag H v`. The Observable Principle theorem (Theorem 1 of
   `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`) forces any retained
   CPT-even scalar observable generator to take the form `c log|Z|`.
   The complex bilinear is NOT CPT-even; it is not a derivative of
   `log|det(D+J)|` at any order. Even with A2.4 dropped, readmitting
   non-CPT-even scalars reintroduces fermionic-phase content and
   contradicts the additivity + scalarity derivation of `W[J]` on
   independent subsystems.

The combination of these defects places `Im(K_12^3)` OUTSIDE the class of
legitimate axiom-native retained scalars. Hence it does not damage the
Case 3 impossibility theorem.

## Unit system and notation

- Hermitian generators are dimensionless.
- `omega = exp(2 pi i / 3)`.
- `v_0 = (1,1,1)/sqrt(3)` is the `C_3`-singlet eigenvector
  (eigenvalue `1`).
- `v_1 = (1, omega, omega^2)/sqrt(3)` is one doublet eigenvector
  (eigenvalue `omega^2`).
- `v_2 = (1, omega^2, omega)/sqrt(3)` is the other doublet eigenvector
  (eigenvalue `omega`).
- `K_{ij} := v_i^T H_src v_j` uses complex BILINEAR (not sesquilinear).
- Notation `H_src = m T_m + delta T_delta + q_+ T_q` as in
  `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`.

## Full bilinear table (closed form; all six Z_3 bilinears)

Direct evaluation on `H_src = m T_m + delta T_delta + q_+ T_q`:

```
K_00 = v_0^T H_src v_0 = m + 2 q_+        (singlet-singlet, REAL)
K_11 = v_1^T H_src v_1 = m - i sqrt(3) delta
K_22 = v_2^T H_src v_2 = m + i sqrt(3) delta  (complex conjugate of K_11)
K_01 = v_0^T H_src v_1 = 0
K_02 = v_0^T H_src v_2 = 0
K_12 = v_1^T H_src v_2 = -q_+            (cross-doublet, REAL)
```

Key observations:

- Singlet-doublet mixing vanishes (`K_01 = K_02 = 0`) because
  `sum_i v_i = sqrt(3)` for `v_0`, but
  `sum_i (v_0)_i (v_k)_j (H_{ij}) = 0` whenever `H_{ij}` is
  `Z_3`-doublet-valued.
- `K_22 = m + i sqrt(3) delta`: the ONLY bilinear carrying the
  `delta`-linear dependence. Everything else is quadratic or higher in
  `delta`.
- `K_12 = -q_+`: cross-doublet bilinear carrying the `q_+` dependence,
  real, `delta`-blind.
- `K_00 = m + 2 q_+`: singlet-singlet, real, `delta`-blind.

## `Z_3`-invariant polynomial scalars from the bilinears

`Z_3`-transformations on `H_src` by conjugation induce weight shifts on
the bilinears. Under `H -> C_3 H C_3^-1`:

```
K_00 -> K_00,  K_11 -> K_11,  K_22 -> K_22,  K_12 -> K_12,
K_01 -> omega K_01,  K_02 -> omega^2 K_02.
```

So `Z_3`-invariant polynomials in these are generated by
`K_00, K_11, K_22, K_12, K_01 K_02, K_01^3, K_02^3, ...` (and products).
In our chart `K_01 = K_02 = 0` identically, so the cubic `K_01^3`,
`K_02^3` branches vanish. The surviving invariants are polynomials in
`(K_00, K_11, K_22, K_12)`.

`K_11 = K_22^*` (from Hermiticity of `H_src`), so the independent
scalars are `(K_00, K_12, K_22)` with `K_22` complex. Real scalars:

```
|K_22|^2 = m^2 + 3 delta^2          (delta-EVEN)
Re K_22 = m                         (delta-EVEN)
Im K_22 = sqrt(3) delta             (delta-ODD, phase-dependent)
Re (K_22)^3 = m^3 - 9 m delta^2     (delta-EVEN)
Im (K_22)^3 = 3 sqrt(3) delta (m^2 - delta^2)   (delta-ODD, phase-dependent)
K_00 = m + 2 q_+                    (delta-EVEN)
K_12 = -q_+                         (delta-EVEN)
```

The two `delta`-ODD entries `Im K_22` and `Im(K_22^3)` are the candidate
escape channels. Both are phase-dependent.

## Why the phase is not axiom-native

Under the gauge `v_2 -> e^{i phi} v_2` (a U(1) freedom that the
`C_3`-eigenvalue equation `C_3 v_2 = omega v_2` does not fix):

```
K_22 -> e^{2 i phi} K_22
```

so

```
Im K_22   -> cos(2 phi) Im K_22 + sin(2 phi) Re K_22
Im K_22^3 -> cos(6 phi) Im K_22^3 + sin(6 phi) Re K_22^3.
```

Under a generic `phi`, the "delta-odd" combination `Im K_22^(k)` rotates
into the "delta-even" combination `Re K_22^(k)`. Only the Z_6 subgroup
`phi in {0, pi/3, 2pi/3, ..., 5pi/3}` leaves the odd/even labeling
untouched. A generic choice mixes them, and delta-parity is NOT an
invariant of the rotated pair.

The retained atlas provides no axiom-native mechanism to pin the phase
of `v_2`:

- The `C_3[111]` action only fixes the eigenvalue, not the eigenvector
  phase.
- The lattice translation operators `T_x, T_y, T_z` commute with `C_3`
  but act trivially on the eigenvector within `H_hw=1` (they just multiply
  by signs in a basis-dependent way and do not pick a canonical phase
  for `v_2`).
- The Cl(3) pseudoscalar `e_123 = e_1 e_2 e_3` provides a canonical
  imaginary unit on the Pauli rep `M_2(C)`, but `H_hw=1` is not directly
  `M_2(C)` — it is a 3-dim `C`-rep of `C_3 subset U(3)`, and the
  pseudoscalar does not project into this sector.
- The retained carrier normal form fixes `phi_+ = arg(r_31)` on `H`
  matrix entries, not on the `C_3`-eigenvector phase.

## The observable-principle obstruction (independent of phase)

Even granting a fixed phase, `Im K_22^3` is ruled out as an axiom-native
retained scalar observable by the Observable Principle theorem:

- `K_22 = v_2^T H_src v_2` is a COMPLEX BILINEAR contraction.
- The unique additive CPT-even scalar generator for independent
  subsystems is `W[J] = c log|Z[J]| + const`.
- `Im K_22^3` is NOT a source derivative of `W[J]` at any order. It is
  a bilinear in `H` with complex weights, not a polynomial in
  sesquilinear traces `Tr[(D+J)^{-1} P_x P_y ...]`.
- The fermionic-phase information of `det(D+J)` is explicitly thrown
  away by CPT-evenness, precisely to exclude non-physical scalars of
  the `Im K_22^3` type.

Dropping A2.4 does not rescue this: A2.4 is derived from
Grassmann-additivity plus CPT-even scalarity, and `Im K_22^3` fails
CPT-evenness.

## Lattice-is-physical check

PASS. The vector `v_2 = (1, omega^2, omega)/sqrt(3)` is defined on the
three lattice sites supporting `H_hw=1`, with complex weights on-site.
The bilinear `v_2^T H_src v_2` is a local quantity in the lattice sense
(site-to-site correlation with complex weights). So the candidate
scalar is lattice-realizable in principle.

## 3+1D check

NEUTRAL. Anomaly-forced 3+1 adds chirality and a `gamma_5`-like splitting
to the full lattice Dirac, but the current `H_hw=1` reduction is a
spatial slice. Lifting `K_22` into a Dirac four-spinor operator adds
chirality blocks but does NOT create a new axiom-native phase for
`v_2`: the chirality operator is `Z_2`-valued (even sub-structure), not
`U(1)`. So the phase ambiguity survives the 3+1 lift. The Pfaffian
of the staggered Dirac on `Z^(3+1)` is proportional to `|det|^(1/2)`,
with sign dependent on fermionic-phase information that CPT-evenness
forbids.

## hw=1 convergence check

FAIL (Koide-style trap). The bivector-grade scalar `K_22` lives
entirely inside `H_hw=1` — it is a contraction of `H_src` over the
three highest-weight-1 lattice sites. It does NOT naturally escape to
cross-hw content. This is the same trap that the
`KOIDE_MICROSCOPIC_SCALAR_SELECTOR_TARGET_NOTE_2026-04-18.md`
obstruction flags for the charged-lepton Koide lane: the residual is
one microscopic scalar inside `H_hw=1`, and the retained atlas cannot
promote it without post-axiom input.

## Chirality-split / Pfaffian-of-staggered-Dirac check

DEAD. The decomposition `det(D) = det(D_L) det(D_R)` on chirality-split
blocks gives `log|det(D_L)| - log|det(D_R)|` as a candidate outside
`W[J]`. But:

- On the retained atlas, `H_src` is a single real-symmetric Hermitian
  block on `H_hw=1`. There is no chirality-split supplied by the axiom
  at this level.
- Lifting to 3+1D would require defining `D_L` and `D_R` from
  `(T_m, T_d, T_q)` in a chirality-aware way. The retained
  `ONE_GENERATION_MATTER_CLOSURE_NOTE.md` flags chirality as
  "load-bearing but part of the accepted framework claim," so any
  chirality-split of `(T_m, T_d, T_q)` is POST-AXIOM input.
- Staggered-Dirac Pfaffian on `Z^(3+1)` has `|Pf(D)|^2 = |det(D)|`, so
  its magnitude gives no new information. Its sign is the fermionic
  phase, which CPT-evenness forbids.

Hence the chirality-split / Pfaffian branch is dead without a
post-axiom chirality assignment.

## Conclusion / exit classification

**DEAD** on strict reading: the bivector-grade polynomial scalar
`Im K_22^3` is neither phase-gauge-invariant nor CPT-even. The A2.4
derivation (Grassmann-additivity + CPT-even scalarity => `W[J] = log|det|`)
survives at strength: dropping A2.4 does not open a legitimate door.

**PARTIAL** on relaxed reading: if the retained atlas were to supply a
canonical phase for `v_2` (e.g. via a new theorem coupling the
`C_3[111]` eigenvector phase to the lattice translations `T_x, T_y, T_z`
or to the bivector `e_123`), then `Im K_22^3 = 3 sqrt(3) delta (m^2 - delta^2)`
would be a legitimate axiom-native `delta`-ODD scalar. On that slice it
pins `delta in {0, +/- m}` — a discrete ambiguity in `delta` — but
still leaves `q_+` undetermined (since `K_22` is `q_+`-blind).

## Implication for Case 3 impossibility theorem

The Case 3 theorem's reliance on assumption A2.4 is VALIDATED by this
scout. Dropping A2.4 exposes the class of complex-bilinear scalars, but
the Observable Principle theorem's derivation (additivity + CPT-even)
already excludes them from the retained-observable class on physical
grounds, independently of A2.4. The impossibility theorem is robust
under A2.4 relaxation.

The ONLY remaining open question: is there an axiom-native mechanism to
fix the phase of `v_2` that the current atlas has missed? If so, and if
that phase is such that `Im K_22^3` survives CPT (which it does not,
per the additivity argument), then a PARTIAL `delta`-pinning scalar
would open. But the phase-fix would have to be derived, not assumed,
from `Cl(3)/Z^3`, and the CPT-obstruction is independent of the
phase-fix.

## Deliverable status

- Scout note: this file.
- Runner: `scripts/frontier_dm_neutrino_source_surface_bivector_pfaffian_scout.py`.
- Verdict: DEAD (strict) / PARTIAL (with phase-axiom and CPT-admission).

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_bivector_pfaffian_scout.py
```
