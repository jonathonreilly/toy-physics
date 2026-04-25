# Koide delta normal endpoint-source exclusion theorem

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_normal_endpoint_source_exclusion_theorem.py`  
**Status:** defense theorem excluding `j_norm` from selected-line local readout

## Purpose

Attack the remaining reviewer escape hatch:

```text
retain a physical normal endpoint source j_norm != 0.
```

## Theorem

For the retained selected-line endpoint inclusion:

```text
i_chi: L_chi -> V,
```

the selected-line local source readout is the pullback:

```text
A -> i_chi^* A i_chi.
```

For the selected projector `P_chi` and normal projector `Q_chi`:

```text
i_chi^* P_chi i_chi = 1
i_chi^* Q_chi i_chi = 0.
```

Therefore a normal source:

```text
j_norm Q_chi
```

is in the pullback kernel.

## Consequence

An ambient source

```text
rho = a P_chi + b Q_chi
```

has selected-line pullback:

```text
i_chi^* rho i_chi = a.
```

Line-local normalization fixes:

```text
a = 1.
```

The coefficient `b` is invisible to selected-line local readout.  Every
line-normalized source class is represented by:

```text
P_chi.
```

Thus:

```text
selected = 1
spectator = 0.
```

## Why Ambient Mixed States Are Extra Readout

To make `b` affect delta, one must use ambient trace normalization:

```text
Tr_V rho = a + b = 1.
```

Then:

```text
selected_ambient = 1 - b
normal_ambient = b.
```

That is an ambient normal endpoint observable.  It is not supplied by the
selected-line local endpoint pullback.  Retaining it is a new endpoint readout,
not a consequence of selected-line locality.

## Sharpened Falsifier

Retaining `j_norm != 0` alone does not falsify the closure; it is pullback
kernel data.

The stronger falsifier is:

```text
retained normal endpoint observable or ambient trace-normalization coupled to delta.
```

## Verification

```bash
python3 scripts/frontier_koide_delta_normal_endpoint_source_exclusion_theorem.py
python3 -m py_compile scripts/frontier_koide_delta_normal_endpoint_source_exclusion_theorem.py
```

Expected closeout:

```text
KOIDE_DELTA_NORMAL_ENDPOINT_SOURCE_EXCLUSION_THEOREM=TRUE
J_NORM_IS_PULLBACK_KERNEL_FOR_SELECTED_LINE_LOCAL_READOUT=TRUE
J_NORM_ALONE_DOES_NOT_FALSIFY_DELTA_CLOSURE=TRUE
AMBIENT_NORMALIZATION_IS_EXTRA_ENDPOINT_READOUT=TRUE
DELTA_LOCAL_READOUT_INDEPENDENT_OF_J_NORM=TRUE
NO_TARGET_IMPORT=TRUE
FALSIFIER=retained_normal_endpoint_observable_or_ambient_trace_normalization_coupled_to_delta
```
