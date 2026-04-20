# DM I12 σ_hier Closure Packet

**Date:** 2026-04-20  
**Lane:** DM A-BCC sigma-chain / open import `I12`  
**Status:** authoritative branch-local closure packet for `I12` on
`morning-4-20`  
**Claim:** `I12` is closed on this branch  
**Exact closure statement:** `sigma_hier = (2,1,0)` is selected on the active
chamber package, and therefore `sin(delta_CP) < 0` follows as a consequence

## What this packet is for

`morning-4-20` contains both:

- an intermediate reduction note,
- and the later theorem notes that actually close `I12`.

This packet names the exact closure chain so the branch owner does not have to
reconstruct it from several notes.

## The exact proof chain

### 1. Chamber completeness is explicit

Per
[DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md](./DM_PMNS_CHAMBER_SPECTRAL_COMPLETENESS_THEOREM_NOTE_2026-04-20.md),
the exact active-chamber `chi^2 = 0` set is

```text
{Basin 1 on sigma=(2,1,0), Basin 2 on sigma=(2,1,0), Basin X on sigma=(2,0,1)}.
```

So the active chamber ambiguity is reduced to these explicit survivors.

### 2. The old parity note is only an intermediate reduction

Per
[DM_PMNS_CP_ORIENTATION_PARITY_REDUCTION_NOTE_2026-04-20.md](./DM_PMNS_CP_ORIENTATION_PARITY_REDUCTION_NOTE_2026-04-20.md),

```text
J_sigma = parity(sigma) * I_src(H) / Delta,
I_src(H) = Im(H_12 H_23 H_31).
```

That note is important, but it does **not** by itself close `I12`. It only
reduces the ambiguity to one parity bit.

### 3. First actual closeout theorem: upper-octant + source cubic

Per
[DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md](./DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md),
the coefficient-free selector system

```text
sin^2(theta_23) > 1/2,
I_src(H) > 0
```

selects Basin 1 uniquely on the exact chamber root set. Therefore

```text
Basin 1  =>  sigma_hier = (2,1,0)  =>  sin(delta_CP) < 0.
```

This already closes `I12` on the active chamber.

### 4. Cleaner reformulation of the same closure

Per
[DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md](./DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md),
the closure can be packaged even more cleanly at the pinned chamber point.

The two `9/9`-magnitude-passing permutations are exactly

```text
(2,0,1), (2,1,0).
```

They preserve `sin^2(theta_12)` and `sin^2(theta_13)`, send

```text
sin^2(theta_23) <-> 1 - sin^2(theta_23),
```

and flip the CP sign.

The exact chamber threshold theorem gives

```text
sin^2(theta_23)_min = 0.540969817889... > 1/2.
```

At the pin:

```text
sigma=(2,0,1): sin^2(theta_23) = 0.455000028664... < 0.540969817889...
sigma=(2,1,0): sin^2(theta_23) = 0.544999971336... > 0.540969817889...
```

So only

```text
sigma_hier = (2,1,0)
```

is chamber-compatible. Then

```text
sin(delta_CP) < 0
```

follows automatically.

## Verdict

`I12` is closed on `morning-4-20`.

The authoritative theorem to cite for the closeout is:

- [DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md](./DM_SIGMA_HIER_UPPER_OCTANT_SELECTOR_THEOREM_NOTE_2026-04-20.md)

The earlier theorem that first closed it on the exact chamber root set is:

- [DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md](./DM_PMNS_UPPER_OCTANT_SOURCE_CUBIC_SELECTOR_THEOREM_NOTE_2026-04-20.md)

The intermediate reduction note is not the closure note:

- [DM_PMNS_CP_ORIENTATION_PARITY_REDUCTION_NOTE_2026-04-20.md](./DM_PMNS_CP_ORIENTATION_PARITY_REDUCTION_NOTE_2026-04-20.md)

## Verification

The branch-local closure is backed by the passing runners:

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_chamber_spectral_completeness_theorem_2026_04_20.py
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_upper_octant_source_cubic_selector_theorem_2026_04_20.py
PYTHONPATH=scripts python3 scripts/frontier_dm_sigma_hier_upper_octant_selector_theorem_2026_04_20.py
```

Expected:

```text
PASS=11 FAIL=0
PASS=14 FAIL=0
PASS=14 FAIL=0
```
