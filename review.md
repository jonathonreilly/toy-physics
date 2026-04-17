# Review: `claude/cl3-minimality`

## Current Call

Not ready to land as a retained axiom-depth closure of why the framework uses
`Cl(3)`.

The branch contains a potentially useful minimality/compatibility argument, but
it still does not clear the retained bar for G16. The load-bearing issue is
that the theorem is trying to derive `d_s = 3` while still importing
`Cl(3)`/`Z^3`-specific retained structure.

## Replay Status

- `python3 -m py_compile scripts/frontier_cl3_minimality.py` passes
- `python3 scripts/frontier_cl3_minimality.py` ends with
  `THEOREM_PASS=13 SUPPORT_PASS=33 FAIL=0`

So the problem is not arithmetic failure. The problem is theorem scope,
dependency hygiene, and overclaim.

## What Must Be True For Retained Pass

To take this as retained, the resubmission has to come back with all four of
these true at once:

1. the theorem no longer presupposes `Cl(3)`/`Z^3` in the premises while trying
   to derive `d_s = 3`
2. the runner actually verifies the Clifford-structure claims the note
   advertises
3. the four-generation statement is proved at the same scope it is claimed
4. the algebra language is mathematically correct and consistent throughout

Until all four are true, this is not a retained closure of G16.

## Blockers And Exact Fix Requirements

### 1. Circular axiom-depth closure

**Problem**

The note says it closes the remaining half of why the framework uses `Cl(3)`,
but:

- its only axiom is `A1. Cl(3) on Z^3 is the physical theory`
- Step 2 imports the retained `8 = 1 + 1 + 3 + 3` orbit algebra from the
  accepted cubic `Z^3` generation surface
- the note's own weakest-link section already admits this is circular on a
  hypothetical non-`Z^3` surface

That means the current theorem is not an axiom-depth derivation of `d_s = 3`.
It is a conditional compatibility theorem on an already-accepted
`Cl(3)`/`Z^3` surface.

**What would clear this**

For retained status, the theorem must be rewritten so the premises do not
already contain the conclusion.

Concrete requirements:

- Replace `A1. Cl(3) on Z^3 is the physical theory` with a genuinely
  comparison-level starting surface.
  Acceptable examples:
  - generic `Cl(n)` candidate family on `Z^n`
  - a weaker accepted one-axiom Hilbert/locality/information surface
  - another retained surface that does not already hard-code `d_s = 3`
- Remove the current Step-2 dependence on the retained cubic generation note as
  a proof of `n = 3`.
- Supply one of the following:
  - a non-circular derivation of the `8`-state requirement from a retained
    principle that is not already cubic-generation-specific
  - an independent route to `n = 3` that does not use the `8 = 1 + 1 + 3 + 3`
    generation surface at all
  - a universal no-go theorem excluding all `n != 3` within the accepted
    comparison family
- Add a one-page dependency table that marks each premise as either:
  - `n`-generic / comparison-level
  - `n = 3`-specific / downstream

**What will not clear this**

- rephrasing the current argument as if compatibility implies derivation
- keeping `A1 = Cl(3) on Z^3` and calling the result “absorbed into the axiom”
- treating the circularity admission in the weakest-link section as sufficient
  honesty for a retained claim

### 2. Clifford-structure runner mismatch

**Problem**

The note advertises runner verification of:

- `Cl(3; C) = M_2(C) ⊕ M_2(C)` by explicit construction + isomorphism
- `Cl^+(3) ≅ Cl(2; C) = M_2(C)` by explicit basis

But the current script explicitly says it is only working in a single Pauli
`M_2(C)` copy for the bivector/SU(2) check. It does not build:

- the direct-sum algebra
- chirality projectors / pseudoscalar split
- an explicit even-subalgebra basis and closure check

So the runner is materially weaker than the note says.

**What would clear this**

Because the retained target depends on these claims, the right fix is to
strengthen the runner rather than weaken the note.

Required additions:

- Build an explicit block-diagonal realization of `Cl(3; C)` as
  `M_2(C) ⊕ M_2(C)`.
- Construct the pseudoscalar / chirality operator and verify the two-factor
  decomposition explicitly.
- Build an explicit basis for the even subalgebra `Cl^+(3)` and verify:
  - closure
  - dimension
  - matrix-algebra identification with `M_2(C)`
- Keep the current Pauli-copy bivector/SU(2) check, but relabel it as one piece
  of the full verification rather than the whole thing.

The note, runner docstring, and appendix have to say the same thing after this.

### 3. Four-generation exclusion is stronger than the proof

**Problem**

The current branch claims exactly-four-generation matter is structurally
forbidden. But the actual check is only:

- `10`, `12`, and `14` are not powers of two
- `16 = 2^4` corresponds to even `n = 4`

That does not exclude higher-dimensional `Cl(n)` realizations with four
generations plus additional sectors. Elsewhere the note already treats larger
odd `n` as over-rich rather than impossible.

**What would clear this**

For retained status, either prove a real no-go theorem or stop claiming one.

A real no-go would need:

- a clearly defined theorem class:
  - all odd `n`?
  - all retained `Cl(n)` comparison-family embeddings?
  - all embeddings preserving the accepted no-rooting / no-proper-quotient /
    observable-species semantics?
- an argument that every four-generation candidate in that class necessarily
  carries extra exact sectors that survive as additional physical species on the
  same accepted surface
- a proof that those extra sectors cannot be quotiented away, reinterpreted, or
  hidden without violating existing retained generation semantics

There is a plausible route here:

- use the retained no-rooting / no-proper-quotient generation stack
- classify the minimal `2^n` carrier spaces capable of supporting four distinct
  generations
- show every such carrier on the accepted comparison family necessarily leaves
  additional exact sectors that remain physically distinct on the same surface

But that theorem is not currently present. Until it is, the four-generation
line must not be called a structural prohibition.

### 4. Incorrect algebra language for larger `n`

**Problem**

Step 1 says the extra bivectors at `n ≥ 4` form an "`su(n)`-like algebra" of
dimension `n(n-1)/2`.

That is wrong. The bivector sector generates `so(n)` / `spin(n)`, whose
dimension is `n(n-1)/2`. `su(n)` has dimension `n^2 - 1`.

**What would clear this**

This is a straightforward correction:

- replace `su(n)`-like with `so(n)` / `spin(n)`
- or use more conservative wording such as “a larger bivector sector”

This is not the main blocker, but it does need to be fixed before resubmission.

## Required Resubmission Shape

If the target is still retained G16 closure, the resubmission should come back
with:

1. a rewritten authority note whose premises are genuinely comparison-level
2. a real non-circular route to `n = 3`
3. a strengthened runner that verifies the full Clifford-structure claims
4. either:
   - a true four-generation no-go theorem, or
   - the four-generation language removed from the retained claim
5. corrected `so(n)` / `spin(n)` language everywhere

## Packaging Rule

Do not spend time on manuscript/package/front-door wiring until the science
stack above is fixed.

If the next resubmission does not clear item 1, the honest classification is
still support/conditional minimality rather than retained closure.

## Bottom Line

The branch has a usable idea, but not yet a retained theorem.

The retained route is:

- remove the circular `Cl(3)`/`Z^3` premise
- supply a genuinely comparison-level derivation of `n = 3`
- make the runner verify the stronger Clifford claims it advertises
- either prove the four-generation no-go at full scope or stop claiming it

Until then, this should not be treated as “G16 closed” or “`d_s = 3` absorbed
into the axiom.”
