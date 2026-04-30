# Distance Law Portability Across Retained Structured Families

**Status:** bounded - bounded or caveated result note
This sweep asked a narrow question:

Can the retained near-Newtonian distance tail transfer beyond the first two grown families into the newer retained structured families?

The answer is **partial only**. The law does not port uniformly across the tested retained rows.

## Sweep

Representative retained rows:

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
| alt-connectivity | `-0.952` | `0/5 TOWARD` | magnitude close to the retained grown-family value, but direction flips |
| third-family | `-2.161` | `0/5 TOWARD` | steepens strongly and loses the retained sign orientation |
| fourth-family | `-1.190` | `0/5 TOWARD` | direction cancels under the quadrant-reflection geometry |
| fifth-family radial | `-0.313` | `5/5 TOWARD` | preserves direction, but the tail flattens far below the retained exponent |

Safe read across the tested rows:

- mean alpha: `-1.154`
- alpha span: `1.847`
- boundary families with AWAY rows: `alt-connectivity`, `third-family`, `fourth-family`
- only `fifth-family radial` stays TOWARD on all sampled rows

## Diagnosis

The distance law is **not** geometry-independent across these retained structured families.

The failure modes look architecture-specific:

- `alt-connectivity` retains a near-grown-family exponent magnitude, but the parity-tapered shell routing plus the fallback dense edges rotate the response away from the retained direction.
- `third-family` is too far from the grown-family transport regime; the deeper branch structure steepens the tail and destroys the retained directional response.
- `fourth-family` enforces a quadrant-reflection symmetry that cancels the long-tail bias.
- `fifth-family radial` is the closest directional match, but the radial-shell confinement over-locks transport and flattens the exponent.

## Conclusion

The retained distance law transfers cleanly across the first two grown families, but not across the newer retained structured families as a group.

What survives here is only a **partial portability story**:

- some families preserve the directional bias
- some families preserve the exponent approximately
- no tested newer family preserves both at the same time

So this sweep is a diagnosed boundary, not a new portability win.
