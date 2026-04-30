# DM PMNS Ordered-Chain Graded-Current Delta Closure Theorem

**Date:** 2026-04-21  
**Lane:** exact-target native/source-map completion
**Status:** support - structural or confirmatory support note
**Primary runner:**  
`scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py`

---

## 0. Executive summary

The exact-target native/source-map last mile had already been reduced to one exact remaining
real object:

```text
after current activation closes q_+,
derive one additional sole-axiom law for the
delta / Im(K_Z3[1,2]) direction
on the retained hw=1 response family.
```

That remaining scalar is now closed.

The graph-first selector, cycle-frame support theorem, and adjacent-chain path
algebra had already fixed the canonical ordered-chain grading

```text
N = diag(1,2,3).
```

Define the ordered-chain graded current

```text
J_N(H) := J_chi(i [N,H]).
```

On the physical affine Hermitian chart

```text
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q
```

this current obeys the exact affine formula

```text
J_N(H) = -1/2 + i (E1/2 - delta/2 - 3 q_+/2),
```

where `E1 = sqrt(8/3)`.

Together with the already-landed affine current law

```text
J_chi(H) = q_+ - i/4,
```

the physical affine active pair is now recovered exactly by

```text
q_+(H) = Re J_chi(H),
delta(H) = E1 - 2 Im J_N(H) - 3 Re J_chi(H).
```

The same two-current law survives exactly after passage to the retained `hw=1`
response columns. So the remaining exact-target native/source-map scalar
last mile is closed on the physical affine/source family.

---

## 1. Inputs

This closure uses only already-landed same-branch structures.

1. `DM_PMNS_GRAPH_FIRST_ORDERED_CHAIN_NONZERO_CURRENT_ACTIVATION_THEOREM_NOTE_2026-04-21.md`
   fixes the canonical ordered-chain grading
   `N = diag(1,2,3)` from the graph-first selector, cycle frame, and
   adjacent-chain algebra.
2. `DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md`
   gives the exact physical affine chart

   ```text
   H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q.
   ```

3. `DM_PMNS_AFFINE_CURRENT_COORDINATE_REDUCTION_THEOREM_NOTE_2026-04-21.md`
   gives the exact affine current law

   ```text
   J_chi(H) = q_+ - i/4.
   ```

So only one additional real law remained.

---

## 2. Canonical graded current

Let

```text
N = diag(1,2,3)
```

be the canonical ordered-chain grading.

Define the graded current

```text
J_N(H) := J_chi(i [N,H]).
```

This is still a sole-axiom graph-first object:

- `N` is fixed by the ordered chain;
- `J_chi` is the already-landed native nontrivial-character current;
- no PMNS target values enter its definition.

---

## 3. Exact affine basis values

On the physical affine basis one has:

```text
J_N(H_base)   = -1/2 + i E1/2,
J_N(T_m)      = 0,
J_N(T_delta)  = - i/2,
J_N(T_q)      = - 3 i/2.
```

Therefore affine linearity gives the full chart formula

```text
J_N(H(m, delta, q_+))
  = J_N(H_base) + m J_N(T_m) + delta J_N(T_delta) + q_+ J_N(T_q)
  = -1/2 + i (E1/2 - delta/2 - 3 q_+/2).
```

This is exact.

---

## 4. The affine pair closes exactly

The earlier affine current theorem already gave:

```text
J_chi(H) = q_+ - i/4.
```

So

```text
q_+(H) = Re J_chi(H).
```

Now use the graded-current formula:

```text
Im J_N(H) = E1/2 - delta/2 - 3 q_+/2.
```

Substituting `q_+ = Re J_chi(H)` yields

```text
delta(H) = E1 - 2 Im J_N(H) - 3 Re J_chi(H).
```

Hence the full physical affine active pair is recovered natively from the
ordered-chain current pair:

```text
(delta, q_+)  <->  (J_N, J_chi).
```

So the graph-first current-activation theorem plus this graded-current closure
now determine the entire physical affine point-selection pair.

---

## 5. The theorem

> **Theorem (ordered-chain graded-current delta closure).**
>
> Assume:
>
> 1. the graph-first ordered-chain current-activation theorem;
> 2. the exact affine Hermitian source chart;
> 3. the affine current-coordinate reduction theorem.
>
> Then:
>
> 1. the ordered-chain graded current
>
>    ```text
>    J_N(H) := J_chi(i [N,H])
>    ```
>
>    is a sole-axiom graph-first scalar law on the physical affine/source
>    family;
> 2. on the affine chart it satisfies
>
>    ```text
>    J_N(H) = -1/2 + i (E1/2 - delta/2 - 3 q_+/2);
>    ```
>
> 3. together with
>
>    ```text
>    J_chi(H) = q_+ - i/4,
>    ```
>
>    it recovers the full physical affine active pair exactly:
>
>    ```text
>    q_+(H) = Re J_chi(H),
>    delta(H) = E1 - 2 Im J_N(H) - 3 Re J_chi(H);
>    ```
>
> 4. the same recovery survives exactly on the retained `hw=1` response family.
>
> Therefore no exact-target native/source-map last-mile residue remains on the physical
> affine/source family.

### Proof sketch

The graph-first ordered-chain theorem fixes `N = diag(1,2,3)` canonically.

The runner verifies the basis values

```text
J_N(H_base) = -1/2 + i E1/2,
J_N(T_m) = 0,
J_N(T_delta) = -i/2,
J_N(T_q) = -3i/2,
```

which immediately imply the affine formula above.

The earlier affine current theorem gives the exact `q_+` readout. Solving the
imaginary part of the graded current for `delta` then gives the exact
recovery law.

The same formulas are verified again after reconstruction from retained
`hw=1` response columns, so the law survives on the actual response-family
carrier rather than only on an abstract affine chart.

QED.

---

## 6. Consequence for the open map

Before this theorem, the honest exact-target native/source-map wording was:

```text
current activation closes q_+,
but one additional real delta / Im(K_Z3[1,2]) law remains.
```

After this theorem, that residual is gone.

The current-package DM lane was already closed. Now the exact-target
native/source map is closed too: the same graph-first ordered-chain structure
supplies both native currents needed to recover the full physical affine
point-selection pair on the retained `hw=1` response family.

---

## 7. What this does not touch

This theorem does **not** address:

- the charged-lepton Koide open bridges,
- the downstream lepton scale lane,
- the quark bounded endpoint/readout lane.

It is only the DM exact-target native/source-map last-mile closure.

---

## 8. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_ordered_chain_graded_current_delta_closure_2026_04_21.py
```

Expected:

```text
SUMMARY: PASS=17 FAIL=0
```
