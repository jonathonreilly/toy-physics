# Bougerol-Lacroix Staggered Blocking Submultiplicativity Tautological Bound

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** source note only. Audit verdicts and effective status
are set by the independent audit lane.
**Primary runner:** [`scripts/frontier_bougerol_lacroix_staggered_blocking_submult_tautological_bound.py`](../scripts/frontier_bougerol_lacroix_staggered_blocking_submult_tautological_bound.py)

## Scope

This note records a bounded support calculation for the 1D scalar model

```text
A_k : R -> R,     A_k(x) = alpha_LM * x,     k = 0, ..., 15.
```

The imported inputs are:

- `alpha_LM` from the same-surface plaquette package
  [`PLAQUETTE_SELF_CONSISTENCY_NOTE.md`](PLAQUETTE_SELF_CONSISTENCY_NOTE.md)
  and its algebraic identity note
  [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md).
- The 16-step count from the staircase/rung specification in
  [`YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md`](YT_P2_TASTE_STAIRCASE_BETA_FUNCTIONS_NOTE_2026-04-17.md)
  and from the independent species-count source
  [`NAIVE_LATTICE_FERMION_TWO_POWER_D_SPECIES_COUNT_NARROW_THEOREM_NOTE_2026-05-10.md`](NAIVE_LATTICE_FERMION_TWO_POWER_D_SPECIES_COUNT_NARROW_THEOREM_NOTE_2026-05-10.md).

## Result

On `R` with the Euclidean norm, each `A_k` has operator norm
`||A_k||_op = alpha_LM`. Therefore the finite product

```text
Pi_16 = A_15 A_14 ... A_0
```

satisfies

```text
||Pi_16||_op = product_{k=0}^{15} ||A_k||_op = alpha_LM^16.
```

This is exact on the 1D scalar model. It is also tautological with the
rung specification `mu_k = mu_0 * alpha_LM^k`: the model is defined so
that every one-step ratio is `alpha_LM`, so the 16-step product is just
`mu_16 / mu_0 = alpha_LM^16`.

The same scalar model has singleton-product Lyapunov exponent
`lambda_1 = log(alpha_LM)`. This is consistent with the external
Bougerol-Lacroix/Oseledets MET statement recorded in
[`BOUGEROL_LACROIX_OSELEDETS_MET_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md`](BOUGEROL_LACROIX_OSELEDETS_MET_EXTERNAL_NARROW_THEOREM_NOTE_2026-05-10.md),
but it adds no independent derivation: the Lyapunov value is the log of
the scalar already put into the 1D model.

## Boundary

This bounded theorem does not close the hierarchy formula. In particular:

- it does not derive `alpha_LM`;
- it does not derive the integer `16`;
- it does not identify the 1D scalar model with the canonical
  Wilson-Kadanoff blocking operator of the framework's gauge theory;
- it does not identify the scalar `alpha_LM` with a staggered Dirac taste
  eigenvalue or with a transfer-matrix spectral gap;
- it does not promote or demote any upstream framework note.

The calculation is still useful because it separates a mathematically true
submultiplicativity statement from the stronger physical bridge that would
be needed for hierarchy closure.

## Admissions

1. The 1D scale-operator family is an admitted mathematical carrier for this
   support calculation, not a derived canonical blocking operator.
2. `alpha_LM` and `16` are imported inputs. The identity above works for any
   `0 < alpha < 1` and any finite step count `N`; it does not select the
   framework values by itself.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_bougerol_lacroix_staggered_blocking_submult_tautological_bound.py
```

Expected result: `PASS=11 FAIL=0`. A passing run supports only the bounded
support statement above.
