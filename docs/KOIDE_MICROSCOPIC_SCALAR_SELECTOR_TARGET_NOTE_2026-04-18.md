# Koide Microscopic Scalar Selector Target

**Date:** 2026-04-18  
**Status:** exact sharpening of the remaining charged-lepton Koide target to one
microscopic scalar selector law  
**Runner:** `scripts/frontier_koide_microscopic_scalar_selector_target.py`

## Question

The charged-lepton Koide lane has already been reduced to:

1. the exact compressed cyclic responses `(r0, r1, r2)` of `dW_e^H`;
2. the exact scalar bridge
   `kappa = sqrt(3) r2 / (2 r0 - r1) = (v-w)/(v+w)`;
3. the exact positive selected line
   `H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3)`;
4. threshold continuity plus first-branch monotonicity.

What exact microscopic object is still missing on the charged-lepton side?

## Bottom line

It is one scalar.

More precisely:

1. `kappa` is exactly one ratio of the compressed `dW_e^H` coordinates,
2. on the selected slice `delta = q_+ = sqrt(6)/3`, the remaining microscopic
   datum is exactly the one-real `Z_3` doublet-block coordinate
   `m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3`,
3. the current exact source/slot/CP invariants are blind to that scalar,
4. on the positive first branch, `kappa(m)` is strictly monotone.

So the charged-lepton finish line is no longer “derive a parent,” “derive a
generic readout,” or even “derive a full selected point.” It is:

```text
derive one microscopic scalar selector law.
```

## Input stack

This note sharpens:

1. [KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md](./KOIDE_DWEH_CYCLIC_COMPRESSION_NOTE_2026-04-18.md)
2. [KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md](./KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md)
3. [KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md](./KOIDE_GAMMA_ORBIT_OBSERVABLE_SELECTOR_GENERATOR_LINE_NOTE_2026-04-18.md)
4. [DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md)
5. [DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_M_SPECTATOR_THEOREM_NOTE_2026-04-16.md)
6. [KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md](./KOIDE_SELECTED_SLICE_FROZEN_BANK_DECOMPOSITION_NOTE_2026-04-18.md)

## Theorem 1: `kappa` is exactly one ratio of the compressed `dW_e^H` data

Write the generic charged Hermitian block as

```text
H_e =
  d1 D1 + d2 D2 + d3 D3
+ x12 X12 + x23 X23 + x13 X13
+ y12 Y12 + y23 Y23 + y13 Y13.
```

The exact cyclic compression theorem gives

```text
r0 = d1 + d2 + d3,
r1 = 2 (x12 + x23 + x13),
r2 = 2 (y12 + y23 - y13).
```

So the bridge scalar is exactly

```text
kappa = sqrt(3) r2 / (2 r0 - r1)
      = sqrt(3) (y12 + y23 - y13)
        / (d1 + d2 + d3 - x12 - x23 - x13).
```

So the remaining charged-lepton bridge is not a whole matrix witness anymore. It
is one ratio of two exact cyclic sums in the compressed `dW_e^H` law.

## Theorem 2: on the selected slice, the remaining microscopic datum is one `Z_3` scalar

The exact affine source-surface chart is

```text
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q.
```

The exact observable-selector slice already fixes

```text
delta = q_+ = sqrt(6)/3.
```

So the charged-lepton selected line is exactly

```text
H_sel(m) = H(m, sqrt(6)/3, sqrt(6)/3).
```

In the exact `Z_3` basis, the doublet-block point-selection theorem gives

```text
K11 = -q_+ + 2 sqrt(2)/9 - 1/(2 sqrt(3)),
K22 = -q_+ + 2 sqrt(2)/9 + 1/(2 sqrt(3)),
K12 = m - 4 sqrt(2)/9 + i (sqrt(3) delta - 4 sqrt(2)/3).
```

On the selected slice this becomes

```text
K11 = const,
K22 = const,
Im K12 = -sqrt(2)/3,
Re K12 = m - 4 sqrt(2)/9.
```

So every doublet-block coordinate is frozen except one scalar:

```text
m = Re K12 + 4 sqrt(2)/9 = Tr K_Z3.
```

That is the exact remaining microscopic datum on the selected slice.

The companion frozen-bank decomposition note sharpens this one step further:
the entire selected kernel is already
```text
K_Z3^sel(m) = K_frozen + m T_m^(K)
```
over the exact frozen slot/CP bank. So the remaining charged-lepton datum is
not just "one scalar somewhere in the block"; it is the coefficient of one
fixed real direction.

## Corollary 1: current exact invariants cannot choose it

The exact `m`-spectator theorem already proves that the current source-facing
mainline invariants are blind to `m`:

- the intrinsic slot pair `(a_*, b_*)` is constant,
- the intrinsic CP pair is constant,
- the exact source package is constant.

The selected charged-lepton slice sits inside the same affine chart, so those
current invariants also remain blind to the selected-line scalar.

Therefore the missing charged-lepton selector really is microscopic. It cannot
be recovered by repackaging the current slot / CP / source bank.

## Theorem 3: on the positive first branch, `kappa(m)` is one-to-one

The selected one-clock block gives the exact reachable slots

```text
v(m) = [exp(H_sel(m))]_(110,110),
w(m) = [exp(H_sel(m))]_(101,101),
```

and hence

```text
kappa(m) = (v(m) - w(m)) / (v(m) + w(m)).
```

On the first positive branch:

- positivity starts at one exact threshold
  `m_pos ~= -1.295794904067`,
- at that threshold
  `kappa_pos = -1/sqrt(3)`,
- numerically `kappa(m)` is strictly monotone all the way to `m = 0`.

So on the physical first branch,

```text
m  <->  kappa
```

is one-to-one.

Therefore a retained microscopic selector law for either of the following is
already enough:

- `m`,
- `Re K12`,
- `Tr K_Z3`,
- `kappa`,
- the compressed `dW_e^H` ratio
  `sqrt(3) (y12 + y23 - y13) / (d_sum - x_sum)`.

They are all the same remaining charged-lepton selection problem on the current
route.

## Why this matters

This is the sharpest honest charged-lepton endpoint now in the tree:

- the Koide lane is not waiting on a generic matrix law,
- it is not waiting on a free selected point in a three-real chart,
- it is not even waiting on the whole `2`-real `Z_3` point-selection law,
- because the charged-lepton selector slice already fixed `delta = q_+`,
- it is waiting only on the one remaining microscopic scalar on that slice.

That is a real narrowing.

## Consequence

Charged leptons are still not fully retained-closed.

But the exact remaining positive target is now as small as it can honestly be:

```text
one microscopic scalar selector law.
```

Equivalently:

- one selected-slice `Z_3` doublet-block scalar,
- one cyclic compressed `dW_e^H` ratio,
- one charged-lepton `kappa` law.

Everything downstream of that scalar is already fixed by the present exact stack.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_koide_microscopic_scalar_selector_target.py
```
