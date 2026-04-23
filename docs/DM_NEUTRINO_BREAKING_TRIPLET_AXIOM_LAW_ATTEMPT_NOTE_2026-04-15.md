# DM Neutrino Breaking-Triplet Axiom-Law Attempt

**Date:** 2026-04-15
**Status:** strongest exact axiom-boundary theorem for the DM breaking triplet
`(delta, rho, gamma)`
**Atlas placement:** canonical toolkit on `main` at
`docs/publication/ci3_z3/DERIVATION_ATLAS.md`
**Script:** `scripts/frontier_dm_neutrino_breaking_triplet_axiom_law_attempt.py`

## Question

Now that the intrinsic DM tensor is exact in the triplet coordinates,

- `Im[(K_mass)01^2] = -2 gamma (delta + rho) / 3`
- `Im[(K_mass)02^2] =  2 gamma (A + b - c - d) / 3`

can the current exact stack derive a **positive axiom-side value law** for the
triplet itself?

## Bottom line

No positive current-stack value law is available.

The strongest exact theorem is a **zero-locus / minimal-source law**:

- the breaking triplet is exactly the 3-real complement of the aligned
  residual-`Z_2` Hermitian core
- its zero locus is exactly the aligned core on the canonical positive patch
- the current bank does not derive the triplet coefficients as axiom-side
  outputs

So the current stack does not merely leave `(delta, rho, gamma)` unnamed. It
identifies their exact source sector and proves that the source sector has
dimension three, while leaving the values open.

## Exact law now available

On the canonical active Hermitian package,

- `H = H_core + B(delta, rho, gamma)`
- `H_core = [[A,b,b],[b,c,d],[b,d,c]]`
- `B = [[0,rho,-rho-i gamma],[rho,delta,0],[-rho+i gamma,0,-delta]]`

the breaking sector is exactly the real span of three Hermitian generators:

- `E_delta = [[0,0,0],[0,1,0],[0,0,-1]]`
- `E_rho   = [[0,1,-1],[1,0,0],[-1,0,0]]`
- `E_gamma = [[0,0,-i],[0,0,0],[i,0,0]]`

with

`B(delta,rho,gamma) = delta E_delta + rho E_rho + gamma E_gamma`.

So the strongest exact current-stack law is:

1. the triplet vanishes iff the aligned residual-`Z_2` core is reached
2. the exact source locus has real dimension three
3. the current bank does not derive the coefficients

This is the correct axiom-native status of the last-mile object.

## Why this matters for DM directly

The intrinsic DM tensor already says the CP-supporting quantities are

- `gamma`
- `delta + rho`
- `A + b - c - d`

So if the current stack does not derive `(delta, rho, gamma)` positively, it
also does not yet derive the two CP channels positively.

In other words, the remaining DM denominator gap is no longer vague:

- it is not washout
- it is not staircase placement
- it is the missing positive triplet law

## Why the live benchmark is `0.30 eta_obs`

The benchmark

`eta ~= 1.81e-10 ~= 0.30 eta_obs`

is now explained sharply:

- at the same `M_1` and washout, the Davidson-Ibarra ceiling would already give
  `eta_DI ~= 6.54e-10 ~= 1.07 eta_obs`
- the current reduced kernel only realizes
  `epsilon_1 / epsilon_DI ~= 0.277`

So the benchmark shortfall is mainly a **CP-kernel suppression number**:

`eta / eta_obs = (epsilon_1 / epsilon_DI) * (eta_DI / eta_obs)`.

That is exactly what we should expect while the triplet coefficients remain
unfixed on the current stack.

## Theorem-level statement

**Theorem (DM breaking-triplet axiom-law boundary).** Assume the exact
positive-section Hermitian CP theorem, the exact breaking-triplet CP theorem,
the exact PMNS global Hermitian mode package, and the exact PMNS breaking-slot
boundary results. Then:

1. the DM breaking triplet `(delta, rho, gamma)` is exactly the 3-real source
   complement to the aligned residual-`Z_2` Hermitian core
2. its zero locus is exactly the aligned core on the canonical positive patch
3. the current exact stack does not derive the triplet coefficients as
   axiom-side outputs
4. therefore the strongest current-stack law is the zero-locus /
   minimal-source law, not a positive value law
5. the benchmark `eta ~= 0.30 eta_obs` is therefore correctly read as a
   CP-kernel suppression effect rather than a washout or staircase failure

## What this closes

This closes the ambiguity around the status of the remaining DM law.

It is now exact that:

- the triplet source sector is exact
- the triplet zero locus is exact
- the missing object is a positive coefficient law for that triplet

## What this does not close

This note does **not** derive:

- the actual values of `(delta, rho, gamma)`
- the actual values of `delta + rho` or `A + b - c - d`
- full zero-import DM closure

So this is an exact axiom-boundary theorem, not a positive completion theorem.

## Command

```bash
python3 scripts/frontier_dm_neutrino_breaking_triplet_axiom_law_attempt.py
```
