# PMNS Transfer-Operator Dominant Mode

**Date:** 2026-04-16 (revised 2026-05-16: the transfer kernel is now derived as
an explicit function of the primitive corner-transport operator on the active
`hw=1` triplet rather than posited from `(xbar, ybar)`, so the spectral
recovery of the active seed pair is a genuine measurement of the constructed
operator and not an algebraic reparameterization of supplied data)
**Status:** support - structural or confirmatory support note
**Script:** [`frontier_pmns_transfer_operator_dominant_mode.py`](../scripts/frontier_pmns_transfer_operator_dominant_mode.py)

## Question

Can a genuinely dynamical native law on the `hw=1` triplet recover any of the
active microscopic PMNS data from corner-to-corner transport?

## Dynamical primitive

The primitive object on the `hw=1` active triplet is the corner-to-corner
transport operator from
[`PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE`](PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md):

`T_act(x, y, delta) = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i delta}) C`

with `C` the canonical `C3` cycle permutation. The seven real parameters
`(x_1, x_2, x_3, y_1, y_2, y_3, delta)` are the microscopic active-block data
on this patch. The seed pair `(xbar, ybar)` is **not** an input to the
construction below.

## Constructed transfer kernel

The native dynamical transfer kernel is built from `T_act` by Hermitization
plus `C3` orbit-averaging:

`T_kernel(T_act) := (1/3) * sum_{k=0,1,2} C^k (T_act + T_act^dagger) C^{-k}`

This is a definite function of the supplied operator `T_act`. Both steps are
canonical: Hermitization gives the symmetric transfer shadow, and the
`C3` orbit-average projects onto the `C3`-equivariant sector
`span{I, C + C^2}`. Nothing in this construction takes `(xbar, ybar)` as input
or pre-supplies a target form.

## Bottom line

`T_kernel(T_act)` always lies in `span{I, C + C^2}` and is Hermitian and
`C3`-equivariant by construction (Part 1 of the runner). Its diagonal and
off-diagonal entries are determined by the `C3` orbit moments of the primitive
`T_act` (Part 3):

`T_kernel[i, i] = 2 Re(t_even)`

`T_kernel[i, i+1 mod 3] = Re(t_fwd) + Re(t_bwd)`

where `t_even = tr(T_act)/3`, `t_fwd = (T_act_{12} + T_act_{23} + T_act_{31})/3`,
`t_bwd = (T_act_{13} + T_act_{32} + T_act_{21})/3` are exactly the orbit moments
used in `PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE`.

On the aligned weak-axis patch (`x_i = xbar`, `y_i = ybar`, `delta = 0`) this
reduces to

`T_kernel = 2 xbar I + ybar (C + C^2)`

with eigenvalues

`lambda_+ = 2 xbar + 2 ybar`  (dominant symmetric mode)

`lambda_- = 2 xbar - ybar`  (doubly-degenerate orthogonal mode)

and the seed pair is read off by spectral inversion of the **dynamically
constructed** operator:

`xbar = (lambda_+ + 2 lambda_-) / 6`

`ybar = (lambda_+ - lambda_-) / 3`

This is a genuine spectral measurement of `T_kernel(T_act)`, not an algebraic
reparameterization of supplied coefficients (Parts 2 and 5).

## What is exact

On the aligned `hw=1` active patch the constructed kernel gives:

- an exact dominant symmetric mode (eigenvector along the uniform direction
  `u_0 = (1, 1, 1)/sqrt(3)`)
- an exact doubly-degenerate orthogonal mode
- an exact spectral measurement of the aligned active seed pair
  `(xbar, ybar)` of `T_act` from the dominant + subdominant eigenvalues
- exact agreement of `T_kernel`'s diagonal and off-diagonal entries with the
  `C3` orbit moments `(t_even, t_fwd, t_bwd)` of the primitive `T_act`

The route is native: it uses only the `hw=1` triplet corner-transport
primitive `T_act` and its canonical Hermitization + `C3` orbit-averaging.

## What it does not give

`T_kernel(T_act)` has a genuine kernel on the 5-real off-seed corner-breaking
carrier (zero-sum `xi, eta` directions on the aligned patch, plus `delta`).
Two distinct off-seed microscopic samples with the same aligned seed averages
collapse to the same `T_kernel` and therefore yield identical spectral seed
measurements (Part 4). So this is a positive but bounded dynamical law:

- it closes the aligned seed-pair subset
- it does not close the full off-seed microscopic value law

This is the same bounded blindness as in `PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK`.

## Theorem

**Theorem (PMNS transfer-operator dominant-mode law).** Let
`T_act(x, y, delta) = diag(x) + diag(y_eff) C` be the primitive `hw=1` active
corner-transport operator (with `y_eff_3 = y_3 e^{i delta}`). Define the
native transfer kernel

`T_kernel(T_act) := (1/3) sum_{k=0,1,2} C^k (T_act + T_act^dagger) C^{-k}`.

Then `T_kernel(T_act)` is Hermitian and `C3`-equivariant, lies in
`span{I, C + C^2}`, and on the aligned weak-axis patch (`x_i = xbar`,
`y_i = ybar`, `delta = 0`) has a unique dominant symmetric mode of eigenvalue
`2 xbar + 2 ybar` and a doubly-degenerate orthogonal mode of eigenvalue
`2 xbar - ybar`. The aligned active seed pair is therefore the spectral
measurement

`xbar = (lambda_+ + 2 lambda_-) / 6`, `ybar = (lambda_+ - lambda_-) / 3`,

of `T_kernel(T_act)`. The route does not determine the 5-real corner-breaking
source: `T_kernel` is constant on the zero-sum off-seed carrier on the aligned
patch.

## Verification

```bash
python3 scripts/frontier_pmns_transfer_operator_dominant_mode.py
```

Expected:

```text
PASS=23  FAIL=0
```
