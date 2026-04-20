# DM PMNS Asymptotic Pure-Source No-Go

**Date:** 2026-04-20  
**Lane:** DM A-BCC basin enumeration / open import `I11`  
**Status:** new no-go theorem for the unbounded-basin family. Exact `chi^2 = 0`
PMNS basins cannot escape to infinity on the pure-source chamber directions.  
**Primary runner:**
`scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py`

---

## 0. Question

The open-import register still flags basin exhaustiveness:

```text
{Basin 1, Basin N, Basin P, Basin X}
```

as empirical rather than structural. The first unresolved loophole is obvious:
could there be additional exact `chi^2 = 0` basins arbitrarily far out in the
active chamber?

This note closes that loophole.

## 1. Bottom line

No.

If a sequence of exact PMNS-fit source points escaped to infinity, then after
dividing by its norm the affine Hermitian family would converge to the
pure-source real-symmetric family

```text
J(m, delta, q_+) = m T_m + delta T_delta + q_+ T_q.
```

So any basin at infinity would have to be realized by a **real orthogonal**
PMNS matrix with the target angles.

For each row permutation and each real CP branch `delta_CP = 0, pi`, write

```text
J = U diag(lambda_1, lambda_2, lambda_3) U^T,
```

with `U` the corresponding real orthogonal PMNS matrix. Membership in the
three-parameter pure-source family imposes exactly the linear constraints

```text
J_22 + J_33 = 0,
J_13 - J_12 - 2 J_22 = 0,
2 J_11 - 2 J_23 + J_12 + J_13 = 0.
```

These become a `3 x 3` homogeneous linear system

```text
A_(perm,delta_CP) lambda = 0.
```

The runner verifies that for all six row permutations and both real CP branches
the matrix `A_(perm,delta_CP)` has full rank. Therefore the only solution is

```text
lambda_1 = lambda_2 = lambda_3 = 0,
```

which is not a physical asymptotic source direction.

So no exact `chi^2 = 0` PMNS fit exists at infinity.

## 2. Theorem

**Theorem (asymptotic pure-source no-go).** Fix the target angle triple

```text
(s12^2, s13^2, s23^2) = (0.307, 0.0218, 0.545).
```

Assume there exists an unbounded sequence of exact PMNS-fit points on the
affine source family

```text
H = H_base + m T_m + delta T_delta + q_+ T_q.
```

Then after dividing by the Euclidean norm of `(m, delta, q_+)` and taking a
convergent subsequence, one obtains a nonzero pure-source matrix

```text
J = m T_m + delta T_delta + q_+ T_q
```

whose PMNS angles equal the target angles.

But `J` is real symmetric, so its diagonalizing matrix is real orthogonal. For
every real-orthogonal PMNS matrix with the target angles, the pure-source
family constraints reduce to a full-rank homogeneous linear system in the three
eigenvalues. Hence the only solution is the zero matrix.

Therefore no such nonzero `J` exists, and no exact PMNS-fit basin can escape to
infinity. QED.

## 3. Consequence for basin completeness

This does **not** yet give full compact-region completeness. It does give the
first structural reduction the open register was missing:

- the remaining basin-completeness problem is now compact;
- any additional exact basin would have to live in a finite-radius region;
- the old loophole "maybe there are more exact basins arbitrarily far out" is
  gone.

So `I11` is reduced from

```text
global completeness
```

to

```text
compact-basin completeness.
```

## 4. Numeric corroboration

The same runner also performs a chamber-sphere minimization on the pure-source
family and finds a strictly positive asymptotic floor:

```text
chi^2_inf >= 1.0e-3
```

across the tested chamber directions and row permutations. That numeric floor
is corroborating evidence for the theorem-level linear-algebra no-go above.

## 5. Scope

What is closed:

- the unbounded pure-source basin family;
- the infinity-tail loophole in `I11`.

What remains open:

- a compact-region completeness theorem ruling out additional bounded basins.

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_asymptotic_source_no_go_2026_04_20.py
```

Expected final line:

```text
PASS=26 FAIL=0
```
