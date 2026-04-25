# Koide delta Chern-Simons level-normalization no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_chern_simons_level_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether a Chern-Simons/lens-space topological action on the retained
`Z_3` boundary produces the selected-line endpoint `eta_APS=2/9`.

## Executable theorem

For a `Z_p` flat sector with `p=3` and generator charge `a=1`, common
quantized `U(1)`-style phase fractions are:

```text
k a^2 / p     = k/3
k a^2 / 2p    = k/6
```

Integer `k` gives thirds or sixths:

```text
k/3: 0, 1/3, 2/3, ...
k/6: 0, 1/6, 1/3, 1/2, ...
```

Neither lattice contains `2/9`.

To hit `2/9`:

```text
k/3 = 2/9  -> k = 2/3
k/6 = 2/9  -> k = 4/3
```

Both are fractional level choices relative to these standard normalizations.

## Residual

```text
RESIDUAL_LEVEL = fractional_CS_level_needed_for_eta_APS
RESIDUAL_ENDPOINT = theta_end - theta0 - eta_APS
```

Even after choosing a fractional normalization that produces `2/9`, one still
needs the physical map from topological action phase to selected-line open
Berry endpoint.

## Why this is not closure

Standard quantized CS levels do not produce the endpoint value.  A fractional
level can be chosen to match it, but that is a normalization primitive unless
derived.  The open endpoint bridge remains separate.

## Falsifiers

- A retained CS/spin-CS normalization whose allowed level lattice contains
  `2/9` for the retained `Z_3` sector.
- A derivation of the fractional level from `Cl(3)/Z^3` data.
- A theorem identifying the resulting topological phase with the selected-line
  open endpoint.

## Boundaries

- The runner covers the simple `k/p` and `k/(2p)` phase lattices for the
  retained `p=3` generator sector.
- It does not exclude a more elaborate TQFT with a derived fractional level.

## Hostile reviewer objections answered

- **"CS invariants can be fractional."**  Yes, but the required fraction must
  be derived from a retained level/normalization, not chosen to match.
- **"APS already gives `2/9`."**  Correct; this runner tests whether CS level
  quantization supplies an independent endpoint bridge.
- **"Could a spin refinement help?"**  The tested `2p` normalization still
  misses `2/9` at integer level.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_chern_simons_level_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_DELTA_CHERN_SIMONS_LEVEL_NO_GO=TRUE
DELTA_CHERN_SIMONS_LEVEL_CLOSES_DELTA=FALSE
RESIDUAL_LEVEL=fractional_CS_level_needed_for_eta_APS
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
```
