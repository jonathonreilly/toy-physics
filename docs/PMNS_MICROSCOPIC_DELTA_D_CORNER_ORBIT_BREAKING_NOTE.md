# PMNS Microscopic `ΔD` Corner-Orbit Breaking

**Date:** 2026-04-15  
**Script:** `scripts/frontier_pmns_microscopic_delta_d_corner_orbit_breaking.py`  
**Status:** exact reduction of generic off-seed microscopic `ΔD` to seed data plus a `5`-real corner-orbit breaking carrier

## Question

Once the active PMNS microscopic deformation is known to lie on the exact
carrier

`ΔD_act
 = diag(x_1-1, x_2-1, x_3-1)
 + diag(y_1, y_2, y_3 e^{i delta}) C`,

what exactly remains beyond the already closed weak-axis seed patch?

## Answer

Not another large family.

The generic active off-seed deformation decomposes uniquely into:

- seed data `(xbar, ybar)` with
  - `xbar = (x_1+x_2+x_3)/3`
  - `ybar = (y_1+y_2+y_3)/3`
- breaking data `(xi, eta, delta)` with
  - `x = xbar * 1 + xi`, `sum_i xi_i = 0`
  - `y = ybar * 1 + eta`, `sum_i eta_i = 0`

So the full active family is exactly:

- `2` real seed values
- `5` real off-seed breaking values

because `xi` contributes `2` real zero-sum coordinates, `eta` contributes `2`
real zero-sum coordinates, and `delta` contributes `1` real phase.

## Seed patch

The exact weak-axis seed patch is **precisely** the vanishing locus of the
breaking carrier:

- `xi = 0`
- `eta = 0`
- `delta = 0`

That is why the seed patch is already positively closed while the generic
off-seed law is not.

## Corner-orbit symmetry

The three generations on the retained lepton surface are the exact `hw=1`
corner orbit

- `(π,0,0)`
- `(0,π,0)`
- `(0,0,π)`

and any full corner-permutation invariant value law forces:

- `x_1 = x_2 = x_3`
- `y_1 = y_2 = y_3`
- `delta = 0`

So a fully corner-symmetric law collapses back to the seed patch.

## Consequence

The genuinely new generic microscopic value law still needed from `Cl(3)` on
`Z^3` is now exact in form:

it must be a **corner-orbit symmetry-breaking source law on the `hw=1`
triplet**, and it must fix exactly the `5` real breaking values beyond the
already closed seed data.

This is the sharpest reduction currently available without overclaiming a
positive generic value law that the retained bank does not yet derive.

## Verification

```bash
python3 scripts/frontier_pmns_microscopic_delta_d_corner_orbit_breaking.py
```

Expected:

```text
PASS=17  FAIL=0
```
