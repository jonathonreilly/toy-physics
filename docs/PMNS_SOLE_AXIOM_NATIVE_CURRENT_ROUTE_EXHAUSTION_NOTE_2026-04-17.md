# PMNS Sole-Axiom Native Current Route Exhaustion

**Date:** 2026-04-17  
**Status:** exact route-exhaustion theorem on the PMNS-native sole-axiom current lane  
**Script:** `scripts/frontier_pmns_sole_axiom_native_current_route_exhaustion_2026_04_17.py`

## Question

Inside the **current PMNS-native sole-axiom bank**, is there any overlooked exact
route from `Cl(3)` on `Z^3` to a nonzero native current

`J_chi`?

## Answer

No.

The current PMNS-native bank is now exhausted exactly:

1. the sole-axiom free route, the canonical sole-axiom `hw=1`
   source/transfer route, and the retained scalar route all force
   `J_chi = 0`
2. the nearest native dynamical positives, namely the transfer-operator
   dominant-mode law and the direct corner-transport law, recover only aligned
   seed data / branch structure and are explicitly blind to the off-seed
   breaking carrier
3. the graph-first / `C3`-holonomy / reduced-channel stack closes the carrier
   and the native readout exactly, but does not furnish a value-selection law,
   since distinct reduced-channel points with distinct `J_chi` are both
   realized on the active response chain

Therefore there is **no overlooked exact PMNS-native route on the current
sole-axiom bank** that already derives nonzero `J_chi`.

## Exact chain

### 1. The explicit sole-axiom retained routes already annihilate `J_chi`

The current exact PMNS-native routes that stay entirely on the retained
sole-axiom bank are:

- the free route
- the canonical sole-axiom `hw=1` source/transfer route
- the retained scalar route

On all three, the native nontrivial `C3` current vanishes exactly:

`J_chi = 0`.

So the current PMNS-native blocker is not “we forgot the obvious retained
route.”

### 2. The nearest native dynamics stop upstream of `J_chi`

The strongest nearby positive native PMNS theorems do not close the current:

- the transfer-operator dominant-mode theorem reconstructs only the aligned
  seed pair `(xbar, ybar)` and explicitly does not determine the off-seed
  breaking source
- the direct corner-transport theorem reconstructs the seed pair and a branch
  bit, but is still blind to the same `5`-real breaking carrier

So those routes are genuine native dynamics, but not hidden current-generating
theorems.

### 3. The reduced current/readout stack is exact but point-blind

The graph-first and `C3`-character notes already close:

- the reduced PMNS carrier
- the native `C3` readout family
- the identification `J_chi = chi = u + i v` on the reduced family

But the reduced-channel nonselection theorem and the current-bank value no-go
show that two distinct reduced-channel points with different `J_chi` are both
realized exactly on the lower-level active response chain.

So the current PMNS-native bank already gives:

- exact carrier,
- exact readout,
- exact realizability,

but **not** a current-activation law.

## Consequence

This sharpens the old boundary.

Before:

- the strongest explicit negative statement was that the canonical
  sole-axiom/source-transfer/scalar routes still give `J_chi = 0`

Now:

- the nearest positive native PMNS routes have also been audited and exhausted
- there is no hidden exact PMNS-native route inside the current bank that
  already reaches nonzero `J_chi`

## One Concrete Next Theorem Target

The next honest theorem target is **not** another route scan.

The sharper current-bank no-go in
`PMNS_GRAPH_FIRST_CURRENT_IMAGE_NONCOLLAPSE_NOTE_2026-04-17.md` shows that the
current bank already realizes the full exact graph-first current image
`(\chi, w) in C x R`, and even fixed `w` slices still realize distinct
nonzero `chi`.

The newer sharper fixed-slice theorem in
`PMNS_GRAPH_FIRST_FIXED_SLICE_SELECTOR_HOLONOMY_NONCOLLAPSE_NOTE_2026-04-17.md`
then proves that the current bank still does **not** collapse `chi` even after
holding fixed:

- the trivial-character slice `w = w0`,
- the exact graph-first selector bundle `(tau, q)`,
- one exact native twisted-flux holonomy value.

So the next honest target is no longer a generic activation law on the whole
reduced family.

It is:

> **PMNS graph-first current-image collapse law.**  
> Derive, or rule out on a sharper exact subbank, a sole-axiom native law on
> the exact graph-first current image `(\chi, w)` that collapses it to a
> proper exact subset; more sharply, derive a genuinely new
> **fixed-slice current-image collapse law** beyond the current selector bundle
> `(tau, q)` and beyond one-angle native twisted-flux holonomy, and in
> particular a fixed-slice nontrivial-current activation law that selects
> nonzero `J_chi = chi`.

This is a genuine theorem target.

By contrast, the following are only conjectural ideas at this stage and are
**not** current-bank theorems:

- importing a Wilson-descendant law from outside the PMNS-native lane
- importing a DM right-sensitive selector law from outside the PMNS-native lane
- asserting that transport or alignment “should” induce nonzero `J_chi`
  without an exact current law

## Verification

```bash
python3 scripts/frontier_pmns_sole_axiom_native_current_route_exhaustion_2026_04_17.py
```
