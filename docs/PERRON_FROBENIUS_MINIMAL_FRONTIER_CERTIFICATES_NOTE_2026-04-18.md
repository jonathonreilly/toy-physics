# Perron-Frobenius Minimal Frontier Certificates

**Date:** 2026-04-18  
**Status:** exact science-only packaging of the remaining PF branch into a
minimal set of frontier certificates on the current bank  
**Script:** `scripts/frontier_perron_frobenius_minimal_frontier_certificates_2026_04_18.py`

## Question

After the Wilson audit, the PMNS-native readout closure, and the sharper
plaquette scalar reductions, what is the smallest honest list of remaining PF
frontier objects on the current bank?

## Answer

The current branch now reduces to three minimal frontier certificates:

1. **Wilson positive reopening certificate**
   one local physical Wilson `2-edge + 3` certificate, equivalently the sharp
   local path-algebra `Phi_chain` route plus the 3 scalar spectral identities;
2. **PMNS-native production certificate**
   one sole-axiom nontrivial fixed-slice holonomy-pair source law,
   equivalently production of nonzero `J_chi = chi`;
3. **Plaquette non-Wilson scalar certificate**
   one fixed-depth minimal `moment + K` certificate on the class-sector
   operator lane.

That is the smallest review-safe exact frontier decomposition now visible on
the branch.

## Setup

From
[PERRON_FROBENIUS_WILSON_DEPENDENCY_AUDIT_NOTE_2026-04-18.md](./PERRON_FROBENIUS_WILSON_DEPENDENCY_AUDIT_NOTE_2026-04-18.md):

- Wilson is the main positive reopening lever,
- but not the only blocker on the current bank.

From
[PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md](./PMNS_GRAPH_FIRST_FIXED_SLICE_TWO_HOLONOMY_PRODUCTION_BOUNDARY_NOTE_2026-04-17.md):

- after readout closure, the remaining PMNS-native blocker is exactly one
  nontrivial fixed-slice holonomy-pair source law.

From
[GAUGE_VACUUM_PLAQUETTE_BETA6_FIXED_DEPTH_SCALAR_CERTIFICATE_NOTE_2026-04-18.md](./GAUGE_VACUUM_PLAQUETTE_BETA6_FIXED_DEPTH_SCALAR_CERTIFICATE_NOTE_2026-04-18.md):

- the fixed-depth non-Wilson plaquette lane is now one minimal scalar
  `moment + K` certificate.

## Theorem 1: exact minimal frontier decomposition of the current PF branch

On the current bank, the remaining PF science is exactly decomposed into the
three frontier certificates listed above.

They are minimal in the following sense:

- the Wilson positive route has already been compressed to its sharpest local
  physical certificate,
- the PMNS-native lane has already been reduced from route search to a single
  production-law object,
- the plaquette non-Wilson lane has already been reduced from operator data to
  one scalar `moment + K` certificate.

So the branch is no longer honestly described as one vague “global PF gap.”
It is one minimal three-certificate frontier.

## Corollary 1: positive global reopening still runs primarily through Wilson

Among those three certificates, only the Wilson certificate is currently a
positive reopening lever for a common sole-axiom PF selector.

The PMNS-native and plaquette certificates are still exact current-bank
blockers.

## What this closes

- one exact minimal decomposition of the remaining PF work
- one reviewer-facing statement of which frontier is the positive reopening
  lever and which frontiers remain blockers

## What this does not close

- a positive global PF selector theorem
- realization of the Wilson certificate
- realization of the PMNS-native production certificate
- realization of the plaquette scalar certificate

## Why this matters

This gives the branch a clean top-level frontier map.

The repo can now say:

- the positive reopening lever is one Wilson local certificate,
- the PMNS-native unresolved object is one production certificate,
- the plaquette unresolved object is one scalar non-Wilson certificate.

That is a much cleaner hard-review statement than “many things are still open.”

## Command

```bash
python3 scripts/frontier_perron_frobenius_minimal_frontier_certificates_2026_04_18.py
```
