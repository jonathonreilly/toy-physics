# PR230 Same-Surface Neutral Multiplicity-One Gate

**Status:** exact support / same-surface neutral multiplicity-one artifact
intake gate; current PR230 surface rejected

## Purpose

This note records the clean source-Higgs route contract after the invariant-ring
attempt exposed the current blocker.  Representation theory, commutants,
primitive cones, Schur kernels, and related math tools are allowed only if they
produce a same-surface artifact that fixes the canonical neutral scalar
generator and its normalization.

The paired runner does not certify `O_H` and does not claim top-Yukawa closure.
It defines the exact positive artifact shape that would let the branch try the
clean source-Higgs closure path next.

## Required Positive Artifact

A future candidate must provide all of the following on the PR230 same surface:

- explicit `Cl(3)/Z3` neutral scalar representation/action data;
- a top-coupled neutral scalar sector;
- a multiplicity-one proof, or a primitive/irreducible transfer proof selecting
  one canonical radial generator;
- canonical metric/LSZ normalization, including the limiting order;
- a source-to-canonical-Higgs identity or a measured `C_spH/C_HH` pole-overlap
  row;
- accepted downstream certificate paths for `O_H` and source-Higgs pole rows;
- an explicit firewall excluding `H_unit`, `yt_ward_identity`, observed
  targets, `alpha_LM`/plaquette/`u0`, pilot evidence, unit `c2`, unit
  `Z_match`, unit `kappa_s`, and value-recognition selectors.

## Current Surface Result

The current PR230 surface fails this intake gate.  It admits a two-singlet
neutral completion with basis

```text
source_singlet, orthogonal_neutral_singlet
```

and trivial current action on both singlets.  The source-only observables remain
fixed while a candidate canonical-Higgs vector rotates through the orthogonal
neutral slot.  Therefore the source-to-candidate overlap varies, but the
current source-only data do not distinguish the candidate.

That is exactly the scalar-source reparametrization/orthogonal-neutral blocker
in executable form.

## Non-Claim

This is not a retained or `proposed_retained` result.  It does not write a
canonical `O_H` certificate, does not set `kappa_s = 1`, does not promote Z3
positive-cone support into a physical transfer, and does not treat source-only
rows as source-Higgs overlap evidence.

## Verification

```bash
python3 scripts/frontier_yt_pr230_same_surface_neutral_multiplicity_one_gate.py
# SUMMARY: PASS=17 FAIL=0

python3 scripts/frontier_yt_pr230_clean_source_higgs_math_tool_route_selector.py
# SUMMARY: PASS=20 FAIL=0
```

## Exact Next Action

Produce the actual candidate file

```text
outputs/yt_pr230_same_surface_neutral_multiplicity_one_certificate_2026-05-07.json
```

with a same-surface representation/action and a multiplicity-one or
primitive-generator proof.  If that candidate passes this gate, rerun the
canonical `O_H` certificate gate, source-Higgs row builder, Gram-purity
postprocessor, scalar-LSZ gates, full assembly gate, retained-route gate, and
completion audit.
