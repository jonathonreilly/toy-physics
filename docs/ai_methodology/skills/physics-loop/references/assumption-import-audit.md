# Assumption And Import Audit

Run this audit before new physics work. The goal is to expose what the lane
depends on and which dependencies block retained or Nature-grade status.

## Ledger Schema

Use this table in `ASSUMPTIONS_AND_IMPORTS.md`:

| Item | Role in claim | Current class | Source surface | Load-bearing? | Needed for target status? | Retirement path | Disposition |
|---|---|---|---|---|---|---|---|

## Classes

Use the narrowest honest class:

- `zero-input structural`: forced by the retained framework surface;
- `framework-derived`: computed from retained framework plus named bridge;
- `retained support`: exact reusable support, not itself headline closure;
- `computed lattice input`: produced by a named runner/log on the current
  surface;
- `admitted normalization`: explicit convention or boundary condition with a
  narrow role;
- `literature theorem`: imported theorem or mathematical fact with source;
- `standard correction`: known correction used as bridge context;
- `observational comparator`: measured target used only for comparison;
- `fitted input`: value tuned to the target, not a derivation;
- `support-only`: useful but not closure-grade;
- `insensitive nuisance`: input shown not to affect the claim materially;
- `unsupported import`: hidden or unjustified dependency.

## Nature-Grade Criteria

For a retained or Nature-grade claim, every load-bearing item must be:

- derived from retained structure;
- retained/exact support with a named bridge;
- explicitly admitted with a narrow non-derivation role;
- quantitatively insensitive; or
- demoted out of the retained claim.

If a selector, unit identification, normalization, target value, chamber
choice, or observed quantity remains hidden, the claim is not retained closure.

## Retirement Paths

For each load-bearing import, name a possible retirement path:

- theorem route;
- exact runner/log route;
- atlas reuse route;
- no-go route that demotes the claim honestly;
- literature bridge that narrows but does not derive the input;
- human decision required.

If no retirement path is visible, mark it as an open Nature-grade blocker.
