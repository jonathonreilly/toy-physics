# DM σ_hier Upper-Octant Selector Theorem

**Date:** 2026-04-20  
**Status:** conditional/support theorem on the open DM PMNS gate  
**Scope:** closes the discrete `σ_hier` ambiguity at the pinned chamber point
without importing the T2K/NOvA CP-phase-sign preference  
**Does not close:** `I5` as the PMNS angle-pin law, or `A-BCC` as an axiom-
native branch-choice theorem  
**Dedicated verifier:**  
`scripts/frontier_dm_sigma_hier_upper_octant_selector_theorem_2026_04_20.py`

## Summary

The older `σ_hier` uniqueness theorem reduced the six `S_3` hierarchy
pairings to the two magnitude-passing permutations

```text
(2,0,1), (2,1,0),
```

then used the imported T2K/NOvA preference `sin(delta_CP) < 0` to choose
`(2,1,0)`.

That external CP-sign discriminator is not actually needed on the current
pinned chamber package.

The exact chamber upper-octant theorem already proves that, at central

```text
(sin^2 theta_12, sin^2 theta_13) = (0.307, 0.0218),
```

any chamber-interior PMNS closure must satisfy

```text
sin^2 theta_23 >= 0.540969817889... > 1/2.
```

But the two surviving `σ` are exactly the `mu↔tau` pair:

- they preserve `sin^2 theta_12`,
- preserve `sin^2 theta_13`,
- send `sin^2 theta_23` to `1 - sin^2 theta_23`,
- and flip the sign of the Jarlskog invariant.

At the pinned chamber point:

```text
sigma = (2,0,1): sin^2 theta_23 = 0.455000028664...
sigma = (2,1,0): sin^2 theta_23 = 0.544999971336...
```

So only `sigma = (2,1,0)` satisfies the exact chamber upper-octant law. The
negative CP sign then becomes a consequence rather than an imported
discriminator.

## Inputs

### P1. 9/9 magnitude filter at the pinned chamber point

Per
[SIGMA_HIER_UNIQUENESS_THEOREM_NOTE_2026-04-19.md](./SIGMA_HIER_UNIQUENESS_THEOREM_NOTE_2026-04-19.md),
the pinned chamber point

```text
(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)
```

has exactly two `S_3` permutations placing all `9/9` PMNS magnitudes inside
the NuFit `3σ` bands:

```text
(2,0,1), (2,1,0).
```

### P2. Exact chamber upper-octant theorem

Per
[PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md](./PMNS_THETA23_UPPER_OCTANT_CHAMBER_CLOSURE_PREDICTION_NOTE_2026-04-17.md),
at central `(sin^2 theta_12, sin^2 theta_13) = (0.307, 0.0218)` the chamber
closure threshold is

```text
sin^2 theta_23,min = 0.540969817889...
```

and is strictly above maximal mixing.

## Theorem statement

**Theorem (upper-octant selector for `σ_hier`).** At the pinned chamber point
`(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`, the unique
hierarchy-pairing permutation satisfying both

1. all `9/9` PMNS magnitudes lie inside the NuFit `3σ` ranges, and
2. the exact chamber upper-octant law
   `sin^2 theta_23 >= 0.540969817889...`

is

```text
sigma_hier = (2,1,0).
```

The alternative magnitude-passing permutation `(2,0,1)` is excluded because
it gives

```text
sin^2 theta_23 = 0.455000028664... < 0.540969817889....
```

So `σ_hier = (2,1,0)` is selected on the current pinned chamber package
without importing the T2K/NOvA CP-phase-sign preference.

## Proof

### Step 1. The magnitude filter reduces `S_3` from six permutations to two

The dedicated verifier rechecks all six permutations directly at `H_pin` and
finds exactly the same surviving pair as the older theorem:

```text
(2,0,1), (2,1,0).
```

The other four permutations fail at least four magnitude entries.

### Step 2. The surviving pair are exact `mu↔tau` partners

Let `P_(201)` and `P_(210)` be the two PMNS matrices. They differ by a
`mu↔tau` row swap, so:

```text
sin^2 theta_12(201) = sin^2 theta_12(210),
sin^2 theta_13(201) = sin^2 theta_13(210),
sin^2 theta_23(201) + sin^2 theta_23(210) = 1,
J(201) = -J(210).
```

Numerically at the pin:

```text
sigma=(2,0,1): s12^2=0.307000397724, s13^2=0.021799951452,
               s23^2=0.455000028664, sin(delta_CP)=+0.987360759210

sigma=(2,1,0): s12^2=0.307000397724, s13^2=0.021799951452,
               s23^2=0.544999971336, sin(delta_CP)=-0.987360759210
```

### Step 3. The chamber law excludes the lower-octant partner

The exact threshold theorem gives

```text
s23^2_min = 0.540969817889...
```

at the same central `(s12^2, s13^2) = (0.307, 0.0218)`.

Comparing the two surviving `σ`:

```text
sigma=(2,0,1): 0.455000028664 - 0.540969817889 = -0.085969789225 < 0
sigma=(2,1,0): 0.544999971336 - 0.540969817889 = +0.004030153447 > 0
```

So exactly one magnitude-passing permutation is chamber-compatible:

```text
sigma_hier = (2,1,0).
```

This proves the theorem. □

## Consequence

The CP sign is no longer needed as the selector input for `σ_hier` on this
package. It becomes a consequence:

```text
sigma_hier = (2,1,0)  =>  sin(delta_CP) < 0.
```

So the logic on the pinned chamber packet becomes:

```text
3-angle pin + magnitude pass + exact chamber upper-octant law
  => sigma_hier = (2,1,0)
  => sin(delta_CP) < 0.
```

## What this closes

This closes the discrete `σ_hier` ambiguity on the current pinned chamber
package more cleanly than the older note:

- the old route used an imported CP-sign preference;
- the new route uses the exact chamber upper-octant law already present in
  the PMNS closure stack.

So `I12` is closed here as:

```text
sigma_hier = (2,1,0) is selected by the exact chamber upper-octant law.
```

## What this does not close

- It does **not** derive the PMNS angle triple itself. That remains the
  remaining `I5` task.
- It does **not** derive `A-BCC` from the axiom alone.
- It is still a pinned-point / chamber-package theorem, not an all-basin
  global theorem.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_sigma_hier_upper_octant_selector_theorem_2026_04_20.py
```

Expected:

```text
PASS=14 FAIL=0
```
