# Lane 4 — Neutrino Quantitative Closure Loop

**Goal:** close Lane 4 at the strongest honest claim-state. Phase-1 priorities
are **4D Dirac vs Majorana global lift** (Tier B; current-stack Majorana
zero law already retained) and **4E seesaw quantitative spectrum closure**
(Tier B-C; Phase 4 of `MASS_SPECTRUM_DERIVED_NOTE.md` is partial).

**User invocation:** `/physics-loop Lane 4 (neutrino quantitative)
--mode run --runtime 4h` (Lane 3 is locked to another worker).

**Target status:** `best-honest-status`. Retained closure if achievable;
substantial exact support, no-go, or import retirement otherwise. Pure
prose passes do not count. Deep Work Rules apply: after 2 audit-grade
cycles, the next cycle must be a stretch attempt from minimal axioms.

## Lane reduction (per lane file)

Per
[`docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md`](../../../../docs/lanes/open_science/04_NEUTRINO_QUANTITATIVE_OPEN_LANE_2026-04-26.md),
the **first parallel-worker target** is to inventory retained neutrino/DM
inputs and separate direct quantitative targets from bounded or
phenomenological forecasts.

The seven derivation targets are:

- **4A** absolute neutrino mass `m_lightest` (Tier C)
- **4B** `Delta m^2_21` solar mass-squared difference (Tier B-C)
- **4C** `Delta m^2_31` atmospheric mass-squared difference (Tier B-C)
- **4D** Dirac vs Majorana global lift (Tier B; current-stack zero law
  already retained — **the most achievable Phase-1 target**)
- **4E** seesaw mass spectrum quantitative closure (Tier B-C; Phase 4 of
  `MASS_SPECTRUM_DERIVED_NOTE.md` is partial)
- **4F** cosmological `Sigma m_nu` constraint (Tier B; connects to Lane 5)
- **4G** cross-validation with retained `delta_CP ≈ -81°` and `theta_23`
  upper octant (Tier A; internal consistency check)

## Loop priorities

In order of next-cycle execution:

1. **Cycle 1 — Route R1 (lane-file's first parallel-worker target):**
   inventory retained neutrino/DM content + separate quantitative targets
   from bounded forecasts (Tier A). Produces grounding for subsequent
   cycles.
2. **Cycle 2 — Route R2 (Dirac global lift attempt, 4D):** lift the
   current-stack Majorana zero law to a global statement. Tier B.
   Existing retained scaffolding: `NEUTRINO_MAJORANA_CURRENT_STACK_ZERO_LAW_NOTE`
   and `NEUTRINO_MASS_REDUCTION_TO_DIRAC_NOTE`.
3. **Cycle 3 — Route R3 (seesaw spectrum partial→retained, 4E):** promote
   Phase 4 partial to retained spectrum. Tier B-C.
4. **Cycle 4 — stretch attempt** (per Deep Work Rules if Cycles 1-2 were
   audit-grade): pick one of `m_lightest` / `Delta m^2_31` / Σm_ν and
   work it from minimal axioms for at least `--deep-block` (90 min).
5. **Cycle 5+ — stuck fan-out** before any honest stop: 3-5 orthogonal
   attack frames on the remaining hardest residual.

## Delivery

Science-only on branch `frontier/neutrino-quantitative-20260428`. Push
that branch to `origin`. Loop will open one review PR at end (per new
physics-loop skill PR policy) unless `--no-pr` is supplied. Proposed
repo-wide weaving recorded in `HANDOFF.md` only; not applied on this
branch.
