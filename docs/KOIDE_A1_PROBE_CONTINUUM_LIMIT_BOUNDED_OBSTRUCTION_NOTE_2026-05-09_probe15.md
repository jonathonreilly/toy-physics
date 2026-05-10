# Koide A1 Probe 15 — Continuum-Limit Hypothesis for U(1)_b Closure

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Status:** source-note proposal — Probe 15 closure attempt for the A1
amplitude-ratio admission via continuum / scaling / thermodynamic / RG
limits of retained Cl(3)/Z³ content. Per Probe 14's residue, the missing
primitive is "the continuous extension of retained discrete C_3 to U(1)_b
on the b-doublet of A^{C_3} — equivalently, a 1-parameter linear action
on the C_3-character-graded vector space that is NOT an algebra
automorphism." This probe asks whether ANY retained continuum / scaling
/ thermodynamic / RG limit produces the U(1)_b — explicitly forbidding
new axioms or external imports per user 2026-05-09 clarification.
**Authority role:** source-note proposal; effective status set only by
the independent audit lane.
**Loop:** koide-a1-probe15-continuum-limit-20260509
**Primary runner:** [`scripts/cl3_koide_a1_probe_continuum_limit_2026_05_09_probe15.py`](../scripts/cl3_koide_a1_probe_continuum_limit_2026_05_09_probe15.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_continuum_limit_2026_05_09_probe15.txt`](../logs/runner-cache/cl3_koide_a1_probe_continuum_limit_2026_05_09_probe15.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner.

## Naming-collision warning

In this note:
- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"A1-condition"** = the Brannen-Rivero amplitude-ratio constraint
  `|b|²/a² = 1/2` for the `C_3`-equivariant Hermitian circulant
  `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`.

These are distinct objects despite the shared label.

## Constraint (per user 2026-05-09 clarification)

**No new axioms. No external imports.** Closure must come from:

  (i) An already-retained limit operation that produces U(1)_b on the
      b-doublet, OR
  (ii) A derivation of U(1)_b from existing cited source-stack content via a
       continuum / scaling / thermodynamic / RG limit operation.

Option (iii) — admit U(1)_b as a new primitive — is OFF the table for
this probe.

**Critical retained constraint** (per
[`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)):
every retained radian on Cl(3)/Z_3 + d=3 is `(rational) × π`. Any
continuum-limit derivation of U(1)_b must respect this AT FINITE
LATTICE; the continuous group can only emerge IN THE LIMIT.

## Question

Does any retained continuum / scaling / thermodynamic / RG limit of the
Cl(3)/Z³ framework extend the discrete `C_3[111]` cyclic group on hw=1
to a continuous `U(1)_b` on the b-doublet of `A^{C_3}`?

## Answer

**No.** Nine candidate limits examined; none produces U(1)_b. The
structural reason: the C_3 cyclic-shift is a **finite combinatorial
group on {0,1}³ BZ-corner indices**, intrinsic to the lattice direction
labeling. Retained limits act on **metric / geometric / coupling
parameters**: lattice spacing (L1), volume (L2), temperature (L3, L4),
effective coupling (L5, L8), Hilbert-space size (L7, L9), and discrete
subgroup density (L6). Combinatorial groups cannot be extended to Lie
groups by metric / geometric / coupling limits — the structures are
incompatible in kind.

Furthermore, `phi_theta` (the closure-target U(1)_b action) is **not
realizable by any conjugation `X → U X U*`** for generic theta, ruling
out the entire class of conjugation-implemented continuous symmetries
that any retained limit could produce.

## Setup

### Closure target (Probes 13, 14 residue)

The U(1)_b "vector action" `φ_θ` on `A^{C_3}` (Hermitian circulants):

```
φ_θ(I)  = I             (weight 0 under C_3 grading)
φ_θ(C)  = e^{+iθ} C     (weight +1, ω-isotype)
φ_θ(C²) = e^{-iθ} C²    (weight -1, ω̄-isotype)
```

Equivalently on `H = aI + bC + b̄C²`:

```
φ_θ(H) = aI + e^{iθ} b C + e^{-iθ} b̄ C²
```

Probe 14 verified: `φ_θ` is **not** an algebra automorphism (preserves
multiplication only at θ ∈ {0, 2π/3, 4π/3}). It is a **linear shift on
the C_3-character grading**, not multiplicative.

### Retained continuum / scaling / thermal / RG content

The framework retains the following limit operations (cited):

- **Lattice-spacing continuum limit** `a → 0`
  ([`CONTINUUM_LIMIT_NOTE.md`](CONTINUUM_LIMIT_NOTE.md), 2026-04-05;
  [`CONTINUUM_BRIDGE_NOTE.md`](CONTINUUM_BRIDGE_NOTE.md))
- **Thermodynamic limit** `|Λ| → ∞` (standard)
- **Thermal / KMS limit** at any `β_th > 0`
  ([`AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md))
- **Wilsonian effective action** (gauge sector retained as
  `<P> → α_LM` running, per Block 03 / 04)
- **Pendleton-Ross IR QFP** for `y_t` (colored Yukawa, retained)
- **Per-site continuous SU(2)** on Cl(3) ≅ M_2(C) (framework property)
- **Discrete C_3 character iteration** (Z_3 subgroup of would-be U(1))

### Forbidden imports

- NO PDG observed values used as derivation input
- NO new axioms (per user 2026-05-09 clarification)
- NO external imports (string theory, NCG primitives, U(3) family
  gauge bosons, spectral action, Sumino tuning, etc.)

## Per-limit candidate analysis

Each limit tested for:
- **C1 (existence)**: limit is cited source-stack content?
- **C2 (matter-sector reach)**: limit acts on M_3(C) on hw=1?
- **C3 (continuous extension of C_3)**: produces 1-parameter family
  containing C_3?
- **C4 (non-algebraic linear action)**: produces `φ_θ` linear shift on
  character grading (not algebra automorphism)?
- **C5 (closure of A1)**: forces `|b|²/a² = 1/2`?

| # | Limit | C1 | C2 | C3 | C4 | C5 | Reason for failure |
|---|---|---|---|---|---|---|---|
| L1 | `a → 0` lattice continuum | ✓ | ✓ | ✗ | ✗ | ✗ | C_3 acts on combinatorial corner indices `{0,1}³`; intrinsic, not a-dependent |
| L2 | `|Λ| → ∞` thermodynamic | ✓ | ✓ | ✗ | ✗ | ✗ | volume scales fiber multiplicity; per-fiber M_3(C) algebra is fixed |
| L3 | `β_th → 0` infinite-T KMS | ✓ | ✓ | ✗ | ✗ | ✗ | maximally-mixed state IS φ_θ-invariant but invariance ≠ algebra action |
| L4 | `β_th → ∞` ground-state | ✓ | ✓ | ✗ | ✗ | ✗ | ground state depends on full (a, b); φ_θ permutes Gibbs states (not symmetry) |
| L5 | Wilsonian effective action | admissible | ✗ | ✗ | ✗ | ✗ | hw=1 has no internal mode hierarchy; renormalization preserves algebra |
| L6 | Z_3 → U(1) rationality density | discrete only | n/a | ✗ | ✗ | ✗ | discrete Z_3 has 3 elements (not dense); rational-π multiples are countable, NOT a Lie subgroup |
| L7 | Per-site SU(2) qubit projection | ✓ | partial | ✗ | ✗ | ✗ | per-site U(1) projects to global phase on hw=1; trivial conjugation on circulants |
| L8 | Matter-sector RG IR/UV | partial | ✓ | ✗ | ✗ | ✗ | Probe 5 confirmed: no retained matter-sector RG flow on `|b|²/a²`; SM-like flow preserves arg(b) |
| L9 | Large-N spectral / replica | n/a | ✗ | ✗ | ✗ | ✗ | hw=1 fixed at 3-dim by retained no-proper-quotient; SU(3) is fixed N=3 |

**Universal failure mechanism (Test C3 across all 9 limits)**: the
C_3 cyclic shift on hw=1 is a finite combinatorial subgroup of GL(3, ℂ)
intrinsic to the BZ-corner indexing on `{0,1}³`. It permutes the three
spatial direction labels {x, y, z}. This is a **combinatorial /
discrete group property**, not a metric / geometric / coupling
property. Retained continuum / scaling / thermal / RG limits act on
parameters that scale metric / geometric / coupling structure: they do
not act on the combinatorial index structure. **A finite combinatorial
group cannot be extended to a continuous Lie group by any limit on
metric parameters.**

**Universal failure mechanism (Test C4 across all 9 limits)**: even if
some limit could produce a U(1)-class symmetry on M_3(ℂ), the closure
target `φ_θ` is **not realizable by any conjugation** `X → U X U*` for
generic theta. Proof (Section 10 of runner): in the C-eigenbasis,
`U(theta) = diag(1, e^{iθ}, e^{-iθ})` is the natural Lie homomorphism
`U(1) → GL(3, ℂ)` extending C_3. Its conjugation action on circulants
(which are diagonal in this basis) is **trivial**. So the natural
extension acts trivially. Conversely: any conjugation must preserve
eigenvalues of `C` (similarity-invariant), but `φ_θ(C) = e^{iθ} C` has
eigenvalues `e^{iθ}{1, ω, ω̄}` which differ from `{1, ω, ω̄}` for
theta ∉ {0, 2π/3, 4π/3}. Therefore `φ_θ` is structurally not a
conjugation-class action.

**All retained continuous symmetries act by conjugation** (Probe 14
candidates 1-9 all fail Test 4 by this same mechanism). This rules out
every retained limit as a source for `φ_θ`.

## Closest miss analysis

Three limits come closest to U(1)_b without producing it:

### Closest miss 1: L6 (Z_3 rationality density)

The discrete `C_3 = Z_3` is exactly the discrete subgroup we want to
extend. **The extension operation is what is missing**:
- `{1, C, C²}` is a 3-element group, not dense in U(1).
- Per the retained no-go, the ACCESSIBLE radians are rational-π
  multiples — countably many, dense in [0, 2π) but not equal to it.
- Even a dense countable subgroup is **not a Lie subgroup** (no
  differentiable structure).
- `Z_3 ⊂ U(1)` is just a subgroup inclusion; it doesn't generate U(1)
  by "taking a limit" — limit operations preserve cardinality of the
  continuous structure, they don't create it.

This is the **closest miss with the sharpest structural failure**:
the discrete-to-continuous extension is precisely what no retained
limit operation supplies.

### Closest miss 2: L3 (high-T KMS)

The maximally-mixed Gibbs state `ρ_0 = I/3` IS `φ_θ`-invariant
(verified algebraically: `Tr(ρ_0 · φ_θ(X)) = Tr(X)/3 = Tr(ρ_0 · X)`).
The U(1)_b-invariant readout (via reduced (ρ_+, ρ_⊥)) IS available at
the readout level by construction. **But invariance of state/readout
is not algebra action**. For finite β_th > 0, the Gibbs state is NOT
φ_θ-invariant (φ_θ(H) ≠ H, so e^{−β_th φ_θ(H)} ≠ e^{−β_th H}).

This is the FUNCTIONAL-PIVOT direction (Probe 14 Strategic Option 2):
the U(1)_b can be enforced AT THE Q-READOUT level, not at the algebra
level. A separate derivation is needed to convert this into an A1
closure.

### Closest miss 3: L7 (per-site SU(2) qubit)

Framework property "continuous in qubit operations" applies to
single-site Cl(3) ≅ M_2(C). The hw=1 carrier is a **three-site
collective** (one BZ corner per spatial direction). The C_3-equivariant
diagonal U(1) ⊂ SU(2)^3 acts as a global phase on hw=1 → trivial
conjugation on circulants. Per-site continuity does not assemble into
a non-trivial multi-site U(1)_b on hw=1 by any retained projection.

This is the same failure mode as Probe 14 candidate 5 (per-site qubit
phase) reconfirmed: per-site continuity is **single-site**, not
multi-site collective.

## Theorem (Probe 15 sharpened bounded obstruction)

**Theorem.** On A1 + A2 + retained C_3-action on hw=1 + retained M_3(ℂ)
on hw=1 + retained Frobenius block-total + retained continuum / scaling
/ thermal / RG limits + retained no-proper-quotient + retained
KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO + retained MRU weight-class structure:

```
(a) The C_3 cyclic shift on hw=1 is a finite combinatorial subgroup
    of GL(3, ℂ), intrinsic to the BZ-corner indexing {0,1}^3. It is
    independent of lattice spacing, volume, temperature, coupling,
    and Hilbert-space size — every retained limit-operation parameter.
    [Proved structurally; runner Sections 1-9, 10.]

(b) The natural Lie homomorphism U(1) -> GL(3, C) extending C_3 is
    U(theta) = diag(1, e^{i theta}, e^{-i theta}) in the C-eigenbasis.
    Its conjugation action on circulants is TRIVIAL.
    [Verified algebraically; runner Section 10.4.]

(c) phi_theta (the closure target) is NOT realizable by any
    conjugation X -> U X U^* for generic theta. The eigenvalues of
    phi_theta(C) = e^{i theta} C are {e^{i theta}, e^{i theta} omega,
    e^{i theta} omega_bar}, which differ from eigenvalues of C
    {1, omega, omega_bar} unless theta in {0, 2pi/3, 4pi/3}.
    [Verified algebraically; runner Sections 10.5, 10.6.]

(d) Every retained continuous symmetry acts by conjugation
    (Probe 14 confirmed across 9 retained U(1) candidates). By (c),
    no retained continuous symmetry can produce phi_theta.
    [Probe 14 dependency; reconfirmed in runner Section 10.7.]

(e) For each of 9 retained limit operations (L1-L9) covering
    lattice-spacing, volume, temperature (high+low), Wilsonian,
    Z_3 density, per-site qubit, RG, large-N: the limit FAILS to
    produce phi_theta by combination of mechanisms (a)-(d).
    [Verified per-limit; runner Sections 1-9.]

Therefore: no retained continuum / scaling / thermal / RG limit
extends the discrete C_3 to U(1)_b on the b-doublet of A^{C_3}. The
A1-condition closure attempt via continuum-limit hypothesis returns
SHARPENED bounded obstruction. The Probe 14 residue is UPHELD with
an added structural-impossibility argument:

  "No retained continuum / scaling / thermal / RG limit produces the
   continuous extension of retained discrete C_3 to U(1)_b. The
   missing primitive is structurally distinct in kind from any
   retained limit operation."

The A1 admission count is unchanged. No new admission is proposed by
this probe.
```

**Proof sketch.** (a) follows from the Block 03 / 04 forcing chain
([`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)):
the C_3[111] cyclic generator acts on the BZ-corner index labels
`(n_x, n_y, n_z) ∈ {0,1}³`, which is a combinatorial structure on a
3-element index set. This labeling is independent of the metric
parameters of the lattice. (b) is a direct algebraic computation:
in the C-eigenbasis, circulants are diagonal, and conjugation by
diagonal matrices preserves diagonal matrices identically. (c) follows
from invariance of eigenvalues under similarity transforms. (d)
restates Probe 14's universal failure mode. (e) is verified in the
runner by per-limit explicit numerical / algebraic checks (Sections
1-9). ∎

## Convention-robustness check

- **Scale-invariance** of `|b|²/a²` under `H → cH`. ✓
- **Basis change** `C → C^{-1} = C²` preserves C_3-action and isotype
  structure. ✓
- **K-action consistency** with C_3: `K(α_g(X)) = α_g(K(X))` ✓ (since
  C is real).
- **Conditional expectation** projects onto circulants. ✓

The combinatorial / metric distinction underlying Probe 15's universal
failure is **convention-robust**: it holds in any basis, at any scale,
under any retained involution.

## Sharpened residue

After Probes 12, 13, 14, 15, the missing primitive is precisely:

> **"The continuous extension of retained discrete `C_3` to U(1)_b on
> the b-doublet of `A^{C_3}` — equivalently, a 1-parameter linear
> action on the C_3-character-graded vector space that is NOT an
> algebra automorphism, NOT realizable by any conjugation, AND not
> derivable from any retained continuum / scaling / thermal / RG
> limit."**

Probe 15 ADDS the structural-impossibility component to Probe 14's
characterization: not only is U(1)_b distinct in kind from retained
algebraic symmetries, it is also distinct in kind from any retained
**limit operation**. The discrete-to-continuous extension is a
**fresh primitive** that is not supplied by any retained operation
(algebraic, metric, geometric, thermal, or coupling-based).

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction; no closure)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["A1-condition: |b|²/a² = 1/2"]` —
  the residual admission, with the Probe 15 sharpening:
  "the continuous extension of retained discrete C_3 to U(1)_b,
   structurally not derivable from any retained limit operation"

**No new admissions added by this probe.**

### What this probe DOES

1. Verifies that 9 retained limit operations (L1-L9) ALL fail to
   produce the U(1)_b on the b-doublet of `A^{C_3}` by per-limit
   algebraic / numerical checks.
2. Identifies the **universal failure mechanism**: the C_3 cyclic
   shift is combinatorial (intrinsic to BZ-corner indexing); retained
   limits are metric/geometric/coupling-based; combinatorial groups
   are not extended to Lie groups by metric limits.
3. Verifies the **conjugation impossibility**: `φ_θ` is not realizable
   by any conjugation for generic theta (Section 10 algebraic argument).
4. Sharpens the residue with the structural-impossibility component:
   the missing primitive is distinct in kind from any retained limit.

### What this probe DOES NOT do

1. Does NOT close the A1-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem (BZ, 3GenObs, Circulant,
   BlockTotalFrob, MRU, KoideAlg, RP, CPT, Θ_H, all prior probes).
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   campaign synthesis.

## Honest assessment

Which continuum limit got closest? **L6 (Z_3 rationality density)** —
the discrete C_3 IS the desired discrete subgroup of U(1)_b, and the
EXTENSION operation is the only missing piece. But it is precisely the
extension operation that is the missing primitive; no retained limit
operation is an "extension operation".

Did any limit actually produce non-algebraic U(1)_b? **No.** Every
retained limit acts on metric / geometric / coupling parameters. The
combinatorial C_3 structure is invariant under all such limits. The
non-algebraic linear action `φ_θ` is structurally not realizable by
any conjugation, ruling out all retained continuous symmetries
(including any that a limit might generate).

What specifically blocks each limit? See per-limit table — but the
universal mechanism is: **C_3 is combinatorial, retained limits are
metric**. They live in different categories of mathematical structure.

### Three options for the residue (none endorsed by this probe)

1. **Admit U(1)_b as a new small continuous primitive.** A 1-dim
   Lie-algebra extension of the C_3 action, scoped to the
   character-graded structure of `A^{C_3}`. This is now confirmed (by
   Probes 14, 15) to be structurally distinct in kind from any
   cited source-stack content, so admitting it is the smallest possible
   extension of the retained library.

2. **Functional pivot to Q-readout level.** The U(1)_b-invariant
   reduced (ρ_+, ρ_⊥) two-slot carrier of MRU IS available at the
   readout level by construction. Whether this converts into A1
   closure requires a separate derivation: showing that the Brannen
   functional Q on hw=1 must factor through this reduced carrier.

3. **Pivot to other bridge work** (Convention C-iso, substrate-to-
   carrier, δ campaign).

The campaign has converged through Probes 12, 13, 14, 15: each round
sharpens the residue without producing closure. The residue is now
characterized as a single named mathematical object — the continuous
extension of discrete C_3 to a linear (non-algebraic) U(1)_b action —
with structural reasons why it is not derivable from cited source-stack content.

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- Substep-4 PDG-input prohibition: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained continuum / scaling / thermal / RG content

- Lattice continuum limit: [`CONTINUUM_LIMIT_NOTE.md`](CONTINUUM_LIMIT_NOTE.md), [`CONTINUUM_BRIDGE_NOTE.md`](CONTINUUM_BRIDGE_NOTE.md)
- Lattice continuum convergence: [`CONTINUUM_CONVERGENCE_NOTE.md`](CONTINUUM_CONVERGENCE_NOTE.md)
- KMS thermal state: [`AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)
- Stefan-Boltzmann / Hawking / Unruh: [`AXIOM_FIRST_STEFAN_BOLTZMANN_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_STEFAN_BOLTZMANN_THEOREM_NOTE_2026-05-01.md), [`AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_HAWKING_TEMPERATURE_THEOREM_NOTE_2026-05-01.md), [`AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_UNRUH_TEMPERATURE_THEOREM_NOTE_2026-05-01.md)
- Microcausality / Lieb-Robinson: [`AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md`](AXIOM_FIRST_MICROCAUSALITY_LIEB_ROBINSON_THEOREM_NOTE_2026-05-01.md)
- Coleman-Mermin-Wagner: [`AXIOM_FIRST_COLEMAN_MERMIN_WAGNER_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_COLEMAN_MERMIN_WAGNER_THEOREM_NOTE_2026-04-29.md)
- Single-clock structure: [`AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md`](AXIOM_FIRST_SINGLE_CLOCK_CODIMENSION1_EVOLUTION_THEOREM_NOTE_2026-05-03.md)
- α_LM running (matter-sector dynamical cited source-stack content): [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)

### Retained no-go (rational-π radians)

- [`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md) — every retained radian is rational × π

### Retained provenance of the C_3 / circulant structure

- M_3(ℂ) on hw=1: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- No proper quotient: [`THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md`](THREE_GENERATION_OBSERVABLE_NO_PROPER_QUOTIENT_NARROW_THEOREM_NOTE_2026-05-02.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class + reduced two-slot carrier (ρ_+, ρ_⊥): [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Eleven-probe campaign + Probes 12, 13, 14

- Synthesis (campaign terminal state): [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 5 (RG fixed-point, dependency for L8): [`KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md`](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)
- Probe 12 (Plancherel/Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real-structure / antilinear-involution): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- Probe 14 (retained-U(1) hunt, immediate predecessor): [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md)

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_continuum_limit_2026_05_09_probe15.py
```

Expected: `=== TOTAL: PASS=73, FAIL=0 ===`

The runner verifies:

1. **Closure-target structural facts** (Section 0): `φ_θ` is linear,
   not an algebra automorphism for generic theta.
2. **Limit L1 (a → 0)** (Section 1): C_3 acts on combinatorial corner
   indices; intrinsic, not a-dependent. BZ-corner triplet preserved.
3. **Limit L2 (volume → ∞)** (Section 2): per-fiber M_3(ℂ) is
   volume-independent.
4. **Limit L3 (β_th → 0 KMS)** (Section 3): maximally-mixed state IS
   φ_θ-invariant; finite-T Gibbs is NOT; state-invariance ≠ algebra
   action; full-eigenvalue Q is NOT φ_θ-invariant; only reduced (a, |b|)
   readout is.
5. **Limit L4 (β_th → ∞ ground state)** (Section 4): ground state
   depends on full (a, b); φ_θ permutes Gibbs states.
6. **Limit L5 (Wilsonian)** (Section 5): hw=1 has no internal mode
   hierarchy; renormalization preserves algebra.
7. **Limit L6 (Z_3 rationality density)** (Section 6): discrete C_3 has
   3 elements (not dense); rational-π multiples are countable but not
   a Lie subgroup.
8. **Limit L7 (per-site SU(2))** (Section 7): per-site U(1) is global
   phase on hw=1; trivial conjugation on circulants.
9. **Limit L8 (matter RG)** (Section 8): SM-like flow preserves arg(b);
   no fixed point at 1/2 (Probe 5 confirmed).
10. **Limit L9 (large-N)** (Section 9): hw=1 is fixed at 3-dim.
11. **Universal-failure structural argument** (Section 10): C-eigenbasis
    proof that natural Lie homomorphism U(1) → GL(3, ℂ) acts trivially
    on circulants; eigenvalue argument that φ_θ is not realizable by
    any conjugation for generic theta.
12. **Verdict** (Section 11): SHARPENED bounded obstruction; A1
    admission count UNCHANGED.
13. **Closest miss analysis** (Section 12): L6, L3, L7 nearest misses.
14. **Convention robustness** (Section 13): scale-invariance, basis
    change, K-commutation, conditional expectation.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links for
audit citation tracking. It does not promote this note or change the
audited claim scope.

- [koide_a1_probe_retained_u1_hunt_bounded_obstruction_note_2026-05-09_probe14](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md)
- [koide_a1_probe_real_structure_bounded_obstruction_note_2026-05-09_probe13](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- [koide_a1_probe_plancherel_peter_weyl_bounded_obstruction_note_2026-05-09_probe12](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- [koide_a1_probe_rg_fixed_point_bounded_obstruction_note_2026-05-08_probe5](KOIDE_A1_PROBE_RG_FIXED_POINT_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe5.md)
- [koide_z3_qubit_radian_bridge_no_go_note_2026-04-20](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_2026-04-20.md)
- [staggered_dirac_bz_corner_forcing_theorem_note_2026-05-07](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- [continuum_limit_note](CONTINUUM_LIMIT_NOTE.md)
- [continuum_bridge_note](CONTINUUM_BRIDGE_NOTE.md)
- [axiom_first_kms_condition_theorem_note_2026-05-01](AXIOM_FIRST_KMS_CONDITION_THEOREM_NOTE_2026-05-01.md)
- [koide_mru_weight_class_obstruction_theorem_note_2026-04-19](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)
- [minimal_axioms_2026-05-03](MINIMAL_AXIOMS_2026-05-03.md)

## Review-loop rule

When reviewing future branches that propose to close A1 via a
continuum / scaling / thermodynamic / RG limit:

1. Verify the proposed limit is **cited source-stack content** (cite a retained
   limit-operation note).
2. Verify the limit acts on **matter-sector hw=1**, not just on gauge
   or geometric content.
3. Test whether the limit **extends discrete C_3 to a continuous
   1-parameter family** containing it (Test C3). Note: the natural
   Lie homomorphism extending C_3 acts trivially on circulants by
   conjugation (Section 10.4) — this is NOT extension to U(1)_b.
4. Test whether the limit produces the **non-algebraic linear action**
   `φ_θ` on the b-doublet (Test C4). For ANY conjugation, the
   eigenvalue argument (Section 10.5) rules out generic theta.
5. The discrete-to-continuous extension is the **specific missing
   primitive**. Limit operations on metric / geometric / coupling
   parameters do not perform this extension.
