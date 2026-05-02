# GOAL — Positive-Theorem-Only Retained-Grade Campaign

**Date:** 2026-05-02
**Slug:** `positive-only-retained-20260502`
**Mode:** campaign
**Strict bar:** every block must qualify as `claim_type = positive_theorem` and route to `effective_status = retained` under the scope-aware classification framework adopted 2026-05-02 (PR #291).

## Strict acceptance criteria

A candidate target survives pre-screening only if all four hold:

1. The proof has a single positive load-bearing statement (no narrow bounded scope).
2. Every load-bearing dependency is at `effective_status ∈ {retained, retained_no_go, retained_bounded}` on the **live audit ledger today**, not "Codex audited_clean awaiting framework-adoption sweep".
3. No load-bearing admitted-context **physics** input (Killing horizons, NEC, Wald-Noether admission, Bisognano-Wichmann admission, Bardeen-Carter-Hawking integrability, etc.). Pure mathematical admissions (Γ-function identities, group theory, basic linear algebra, complex analysis) are allowed.
4. The runner has classifiable PASS lines that demonstrate the positive_theorem at the structural level (class C first-principles compute, not just A algebraic identities or G numerical matches).

## Pre-screening result (2026-05-02)

Surveyed eight candidate targets against the live ledger:

| Candidate | Result | Why |
|---|---|---|
| photon_masslessness | DROP | Standard derivation needs A_min directly (audited_conditional) and one_generation_matter_closure_note (audited_conditional) to fix the matter content. Could be redone but path unclear. |
| gluon_masslessness | KEEP — Block 1 | Tree-level bare gluon mass forbidden by retained SU(3) gauge invariance. Deps: native_gauge_closure_note (retained_bounded) + graph_first_su3_integration_note (retained_bounded). Both chain-clean. |
| conservation_electric_charge | DROP | yt_ward_identity_derivation_theorem is `audited_renaming` — load-bearing dep is itself a renaming verdict. |
| charge_quantization {0, ±1/3, ±2/3, ±1} | DROP | standard_model_hypercharge_uniqueness_theorem and fractional_charge_denominator_from_n_c_theorem are both `unaudited` on live ledger. |
| Gell-Mann-Nishijima Q = T_3 + Y/2 | DROP | Same as above — hypercharge uniqueness is unaudited. |
| Furry's theorem | DROP | Needs C-symmetry on QED matter content; one_generation_matter_closure_note is audited_conditional. |
| Goldstone's theorem on SSB | DROP | No clean retained SSB target available; Higgs-related notes are unaudited or conditional. |
| energy_momentum_conservation | DROP | Lattice Noether is retained, but the standard derivation also needs minimal_axioms_2026-04-11 directly (audited_conditional). |

Two new candidates surface from the survey of the 147 retained rows:

| Candidate | Result | Why |
|---|---|---|
| pauli_exclusion_principle | KEEP — Block 2 | Single-line consequence of axiom_first_spin_statistics_theorem (retained). |
| cpt_particle_antiparticle_mass_equality | KEEP — Block 3 | Standard CPT consequence on cpt_exact_note (retained). |

## Initial 3-block queue

1. Gluon masslessness from retained SU(3) gauge invariance
2. Pauli exclusion principle from retained spin-statistics
3. Particle/antiparticle mass equality from retained CPT exact theorem

If the campaign has time after Block 3, do a **stretch survey** for additional positive_theorem candidates among the 147-row retained set + 169-row retained_bounded set. Target may be e.g.:

- additional spin-statistics consequences (anti-symmetry of multi-fermion states; positivity of Grassmann determinants)
- additional CPT consequences (equal lifetimes; equal magnetic moments)
- Coleman-Mermin-Wagner extensions (no continuous SSB in d ≤ 2)
- lattice Noether currents in specific cases

## Out of scope

- Anything from the previous 24h thermo campaign (Blocks 01-10)
- Any target requiring upstream not yet at retained / retained_bounded today
- Any target with admitted physics inputs that would force bounded_theorem
- BH thermodynamics, Hawking radiation, Unruh effect, etc.

## Stop conditions

- Runtime exhausted
- Queue exhausted (every viable retained-positive candidate is blocked)
- Pre-screen failure rate exceeds 80% across 5 consecutive candidates
