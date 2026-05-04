# Scalar-Tensor Ray Complementarity (STRC) — Historical Observable-Principle Framing (SUPERSEDED)

**Date:** 2026-04-19
**Lane:** Quark up-amplitude LO-balance.
**Status:** support / route-history note (status line rephrased 2026-04-28 per audit-lane verdict). **SUPERSEDED** by the explicit derivation in `docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`. This note records the earlier observable-principle framing of STRC-LO and should not be cited as the primary source for the STRC-LO relation.
This note is kept as route-history only and should not be cited as
the primary STRC source.
**Primary runner:** `scripts/frontier_quark_strc_observable_principle.py`
(PASS=19 FAIL=0) — verifies the STRC identity and its implications,
independent of derivation framing.

---

## 0. Executive summary

**STRC (Scalar-Tensor Ray Complementarity)** is a linear amplitude sum
rule on the 1(+)5 CKM projector ray:

    a_u  +  rho * sin(delta_std)  =  sin(delta_std)          (STRC-LO)

equivalently (solved for `a_u`):

    a_u  =  Im(p) * (1 - Re(r))  =  sin(delta_std) * (1 - rho)

where `p = cos(delta_std) + i sin(delta_std)` is the retained unit
projector ray, `r = rho + i eta = p / sqrt(7)` is the collinear scalar
ray, and `a_u`, `a_d = rho` are the retained real reduced amplitudes.

**Structural parallel to Koide.** STRC is to CKM reduced amplitudes
what the Koide sum rule is to charged-lepton square-root masses: a
single linear scalar relation retained as an observable principle
rather than derived from symmetry or unitarity.

| Principle | Sector | Form | Status |
|:---|:---:|:---:|:---:|
| Koide | Charged lepton sqrt-masses | `(sum m) / (sum sqrt(m))^2 = 2/3` | Retained observable |
| **STRC** | CKM reduced amplitudes | `a_u + rho * sin_d = sin_d` | **Retained observable** |

Both are scalar amplitude relations on a specific retained ray;
neither is a consequence of retained quadratic structure.

**Six SM-native structural sources ruled out.** The LO balance is not
derivable from electroweak charges, 1(+)5 block factorization,
first-row unitarity NLO, discrete flavor groups, anomaly cancellation,
or Clifford bimodule scalar-ray retention (see Sec. 3). A literature
survey of standard SM-adjacent sum rules (QLC, Koide extensions,
Froggatt-Nielsen, SO(10) mass sum rules) also does not produce STRC.
Retention of STRC as an observable principle is the minimal path to
closing the quark up-amplitude gate.

**Numerical verification.** RPSR holds exactly under STRC; target
`a_u = 0.7748865611` reproduced to 10 decimals.

---

## 1. Statement of the principle

### 1.1 Background (retained)

On the retained 1(+)5 CKM projector ray:

- `p = cos(delta_std) + i sin(delta_std)`, `|p|^2 = 1` (unit tensor
  projector ray; `CKM_ATLAS_AXIOM_CLOSURE_NOTE`).
- `r = rho + i eta = p / sqrt(7)`, `|r|^2 = 1/7` (retained scalar-
  comparison ray; `SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19`).
- `a_d = rho = 1 / sqrt(42)` (`QUARK_PROJECTOR_PARAMETER_AUDIT`).
- Retained atoms: `sin_d = sqrt(5/6)`, `cos_d = 1/sqrt(6)`,
  `eta = sqrt(5/42)`, `supp = 6/7`, `delta_A1 = 1/42`.

### 1.2 Statement (STRC-LO)

*On the common 1(+)5 CKM projector ray with `a_d = rho = Re(r)`
retained, the up-sector reduced amplitude `a_u` satisfies the linear
completeness relation*

    a_u  +  a_d * sin(delta_std)  =  sin(delta_std).                (STRC-LO)

*Geometrically, `a_u` equals the unit tensor ray's imaginary-axis
component reduced by the scalar ray's real-axis fraction:*

    a_u  =  Im(p) * (1 - Re(r)).

### 1.3 NLO extension

STRC combined with the retained minimal 3-atom contraction
`rho * supp * delta_A1 = rho / 49` gives RPSR:

    a_u / sin_d  +  a_d  =  1 + rho / 49  =  1 + rho * supp * delta_A1.

This reproduces target
`a_u = sqrt(5/6) * (1 - 48 rho / 49) = 0.7748865611` to 10 decimals.

---

## 2. Structural parallel to Koide

STRC and Koide share four structural features:

1. **Linear scalar relation.** Both are single real-valued linear sum
   rules on a fixed basis; neither is a quadratic normalization.
2. **Retained specific ray.** Koide is on the charged-lepton
   sqrt-mass triplet (orthonormal basis in `R^3`). STRC is on the
   retained 1(+)5 CKM projector ray (a specific unit direction in
   `C^6`).
3. **Amplitude (not symmetry) principle.** Both fix a specific linear
   combination; neither is a symmetry axiom (gauge, discrete, or
   global).
4. **Retention is observable-principle level.** Neither is derivable
   from the retained Clifford / Z_d / unitarity stack; both are
   promoted to retained principle at the same epistemic level.

### 2.1 Algebraic form in framework blocks

    a_u  =  sqrt(5) * (sqrt(42) - 1) / (6 * sqrt(7))

This expresses `a_u` as an algebraic number in `{sqrt(5), sqrt(7)}`:
the 5 from the 5-plet dimension (tensor block), the 7 from the
scalar-ray `A_1` democratic block (`1 + 6 = 7`). STRC is therefore a
**block-algebra identity**; both roots come from retained structure.

---

## 3. Six SM-native candidate derivations do not close STRC

Six named candidate SM-native structural sources were systematically
checked and each fails to reproduce the specific linear combination
`a_u + rho * sin_d = sin_d`.

### 3.1 Angle 1: EW-charge asymmetry

Tested: `Q_u^2 a_u + Q_d^2 a_d = Q_u^2 sin_d`,
`a_u / |Q_u| = sin_d (1 - rho/|Q_u|)`, and a systematic enumeration
of linear charge-weighted combinations. **All fail.** Denominators
from `Q = 2/3, 1/3` produce `3, 9`, not `7`; `rho = 1/sqrt(42)` needs
the `sqrt(7)` from the scalar block, absent in EW-charge arithmetic.

Side identity (genuine cross-link, not a derivation):
`Q_u^2 + Q_d^2 = (2/3) sin^2(delta_std) = 5/9`.

### 3.2 Angle 2: 1(+)5 block-factor decomposition

Block-weighted sums with weights `{1, 5, 6, 1/6, 5/6}` do not
reproduce the linear combination. Cross-link:
`6 * rho = sqrt(6/7) = sqrt(supp)`, giving the clean factorization
`rho = sqrt(supp) / 6 = 1 / sqrt(42)`. This pins `rho` in block
dimensions but does not force the **linear** balance
`a_u + rho sin_d = sin_d` from block-weighted **quadratic** sums.

### 3.3 Angle 3: First-row unitarity NLO

CKM first-row unitarity NLO (`|V_ub|^2 ~ 1.9e-6`) is ~1000x smaller
than the LO-balance NLO correction (`rho / 49 ~ 3.1e-3`). Scales
incompatible; row-unitarity NLO cannot be the structural source.

### 3.4 Angle 4: Discrete flavor symmetries

`A_4` tri-bimaximal: predicts `|U_e2|^2 = 1/3`, incompatible with
retained `sin^2(delta_std) = 5/6`. STRC's `a_u` is algebraic in
framework block roots `{sqrt(5), sqrt(7)}`, not in small-discrete-
group character rings (`A_4`, `S_4`, `Delta(27)`, `T'`). Koide-scan
`(a_u + a_d) / (sqrt(a_u) + sqrt(a_d))^2 = 0.573` does not match
`2/3` or other clean Koide numbers.

### 3.5 Angle 5: Anomaly cancellation

SM anomalies cancel exactly per generation, pinning zero free
parameters. Side identity (mnemonic, not derivation):
`3/4 + 1/12 = 5/6 = sin^2(delta_std)`. No linear amplitude sum rule
arises from anomaly arithmetic.

### 3.6 Angle 6: Clifford bimodule

The retained `Cl(3)/Z_3` acts on hw=1 for the scalar-ray sector. A
natural extension to the CKM sector is the bimodule
`Cl(3)/Z_3 (x) Cl_CKM(1(+)5)`. On this bimodule, `|p|^2 = 1` is
*quadratic* and `r || p` is *directional*, but STRC is a *linear*
amplitude completeness statement. **Quadratic bimodule unitarity does
not force linear amplitude sum rules.** This is the sharp structural
obstruction: STRC's *type* (linear amplitude completeness) is
different from retained quadratic normalization and directional
collinearity.

### 3.7 Angle 7: Literature survey

Surveyed candidates: quark-lepton complementarity (QLC;
`theta_C + theta_12^PMNS = pi/4`), Koide-type sum rules,
Froggatt-Nielsen flavon mechanisms, SO(10) GUT mass sum rules,
Uhlig 1982 Hermitian-pencil structure (relevant for `F_4` via DPLE,
not for CKM linear amplitude sum rules). None of these
literature-standard structures produces `a_u + rho sin_d = sin_d`
directly. STRC is **novel** as a CKM-amplitude sum rule.

### 3.8 Verdict

All six SM-native angles and the literature survey fail to derive STRC
from retained or retained-adjacent structure. The LO balance is a
genuinely new linear amplitude sum rule on the CKM projector ray.
Retention as an observable principle (STRC) is the minimal-cost path.

---

## 4. Numerical verification

### 4.1 STRC LO form

    a_u_LO  =  sin_d * (1 - rho)  =  0.7720118867
    a_u_LO + rho * sin_d          =  0.9128709292
    sin_d                          =  0.9128709292
    |LHS - RHS|                    =  0.00e+00

### 4.2 STRC + NLO = RPSR target

    a_u_target  =  sin_d * (1 - 48 rho / 49)  =  0.7748865611  (10 dec)
    a_u_target / sin_d + a_d                  =  1 + rho / 49

### 4.3 Retained no-go regression

All 7 retained no-gos pass. Target `a_u = 0.7748865611` reproduced to
10 decimals. `frontier_quark_projector_parameter_audit.py`: PASS=6
FAIL=0.

---

## 5. Scenario A: bundling with `QUARK_PROJECTOR_PARAMETER_AUDIT`

### 5.1 Existing retention

`docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` retains
`a_d = rho = 1 / sqrt(42)` as a reduced-amplitude axiom.

### 5.2 STRC-augmented retention (Scenario A)

The single retained reduced-amplitude axiom is upgraded to:

> *Retained reduced-amplitude axiom (STRC-augmented).*
> *On the 1(+)5 CKM projector ray with `a_d = rho` (scalar-ray real
> axis) and `a_u` the up-sector tensor-ray amplitude, STRC-LO holds:*
>
>     a_u + a_d * sin(delta_std)  =  sin(delta_std)
>
> *with NLO correction `rho * supp * delta_A1 = rho / 49` from the
> retained scalar-tensor support bridge.*

This single axiom subsumes the two formerly separate retentions
(`a_d = rho` and the up-amplitude atlas conditional). Net axiom
cost is approximately 1 observable principle.

### 5.3 Axiom-count scenarios

| Scenario | STRC status | 4-gate outcome |
|:---|:---|:---|
| A (bundled, recommended) | Bundled into `QUARK_PROJECTOR_PARAMETER_AUDIT` | current honest meta read: `DIM-UNIQ + STRC` |
| B (standalone) | New standalone observable axiom | route-history packaging without the meta compression |
| C (future) | Derived via bimodule ray-saturation theorem | stronger meta-closure than A; still not reviewer-grade by itself |

Scenario C target:
`docs/CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`.

---

## 6. Cross-sector picture

| Sector | Retention | Type |
|:---|:---|:---|
| Charged leptons | Koide sum rule | Linear amplitude on sqrt-mass triplet |
| **Quarks** | **STRC** | **Linear amplitude on CKM projector ray** |
| Neutrinos | `sigma = 0` (no-go) | Trivial |
| DM | DPLE theorem | Dim-parametric log det extremum |

STRC is the quark-sector analog of Koide for leptons: a linear
amplitude sum rule retained as an observable principle on a specific
retained ray.

---

## 7. Cross-links (novel identities)

Novel exact identities on the retained atom bank:

1. `Q_u^2 + Q_d^2 = (2/3) * sin^2(delta_std)` (EW charges x tensor
   block).
2. `6 * rho = sqrt(6/7) = sqrt(supp)` (scalar/tensor block bridge).
3. `a_u = sqrt(5) * (sqrt(42) - 1) / (6 sqrt(7))` (framework-block
   algebraic form).
4. `3/4 + 1/12 = sin^2(delta_std)` (anomaly-residual mnemonic).
5. `rho = Re(r) = cos(delta_std) / sqrt(7)` (scalar-ray real axis).
6. `a_u = Im(p) * (1 - Re(r))` (cleanest geometric form of STRC).

These serve as bridges toward the future bimodule ray-saturation
theorem.

---

## 8. Limitations and honest framing

1. STRC is an **observable principle**, not a theorem. It has the
   same epistemic status as Koide for leptons: a retained linear
   amplitude sum rule not derivable from retained symmetry or
   unitarity.
2. The six named SM-native sources ruled out are exhaustive for
   standard-literature structural sources (EW, discrete flavor, GUT
   sum rules, anomaly); they do not exclude every conceivable
   derivation.
3. Scenario A bundling saves one axiom slot relative to Scenario B.
   The net axiom cost of ~1 observable principle should not be
   misread as "zero axiom cost."
4. Scenario C is a **future target**, not a result. See the bimodule
   ray-saturation note.

---

## 9. Cross-references

- `docs/QUARK_UP_AMPLITUDE_RPSR_CONDITIONAL_THEOREM_NOTE_2026-04-19.md`
  (RPSR derivation; conditional closure)
- `docs/QUARK_PROJECTOR_PARAMETER_AUDIT_NOTE_2026-04-19.md` (retained
  `a_d = rho`; Scenario A bundling host)
- `docs/CKM_ATLAS_AXIOM_CLOSURE_NOTE.md` (retained unit projector
  ray, `supp`, `delta_A1`)
- `docs/SCALAR_TENSOR_RAY_MAGNITUDE_BRIDGE_NOTE_2026-04-19.md`
  (retained scalar ray `r`, magnitude `1/sqrt(7)`)
- `docs/CLIFFORD_BIMODULE_RAY_SATURATION_FUTURE_TARGET_NOTE_2026-04-19.md`
  (future target: derive STRC as theorem)
- `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md` (reading order)

---

## 10. Runner

`scripts/frontier_quark_strc_observable_principle.py` verifies:

- STRC-LO identity (linear form).
- STRC geometric form `a_u = Im(p) * (1 - Re(r))`.
- All seven rule-outs (six SM-native sources + literature survey).
- RPSR closure under STRC + minimal 3-atom NLO.
- Uniqueness vs Pareto candidates.
- Framework-block algebraic form for `a_u`.
- No retained no-go regression.

Expected: PASS=19 FAIL=0.

## Audit boundary (2026-04-28)

Audit verdict (`audited_failed`, leaf criticality):

> Issue: The proposed-retained claim is a superseded route-history
> observable-principle framing, and its runner hard-codes
> `a_u_LO = sin_d * (1 - rho)` before verifying STRC and RPSR
> identities. Why this blocks: finite rule-outs of several candidate
> sources plus algebraic consequences of an assumed relation do not
> derive the STRC relation or justify retaining this note as the
> primary source, and the note itself directs readers to a separate
> collinearity theorem for derivation.

The note has been re-tiered to `support` (route-history). Readers
should cite `docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`
for the STRC-LO derivation.

## What this note does NOT claim

- A derivation of STRC-LO. The runner assumes
  `a_u_LO = sin_d * (1 - rho)` rather than deriving it; the genuine
  derivation is in the separate collinearity theorem note.
- A primary-source role for the STRC-LO relation.
- A retained observable-principle status — that framing is superseded.

## What would close this lane (Path A future work)

Not applicable: the derived theorem already exists in
`docs/STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md`. This note is
preserved only as route-history support.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [strc_lo_collinearity_theorem_note_2026-04-19](STRC_LO_COLLINEARITY_THEOREM_NOTE_2026-04-19.md)
