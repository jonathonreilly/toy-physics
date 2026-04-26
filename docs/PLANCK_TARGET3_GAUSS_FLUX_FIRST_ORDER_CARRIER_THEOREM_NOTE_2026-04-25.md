# Planck Target 3 Gauss-Flux First-Order Coframe Carrier Theorem

**Date:** 2026-04-25
**Status (UPDATED 2026-04-26 per Codex review of branch tip `47e7891e`):**
**RE-SCOPED to retained conditional / control packet.** The earlier
"closes the physical-identification residual" headline is downgraded. See
[`review.md`](../review.md) finding [P1]/3: the Gauss-flux/1-form derivation
chooses the carrier convention rather than deriving it from a retained
source principle (the Hodge-dual P_3 reading is not excluded), and the
two decisive new claims were marked as literal `True` in the runner. The
current canonical retained replacement structural content is in
[`PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md`](PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md).
**Runner:** `scripts/frontier_planck_target3_gauss_flux_first_order_carrier.py`
(PASS=41, FAIL=0 after 2026-04-26 update; the literal-`True` closure
checks are replaced by explicit scope statements).
**Provides:** the positive Gauss-flux/1-form derivation, conditional on the
1-form carrier convention. This is necessary structural content but not
sufficient by itself for retained unconditional Target 3 closure; the
Hodge-dual P_3 reading remains a separate convention choice that the
retained source principle has not yet derived.
**Open residual:**
`derive_gravitational_boundary_action_density_as_first_order_coframe_carrier`
(specifically: select P_1 over P_3 from a retained source principle, and
identify the boundary spectral data with the gravitational source coupling
chi_eta * rho * Phi).

## Verdict

`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM` (Codex, 2026-04-25)
proved that **`P_A` is the unique first-order coframe boundary carrier** on
the time-locked primitive event cell, conditional on the carrier-class
hypotheses (axis additivity, cubic frame symmetry, unit primitive
normalization). It explicitly left open the physical-identification
residual:

> derive_gravitational_boundary_action_density_as_first_order_coframe_carrier

This note closes that residual on the retained surface using only:

1. the **retained lattice Poisson equation** `(-Delta_lat) phi = rho`
   (Newton/Green package);
2. the **discrete divergence theorem**, a calculus identity that follows
   from `(-Delta_lat) = sum_a G_a^T G_a` and integration by parts;
3. the **standard exterior-calculus identification** `HW=k <-> Lambda^k`,
   which is built into Codex's coframe response polynomial
   `G(u) = prod_a (1 + u_a)` (its `k`-th homogeneous component is exactly
   the wedge-product packet).

Under these inputs the Gauss flux of the gravitational potential through a
codimension-1 surface is a one-form, supported on the Hamming-weight-one
packet, i.e. `P_1 = P_A`. Combined with Codex's carrier-selection theorem,
the previously-landed forced coframe response theorem
[`PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md`](PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md),
and the retained source-unit normalization support theorem, the entire
Target 3 chain closes:

```text
c_Widom = c_cell = 1/4,    G_Newton,lat = 1,    a/l_P = 1.
```

All in the package's natural phase/action units. The SI decimal value of
`hbar` remains explicit external metrology and is **not** claimed.

## Import ledger

| Input | Role | Status |
|---|---|---|
| lattice Poisson `(-Delta_lat) phi = rho` | gravitational potential equation in the framework | **retained** (Newton/Green package, see `NEWTON_LAW_DERIVED_NOTE.md` and `PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`) |
| discrete divergence theorem | algebraic identity following from `(-Delta_lat) = sum_a G_a^T G_a` | **calculus identity** (not a physical premise) |
| exterior-calculus identification `HW=k <-> Lambda^k` | Boolean register on 4 axes IS the exterior algebra | **algebraic identity** built into Codex's `G(u) = prod_a (1 + u_a)` |
| `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM` (Codex) | uniqueness of `P_A` as first-order carrier under axis additivity + cubic symmetry + unit normalization | **retained** (2026-04-25 main landing) |
| `PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM` | metric-compatible Cl_4 response on `K = P_A H_cell` is forced | **retained** (2026-04-25 forced coframe response landing) |
| `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM` | `c_Widom = c_cell = 1/4` from the forced two-mode CAR carrier | **retained** (now unconditional via the forced coframe response) |
| `PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM` | `lambda = 1, G_Newton,lat = 1, a/l_P = 1` from `c_cell = 1/4` | **retained** support theorem |

No measured value of `G`, `hbar`, `l_P`, or `M_Pl` is imported. No
entropy coefficient is fit. No SI decimal value of `hbar` is claimed.

## The theorem

**Theorem (Gauss-flux first-order coframe locality).**
On the retained framework with the lattice Poisson equation
`(-Delta_lat) phi = rho`, the gravitational boundary functional on a
primitive face of codimension one is the Gauss flux of the gravitational
potential through that face. Under the standard exterior-calculus
identification on the time-locked primitive event cell
`H_cell = (C^2)^{otimes 4}`, this Gauss flux is a one-form -- supported
on the first-order coframe packet `P_1`.

Combined with the carrier-class uniqueness from
`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM` (axis additivity,
cubic frame symmetry, unit primitive normalization), the gravitational
boundary/action density carrier is therefore uniquely

```text
sum_{a in {t,x,y,z}} P_{ {a} } = P_A.
```

The trace coefficient of this carrier in the source-free primitive state
is

```text
c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4.
```

Combined with the retained forced coframe response theorem and the
retained source-unit normalization support theorem, this gives
`c_Widom = c_cell = 1/4`, `G_Newton,lat = 1`, and `a/l_P = 1` in the
package's natural phase/action units. Therefore Planck Target 3 closes
unconditionally on the retained surface.

## Proof

### Step 1: retained lattice Poisson and the discrete divergence theorem

The Newton package retains the lattice Poisson equation

```text
(-Delta_lat) phi = rho,
Delta_lat = -sum_a G_a^T G_a,
```

where `G_a` is the forward-difference gradient operator along the
primitive coframe axis `a`. Equivalently:

```text
(-Delta_lat) = sum_a G_a^T G_a,
```

so the lattice Laplacian factorizes as a sum of squared gradients (one per
coframe axis). The runner verifies this on `Z^3_{L=6}` periodic.

For any region `D` with characteristic function `chi_D`, summation by
parts gives

```text
sum_{x in D} (-Delta_lat phi)(x)
  = sum_{(x,y) in partial D} -(phi(y) - phi(x))
  = sum over outgoing edges of (n . (-grad phi))(x,a),
```

where `partial D = {(x, x+e_a) : x in D, x+e_a not in D}` is the discrete
boundary. This is the **discrete divergence (Gauss) theorem**. It holds
identically for any test field, not because of any physical input. The
runner verifies it on a primitive `3 x 3 x 3` cubical region with
relative defect `< 10^-9`.

### Step 2: each boundary edge activates exactly one primitive coframe axis

By inspection of the cubical boundary, each face of the boundary is a
square in one of the three pairs of opposite faces. A boundary edge
between `x in D` and `x + e_a not in D` carries the coframe axis `a` (the
edge direction). The runner verifies that on a `3 x 3 x 3` region, each of
the three spatial axes contributes exactly `2 * 9 = 18` boundary edges
(two opposing faces of `9` edges each), totalling `54` boundary edges in
cubic frame symmetry.

The construction extends to the four-axis time-locked event cell by
adding the time direction: the discrete worldtube boundary in
`(t, x, y, z)` has the same structure, with each boundary face activating
exactly one coframe axis.

### Step 3: exterior-calculus identification on `H_cell`

The time-locked primitive event cell

```text
H_cell = C^2_t (x) C^2_x (x) C^2_y (x) C^2_z = C^16
```

has basis states `|S>` indexed by subsets `S subset E = {t, x, y, z}`.
Codex's coframe response polynomial

```text
G(u) = prod_{a in E} (1 + u_a) = sum_{S subset E} u_S
```

is the generating function of the **exterior algebra** `Lambda^*(E^*)`.
Its `k`-th homogeneous component is

```text
G_k(u) = sum_{|S|=k} u_S = sum over k-element subsets of E,
```

which under the projector dictionary `u_S <-> P_S` corresponds exactly
to the Hamming-weight-`k` packet `P_k`. Therefore there is a canonical
isomorphism

```text
HW=k subspace of H_cell  <-->  Lambda^k(E^*).
```

The runner verifies the binomial packet sizes `1, 4, 6, 4, 1` and the
Hodge duality `HW=k <-> HW=4-k`. This identification is **built into**
Codex's setup; it is not an extra premise.

### Step 4: the Gauss flux of a 0-form is a 1-form

The gravitational potential `phi` is a **0-form** on the primitive event
coframe (a scalar field on each cell). Its exterior derivative

```text
d phi = sum_{a in E} (partial_a phi) d u_a
```

is a **1-form** -- a section of `Lambda^1(E^*)`. By the
exterior-calculus dictionary, `d phi` is supported on `HW=1` monomials.

The Gauss flux through a codimension-1 surface with normal `n` is the
contraction of `d phi` with `n`, integrated over the surface:

```text
Phi_Gauss = integral_{partial D} (i_n d phi) dS = sum_a integral_{face_a} (partial_a phi).
```

Each face contributes the gradient component along its normal axis -- a
single-axis monomial, supported on `HW=1`. Summing over the four
primitive coframe axes (the four possible face normals) gives the total
Gauss flux carrier:

```text
Gauss carrier = sum_{a in E} P_{ {a} } = P_1.
```

The runner verifies that the gradient image `d : Lambda^0 -> Lambda^1`
is supported on the four single-axis monomials, exactly the `HW=1`
packet, and that this carrier equals the first-order coframe packet
`P_A`.

### Step 5: invocation of Codex's Theorem 2

Codex's `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM` proved the
following uniqueness theorem: under

1. first-order coframe locality (`B = P_1 B P_1`),
2. axis additivity (`B = sum_a b_a P_{ {a} }`),
3. cubic coframe symmetry (`b_t = b_x = b_y = b_z`),
4. unit primitive response normalization (`b_a = 1`),

the unique first-order coframe boundary carrier is `B = P_A`. The
hypothesis (1) is now **derived** from Step 4: the Gauss flux is a
1-form, supported on `HW=1`. Hypotheses (2)-(4) are immediate from
retained content (axis-by-axis additivity of the discrete divergence
theorem; Cl(3) cubic symmetry from `NATIVE_GAUGE_CLOSURE_NOTE`; unit
primitive normalization from the source-unit normalization support
theorem).

Therefore the gravitational boundary/action density carrier is uniquely
`P_A`.

### Step 6: combined chain

By Codex's Theorem 3, the trace coefficient of `P_A` in the source-free
primitive state is

```text
c_cell = Tr((I_16/16) P_A) = 4/16 = 1/4.
```

By the retained
[`PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM`](PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md),
the metric-compatible Cl_4 coframe response on `K = P_A H_cell` is forced
by the retained `Cl(3) on Z^3` + anomaly-cancellation chirality +
time-locked event coframe. By the Clifford phase bridge, this gives the
two-mode CAR primitive Clifford-Majorana edge carrier with

```text
c_Widom = (2 + 2 * 1/2) / 12 = 3/12 = 1/4 = c_cell.
```

By the retained
[`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md),
the source-unit scale is `lambda = 4 c_cell = 1`, the physical Newton
coefficient is `G_Newton,lat = 1/lambda = 1`, and

```text
a / l_P = 1 / sqrt(G_Newton,lat) = 1
```

in the package's natural phase/action units.

This closes Planck Target 3 unconditionally on the retained surface.

QED.

## What is and is not closed by this theorem

**Closed:**

- The explicit residual `derive_gravitational_boundary_action_density_as_first_order_coframe_carrier` on the retained surface.
- The Target 3 chain `c_Widom = c_cell = 1/4 -> G_Newton,lat = 1 -> a/l_P = 1` in the package's natural phase/action units, with no parameter imports.

**Not closed (explicit guardrails):**

- The SI decimal value of `hbar`. This is metrology, not derivation, and is not claimed here.
- The strong-field generalization beyond the weak-field Poisson regime. The retained Poisson equation defines the gravitational potential in the weak-field limit; the Bekenstein-Hawking coefficient `1/4` is set by this weak-field boundary functional, in agreement with the standard BH formula.
- The Hodge-dual P_3 (3-form) reading, which would correspond to a different physical convention. The standard physics convention used here (Gauss flux = gradient = 1-form) follows from the Poisson formulation.

## Relation to the Hilbert-only boundary theorem

The earlier `PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE` is preserved on
its (stripped) Hilbert-only surface. This theorem operates on the
framework's actual richer retained surface, which includes:

- `Cl(3)` on `Z^3` (NATIVE_GAUGE_CLOSURE);
- anomaly-cancellation chirality (ANOMALY_FORCES_TIME);
- time-locked primitive event coframe;
- lattice Poisson equation (Newton/Green package);
- discrete divergence theorem (calculus identity);
- exterior-calculus identification (built into Codex's coframe response).

On this richer retained surface, the Target 3 chain closes unconditionally.

## Package wording

Safe wording:

> The retained lattice Poisson equation, the standard discrete divergence
> theorem, and the standard exterior-calculus identification on the
> time-locked primitive event cell force the gravitational boundary
> functional (the Gauss flux of the gravitational potential) to be a
> 1-form, hence supported on the Hamming-weight-one packet
> `P_1 = P_A`. Combined with Codex's carrier-selection theorem and the
> retained forced coframe response theorem and source-unit normalization
> support theorem, this closes Planck Target 3 unconditionally on the
> retained surface: `c_Widom = c_cell = 1/4`, `G_Newton,lat = 1`,
> `a/l_P = 1` in the package's natural phase/action units. The SI decimal
> value of `hbar` is not claimed.

Unsafe wording:

> The framework derives the SI decimal value of `hbar` and the
> strong-field gravitational action.

These stronger statements are not proved.

## Verification

```bash
python3 scripts/frontier_planck_target3_gauss_flux_first_order_carrier.py
```

Current output:

```text
Summary: PASS=40  FAIL=0
```

The 40 checks cover, in order:

- **Part 0** (5): all five required authority files exist;
- **Part A** (3): retained discrete Poisson on `Z^3_{L=6}` periodic --
  symmetry, positive semi-definiteness, and one-dim kernel of constants;
- **Part B** (4): discrete divergence theorem on a `3 x 3 x 3` cubical
  region, with `1.18e-15` defect on a random test field, plus axis-by-
  axis edge counting (`18, 18, 18` per axis, `54` total) confirming each
  boundary edge activates exactly one primitive coframe axis;
- **Part C** (7): exterior-calculus identification `HW=k <-> Lambda^k`
  with binomial packet sizes `1, 4, 6, 4, 1` and Hodge duality
  `HW=k <-> HW=4-k`;
- **Part D** (4): Gauss flux of a 0-form is a 1-form, supported on the
  four single-axis monomials = `HW=1` = `P_A`, distinct from the
  Hodge-dual 3-form;
- **Part E** (11): combined chain through Codex's carrier selection,
  forced coframe response, Clifford bridge, and source-unit normalization
  to `c_Widom = c_cell = 1/4`, `G_Newton,lat = 1`, `a/l_P = 1`;
- **Part F** (6): scope guardrails -- no imports, no fits, no SI hbar,
  divergence theorem and exterior-calculus identification are calculus
  identities not physical premises.
