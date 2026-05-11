# Wilson Term BZ-Corner Hamming-Weight Staircase Bounded Note

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status authority:** source-note proposal only; audit verdict and
pipeline-derived status are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_wilson_bz_corner_hamming_staircase.py`](../scripts/frontier_wilson_bz_corner_hamming_staircase.py)

**Closed-form companion (added 2026-05-09):**
`WILSON_BZ_CORNER_HAMMING_STAIRCASE_CLOSED_FORM_NOTE_2026-05-09.md`
lifts this bounded proof-walk to a full closed-form theorem.
(Backticked to break the length-2 citation cycle with the closed-form
companion; citation graph direction is *closed_form → this_bounded*,
since the closed-form note lifts the bounded proof-walk while this
bounded note's combinatorial identity does not consume the
closed-form theorem as an input.)
It establishes T1 (closed-form formula `W(n)/r = 2·hw(n)` with
multiplicities `binomial(4, k)`), T2 (`S_4` axis-permutation
equivariance, including the spatial `C_3[111]` and full
`C_4[1111]` sub-actions), T3 (lattice-independence under any
rectangular Bravais rescaling — the staircase depends only on the
`F_2^4` quotient structure), and T4 (sister `Z^3` corollary
recovering the `1+3+3+1` decomposition). The independent audit
lane decides whether that companion closes the closed-form gap.

## Claim

On the canonical staggered Kogut-Susskind Dirac fermion action with
Wilson plaquette gauge action on `Z^3 + t = Z^4` APBC at the minimal
block (`L = 2` in each of the four directions, so `N_sites = 2^4 = 16`),
the Wilson term

```text
W(k)  =  r · Σ_μ ( 1 - cos k_μ )                                      (1)
```

evaluated at the 16 BZ corners `k_μ = n_μ · π` with
`n = (n_t, n_x, n_y, n_z) ∈ {0,1}^4` decomposes the 16-fold staggered
taste degeneracy into five Hamming-weight classes with multiplicities

```text
( 1, 4, 6, 4, 1 )    for hw ∈ { 0, 1, 2, 3, 4 },                      (2)
```

i.e. `binomial(4, hw)`, summing to `1 + 4 + 6 + 4 + 1 = 16`. All
corners in the same Hamming-weight class carry the same Wilson mass
shift

```text
W(hw)  =  2 · r · hw                                                    (3)
```

i.e. shifts `( 0, 2r, 4r, 6r, 8r )` for `hw ∈ { 0, 1, 2, 3, 4 }`.

This is a direct combinatorial identity on the existing canonical
Wilson + staggered surface. It does not use a Monte Carlo
measurement, a continuum-limit RG flow, or any observational input.
It does not add a new axiom, a new repo-wide theory class, or a
retained status claim.

## Proof-Walk

| Step | Load-bearing input | Lattice-action input? |
|---|---|---|
| BZ-corner enumeration: each of `2^4 = 16` corners labeled by `n ∈ {0,1}^4` with `k_μ = n_μ·π` | finite combinatorics on `{0,1}^4` | already-admitted Wilson plaquette + staggered + APBC surface (cited upstream) |
| Hamming-weight grading: each corner has `hw(n) = n_t + n_x + n_y + n_z ∈ {0,1,2,3,4}` | structural counting on bit-vectors | no (pure combinatorics on the corner labels) |
| Multiplicity per class: `\|{n : hw(n) = k}\|  =  binomial(4, k)` | binomial-coefficient identity | no |
| State-count identity: `Σ_{k=0}^{4} binomial(4, k) = 2^4 = 16` | binomial-sum identity | no |
| Per-corner Wilson value: `1 - cos(n_μ·π) = 1 - (-1)^{n_μ} = 2·n_μ` | exact integer evaluation of `cos(n·π)` for `n ∈ {0,1}` | no |
| Per-class mass shift: `W(n) = r · Σ_μ 2 n_μ = 2 r · hw(n)` | linearity + the previous step | no |
| Class-uniformity: any two corners with the same `hw` get the same `W` | direct substitution | no |

Every load-bearing step is finite combinatorics or exact integer
arithmetic. The Wilson plaquette form, staggered phases, link
unitaries, lattice scale `a`, plaquette value `<P>`, mean-field link
`u_0`, and Monte Carlo machinery do not appear as load-bearing inputs
to the staircase identity itself. (The Wilson coefficient `r` is a
normalization choice already cited at the upstream Wilson surface and
is carried through symbolically; this note does not derive it.)

## Exact Arithmetic Check

For `hw = k ∈ {0, 1, 2, 3, 4}` the runner reports the multiplicity
`binomial(4, k)` and the Wilson mass shift `W(k) = 2 r k` (with `r`
treated symbolically as a `Fraction(1, 1)` placeholder and the shift
read off as `2 k`):

```text
hw   multiplicity  shift / r
 0     1               0
 1     4               2
 2     6               4
 3     4               6
 4     1               8
```

State count check: `1 + 4 + 6 + 4 + 1 = 16  =  2^4`.

For each Hamming weight `k`, the runner picks one representative
corner `n` with `hw(n) = k` (e.g. the leading-bits corner) and
verifies `W(n) / r = Σ_μ (1 - (-1)^{n_μ}) = 2 k` by exact integer
arithmetic.

## Dependencies

- [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
  for the staggered Dirac realization context.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  for the framework axioms `A1` (`Cl(3)`) and `A2` (`Z^3`) and the
  recategorized open derivation targets used by this note's setup.
- [`THREE_GENERATION_STRUCTURE_NOTE.md`](THREE_GENERATION_STRUCTURE_NOTE.md)
  for the existing `1 + 1 + 3 + 3` BZ-corner-on-`Z^3` Hamming-weight
  decomposition (a sister 3-spatial-dim split, `2^3 = 8` corners,
  multiplicities `binomial(3, hw)`). The present note's `2^4 = 16`
  staircase on `Z^3 + t` is the time-extended version on the higgs-
  gap-chain surface; it does not replace or extend the `Z^3` sister.

`HIGGS_MASS_FROM_AXIOM_NOTE.md` is the parent gap-chain surface this
note is meant to support, not a load-bearing dependency of the
combinatorial identity. The parent points here for the staircase-only
authority; the quantitative effect on `m_H_tree` remains open.

These are imported authorities for a bounded theorem. The row remains
unaudited until the independent audit lane reviews this note, its
dependencies, and the runner.

## Boundaries

This note does not close:

- the continuum-limit numerical Higgs mass `m_H` value, or the
  `m_H / m_W` continuum convergence;
- the actual closure of the `+12%` Higgs gap chain;
- any retention upgrade of `HIGGS_MASS_FROM_AXIOM_NOTE.md`;
- the Wilson coefficient `r` itself (a separate normalization choice
  carried at the upstream Wilson surface);
- the staggered-Dirac realization gate;
- the `g_bare = 1` derivation;
- any claim that multiple lattice realizations exist in the framework;
- any follow-on proof-walk for other algebraic bookkeeping notes;
- any parent theorem/status promotion.

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_wilson_bz_corner_hamming_staircase.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: the 16 BZ corners on Z^3+t APBC decompose into five
Hamming-weight classes with multiplicities (1, 4, 6, 4, 1) and
Wilson mass shifts (0, 2r, 4r, 6r, 8r) by direct combinatorial
identity on {0,1}^4.
```
