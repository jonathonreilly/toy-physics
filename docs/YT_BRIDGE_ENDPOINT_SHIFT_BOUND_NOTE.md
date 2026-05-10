# `y_t` Bridge Endpoint Shift Bound Note

**Date:** 2026-04-15
**Status:** bounded support note
**Primary runner:** `scripts/frontier_yt_bridge_endpoint_shift_bound.py`

## Role

This note turns the current bridge-control stack into a single intrinsic
endpoint-shift bound.

The earlier branch results already established, in order:

- a positive local quadratic selector on the forced UV window
- a higher-order correction audit on the viable UV-localized family
- a nonlocal correction audit on the same forced UV window

The remaining question is narrower:

> how far can the exact interacting bridge move the endpoint away from the
> local selector once those correction tails are taken into account?

## Hypotheses

This bound is conditional on the current package hypotheses:

1. the forced UV window is `x >= 0.95`
2. the exact interacting bridge is quasi-local and stable on that window
3. the endpoint shift decomposes into a local-Hessian piece plus higher-order
   local tails plus a nonlocal tail
4. the audited correction ratios are valid upper bounds for the corresponding
   residual pieces on the exact bridge
5. the residual pieces enter additively on the fixed-endpoint slice, so the
   triangle inequality applies

These are the same assumptions already used implicitly by the branch control
stack. The note makes them explicit.

## Inputs from the branch stack

Local selector on the viable bridge family:

- `y_loc = 0.917605`

Higher-order local correction ratio:

- `r_ho = 7.123842e-3`

Nonlocal correction ratio, conservative operator-norm form:

- `r_nl = 5.023669e-3`

Nonlocal correction ratio, measured family-average support form:

- `r_nl,avg = 4.262215e-4`

Current branch target:

- `y_t(v) = 0.9176`

## Endpoint-shift bound

By the additive residual hypothesis and triangle inequality, the exact bridge
endpoint shift relative to the local selector obeys

`|y_exact - y_loc| / y_loc <= r_ho + r_nl`

so the conservative paper-safe relative bound is

`X_cons = 7.123842e-3 + 5.023669e-3 = 1.2147511e-2`

That is a `1.2147511%` relative shift budget.

In absolute terms, with `y_loc = 0.917605`,

`|y_exact - y_loc| <= 1.114661683e-2`

so the conservative endpoint interval is

`y_exact in [0.906458383, 0.928751617]`

The measured family-average nonlocal support gives a tighter empirical support
budget:

`X_tight = 7.123842e-3 + 4.262215e-4 = 7.5500635e-3`

or `0.75500635%` relative shift, corresponding to

`|y_exact - y_loc| <= 6.927976018e-3`

and the tighter interval

`y_exact in [0.910677024, 0.924532976]`

The branch target differs from the local selector by only

`|0.9176 - 0.917605| = 5e-6`

which is `5.44897e-6` relative to the local selector, far inside either bound.

## Meaning

The result is a theorem-style bounded-support statement, not an unboundedness
proof:

- the selector is no longer the mystery
- the higher-order tail is small
- the nonlocal tail is small
- the exact bridge endpoint is confined to a narrow band around the local
  selector

So the branch now has an intrinsic endpoint-shift bound for the exact bridge,
but not yet a proof that the `y_t` lane is fully unbounded.

## Paper-safe claim

> Under the current forced UV window and quasi-local stability hypotheses, the
> exact interacting bridge can shift the endpoint by at most
> `1.2147511%` relative to the local selector, with a support-tight
> empirical bound of `0.75500635%` on the viable family average. At the
> current local selector `y_loc = 0.917605`, this corresponds to an absolute
> conservative shift budget of `1.114661683e-2` and a support-tight budget of
> `6.927976018e-3`. The branch target `y_t(v)=0.9176` sits comfortably inside
> both intervals.

## Honest boundary

This note does **not** remove the residual backward-Ward / QFP systematic.
It only bounds the bridge-specific endpoint shift above the local selector.

The exact bridge may still reduce to a smaller bounded systematic, or it may
ultimately close if a package-native transport theorem lands later. This note
does not claim that final step.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with the
substantive observation that the load-bearing inequality is a valid
triangle-inequality closure only after importing the additive-residual,
quasi-local-stability, and ratio-validity hypotheses, and that the cited
authorities include `audited_conditional` and `audited_numerical_match`
notes, so retained status cannot propagate to this bound. The
hypotheses are listed explicitly above; this addendum makes the auditor
read explicit so the audit lane can treat the citations correctly.

This addendum is graph-bookkeeping only. It does not change the
conditional status, does not promote the row, and does not modify the
budget arithmetic.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [yt_bridge_hessian_selector_note](YT_BRIDGE_HESSIAN_SELECTOR_NOTE.md)
- [yt_bridge_higher_order_corrections_note](YT_BRIDGE_HIGHER_ORDER_CORRECTIONS_NOTE.md)
- [yt_bridge_nonlocal_corrections_note](YT_BRIDGE_NONLOCAL_CORRECTIONS_NOTE.md)
- [yt_constructive_uv_bridge_note](YT_CONSTRUCTIVE_UV_BRIDGE_NOTE.md)
