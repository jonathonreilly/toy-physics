# Distance Law Portability Across Structured Families

**Status:** bounded — bounded sweep result.
**Last sync:** 2026-05-10 — registered the primary runner explicitly,
declared the direct generator imports, and pinned the table
values with assertions inside the runner. No table values change.
**Primary runner:** [`scripts/DISTANCE_LAW_PORTABILITY_COMPARE.py`](../scripts/DISTANCE_LAW_PORTABILITY_COMPARE.py)
**Generator imports (explicit; audit status is ledger-owned):**
- [`GATE_B_NO_RESTORE_FARFIELD_NOTE.md`](GATE_B_NO_RESTORE_FARFIELD_NOTE.md)
  / `scripts/gate_b_no_restore_farfield.py` — `grow` baseline geometry
- [`ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md`](ALT_CONNECTIVITY_FAMILY_SIGN_NOTE.md)
  / `scripts/ALT_CONNECTIVITY_FAMILY_SIGN_SWEEP.py` — `_build_alt_connectivity`
- [`THIRD_GROWN_FAMILY_SIGN_NOTE.md`](THIRD_GROWN_FAMILY_SIGN_NOTE.md)
  / `scripts/THIRD_GROWN_FAMILY_SIGN_SWEEP.py` — `_build_third_connectivity`
- [`FOURTH_FAMILY_QUADRANT_NOTE.md`](FOURTH_FAMILY_QUADRANT_NOTE.md)
  / `scripts/FOURTH_FAMILY_QUADRANT_SWEEP.py` — `_build_quadrant_reflection_connectivity`

The radial-shell builder (`_build_radial_shell_connectivity`) used for
the `fifth-family radial` row is defined inline in
`scripts/DISTANCE_LAW_PORTABILITY_COMPARE.py` itself; it has no separate
upstream module.

This sweep asked a narrow question:

Can the near-Newtonian distance-tail behavior transfer beyond the first two grown families into the newer structured families?

The answer is **partial only**. The law does not port uniformly across the tested structured-family rows.

## Sweep

Representative rows:

- `alt-connectivity`: `(drift=0.20, seed=0)`
- `third-family`: `(drift=0.20, seed=2)`
- `fourth-family`: `(drift=0.00, seed=0)`
- `fifth-family radial`: `(drift=0.05, seed=0)`

Test setup:

- same gravity-style source-centroid observable as the grown-geometry distance-law replay
- sampled impact parameters `b = [5, 6, 7, 8, 10]`
- field strength `0.004`
- `k = 5.0`
- `beta = 0.8`

## Results

| Family | alpha | Direction | Notes |
| --- | ---: | --- | --- |
| alt-connectivity | `-0.952` | `0/5 TOWARD` | magnitude close to the grown-family value, but direction flips |
| third-family | `-2.161` | `0/5 TOWARD` | steepens strongly and loses the grown-family sign orientation |
| fourth-family | `-1.190` | `0/5 TOWARD` | direction cancels under the quadrant-reflection geometry |
| fifth-family radial | `-0.313` | `5/5 TOWARD` | preserves direction, but the tail flattens far below the grown-family exponent |

Safe read across the tested rows:

- mean alpha: `-1.154`
- alpha span: `1.847`
- boundary families with AWAY rows: `alt-connectivity`, `third-family`, `fourth-family`
- only `fifth-family radial` stays TOWARD on all sampled rows

## Diagnosis

The distance law is **not** geometry-independent across these structured families.

The failure modes look architecture-specific:

- `alt-connectivity` keeps a near-grown-family exponent magnitude, but the parity-tapered shell routing plus the fallback dense edges rotate the response away from the grown-family direction.
- `third-family` is too far from the grown-family transport regime; the deeper branch structure steepens the tail and destroys the grown-family directional response.
- `fourth-family` enforces a quadrant-reflection symmetry that cancels the long-tail bias.
- `fifth-family radial` is the closest directional match, but the radial-shell confinement over-locks transport and flattens the exponent.

## Conclusion

The grown-family distance law transfers cleanly across the first two grown families, but not across the newer structured families as a group.

What survives here is only a **partial portability story**:

- some families preserve the directional bias
- some families preserve the exponent approximately
- no tested newer family preserves both at the same time

So this sweep is a diagnosed boundary, not a new portability win.
