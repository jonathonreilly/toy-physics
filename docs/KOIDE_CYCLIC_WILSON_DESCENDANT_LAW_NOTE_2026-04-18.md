# Koide Cyclic Wilson-Descendant Law

**Date:** 2026-04-18
**Status:** constructive law on the charged-lepton Koide lane
**Runner:** `scripts/frontier_koide_cyclic_wilson_descendant_law.py`

## Question

The previous Koide Wilson target was already narrowed to the right size:

- not a generic `9`-real Hermitian reconstruction first,
- but the `3`-real `C_3[111]`-covariant Hermitian family
  `a I + b C + b* C^2`,
- followed by one scalar selector equation.

That still left one missing constructive step:

> what is the **actual cyclic Wilson descendant law** on the local adjacent-chain
> algebra, written explicitly rather than only as a target shape?

## Bottom line

The law is now explicit.

Let
```
B0 = I,
B1 = C + C^2,
B2 = i(C - C^2),
```
where `C` is the retained forward cycle on the charged-lepton triplet.

These three Hermitian elements already lie in the local adjacent-chain path
algebra. Given any local Wilson first-variation law `dW_W` on the Hermitian
image of that algebra, its cyclic descendant is determined by the three real
responses
```
r0 = dW_W(B0),
r1 = dW_W(B1),
r2 = dW_W(B2).
```

Those three numbers reconstruct the unique cyclic Hermitian target
```
H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2.
```

So the "cyclic Wilson descendant law" is not vague anymore. It is exactly a
`3`-response law.

Inside that law, Koide is one scalar equation:
```
2 r0^2 = r1^2 + r2^2.
```

That is the sharp constructive statement we needed.

## Why this is the right positive move

The generic DM Wilson notes already proved:

- one adjacent-chain path algebra generates all of `Herm(3)`,
- the generic Wilson-to-`dW_e^H` route can be packaged as one local minimal
  certificate.

For Koide, we do not need the whole `9`-real generic codomain first. The
charged-lepton Koide lane lives in the cyclic `3`-real subfamily. So the right
constructive reduction is:

1. project the local chain algebra to its cyclic `C_3[111]` sector;
2. read off the three cyclic Wilson responses `(r0, r1, r2)`;
3. impose one scalar selector relation.

That is now done exactly.

## The cyclic basis inside the adjacent-chain algebra

From the local adjacent two-edge chain:
```
E12, E23
```
and adjoints, one already generates the long corners
```
E13 = E12 E23,
E31 = E32 E21.
```

Therefore the forward and backward cycles are already present:
```
C   = E21 + E32 + E13,
C^2 = E12 + E23 + E31.
```

Hence all three cyclic Hermitian generators lie in the same local path algebra:
```
B0 = E11 + E22 + E33,
B1 = C + C^2,
B2 = i(C - C^2).
```

Equivalently:
```
B2 = Y12 + Y23 - Y13.
```

So one local adjacent-chain embedding already contains the entire Koide carrier.

## The canonical cyclic projector

Define the `C_3` average
```
P_cyc(X) = (1/3) Σ_{k=0}^2 C^k X C^{-k}.
```

Then:

- `P_cyc` is idempotent;
- its image is exactly the cyclic `3`-real Hermitian space
  `span_R{B0, B1, B2}`;
- every projected Hermitian is reconstructed uniquely from the three real trace
  responses against `B0, B1, B2`.

The runner verifies the basis is orthogonal for the real trace pairing:
```
Re Tr(B0^2) = 3,
Re Tr(B1^2) = 6,
Re Tr(B2^2) = 6,
Re Tr(Bi Bj) = 0  for i != j.
```

That is why the reconstruction formula is so simple:
```
H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2.
```

## The actual cyclic Wilson-descendant law

This is the constructive theorem:

> any local Wilson first variation on the adjacent-chain image descends
> canonically, after cyclic projection, to exactly three real cyclic responses
> `(r0, r1, r2)`, and those three responses reconstruct the unique cyclic
> charged-lepton target `H_cyc`.

So the Wilson task is no longer:

- derive some large unknown matrix law.

It is now:

- derive exactly the three cyclic response channels
  `(r0, r1, r2)`.

## Koide as one scalar selector equation

Write the cyclic target as
```
H_cyc = a B0 + x B1 + y B2.
```

Because
```
a = r0/3,
x = r1/6,
y = r2/6,
```
the Koide cone condition
```
a^2 = 2(x^2 + y^2)
```
becomes
```
2 r0^2 = r1^2 + r2^2.
```

This is the sharpest form of the selection problem on the Wilson side.

Instead of "select a full mass matrix," the positive next target is:

> derive three cyclic Wilson responses satisfying one circle law.

## Observed charged-lepton witness

The observed charged-lepton amplitude operator built from the PDG
`√m = (√m_e, √m_μ, √m_τ)` spectrum satisfies this law exactly to Koide
precision.

Its cyclic responses obey
```
(r1^2 + r2^2) / (2 r0^2) = 1.000018...
```
and its spectrum reconstructs the observed `√m` triple.

So the law is not just algebraically neat. It already matches the actual
charged-lepton target.

## What this changes

This closes the missing constructive step between:

- "the cyclic target is the right size,"
and
- "what exactly should we derive on the Wilson side?"

The answer is now explicit:

1. derive the three cyclic Wilson responses `(r0, r1, r2)`,
   equivalently derive the full charged Hermitian source law and apply the
   exact compression theorem in
   [KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md](./KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md),
2. derive the single selector equation
   ```
   2 r0^2 = r1^2 + r2^2,
   ```
3. then attach the remaining scale/readout interpretation.

## What this does not yet close

This note does **not** yet derive:

- the microscopic Wilson law producing `(r0, r1, r2)`,
- the selector mechanism enforcing `2 r0^2 = r1^2 + r2^2`,
- the final retained readout primitive.

But it does fix the exact constructive law those future derivations must hit.

## Bottom line

The sharp next move is no longer just a slogan.

The actual charged-lepton Koide Wilson descendant law is:

- three cyclic responses on `B0 = I`, `B1 = C + C^2`, `B2 = i(C - C^2)`,
- reconstructing the unique cyclic Hermitian target,
- with Koide imposed by the single scalar equation
  `2 r0^2 = r1^2 + r2^2`.
