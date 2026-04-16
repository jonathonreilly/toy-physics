# PMNS Right-Frame Orbit Obstruction

**Date:** 2026-04-15  
**Status:** exact current-bank theorem on the admitted right-sensitive PMNS
completion data  
**Atlas front door:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`  
**Script:** `scripts/frontier_pmns_right_frame_orbit_obstruction.py`

## Question

The current PMNS packet now has an admitted right-sensitive completion route:

- a sector-labeled right-Gram support comparison can realize the unique reduced
  selector class
- one right-Gram scalar can fix the residual selected-branch sheet

Can the retained atlas / axiom bank already derive those right-Gram completion
data internally?

## Bottom line

No.

The retained PMNS bank fixes the **left/Hermitian core** and the
right-handed representation content, but it does **not** fix a canonical
right-handed frame.

For each lepton sector and each `U_R in U(3)`,

`Y -> Y U_R^dag`

leaves

`H = Y Y^dag`

and the singular values unchanged, while sending

`K = Y^dag Y -> U_R K U_R^dag`.

So the current bank determines only a **right-orbit bundle** over the retained
left/Hermitian core, not a canonical right frame.

Along that exact right orbit:

- the admitted selector datum `m_R(Y)` can change
- the admitted sheet-fixing modulus `|(Y^dag Y)12|` can change

while all retained left/Hermitian data stay fixed.

Therefore the admitted right-Gram route is still **basis-conditional**. To
derive it from the axiom bank, one needs a genuinely new right-frame-fixing
theorem or a genuinely right-sensitive observable principle.

## Atlas and axiom inputs

This theorem reuses:

- `One-generation matter closure`
- `PMNS branch sheet nonforcing`
- `PMNS right-Gram selector realization`
- `PMNS right-Gram sheet fixing`

It also reuses the same exact structural pattern already isolated on the GR
side:

- `Universal GR A1 invariant section`
- `Universal GR invariant-frame obstruction`

The reuse is only structural. The common pattern is:

- an exact invariant core
- no canonical complementary frame from the current invariant data alone

## Why this is the honest next step

The admitted right-Gram notes were already careful: they identified exact
positive completion routes, not retained-bank derivations.

This note says why that caution is load-bearing.

The current retained PMNS bank sees:

- sector labels
- branch Hermitian data `H`
- left mixing data derived from `H`

but it does not yet supply a canonical right-handed orientation inside the
three-generation singlet sector.

So the remaining gap is not merely “find a right-sensitive number.” It is
“find a right-sensitive number together with the exact right-frame law that
makes it intrinsic.”

## Explicit orbit evidence

Two exact orbit facts sharpen the point:

1. On a monomial lane `Y = D P`, the admitted right-support score
   `m_R(Y) = number of nonzero upper-triangular off-diagonal entries of
   Y^dag Y` starts at `0`. After a nontrivial right-unitary change of frame,
   `H` stays fixed while `K` becomes dense and `m_R` jumps.
2. On a selected canonical two-Higgs lane, a simple right rotation changes
   `|(Y^dag Y)12|` while keeping `H` fixed.

So both admitted right-Gram completion data vary on the same retained
left/Hermitian core.

## Theorem-level statement

**Theorem (The retained PMNS bank fixes a right orbit, not a canonical right
frame).** Assume the retained PMNS boundary packet, the retained
right-handed-generation completion, and the admitted right-Gram selector and
sheet-fixing routes. Then:

1. for each lepton Yukawa representative `Y`, every right-unitary transform
   `Y -> Y U_R^dag` preserves `H = Y Y^dag` and the singular values
2. the same transform conjugates `K = Y^dag Y`
3. on explicit retained-branch samples, the admitted selector datum `m_R(Y)`
   and the admitted sheet-fixing datum `|(Y^dag Y)12|` vary along this exact
   right orbit while `H` stays fixed

Therefore the current retained PMNS bank does not determine a canonical
right-handed frame and does not derive the admitted right-Gram completion data
as intrinsic observables. The strongest exact endpoint is a right-orbit bundle
over the retained left/Hermitian core.

## What this closes

This closes the next derivation-bank question cleanly.

It is now exact that:

- the admitted right-Gram route exists
- but it is not yet an internal axiom-side derivation
- the obstruction is not vague coefficient freedom
- the obstruction is a missing canonical right frame / right-sensitive
  observable law

## What this does not close

This note does **not** derive:

- a canonical right-handed frame
- a retained right-sensitive observable principle
- the branch Hermitian data themselves
- the actual selected-branch coefficients

So it does not upgrade the neutrino lane to positive full closure. It sharpens
the last missing object.

## Command

```bash
python3 scripts/frontier_pmns_right_frame_orbit_obstruction.py
```
