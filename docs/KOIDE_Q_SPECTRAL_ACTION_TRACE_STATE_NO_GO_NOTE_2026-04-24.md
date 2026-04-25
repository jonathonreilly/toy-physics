# Koide Q spectral-action / modular trace-state no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_spectral_action_trace_state_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

Test whether a heat-kernel, spectral-action, zeta-residue, or modular/KMS trace
on the retained finite `C_3` quotient forces equal total singlet/doublet block
weights.  If it did, it would derive the missing `K_TL=0` law rather than
choosing the equal-block trace state.

## Executable theorem

The retained `C_3` graph Laplacian is

```text
L = 2I - C - C^2.
```

It has eigenvalue `0` on the rank-1 singlet and eigenvalue `3` on the rank-2
real doublet.  The heat/modular trace block totals are therefore

```text
W_plus(t) = 1
W_perp(t) = 2 exp(-3t)
R(t) = W_perp/W_plus = 2 exp(-3t).
```

Equal block totals occur only at

```text
t = log(2)/3.
```

The Hilbert/rank trace is `t=0`, which gives `R=2`, `Q=1`, and nonzero
`K_TL`.  The heat family itself realizes inequivalent block laws:

```text
t = 0          -> R = 2
t = log(2)/3  -> R = 1
t = log(4)/3  -> R = 1/2
```

The finite spectral action has the same problem in cutoff-function form:

```text
R_f = 2 f(3/Lambda^2) / f(0).
```

Equal block totals require `f(3/Lambda^2)=f(0)/2`, an extra cutoff
normalization.  The finite nonzero-spectrum zeta function `2*3^-s` is entire,
so there is no residue trace that canonically selects the equal-block state.

## Residual

```text
RESIDUAL_SCALAR = t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL
RESIDUAL_TRACE_STATE = t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL
```

The spectral-action route converts the missing Q primitive into a missing
modular-time/cutoff-value law.

## Why this is not closure

The result does not derive the equal-block trace state.  It shows that natural
spectral traces on the finite retained carrier give a one-parameter family or
a cutoff-function choice.  Selecting `t=log(2)/3` or `f3=f0/2` would be target
equivalent unless independently derived.

## Falsifiers

- A retained modular principle fixing `t=log(2)/3` from `Cl(3)/Z^3` data.
- A spectral-action theorem fixing `f(3/Lambda^2)=f(0)/2` from a canonical
  cutoff, not from the desired Q value.
- A non-finite spectral triple extension whose residue trace exists and
  proves equal total weights on the retained singlet/doublet quotient.

## Boundaries

- This runner covers the finite `C_3` carrier, its canonical graph Laplacian,
  heat/KMS traces, finite spectral-action test functions, and finite zeta
  residues.
- It does not exclude an enlarged noncommutative geometry where a new
  continuum residue theorem pushes down to the equal-block state.

## Hostile reviewer objections answered

- **"Heat flow might naturally choose the equal state."**  Heat flow provides
  the family `R(t)=2 exp(-3t)`; the equal point requires a specified time.
- **"The spectral action has canonical traces."**  The finite trace is
  rank-weighted unless a cutoff value is chosen.  The equal value needs
  `f3=f0/2`.
- **"Could zeta residues remove the parameter?"**  Not on this finite
  nonzero spectrum; the zeta function is entire and has no selecting residue.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_spectral_action_trace_state_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_SPECTRAL_ACTION_TRACE_STATE_NO_GO=TRUE
Q_SPECTRAL_ACTION_TRACE_STATE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL
RESIDUAL_TRACE_STATE=t_minus_log2_over3_or_f3_minus_f0_over2_equiv_K_TL
```
