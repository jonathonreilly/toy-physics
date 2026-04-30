# DM PMNS Native Current Last-Mile Reduction Theorem

**Date:** 2026-04-21
**Lane:** native/source DM last-mile sharpening
**Status:** support - structural or confirmatory support note
later same-day affine sharpening and ordered-chain graded-current closure
theorems complete the physical native/source last mile
**Positive activation theorem:**
`docs/DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`
**Primary runner:**
`scripts/frontier_dm_pmns_native_current_last_mile_reduction_2026_04_21.py`

---

## 0. Executive summary

The native/source DM map is now sharper than:

```text
derive the PMNS angle triple somehow.
```

Two same-branch reductions now compose:

1. the exact target-surface source-cubic theorem removes any separate
   target-surface A-BCC residue;
2. the native `C_3` character/current theorems identify the remaining PMNS
   value problem with one exact complex current.

The reduced-carrier result is:

> on the reduced graph-first carrier, the remaining PMNS value datum is one
> exact complex current
>
> ```text
> J_chi(A) = (h_0 + omega h_1 + omega^2 h_2) / 3
> ```
>
> on the retained `hw=1` response family.

Equivalently:

- the old separate A-BCC branch-choice residue is gone once the exact PMNS
  target surface is granted;
- the old vague PMNS-angle residue is now the intrinsic `2`-real law carried
  by
  `Re J_chi` and `Im J_chi`.

So the reduced graph-first object is not "the PMNS angle triple" in an
undifferentiated sense. It reduces to one native complex
nontrivial-character current. The graph-first ordered-chain theorem now lands
one explicit sole-axiom nonzero-current law on that reduced target.

The later same-day affine sharpening theorem
`DM_PMNS_AFFINE_CURRENT_COORDINATE_REDUCTION_THEOREM_NOTE_2026-04-21.md`
showed that on the physical affine Hermitian chart this current reads only the
`q_+` coordinate:

```text
J_chi(H) = q_+ - i/4.
```

The later same-day closure theorem
`DM_PMNS_ORDERED_CHAIN_GRADED_CURRENT_DELTA_CLOSURE_THEOREM_NOTE_2026-04-21.md`
then closes that remaining affine scalar exactly by the ordered-chain graded
current.

---

## 1. Inputs

### 1.1 Exact target-surface branch reduction

The note

`DM_ABCC_EXACT_TARGET_SURFACE_SOURCE_CUBIC_CLOSURE_THEOREM_NOTE_2026-04-21.md`

proves:

- the active-half-plane chamber is exact on the source side;
- on the exact `chi^2 = 0` PMNS target surface, the chamber roots are exactly
  `{Basin 1, Basin 2, Basin X}`;
- on those roots, the coefficient-free source cubic `I_src(H) > 0` selects
  `Basin 1` uniquely.

So there is no longer a separate target-surface A-BCC residue once the exact
PMNS target surface is fixed.

### 1.2 Exact local `2`-real PMNS source manifold

The note

`DM_PMNS_NE_SEED_SURFACE_EXACT_SOURCE_MANIFOLD_THEOREM_NOTE_2026-04-20.md`

proves that the physical PMNS target already lies on an exact local `2`-real
regular source manifold on the fixed native `N_e` seed surface.

So the remaining native burden is a `2`-real point-selection law.

### 1.3 Native `C_3` current reduction

The notes

- `PMNS_C3_CHARACTER_HOLONOMY_CLOSURE_NOTE.md`
- `PMNS_C3_CHARACTER_MODE_REDUCTION_NOTE.md`
- `PMNS_C3_NONTRIVIAL_CURRENT_BOUNDARY_NOTE.md`

prove:

- the reduced graph-first PMNS cycle values admit an exact native
  `C_3`-character holonomy readout;
- on the reduced graph-first family

  ```text
  A_fwd(u,v,w) = (u + i v) E12 + w E23 + (u - i v) E31,
  ```

  the remaining nontrivial value datum is exactly one complex amplitude

  ```text
  chi = u + i v;
  ```

- the native nontrivial-character current satisfies

  ```text
  J_chi = chi.
  ```

So the reduced PMNS value problem is exactly `2` real dimensions, carried by
one complex current.

---

## 2. The theorem

> **Theorem (reduced graph-first native PMNS last mile reduces to one complex
> current).**
>
> Assume:
>
> 1. the exact target-surface source-cubic theorem;
> 2. the exact local `2`-real PMNS source-manifold theorem;
> 3. the native `C_3` character holonomy closure;
> 4. the native `C_3` character-mode reduction;
> 5. the native nontrivial-character current boundary theorem.
>
> Then:
>
> 1. no separate native/source A-BCC branch-choice residue remains once the
>    exact PMNS target surface is granted;
> 2. the remaining native/source PMNS value problem is exactly `2` real
>    dimensional;
> 3. that `2`-real datum is carried natively by one complex current
>
>    ```text
>    J_chi(A) = (h_0 + omega h_1 + omega^2 h_2) / 3;
>    ```
>
> 4. on the reduced graph-first family,
>
>    ```text
>    J_chi = u + i v,
>    ```
>
>    so `Re J_chi` and `Im J_chi` are exactly the remaining `2` real degrees of
>    freedom;
> 5. the current sole-axiom retained routes still set
>
>    ```text
>    J_chi = 0.
>    ```
>
> Therefore the reduced graph-first carrier burden is exactly:
>
> ```text
> derive a sole-axiom law producing nonzero J_chi
> on the retained hw=1 response family.
> ```
>
> A positive same-branch current-activation theorem now supplies one explicit
> sole-axiom nonzero-current law on that reduced target.

### Proof sketch

The first point is exactly the content of the target-surface source-cubic
theorem: once the exact target surface is fixed, the chamber plus
`I_src(H) > 0` select `Basin 1` uniquely.

The second point is exactly the content of the exact source-manifold theorem:
the physical PMNS target fiber is a local `2`-real manifold.

The third and fourth points are exactly the content of the native
`C_3` character-mode reduction and nontrivial-current boundary notes:
the reduced PMNS data are already natively read by character holonomies,
and the remaining nontrivial value datum is one complex current
`J_chi = u + i v`.

The fifth point is exactly the content of the nontrivial-current boundary on
the current sole-axiom retained bank: the free route, the sole-axiom
`hw=1` source/transfer route, and the retained scalar route all annihilate
`J_chi`.

So the exact remaining reduced-carrier DM object is no longer a separate A-BCC
law plus a vague PMNS angle-triple law. It is one complex current whose
nonzero activation was the current constructive subtarget.

The later affine current-coordinate theorem sharpened the physical
native/source last mile one step further, and the later ordered-chain
graded-current closure theorem then closed the remaining affine `delta`
direction exactly.

QED.

---

## 3. Consequence for the open map

Before this theorem, the native/source DM burden could still be summarized too
coarsely as:

```text
target-surface branch choice + PMNS angle triple.
```

After this theorem, the reduced-carrier exact statement is:

```text
no separate target-surface branch-choice residue remains;
the reduced graph-first remaining datum is one complex native current J_chi.
```

This is equivalent to a `2`-real reduced-carrier point-selection law, but it is
now expressed in native current language rather than as a generic angle target.
The graph-first ordered-chain theorem gives one explicit same-branch
activation of that current. The later affine sharpening theorem identified the
remaining real scalar, and the later ordered-chain graded-current closure
theorem closed it.

---

## 4. What this does not close

This note does **not** derive:

- the Koide-side open bridges;
- the broader full-neutrino pair `(J_chi, mu)` outside the flagship DM scope.

It is a reduced-carrier reduction theorem only.

---

## 5. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_native_current_last_mile_reduction_2026_04_21.py
```

Expected final line:

```text
SUMMARY: PASS=17 FAIL=0
```
