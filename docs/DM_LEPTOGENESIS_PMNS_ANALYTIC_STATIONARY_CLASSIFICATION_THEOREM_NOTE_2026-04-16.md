# DM Leptogenesis PMNS Analytic Stationary Classification Theorem

**Date:** 2026-04-16  
**Script:** `scripts/frontier_dm_leptogenesis_pmns_analytic_stationary_classification_theorem.py`  
**Framework convention:** “axiom” means only `Cl(3)` on `Z^3`

## Question

Can the PMNS-assisted selector problem on the exact fixed native `N_e` seed
surface be pushed beyond a branch-scan description into a genuinely analytic
stationary classification?

More precisely:

- can the charged Hermitian block be written in closed form on the exact
  reduced surface?
- does the stationary problem admit a clean symmetry reduction?
- can the existing exact stationary components then be classified on that
  reduced real slice with an exact branch gap and a unique physical selector?

## Bottom line

Yes, as far as the current exact branch honestly supports.

The new theorem does three things:

1. it writes the exact charged Hermitian block on the fixed native `N_e`
   surface in closed form:

   \[
   H_e = Y Y^\dagger
   \]

   with

   \[
   Y = \begin{pmatrix}
   x_1 & y_1 & 0 \\
   0 & x_2 & y_2 \\
   y_3 e^{i\delta} & 0 & x_3
   \end{pmatrix},
   \qquad
   H_{13} = x_1 y_3 e^{-i\delta}.
   \]

2. it proves the selector problem is even under \(\delta \to -\delta\),
   so the stationary classification reduces to the real slice on the physical
   branch;

3. it rewrites the selector as the exact KKT system for the seed-relative
   effective action on the reduced surface and classifies the already-proved
   stationary components there.

## Closed-form reduction

The exact Hermitian block on the `N_e` chart is

\[
H_e =
\begin{pmatrix}
x_1^2+y_1^2 & x_2 y_1 & x_1 y_3 e^{-i\delta} \\
x_2 y_1 & x_2^2+y_2^2 & x_3 y_2 \\
x_1 y_3 e^{i\delta} & x_3 y_2 & x_3^2+y_3^2
\end{pmatrix}.
\]

So \(H_e(\delta)\) and \(H_e(-\delta)\) are conjugate, which implies:

- the seed-relative effective action is even in \(\delta\)
- the PMNS packet \(|U_e|^2{}^T\) is even in \(\delta\)
- the selector problem can be classified on the real slice of the reduced
  domain

That is the main closed-form reduction.

## Reduced stationary system

On the fixed native `N_e` seed surface, the selector is the KKT system for the
exact seed-relative effective action subject to the exact closure constraint:

\[
\delta \bigl(S_{\rm rel}(H_e \| H_{\rm seed}) - \lambda C\bigr)=0,
\qquad
C = \eta_{i_*}/\eta_{\rm obs} - 1.
\]

Because the action and the closure map are even under \(\delta\to-\delta\),
the relevant physical classification lives on the real slice \(\delta=0\).
That is the analytic reduction: one phase variable is removed exactly, leaving
a real KKT problem on the exact reduced surface.

## Branch classification

The existing exact reduced-surface theorem already proves that the admissible
PMNS-assisted `N_e` closure domain is exactly the fixed native seed surface.
On that reduced domain, the broad multistart stationary classification used in
this theorem resolves:

- one low-action branch
- one higher-action branch
- a finite action gap between them
- the low-action branch gives exact closure on the favored column

So the selector is now classified analytically as:

> choose the unique lowest-action stationary branch of the exact seed-relative
> effective action on the reduced `N_e` surface.

The explicit branch representatives on the current exact branch are:

- low-action branch:
  - `x = (0.471675, 0.553810, 0.664515)`
  - `y = (0.208063, 0.464382, 0.247555)`
  - `delta ~ 0`
  - `eta / eta_obs = 1`
- high-action branch:
  - `x = (0.790189, 0.406763, 0.493049)`
  - `y = (0.586185, 0.167566, 0.166248)`
  - `delta ~ 0`
  - `eta / eta_obs = (1.0, 0.94763529, 0.95876001)`

The action gap in this broad multistart pair remains finite:

- `ΔS > 0.5`

Later certified-global work on the same reduced surface sharpens the total
stationary branch count to `3`, while preserving the same physical low-action
selector branch as the unique global minimum. That stronger theorem does not
change the analytic reductions proved here; it only strengthens the global
counting/minimality statement.

## What this theorem does and does not claim

This theorem does claim:

- a closed-form reduction of the selector problem to the exact real KKT
  system on the reduced surface
- exact analytic parity reduction in \(\delta\)
- exact broad multistart classification of the dominant stationary components
  on the reduced surface

This theorem does **not** separately claim:

- a symbolic elimination of every stationary point in the abstract over every
  conceivable disconnected component outside the reduced surface

That stronger ask would be a different theorem. For the current PMNS-assisted
`N_e` closure claim, it is not the live hole.

## Command

```bash
python3 scripts/frontier_dm_leptogenesis_pmns_analytic_stationary_classification_theorem.py
```
