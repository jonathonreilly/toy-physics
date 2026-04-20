# DM PMNS Chamber Spectral Completeness Theorem

**Date:** 2026-04-20  
**Lane:** DM A-BCC / open import `I11`  
**Status:** closed on this branch for the **active chamber**. The compact
`chi^2 = 0` chamber set is exactly three points:

- Basin 1 on `sigma = (2,1,0)`
- Basin 2 on `sigma = (2,1,0)`
- Basin X on `sigma = (2,0,1)`

**Primary runner:**  
`scripts/frontier_dm_pmns_chamber_spectral_completeness_theorem_2026_04_20.py`

---

## 0. Question

After `DM_PMNS_ASYMPTOTIC_SOURCE_NO_GO_NOTE_2026-04-20.md` rules out
unbounded exact PMNS-fit basins, can the remaining compact chamber problem be
closed exactly enough to enumerate the chamber `chi^2 = 0` roots?

## 1. Bottom line

Yes.

On the two branches with electron row fixed to the third axis,

```text
sigma = (2,1,0),  sigma = (2,0,1),
```

the PMNS angle constraints admit an exact ordered-eigenvalue reduction.  On
each branch the three angle equations collapse to:

1. two linear equations for `(delta, q_+)` in terms of the ordered eigenvalues
   `(lambda_1 < lambda_2 < lambda_3)`,
2. plus one residual projector equation,
3. together with the exact `Tr(H^2)` and `det(H)` spectral identities.

The reduced real ordered-eigenvalue system has:

- exactly four real roots on `sigma = (2,1,0)`, namely
  `{Basin 1, Basin 2, Basin N, Basin P}`;
- exactly four real roots on `sigma = (2,0,1)`, namely
  `{Basin X, X_a, X_b, X_c}`.

Applying the active-chamber inequality

```text
q_+ + delta >= sqrt(8/3)
```

keeps exactly

```text
{Basin 1, Basin 2, Basin X}.
```

An independent direct chamber solve over all six row permutations returns the
same three `(point, sigma)` pairs and no others.

So the compact chamber completeness problem is closed on this branch.

## 2. Theorem

**Theorem (compact active-chamber PMNS completeness).** Fix the target PMNS
angle triple

```text
(sin^2 theta_12, sin^2 theta_13, sin^2 theta_23)
= (0.307, 0.0218, 0.545).
```

On the affine DM Hermitian family

```text
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q,
```

the chamber `chi^2 = 0` set

```text
chi^2 = (s12^2 - 0.307)^2 + (s13^2 - 0.0218)^2 + (s23^2 - 0.545)^2 = 0,
q_+ + delta >= sqrt(8/3),
```

consists of exactly three points:

```text
sigma = (2,1,0): Basin 1, Basin 2
sigma = (2,0,1): Basin X.
```

No other row permutation supports a chamber `chi^2 = 0` root.

### Proof sketch

For `sigma = (2,1,0)` and `sigma = (2,0,1)`, use the diagonal projector
formula

```text
|V_{a k}|^2 = adj(H - lambda_k I)_{aa} / prod_{j != k}(lambda_k - lambda_j).
```

On each branch, the three PMNS angle constraints give:

- one projector equation at `lambda_3` for the electron-axis `s13^2`,
- one projector equation at `lambda_2` for the electron-axis `s12^2`,
- one projector equation at `lambda_3` for the mu-axis `s23^2`.

Taking differences cancels the quadratic terms in `(delta, q_+)`, leaving two
linear relations for `(delta, q_+)` in terms of `(lambda_1, lambda_2,
lambda_3)`. Substituting those into the residual projector equation and the
exact identities

```text
lambda_1^2 + lambda_2^2 + lambda_3^2 = Tr(H^2),
lambda_1 lambda_2 lambda_3 = det(H),
```

gives a reduced ordered-eigenvalue system.

The runner solves that reduced system directly and finds exactly four real
ordered roots on each of the two branches above. Their chart points are:

- `sigma = (2,1,0)`:
  - Basin 1: `(0.657061342210, 0.933806343759, 0.715042329587)`
  - Basin 2: `(28.006188289565, 20.721831213931, 5.011599458305)`
  - Basin N: `(0.501997247472, 0.853543345404, 0.425916455114)`
  - Basin P: `(1.037883050950, 1.433018557503, -1.329548075477)`
- `sigma = (2,0,1)`:
  - Basin X: `(21.128263668694, 12.680028023619, 2.089234805861)`
  - plus three off-chamber companions.

Their chamber margins are:

- Basin 1: `+0.0158555`
- Basin 2: `+24.1004`
- Basin N: `-0.3535`
- Basin P: `-1.5295`
- Basin X: `+13.1363`
- the three `sigma = (2,0,1)` companions: all negative.

So only Basin 1, Basin 2, and Basin X survive the chamber cut.

Finally, an independent direct chamber solve in the original variables
`(m, delta, q_+)`, across all six row permutations, returns exactly the same
three chamber roots and no others.

QED.

## 3. Consequence for `I11`

This closes `I11` in the form actually needed by the DM gate:

- the asymptotic theorem already removed the infinity-tail loophole;
- the present theorem closes the compact chamber remainder.

So the active-chamber `chi^2 = 0` landscape is no longer empirical. It is
exactly the 3-point set above.

## 4. What this does and does not say

What is closed:

- compact chamber completeness for the PMNS angle system,
- exact chamber enumeration of the surviving `(point, sigma)` pairs.

What is not claimed:

- that Basin 1 is already selected without further law,
- that off-chamber real roots are physically relevant,
- that `sigma_hier` is derived.

This theorem closes the chamber **root list**. It does not by itself close the
remaining basin / parity / CP selection among that list.

## 5. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_chamber_spectral_completeness_theorem_2026_04_20.py
```

Expected final line:

```text
PASS=11  FAIL=0
```
