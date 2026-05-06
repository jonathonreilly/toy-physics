# PR230 Z3-Triplet Conditional Primitive-Cone Theorem

**Status:** conditional-support / exact Z3-triplet primitive-cone theorem;
same-surface PR230 primitive premise absent.

**Runner:** `scripts/frontier_yt_pr230_z3_triplet_conditional_primitive_cone_theorem.py`

**Certificate:** `outputs/yt_pr230_z3_triplet_conditional_primitive_cone_theorem_2026-05-06.json`

## Purpose

The neutral primitive/rank-one route is one of the remaining clean PR230
closure contracts.  The `origin/main` composite-Higgs stretch packet supplies a
concrete Z3 triplet candidate, but it is explicitly cross-lane and conditional.
This note asks a narrower question:

```text
If a same-surface PR230 action supplies that Z3 triplet as a positive neutral
transfer, does the primitive/rank-one mathematical premise follow?
```

The answer is yes, conditionally.

## Exact Theorem

Let `P` be the cyclic Z3 permutation on the triplet
`(Phi_1', Phi_2', Phi_3')`.  Then `P^3 = I`, but `P` alone is periodic and not
primitive.  The load-bearing primitive object is the lazy cyclic transfer

```text
L = (I + P) / 2 .
```

Exact arithmetic gives

```text
L^2 = (I + 2P + P^2) / 4 ,
```

and every entry of `L^2` is strictly positive.  Therefore `L` is a primitive
nonnegative matrix.  Perron-Frobenius then gives a unique positive triplet
eigenvector, here the uniform vector, and the stochastic powers converge to the
rank-one uniform projector.

This retires a mathematical part of the neutral primitive contract under named
premises.  It does not derive those premises on the current PR230 surface.

## Missing Current-Surface Premises

The current PR230 surface still lacks:

- same-surface EW/Higgs or composite action tying the triplet to the top FH/LSZ
  source coordinate;
- a derived off-diagonal neutral generator or production non-source response
  row;
- a strict neutral primitive-cone certificate on the PR230 surface;
- canonical `O_H`/source-Higgs pole overlap or an accepted physical-response
  bridge.

Pure Z3 cyclicity is not enough; the self/lazy aperiodic term is load-bearing.
Equal-magnitude condensate language is not enough; the positive transfer
operator has to be defined on the same surface.

## Claim Boundary

This block does not claim retained or proposed-retained top-Yukawa closure.  It
does not write
`outputs/yt_neutral_scalar_primitive_cone_certificate_2026-05-05.json`, does
not identify `O_s` or `O_sp` with canonical `O_H`, and does not use `H_unit`,
`yt_ward_identity`, observed targets, `alpha_LM`, plaquette, `u0`, or unit
assignments for `kappa_s`, `c2`, or `Z_match`.

## Literature Context

FMS/gauge-invariant Higgs literature remains the right language after a
same-surface gauge-Higgs or composite action is supplied.  Perron-Frobenius and
Krein-Rutman theory provide the primitive-cone/rank-one certificate engine only
after the transfer operator is defined.  They are not source-overlap or
normalization selectors by name.

## Verification

```bash
python3 scripts/frontier_yt_pr230_z3_triplet_conditional_primitive_cone_theorem.py
# SUMMARY: PASS=13 FAIL=0
```
