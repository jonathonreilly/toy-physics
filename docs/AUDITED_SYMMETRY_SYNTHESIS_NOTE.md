# Audited Symmetry Synthesis Note

**Date:** 2026-04-03  
**Status:** synthesis-ready on the validated subset only

This note consolidates the symmetry-program results after a direct audit of the
current code and saved artifacts. The goal is to separate the claims that are
solid enough to synthesize now from the ones that are still one step short.

## Primary Artifacts

- exact mirror / bounded coexistence:
  [`docs/MIRROR_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_CHOKEPOINT_NOTE.md)
- higher-symmetry joint validation:
  [`docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/HIGHER_SYMMETRY_JOINT_VALIDATION_NOTE.md)
- higher-symmetry gravity follow-up:
  [`docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/HIGHER_SYMMETRY_GRAVITY_PROBE_NOTE.md)
- exact 2D mirror validation:
  [`docs/MIRROR_2D_VALIDATION_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_2D_VALIDATION_NOTE.md)
  [`scripts/mirror_2d_validation.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_2d_validation.py)
  [`logs/2026-04-03-mirror-2d-validation.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-2d-validation.txt)
- structured-growth reproduction:
  [`logs/2026-04-03-structured-mirror-growth.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-structured-mirror-growth.txt)
- structured-growth Born audit:
  [`scripts/structured_mirror_born_audit.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_born_audit.py)
  [`logs/2026-04-03-structured-mirror-born-audit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-structured-mirror-born-audit.txt)

## What Is Solid Now

### 1. Exact symmetry really matters

The exact-mirror program survives audit. The current safe statement is still:

- random growth tends toward the CLT / rank-1 ceiling
- exact discrete symmetry can delay or prevent that convergence in bounded
  windows
- approximate or heuristic symmetry is not enough to inherit the same benefit

The exact mirror chokepoint lane remains the canonical parity-protected result:

- Born-clean at machine precision
- positive gravity
- decohering through the retained bounded window

That result is frozen in
[`docs/MIRROR_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_CHOKEPOINT_NOTE.md).

### 2. `Z2 x Z2` is a real bounded coexistence lane

The higher-symmetry joint validator survives audit and remains the strongest
new symmetry result that is clean on all three axes:

- Born-clean at machine precision
- `k=0` exactly zero
- positive band-averaged gravity
- much slower decoherence decay than random

Bounded validated rows:

| N | `pur_cl` | gravity-band | Born |
|---|---:|---:|---:|
| 25 | `0.660±0.025` | `+0.690±0.323` | `9.02e-16` |
| 40 | `0.667±0.023` | `+0.916±0.403` | `1.24e-15` |
| 60 | `0.685±0.028` | `+1.493±0.454` | `9.86e-16` |
| 80 | `0.783±0.019` | `+1.736±0.337` | `1.48e-15` |

Its bounded decoherence fit is:

- `1 - pur_cl ~= C * N^alpha`
- `alpha = -0.335`
- bootstrap `95% CI [-0.509, -0.139]`

So `Z2 x Z2` is synthesis-grade as a bounded symmetry-protected coexistence
lane.

### 3. The higher-symmetry gravity law is still not clean

The gravity-side follow-up on dense `Z2 x Z2` remains useful but negative for
the stronger claim:

- mass windows are positive but weak / non-monotone
- distance sweeps show broad bumps rather than one retained law

So the safe summary is:

- `Z2 x Z2` is a real coexistence lane
- it is not yet a clean gravity-law lane

## What Does **Not** Survive Audit Yet

### 1. Structured mirror growth is not currently Born-safe

The geometry result is real: the current structured-growth script reproduces a
strong grown-graph pocket with substantial decoherence and strong positive
gravity. For example, the reproduced current rows are:

| config | N | `pur_min` | gravity |
|---|---:|---:|---:|
| `npl_half=15, d=2` | 25 | `0.7700` | `+1.454` |
| `npl_half=20, d=2` | 25 | `0.8123` | `+2.654` |
| `npl_half=30, d=2` | 30 | `0.8869` | `+3.966` |

But the current propagator in
[`scripts/structured_mirror_growth.py`](/Users/jonreilly/Projects/Physics/scripts/structured_mirror_growth.py)
uses explicit per-layer normalization, so Born cannot be assumed. The direct
audit in
[`logs/2026-04-03-structured-mirror-born-audit.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-structured-mirror-born-audit.txt)
finds:

- min `|I3|/P = 1.000000`
- median `|I3|/P = 1.000000`
- max `|I3|/P = 1.000000`

across all tested 3-slit combinations on the representative `N=25`,
`npl_half=15`, `d=2` lane.

So the current safe interpretation is:

- **geometry win:** yes
- **Born-clean grown successor:** no, not with the current layer-norm propagator

### 3. Exact mirror MI is now artifact-backed, but bounded

The mirror-specific MI chain is now frozen in:

- [`scripts/mirror_mutual_information_chokepoint.py`](/Users/jonreilly/Projects/Physics/scripts/mirror_mutual_information_chokepoint.py)
- [`logs/2026-04-03-mirror-mutual-information-chokepoint-n60-r5p0.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-03-mirror-mutual-information-chokepoint-n60-r5p0.txt)
- [`docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md`](/Users/jonreilly/Projects/Physics/docs/MIRROR_MUTUAL_INFORMATION_CHOKEPOINT_NOTE.md)

On the retained dense exact mirror chokepoint family, mirror keeps a clear
mid-N MI advantage over the matched random baseline, but the comparison is not
monotone and does not support a clean slower-decay theorem:

- `N=40`: mirror MI `0.4295±0.068` bits vs random `0.1774±0.034`
- `N=60`: mirror MI `0.1973±0.041` bits vs random `0.0846±0.032`
- `N=80`: mirror MI `0.1385±0.021` bits vs random `0.0564±0.018`
- `N=100`: mirror MI `0.0408±0.011` bits vs random `0.0574±0.021`

The CL-bath purity stays in the same bounded pocket, but the MI and purity
orderings are not identical. The important synthesis point is:

- the exact mirror chokepoint family has a real, review-safe, bounded MI
  advantage
- the exponent fit is too noisy to claim a global asymptotic theorem

The canonical 3D mirror MI artifact remains useful too:

- `S4` mirror:
  - `N=25`: `0.7213±0.073` bits
  - `N=40`: `0.5956±0.067` bits
  - `N=60`: `0.5248±0.067` bits
  - `N=80`: `0.2559±0.047` bits

So the earlier “not artifact-backed” concern is resolved for both the
canonical 3D mirror MI chain and the new exact 2D mirror validation chain.
The exact 2D lane should be treated as the more review-safe family-level
confirmation, while the canonical `S4` lane remains the scalable MI lane.

### 3. The `Z2`-breaking fragility curve is not retained as a repo artifact

The branch history contains a strong prose claim that controlled mirror-edge
dropout rapidly destroys the symmetry benefit. That claim is plausible and
scientifically interesting, but I did **not** find a retained script/log pair
for it in the current repo snapshot.

So the fragility story should be treated as:

- **interesting working claim:** yes
- **synthesis-grade retained artifact:** not yet

## Synthesis-Grade Story

The strongest audited story we can tell now is:

1. random growth fails by a rank-1 / CLT-type mechanism
2. exact discrete symmetry can preserve distinct sectors and delay that failure
3. exact mirror symmetry gives a retained bounded coexistence pocket
4. exact 2D mirror gives a review-safe bounded coexistence pocket with strong
   MI and dTV separation on the same family
5. `Z2 x Z2` strengthens the decoherence side and remains Born-clean and
   gravity-positive in a bounded window
6. structured mirror growth shows that the geometry idea is not purely an
   imposed toy, but its **current** propagation rule is not Born-safe

So the program is not yet “fully mature” in the strongest sense. The accurate
statement is:

- **mature bounded symmetry program:** yes
- **fully unified axiom-compliant grown Born+gravity+decoherence lane:** not yet

## Best Next Wins

The highest-value next steps are now sharply defined:

1. Replace or linearize the structured-growth propagator so the grown symmetry
   lane can be Born-audited cleanly.
2. Retain the `Z2`-breaking fragility curve with an actual script/log pair.
3. Keep `Z2 x Z2` as the strongest bounded coexistence lane while the grown
   lane is repaired.
4. Use exact 2D mirror as the family-level confirmation while the grown lane
   is repaired.

## Bottom Line

Proceed on solid ground by making exact 2D mirror, `Z2 x Z2`, and exact
mirror the synthesis headline, and treating structured mirror growth as a
promising geometry result that still needs a Born-safe propagator before it
can become the canonical successor lane.
