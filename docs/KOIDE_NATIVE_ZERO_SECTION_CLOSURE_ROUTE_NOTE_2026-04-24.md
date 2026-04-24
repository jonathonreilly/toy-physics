# Koide native zero-section closure route

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_native_zero_section_closure_route.py`
**Status:** exact conditional native route; not yet retained-only closure

## Purpose

Figure out how the Koide lane could close natively after the residual
cohomology obstruction reduced the gap to one zero-section theorem:

```text
z = 0
spectator = 0
c = 0.
```

## Route

The viable native route is not another rank-one selected-line theorem.  It is:

```text
Q:
  native zero-source charged-lepton scalar readout
  -> z = 0
  -> K_TL = 0
  -> Q = 2/3.

delta:
  Brannen endpoint is the whole real nontrivial Z3 primitive
  -> no equivariant spectator projector
  -> spectator = 0.

  unit-preserving determinant-line endpoint readout
  -> c = 0.

  APS fixed-point computation
  -> eta_APS = 2/9
  -> delta_open = 2/9.
```

## Real `Z3` Primitive Theorem

On the retained real nontrivial `Z3` character pair, the generator is a
rotation by `2pi/3`.  Its real equivariant endomorphisms are:

```text
a I + b J,  J^2 = -I.
```

Solving the equivariant idempotent equation gives only:

```text
0
I.
```

Therefore the real primitive has no retained `Z3`-equivariant selected/spectator
projector.  If the Brannen endpoint is this native real primitive, the
spectator channel is killed by representation theory:

```text
spectator = 0.
```

## Rank-One Boundary

A real rank-one line projector inside the real doublet does not commute with
the retained `Z3` rotation.  So a rank-one selected Brannen line is not native
to the retained real primitive; it is extra boundary data.

This is the important pivot:

```text
native closure must identify Brannen delta with the whole real Z3 primitive,
not with an arbitrary CP1 line inside the primitive.
```

## Unit Endpoint

For an open determinant-line endpoint coordinate:

```text
F(phi) = phi + c.
```

The unit condition:

```text
F(0) = 0
```

forces:

```text
c = 0.
```

An unbased torsor coordinate remains the exact falsifier.  For example:

```text
eta_APS = 2/9
c = 1/9
delta_open = 1/3.
```

## Conditional Closure

Under the native zero-section identifications:

```text
z = 0
spectator = 0
c = 0
```

the runner verifies:

```text
Q = 2/3
delta_open = eta_APS = 2/9.
```

## Review Boundary

This is not yet retained-only closure.  It identifies exactly what a retained
native closure must prove:

```text
1. the physical Brannen endpoint is the whole real nontrivial Z3 primitive,
   not a rank-one selected line inside its multiplicity space;

2. the physical open determinant-line endpoint readout is unit-preserving /
   based, not an unbased torsor coordinate;

3. the charged-lepton scalar readout is the zero-source source-response
   coefficient on the normalized second-order carrier.
```

The old retained no-gos remain valid against the rank-one selected-line route.
This route says the native closure has to change that interpretation: the
native object is the irreducible real primitive.

## Falsifiers

- A retained reason why Brannen delta must be a rank-one line rather than the
  real nontrivial `Z3` primitive.
- A retained spectator channel that is `Z3` equivariant on the real primitive.
- A physical endpoint readout that is genuinely unbased, so `c` is observable.
- A nonzero charged-lepton selector source that is native rather than a hidden
  value parameter.

## Verification

Run:

```bash
python3 scripts/frontier_koide_native_zero_section_closure_route.py
python3 scripts/frontier_koide_hostile_review_guard.py
python3 scripts/frontier_koide_lane_regression.py
```

Expected closeout:

```text
KOIDE_NATIVE_ZERO_SECTION_CLOSURE_ROUTE=CONDITIONAL
CONDITIONAL_NATIVE_ZERO_SECTION_IMPLIES_Q=TRUE
CONDITIONAL_NATIVE_ZERO_SECTION_IMPLIES_DELTA=TRUE
CONDITIONAL_NATIVE_ZERO_SECTION_IMPLIES_NATIVE_VALUES=TRUE
RETAINED_ONLY_NATIVE_CLOSURE_CLAIMED=FALSE
RESIDUAL_IDENTIFICATION_DELTA=Brannen_endpoint_is_real_Z3_primitive_not_rank_one_line
RESIDUAL_TRIVIALIZATION=unit_preserving_determinant_line_endpoint_readout
```
