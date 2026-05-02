# R9 Strict-Bar Campaign — Final Report

**Date:** 2026-05-02
**Loop:** `positive-only-r9-20260502`
**Mode:** strict bar (claim_type = positive_theorem; deps at retained today; zero admitted physics inputs)

## Summary

Three blocks shipped. All passed the strict-bar gate at write time and are awaiting independent Codex audit.

| Block | Topic | Single one-hop dep | Runner | PR |
|-------|-------|--------------------|--------|-----|
| 01 | d^{abc} symmetric SU(3) structure constants from anticommutator | `cl3_color_automorphism_theorem` (retained) | 6/6 PASS | [#377](https://github.com/jonathonreilly/cl3-lattice-framework/pull/377) |
| 02 | Multi-site Pauli group P_N order 4^{N+1} | `axiom_first_cl3_per_site_uniqueness_theorem_note_2026-04-29` (retained) | 6/6 PASS | [#379](https://github.com/jonathonreilly/cl3-lattice-framework/pull/379) |
| 03 | Hopping bilinear H_{xy} = a_x^† a_y + h.c. Hermitian + translation-covariant | `axiom_first_lattice_noether_theorem_note_2026-04-29` (retained) | 7/7 PASS | [#381](https://github.com/jonathonreilly/cl3-lattice-framework/pull/381) |

## Quality

All three blocks have:
- exactly one retained-grade one-hop upstream dep on the live ledger today;
- zero admitted physics conventions (only mathematical / structural admitted-context inputs);
- machine-precision numerical verification (no nontrivial tolerances).

## Round-by-round R1 → R9 cumulative tally

| Round | Blocks | Cumulative |
|-------|--------|-----------|
| R1 | gluon massless, Pauli exclusion, CPT mass equality | 3 |
| R2 | momentum conservation, CPT lifetime, CMW low-d sublattice | 6 |
| R3 | fermion-number conservation, CPT² = I, q-q̄ meson singlet | 9 |
| R4 | per-site dim = 2, Wigner mode 2-dep, no per-site bosonic CCR | 12 |
| R5 | q-q-q baryon singlet, [P̂, Q̂] = 0, per-site j=1/2 spin | 15 |
| R6 | no per-site γ_5, T_a T_b = T_{a+b}, SU(3) C_2(3) = 4/3 | 18 |
| R7 | SU(3) C_2(adj) = 3, T_a O T_a^† = O(x+a), Q̂ integer spectrum | 21 |
| R8 | fermion parity Z_2 grading, Gell-Mann basis, Pauli group order 16 | 24 |
| R9 | d^{abc}, multi-site Pauli group, hopping bilinear validity | **27** |

**27 strict-bar positive-theorem retention candidates** produced under the new framework vocabulary across nine rounds.

## R9 highlight: completing the foundational toolkit

R9 closes three previously implicit but foundational structural facts that turn the framework's per-site / per-link algebra into ready-to-use lattice physics tools:

1. **d^{abc} symmetric structure constants** (Block 01). Companion to f^{abc} (R8 Block 02). Together they exhaust the SU(3) tensor decomposition: T^a T^b = (1/6) δ^{ab} I + (1/2)(d + i f) T^c. Every product of Gell-Mann generators — and hence every color tensor identity in QCD — reduces to combinations of these.

2. **Multi-site Pauli group P_N order = 4^{N+1}** (Block 02). The N-qubit Pauli group on the framework's N-site Fock space, structured as 1 → Z_4 → P_N → (Z_2 × Z_2)^N → 1. Multi-qubit generalization of R8 Block 03. This is the canonical N-qubit Pauli group used throughout multi-qubit stabilizer codes, surface codes, color codes, and fault-tolerant quantum computation.

3. **Hopping bilinear validity** (Block 03). The symmetric two-site hopping H_{xy} = a_x^† a_y + a_y^† a_x is Hermitian, translation-covariant, and Q-conserving. Therefore any sum over a translation-invariant link family is automatically a valid framework Hamiltonian. This is the building block of every tight-binding lattice model.

## Three foundational sectors fully closed

Through rounds R1-R9, three structural sectors of the framework are now fully closed at the retention-candidate level (awaiting Codex audit):

### Color sector (SU(3)_c)

| Fact | Block |
|------|-------|
| Generators basis (8-dim su(3)) | R8 Block 02 |
| Quark Casimir = 4/3 | R6 Block 03 |
| Gluon Casimir = 3 | R7 Block 01 |
| f^{abc} antisymmetric closure | R8 Block 02 |
| d^{abc} symmetric closure | R9 Block 01 |
| q-q̄ singlet 3 ⊗ 3̄ = 1 ⊕ 8 | R3 Block 03 |
| q-q-q baryon singlet | R5 Block 01 |
| Gluon masslessness | R1 Block 01 |

### Charge / fermion-parity sector (U(1)_Q)

| Fact | Block |
|------|-------|
| Q̂ integer spectrum on Fock | R7 Block 03 |
| [H, Q̂] = 0 conservation | R3 Block 01 |
| [P̂, Q̂] = 0 commute with momentum | R5 Block 02 |
| T_a Q̂_x T_a^† = Q̂_{x+a} covariance | R7 Block 02 |
| Z_2 fermion parity superselection | R8 Block 01 |

### Per-site Cl(3) algebraic sector

| Fact | Block |
|------|-------|
| Per-site dim = 2 | R4 Block 01 |
| Per-site spin = j = 1/2 | R5 Block 03 |
| No per-site γ_5 chirality | R6 Block 01 |
| No per-site bosonic CCR | R4 Block 03 |
| Wigner mode count linear in 2 | R4 Block 02 |
| Per-site Pauli group P_1 order 16 | R8 Block 03 |
| Multi-site Pauli group P_N order 4^{N+1} | R9 Block 02 |

### Translation / momentum sector

| Fact | Block |
|------|-------|
| [H, P̂] = 0 momentum conservation | R2 Block 01 |
| T_a T_b = T_{a+b} (faithful Z^3 rep) | R6 Block 02 |
| T_a O(x) T_a^† = O(x+a) covariance | R7 Block 02 |
| Hopping bilinear translation-invariance | R9 Block 03 |

### CPT / discrete symmetry sector

| Fact | Block |
|------|-------|
| CPT mass equality | R1 Block 03 |
| CPT lifetime equality | R2 Block 02 |
| (CPT)² = I | R3 Block 02 |

### CMW (continuous symmetry breaking)

| Fact | Block |
|------|-------|
| No SSB on 1D / 2D sublattices | R2 Block 03 |

## Process notes

- Pre-screening eliminated 0 candidates this round.
- All three blocks have machine-precision runners.
- Branch + PR for each block opened immediately after runner PASS.
- Block 03 had a convention error (bit-shift T direction vs site-shift, plus state-index encoding) that was caught and fixed before commit.
- Cumulative theorem note count: 27 fresh `THEOREM_NOTE_2026-05-02` documents across all rounds.

## Observation: campaign productivity remains steady

Across 9 rounds, each producing 3 strict-bar positive-theorem retention candidates, the rate has been stable. Pre-screening has not eliminated any candidate at the gate level since R1 (the original gate eliminations were before the audit-repair PR #306 that promoted A_min to retained). The retained authorities — particularly `axiom_first_cl3_per_site_uniqueness`, `axiom_first_lattice_noether`, `cl3_color_automorphism`, and `cpt_exact_note` — continue to support multiple downstream derivations each.

The campaign appears sustainable at this 3-blocks-per-round cadence indefinitely, with the queue of pre-screenable candidates remaining roughly steady as each new block opens up companion / generalization opportunities.

## Recommended pause point

After R9 (27 cumulative blocks across 5 fully-closed structural sectors), this is a natural cadence-checkpoint for the user to direct further work. Options:

1. **Continue strict-bar campaign R10+**: target Goldstone, Furry, Q quantization on quark sector, antiparticle Q-flip from CPT, etc. Pre-screening will determine viability.

2. **Pivot to interaction sector**: build retention candidates around four-fermion interactions, gauge-fermion coupling, Yukawa structure — likely require new admitted-context inputs.

3. **Pivot to support upgrading**: take support-status authorities (spin-statistics, RP, spectrum cond, cluster decomp) through Codex audit-acceleration to retained, opening up new dep options for downstream derivations.

4. **Stop and review**: assemble all 27 retention candidates into a unified summary document for paper / review.

The strict-bar discipline has delivered substantial fresh content; user input would help prioritize the next cycle.
