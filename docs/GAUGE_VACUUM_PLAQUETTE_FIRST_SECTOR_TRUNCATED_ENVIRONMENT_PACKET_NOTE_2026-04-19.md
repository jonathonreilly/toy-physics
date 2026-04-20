# Gauge-Vacuum Plaquette First-Sector Truncated Environment Packet

**Date:** 2026-04-19  
**Status:** exact retained-sector theorem on the plaquette/Wilson first-sector reopening; the completed first-sector triple already determines one explicit truncated diagonal/environment packet on the retained first-symmetric sector  
**Script:** `scripts/frontier_gauge_vacuum_plaquette_first_sector_truncated_environment_packet_theorem_2026_04_19.py`

## Question

Before the full framework-point environment packet is known, does the completed
first-sector triple at least determine an exact retained diagonal/environment
packet on the first-symmetric sector?

## Answer

Yes.

Let `v_min` be the retained first-sector coefficient vector determined by the
completed triple `Z_min`.

Then:

- `z00_min = v_min(0,0)`,
- `rho_ret = v_min / z00_min`.

For the explicit retained first-sector completion,

`v_min = (0.349606952458, 0.093393849311, 0.093393849311, 0)`,

so the normalized retained packet is

`rho_ret = (1, 0.267139565315, 0.267139565315, 0)`.

This packet is:

- normalized, `rho_(0,0) = 1`,
- conjugation-symmetric, `rho_(1,0) = rho_(0,1)`,
- nonnegative on the retained first-symmetric sector.

And it reconstructs the retained three-sample triple exactly:

`Z_min = z00_min E_3 rho_ret`.

So the remaining open object is not retained diagonal/environment packet
existence. It is the extension / realization of this retained packet inside
the full `beta = 6` environment data.

## Commands run

```bash
PYTHONPATH=scripts python3 scripts/frontier_gauge_vacuum_plaquette_first_sector_truncated_environment_packet_theorem_2026_04_19.py
```

Expected summary:

- `PASS=6 FAIL=0`
