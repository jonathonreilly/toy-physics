# Frontier Map: 2026-03-30

## Coverage Summary
- Total scripts: 192
- Total log files: 46
- Mechanism families: ~8 (pocket_wrap dominant, plus long, taper, threshold, secondary, extended, wider, route)
- Confirmed results: 6 (effective delay, gravity-like continuation, record-based interference suppression, stable mechanism families, family growth without proliferation, shared structure in low-overlap basin)
- Unvalidated observations: several (beyond-ceiling packet behavior, ultra shoulder depletion pattern, non-base generated transfer failures)
- Dead ends: non-base exhausted wall (explicitly empty), rect-only beyond-ceiling continuation (tested, stays rect-local)

## Family Census

| Family | Scripts | Logs | Focus | Status |
|--------|---------|------|-------|--------|
| pocket_wrap_suppressor | 144 | 46 | Low-overlap order parameters, mechanism classification, frontier compression | ACTIVE — dominant thread |
| long_* | 20 | 0 | Degree thresholds, hub mechanisms, neighborhood basis, motif ablation | EXHAUSTED — no recent logs |
| taper_wrap | 7 | 0 | Cross-context jumps, endpoint analysis, shell mode, offender interpolation | PARTIAL — scripts exist, no recent standalone logs |
| threshold | 3 | 0 | Core-shell mechanisms, scaling | EXHAUSTED — no recent logs |
| secondary | 2 | 0 | Offender rule generalization/search | EXHAUSTED |
| extended | 2 | 0 | Atomic route overlap, route classification | EXHAUSTED |
| wider | 1 | 0 | Generated family mechanism check | PARTIAL |
| overnight/automation | 5 | 0 | Batch runners, lock management, push helpers | INFRASTRUCTURE |

## Parameter Space Gaps

### Heavily Explored
- Low-overlap order parameters across pocket_wrap_suppressor families (41 scripts, 46 logs)
- Beyond-ceiling subbranch comparisons (wider, ultra sentinel guardrails)
- Anchor-balance band geometry (anchor_closure_intensity_gap, mid_anchor_closure_peak)
- Support-collapse domain edges (zero-support guard)

### Under-Explored (ranked by information value)

1. **Interference / two-slit regime** — `two_slit_distribution()` exists in the simulator with record_created toggle and phase_shift, but NO scripts or logs explore this systematically with parameter sweeps. The record-based interference suppression claim (Result #3) has no dedicated sweep testing how the suppression threshold depends on record durability.

2. **Geodesic comparison across distortion strengths** — `compare_geodesics()` exists and is used in benchmarks, but NO parameter sweep varies the *strength* of the persistent-pattern distortion to trace the gravity-like bending from zero distortion to strong distortion. The gravity claim (Result #2) lacks a quantitative distortion-response curve.

3. **Continuation landscape topology** — `stationary_action_path()`, `frontier_distorted_action_tree()` exist. The action landscape (the "continuation structure" that produces inertia-like behavior) has not been mapped as a function of network size or topology variation. How does the number/depth of action minima scale?

4. **Self-maintenance rule space** — `scan_self_maintaining_rules_fallback_only()`, `select_self_maintenance_rule()` exist. The space of viable self-maintenance rules has not been systematically swept. Which rules produce stable persistent patterns and which don't? What's the boundary?

5. **Cross-family observable transfer** — The low-overlap law transfers within the pocket_wrap_suppressor family but breaks on taper-wrap/skew-wrap generated families. No systematic study of WHICH observables transfer vs. which are family-specific.

## Observable Coverage

| Observable Category | Measured | Multi-Family | In Code But Not Swept |
|---------------------|----------|-------------|----------------------|
| Support/closure load | YES | YES | - |
| Anchor geometry (gap, peak, deep_share) | YES | YES | - |
| Bridge topology (right_count, right_low) | YES | YES | - |
| Edge identity (event_count, density) | YES | PARTIAL | - |
| Boundary roughness | YES | NO | roughness sweep |
| Geodesic comparison (free vs distorted) | YES | NO | distortion strength sweep |
| Two-slit distribution | BASIC | NO | phase_shift sweep, record threshold sweep |
| Action discriminator | YES | NO | action landscape mapping |
| Pattern persistence lifetime | CODE EXISTS | NO | stability vs parameters |
| Perturbation weight stability | CODE EXISTS | PARTIAL | systematic sweep |

## Top 5 Highest-Value Gaps

1. **Record-suppression threshold sweep in two-slit setup** — The interference claim is qualitative. Sweeping `record_created` is binary; the real question is how PARTIAL or DELAYED record formation affects the distribution. The simulator has `phase_shift_upper` and the machinery for this. **Why high-value:** Would give the first quantitative curve connecting record durability to interference suppression — the model's version of decoherence. **Effort:** Interactive, ~1 hour. Can adapt `two_slit_distribution()` directly.

2. **Distortion-response curve for gravity-like bending** — Sweep the number/placement of persistent nodes to trace path-bending from zero to strong. **Why high-value:** The gravity claim needs a quantitative relationship, not just "bending happens." **Effort:** Interactive, ~2 hours. Uses `compare_geodesics()` directly.

3. **Action landscape topology as a function of network size** — Map the action tree depth, branching, and minima count vs grid size. **Why high-value:** Tests whether "locally simplest continuation" (Axiom 6) produces qualitatively different behavior at different scales — a scale-dependence question fundamental to the model. **Effort:** Interactive to autopilot, ~2-4 hours.

4. **Self-maintenance rule viability boundary** — Systematic sweep of rule parameters to map which produce stable persistent patterns. **Why high-value:** The entire model depends on persistent patterns existing. Understanding when they DON'T exist is as important as when they do. **Effort:** Autopilot, ~4 hours.

5. **Cross-family observable invariance** — Identify which observables are "universal" (same across families) vs "family-specific." **Why high-value:** Would tell us which features of the model are structural vs. accidental. **Effort:** Interactive, ~2 hours. Uses existing log data.

## Dead Ends (do not revisit)

- **Non-base exhausted wall** — Explicitly empty frontier; no non-base families match the packet lift mechanism.
- **Rect-only beyond-ceiling continuation** — Tested through wider|ultra|mega. Stays rect-local. Only expands at base peta|exa with taper-hard.
- **Non-rect late guardrails (large, mirror families)** — Scanned through exa. Empty at all tiers.
- **long_* degree/hub/threshold mechanisms** — 20 scripts, 0 recent logs. Appears to have been a prior research thread that was superseded by the low-overlap order-parameter work.
