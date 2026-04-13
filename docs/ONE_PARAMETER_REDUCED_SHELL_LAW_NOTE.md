# Exact One-Parameter Reduced Sewing-Shell Law

**Date:** 2026-04-13  
**Branch:** `codex/review-active`  
**Script:** `scripts/frontier_one_parameter_reduced_shell_law.py`  
**Status:** Exact reduced-shell theorem plus bounded shell-stress interpretation

## Purpose

The gravity line had already established:

- the radial DtN shell kernel is exact
- the anisotropic shell sector is one exact reduced DtN mode

That still left one genuine open question:

> is the amplitude of that anisotropic mode an additional free datum, or is it
> already fixed by the microscopic source law on the current exact source class?

This note answers that question on the reduced shell surface.

## Exact one-parameter law

Take the seven star-support point-Green columns and compute their exact
sewing-shell source at cutoff `R = 4`.

For each unit-charge point column, the script finds:

- the same radial shell kernel per unit charge
- the same anisotropic orbit-mode vector per unit charge
- the same shell-mean exterior response per unit charge

By linearity of the exterior projector, the lattice Laplacian, and the Green
solve, this gives an exact theorem on the star-supported source class:

> on the reduced shell surface, the sewing-shell law is fixed entirely by total
> charge `Q`

Equivalently,

`sigma_red(Q) = Q * (k_rad + c_aniso * m_orb)`

where:

- `k_rad` is the exact radial DtN shell kernel
- `m_orb` is the exact reduced anisotropic DtN mode
- `c_aniso` is one exact lattice constant

The script finds:

`c_aniso = 0.081435402995901`

so the anisotropic anchor amplitude obeys

`A_aniso = c_aniso * Q`

with no extra family-dependent parameter on this reduced surface.

## Exact agreement with the current exact source families

The script then checks the two exact source families already used in the
gravity line:

1. the exact local `O_h` family
2. the broader exact finite-rank family

and finds machine-precision agreement with the same reduced one-parameter law.

So the current exact source families are not introducing an additional
independent anisotropic amplitude. They realize the same charge-fixed reduced
shell law already latent in the star-support DtN problem.

## Interpretation

This is the cleanest strong-field gravity statement so far about the sewing
shell:

> on the reduced surface relevant to the current gravity program, the exact
> sewing-shell law is one isotropic shell-density kernel plus one universal
> cubic shear mode, both tied to the same scalar charge

That is still not full nonlinear GR, but it removes one more degree of freedom
from the matching problem.

## What this closes

This closes another real ambiguity:

> on the current exact star-supported source class, the anisotropic shell-mode
> amplitude is not free; it is fixed exactly by total charge

## What this still does not close

This note still does **not** close:

1. the full shell-stress / junction interpretation of the reduced shell law
2. the lifting from reduced orbit/shell-mean data to the full nonlinear 4D
   spacetime theorem
3. the final Einstein/Regge closure

## Updated gravity target

After this note, the gravity target tightens again:

- the reduced sewing-shell law is now exact and one-parameter
- the remaining blocker is no longer the radial kernel, the anisotropic mode,
  or its amplitude
- the remaining blocker is the nonlinear shell-stress / junction
  interpretation that lifts this exact reduced shell law into the full 4D
  closure
