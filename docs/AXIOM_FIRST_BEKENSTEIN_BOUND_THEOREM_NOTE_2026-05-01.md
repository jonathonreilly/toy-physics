# Axiom-First Bekenstein Bound from Retained BH 1/4 Carrier + Spectrum Condition

**Date:** 2026-05-01
**Type:** bounded_theorem
**Claim scope:** for any sub-Schwarzschild matter system (2GE < R) localized in a sphere of asymptotic radius R with mass-energy E, the entropy obeys S(R, E) ≤ 2πRE/(ℏc); saturated by Schwarzschild at 2GE = R. Conditional on retained BH 1/4 carrier (which admits Wald-Noether) and on universal-physics second-law direction.
**Status:** awaiting independent audit. Under the scope-aware classification framework (audit-lane proposal #291), `effective_status` is computed by the audit pipeline.
**Loop:** `24h-axiom-first-derivations-20260501`
**Cycle:** 3 (Block 03; independent of Blocks 01-02)
**Branch:** `physics-loop/24h-axiom-first-block03-bekenstein-20260501`
**Runner:** `scripts/axiom_first_bekenstein_bound_check.py`
**Log:** `outputs/axiom_first_bekenstein_bound_check_2026-05-01.txt`

## Scope

This note proves, on the framework's retained discrete GR action surface
plus retained BH 1/4 carrier composition plus retained axiom-first
spectrum condition, the **Bekenstein universal bound**:

```text
    S(R, E)  ≤  (2 π R E) / (ℏ c)              (Bekenstein 1981 form)
             =  2 π R E                          (in natural units ℏ = c = k_B = 1)
```

for the entropy `S(R, E)` of any matter system contained within a sphere
of asymptotic-radius `R` and total mass-energy `E` (with `2 G E < R` so
the system has not collapsed to a black hole).

The proof is the standard Bousso/Casini-style reasoning: the
black-hole entropy `S_BH = A/(4G)` of the smallest BH that can fit
inside the same region plays the role of an extremal entropy bound,
and the holographic Bekenstein-Hawking entropy bounds the entropy of
any sub-Schwarzschild matter system in the same region.

After this note, the package's holographic / information-theoretic
language can quote a branch-local Bekenstein bound theorem on the
framework's retained GR + BH 1/4 surface instead of treating it as a
continuum-QFT-only result.

## Retained inputs

- **Framework GR action surface.** As in Block 02; the framework's
  discrete GR action on PL S³ × R supports stationary spherically-
  symmetric solutions in the smooth-limit equivalence regime
  (Schwarzschild family).
- **BH 1/4 carrier composition.** From the retained
  `BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`,
  the entropy of any horizon of area `A` is
  `S_BH = A · c_cell = A / (4 G_Newton,lat)` where `c_cell = 1/4` is
  the framework's primitive coframe boundary carrier coefficient
  (`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`).
- **Spectrum condition.** From the retained
  `AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`, the
  reconstructed Hamiltonian on `H_phys` is bounded below
  (`H ≥ 0`), so the energy `E` of any normalizable matter state on
  `H_phys` is well-defined and `≥ 0`.
- **Cluster decomposition (used implicitly).** From the retained
  `AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`,
  matter states localized in a finite region have correlators that
  decay exponentially outside the region, supporting the localization
  premise needed for the Bekenstein bound.

## Admitted-context inputs

- **Schwarzschild metric in the smooth-limit equivalence regime.**
  The framework's GR action equals the canonical Einstein-Hilbert
  action on smooth backgrounds
  (`UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`),
  so the standard Schwarzschild family `r_s = 2 G M` lies in the
  framework's stationary solution class. This is the same admission
  already paid for by the retained Wald-Noether composition.
- **Asymptotic mass-energy identification.** The asymptotic ADM mass
  on a stationary asymptotically-flat solution equals the total
  energy `E`; this is standard stationary GR.

These are the same admitted-context inputs already paid for by the
retained Wald-Noether composition in
`BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`.
We do not introduce new admitted inputs.

## Statement

Let `B(R) ⊂ M` be a ball of asymptotic-radius `R > 0` in the
framework's smooth-limit Schwarzschild family on the retained GR
action surface. Let `Σ` be a Cauchy slice with `B(R) ⊂ Σ`. Let `S`
be the entropy of any matter state localized in `B(R)` with total
asymptotic mass-energy `E` such that `2 G E < R` (sub-Schwarzschild
condition).

Then on `A_min` plus the retained inputs above:

**(B1) Sub-Schwarzschild geometric inequality.** For any matter state
satisfying `2 G E < R`,

```text
    A_BH(M = E)  =  4 π (2 G E)²  ≤  4 π R · 2 G E  =  8 π G R E             (1)
```

since `2 G E ≤ R` implies `(2 G E)² ≤ R · 2 G E`. Here `A_BH(M = E)`
is the area of the smallest Schwarzschild BH whose mass equals the
matter system's mass-energy.

**(B2) Holographic entropy upper bound.** Any matter state with
mass-energy `E` localized in `B(R)` (sub-Schwarzschild) has entropy
bounded by the BH entropy of the BH whose mass equals `E`:

```text
    S_matter(R, E)  ≤  S_BH(M = E)                                          (2)
```

This is the *generalized second law in inverse direction* — it follows
because if `S_matter > S_BH(M = E)`, then collapsing the matter system
to the BH would *decrease* total entropy, violating the second law.
(See Bousso 2002, Bekenstein 1981.)

**(B3) Bekenstein bound.** Combining (B1), (B2), and (B0) of the
retained BH 1/4 carrier composition `S_BH = A / (4 G)`:

```text
    S_matter(R, E)  ≤  S_BH(M = E)  =  A_BH(M = E) / (4 G)                  (3)
                    ≤  (8 π G R E) / (4 G)  =  2 π R E                       (4)
```

restoring `ℏ`, `c`, `k_B`,

```text
    S(R, E)  ≤  (2 π R E) / (ℏ c)  ·  k_B                                     (5)
```

This is the **Bekenstein universal bound**.

**(B4) Saturation at the Schwarzschild boundary.** When `2 G E = R`,
inequality (1) is saturated and `S_BH(M = E) = A / (4 G) =
4 π R² / (4 G) = π R² / G = 2 π R E`. So the Schwarzschild BH itself
saturates the Bekenstein bound; the bound is tight.

Statements (B1)–(B4) constitute the Bekenstein bound theorem on the
framework's retained GR + BH 1/4 carrier + spectrum condition surface.

## Proof

The proof has three steps. Step 1 is geometric, Step 2 invokes the
generalized second law on the framework's retained surface, Step 3 is
algebraic.

### Step 1 — Sub-Schwarzschild geometric inequality

Suppose `2 G E < R`. The Schwarzschild radius of the system's mass-
energy is `r_s = 2 G E`. Compute the corresponding BH area:

```text
    A_BH(M = E)  =  4 π r_s²  =  4 π (2 G E)²
                =  16 π G² E²                                                (6)
```

Since `2 G E ≤ R` (sub-Schwarzschild condition), we have

```text
    16 π G² E²  =  4 π · (2 G E) · (2 G E)  ≤  4 π · (2 G E) · R
                =  8 π G R E                                                 (7)
```

establishing (B1). The inequality is saturated when `2 G E = R`. ∎

### Step 2 — Holographic entropy upper bound from GSL

Suppose the matter state has entropy `S_matter > S_BH(M = E)`. Now
imagine a quasi-static gravitational collapse process where the
matter system, while preserving its mass-energy `E`, is compressed
into a Schwarzschild BH of mass `M = E` and area `A_BH(M = E)`.

By the retained framework GR action surface, the resulting solution
is the Schwarzschild metric with the same asymptotic mass `E`. Its
entropy is `S_BH = A_BH / (4 G)` from the retained BH 1/4 carrier
composition.

Apply the second law of thermodynamics to the entire spacetime
(matter + horizon):

```text
    ΔS_total  =  S_BH - S_matter  ≥  0                                       (8)
```

If `S_matter > S_BH`, then `ΔS_total < 0`, which violates the second
law. Hence

```text
    S_matter(R, E)  ≤  S_BH(M = E)                                          (9)
```

establishing (B2). ∎

(Remark: The framework derivation of the generalized second law
itself (Block 09 of this campaign) closes the second-law step
formally on the framework's retained KMS + BH 1/4 carrier surface.
For the Bekenstein bound proof we use only the *direction* implied by
the second law: net entropy never decreases under physical processes.
This is the universal physics input that already underwrites the
retained Wald-Noether composition.)

### Step 3 — Combine into the Bekenstein bound

From (B1), `A_BH(M = E) ≤ 8 π G R E`.
From (B2), `S_matter ≤ S_BH(M = E)`.
From the retained BH 1/4 carrier, `S_BH = A_BH / (4 G)`.

Chain these:

```text
    S_matter(R, E)  ≤  S_BH(M = E)
                   =  A_BH(M = E) / (4 G)                                   (10)
                   ≤  (8 π G R E) / (4 G)
                   =  2 π R E                                               (11)
```

establishing (B3). The saturation condition (B4) follows from
saturating (B1) at `2 G E = R`. ∎

## Hypothesis set used

- A_min (only as inherited from upstream retained spectrum-condition
  note via the spectrum-condition role in Step 2).
- Retained framework GR action surface.
- Retained canonical Einstein-Hilbert equivalence (smooth-limit).
- Retained BH 1/4 carrier composition (Wald-Noether admitted).
- Retained spectrum condition (`H ≥ 0` ⇒ `E ≥ 0`).
- Standard Schwarzschild family / asymptotic ADM mass identification
  (admitted-context, same as upstream Wald-Noether).
- Universal second-law direction (`ΔS_total ≥ 0`); admitted at the
  same level as the retained Wald-Noether composition uses thermodynamic
  reasoning.

No fitted parameters. No observed values used as proof inputs. No
imports beyond the explicit admitted-context list.

## Corollaries

C1. **Holographic information bound.** Any localized quantum system
of radius `R` and energy `E` can store at most `S / log 2 ≤ 2 π R E /
(ℏ c log 2)` bits of information. This is the universal information
content of the region.

C2. **Schwarzschild BH saturates Bekenstein.** From (B4), the
Schwarzschild BH is the unique entropy maximizer in any region of
radius `R = 2 G M`. This identifies BHs as "maximum-entropy objects".

C3. **Cosmological-constant correction.** On de Sitter background
(`Λ > 0`), the Bekenstein bound generalizes to `S ≤ 2 π R E +
S_dS(R)` where `S_dS = π / (G Λ)` is the de Sitter horizon entropy
contribution. This corollary uses the framework's retained
cosmological-constant identity but is recorded here only as a
qualitative pointer.

C4. **Complementary Bousso covariant bound.** Bousso's covariant
holographic bound `S(L) ≤ A(L) / (4 G)` for any light-sheet `L`
generalizes (B3); it follows from the same retained BH 1/4 carrier
plus a focusing-theorem geometric step. This is recorded for future
work; not derived in this note.

## Honest status

**Branch-local theorem on retained framework GR + retained BH 1/4
carrier + retained spectrum condition.** (B1)–(B4) are derived from:

- the retained framework GR action surface;
- the retained BH 1/4 carrier composition;
- the retained spectrum condition (`E ≥ 0`);
- standard Schwarzschild geometry (admitted-context, same as upstream
  Wald-Noether);
- the universal second-law direction (admitted-context).

The runner verifies the algebraic Bekenstein chain on a sweep of
`(R, E)` parameter pairs and confirms saturation at the Schwarzschild
boundary `2 G E = R`.

**Honest claim-status fields:**

```yaml
actual_current_surface_status: support
conditional_surface_status: derived support theorem on retained framework GR + retained BH 1/4 carrier + retained spectrum condition
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "Depends on retained-but-audit-pending BH 1/4 carrier composition (per its own status line: 'bounded: S_BH=A/(4G_N) framework composition, conditional on Wald formula admission and gravitational boundary/action-density bridge premise'). Per physics-loop SKILL retained-proposal certificate item 4, a chain that depends on a bounded composition cannot promote to proposed_retained until the upstream is ratified retained on the current authority surface. Note also: universal second-law direction is admitted-context input."
audit_required_before_effective_retained: true
bare_retained_allowed: false
```

**Not in scope.**

- The full Bousso covariant entropy bound `S(L) ≤ A(L)/(4G)` for an
  arbitrary light-sheet `L`. (C4 — future work.)
- Promotion to retained / Nature-grade in the canonical paper
  package. That requires upstream BH 1/4 carrier ratified retained,
  plus independent audit.

## Citations

- A_min: `docs/MINIMAL_AXIOMS_2026-04-11.md`
- retained framework GR action: `docs/UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`,
  `docs/UNIVERSAL_GR_LORENTZIAN_GLOBAL_ATLAS_CLOSURE_NOTE.md`,
  `docs/UNIVERSAL_QG_CANONICAL_TEXTBOOK_GEOMETRIC_ACTION_EQUIVALENCE_NOTE.md`
- retained BH 1/4 carrier composition:
  `docs/BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`
- retained primitive coframe carrier:
  `docs/PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`
- retained spectrum condition:
  `docs/AXIOM_FIRST_SPECTRUM_CONDITION_THEOREM_NOTE_2026-04-29.md`
- retained cluster decomposition (used implicitly):
  `docs/AXIOM_FIRST_CLUSTER_DECOMPOSITION_THEOREM_NOTE_2026-04-29.md`
- standard external references (theorem-grade, no numerical input):
  Bekenstein (1981) *Phys. Rev. D* 23, 287;
  Bousso (1999) *JHEP* 9907, 004;
  Bousso (2002) *Rev. Mod. Phys.* 74, 825;
  Casini (2008) *Class. Quantum Grav.* 25, 205021.
