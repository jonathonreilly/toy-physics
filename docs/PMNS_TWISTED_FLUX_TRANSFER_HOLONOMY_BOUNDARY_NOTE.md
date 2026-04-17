# PMNS Twisted Flux Transfer Holonomy Boundary

**Status:** theorem-grade boundary with a positive fluxed-holonomy sublaw  
**Script:** `scripts/frontier_pmns_twisted_flux_transfer_holonomy_boundary.py`

## Question

Can a twisted transfer, flux insertion, or cycle-holonomy law on the
graph-first oriented-cycle frame select the remaining values of the retained
PMNS cycle channel?

## Answer

Partially.

On the canonical graph-first cycle frame `E12, E23, E31`, the flux-threaded
transfer kernel

```text
T(xbar, ybar, phi) = xbar I + ybar (e^{i phi} C + e^{-i phi} C^2)
```

has an exact holonomy/spectral value law:

```text
tr(T)/3 = xbar
tr(C^2 T)/3 = ybar e^{i phi}
```

so `xbar`, `ybar`, and `phi` are recovered exactly from the twisted transfer
data. This is a genuine axiom-native value law for the fluxed transfer carrier.

But the current exact bank still does not select the full reduced PMNS oriented
cycle family

```text
A_fwd(u, v, w) = (u + i v) E12 + w E23 + (u - i v) E31
```

with one flux holonomy alone. The one-angle holonomy probe has a 2-real kernel
on that reduced carrier, so it does not collapse the full reduced family to a
unique point.

## What This Buys

- The graph-first frame remains canonical.
- The flux-threaded transfer carrier now has an exact nontrivial value law.
- The retained PMNS reduced carrier is still not fully value-selected by a
  single holonomy probe.

## What Remains

Any further positive selection law would have to use genuinely new dynamics or
a further admitted extension beyond the current exact bank.

## Verification

```bash
python3 scripts/frontier_pmns_twisted_flux_transfer_holonomy_boundary.py
```

