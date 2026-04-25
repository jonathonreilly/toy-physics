# Koide Q Noether-source admissibility no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_noether_source_admissibility_no_go.py`  
**Status:** no-go under current retained data; conditional positive only after
adding Noether-only source admissibility plus a retained plus/perp mixer

## Theorem Attempt

Try to exclude the final central label source

```text
Z = P_plus - P_perp
```

by treating its coefficient as a chemical potential.  If physical
charged-lepton sources are allowed only for conserved Noether charges, and if
the retained dynamics mixes the normalized plus/perp carrier, then `Z` is not
conserved.  The chemical potential for `Z` must vanish:

```text
K_TL = 0
-> Y = I_2
-> Q = 2/3.
```

## Brainstormed Route Variants

1. **Noether-only source grammar:** only conserved charges may carry source
   coefficients.
2. **Retained plus/perp mixer:** a physical mixing generator makes
   `[H,Z] != 0`.
3. **What if source probes are broader than charges?** Then local
   observable-principle sources may still probe `Z`.
4. **What if the retained dynamics is block-preserving?** Then `Z` is
   conserved and its source coefficient is allowed.
5. **What if chemical equilibrium is imposed instead of conservation?** Then
   equal chemical potentials close Q, but the equilibration/mixer law is the
   same missing input.

Ranking before the audit: the Noether-only route is strong because it attacks
the exact residual `Z` directly, but it is fragile under hostile review because
the observable principle has historically allowed local probes, not only
Noether charges.

## Exact Result

For a diagonal source

```text
K = a I + b Z
```

and a plus/perp mixer

```text
H_mix = [[0,g],[g,0]],
```

the commutator equation gives:

```text
[H_mix,K] = 0  =>  b = 0.
```

So the route would close Q if both the mixer and Noether-only source grammar
were retained.

But the current retained carrier still admits the block-preserving
countermodel:

```text
H_diag = diag(h_plus,h_perp)
[H_diag,Z] = 0
[H_diag,aI+bZ] = 0 for every b.
```

The nonclosing retained source state remains:

```text
w = 1/3
Q = 1
K_TL = 3/8.
```

## Hostile Review

- **Circular assumption:** avoided.  `K_TL=0` is not assumed; it is derived
  only in the conditional mixer branch.
- **Target import:** none.  `Q=2/3` appears only after solving `b=0`.
- **Hidden observational pin:** none.
- **Unstated primitive:** exact.  The route needs two extra physical inputs:
  Noether-only source admissibility and retained block mixing.
- **Missing axiom link:** exact.  The observable principle differentiates
  `W[J]` with respect to local probes; it does not restrict `J` to conserved
  charges.

## Residual

```text
RESIDUAL_SCALAR = noether_admissible_Z_source_coefficient_equiv_K_TL
RESIDUAL_PRIMITIVE =
  derive_no_Z_conserved_charge_or_noether_only_source_grammar
```

## Musk Simplification Pass

- **Make requirements less wrong:** the real requirement is not "source-free";
  it is "no admissible physical source in the `Z` direction."
- **Delete:** the Noether language can be deleted unless a retained conserved
  charge/source grammar is added.
- **Simplify:** the whole route is the single commutator identity
  `[H_mix,aI+bZ]=0 => b=0`, plus the counteridentity
  `[H_diag,aI+bZ]=0`.
- **Accelerate:** future attacks should look for a retained theorem making
  `H_mix` physical or making non-Noether source probes inadmissible.
- **Automate:** this runner now guards against promoting "chemical potential
  must vanish" without proving the admissibility and mixing premises.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_noether_source_admissibility_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected closeout:

```text
KOIDE_Q_NOETHER_SOURCE_ADMISSIBILITY_NO_GO=TRUE
Q_NOETHER_SOURCE_ADMISSIBILITY_CLOSES_Q=FALSE
CONDITIONAL_Q_CLOSES_IF_NOETHER_ONLY_PLUS_MIXER=TRUE
RESIDUAL_SCALAR=noether_admissible_Z_source_coefficient_equiv_K_TL
RESIDUAL_PRIMITIVE=derive_no_Z_conserved_charge_or_noether_only_source_grammar
```
