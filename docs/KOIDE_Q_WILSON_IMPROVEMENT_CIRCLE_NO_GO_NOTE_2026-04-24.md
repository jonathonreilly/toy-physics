# Koide Q Wilson/Improvement Circle No-Go Note

**Date:** 2026-04-24
**Runner:** `scripts/frontier_koide_q_wilson_improvement_circle_no_go.py`
**Status:** executable no-go

RESIDUAL_SCALAR=`sigma_W = r1^2 + r2^2 - 2*r0^2`

## Theorem Attempt

The strongest remaining Wilson-side attempt was: the retained local
Wilson/improvement descendant on the cyclic charged-lepton carrier might force
the response circle

```text
r1^2 + r2^2 = 2 r0^2
```

from locality plus `C3` covariance. If true, this would supply the missing
source/radius law on the normalized second-order carrier and would feed the
already-executable chain to `Q = 2/3`.

## Brainstormed Variants

1. **Local Wilson coefficient collapse:** maybe the adjacent-chain Wilson
   improvement coefficients collapse to one universal ratio.
2. **Reflection-even subroute:** maybe time reversal removes `r2` and forces
   `r1/r0`.
3. **Scale-normalized extremum:** maybe fixing `r0` plus a retained quadratic
   action forces the radius of `(r1,r2)`.
4. **Assumption inversion:** maybe the microscopic law should not determine
   `(r0,r1,r2)` independently; test whether the exact response map has a
   kernel or rank drop.
5. **What if locality is too weak:** if locality only supplies the carrier, the
   missing theorem must be a coefficient law, not another compression theorem.

Ranking for this cycle:

1. Wilson/improvement coefficient law: best direct attack on the microscopic
   three-response source law.
2. PMNS `hw=1` transfer-pack projection: retained interface but likely repeats
   source-bank freedom.
3. Odd-slot transfer-kernel extension: useful next route if Wilson fails.
4. Delta Wilson-line phase law: only after Q stalls.
5. Color-sector correction: weaker for charged-lepton `K_TL`.

## Executable Result

Use the retained cyclic basis

```text
B0 = I
B1 = C + C^2
B2 = i(C - C^2)
```

The exact Frobenius Gram matrix is

```text
diag(3, 6, 6).
```

For the most general retained `C3`-covariant local first-variation target

```text
H_W = c0 B0 + c1 B1 + c2 B2,
```

the responses are

```text
r0 = 3 c0
r1 = 6 c1
r2 = 6 c2.
```

The coefficient-to-response map has rank `3`. Therefore `C3` covariance and
locality give the coordinates, not a relation among them.

The Koide response residual becomes

```text
sigma_W = r1^2 + r2^2 - 2 r0^2
        = -18 c0^2 + 36 c1^2 + 36 c2^2.
```

This polynomial is not identically zero. Exact witnesses:

```text
scalar_only       (c0,c1,c2) = (1,0,0)  -> sigma_W = -18
even_only         (c0,c1,c2) = (0,1,0)  -> sigma_W =  36
odd_only          (c0,c1,c2) = (0,0,1)  -> sigma_W =  36
generic_off_circle(c0,c1,c2) = (1,1,0)  -> sigma_W =  18
```

Reflection/time-reversal improves the situation only by setting `c2 = 0`.
Then

```text
sigma_even = 18(2 c1^2 - c0^2),
```

so the circle requires

```text
c1/c0 = +/- 1/sqrt(2).
```

That is a new scalar coefficient law. It is not a retained consequence of the
Wilson carrier, the cyclic compression theorem, or reflection symmetry.

## Hostile Review

- **Circularity:** the runner does not insert `sigma_W = 0`; it tests whether
  it is an identity and finds exact counterexamples.
- **Target import:** no `K_TL`, `K`, `P_Q`, Koide value, Brannen value, PDG mass
  data, or `H_*` witness is used as input.
- **Hidden selector:** imposing `sigma_W = 0` would be exactly the missing
  selector/source law, not a theorem from the Wilson carrier.
- **Axiom link:** locality plus `C3` covariance explain why the carrier is
  three-dimensional, but do not explain why its coefficient vector has the
  Koide radius.
- **Scope:** this rejects only the claim that the present retained
  Wilson/improvement structure already forces the circle. A stronger future
  microscopic coefficient theorem would still be a new route.

## Musk Simplification Pass

1. **Make requirements less wrong:** the Wilson route does not need a larger
   Hermitian target; it needs one coefficient/radius law on three responses.
2. **Delete:** further carrier-compression work is not the bottleneck for this
   route.
3. **Simplify:** the entire obstruction is the single residual
   `sigma_W = r1^2 + r2^2 - 2*r0^2`.
4. **Accelerate:** future Wilson attacks should test coefficient-ratio theorems
   directly before building larger constructions.
5. **Automate:** the hostile-review guard should keep requiring residual labels
   and negative closeout flags on every no-go note/script.

## Verdict

The Wilson/improvement route does not close charged-lepton Koide on the current
retained package.

```text
WILSON_IMPROVEMENT_FORCES_K_TL=FALSE
KOIDE_Q_WILSON_IMPROVEMENT_CIRCLE_CLOSES_Q=FALSE
RESIDUAL_SCALAR=sigma_W=r1^2+r2^2-2*r0^2
```

