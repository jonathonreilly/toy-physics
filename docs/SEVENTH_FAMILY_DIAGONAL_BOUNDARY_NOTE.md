# Seventh Family Diagonal Boundary Note

The diagonal-stripe seventh-family scout is highly selective.

Exact-gate result:
- exact zero-source baseline survives on every tested row
- exact neutral cancellation survives on every tested row
- the sign gate is the selector
- weak-field `F~M` stays close to `1` on the tested rows and does not rescue
  the failing sign rows

Sweep summary:
- passing rows: `6/18`
- passing rows: `drift = 0.0` seeds `0,1,2`
- passing rows: `drift = 0.2` seed `2`
- passing rows: `drift = 0.3` seeds `1,2`
- passing rows: `drift = 0.5` seed `1`
- nearby failures: `drift = 0.05` seeds `0,1,2`
- nearby failures: `drift = 0.1` seeds `0,1,2`
- nearby failures: `drift = 0.2` seeds `0,1`
- nearby failures: `drift = 0.3` seed `0`
- nearby failures: `drift = 0.5` seeds `0,2`

Boundary read:
- the family is seed-selective rather than family-wide
- this is a diagnosed boundary pocket, not a promoted theorem
- the structural miss is local selectivity of the diagonal-stripe routing, not
  control leakage

So the honest interpretation is:
- seed-selective boundary, yes
- broad seventh-family closure, no
