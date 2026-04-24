# Koide native dimensionless review packet

**Date:** 2026-04-24
**Status:** retained support / no-go packet.  This packet does **not** close the
dimensionless charged-lepton Koide lane.

## Decision

The reviewed branch contains useful science, but the full "native closure"
claim is not retained on `main`.

What lands here is narrower:

```text
Q:
  strict zero-source source-response readout
  -> K_TL = 0
  -> Q = 2/3
  remains a physical-readout identification theorem unless separately derived.

delta:
  whole real nontrivial Z3 primitive + unit-preserving endpoint readout
  -> spectator = 0 and c = 0
  -> delta = eta_APS = 2/9
  remains conditional until the Brannen endpoint is derived as that primitive
  and the endpoint readout is derived as based/unit-preserving.
```

So the strongest retained statement is:

```text
KOIDE_DIMENSIONLESS_NATIVE_CLOSURE=FALSE
KOIDE_NATIVE_ZERO_SECTION_ROUTE=CONDITIONAL
NEXT_NATIVE_THEOREM=
  derive_Brannen_endpoint_as_real_Z3_primitive_and_unit_determinant_readout
```

## Landed science

1. **Residual cohomology obstruction.**  Exactness identifies the Q and delta
   kernels but does not choose their zero section.  The missing statement is a
   retained canonical-section / primitive-readout theorem.

2. **Readout-retention split.**  The Q side is reduced to the strict
   zero-source source-response readout question.  The delta side still needs a
   closed-APS to open-endpoint functor.

3. **Marked relative-cobordism no-go.**  A boundary mark derived from retained
   Wilson/APS data is scalar on the multiplicity space, so it does not select a
   rank-one Brannen line or endpoint basepoint.

4. **Finite Wilson selected-eigenline no-go.**  The finite Wilson realization
   does not itself reproduce the exact APS value in this audit, and in any case
   its zero-mode character sector remains rank two.  It therefore does not
   select the physical Brannen line.

5. **Conditional native zero-section route.**  If the physical Brannen endpoint
   is the whole real nontrivial `Z3` primitive and the open determinant endpoint
   is unit-preserving, representation theory kills the spectator channel and
   the endpoint offset.  This is the clearest next theorem target, not current
   closure.

## Explicitly not landed

The branch's stronger `KOIDE_NATIVE_BRANNEN_REAL_PRIMITIVE_CLOSURE_THEOREM`
claim is not landed as retained closure.  Its decisive steps identify:

```text
physical Brannen endpoint = whole real nontrivial Z3 primitive
open endpoint readout = based/unit-preserving determinant functor
physical charged-lepton scalar selector = zero-source readout
```

Those identifications are exactly the remaining scientific work unless a later
retained theorem derives them from the accepted charged-lepton construction.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_delta_residual_cohomology_obstruction_no_go.py
python3 scripts/frontier_koide_q_delta_readout_retention_split_no_go.py
python3 scripts/frontier_koide_delta_marked_relative_cobordism_no_go.py
python3 scripts/frontier_koide_delta_lattice_wilson_selected_eigenline_no_go.py
python3 scripts/frontier_koide_native_zero_section_closure_route.py
python3 scripts/frontier_koide_native_zero_section_nature_review.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected boundary:

```text
KOIDE_NATIVE_ZERO_SECTION_RETAINED_CLOSURE=FALSE
NATIVE_ROUTE_IMPLIES_VALUES_CONDITIONALLY=TRUE
KOIDE_Q_DELTA_RESIDUAL_COHOMOLOGY_CLOSES_FULL_LANE=FALSE
Q_DELTA_READOUT_RETENTION_SPLIT_CLOSES_FULL_LANE=FALSE
DELTA_MARKED_RELATIVE_COBORDISM_CLOSES_DELTA=FALSE
DELTA_LATTICE_WILSON_SELECTED_EIGENLINE_CLOSES_DELTA=FALSE
```
