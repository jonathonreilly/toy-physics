# Gauge Plaquette Source Theorem and Constant-Lift No-Go

**Date:** 2026-04-15  
**Status:** exact gauge-side theorem plus exact no-go on the proposed constant-lift closure  
**Script:** `scripts/frontier_gauge_plaquette_source_no_go.py`

## Question

Can the `3 spatial + 1 time` plaquette

`P(beta) = <(1/3) Re Tr U_P>`

be replaced by an exact one-plaquette formula of the form

`P(beta) = P_1plaq(c beta)`

with a fixed lift constant `c`, in particular

`c = (3/2) (2 / sqrt(3))^(1/4)`?

## Exact answer

No.

What is exact is:

1. the pure-gauge plaquette as a source derivative of the Wilson partition
   function
2. the local `SU(3)` one-plaquette block as an exact Toeplitz/Bessel integral
3. the strong-coupling slope

What is ruled out exactly is the proposed constant-lift closure.

The key theorem is:

`dP_full / d beta |_(beta=0) = dP_1plaq / d beta |_(beta=0) = 1/18`.

Therefore any exact identity

`P_full(beta) = P_1plaq(c beta)`

valid on an interval forces

`c = 1`.

So the proposed

`c = (3/2) (2 / sqrt(3))^(1/4) = 1.554921974442116...`

cannot be exact.

## The exact theorem stack

### Theorem 1: pure-gauge source identity

On a finite `3+1` Wilson lattice `Lambda`, define

`P_p(U) = (1/3) Re Tr U_p`

and

`Z_Lambda(beta) = integral dU exp[beta sum_(p in Lambda) P_p(U)]`.

Then the average plaquette is exactly

`P_Lambda(beta) = (1 / N_p) d/d beta log Z_Lambda(beta)`.

This is the exact source-response identity on the gauge side. It does not use
the fermionic determinant source machinery.

### Theorem 2: exact one-plaquette block

For a single plaquette with Wilson weight `exp[(beta/3) Re Tr U]`,

`Z_1plaq(beta) = sum_(m in Z) det[I_(m+i-j)(beta/3)]_(i,j=0..2)`

and

`P_1plaq(beta) = d/d beta log Z_1plaq(beta)`.

This is an exact `SU(3)` group integral. The retained runner cross-checks it
against the independent Weyl-angle integral to machine precision.

At `beta = 6`,

`P_1plaq(6) = 0.422531739649983`.

So the local block is real, but it is not the physical plaquette by itself.

### Theorem 3: exact strong-coupling slope of the full plaquette

Expand the full partition function at small `beta`:

`exp[beta sum_p P_p] = 1 + beta sum_p P_p + O(beta^2)`.

Then

`P_Lambda(beta) = beta sum_p <P_q P_p>_0 + O(beta^2)`

for any tagged plaquette `q`, where `<...>_0` is the `beta = 0` Haar measure.

At order `beta`, every term with `p != q` vanishes because it leaves at least
one unmatched link integral. Only the tagged plaquette survives. Therefore

`P_Lambda(beta) = beta <P_q^2>_0 + O(beta^2)`.

Using

`P_q = (Tr U_q + Tr U_q^dag) / 6`

and Haar orthogonality

`integral dU Tr U Tr U^dag = 1`,

one gets

`<P_q^2>_0 = 1/18`.

So on any finite `3+1` lattice with at least one plaquette,

`P_Lambda(beta) = beta/18 + O(beta^2)`.

Hence

`dP_Lambda / d beta |_(beta=0) = 1/18`.

### Theorem 4: exact strong-coupling slope of the one-plaquette block

The exact one-plaquette determinant has the small-`beta` expansion

`Z_1plaq(beta) = 1 + beta^2 / 36 + O(beta^4)`,

so

`P_1plaq(beta) = d/d beta log Z_1plaq(beta) = beta/18 + O(beta^2)`.

Therefore

`dP_1plaq / d beta |_(beta=0) = 1/18`.

### Corollary: constant-lift closure is impossible unless `c = 1`

Assume

`P_Lambda(beta) = P_1plaq(c beta)`

holds exactly for `beta` in a neighborhood of `0`.

Differentiate at `beta = 0`:

`1/18 = dP_Lambda / d beta |_(0) = c dP_1plaq / d beta |_(0) = c / 18`.

Therefore

`c = 1`.

This kills the proposed closure constant immediately.

## What survives and what does not

The exact local block survives:

- `P_1plaq(6) = 0.422531739649983`
- Weyl-angle and Toeplitz/Bessel evaluations agree to machine precision

The proposed lifted value is only numerically suggestive:

- `c_prop = (3/2) (2 / sqrt(3))^(1/4) = 1.554921974442116`
- `P_1plaq(c_prop * 6) = 0.593530679977098`

That near-hit is real, but it is not an exact theorem because the exact
strong-coupling slope forces `c = 1`.

## Honest frontier

If `P(beta)` is ever to be derived analytically, the derivation has to happen
on the pure-gauge side:

1. exact gauge source identity
2. exact Wilson-loop / plaquette hierarchy
3. exact closure of that hierarchy, or a new physical closure principle stated
   honestly as such

The one-plaquette block is not enough, and the scalar temporal-completion
factor does not close the missing gauge theorem.

The first exact geometric step of that hierarchy is recorded in
`docs/PLAQUETTE_OPEN_SURFACE_HIERARCHY_NOTE.md`: after the area-`1` local
plaquette, the first unavoidable nonlocal completions already appear at area
`5` with multiplicity `4` on the exact `3+1` lattice.

The first constructive finite-order correction is now recorded in
`docs/PLAQUETTE_FIRST_NONLOCAL_CONNECTED_CORRECTION_NOTE.md`: once the exact
local one-plaquette block is factored out, the first nonlocal connected
correction is the area-`5` cube-complement term with coefficient
`1/472392`.

The corrected rooted hierarchy and the exact local obstruction surface are now
recorded in:

- `docs/ROOTED_3CHAIN_COEFFICIENT_ENGINE_NOTE.md`
- `docs/DIRECTED_CELL_BOUNDARY_CLUSTER_THEOREM_NOTE.md`
- `docs/ROOT_FACE_LAUNCH_THEOREM_NOTE.md`
- `docs/DIRECTED_CELL_BOUNDARY_STATE_TRANSFER_NOTE.md`
- `docs/LOCAL_FACE_CLOSURE_REJECTION_NOTE.md`

So the safe package statement is:

`P` is still a same-surface evaluated observable of the `3+1` Wilson gauge
partition function, not an exact analytic output of the current atlas.

The current honest carrier for that evaluated quantity is
`docs/PLAQUETTE_SELF_CONSISTENCY_NOTE.md`.

## Commands run

```bash
python3 scripts/frontier_gauge_plaquette_source_no_go.py
```

Output summary:

- exact checks: `7 pass / 0 fail`
- bounded checks: `1 pass / 0 fail`
- exact no-go: any constant-lift identity `P(beta) = P_1plaq(c beta)` forces
  `c = 1`
