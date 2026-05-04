# Quantum Horizon k-Sweep

**Date:** 2026-04-05  
**Status:** bounded no-go against the stronger wavelength-dependent horizon claim on the proposed_retained absorbing family

## Artifact chain

- [`scripts/quantum_horizon_k_sweep.py`](/Users/jonreilly/Projects/Physics/scripts/quantum_horizon_k_sweep.py)
- [`logs/2026-04-05-quantum-horizon-k-sweep.txt`](/Users/jonreilly/Projects/Physics/logs/2026-04-05-quantum-horizon-k-sweep.txt)

## Question

On the retained absorbing-horizon sector-stencil family, does the 50%-escape
threshold `alpha_crit` shift meaningfully with wavelength `k`, or was the
stronger "quantum horizon" story ahead of the retained evidence?

This note is intentionally narrow:

- one family: retained generated-geometry sector-stencil horizon family
- one observable: `alpha_crit` where escape falls to 50% of free propagation
- one separation: sub-Nyquist rows vs above-Nyquist rows

## Frozen result

The retained sweep uses:

- `k = 1, 2, 3, 4, 5, 6, 7, 10`
- `alpha = 0.00 .. 2.00` in steps of `0.05`
- the same retained generated-geometry sector-stencil family as the minimal
  absorbing horizon probe

Frozen readout:

| `k` | escape at `alpha=0` | `alpha_crit` | regime |
| --- | ---: | ---: | --- |
| `1.0` | `1.000` | `0.08` | sub-Nyquist |
| `2.0` | `1.000` | `0.08` | sub-Nyquist |
| `3.0` | `1.000` | `0.08` | sub-Nyquist |
| `4.0` | `1.000` | `0.08` | sub-Nyquist |
| `5.0` | `1.000` | `0.09` | sub-Nyquist |
| `6.0` | `1.000` | `0.09` | sub-Nyquist |
| `7.0` | `1.000` | `0.09` | above Nyquist |
| `10.0` | `1.000` | `0.08` | above Nyquist |

Sub-Nyquist fit from the frozen sweep:

- `alpha_crit ≈ 0.08 * k^0.03`

## Safe read

The strongest retained statement is:

- on this horizon observable, `alpha_crit` is nearly flat in `k`
- the retained family does **not** support a strong wavelength-dependent
  horizon shift
- the stronger "quantum horizon" narrative does not survive this bounded sweep

## Honest limitation

This is a no-go only for this observable on this retained family.

- it does **not** rule out every possible wavelength-dependent trapping effect
- it does say the present absorbing-horizon escape threshold is not carrying
  that stronger claim
- if a spectral or wavelength-dependent horizon story survives elsewhere, it
  still needs a fresh script/log/note chain

## Branch verdict

Treat this as a useful overclaim-killer:

- the retained absorbing proxy still has a real trapping threshold
- but it does **not** currently support a strong `k`-dependent horizon law

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [minimal_absorbing_horizon_probe_note](MINIMAL_ABSORBING_HORIZON_PROBE_NOTE.md)
