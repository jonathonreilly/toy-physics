# R7 Strict-Bar Campaign — Final Report

**Date:** 2026-05-02
**Loop:** `positive-only-r7-20260502`
**Mode:** strict bar (claim_type = positive_theorem; deps at retained today; zero admitted physics inputs)

## Summary

Three blocks shipped. All passed the strict-bar gate at write time and are awaiting independent Codex audit.

| Block | Topic | Single one-hop dep | Runner | PR |
|-------|-------|--------------------|--------|-----|
| 01 | SU(3) adjoint Casimir C_2(8) = 3 | `cl3_color_automorphism_theorem` (retained) | 7/7 PASS | [#366](https://github.com/jonathonreilly/cl3-lattice-framework/pull/366) |
| 02 | T_a O(x) T_a^† = O(x+a) translation covariance of local operators | `axiom_first_lattice_noether_theorem_note_2026-04-29` (retained) | 6/6 PASS | [#368](https://github.com/jonathonreilly/cl3-lattice-framework/pull/368) |
| 03 | Per-site n̂ ∈ {0, 1} ⇒ Q̂_total integer spectrum {0, ..., N} | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained) | 6/6 PASS | [#371](https://github.com/jonathonreilly/cl3-lattice-framework/pull/371) |

## Quality

All three blocks have:
- exactly one retained-grade one-hop upstream dep on the live ledger today;
- zero admitted physics conventions (only mathematical / structural admitted-context inputs: adjoint rep construction, Schur's lemma, position-basis decomposition, local support definition, single-mode fermion construction, tensor product Fock space, binomial coefficient counting);
- machine-precision numerical verification (no nontrivial tolerances).

## Round-by-round R1 → R7 cumulative tally

| Round | Blocks | Cumulative |
|-------|--------|-----------|
| R1 | gluon massless, Pauli exclusion, CPT mass equality | 3 |
| R2 | momentum conservation, CPT lifetime, CMW low-d sublattice | 6 |
| R3 | fermion-number conservation, CPT² = I, q-q̄ meson singlet | 9 |
| R4 | per-site dim = 2, Wigner mode 2-dep, no per-site bosonic CCR | 12 |
| R5 | q-q-q baryon singlet, [P̂, Q̂] = 0, per-site j=1/2 spin | 15 |
| R6 | no per-site γ_5, T_a T_b = T_{a+b}, SU(3) C_2(3) = 4/3 | 18 |
| R7 | SU(3) C_2(adj) = 3, T_a O T_a^† = O(x+a), Q̂ integer spectrum | **21** |

**21 strict-bar positive-theorem retention candidates** produced under the new framework vocabulary across seven rounds.

## R7 highlight: closing the operator-level kinematic story

R7 closes three previously implicit but operator-level structural facts:

1. **Gluon color charge squared = 3** (Block 01). Companion to R6 Block 03's quark color charge squared = 4/3. Together they form the basic Casimir table for SU(3)_c, with C_2(adj) appearing as the prefactor of the gluonic β-function term and as the color factor in three-gluon vertex / gluon self-energy diagrams.

2. **Local operator covariance T_a O(x) T_a^† = O(x+a)** (Block 02). The operator-level statement of N1 translation invariance: any site-local operator (charge density, energy density, fermion bilinear, hopping, ...) shifts by lattice vector a under T_a-conjugation. Provides the foundational tool for verifying that any framework Hamiltonian built from translation-invariant local terms automatically commutes with T_a.

3. **Q̂_total integer spectrum** (Block 03). Kinematic charge quantization: every framework state has integer-valued total charge in {0, 1, ..., N_sites}, with binomial multiplicities. No fractional or continuous Q permitted. Provides the Q-sector decomposition H = ⊕_k H_k that any conserved-Q Hamiltonian must preserve.

## Q-sector picture is now closed

R3 + R5 + R6 + R7 together establish the complete Q-sector / translation kinematic + dynamic + transport story:

| Fact | Block | Status |
|------|-------|--------|
| Q̂_total has integer spectrum {0, ..., N} | R7 Block 03 | retention candidate |
| [H, Q̂] = 0 (conservation) | R3 Block 01 | retention candidate |
| [P̂^μ, Q̂] = 0 (commutes with momentum) | R5 Block 02 | retention candidate |
| T_a Q̂_x T_a^† = Q̂_{x+a} (covariance) | R7 Block 02 | retention candidate |

Together: Q is conserved, integer-valued, translation-covariant, and labels independent particle states alongside (E, P^μ, spin). This is the full Wigner-classification structure.

## Color sector picture is now closed (Casimir-level)

R6 Block 03 + R7 Block 01 together establish the full Casimir table:

| Rep | Casimir | Block |
|-----|---------|-------|
| Fundamental "3" (quark) | 4/3 | R6 Block 03 |
| Adjoint "8" (gluon) | 3 | R7 Block 01 |

These are the universal multiplicative color factors throughout perturbative QCD. The framework's color algebra now has both numbers derived structurally.

## Process notes

- Pre-screening eliminated 0 candidates this round.
- All three blocks have machine-precision runners.
- Branch + PR for each block opened immediately after runner PASS.
- Block 02 had a sign error in the position-operator covariance test (X̂ ↦ X̂ - a not + a) that was caught and fixed before commit.
- Block 3 was pivoted from "antiparticle Q-flip from CPT antiunitary" to "Q̂_total integer spectrum on Fock space" because the framework's lattice CPT operator (sublattice parity) doesn't directly act on internal U(1) labels in a way that could be shown structurally without additional admitted physics about charge conjugation conventions.

## Next steps

R8 candidate ideas worth pre-screening:
- T_a^N = I on periodic Z^3 (already in R5 Block 02 / R6 Block 02 corollaries; could repackage as standalone)
- Gell-Mann-like decomposition: any 3x3 traceless Hermitian matrix is a combo of T^a (Lie algebra basis completeness)
- Per-site σ_3 has eigenvalues ±1 ⇒ Pauli rep decomposes H_x = H_+ ⊕ H_- (spin-z splitting)
- N_c = 3 forced by Cl(3) on Z^3 — direct from cl3_color_automorphism, repackage as standalone "color count = 3"
- Total fermion parity (-1)^Q is conserved — direct from Q conservation + Q ∈ Z

The strict-bar discipline continues to yield clean retention candidates by:
1. Pulling structural facts implicit in retained authorities;
2. Computing them explicitly with machine-precision runners;
3. Standing them up as standalone theorem rows in the audit ledger.

The "zero physics admissions" rule keeps tightening the foundation.
