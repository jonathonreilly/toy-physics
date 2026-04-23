# Clifford Bimodule Ray-Saturation Theorem — Future Target

**Date:** 2026-04-19
**Lane:** Quark up-amplitude.
**Status:** **Future mathematical target.** Explicitly NOT a retained
theorem. Named and scoped as the concrete math target that, if proven,
would derive STRC
(`docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md`) from
retained structure alone and reduce the full scalar-selector axiom
cost from ~1 observable principle (Scenario A) to 0 (Scenario C). No
retention is claimed here.

---

## 0. Executive summary

**Ray-saturation theorem (proposed target).** On the Clifford
bimodule

    M_CKM  =  Cl(3) / Z_3  (x)  Cl_CKM(1 (+) 5)

prove that the retained pre-conditions (bimodule unitarity,
scalar-tensor support bridge `supp = 6/7`, democratic center-excess
`delta_A1 = 1/42`) jointly force the linear amplitude completeness
relation

    a_u  +  a_d * sin(delta_std)  =  sin(delta_std)                     (STRC-LO)

on the imaginary axis of the retained unit projector ray
`p = cos(delta_std) + i sin(delta_std)`.

If proven, STRC ceases to be a standalone observable principle and becomes a
derived theorem on the quark side. That would tighten the
**meta-axiom** accounting of the scalar-selector program substantially, but it
would still sit alongside the separate per-lane object-derivation work needed
to clear the reviewer's bar.

This note documents the target, its significance, and concrete
approach hints. It does not claim any retention.

---

## 1. Why this target

Six SM-native structural sources were ruled out for STRC
(electroweak charges, 1(+)5 block factor, row-unitarity NLO,
discrete flavor groups, anomaly cancellation, Clifford bimodule
scalar-ray retention alone; see
`docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md` Sec. 3).
The Clifford bimodule (Angle 6) identifies the structural obstruction
sharply:

> STRC is a **linear** amplitude sum rule, but retained bimodule
> structure supplies only **quadratic** normalization (`|p|^2 = 1`,
> `|r|^2 = 1/7`) and directional collinearity (`r || p`). Quadratic
> + directional does not force a linear amplitude completeness
> relation.

What is therefore needed is a **new structural principle** internal
to the bimodule that produces linear amplitude sum rules. The
literature for SM-adjacent physics (QLC, Koide, Froggatt-Nielsen,
SO(10) sum rules) does not contain this principle. A ray-saturation
theorem on the bimodule is the minimal mathematical object that
could supply it.

---

## 2. Precise statement of the target

### 2.1 Setup

Retained ingredients on the CKM sector:

- Tensor projector ray `p = cos(delta_std) + i sin(delta_std)` with
  `|p|^2 = 1`, on the 1(+)5 decomposition of `sym^2 R^3`
  (`CKM_ATLAS_AXIOM_CLOSURE_NOTE`).
- Scalar-comparison ray `r = rho + i eta = p / sqrt(7)` with
  `|r|^2 = 1/7`, collinear with `p`
  (`SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19`).
- Scalar-tensor support `supp = 6/7` retained on
  `CKM_ATLAS_AXIOM_CLOSURE_NOTE`.
- Democratic center-excess `delta_A1 = 1/42` at `r = sqrt(6)`.
- Retained `a_d = rho` (`QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE`).

### 2.2 Bimodule

The proposed bimodule:

    M_CKM  =  Cl(3) / Z_3  (x)  Cl_CKM(1 (+) 5)

where:

- `Cl(3) / Z_3` is the retained Z_3-quotient Clifford algebra acting
  on the scalar-ray sector (hw = 1; retained in
  `DIMENSION_SELECTION_NOTE`, `CKM_ATLAS_AXIOM_CLOSURE_NOTE`).
- `Cl_CKM(1 (+) 5)` is the Clifford algebra on the 6-dimensional
  tensor direction of `sym^2 R^3` (the 1-plet + 5-plet
  decomposition).

### 2.3 Theorem statement (target)

> **Ray-saturation theorem on `M_CKM` (target).**
> *On the Clifford bimodule
> `M_CKM = Cl(3)/Z_3 (x) Cl_CKM(1(+)5)` with retained bimodule
> unitarity, scalar-tensor support bridge `supp = 6/7`, and
> democratic center-excess `delta_A1 = 1/42`, the reduced amplitudes
> `a_u, a_d in R` on the common 1(+)5 projector ray satisfy the
> linear completeness relation*
>
>     a_u  +  a_d * sin(delta_std)  =  sin(delta_std)                    (STRC-LO)
>
> *together with the NLO correction (already retained)*
>
>     a_u / sin_d + a_d  =  1 + rho * supp * delta_A1.                   (RPSR)

If proven, STRC becomes a theorem; the "observable principle" status
is upgraded to derived-theorem status.

---

## 3. Significance

### 3.1 Axiom-count consequence

Current state (Scenario A):

- public: support/conditional packet, not full closure
- meta-axiom layer: `DIM-UNIQ + STRC`

If the bimodule ray-saturation theorem is proven:

- public: still requires the separate per-lane object derivations
- meta-axiom layer: tighter than `DIM-UNIQ + STRC`, because STRC is no longer
  carried separately as an observable principle

This is the honest **Scenario C** read: stronger meta-closure across the
scalar-selector investigation, not an automatic reviewer-grade closure.

### 3.2 Structural consequence

The three existing non-quark routes (MRU, Berry, DPLE) already fit one
dim-uniqueness pattern. A proven ray-saturation theorem would make the
quark-side route structurally less isolated and would strengthen the
meta-closure story substantially. But that uniformity would still sit above,
not replace, the object-derivation requirement on each lane.
by eliminating any residual "observable principle" from the scalar-
selector investigation.

---

## 4. Approach hints

These are suggestive directions, **not proofs**. Each is a concrete
research target.

### 4.1 Frobenius-type scalar-tensor duality

The cross-link `6 * rho = sqrt(supp) = sqrt(6/7)` suggests a
Frobenius-type reciprocity between the scalar-ray and tensor-ray
embeddings. A Frobenius identity of the form

    <r, p>_scalar  *  <p, r>_tensor  =  supp

(schematic) would relate scalar and tensor inner products by the
support bridge. Linear amplitude sum rules could emerge from
Frobenius-type pairings rather than quadratic normalizations.

### 4.2 Anomaly inflow on the bimodule

Anomaly inflow between sectors (anomaly in one sector balanced by
inflow from another) is naturally linear in amplitudes. Extending
retained anomaly cancellation (SM anomalies cancel per generation)
to a bimodule-internal inflow principle on `M_CKM` could supply the
linear amplitude structure. SM anomaly cancellation itself does not
produce STRC; bimodule-internal inflow is a different and unexplored
direction.

### 4.3 Bimodule unitarity + democratic center-excess saturation

The retained atoms `supp = 6/7` and `delta_A1 = 1/42` combine as
`supp * delta_A1 = 1/49`, the retained NLO 3-atom contraction. If
the bimodule has a "ray-saturation" notion — a statement that the
reduced amplitudes fully span the retained-ray complement — then
the combination of bimodule unitarity with saturation at
`supp * delta_A1` might produce STRC.

### 4.4 Representation-theoretic content

`Cl(3) / Z_3` has specific isotype decomposition on the Koide
singlet-doublet pair (retained in
`KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE`). `Cl_CKM(1 (+) 5)` has its
own isotype decomposition under `SO(3)`. The tensor product
`M_CKM = Cl(3)/Z_3 (x) Cl_CKM(1 (+) 5)` inherits a bi-isotype
structure. If a linear amplitude relation emerges at the unique
bi-isotype where both factors act as singlets (or as matched
doublets), that would be a representation-theoretic source for
STRC.

### 4.5 RG flow fixed point on reduced amplitude space

`QUARK_PROJECTOR_PARAMETER_AUDIT` retains a unique Pareto target. If
the reduced amplitude space `(a_u, a_d) in R^2` admits a natural RG
flow under a retained gauge coupling, and that flow has a unique
UV/IR fixed point, the fixed point could coincide with the STRC
surface. This is speculative but concrete.

---

## 5. What this note does NOT claim

1. **No theorem is proven.** Section 2.3 is a target statement, not
   a result.
2. **No retention is claimed.** STRC remains an observable principle
   under the current state (Scenario A).
3. **No approach is validated.** The Section 4 approach hints are
   suggestive directions, not pre-registered claims.
4. **No paper claim depends on this target.** The publishable claim
   now rests on the honest support/conditional packet plus the
   `DIM-UNIQ + STRC` meta-closure read; this note flags the future
   target for transparency.

---

## 6. Cross-references

- `docs/QUARK_STRC_OBSERVABLE_PRINCIPLE_NOTE_2026-04-19.md` (STRC;
  six SM-native sources ruled out)
- `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
  (RPSR; conditional on STRC)
- `docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
  (retained `|r|^2 / |p|^2` and `supp = 6/7`)
- `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` (retained unit projector
  ray, `supp`, `delta_A1`)
- `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`
  (retained Z_3 isotype structure on `Cl(3)/Z_3`)
- `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md` (reading order)

---

## 7. Honest status

**This is a named research target, not a retained theorem.**

It is flagged here so that (a) reviewers can see the concrete path
to Scenario C, (b) future work has a pre-registered mathematical
object to attack, and (c) the axiom-count claim (Scenario A: ~1
observable principle) is bounded explicitly — the remaining gap is
precisely the content of this target.

No portion of the current publishable claim rests on this target
being proven.
