# PMNS Right Polar Section Note

**Date:** 2026-04-15
**Status:** exact generic conditional theorem on intrinsic PMNS completion
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_right_polar_section.py`

## Question

After the exact right-orbit obstruction and the exact no-go for
right-conjugacy-invariant observables of `K = Y^dag Y`, does the generic
selected-branch right orbit still admit any canonical intrinsic representative
from branch Hermitian data alone?

## Bottom line

Yes, on the generic full-rank patch.

For any full-rank Yukawa matrix `Y`, let

`H = Y Y^dag`.

Then the left polar decomposition gives

`Y = H^(1/2) U_R`

with `U_R in U(3)` and unique positive Hermitian factor `H^(1/2)`.

So the generic right orbit already carries a canonical intrinsic section

`Y_+(H) := H^(1/2)`.

This does **not** contradict the right-frame orbit obstruction. That theorem
closed only the stronger claim that the **admitted raw right-Gram data**
`m_R(Y)` and `|(Y^dag Y)12|` are already intrinsic on arbitrary orbit
representatives. They are not.

What is true is narrower and useful:

- the current bank does supply a canonical **positive orbit representative**
  once the branch Hermitian data are available
- on the one-sided minimal PMNS branches, the positive-section off-diagonal
  support realizes the reduced selector class from Hermitian data
- because `Y_+` factors only through `H`, it is still sheet-even and therefore
  cannot fix the residual selected-branch `Z_2` coefficient sheet

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`
- `PMNS branch-conditioned quadratic-sheet closure`
- `PMNS branch sheet nonforcing`
- `PMNS right-frame orbit obstruction`
- `PMNS right-conjugacy-invariant no-go`

It also reuses the same orbit-bundle framing already isolated on the GR side,
but here the conclusion is different on the generic full-rank patch:

- GR universal complement: invariant core plus orbit bundle, no canonical
  complement section from the current invariant bank
- PMNS right orbit: generic full-rank branch Hermitian data do admit a unique
  positive orbit representative `H^(1/2)`

So the PMNS lane is not blocked at the same place as the GR complement lane.

## Exact positive section

If `Y` is full rank, the left polar factor

`P := (Y Y^dag)^(1/2)`

is the unique positive Hermitian matrix with `P^2 = H`.

Since `Y = P U_R`, the matrix `P` lies on the same exact right orbit as `Y`.
Therefore

`Y_+(H) := H^(1/2)`

is a canonical right-orbit representative on the generic full-rank patch.

This section depends only on `H`, so it is intrinsic once the selected-branch
Hermitian data are known.

## Selector handoff from Hermitian data

Define the positive-section support score

`s_+(H) := # { upper-triangular off-diagonal entries of H^(1/2) that are nonzero }`.

Then on the minimal PMNS classes:

- on a monomial one-offset branch, `H` is diagonal, so `H^(1/2)` is diagonal
  and `s_+(H) = 0`
- on a generic canonical two-Higgs branch, `H^(1/2)` has all three upper
  off-diagonal entries nonzero, so `s_+(H) = 3`

Therefore the intrinsic Hermitian selector

`a_pol(H_nu, H_e) := s_+(H_nu) - s_+(H_e)`

realizes the reduced branch class on the universal and one-sided minimal patch:

`(U1, U2, N_nu, N_e) -> (0, 0, +3, -3)`.

Up to positive normalization, this is the same reduced selector class that the
earlier packet compressed to one one-dimensional slot.

So once the branch Hermitian data are derived, the active one-sided branch is
already intrinsically visible. No extra right-frame law is needed just to read
that branch from `H`.

## Sheet-even boundary

The positive section still factors only through `H`.

But the exact branch-sheet nonforcing theorem already proves that the two
selected-branch coefficient sheets are distinct Yukawa data with the **same**
Hermitian matrix `H`.

So the positive polar section is identical on both sheets.

Therefore:

- the positive section helps with the branch-orientation side once `H` is
  known
- it does **not** fix the residual canonical-sheet bit

That remaining bit still requires a genuinely non-Hermitian or otherwise
right-sensitive datum beyond `H`.

## Theorem-level statement

**Theorem (Generic polar section on the PMNS right orbit, with selector but not
sheet closure).** Assume the exact selected-branch Hermitian inverse-problem
theorems, the exact PMNS right-frame orbit obstruction theorem, the exact PMNS
right-conjugacy-invariant no-go theorem, and the exact PMNS branch sheet
nonforcing theorem. Then on the generic full-rank selected-branch patch:

1. every right orbit `Y -> Y U_R^dag` admits a unique positive Hermitian
   representative
   `Y_+(H) = H^(1/2)`, depending only on `H = Y Y^dag`
2. on the minimal one-sided PMNS classes, the positive-section support score
   `s_+(H)` realizes the reduced branch selector intrinsically from the
   Hermitian data
3. because `Y_+` factors through `H`, it is identical on the two residual
   selected-branch coefficient sheets and therefore cannot fix the residual
   `Z_2` sheet

So the current frontier sharpens again:

- once branch Hermitian data are available, the branch side is intrinsically
  readable from them
- the remaining post-Hermitian datum is the residual non-Hermitian/right-sensitive
  sheet-fixing information

## What this closes

This closes an important ambiguity in the previous endpoint.

It is now exact that:

- the PMNS right-orbit obstruction is **not** a total no-section theorem
- the generic full-rank right orbit already has a canonical positive section
  from `H`
- the remaining exact PMNS gap is therefore sharper than “find any right-frame
  law”
- if the goal is PMNS/intrinsic branch closure, the real missing object is the
  branch Hermitian data law
- if the goal is canonical coefficient-sheet closure, one extra non-Hermitian
  or right-sensitive datum is still needed

## What this does not close

This note does **not** derive:

- the selected-branch Hermitian data themselves from the axiom bank
- the residual selected-branch `Z_2` coefficient sheet
- the full canonical two-Higgs coefficients as current-bank outputs
- a derivation of the two-Higgs extension itself

So it does not yet upgrade the neutrino lane to full positive coefficient
closure. It removes the generic right-frame ambiguity on the full-rank
Hermitian patch and isolates the truly remaining datum.

## Command

```bash
python3 scripts/frontier_pmns_right_polar_section.py
```
