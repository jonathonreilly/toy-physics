# PMNS `C3` Character Holonomy Closure

**Status:** bounded - bounded or caveated result note
**Date:** 2026-04-16  
**Script:** `scripts/frontier_pmns_c3_character_holonomy_closure.py`

## Question

Does the exact coordinate-cycle symmetry already furnish a native three-mode
holonomy family on the retained `hw=1` triplet, so that the reduced PMNS cycle
values close without admitting an external generic three-flux family?

## Answer

Yes.

On the retained `hw=1` triplet, the exact coordinate-cycle unitary projects to
the forward-cycle matrix `C`, whose characters are exactly:

- `1`
- `omega = exp(2 pi i / 3)`
- `omega^2 = exp(4 pi i / 3)`

So the native character phases are:

- `0`
- `2 pi / 3`
- `4 pi / 3`

## Reduced-Cycle Law

On the reduced graph-first family

`A_fwd(u,v,w) = (u + i v) E12 + w E23 + (u - i v) E31`

the corresponding character holonomies are exactly the one-angle holonomies at
those canonical phases. Their design matrix is

```text
[[ 2,  0,        1],
 [-1,  sqrt(3),  1],
 [-1, -sqrt(3),  1]]
```

and has nonzero determinant.

Therefore `(u,v,w)` are reconstructed exactly from the exact `C3` character
triple itself.

## Consequence

This strengthens the earlier three-flux theorem.

Before:
- a generic three-flux family was admitted and shown to close `(u,v,w)`

Now:
- the exact coordinate-cycle symmetry already supplies a canonical native
  three-mode holonomy family
- so the reduced PMNS cycle values close on an exact native `C3`-character
  route

## What It Does Not Claim

This still does **not** give full sole-axiom positive neutrino closure.

What remains blocked is not the reduced-cycle readout family anymore. It is the
sole-axiom production of **nontrivial values** on that native character family.

The sole axiom still yields only the trivial free retained response profiles,
and those do not realize the PMNS-active lane.

## Verification

```bash
python3 scripts/frontier_pmns_c3_character_holonomy_closure.py
```
