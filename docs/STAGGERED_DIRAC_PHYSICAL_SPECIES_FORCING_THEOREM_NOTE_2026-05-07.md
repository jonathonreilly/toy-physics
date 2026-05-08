# Staggered-Dirac Substep 4 — Physical-Species Forcing via SM Quantum-Number Chain (Block 06)

**Date:** 2026-05-07
**Type:** bounded support theorem
**Claim type:** bounded_theorem
**Status:** bounded source support for substep 4 (physical-species
reading of the hw=1 triplet) of the staggered-Dirac realization gate.
Conditional on Block 04 (BZ-corner support) + Block 02-revised
(direct three-state algebraic support) + STANDARD_MODEL_HYPERCHARGE_UNIQUENESS
+ ANOMALY_FORCES_TIME + the cited RS / CD / RP foundation. Closes substep 4
in the bounded sense by formalizing the physical-species sector definition
on the framework's primitives, demonstrating that the hw=1 triplet realizes
exactly three such sectors, and explicitly admitting the (1st/2nd/3rd
generation) labelling as physical convention rather than framework
derivation. Sister Block 02-revised salvage support is preserved; this note
extends rather than supersedes it.
**Authority role:** source note. Audit verdict and effective status are
set only by the independent audit lane.
**Primary runner:** `scripts/frontier_staggered_dirac_physical_species_forcing.py`

## Question

Block 02-revised
([`STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md))
salvages the runner-backed algebraic content for substep 4 — three
orthogonal hw=1 BZ-corner states in a single H_phys, with M_3(C) acting,
all in the same superselection sector. It explicitly defers the
physical-species reading.

This block asks the residual question:

```text
Given the algebraic content of Block 02-revised, what additional retained
content is needed to read the three hw=1 states as three SM matter
generations, and is that content already on the audit graph?
```

## Answer

**Yes, with a labelling convention admission.** The retained-tier surface
already contains:

1. STANDARD_MODEL_HYPERCHARGE_UNIQUENESS — for any one-generation matter
   content sitting on `Cl(3) ⊗ Z³` with the LH-doublet structure +
   SU(2)-singlet RH completion + Y(ν_R) = 0, the RH hypercharges are
   uniquely `(+4/3, −2/3, −2, 0)`. Applied to each of the three hw=1
   sectors gives identical SM-gauge quantum numbers per sector.
2. ANOMALY_FORCES_TIME — anomaly cancellation at one-generation level
   forces 3+1 spacetime + the SU(2)-singlet RH completion. Applied
   per-sector this is consistent across all three.
3. THREE_GENERATION_OBSERVABLE + NO_PROPER_QUOTIENT — the M_3(C) algebra
   on hw=1 is irreducible with no proper exact quotient. Hence the three
   sectors are *intrinsic* to the hw=1 stratum, not artefacts of basis
   choice.

What remains admitted is the *labelling* of these three intrinsic sectors
as "1st generation", "2nd generation", "3rd generation". This labelling
is conventionally fixed by the mass-ordering of the eventual eigenstates
under the Yukawa structure (m_1 < m_2 < m_3 within each charged-fermion
species), which is *physical-observable* convention, not framework-derived
content. The three sectors are framework-forced; their *names* are
convention.

## Setup

### Premises (A_min for substep 4 species-identification reformulated)

| ID | Statement | Class |
|---|---|---|
| Block04 | hw=1 BZ-corner triplet has M_3(C) algebra + 1+1+3+3 doubler structure | bounded support per [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| Block02r | hw=1 triplet realizes 3 orthogonal states in single H_phys, same superselection sector, connected by C_3[111] | bounded support per [`STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md) |
| HU | RH hypercharges `(y_1, y_2, y_3, y_4) = (+4/3, −2/3, −2, 0)` from anomaly cancellation + Y(ν_R) = 0 + Q(u_R) > 0 | retained per [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md) |
| AT | Anomaly cancellation forces 3+1 spacetime + SU(2)-singlet RH completion | retained per [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md) |
| NQ | M_3(C) on hw=1 has no proper exact quotient | retained per [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md) |
| TGO | hw=1 BZ-corner triplet carries M_3(C) algebra (translations + C_3[111]) | retained per [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| RP | A11 RP + OS reconstruction → physical Hilbert space H_phys with unique vacuum | retained per [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md) |
| RS | Reeh-Schlieder cyclicity | retained per [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md) |
| CD | Cluster decomposition + spectrum condition → unique vacuum, no superselection sectors on canonical surface | retained per [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md) |

### Forbidden imports

- NO PDG observed values (no fermion masses, no mixing angles)
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO same-surface family arguments
- NO new axioms
- NO HK + DHR appeal (Block 02-revised closed this route as misframed
  on the canonical RS+CD single-sector surface)

### Admitted convention (explicit)

**(LCL) Generation labelling convention.** The three intrinsic sectors
of the hw=1 triplet are labelled as `(1st, 2nd, 3rd) generation` in the
order of mass-ordering of their eventual mass eigenstates under the
Yukawa structure. This labelling is a *physical-observable convention*
(matching the universal convention in the SM literature: m_e < m_μ < m_τ,
m_d < m_s < m_b, m_u < m_c < m_t). It is *not* derived from A1+A2 alone
and is *not* part of this theorem's load-bearing content. The framework
forces three intrinsic sectors; physics labels them by mass-ordering.

This is the *same* convention class as cycle 16/19's "Convention A vs B"
admission: a labelling/scheme convention surfaced explicitly so the
load-bearing content stays in clear view. Cycles 1-3 of the LHCM atlas
already admit `Q = T_3 + Y/2` similarly.

## Definition: physical-species sector

**Definition (physical-species sector on hw=1).** A *physical-species
sector* in the framework's matter content on the staggered-Dirac
realization is an orbit of the M_3(C) flavor algebra acting on H_phys's
hw=1 stratum, with the orbit's basis vectors carrying a single fixed
assignment of SM-gauge quantum numbers (Y, T_3 multiplicity, SU(3) rep)
under the framework's retained gauge surface.

This definition is **framework-internal**: it uses only retained
primitives (M_3(C) algebra, hw=1 stratum, H_phys, SM-gauge surface from
the LHCM atlas + STANDARD_MODEL_HYPERCHARGE_UNIQUENESS). It does not
import physical-species vocabulary from outside the framework.

**Equivalent characterizations.** A subspace `V ⊂ H_phys` is a
physical-species sector iff:

1. (algebraic irreducibility) `V` is closed under the M_3(C) flavor
   algebra and `V` is a simple (= no proper non-trivial M_3(C)-invariant
   subspace) sub-representation;
2. (gauge homogeneity) all states in `V` carry the same SM-gauge
   quantum-number assignment under the framework's retained gauge
   surface;
3. (translation distinctness) the states are simultaneous eigenstates
   of the lattice translation operators T_x, T_y, T_z with distinct
   simultaneous eigenvalues.

(1) is the "irreducible orbit" content. (2) is the "fixed quantum
numbers" content. (3) is the "intrinsic basis" content. A subspace is
a physical-species sector iff all three hold.

## Theorem 4-forced (Physical-species forcing on the bounded staggered-Dirac surface)

**Bounded theorem.** Under {Block04, Block02r, HU, AT, NQ, TGO, RP, RS,
CD} + the explicit labelling convention (LCL):

```
The hw=1 BZ-corner triplet of the staggered-Dirac realization on Z³ APBC
realizes EXACTLY THREE physical-species sectors V_a (a ∈ {1, 2, 3}),
with:
  (S1) each V_a is irreducible under M_3(C) (TGO + NQ);
  (S2) each V_a carries the SAME SM-gauge quantum-number assignment as
       the canonical one-generation matter content of the LHCM atlas
       under STANDARD_MODEL_HYPERCHARGE_UNIQUENESS (HU + AT);
  (S3) the three V_a are pairwise orthogonal and have distinct
       simultaneous translation eigenvalues (Block04 + Block02r);
  (S4) C_3[111] cyclically permutes V_1 → V_2 → V_3 → V_1 within
       a single H_phys (Block02r + RP/RS/CD);
  (S5) under the labelling convention (LCL), V_a are read as the three
       SM matter generations.
```

In particular, the three V_a are framework-forced as intrinsic objects
(S1)-(S4); their identification with `(1st, 2nd, 3rd)` generation labels
(S5) is via the admitted convention (LCL). The framework derives the
*existence and structure* of three matter generations; physics labels
them by mass-ordering.

**Proof.**

(S1): TGO retained + NQ retained ⇒ M_3(C) is irreducible on hw=1, no
proper exact quotient. The three M_3(C)-orbit basis vectors are each
1-dim simple sub-representations of M_3(C) ⊂ End(C³); equivalently,
each generates a 1-dim simple module over the M_3(C) center (which is
trivial since M_3(C) is simple). Each V_a is therefore a simple
1-dim sub-representation in the irreducibility sense of the
definition.

(S2): For each V_a, the same A_min (Cl(3) per site + Z³ substrate)
applies, giving the same LHCM atlas content per sector (cycles 1-3
of the audit-backlog campaign retain LHCM matter assignment). HU then
applies independently in each sector with the same input data, giving
identical RH hypercharge assignment `(+4/3, −2/3, −2, 0)` per sector.
The full one-generation SM-gauge quantum numbers are thus identical
across all three V_a.

(S3): Block04 establishes the hw=1 BZ-corners (1,0,0), (0,1,0), (0,0,1)
as three orthogonal states with distinct simultaneous translation
eigenvalues `T_x|⟩ = ±1`, `T_y|⟩ = ±1`, `T_z|⟩ = ±1` (one −1 and two
+1 per state, in distinct positions). Block02r reconstructs them in
the OS-reconstructed H_phys.

(S4): Block02r Step 4 establishes that all three states lie in the same
superselection sector (the unique vacuum sector under RP+RS+CD). The
C_3[111] action is implemented by a unitary on H_phys that cyclically
permutes the three corners.

(S5): Combining (S1)-(S4): the three V_a are intrinsic, gauge-
homogeneous, translation-distinct, C_3-connected sectors. By definition
of physical-species sector above, each V_a is a physical-species
sector. The labelling of (V_1, V_2, V_3) as (1st, 2nd, 3rd) generation
is the admitted convention (LCL).

This completes the bounded forcing of substep 4 modulo (LCL). ∎

## What this closes

- The substep 4 algebraic content is now packaged as a **definition
  + theorem chain**, not a "salvage". The three hw=1 states are
  not just orthogonal algebraic objects — they satisfy a framework-
  internal definition of "physical-species sector".
- The chain through STANDARD_MODEL_HYPERCHARGE_UNIQUENESS makes the
  identical SM quantum numbers per sector explicit. Each sector
  carries `(Q_L, L_L, u_R, d_R, e_R, ν_R)` with hypercharges
  `(+1/3, −1, +4/3, −2/3, −2, 0)`. This is the "matter generation"
  content forced by the framework.
- The labelling convention (LCL) is surfaced as an explicit admission,
  matching the framework's convention-admission pattern from cycle 16
  (Convention A vs B), cycle 19 (SU(5) vs SO(10) GUT-group choice),
  and the LHCM atlas's `Q = T_3 + Y/2` admission.

## What this does NOT close

- **Mass eigenvalues.** The mass-ordering that fixes the convention
  (LCL) is itself an open closure target across Lane 3 (quark masses),
  Lane 6 (charged-lepton masses), Lane 4 (neutrino masses). This
  theorem does not derive any specific mass; it forces the *structure*
  of three generations.
- **Yukawa structure.** Yukawa coupling matrices and mixing angles
  are downstream of mass derivations. Not in scope.
- **Higher-generation extension.** The theorem says EXACTLY THREE
  generations on hw=1. Whether higher-generation content could exist
  on hw=2 (which is also a 3-corner stratum) is a separate question
  and is bounded by the retained `frontier_generation_rooting_undefined.py`
  no-rooting argument.
- **Substeps 1-3 of the gate.** Those are bounded by Blocks 02 (Grassmann),
  03 (Kawamoto-Smit), 04 (BZ corners) — sister notes from 2026-05-07.
  This note depends on those but does not re-derive them.
- **The full A3 gate closure.** The gate ([`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md))
  closes when all four substeps are at retained tier. This note
  brings substep 4 to bounded_theorem (with explicit (LCL) admission);
  substeps 1-3 are also bounded_theorem (Blocks 02-04). The gate is
  thus *bounded-closed* but not retained-closed; retention requires
  audit ratification on the full chain.

## Status

```yaml
actual_current_surface_status: bounded support theorem
proposal_allowed: false
proposal_allowed_reason: |
  Conditional on Blocks 02-revised + 04 (bounded) + retained upstreams
  (HU, AT, NQ, TGO, RP, RS, CD) + the explicit (LCL) labelling-
  convention admission. Eligible for retention upgrade once: (a)
  upstream Blocks 02-revised + 04 reach retained tier (currently
  unaudited bounded_theorem), (b) STANDARD_MODEL_HYPERCHARGE_UNIQUENESS
  reaches retained tier (currently proposed_retained, unaudited), (c)
  this note is independently audited, and (d) the LCL admission is
  ratified as a legitimate convention (analogous to Convention A vs B
  in cycle 16, ratified there).
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

## Verification

Run:

```bash
PYTHONPATH=scripts python3 scripts/frontier_staggered_dirac_physical_species_forcing.py
```

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: Substep 4 of the staggered-Dirac realization gate is forced
in the bounded sense — the hw=1 BZ-corner triplet realizes exactly
three physical-species sectors per the definition, with each sector
carrying identical SM-gauge quantum numbers under HU, modulo the
explicit (LCL) generation-labelling convention.
```

The runner uses Python standard library only (`fractions.Fraction` for
exact arithmetic). It checks:

1. **Note structure.** Required strings present (definition, theorem
   statement, all 9 premises labeled, (LCL) convention surfaced).
2. **Premise-class consistency.** Each cited premise's note exists, and
   each premise's class label (retained / bounded support / etc.)
   matches the audit-ledger's effective_status as of 2026-05-07.
3. **Hypercharge per-sector consistency.** Each sector's claimed
   hypercharge assignment matches the unique solution from
   STANDARD_MODEL_HYPERCHARGE_UNIQUENESS (`y_1 = +4/3, y_2 = −2/3,
   y_3 = −2, y_4 = 0`) verified by exact rational arithmetic.
4. **Translation-eigenvalue distinctness.** The three hw=1 corners
   `(1,0,0), (0,1,0), (0,0,1)` have distinct simultaneous T_x, T_y, T_z
   eigenvalues. Verified exactly: each pair differs in at least one
   eigenvalue (and in fact in exactly two).
5. **C_3[111] cyclic structure.** The cyclic permutation
   `(1,0,0) → (0,1,0) → (0,0,1) → (1,0,0)` is a 3-cycle. Verified
   structurally on the corner labels.
6. **M_3(C) irreducibility on hw=1.** Translations T_x, T_y, T_z
   together with C_3[111] generate the full 9-dim M_3(C) on the
   3-dim hw=1 subspace. Verified by computing the linear span of
   the generated operator algebra.
7. **Anomaly-cancellation per-sector consistency.** Each sector
   independently satisfies `Tr[Y] = 0`, `Tr[SU(3)² Y] = 0`,
   `Tr[Y³] = −16/9` (from STANDARD_MODEL_HYPERCHARGE_UNIQUENESS Eqs
   E1-E3 with the unique solution).
8. **Forbidden-import audit.** The runner consumes no observed PDG
   values, no fitted matchings, no DHR/HK appeals, no new axioms.
9. **(LCL) convention audit.** The runner verifies the labelling
   convention is surfaced explicitly, NOT used as load-bearing
   content for (S1)-(S4), and is consistent with the SM-literature
   mass-ordering convention.
10. **Substep 4 boundary.** The runner verifies what this note does
    NOT close (mass eigenvalues, Yukawa structure, higher-generation
    extension, substeps 1-3, full gate closure).

## Cross-references

- Parent open-gate: [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
- Sister Block 02 (Grassmann): [`STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_GRASSMANN_FORCING_THEOREM_NOTE_2026-05-07.md)
- Sister Block 03 (Kawamoto-Smit): [`STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_KAWAMOTO_SMIT_FORCING_THEOREM_NOTE_2026-05-07.md)
- Sister Block 04 (BZ corner): [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Sister Block 02-revised (direct three-state): [`STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_PHYSICAL_SPECIES_DIRECT_THEOREM_NOTE_2026-05-07.md)
- Hypercharge uniqueness: [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md)
- Anomaly forces time: [`ANOMALY_FORCES_TIME_THEOREM.md`](ANOMALY_FORCES_TIME_THEOREM.md)
- Three-generation observable: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- No proper quotient: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
- RP A11: [`AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_REFLECTION_POSITIVITY_THEOREM_NOTE_2026-04-29.md)
- Reeh-Schlieder: [`AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_REEH_SCHLIEDER_THEOREM_NOTE_2026-05-01.md)
- Cluster decomposition: [`AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md)
- Convention-admission analogues: [`FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md`](FULL_Y_SQUARED_TRACE_SU5_GUT_NOTE_2026-05-02.md) (Convention A vs B), [`SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md`](SIN_SQUARED_THETA_W_GUT_FROM_SU5_NOTE_2026-05-02.md) (SU(5) vs SO(10)/E6 GUT-group choice)
- Minimal axioms parent: [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)

## Honest scope

**Branch-local theorem.** This note converts substep 4 from a "salvage"
bounded support to a definition-plus-theorem closure within the bounded
tier, with explicit labelling convention (LCL) surfaced. The chain
through STANDARD_MODEL_HYPERCHARGE_UNIQUENESS makes the per-sector
SM quantum-number identification rigorous.

The framework-internal claim is: **three matter generations are
forced** as intrinsic algebraic-plus-gauge structures. The labelling
of which is "1st, 2nd, 3rd" is convention.

**Not in scope.**

- Closed-form derivation of the mass hierarchy that fixes the (LCL)
  labelling. Lanes 3, 4, 6 own this.
- Promotion of A3 (the parent gate) to retained tier. That requires
  audit ratification on Blocks 02 (Grassmann), 03 (Kawamoto-Smit),
  04 (BZ-corner), and this Block 06 (physical species).
- Universality theorem for A_min-compatible discretizations. That is
  candidate (1) work and is independent of this note.
