# CKM Gate: Elegant Mathematical Approaches

**Date:** 2026-04-13
**Type:** Theoretical brainstorm (no computation)
**Goal:** Identify a proof-level route to the CKM matrix from Cl(3)

---

## Current State of Play

The compute-driven program has achieved:
- V_us to 0.3% (from Z_3 lattice overlap, effectively the Cabibbo angle)
- V_cb to 4.6% (multi-L mean K, no calibration)
- V_ub to 18% (sector-dependent FN fit, not derived)
- J/J_PDG = 0.73 (Higgs Z_3^3 charge, no fitting, 27% gap)

Three structural tensions block closure:
1. K (the S_23 matching constant) is sector-dependent: K_12 and K_23 differ
2. c_13 is a factor of 15 off at physical y_v (lattice gives ~1, need ~0.02)
3. J requires an asymmetric phase split from EWSB that is fitted, not derived

The compute approach (larger lattices, more matching parameters) can improve
numerics but does not resolve these tensions at the structural level. What
follows are five mathematical approaches that might.

---

## Approach 1: CKM as Deformed Z_3 Fourier Transform

### The Idea

The three generations are Z_3 eigenstates {1, omega, omega^2}. The mass
basis and weak basis are related by a change of basis on Z_3. In the
discrete Fourier analysis of a cyclic group, the canonical transform is
the DFT matrix:

    F_3 = (1/sqrt{3}) [[1,1,1],[1,omega,omega^2],[1,omega^2,omega^4]]

This is maximally democratic: all off-diagonal elements have equal magnitude.
The physical CKM is close to the identity (near-diagonal). So the CKM is
NOT F_3 --- it is a deformed DFT where EWSB breaks the Z_3 democracy.

### What This Buys

The deformation has a natural expansion parameter. If EWSB selects direction
1 with strength v, the Z_3 symmetry is broken to Z_2 (residual swap of
directions 2,3). The deformation of F_3 can be written as:

    V_CKM = exp(-epsilon * H) * F_3

where H is the Z_3-breaking Hamiltonian and epsilon = v_color/v_weak encodes
the EWSB hierarchy. The key claim: epsilon IS lambda (the Wolfenstein
parameter). Then the Wolfenstein expansion is literally the Taylor expansion
of the deformed DFT.

### What's Proved

- Z_3 is the generation symmetry on the taste lattice (established)
- EWSB breaks S_3 -> Z_2 -> trivial (EWSB_GENERATION_CASCADE_NOTE)
- F_3 diagonalizes the Z_3 regular representation (textbook)
- The mass basis differs from the Z_3 eigenbasis (follows from EWSB)

### What's Missing

- The identification epsilon = lambda = 0.224. This requires computing the
  ratio v_color/v_weak from the Coleman-Weinberg potential, which currently
  gives order-of-magnitude but not 3-digit precision.
- The generator H of the deformation. The EWSB cascade gives 1+2 splitting
  but the specific form of H (which generates a near-identity rather than
  a near-democratic matrix) has not been derived.
- The phase. F_3 already contains complex entries (omega), but the physical
  CKM phase delta ~ 68.5 deg is not simply related to arg(omega) = 120 deg.

### The Elegant Proof Would Be

**Theorem:** Let G = Z_3 act on the 3-cube taste lattice. Let V(phi) be the
Coleman-Weinberg potential with EWSB minimum phi_0 = (v,0,0). Then the
unitary matrix diagonalizing the Yukawa operator Y = y * v * Gamma_1 in
the mass basis is:

    V = F_3 * diag(1, e^{-i*alpha}, e^{-2i*alpha}) + O(epsilon^2)

where alpha = (2pi/3)(1 - epsilon) and epsilon = g^2/(16pi^2) * log(M_Pl/v).

This would give V_us = sin(pi/3 - epsilon*pi/3) ~ (sqrt{3}/2)(1 - epsilon^2/2)
and determine all four CKM parameters from one number.

### Feasibility: MEDIUM

The conceptual framework is clean but the quantitative connection
(epsilon = lambda) is not sharp. The approach is most likely to succeed
as a structural explanation of WHY the CKM is near-diagonal, rather than
as a precision derivation.

---

## Approach 2: Wolfenstein Lambda from EWSB Ratio

### The Idea

The Wolfenstein parametrization expands V_CKM in powers of lambda = 0.2243.
This is the sine of the Cabibbo angle. All four CKM parameters are expressed
in terms of (lambda, A, rho, eta).

Claim: lambda is the ratio of two EWSB scales:

    lambda = v_color / v_weak

where v_weak is the VEV in the selected (weak) direction and v_color is
the residual condensate in the color directions. The selector potential
V_sel breaks S_3 -> Z_2 and determines this ratio.

### What This Buys

If lambda is fixed by the EWSB structure, then:
- V_us = lambda = 0.224 (the Cabibbo angle, already derived)
- V_cb = A * lambda^2 where A ~ O(1) is determined by the Z_2 -> trivial
  breaking (the JW cascade)
- V_ub = A * lambda^3 * sqrt(rho^2 + eta^2) where (rho, eta) encode the
  Z_3 phase

The entire Wolfenstein expansion becomes a DERIVATIVE of the EWSB cascade:
- O(lambda^1): Cabibbo from Z_3 -> Z_2 (first breaking step)
- O(lambda^2): V_cb from Z_2 -> trivial (second breaking step)
- O(lambda^3): V_ub from the CP phase (geometric, third step)

### What's Proved

- Lambda = 0.224 is derived from the Z_3 lattice overlap (V_us gate: closed)
- The EWSB cascade gives S_3 -> Z_2 -> trivial (EWSB_GENERATION_CASCADE)
- The JW string structure breaks the residual Z_2 (bounded)

### What's Missing

- A (the Wolfenstein A parameter) from first principles. Currently A = 0.821
  is fitted. The NNI overlap ratio c_23^u/c_23^d gives the UP/DOWN
  asymmetry but not the absolute scale.
- The connection lambda = v_color/v_weak. The CW potential determines the
  ratio of Hessian eigenvalues (64v^2 for the massive modes, 0 for the
  Goldstone) but the effective ratio of condensates is not the ratio of
  eigenvalues --- it requires a careful 1-loop computation.
- (rho, eta) from the Z_3 phase. Currently rho and eta are not independently
  derived.

### The Elegant Proof Would Be

**Theorem:** The Wolfenstein A parameter equals the ratio of the two
Z_2-breaking radiative corrections:

    A = delta_m(JW=1) / delta_m(JW=0) = (1 + beta) / 1

where beta = alpha_s / (4pi) * C_F * n_JW is the JW-dependent taste-breaking
coefficient. With alpha_s(M_Pl) ~ 0.02 and C_F = 4/3, this gives
A ~ 1 + 0.008 ~ 1, which is close to the PDG A = 0.821 but not precise.

More promising: A = c_23/c_12 where c_12 and c_23 are the NNI coefficients
from the two independent Z_3 orbit transitions. If the overlap integrals
factorize as c_{ij} ~ epsilon^{|q_i - q_j|} with FN charges, then
A = epsilon^{Dq_23 - Dq_12} / lambda^2. The FN charges must be derived
from the Z_3^3 structure.

### Feasibility: MEDIUM-HIGH

This is the most direct route. The missing piece (A from Z_3 structure) is
a specific, well-posed mathematical question: compute the ratio of two
overlap integrals on the Z_3 orbifold. It does not require new conceptual
machinery, just careful analysis of the existing lattice structure.

---

## Approach 3: CP Phase from the Z_3 Orbifold Volume

### The Idea

The CP-violating phase delta is geometrically the area of the unitarity
triangle. On the taste lattice, the Z_3 action defines a discrete orbifold.
This orbifold has a natural geometric phase: the Berry phase acquired by
a Z_3 eigenstate transported around the orbifold.

On a discrete orbifold C^3 / Z_3, the geometric phase is:

    phi_Berry = (2pi/3) * (q_1 + q_2 + q_3) mod 2pi

where (q_1, q_2, q_3) are the Z_3 charges. For the Higgs embedding
q_H = (2,1,1), the total charge is 4 mod 3 = 1, giving phi = 2pi/3 = 120 deg.

The physical CKM phase is delta ~ 68.5 deg = 1.196 rad. The ratio
delta / phi_Berry = 0.571. This is NOT a simple fraction, which suggests
that the physical phase is not the bare Berry phase but its projection
through the mass hierarchy.

### What This Buys

A purely topological derivation of the CP phase source. The Berry phase
2pi/3 is the Z_3 analog of the pi phase in Z_2 (which gives parity).
The factor 0.571 by which the physical phase is reduced from the Berry
phase is determined by the mass hierarchy: it is the same suppression
factor S = 0.41 identified in CKM_J_DERIVED_NOTE (Attack 1), modulated
by the angle dependence.

### What's Proved

- q_H = (2,1,1) from the T_1-T_2 bilinear (derived)
- The Berry phase of Z_3 on C^3 is 2pi/3 for total charge 1 mod 3 (textbook)
- The suppression from mass hierarchy gives S ~ 0.41 (computed, Attack 1)
- J/J_PDG = 0.73 with single-phase NNI using this Berry phase (computed)

### What's Missing

- The reduction delta_physical / delta_Berry = 0.571. This is currently
  a numerical output of the NNI diagonalization, not a derived quantity.
  An analytic formula for this ratio in terms of mass ratios would close
  the phase.
- The distinction between the Berry phase (a property of the Z_3 action)
  and the CKM phase (a property of the Yukawa diagonalization). These
  are related but not identical, and the precise map between them goes
  through the full 3x3 NNI structure.

### The Elegant Proof Would Be

**Lemma:** For a 3x3 NNI matrix with Z_3 phase phi in the (1,3) entry,
the physical CKM phase is:

    delta = phi * f(r_u, r_d)

where r_u = m_u/m_t, r_d = m_d/m_b are the first/third generation mass
ratios, and f is a known function satisfying f -> 1 as r -> 0 (decoupling
limit) and f -> 0 as r -> 1 (degenerate limit).

If f(r_u, r_d) can be evaluated analytically in terms of quark mass ratios,
and if these mass ratios are themselves derived from the EWSB cascade
(Approach 2), then the CKM phase is fully determined by the Z_3 Berry phase
and the mass hierarchy.

### Feasibility: MEDIUM

The topological origin is solid but the reduction factor f is the hard part.
The NNI diagonalization can be done analytically in the 2x2 block case
(giving the well-known sqrt{m_i/m_j} formulas) but the 3x3 case with
complex off-diagonal entries does not have a clean closed form. A
perturbative expansion in the small mass ratios may suffice.

---

## Approach 4: Jarlskog from the Z_3 Volume Form

### The Idea

The Jarlskog invariant J = Im(V_us V_cb V*_ub V*_cs) is the unique
CP-violation measure. It is a single real number. On the Z_3 orbifold,
there is a natural 3-form:

    Omega = omega_1 ^ omega_2 ^ omega_3

where omega_i are the dual 1-forms to the Z_3 generators. The integral
of Omega over the taste space is a topological invariant of the orbifold.

Claim: J is proportional to the integral of Omega, with a proportionality
constant determined by the mass spectrum.

### What This Buys

A direct computation of J without going through individual V_ij elements.
This would bypass the J-V_ub tension entirely: instead of computing V_ub
and then extracting J (which requires both |V_ub| and delta to be precise),
J would be computed as a single topological integral.

The key formula would be:

    J = (1/N) * integral_T Omega * det(M_u)^{-1/3} * det(M_d)^{-1/3}

where T is the taste space, N is a normalization, and the mass determinants
provide the correct dimensionful scaling.

### What's Proved

- J is a rephasing-invariant of the CKM matrix (textbook)
- J is proportional to the product of all mass differences:
  J ~ prod_{i>j}(m_ui^2 - m_uj^2) * prod_{i>j}(m_di^2 - m_dj^2) / v^12
  times a function of mixing angles (Jarlskog's original formula)
- The Z_3 structure provides the CP source (established)
- The volume of Z_3 on the 3-cube is well-defined (3 elements, discrete)

### What's Missing

This is the most speculative approach. The connection between the discrete
3-form on Z_3 and the continuous Jarlskog invariant is not established.
The key difficulty: Omega on the discrete orbifold is a combinatorial
quantity (essentially just the group determinant of Z_3, which equals
3*sqrt{3}*i), while J depends on continuous parameters (the mass ratios).

The approach requires a bridge between the discrete (topological) and
continuous (spectral) aspects of the theory. This bridge might exist
through the heat kernel on the orbifold: the short-time expansion of
Tr(exp(-t*D^2)) on C^3/Z_3 contains both the topological data (Euler
character, index) and the spectral data (mass eigenvalues). If J appears
as a specific coefficient in this expansion, the connection is established.

### The Elegant Proof Would Be

**Theorem:** Let D be the Dirac operator on the Z_3 orbifold with Yukawa
mass insertions. Then the eta-invariant of D equals:

    eta(D) = 2 * J / (m_t^2 * m_b^2)

This would relate J to the index theory of the orbifold Dirac operator,
making the CP phase a spectral invariant rather than a fitting target.

### Feasibility: LOW-MEDIUM

Beautiful if true, but the mathematical machinery (eta-invariants of
discrete orbifold Dirac operators) is heavy and the connection to the
physical Jarlskog invariant is not obvious. This is a high-risk,
high-reward direction. It would be most productive as a theoretical
investigation rather than a computational project.

---

## Approach 5: Hierarchy from EWSB Cascade without Lattice Computation

### The Idea

The three CKM mixing angles satisfy theta_12 >> theta_23 >> theta_13.
This hierarchy mirrors the EWSB cascade: S_3 -> Z_2 -> trivial breaks
in two steps, and each step generates one mixing angle.

- Step 1 (S_3 -> Z_2): distinguishes the weak direction from the two
  color directions. This generates the Cabibbo angle theta_12 because
  it creates a large overlap between the first two mass eigenstates.

- Step 2 (Z_2 -> trivial): distinguishes the two color directions via
  JW strings. This generates theta_23 because it creates a smaller
  overlap between the second and third mass eigenstates.

- Step 3 (CP phase): the phase mismatch between up and down sectors
  generates theta_13 as a higher-order cross-coupling.

The hierarchy theta_12 >> theta_23 >> theta_13 then follows from the
ALGEBRAIC structure of the symmetry breaking chain, not from numerical
computation of overlap integrals.

### What This Buys

A PROOF that the CKM hierarchy exists, independent of lattice numerics.
The argument would be:

1. The first breaking (S_3 -> Z_2) is driven by the CW potential, which
   is O(g^2). This gives theta_12 ~ g ~ 0.5 (rough).

2. The second breaking (Z_2 -> trivial) is driven by JW taste-breaking,
   which is O(g^2 * a^2). This gives theta_23 ~ g * a ~ g^2/(4pi) ~ 0.01.

3. The third effect (CP cross-coupling) involves both breakings simultaneously,
   giving theta_13 ~ theta_12 * theta_23 ~ g^3 ~ 0.004.

The parametric scaling theta_12 : theta_23 : theta_13 ~ 1 : epsilon : epsilon^2
with epsilon = g^2/(16pi^2) would be derived from the COUNTING of loop
factors in the symmetry breaking chain.

### What's Proved

- The EWSB cascade S_3 -> Z_2 -> trivial is established
  (EWSB_GENERATION_CASCADE_NOTE)
- The first step is O(g^2) from the CW potential (proved)
- The second step involves JW strings (bounded)
- The hierarchy |V_us| > |V_cb| > |V_ub| exists in the framework
  (observed numerically)

### What's Missing

- The quantitative connection between the symmetry-breaking order and
  the mixing angle magnitude. The argument "first breaking gives large
  angle, second gives small angle" is plausible but not proved.

- The key subtlety: the CKM matrix mixes the UP and DOWN sectors, each
  of which has its own EWSB structure. The mixing angles depend on the
  DIFFERENCE between the up and down diagonalization matrices, not on
  either one alone. This means the hierarchy argument must work at the
  level of the difference V = U_u^dagger * U_d, not at the level of U_u
  or U_d individually.

- The specific role of quark masses. The observed hierarchy correlates
  with mass ratios: |V_us| ~ sqrt(m_d/m_s), |V_cb| ~ m_s/m_b,
  |V_ub| ~ sqrt(m_u/m_b). These mass-ratio relations are properties of
  the NNI texture, but deriving the NNI texture FROM the EWSB cascade
  requires showing that the cascade generates nearest-neighbor couplings
  with the right coefficients.

### The Elegant Proof Would Be

**Theorem:** Let the Yukawa matrix Y be generated by the EWSB cascade on
the Z_3 orbifold with CW potential V. Then Y has NNI form (only nearest-
neighbor entries nonzero in the Z_3 basis) and the off-diagonal entries
satisfy:

    |Y_{12}| / |Y_{23}| = (g_weak / g_color) * (loop factor)

where the loop factor is determined by the number of JW strings
connecting the relevant BZ corners. This ratio equals lambda = 0.224
at 1-loop in the EWSB-improved perturbation theory.

### Feasibility: HIGH

This is the most promising direction because it asks a well-defined
question (why does the EWSB cascade generate the observed hierarchy?)
that has a natural answer (the cascade proceeds in two steps of
decreasing magnitude). The proof requires:

1. Show that the CW potential generates NNI texture (not general 3x3)
2. Show that the NNI coefficients scale with the symmetry-breaking order
3. Compute the ratio of adjacent off-diagonal entries at 1-loop

Each of these is a concrete, finite calculation. The result would be a
structural theorem: "The CKM hierarchy is a necessary consequence of the
EWSB cascade on the Z_3 taste orbifold."

---

## Ranking by Likelihood of Success

| Rank | Approach | Feasibility | What It Closes | Key Obstacle |
|------|----------|-------------|----------------|--------------|
| 1 | **5: EWSB Cascade Hierarchy** | HIGH | The hierarchy theta_12 >> theta_23 >> theta_13 | NNI texture from CW potential |
| 2 | **2: Wolfenstein from EWSB** | MEDIUM-HIGH | lambda + A (two of four params) | A from Z_3 overlap ratio |
| 3 | **1: Deformed DFT** | MEDIUM | Structural understanding | Quantitative epsilon = lambda |
| 4 | **3: Berry Phase** | MEDIUM | The CP phase source | Reduction factor f(mass ratios) |
| 5 | **4: Volume Form** | LOW-MEDIUM | J directly | Mathematical machinery gap |

## Recommended Strategy

The approaches are not mutually exclusive. The recommended attack order:

**Phase 1 (immediate):** Pursue Approach 5 (EWSB cascade hierarchy).
This is the most concrete: show that the CW potential on the 3-cube
generates NNI texture with the right scaling. The calculation is finite
and well-defined. Success gives the hierarchy without lattice computation.

**Phase 2 (if Phase 1 succeeds):** Combine with Approach 2 (Wolfenstein
from EWSB) to pin the absolute scale. With the hierarchy proved and
lambda derived, the remaining freedom is A and (rho, eta). Use the
Z_3 overlap integral analysis to determine A.

**Phase 3 (for the phase):** Use Approach 3 (Berry phase) to handle
the CP sector. The Berry phase 2pi/3 is already derived; the remaining
task is the analytic reduction factor. This can be done perturbatively
in the small mass ratios.

**Long-term (theoretical):** Investigate Approach 4 (volume form) as a
unifying perspective. Even if it does not yield a sharper numerical
prediction, the connection between J and orbifold topology would be a
deep structural result.

---

## The One-Line Version

If there is an elegant route to the CKM, it is this: **the Wolfenstein
expansion IS the EWSB cascade, with lambda = epsilon(S_3 -> Z_2),
A = epsilon(Z_2 -> 1), and (rho, eta) = the Z_3 Berry phase projected
through the mass hierarchy.** Proving this requires three finite
calculations, not an infinite lattice extrapolation.
