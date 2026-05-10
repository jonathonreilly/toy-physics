# Koide A1 Probe 17 — Non-Conjugation Lift of Retained Per-Site Qubit U(1) Sharpened Bounded Obstruction

**Date:** 2026-05-09
**Type:** bounded_theorem (sharpened obstruction; no positive closure; no new admission)
**Claim type:** bounded_theorem
**Scope:** review-loop source-note proposal — Probe 17 of the Koide
A1-condition closure campaign. Tests whether any **non-conjugation lift**
of the retained per-site qubit U(1) (the continuous U(1) on each per-site
`Cl(3) ≅ M_2(ℂ)`) can produce the missing U(1)_b symmetry on the b-doublet
of `A^{C_3}`. Probe 14 (RETAINED_U1_HUNT) closed the algebra-automorphism
case; this probe closes the non-conjugation case.
**Status:** source-note proposal for a **sharpened** bounded obstruction.
The five candidate non-conjugation attack vectors (V1: character-graded
per-site phase; V2: bimodule/left-module action; V3: twisted conjugation
`X → UXV*` with `U≠V`; V4: pseudoscalar-twisted action; V5: spatial
site-position phase) ALL collapse back to one of: (i) algebra-automorphism
(= conjugation, covered by Probe 14, trivial on `A^{C_3}`); (ii) non-algebra
group action that fails associativity, unitality, multiplicativity, or
Hermiticity preservation; or (iii) non-equivariant action that breaks
`A^{C_3}` structure. The structural obstruction is identified precisely:
**U(1)_b is intrinsically a SPECTRUM-NON-PRESERVING transformation on `M_3(ℂ)`**,
hence cannot be realized by ANY unitary similarity — including the most
general unitary similarity (conjugation by an arbitrary U(3) element). The
A1 admission count is UNCHANGED.
**Authority role:** source-note proposal — audit verdict and downstream
status set only by the independent audit lane.
**Loop:** koide-a1-probe-lattice-non-conjugation-20260509
**Primary runner:** [`scripts/cl3_koide_a1_probe_lattice_non_conjugation_2026_05_09_probe17.py`](../scripts/cl3_koide_a1_probe_lattice_non_conjugation_2026_05_09_probe17.py)
**Cache:** [`logs/runner-cache/cl3_koide_a1_probe_lattice_non_conjugation_2026_05_09_probe17.txt`](../logs/runner-cache/cl3_koide_a1_probe_lattice_non_conjugation_2026_05_09_probe17.txt)

## Authority disclaimer

This is a source-note proposal. Pipeline-derived status is generated
only after the independent audit lane reviews the claim, dependency
chain, and runner. The `claim_type`, scope, named admissions, and
bounded-obstruction classification are author-proposed; the audit
lane has full authority to retag, narrow, or reject the proposal.

## Naming-collision warning

In this note:

- **"framework axiom A1"** = retained `Cl(3)` local-algebra axiom per
  `MINIMAL_AXIOMS_2026-05-03.md`.
- **"A1-condition"** = the Brannen-Rivero amplitude-ratio constraint
  `|b|²/a² = 1/2` for the `C_3`-equivariant Hermitian circulant
  `H = aI + bC + b̄C²` on `hw=1 ≅ ℂ³`.
- **"Probe 14"** = a prior closure attempt (RETAINED_U1_HUNT) that
  found every retained continuous U(1) acts on `M_3(ℂ)` as conjugation
  `X → UXU*`; on `A^{C_3}`, conjugation by any U commuting with C_3 is
  TRIVIAL.

These are distinct objects despite the shared label. This probe
concerns the A1-condition only; framework axiom A1 is retained and
untouched.

## Hypothesis

Probe 14 found per-site qubit U(1) acts trivially on `A^{C_3}` *under
conjugation*. But conjugation is just one possible action of a unitary
group on a matrix algebra. The hypothesis tested by this probe:

> There might be a *non-conjugation lift* of the retained per-site qubit
> U(1) to `M_3(ℂ)` that:
> (a) acts non-trivially on the b-doublet,
> (b) restricts as the linear vector-space action `φ_θ` (NOT an
>     algebra-automorphism),
> (c) is derivable from cited source-stack content (no new axioms).

The framework's hw=1 sector is a 3-dim subspace of the larger Z³ lattice
Hilbert space. The C_3 action on hw=1 comes from a specific lattice
construction (BZ-corner forcing per
[`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)).
The per-site qubit U(1) acts on each per-site `Cl(3) ≅ M_2(ℂ)`. Their
*combined* action on the lattice Hilbert space, restricted to hw=1,
might in principle be non-conjugation.

## Answer

**No.** The hypothesis fails. **Five candidate non-conjugation attack
vectors all collapse**, each by a different but related structural mechanism.

The deeper structural reason — verified algebraically — is the **Skolem-Noether
rigidity** combined with a sharper observation:

> U(1)_b is intrinsically a SPECTRUM-NON-PRESERVING transformation on
> `M_3(ℂ)`. The map `H = aI + bC + b̄C² ↦ H_φ = aI + e^{iφ}bC + e^{-iφ}b̄C²`
> changes the eigenvalues of H (verified numerically by the runner at
> Section 7.6). Since every unitary similarity preserves eigenvalues,
> U(1)_b cannot be ANY unitary similarity. In particular, it cannot be
> a conjugation by ANY U(3) element — and a fortiori not a conjugation
> by an element of any retained continuous symmetry group.

This sharpens Probe 14 substantially: Probe 14 said "every retained U(1)
acts as conjugation, hence (by Schur) trivially on `A^{C_3}` when the U
commutes with C_3." Probe 17 says: even if we drop the requirement that
U commutes with C_3, and even if we drop the requirement that the action
be conjugation (allowing arbitrary linear maps `M_3(ℂ) → M_3(ℂ)`), there
is no unitary lift that produces U(1)_b — because U(1)_b is intrinsically
non-unitary.

**Verdict: SHARPENED bounded obstruction.** The A1 admission count is
UNCHANGED. The structural obstruction is now precisely identified: U(1)_b
must be a NON-unitary linear automorphism of `A^{C_3}` (preserving its
4-real-dim vector space structure but not its spectral structure on the
ambient `M_3(ℂ)`).

## Setup

### Premises (A_min for Probe 17)

| ID | Statement | Class |
|---|---|---|
| A1 | `Cl(3)` local algebra | framework axiom; see `MINIMAL_AXIOMS_2026-05-03.md` |
| A2 | `Z³` spatial substrate | framework axiom; same source |
| BZ | hw=1 BZ-corner triplet ≅ `ℂ³` with `C_3[111]` action | source dependency; see [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md) |
| 3GenObs | hw=1 carries `M_3(ℂ)` algebra; no proper exact quotient | source dependency; see [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md) |
| Circulant | `C_3`-equivariant Hermitian on hw=1 is `aI + bC + b̄C²` | source dependency; see [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md) R1 |
| PerSite | Per-site Hilbert ≅ `M_2(ℂ)` (qubit), generated by `σ_i` | source dependency; see [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md) U2 |
| PerSiteU1 | Per-site qubit U(1) ⊂ U(`M_2(ℂ)`) is the continuous Lie group of phases on each site | source dependency: per-site uniqueness plus standard exponentiation |
| Probe14 | Every retained U(1) acts on `M_3(ℂ)` as conjugation; on `A^{C_3}` trivial | source dependency; see [`KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md`](KOIDE_A1_PROBE_RETAINED_U1_HUNT_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe14.md) |
| Probe13 | `K`-real-structure supplies Z_2 part of doublet combination, not SO(2) | source dependency; see [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md) |
| KoideAlg | Koide `Q = 2/3 ⟺ a₀² = 2|z|² ⟺ |b|²/a² = 1/2` | source dependency; see [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md) |

### Forbidden imports

- NO PDG observed mass values used as derivation input (per
  [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md))
- NO lattice MC empirical measurements
- NO fitted matching coefficients
- NO new admissions added by this probe (verdict: SHARPENED, no closure
  achieved without admission, and no admission proposed)

## Five attack vectors and their collapse

### V1 — Per-site phase with C_3-character-graded angle

**Proposal:** for the three sites supporting hw=1, apply per-site U(1)
phase `e^{iθ·χ_k σ_3 / 2}` where `χ_k ∈ {0, +1, -1}` is the C_3-character
of corner k. Does this lift to `M_3(ℂ)` as the U(1)_b vector action?

**Collapse:** to be a candidate for U(1)_b on `A^{C_3}`, the action must
be **C_3-equivariant**. But C_3 cyclically permutes the three corners,
so a C_3-equivariant assignment of angles `(θ_1, θ_2, θ_3)` to corners
must satisfy `θ_1 = θ_2 = θ_3 = θ`. The resulting unitary on `H_hw=1` is
`U_θ = e^{iθ} · I` — a global scalar. Conjugation by a global scalar is
**trivial**. (Runner Section 2: PASS, 7 checks.)

If we relax C_3-equivariance, the action breaks `A^{C_3}` (takes
circulants out of the circulant subalgebra). Either way, V1 cannot supply
U(1)_b.

### V2 — Bimodule action distinct from conjugation

**Proposal:** on `M_3(ℂ)` viewed as a left-`M_3(ℂ)`-module, the action
`L_U(X) = U·X` (left multiplication) is not an algebra automorphism. Does
this give U(1)_b?

**Collapse:** `L_U` is **NOT** a group homomorphism for the `U(1)`
group structure (since `L_U(AB) = U·A·B ≠ U·A·U·B = L_U(A)·L_U(B)`).
Even when restricted to `A^{C_3}` (commutative subalgebra), `L_U` for U
in the maximal C_3-commuting U(1) acts by **multiplication of circulants**.
This induces a 3-torus T³ action on the three character isotypes
`(χ_1, χ_ω, χ_ω̄)` — distinct from U(1)_b (which fixes `χ_1` while rotating
the doublet). The "doublet-only" subgroup `U_b(θ) = F·diag(1, e^{iθ}, e^{-iθ})·F*`
COMMUTES with C_3 (so by Probe 14 conjugation by it is trivial on `A^{C_3}`),
and acts by left-multiplication on `A^{C_3}` as a unitary in the circulant
algebra — but left-multiplication MIXES the a-coefficient (= projection
on `χ_1`) with the b-doublet, NOT a clean U(1)_b on b alone. (Runner
Section 3: PASS, 10 checks.)

### V3 — Twisted conjugation `X → U X V*` with `U ≠ V`

**Proposal:** instead of `X → UXU*`, try `X → UXV*` for `U ≠ V` in the
retained per-site qubit U(1) sector. Is this a "twisted" conjugation
producing U(1)_b?

**Collapse:** the twisted action **IS** a 1-parameter group action
(verified Section 4.1: `α_{U_1, V_1} ∘ α_{U_2, V_2} = α_{U_1U_2, V_1V_2}`),
but it fails THREE structural requirements:
1. **NOT unital:** `α_{U,V}(I) = U V* ≠ I` in general (Section 4.2).
2. **NOT multiplicative:** `α_{U,V}(AB) = U·A·B·V* ≠ α_{U,V}(A)·α_{U,V}(B) = U·A·V*·U·B·V*`
   in general (requires `V*U` central) (Section 4.3).
3. **NOT Hermiticity-preserving:** maps Hermitian circulants to non-Hermitian
   matrices (Section 4.4a).

The action on EIGENVALUES of H (`λ_1, λ_ω, λ_ω̄`) multiplies them by
phases, but U(1)_b acts on `(a, b)` coefficients (a NON-LINEAR action on
eigenvalues — see Section 7.6 for the spectral-non-preservation diagnostic).
Hence twisted conjugation cannot implement U(1)_b. (Runner Section 4: PASS,
4 checks.)

### V4 — Pseudoscalar-twisted action

**Proposal:** combine retained per-site qubit U(1) with the pseudoscalar
`ω = e_1 e_2 e_3` (central in `Cl(3)`). Does pseudoscalar-twisted
conjugation give non-conjugation action on `M_3(ℂ)`?

**Collapse:** on per-site `Cl(3) ≅ M_2(ℂ)` (Pauli irrep `γ_i = σ_i`),
the pseudoscalar `ω = σ_1 σ_2 σ_3 = i·I_2` is a **central scalar**
(Section 5.1). On `H_hw=1`, by the per-site uniqueness theorem and the
single-fermion-number sector reduction, `ω` acts as `i·I_3` (central
scalar). Pseudoscalar-twisted conjugation `α_ω(X) = ω X ω^{-1} = X` is
therefore **trivial** (Section 5.3, 5.4). Pseudoscalar-twisted
EXPONENTIATION `exp(iθ σ_3 ω / 2) = exp(-θ σ_3 / 2)` gives a NON-UNITARY
hyperbolic flow, not a U(1) (Section 5.5).

Either way (twist of conjugation = trivial, or exponentiation of twisted
generator = non-unitary), V4 cannot supply U(1)_b. (Runner Section 5:
PASS, 4 checks.)

### V5 — Spatial site-position-dependent phase (local-to-global lift)

**Proposal:** apply per-site phase `e^{iθ·n(x)·σ_3 / 2}` with `n(x)`
indexing site location. This gives a "shift" rather than uniform phase,
producing momentum-eigenstate phases on hw=1.

**Collapse:** any single-direction shift (e.g., `n(x) = x_1`) gives a
unitary `U_θ = diag(e^{iπθ}, 1, 1)` on `H_hw=1` (the (π,0,0) corner picks
up `e^{iπθ}`, others unchanged). This `U_θ` does NOT commute with C_3
(Section 6.2b), so conjugation by `U_θ` breaks `A^{C_3}` (Section 6.3).

To restore C_3-equivariance, sum over all three directions: `T_x · T_y · T_z = -I`
on hw=1 (Section 6.1b), giving a SCALAR for any continuous-θ extension.
Trivial on `M_3(ℂ)`. (Runner Section 6: PASS, 5 checks.)

More generally: any per-site phase with **C_3-equivariant** site-indexing
function `n(x)` yields a unitary on `H_hw=1` that COMMUTES with C, hence
is in the circulant algebra `A^{C_3}` (by Schur, since the centralizer
of C in U(3) is the maximal C_3-commuting torus = circulant unitaries).
Conjugation by such a unitary is **trivial on `A^{C_3}`** (Section 7.4)
since `A^{C_3}` is commutative as an algebra over ℂ.

## The structural obstruction theorem

**Theorem (Probe 17 sharpened bounded obstruction).**

```
Let U(θ): U(1) → U(M_2(ℂ)) be the retained per-site qubit U(1) on each
per-site Cl(3) ≅ M_2(ℂ). Let ⊗_x U_θ(x) be a per-site assignment of
this U(1) to each lattice site x ∈ Z³, restricted to the hw=1 BZ-corner
triplet. Let φ_θ: M_3(ℂ) → M_3(ℂ) be any of:
  (i) algebra-automorphism (= conjugation by some V_θ ∈ U(3));
  (ii) twisted conjugation X → U_θ X V_θ^* with U_θ ≠ V_θ;
  (iii) left-module action L_{U_θ}(X) = U_θ · X;
  (iv) pseudoscalar-twisted lift via ω ∈ Cl(3);
  (v) spatial site-position-graded phase composition.

Then φ_θ is NOT the U(1)_b symmetry on the b-doublet of A^{C_3}, for
the following structural reasons:

(a) Skolem-Noether rigidity. Every *-algebra automorphism of M_3(ℂ) is
    inner, i.e., conjugation by some V_θ ∈ U(3). Restricted to A^{C_3}
    (= circulants), conjugation by V_θ commuting with C is trivial
    (since A^{C_3} is commutative). Conjugation by V_θ NOT commuting
    with C breaks A^{C_3}. So no algebra-automorphism produces U(1)_b
    on A^{C_3}.

(b) Non-algebra-action failures. Twisted conjugation (V3), left-module
    action (V2), and pseudoscalar twist (V4) each fail at least one of:
    unital / multiplicative / Hermiticity-preserving / unitary. Hence
    none defines a U(1) action by *-algebra automorphisms of M_3(ℂ).

(c) Spectrum-non-preservation. U(1)_b on (a, b) ↦ (a, e^{iφ}b) does NOT
    preserve the spectrum of H = aI + bC + b̄C². Verified numerically
    (Section 7.6): for a=1, b=0.5+0.3i, the eigenvalues at φ=0 are
    {-0.0196, 1.0196, 2.0} and at φ=0.7 are {-0.144, 1.378, 1.766} —
    a different multiset. Since every unitary similarity preserves
    eigenvalues, U(1)_b CANNOT be implemented by ANY unitary similarity.

Therefore: U(1)_b is intrinsically a NON-UNITARY linear automorphism of
A^{C_3} (preserving its 4-real-dim vector-space structure but not its
spectral structure on the ambient M_3(ℂ)). No retained per-site qubit
U(1) lift produces U(1)_b. The A1 admission count is UNCHANGED.
```

**Proof.** Sections 2-6 verify each of the five attack vectors collapses.
Section 7 verifies Skolem-Noether and the spectrum-non-preservation
diagnostic. Section 8 verifies convention-robustness (scale invariance
preserved; C ↔ C^2 basis change preserves A^{C_3}; K-fixed-point of
A^{C_3} is the real-b line, confirming Probe 13's Z_2 not SO(2) finding).
Section 9 records the closure status. ∎

## What this probe contributes to the campaign

1. **Closes the non-conjugation case.** Probe 14 closed the
   algebra-automorphism (= conjugation) case for every retained U(1).
   Probe 17 closes the orthogonal "non-conjugation lift" case: V1-V5
   all collapse. Combined, Probes 14 + 17 close the entire space of
   "U(1)-action-on-M_3(ℂ) lifted from retained continuous symmetries."

2. **Identifies the deeper structural obstruction precisely.** U(1)_b
   is intrinsically NON-UNITARY as a transformation on M_3(ℂ). It does
   NOT preserve the spectrum of H. This is sharper than "every retained
   U(1) acts as conjugation"; it is "U(1)_b cannot be ANY unitary
   similarity, conjugation or otherwise."

3. **Sharpens the named admission residue.** The Probe 13 sharpening
   was: "the canonical SO(2) phase quotient on the non-trivial doublet
   of A^{C_3} = the U(1)_b symmetry of the Brannen δ-readout." Probe 17
   sharpens this further to:

   ```
   the canonical NON-UNITARY linear automorphism U(1)_b of A^{C_3}
   that fixes the trivial-character isotype (a-coefficient) and rotates
   the non-trivial doublet (b-coefficient) by phase, equivalent to a
   functional-level (not algebra-level) symmetry of the Brannen
   Q-readout.
   ```

   The U(1)_b is now *known to be a functional / readout symmetry, NOT
   an algebra symmetry of M_3(ℂ)*. This rules out a wide class of
   future attempts (any lift via lattice/continuous symmetry) and points
   to the third option flagged in Probe 13's honest assessment:

   > "Pivot to the SO(2)-quotient at the readout level (functional, not
   > algebraic). The Brannen Q-functional IS U(1)_b-invariant
   > (Q depends only on `|b|²/a²`, not arg(b)). So the SO(2)-quotient
   > could be enforced AT THE Q-READOUT STEP, not at the algebra level.
   > This would be a different framing: not 'M_3(ℂ) has a canonical
   > SO(2) symmetry', but 'the Koide functional Q(H) factors through
   > the SO(2)-quotient of H'."

   Probe 17 confirms that this readout-level framing is the **only**
   remaining option compatible with cited source-stack content; no algebra-level
   route exists.

## Convention-robustness check

The runner verifies (Section 8):

- **Scale invariance** of `|b|²/a²` is preserved under `H → cH` (T8.1). ✓
- **Basis change** `C → C² = C^{-1}` preserves A^{C_3} (T8.2). ✓
- **K-real-structure** fixed-point on A^{C_3} is the real-b line (Z_2
  fixed, not SO(2)) — confirming Probe 13's Z_2-not-SO(2) finding (T8.3). ✓

The new Probe 17 result is robust under:

- Choice of which faithful Cl(3) irrep (positive vs negative chirality) —
  the Skolem-Noether argument applies to both;
- Choice of basis for the C_3 cyclic shift (`C` vs `C^2`);
- Choice of C_3-character labeling (`ω` vs `ω̄`);
- Specific choice of per-site U(1) generator (any single Pauli or
  bivector — they're all equivalent under per-site uniqueness).

## Attack-vector enumeration

Per the eleven-probe campaign + Probes 12-16 synthesis, this is the
seventeenth attack vector:

| # | Attack vector | Outcome |
|---|---|---|
| 17 | Non-conjugation lift of retained per-site qubit U(1) (V1: character-graded; V2: bimodule; V3: twisted; V4: pseudoscalar; V5: spatial) | sharpened obstruction; all five collapse via Skolem-Noether + spectrum-non-preservation |

This refines the residue from Probe 14 (RETAINED_U1_HUNT). Specifically:

- **Probe 14** said: every retained U(1) acts as conjugation on M_3(ℂ).
  Probe 17 generalizes: even allowing non-conjugation lifts (V2 left-module,
  V3 twisted, V4 pseudoscalar, V5 spatial), no retained U(1) lift produces
  U(1)_b.

- **Probe 13 closure-step (d)** said: K alone supplies only Z_2 reflection,
  not SO(2) rotation, on the b-doublet. Probe 17 confirms this and adds:
  no continuous unitary group at all (regardless of how it's lifted to
  M_3(ℂ)) can supply the SO(2) rotation, because U(1)_b is non-unitary.

- **MRU note §4** identified the SO(2)-angular-quotient inside the
  doublet as the "missing object". Probes 13 and 17 jointly prove:
  this SO(2) is NOT a unitary symmetry of M_3(ℂ); it is at most a
  functional-readout symmetry of the Brannen Q-functional.

## Status block

### Author proposes (audit lane decides):

- `claim_type`: `bounded_theorem` (sharpened obstruction; no closure)
- audit-derived effective status: set only by the independent audit lane after review
- `admitted_context_inputs`: `["A1-condition: |b|²/a² = 1/2"]` —
  the residual admission, with the Probe 17 sharpening:
  "the U(1)_b symmetry is NOT a unitary symmetry of M_3(ℂ); it is at
  most a functional-readout symmetry of the Brannen Q-functional"

**No new admissions added by this probe.**

### What this probe DOES

1. Verifies that all five candidate non-conjugation lifts of retained
   per-site qubit U(1) collapse to one of: trivial scalar action;
   non-algebra group action; non-equivariant action breaking A^{C_3}.
2. Identifies the structural rigidity: Skolem-Noether forces every
   *-algebra automorphism of M_3(ℂ) to be inner.
3. Identifies the sharper obstruction: U(1)_b is spectrum-non-preserving,
   hence cannot be ANY unitary similarity.
4. Sharpens the residue from "U(1)_b angular quotient" (Probe 13) to
   "U(1)_b is a non-unitary functional-readout symmetry" — pointing
   to the third option flagged in Probe 13's honest assessment as the
   only remaining route.

### What this probe DOES NOT do

1. Does NOT close the A1-condition.
2. Does NOT add any new axiom or new admission.
3. Does NOT modify any retained theorem.
4. Does NOT promote any downstream theorem.
5. Does NOT load-bear PDG values into a derivation step.
6. Does NOT modify the audit-honest options enumerated by the
   eleven-probe campaign synthesis or Probes 12-13 (admit/derive/pivot).
7. Does NOT promote the readout-level pivot to a closure; that pivot
   remains a separate route requiring its own derivation.

## Honest assessment

Probe 17 was the most concrete remaining attack vector after Probes 12-14
identified the U(1)_b residue as the sole missing primitive. It exploited
the framework's "continuous in qubit operations" structure (the per-site
qubit U(1) on each Cl(3) ≅ M_2(ℂ)) — a structural feature that prior
probes had not fully tested.

The honest finding: **per-site qubit U(1) is the wrong group**. Not because
it's discrete or has the wrong rank, but because:

1. **As a continuous symmetry, per-site qubit U(1) acts on the lattice
   Hilbert space H_lat by a tensor-product unitary `⊗_x U_θ(x)`. Restricted
   to H_hw=1 (a 1-particle sector), this acts as a single unitary on a
   3-dim Hilbert space. By Skolem-Noether, the induced action on M_3(ℂ)
   is conjugation. Hence Probe 14's domain.**

2. **Even relaxing the "lift via single Hilbert-space unitary" requirement
   to allow non-conjugation actions (V2-V5), all such actions either fail
   to be group homomorphisms / *-algebra actions, or collapse to scalar.**

3. **The fundamental obstruction: U(1)_b is intrinsically non-unitary on
   M_3(ℂ). It changes the spectrum of H. No unitary similarity can do that.**

The probe's contribution to the campaign is therefore:

- **Confirmation that all algebra-level U(1) routes are closed.** Probes
  14 + 17 jointly close the algebra-level closure space.
- **Identification of the only remaining option.** The readout-level pivot
  (Probe 13's option 3): not "M_3(ℂ) has a canonical SO(2) symmetry", but
  "the Koide functional Q(H) factors through the SO(2)-quotient of H".
  This is qualitatively different from any prior closure attempt — it
  doesn't require a symmetry of the algebra, only of the readout
  functional. Whether such a readout-level pivot is itself derivable from
  cited source-stack content is a separate question (and a candidate for a future
  probe).

The campaign's residue is now: **whether the SO(2)-quotient on the b-doublet
can be enforced at the Brannen Q-readout level (functional, not algebraic)
and whether such a readout-level enforcement is derivable from retained
content**. This is more precisely localized than Probe 13's "U(1)_b angular
quotient" phrasing, which left ambiguous whether the symmetry was algebra-
or readout-level. Probe 17 closes the algebra-level route negatively.

## Cross-references

### Foundational baseline

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Per-site uniqueness: [`AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md`](AXIOM_FIRST_CL3_PER_SITE_UNIQUENESS_THEOREM_NOTE_2026-04-29.md)
- Per-site SU(2) spin-1/2: [`PER_SITE_SU2_SPIN_HALF_THEOREM_NOTE_2026-05-02.md`](PER_SITE_SU2_SPIN_HALF_THEOREM_NOTE_2026-05-02.md)
- Multi-site Pauli group: [`MULTISITE_PAULI_GROUP_THEOREM_NOTE_2026-05-02.md`](MULTISITE_PAULI_GROUP_THEOREM_NOTE_2026-05-02.md)
- Substep-4 AC narrowing: [`STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`](STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md)

### Retained provenance of the C_3 / circulant structure

- BZ-corner forcing: [`STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md`](STAGGERED_DIRAC_BZ_CORNER_FORCING_THEOREM_NOTE_2026-05-07.md)
- M_3(ℂ) on hw=1: [`THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md`](THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
- Circulant character / eigenvalue: [`KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md`](KOIDE_CIRCULANT_CHARACTER_DERIVATION_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence: [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

### Block-total Frobenius and weight-class structure

- Block-total Frobenius: [`KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md`](KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM_NOTE_2026-04-19.md)
- MRU weight-class + reduced two-slot carrier `(ρ_+, ρ_⊥)`: [`KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md`](KOIDE_MRU_WEIGHT_CLASS_OBSTRUCTION_THEOREM_NOTE_2026-04-19.md)

### Eleven-probe campaign + Probes 12-16

- Synthesis (campaign terminal state): [`KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md`](KOIDE_A1_11_PROBE_CAMPAIGN_BOUNDED_ADMISSION_META_NOTE_2026-05-08.md)
- Probe 1 (RP/GNS): [`KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md`](KOIDE_A1_PROBE_RP_FROBENIUS_BOUNDED_OBSTRUCTION_NOTE_2026-05-08_probe1.md)
- Probe 7 (Z_2 × C_3 pairing; structural locus): synthesis cross-ref
- Probe 12 (Plancherel / Peter-Weyl): [`KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md`](KOIDE_A1_PROBE_PLANCHEREL_PETER_WEYL_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe12.md)
- Probe 13 (real-structure / antilinear-involution): [`KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md`](KOIDE_A1_PROBE_REAL_STRUCTURE_BOUNDED_OBSTRUCTION_NOTE_2026-05-09_probe13.md)
- Probe 14 (RETAINED_U1_HUNT, immediate predecessor): PR #784 (referenced)

## Validation

```bash
python3 scripts/cl3_koide_a1_probe_lattice_non_conjugation_2026_05_09_probe17.py
```

Expected: `=== TOTAL: PASS=56, FAIL=0 ===`

The runner verifies:

1. Retained inputs (Section 1): C is unitary, order 3, eigenvalues
   `{1, ω, ω̄}`; H = aI + bC + b̄C² is Hermitian and circulant; Pauli
   `σ_3` has eigenvalues `{-1, +1}`; per-site qubit U(1) `exp(iθσ_3/2)`
   is in U(2).

2. V1 character-graded phase (Section 2): C_3-equivariant per-site phase
   collapses to scalar; non-equivariant breaks A^{C_3}.

3. V2 bimodule action (Section 3): left-module is not a group action
   (not multiplicative); circulant left-multiplication mixes a and b.

4. V3 twisted conjugation (Section 4): IS a group action but is not
   unital, not multiplicative, not Hermiticity-preserving.

5. V4 pseudoscalar twist (Section 5): pseudoscalar is central scalar
   `i·I`; conjugation-twist is trivial; exponentiation-twist is
   non-unitary.

6. V5 spatial phase (Section 6): single-direction shift breaks C_3;
   C_3-symmetrized shift = scalar.

7. Structural obstruction (Section 7): Skolem-Noether forces inner
   automorphism; conjugation by C_3-commuting U is trivial on A^{C_3};
   U(1)_b does NOT preserve the spectrum of H.

8. Convention-robustness (Section 8): scale invariance preserved;
   basis change C ↔ C² preserves A^{C_3}; K-fixed-point of A^{C_3} is
   the real-b line (Z_2 only, not SO(2)).

9. Closure status (Section 9): A1 admission count unchanged; Probes
   14 + 17 jointly close all algebra-level U(1) closure routes.
