# Pointwise Whole-Shell Closure on the Exact Local `O_h` Source Class

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_oh_pointwise_shell_closure.py`  
**Status:** Exact pointwise shell closure on the local `O_h` class plus bounded finite-rank consequence

## Purpose

After the reduced whole-shell law, orbit-mean whole-shell law, and same-charge
bridge closure, there was still one remaining geometric objection:

> perhaps the local/angular shell law is still genuinely open, even if the
> shell means and orbit means are fixed

This note closes that objection on the exact local `O_h` source class already
used throughout the strong-field gravity line.

## Exact pointwise orbit law

On the exact local `O_h` source class, the whole-shell sewing band

- `3 < r <= 5`

is already pointwise constant on each cubic orbit for:

- the exterior-projector profile per unit charge `u = phi_ext / Q`
- the shell-source profile per unit charge `k = sigma_R / Q`

So the whole-shell law is not merely orbit-averaged there. It is already the
pointwise orbit law.

## Exact pointwise bridge stress law

With the same-charge bridge fixed:

- `psi = 1 + phi_ext`
- `chi = alpha psi = 1 - phi_ext`

the induced bridge density and stress-trace are:

- `rho = sigma_R / (2 pi psi^5)`
- `S = 0.5 rho (1/alpha - 1)`

The script finds that these are also pointwise constant on each orbit for the
exact local `O_h` source class to machine precision.

So on that class, the whole-shell bridge law is no longer merely reduced or
orbit-mean. It is pointwise exact at orbit resolution.

## Bounded broader-family consequence

For the broader exact finite-rank source family, the same quantities remain
close to the exact local `O_h` pointwise orbit law:

- `u` within-orbit spread below about `1.4%`
- `k` below about `1.7%`
- `rho` below about `1.4%`
- `S` below about `2.7%`

So the broader-family correction is not a large uncontrolled angular sector.

## What this closes

This closes the last shell-side ambiguity on the symmetric strong-field source
class:

> on the exact local `O_h` source class, the whole-shell bridge law is already
> pointwise exact at orbit resolution

## What this still does not close

This note still does **not** close:

1. the final Einstein/Regge interpretation beyond the current static isotropic
   conformal bridge
2. the fully general pointwise 4D closure for broader non-`O_h` source classes
3. fully general nonlinear GR

## Updated gravity target

After this note, the remaining open gravity problem is narrower again:

- the shell law is pointwise exact on the exact local `O_h` source class
- the broader finite-rank class differs only by a small within-orbit correction
- the real remaining work is the final 4D Einstein/Regge lift beyond the
  current bridge surface
