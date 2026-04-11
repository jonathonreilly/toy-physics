# Main Open-Cubic Validation

**Date:** 2026-04-11  
**Scope:** promoted open-cubic staggered subset on `main`  
**Worktree:** `codex/main-open-cubic-validation` at `410ce75`

## Validated scripts

- `scripts/frontier_staggered_newton_reproduction.py`
- `scripts/frontier_staggered_newton_blocking_sensitivity.py`
- `scripts/frontier_staggered_3d_self_gravity_sign.py`

## Rerun results

### 1. Open-cubic staggered Newton reproduction

Rerun output matched the promoted note exactly.

- global exact-force fit: `|F0| ~ d^-2.003`, `R^2 = 0.9994`
- global blocked-trajectory fit: `|a_block| ~ d^-1.982`, `R^2 = 0.9232`
- global raw fit: `|a_raw| ~ d^-1.977`, `R^2 = 0.8411`

Per-side blocked fits:

- `side=12`: `|a_block| ~ d^-1.975`, `R^2 = 1.0000`
- `side=14`: `|a_block| ~ d^-1.997`, `R^2 = 0.9961`
- `side=16`: `|a_block| ~ d^-1.975`, `R^2 = 1.0000`

Representative rows:

- `side=12, d=3`: `F0=+8.5715e-04`, `Ff=+7.1747e-04`, `block_a=+1.1574e-04`
- `side=14, d=4`: `F0=+4.9691e-04`, `Ff=+4.5923e-04`, `block_a=+5.0381e-05`
- `side=16, d=6`: `F0=+2.1428e-04`, `Ff=+2.1900e-04`, `block_a=+2.9515e-05`

### 2. Open-cubic staggered blocking sensitivity

Rerun output matched the promoted note exactly.

Global fits:

- `raw`: exponent `-1.977`, `R^2 = 0.8411`, side span `0.190`
- `z2`: exponent `-1.982`, `R^2 = 0.9232`, side span `0.022`
- `cube2`: exponent `-1.982`, `R^2 = 0.9232`, side span `0.022`
- `cube4`: exponent `-1.658`, `R^2 = 0.2808`, side span `0.919`

All rows remained TOWARD on rerun.

### 3. 3D staggered self-gravity contraction / sign split

Rerun output matched the promoted note exactly.

Blocked width ratios:

- `side=9`: attract `0.640444`, repulse `0.640430`
- `side=11`: attract `0.634800`, repulse `0.634770`
- `side=13`: attract `0.632080`, repulse `0.631604`

Core excess:

- attract: `+0.428363`, `+0.429278`, `+0.428541`
- repulse: `+0.428364`, `+0.429244`, `+0.428475`

Field-side sign control:

- attract shell-gradient sign: `20/20` positive on every size
- repulse shell-gradient sign: `0/20` positive on every size

Trajectory-side sign separation remained absent:

- `|Δ width ratio| = 1.394913e-05`, `3.016553e-05`, `4.756634e-04`

## Discrepancies

None. The reruns reproduced the promoted notes within print precision.

## Validation verdict

The newly promoted open-cubic staggered subset is scientifically consistent on
`main`.

What this validation supports:

- the bounded open-cubic staggered external-source `d^-2` reproduction note
- the blocking-sensitivity note that shows `z2` and `2x2x2` stability
- the 3D staggered self-gravity contraction note with a clean sign-split
  positive/negative interpretation

What it does not upgrade:

- staggered both-masses closure
- staggered self-consistent two-body trajectory closure
- any broader Newton closure beyond the bounded open-cubic surfaces already
  stated in the promoted notes
