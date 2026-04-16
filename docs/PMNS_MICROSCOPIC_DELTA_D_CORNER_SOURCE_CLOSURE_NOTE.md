# PMNS Microscopic `ΔD` Corner-Source Closure

**Date:** 2026-04-15  
**Script:** `scripts/frontier_pmns_microscopic_delta_d_corner_source_closure.py`  
**Status:** exact reduction of the genuinely new PMNS value-law output to a `5`-real corner-breaking source beyond the already closed seed pair

## Question

After the free microscopic core and weak-axis seed patch are already closed,
what exactly must a genuinely new value law from `Cl(3)` on `Z^3` output in
order to close the PMNS microscopic deformation?

## Answer

Only the `5`-real corner-breaking source on the `hw=1` triplet:

- `xi_1`
- `xi_2`
- `eta_1`
- `eta_2`
- `delta`

together with the already closed seed pair `(xbar, ybar)`.

The missing coordinates `xi_3` and `eta_3` are then fixed by the zero-sum
conditions:

- `xi_3 = -xi_1 - xi_2`
- `eta_3 = -eta_1 - eta_2`

So the full active deformation is reconstructed uniquely as

`ΔD_act
 = diag(xbar*1 + xi - 1)
 + diag(ybar*1 + eta)_delta C`.

## Consequence

Once that `5`-real corner-breaking source is supplied:

- the active microscopic operator is fixed
- the branch-conditioned triplet pair is fixed
- the Hermitian data and quadratic-sheet pair are fixed
- the residual sheet bit is fixed by the active microscopic operator

So after the seed pair, the remaining PMNS closure is algorithmic.

## Meaning

This is the sharpest exact stop condition currently available without
overclaiming a positive law that the retained bank does not yet derive:

the genuinely new law still needed from `Cl(3)` on `Z^3` is **not** another
large matrix family. It is exactly a `5`-real corner-breaking source law on
the `hw=1` generation triplet.

## Verification

```bash
python3 scripts/frontier_pmns_microscopic_delta_d_corner_source_closure.py
```

Expected:

```text
PASS=14  FAIL=0
```
