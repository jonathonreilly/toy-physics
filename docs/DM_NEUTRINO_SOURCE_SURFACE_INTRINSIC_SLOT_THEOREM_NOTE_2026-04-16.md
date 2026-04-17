# DM Neutrino Source-Surface Intrinsic Slot Theorem

**Date:** 2026-04-16  
**Status:** exact mainline blocker-reduction theorem on the live source-oriented sheet  
**Script:** `scripts/frontier_dm_neutrino_source_surface_intrinsic_slot_theorem.py`

## Question

Once the live source-oriented `H`-side bundle is reduced to the explicit
shift-quotient bundle, what intrinsic `Z_3` singlet-doublet slot pair does the
canonical positive section read from that bundle?

## Bottom line

The intrinsic slot pair is already exact and constant on the whole live
source-oriented bundle:

- `a_* = E2/3 - sqrt(3) gamma/6 + i(E2 + gamma/2)`
- `b_* = E2/3 + sqrt(3) gamma/6 + i(gamma/2 - E2)`

with the exact source-oriented values

- `gamma = 1/2`
- `E2 = sqrt(8)/3`

equivalently

- `a_* = 2 sqrt(2)/9 - sqrt(3)/12 + i(1/4 + 2 sqrt(2)/3)`
- `b_* = 2 sqrt(2)/9 + sqrt(3)/12 + i(1/4 - 2 sqrt(2)/3)`

So the live mainline object no longer includes any open intrinsic slot/readout
law on the source-oriented sheet. What remains is only the post-canonical
`H`-side law selecting a point on the explicit shift-quotient bundle.

## Exact content

### 1. The slot readout descends to the shift quotient

The intrinsic slot pair on the positive section is read from

- `K_Z3(H) = U_Z3^dag H U_Z3`

through the off-diagonal singlet-doublet slots

- `a(H) = (K_Z3(H))_01`
- `b(H) = (K_Z3(H))_02`.

Adding a common diagonal shift

- `H -> H + lambda I`

changes only diagonal entries of `K_Z3(H)`. So the intrinsic slot pair is
shift-invariant and therefore descends to the explicit shift-quotient bundle.

### 2. The live source-oriented quotient bundle collapses to one exact pair

On the quotient gauge

- `d1 = m`
- `d2 = delta`
- `d3 = -delta`
- `phi_+(r31) = asin(1 / (2 r31))`
- `r12 = 2 sqrt(8/3) - 2 delta + r31 cos(phi_+)`
- `r23 = m - delta + sqrt(8/3) - sqrt(8)/3 + r31 cos(phi_+)`

the intrinsic slot pair simplifies exactly to the constant pair above. The
quotient-bundle coordinates

- `m`
- `delta`
- `r31`

drop out of `a(H)` and `b(H)` completely on the live source-oriented sheet.

### 3. Positive representatives carry the same pair and the same CP data

Every quotient point has a positive representative after adding a sufficiently
large common diagonal shift. Since the slot pair is shift-invariant, all such
positive representatives carry the same exact pair `(a_*, b_*)`.

The exact source-oriented CP pair is therefore already encoded by that same
constant intrinsic slot pair via

- `Im[((a_* - b_*) / sqrt(2))^2]`
- `Im[((a_* + b_*) / sqrt(2))^2]`

and reproduces the exact source-oriented package.

## Consequence

The live mainline object is now sharper again.

It is **not**:

- a missing triplet-value law
- a missing source-surface law
- a missing quotient-bundle law
- a missing intrinsic slot/readout law on that bundle

It is only the post-canonical `H`-side law that selects a point on the
explicit shift-quotient bundle.

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_intrinsic_slot_theorem.py
```
