# DM Selector Shifted-Relative-Action Recovered-Packet Closure Theorem

**Date:** 2026-04-21
**Status:** support - structural or confirmatory support note
**Primary runner:** `scripts/frontier_dm_selector_shifted_relative_action_recovered_packet_closure_2026_04_21.py`

## Statement

The remaining DM selector residue can now be closed on the **current recovered
selector packet**.

Keep the exact scalar observable-principle law already used by the internal
off-seed selector,

```text
S_rel(H || H_seed)
  = Tr(H_seed^(-1) H) - log det(H_seed^(-1) H) - 3,
```

and transport it to the common positive comparison windows

```text
A_mu(H) = H + mu I.
```

This gives the shifted same-law packet

```text
S_mu(H || H_seed)
  = Tr(A_mu(H_seed)^(-1) A_mu(H))
    - log det(A_mu(H_seed)^(-1) A_mu(H)) - 3.
```

Then on the current recovered bank of five lifts:

- for every audited common positive shift in the packet, the preferred
  recovered lift `0` is the **unique** minimizer of `S_mu`,
- on a dense admissible stress range from the positivity edge to large shifts,
  the same unique minimizer persists,
- and that same lift `0` is exactly the unique recovered point with
  `Im(K_Z3[1,2]) > 0`.

So the current-package selector residue is closed on the recovered
packet by the **same exact scalar law** already present in the internal
selector grammar.

## Prior branch state

Four earlier same-day results are integrated here.

1. `docs/DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md`
   gives the exact scalar observable-relative-action law on the fixed native
   `N_e` seed surface.
2. `docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_BRANCH_SEPARATION_SUPPORT_THEOREM_NOTE_2026-04-21.md`
   shows that the internal selector does **not** itself land on the recovered
   selector branch.
3. `docs/DM_SELECTOR_RELATIVE_ACTION_RECOVERED_PROJECTION_SUPPORT_THEOREM_NOTE_2026-04-21.md`
   shows that the same internal selector already has one canonical recovered
   image: the preferred recovered lift `0`.
4. `docs/DM_SELECTOR_SHIFTED_DOUBLET_IMAG_SIGN_SUPPORT_THEOREM_NOTE_2026-04-21.md`
   shows that among recovered lifts only the preferred lift `0` lies on the
   positive side of the canonical odd doublet boundary
   `Im(K_Z3[1,2]) = 0`.

Those results still left one live current-package burden:

- justify the recovered selector law itself, rather than only a projection
  toward it.

## New closure theorem

### 1. The same scalar logdet law extends naturally to the common positive windows

The raw seed-relative action is not defined on the whole recovered bank, since
some recovered lifts leave the seed-positive branch.

But the exact scalar grammar is unchanged by passing to any common positive
window

```text
A_mu(H) = H + mu I,
```

with `mu > mu_floor`, where

```text
mu_floor = max_i repair(H_i).
```

This is the natural SPD-cone continuation of the same LogDet/Bregman law on
the recovered packet.

### 2. Every audited common positive shift already selects the preferred recovered lift

For the branch-local audited shift family

```text
mu = mu_floor + s,  s in SHIFT_OFFSETS,
```

the shifted relative action `S_mu(H_i || H_seed)` has the same unique
minimizer on the whole recovered bank:

- lift `0` is always the unique minimizer,
- the worst audited uniqueness gap is still strictly positive.

So the selector is not a one-window accident.

### 3. The same minimizer survives dense admissible stress

On a dense stress sweep from immediately above the positivity threshold out to
large shifts, the same unique minimizer persists.

So the branch-local packet does not show any minimizer swap within the
admissible shifted family:

```text
argmin_i S_mu(H_i || H_seed) = 0
```

throughout the audited stress range.

### 4. The same exact law activates the positive odd doublet side

The shifted-imaginary sign theorem already showed:

- lift `0`: `Im(K_Z3[1,2]) > 0`
- lifts `1,2,3,4`: `Im(K_Z3[1,2]) < 0`.

Therefore the shifted same-law minimizer is not just the preferred recovered
lift abstractly. It is exactly the unique recovered point on the positive side
of the canonical odd doublet boundary.

### 5. Consequence

On the current recovered selector packet, the branch now has one coherent
selector closure stack:

- the exact internal observable-relative-action law,
- its canonical recovered image,
- the threshold selector `tau_b,min`,
- the positive shifted-imaginary doublet side,
- and the shifted same-law packet selector

all pick the same preferred recovered lift `0`.

So the **current-package DM selector residue is closed** on the current
recovered packet.

## What this does and does not close

### Closed at this grade

- current recovered-packet point selection on the DM current package surface
- the last live current-package selector residue after the retained-measurement
  A-BCC closure and split-2 interval certification

### Still not closed

This is **not** a pure target-free global sign/source-chart theorem from
`Cl(3)/Z^3` alone.

What remains outside the grade of this theorem by itself is:

- a global source-chart / sign law on all of source space, without granting
  the exact PMNS target surface.

But after the companion exact target-surface source-cubic closure theorem,
that is no longer a live exact-target native/source-map blocker.

So the branch now separates cleanly:

- **current package surface:** DM flagship lane closed
- **exact-target native/source map:** no separate native A-BCC residue remains
- **pure target-free global sign law:** still outside the package grade

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_selector_shifted_relative_action_recovered_packet_closure_2026_04_21.py
```

Expected:

```text
SUMMARY: PASS=14 FAIL=0
```
