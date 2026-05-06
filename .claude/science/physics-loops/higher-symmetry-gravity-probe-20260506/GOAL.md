# Higher-Symmetry Gravity Probe Cache Closure

Target: close the failed audit chain for
`docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md`.

The failed audit did not identify a physics no-go. It identified a stale
audit-cache surface: the cache for `scripts/higher_symmetry_gravity_probe.py`
used the runner's default parameters (`N=25,40,60,80,100`,
`z2z2_quarter=12`, `connect_radius=5.0`) while the note claimed the dense
surface (`N=80,100,120`, `z2z2_quarter=16`, `connect_radius=5.2`).

Closure target:

- make the runner's audit-facing default invocation match the note's dense
  parameter surface;
- refresh the SHA-pinned runner cache consumed by the audit lane;
- state the claim narrowly as a positive-row subfit inside
  `M in {2,3,5,8}`, not rowwise positivity over the whole window and not a
  clean gravity law.

