# Koide Q Witten/global-anomaly source no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_witten_global_anomaly_source_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use the strongest available global gauge-anomaly constraint to derive the
remaining source law:

```text
SU(2) mod-2 / Witten anomaly cancellation
  -> equal C3 center source
  -> K_TL = 0.
```

## Executable theorem

The SU(2) global anomaly is a parity law:

```text
(-1)^N_doublet = +1.
```

For one Standard-Model charge generation:

```text
N_doublet = 3 quark-color doublets + 1 lepton doublet = 4
```

and for three generations:

```text
N_doublet = 12.
```

Both give anomaly sign `+1`.

## Obstruction

The anomaly condition is a parity condition on electroweak doublet count.  It
does not contain the normalized C3 center-source variable:

```text
p(P_plus) = u
p(P_perp) = 1-u.
```

The runner verifies that closing and non-closing center states all have the
same anomaly sign:

```text
u = 1/3 -> Q = 1,   K_TL = 3/8
u = 1/2 -> Q = 2/3, K_TL = 0
u = 2/3 -> Q = 1/2, K_TL = -3/8.
```

## Pin/mod-2 refinement

A Pin or mod-2 index refinement still returns a parity class.  Mapping that
class to the equal center-label source requires an additional affine source
map:

```text
u = a * (N mod 2) + b
```

For the anomaly-free class this route needs:

```text
b = 1/2.
```

That is the missing source primitive in another notation.

## Residual

```text
RESIDUAL_SCALAR = center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_MAP = global_anomaly_parity_to_C3_center_source_not_retained
```

## Why this is not closure

Global anomaly cancellation is real physics, but it acts on electroweak doublet
parity.  The charged-lepton Koide residual is a normalized C3 center-source
state.  No retained theorem maps the former to the latter.

## Falsifiers

- A retained anomaly inflow theorem whose boundary source is exactly the C3
  center-label state.
- A mod-2 index pairing with the charged-lepton source carrier whose vanishing
  is equivalent to `u=1/2`.
- A physical derivation of the parity-to-center-source map that does not set
  the target value by hand.

## Boundaries

- Covers SU(2) mod-2/Witten anomaly parity and parity-valued refinements.
- Does not refute a future mixed anomaly that directly couples to the retained
  C3 source scalar.

## Hostile reviewer objections answered

- **"This is a physical anomaly."**  Yes, but it is blind to the residual
  center-state scalar.
- **"The lepton doublet count appears."**  It appears only inside an evenness
  law once quark colors are included.
- **"Use the anomaly-free parity to choose `u=1/2`."**  That requires the
  non-retained parity-to-source map.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_witten_global_anomaly_source_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_WITTEN_GLOBAL_ANOMALY_SOURCE_NO_GO=TRUE
Q_WITTEN_GLOBAL_ANOMALY_SOURCE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=center_label_source_u_minus_one_half_equiv_K_TL
RESIDUAL_MAP=global_anomaly_parity_to_C3_center_source_not_retained
```
