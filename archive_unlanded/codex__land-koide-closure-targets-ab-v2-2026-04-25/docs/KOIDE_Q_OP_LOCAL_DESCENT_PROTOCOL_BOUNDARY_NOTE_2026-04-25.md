# Koide Q OP Local-Descent Protocol Boundary Note

**Date:** 2026-04-25
**Status:** exact support / boundary note for the charged-lepton `Q`
source-domain problem; not retained Koide closure
**Primary runner:** `scripts/frontier_koide_q_op_local_descent_protocol_boundary.py`

## Purpose

This note lands the useful science from the `koide-closure-targets-AB-v2`
branch without accepting its overclaim.

The branch proposed:

```text
OP local-source principle + canonical descent
    -> dimensionless Q readout must use E_loc before evaluation
    -> z_eff = 0
    -> Q = 2/3
```

The exact algebra in that proposal is useful.  The physical inference is not
yet retained.  The missing theorem is still:

```text
derive that the physical charged-lepton dimensionless readout uses canonical
onsite descent before evaluating projected commutant source data.
```

So this note records the conditional route and the counterdomain sharply:
canonical descent erases `Z`; direct commutant readout does not.

## Retained inputs

| Tag | Input | Status |
|---|---|---|
| OP | Observable-principle scalar observables are local-source expansion coefficients for onsite projectors `P_x`. | retained OP authority |
| CD | Unique trace-preserving descent from `A=span{I,Z}` to strict onsite `D^C3=span{I}` is `E_loc(X)=Tr(X)I/3`. | exact support / criterion theorem |
| CRIT | On the admitted normalized reduced carrier, `z=0 <=> Q=2/3`; nonzero `z` gives non-Koide values. | exact support / criterion theorem |
| ONSITE | Strict onsite `C3`-invariant scalar sources erase `Z`, while the projected commutant grammar still admits `Z`. | support/no-go synthesis |

These inputs do not by themselves prove that the physical charged-lepton
dimensionless readout must descend projected commutant data before evaluation.

## Exact algebra that lands

Let `C` be the cyclic shift on the three-generation orbit.  The projected
commutant coordinate is

```text
Z = P_plus - P_perp
  = -I/3 + (2/3) C + (2/3) C^2.
```

Since `Tr(I)=3` and `Tr(C)=Tr(C^2)=0`,

```text
Tr(Z) = -1.
```

The operator `Z` has off-diagonal entries in the site basis, hence

```text
Z notin span{P_x}.
```

For a commutant source

```text
K = s I + z Z,
```

canonical local descent gives

```text
E_loc(K) = (Tr K / 3) I = (s - z/3) I.
```

Thus descent sends every projected commutant source to a strict onsite scalar
and kills the reduced traceless coordinate:

```text
z_eff(E_loc(K)) = 0.
```

Combining with CRIT gives the exact conditional implication:

```text
if physical Q-readout uses canonical onsite descent first,
then Q[K] = Q[E_loc(K)] = Q(z_eff=0) = 2/3.
```

## Why this is not a retained closure

The load-bearing step is not the formula for `E_loc`.  That formula is already
audited.  The load-bearing step is the protocol statement:

```text
Q[K] = Q[E_loc(K)]
```

for physical charged-lepton dimensionless readout.

OP proves locality for scalar observables in its local-source expansion.  It
does not, on current main, prove that every projected commutant background
source offered to the charged-lepton `Q` readout must first be replaced by its
trace-preserving onsite descent.  That is exactly the physical source-domain
law still under review.

Therefore the proposed branch does not prove:

```text
Q = 2/3 retained closure,
delta = 2/9 rad retained closure,
full charged-lepton Koide closure.
```

It proves a conditional route and a boundary:

```text
canonical descent closes Q if the physical readout protocol selects it;
direct commutant readout remains z-dependent.
```

## Counterdomain

On the admitted reduced carrier used by CRIT,

```text
Q(z) = 2 / (3(1+z)).
```

So direct evaluation without descent gives, for example,

```text
z = 0      -> Q = 2/3,
z = 1/3    -> Q = 1/2,
z = -1/3   -> Q = 1.
```

This is the important guardrail.  The descent protocol is not cosmetic; it is
load-bearing.  If the physical readout is allowed to use the projected
commutant coordinate directly, the branch does not close Koide.

## What lands

This note lands four support-grade facts:

1. `Z` is a `C3`-commutant source coordinate but not an onsite local source.
2. `E_loc(sI+zZ)=(s-z/3)I` exactly.
3. Canonical descent erases the reduced `Z` coordinate and conditionally gives
   `Q=2/3` through CRIT.
4. The physical protocol theorem `Q[K]=Q[E_loc(K)]` remains the missing
   primitive; until it is derived, `Q` and `delta` remain open.

## Closeout flags

```text
OP_LOCAL_DESCENT_ALGEBRA_EXACT=TRUE
CONDITIONAL_Q_CLOSES_IF_PHYSICAL_READOUT_USES_E_LOC=TRUE
DIRECT_COMMUTANT_READOUT_COUNTERDOMAIN_PRESENT=TRUE
Q_RETAINED_NATIVE_CLOSURE=FALSE
DELTA_2_OVER_9_RAD_RETAINED_CLOSURE=FALSE
FULL_DIMENSIONLESS_KOIDE_CLOSURE=FALSE
RESIDUAL_Q=derive_physical_charged_lepton_dimensionless_readout_uses_canonical_onsite_descent_or_excludes_Z
```
