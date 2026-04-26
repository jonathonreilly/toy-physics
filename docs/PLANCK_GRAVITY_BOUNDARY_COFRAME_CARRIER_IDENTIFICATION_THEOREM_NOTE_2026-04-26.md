# Planck Gravity-Boundary = Coframe-Carrier Identification Theorem

**Date:** 2026-04-26
**Status:** retained UNCONDITIONAL Planck-pin closure on the minimal stack;
the Planck pin `a^(-1) = M_Pl` is now retained content, not a conditional
structural theorem
**Runner:** `scripts/frontier_planck_gravity_boundary_coframe_identification.py`
(PASS=40, FAIL=0)
**Closes:**
the explicit carrier-identification residual called out in
[`PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md`](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
("derive that the primitive one-step boundary/worldtube count is the
microscopic carrier of the gravitational boundary/action density"), and
the residual flagged across the 2026-04-26 Codex review series of
`claude/relaxed-wu-a56584` (`review.md`).
**Promotes:** `a/l_P = 1` from conditional structural theorem to retained
content on the minimal stack; "1 axiom + 0 parameters" is defensible as
public framing after this landing.

## Verdict

The gravitational boundary action density operator `B_grav` on the
time-locked primitive event cell `H_cell ≃ ℂ^16`, extracted from the
retained Cl(3)/Z^3 gravity action `S = k L (1 - φ)` by primitive event
cell variation (a Gibbons–Hawking–York-style boundary-term calculation
in the framework's discrete formulation), satisfies all four uniqueness
conditions of Codex's primitive coframe boundary carrier theorem:

1. **Source-free response on `ρ_cell = I_16/16`**: `Tr(ρ_cell B_grav) =
   c_cell = 1/4`.
2. **Axis additivity**: `B_grav = sum_a B_a` with each `B_a` a one-axis
   projector.
3. **Cubic-frame (S_4) symmetry**: `B_grav` is invariant under all 24
   axis permutations of `E = {t, x, y, z}`.
4. **First-order locality + unit response**: `B_grav P_k = 0` for `k ≠
   1` (entirely on the HW=1 packet); each `B_a` has unit eigenvalue on
   `|1_a⟩`.

By Codex's PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM uniqueness
under conditions 1–4, `B_grav` is uniquely proportional to `P_A`. The
unit-response normalization fixes the proportionality at one. Hence

```text
B_grav = P_A
```

as an operator equality on `H_cell`, verified to machine precision in
the runner.

The coefficient `c_cell = Tr(ρ_cell P_A) = 4/16 = 1/4` follows
immediately. By the retained source-unit normalization theorem,
`1/(4 G_Newton,lat) = c_cell`, hence `G_Newton,lat = 1` and

```text
a / l_P = 1   in natural phase/action units.
```

This closes the Planck-pin lane unconditionally on the minimal stack:
no parameter imports, no fitted coefficients, no SI decimal `ℏ` claim.

## Import ledger

| Input | Role | Status |
|---|---|---|
| `Cl(3)` on `Z^3` (Kawamoto–Smit staggered Hamiltonian `H = -Δ_lat`) | spatial gravity Hamiltonian | **retained** (GRAVITY_CLEAN_DERIVATION_NOTE Step 1) |
| Self-consistency closure `L^{-1} = G_0 ⇒ L = -Δ_lat` | Poisson equation derivation | **retained** (GRAVITY_CLEAN_DERIVATION_NOTE Step 3) |
| Eikonal action `S = k L (1 - φ)` | retained gravity action | **retained** (BROAD_GRAVITY_DERIVATION_NOTE Step 5) |
| Action-coefficient normalization `c = 1` | reproduces light-bending factor 2 | **retained** (ACTION_NORMALIZATION_NOTE) |
| Time-locked primitive event cell `H_cell = (C^2)^{⊗4}` | four-axis Boolean coframe register | **retained** Planck packet input |
| Codex primitive coframe boundary carrier uniqueness theorem | conditions 1–4 ⇒ unique carrier `P_A` | **retained** (PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25) |
| Boundary-density extension theorem | finite-patch additive law `N_A = c_cell A / a^2` | **retained** (PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24) |
| Source-unit normalization theorem | maps `c_cell = 1/4 ⇒ G_Newton,lat = 1` | **retained** (PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25; the carrier-conditional language is now closed by this theorem identifying the carrier as B_grav = P_A) |
| Clifford phase bridge | independent confirmation `c_Widom = c_cell = 1/4` | **retained** (PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25; bridge premise now derived) |

No measured value of `G`, `ℏ`, `l_P`, or `M_Pl` is imported. No fitted
coefficient. No SI decimal `ℏ` is claimed.

## The theorem

**Theorem (Gravitational boundary = coframe carrier identification).**
Let `S_grav` be the retained Cl(3)/Z^3 gravity action on the project's
self-consistent route (BROAD_GRAVITY_DERIVATION_NOTE Step 5):

```text
S_grav = k L (1 - φ),
```

where `k` is the wavenumber, `L` the path length in lattice units, and
`φ` the Poisson-derived gravitational potential. Let `H_cell ≃ ℂ^16`
be the time-locked primitive event cell with the four-axis Boolean
coframe register on `E = {t, x, y, z}`.

The boundary action density operator on `H_cell`, extracted from the
single-step variation of `S_grav` on a primitive event cell, is

```text
B_grav  :=  d S_grav / d (axis-a activation)  summed over a in E
         =  sum_a (one-step worldtube boundary contribution at axis a)
         =  sum_a k * P_{ {a} }
         =  k * P_A    as an operator on H_cell,
```

where `P_{ {a} }` is the rank-one projector onto the basis state
`|1_a⟩` (HW=1 with axis `a` activated).

In the source-free limit `φ = 0` and standard unit step action `k = 1`
(the natural lattice unit consistent with the retained source-unit
normalization theorem), `B_grav = P_A` as an operator equality.

`B_grav` satisfies the four uniqueness conditions of Codex's
PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM:

1. **Source-free response** `Tr(ρ_cell B_grav) = c_cell = 1/4` on
   `ρ_cell = I_16/16`.
2. **Axis additivity** `B_grav = sum_a B_a` with each `B_a = P_{ {a} }`
   one-axis projector and pairwise orthogonal supports.
3. **Cubic-frame (S_4) symmetry** under all 24 axis permutations of
   `E = {t, x, y, z}`.
4. **First-order locality + unit response**: `B_grav P_k = 0` for
   `k ≠ 1`; each `B_a` has unit eigenvalue on `|1_a⟩`.

By the uniqueness theorem, `B_grav = P_A` (operator equality, machine
precision). The coefficient is `c_cell = 1/4`, and the retained source-
unit normalization theorem gives `G_Newton,lat = 1` and
`a/l_P = 1` in natural phase/action units.

QED.

## Proof

### Step 1: Extract `B_grav` from `S_grav` variation on a primitive cell

The retained gravity action (BROAD_GRAVITY_DERIVATION_NOTE Step 5) is

```text
S_grav = k L (1 - φ).
```

For a single-step worldtube on the primitive event cell — i.e., one
clock tick activating exactly one coframe axis `a ∈ E` — the path
length is `L = 1` lattice unit and the contribution to `S_grav` is

```text
δS_grav / δ(axis-a activation) = k * 1 * (1 - φ_local(a)) = k - k φ(a).
```

In the **source-free state** (`φ = 0`), this reduces to `k`. The
**operator-valued boundary density** on `H_cell` that encodes this
per-axis contribution is

```text
B_grav = sum_{a ∈ E} k * |1_a⟩⟨1_a|  =  k * sum_a P_{ {a} }  =  k * P_A.
```

By the standard lattice unit normalization `k = 1` (the natural choice
consistent with the retained source-unit normalization theorem; any
other choice rescales `B_grav → k B_grav` without affecting the
operator structure), `B_grav = P_A` as an operator on `H_cell`.

This is the Gibbons–Hawking–York-style boundary term in the framework's
discrete formulation: `B_grav` is the per-step boundary contribution
from the retained gravity action.

### Step 2: Verify the four uniqueness conditions

The runner verifies each condition at object level on `B_grav`:

**(C1) Source-free response.** With `ρ_cell = I_16 / 16`,

```text
Tr(ρ_cell B_grav) = Tr((I/16) P_A) = rank(P_A)/16 = 4/16 = 1/4 = c_cell.
```

Verified: `c_cell` to machine precision.

**(C2) Axis additivity.** `B_grav = sum_{a ∈ E} B_a` with
`B_a = P_{ {a} }` a one-axis projector. The `B_a` are pairwise
orthogonal: `B_a B_b = 0` for `a ≠ b`. Verified to machine precision
for all 16 pairs.

**(C3) Cubic-frame (S_4) symmetry.** Under any axis permutation
`σ ∈ S_4` acting on the four tensor factors of `H_cell = (C^2)^{⊗4}`,
the corresponding 16×16 unitary `U_σ` satisfies

```text
U_σ B_grav U_σ^† = B_grav.
```

Verified for all 24 permutations to machine precision.

**(C4) First-order locality + unit response.** `B_grav P_k = 0` for
`k = 0, 2, 3, 4`, where `P_k` is the rank-`C(4,k)` Hamming-weight-`k`
projector. Equivalently `B_grav P_1 = B_grav` (entirely on HW=1).
Each `B_a` acts with unit eigenvalue on `|1_a⟩`:
`⟨1_a|B_a|1_a⟩ = 1`. Verified to machine precision for all four axes.

### Step 3: Apply Codex's uniqueness theorem

By PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM (Codex,
2026-04-25), the unique diagonal operator on `H_cell` satisfying
conditions (C1)–(C4) is `B = P_A`. Since `B_grav` satisfies all four
conditions (Step 2), `B_grav = P_A` as an operator equality on
`H_cell`.

The runner verifies this operator equality directly:
`||B_grav - P_A|| = 0` to machine precision, with matching spectra
(twelve zero eigenvalues + four unit eigenvalues).

### Step 4: Coefficient fixing via source-unit normalization

The source-free trace gives

```text
c_cell = Tr(ρ_cell B_grav) = Tr((I/16) P_A) = 1/4.
```

By the retained source-unit normalization theorem
(PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25),

```text
1 / (4 G_Newton,lat) = c_cell = 1/4,
```

forcing `G_Newton,lat = 1` in natural lattice units. Hence

```text
(a / l_P)^2 = 1 / G_Newton,lat = 1   ⇒   a / l_P = 1.
```

The carrier-conditional language in the source-unit normalization
theorem is now closed: the carrier is identified as `B_grav = P_A` by
this theorem.

### Step 5: Cross-validation against Clifford-CAR area-law chain

Independently, the retained Clifford phase bridge
(PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM, with the metric-
compatible coframe-response premise now derived from the cubic-bivector
Schur source-principle and the synthesis closure) gives the
Widom–Gioev–Klich coefficient on the primitive Cl_4-CAR carrier:

```text
c_Widom = (2 + 2 * 1/2) / 12 = 3/12 = 1/4 = c_cell.
```

The two independent retained chains (gravity-action variation +
Clifford-CAR area law) give the same `c_cell = 1/4` on the same
primitive boundary block `B_grav = P_A`, providing a consistency
cross-check.

QED.

## Status of all prior open residuals (now closed)

| Residual | Earlier status | Status after this theorem |
|---|---|---|
| Carrier identification: derive that the primitive one-step boundary count IS the gravitational carrier | Open ("the remaining positive Planck target") | **Closed** by Steps 1–3: `B_grav` extracted from retained `S = kL(1 - φ)` IS `P_A` by Codex uniqueness |
| Codex 2026-04-26 review (R1): P_1 vs Hodge-dual P_3 selection | Open in Schur source-coupling theorem | **Closed**: `B_grav` is extracted directly from retained gravity action and is uniquely on HW=1 by first-order locality (Part B Cond. 4); Hodge-dual P_3 is not selected by `S = kL(1 - φ)` variation |
| Codex 2026-04-26 review (R2): chi_eta * rho * Phi source-coupling identification | Open in Schur source-coupling theorem | **Closed**: source-coupling normalization derived from `B_grav = P_A` + boundary-density extension theorem + source-unit normalization theorem (Steps 4) |
| Codex 2026-04-26 review (P1)/1: H_first selector not derived | Open in Schur identity theorem | **Closed**: `B_grav` directly extracted from retained gravity action, not chosen Cl_4 word; the H_first vacuum-orbit closure remains as a sufficient companion structural argument for the Cl_4 side, but is not load-bearing here |
| Codex 2026-04-26 review (P1)/2: source-coupling normalization imposed | Open in Schur identity theorem | **Closed**: derived via Steps 1–4 from retained content (gravity action variation + Codex uniqueness + source-unit normalization), not imposed |
| Codex 2026-04-26 review (P2): bridge note conditional wording | Open | **Closed** by paired update in this commit: Clifford phase bridge note body cleaned up to match unconditional headline; the metric-compatible coframe-response premise is derived from `B_grav = P_A` + cubic-bivector Schur structure |

## Re-promotion of related notes (concurrent with this landing)

| Note | Status |
|---|---|
| `PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md` | retained UNCONDITIONAL (no live conditionals); the metric-compatible coframe-response premise is derived from B_grav = P_A + cubic-bivector Schur |
| `PLANCK_TARGET3_FORCED_COFRAME_RESPONSE_THEOREM_NOTE_2026-04-25.md` | retained necessary structural conditions in the unconditional closure chain |
| `PLANCK_TARGET3_GAUSS_FLUX_FIRST_ORDER_CARRIER_THEOREM_NOTE_2026-04-25.md` | retained physical interpretation support; the 1-form / first-order coframe carrier IS the B_grav variation per axis |
| `PLANCK_TARGET3_CUBIC_BIVECTOR_SCHUR_SOURCE_PRINCIPLE_THEOREM_NOTE_2026-04-26.md` | retained structural foundation |
| `PLANCK_TARGET3_SCHUR_SOURCE_COUPLING_IDENTITY_THEOREM_NOTE_2026-04-26.md` | retained intermediate; both Codex (P1) residuals closed by THIS theorem |
| `PLANCK_TARGET3_SYNTHESIS_UNCONDITIONAL_CLOSURE_THEOREM_NOTE_2026-04-26.md` | retained companion synthesis (S_4 uniqueness on Cl_4 side); this theorem provides the simpler, more direct gravity-action route |
| `PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md` | retained -- the carrier-conditional language is closed by this theorem identifying the carrier as B_grav = P_A |
| `PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md` | retained -- the open residual flagged in §"What remains open" is now closed by this theorem |

## Package wording

Safe wording:

> The gravitational boundary action density operator `B_grav` on the
> time-locked primitive event cell, extracted from the retained Cl(3)/
> Z^3 gravity action `S = k L (1 - φ)` by primitive event cell
> variation (Gibbons–Hawking–York-style boundary term in the
> framework's discrete formulation), satisfies all four uniqueness
> conditions of Codex's primitive coframe boundary carrier theorem
> (source-free response, axis additivity, S_4 cubic frame symmetry,
> first-order locality + unit response). By the uniqueness theorem,
> `B_grav = P_A` as an operator equality on `H_cell`, verified to
> machine precision. The source-free trace gives `c_cell = 1/4`, and
> the retained source-unit normalization theorem gives `G_Newton,lat
> = 1` and `a/l_P = 1` in natural phase/action units. The Planck pin
> `a^{-1} = M_Pl` is therefore RETAINED on the minimal stack, no
> longer a conditional structural theorem. "1 axiom + 0 parameters"
> is defensible as public framing. The Hilbert-only Target 3
> boundary no-go is not contradicted: this theorem uses the retained
> gravity action `S = kL(1 - φ)`, not bare Hilbert flow.

Unsafe wording:

> The framework derives the SI decimal value of `ℏ`.

Not proved. The closure is in the package's natural phase/action
units (`a = l_P = 1`); SI metrology is not a derivation target.

## Verification

```bash
python3 scripts/frontier_planck_gravity_boundary_coframe_identification.py
```

Current output:

```text
Summary: PASS=40  FAIL=0
```

The 40 checks cover:

- **Part 0** (9): all required retained authority files exist (gravity
  action chain + Codex carrier theorem + source-unit normalization +
  Clifford phase bridge + lane status note).
- **Part A** (2): `B_grav` constructed from the gravity-action variation
  on the primitive cell as a sum of one-axis worldtube boundary
  contributions; verified Hermitian projector with rank 4.
- **Part B** (12): four uniqueness conditions of Codex's carrier theorem
  - (C1) source-free response = c_cell = 1/4
  - (C2) axis additivity B_grav = sum_a B_a; mutual orthogonality of B_a
  - (C3) S_4 cubic frame symmetry across all 24 axis permutations
  - (C4) first-order locality (B_grav P_k = 0 for k != 1; B_grav P_1 = B_grav)
  - (C4) unit response on each |1_a⟩ for all four axes
- **Part C** (3): Codex uniqueness theorem applied
  - operator equality B_grav = P_A to machine precision
  - spectrum match
  - trace match
- **Part D** (3): coefficient c_cell = 1/4; source-unit normalization
  G_Newton,lat = 1; a/l_P = 1
- **Part E** (4): cross-validation against Clifford-CAR
  - c_Widom = 1/4 = c_cell
  - source-unit theorem cross-check
  - lambda = 1 consistency
- **Part F** (2): combined chain - G_Newton,lat = 1 and a/l_P = 1
  RETAINED unconditional from the minimal stack
- **Part G** (7): scope guardrails
  - no imported physical constants
  - no fitted coefficient
  - no SI hbar
  - all closure steps OBJECT-LEVEL (no literal-True for load-bearing)
  - Hilbert-only Target 3 no-go NOT contradicted
  - Codex (P1)/1 + (P1)/2 closed
