# Central-Band Dense Joint Card Note

**Date:** 2026-04-02  
**Status:** complete, bounded same-graph joint card

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/central_band_dense_joint_card.py` exits 0 with PASS in the current cache; the prior audit verdict citing an unregistered artifact was generated against an earlier cache state and is invalidated by this source-note hash drift.

This note records the same-graph joint card for the dense central-band pocket
that is already Born-clean on the corrected three-slit harness.

Script:
[`scripts/central_band_dense_joint_card.py`](/Users/jonreilly/Projects/Physics/scripts/central_band_dense_joint_card.py)

## Setup

- corrected dense central-band graph family
- `N = 40, 60`
- `npl = 60`
- `y_cut = 2.0`
- `yz_range = 12.0`
- `connect_radius = 3.0`
- `4` matched seeds
- `8` Monte Carlo realizations for the collapse rows

## Strongest Retained Rows

The dense pocket is Born-clean at machine precision for both retained LN
rows.

| N | mode | Born `|I3|/P` | `pur_min` / purity | gravity delta | note |
|---|---|---:|---:|---:|---|
| 40 | `LN + |y|` | `0.000±0.000` | `1.000±0.000` | `-0.529±0.497` | Born-safe, but not yet a positive gravity row |
| 40 | `LN + |y| + collapse` | `0.000±0.000` | `0.587±0.065` | `-0.554±0.493` | collapse helps purity, gravity still negative |
| 60 | `LN + |y|` | `0.000±0.000` | `0.875±0.125` | `+0.455±0.384` | retained joint row |
| 60 | `LN + |y| + collapse` | `0.000±0.000` | `0.550±0.082` | `+0.454±0.385` | best purity on the dense pocket |

## Narrow Read

- The dense central-band pocket is Born-clean on the corrected harness.
- `N=40` is Born-clean but not yet a retained joint gravity row.
- `N=60` is the retained same-graph joint row:
  - `LN + |y|` keeps gravity positive
  - `LN + |y| + collapse` lowers purity further while keeping gravity positive
- The collapse term improves the purity floor inside the dense pocket, but
  it does not change the gravity mean in this sample.

## Interpretation

This is the cleanest same-graph statement so far for the dense central-band
lane:

- corrected Born survives at machine precision
- the hard-geometry lane keeps a real decoherence improvement
- the collapse term can sit inside the pocket without breaking Born
- the retained coexistence window is still bounded, with the strongest
  positive gravity row at `N = 60`

