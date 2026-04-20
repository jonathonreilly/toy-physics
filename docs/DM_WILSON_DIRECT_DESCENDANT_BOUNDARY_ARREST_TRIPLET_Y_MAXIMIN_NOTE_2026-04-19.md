# DM Wilson Direct-Descendant Boundary-Arrest Triplet/Y Maximin Note

**Date:** 2026-04-19  
**Status:** exact positive boundary-arrest result on the DM source-fiber /
boundary-drift lane downstream of the same-day spectral completion and
`J_iso` no-go notes

**Primary runner:**  
`scripts/frontier_dm_wilson_direct_descendant_boundary_arrest_triplet_y_maximin_2026_04_19.py`
(`PASS=15 FAIL=0`).

## Question

After the same-day transport-fiber spectral completion theorem, the remaining
source ambiguity above the canonical favored transport column was already an
explicit local spectral fiber. After the same-day `J_iso` no-go note, the
branch also knew that pure Schur-side isotropy maximization does **not** pick
an interior source: it runs toward the constructive boundary.

So the next honest question was:

> what is the **first retained law** that arrests that drift and selects an
> interior source on the canonical column fiber?

## Bottom line

The answer on the explicit boundary-drift lane is **not** another pure
Schur-side scalar.

The first successful retained arrest law is the coefficient-free two-law
maximin system

```text
t_* = max on the canonical transport-column fiber of min(J_ctr, J_y),
```

where

```text
J_ctr = 27 gamma E1 E2 / (gamma + E1 + E2)^3
J_y   = 27 y1 y2 y3 / (y1 + y2 + y3)^3.
```

Here:

- `J_ctr` is the unique normalized symmetric cubic on the positive
  constructive triplet `(gamma, E1, E2)`;
- `J_y` is the parallel unique normalized symmetric cubic on the native
  descended `y`-simplex.

The same-day `J_iso` no-go note showed that pure Schur isotropy ignores the
constructive boundary and runs outward. The new note sharpens that picture:

1. pure `J_ctr` does arrest the constructive-sign collapse;
2. but pure `J_ctr` still runs to the **native source boundary** `y2 = 0`;
3. the missing retained law is therefore the first exact source-boundary
   barrier that `J_iso` and `J_ctr` both fail to see;
4. balancing `J_ctr` against `J_y` by maximin selects an interior source.

On the tested boundary-drift start packet

- `W0`,
- `W1`,
- `W3`,
- `B_major`,
- and the explicit `epsilon = 0.05, 0.02, 0.01, 0.005, 0.001` drift packet,

the maximin law collapses to one common interior certificate

```text
I_* = (0.84637802..., 0.32460908..., 0.71824284..., 0.02499042..., 2.22347386...)
```

with

```text
(eta_1, gamma, E1, E2, Delta_src)
= (1.05222031..., 0.11886042..., 0.06469214..., 1.08709333..., 0.01979377...)
```

and exact active-barrier equalization

```text
J_ctr(I_*) = J_y(I_*) = t_* = 0.110013443757...
```

while the Schur isotropy cubic stays strictly above the floor:

```text
J_iso(I_*) = 0.121416735777... > t_*.
```

So the interior boundary-arrest point is fixed by the **constructive-triplet /
native-y bottleneck**, not by pure Schur isotropy.

## What the runner proves

### 1. The constructive triplet forces its own exact cubic

Exactly as in the same-day `J_iso` derivation, the normalized positive triplet

```text
p = (gamma, E1, E2) / (gamma + E1 + E2)
```

admits only one normalized symmetric cubic law that vanishes when any triplet
channel collapses:

```text
J_ctr = 27 p_1 p_2 p_3
      = 27 gamma E1 E2 / (gamma + E1 + E2)^3.
```

So there is a coefficient-free constructive-boundary barrier available on the
exact retained triplet.

### 2. Pure J_ctr still has a no-go: it runs to the source boundary

Starting from the explicit boundary-drift packet, pure `J_ctr` maximization on
the canonical transport-column fiber collapses to one common source-boundary
certificate

```text
S_ctr
= (0.84741148..., 0.32885008..., 0.70537023..., 10^-9, 2.37373298...),
```

with

```text
(gamma, E1, E2) = (0.12633313..., 0.08047720..., 1.05714411...)
J_ctr(S_ctr)    = 0.143712259311...
J_y(S_ctr)      = 5.249374586614... x 10^-9.
```

So pure constructive-triplet isotropy fixes the first no-go but reveals the
next one immediately:

> it stops the constructive-sign collapse, but it still evacuates to the
> native source face `y2 = 0`.

### 3. The native y-simplex contributes the missing retained barrier

On the fixed seed surface, the descended `y`-coordinates already live on a
native `3`-simplex. Repeating the same normalized symmetric cubic argument
gives the unique source-boundary barrier

```text
J_y = 27 y1 y2 y3 / (y1 + y2 + y3)^3.
```

This is the first exact law on the current lane that vanishes at the explicit
source-boundary escape route found by pure `J_ctr`.

### 4. The maximin bottleneck law selects an interior source

The new selector system is:

```text
fix the canonical transport column;
stay in gamma > 0, E1 > 0, E2 > 0;
maximize t subject to J_ctr >= t and J_y >= t.
```

Equivalently:

```text
maximize min(J_ctr, J_y).
```

On the tested boundary-drift start packet, this collapses to the single
interior certificate `I_*` above. At that point:

- `J_ctr = J_y = t_*`;
- `J_iso` is strictly larger than `t_*`;
- `y2 = 0.02499042... > 0`, so the source is genuinely interior;
- the point stays on the canonical column orbit.

The selected point is new but still `W1`-local:

```text
||I_* - W1|| = 0.090092068708...
```

So the first successful retained arrest principle is now explicit:

> do not let the constructive-triplet barrier outrun the native y-boundary
> barrier.

## Why this matters

This closes the first honest boundary-drift gap left by the same-day no-go.

Before this note, the branch knew only the negative statement:

> pure Schur isotropy drives toward the constructive boundary.

After this note, the sharper positive statement is:

> the first successful interior arrest law on the current lane is the
> coefficient-free maximin bottleneck between the exact constructive triplet
> cubic and the exact native y-simplex cubic.

That is a real selector advance because it:

- uses only exact same-day retained quantities;
- needs no fitted coefficients;
- explains why pure `J_iso` fails;
- explains why pure `J_ctr` is still incomplete;
- and produces an explicit interior source certificate on the canonical column
  fiber.

## Honest scope

This is a **boundary-drift lane** result, not yet a final global uniqueness
theorem on the whole canonical fiber.

What is proved here is:

- pure `J_iso` fails by constructive-boundary drift;
- pure `J_ctr` fails by source-boundary drift;
- the coefficient-free maximin bottleneck `min(J_ctr, J_y)` selects one common
  interior certificate on the explicit boundary-drift packet.

What remains open is narrower:

- a reviewer-grade theorem that this same interior point is the unique global
  selector on the full canonical fiber;
- or a derivation from `Cl(3)` on `Z^3` of why the `J_ctr / J_y` bottleneck is
  the physical microscopic law rather than only the first successful retained
  arrest system.

## Relation to the earlier same-day DM notes

This note sits immediately downstream of:

1. `docs/DM_WILSON_DIRECT_DESCENDANT_TRANSPORT_FIBER_SPECTRAL_COMPLETION_THEOREM_NOTE_2026-04-19.md`
2. `docs/DM_WILSON_DIRECT_DESCENDANT_CONSTRUCTIVE_TRANSPORT_PLATEAU_J_ISO_DERIVATION_AND_SCHUR_ISOTROPY_NO_GO_NOTE_2026-04-19.md`
3. `docs/DM_WILSON_DIRECT_DESCENDANT_CANONICAL_TRANSPORT_COLUMN_FIBER_THEOREM_NOTE_2026-04-19.md`
4. `docs/DM_WILSON_DIRECT_DESCENDANT_LOCAL_OBSERVABLE_COORDINATE_THEOREM_NOTE_2026-04-19.md`

The first note localizes the unresolved object as an explicit completed fiber.
The second proves that pure Schur isotropy fails. The new note identifies the
first retained source-boundary law needed to stop that drift and gives the
resulting interior certificate on the tested lane.

## Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_wilson_direct_descendant_boundary_arrest_triplet_y_maximin_2026_04_19.py
```

Expected:

- `PASS=15 FAIL=0`;
- one pure `J_ctr` source-boundary certificate with `y2 = 10^-9`;
- one common interior triplet/y maximin certificate with
  `J_ctr = J_y = 0.110013443757...`;
- `J_iso` strictly above that active floor.
