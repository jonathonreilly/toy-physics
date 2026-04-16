# PMNS Microscopic `ΔD` Generic Underdetermination

**Date:** 2026-04-15  
**Script:** `scripts/frontier_pmns_microscopic_delta_d_generic_underdetermination.py`  
**Status:** exact current-bank underdetermination theorem for generic off-seed microscopic `ΔD`

## Question

After deriving the native free microscopic core

`D_free|_{E_nu \oplus E_e} = I_6`

and reducing the PMNS-relevant microscopic deformation to the exact channel
carrier

`ΔD = U + V C + W C^2`,

does the current retained `Cl(3)` on `Z^3` bank determine the **generic
off-seed** values of `ΔD`?

## Answer

No.

On a fixed one-sided minimal PMNS branch with passive monomial lane held fixed,
the active microscopic deformation is already the exact `7`-real family

`ΔD_act(x,y,delta)
 = diag(x_1-1, x_2-1, x_3-1)
 + diag(y_1, y_2, y_3 e^{i delta}) C`.

That family has local real rank `7` at a generic point on the fixed canonical
support class.

The exact weak-axis seed patch is only the codimension-`5` slice

- `x_1 = x_2 = x_3`
- `y_1 = y_2 = y_3`
- `delta = 0`

and that seed slice is already positively closed by the separate seed-law
theorem.

Away from that slice, the current retained bank does not fix the values.

## Strong form

Two distinct generic off-seed points on the same retained neutrino-active
class can be embedded into full charge-preserving microscopic operators

`D^(A), D^(B)`

with all of the same exact structural data:

- same retained lepton supports `E_nu, E_e`
- same charge-preserving block form
- same passive monomial lane
- same canonical active support class `I + C`

but with different active Schur targets and therefore different generic
off-seed deformations

`ΔD^(A) != ΔD^(B)`.

So the current retained bank fixes the **carrier** of `ΔD`, but not its
generic off-seed **values**.

## Exact boundary

What is already closed:

- the native free microscopic core: `D_free = I`
- the exact charge-sector Schur localization
- the retained triplet entry patterns
- the aligned weak-axis seed patch

What is **not** closed by the current retained bank:

- the generic off-seed active `7`-real values of `ΔD`

Therefore the honest endpoint is:

**full positive neutrino closure is not available from the retained bank unless
a new derived value law from `Cl(3)` on `Z^3` is added.**

## Verification

```bash
python3 scripts/frontier_pmns_microscopic_delta_d_generic_underdetermination.py
```

Expected:

```text
PASS=18  FAIL=0
```
