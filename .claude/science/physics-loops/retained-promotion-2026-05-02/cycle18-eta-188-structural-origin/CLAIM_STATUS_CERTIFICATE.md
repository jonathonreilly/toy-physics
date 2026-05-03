# Claim Status Certificate — Cycle 18: Structural Origin of 0.1888

**Date:** 2026-05-03
**Cycle:** 18
**Branch:** `physics-loop/eta-188-structural-origin-2026-05-03`
**Parent target:** Cycle 09 Obstruction 3 (structural origin of 0.1888 ambiguous)
**Type:** (c) stretch attempt with partial closing on pure-rational sub-structure

## Current-surface status fields

```yaml
actual_current_surface_status: bounded-support
target_claim_type: bounded_theorem
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: g_weak = 0.653 (bare weak coupling at v_EW scale, phenomenological)
claim_type_reason: "Structural decomposition identifies five-factor product. ABC sub-factor closes to pure rational 516/53009. Three remaining factors are structural-once-Yukawa-import-resolved. Y0^2 import is the named phenomenological obstruction inherited from cycle 09 Obstruction 1 / cycle 12 R2. Cycle 09's four candidate near-fits are shown to be numerical coincidences, NOT structural identifications."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## V1–V5 Promotion Value Gate (mandatory pre-PR self-review)

### V1 — Specific verdict-identified obstruction this PR closes

**Cycle 09 Obstruction 3 verdict text:**
> "Obstruction 3: structural origin of 0.1888 ambiguous; multiple near-fits
> (17/90, 31/32·√6/(4π), (7/8)^(1/4)·√6/(4π)) consistent within sub-percent,
> none derived"

**This PR closes:** the ambiguity by identifying the EXACT structural form
of 0.1888 from the framework's transport calculation chain. The structural
form is NOT any of the four cycle-09 candidate near-fits — those are
numerical coincidences. The actual form is a five-factor product whose
ABC sub-factor closes to a pure rational 516/53009.

The Obstruction is partially closed: the structural decomposition is now
explicit. The residual phenomenological import (Y0^2) is identified as a
specific, named, isolatable factor.

### V2 — NEW derivation content

**Genuine new content not in cycle 09 catalogue or any prior cycle:**

1. **Five-factor decomposition theorem** of `eta/eta_obs` from the
   framework's `dm_leptogenesis_exact_common.exact_package()` transport
   chain:
   ```
   eta/eta_obs = (516/53009) * Y0^2 * F_CP * kappa_axiom / eta_obs
   ```
   where each factor is named, traced, and classified as
   structural / phenomenological.

2. **Pure-rational ABC closure**: the product
   `(s/n_gamma) * C_sph * d_N` reduces to `516/53009` exactly, derived
   from `g_*=427/4` (SM dofs at leptogenesis), `g_S=43/11` (CMB dofs),
   `C_sph=28/79` (sphaleron), with `pi^4` and `zeta3` cancelling
   between `s/n_gamma` and `d_N`.

3. **Falsification of all four cycle-09 near-fits** as structural
   identifications:
   - 17/90 differs from actual structural form by 0.055% — coincidence.
   - 31/32·√6/(4π) differs by 0.025% — coincidence.
   - (7/8)^(1/4)·√6/(4π) differs by 0.138% — coincidence.
   - √6/(4π) differs by 3.25% — not a near-fit at all.
   None of the four candidates contains the factors {516/53009, Y0^2,
   F_CP, kappa_axiom} that actually compute the value.

4. **Phenomenological-import isolation**: only Y0^2 = (g_weak^2/64)^2
   carries non-structural content; all other factors trace to retained
   primitives (g_*, g_S, sphaleron, M_PL, alpha_LM via PLAQ_MC, PMNS
   chart constants gamma/E1/E2/K00 with cycle-16 progress).

### V3 — Could the audit lane derive this from existing primitives?

**No.** The audit lane catalogues four candidate fits (cycle 09) and
characterizes them as "consistent within sub-percent, none derived". To
identify the actual structural form requires:

- reading the framework's transport runner
  (`dm_leptogenesis_transport_status.py` plus
  `dm_leptogenesis_exact_common.py`),
- tracing through six chained quantities (s/n_gamma, C_sph, d_N,
  epsilon_1, kappa_axiom, eta_obs),
- recognizing the rational closure of A*B*C using `g_* = 427/4` and
  `g_S = 43/11` and `pi^4*zeta3` cancellation,
- isolating Y0^2 as the unique phenomenological import.

This is multi-step content from framework code, not a textbook
identity, and the audit-lane verdict explicitly says "none derived".

### V4 — Marginal content non-trivial

**Yes.** The marginal content is non-trivial because:

- The pi^4 and zeta3 cancellation across (s/n_gamma) and d_N is not
  a textbook identity — it requires recognizing both factors share
  the same thermodynamic origin and have been computed to high
  precision in the framework's standard form.
- The reduction `516/53009 = (3*7*172)/(79*7*671) = 516/(79*11*61)`
  uses the specific structural integers `g_*=427/4` (where 427 = 7*61)
  and `g_S=43/11`, both retained framework primitives.
- The falsification of cycle 09's candidates is itself substantive:
  recognizing that 17/90 and 31/32·√6/(4π) are accidental rationalists,
  not structural identifications, requires comparing the actual form
  to each candidate.

### V5 — One-step variant of an already-landed cycle?

**No.** Closest prior cycle is cycle 09 (the catalogue cycle).
Structural distinction:

- **Cycle 09**: catalogues four near-fits to 0.1888 without deriving
  their structural origin; explicitly leaves Obstruction 3 open.
- **Cycle 18**: identifies the actual five-factor decomposition,
  closes the ABC sub-factor as pure rational 516/53009, falsifies
  all four cycle-09 candidates as numerical coincidences, and
  isolates Y0^2 as the unique phenomenological obstruction.

The structural distinction is *categorical*: cycle 09 says "we don't
know what 0.1888 is structurally". Cycle 18 says "0.1888 = (516/53009)
× Y0^2 × F_CP × kappa, with Y0^2 the only non-structural factor".

The closest sibling (not a prior cycle) is cycle 12 (epsilon_1 chain),
which sharpens the epsilon_1 / cp1 / cp2 inputs. Cycle 18 is downstream
of cycle 12: it uses the cycle-12 ratios, but rather than re-deriving
them, it integrates them into the full eta/eta_obs decomposition.

### V1–V5 verdict

All five gate questions pass. PR allowed.

## Forbidden imports — discipline check

- [x] No PDG observed values consumed as derivation inputs
  (eta_obs is comparator only).
- [x] No literature numerical comparators consumed.
- [x] No fitted selectors consumed.
- [x] No same-surface family arguments.
- [x] g_weak = 0.653 is **acknowledged** as a phenomenological import,
  flagged as the named residual obstruction (cycle 09 O1 / cycle 12 R2),
  not a derivation input. Cycle 18 does not USE g_weak to derive
  anything new; it identifies g_weak as the phenomenological factor
  in the structural decomposition.

## Expected outcome and disposition

**Outcome: bounded-support / partial-closing / falsification.**

- The pure-rational ABC sub-factor IS a closing identification
  (516/53009).
- The remaining factors (CP package, kappa_axiom) are
  structural-functional, with their non-structural content isolated
  to Y0^2.
- The four cycle-09 candidates are FALSIFIED as structural origins:
  none of them contains the actual factors that compute 0.1888.

**Audit-lane disposition:** This certificate should treat cycle 18 as a
*partial closing* of cycle 09 Obstruction 3. The Obstruction's residual
content (after this cycle) is the Y0^2 phenomenological import, which
is the same residual already named in cycle 09 Obstruction 1 / cycle
12 R2 (leptogenesis convention 0.77%). The structural-origin question
itself is now resolved: 0.1888 has the explicit five-factor form, with
ABC = 516/53009 closing.

## Imports inventory

**Retained / structural inputs (used downstream):**
- `g_* = 427/4` (SM dofs at leptogenesis scale, structural integer combination)
- `g_S = 43/11` (CMB dofs, structural)
- `C_sph = 28/79` (sphaleron, structural rational)
- `M_PL` (Planck mass, dimensional reference)
- `PLAQ_MC = 0.5934` → `alpha_LM = 0.0907` (lattice MC, framework primitive)
- `gamma = 1/2`, `E1 = √(8/3)`, `E2 = √8/3`, `K00 = 2`
  (PMNS chart constants, retained via cycle 12 / 16 progress)
- `(7/8)^(1/4)` (APBC factor in v_EW, structural)
- `eta_obs = 6.12e-10` (comparator only, NOT a derivation input)

**Phenomenological imports (named obstructions):**
- `g_weak = 0.653` → `Y0 = g_weak^2/64` → `Y0^2` enters epsilon_1 and
  K_decay. This is the unique non-structural factor in the entire
  five-factor decomposition.

## Branch isolation

- Branch: `physics-loop/eta-188-structural-origin-2026-05-03`
- Created clean from `origin/main` post-fetch.
- No interaction with parallel cycles 17 (`v-even-theorem-retention`)
  or 19 (`pl-s3-atlas-refinement`); no shared files modified.
