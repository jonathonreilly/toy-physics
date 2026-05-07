# Route Portfolio — Staggered-Dirac Realization Gate

**Date:** 2026-05-07

## Block 02 candidate routes (Substep 1: Grassmann partition forcing)

### R1.A — Spin-statistics S2 packaging (PRIMARY)

**Premise:** the spin-statistics theorem (S2) already proves the
Grassmann-forcing argument — bosonic 2nd quantization on a Cl(3) site
gives infinite-dim Fock incompatible with finite Cl(3) dim 2 module.
This is exactly what the gate's substep 1 needs.

**Method:** package spin-statistics S2 as the substep-1 forcing
theorem for the staggered-Dirac realization gate. Two contributions:
1. Re-state S2 specifically as "A1+A2 + finite Cl(3) dim 2 → matter
   measure must be Grassmann"
2. Verify that the spin-statistics dependency on Cl(3) per-site
   uniqueness (post-2026-05-03 chirality repair) is consistent

**Risk:** spin-statistics note is "support — awaiting re-audit". May
need re-audit before becoming load-bearing. Block 02 produces an
audit-ready packet.

**V1-V5 gate:**
- V1: closes substep 1 of staggered-Dirac realization gate
- V2: explicit packaging of spin-statistics S2 as substep-1 forcing
- V3: audit lane could combine spin-statistics + per-site dim 2 +
  gate parent, but this PR does it cleanly
- V4: marginal content non-trivial — closes one of four substeps
- V5: not a one-step variant — first explicit substep packaging

**PASS V1-V5.**

## Block 03 candidate routes (Substep 2: Kawamoto-Smit phase forcing)

### R2.A — Chirality-grading forcing (PRIMARY)

**Premise:** the staggered-Dirac kinetic structure on Z³ has Kawamoto-
Smit phases η_μ(n) given by:
- η_1 = 1
- η_2(n) = (−1)^{n_1}
- η_3(n) = (−1)^{n_1 + n_2}

These can be derived from requiring the kinetic operator anticommute
with the sublattice parity ε(x) = (−1)^{n_1 + n_2 + n_3}. Chirality
grading on the matter sector (per `FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02`)
is the retained Z_2 grading. Combining with `frontier_generation_rooting_undefined`
irreducibility on C^8: the phase choice is unique up to gauge equivalence.

**Method:**
1. Show that chirality-anticommutation `{ε, M_KS} = 0` constrains η_μ(n)
2. Show that on the four sublattices labeled by (n_1, n_2 mod 2),
   the constraint reduces to a finite linear-algebra problem
3. Solve the LAS to find η_μ(n) up to global signs / boundary phases
4. Show that the solution is exactly Kawamoto-Smit (or unique up to
   trivial gauge)

**Risk:** the actual solving may have a multi-parameter family. Need
to check whether the rooting-no-go irreducibility narrows it.

### R2.B — BZ-momentum forcing (alternative)

**Premise:** the BZ-corner doubling structure (8 corners on Z³ with
APBC) has a specific chirality assignment per Hamming weight. The
Kawamoto-Smit phases are precisely the staggered phases that produce
this BZ-corner structure with the correct chirality grading.

**Method:** start from the desired BZ-corner output (1+1+3+3) and
work backwards to the unique phase choice. This is REVERSE engineering;
it's a consistency check but not a forcing argument.

**Status:** secondary; useful as cross-validation but not primary.

## Block 04 candidate routes (Substep 3: BZ-corner three-generation forcing)

### R3.A — Hamming-weight Brillouin-zone decomposition (PRIMARY)

**Premise:** the staggered-Dirac kinetic operator on Z³ with APBC has
8 BZ corners labeled by `(±π/2, ±π/2, ±π/2)`. Under the chirality
grading and the Kawamoto-Smit phase structure (Block 03), the corners
decompose by Hamming weight:
- HW=0: 1 corner — singlet
- HW=1: 3 corners — three-generation triplet
- HW=2: 3 corners — anti-triplet
- HW=3: 1 corner — anti-singlet

The retained `frontier_generation_fermi_point.py` confirms this
spectral structure. The forcing argument: under chirality + Z³
substrate + Kawamoto-Smit phases, the 8-corner decomposition is unique.

**Method:**
1. Derive the 8 BZ corners from Z³ APBC (standard staggered-fermion
   doubler counting)
2. Apply chirality grading: corners group by parity of Σ k_i / (π/2)
3. Apply Hamming-weight distinction within parity sectors
4. Confirm the 1+1+3+3 structure

### R3.B — S_3 representation-theoretic forcing (alternative)

The `S3_TASTE_CUBE_DECOMPOSITION_NOTE` shows C^8 ~= 4 A_1 + 2 E under
S_3 permutations of taste indices. Combined with the Z_2 sublattice
grading, this gives a unique decomposition: hw=1 carries the
3-dim "standard" rep + 1-dim "trivial" rep, with the 3-dim being
the three generations.

## Block 05 candidate routes (Substep 4: Physical-species bridge)

### R4.A — Observable-descent + Hilbert/locality/info (PRIMARY)

**Premise:** the retained `THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT`
shows that the M_3(C) algebra on hw=1 has no proper exact quotient.
The physical-species reading requires that observable separability +
no-quotient → distinct physical species sectors on the accepted
Hilbert/locality/information surface. This is largely captured by
`PHYSICAL_LATTICE_NECESSITY_NOTE` (substrate-level reading retained)
+ the observable-descent lemma.

**Method:** package the observable-descent + no-proper-quotient + 
PHYSICAL_LATTICE_NECESSITY into a single closure step.

**Risk:** the open gate note explicitly says this step is "out-of-scope
admitted-context" in `GENERATION_AXIOM_BOUNDARY_NOTE`. Closing it may
require a specific Hilbert-space-semantics argument not yet retained.

## Block 06 — Synthesis

### R5.A — Single canonical-parent positive theorem (PRIMARY)

If Blocks 02-05 succeed: synthesize into a single canonical-parent
positive theorem that runs (1)-(4) end-to-end on A1+A2.

### R5.B — Consolidated obstruction note (FALLBACK)

If any substep doesn't close: produce a sharp obstruction note
identifying the precise remaining gap. Acceptable outcome under
no-new-axiom rule.

## Ranking by retained-positive probability

| Block | Route | Retained-positive prob | Runtime | Risk |
|---|---|---|---|---|
| 02 | R1.A spin-statistics packaging | HIGH | 60-90m | LOW (pieces retained) |
| 03 | R2.A chirality-grading forcing | MEDIUM | 90m | MEDIUM (LAS may have multi-parameter family) |
| 04 | R3.A HW-BZ decomposition | HIGH | 60-90m | LOW (pieces retained) |
| 05 | R4.A physical-species bridge | MEDIUM | 60-90m | MEDIUM (admitted-context gap) |
| 06 | R5.A canonical parent | HIGH (after 02-05) | 60m | LOW |

## Selection for execution

**Block 02 → R1.A first** (spin-statistics packaging, lowest risk).
Then Blocks 03, 04, 05 in sequence. Block 06 synthesizes.

If Block 02 succeeds quickly, accelerate to Block 03 (highest-risk
substep). Reserve Block 06 synthesis for end-of-runtime.
