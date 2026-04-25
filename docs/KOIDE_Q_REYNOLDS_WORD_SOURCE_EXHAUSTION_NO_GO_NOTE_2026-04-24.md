# Koide Q Reynolds-projected word-source exhaustion no-go

**Date:** 2026-04-24  
**Runner:** `scripts/frontier_koide_q_reynolds_word_source_exhaustion_no_go.py`  
**Status:** no-go; not closure

## Theorem attempt

The previous local `C_3` polynomial audit worked inside the central
singlet/doublet idempotent algebra.  This packet strengthens the source class:
start with an arbitrary higher-order local matrix/Clifford word `W`, then
retain only its `C_3`-equivariant part by the Reynolds projector

```text
R(W) = (W + C W C^-1 + C^2 W C^-2)/3.
```

If this larger grammar forced the normalized traceless coefficient to vanish,
it would derive `K_TL=0` without importing the missing primitive.

## Executable theorem

The Reynolds image is exactly the full `C_3` commutant:

```text
R(W) = a0 I + a1 C + a2 C^2.
```

On the real symmetric second-order carrier this becomes

```text
S(d,p) = d I + p(C + C^2).
```

The block eigenvalues are

```text
lambda_plus = d + 2p
lambda_perp = d - p
A_odd = (lambda_plus - lambda_perp)/2 = 3p/2.
```

Trace normalization removes `d` but leaves `p(C+C^2)`.  Positivity also does
not select `p=0`: with trace fixed to `3`, the positive interval contains
negative, zero, and positive quotient coefficients.

## Residual

```text
RESIDUAL_SCALAR = p_equiv_A_odd_equiv_K_TL
RESIDUAL_COEFFICIENT = p_equiv_A_odd_equiv_K_TL
```

The strengthened higher-order word source class therefore reduces to the same
one scalar already isolated in the Q lane.

## Why this is not closure

The result is an exhaustion theorem with a negative closeout.  It proves that
`C_3` Reynolds projection, arbitrary word order, trace fixing, and positivity
do not derive the missing source law.  The codimension-one condition `p=0`
would still be an extra physical principle.

## Residual atlas and route selection

After this exhaustion, the Q residual is still one scalar:

```text
Which retained theorem sets A_odd = 0 on the normalized second-order carrier?
```

Routes that remain logically distinct from the just-closed local variations:

1. **Generator-selective electroweak grading:** derive `SU(2)_L - U(1)_Y`
   as an internal superconnection law rather than field-statistics grading.
2. **Nonlocal topological inflow:** tie `A_odd` to a boundary index density not
   captured by local anomaly cancellation.
3. **Modular/spectral-action residue:** test whether heat-kernel residues at
   the quotient force the trace state to be block-total rather than rank-total.
4. **Monoidal/categorical trace upgrade:** add tensor functoriality constraints
   beyond central-state naturality and see whether rank asymmetry is forbidden.
5. **Gauge-neutral quotient theorem:** prove all gauge-neutral quotient
   observables have zero traceless source after integrating the retained taste
   carrier.
6. **Selected-line Berry/APS bridge:** shift to delta and derive the physical
   endpoint law, not the ambient `2/9`.
7. **Spectral-flow boundary condition:** test whether a Wilson/Dirac endpoint
   condition fixes the selected line rather than only the integer flow.
8. **Exhaustive nonlocal source-class theorem:** classify all finite-range
   `C_3`-equivariant kernels on the quotient and prove the residual coefficient
   is the only remaining primitive.

The hardest viable next Q route is the spectral-action/modular-residue route:
it is not a local polynomial variation, and it can in principle impose a trace
state rather than a source coefficient by hand.

## Falsifiers

- A retained theorem proving the Reynolds quotient coefficient `p` must vanish
  for all admissible higher-order local words.
- A positivity, reflection-positivity, or locality axiom that collapses the
  allowed interval for `p` to the single point `p=0`.
- A nonlocal source classification where the local Reynolds counterfamily is
  forbidden by a physical boundary condition.

## Boundaries

- The runner covers finite local word sources on the three-state cyclic
  carrier followed by exact `C_3` Reynolds projection.
- It does not rule out nonlocal kernels, topological boundary terms, or a new
  physical principle that sets the quotient coefficient after projection.

## Hostile reviewer objections answered

- **"Higher-order words may cancel the odd coefficient."**  They may for
  special choices, but the projection image is onto the full commutant.  There
  are admissible word representatives with any `p`.
- **"Trace normalization should remove the source."**  It removes `d`; the
  coefficient `p` survives.
- **"Positivity should select equality."**  The runner gives trace-fixed
  positive examples with `p<0`, `p=0`, and `p>0`.

## Verification

Run:

```bash
python3 scripts/frontier_koide_q_reynolds_word_source_exhaustion_no_go.py
python3 scripts/frontier_koide_hostile_review_guard.py
```

Expected runner closeout:

```text
KOIDE_Q_REYNOLDS_WORD_SOURCE_EXHAUSTION_NO_GO=TRUE
Q_REYNOLDS_WORD_SOURCE_EXHAUSTION_CLOSES_Q=FALSE
RESIDUAL_SCALAR=p_equiv_A_odd_equiv_K_TL
RESIDUAL_COEFFICIENT=p_equiv_A_odd_equiv_K_TL
```
