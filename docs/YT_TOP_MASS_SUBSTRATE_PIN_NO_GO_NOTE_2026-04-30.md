# Top-Sector Bare-Mass Substrate Pin: Five-Frame No-Go Theorem

**Date:** 2026-04-30
**Status:** exact-negative-boundary / no-go — five-frame stuck fan-out, no
  derivation found on any explored route
**Claim boundary authority:** this note
**Import ledger:** `YT_TOP_MASS_SUBSTRATE_PIN_ASSUMPTIONS_AND_IMPORTS_2026-04-30.md`
**Runner:** `scripts/frontier_yt_top_mass_substrate_pin_no_go.py`
**Delivery surface:** PR #230 (`claude/yt-direct-lattice-correlator-2026-04-30`)

---

## 0. Purpose and Question

PR #230 lands a direct staggered-correlator measurement gate for the top-sector
Yukawa `y_t = sqrt(2) m_t / v`. That note identifies a single remaining
condition for derivational status:

> *"an independent non-MC substrate pin for the top-sector mass parameter"*

This note executes a five-frame exhaustive search for such a pin on the
`Cl(3)/Z^3` / `g_bare = 1` / staggered-Dirac substrate. Forbidden as proof
inputs: `H_unit`, `yt_ward_identity`, `alpha_LM`/plaquette/tadpole routes,
PDG `m_t`, target `y_t`, observed top-mass tuning, fitted selectors, and
algebraic definitions of `y_t_bare`.

The five frames are:

1. Spectral / Dirac eigenvalue route
2. Topological / Z^3 boundary-condition route
3. Taste / staggered-representation route
4. Algebraic / Cl(3) representation-theoretic route
5. Anomaly / 't Hooft anomaly-matching route

Each frame is executed from minimal permitted inputs (section A of the import
ledger). Each reaches the same obstruction. After the five-frame fan-out, a
synthesis identifies the exact Nature-grade wall.

**Verdict: No-go / exact-negative-boundary.** No substrate-native pin for the
top-sector heavy bare mass parameter exists within the permitted input set.

---

## 1. Substrate Inputs Available (Permitted Set)

The following are available as proof inputs. All others are excluded.

| Input | Class |
|---|---|
| `Z^3` bipartite topology → `Z_2` → `Cl(3)` → `SU(2)` | exact structural |
| Graph-first axis selector → structural `SU(3)` | exact structural |
| `g_bare = 1` (axiom) | axiom |
| `N_gen = N_color = 3`, `N_pair = 2`, `N_quark = 6` | exact retained counts |
| `R_conn = 8/9` | zero-input structural |
| `(7/8)^(1/4)` APBC selector | exact structural |
| SM one-Higgs Yukawa monomial `bar Q_L tilde H u_R` | exact retained |
| Staggered Dirac Clifford structure on `Z^3` | exact structural |
| SU(3) Casimirs `C_F = 4/3`, `C_A = 3`, `T_F = 1/2` | exact retained |
| Taste cube `V = {0,1}^3`, axis shifts `S_1, S_2, S_3` | exact structural |

---

## 2. Frame 1 — Spectral / Dirac Eigenvalue Route

### 2.1 Attempt

The staggered Dirac operator `D(m_0)` on `Z^3` (with gauge coupling `g_bare = 1`)
has an eigenvalue spectrum `{λ_k(m_0)}` that depends on the bare mass parameter
`m_0`. The search question is: does any spectral property of `D(m_0)` select a
unique value of `m_0` without additional physical input?

Spectral properties investigated:

**(a) Zero modes / Index theorem.** By the Atiyah-Singer index theorem on
a 4-torus `T^4`,

```
  index(D) = n_+ - n_- = Q   (topological charge)
```

Zero modes exist only at `m_0 = 0` (chiral limit, specific gauge backgrounds).
They constrain the spectrum at `m_0 → 0`, not at large `m_0`. No pinning of
a heavy mass follows.

**(b) Spectral gap / phase transition.** The staggered Dirac spectrum has a gap
near `m_0 = 0` in the strong-coupling phase. At heavy `m_0`, the spectrum is
gapped by `m_0` itself. There is no additional spectral gap structure that
collapses at a specific large `m_0` value without gauge-field MC data. The
spectral density `ρ(λ; m_0)` at fixed `g_bare` is a smooth function of `m_0`
for large `m_0`; it has no canonical zero or extremum.

**(c) Free-field limit.** At `g_bare = 1` (strong coupling), the free-field
approximation `D_free = i sum_μ γ_μ sin(p_μ) + m_0` gives eigenvalues
`λ_k = sqrt(sum_μ sin^2(p_k,μ)) + m_0`. These grow monotonically with `m_0`;
no special value is singled out.

**(d) Effective-mass plateau value.** The large-time limit of the top-sector
correlator `C_t(τ) → A exp(-m_t τ)` gives `m_t = m_t(m_0, g_bare)`, a
continuously variable function. It does not have a substrate-native extremum
or critical value without a separate input.

### 2.2 Obstruction

The staggered Dirac spectrum does not pin a heavy mass. The spectrum depends
continuously on `m_0`; zero modes pin only the chiral limit; phase transitions
(if any) pin only a coupling-dependent crossover, not a specific dimensionful
mass value.

**Exact obstruction statement (Frame 1)**: For any value of `m_0` in the range
`(0, a^{-1})`, the staggered Dirac spectrum on `Z^3` at `g_bare = 1` is
consistent with QCD confinement physics. No substrate-native eigenvalue
condition selects the top-sector mass.

---

## 3. Frame 2 — Topological / Z^3 Boundary-Condition Route

### 3.1 Attempt

The spatial lattice `Z^3` (or compactified `T^3`) has topological structure:

- `π_1(T^3) = Z^3` (translation cycles)
- `π_2(T^3) = 0`
- `π_3(T^3) = Z` (3-cycles, wrapping number)

For a gauge theory on `T^3 x T` (periodic/antiperiodic boundary conditions),
topological constraints operate via:

**(a) Witten SU(2) anomaly.** For `SU(2)` gauge theory on `S^4`, `π_4(SU(2)) = Z_2`
produces an anomaly requiring an even number of Weyl doublets. In the retained
SM matter content on the `Cl(3)/Z^3` surface, each generation contributes
`N_color = 3` quark doublets and 1 lepton doublet, giving `(3+1) * N_gen = 12`
doublets total. `12` is even. This cancels the Witten anomaly and constrains
the *number* of doublets, but NOT the fermion masses.

**(b) Discrete translation anomaly (Lieb-Schultz-Mattis type).** For a lattice
system with `N` sites and filling fraction `n/N`, the LSM theorem constrains
whether the spectrum is gapped or gapless. For a 4D lattice QCD system, LSM-type
arguments constrain the existence of a mass gap (confinement) but not the value
of a specific heavy quark mass.

**(c) Instanton / BPST solitons.** On `T^4` with gauge group `SU(3)`,
instantons contribute to the mass spectrum through the `θ`-term and the
`eta'` mass (`m_η'² ≈ 2 N_f / f_π² × χ_top`). This gives a constraint on
the pseudoscalar singlet, not on the heavy top mass. The topological
susceptibility `χ_top` depends on MC data.

**(d) Z_N center vortex / center symmetry on T^3.** The Polyakov loop `L(x) = Tr P exp(i∫ A_0 dt)` can wind around the temporal direction. The center symmetry `Z_3` is unbroken below the deconfinement temperature. For a single quark species of mass `m_0`, adding any `m_0 ≠ 0` explicitly breaks `Z_3`. The deconfinement transition temperature `T_c` depends weakly on `m_0` for heavy quarks; it does not pin a unique `m_0`.

**(e) Boundary-condition anomaly (APBC/PBC).** The antiperiodic temporal boundary conditions (APBC) for fermions create a parity-twisted fermion sector. The staggered spectrum with APBC has eigenvalues shifted by `π/T` in the temporal Matsubara modes. This shifts all mass poles equally; it does not select a specific heavy mass.

**(f) Euler characteristic / Gauss-Bonnet on Z^3.** The spatial `Z^3` lattice as a simplicial complex has `χ(Z^3) = 0` (acyclic, contractible for infinite `Z^3`). For finite `T^3`, `χ(T^3) = 0`. The Gauss-Bonnet theorem relates `χ` to the integrated curvature, but `T^3` is flat, so no curvature-induced mass follows.

### 3.2 Obstruction

Topological arguments on `Z^3 / T^3 x T` constrain:
- Counting (anomaly cancellation, LSM filling)
- Existence of gaps (LSM for gapped vs. gapless)
- Integer-valued invariants (instanton number, wrapping number)

None produces a dimensionful mass constraint for a specific heavy fermion flavor.

**Exact obstruction statement (Frame 2)**: The topological structure of the
`Z^3 / T^4` substrate, including all boundary conditions (PBC/APBC), center
symmetry, instanton structure, and Witten anomaly, constrains the counting and
integral invariants of the theory but cannot select a specific numerical value
for the top-sector bare mass parameter.

---

## 4. Frame 3 — Taste / Staggered-Representation Route

### 4.1 Attempt

On `Z^3` (3D spatial lattice), the staggered fermion phases `η_μ` produce
`2^3 = 8` taste species with a `Cl(3)` algebra in taste space. In 4D
(spatial `Z^3` plus temporal `Z`), the full staggered theory has `2^4 = 16`
taste species with a `Cl(4)` algebra. These form specific representations of
the taste group `SU(4)` (approximate symmetry of the staggered action):

- `1` scalar taste (ξ = 0)
- `4` vector tastes
- `6` tensor tastes
- `4` axial-vector tastes
- `1` pseudoscalar taste (ξ = 5, pseudo-Goldstone)

**(a) Taste degeneracy.** All 16 staggered tastes carry the same bare mass `m_0`.
There is no taste-selective mass splitting from the action; taste splitting
enters only at `O(α_s a^2)`. This is numerically small and depends on the
lattice spacing `a` (which requires the plaquette/scale-setting route to fix
numerically). **Taste arguments do not select a specific bare mass value.**

**(b) Taste-breaking spectrum.** The taste-breaking operator `Δ_taste` generates
splittings `δm² ∝ α_s a²`. For the top quark at large `m_0`, the taste
splitting `δm²/(m_0^2) ∝ α_s a²/m_0^2` → 0. At the heavy-mass scale of the
top, taste splittings are entirely sub-dominant; no taste eigenvalue is pinned
at the top mass.

**(c) Taste-staircase transport.** The YT UV-to-IR transport obstruction theorem
(P2 primitive) defines a 16-step staggered taste staircase. The v-matching
coefficient `M = sqrt(u_0) * F_yt * sqrt(8/9) ≈ 1.927` is partially derivable.
But this coefficient pins the *transport ratio* `y_t(v)/y_t_bare`, not the
bare mass itself. To get a bare mass from this, one needs `y_t_bare`, which is
either a free parameter or the Ward identity (forbidden).

**(d) Pseudo-Goldstone pion mass.** The lightest staggered taste (pseudo-Goldstone)
has mass `m_π² ∝ m_0 Λ_QCD` (PCAC). This pins the pion mass given the light
quark mass, but does not constrain the heavy top mass.

**(e) Graph-first axis selector applied to taste masses.** The substrate-native
graph-first selector function

```
V_sel(φ) = Tr H(φ)^4 - (1/8)(Tr H(φ)^2)^2 = 32 Σ_{i<j} φ_i^2 φ_j^2
```

minimizes along the three axis vertices of `{0,1}^3`. This selects the SU(2)
weak axis structurally. If one tries to apply an analogous selector to the
three up-type quark masses `(m_u, m_c, m_t)` by analogy, treating them as
components of a 3-vector, the selector would extremize when two masses are equal
or when one dominates. But: (i) this would require an identification between
the taste-cube geometry and the mass spectrum that has no substrate-native
justification; (ii) the selector picks an *axis* (direction), not a specific
*magnitude*. Even if axis selection is structural, the magnitude of the mass
vector requires physical input.

### 4.2 Obstruction

Taste arguments:
- Cannot break the universal bare-mass degeneracy (all tastes share `m_0`)
- Can constrain the *transport ratio* but not the bare mass independently
- Produce splittings that require `a` (lattice spacing), which requires the
  plaquette route

**Exact obstruction statement (Frame 3)**: The staggered taste structure on
`Z^3 / T^4` cannot select a specific value for the top-sector bare mass
parameter. All 16 taste species carry the same `m_0`; taste splittings are
sub-dominant at the top mass scale and require the plaquette/tadpole route to
evaluate.

---

## 5. Frame 4 — Algebraic / Cl(3) Representation-Theoretic Route

### 5.1 Attempt

The `Cl(3)` Clifford algebra and the structural `SU(3)` together produce a
gauge group with known Casimirs:
- `C_F(SU(3)) = 4/3` (fundamental)
- `C_A(SU(3)) = 3` (adjoint)
- `C_2(SU(2)) = 3/4` (fundamental)
- `C_2(Cl(3)) for spinor = 3/4`

**(a) Casimir mass.** Could a "Casimir mass" `m_cas ~ Λ * C_2(rep)` pin the
top mass? Any such formula requires Λ (a UV energy scale). On the substrate,
Λ could be `M_Planck` (from the axiom stack), but converting `M_Planck * C_2 / (some N-factor)` to GeV requires the plaquette/coupling chain to fix the ratio
`a M_Planck`. This imports the forbidden plaquette route.

**(b) Representation eigenvalue / highest weight.** The top quark (as `u_R`)
is in the `(1, 3)` representation of `SU(2)_L x SU(3)_c`. The highest-weight
label is `λ = (1, 0)` for `SU(3)_c` fundamental. The dimension of this
representation is 3. No eigenvalue of the `SU(3)` Casimir gives a mass without
a coupling/scale input.

**(c) Cl(3) trilinear invariant.** The Clifford algebra `Cl(3)` (acting on the
8-dimensional taste space) has a trilinear invariant from the `ε_{ijk}`
structure of the three generators `Γ_1, Γ_2, Γ_3`. Could this trilinear
invariant select a mass ratio? A trilinear invariant produces an integer or
rational number (e.g., `Tr[Γ_1 Γ_2 Γ_3] = ±8i`), not a dimensionful mass.

**(d) Generation ratio / N_gen = N_color constraint.** The retained equality
`N_gen = N_color = 3` constrains the counting but not the mass hierarchy. For
three up-type quarks `(m_u, m_c, m_t)`, the only substrate-native count
constraint is `count = 3`. The ratio `m_t / m_c` or `m_t / m_u` is NOT fixed
by this counting constraint.

**(e) Koide-type formula for up-type quarks.** The Koide relation

```
Q = (m_u + m_c + m_t) / (sqrt(m_u) + sqrt(m_c) + sqrt(m_t))^2 = 2/3
```

is a mass relation for the up-type sector. If valid, it provides one constraint
among three unknowns. However:
  - The Koide relation for up-type quarks has NOT been derived from the
    `Cl(3)/Z^3` substrate (the charged-lepton direct Ward-free Yukawa no-go note
    already records the failure of substrate-native Koide for charged leptons;
    see `CHARGED_LEPTON_DIRECT_WARD_FREE_YUKAWA_NO_GO_NOTE_2026-04-26.md`)
  - Even if the Koide relation held, it provides one equation for three unknowns;
    the two lighter masses must be supplied as additional inputs
  - Using PDG `m_u` or PDG `m_c` to get `m_t` would import forbidden observed
    mass data

**(f) Weight lattice / SU(3) Lie algebra roots.** The SU(3) root lattice has
three simple roots `α_1, α_2, α_3`. The highest root has length squared `2`.
There is no mechanism by which the root-length spectrum of the Lie algebra
produces a mass spectrum for the quarks.

**(g) R_conn = 8/9 as a mass ratio seed.** The retained ratio `R_conn = 8/9`
enters the Yukawa color projection. If `y_t_bare = g_bare * sqrt(R_conn / (2 N_c))`
were derivable, it would give a specific value. But this identity is equivalent
to the Ward identity up to the SU(3) normalization factor, which is the
forbidden route. Specifically: `R_conn / (2 N_c) = (8/9) / 6 = 4/27 ≠ 1/6`,
so this is not the same as the Ward identity, but deriving it would still
require identifying `y_t_bare` with a specific expression involving the gauge
coupling — which is the class of forbidden algebraic-definition routes.

### 5.2 Obstruction

The `Cl(3)` and `SU(3)` algebraic structure produces structural integers,
Casimirs, and counting constraints. None produces a dimensionful mass without a
scale anchor (which requires the plaquette route) or without the Yukawa-gauge
identification (which is the Ward identity route). The Koide approach requires
additional mass inputs or a substrate derivation of Koide that does not exist.

**Exact obstruction statement (Frame 4)**: The `Cl(3) / SU(3)` representation
theory and structural counting on the `Z^3` substrate produce dimensionless
Casimirs, integer counts, and structural ratios. None pins a specific value for
the top-sector bare mass without importing either (i) the forbidden Ward identity
or (ii) a scale anchor from the plaquette/tadpole coupling route.

---

## 6. Frame 5 — Anomaly / 't Hooft Anomaly-Matching Route

### 6.1 Attempt

In QFT, 't Hooft anomaly matching is a powerful non-perturbative constraint:
if a global symmetry has a 't Hooft anomaly, the IR spectrum must match that
anomaly. The question is whether any 't Hooft anomaly of the `Cl(3)/Z^3` substrate
constrains the top-sector bare mass.

**(a) Baryon-number U(1)_B anomaly.** The baryon-number current `J_B = (1/3) bar q_i γ_μ q_i`
has a mixed anomaly with SU(3)_c:
```
∂_μ J_B^μ = (1/32π²) F^a_{μν} tilde F^a_{μν}   (QCD θ-term contribution)
```
This anomaly is present in the IR as well (via the QCD θ-term). It constrains
the axial baryon-number spectrum (the eta') but does NOT constrain the vector
quark masses `m_t`.

**(b) Chiral anomaly / ABJ anomaly.** The axial flavor symmetry `U(N_f)_A` has
anomalies with SU(3)_c and U(1)_B. The ABJ anomaly gives the axial-current
divergence `∂_μ J^5_μ ∝ F tilde F`. This constrains the pseudo-Goldstone
spectrum (pion masses from `m_π² ∝ m_q Λ_QCD`) but not the heavy quark mass.

**(c) Discrete chiral anomaly / Z_{2N_f} symmetry.** At `m_q = 0`, the discrete
chiral symmetry `Z_{2N_f}` has an anomaly that constrains the vacuum structure
(chiral condensate, confinement). But heavy quarks (top quark with `m_t >> Λ_QCD`)
decouple from the chiral dynamics; their contribution to the anomaly coefficient
is suppressed by `(Λ_QCD / m_t)^n`.

**(d) Mixed gauge-gravity anomaly.** For a chiral fermion of hypercharge Y,
the mixed gauge-gravity anomaly coefficient is `Tr[Y]`. In the SM, anomaly
cancellation requires specific charge assignments, which are already captured
by the retained matter-content and EW structure. The anomaly conditions are
satisfied by the charge assignments of all quarks and leptons together; they
do not constrain individual fermion masses.

**(e) Gravitational anomaly `Tr[T]`.** The trace anomaly (energy-momentum
tensor) `T^μ_μ = -b g² F²` relates the running of the coupling to the
energy-momentum trace. This is connected to scale invariance violation (conformal
anomaly). In the top sector, the conformal anomaly contributes `m_t T_bar t`
to the trace, but this is a *consequence* of the mass, not a constraint on it.

**(f) 't Hooft anomaly for discrete `Z_3` center symmetry.** The SU(3) center
`Z_3` in the confined phase has a specific 't Hooft anomaly that constrains the
confinement/deconfinement structure. But this constrains whether the fundamental
representation quarks are confined, not their mass values.

**(g) Discrete `Z_3` flavor symmetry anomaly.** If the substrate had a `Z_3`
flavor permutation symmetry acting on `(u, c, t)`, an anomaly for that symmetry
could constrain mass ratios. However: (i) in the staggered theory, all species
carry the same bare mass `m_0`, so there is no flavor-permutation anomaly in the
bare theory; (ii) even if the IR theory had a broken `Z_3` flavor symmetry, its
anomaly would constrain only whether the symmetry-breaking is partial or complete
(`m_u = m_c ≠ m_t` vs. `m_u ≠ m_c ≠ m_t`), not the specific values.

**(h) Anomaly inflow and boundary states.** On a 4D manifold with boundary,
the Chern-Simons term on the boundary provides anomaly inflow to compensate
for the boundary anomaly. This is relevant for describing edge modes in
topological insulators (which have a structural analogy to the staggered
fermion). Could the edge modes have pinned mass? Edge-mode masses are
`m_edge ~ 1/L` (inverse system size), not the top quark mass scale.

### 6.2 Obstruction

Anomaly matching constraints preserve 't Hooft anomalies from UV to IR. They
pin: (i) the qualitative pattern of symmetry breaking (Goldstone spectrum,
confinement), (ii) counting (Witten SU(2) parity), and (iii) charge
assignments. They do NOT pin the dimensionful mass of a specific heavy quark
flavor.

**Exact obstruction statement (Frame 5)**: All 't Hooft anomaly-matching
arguments for the `Cl(3)/Z^3` substrate (gauge, chiral, discrete center,
gravitational, mixed gauge-gravity) constrain counting, charge assignments, and
qualitative symmetry-breaking patterns. None provides a specific numerical
constraint on the top-sector bare mass parameter `m_0`.

---

## 7. Synthesis: The Exact Nature-Grade Wall

### 7.1 Agreements across all five frames

All five frames agree on the following:

1. The `Cl(3)/Z^3` substrate fully determines the gauge group structure
   (`SU(3) x SU(2)_L x U(1)_Y`) and matter representations.
2. The gauge symmetry does NOT constrain the Yukawa coupling coefficients.
3. The only known substrate-native constraint on the top Yukawa (`y_t_bare^2 =
   g_bare^2 / (2 N_c) = 1/6`) is explicitly forbidden as a proof input.
4. None of the five frames (spectral, topological, taste, representation,
   anomaly) produces a substitute constraint that pins `m_0` without importing
   a forbidden input.

### 7.2 The exact Nature-grade wall

The fundamental obstruction is the **Yukawa Coupling Freedom Theorem**:

> In any gauge field theory with gauge group G, matter fields in representations
> R_i, and a scalar sector H, the Yukawa couplings `y_ij` (coefficients of the
> gauge-invariant monomials `bar ψ_i H ψ_j` plus h.c.) are independent free
> parameters not constrained by G-gauge invariance or the spacetime topology of
> the base manifold. They transform as singlets under G and require independent
> physical/dynamical input to fix.

On the `Cl(3)/Z^3` substrate:
- The gauge group G = `SU(3) x SU(2)_L x U(1)_Y` is derived from the topology.
- The matter representations are derived from the taste structure.
- The Yukawa monomial structure is derived from the gauge selection theorem.
- The **coefficient** `y_t_bare` in `y_t_bare (bar Q_L tilde H u_R)` remains a
  free dimensionless parameter.

This freedom is the exact wall. No algebraic, spectral, topological, taste,
representation, boundary-condition, or anomaly argument can circumvent it
without either (a) the Ward identity (forbidden), or (b) an additional dynamical
mechanism that does not exist in the standard staggered-fermion substrate.

### 7.3 Additional routes explored and blocked

Beyond the five main frames, the following routes were also explored:

| Route | Obstruction |
|---|---|
| Top Yukawa IR quasi-fixed-point (Pendleton-Ross) | Requires `alpha_s(v)` or `alpha_LM` (forbidden) |
| Winding number / baryon-number soliton mass | `m_soliton ~ f_π/a`; requires plaquette for `a^{-1}` |
| Conformal fixed-point mass spectrum | QCD at `g_bare = 1` is not conformal; no IR fixed point |
| Yukawa-gauge unification at UV scale | Equivalent to Ward identity (forbidden) |
| Staggered threshold / scale-setting correction | Requires lattice spacing `a` (plaquette route) |
| Discrete graph-first selector applied to mass ratios | Selector pins direction (axis), not magnitude |
| CKM-structure seed for up-quark mass ratio | CKM forbiddance and chain requires light quark masses |

### 7.4 What changes would enable a pin

For completeness, the following changes to the permitted input set would allow a
substrate-native pin to exist:

| Change | Resulting pin |
|---|---|
| Permit `yt_ward_identity` | `y_t_bare = g_bare/sqrt(2 N_c) = 1/sqrt(6)` exactly |
| Permit `alpha_LM` / plaquette | IR quasi-fixed-point pin; `y_t(v) ≈ g_s(v) / sqrt(2)` approximately |
| Add a new dynamical mechanism (SUSY, compositeness) | Would require a new substrate axiom |
| Add Koide derivation for up-type quarks | Would require three-mass solution; speculative |

None of these is available within the current forbiddance set.

---

## 8. Claim Status

```yaml
actual_current_surface_status: no-go / exact-negative-boundary
conditional_surface_status: null
hypothetical_axiom_status: "conditional on permitting yt_ward_identity: exact y_t_bare = 1/sqrt(6)"
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: "No-go result; there is no positive substrate pin to propose for retention."
audit_required_before_effective_retained: false
bare_retained_allowed: false
```

---

## 9. Implication for PR #230

The no-go result implies that, within the current forbiddance set, the direct
staggered-correlator lane (PR #230) **cannot** achieve derivational status
through a substrate-native non-MC pin. The only available upgrade paths are:

1. **Permit `yt_ward_identity`**: If the loop goal is revised to allow the Ward
   identity as a proof input, the substrate pin becomes trivially exact:
   `y_t_bare = g_bare / sqrt(2 N_c) = 1/sqrt(6)`. The correlator then measures
   the IR observables `m_t(v), y_t(v)` from a substrate whose UV parameter is
   analytically fixed. This would upgrade PR #230 from calibration to derivation.

2. **Downgrade to calibrated readout**: Accept PR #230's current status as a
   calibrated physical-observable readout lane. The PR already explicitly
   provides this downgrade path (option 2 in the theorem note). This is the
   honest current status.

3. **New dynamical mechanism outside the current substrate**: A future substrate
   extension (new axiom, new symmetry) could provide an alternative pin. This
   requires a new proposal outside the current framework.

**Safe current claim for PR #230**: The direct staggered-correlator lane is a
production-capable measurement gate that, after production data exists, will
read out `m_t -> y_t` from the ensemble. Its derivational vs. calibration status
depends on whether the top-sector bare mass parameter is fixed by the Ward
identity (which is derivable from the substrate but currently forbidden as a
proof input) or by tuning to observation.

---

## 10. Appendix: Runner Check Map

The paired runner `scripts/frontier_yt_top_mass_substrate_pin_no_go.py`
verifies:

1. That the Ward identity `y_t_bare^2 = g_bare^2 / (2 N_c) = 1/6` is
   structurally derivable from the permitted axioms (D16 + D17 + D12 + S2) —
   confirming it IS a substrate-native pin — while verifying it is FORBIDDEN
   as a proof input under the loop goal.

2. That no Frame 1-5 route produces a numerical mass value different from
   importing a forbidden input.

3. That the `R_conn = 8/9` structural factor, when substituted into a
   Yukawa-like formula without the Ward identity, does not independently pin
   `y_t_bare` (i.e., `sqrt(R_conn / (2 N_c)) ≠ 1/sqrt(6)` and thus does not
   bypass the Ward identity route).

4. The exact blocker decomposition: Yukawa coupling freedom theorem holds under
   permitted inputs.

5. The three alternative paths (permit Ward, downgrade to calibration, new
   mechanism) are mutually exclusive at the current surface.

Expected: `PASS = 19, FAIL = 0`
