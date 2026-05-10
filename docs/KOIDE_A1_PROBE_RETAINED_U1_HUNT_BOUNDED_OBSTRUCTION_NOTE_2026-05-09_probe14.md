# Koide A1 Probe 14 — Retained-U(1) Hunt for U(1)_b Closure

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure)
**Claim type:** bounded_theorem
**Status:** source-note proposal — Probe 14 bounded-obstruction attempt for the A1
amplitude-ratio admission via hunt for an existing retained U(1) that
projects onto the U(1)_b angular quotient on the b-doublet of the
Brannen circulant. Per Probe 13's residue, the missing primitive is
"the SO(2) phase quotient on the b-doublet of A^{C_3} = the U(1)_b
symmetry of the Brannen δ-readout." This probe asks whether any of the
currently inventoried retained framework U(1) candidates — explicitly
forbidding new axioms or external imports per user 2026-05-09
clarification — can supply U(1)_b.
**Authority role:** source-note proposal; effective_status set only by
the independent audit lane.
**Loop:** koide-a1-probe14-retained-u1-hunt-20260509
**Primary runner:** [`scripts/cl3_koide_a1_probe_retained_u1_hunt_2026_05_09_probe14.py`](../scripts/cl3_koide_a1_probe_retained_u1_hunt_2026_05_09_probe14.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_retained_u1_hunt_2026_05_09_probe14.txt`](../logs/runner-cache/cl3_koide_a1_probe_retained_u1_hunt_2026_05_09_probe14.txt)

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

**No new axioms. No external imports.** Any future closure would have to
come from:

  (i) An already-retained U(1) that projects onto U(1)_b on the
      b-doublet, OR
  (ii) A derivation of U(1)_b from existing retained content (extending
       the retained library, no new axiom needed).

Option (iii) — admit U(1)_b as a new primitive — is OFF the table for
this probe.

## Question

Does any currently inventoried retained framework U(1) project onto U(1)_b
on the b-doublet of the C_3-fixed subalgebra `A^{C_3}`?

## Answer

**No candidate in this nine-case inventory succeeds.** Nine retained U(1)
candidates were examined, and none projects to U(1)_b. The structural
reason for the algebra-automorphism candidates is that they act by
conjugation, while U(1)_b acts as a **linear shift** on the C_3-character
grading — not multiplicative, not an algebra automorphism. The two
structures are qualitatively different.

## Setup

### Closure target (Probe 13 residue)

The U(1)_b "vector action" on `A^{C_3}` (the Hermitian circulants):

```
φ_θ(I)  = I             (weight 0 under C_3 grading)
φ_θ(C)  = e^{+iθ} C     (weight +1, ω-isotype)
φ_θ(C²) = e^{-iθ} C²    (weight -1, ω̄-isotype)
```

Equivalently on `H = aI + bC + b̄C²`:

```
φ_θ(H) = aI + e^{iθ} b C + e^{-iθ} b̄ C²
```

**Critical structural fact (Section 1 of runner)**: φ_θ is **NOT** an
algebra automorphism. It does NOT preserve multiplication:
- `φ_θ(C · C) = φ_θ(C²) = e^{-iθ} C²`
- `φ_θ(C) · φ_θ(C) = e^{+2iθ} C²`
- These differ unless `θ ∈ {0, 2π/3, 4π/3}` (the discrete C_3 subgroup).

So U(1)_b is the continuous linear extension of the discrete C_3
character grading. The retained C_3 is the multiplicative subgroup; the
continuous extension is purely additive on graded weights.

### Forbidden imports

- NO PDG observed values used as derivation input
- NO new axioms (per user 2026-05-09 clarification)
- NO external imports (string theory, NCG primitives, U(3) family
  gauge bosons, spectral action, Sumino tuning, etc.)

## Candidate-by-candidate analysis

Nine retained U(1) candidates examined. Each tested for:
- **T1 (existence)**: retained on main?
- **T2 (action on M_3(C))**: acts non-trivially?
- **T3 (compatibility with C_3)**: commutes with retained C_3?
- **T4 (projection to U(1)_b)**: restricts to b-doublet as the linear
  vector action `φ_θ`?
- **T5 (closure of A1)**: forces `|b|²/a² = 1/2`?

| # | Candidate | T1 | T2 | T3 | T4 | T5 | Reason for failure |
|---|---|---|---|---|---|---|---|
| 1 | `Q̂_total` (fermion number) | ✓ | trivial on bilinears | trivially | ✗ | ✗ | acts as identity on M_3(C); no projection |
| 2 | `U(1)_Y` hypercharge | ✓ | non-trivial on full Cl(3) | ✓ | ✗ | ✗ | Y commutes with circulants → conjugation trivial on `A^{C_3}` |
| 3 | `e^{iθω}` (pseudoscalar) | ✓ | non-trivial on Cl(3) | ✓ | ✗ | ✗ | ω is central in Cl(3); conjugation by e^{iθω} is identity |
| 4 | `U(1)_em` electromagnetic | ✓ | non-trivial | ✓ | ✗ | ✗ | same structure as U(1)_Y; projects to identity on `A^{C_3}` |
| 5 | Per-site qubit phase U(1) | ✓ | non-trivial per-site | ✓ | ✗ | ✗ | per-site phase commutes with C_3-cyclic-shift on hw=1; trivial conjugation on circulants |
| 6 | Time-evolution `e^{-iHt}` | ✓ | non-trivial | depends on `[H, C]` | ✗ | ✗ | for `[H, C] = 0` (C_3-equivariant H), conjugation is identity on circulants |
| 7 | Global state-phase U(1) | ✓ | trivial on operators | trivially | ✗ | ✗ | global phase acts only on states, not algebra |
| 8 | Cl⁺(3) ⊃ SU(2) maximal torus | ✓ | non-trivial in SU(2) | non-trivially | ✗ | ✗ | SU(2)-torus on Cl⁺(3) does not project to b-doublet on `A^{C_3}` |
| 9 | Z_3 ⊂ U(1) continuous extension | discrete C_3 retained; continuous extension NOT retained | n/a | n/a | n/a | n/a | per `KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE`: every retained radian is rational × π, generic θ ∈ [0, 2π) is not retained |

**Common failure mode (T4 across the algebra-automorphism candidates)**:
the examined retained continuous U(1)'s act on M_3(C) as algebra
automorphisms (via conjugation `X → U X U^*`). On the C_3-fixed
subalgebra `A^{C_3}` — which is the commutant of C_3 — any such U(1)
that commutes with C_3 acts trivially by conjugation.

The U(1)_b residue, by contrast, is a **non-algebraic linear action** on
the C_3-character-graded vector space: it shifts weights `(+1, -1)`
of the doublet by phase `e^{±iθ}` without preserving the algebra
multiplication. No examined retained continuous algebra symmetry produces
this non-algebraic linear shift.

Candidate 9 (Z_3 → U(1) continuous extension) is the closest miss: the
retained C_3 character grading IS the discrete subgroup of U(1)_b. Per
the retained `KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE`, every retained
radian is rational × π; generic θ ∈ [0, 2π) is not in retained content.
Extending Z_3 → U(1) is exactly what would be needed; the framework's
discrete-in-time + discrete-lattice + continuous-in-qubit structure
provides per-site continuous SU(2) but not the doublet-graded U(1)_b
extension.

## Why this is structurally rigorous

The 9 candidates inventory the campaign's currently cited retained
continuous-symmetry surface; this note does not certify global
exhaustiveness outside those cited surfaces:

- **Internal symmetries**: Q̂_total (fermion #), U(1)_Y (hypercharge),
  U(1)_em (electromagnetic) — all act on Cl(3) as conjugation
- **Discrete-symmetry continuous extensions**: e^{iθω} (pseudoscalar),
  Z_3 ⊂ U(1) (C_3 character grading) — pseudoscalar is central → trivial
  conjugation; Z_3 has no retained continuous extension
- **Geometric symmetries**: Cl⁺(3) maximal torus, per-site qubit phase
  — both factor as algebra automorphisms commuting with C_3 → trivial
- **Dynamics-derived symmetries**: time-evolution, global state-phase
  — time evolution is trivial on commutant; global phase is on states

The 9 categories cover the current campaign inventory.
None projects to U(1)_b on the b-doublet because U(1)_b is qualitatively
different in kind: linear/non-algebraic, not multiplicative/algebraic.

## Sharpened residue

After Probes 12, 13, 14, the missing primitive is precisely:

> **"The continuous extension of retained discrete `C_3` to U(1)_b on
> the b-doublet of `A^{C_3}` — equivalently, a 1-parameter linear
> action on the C_3-character-graded vector space that is NOT an
> algebra automorphism."**

This is the smallest possible characterization. It is a derivation
target (not closeable from the examined retained content alone), distinct
in kind from all 9 examined retained continuous U(1)'s.

## Strategic options

This probe **does not select** an option; that authority is the user's.
Three options remain after 14 probes:

1. **Continue derivation hunt** — the residue is now precisely
   characterized. A future probe might find a derivation of the
   non-algebraic U(1)_b from retained content (e.g., from continuum
   limits of the retained discrete C_3, or from a specific lattice-
   level construction). Probability is low after 14 negative probes,
   but not zero.

2. **Functional pivot to Q-readout level** — the Brannen Koide ratio
   `Q = (Σ √λ_k)²/(3 Σ λ_k)` is **U(1)_b-invariant by construction**:
   it depends only on `(a, |b|)`, not on `arg(b)`. So at the readout
   level, the residue is automatically respected. Whether this
   converts into closure of A1 requires a separate derivation.

3. **Pivot to other bridge work** — Convention C-iso engineering (in
   flight), substrate-to-carrier forcing (toward Planck-from-structure,
   3 missing theorems), δ campaign (parallel structure to A1).

The campaign has converged to a bounded obstruction: 14 independent
probes, monotonic sharpening each round, residue now precisely
characterized as a single named mathematical object that no inventoried
retained framework symmetry supplies.

## Cross-references

- **Foundational notes**:
  `MINIMAL_AXIOMS_2026-05-03.md`,
  [`PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md`](PHYSICAL_LATTICE_FOUNDATIONAL_INTERPRETATION_NOTE_2026-05-08.md),
  [`C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md`](C3_SYMMETRY_PRESERVED_INTERPRETATION_NOTE_2026-05-08.md)
- **Campaign synthesis**:
  [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
  (PR #751)
- **Immediate predecessors**:
  [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
  (PR #755),
  [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
  (PR #763)
- **Retained continuous-symmetry sources**:
  [`CL3_SM_EMBEDDING_THEOREM.md`](CL3_SM_EMBEDDING_THEOREM.md),
  [`STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md`](STANDARD_MODEL_HYPERCHARGE_UNIQUENESS_THEOREM_NOTE_2026-04-24.md),
  [`FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md`](FERMION_PARITY_Z2_GRADING_THEOREM_NOTE_2026-05-02.md)
- **Retained no-go**:
  [`KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE_*.md`](KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE.md)
  — every retained radian is rational × π
- **Substep-4 PDG-input prohibition**:
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_retained_u1_hunt_2026_05_09_probe14.py
```

Runner verifies, for each of 9 candidates, the structural failure mode
(specifically T4 — projection to U(1)_b) by explicit matrix computation.

**Runner result: 70/0 PASS, 0 FAIL.**

## Review-loop rule

When reviewing future branches that propose to close A1 via an existing
continuous symmetry:

1. Verify the proposed symmetry acts as **algebra automorphism** vs.
   **linear vector action**. If it's the former (i.e., conjugation), it
   cannot project to U(1)_b on `A^{C_3}` (Probe 14 covers this case
   across the nine candidate families examined here).
2. If it's a linear non-algebraic action, ask whether it's derivable
   from retained content (the open question after Probe 14).
3. Discrete-to-continuous extensions of retained C_3 must respect the
   retained `KOIDE_Z3_QUBIT_RADIAN_BRIDGE_NO_GO_NOTE` (every retained
   radian is rational × π).
