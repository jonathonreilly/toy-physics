# PMNS Triplet-Pair Closure Program

**Date:** 2026-04-15  
**Status:** exact downstream closure program  
**Script:** `scripts/frontier_pmns_triplet_pair_closure_program.py`

## Question

Once the PMNS-relevant microscopic triplet pair

- `D_0^trip` on `E_nu`
- `D_-^trip` on `E_e`

is supplied, can the remaining full neutrino closure data be solved exactly?

## Bottom line

Yes.

On the one-sided minimal PMNS classes, the closure problem below the triplet
pair is algorithmically exact.

The program does five things:

1. identifies the realized branch
2. reads the passive monomial offset `q` and coefficients `a_i`
3. canonicalizes the active two-Higgs operator to `A + B C`
4. reconstructs the two Hermitian quadratic sheets
5. fixes the realized sheet from the microscopic active operator itself

So once `(D_0^trip, D_-^trip)` are known, the remaining branch/coefficient/sheet
data are no longer an open conceptual problem.

## Exact program content

### 1. Branch detection

The solver checks which sector is:

- monomial `diag(a_i) P_q`
- active two-Higgs `A + B C`.

That identifies:

- neutrino-active branch, or
- charged-lepton-active branch.

### 2. Passive monomial solve

On the passive sector the solver reads:

- the exact offset `q`
- the coefficient triple `a_1,a_2,a_3`.

### 3. Active canonical solve

On the active sector the solver:

- generation-relabels into the canonical support class
- performs the exact phase reduction
- returns the canonical coefficients
  `x_1,x_2,x_3,y_1,y_2,y_3,delta`.

### 4. Sheet solve

From the active Hermitian data it reconstructs the two exact quadratic sheets.
The microscopic active operator then picks which one is realized.

### 5. End-to-end conclusion

Therefore the remaining unresolved science is not a downstream PMNS closure
program anymore. It is only the derivation of `(D_0^trip,D_-^trip)` from
`Cl(3)` on `Z^3`.

## Solver mode

The script is also a usable solver, not only a theorem harness.

Given a JSON file containing

- `D0_trip`
- `Dm_trip`

as `3 x 3` matrices, it returns:

- the realized one-sided branch
- the passive monomial offset and coefficients
- the active canonical two-Higgs coefficients
- the residual sheet index and both quadratic candidates

Accepted matrix-entry formats are:

- real numbers
- Python-style complex strings
- `[re, im]`
- `{"re": ..., "im": ...}`

### Example

```json
{
  "D0_trip": [
    [[0.9, 0.0], [0.3, 0.0], [0.0, 0.0]],
    [[0.0, 0.0], [1.2, 0.0], [0.5, 0.0]],
    [[0.325873, 0.232676], [0.0, 0.0], [1.1, 0.0]]
  ],
  "Dm_trip": [
    [[0.0, 0.0], [0.0, 0.0], [0.07, 0.0]],
    [[0.11, 0.0], [0.0, 0.0], [0.0, 0.0]],
    [[0.0, 0.0], [0.23, 0.0], [0.0, 0.0]]
  ]
}
```

## Boundary

This note does **not** claim that the triplet pair itself is already derived
from `Cl(3)` on `Z^3`.

It proves a narrower exact statement:

> once the triplet pair is supplied, the remaining closure data are solved.

## What this changes

Before this program, the remaining target still looked like:

- derive branch
- derive active coefficients
- derive passive coefficients
- derive sheet

After this program, those are no longer separate science objects below the
triplet pair. They are exact outputs of the solver.

So the remaining science target is now as small as it can honestly get:

- derive the triplet pair itself from `Cl(3)` on `Z^3`.

## Command

```bash
python3 scripts/frontier_pmns_triplet_pair_closure_program.py
```

```bash
python3 scripts/frontier_pmns_triplet_pair_closure_program.py --input triplet_pair.json --pretty
```
