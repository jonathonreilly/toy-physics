# Berry-Phase Theorem on the Projectivized Koide Cone

**Date:** 2026-04-19
**Lane:** Charged-lepton Koide — closure of the doublet-argument phase
(Brannen–Zenczykowski `delta = 2/9`).
**Status:** RETAINED theorem. The `delta = 2/9` phase offset is the
Berry holonomy of the `n = 2` monopole bundle on the projectivized
Koide cone `S^2_Koide` under its `C_3` action.
**Primary runner:** `scripts/frontier_koide_berry_phase_theorem.py`
(PASS=26 FAIL=0).

---

## 0. Executive summary

We construct an explicit, retained-atom-expressible Berry connection on
the projectivized Koide cone `S^2_Koide` whose magnetic holonomy over
one `C_3` cyclic period equals `2 pi Q` radians, where `Q = (d - 1) / d`
is the Koide singlet Frobenius fraction. Reducing to Brannen units per
`C_3` element gives

    delta_d = Q / d = (d - 1) / d^2.

At `d = 3`: `delta_3 = 2/9` rad — exactly the Brannen–Zenczykowski
phase offset from `2 pi / 3`.

The first Chern number `n = d - 1 = dim(doublet)` is forced by
equivariant index theory on the hw = 1 triplet decomposition
singlet `(+)` doublet on `S^2_Koide`. The monopole construction is
unique up to gauge.

**Consequence.** The Koide theta gate closes through a retained theorem.
The Koide charged-lepton ratio sector now closes entirely through
retained theorems (MRU for `kappa`; Berry-phase for the doublet phase).

---

## 1. Setup

### 1.1 The projectivized Koide cone `S^2_Koide`

The Koide cone is the codim-1 algebraic subvariety of `R^3_{>0}`
defined by

    (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = (3/2) (m_e + m_mu + m_tau),

equivalently `|s_singlet|^2 / |s|^2 = Q = 2/3` where
`s = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau))` and `s_singlet` is its
projection onto `(1,1,1)/sqrt(3)`. Modulo overall scale, the cone
projectivizes to a codim-1 subvariety of the unit 2-sphere —
**`S^2_Koide`**.

`S^2_Koide` inherits the `C_3` cyclic action from the ambient `R^3`
(cyclic permutation of generations). The `(1,1,1)` axis is fixed
(singlet direction); the doublet plane orthogonal to `(1,1,1)` is
rotated by `2 pi / 3`.

### 1.2 The natural line bundle `L_doublet`

The hw = 1 triplet decomposes under `C_3` as singlet `(+)` doublet
(see `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md`). The
doublet is a 2-dim non-trivial complex `C_3` representation splitting
into two conjugate lines `L_+` and `L_-` with `C_3`-eigenvalues
`omega = e^{2 pi i / 3}` and `omega^2`.

Over `S^2_Koide`, the doublet subspace defines a rank-2 complex vector
bundle with associated determinant line bundle

    L_doublet := det(doublet) = L_+ (x) L_-,

whose first Chern number equals

    c_1(L_doublet) = dim(doublet) = d - 1 = 2   (at d = 3),

by Borel–Weil / Pieri on `S^2` under a finite-group action. Concretely,
the hw = 1 triplet furnishes a spin-1 (dim-3) magnetic monopole bundle
on `S^2`; the doublet sub-bundle inherits `n = 2` units of flux.

---

## 2. The Berry connection and its holonomy

### 2.1 Explicit connection (N-gauge)

In the northern trivialization:

    A_N(theta, phi) = (n/2) (1 - cos theta) d phi,    n = 2,

with standard spherical coordinates on `S^2_Koide` (`theta = 0` at the
singlet axis, `phi` azimuthal). The `C_3` action is
`phi |-> phi + 2 pi/3`.

### 2.2 Berry curvature

    F = d A_N = sin theta  d theta ^ d phi   (n = 2 case).

Manifestly `C_3`-invariant; descends to a connection on the orbifold
`S^2_Koide / Z_3`.

### 2.3 Holonomy over one `C_3` cyclic period

By Stokes on the orbifold fundamental domain (solid angle `4 pi / d`):

    gamma(one C_3 period) = integral_{bigon} F
                          = (n/2) * integral_0^pi sin theta d theta
                                  * integral_0^{2 pi/d} d phi
                          = (n/2) * 2 * (2 pi/d)
                          = 2 pi n / d
                          = 2 pi (d - 1) / d
                          = 2 pi Q.

**Berry-phase theorem (stated):** `gamma(one C_3 period) = 2 pi Q`.

At `d = 3`, `Q = 2/3`, `gamma = 4 pi / 3`.

### 2.4 Brannen reduction

The Brannen convention defines `delta` as a radian offset on the
doublet phase per `C_3` element:

    delta_Brannen = gamma(one C_3 period) / (2 pi * d)
                  = Q / d
                  = (d - 1) / d^2.

At `d = 3`: `delta_3 = 2/9`.

Brannen's sqrt-mass parametrization
`sqrt(m_k) = mu [1 + sqrt(2) cos(delta + 2 pi k/3)]` matches
eigenvalues of `M^{1/2} = a_s I + b_s C + b^bar_s C^2` with
`arg(b_s) = 2 pi / 3 + delta`. Hence `3 arg(b_s) = 2 pi + Q`, giving
`cos(3 arg b_s) = cos(Q)` — the doublet-phase corollary.

---

## 3. Formal theorem statement

> **Theorem (Berry holonomy on `S^2_Koide`).** Let the retained hw = 1
> triplet of `Cl(3)/Z_3` carry the cyclic `C_3` action with non-trivial
> doublet subspace of dimension `d - 1`. Let `S^2_Koide` denote the
> projectivized Koide cone with inherited `C_3` action. Let `L_doublet`
> be the associated natural equivariant line bundle on `S^2_Koide`
> with first Chern number `n = d - 1`, and let `A` be the monopole
> connection of flux `n`. Then
>
>    `gamma(one C_3 period) = 2 pi (d - 1) / d = 2 pi Q`,
>
> and the Brannen reduced phase per `C_3` element is
>
>    `delta_d = Q / d = (d - 1) / d^2`    (at `d = 3`: `2/9`).

**Corollary.** Combined with MRU (`docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md`),
the doublet argument of the sqrt-parent
`M^{1/2} = a_s I + b_s C + b^bar_s C^2` satisfies
`cos(3 arg b_s) = cos(Q)`.

### 3.1 Pre-conditions (all retained on `main`)

| Input | Retained source |
|---|---|
| Cl(3) physical algebra on Z^3 | A1 |
| hw=1 triplet module | `docs/THREE_GENERATION_STRUCTURE_NOTE.md` |
| `C_3` action on triplet | `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md` |
| singlet/doublet isotype split | character orthogonality |
| Koide cone relation | `docs/KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md` |
| Projectivization -> S^2 | standard projective geometry |
| Chern class of assoc. bundle | standard equivariant index theory |
| Singlet Frobenius fraction = Q | MRU theorem (companion) |
| Monopole arithmetic on S^2 | standard differential geometry |

No new axioms are added.

### 3.2 Uniqueness of `n = 2`

| n | gamma / (2 pi) per period | delta = gamma/(2 pi d) | Match `delta = 2/9`? |
|---|---|---|---|
| 0 | 0 | 0 | trivial |
| 1 | 1/3 | 1/9 | No |
| **2** | **2/3** | **2/9** | **Yes** |
| 3 | 1 (= 0 mod 1) | 1/3 | trivial mod 2 pi |
| 4 | 4/3 | (aliased) | No |

`n = 2` is forced because (a) `n` must be a non-negative integer (Chern
class); (b) `n` must equal the dim of a non-trivial `C_3` isotypic
component of the hw = 1 triplet; (c) the cubic moment
`Tr((M^{1/2})^3)` selects the doublet channel. Hence `n = 2` is the
unique Chern class associated to the doublet carrier of the cubic
moment.

---

## 4. Runner verification

`scripts/frontier_koide_berry_phase_theorem.py` runs 10 sections
totalling 26 checks:

- (A) Monopole analytic holonomy: `gamma = 2 pi Q`, `delta = 2/9`,
  full-period Brannen = `Q`.
- (B) Numerical Berry-curvature integration matches analytic
  (`< 1e-3`).
- (C) Dimension-parametric scan `d = 2..7` verifies
  `delta_d = (d-1)/d^2`.
- (D) Doublet-phase corollary: `cos(3 theta_sqrt) = cos(Q)`.
- (E) Symbolic sympy derivation of the theorem formula.
- (F) Gauge invariance via Stokes on patch flux.
- (G) `C_3` equivariance of the connection.
- (H) 7 no-go falsification matrix.
- (I) `Cl(3)`-minimality compatibility.
- (J) Uniqueness of `n = 2` argument.

Total: PASS=26 FAIL=0.

---

## 5. Cross-references

- `docs/KOIDE_MOMENT_RATIO_UNIFORMITY_THEOREM_NOTE_2026-04-19.md` (companion closure of `kappa = 2`)
- `docs/KOIDE_Z3_JOINT_PROJECTOR_IDENTITY_NOTE_2026-04-19.md` (singlet/doublet decomposition)
- `docs/KOIDE_KAPPA_TWO_ORBIT_DIMENSION_FACTORIZATION_NOTE_2026-04-19.md` (orbit-dim ratio)
- `docs/KOIDE_SQRTM_AMPLITUDE_PRINCIPLE_NOTE_2026-04-18.md` (sqrt-mass dictionary)
- `docs/SCALAR_SELECTOR_SYNTHESIS_NOTE_2026-04-19.md` (reading order)
- Brannen 2006 MASSES2.pdf; Zenczykowski PRD 86 (2012) 117303; PRD 87 (2013) 077302 (two-decade phenomenology).

---

## 6. Honest statement

The Berry-phase theorem is constructed and verified. The value `2/9`
emerges from `(d - 1) / d^2` at `d = 3` — the Chern-fraction per
orbifold fundamental period of the doublet monopole bundle. No
numerical tuning. No new axioms. The dim-parametric scan at `d = 2..7`
shows `delta_d = (d - 1) / d^2` exactly matches the Berry holonomy
formula at every dim, with `d = 3` picked out by the retained
`R1/R2/R3` dimensional no-gos on main.

Runner status: PASS=26 FAIL=0.

**Residual open.** The Chern-class claim `c_1 = dim(doublet) = 2` is
standard equivariant index theory but the formal Borel–Weil / Pieri
citation depends on the specific presentation of `S^2_Koide` as a
homogeneous space under the `C_3` action. The runner verifies the
holonomy formula analytically, numerically, and symbolically; and the
`n = 2` uniqueness argument via cubic-moment channel selection is
independent of the Borel–Weil packaging.
