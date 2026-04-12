# Graph-First Chiral Completion Search

**Date:** 2026-04-12  
**Status:** targeted gate analysis on the current graph-first gauge surface  
**Script:** `scripts/frontier_graph_first_chiral_completion.py`

---

## Question

The current retained graph-first gauge result gives:

\[
V_L = (2,3)_{+1/3} \oplus (2,1)_{-1}
\]

on the left-handed `8`-state surface.

Can the missing right-handed singlets needed for anomaly-complete hypercharge
arise *internally* from this surface, or does the framework need a genuinely
new completion sector?

---

## Result

The answer is sharp:

- there are **no weak singlets at all** on the one-particle `8`-state surface
- a permissive tensor-power search finds:
  - `d_R`-like singlets by degree `2`
  - `e_R`-like singlets by degree `2`
  - `u_R`-like singlets only by degree `4`

This is a strong obstruction to a clean low-degree chiral completion from the
current one-particle surface alone.

---

## Why this matters

The current graph-first result is structurally strong but still left-handed:

- `Q_L : (2,3)_{+1/3}`
- `L_L : (2,1)_{-1}`

To reach anomaly-complete hypercharge, the framework still needs the
right-handed singlet sector:

- `u_R`
- `d_R`
- `e_R`

The new search shows:

- these states are **not present** on the one-particle surface
- and even in a permissive composite search, they do **not** emerge uniformly
  at low degree

The hardest missing state is `u_R`: it only appears at degree `4`.

That means the present surface does not contain a natural, symmetric, low-degree
completion of the Standard Model chiral matter content.

---

## Interpretation

This is not a full no-go theorem for all possible completions.

The search is intentionally permissive:

- tensor products only
- no locality requirement
- no Fermi-statistics constraint

So the logic is:

- if a target state is absent here, that is a strong obstruction
- if a target state is present here, that is only a candidate, not closure

## Relation To The 4D Completion

The 4D chirality + anomaly-cancellation theorem in
[`RIGHT_HANDED_SECTOR_NOTE.md`](/private/tmp/physics-review-active/docs/RIGHT_HANDED_SECTOR_NOTE.md)
does close the physical right-handed sector.
This search remains the graph-canonical blocker for the stronger claim:
the present 3D one-particle surface does not by itself generate the
right-handed template.

On that permissive surface, the completion is already awkward:

- `d_R`-like and `e_R`-like states appear early
- `u_R`-like does not

So the current graph-first gauge surface does **not** naturally produce a full,
balanced one-generation chiral completion by itself.

---

## Relevant prior work on this axis

### 1. `frontier_alpha_em_lattice_running.py`

This is the strongest prior pointer toward chiral completion.

What it contributed:

- noticed the counting fact
  - `8 Dirac = 16 Weyl`
- compared that to one `SO(10)` generation
- proposed explicit anomaly-free assignment models

Why it helps:

- it suggests the right *counting target* for a completion theorem
- it gives a concrete one-generation / `SO(10)`-style hypothesis to test

Why it is not closure:

- it is still a counting/embedding argument
- it does not derive a graph-canonical right-handed singlet sector
- it does not solve the current graph-first gate on its own

### 2. `WILSON_BREAKS_EVERYTHING_NOTE.md`

This is the strongest prior pointer toward generation physicality.

What it contributed:

- showed Wilson breaking preserves the `1+3+3+1` counting but destroys the
  gauge structure

Why it helps:

- it supports the claim that taste physicality is not completely separate from
  the gauge structure
- it strengthens the idea that generations must be tied to the same exact
  `Cl(3)` / gauge backbone

Why it is not closure:

- it does not provide the missing canonical matter assignment
- it does not by itself upgrade `8 = 1+1+3+3` into physical three generations

### 3. `DARK_MATTER_SINGLETS_NOTE.md`

This is relevant mainly because it stress-tests the two singlets.

What it contributed:

- explored whether the two singlets could be dark states
- made the `U(1)` and `SU(2)` problems explicit

Why it helps:

- it clarifies that the singlets are not automatically harmless spectators
- it makes the unresolved charge and weak-coupling questions concrete

Why it is not closure:

- it leaves both the `U(1)` and `SU(2)` singlet issues unresolved
- it is a bounded phenomenology lane, not a gauge/matter theorem

### 4. `NEUTRINO_MASSES_NOTE.md`

This is a speculative right-handed-sector hint.

What it contributed:

- proposed identifying the `T_2` orbit with right-handed neutrinos
- used singlets as sterile-neutrino candidates

Why it helps:

- it shows there is already internal repo pressure toward a right-handed
  completion sector

Why it is not closure:

- it is downstream phenomenology, not a retained gauge/matter theorem
- it assumes rather than derives the needed assignment

---

## Current decision

The current gate should be stated as:

- **structural graph-first `su(3)` is closed**
- **anomaly-complete hypercharge / chiral completion remains open**

The best next theorem is now clearer:

### Chiral completion theorem

Either:

1. derive a genuinely new graph-canonical completion sector carrying
   `u_R`, `d_R`, `e_R` cleanly,

or:

2. derive a physically justified composite/bilinear completion and explain why
   its asymmetry (`u_R` only appearing much later) is not fatal.

Until one of those happens, the hypercharge lane remains bounded at:

- structural `su(3) \oplus u(1)`
- left-handed charge matching

not yet:

- anomaly-complete `U(1)_Y`
