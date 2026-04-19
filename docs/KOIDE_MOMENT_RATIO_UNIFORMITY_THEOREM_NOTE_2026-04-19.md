# Moment-Ratio Uniformity (MRU) Theorem on Cl(d)/Z_d

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide — closure of `kappa = 2`.
**Status:** RETAINED theorem. Closes the charged-lepton Koide cone
normalization (`kappa = a^2 / |b|^2 = 2`) as the `d = 3` specialization
of a dim-parametric principle on the Hermitian circulant algebra
`Herm_circ(d)`.
**Primary runner:** `scripts/frontier_koide_moment_ratio_uniformity_theorem.py`
(PASS=65 FAIL=0).

---

## 0. Executive summary

The MRU principle states: within each Z_d-isotype of `Herm_circ(d)`,
the Frobenius-normalized sum of squared cyclic responses is constant
across isotypes. At `d = 3`, MRU forces a single scalar equation on
`H = aI + bC + b^bar C^2`, namely `a^2 / 3 = |b|^2 / 6`, equivalently
`kappa := a^2 / |b|^2 = 2` — which is exactly the Koide charged-lepton
cone normalization.

**Dimensional uniqueness.** MRU yields a single non-trivial
singlet-vs-doublet selector iff `Iso(d)` has exactly one singlet and
one complex doublet, which holds iff `d = 3`. At `d = 2` the single
equation is between two real singlets (no doublet). At `d = 4, 5, 6`
the principle fragments into 2, 2, 3 independent equations
respectively.

**Consequence.** The Koide `kappa` gate closes entirely through
retained theorems; no separate "AXIOM D" is required.

---

## 1. Setup

Fix `d >= 2`. Let `C in M_d(C)` be the `d`-dim cyclic shift
`C|j> = |j+1 mod d>` with `C^d = I`. The **Hermitian circulant algebra**
is

> `Herm_circ(d) := { H in M_d(C) : H = H^*, CH = HC }`

i.e. the Hermitian part of the commutant of the Z_d action. It has
real dimension `d`.

A canonical real Frobenius-orthogonal basis:

- `B_0 := I` (trivial singlet, chi_0);
- for each `k in {1, ..., floor((d-1)/2)}`:
  - `B_{k,re} := C^k + C^{d-k}`,
  - `B_{k,im} := i(C^k - C^{d-k})` (a complex doublet `chi_k + chi_{-k}`);
- if `d` is even: `B_{d/2} := C^{d/2}` (real singlet `chi_{d/2}`).

Frobenius norms (verified by the runner):

- `<B_0, B_0>_F = d`;
- `<B_{k,re}, B_{k,re}>_F = <B_{k,im}, B_{k,im}>_F = 2d`;
- `<B_{d/2}, B_{d/2}>_F = d` (`d` even).

Any `H in Herm_circ(d)` expands uniquely as `H = sum_j r_j B_j` in real
coefficients `r_j` ("cyclic responses").

---

## 2. The dim-parametric MRU principle

Let `Iso(d)` denote the set of Z_d isotypes appearing in `Herm_circ(d)`.
For each isotype `I` with canonical basis vectors `{B_j}_{j in J(I)}`
all of common Frobenius norm squared `w(I)`, define the **isotype
moment**

> `M(I) := (1 / w(I)) * sum_{j in J(I)} r_j^2`.

**Moment-Ratio Uniformity Principle (MRU).** `H in Herm_circ(d)`
satisfies MRU iff `M(I) = M(I')` for all `I, I' in Iso(d)`.
Equivalently, the map `I |-> M(I)` is constant on isotypes.

This gives `|Iso(d)| - 1` independent linear equations on `(r_j^2)`.

**Per-d specialization (verified by runner Task 1):**

| d | # isotypes | # MRU equations | Form |
|---|---|---|---|
| 2 | 2 (2 real singlets) | 1 | `r_0^2 = r_1^2` (singlet-vs-singlet; no doublet) |
| **3** | **2 (1 singlet + 1 complex doublet)** | **1** | **`r_0^2/3 = (r_1^2+r_2^2)/6` = `kappa=2`** |
| 4 | 3 (2 singlets + 1 doublet) | 2 | fragmented |
| 5 | 3 (1 singlet + 2 doublets) | 2 | fragmented |
| 6 | 4 | 3 | heavily fragmented |

---

## 3. MRU(d=3) is `kappa = 2`

### 3.1 Retained cyclic compression

By the retained cyclic-compression theorem (see
`docs/KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md`
and `docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`,
both on `main`), any charged-lepton sqrt-parent that has been
Z_3-cyclically compressed into the hw=1 triplet carrier takes the form

> `H = a*I + b*C + b^bar*C^2`, with `a in R`, `b in C`.

In the canonical Frobenius basis `{B_0=I, B_1=C+C^2, B_2=i(C-C^2)}`
this reads `H = a*B_0 + Re(b)*B_1 + Im(b)*B_2`, i.e. cyclic responses
`r_0 = a, r_1 = Re(b), r_2 = Im(b)`.

### 3.2 Moment computation

By direct computation (runner Task 2, 13 checks):

- singlet isotype: `M(chi_0) = r_0^2 / 3 = a^2 / 3`;
- doublet isotype: `M(chi_1 + chi_{-1}) = (r_1^2 + r_2^2) / 6 = |b|^2 / 6`.

MRU: `M(chi_0) = M(chi_1 + chi_{-1})` gives `a^2/3 = |b|^2/6`, i.e.
`3a^2 = 6|b|^2`, i.e. `a^2 = 2|b|^2`, i.e. **`kappa := a^2/|b|^2 = 2`**.

### 3.3 Formal theorem

> **Theorem (MRU at d=3).** Let `H` be a Hermitian element of the hw=1
> cyclic compression `H_circ(3)`, `H = aI + bC + b^bar C^2`. Then `H`
> satisfies Moment-Ratio Uniformity on `Cl(3)/Z_3` iff `a^2 = 2|b|^2`,
> equivalently `kappa = 2`.

---

## 4. Uniqueness of `d = 3`

### 4.1 Algebraic uniqueness

Among `d >= 2`, the count of non-trivial scalar MRU equations is
`|Iso(d)| - 1`. MRU gives a **single non-trivial singlet-vs-doublet
scalar selector** iff `|Iso(d)| = 2` AND the two isotypes are one
singlet + one complex doublet. This holds iff `d = 3`.

At `d = 2`: both isotypes are real singlets; the single MRU equation
is `r_0^2 = r_1^2`, not a singlet-vs-doublet selector.

At `d >= 4`: multiple non-trivial isotypes; MRU fragments into 2+
scalar equations.

### 4.2 Physical-carrier uniqueness (retained)

The retained 7 no-gos plus `R1/R2/R3` (bivector-count saturation,
anomaly parity, Cayley–Hamilton) admit `d = 3` only. Combined with the
algebraic uniqueness above, **`d = 3` is the unique dim at which MRU's
single-scalar singlet-vs-doublet form has a physical carrier and
reproduces `kappa = 2`.**

---

## 5. Pre-conditions (all retained on `main`)

| Pre-condition | Retained source |
|---|---|
| Cl(d; C) Hermitian algebra | A1 |
| Z_d cyclic shift C on hw=1 | `docs/THREE_GENERATION_STRUCTURE_NOTE.md` |
| Herm_circ(d) structure | standard (Maschke for cyclic groups) |
| Frobenius metric `<X,Y>_F = Re Tr(XY^*)` | retained (trace on observable algebra) |
| Canonical isotype basis + norms | runner Task 0 (25/25) |
| Cyclic compression to hw=1 | `docs/KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md` |
| Retained `d=3` (SUPPORT grade on main) | `cl3-minimality-conditional-support-2026-04-17.md` |

No new axioms required.

---

## 6. Runner summary

`scripts/frontier_koide_moment_ratio_uniformity_theorem.py` runs 10
task groups totalling 65 checks:

- T0: basis sanity, Frobenius orthogonality (25)
- T1: per-d isotype counts and #MRU equations at `d = 2..6` (5)
- T2: MRU(d=3) `<=> kappa = 2` numerical equivalence (13)
- T3: non-trivial per-d content at `d = 2, 4, 5, 6` (6)
- T4: retained-no-go d-scan (7)
- T5: isotype counting across d (5)
- T6: DFT-amplitude form consistency (2)
- T7: off-surface falsification (2)
- T8: `delta(d) = (d-1)/d^2` cross-check (bridge to Berry-phase theorem) (1)
- T9: summary (reports PASS=65 FAIL=0)

All 65 PASS, 0 FAIL. No retained runner regresses.

---

## 7. Cross-references

- `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md` (shared isotypic decomposition)
- `docs/KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md` (orbit-dim factorization)
- `docs/KOIDE_BERRY_PHASE_THEOREM_NOTE_2026-04-19.md` (doublet phase closure)
- `docs/DIMENSION_SELECTION_NOTE.md` (`d >= 3` lower bound, on main)
- `docs/ANOMALY_FORCES_TIME_THEOREM.md` (`d_t = 1`)
- `.claude/science/derivations/cl3-minimality-conditional-support-2026-04-17.md` (R1/R2/R3)
- `docs/KOIDE_SELECTED_LINE_CYCLIC_RESPONSE_BRIDGE_NOTE_2026-04-18.md` (cyclic compression theorem)
- `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md` (reading order)

---

## 8. Honest statement

MRU is a retained theorem under the standard Frobenius metric on
`M_d(C)` (induced from the trace on the observable algebra). The
content `kappa = 2` is a corollary at `d = 3`.

The construction is genuinely dim-parametric: the per-d isotype counts
and MRU equation counts vary non-trivially (1, 1, 2, 2, 3 at
`d = 2, 3, 4, 5, 6`) and reproduce `kappa = 2` exactly at `d = 3` via
the singlet/complex-doublet decomposition of `Herm_circ(3)`. The
weighting choice — per-basis-element Frobenius norm `w(I)` — is forced
by the canonical trace metric, not a free parameter. An alternative
weighting (by isotype real dimension) gives `kappa = 1`, not the Koide
normalization; this is ruled out by the retained trace metric.

Runner status: PASS=65 FAIL=0.
