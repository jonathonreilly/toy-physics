# DM Clear Blocker Note

**Date:** 2026-04-14
**Branch:** `codex/dm-across-the-line`
**Purpose:** state the sharpest remaining blocker after the direct-observable
pivot and branch audit

---

## Status

**BOUNDED / OPEN**

The direct-observable pivot materially strengthens the DM numerator:

- `sigma_v` is on a native `H -> T-matrix -> sigma_v` route
- the Coulomb shape is on a native lattice Green's-function route
- the Boltzmann / thermodynamic wording is materially tighter than the older
  branch state

The overall lane is still not closed. After the audit, the sharpest honest
blocker is no longer "find more numerator algebra" and no longer "go back to
transport first."

It is this:

> is the unit coefficient in `H = sum eta_ij U_ij` allowed to stand as a
> physical framework constraint, or does the paper bar require a theorem-grade
> derivation of `g = 1` beyond that premise?

**Update after the rigidity pass:** the branch now has a stronger candidate
response in
[G_BARE_RIGIDITY_THEOREM_NOTE.md](/Users/jonBridger/Toy%20Physics-dm/docs/G_BARE_RIGIDITY_THEOREM_NOTE.md:1).
That route does **not** claim a dynamical selection principle for `1`; it
claims instead that, once the concrete `su(3)` operator algebra is fixed,
there is no independent bare coupling parameter left. Until that route is
fully integrated into branch authority, this note keeps the blocker explicit.

---

## Why This Is The Blocker

The current branch already has:

1. a direct-observable route that dissolves the old "is the same coupling
   entering `sigma_v`?" objection
2. a negative audit of the self-duality route
3. no present determinant / source-response DM derivation that could replace
   the direct-observable numerator stack, though that machinery now does carry
   a real denominator normalization result on the neutrino bridge

So the unresolved issue is not scheme ambiguity and not a missing alternative
physics route already living on the branch.

It is the physical status of the unit coefficient in the Hamiltonian.

If the framework premise is accepted, the remaining work is mostly:

- packaging coherence
- secondary `k = 0` / radiation-era wording
- honest relic-summary boundaries

If the framework premise is **not** accepted, then the branch does not
currently contain a theorem-grade closure route for `g = 1`.

If the rigidity theorem route **is** accepted, then the old `g = 1` blocker
is substantially narrowed and the next honest pressure point moves back
downstream to the full relic denominator / cosmology surface.

---

## Secondary Issues

Two issues remain real but secondary to the blocker above:

1. **`k = 0` / freeze-out expansion wording**
   - this is still bounded where the Newtonian Friedmann route is used
   - current branch notes make a strong case that it is numerically
     negligible at freeze-out

2. **Thermodynamic / radiation-era bridge wording**
   - this still needs disciplined language
   - but the branch already has much stronger numerator and Boltzmann support
     than before the pivot

These are not the cleanest branch headline blocker anymore.

---

## What Does Not Work

The audit rules out three easy escapes:

1. **Self-duality does not close `g = 1`.**
   That route is an honest negative result.

2. **The determinant / source-response machinery is not a substitute numerator
   route.**
   It now helps on the denominator normalization surface, but it does not
   solve the Hamiltonian-normalization question addressed in this note.

3. **Returning to `eta` transport does not solve this blocker.**
   It changes the problem rather than resolving the Hamiltonian-normalization
   question.

---

## Decision Boundary

This is the practical branch decision boundary:

- If the publication bar accepts framework-defining normalization as physical,
  keep driving the direct-observable route and clean up the remaining
  secondary wording.
- If the publication bar requires a theorem beyond the framework premise,
  the branch needs a genuinely new selection principle for `g = 1`, and that
  route does not currently exist here.

That is the clear blocker.
