# DM A-BCC Exact Target-Surface Source-Cubic Closure Theorem

**Date:** 2026-04-21  
**Lane:** strict/native DM A-BCC sharpening  
**Status:** exact target-surface closure theorem. Once the exact PMNS target
surface is granted, no separate native branch-choice residue remains: the
active half-plane chamber is already exact on the source side, the exact
target-surface chamber roots are exactly `{Basin 1, Basin 2, Basin X}`, and
the coefficient-free source cubic `I_src(H) > 0` selects `Basin 1` uniquely.
So the remaining strict/native DM burden is not a separate A-BCC sign law; it
is the PMNS angle triple itself.  
**Boundary:** this does **not** contradict the global sign-blindness audit.
Outside the exact target chamber root set, `I_src(H)` does **not** determine
`det(H)` globally: `Basin N` and `Basin P` remain explicit counterexamples.
This is therefore a target-surface theorem, not a pure `Cl(3)/Z^3` sign law on
all of source space.  
**Primary runner:**  
`scripts/frontier_dm_abcc_exact_target_surface_source_cubic_closure_2026_04_21.py`

---

## 0. Executive summary

The strict/native DM map had been carrying one residual A-BCC caveat:

> even though the review-surface gate is closed, does a separate native
> branch-choice / source-chart problem still remain outside the PMNS angle
> triple itself?

This note answers:

> **No, once the exact target surface is fixed.**

Three same-branch theorems now compose directly:

1. the active-half-plane theorem gives the source-side chamber exactly as

   ```text
   q_+ >= sqrt(8/3) - delta;
   ```

2. the basin-enumeration completeness theorem gives the exact target-surface
   `chi^2 = 0` basin chart

   ```text
   {Basin 1, Basin N, Basin P, Basin 2, Basin X},
   ```

   with chamber survivors exactly

   ```text
   {Basin 1, Basin 2, Basin X};
   ```

3. on those exact chamber roots, the coefficient-free source cubic

   ```text
   I_src(H) := Im(H_12 H_23 H_31)
   ```

   has signs

   ```text
   I_src(Basin 1) > 0,
   I_src(Basin 2) < 0,
   I_src(Basin X) < 0.
   ```

So on the exact target chamber root set:

```text
I_src(H) > 0   <=>   Basin 1.
```

Since `det(H)` is also positive exactly on Basin 1 and negative on Basin 2 and
Basin X, A-BCC follows on that target surface without any extra retained
measurement pin beyond the PMNS angle triple that defines the target surface
itself.

That is the real scientific reduction:

- A-BCC no longer survives as a separate strict/native blocker;
- the remaining strict/native DM content is just the PMNS angle triple.

---

## 1. Setup

Take the exact active affine Hermitian family

```text
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q
```

with fixed exact source package

```text
gamma = 1/2,
E1 = sqrt(8/3),
E2 = sqrt(8)/3.
```

Let

```text
I_src(H) = Im(H_12 H_23 H_31).
```

Let the exact target-surface basin chart be the retained `chi^2 = 0`
PMNS-compatible source chart from the basin-enumeration completeness theorem:

| Basin | `(m, delta, q_+)` | chamber? | `det(H)` |
|---|---|---|---:|
| Basin 1 | `(0.657061, 0.933806, 0.715042)` | IN | `+0.959...` |
| Basin N | `(0.501997, 0.853543, 0.425916)` | OUT | `+0.566...` |
| Basin P | `(1.037883, 1.433019, -1.329548)` | OUT | `-9.860...` |
| Basin 2 | `(28.006..., 20.722..., 5.012...)` | IN | `-7.05e4` |
| Basin X | `(21.128264, 12.680028, 2.089235)` | IN | `-2.03e4` |

The active-half-plane theorem says the source-side chamber is exactly

```text
q_+ >= sqrt(8/3) - delta.
```

So the chamber cut is exact source geometry, not extra branch bookkeeping.

---

## 2. The theorem

> **Theorem (exact target-surface source-cubic closure of A-BCC).**
>
> Assume:
>
> 1. the exact active-half-plane theorem on the live source-oriented sheet,
>    giving the native chamber
>    `q_+ >= sqrt(8/3) - delta`;
> 2. the retained basin-enumeration completeness theorem on the exact PMNS
>    target surface;
> 3. the coefficient-free source-cubic law
>    `I_src(H) = Im(H_12 H_23 H_31)`.
>
> Then on the exact target-surface chamber root set:
>
> ```text
> {Basin 1, Basin 2, Basin X},
> ```
>
> the source-cubic sign selects Basin 1 uniquely:
>
> ```text
> I_src(Basin 1) > 0,
> I_src(Basin 2) < 0,
> I_src(Basin X) < 0.
> ```
>
> Hence on the exact target surface, A-BCC is already downstream of the native
> chamber plus the coefficient-free source-cubic law. No separate native
> branch-choice residue remains beyond the PMNS angle triple itself.

### Proof

From the active-half-plane theorem:

```text
q_+ >= sqrt(8/3) - delta
```

is exact on the source side. Evaluating the chamber margin `q_+ + delta -
sqrt(8/3)` on the five retained target-surface basins gives:

- Basin 1: positive;
- Basin 2: positive;
- Basin X: positive;
- Basin N: negative;
- Basin P: negative.

So the exact target-surface chamber roots are exactly

```text
{Basin 1, Basin 2, Basin X}.
```

Now evaluate the exact source cubic:

```text
I_src(H) = Im(H_12 H_23 H_31).
```

On those three chamber roots:

- `I_src(Basin 1) > 0`,
- `I_src(Basin 2) < 0`,
- `I_src(Basin X) < 0`.

Therefore `I_src(H) > 0` selects Basin 1 uniquely on the exact target-surface
chamber root set.

Finally, the explicit projected-source branch scalar is

```text
Delta_src = det(H),
```

and on the same chamber roots:

- `det(H)` is positive on Basin 1,
- `det(H)` is negative on Basin 2 and Basin X.

So the unique source-cubic-positive chamber root is exactly the unique
`C_base` chamber root. That is A-BCC on the exact target surface.

QED.

---

## 3. Why this does not contradict the global sign-blindness no-go

This note is intentionally weaker than a pure algebraic sign theorem.

Outside the exact target chamber root set, `I_src(H)` does **not** determine
the sign of `det(H)` globally:

- Basin N has `I_src(H) < 0` but `det(H) > 0`;
- Basin P has `I_src(H) > 0` but `det(H) < 0`.

So the five-route audit remains correct:

- pure `Cl(3)/Z^3` algebra alone does not fix the sign of `det(H)` on all of
  source space.

What changes here is more precise:

- once the exact PMNS target surface is fixed,
- and once the exact source-side chamber is imposed,
- the remaining chamber-root ambiguity is already killed by the
  coefficient-free source cubic.

So the old “strict native A-BCC gap” was overstated. The true remaining strict
gap is not a separate branch-choice law on that target surface; it is the
target PMNS surface itself.

---

## 4. Consequence for the DM open map

Before this theorem, the strict/native open map was phrased as if DM still had
two separable residues:

1. source-chart / branch-choice derivation;
2. the PMNS angle triple.

After this theorem, the sharper statement is:

- on the exact PMNS target surface, A-BCC is already downstream of the native
  chamber plus `I_src(H) > 0`;
- the review-surface selector residue is already closed on the current
  recovered packet;
- therefore the only remaining strict/native DM burden is the PMNS angle
  triple itself, equivalently the missing point-selection law on the exact
  local `2`-real PMNS source manifold.

So this theorem does **not** finish full DM sole-axiom closure. It proves
something narrower and more useful:

> there is no longer a separate native A-BCC blocker once the exact target
> PMNS surface is granted.

---

## 5. What this closes

- the claim that DM still has a separate strict/native branch-choice residue
  once the exact PMNS target surface is fixed;
- the need to keep treating A-BCC as independent of the PMNS angle-triple
  problem on that exact target surface.

## 6. What this does not close

- a pure `Cl(3)/Z^3` sign theorem on all of source space;
- the PMNS angle triple itself;
- full sole-axiom DM closure.

---

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_abcc_exact_target_surface_source_cubic_closure_2026_04_21.py
```

Expected final line:

```text
SUMMARY: PASS=15 FAIL=0
```
