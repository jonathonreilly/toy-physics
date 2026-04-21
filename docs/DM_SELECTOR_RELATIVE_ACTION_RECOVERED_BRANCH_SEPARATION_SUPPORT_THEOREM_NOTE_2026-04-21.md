# DM Selector Relative-Action / Recovered-Branch Separation Support Theorem

**Date:** 2026-04-21  
**Status:** selector-side support theorem on the open DM gate  
**Primary runner:** `scripts/frontier_dm_selector_relative_action_recovered_branch_separation_support_2026_04_21.py`

## Statement

The strongest current framework-internal selector law still does **not**
collapse to the recovered right-sensitive selector branch.

Concretely, the observable-relative-action law from
`docs/DM_LEPTOGENESIS_PMNS_OBSERVABLE_RELATIVE_ACTION_LAW_NOTE_2026-04-16.md`
selects one exact `eta / eta_obs = 1` source on the fixed native `N_e` seed
surface. But that exact source:

- does not coincide with any recovered-bank point;
- does not coincide with any recovered active target;
- is not selected by the recovered-bank canonical breakpoint
  `tau_b,min = min_i log(1 + b_i)`;
- and instead carries its own later breakpoint `tau_b,rel`.

So the remaining selector burden is sharper than “derive minimal relative
action.” The live theorem object must bridge the current exact internal
selector law to the recovered right-sensitive selector branch, or replace it
with a finer microscopic law.

## Inputs already on branch

### 1. Strongest current framework-internal selector law

The observable-relative-action note already fixed the strongest current
framework-internal selector law:

1. stay on the exact fixed native `N_e` seed surface;
2. fix the favored transport column from the exact transport-extremal class;
3. among exact-closure points on that surface, minimize the exact relative
   bosonic action

```text
S_rel(H_e || H_seed)
  = Tr(H_seed^{-1} H_e) - log det(H_seed^{-1} H_e) - 3.
```

That law selects the exact source

```text
x_rel = (0.47167533, 0.55381069, 0.66451397),
y_rel = (0.20806279, 0.46438280, 0.24755440),
delta_rel ≈ 0,
```

with

```text
eta / eta_obs = (1.0, 0.75917896, 0.48458840).
```

### 2. Recovered-bank selector target

The reviewed selector obstruction stack had already reduced the live
selector-side burden to the recovered bank and its intrinsic threshold-volume
family. Two new same-branch support notes then sharpened that family:

- `docs/DM_SELECTOR_THRESHOLD_STABILIZATION_SUPPORT_THEOREM_NOTE_2026-04-21.md`
  proved the stabilization window
  `(tau_star, tau_zero(next))`;
- `docs/DM_SELECTOR_FIRST_SHOULDER_EXIT_THRESHOLD_SUPPORT_NOTE_2026-04-21.md`
  isolated the recovered-bank canonical breakpoint

```text
tau_b,min = min_i log(1 + b_i) = 0.148036252277635...
```

which belongs uniquely to the preferred recovered lift and already selects it
on the recovered bank.

## New separation result

### 1. The relative-action source stays off the recovered selector branch

Using the exact reconstructed relative-action source and the same recovered
bank as the selector-support packet:

- the smallest Frobenius distance from the relative-action `H_rel` to the
  recovered bank is

```text
min_j ||H_rel - H_j||_F = 2.493910179587...
```

  attained at the preferred recovered lift `0`;
- the smallest active-target distance from the relative-action source to the
  recovered target bank is

```text
min_j ||T_rel - T_j||_2 = 0.496150820200...
```

  again at the preferred recovered lift.

So the strongest current internal selector law does not already land on the
recovered selector branch.

### 2. The relative-action source is not selected by the recovered-bank canonical breakpoint

Working on the same common positive comparison window `A_mu(H)` used by the
threshold-volume notes:

- the relative-action source has its own middle-branch breakpoint

```text
tau_b,rel = log(1 + b_rel) = 0.155402228412994...
```

  which is strictly later than the recovered-bank candidate
  `tau_b,min = 0.148036252277635...`;
- at the recovered-bank breakpoint, the preferred recovered lift still beats
  the relative-action source:

```text
V_tau_b,min(H_pref) = 0.72425153...
V_tau_b,min(H_rel)  = 0.77818829...
```

So the recovered-bank canonical breakpoint does not select the
observable-relative-action source.

### 3. The relative-action source carries a distinct breakpoint of its own

The relative-action source is not merely “close but wrong.” It carries a
distinct selector breakpoint:

- at `tau = 0.13` and `tau = 0.14`, the relative-action source still has full
  witness volume

```text
V_0.13(H_rel) = V_0.14(H_rel) = 1;
```

- at its own breakpoint `tau_b,rel`, it becomes strictly smaller than every
  recovered-bank competitor:

```text
V_tau_b,rel(H_rel) = 0.030950966183...
min_j V_tau_b,rel(H_j) = 0.58078354...
```

So the current exact internal selector law and the recovered-bank canonical
threshold candidate are two distinct exact selector objects, not one object in
two notations.

## Consequence

This sharpens the remaining open selector burden again.

Before this note, the selector-side positive target could be phrased as:

- derive why the physical threshold law is the earliest intrinsic breakpoint
  `tau_b,min`; or
- derive a stronger microscopic selector law.

After this note, the open object is stricter:

- either bridge the current exact observable-relative-action selector to the
  recovered right-sensitive selector branch;
- or replace both by a finer microscopic selector law that explains why the
  physical source branch chooses one of them and not the other.

So the remaining burden is no longer just “force minimal relative action” in
the abstract. It is to close the separation between the strongest current
internal selector law and the recovered right-sensitive selector target.

## Boundary

This is a support theorem, not closure.

It does **not** prove that the observable-relative-action law is unphysical,
and it does **not** prove that the recovered-bank threshold route is the final
selector. It proves only that the two exact constructions now live as
distinct objects on the current branch, so a genuine bridge or finer law is
still required.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_selector_relative_action_recovered_branch_separation_support_2026_04_21.py
```

Expected:

```text
SUMMARY: PASS=14 FAIL=0
```
