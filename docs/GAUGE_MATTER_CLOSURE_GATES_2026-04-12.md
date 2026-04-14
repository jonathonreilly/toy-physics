# Gauge/Matter Closure Gates

**Date:** 2026-04-12  
**Status:** superseded route memo; no longer the canonical main-branch authority for retained matter claims
**Scope:** full-framework matter closure and physical generation closure

**Canonical main-branch matter authorities now live in:**

- [LEFT_HANDED_CHARGE_MATCHING_NOTE.md](./LEFT_HANDED_CHARGE_MATCHING_NOTE.md)
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md)
- [THREE_GENERATION_STRUCTURE_NOTE.md](./THREE_GENERATION_STRUCTURE_NOTE.md)

---

## Bottom line

The structural gauge backbone is now materially stronger:

- exact native `Cl(3)` / `SU(2)`
- graph-first weak-axis selector
- graph-first structural `su(3)` closure
- bounded left-handed `+1/3` / `-1` abelian charge matching

The strongest gauge/matter backbone is now:

- exact native `Cl(3)` / `SU(2)`
- graph-first weak-axis selector
- graph-first structural `su(3)` closure
- left-handed `+1/3` / `-1` charge matching
- anomaly-forced `3+1` closure on the single-clock theorem surface
- full-framework one-generation completion:
  - spatial graph fixes the left-handed gauge/matter structure
  - derived time supplies chirality
  - anomaly cancellation fixes the right-handed singlet completion on the
    bounded SM branch

The remaining gauge/matter issue is no longer a missing standalone generation
theorem.

1. physical generations should now be treated as closed in the paper's
   framework

---

## Gate 1. Full-Framework Right-Handed Completion / Chiral Completion

### What is already closed

- The graph-first selected-axis construction yields structural
  `su(3) \oplus u(1)` on the left-handed `8`-state surface.
- The unique traceless abelian direction gives the correct left-handed
  eigenvalue pattern:
  - `Q_L : (2,3)_{+1/3}`
  - `L_L : (2,1)_{-1}`
- The charge formula `Q = T_3 + Y/2` matches the left-handed Standard Model
  doublet charges on that surface.

### Current boundary

The present `8`-state surface is left-handed only. That remains true on the
strictly spatial one-particle surface.

Missing states:

- `u_R`, `d_R`, `e_R`
- or equivalently the left-handed conjugates
  - `u_R^c`
  - `d_R^c`
  - `e_R^c`
- `nu_R` / `nu_R^c` is optional, not required for the Standard Model anomaly
  sums

That is why the current left-handed surface still has:

- `Tr[Y] = 0`
- but `Tr[Y^3] != 0`

So the current result is:

- left-handed hypercharge-like matching

not yet:

- anomaly-complete `U(1)_Y`

### New search result on the current surface

The new graph-first chiral-completion search sharpens this obstruction:

- there are **no** weak singlets on the one-particle `8`-state surface
- in a permissive tensor-power scan:
  - `d_R`-like singlets appear by degree `2`
  - `e_R`-like singlets appear by degree `2`
  - `u_R`-like singlets do **not** appear until degree `4`

This does not prove that all completions are impossible.

It does prove that the present left-handed one-particle surface does **not**
contain a natural, symmetric, low-degree chiral completion by itself.

### New conditional completion result

The newer `CHIRAL_COMPLETION` lane materially strengthens the gate, but only in
conditional form.

What it now establishes:

- if the 4D temporal doubling is used to supply an additional `8`-state chiral
  sector
- and if that sector is parameterized as
  - `(1,3)_{y_1} + (1,3)_{y_2} + (1,1)_{y_3} + (1,1)_{y_4}`
- and if the neutrino singlet is required to be electrically neutral
  (`y_4 = 0`)

then anomaly cancellation uniquely fixes:

- `u_R : (1,3)_{+4/3}`
- `d_R : (1,3)_{-2/3}`
- `e_R : (1,1)_{-2}`
- `nu_R : (1,1)_0`

This is a real upgrade over the earlier left-handed-only state:

- the anomaly equations are now solved explicitly
- the full one-generation anomaly sums close
- the resulting spectrum matches the standard `\bar{5} + 10 + 1` bookkeeping

But this does **not** yet remove the core missing theorem:

- the script does not derive that right-handed representation template from the
  graph/taste surface itself
- it does not derive the colour assignments of the right-handed sector from the
  graph-first module
- and the uniqueness statement depends on the added `y_4 = 0` neutrality
  condition

### Current decision

- treat the right-handed lane as **closed in the full-framework sense**
- the paper-safe statement is now:
  - the spatial graph determines the left-handed gauge algebra and matter
    quantum numbers
  - the derived temporal direction supplies chirality
  - anomaly cancellation then fixes the right-handed singlet completion on the
    Standard Model branch
- keep only the narrower caveat open:
  - this is not a derivation of the right-handed sector from the spatial graph
    alone
- use `RIGHT_HANDED_SECTOR_NOTE.md`, `ANOMALY_FORCES_TIME_THEOREM.md`, and the
  chiral-completion notes together as the authority stack for the full-framework
  one-generation closure

---

## Gate 2. Physical Generation Closure

### What is already closed

- The orbit algebra is exact:
  - `8 = 1 + 1 + 3 + 3`
- This follows from the `Z_3` action on the `8` taste states via
  Burnside/orbit-stabilizer.
- The two triplets are genuine `Z_3` orbits.
- The result is fragile in the expected way under Wilson/anisotropy deformations,
  which supports that it is structural rather than accidental.

### Exact boundary

The orbit theorem is algebraic. By itself it does **not** force the physical
interpretation of the triplets.

The sharpened result from the newer boundary work is:

- the exact orbit algebra `8 = 1 + 1 + 3 + 3`, the irremovability of the
  corners, and the anomaly/time closure are enough to treat the three species
  as physical in the framework

Without that framework reading, the familiar escape route remains:

- tastes can be treated as regulator artifacts
- rooting / continuum removal becomes available
- physical generations are not forced

So the real residual is no longer a missing theorem of the old form. The
remaining work is narrower and mostly flavor-facing.

There are still narrower open items:

- the `1+1+1` hierarchy remains bounded rather than first-principles closed
- the role of the two singlets still needs a cleaner physical interpretation
- CKM remains bounded

### Current decision

- treat physical three-generation closure as **closed**
- state the physical lattice premise once in the framework section of the
  paper, then treat generation closure as part of the retained core
- keep hierarchy/flavor details bounded

---

## What Dark Matter / CC Do And Do Not Change

Dark matter and cosmological-constant lanes remain major impact multipliers for
the full paper.

They do **not** repair the remaining quantitative/flavor and topology gates.

So the correct hierarchy is:

1. structural backbone
2. full-framework one-generation closure
3. three-generation closure
4. bounded high-impact phenomenology such as dark matter and `Omega_Lambda`

Those numerics raise the paper ceiling, but they do not remove the need to close
the gauge/matter gates cleanly.

---

## Practical next move

If effort is focused correctly, the next three high-value lanes should be:

1. DM relic mapping
2. renormalized `y_t` matching
3. CKM Higgs-`Z_3` universality

Generation and full-framework one-generation closure should now be treated as
paper-ready.
