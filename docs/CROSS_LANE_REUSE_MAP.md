# Cross-Lane Theorem Reuse Map

**Date:** 2026-04-12
**Branch:** `claude/youthful-neumann`
**Purpose:** Identify theorems and intermediate results that appear in one lane
but would strengthen another if explicitly connected.

Each connection is classified as:
- **(a) Already made** -- the connection exists in a current note or script.
- **(b) Straightforward** -- the ingredients are proved; writing the bridge is editorial.
- **(c) Requires new work** -- a genuine gap separates the two lanes.

---

## 1. Cl(3) Centrality (from y_t lane)

**Source theorem:** In d=3 (odd dimension), the Clifford volume element
Gamma_5 = i G_1 G_2 G_3 is central: [Gamma_5, X] = 0 for all X in Cl(3).
Any Feynman diagram with a Gamma_5 insertion factorizes:
D[Gamma_5] = Gamma_5 * D[I]. This protects y_t/g_s = 1/sqrt(6) against
all radiative corrections at the lattice scale.

**Source files:** `docs/RENORMALIZED_YT_PAPER_NOTE.md`,
`docs/YT_FIXED_POINT_NOTE.md`, `docs/SLAVNOV_TAYLOR_COMPLETION_NOTE.md`

### 1A. Centrality -> Generation mass matrix

**Target lane:** Generation physicality (mass hierarchy, Layer E)

**Connection:** The generation mass hierarchy depends on the EWSB cascade
producing different radiative corrections for different Z_3 orbit members.
The Cl(3) centrality theorem says that Gamma_5 insertions factorize, but
the Wilson mass M_W (which determines generation masses) is NOT proportional
to Gamma_5 -- it is a sum of terms ~s_mu * t_mu. Therefore Cl(3) centrality
does NOT protect the generation mass matrix from radiative corrections.

The generation mass splitting is entirely radiative (tree-level masses are
degenerate within each orbit), so the non-protection of M_W by centrality
is actually required for the generation mechanism to work.

**Status: (b) Straightforward to state as a negative result.** The paper
should note that Cl(3) centrality protects y_t but does NOT constrain the
generation mass hierarchy -- and that this is consistent, because the
mass hierarchy is a radiative effect that centrality would kill if it applied.

**Files:** `docs/EWSB_GENERATION_CASCADE_NOTE.md` (mass hierarchy mechanism),
`docs/GENERATION_AXIOM_FIRST_NOTE.md` (Wilson mass structure)

### 1B. Centrality -> DM Sommerfeld computation

**Target lane:** DM relic mapping

**Connection:** The DM Sommerfeld enhancement uses the Coulomb potential
V(r) = -C_F * alpha_s / r and the Born cross-section sigma_v ~ alpha_s^2/m^2.
Both depend on the gauge coupling alpha_s, which enters through the plaquette
action. The centrality theorem says nothing about the gauge sector directly --
it constrains the Yukawa vertex (Gamma_5 insertion), not the gauge vertex
(G_mu insertion). However, the g_bare = 1 derivation
(`docs/G_BARE_DERIVATION_NOTE.md`) uses the Cl(3) normalization of the
gauge connection, which is related to centrality only indirectly (both derive
from the Cl(3) algebra structure).

The DM sigma_v lattice derivation (`docs/DM_SIGMA_V_LATTICE_NOTE.md`)
uses the optical theorem + Lippmann-Schwinger T-matrix, which are
algebraic/unitarity results, not centrality results. Centrality does not
simplify the Sommerfeld computation.

**Status: (b) Straightforward to document as no direct connection.** The
indirect connection (both centrality and g_bare = 1 derive from Cl(3)
normalization) could be mentioned as a shared root, but there is no
theorem-level reuse.

### 1C. Centrality -> CKM mixing

**Target lane:** CKM (bounded)

**Connection:** The CKM lane requires Higgs Z_3 charge = 1, which is
obstructed (see `docs/CKM_HIGGS_Z3_UNIVERSAL_NOTE.md`). The staggered
mass operator eps(x) does not carry a well-defined Z_3 charge. Cl(3)
centrality of Gamma_5 means the mass insertion factorizes, but this says
nothing about Z_3 charge selection -- the obstruction is in the Z_3 Fourier
decomposition of the mass operator, not in its radiative corrections.

**Status: (c) No connection.** Centrality does not resolve the CKM blocker.

---

## 2. No-Continuum-Limit Theorem (from generation lane)

**Source theorem:** The Cl(3) framework has no continuum limit: (i) taking
a -> 0 sends all non-trivial taste masses to infinity, (ii) there is no
tunable bare coupling to define a Line of Constant Physics, (iii) forcing
a -> 0 gives a trivial (free, degenerate) theory, (iv) no fourth-root trick
exists in the Hamiltonian formulation.

**Source files:** `docs/GENERATION_PHYSICALITY_PAPER_NOTE.md` (Layer C),
`docs/GENERATION_AXIOM_FIRST_NOTE.md` (taste-physicality arguments)

### 2A. No-continuum-limit -> DM (g_bare = 1)

**Target lane:** DM relic mapping

**Connection:** The g_bare = 1 derivation explicitly uses the no-continuum-limit
theorem as its Axiom (3): "g does not run. It is a fixed pure number, not a
parameter to be tuned toward a continuum limit." Without this axiom, g would
be a bare coupling that runs under RG, and its lattice-scale value would be
arbitrary.

**Status: (a) Already made.** `docs/G_BARE_DERIVATION_NOTE.md` explicitly
lists "The lattice is the UV completion (no continuum limit)" as Assumption 3.
The connection is clear and used.

### 2B. No-continuum-limit -> S^3 (PL manifold)

**Target lane:** S^3 compactification

**Connection:** The PL manifold approach (`docs/S3_PL_MANIFOLD_NOTE.md`)
eliminates the discrete-to-continuum gap by arguing that the cubical complex
IS a PL 3-manifold -- no continuum limit needed. This is philosophically
aligned with the no-continuum-limit theorem: if the lattice IS the physics,
then the PL structure IS the manifold structure. The no-continuum-limit
theorem removes the motivation for seeking a smooth continuum limit
altogether.

However, the two arguments are logically independent. The PL manifold
argument works by showing the cubical complex satisfies the link condition,
which is a geometric fact about Z^3. The no-continuum-limit theorem is
about the non-existence of a Lines of Constant Physics. They complement
each other but neither implies the other.

**Status: (b) Straightforward to state the philosophical alignment.**
The paper should note that the PL approach and the no-continuum-limit theorem
are independently motivated but mutually reinforcing: the lattice has no
continuum limit (generation lane) AND it does not need one for S^3 topology
(compactification lane).

**Files:** `docs/S3_PL_MANIFOLD_NOTE.md`, `docs/S3_DISCRETE_CONTINUUM_NOTE.md`

### 2C. No-continuum-limit -> y_t (boundary condition protection)

**Target lane:** Renormalized y_t

**Connection:** The y_t boundary condition protection argument says that
y_t(M_Pl) = g_s/sqrt(6) is exact at the lattice scale. Below the lattice
scale, y_t and g_s run independently via SM RGEs. The no-continuum-limit
theorem supports this separation: the lattice scale IS the UV scale; there
is no regime above it where the relation might be modified by some
unknown UV physics.

**Status: (b) Straightforward.** The connection is implicit in
`docs/RENORMALIZED_YT_PAPER_NOTE.md` (Assumption 2: "a = l_Planck is the
unique length scale") but not explicitly stated as a consequence of the
no-continuum-limit theorem. Making this explicit would strengthen the
y_t argument by anchoring the UV boundary condition to the generation lane.

### 2D. No-continuum-limit -> Gauge coupling normalization

**Target lane:** Gauge couplings (bounded)

**Connection:** The alpha_s(M_Pl) = 0.092 value enters both the y_t and DM
lanes. The V-scheme plaquette coupling is a lattice observable, and its
identification with the physical coupling at M_Pl relies on the lattice
being physical (no continuum limit to take). If the lattice were a regulator,
alpha_plaq would be a bare coupling with no direct physical interpretation.

**Status: (b) Straightforward.** The connection is implicit but should be
stated explicitly in the gauge coupling lane.

---

## 3. Kawamoto-Smit Uniqueness (from S^3 lane)

**Source theorem:** The Kawamoto-Smit staggered fermion action on Z^d with
Cl(d) at each site is unique up to gauge freedom and an overall coupling
constant (Sharatchandra, Thun, Weisz 1981). This forces homogeneous hopping
amplitudes (translational invariance is a gauge choice, not an imported
assumption).

**Source files:** `docs/S3_GAP_CLOSURE_NOTE.md` (G1/A4 closure, Test 1),
`docs/S3_COMPACTIFICATION_PAPER_NOTE.md`

### 3A. KS uniqueness -> Generation Hamiltonian

**Target lane:** Generation physicality

**Connection:** The axiom-first note (`docs/GENERATION_AXIOM_FIRST_NOTE.md`)
discovered that the Kawamoto-Smit Gamma matrices (hopping operators with eta
phases) do NOT commute with Z_3. This is finding (vii): "eta_mu(x) =
(-1)^{sum_{nu<mu} x_nu} are direction-dependent and break the Z_3 permutation
symmetry on the off-diagonal (hopping) part of the Hamiltonian."

KS uniqueness is directly relevant here. The uniqueness theorem says the
staggered action is UNIQUE -- there is no freedom to choose a different set
of eta phases that might commute with Z_3. The Z_3 breaking on the hopping
sector is therefore a FORCED consequence of the unique KS structure, not
an artifact of a representation choice.

This means the obstruction O1 ("Z_3 is a mass-spectrum symmetry, not a full
Hamiltonian symmetry") is not a fixable gap but a structural feature of the
unique staggered action. KS uniqueness elevates this from "we chose phases
that break Z_3" to "THE unique staggered Hamiltonian breaks Z_3 on hopping."

**Status: (b) Straightforward and important.** The axiom-first note documents
the Z_3 breaking but does not cite KS uniqueness as the reason the breaking
is unavoidable. Adding this citation would sharpen the obstruction statement
significantly. The paper should say: "The Kawamoto-Smit uniqueness theorem
forces the eta-phase structure that breaks Z_3 on the hopping Hamiltonian.
Z_3 is therefore a mass-spectrum symmetry by necessity, not by choice."

**Files:** `docs/GENERATION_AXIOM_FIRST_NOTE.md` (finding vii),
`docs/S3_GAP_CLOSURE_NOTE.md` (KS uniqueness proof)

### 3B. KS uniqueness -> SU(3) canonical closure

**Target lane:** SU(3) closure

**Connection:** The SU(3) canonical closure note
(`docs/SU3_CANONICAL_CLOSURE_NOTE.md`, Step 1) states that the KS tensor
product structure C^2 x C^2 x C^2 is "canonical given the lattice
coordinates." KS uniqueness strengthens this: the tensor product structure
is not just canonical but UNIQUE -- it is the only staggered fermion
realization on Z^3. This means the entire SU(3) derivation chain
(tensor structure -> graph shifts -> quartic selector -> su(2) -> su(3))
is forced, not chosen.

**Status: (a) Already partially made.** The SU3 closure note references the
KS tensor product structure as canonical. The explicit invocation of the
UNIQUENESS theorem (not just "canonical" language) would strengthen the
argument.

### 3C. KS uniqueness -> g_bare normalization

**Target lane:** DM (g_bare = 1)

**Connection:** The g_bare = 1 derivation uses Cl(3) normalization of the
gauge connection. KS uniqueness says the hopping amplitude is fixed up to
one overall constant. This overall constant IS the gauge coupling g.
KS uniqueness therefore reduces the coupling freedom to a single parameter,
consistent with the g_bare derivation. However, KS uniqueness does not FIX
g = 1 -- it only reduces the freedom to one parameter.

**Status: (b) Straightforward supporting connection.** KS uniqueness
narrows the coupling freedom to exactly one parameter, which the Cl(3)
normalization argument then fixes to g = 1.

---

## 4. Anomaly Cancellation (from time/3+1 lane)

**Source theorem:** The spatial graph determines the left-handed gauge algebra
and matter structure. The derived temporal direction supplies chirality.
Anomaly cancellation (gravitational and gauge) then fixes the right-handed
singlet completion on the Standard Model branch.

**Source files:** `docs/RIGHT_HANDED_SECTOR_NOTE.md`,
`docs/S3_GAP_CLOSURE_NOTE.md` (G1/A4 test 2: torsional anomaly)

### 4A. Anomaly cancellation -> Generation physicality

**Target lane:** Generation physicality

**Connection:** The generation anomaly obstruction note
(`docs/GENERATION_ANOMALY_OBSTRUCTION_NOTE.md`) already uses a DIFFERENT
anomaly argument -- the 't Hooft Z_3 anomaly matching via Dai-Freed
invariants. This is a discrete anomaly (Z_3 bordism), not the continuous
gauge/gravitational anomaly used for RH matter.

The continuous anomaly cancellation used for the RH sector operates
generation-by-generation: each SM generation is anomaly-free separately.
This is a standard QFT result. The question is whether it constrains the
Cl(3) framework's generation structure.

The answer is nuanced. If the three Z_3 taste sectors are identified as
three SM generations, then anomaly cancellation requires each sector to
contain a complete anomaly-free fermion set. The 8 = (2,3)_{+1/3} +
(2,1)_{-1} structure from the commutant theorem gives ONE generation of
LH fermions. Three copies (from three Z_3 sectors) give three LH
generations. Anomaly cancellation then requires three copies of the RH
completion, which is provided by the 4D taste space (16 states split into
8_L + 8_R by gamma_5).

However, this is circular: it assumes the Z_3 sectors ARE generations
(the very thing generation physicality is trying to prove) and then checks
that anomaly cancellation is consistent.

A sharper result would be: "anomaly cancellation FORCES the Z_3 sectors
to be independent generations (not copies of the same generation)." This
would require showing that a single-generation interpretation of the 24
LH states (8 tastes x 3 sectors, treated as one generation with 24 states)
has uncancelled anomalies, while the 3-generation interpretation (each
sector is one generation of 8 states) is anomaly-free.

**Status: (c) Requires new work.** The 't Hooft Z_3 anomaly obstruction
note provides the discrete analog (merging sectors changes the anomaly
invariant). The continuous gauge anomaly version of this argument has not
been written. If it can be shown that the multi-generation interpretation
is the UNIQUE anomaly-free assignment, this would be a significant step
toward closing generation physicality.

**Files:** `docs/GENERATION_ANOMALY_OBSTRUCTION_NOTE.md` (discrete Z_3 anomaly),
`docs/RIGHT_HANDED_SECTOR_NOTE.md` (RH sector from 4D taste space)

### 4B. Anomaly cancellation -> S^3 homogeneity

**Target lane:** S^3 compactification

**Connection:** The S^3 gap closure note (`docs/S3_GAP_CLOSURE_NOTE.md`,
G1/A4 test 2) already uses anomaly cancellation to derive translational
invariance: a non-homogeneous lattice has non-zero torsion, producing a
torsional parity anomaly (Nieh-Yan invariant). The gauge sector has no
matching torsional anomaly, so anomaly cancellation requires zero torsion,
hence homogeneity.

**Status: (a) Already made.** This connection is explicitly present in the
S^3 gap closure note.

### 4C. Anomaly cancellation -> CKM

**Target lane:** CKM (bounded)

**Connection:** The CKM lane is blocked by the Higgs Z_3 charge obstruction.
Anomaly cancellation does not resolve this: the obstruction is in the Z_3
Fourier structure of the mass operator, not in anomaly matching. Anomaly
cancellation constrains the FERMION content (requires complete generations),
not the SCALAR sector (Higgs Z_3 charge).

**Status: (c) No connection to the CKM blocker.**

---

## 5. SU(3) Canonical Closure / Quartic Selector (graph-shift surface)

**Source theorem:** The quartic selector V_sel = Tr H^4 - (Tr H^2)^2/8 =
32 sum_{i<j} phi_i^2 phi_j^2 identifies axis vertices as minima, breaking
S_3 -> Z_2. This selects the weak axis, from which su(2) is determined,
and the commutant gives su(3) + u(1).

**Source files:** `docs/SU3_CANONICAL_CLOSURE_NOTE.md` (Step 3),
`docs/EWSB_GENERATION_CASCADE_NOTE.md`

### 5A. Quartic selector -> EWSB generation cascade

**Target lane:** Generation physicality (EWSB mechanism)

**Connection:** The EWSB generation cascade note
(`docs/EWSB_GENERATION_CASCADE_NOTE.md`) explicitly uses V_sel as the
symmetry-breaking potential. The cascade is:
V_sel breaks S_3 -> Z_2 (selects weak axis) -> Z_3 breaks (VEV projection
asymmetry) -> Z_2 breaks (JW structure cascade) -> three distinct masses.

This IS the quartic selector. The same object that identifies the weak axis
(and hence su(2) + su(3)) also drives the generation mass splitting. The
selector does double duty: gauge algebra emergence AND generation breaking.

**Status: (a) Already made.** The EWSB cascade note explicitly references
V_sel and the S_3 -> Z_2 breaking. The SU3 canonical closure note lists
"three generations" as NOT derived by the su(3) argument but as a separate
lane. The connection between the two (same selector drives both) is present
but could be stated more prominently.

### 5B. Quartic selector -> Generation mass hierarchy

**Target lane:** Generation physicality (Layer E: mass ratios)

**Connection:** The mass hierarchy depends on the VEV direction selected by
V_sel. The heavy generation member is the one whose taste bit is "1" in the
selected axis direction. The mass ratio m_heavy/m_light depends on the
coupling to the VEV, which is set by the selector's minimum structure.

The quartic selector has axis minima with V_sel = 0 and a democratic maximum
with V_sel = 1/3. The DEPTH of the selector potential (difference between
max and min) is 1/3, independent of any coupling. This sets the scale of
EWSB and hence the scale of the 1+2 mass splitting.

**Status: (b) Straightforward.** The connection exists implicitly in the
EWSB cascade note but the paper could make it explicit: "The same quartic
invariant that selects the gauge algebra also determines the leading mass
hierarchy."

### 5C. Quartic selector -> CKM mixing

**Target lane:** CKM (bounded)

**Connection:** The CKM matrix arises from misalignment between the mass
eigenbasis and the weak interaction eigenbasis. In the Cl(3) framework,
both are determined by the quartic selector -- the weak eigenbasis by the
selected axis, and the mass eigenbasis by the Wilson mass + radiative
corrections. CKM mixing would arise if the radiative corrections rotate
the mass eigenstates relative to the weak states.

However, the CKM lane is blocked by the Higgs Z_3 charge obstruction
(`docs/CKM_HIGGS_Z3_UNIVERSAL_NOTE.md`), which prevents the derivation
from proceeding to quantitative CKM matrix elements. The selector is
necessary but not sufficient for CKM.

**Status: (c) Requires resolution of the Higgs Z_3 blocker first.** The
quartic selector provides the structural framework for CKM (it defines the
weak axis), but the blocker prevents quantitative predictions.

---

## 6. Spectral Gap -> Vacuum Energy -> Expansion (from DM lane)

**Source theorem:** On a finite graph, the Laplacian has a spectral gap
lambda_min > 0. Identifying Lambda = 3/R^2 (lowest eigenvalue on S^3)
gives Lambda_pred = 1.59 x 10^{-52} m^{-2}, within 46% of Lambda_obs.
The positivity of the spectral gap ensures H^2 >= Lambda/3 > 0, i.e.,
expansion is forced. The 2nd law (entropy increase from node addition)
selects the expanding branch.

**Source files:** `docs/DM_RELIC_SYNTHESIS_NOTE.md` (Closure A),
`docs/COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`

### 6A. Spectral gap -> S^3 compactification (Lambda from topology)

**Target lane:** S^3 compactification

**Connection:** The cosmological constant prediction Lambda = 3/R^2
ASSUMES S^3 topology (the coefficient 3 is the first Laplacian eigenvalue
on S^3; it would be different on T^3 or RP^3). Therefore the spectral gap
argument is DOWNSTREAM of S^3 compactification, not independent of it.

However, the reverse connection is valuable: the CC scan
(`docs/S3_COMPACTIFICATION_PAPER_NOTE.md`, RP^3 refinement) shows that
S^3 gives Lambda_pred/Lambda_obs = 1.46 while T^3 gives 4.74. This is
one of the four independent T^3 exclusion arguments. The spectral gap
PLUS observed Lambda provides evidence for S^3 over T^3.

Furthermore, the RP^3 refinement (Lambda ratio = 0.92, 8% deviation)
suggests that the true topology may be S^3/Z_2 rather than S^3. This is
detectable via CMB matched-circle searches.

**Status: (a) Already made as a T^3 exclusion argument.** The CC spectral
mismatch is argument #4 in the T^3 exclusion list. The RP^3 refinement
adds a testable prediction. The reverse direction (S^3 -> Lambda) is the
CC prediction itself.

### 6B. Spectral gap -> DM freeze-out (H > 0)

**Target lane:** DM relic mapping

**Connection:** The DM synthesis note (`docs/DM_RELIC_SYNTHESIS_NOTE.md`,
Closure A) explicitly uses Lambda > 0 (from spectral gap) plus positive
energy density to prove H > 0. This eliminates "the universe expands" as
an imported assumption. The 2nd law selects the expanding branch.

**Status: (a) Already made.** This connection is explicitly present in the
DM synthesis note.

### 6C. Spectral gap -> y_t (cosmological running)

**Target lane:** Renormalized y_t

**Connection:** The y_t prediction involves running from M_Pl to M_Z via
SM RGEs. The existence of a Hubble expansion (H > 0 from spectral gap) is
not directly relevant to the running -- the RGEs are local QFT equations,
not cosmological. However, the spectral gap indirectly validates the
framework's claim that the lattice produces a universe with the right
cosmological properties, which supports the overall consistency of
identifying the lattice scale with M_Pl.

**Status: (c) No direct connection.** The spectral gap does not enter the
y_t RGE running.

---

## Summary Table

| # | Connection | Source Lane | Target Lane | Status |
|---|-----------|------------|-------------|--------|
| 1A | Cl(3) centrality does NOT protect generation masses | y_t | generation | **(b)** important negative |
| 1B | Cl(3) centrality does not simplify DM Sommerfeld | y_t | DM | **(b)** no connection |
| 1C | Cl(3) centrality does not resolve CKM blocker | y_t | CKM | **(c)** no connection |
| 2A | No-continuum-limit forces g_bare = 1 | generation | DM | **(a)** already used |
| 2B | No-continuum-limit aligns with PL manifold approach | generation | S^3 | **(b)** philosophical |
| 2C | No-continuum-limit anchors y_t UV boundary condition | generation | y_t | **(b)** implicit, make explicit |
| 2D | No-continuum-limit validates alpha_s identification | generation | gauge couplings | **(b)** implicit |
| 3A | KS uniqueness forces Z_3 breaking on hopping | S^3 | generation | **(b)** important, sharpen |
| 3B | KS uniqueness forces tensor product structure | S^3 | SU(3) | **(a)** partially made |
| 3C | KS uniqueness narrows coupling to one parameter | S^3 | DM | **(b)** supporting |
| 4A | Anomaly -> generation physicality (continuous) | time/3+1 | generation | **(c)** requires new work |
| 4B | Anomaly -> S^3 homogeneity | time/3+1 | S^3 | **(a)** already made |
| 4C | Anomaly -> CKM | time/3+1 | CKM | **(c)** no connection |
| 5A | Quartic selector drives EWSB cascade | SU(3) | generation | **(a)** already made |
| 5B | Quartic selector sets mass hierarchy scale | SU(3) | generation | **(b)** make explicit |
| 5C | Quartic selector needed for CKM but blocked | SU(3) | CKM | **(c)** blocked by Z_3 |
| 6A | Spectral gap supports S^3 over T^3 | DM | S^3 | **(a)** already used |
| 6B | Spectral gap gives H > 0 for freeze-out | DM | DM | **(a)** already used |
| 6C | Spectral gap does not enter y_t running | DM | y_t | **(c)** no connection |

---

## Priority Actions

### High-value connections to formalize (status (b), important):

1. **3A: KS uniqueness -> Z_3 hopping obstruction.** Add to
   `docs/GENERATION_AXIOM_FIRST_NOTE.md` an explicit statement that
   KS uniqueness makes the Z_3 breaking on hopping FORCED, not a
   representation artifact. This elevates obstruction O1 from "the
   phases happen to break Z_3" to "the unique staggered action
   necessarily breaks Z_3."

2. **1A: Cl(3) centrality does NOT protect generation masses.** Add to
   `docs/EWSB_GENERATION_CASCADE_NOTE.md` or the generation paper note
   an explicit statement that centrality protects y_t but not the
   generation mass matrix, and explain why this is consistent (the
   hierarchy IS radiative).

3. **2C: No-continuum-limit -> y_t boundary condition.** Add to
   `docs/RENORMALIZED_YT_PAPER_NOTE.md` an explicit citation of the
   no-continuum-limit theorem as the reason the UV boundary condition
   is the physical boundary condition (not an intermediate bare value).

### Highest-value new-work connection:

4. **4A: Continuous anomaly cancellation -> generation physicality.**
   If one can show that the 3-generation interpretation of the 24 LH
   taste states is the UNIQUE anomaly-free assignment (while a
   single-generation interpretation of 24 states has uncancelled
   anomalies), this would be a significant advance toward closing
   generation physicality. This is the most promising cross-lane
   theorem that requires genuine new work.
