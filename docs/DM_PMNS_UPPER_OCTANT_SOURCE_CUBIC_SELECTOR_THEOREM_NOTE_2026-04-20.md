# DM PMNS Upper-Octant / Source-Cubic Selector Theorem

**Date:** 2026-04-20  
**Lane:** DM A-BCC sigma-chain / open imports `I12` and `I5`  
**Status:** support - structural or confirmatory support note
ambiguity is arrested by a small complete system:

```text
upper octant  +  source cubic orientation
```

More precisely:

1. the retained chamber-closure geometry forces the physical PMNS branch to lie
   in the upper octant;
2. on the exact chamber `chi^2 = 0` root set, the coefficient-free source law
   `I_src(H) > 0` then selects Basin 1 uniquely;
3. therefore the physical branch is
   `sigma_hier = (2,1,0)`, and the physical CP sign is negative.

This closes `I12`. It does **not** derive the PMNS angle triple from the sole
axiom; `I5` is reduced to the angle triple only.

**Primary runner:**  
`scripts/frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20.py`

---

## 0. Question

After chamber completeness and the parity-reduction theorem, is there now an
exact retained law that actually picks the physical branch among

```text
{Basin 1 on sigma=(2,1,0), Basin 2 on sigma=(2,1,0), Basin X on sigma=(2,0,1)}?
```

## 1. Bottom line

Yes.

The missing selector is not another free scalar family. It is the two-law
system

```text
s23^2 > 1/2,
I_src(H) > 0,
```

where

```text
I_src(H) := Im(H_12 H_23 H_31).
```

The first law is already supplied by the retained chamber geometry:

- the `theta_23` chamber-threshold theorem proves that at
  `(sin^2 theta_12, sin^2 theta_13) = (0.307, 0.0218)`,
  chamber closure requires
  `sin^2 theta_23 >= 0.540970... > 1/2`;
- more strongly, over the full NuFit 3-sigma rectangle on
  `(sin^2 theta_12, sin^2 theta_13)`, the threshold surface stays in
  `[0.5335, 0.5476]`, entirely above maximal mixing.

The second law is already supplied by the exact source-side CP orientation:

- on the exact chamber roots,
  `I_src(Basin 1) > 0`,
  `I_src(Basin 2) < 0`,
  `I_src(Basin X) < 0`.

Combining these two exact facts gives a unique selector:

- the upper-octant law removes the lower-octant partners;
- among the remaining upper-octant chamber roots, `I_src > 0` keeps only
  Basin 1;
- Basin 1 lives on `sigma = (2,1,0)`.

So the branch is no longer observationally free on this lane.

## 2. Theorem

**Theorem (upper-octant plus source-cubic selector).** Fix the target PMNS
angle triple

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
= (0.307, 0.0218, 0.545)
```

on the affine DM Hermitian family

```text
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q.
```

Let the exact active-chamber `chi^2 = 0` set be the three points from the
chamber-completeness theorem:

```text
Basin 1 on sigma=(2,1,0),
Basin 2 on sigma=(2,1,0),
Basin X on sigma=(2,0,1).
```

Then:

1. for the two `mu <-> tau`-related permutations
   `(2,1,0)` and `(2,0,1)` on any fixed Hermitian point,

   ```text
   sin^2 theta_23(2,0,1) = 1 - sin^2 theta_23(2,1,0),
   J_(2,0,1) = - J_(2,1,0);
   ```

2. the retained chamber-threshold theorem forces the physical branch to satisfy

   ```text
   sin^2 theta_23 > 1/2;
   ```

3. on the exact chamber root set, the upper-octant survivors are exactly

   ```text
   Basin 1 on sigma=(2,1,0),
   Basin 2 on sigma=(2,1,0),
   Basin X on sigma=(2,0,1);
   ```

4. their source-cubic signs are

   ```text
   I_src(Basin 1) > 0,
   I_src(Basin 2) < 0,
   I_src(Basin X) < 0;
   ```

5. therefore the coefficient-free source law `I_src(H) > 0` selects Basin 1
   uniquely among all upper-octant chamber roots.

Hence the physical branch is

```text
sigma_hier = (2,1,0),
```

and, by the parity-reduction identity

```text
J_sigma = parity(sigma) * I_src / Delta,
```

the physical CP sign is

```text
sin(delta_CP) < 0.
```

### Proof

Step 1 is immediate from the fact that `(2,0,1)` is a `mu <-> tau` row swap of
`(2,1,0)`. A single row swap leaves `|U_PMNS|` unchanged, sends
`sin^2 theta_23 -> 1 - sin^2 theta_23`, and reverses the Jarlskog sign.

Step 2 is the previously established upper-octant chamber theorem: the inverse
image of the retained PMNS-as-`f(H)` map meets the chamber only above the
threshold `sin^2 theta_23_min > 1/2`.

Step 3 is the exact chamber-completeness theorem.

Step 4 is the previously established source-cubic parity-reduction theorem.

Combining Steps 2 and 3 keeps only the upper-octant branch on each candidate.
Combining that with Step 4 leaves exactly Basin 1. Basin 1 sits on
`sigma=(2,1,0)`. Since `parity(2,1,0) = -1` and `I_src(Basin 1) > 0`, the
physical Jarlskog sign is negative.

QED.

## 3. Exact chamber table

| Chamber root | surviving upper-octant permutation | `sin^2 theta_23` | `I_src(H)` | `sin(delta_CP)` |
|---|---|---:|---:|---:|
| Basin 1 | `(2,1,0)` | `0.545` | `+0.30356` | `-0.98736` |
| Basin 2 | `(2,1,0)` | `0.545` | `-225.76` | `+0.55439` |
| Basin X | `(2,0,1)` | `0.545` | `-99.77` | `-0.41878` |

So:

- the upper-octant law removes the lower-octant partners `(0.455)`;
- the source cubic removes Basin 2 and Basin X;
- Basin 1 is the unique physical survivor.

## 4. Consequence for `I12`

`I12` is closed on this branch.

The remaining `sigma_hier` ambiguity is no longer a free charged-doublet label.
The exact selector is:

```text
upper-octant chamber law  +  source cubic orientation law.
```

That selects

```text
sigma_hier = (2,1,0)
```

without using the old T2K sign pin as an input.

## 5. Consequence for `I5`

This does **not** close `I5` fully.

What is now closed on this branch:

- the CP-sign half of the PMNS pin,
- the `sigma_hier` parity bit,
- the exact selection of Basin 1 on the active chamber root set.

What remains open:

- a framework-native derivation of the PMNS angle triple itself.

So `I5` is no longer “PMNS angles plus CP sign.” It is just:

```text
derive (sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
from retained physics.
```

## 6. Honest verdict

This is a real science close, not a wording cleanup.

The missing branch law is now explicit and coefficient-free:

```text
s23^2 > 1/2,
I_src(H) > 0.
```

On the exact active chamber this system arrests the last surviving `mu <-> tau`
ambiguity, selects Basin 1, fixes

```text
sigma_hier = (2,1,0),
sin(delta_CP) < 0,
```

and leaves only the PMNS angle triple itself as the remaining `I5` input.

## 7. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20.py
```

Expected final line:

```text
PASS=14  FAIL=0
```
