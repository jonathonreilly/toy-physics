# Koide kappa = 2 Orbit-Dimension Factorization

**Date:** 2026-04-19
**Scope:** Structural factorization of the charged-lepton identity
`kappa = g_0^2 / |g_1|^2 = 2` into (i) an axiom-native integer piece
(the Z_3 orbit-dimension ratio on `Herm(3)` circulants) and (ii) the
Koide cone normalization condition, which is the content of the MRU
theorem at `d = 3`.
**Primary runner:**
`scripts/frontier_koide_kappa_two_orbit_dimension_factorization.py`
(PASS=26 FAIL=0)

## Summary

On the retained `Cl(3)/Z^3 + A0-A3` surface, the charged-lepton target
`kappa = g_0^2 / |g_1|^2 = 2` factors into two structurally independent
pieces:

- **(i) The integer "2" is axiom-native.** It is exactly the real-
  dimension ratio

  ```text
  2  ==  dim_R( non-trivial Z_3 iso-type on Herm(3) circulant )
         ---------------------------------------------------------
         dim_R( trivial Z_3 iso-type on Herm(3) circulant ).
  ```

  Equivalently, on the `C_3[111]` circulant commutant with cyclic
  bundle `B_0 = I`, `B_1 = C + C^2`, `B_2 = i(C - C^2)`, the Gram
  matrix under the real trace pairing `<A,B> := Tr(A^dagger B)` is

  ```text
  diag(Tr B_0^2, Tr B_1^2, Tr B_2^2)  ==  diag(3, 6, 6)  ==  3 * diag(1, 2, 2),
  ```

  and `Tr(B_1^2) / Tr(B_0^2) = 6/3 = 2`. This "2" counts the
  non-trivial Z_3 orbit size on `{I, C, C^2}` (the orbit `{C, C^2}`)
  versus the trivial orbit size (`{I}`, size 1). Z_3 is the unique
  cyclic group with this real-irrep dimension ratio `2 : 1`.

- **(ii) The Koide cone normalization `alpha:beta = 2:-1` (the MRU
  condition).** The most general Z_3-invariant quadratic functional of
  the responses `(r_0, r_1, r_2)` is

  ```text
  Q(G)  =  alpha * r_0^2  +  beta * (r_1^2 + r_2^2),
  ```

  with `gamma = delta = epsilon = 0` forced on the cross-terms by the
  doublet rotation `(r_1, r_2) -> R(2 pi / 3) (r_1, r_2)`. The Koide
  cone is the leaf `alpha : beta = 2 : -1` (giving `kappa = 2`); other
  leaves are equally Z_3-invariant. The specific leaf is pinned by the
  Moment-Ratio Uniformity theorem on `Cl(d)/Z_d`:

  ```text
  Var(sqrt(m_k))  ==  <sqrt(m_k)>^2,   equivalently  CoV(sqrt(m_k)) = 1.
  ```

  See `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
  for the full derivation of MRU at `d = 3` and its equivalence to
  `kappa = 2`.

## Derivation

### Piece (i) — axiom-native "2"

The retained master identity (Koide one-scalar obstruction triangulation
theorem) reads

```text
2 r_0^2 - (r_1^2 + r_2^2)  =  18 (g_0^2 - 2 |g_1|^2),                         (*)
```

with `r_i := Re Tr(G * B_i)` and `G = g_0 I + g_1 C + g_1^* C^2`. The
right-hand side's "2" is fully determined by `Tr(B_1^2) / Tr(B_0^2) = 2`.
This trace ratio is a pure circulant-Gram fact:

- `Tr(I^2) = 3`.
- `Tr((C + C^2)^2) = Tr(C^2) + 2 Tr(I) + Tr(C) = 0 + 6 + 0 = 6`.
- `Tr((i(C - C^2))^2) = -Tr(C^2 - 2 I + C) = 0 + 6 + 0 = 6`.

The ratio `6/3 = 2` equals `|orbit(C, C^2)| / |orbit(I)|`. This is an
immutable Z_3-representation fact over `R`: Z_3 has exactly two real
irreps (1-dim trivial, 2-dim complex-doublet); the real-dimension ratio
is `2:1`. Z_3 is the **unique** cyclic group with this irrep pattern
(Z_4 has `1 + 1 + 2 = 4` real dims split across 3 irreps; Z_2 has two
1-dim real irreps only).

### Piece (ii) — cone normalization via MRU

Enumerate Z_3-invariant quadratic functionals of the cyclic responses:

```text
Q(G) = alpha r_0^2
     + beta  (r_1^2 + r_2^2)
     + gamma r_0 r_1
     + delta r_0 r_2
     + epsilon r_1 r_2.
```

Under the Z_3 generator `g_1 -> omega g_1`, the doublet `(r_1, r_2)`
rotates by 120° in the real plane. Invariance forces
`gamma = delta = epsilon = 0` (standard doublet invariant theory). So
the Z_3-invariant quadratic family is exactly

```text
Q(G)  =  alpha r_0^2 + beta (r_1^2 + r_2^2)
      =  9 alpha g_0^2 + 36 beta |g_1|^2.
```

Setting `Q = 0` gives `kappa = -4 beta / alpha`. The MRU theorem picks
the leaf `alpha : beta = 2 : -1` (equivalently `kappa = 2`) by
requiring Frobenius-normalized cyclic responses to be uniform across
Z_3 isotypes.

### Equivalent phrasings of the cone normalization

- **Brannen–Rivero CoV form.** `CoV(sqrt(m_k)) := sqrt(Var)/ <.> = 1`.
- **Circulant-Fourier form.** `Var(sqrt(m_k)) = 2 |g_1|^2`,
  `<sqrt(m_k)> = g_0`. Koide cone `<=>  2 |g_1|^2 = g_0^2`, which after
  the orbit "2" from (i) is exactly `<sqrt(m_k)>^2 = Var(sqrt(m_k))`.
- **Koide Q form.** The sum-square ratio
  `Q = (sum sqrt(m_k))^2 / (3 sum m_k)` equals `2/3` iff `CoV = 1`.

## Falsification checks (runner, all PASS)

1. `Tr B_0^2 = 3`, `Tr B_1^2 = 6`, `Tr B_2^2 = 6`, symbolic (sympy).
2. Circulant-Gram ratio `Tr B_1^2 / Tr B_0^2 == 2` symbolically.
3. Master identity `2 r_0^2 - (r_1^2 + r_2^2) == 18 (g_0^2 - 2 |g_1|^2)`
   verified symbolically.
4. Master identity invariant under an `SO(2)` rotation of the doublet
   `(B_1, B_2) -> (B_1', B_2')` by arbitrary angle `theta` (symbolic
   residual = 0).
5. Master identity **not** invariant under non-orthonormal scalings
   `(B_1, B_2) -> (lambda B_1, mu B_2)` with `lambda != mu` — the
   "2:1" ratio is pinned by the Hermitian-orthonormal choice.
6. sigma=0 no-go check: `kappa` uses only circulant commutant DOF.
7. right-conjugacy-invariance no-go check: `Tr(G B_i)` is a left-trace
   functional, right-invariance not invoked.
8. positive-parent-axis no-go check: `kappa` constrains cyclic
   Fourier eigenvalues of `G`, not axis-basis diagonalization.
9. Group-theoretic uniqueness: `Z_3` is the unique cyclic group with
   the real-irrep dimension ratio `2:1`.
10. Observational (flagged separately): PDG charged-lepton masses give
    `a^2 / |b|^2 = 2.00004` (sub-percent); not a derivation.

## Interpretation

The one-scalar obstruction theorem of 2026-04-18 reduces Koide on the
retained surface to the single real equation `kappa = 2`. This note
factors that equation into the two structurally independent pieces
above: the integer "2" is the Z_3 orbit-dimension ratio (axiom-native);
the normalization `=` is the MRU condition. With MRU now a retained
theorem, both pieces close inside A0–A3.

## Scope

### What is established

1. The coefficient "2" in the charged-lepton Koide master identity is
   axiom-native: it is the real-dimension ratio of the non-trivial to
   trivial Z_3 iso-types on `Herm(3)`.
2. The coefficient is stable under orthonormal rotations of the doublet
   bundle `(B_1, B_2)` and unstable under non-orthonormal rescalings.
3. The Koide cone normalization `alpha : beta = 2 : -1` is not forced
   by Z_3-invariance alone; it is forced by the MRU theorem at `d = 3`.

### What is not established

- No statement about the doublet phase (that is the Berry-phase theorem;
  see `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`).
- No statement about the quark or neutrino sectors.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_kappa_two_orbit_dimension_factorization.py
```

Expected: final line emits `PASS=26 FAIL=0`.

## Citations

- `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`
- `docs/KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md`
- `docs/KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md`
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
- `docs/KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md`
- `docs/PMNS_RIGHT_CONJUGACY_INVARIANT_NO_GO_NOTE.md`
- Companion notes:
  - `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`
  - `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`
  - `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md`
