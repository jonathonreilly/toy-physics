# Exact One-Parameter Reduced Sewing-Shell Law

**Date:** 2026-04-13  
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

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream operators
the load-bearing linearity step relies on, in response to the
2026-05-05 audit verdict's `missing_dependency_edge` repair target
(audit row: `one_parameter_reduced_shell_law_note`). It does not
promote this note or change the audited claim scope, which remains the
linearity-from-identical-normalized-columns argument plus the two
exact source-family checks at cutoff `R = 4`.

The runner `scripts/frontier_one_parameter_reduced_shell_law.py`
imports five frontier helper modules via `_frontier_loader.load_frontier`:

- `frontier_star_shell_projector.py` — exterior projector and
  shell-mean operator.
- `frontier_same_source_metric_ansatz_scan.py` — exact source-family
  constructors (the exact local `O_h` family and the broader exact
  finite-rank family checked in §"Exact agreement with the current exact
  source families").
- `frontier_coarse_grained_exterior_law.py` — coarse-grained exterior
  law on the truncated star.
- `frontier_sewing_shell_source.py` — sewing-shell projection at
  cutoff `R = 4`.
- `frontier_radial_shell_matching_law.py` — radial shell kernel
  `k_rad` and the radial-shell average operator.

None of these helper modules currently has a dedicated retained
audit-clean source note registered as a one-hop authority for this row.
The audit verdict treats this as a `missing_dependency_edge` (or, if
no retained authority exists at all, a `missing_bridge_theorem`).

Open registration targets (class D gaps):

- A retained source note for the `star_shell_projector` exterior
  projector and shell-mean operator.
- A retained source note for the `same_source_metric_ansatz_scan`
  exact source-family constructors covering both the local `O_h` family
  and the broader finite-rank family.
- A retained source note for the `coarse_grained_exterior_law`.
- A retained source note for the `sewing_shell_source` projection at
  cutoff `R = 4`.
- A retained source note for the `radial_shell_matching_law` exact
  radial DtN shell kernel `k_rad` and the radial-shell average
  operator.

The runner-checked content of this note (seven point-Green columns
carrying unit total charge to machine precision; identical radial
profile, identical orbit-mode vector, identical shell-mean
exterior response per unit charge across all seven; the resulting
reduced one-parameter law `sigma_red(Q) = Q * (k_rad + c_aniso *
m_orb)` with `c_aniso = 0.081435402995901`; machine-precision
agreement of the two exact source families with the same one-parameter
law) is exact lattice arithmetic on the constructed objects and is
independent of the registration status of the underlying helper
modules. The cite-chain repair simply records that those operators
and source families currently sit as runner-defined inputs rather than
audit-clean retained authorities, matching the verdict's
`missing_dependency_edge` flag.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with the
substantive observation that the runner produces six classified A-class
PASS lines (plus one B-class summary) on the reduced shell calculation,
but the load-bearing operators — exterior projector, lattice Laplacian
encoded in the Green solve, source-family constructors, and the radial
DtN shell kernel — are imported from frontier modules that the
restricted packet does not certify as audit-clean retained authorities.
The audit's repair target is either (a) wire those modules to retained
authority notes, or (b) recognize that no retained authority currently
exists, in which case the gap is a real `missing_bridge_theorem`. The
explicit registration above implements path (a) by listing the five
helper modules as open registration targets rather than asserting any
already-retained authority. Effective status remains
`audited_conditional`. The note's audit_status is unchanged by this
addendum.

## Scope of this rigorization

This rigorization is class D (gap registration). It does not change any
algebraic content, runner output, or load-bearing step classification.
It registers the five frontier helper modules as open one-hop
dependency targets matching the audit verdict's named missing
dependency edges. Mirrors the live cite-chain pattern used by the
`DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `02ad4fadd`).
