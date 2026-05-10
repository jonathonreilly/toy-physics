# Wilson Term BZ-Corner Hamming-Weight Staircase Closed-Form Note

**Date:** 2026-05-09
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
pipeline-derived status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_wilson_bz_corner_hamming_staircase_closed_form_certificate_2026_05_09.py`](../scripts/frontier_wilson_bz_corner_hamming_staircase_closed_form_certificate_2026_05_09.py)
**Companion bounded note (proof-walk):** [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)

## Summary

Lifts the bounded proof-walk in
[`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
to a closed-form theorem. The bounded note carried four deferrals:
the multiplicity formula, the per-class shift formula, the
class-uniformity statement, and a lattice-independence remark. This
note closes all four as exact identities by proving:

- **T1.** Closed-form enumeration on `{0,1}^4`: `W(n)/r = 2·hw(n)`,
  multiplicities `binomial(4, k)`.
- **T2.** Equivariance under the full `S_4` axis-permutation group.
- **T3.** Lattice-independence under any rectangular Bravais
  rescaling: the staircase depends only on the `F_2^4` quotient
  structure of corner labels.
- **T4.** Sister `Z^3` corollary: the spatial restriction recovers
  the `1+3+3+1` triplet decomposition of
  [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md).

This is finite combinatorics over `{0,1}^4` plus an exact symbolic
check that `1 - cos(n_μ π) = 2 n_μ` for `n_μ ∈ {0, 1}`. No Monte
Carlo, RG flow, or observational input is used. No new axiom, no
new repo-wide theory class, and no retained-status claim are
introduced.

## Setup (mirrors the bounded note)

On the canonical staggered Kogut-Susskind Dirac fermion action with
Wilson plaquette gauge action on `Z^3 + t = Z^4` APBC at the minimal
block (`L = 2` in each direction, `N_sites = 2^4 = 16`), the Wilson
term

```text
W(k)  =  r · Σ_μ ( 1 - cos k_μ )                                      (1)
```

is evaluated at the 16 BZ corners `k_μ = n_μ · π` with
`n = (n_t, n_x, n_y, n_z) ∈ {0,1}^4`.

## T1. Closed-form enumeration

**Theorem T1 (closed-form Wilson staircase).** For every
`n = (n_t, n_x, n_y, n_z) ∈ {0,1}^4`,

```text
W(n) / r  =  2 · hw(n)                                               (T1)
```

with `hw(n) = n_t + n_x + n_y + n_z ∈ {0, 1, 2, 3, 4}`. The 16
corners decompose into five Hamming-weight classes whose
multiplicities are the binomial coefficients

```text
| { n ∈ {0,1}^4 : hw(n) = k } |  =  binomial(4, k)                   (T1')
```

giving the closed-form multiplicity tuple `(1, 4, 6, 4, 1)` and the
state-count identity `Σ_{k=0}^{4} binomial(4, k) = 2^4 = 16`.

**Proof.** For each `μ`, `n_μ ∈ {0, 1}` so `n_μ · π ∈ {0, π}` and

```text
1 - cos(n_μ · π)  =  1 - (-1)^{n_μ}  =  2 · n_μ.                     (i)
```

This is an exact integer identity, not a Taylor expansion: `cos(0)`
and `cos(π)` are evaluated on the unit circle to `+1` and `-1`. Sum
(i) over `μ ∈ {t, x, y, z}` to get

```text
W(n) / r  =  Σ_μ (1 - cos(n_μ π))  =  Σ_μ 2 · n_μ  =  2 · hw(n).     (ii)
```

For (T1'), the multiplicity `|{n ∈ {0,1}^4 : hw(n) = k}|` equals
the number of length-4 binary strings with exactly `k` ones, which
is `binomial(4, k)` by direct combinatorics on bit-vectors. The
state-count identity is the binomial-sum identity
`Σ_k binomial(d, k) = 2^d` at `d = 4`. ∎

The runner `frontier_wilson_bz_corner_hamming_staircase_closed_form_certificate_2026_05_09.py`
verifies (i), (ii), and (T1') by:

1. exact symbolic evaluation `sp.cos(0) = 1` and `sp.cos(sp.pi) = -1`
   (sympy);
2. enumeration of all 16 corners and direct computation of `W(n)/r`
   as a sympy integer;
3. enumeration-based count of each Hamming-weight class against
   `binomial(4, k)`.

## T2. S_4 axis-permutation equivariance

**Theorem T2 (equivariance).** Let `S_4` act on `n ∈ {0,1}^4` by
permutation of the four axis labels `(t, x, y, z)`. Then for every
`σ ∈ S_4`:

- `hw(σ · n) = hw(n)` for every `n ∈ {0,1}^4`;
- `W(σ · n) / r = W(n) / r`.

Hence each Hamming-weight level set is fixed setwise by `S_4`, and
each level is a single `S_4`-orbit (the action is transitive on
each level).

**Proof.** Hamming weight is the sum of components, which is
permutation-invariant by commutativity of integer addition. The
Wilson value `W(n)/r = 2·hw(n)` is therefore likewise invariant.
For transitivity within a level: any two binary strings of length 4
with the same number of ones are related by some permutation of
positions, which is an `S_4` element acting on the four axis
labels. ∎

The `S_4 axis-permutation` group has order `4! = 24`. Two
distinguished subgroups are:

- The **spatial cyclic** `C_3[111]`, consisting of cyclic
  permutations of the three spatial axes `(x, y, z)` with the time
  axis `t` fixed. Its concrete elements as full-4D permutations are
  `id`, `(x → y → z → x)`, `(x → z → y → x)`. This is the cyclic
  group used by [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
  and [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md).
- The **full cyclic** `C_4[1111]`, consisting of cyclic shifts of
  all four axis labels.

Under `C_3[111]`, the spatial `hw=1` triplet `{(0,1,0,0), (0,0,1,0),
(0,0,0,1)}` is a single orbit; under the full `S_4`, the entire
`hw=1` 4-element class is a single orbit.

The runner verifies that all 24 elements of `S_4` preserve `hw` and
`W/r`, and that each level is a single orbit.

## T3. Lattice-independence

**Theorem T3 (lattice-independence).** Let `L = diag(a_t, a_x, a_y, a_z)`
with `a_μ > 0` be any rectangular Bravais lattice on `Z^3 + t` with
APBC and minimal block `2` in each direction. The BZ corners are
then `k_μ = n_μ · π / a_μ` with `n_μ ∈ {0, 1}`. The Wilson value at
each corner is

```text
W(n) / r  =  Σ_μ (1 - cos(k_μ · a_μ))  =  Σ_μ (1 - cos(n_μ π))
          =  2 · hw(n).
```

The right-hand side does not depend on the lattice spacings `a_μ`;
the staircase decomposition `(1, 4, 6, 4, 1)` and the closed-form
shifts `(0, 2, 4, 6, 8)` are therefore **lattice-independent**.

**Proof.** The cancellation `(n_μ π / a_μ) · a_μ = n_μ π` is exact.
Therefore `cos(k_μ a_μ) = cos(n_μ π)` and the per-direction value
is the parity-only function `1 - cos(n_μ π) = 2 n_μ`. The corner
labels `n ∈ {0,1}^4` constitute the `F_2^4` quotient of the BZ
boundary parities — they are the bit-vectors mod 2, independent of
`a_μ`. Hence `W(n)/r = 2 · hw(n)` for every rectangular Bravais
rescaling, and the multiplicity formula `binomial(4, k)` carries
across unchanged. ∎

This statement is **canonical given the C_3[111]-equivariant
primitive cube structure**: any rectangular lattice that admits the
spatial `C_3[111]` action and the minimal `L = 2` block produces
the same Hamming staircase. The bounded note's proof-walk citation
of `<P>`, `u_0`, and the lattice scale `a` is therefore explicitly
not load-bearing: those quantities cancel out of the staircase
identity itself.

The runner verifies lattice-independence symbolically with positive
abstract spacings `a_t, a_x, a_y, a_z` and numerically on three
independent rectangular lattices (rational, square-root-of-prime,
unit).

## T4. Sister Z^3 corollary

**Corollary T4 (spatial restriction).** Setting `n_t = 0` restricts
to the spatial sub-cube `{0,1}^3`. The 8 spatial BZ corners
decompose under spatial `C_3[111]` (cyclic permutation of `(x, y, z)`)
into four Hamming-weight classes with multiplicities `(1, 3, 3, 1)
= binomial(3, k)` and Wilson shifts `(0, 2, 4, 6)` (in units of `r`),
matching

```text
8  =  1 + 3 + 3 + 1
```

cited by [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md).

**Proof.** Apply T1, T2, and T3 to the spatial `d = 3` case: the
identical proof-walk runs on `{0,1}^3` with `S_3` axis-permutation
group. The `hw = 1` triplet is a single `C_3[111]` orbit. ∎

The runner verifies the `Z^3` corollary directly.

## Closed-form table (all 16 corners)

```text
hw   multiplicity = binomial(4, hw)   shift / r = 2·hw
 0     1                                0
 1     4                                2
 2     6                                4
 3     4                                6
 4     1                                8
sum    16  =  2^4                        --
```

Per-corner enumeration (lex order on `(n_t, n_x, n_y, n_z)`):

```text
(0,0,0,0)  hw=0  W/r=0
(0,0,0,1)  hw=1  W/r=2
(0,0,1,0)  hw=1  W/r=2
(0,0,1,1)  hw=2  W/r=4
(0,1,0,0)  hw=1  W/r=2
(0,1,0,1)  hw=2  W/r=4
(0,1,1,0)  hw=2  W/r=4
(0,1,1,1)  hw=3  W/r=6
(1,0,0,0)  hw=1  W/r=2
(1,0,0,1)  hw=2  W/r=4
(1,0,1,0)  hw=2  W/r=4
(1,0,1,1)  hw=3  W/r=6
(1,1,0,0)  hw=2  W/r=4
(1,1,0,1)  hw=3  W/r=6
(1,1,1,0)  hw=3  W/r=6
(1,1,1,1)  hw=4  W/r=8
```

## Dependencies

- [`WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md`](WILSON_BZ_CORNER_HAMMING_STAIRCASE_BOUNDED_NOTE_2026-05-08.md)
  for the bounded proof-walk this note lifts to closed form.
- `STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`
  for the staggered Dirac realization context.
- `MINIMAL_AXIOMS_2026-05-03.md`
  for the framework axioms `A1` (`Cl(3)`) and `A2` (`Z^3`) and the
  recategorized open derivation targets used by this note's setup.
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  for the sister `Z^3` `1+3+3+1` decomposition and the spatial
  `C_3[111]` group action.
- [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
  for the `C_3[111]` axis-permutation usage.

These are imported authorities for a closed-form theorem on a
finite combinatorial surface. The row remains unaudited until the
independent audit lane reviews this note, its dependencies, and the
runner.

## Boundaries

This note does not close:

- the continuum-limit numerical Higgs mass `m_H` value, or the
  `m_H / m_W` continuum convergence;
- the actual closure of the `+12%` Higgs gap chain;
- any retention upgrade of `HIGGS_MASS_FROM_AXIOM_NOTE.md`;
- the Wilson coefficient `r` itself;
- the staggered-Dirac realization gate;
- the `g_bare = 1` derivation;
- any claim that multiple lattice realizations exist in the framework;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_wilson_bz_corner_hamming_staircase_closed_form_certificate_2026_05_09.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: closed-form theorem certified.
```

The runner emits a JSON certificate at
`outputs/wilson_bz_corner_hamming_staircase_certificate_2026_05_09.json`
containing all 8 spatial corners, all 16 spacetime corners, their
Hamming weights, the closed-form Wilson shifts, the binomial
multiplicities, the `S_4` / `C_3[111]` equivariance verification,
and the lattice-rescaling invariance check.
