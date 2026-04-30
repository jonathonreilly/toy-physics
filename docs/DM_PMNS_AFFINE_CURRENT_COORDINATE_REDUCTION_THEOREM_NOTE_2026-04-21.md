# DM PMNS Affine Current-Coordinate Reduction Theorem

**Date:** 2026-04-21
**Lane:** native/source DM last-mile sharpening
**Status:** support - structural or confirmatory support note
the closure theorem
`DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md`
**Primary runner:**
`scripts/frontier_dm_pmns_affine_current_coordinate_reduction_2026_04_21.py`

---

## 0. Executive summary

The same-day graph-first ordered-chain theorem landed something real:

```text
one explicit sole-axiom nonzero-current law on the retained hw=1 response family.
```

What it did **not** yet settle, at this stage of the same-day theorem stack,
was the physical native/source PMNS last mile.

The reason is now exact on the retained affine Hermitian chart

```text
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q.
```

On that chart the native nontrivial-character current satisfies

```text
J_chi(H) = q_+ - i/4.
```

So:

- `T_m` is current-blind,
- `T_delta` is current-blind,
- `T_q` is read with unit coefficient,
- current activation closes the `q_+` coordinate exactly,
- but it leaves the shifted imaginary doublet-mixing coordinate

  ```text
  delta = (Im K_Z3[1,2] + 4 sqrt(2)/3) / sqrt(3)
  ```

  still open.

Since the physical PMNS target already lives on an exact local `2`-real source
manifold on the fixed native `N_e` seed surface, this means the native/source
DM last mile is now sharper than either of the older descriptions:

- it is **not** a separate target-surface A-BCC residue,
- and it is **not** fully discharged by current activation alone.

At this stage, the honest remaining native object was:

```text
one additional real sole-axiom selector law
for the current-blind delta / Im K_Z3[1,2] direction
on the retained hw=1 response family.
```

---

## 1. Inputs

This sharpening uses only already-landed exact branch theorems.

1. `DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`
   gives one explicit sole-axiom nonzero-current law on the retained `hw=1`
   response family.
2. `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
   gives the exact affine Hermitian chart
   `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`.
3. `DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_POINT_SELECTION_THEOREM_NOTE_2026-04-16.md`
   gives the exact `Z_3` doublet-block readout:

   ```text
   q_+ = 2 sqrt(2)/9 - (K11 + K22)/2,
   delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3).
   ```

4. `DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md`
   gives the exact local `2`-real PMNS source manifold on the fixed native
   `N_e` seed surface.

---

## 2. Exact affine current formula

Let the exact affine basis be

```text
T_m,
T_delta,
T_q.
```

Then the native nontrivial-character current on the affine chart satisfies

```text
J_chi(H_base) = -i/4,
J_chi(T_m) = 0,
J_chi(T_delta) = 0,
J_chi(T_q) = 1.
```

Therefore, by exact affine linearity on the chart,

```text
J_chi(H(m, delta, q_+))
  = J_chi(H_base) + m J_chi(T_m) + delta J_chi(T_delta) + q_+ J_chi(T_q)
  = q_+ - i/4.
```

This is the full chart formula.

So the native current does **not** read the whole affine pair `(delta, q_+)`.
It reads only the centered doublet-trace coordinate `q_+`, together with the
fixed base offset `-i/4`.

---

## 3. Consequence for the remaining native selector

The `Z_3` doublet-block theorem already shows that the remaining microscopic
datum lives entirely in the moving doublet block:

```text
q_+   = 2 sqrt(2)/9 - (K11 + K22)/2,
delta = (Im K12 + 4 sqrt(2)/3) / sqrt(3).
```

The affine current formula above sharpens that further:

- current activation fixes the first of those two coordinates exactly;
- it is blind to the second.

So the graph-first ordered-chain theorem is best read as a genuine **current
activation** theorem, not as the end of the native/source PMNS last mile.

What remained open was not “some generic PMNS law” and not “whether any
nonzero-current law exists.” Those are already narrowed away.

What remained open was:

```text
the native selector law for delta,
equivalently the shifted Im K_Z3[1,2] direction,
after current activation has already fixed q_+.
```

---

## 4. The theorem

> **Theorem (affine current-coordinate reduction).**
>
> Assume:
>
> 1. the exact affine Hermitian PMNS chart,
> 2. the exact `Z_3` doublet-block readout theorem,
> 3. the exact native nontrivial-character current,
> 4. the exact local `2`-real PMNS source-manifold theorem.
>
> Then:
>
> 1. on the affine chart,
>
>    ```text
>    J_chi(H) = q_+ - i/4;
>    ```
>
> 2. current activation therefore fixes the affine `q_+` coordinate exactly;
> 3. the affine `delta` coordinate remains current-blind;
> 4. at this stage of the theorem stack, since the physical PMNS target
>    already lies on an exact local `2`-real source manifold, one additional
>    real sole-axiom selector law is still
>    required beyond current activation.
>
> Equivalently: the remaining native/source DM last mile is the
> `delta / Im K_Z3[1,2]` law, not merely the existence of a nonzero-current
> route.

### Proof sketch

The affine basis values of the current are exact and runner-verified:

```text
J_chi(H_base) = -i/4,
J_chi(T_m) = 0,
J_chi(T_delta) = 0,
J_chi(T_q) = 1.
```

So affine linearity gives

```text
J_chi(H(m, delta, q_+)) = q_+ - i/4.
```

The `Z_3` doublet-block theorem gives independent exact readouts of `q_+` and
`delta`. Since `J_chi` reproduces only the `q_+` readout, it cannot by itself
fix `delta`.

The exact source-manifold theorem already reduces the physical PMNS target to a
local `2`-real source manifold. So after current activation closes one of those
two real coordinates, one real scalar law remains.

QED.

---

## 5. What this changes in the open map

Before this theorem, the native/source DM remainder could still be phrased too
coarsely as:

```text
is the ordered-chain current-activation law the physical PMNS law?
```

After this theorem, the sharper exact statement was:

```text
the ordered-chain theorem closes current activation,
but the current closes only q_+ on the physical affine chart;
the remaining native/source scalar is delta.
```

This was a stronger and cleaner last-mile reduction than the older wording.
The later same-day ordered-chain graded-current closure theorem then closed
that remaining scalar exactly.

---

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_affine_current_coordinate_reduction_2026_04_21.py
```

Expected final line:

```text
SUMMARY: PASS=13 FAIL=0
```
