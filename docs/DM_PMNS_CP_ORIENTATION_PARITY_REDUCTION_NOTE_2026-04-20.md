# DM PMNS CP-Orientation Parity Reduction

**Date:** 2026-04-20  
**Lane:** DM A-BCC sigma-chain / open imports `I12` and `I5`  
**Status:** new exact reduction theorem plus a named-family no-go. The
remaining gap is not another source-side CP-odd scalar; it is exactly the
parity / charged-doublet label law for `sigma_hier`.  
**Primary runner:**  
`scripts/frontier_dm_pmns_cp_orientation_parity_reduction_2026_04_20.py`

---

## 0. Question

After the chamber `chi^2 = 0` set is reduced to

```text
{Basin 1, Basin 2, Basin X},
```

what is the exact remaining difference between:

- source-side CP orientation on the DM Hermitian family, and
- the physical PMNS CP sign / `sigma_hier` choice?

## 1. Bottom line

The gap is exactly one parity bit.

Define the source cubic orientation

```text
I_src(H) := Im(H_12 H_23 H_31).
```

For the ascending-eigenvalue basis `V` of `H`, with
`lambda_1 < lambda_2 < lambda_3`, one has the exact identity

```text
J_basis
= Im(V_11 V_22 V_12^* V_21^*)
= I_src(H) / ((lambda_1 - lambda_2)(lambda_2 - lambda_3)(lambda_3 - lambda_1)).
```

If `P_sigma = rowperm_sigma(V)`, then

```text
J_sigma = parity(sigma) * J_basis.
```

So the physical PMNS CP sign differs from the source CP orientation only by
`parity(sigma_hier)`.

That means:

1. the source family already carries an exact CP-oriented cubic scalar;
2. source-side CP-odd data by themselves are still blind to the
   `mu <-> tau` relabeling;
3. the remaining missing law for `I12`, and for the sign half of `I5`, is
   exactly the parity / charged-doublet label law on `sigma_hier`.

## 2. Theorem

**Theorem (source cubic parity reduction).** On the chamber roots

```text
Basin 1, Basin 2, Basin X,
```

let `H` be the DM Hermitian, `V` its ascending-eigenvalue eigenbasis, and
`P_sigma` any row permutation of `V`. Then:

1. `I_src(H) = Im(H_12 H_23 H_31)` is an exact source-side CP-oriented scalar;
2. the ascending-basis Jarlskog is exactly

   ```text
   J_basis = I_src(H) / Delta,
   Delta := (lambda_1 - lambda_2)(lambda_2 - lambda_3)(lambda_3 - lambda_1) > 0;
   ```

3. for any row permutation `sigma`,

   ```text
   J_sigma = parity(sigma) * I_src(H) / Delta;
   ```

4. at the same pinned Hermitian `H_pin`, the two surviving permutations
   `(2,1,0)` and `(2,0,1)` therefore give opposite PMNS CP signs while sharing
   the same source cubic orientation.

Therefore no source-side CP-odd scalar law of this cubic orientation type can
close `sigma_hier` by itself. The remaining missing ingredient is the parity /
charged-doublet label law on `sigma_hier`.

### Proof

The identity

```text
Im(H_12 H_23 H_31) = J_basis prod_{i<j}(lambda_i - lambda_j)
```

is the standard one-Hermitian Jarlskog bridge in the charged-lepton diagonal
basis. Since the runner orders eigenvalues ascending,

```text
Delta = (lambda_1 - lambda_2)(lambda_2 - lambda_3)(lambda_3 - lambda_1) > 0.
```

So `J_basis = I_src / Delta`.

A row permutation multiplies the Jarlskog by the sign of that permutation, so
`J_sigma = parity(sigma) J_basis`. Combining the two gives the displayed
formula.

At the physical pin, `(2,1,0)` and `(2,0,1)` differ by one `mu <-> tau`
transposition, hence have opposite parity, hence opposite CP sign, while
`I_src(H_pin)` is unchanged because `H_pin` itself is unchanged.

QED.

## 3. Chamber sign table

On the exact chamber roots from the chamber-completeness theorem:

| Root | `I_src(H)` | `J_(2,1,0)` | `J_(2,0,1)` |
|---|---:|---:|---:|
| Basin 1 | `+0.30356` | `−0.03275` | `+0.03275` |
| Basin 2 | `−225.76` | `+0.01839` | `−0.01839` |
| Basin X | `−99.77` | `+0.01389` | `−0.01389` |

So:

- on the odd branch `sigma = (2,1,0)`, the coefficient-free source law
  `I_src > 0` selects Basin 1 uniquely;
- on the even branch `sigma = (2,0,1)`, no chamber root has `I_src > 0`.

This is the exact reduction:

> once the parity bit is fixed, the source cubic sign immediately selects the
> physical chamber root and the sign of `sin(delta_CP)`.

## 4. Consequence for `I12` and `I5`

This does not close `I12` outright. It does sharpen it substantially.

What is now closed negatively:

- another source-side CP-odd scalar will **not** fix `sigma_hier`;
- the remaining sign ambiguity is **not** in the source cubic orientation.

What remains:

- a parity / charged-doublet label law telling us whether the physical branch
  is `sigma = (2,1,0)` or `sigma = (2,0,1)`.

For `I5`, the sign half is now reduced to exactly the same missing primitive.
The angle triple itself remains observational on this branch.

## 5. Honest verdict

This note supplies a real theory gain:

- source-side CP orientation is exact,
- chamber completeness is exact,
- the remaining miss is one explicit parity law.

So the `I12` / `I5` boundary is no longer “derive PMNS CP somehow.” It is:

```text
derive the charge-sign / hierarchy-parity map on the surviving Z_3 doublet.
```

## 6. Reproduction

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_pmns_cp_orientation_parity_reduction_2026_04_20.py
```

Expected final line:

```text
PASS=16  FAIL=0
```
