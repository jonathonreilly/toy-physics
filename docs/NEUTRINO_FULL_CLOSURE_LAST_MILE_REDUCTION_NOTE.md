# Full Neutrino Closure: Last-Mile Reduction

**Date:** 2026-04-15  
**Status:** exact current-bank reduction theorem on the remaining full-neutrino
closure gap under the minimal-branch assumption  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_neutrino_full_closure_last_mile_reduction.py`

## Question

After the retained Majorana lane is closed negatively and the exact minimal
PMNS-producing branches are isolated, what exactly remains between the current
exact bank and **full neutrino closure**?

## Bottom line

The remaining gap is no longer a generic flavor problem.

On the minimal-branch assumption, it is branch-conditioned:

- **neutrino-side minimal branch:** `7` real quantities
- **charged-lepton-side minimal branch:** `3` neutrino Dirac mass moduli plus
  `7` charged-lepton-branch quantities

and the current atlas does **not** yet select the branch.

So the last mile has been reduced to:

- one discrete selector question
- plus, on the selected branch, an explicit algebraic reconstruction problem
- with one residual `Z_2` sheet on the selected two-Higgs branch

## Atlas and axiom inputs

This theorem reuses:

- `Neutrino mass reduction to Dirac lane`
- `Neutrino Dirac two-Higgs canonical reduction`
- `Neutrino Dirac two-Higgs observable inverse problem`
- `Charged-lepton two-Higgs canonical reduction`
- `Charged-lepton two-Higgs observable inverse problem`
- `PMNS minimal-branch nonselection`
- `Lepton shared-Higgs universality underdetermination`
- `PMNS sector-orientation orbit reduction`
- `PMNS sector-exchange nonforcing`
- `PMNS scalar bridge nonrealization`
- `PMNS selector sector-odd reduction`
- `PMNS selector non-universal support reduction`
- `PMNS selector class-space uniqueness`
- `PMNS selector unique amplitude slot`
- `PMNS selector current-stack zero law`
- `PMNS selector sign-to-branch reduction`
- `PMNS selector minimal microscopic extension`
- `PMNS branch-conditioned quadratic-sheet closure`
- `PMNS right-Gram selector realization`
- `PMNS right-Gram sheet fixing`
- `PMNS right-frame orbit obstruction`
- `PMNS intrinsic completion boundary`

The branch-conditioned count here should be read together with the companions
[LEPTON_SHARED_HIGGS_UNIVERSALITY_COLLAPSE_NOTE.md](./LEPTON_SHARED_HIGGS_UNIVERSALITY_COLLAPSE_NOTE.md):
the present piecewise `7` versus `3+7` reduction is the honest current-bank
endpoint while the sector-choice split remains available, but a future
shared-Higgs universality theorem would collapse that side-choice bit rather
than choose one side.

[LEPTON_SHARED_HIGGS_UNIVERSALITY_UNDERDETERMINATION_NOTE.md](./LEPTON_SHARED_HIGGS_UNIVERSALITY_UNDERDETERMINATION_NOTE.md):
the current retained stack does not yet force shared-Higgs universality and
does not force its failure, so the piecewise last-mile count remains the
honest exact endpoint rather than an artifact of incomplete bookkeeping.

[PMNS_SECTOR_ORIENTATION_ORBIT_NOTE.md](./PMNS_SECTOR_ORIENTATION_ORBIT_NOTE.md):
on the non-universal one-sided surface, the unordered core is already fixed as
`{single-offset monomial lane, two-offset canonical lane}`, and the residual
discrete freedom is exactly one sector-orientation bit choosing whether the
two-Higgs lane sits on `Y_nu` or on `Y_e`.

[PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md](./PMNS_SECTOR_EXCHANGE_NONFORCING_NOTE.md):
that remaining bit is not forceable by the current support-side bank, because
the reduced one-sided surface has an exact sector-exchange involution and the
retained descriptors are invariant under it.

[PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md](./PMNS_SCALAR_BRIDGE_NONREALIZATION_NOTE.md):
the current additive scalar observable grammar is also block-local on the
lepton surface and does not generate a mixed scalar bridge selecting the active
sector.

[PMNS_SELECTOR_SECTOR_ODD_REDUCTION_NOTE.md](./PMNS_SELECTOR_SECTOR_ODD_REDUCTION_NOTE.md):
any future branch-distinguishing selector can be reduced to its sector-odd part
under the exact sector exchange, so the minimal missing object is now sharpened
to a nonzero sector-odd mixed bridge functional.

[PMNS_SELECTOR_NONUNIVERSAL_SUPPORT_REDUCTION_NOTE.md](./PMNS_SELECTOR_NONUNIVERSAL_SUPPORT_REDUCTION_NOTE.md):
the universal one-offset and two-offset classes are fixed under the exact
sector exchange, so any future sector-odd selector vanishes there. The missing
object is therefore supported only on the non-universal locus: it must detect
universality failure and orient it.

[PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md](./PMNS_SELECTOR_CLASS_SPACE_UNIQUENESS_NOTE.md):
once parity and support are fixed, the reduced class-level selector space is
one-dimensional, spanned by the signed non-universality indicator
`chi_N_nu - chi_N_e`. So the remaining selector gap is not a search over
multiple reduced branch-class shapes, but the microscopic realization of one
unique reduced selector class up to scale.

[PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md](./PMNS_SELECTOR_UNIQUE_AMPLITUDE_SLOT_NOTE.md):
that unique reduced selector class carries one real amplitude `a_sel`, so the
microscopic bridge problem is now an amplitude-law question rather than a
family-search over reduced selector classes.

[PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md](./PMNS_SELECTOR_CURRENT_STACK_ZERO_LAW_NOTE.md):
on the currently retained support-plus-scalar bank, that unique reduced
selector amplitude obeys the exact present-tense law `a_sel,current = 0`.

[PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md](./PMNS_SELECTOR_SIGN_TO_BRANCH_REDUCTION_NOTE.md):
if a future microscopic bridge realizes `a_sel != 0`, then `sign(a_sel)`
selects the branch and the remaining neutrino problem becomes exactly the
branch-conditioned coefficient inverse problem already isolated by the atlas.

[PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md](./PMNS_SELECTOR_MINIMAL_MICROSCOPIC_EXTENSION_NOTE.md):
the smallest honest positive selector realization class is now fully specified:
a genuinely new non-additive sector-sensitive mixed bridge, supported only on
the non-universal locus and carrying one real reduced amplitude `a_sel` on the
unique class `chi_N_nu - chi_N_e`.

[PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md](./PMNS_BRANCH_CONDITIONED_QUADRATIC_SHEET_CLOSURE_NOTE.md):
once a future selector realizes `a_sel != 0`, the remaining coefficient
problem on the selected minimal branch is no longer an open-ended seven-number
search. On either selected two-Higgs branch, the canonical coefficients
reconstruct explicitly from branch Hermitian data by one quadratic equation and
rational back-substitution, with a residual generic `Z_2` sheet. On the
charged-lepton-side branch, the extra monomial neutrino data are just the three
direct Dirac mass moduli.

## Why the two branches have different full-closure sizes

### Neutrino-side minimal branch

If the neutrino sector is the first lepton lane to leave the single-Higgs
monomial class, while the charged-lepton sector stays monomial, then the
canonical neutrino two-Higgs branch already carries the full Dirac-neutrino
data count:

- `3` neutrino masses
- `3` PMNS angles
- `1` Dirac phase

So full neutrino closure on that branch is a seven-real-quantity problem.

### Charged-lepton-side minimal branch

If the charged-lepton sector is instead the first non-monomial lepton lane,
then PMNS can live on the charged-lepton branch. But the monomial neutrino
Dirac lane still contributes its own exact residual data: the `3` positive
Dirac singular values.

So branch-local zero-import full neutrino closure on that branch is not just a
seven-quantity PMNS problem. It is:

- `3` neutrino Dirac mass moduli
- `7` charged-lepton-side branch quantities

for a total of `10` real quantities.

## Theorem-level statement

**Theorem (Last-mile reduction for full neutrino closure).** Assume:

1. the retained three-generation Majorana current-stack law
   `M_R,current = 0_(3 x 3)`
2. the exact minimal neutrino-side and charged-lepton-side PMNS-producing
   branches
3. the exact current-atlas nonselection theorem for those branches

Then:

1. on the neutrino-side minimal branch, full neutrino closure reduces to
   deriving `7` real quantities
2. on the charged-lepton-side minimal branch, branch-local zero-import full
   neutrino closure reduces to deriving `3` neutrino Dirac mass moduli plus `7`
   charged-lepton-branch quantities
3. the current atlas does not yet select between those branches

Therefore the remaining exact gap is branch-conditioned rather than a generic
flavor-texture problem.

Equivalently: on the current bank, the remaining gap is still piecewise because
shared-Higgs universality is not yet derived. If that universality were later
proved, the current one-sided branch split would collapse and the last-mile
count would need to be recomputed on the resulting shared support class.
The new underdetermination theorem sharpens the same point from the opposite
direction: the current stack does not yet derive universality failure either.
And the new quadratic-sheet closure theorem sharpens the coefficient side:
after selector realization, the surviving branch no longer carries an
open-ended coefficient family. Its residual ambiguity is finite and explicit.
The new right-Gram extension theorems then show that there is an admitted
right-sensitive route closing both remaining post-boundary bits: a right-Gram
support comparison realizes the selector class, and one right-Gram scalar
fixes the residual sheet generically.

[PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md](./PMNS_RIGHT_FRAME_ORBIT_OBSTRUCTION_NOTE.md):
that admitted right-Gram route is still not intrinsic on the retained bank.
The current packet fixes the left/Hermitian core and the right-handed
representation content, but it leaves an exact right-unitary orbit
`Y_s -> Y_s U_R,s^dag`; along that orbit the admitted selector datum and the
admitted sheet-fixing scalar vary while `H_s` stays fixed. So the strongest
exact endpoint is now sharper than “a right-sensitive completion route exists”:
the bank determines a right-orbit bundle, not a canonical right frame.

[PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md](./PMNS_INTRINSIC_COMPLETION_BOUNDARY_NOTE.md):
the selected-branch Hermitian inverse problems are already exact, so the
remaining intrinsic gap is no longer another local inverse-problem reduction.
With the positive polar section now in hand on the generic full-rank patch,
the real remaining object is the selected branch Hermitian data law, together
with one residual non-Hermitian/right-sensitive sheet-fixing datum if
canonical coefficient-sheet closure is required.

[PMNS_GLOBAL_HERMITIAN_MODE_PACKAGE_NOTE.md](./PMNS_GLOBAL_HERMITIAN_MODE_PACKAGE_NOTE.md):
the global active Hermitian law is no longer best thought of as a raw
seven-real target. It splits exactly into a `2 + 2 + 3` package:
- weak-axis seed pair `(A,B)`
- aligned deformation pair
- exact breaking triplet `(delta,rho,gamma)`
So the remaining global Hermitian question is already sectorized exactly,
rather than left as a generic flavor object.

[PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md](./PMNS_EWSB_RESIDUAL_Z2_HERMITIAN_CORE_NOTE.md):
under the explicit bridge condition that the active one-sided PMNS branch is
aligned with the exact weak-axis EWSB selection, the active Hermitian law
sharpens from the generic seven-coordinate grammar to the four-real core
`[[a,b,b],[b,c,d],[b,d,c]]`, while the passive monomial sector stays
diagonal. Equivalently, the generic active branch splits into that exact core
plus three explicit symmetry-breaking slots `(d_2-d_3, r_12-r_31, phi)`. This
does not yet change the honest current-bank endpoint, because the current bank
still does not derive the alignment condition itself or those breaking slots,
but it does narrow the `H_nu/H_e` target on the aligned one-sided surface.

[PMNS_EWSB_RESIDUAL_Z2_SPECTRAL_PRIMITIVE_NOTE.md](./PMNS_EWSB_RESIDUAL_Z2_SPECTRAL_PRIMITIVE_NOTE.md):
on that aligned surface, the four-real core is not the sharpest package.
The exact even/odd split reduces it further to one `2 + 1` spectral primitive
package
`(lambda_+, lambda_-, lambda_odd, theta_even)`.
So if an alignment bridge were later derived, the honest Hermitian target
would become three spectral invariants plus one even-sector angle, rather than
raw matrix entries.

[PMNS_EWSB_WEAK_AXIS_Z3_SEED_NOTE.md](./PMNS_EWSB_WEAK_AXIS_Z3_SEED_NOTE.md):
the current bank now derives one concrete Hermitian seed even before the full
active Hermitian law is known. The exact weak-axis `1+2` split
`diag(A,B,B)` lifts through the canonical `Z_3` bridge to the even-circulant
seed `mu I + nu(C+C^2)`. On the canonical active Yukawa chart this seed is
realized if and only if `A <= 4B`, and when realized it is forced onto the
unique symmetric active two-Higgs slice `Y=xI+yC`. So the aligned Hermitian target is now
sharper than “four unknown core amplitudes”: it contains an exact two-parameter
weak-axis seed, plus two aligned deformation directions, before the generic
three-slot breaking vector is added.

[PMNS_EWSB_WEAK_AXIS_SEED_COEFFICIENT_CLOSURE_NOTE.md](./PMNS_EWSB_WEAK_AXIS_SEED_COEFFICIENT_CLOSURE_NOTE.md):
on that compatible seed patch, the coefficient side also sharpens. The exact
canonical active coefficients are explicit as `Y_+ = x_+ I + y_+ C` and
`Y_- = y_+ I + x_+ C`, so the residual ambiguity is exactly one exchange
sheet `x <-> y`. This is stronger than the generic branch-conditioned
quadratic-sheet closure: even right-Gram data collapse on the seed patch,
since both sheets satisfy `Y^dag Y = H_seed`. So the remaining object there is
not a generic coefficient fit and not a right-Gram datum, but one genuinely
`Y`-level sheet selector; more sharply, it is exactly the restricted
Higgs-offset / monomial-edge selector on the canonical `(0,1)` pair.

[PMNS_EWSB_ALIGNMENT_NONFORCING_NOTE.md](./PMNS_EWSB_ALIGNMENT_NONFORCING_NOTE.md):
the current retained bank does not force the active one-sided PMNS branch onto
that aligned residual-`Z_2` core. Full-rank aligned and non-aligned points
coexist on the same exact canonical active branch while satisfying the current
support and Hermitian inverse-problem conditions, so alignment remains a
conditional sharpening rather than a selected current-bank law.

[PMNS_EWSB_BREAKING_SLOT_NONREALIZATION_NOTE.md](./PMNS_EWSB_BREAKING_SLOT_NONREALIZATION_NOTE.md):
the current retained bank also does not yet derive the generic breaking-slot
vector away from the aligned core. Distinct full-rank points on the same exact
canonical active branch can carry different values of
`(d_2-d_3, r_12-r_31, phi)` while satisfying all current-bank conditions.
So the current bank now gives the correct `4 + 3` coordinate split on the
active Hermitian branch, but not yet the law fixing those three slots.

## What this closes

This closes the last-mile bookkeeping question.

It is now exact that:

- the current bank has already eliminated generic `3 x 3` texture freedom
- the remaining gap is not symmetric across the two minimal branches
- the current bank still lacks the selector that would turn the piecewise gap
  into one concrete closure target
- once a selector is realized, the remaining coefficient problem is explicit
  up to one residual `Z_2` sheet on the selected two-Higgs branch
- there is now an admitted right-sensitive completion route that closes both
  the selector bit and the residual sheet bit exactly on the generic patch
- and on the generic full-rank patch the retained bank already has the
  canonical positive orbit representative `Y_+(H) = H^(1/2)`, so the branch
  side is intrinsically readable once the Hermitian data are known
- but the retained bank still does not derive those Hermitian data themselves
  and still does not fix the residual `Z_2` sheet from `H` alone

## What this does not close

This note does **not** derive:

- the discrete selector theorem
- the `7` neutrino-side quantities
- the `3 + 7` charged-lepton-side quantities
- the branch Hermitian data themselves
- the residual `Z_2` sheet from the retained bank alone
- the admitted right-sensitive completion datum from the retained axiom bank

It is a reduction theorem only.

## Command

```bash
python3 scripts/frontier_neutrino_full_closure_last_mile_reduction.py
```
