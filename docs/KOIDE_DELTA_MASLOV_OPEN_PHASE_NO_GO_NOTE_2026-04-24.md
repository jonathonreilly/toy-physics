# Koide delta Maslov/open-phase no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_delta_maslov_open_phase_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Use Maslov/caustic quantization of the selected open line, possibly combined
with retained `C_3` character phases, to derive the physical Brannen endpoint:

```text
theta_end - theta0 = eta_APS = 2/9.
```

## Executable theorem

The ambient support scalar remains exact:

```text
eta_APS = 2/9.
```

Maslov jump phases in cycle units lie on the quarter-integer lattice:

```text
mu/4 = {0, 1/4, 1/2, 3/4} mod 1.
```

The APS value is not on that lattice:

```text
2/9 notin {0,1/4,1/2,3/4}.
```

Adding `C_3` character phases gives:

```text
k/3 + mu/4 mod 1,
```

a denominator-12 lattice.  The runner verifies that `2/9` is not in that
combined lattice either.

## Open-phase obstruction

For an open selected line, the phase has a smooth/open contribution and endpoint
trivialization:

```text
delta_open = a + mu/4 + chi_end - chi_start.
```

Solving for the missing continuous piece gives:

```text
a = -chi_end + chi_start - mu/4 + 2/9.
```

Solving for endpoint trivialization gives:

```text
chi_end = -a + chi_start - mu/4 + 2/9.
```

So the endpoint can always be fitted once a smooth integral or endpoint gauge is
left free.  That is not a derivation.

## Residual

```text
RESIDUAL_ENDPOINT = theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION = selected_line_open_phase_smooth_part_or_endpoint_gauge
```

## Why this is not closure

Maslov data quantize caustic jumps.  They do not determine the smooth open
Berry contribution or endpoint trivialization.  The equality with ambient APS
eta remains the bridge law.

## Falsifiers

- A retained theorem making the selected-line smooth Berry contribution vanish
  and placing `2/9` on a physically normalized Maslov/C3 lattice.
- A canonical endpoint trivialization that identifies the open selected-line
  phase with the ambient APS eta invariant.
- A proof that the relevant Maslov normalization is not `mu/4` in cycle units
  but a retained denominator-9 refinement.

## Boundaries

- Covers standard Maslov quarter-lattice arithmetic and its combination with
  `C_3` character phases.
- Does not exclude a future retained open-line functor with a denominator-9
  endpoint normalization.

## Hostile reviewer objections answered

- **"Maslov indices are topological, so they should fix the phase."**  They fix
  jump data, not the entire open Berry phase.
- **"`C_3` supplies thirds."**  Thirds plus quarters produce denominator 12,
  not the APS value `2/9`.
- **"You can choose the smooth contribution to hit `2/9`."**  Yes, and that
  confirms the residual is a free endpoint law.

## Verification

Run:

```bash
python3 scripts/frontier_koide_delta_maslov_open_phase_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_DELTA_MASLOV_OPEN_PHASE_NO_GO=TRUE
DELTA_MASLOV_OPEN_PHASE_CLOSES_DELTA=FALSE
RESIDUAL_ENDPOINT=theta_end-theta0-eta_APS
RESIDUAL_TRIVIALIZATION=selected_line_open_phase_smooth_part_or_endpoint_gauge
```
