# Review: `codex/lepto-selector-closeout-main-2026-04-17`

## Verdict

This branch does **not** close the DM selector lane.

Current status after review:

- `DM_NEUTRINO_SOURCE_SURFACE_ZERO_IMPORT_ACTIVE_QUADRATIC_SELECTOR...`
  does **not** clear.
- `DM_NEUTRINO_SOURCE_SURFACE_MINIMAL_ACTIVE_DISPLACEMENT_SELECTOR...`
  is mathematically fine as a **conditional** theorem, but it is **not**
  theorem-native closeout.

So nothing here is ready to wire through `main` as selector closure.

## Findings

### 1. Zero-import quadratic still depends on a special scalar baseline

The claimed native quadratic

- `Q_act(delta,q_+) = 6(delta^2 + q_+^2)`

is only obtained after restricting the observable-principle generator to

- `D = m I_3`.

That scalar baseline is not itself derived from the accepted active-bank
surface. Under generic positive baselines, the active curvature is not
isotropic and picks up a mixed term.

Concrete counterexample used in review:

- `D = diag(1,2,3)` gives
  - `K(T_delta,T_delta) = 2.027777...`
  - `K(T_q,T_q) = 2.0`
  - `K(T_delta,T_q) = -1/3`

So the isotropic quadratic is not currently a canonical old-bank theorem.

### 2. The selector principle is still being inserted at the end

Even after deriving the scalar-baseline quadratic, the note closes by
minimizing that quadratic on the active chamber and declaring that minimizer
to be the physical point.

That is still an extra selector principle unless you derive one of:

- why the physical point is the minimizer of that descended curvature,
- why the scalar baseline is the canonical one selected by the old bank,
- or the missing right-sensitive `2`-real `Z_3` doublet-block law directly.

Without one of those, the old variational selector has only been repackaged.

### 3. Minimal active-displacement is conditional support only

This note is internally clean, but it explicitly adds a new right-sensitive
input:

- the physical point minimizes the Frobenius active displacement.

That makes it a legitimate **conditional comparison theorem**, not a closeout
of the theorem-native DM lane.

## What To Do

### Option A: salvage the zero-import note honestly

Do **not** present it as selector closure.

Instead:

- rename the note and runner to a bounded diagnostic status
- make the title/status match the actual result, e.g. scalar-baseline active
  quadratic diagnostic
- explicitly state that the law is exact only on the chosen scalar baseline
- explicitly state that minimizing the quadratic is **not** yet derived as the
  physical selector principle
- explicitly state the exact remaining attack target

Safe statement:

- on the chosen scalar baseline `D = m I_3`, the observable-principle
  curvature yields an exact comparison quadratic on the active pair whose
  chamber minimizer is `(sqrt(6)/3, sqrt(6)/3)`.

Unsafe statement:

- zero-import selector theorem / selector closeout / old-bank-only closure

### Option B: keep the minimal active-displacement note, but relabel it

This note can stay if you package it honestly as:

- conditional support theorem
- explicit new-input theorem
- comparison route for future selector work

Required edits:

- status line must say conditional / new-input / bounded support
- theorem statement must continue to foreground the new right-sensitive input
- remove any language implying old-bank-only closure

### Option C: actually close the lane

To come back with a real selector closeout, derive at least one of the
following on retained surfaces:

1. a theorem-native reason the physically relevant descended curvature must be
   evaluated on a canonical scalar baseline
2. a theorem-native reason the physical active point is selected by minimizing
   a specific right-sensitive functional on the chamber
3. the missing right-sensitive `2`-real `Z_3` doublet-block selector law
   directly

Absent one of those, the lane is still open.

## Packaging Guidance

Do **not** wire either note through:

- `DERIVATION_VALIDATION_MAP.md`
- `CLAIMS_TABLE.md`
- `PUBLICATION_MATRIX.md`
- front door
- manuscript / arXiv

Only possible near-term salvage:

- zero-import note as a bounded diagnostic/comparison tool
- minimal-displacement note as a conditional support note

If you pursue the bounded diagnostic route later, it can potentially be added
to the atlas as a diagnostic tool, but **not** as selector closure.

## Naming Rule

Please keep note names and statuses aligned with what they actually prove.

Examples:

- `...ZERO_IMPORT...THEOREM...` is wrong if the note still depends on a chosen
  scalar baseline plus an inserted minimization principle
- `...MINIMAL_ACTIVE_DISPLACEMENT_SELECTOR_THEOREM...` is acceptable only if
  the header/status clearly says it is conditional on a new input

## Bottom Line

The branch is useful, but not as closeout.

The zero-import route is still blocked by:

- baseline dependence
- missing physical minimization principle

The minimal-displacement route is still:

- a conditional theorem with a new selector input

That is the honest state of the lane.
