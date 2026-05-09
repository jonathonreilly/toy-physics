# Dense Prune Guard Seed Note

**Audit-lane runner update (2026-05-09):** the primary runner `scripts/channel_count_guarded_prune.py` previously timed out under the audit-lane 120s default budget; AUDIT_TIMEOUT_SEC=1800 has been declared and the cache refreshed under the new budget. The runner output and pass/fail semantics are unchanged.

This note compares the exact flip-prone seed IDs from the replay work against the current channel-count guard path.

The code path has evolved a bit since the earlier replay logs, so treat these as same-seed diagnostic comparisons rather than a literal byte-for-byte rerun of the older numbers.

Historical flip seeds from the replay set:
- `N=80`: seeds `8, 12, 13`
- `N=100`: seeds `2, 3, 13`

Current guard path:
- `scripts/channel_count_guarded_prune.py`
- guard mode: channel-count preserving, `q=0.10`

## Per-seed comparison

### N = 80

| seed | mode | grav_b | grav_p | d_grav | pur_b | pur_p | d_pur | eff_b | eff_p | flip |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 | plain | +0.235 | +6.003 | +5.768 | 1.0000 | 0.9773 | -0.0227 | 4.14 | 3.92 | 0 |
| 8 | guard | +0.235 | +1.697 | +1.462 | 1.0000 | 0.9938 | -0.0062 | 4.14 | 6.64 | 0 |
| 12 | plain | +0.436 | -0.214 | -0.650 | 0.9994 | 0.9804 | -0.0190 | 8.22 | 5.80 | 1 |
| 12 | guard | +0.436 | +3.753 | +3.317 | 0.9994 | 0.9742 | -0.0252 | 8.22 | 8.99 | 0 |
| 13 | plain | -0.239 | +3.254 | +3.493 | 1.0000 | 0.8250 | -0.1750 | 8.82 | 7.55 | 0 |
| 13 | guard | -0.239 | -0.239 | +0.000 | 1.0000 | 1.0000 | +0.0000 | 8.82 | 8.82 | 0 |

### N = 100

| seed | mode | grav_b | grav_p | d_grav | pur_b | pur_p | d_pur | eff_b | eff_p | flip |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | plain | +9.334 | +0.327 | -9.007 | 1.0000 | 0.9994 | -0.0006 | 5.36 | 2.84 | 0 |
| 2 | guard | +9.334 | +10.258 | +0.924 | 1.0000 | 1.0000 | -0.0000 | 5.36 | 4.44 | 0 |
| 3 | plain | +0.486 | -0.545 | -1.031 | 1.0000 | 0.9957 | -0.0043 | 3.02 | 2.72 | 1 |
| 3 | guard | +0.486 | -0.424 | -0.910 | 1.0000 | 0.9981 | -0.0019 | 3.02 | 2.60 | 1 |
| 13 | plain | +3.652 | -0.054 | -3.707 | 0.9999 | 0.9959 | -0.0040 | 4.09 | 2.97 | 1 |
| 13 | guard | +3.652 | +3.652 | +0.000 | 0.9999 | 0.9999 | +0.0000 | 4.09 | 4.09 | 0 |

## Readout

The guard is not just changing the average. It fixes specific seeds when it preserves the effective detector-channel count (`eff_ch`) and leaves other seeds vulnerable when `eff_ch` still drops.

The clearest rescue cases are:
- `N=80`, seed `12`: flip removed and `eff_ch` rises `8.22 -> 8.99`
- `N=100`, seed `13`: flip removed and `eff_ch` stays at `4.09`

The clearest non-rescue case is:
- `N=100`, seed `3`: flip remains and `eff_ch` still falls `3.02 -> 2.60`

So the guard is a seed-selective channel-preservation mechanism, not a pure averaging fix.
