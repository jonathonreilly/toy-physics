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

## Counterfactual Pass

The import ledger above catalogs **explicit external dependencies**. The
counterfactual pass surfaces **implicit framework choices** — the
assumptions you usually treat as fixed (geometry, boundary conditions,
observable definitions, irrep truncations, traversal conventions,
sector choices, normalization conventions) — and asks what alternatives
they hide.

The exercise's payoff is route discovery. A blocked lane often has a
silent assumption no one challenged; relaxing it reveals a route the
ledger alone never names.

### Protocol

For each item in the import ledger AND each implicit framework choice
on the active lane, write a row:

| Assumption | What if it's wrong? | Concrete alternative | Direction it opens | Feasibility | Score |
|---|---|---|---|---|---|

Definitions:
- **Assumption**: one sentence. Include implicit choices: e.g.
  "we use the L_s=2 PBC cube as the V-invariant minimal block",
  "the Wilson plaquette uses +d1+d2-d1-d2 traversal",
  "boundary condition is periodic in time".
- **What if it's wrong?**: state the negation concretely, not as
  "what if A is wrong then A is wrong".
- **Concrete alternative**: name the replacement (another geometry,
  another observable form, another boundary condition, another
  truncation level, etc.). If no alternative exists, mark
  `forced` and skip.
- **Direction it opens**: does the alternative admit simpler closure,
  escape a known no-go, change the headline number, reveal a new
  bridge, or expose a hidden no-go? One sentence.
- **Feasibility**: `live` (worth pursuing), `infeasible`
  (contradicts retained theorem — name it), or `falsified`
  (contradicts observed/computed data — name it).
- **Score**: retained-positive probability × verifiability,
  rough 0-3.

### Allowed counterfactual outcomes

A counterfactual is **only** a route candidate if its closure path
fits one of these allowed shapes:

1. **Derivation from existing retained primitives**: the alternative
   is itself derivable from the current authority surface — no new
   axiom needed.
2. **Take an import → bounded theorem/support → retire it**: import a
   theorem, value, or convention with a narrow non-derivation role;
   the resulting headline status caps at **bounded theorem/support**, and
   the next work in this lane is the import-retirement audit.
3. **Demote**: the assumption is correct but the claim it supports
   is weaker than previously stated; demote status honestly.
4. **Forced finding**: no live alternative exists. Record the
   negative result; do not invent a route.

Forbidden counterfactual outcomes (these are NOT routes):

- **"Adopt a new axiom that says X is different"** — the repo does
  NOT accept new axioms. `A_min` means the minimum axiom set, NOT
  permission to extend it. A counterfactual that requires extending
  the axiom stack is `infeasible` regardless of how productive its
  consequences would be.
- **"Add a hypothetical premise and map consequences"** — allowed
  only as `hypothetical consequence map` artifacts, never as a
  retained-grade route. The `hypothetical_axiom_status` field exists
  to label such maps as conditional-on-unadopted-axiom; it is not a
  promotion path.
- **"Treat an observed value or fitted selector as a derivation
  input"** — already a forbidden import, called out here for the
  counterfactual context: a counterfactual that turns into a
  fit-to-target is `falsified` as a route.

### Synthesis

After enumerating, pick the **2-3 highest-scoring live counterfactuals**
that fit an allowed outcome and add them to `ROUTE_PORTFOLIO.md` as
new candidate routes. The `infeasible` and `falsified` rows are not
new routes, but their elimination clarifies what's actually
constrained vs chosen — which itself sharpens future stretch attempts.

If every counterfactual scores `0` or is `infeasible`/`falsified`, the
lane's framework choices are genuinely forced and the blocker is in
the load-bearing imports, not the surrounding choices. That itself
is a useful finding: it narrows the next campaign to either an
import-retirement audit or a deep stretch attempt within the existing
axiom stack.

### When to run

- After the import ledger (workflow step 3), before route generation.
- When the route portfolio (step 5) returns only routes that re-use
  the same load-bearing assumptions and produces low-novelty cycles.
- As the stretch-attempt input when the Deep Work Rules trigger
  (step 9): the counterfactual pass is a fast way to find the next
  named hard residual.

### Anti-patterns

- A counterfactual that simply restates the assumption ("what if A
  is wrong? then A would be wrong") is no use. Each row must name a
  concrete alternative AND a concrete direction.
- Listing only counterfactuals that contradict retained theorems
  ("what if SU(3) gauge invariance is wrong?") is showmanship, not
  route discovery. Filter for ones that touch the lane's actual
  load-bearing assumptions.
- Generating 30 counterfactuals and not synthesizing — the value is
  in the 2-3 picked, not the enumeration itself.
