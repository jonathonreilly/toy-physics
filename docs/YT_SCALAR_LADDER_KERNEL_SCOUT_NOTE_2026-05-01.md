# Top-Yukawa Scalar-Channel Ladder Kernel Scout

**Date:** 2026-05-01  
**Status:** bounded support / ladder-kernel scout; no retention proposal  
**Runner:** `scripts/frontier_yt_scalar_ladder_kernel_scout.py`  
**Certificate:** `outputs/yt_scalar_ladder_kernel_scout_2026-05-01.json`

```yaml
actual_current_surface_status: bounded-support
conditional_surface_status: conditional-support for a future exact Bethe-Salpeter kernel theorem
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Scout depends on explicit mass, IR regulator, and simplified scalar projector."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Purpose

The HS/RPA contact attempt showed that a local scalar contact coupling `G` is
not part of `A_min`.  The constructive alternative is to use the actual Wilson
gauge exchange as a scalar-channel ladder kernel and look for a pole condition:

```text
lambda_max(K_scalar Pi) = 1.
```

This note records a finite-momentum scout for that route.

## Scout Setup

The runner builds a finite `4^4` momentum-grid kernel:

```text
K(k,q) = C_F / (q_hat^2 + mu_IR^2),
C_F = 4/3,
Pi weight ~ 1 / (m^2 + sum_mu sin^2 k_mu)^2.
```

The largest eigenvalue of the symmetrized kernel is used as a scout pole
criterion.  This is not the final theorem: the exact staggered taste/spin/color
projector, the IR treatment, and the finite-volume limit are deliberately left
visible.

## Runner Result

```text
python3 scripts/frontier_yt_scalar_ladder_kernel_scout.py
# SUMMARY: PASS=6 FAIL=0
```

The scout finds:

| Check | Result |
|---|---|
| finite ladder scan runs | `24` points |
| eigenvalue sensitivity | spread `8.112e+04` |
| pole criterion crosses under IR choice | yes, at `m=0.5` |
| heavy mass can remove scout pole | `m=1.0` has `lambda_max < 1` across scan |
| light mass produces scout pole | `m=0.1` has `lambda_max >= 1` across scan |

## Interpretation

This is useful bounded support for the next theorem shape:

```text
derive exact scalar-channel Wilson-staggered ladder kernel
-> fix scalar color/taste/spin projector without H_unit readout authority
-> control finite-volume and IR limits
-> prove eigenvalue crossing
-> compute pole residue from d lambda / d p^2.
```

It is not retained closure.  The scout pole criterion moves under mass and
IR/kernel treatment, which means the current campaign still lacks the exact
interacting kernel theorem needed to convert the source bubble into a physical
Higgs-carrier pole residue.

## Non-Claims

- This note is not a production measurement.
- This note is not a retained scalar pole theorem.
- This note does not use observed top, Higgs, or Yukawa values.
- This note does not define `y_t` by an `H_unit` matrix element.
