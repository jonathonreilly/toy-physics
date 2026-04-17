# Review: `claude/cl3-minimality`

## Current Call

Not ready to land as an axiom-depth closure for `d_s = 3`.

The branch has a usable support idea, but only in a narrower form:

> given the retained cubic three-generation `8`-state orbit algebra, the
> retained native `SU(2)` bivector requirement, and odd-parity chirality
> compatibility, `n = 3` is the unique compatible Clifford size.

That is a conditional minimality/support note. It is not yet a route that
closes the axiom-depth question from framework-internal structure alone.

## Replay Status

- `python3 -m py_compile scripts/frontier_cl3_minimality.py` passes
- `python3 scripts/frontier_cl3_minimality.py` ends
  `THEOREM_PASS=13 SUPPORT_PASS=33 FAIL=0`

So the issue is not arithmetic failure. The issue is claim boundary.

## Blocking Gaps

### 1. The dimensional-match step is circular as a `d_s` derivation

The current Step 2 uses the retained `8 = 1 + 1 + 3 + 3` orbit algebra to
force `2^n = 8`, hence `n = 3`.

But that orbit algebra is itself derived on the accepted cubic `Z^3` surface.
So this does not derive `d_s = 3` independently; it conditions on a
`d_s = 3`-specific retained structure and then reads `d_s = 3` back out.

This is already acknowledged in the note's weakest-link section. The public
claim needs to match that admission.

#### Acceptable fixes

Option A: close the gap for real

- derive an `8`-state requirement from a retained principle that does **not**
  already presuppose the cubic `Z^3` orbit surface, or
- derive a different route to `n = 3` that does not import a `d_s = 3`-specific
  matter structure.

Option B: narrow the claim

- change the note from "closes the remaining half" / "absorbs `d_s = 3` into
  the axiom" to a conditional support statement
- explicitly say this is a **compatibility/minimality corollary** on the
  retained cubic generation surface, not a first-principles axiom-depth closure

### 2. The larger-`n` bivector algebra is described incorrectly

The current text says the larger-`n` bivectors form an "`su(n)`-like algebra"
with dimension `n(n-1)/2`.

That is not correct. The bivectors generate `so(n)` / `spin(n)`, whose
dimension is `n(n-1)/2`. `su(n)` has dimension `n^2 - 1`.

#### Required fix

- replace the `su(n)` language with `so(n)` / `spin(n)` or with the more
  conservative wording "a larger bivector sector"

This is not the main blocker, but it needs to be corrected before resubmission.

### 3. The runner claims more than it actually checks

The note says the runner verifies:

- `Cl(3; C) = M_2(C) ⊕ M_2(C)` by explicit construction + isomorphism
- `Cl^+(3) ≅ Cl(2; C) = M_2(C)` by explicit basis

The current runner does not do that. It works in a single Pauli
`M_2(C)` copy for the bivector closure check and never constructs:

- the direct-sum algebra
- chirality projectors
- an explicit `Cl^+(3)` basis/isomorphism check

#### Acceptable fixes

Option A: strengthen the runner

- explicitly build the two-copy `M_2(C) ⊕ M_2(C)` realization
- construct the pseudoscalar / chirality split
- exhibit the even-subalgebra basis and its `M_2(C)` closure explicitly

Option B: narrow the runner claims

- keep the Pauli-copy check as a bivector/SU(2) support computation
- remove the stronger "explicit isomorphism verification" language from the
  note, runner docstring, and appendix

### 4. The four-generation statement is too strong for the current check

The current branch presents a structural fourth-generation exclusion theorem.

But the actual check is narrower:

- `10`, `12`, `14` are not powers of two
- `16 = 2^4` would use even `n = 4`

That does **not** rule out higher-dimensional `Cl(n)` realizations with four
generations plus additional sectors. Elsewhere the note already treats larger
`n` as over-rich rather than impossible.

#### Required fix

- narrow this to a bounded support/tension statement against a **clean**
  four-generation fit on the current retained surface, or
- supply a real no-go argument that excludes all higher-dimensional
  four-generation embeddings as well

## Resubmission Paths

### Path 1: Narrow, honest support note

This is the fastest clean resubmission.

Make the note say:

- this is a **conditional minimality / compatibility support theorem**
- it does **not** close G16 outright
- it does **not** absorb `d_s = 3` into the axiom from first principles
- it does show that the retained cubic generation surface, native weak
  closure, and anomaly-forced chirality are jointly compatible only with
  `n = 3`

If you take this path, also:

- fix `su(n)` -> `so(n)` / `spin(n)`
- align the runner claims with what is actually computed
- demote the fourth-generation statement to bounded support

### Path 2: Try to close the full axiom-depth gap

This is higher-risk and requires genuinely new science.

You would need at least one of:

- a non-circular derivation of the `8`-state requirement
- an independent retained theorem selecting `n = 3` without importing the
  cubic orbit algebra
- a stronger universal exclusion argument for larger `n`

Without that, the current branch is still conditional.

## Packaging Guidance

If resubmitted in the narrow form, package it as:

- companion/support
- optional atlas support tool if you think the minimality diagnostic has reuse
- not a mainline retained closure of axiom depth

Do **not** route it as:

- "G16 closed"
- "remaining half closed"
- "`d_s = 3` fully absorbed into the axiom"
- "four generations structurally forbidden" without stronger proof

## Bottom Line

There is something worth preserving here, but only if the claim is narrowed to
match the actual dependency structure.

As written now:

- math replay: fine
- closure claim: too strong
- resubmission target: conditional minimality/support theorem
