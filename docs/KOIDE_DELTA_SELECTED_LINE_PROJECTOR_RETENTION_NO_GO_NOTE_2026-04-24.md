# Koide Delta Selected-Line Projector-Retention No-Go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_selected_line_projector_retention_no_go.py`  
**Status:** conditional support theorem; executable no-go for retained closure

## Theorem Attempt

Try to derive the selected endpoint identity from the retained selected-line
`CP1` ray:

```text
chi(theta) = (1, exp(-2i theta)) / sqrt(2).
```

This ray defines a canonical projector:

```text
P_chi = |chi><chi|.
```

If the physical open boundary source is forced to have support projector
`P_chi`, then the spectator channel is zero.  If the endpoint torsor is also
based, then:

```text
delta_open = eta_APS = 2/9.
```

## Brainstormed Variants

1. Selected-line existence alone.
2. Selected-line projector support as a physical source law.
3. Convex mixtures of selected and spectator projectors.
4. What if projector support is retained but endpoint exact offsets remain?
5. What if endpoint basing is retained but projector support is not?

## Exact Audit

The runner verifies:

```text
P_chi^2 = P_chi
tr(P_chi) = 1
det(P_chi) = 0
Q_chi = I - P_chi.
```

A generic retained positive boundary source on this split is:

```text
rho = p P_chi + (1-p) Q_chi.
```

Therefore:

```text
selected_channel = p
spectator_channel = 1-p
delta_open = p eta_APS + c.
```

Closure requires:

```text
p = 1
c = 0.
```

## Hostile Review

The route does not fail because the selected projector is absent.  It fails
because the projector's existence is weaker than the physical boundary-source
support theorem:

```text
derive_selected_line_projector_as_physical_boundary_source_support.
```

Even if `p=1` is supplied, the endpoint exact offset remains unless:

```text
derive_selected_endpoint_exact_counterterm_zero.
```

## Verdict

```text
KOIDE_DELTA_SELECTED_LINE_PROJECTOR_RETENTION_NO_GO=TRUE
DELTA_SELECTED_LINE_PROJECTOR_RETENTION_CLOSES_DELTA_RETAINED_ONLY=FALSE
CONDITIONAL_DELTA_CLOSES_IF_PROJECTOR_RETENTION_AND_BASEPOINT_ARE_PHYSICAL=TRUE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_CHANNEL=derive_selected_line_projector_as_physical_boundary_source_support
RESIDUAL_TRIVIALIZATION=derive_selected_endpoint_exact_counterterm_zero
RESIDUAL_SCALAR=minus_spectator_channel_plus_c_over_eta_APS
COUNTERSTATE=unpolarized_projector_mixture_or_selected_projector_with_endpoint_shift
```

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_selected_line_projector_retention_no_go.py
python3 -m py_compile scripts/frontier_koide_delta_selected_line_projector_retention_no_go.py
```
