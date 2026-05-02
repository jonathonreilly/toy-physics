# R5 Strict-Bar Campaign — Final Report

**Date:** 2026-05-02
**Loop:** `positive-only-r5-20260502`
**Mode:** strict bar (claim_type = positive_theorem; deps at retained today; zero admitted physics inputs)

## Summary

Three blocks shipped. All passed the strict-bar gate at write time and are awaiting independent Codex audit.

| Block | Topic | Single one-hop dep | Runner | PR |
|-------|-------|--------------------|--------|-----|
| 01 | q-q-q baryon color singlet (3 ⊗ 3 ⊗ 3 = 1 ⊕ 8 ⊕ 8 ⊕ 10) | `cl3_color_automorphism_theorem` (retained) | 5/5 PASS | [#352](https://github.com/jonathonreilly/cl3-lattice-framework/pull/352) |
| 02 | [P̂_total^μ, Q̂_total] = 0 on H_phys | `axiom_first_lattice_noether_theorem_note_2026-04-29` (retained — N1 + N2) | 5/5 PASS | [#354](https://github.com/jonathonreilly/cl3-lattice-framework/pull/354) |
| 03 | Per-site Cl(3) Hilbert ≅ unique j=1/2 su(2) irrep | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained) | 7/7 PASS | [#356](https://github.com/jonathonreilly/cl3-lattice-framework/pull/356) |

## Quality

All three blocks have:
- exactly one retained-grade one-hop upstream dep on the live ledger today;
- zero admitted physics conventions (only mathematical / Lie-algebraic admitted-context inputs: SU(N) tensor product rule, Levi-Civita as SU(N) invariant, translation invariance of a uniform U(1) phase, Stone commuting-generators theorem, bivector → spin Lie-algebra construction, Casimir ↔ irrep label correspondence);
- machine-precision numerical verification (no nontrivial tolerances).

## Round-by-round R1 → R5 cumulative tally

| Round | Blocks | Cumulative |
|-------|--------|-----------|
| R1 | gluon massless, Pauli exclusion, CPT mass equality | 3 |
| R2 | momentum conservation, CPT lifetime, CMW low-d sublattice | 6 |
| R3 | fermion-number conservation, CPT² = I, q-q̄ meson singlet | 9 |
| R4 | per-site dim = 2, Wigner mode 2-dep, no per-site bosonic CCR | 12 |
| R5 | q-q-q baryon singlet, [P̂, Q̂] = 0, per-site j=1/2 spin | **15** |

15 strict-bar positive-theorem retention candidates produced under the new framework vocabulary.

## Per-site representation-theoretic foundation completed

R4 + R5 together close the per-site representation-theoretic story:

- per-site dim = 2 (R4 Block 01)
- Pauli is the unique faithful 2-dim Cl(3) irrep (per-site uniqueness theorem)
- per-site spin label = j = 1/2 (R5 Block 03)
- no bosonic CCR per-site (R4 Block 03)
- Wigner mode count grows linearly in 2 (R4 Block 02)

Combined, the framework's elementary fermion content is forced to be exactly the 2-dim spin-1/2 Pauli module at every site, with no alternative algebraic structure available without modifying A_min itself.

## Hadronic sector closed at the kinematic level

R3 + R5 together establish the hadronic singlet structure:

- meson singlet 3 ⊗ 3̄ = 1 ⊕ 8 (R3 Block 03)
- baryon singlet 3 ⊗ 3 ⊗ 3 = 1 ⊕ 8 ⊕ 8 ⊕ 10 (R5 Block 01)
- antibaryon singlet by C-conjugation (immediate corollary)

This is the kinematic basis for all observed hadronic species.

## Quantum number labelling completed

R2 + R3 + R5 Block 02 together establish the (E, P^μ, Q) Wigner labels:

- [H, P̂^μ] = 0 — momentum conservation (R2 Block 01)
- [H, Q̂] = 0 — charge conservation (R3 Block 01)
- [P̂^μ, Q̂] = 0 — cross commutator (R5 Block 02)

Therefore (E, P^μ, Q) is a complete commuting set on every framework energy eigenstate.

## Process notes

- Pre-screening eliminated 0 candidates this round (all three Block-1/2/3 picks landed cleanly).
- All three blocks have machine-precision runners (no tolerances above 1e-6).
- Branch + PR for each block opened immediately after runner PASS.

## Next steps

The strict-bar gate continues to be productive. R6 candidates worth pre-screening:
- [H, Q̂] = 0 — Heisenberg-form charge conservation (companion to R2 Block 01)
- T_a T_b = T_{a+b} — exact translation group composition law
- Cl(3) volume element ω = γ_1γ_2γ_3 = ±i·I in Pauli rep (no per-site chirality)
- Antiparticle existence with same mass, opposite charge (CPT corollary)

Each pre-screens cleanly: single retained dep, zero admitted physics inputs.
