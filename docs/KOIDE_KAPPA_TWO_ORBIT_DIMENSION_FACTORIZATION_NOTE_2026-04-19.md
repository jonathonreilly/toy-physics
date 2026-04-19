# Koide kappa=2 Orbit-Dimension Factorization

**Date:** 2026-04-19
**Status:** sharpening of the charged-lepton kappa=2 identity; the integer
"2" is axiom-native as an orbit-dimension ratio. **Cycle 10A update:** the
cone-normalization gap `Var(sqrt(m_k)) = <sqrt(m_k)>^2` has now been closed
by the Moment-Ratio Uniformity (MRU) theorem on Cl(d)/Z_d, which derives
kappa=2 as the d=3 specialization of a dim-parametric principle (see
`docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`). AXIOM D
has dropped from the axiom list.
**Primary runner:**
`scripts/frontier_koide_kappa_two_orbit_dimension_factorization.py` (PASS=26 FAIL=0)

## Summary

The open charged-lepton target `kappa = g_0^2 / |g_1|^2 = 2` on the retained
Cl(3)/Z^3 + A0-A3 surface factorizes into two structurally independent
pieces:

- **(i) The integer "2" is axiom-native.** It is exactly the real-dimension
  ratio

  ```text
  2  ==  dim_R( non-trivial Z_3 iso-type on Herm(3) circulant )
         ---------------------------------------------------------
         dim_R( trivial Z_3 iso-type on Herm(3) circulant ).
  ```

  Equivalently, on the `C_3[111]` circulant commutant with cyclic bundle
  `B_0 = I`, `B_1 = C + C^2`, `B_2 = i(C - C^2)`, the Gram matrix under the
  real trace pairing `<A,B> := Tr(A^dagger B)` is

  ```text
  diag(Tr B_0^2, Tr B_1^2, Tr B_2^2)  ==  diag(3, 6, 6)  ==  3 * diag(1, 2, 2),
  ```

  and the "2" is `Tr(B_1^2) / Tr(B_0^2) = 6/3 = 2`. The `6 = 2 * 3` arises
  because `(C + C^2)^2 = C^2 + 2 I + C^4 = C^2 + 2 I + C`, and the two
  copies of `I` each contribute `Tr(I) = 3`. The "2" counts the
  non-trivial Z_3 orbit size on `{I, C, C^2}` (the orbit `{C, C^2}`) versus
  the trivial orbit size (`{I}`, size 1).

- **(ii) The Koide cone normalization `alpha:beta = 2:-1` is NOT forced by
  Z_3 invariance alone.** The most general Z_3-invariant quadratic
  functional of the responses `(r_0, r_1, r_2)` is

  ```text
  Q(G)  =  alpha * r_0^2  +  beta * (r_1^2 + r_2^2),
  ```

  with `gamma = delta = epsilon = 0` forced on the cross-terms by the
  doublet rotation `(r_1, r_2) -> R(2 pi / 3) (r_1, r_2)`. Setting `Q = 0`
  yields a one-parameter family of candidate cones
  `kappa = -4 beta / alpha`; the specific leaf `alpha / beta = -2`
  (equivalently `kappa = 2`) is not selected by A0-A3.

The remaining open target is therefore **not** the bare value "2" but the
normalization condition

```text
Var(sqrt(m_k))  ==  <sqrt(m_k)>^2,
```

equivalently `CoV(sqrt(m_k)) = 1` in the Brannen-Rivero
`sqrt(m_k) = v_0 (1 + sqrt(2) cos(delta + 2 pi k / 3))` parametrization.

## Closure candidate — retained Frobenius uniformity (cycle 2)

A cycle-2 investigation of axiomatic candidates for closing the `alpha:beta`
ratio identified **Candidate D: retained Frobenius uniformity on the cyclic
compression image** as the cleanest axiom-native closure route. Candidate D
uses no new free axiom — it invokes the same uniform-measure principle that
justifies the Frobenius metric as the retained operator metric, applied on
the 3-real image of the cyclic compression of `dW_e^H`, and demands that
the singlet-block and doublet-block Frobenius energies on that image be
equal. This forces `3 a^2 = 6 |b|^2`, i.e. `a_0^2 = 2 |z|^2`, i.e.
`kappa = 2`.

Candidate D has been cross-checked against all 7 retained no-gos (all
clean). The remaining work to promote it to a retained theorem is to
identify a dynamical action whose retained-metric stationarity *forces*
the equipartition condition (as opposed to merely having equipartition as
its unique block-democratic critical point). See
`docs/KOIDE_FROBENIUS_UNIFORMITY_AXIOM_CANDIDATE_NOTE_2026-04-19.md` for
the full analysis.

## Derivation

### Piece (i) — axiom-native "2"

Starting from the retained master identity (Koide one-scalar obstruction
triangulation theorem)

```text
2 r_0^2 - (r_1^2 + r_2^2)  =  18 (g_0^2 - 2 |g_1|^2)                         (*)
```

with `r_i := Re Tr(G * B_i)` and `G = g_0 I + g_1 C + g_1^* C^2`, the
right-hand side's "2" is fully determined by
`Tr(B_1^2) / Tr(B_0^2) = 2`. This trace ratio is a pure circulant-Gram
fact and does not involve any scalar choice:

- `Tr(I^2) = 3`.
- `Tr((C + C^2)^2) = Tr(C^2) + 2 Tr(I) + Tr(C) = 0 + 6 + 0 = 6`.
- `Tr((i(C - C^2))^2) = -Tr(C^2 - 2 I + C) = 0 + 6 + 0 = 6`.

The ratio `6/3 = 2` equals `|orbit(C, C^2)| / |orbit(I)|`. This is an
immutable Z_3-representation fact over `R`: Z_3 has exactly two real
irreps, the 1-dim trivial and the 2-dim complex-doublet; the real-dimension
ratio is `2:1`. Z_3 is the **unique** cyclic group with this irrep pattern
(Z_4 has `1 + 1 + 2 = 4` real dims split across 3 irreps; Z_2 has two
1-dim real irreps only).

### Piece (ii) — cone normalization open

Enumerate all Z_3-invariant quadratic functionals of the cyclic responses:

```text
Q(G) = alpha r_0^2
     + beta  (r_1^2 + r_2^2)
     + gamma r_0 r_1
     + delta r_0 r_2
     + epsilon r_1 r_2.
```

Under the Z_3 generator `g_1 -> omega g_1`, the doublet `(r_1, r_2)` rotates
by 120 degrees in the real plane. Invariance forces
`gamma = delta = epsilon = 0` (standard doublet invariant theory). So the
Z_3-invariant quadratic family is exactly

```text
Q(G)  =  alpha r_0^2 + beta (r_1^2 + r_2^2)
      =  9 alpha g_0^2 + 36 beta |g_1|^2.
```

Setting `Q = 0` gives `kappa = -4 beta / alpha`. The Koide cone is the
leaf `alpha : beta = 2 : -1`, giving `kappa = 2`. Other leaves are
equally Z_3-invariant. Axioms A0-A3 do not pick one. Candidate D (see
closure section above) proposes Frobenius-uniformity as the single
additional promotion that pins this leaf.

### Equivalent phrasings of the remaining scalar

- **Brannen-Rivero CoV form.** `CoV(sqrt(m_k)) := sqrt(Var)/ <.> = 1`.
- **Circulant-Fourier form.** `Var(sqrt(m_k)) = 2 |g_1|^2`, `<sqrt(m_k)> = g_0`.
  Koide cone <=> `2 |g_1|^2 = g_0^2`, which after the orbit "2" from (i) is
  exactly `<sqrt(m_k)>^2 = Var(sqrt(m_k))`.
- **Koide Q form.** The sum-square ratio `Q = (sum sqrt(m_k))^2 / (3 sum m_k)`
  equals `2/3` iff `CoV = 1`.

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
9. Group-theoretic uniqueness: `Z_3` is the unique cyclic group with the
   real-irrep dimension ratio `2:1`.
10. Observational (flagged separately): PDG charged-lepton masses give
    `a^2 / |b|^2 = 2.00004` (sub-percent); not a derivation.

## Interpretation

The one-scalar obstruction theorem of 2026-04-18 states that Koide on the
retained surface reduces exactly to the single real equation `kappa = 2`.
The present note sharpens that statement: of the two numerical
ingredients in `kappa = 2`, the "2" on the right is axiom-native from
Z_3 orbit combinatorics, and the "=" is the remaining scalar gap. The
gap is now identified with the physically motivated coefficient-of-
variation condition `CoV(sqrt(m_k)) = 1`, not with a bare numerical
factor of 2. Cycle-2 Candidate D (retained Frobenius uniformity on the
cyclic compression image) supplies a clean axiom-native closure route
for this equality under one axiom promotion.

Practically, this re-targets the open attack surface:

- **No longer useful.** "Derive the value 2 from A0-A3." Already axiom-
  native (Z_3 dimension ratio).
- **Now the single open target.** "Derive `CoV(sqrt(m_k)) = 1` from
  A0-A3, or demonstrate that no A0-A3-compatible primitive forces it."
  Cycle 2 proposes the Frobenius-uniformity axiom as the forcing primitive;
  see Candidate D note.

## Scope

### What is established

1. The coefficient "2" in the charged-lepton Koide master identity is
   axiom-native: it is the real-dimension ratio of the non-trivial to
   trivial Z_3 iso-types on `Herm(3)`.
2. The coefficient is stable under orthonormal rotations of the doublet
   bundle `(B_1, B_2)` and unstable under non-orthonormal rescalings.
3. The Koide cone normalization `alpha : beta = 2 : -1` is not forced by
   Z_3-invariance alone; a one-parameter family of Z_3-invariant cones
   exists and the Koide leaf is one specific choice.
4. Three previously named candidate selectors (Candidate A
   Ginsparg-Wilson, Candidate B Casimir/Dyson-beta, Candidate C
   orbit-counting) were re-examined. A and B are ruled out as sole
   mechanisms; C is confirmed for piece (i) only.
5. All three no-go cross-checks (sigma=0, right-conj, positive-parent-
   axis) pass.
6. **(cycle 2)** Candidate D — retained Frobenius uniformity on the
   cyclic compression image — identified as the cleanest axiom-native
   closure route. Forces `3 a^2 = 6 |b|^2` ⇒ `kappa = 2` under one
   axiom promotion, cross-checks against all 7 retained no-gos.

### What is not established

- No derivation of `kappa = 2` (equivalently `CoV = 1`) from any structure
  strictly contained in A0-A3. Candidate D adds one axiom.
- No promotion of charged-lepton Koide to a retained theorem. The
  bounded-observational-pin status from the April 17 review remains.
- No statement about the quark or neutrino sectors.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_kappa_two_orbit_dimension_factorization.py
```

Expected: final line emits `PASS=N FAIL=0`.

## Citations

- `docs/KOIDE_ONE_SCALAR_OBSTRUCTION_TRIANGULATION_THEOREM_NOTE_2026-04-18.md`
- `docs/KOIDE_Z3_SCALAR_POTENTIAL_SUPPORT_NOTE_2026-04-19.md`
- `docs/KOIDE_POSITIVE_PARENT_AXIS_OBSTRUCTION_NOTE_2026-04-18.md`
- `docs/KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`
- `docs/KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md`
- `docs/PMNS_RIGHT_CONJUGACY_INVARIANT_NO_GO_NOTE.md`
- Sibling cycles-1+2 stack:
  - `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`
  - `docs/KOIDE_FROBENIUS_UNIFORMITY_AXIOM_CANDIDATE_NOTE_2026-04-19.md`
  - `docs/QUARK_UP_AMPLITUDE_RETAINED_NATIVE_CANDIDATE_NOTE_2026-04-19.md`
  - `docs/DM_CHAMBER_SIGNATURE_STRUCTURE_NOTE_2026-04-19.md`
