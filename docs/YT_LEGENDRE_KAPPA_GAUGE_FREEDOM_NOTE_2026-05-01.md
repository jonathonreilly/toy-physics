# Top-Yukawa Legendre Kappa Gauge-Freedom Note

**Date:** 2026-05-01  
**Status:** exact negative boundary / Legendre normalization freedom  
**Runner:** `scripts/frontier_yt_legendre_kappa_gauge_freedom.py`  
**Certificate:** `outputs/yt_legendre_kappa_gauge_freedom_2026-05-01.json`

```yaml
actual_current_surface_status: exact negative boundary
conditional_surface_status: conditional-support for a future pole-residue or canonical-kinetic normalization theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "kappa_H remains a field-normalization freedom without a residue/kinetic condition."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The source-to-Higgs route needs the Legendre transform to fix the
source-to-canonical-field normalization `kappa_H`.  This note checks whether
the Legendre transform alone can select that normalization.

## Result

It cannot.

For a source generator `W[J]`, a source/operator rescaling

```text
W_k(J) = W(k J)
```

induces

```text
phi_k = dW_k/dJ = k phi,
Gamma_k(phi_k) = Gamma(phi_k / k).
```

The Legendre identity is preserved, but the curvature and the Yukawa readout
scale with `k`.

## Runner Result

```text
python3 scripts/frontier_yt_legendre_kappa_gauge_freedom.py
# SUMMARY: PASS=6 FAIL=0
```

The runner uses a quadratic source response as the minimal local model and
checks several `kappa` values:

| `kappa` | `Gamma''` | `y_readout = (1/sqrt(6)) kappa` |
|---:|---:|---:|
| `0.5` | `1.454545` | `0.204124` |
| `sqrt(8/9)` | `0.409091` | `0.384900` |
| `1.0` | `0.363636` | `0.408248` |
| `2.0` | `0.090909` | `0.816497` |

All rows satisfy the Legendre relation exactly.  The transform therefore does
not select `kappa_H = 1`.

## Consequence

The next theorem must supply an additional physical normalization condition:

```text
momentum-dependent scalar two-point function
-> physical scalar pole or canonical kinetic term
-> residue/kinetic normalization
-> kappa_H
```

Without that condition, the Legendre transform is exact support for the source
formalism, not a physical Yukawa readout.

## Non-Claims

- This note does not derive `kappa_H = 1`.
- This note does not identify the source scalar with `H_unit`.
- This note does not use observed `y_t` or `m_t`.
- This note does not promote the Ward theorem.
