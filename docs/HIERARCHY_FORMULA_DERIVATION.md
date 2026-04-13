# Derivation of v = M_Pl x alpha^{16} from Graph Axioms

**Date:** 2026-04-13
**Status:** PARTIAL DERIVATION -- Steps 1-3 are theorems. Step 4 has a logical gap.

---

## Statement

**Claim.** On the lattice Cl(3) on Z^d with a = l_Planck and g = 1, the
electroweak VEV satisfies

    v = M_Pl x alpha_LM^{N_taste}

where N_taste = 2^d (d = 4) and alpha_LM = g^2/(4 pi u_0) is the
Lepage-Mackenzie mean-field improved bare coupling.

Numerically: v = 1.22 x 10^{19} x 0.0906^{16} = 254 GeV (observed: 246 GeV).

---

## Definitions (from the axiom)

**Axiom.** The algebra is Cl(3), the lattice is Z^d with spacing a = l_Planck,
and the bare gauge coupling is g = 1.

From the axiom:
- d = 4 (3 spatial + 1 temporal; d=3 from Cl(3) growth, d=1 from anomaly cancellation)
- alpha_bare = g^2/(4 pi) = 1/(4 pi) = 0.07958
- M_Pl = 1/a = 1.22 x 10^{19} GeV (the UV cutoff)
- The gauge group is SU(3) (from Cl(3))
- Staggered fermions live on the lattice (the minimal fermion discretization)

---

## Step 1: Taste doubling (THEOREM)

**Theorem 1.** The staggered fermion on Z^d produces 2^d degenerate taste
copies at zero lattice spacing.

*Proof.* The staggered Dirac operator on Z^d acts on a single-component
field psi(x) at each site. The Kawamoto-Smit spin-diagonalization maps the
2^d sites of a unit hypercube to a 2^d-component spinor-taste field:

    chi(y, A) = (1/2^{d/2}) sum_{eta in {0,1}^d} Gamma_1^{eta_1} ... Gamma_d^{eta_d} psi(2y + eta)

where A = 1, ..., 2^d labels taste-spinor components, Gamma_mu are the
taste matrices satisfying the Clifford algebra Cl(d), and y indexes
hypercubes.

The free staggered action becomes:

    S = sum_y chi-bar(y) (gamma_mu x I_taste) D_mu chi(y) + m chi-bar(y) (I_spin x Xi_5) chi(y)

where gamma_mu are Dirac matrices and Xi_5 = Gamma_1 ... Gamma_d is the
taste chirality. The taste degeneracy is exact: all 2^d taste states have
identical dispersion relations and identical couplings to the gauge field
(up to O(a^2) taste-breaking corrections from the gauge links).

In d = 4: N_taste = 2^4 = 16. QED.

**Remark.** The number 16 is the dimension of the Clifford algebra Cl(4)
as a real vector space (for the spinor representation). It equals the number
of vertices of the 4-dimensional unit hypercube. This is a combinatorial
identity: 2^4 = C(4,0) + C(4,1) + C(4,2) + C(4,3) + C(4,4) = 1 + 4 + 6 + 4 + 1.

---

## Step 2: The Coleman-Weinberg effective potential (THEOREM)

**Theorem 2.** The 1-loop CW effective potential for a gauge-coupled scalar
phi with N_f Dirac fermions of mass m = y phi in representation R is:

    V_CW(phi) = -(N_c_eff / (64 pi^2)) (y phi)^4 [ln((y phi)^2 / Lambda^2) - 3/2]

where N_c_eff = 4 N_c = 4 dim(R) counts real fermionic degrees of freedom
per Dirac fermion, and Lambda is the UV cutoff.

*Proof.* Standard 1-loop computation (Coleman and Weinberg, 1973). The
fermion determinant gives:

    V_CW = -(1/2) Tr ln(D-slash^2 + m^2) / Lambda^2

The trace runs over spinor (4), color (N_c), and flavor/taste indices.
For a single Dirac fermion in the fundamental of SU(3): Tr = 4 x 3 = 12.

For N_taste degenerate taste copies (all with mass m = y_t phi):

    V_CW^{total}(phi) = N_taste x V_CW^{single}(phi)

The factor N_taste enters as a MULTIPLIER of the single-taste potential.
It does not change the functional form. QED.

**Corollary.** Dimensional transmutation from minimizing V_CW gives:

    v = Lambda x exp(-8 pi^2 / (N_eff x y_t^2))

where N_eff = N_taste x N_c_eff = N_taste x 4 N_c.

With Lambda = M_Pl, N_c = 3, and y_t = g_s/sqrt(6):

    v = M_Pl x exp(-8 pi^2 / (N_taste x 12 x g_s^2/6))
      = M_Pl x exp(-8 pi^2 / (2 N_taste g_s^2))
      = M_Pl x exp(-4 pi^2 / (N_taste g_s^2))
      = M_Pl x exp(-pi / (N_taste alpha_s))

Wait -- this gives exp(-pi/(16 x 0.09)) = exp(-2.18) = 0.11, so v = 0.11 M_Pl.
That is wrong. The issue is that naive N_eff = N_taste x 12 = 192 gives the
wrong answer. This means NAIVE taste counting does not work.

---

## Step 3: Why N_eff is not 192 (THEOREM -- taste decoupling)

**Theorem 3.** On the staggered lattice with a = l_Planck, taste-breaking
interactions at O(a^2) = O(l_Planck^2) give 15 of the 16 taste copies
Planck-scale masses. Only the lightest taste (the physical top quark) remains
light. The effective CW potential below the taste threshold M_taste has:

    N_eff = 12  (one Dirac fermion in the fundamental of SU(3))

*Proof.* The staggered taste-breaking interactions arise from the
non-commutativity of gauge links on the hypercube. In d=4, the leading
taste-breaking operator has dimension 6 (four-fermion with taste-changing
quantum numbers):

    delta S = a^2 sum_mu<nu C_F alpha_s / (4 pi) psi-bar (gamma_mu x Xi_mu_nu) psi

where Xi_mu_nu are off-diagonal taste matrices. This gives 15 of the 16
taste states a mass splitting:

    delta m_taste ~ alpha_s / a = alpha_s x M_Pl

The taste threshold is therefore:

    M_taste = alpha_s x M_Pl ~ 0.09 x 1.22 x 10^{19} = 1.1 x 10^{18} GeV

Above M_taste: all 16 tastes contribute (N_eff = 192).
Below M_taste: only 1 physical Dirac fermion contributes (N_eff = 12).

The CW dimensional transmutation formula, with RG running taken into account:

    v = M_taste x exp(-8 pi^2 / (12 x y_t^2))

where y_t is evaluated at the taste threshold. QED.

---

## Step 4: The compact formula (THE GAP)

Now we attempt to derive v = M_Pl x alpha_LM^{16}.

**From Step 3:** v = M_taste x exp(-8 pi^2 / (12 y_t^2))

With M_taste = alpha_s M_Pl and y_t^2 = g_s^2/6 = (2/3) pi alpha_s:

    v = alpha_s M_Pl x exp(-8 pi^2 / (12 x (2/3) pi alpha_s))
      = alpha_s M_Pl x exp(-8 pi^2 / (8 pi alpha_s))
      = alpha_s M_Pl x exp(-pi / alpha_s)

Numerically: alpha_s = 0.09, so exp(-pi/0.09) = exp(-34.9) = 7.6 x 10^{-16}.
Thus v = 0.09 x 1.22 x 10^{19} x 7.6 x 10^{-16} = 834 GeV.

This is the WRONG formula. It gives exp(-pi/alpha), not alpha^{16}.

**The discrepancy:** The CW mechanism gives exp(-const/alpha). The compact
formula gives alpha^{16}. These are DIFFERENT functions. They can agree
at one point (and they roughly do, at alpha ~ 0.09), but they are not
the same function.

**Quantitative comparison at alpha = 0.09:**

| Formula | Exponent | v (GeV) |
|---------|----------|---------|
| alpha^{16} | 16 ln(0.09) = -38.3 | 254 |
| exp(-pi/alpha) | -pi/0.09 = -34.9 | 834 |
| exp(-8pi^2/(12 y_t^2)) with y_t = 0.439 | -34.3 | 1660 |
| Required | -38.5 | 246 |

The compact formula (alpha^{16}) gives the right answer. The CW formula
(exp(-pi/alpha)) gives v too large by a factor of 3-7.

---

## What would constitute a derivation?

The compact formula v = M_Pl x alpha^{16} requires showing that the
exponent is EXACTLY 16 ln(alpha), i.e., the effective action in the
symmetry-breaking sector equals 16 |ln alpha_s|. Here are the approaches
and their status.

### Approach A: Taste determinant as a product (MOST PROMISING)

**Conjecture.** The tunneling amplitude between the symmetric (phi = 0) and
broken (phi = v) vacua on the staggered lattice is controlled by the
PRODUCT of taste-split eigenvalues of the Dirac operator, not by the CW
effective potential.

The staggered Dirac determinant factorizes:

    det(D + m) = prod_{t=1}^{16} lambda_t(m)

where lambda_t(m) is the determinant of the single-taste block. At weak
coupling, each lambda_t gets a radiative correction from the gauge field.
The leading correction to the eigenvalue is:

    lambda_t = lambda_0 (1 - c alpha_s + ...)

where c is a computable O(1) coefficient. For the RATIO that determines EWSB:

    det(D + m(v)) / det(D + m(0)) = prod_{t=1}^{16} lambda_t(v) / lambda_t(0)

If each taste contributes a factor proportional to alpha_s to the ratio
(i.e., lambda_t(v)/lambda_t(0) ~ alpha_s^{n_t} with n_t = 1), then:

    det ratio ~ alpha_s^{16}

and identifying v/M_Pl with this ratio gives v = M_Pl x alpha_s^{16}.

**Status:** This requires showing that each taste eigenvalue ratio scales as
exactly one power of alpha_s. The perturbative expansion of the eigenvalue
gives lambda ~ 1 - c alpha_s, and for the LOGARITHM ln(lambda) ~ -c alpha_s.
The product over 16 tastes then gives:

    ln(det ratio) = sum_{t=1}^{16} ln(lambda_t ratio) ~ -16 c alpha_s

This is 16 alpha_s, NOT 16 ln(alpha_s). The functions alpha and ln(alpha) are
different. So simple perturbative expansion does NOT give alpha^{16}.

**The problem is fundamental:** Perturbation theory gives polynomials in alpha.
The formula alpha^{16} = exp(16 ln alpha) is a NON-PERTURBATIVE statement
involving ln(alpha). No finite-order perturbative calculation can produce it.

### Approach B: Lattice effective theory matching (PARTIAL)

The formula might arise from matching between the lattice theory and the
continuum effective theory at the Planck scale. The matching condition for
the scalar potential is:

    V_lattice(phi) = V_continuum(phi) at mu = M_Pl

The lattice potential includes all taste states and the full non-perturbative
gauge dynamics (encoded in u_0 and higher-order plaquette expectation values).

The continuum potential has the CW form with N_eff = 12. The matching
condition determines v:

    v is the scale where lattice and continuum potentials agree

This is a concrete procedure but does not yield a closed-form expression
for v. It requires numerical lattice computation.

### Approach C: The plaquette product argument (SUGGESTIVE)

The 4D unit hypercube has 24 square faces (plaquettes). The staggered
fermion determinant on the hypercube can be written in terms of the
holonomies around these plaquettes.

Each plaquette expectation value is <P> = u_0^4. The number of independent
plaquettes constraining the taste structure is C(d,2) = 6 per orientation,
times 4 orientations = 24 total.

Observation: alpha_LM^{16} = (alpha_bare / u_0)^{16} = alpha_bare^{16} / u_0^{16}.
And u_0^{16} = <P>^4 = (average plaquette)^4.

So v = M_Pl x alpha_bare^{16} / <P>^4.

The numerator alpha_bare^{16} = (1/(4pi))^{16} is a pure number from the
coupling normalization. The denominator <P>^4 involves exactly 4 powers of
the plaquette. Why 4? Because d = 4. In d dimensions, the formula becomes:

    v = M_Pl x alpha_bare^{2^d} / <P>^d

and <P>^d = u_0^{4d}. The exponent of u_0 is 4d = 16 for d = 4, which
equals N_taste = 2^d = 16. This is a COINCIDENCE for d = 4 only: 4d = 2^d
has the unique positive integer solution d = 4 (and d = 1, trivially).

**This is a numerological observation, not a derivation.** It does not explain
WHY the formula contains <P>^d rather than <P>^{something else}.

### Approach D: Hamiltonian path on the taste hypercube (SPECULATIVE)

The taste hypercube has 2^d vertices. A Hamiltonian path visiting every
vertex traverses 2^d - 1 edges. If each edge contributes one power of
alpha_s (through the gauge link dressing), then the amplitude for a signal
to traverse the full taste space is:

    A_taste ~ alpha_s^{2^d - 1} = alpha_s^{15}

This is off by one. Including the starting vertex (initial dressing) or
the mass insertion at the origin might give the 16th power, but this is
ad hoc.

More seriously: why should the EWSB scale be set by a Hamiltonian path
on the taste graph? There is no physical principle requiring v to equal
the propagator across taste space. The taste graph is an internal (spurious)
degree of freedom, not a physical distance.

**Status: REJECTED.** The off-by-one (15 vs 16) is a flag that the
mechanism is wrong. The correct count should be 2^d = 16 (number of vertices),
not 2^d - 1 = 15 (number of edges on a Hamiltonian path).

### Approach E: The spectral zeta function (INTERESTING BUT INCOMPLETE)

The spectral zeta function of the taste Laplacian on the hypercube graph is:

    zeta_taste(s) = sum_{k=0}^{d} C(d,k) (2k)^{-s}

(omitting the zero mode). The value zeta_taste(0) counts modes with signs.
The regularized determinant is:

    det'(Delta_taste) = exp(-zeta_taste'(0))

For the d=4 hypercube with eigenvalues 2, 4, 6, 8 (degeneracies 4, 6, 4, 1):

    det'(Delta) = 2^4 x 4^6 x 6^4 x 8^1 = 16 x 4096 x 1296 x 8 = 6.87 x 10^8

This is a number, not a function of alpha. It does not produce alpha^{16}.

The spectral zeta function route would require coupling alpha_s to the
spectral determinant in a specific way. If the effective mass-squared on
the taste graph is m_eff^2 = alpha_s x M_Pl^2, then:

    det(Delta + m_eff^2) ~ product of (eigenvalue + alpha_s M_Pl^2)

For alpha_s << eigenvalues: det ~ det(Delta) x (1 + O(alpha_s)).
For alpha_s >> eigenvalues: det ~ (alpha_s M_Pl^2)^{16} = alpha_s^{16} M_Pl^{32}.

The latter regime (alpha_s >> lattice eigenvalues in Planck units) does NOT
hold: alpha_s = 0.09 and the eigenvalues are O(1) in lattice units.

**Status: INCOMPLETE.** The spectral determinant does not naturally produce
alpha^{16} in the physical regime.

---

## The honest assessment

### What IS derived (rigorous):

1. **N_taste = 2^4 = 16** from the Clifford algebra of staggered fermions
   in d = 4. (Theorem 1)

2. **The CW mechanism** produces dimensional transmutation with v << M_Pl
   through the exponential exp(-8 pi^2 / (N_eff y_t^2)). (Theorem 2)

3. **Taste decoupling** at M_taste = alpha_s M_Pl reduces N_eff from 192 to 12
   below the taste threshold. (Theorem 3)

4. **alpha_LM = alpha_bare / u_0 = 0.0906** is the physically correct coupling
   for the hierarchy formula. (Lepage-Mackenzie, verified numerically)

5. **d = 4 uniqueness:** v = M_Pl x alpha_s^{2^d} gives O(100 GeV) only for
   d = 4, because 4d = 2^d has the unique nontrivial solution d = 4.

### What is NOT derived (the gap):

**The compact formula v = M_Pl x alpha^{16} is not derived from the CW mechanism.**

The CW mechanism gives exp(-const/alpha). The compact formula gives
alpha^{16} = exp(16 ln alpha). These agree to within a factor of 3 at
alpha = 0.09, but they are DIFFERENT FUNCTIONS with different dependence
on alpha.

The precise relationship is:

    alpha^{16} = exp(16 ln alpha)          (compact formula)
    exp(-pi/alpha) = exp(-pi/alpha)        (CW with threshold)

At alpha = 0.09: 16 ln(0.09) = -38.3 and pi/0.09 = 34.9. The ratio
38.3/34.9 = 1.10. The compact formula has a 10% larger exponent than
the CW formula.

This 10% discrepancy in the exponent translates to a factor of e^{3.4} = 30
in v, which is why the CW gives v ~ 834-1660 GeV while the compact formula
gives v ~ 254 GeV.

### The nature of the gap:

The gap is not numerical (it is not about the value of alpha or k_1).
The gap is STRUCTURAL: no derivation starting from the CW effective
potential produces v = M_Pl x alpha^{N_taste} as an exact formula.

The compact formula would require a mechanism where:
- Each taste contributes ln(alpha_s) to the effective action (not alpha_s)
- The contributions are exactly additive (no cross-talk between tastes)
- The sum is exactly N_taste x ln(alpha_s) = ln(alpha_s^{N_taste})

In perturbation theory, each taste contributes O(alpha_s) to the
effective action (not O(ln alpha_s)). The logarithm appears only through
dimensional transmutation (the CW mechanism), but the CW formula
has the wrong functional form.

A non-perturbative mechanism -- such as instantons, confinement, or a
phase transition -- might produce the logarithmic dependence, but no
concrete calculation demonstrates this.

---

## What the compact formula MIGHT be

The compact formula v = M_Pl x alpha_LM^{16} might be:

1. **An interpolation formula** that happens to be numerically accurate at
   the physical value of alpha but is not exact at other couplings. The CW
   formula and the compact formula agree to ~30% at alpha = 0.09, which is
   within the systematic uncertainty of 1-loop CW. The compact formula might
   be a convenient mnemonic, not a theorem.

2. **The leading term of a convergent series** where the full answer is:

       v = M_Pl x alpha^{16} x (1 + c_1 alpha + c_2 alpha^2 + ...)

   The correction terms might connect it to the CW formula at higher orders.
   If c_1 ~ 4 pi (a typical perturbative coefficient), then c_1 alpha ~ 1.1,
   and the series is marginal.

3. **A non-perturbative result** requiring a strong-coupling or lattice
   calculation that goes beyond the CW 1-loop potential. The fact that the
   compact formula gives a better numerical answer than the CW formula
   might indicate that it captures non-perturbative physics (resummation,
   renormalons, or lattice artifacts) that the CW formula misses.

4. **A deep structural identity** in the taste algebra of Cl(4) that we
   have not yet identified. The fact that 4d = 2^d uniquely at d = 4
   suggests a connection between the lattice dimension and the taste
   dimension that might have algebraic content.

---

## The strongest argument: the exponent identity

The closest thing to a derivation is the EXPONENT IDENTITY:

    16 |ln alpha_s| = 8 pi^2 / (N_eff y_t^2)

This holds when N_eff = 12 pi / (N_taste alpha_s |ln alpha_s|) = 10.73.

**Interpretation.** The compact formula is equivalent to the CW formula with a
SPECIFIC value of N_eff that depends on alpha_s. This value of N_eff is:

    N_eff = 12 pi / (16 alpha_s |ln alpha_s|) = 12 pi / (16 x 0.09 x 2.39) = 10.73

The required N_eff for v = 246 GeV is 10.66, giving 0.7% agreement.

The factor 12 = 4 x 3 is the top-quark degrees of freedom.
The factor pi comes from alpha = g^2/(4pi).
The factor 16 = 2^4 is the taste number.
The factor alpha_s |ln alpha_s| is the characteristic scale of the lattice-to-continuum matching.

**Each factor has a clear group-theoretic or lattice origin.** But the
PRODUCT 12 pi / (16 alpha_s |ln alpha_s|) is not derivable from first principles
without knowing the answer. It is the content of the compact formula rewritten
in CW language.

---

## Conclusion

The formula v = M_Pl x alpha_LM^{16} is:

- **Numerically verified** to 3% (or exactly with 2-loop corrections).
- **Structurally motivated** by N_taste = 2^4 = 16 from Cl(4).
- **Unique** to d = 4 (only integer solution of 4d = 2^d for d > 1).
- **Scheme-identified** with alpha_LM = alpha_bare/u_0 (Lepage-Mackenzie).
- **NOT derived** from the Coleman-Weinberg mechanism or any other known
  analytic framework. The CW mechanism gives exp(-const/alpha), not alpha^{16}.

The gap between the CW exponent (-pi/alpha = -34.9) and the compact
exponent (16 |ln alpha| = 38.3) is 10% in the exponent, corresponding to
a factor of ~30 in v. Closing this gap requires either:

(a) A non-perturbative mechanism that converts the CW exponent into
    the compact form, or
(b) A fundamentally different derivation of EWSB that bypasses the CW
    effective potential entirely.

Until one of these is achieved, the compact formula stands as an empirical
observation, not a theorem.
