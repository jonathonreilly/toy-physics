# Koide residual atlas second reassessment

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_residual_atlas_second_reassessment.py`  
**Status:** route selection; not closure

## Residuals

The live residuals remain:

```text
RESIDUAL_Q = equal_C3_center_label_source_equiv_K_TL
RESIDUAL_DELTA = open_selected_line_Berry_APS_endpoint
```

## Forbidden shortcuts

The next route cannot:

```text
postulate equal labels
postulate K_TL vanishing
choose a zero moment-map/FI level because it closes Q
choose a Berry endpoint because it equals eta_APS
fit Brannen delta by endpoint gauge
promote source-free algebra to physical closure.
```

## Fresh route atlas

The runner ranks ten genuinely distinct routes:

```text
D-term / moment-map neutrality for C3 center source
Osterwalder-Schrader reflection positivity on the source carrier
Cobordism / invertible-phase classification beyond mod-2 anomaly
Markov-category terminal-state theorem for classical center labels
Noncommutative-geometry real-action spectral triple with finite Hilbert state
Adiabatic spectral-projector endpoint theorem
Relative eta/rho endpoint theorem
Dai-Freed functorial gluing with selected boundary condition
Spectral-flow endpoint quantization with fractional offset removed
Joint Q/delta cobordism boundary source functor.
```

## Selected next attack

The highest-ranked fresh Q route is:

```text
frontier_koide_q_moment_map_dterm_source_no_go.py
```

Reason: a D-term or moment-map equation is a physical mechanism that can set a
real scalar to zero without invoking a label-counting prior.  The hostile risk
is that the zero level is an FI/source parameter rather than a retained law.

## Boundaries

This note does not close Q or delta.  It records a nonlocal step-back and
route-ranking checkpoint so the work does not keep cycling through the same
local obstruction.

## Verification

Run:

```bash
python3 scripts/frontier_koide_residual_atlas_second_reassessment.py
```

Expected closeout:

```text
KOIDE_RESIDUAL_ATLAS_SECOND_REASSESSMENT=TRUE
KOIDE_RESIDUAL_ATLAS_SECOND_CLOSES_Q=FALSE
KOIDE_RESIDUAL_ATLAS_SECOND_CLOSES_DELTA=FALSE
RESIDUAL_Q=equal_C3_center_label_source_equiv_K_TL
RESIDUAL_DELTA=open_selected_line_Berry_APS_endpoint
NEXT_ATTACK=frontier_koide_q_moment_map_dterm_source_no_go.py
```
