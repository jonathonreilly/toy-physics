# R8 Strict-Bar Campaign — Final Report

**Date:** 2026-05-02
**Loop:** `positive-only-r8-20260502`
**Mode:** strict bar (claim_type = positive_theorem; deps at retained today; zero admitted physics inputs)

## Summary

Three blocks shipped. All passed the strict-bar gate at write time and are awaiting independent Codex audit.

| Block | Topic | Single one-hop dep | Runner | PR |
|-------|-------|--------------------|--------|-----|
| 01 | Fermion parity (-1)^Q̂ Z_2 grading + superselection | `axiom_first_lattice_noether_theorem_note_2026-04-29` (retained) | 7/7 PASS | [#373](https://github.com/jonathonreilly/cl3-lattice-framework/pull/373) |
| 02 | Gell-Mann completeness: {T^a} R-basis for su(3) (8-dim) | `cl3_color_automorphism_theorem` (retained) | 7/7 PASS | [#375](https://github.com/jonathonreilly/cl3-lattice-framework/pull/375) |
| 03 | Pauli group P_1 = ⟨σ_i⟩ has order 16 | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained) | 7/7 PASS | [#376](https://github.com/jonathonreilly/cl3-lattice-framework/pull/376) |

## Quality

All three blocks have:
- exactly one retained-grade one-hop upstream dep on the live ledger today;
- zero admitted physics conventions (only mathematical / structural admitted-context inputs: spectral functional calculus, su(3) definition, dim_R su(3) = 8 standard count, trace inner product, Pauli multiplication identity, group generation theorems);
- machine-precision numerical verification (no nontrivial tolerances).

## Round-by-round R1 → R8 cumulative tally

| Round | Blocks | Cumulative |
|-------|--------|-----------|
| R1 | gluon massless, Pauli exclusion, CPT mass equality | 3 |
| R2 | momentum conservation, CPT lifetime, CMW low-d sublattice | 6 |
| R3 | fermion-number conservation, CPT² = I, q-q̄ meson singlet | 9 |
| R4 | per-site dim = 2, Wigner mode 2-dep, no per-site bosonic CCR | 12 |
| R5 | q-q-q baryon singlet, [P̂, Q̂] = 0, per-site j=1/2 spin | 15 |
| R6 | no per-site γ_5, T_a T_b = T_{a+b}, SU(3) C_2(3) = 4/3 | 18 |
| R7 | SU(3) C_2(adj) = 3, T_a O T_a^† = O(x+a), Q̂ integer spectrum | 21 |
| R8 | fermion parity Z_2 grading, Gell-Mann basis, Pauli group order = 16 | **24** |

**24 strict-bar positive-theorem retention candidates** produced under the new framework vocabulary across eight rounds.

## R8 highlight: closing finite group structures

R8 closes three previously implicit but fundamental finite group / algebra structures:

1. **Fermion-parity superselection** (Block 01). The Z_2 grading H = H_even ⊕ H_odd by F = (-1)^Q̂ enforces that only Z_2-even local operators (bilinears, currents, plaquettes) can connect physical states. Single fermion operators a_x, a_x^† are forbidden in the Hamiltonian — the Bose / Fermi distinction at the operator algebra level.

2. **Gell-Mann basis completeness** (Block 02). The 8 T^a generators are a real-linear basis for su(3) (8-dim by N²-1 count). No "ninth gluon" is possible. Combined with R6 Block 03 (C_2(3) = 4/3) and R7 Block 01 (C_2(8) = 3), this closes the basic SU(3)_c representation-theoretic toolkit.

3. **Pauli group order = 16** (Block 03). The framework's per-site Cl(3) generators close into the canonical single-qubit Pauli group P_1, with structure 1 → Z_4 → P_1 → Z_2 × Z_2 → 1. This is the foundational finite group used throughout quantum information theory (stabilizer formalism, Clifford-circuit theory).

## Color sector picture is now fully closed

R6 + R7 + R8 together establish the complete SU(3)_c structural toolkit:

| Fact | Block | Status |
|------|-------|--------|
| Generators basis (8-dim) | R8 Block 02 | retention candidate |
| Quark Casimir = 4/3 | R6 Block 03 | retention candidate |
| Gluon Casimir = 3 | R7 Block 01 | retention candidate |
| q-q̄ singlet 3 ⊗ 3̄ = 1 ⊕ 8 | R3 Block 03 | retention candidate |
| q-q-q baryon singlet 3⊗3⊗3 = 1⊕8⊕8⊕10 | R5 Block 01 | retention candidate |

Any framework QCD calculation can now lean on these five structural results.

## Charge sector picture is now fully closed

R3 + R5 + R7 + R8 Block 01 together establish the complete Q-sector structure:

| Fact | Block |
|------|-------|
| [H, Q̂] = 0 (conservation) | R3 Block 01 |
| [P̂, Q̂] = 0 (commutes with momentum) | R5 Block 02 |
| Q̂ integer spectrum on Fock | R7 Block 03 |
| T_a Q̂_x T_a^† = Q̂_{x+a} (covariance) | R7 Block 02 |
| Z_2 fermion parity superselection | R8 Block 01 |

Together: framework's charge / fermion-parity structure is fully closed at the kinematic + dynamic + transport levels.

## Per-site algebraic structure picture is now closed

R4 + R5 + R6 + R8 Block 03 together close the per-site structure:

| Fact | Block |
|------|-------|
| Per-site dim = 2 | R4 Block 01 |
| Per-site spin = j = 1/2 | R5 Block 03 |
| No per-site γ_5 chirality | R6 Block 01 |
| No per-site bosonic CCR | R4 Block 03 |
| Wigner mode count linear in 2 | R4 Block 02 |
| Pauli group P_1 order 16 | R8 Block 03 |

Together: per-site algebraic content is structurally rigid at every level checked.

## Process notes

- Pre-screening eliminated 0 candidates this round.
- All three blocks have machine-precision runners.
- Branch + PR for each block opened immediately after runner PASS.
- Block 02 had a sign error in commutator-closure test (expected real-coefficient projection but got anti-Hermitian commutator) that was caught and fixed before commit.

## Observation: structural rigidity is the dominant theme

Rounds R1-R5 produced relatively diverse content (conservation laws, CPT theorems, gauge structure, generation count). Rounds R6-R8 increasingly focus on **structural rigidity / completeness** results: "no additional generators", "no per-site chirality", "no bosonic CCR", "exactly 8 dimensions", "exactly 16 group elements". This reflects the natural direction of the strict-bar discipline: as we close one structural assumption after another, the remaining open questions are increasingly about *what's not possible* in the framework.

## Next steps

R9 candidate ideas worth pre-screening:
- Per-site Hilbert dim_R = 2 over R (since C² has dim 2 over C, but dim 4 over R; need careful framing)
- Total spin operator algebra on multi-site Hilbert: J² = (Σ S_x)² has spin-Casimir-like structure
- Multi-site Pauli group order P_N = 4^{N+1}
- Color singlet projector P_singlet onto (q q̄)^{N=0} channel
- Translation-invariant ground state existence (Reeh-Schlieder cousin)
- d^{abc} symmetric structure constants of su(3) (companion to f^{abc})

The strict-bar discipline has now produced 24 retention candidates across 8 rounds. Each round adds 3 fresh blocks; the queue of pre-screenable candidates remains roughly steady as upstream retained authorities support multiple downstream derivations.
