# DM `sigma_hier` H-Intrinsic No-Go Theorem

**Date:** 2026-04-20  
**Lane:** DM A-BCC sigma-chain / open import `I12`  
**Status:** no-go theorem for a named derivation family. Any `H`-intrinsic or
`mu <-> tau`-even selector family is blind to the surviving
`sigma_hier` ambiguity at the physical chamber pin.  
**Primary runner:**
`scripts/frontier_dm_sigma_hier_h_intrinsic_no_go_theorem_2026_04_20.py`

---

## 0. Question

After the chamber pin is fixed, can the remaining permutation ambiguity

```text
sigma_hier in {(2,0,1), (2,1,0)}
```

be closed by a law that lives entirely on the pinned Hermitian `H_pin`, or on
`mu <-> tau`-even scalar data built from the PMNS matrix?

## 1. Bottom line

No.

At the pinned chamber point, the eigenvector matrix `V` of `H_pin` is fixed.
The two observationally surviving PMNS candidates are

```text
P_+ = P_(2,0,1) = S_(mu tau) P_-
P_- = P_(2,1,0),
```

where `S_(mu tau)` is the `mu <-> tau` row swap.

This means:

1. both candidates come from the **same** pinned Hermitian `H_pin`;
2. any selector family built only from `H_pin` itself is automatically blind
   to the choice between them;
3. any `mu <-> tau`-even scalar family on the PMNS matrix is also blind to the
   choice, because the two candidates differ only by that row swap;
4. the Jarlskog sign flips:

```text
sin(delta_CP)(2,0,1) = - sin(delta_CP)(2,1,0).
```

So the first missing ingredient is not another `H`-intrinsic scalar. It is a
**flavor-orienting law**: something `mu <-> tau`-odd, equivalently a genuinely
oriented CP/f flavor selector.

## 2. Theorem

**Theorem (`H`-intrinsic / `mu <-> tau`-even no-go for `sigma_hier`).** Let
`H_pin` be the pinned chamber Hermitian at

```text
(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042),
```

and let `V` be its eigenvector matrix in ascending eigenvalue order. Define

```text
P_(sigma) := rowperm_sigma(V).
```

Then:

1. exactly two permutations survive the magnitude filter:
   `sigma = (2,0,1)` and `sigma = (2,1,0)`;
2. they satisfy
   `P_(2,0,1) = S_(mu tau) P_(2,1,0)`;
3. both are generated from the same `H_pin`, so every `H`-intrinsic scalar law
   takes the same value on both;
4. every `mu <-> tau`-even scalar functional of the PMNS matrix also takes the
   same value on both;
5. but their Jarlskog signs are opposite.

Therefore no selector family living entirely on `H_pin`, or on
`mu <-> tau`-even scalar PMNS data, can determine `sigma_hier`. Any genuine
closure of `I12` must add a flavor-orienting law that is odd under the
surviving row transposition.

### Proof

The surviving pair is already known from the `sigma_hier` uniqueness runner:
they are the only two permutations with all `9/9` PMNS magnitudes inside the
NuFit bands at the pin.

Their relation is immediate:

```text
(2,0,1) = (23) o (2,1,0),
```

so the corresponding PMNS matrices differ only by the `mu <-> tau` row swap.
This transposition is applied **after** diagonalizing the same `H_pin`; it is a
flavor-label ambiguity, not a new Hermitian point.

Hence every scalar of `H_pin` is identical on the two branches, because
`H_pin` itself is identical. Likewise any PMNS scalar `F(P)` satisfying
`F(S_(mu tau) P) = F(P)` is identical on the two branches.

But the Jarlskog invariant changes sign under a single row swap, so the two
branches carry opposite `sin(delta_CP)`.

Therefore an `H`-intrinsic or `mu <-> tau`-even family cannot choose between
them. QED.

## 3. Consequence for the open import

This does not close `I12` outright. It closes a family of candidate routes:

- no additional scalar of `H_pin` can fix `sigma_hier`;
- no `mu <-> tau`-even PMNS scalar can fix `sigma_hier`.

So the first law that could honestly close `I12` has to be one of:

- a flavored CP-odd orientation law,
- a charged-lepton labeling law that is not `H`-intrinsic,
- or a retained `mu <-> tau`-odd structure outside the current scalar bank.

That is the exact remaining target.

## 4. Scope

What is ruled out:

- `H`-intrinsic selector families;
- `mu <-> tau`-even scalar PMNS families.

What is not ruled out:

- a genuine flavor-orienting law;
- a CP-odd selector tied to charged-lepton labeling rather than to `H` alone.

## 5. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_sigma_hier_h_intrinsic_no_go_theorem_2026_04_20.py
```

Expected final line:

```text
PASS=11 FAIL=0
```
