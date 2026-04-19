# PMNS Local Scalar Deformation Boundary

**Date:** 2026-04-16  
**Status:** exact negative extension theorem  
**Script:** `scripts/frontier_pmns_local_scalar_deformation_boundary.py`

## Question

If we admit the retained lowest-order local scalar field from the current
architecture, can that route by itself generate the nontrivial retained PMNS
triplet structure?

## Answer

No.

The projected commutative local scalar algebra on the retained `hw=1`
generation triplet is exactly the **diagonal algebra**. Therefore any local
scalar deformation on the retained lepton surface produces only diagonal
triplet blocks. The induced lower-level response profiles remain diagonal, and
the live retained PMNS closure stack rejects that whole route.

So the retained lowest-order local scalar field cannot by itself generate the
PMNS-active non-monomial triplet structure.

## Exact chain

### 1. Projected local scalar algebra is diagonal

Take the commutative graph algebra `C(V)` on the 8-site unit cell, i.e. the
8 diagonal site projectors.

Project those diagonal operators onto the retained `hw=1` triplet

- `(1,0,0)`
- `(0,1,0)`
- `(0,0,1)`.

The projected span has exact dimension `3`, and the surviving basis elements are
just the diagonal matrix units on the triplet. No off-diagonal cycle channels
survive this projection.

### 2. Any local scalar field gives only diagonal triplet blocks

Any local scalar field `Phi(x)` acts by multiplication, hence is diagonal in the
site basis. Since the projected scalar algebra is diagonal, its retained
triplet block is always

`diag(u_1, u_2, u_3)`.

So even a nonuniform local scalar field can only split the three generation
corners diagonally. It cannot produce the PMNS-active cyclic channels.

### 3. Lower-level response profiles stay diagonal

Feeding such diagonal triplet blocks into the lower-level response formulas
produces diagonal response-column matrices again. The active cycle-channel data
stay zero.

### 4. Retained PMNS closure rejects the whole local-scalar route

The retained lower-level PMNS closure stack requires a **one-sided minimal PMNS
class**, meaning exactly one sector must carry the canonical non-monomial active
support.

But diagonal local-scalar data give:

- no active support `I + C`
- no cycle-channel source data
- no one-sided minimal PMNS class

So the live retained PMNS closure stack rejects that whole route exactly.

## Consequence

This is stronger than the uniform scalar / Coleman-Weinberg boundary.

That earlier theorem said:

> the translation-invariant scalar/Coleman-Weinberg route only rescales the
> free point.

This theorem says:

> the entire retained lowest-order local scalar-field route only produces
> diagonal generation splitting on the retained triplets, and therefore still
> cannot realize PMNS-active structure.

So the next positive lane, if one exists, is no longer “a scalar deformation
law.” It has to be a genuinely non-scalar deformation on the retained lepton
triplets.

## Boundary

This note closes the **local scalar-field route** on the retained PMNS lane.

It does **not** rule out:

- a non-scalar deformation law,
- a route that leaves the retained one-sided minimal class,
- or a different extension of the microscopic lepton dynamics.

## Command

```bash
python3 scripts/frontier_pmns_local_scalar_deformation_boundary.py
```
