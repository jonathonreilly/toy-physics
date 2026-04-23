# PMNS Intrinsic Completion Boundary

**Date:** 2026-04-15
**Status:** exact current-bank boundary theorem on intrinsic PMNS completion
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_pmns_intrinsic_completion_boundary.py`

## Question

After the current bank:

- isolates the minimal PMNS-producing branches
- proves the selected-branch Hermitian inverse problems are exact
- identifies admitted right-Gram completion routes
- and proves those right-Gram data are not yet intrinsic on the retained bank

what exactly remains between the current package and **intrinsic full PMNS /
neutrino closure**?

## Bottom line

The remaining gap is no longer a branch-local inverse-problem gap.

The current bank already gives:

- exact local closure targets for `H_nu` on the neutrino-side minimal branch
- exact local closure targets for `H_e` on the charged-lepton-side minimal
  branch
- exact algebraic selected-branch coefficient closure up to one residual
  `Z_2` sheet
- on the generic full-rank selected-branch patch, the canonical positive
  right-orbit representative `Y_+(H) = H^(1/2)`

But it does **not** yet give:

- the branch Hermitian data themselves as axiom-side outputs
- a retained law producing those branch Hermitian data from the axiom bank
- the residual selected-branch `Z_2` sheet as a retained-bank output

So the minimal missing intrinsic object is now sharp:

> the selected branch’s Hermitian data law, together with one genuinely
> non-Hermitian or otherwise right-sensitive sheet-fixing datum if canonical
> coefficient-sheet closure is required.

And the new no-go theorem sharpens one tempting escape hatch:

- no right-conjugacy-invariant observable of `K = Y^dag Y` can intrinsicize
  the admitted right-Gram route either

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs observable inverse problem`
- `PMNS branch-conditioned quadratic-sheet closure`
- `PMNS selector minimal microscopic extension`
- `PMNS selector current-stack zero law`
- `PMNS right-frame orbit obstruction`
- `PMNS right-conjugacy-invariant no-go`
- `PMNS right polar section`

It also uses the same structural pattern already isolated on the GR side:

- `Universal GR A1 invariant section`
- `Universal GR invariant-frame obstruction`

As on the GR lane, the current bank gives an invariant core but not the full
intrinsic complementary frame data needed for positive closure.

One new conditional refinement now sharpens the Hermitian side:

- `PMNS global Hermitian mode package`
- `PMNS EWSB residual-Z2 Hermitian core`
- `PMNS EWSB weak-axis Z3 seed`
- `PMNS EWSB weak-axis seed coefficient closure`

If the active one-sided PMNS branch is aligned with the exact weak-axis EWSB
selection, then the active Hermitian law is no longer a generic seven-real
object. It reduces to the four-real-parameter core
`[[a,b,b],[b,c,d],[b,d,c]]`, with the passive monomial sector staying
diagonal, and the generic active branch splitting into that exact core plus
three explicit symmetry-breaking slots. The current bank still does not derive
that alignment itself or the breaking slots, so this is a conditional
refinement rather than a full closure.

Inside that aligned surface, the current bank already derives one concrete
two-parameter Hermitian seed from the exact weak-axis `1+2` split:
the weak-axis seed `diag(A,B,B)` lifts through the canonical `Z_3` bridge to
the even-circulant seed `mu I + nu(C+C^2)`. On the canonical active Yukawa
chart this seed is realized if and only if `A <= 4B`, and when realized it is
forced onto the unique symmetric active slice `Y=xI+yC`.

One new boundary theorem then closes the status question:

- `PMNS EWSB alignment nonforcing`

The current retained bank still does **not** force the active one-sided PMNS
branch onto that aligned submanifold. Full-rank aligned and non-aligned points
coexist on the same canonical active branch while satisfying the current
support and Hermitian inverse-problem conditions. So the aligned core remains
an exact conditional sharpening, not a current-bank selection.

## Why this is stronger than the last-mile reduction note

The last-mile reduction note already reduced the remaining problem to:

- a selector question
- a selected-branch coefficient problem

This note sharpens that one step further.

It says the selected-branch coefficient problem is **not** the real remaining
bank-level obstruction. The real obstruction is now the production of the
branch Hermitian data themselves, plus one residual post-Hermitian sheet datum
if canonical coefficient closure is the target:

- the branch Hermitian inverse problems are exact once a branch is selected
- the global active Hermitian target is exactly a `2 + 2 + 3` package:
  one real aligned core, equivalently weak-axis seed pair plus aligned
  deformations, together with the exact breaking triplet
  `(delta,rho,gamma)`
- and on the EWSB-aligned one-sided branch, the active Hermitian law already
  collapses to a four-real core plus three explicit breaking slots
- the generic full-rank right orbit already has the canonical positive section
  `Y_+(H) = H^(1/2)`
- so once the branch Hermitian data are known, the one-sided branch becomes
  intrinsically readable from `H`
- but the positive section still factors through `H`, so it cannot fix the
  residual coefficient sheet
- and on the compatible weak-axis seed patch that residual coefficient problem
  already collapses to one explicit exchange sheet `x <-> y`, with even
  right-Gram data collapsing there as well; on that patch the remaining
  selector is exactly the restricted Higgs-offset / monomial-edge selector on
  the canonical `(0,1)` pair

So the finish line is no longer “derive seven more numbers” in the abstract.
It is “derive the selected-branch Hermitian data law, and if canonical
two-Higgs coefficients are needed, one extra sheet-fixing datum beyond `H`.”

## Theorem-level statement

**Theorem (Current bank boundary for intrinsic PMNS completion).** Assume:

1. the exact selected-branch local inverse-problem theorem for `H_nu`
2. the exact selected-branch local inverse-problem theorem for `H_e`
3. the exact branch-conditioned quadratic-sheet closure theorem
4. the exact PMNS selector minimal microscopic extension theorem
5. the exact PMNS selector current-stack zero law
6. the exact PMNS right-frame orbit obstruction theorem
7. the exact PMNS right-conjugacy-invariant no-go theorem
8. the exact PMNS right polar section theorem
9. the exact PMNS EWSB residual-Z2 Hermitian core theorem

Then:

1. on either selected minimal PMNS branch, the Hermitian branch data are exact
   local closure targets and the coefficient problem is explicit up to one
   residual `Z_2` sheet
2. on the generic full-rank patch, the exact right polar section theorem gives
   the canonical positive representative `Y_+(H) = H^(1/2)`, so once
   branch Hermitian data are known the one-sided branch is intrinsically
   readable from `H`
3. under the explicit EWSB-alignment bridge condition, the active Hermitian
   data law sharpens further to a four-real residual-`Z_2` core plus three
   explicit breaking slots, with the passive monomial sector diagonal
4. inside that aligned surface, the current bank already derives one concrete
   two-parameter weak-axis Hermitian seed
5. on the compatible weak-axis seed patch, the coefficient side already
   collapses to one explicit exchange sheet `x <-> y`, and even right-Gram
   data collapse there too; the remaining object on that patch is exactly the
   restricted Higgs-offset / monomial-edge selector on the canonical `(0,1)`
   pair
6. the current retained bank does not force that EWSB alignment and does not
   yet derive the generic breaking-slot vector away from the aligned core
7. on the aligned surface itself, that four-real core is already exactly one
   `2 + 1` spectral primitive package
   `(lambda_+, lambda_-, lambda_odd, theta_even)`
8. the current retained bank still does not produce those branch Hermitian
   data as axiom-side outputs, and because the polar section factors through
   `H` it cannot fix the residual `Z_2` coefficient sheet either
9. therefore the remaining exact gap to intrinsic PMNS completion is not
   another local inverse-problem reduction, but the derivation of:
   - the selected branch Hermitian data as axiom-side outputs
   - and, for coefficient-level closure, one genuinely non-Hermitian or
     otherwise right-sensitive sheet-fixing datum

So the strongest exact endpoint is:

- selected-branch Hermitian closure is exact but conditional
- the generic right-orbit ambiguity is resolved by the positive polar section
- intrinsic full PMNS completion remains open at the Hermitian-data law layer
- coefficient-level closure remains open at one residual sheet-fixing datum

## What this closes

This closes the planning ambiguity around the post-agent search.

It is now exact that:

- the branch Hermitian data are not the vague part anymore
- the admitted right-Gram route is not the vague part anymore
- the generic right-frame issue is no longer the vague part either
- the remaining science is concentrated in the Hermitian-data law, including
  the weak-axis-derived aligned seed, the aligned `2 + 1` spectral primitive
  package, the generic active breaking-slot law away from that aligned
  surface, and the residual post-Hermitian sheet datum

## What this does not close

This note does **not** derive:

- the selected branch Hermitian data themselves
- the two aligned deformation directions away from the weak-axis seed
- the aligned spectral primitive values
  `(lambda_+, lambda_-, lambda_odd, theta_even)`
- the generic active breaking-slot vector as an axiom-side output
- the residual selected-branch `Z_2` coefficient sheet
- the selected-branch coefficients as current-bank outputs

So it does not upgrade the package to positive full neutrino closure.

## Command

```bash
python3 scripts/frontier_pmns_intrinsic_completion_boundary.py
```
