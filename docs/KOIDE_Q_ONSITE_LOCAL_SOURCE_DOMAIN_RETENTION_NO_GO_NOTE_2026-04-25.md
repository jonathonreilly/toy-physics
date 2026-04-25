# Koide Q onsite local source-domain retention no-go

**Date:** 2026-04-25  
**Runner:** `scripts/frontier_koide_q_onsite_local_source_domain_retention_no_go.py`  
**Status:** conditional support; retained no-go; Q not closed

## Theorem attempt

Use the retained exact lattice observable principle to force the undeformed
charged-lepton scalar source domain to be onsite local lattice functions:

```text
J = sum_x j_x P_x.
```

If the physical undeformed scalar backgrounds are exactly those local functions,
then `C3` invariance on the physical three-site generation orbit forces:

```text
diag(a,b,c) = s I.
```

That would exclude the native traceless background

```text
zZ,  Z = P_plus - P_perp,
```

and the zero-source Q support chain would close.

## Exact separation

The onsite local source object is the diagonal function algebra:

```text
C^3 = span{P_0, P_1, P_2}.
```

The runner verifies:

```text
C diag(a,b,c) C^-1 = diag(a,b,c)
  -> a = b = c.
```

So the `C3`-fixed onsite local scalar source space is one-dimensional.

The central/projected source object is different.  On the same carrier:

```text
P_plus = (I + C + C^2)/3,
P_perp = I - P_plus,
Z = P_plus - P_perp
  = -1/3 I + 2/3 C + 2/3 C^2.
```

Thus `Z` lies in the `C3` commutant `End_C3(V)`, but not in the onsite
function algebra.  The intersection of onsite functions with the `C3`
commutant is only scalar `I`.

## Conditional positive result

If the retained physical source-domain theorem were:

```text
physical undeformed scalar sources = onsite local functions,
```

then:

```text
z = 0 -> K_TL = 0 -> Q = 2/3.
```

This is the strongest version of the physical-lattice route so far.  It
separates local source functions from projected commutant sources exactly.

## Why this is not retained closure

The current retained Q source-domain notes still admit central/projected source
effects:

```text
P_plus, P_perp, Z.
```

The observable principle tells how to read scalar responses once the source
direction is supplied.  It does not, by itself, prove that the physical
charged-lepton source domain is only onsite functions rather than the broader
`C3` commutant/projected source domain used in the Q no-go stack.

So the retained counterdomain remains:

```text
sI + zZ.
```

For example:

```text
z = -1/3 -> Q = 1, K_TL = 3/8.
```

## Hostile review

- No Koide target is assumed.  The target appears only after comparing the
  closing onsite-function domain with the counterclosing commutant domain.
- No PDG masses, observational `H_*` pin, `delta=2/9`, or Brannen-phase input
  appears.
- The conditional onsite-domain theorem is not promoted as retained closure.
- The missing theorem is named directly: retain the local-function source
  domain over the `C3` commutant/projected source domain.

## Residual

```text
RESIDUAL_SCALAR =
  derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant

RESIDUAL_SOURCE =
  current_Q_source_domain_still_admits_C3_commutant_Z

COUNTERMODEL =
  C3_commutant_source_z_minus_1_over_3_Q_1_K_TL_3_over_8
```

## Verification

Run:

```bash
python3 -m py_compile scripts/frontier_koide_q_onsite_local_source_domain_retention_no_go.py
python3 scripts/frontier_koide_q_onsite_local_source_domain_retention_no_go.py
```

Expected result:

```text
KOIDE_Q_ONSITE_LOCAL_SOURCE_DOMAIN_RETENTION_NO_GO=TRUE
Q_ONSITE_LOCAL_SOURCE_DOMAIN_CLOSES_Q_RETAINED_ONLY=FALSE
CONDITIONAL_Q_CLOSES_IF_SOURCE_DOMAIN_EQUALS_ONSITE_FUNCTION_ALGEBRA=TRUE
RESIDUAL_SCALAR=derive_retained_source_domain_equals_onsite_function_algebra_not_C3_commutant
```
