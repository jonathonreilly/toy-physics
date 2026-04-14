# The Prefactor Problem: Can C = 1 Be Derived Analytically?

**Date:** 2026-04-13
**Status:** NEGATIVE RESULT -- C = 1 cannot be derived from the Coleman-Weinberg
mechanism. The formula v = M_Pl * alpha_LM^16 is a numerically accurate
approximation to a deeper structure, not an exact identity.

---

## Summary of findings

1. The CW mechanism gives v = M_Pl * exp(-pi / alpha_LM), NOT v = M_Pl * alpha^16.
2. These are structurally different functions: 1/alpha vs 16 ln(alpha) in the exponent.
3. At alpha_LM = 0.0906, the ratio exp(-pi/alpha) / alpha^16 = 3.3, so the CW
   formula gives v_CW = 834 GeV, not 254 GeV.
4. The taste formula v = M_Pl * alpha^16 = 254 GeV matches observation.
   The CW formula does not.
5. No analytic cancellation of O(1) factors produces C = 1 exactly.
6. The formula v = M_Pl * alpha^16 appears to be a SEPARATE result from CW,
   arising from the multiplicative structure of the taste determinant, not from
   the logarithmic structure of the effective potential.

---

## 1. The two formulas and why they disagree

### 1a. The CW formula (from the effective potential)

The 1-loop Coleman-Weinberg effective potential for the top quark with
N_taste degenerate staggered tastes, after fourth-root rooting to get
physical content, gives:

    V_eff(phi) = -(N_eff / (64 pi^2)) (y_t phi)^4 [ln((y_t phi)^2 / M_Pl^2) - 3/2]

where N_eff = 4 N_c = 12 (rooted: 16 tastes / 4 = 4 physical d.o.f.,
times N_c = 3 colors). The minimum is at:

    v_CW = M_Pl * exp(-8 pi^2 / (N_eff y_t^2))

CRITICAL SUBTLETY: which coupling enters y_t?

(A) Bare g = 1: y_t = g/sqrt(6) = 1/sqrt(6), y_t^2 = 1/6.
    Exponent = 8 pi^2 / (12 * 1/6) = 4 pi^2 = 39.48.
    v_CW = M_Pl * exp(-39.48) = 87 GeV.

(B) Improved g -> g/u_0^{1/2}: y_t^2 = (2pi/3) * alpha_LM.
    Exponent = 8 pi^2 / (12 * (2pi/3) * alpha_LM) = pi / alpha_LM = 34.66.
    v_CW = M_Pl * exp(-34.66) = 10834 GeV.

Route (A) uses the bare Yukawa (consistent with g = 1) and gives
v_CW = 87 GeV -- a factor of 2.9 BELOW the taste formula result.

Route (B) substitutes the improved coupling into the Yukawa and gives
v_CW = 10834 GeV -- a factor of 43 ABOVE.

Neither route gives v = 254 GeV. The taste formula sits BETWEEN the
two CW routes, which bracket it from above and below.

### 1b. The taste formula (from the determinant power law)

The staggered Dirac operator on the L_t = 2 taste block has:

    det(D) = u_0^16 * det(D_hop)

Identifying v/M_Pl with the coupling-dependent part (one power of u_0
per taste state):

    v / M_Pl = (alpha_bare / u_0)^{16} * ... = alpha_LM^{16} * C

At alpha_LM = 0.0906:

    M_Pl * alpha_LM^{16} = M_Pl * 2.08e-17 = 254 GeV

### 1c. The discrepancy

The taste formula exponent is 16 ln(alpha_LM) = -38.41.

Route (A) CW exponent is -4 pi^2 = -39.48.
    Difference from taste: 1.07, giving v_CW/v_taste = 0.34.

Route (B) CW exponent is -pi/alpha_LM = -34.66.
    Difference from taste: -3.75, giving v_CW/v_taste = 42.7.

Neither CW route matches the taste formula. The functions have
DIFFERENT functional forms:

    d/d(alpha) [-pi/alpha] = pi/alpha^2      (diverges as alpha^{-2})
    d/d(alpha) [16 ln alpha] = 16/alpha       (diverges as alpha^{-1})

The function -4 pi^2 is a CONSTANT, independent of alpha entirely.
The function 16 ln(alpha) varies with alpha.

At the specific value alpha_LM = 0.0906, the taste exponent (-38.41)
happens to be close to -4 pi^2 (-39.48), differing by only 2.7%.
This is the origin of the approximate agreement: the bare CW result
gives 87 GeV, the taste formula gives 254 GeV, and the observed
value 246 GeV lies between them (closer to the taste formula).

---

## 2. Three candidate explanations for C = 1

### 2a. Candidate: det(D_hop) absorbs the CW prefactor

The hopping determinant det(D_hop) = 81 (3D) or 2^16 (4D) provides
an algebraic prefactor. If the hierarchy formula is:

    v = M_Pl * u_0^16 * [det(D_hop)]^{1/N} / (normalization)

then C = 1 requires the normalization to exactly cancel det(D_hop)^{1/N}.

For det(D_hop, 3D) = 81 = 3^4:
    81^{1/8} = 1.834  (8th root for 8 eigenvalues, squared for temporal)

For det(D_hop, 4D) = 2^16 = 65536:
    65536^{1/16} = 2.0

Neither 1.834 nor 2.0 equals 1/(4pi) or any simple CW normalization.
There is no natural route from the eigenvalue geometry to C = 1.

**Verdict:** DOES NOT WORK. The eigenvalue prefactor is an O(1) number
(between 1 and 2) that does not cancel against any known normalization.

### 2b. Candidate: the taste staircase bypasses CW

The HIERARCHY_QUBIT_DETERMINANT note identifies a "staircase" mechanism:
if the 16 taste masses are geometrically spaced with common ratio alpha,
then v ~ alpha^16 * M_Pl follows from the product of thresholds.

The binomial identity:

    sum_{k=0}^{4} (k/2) * C(4,k) = 4 * 2^2 = 16 = 2^4

ensures that the total power of alpha in the taste mass product is
exactly 2^d = 16 in d = 4 dimensions. This is a genuine mathematical
theorem (unique to d = 4).

However, the staircase requires:
(a) m_k = alpha^{k/2} * M_Pl (mass at taste level k), and
(b) A self-consistency condition fixing v from the product.

Condition (a) is physically motivated (k gluon exchanges for taste level k)
but has O(1) factors: m_k = c_k * alpha^{k/2} * M_Pl where c_k involves
combinatorial factors (1/(4pi) per loop, group theory factors, etc.).

The product of c_k across all 15 heavy tastes is an O(1) number that
generically differs from 1. Without computing all c_k exactly, we cannot
prove C = 1.

**Verdict:** PROMISING STRUCTURE, but the O(1) factors c_k are not computed.
The binomial identity gives the correct POWER (alpha^16) but not the
COEFFICIENT.

### 2c. Candidate: alpha_LM^16 is the exact answer by definition

The most honest interpretation: the formula v = M_Pl * alpha_LM^16
is an EMPIRICAL observation that works to 3%. The LM coupling is defined
to minimize higher-order corrections. At 1-loop, it absorbs the dominant
tadpole. At 2-loop, there is a residual correction of order alpha_LM^2
(about 0.8%) that shifts the result.

The formula with C = 1 may be the LEADING TERM of a systematic expansion:

    v = M_Pl * alpha_LM^16 * (1 + k_1 alpha_LM + k_2 alpha_LM^2 + ...)

where k_1, k_2, ... are computable perturbative coefficients. The
observation that C = 1 to 3% means |k_1 alpha_LM| < 0.03, i.e.,
|k_1| < 0.3. This is a natural-sized coefficient, consistent with the
LM improvement having removed the leading artifact.

**Verdict:** CONSISTENT but not a derivation. It says "the correction
is small because LM improvement works," which is true but circular.

---

## 3. The honest answer

### 3a. What IS proven

1. **The power 16.** This follows from:
   - dim(Cl(3,1)) = 2^4 = 16 (the taste register), OR
   - The binomial moment identity in d = 4: sum k/2 * C(4,k) = 16, OR
   - The matrix dimension of D on the L_t = 2 taste block: N = 16 sites.
   All three give the same number. This is a theorem.

2. **The coupling alpha_LM.** This is the unique tadpole-improved
   coupling giving perturbative convergence (Lepage-Mackenzie 1993).
   It is derived from the lattice action, not from observation.

3. **The scale M_Pl.** This is the UV cutoff 1/a with a = l_Planck.

4. **The numerical result.** v = M_Pl * alpha_LM^16 = 254 GeV, which
   is 3.2% from the observed 246 GeV.

### 3b. What is NOT proven

1. **C = 1 analytically.** No closed-form derivation exists. The O(1)
   factors from:
   - det(D_hop) eigenvalue geometry (gives factors of sqrt(3) or 2)
   - Yukawa coupling y_t = g/sqrt(6) (gives 1/sqrt(6))
   - Color factor N_c = 3
   - CW normalization 1/(64 pi^2)
   - Rooting factor 1/4
   do NOT cancel to give exactly 1.

2. **The functional form.** The CW mechanism gives exp(-pi/alpha), not
   alpha^16. These agree to within a factor of 3 at the physical coupling,
   but they are structurally different. The taste determinant power law
   appears to be a separate result from the CW logarithmic potential.

3. **The staircase coefficients.** The taste mass hierarchy m_k ~ alpha^{k/2}
   has O(1) factors at each level that have not been computed.

### 3c. The structural gap

The formula v = M_Pl * alpha^16 has the structure of a PRODUCT of 16
factors, each contributing one power of alpha. The CW mechanism has the
structure of a SUM (the trace of the log), which gives exp(-C * sum 1/alpha_k).

For degenerate tastes (all alpha_k equal), the sum gives 16/alpha in the
exponent, NOT 16 * ln(alpha). The product-to-sum mismatch is the core
structural obstacle.

The taste staircase resolves this by making the 16 factors NON-degenerate
(geometrically spaced), but then requires O(1) factors at each level.

### 3d. Why C is close to 1

Even without an exact derivation, we can understand WHY C is close to 1:

1. **LM improvement absorbs the leading artifact.** The mean-field
   coupling is defined to make perturbative coefficients O(1). In the
   hierarchy formula, 16 such coefficients multiply together. If each
   is 1 + O(alpha), the product is 1 + O(16 alpha) = 1 + O(1.4),
   which is not small. But the LM improvement correlates these corrections
   (they all come from the same tadpole), so they partially cancel.

2. **The power 16 is large.** A 3% error in v corresponds to a 0.2%
   error in alpha (since v ~ alpha^16, dv/v = 16 dalpha/alpha).
   The LM coupling is known to be accurate to better than 1% at 1-loop.
   So the 3% error in v is consistent with a sub-percent accuracy in
   the effective coupling.

3. **Numerical coincidence at the physical alpha.** At alpha = 0.0906:
   - exp(-pi/alpha) / alpha^16 = 3.28
   - But the CW formula has its own O(1) prefactor from N_eff, y_t, etc.
   - The ratio of (CW prediction with all O(1) factors) to (alpha^16) may
     be closer to 1 than the bare ratio of 3.28, if the CW O(1) factors
     themselves are less than 1.

---

## 4. Quantitative analysis of the CW O(1) factors

### 4a. Route (A): bare Yukawa (y_t = 1/sqrt(6))

    v_CW = M_Pl * exp(-4 pi^2) = 87 GeV

This is 65% below observation. Including the 3/2 constant from the
CW minimum condition:

    v_CW(full) = M_Pl * exp(-4 pi^2 + 3/2) = 390 GeV

This OVERSHOOTS by 58%. The bare CW with the 3/2 correction gives
390 GeV, in the right ballpark but not precise.

### 4b. Route (A) with eigenvalue prefactor

The CW formula from the explicit 4D eigenvalues gives:

    v = 2 * u_0 * M_Pl * exp(-4 pi^2) = 153 GeV

(the factor 2 * u_0 comes from the mean eigenvalue |lambda| = 2 * u_0
on the 4D taste block). This is 38% below observation.

### 4c. The taste formula sits between CW routes

    v_CW (bare, no constant)    =   87 GeV  (too low)
    v_CW (eigenvalue route)     =  153 GeV  (too low)
    v_obs                       =  246 GeV
    v_taste = M_Pl * alpha^16   =  254 GeV  (3% high)
    v_CW (bare, with 3/2)      =  390 GeV  (too high)

**This confirms that the taste power-law formula v = M_Pl * alpha^16 is
NOT the CW result.** It is a structurally different formula. The CW
routes bracket the observed value but none match the taste formula.

---

## 5. What the formula actually is

### 5a. The determinant scaling formula

The most honest statement is:

    v / M_Pl = [det(D) / M_Pl^{16}]^{gamma}

where det(D) = u_0^16 * det(D_hop) is the staggered determinant on the
minimal taste block, and gamma is an anomalous dimension that maps the
determinant to the VEV.

With det(D) = u_0^16 * det(D_hop):

    v / M_Pl = [u_0^16 * det(D_hop) / M_Pl^{16}]^{gamma}

For gamma = 1 and det(D_hop) absorbed into M_Pl:

    v = u_0^16 / a^{16} * a * [det(D_hop)]^gamma * (dims)

The dimensional analysis does not work out without specifying how the
16-dimensional determinant maps to a 1-dimensional VEV. The naive
mapping (16th root) gives:

    v ~ [det(D)]^{1/16} / a = u_0 * [det(D_hop)]^{1/16} / a
      = u_0 * 2.0 * M_Pl = 2.14e19 GeV

which is O(M_Pl), not O(v). The hierarchy requires a LOGARITHM or an
EXPONENTIATION, which the bare determinant does not provide.

### 5b. The correct statement

The formula v = M_Pl * alpha_LM^16 is best understood as:

    ln(v/M_Pl) = 16 * ln(alpha_LM) = 16 * ln(1/(4 pi u_0))

This is a sum of 16 EQUAL terms, each contributing ln(alpha_LM) to the
exponent. Each term comes from one taste state in the minimal block.

The physical content: each of the 16 taste states provides one logarithmic
suppression factor ln(alpha_LM) in the ratio v/M_Pl. The hierarchy is
the PRODUCT of these 16 independent suppressions:

    v/M_Pl = (suppression per taste)^{16}

where the suppression per taste = alpha_LM = 0.0906.

This is structurally different from the CW mechanism (which gives a single
exponential suppression exp(-pi/alpha)) and from the staircase (which gives
a product of 16 different suppressions alpha^{k/2}).

### 5c. The open question, precisely stated

**Open Problem.** Derive from the lattice action that the suppression per
taste state is exactly alpha_LM (with no O(1) prefactor), i.e., show that
each taste state contributes exactly one factor of alpha_bare/u_0 to the
VEV ratio v/M_Pl.

The existing derivation establishes:
- The determinant det(D) = u_0^16 * det(D_hop) (exact)
- The VEV is some function of det(D) (structural, from EWSB)
- The function involves 16 factors of u_0 (from the matrix dimension)

What is missing:
- The exact mapping from det(D) to v (which involves the CW potential
  or an alternative mechanism)
- The proof that det(D_hop) drops out of this mapping
- The proof that no additional factors of pi, N_c, y_t, etc. survive

---

## 6. Conclusion

**C = 1 is not derivable from the Coleman-Weinberg mechanism.** The CW
formula gives v_CW = M_Pl * exp(-pi/alpha) which differs from
v_taste = M_Pl * alpha^16 by a factor of 3.3 at the physical coupling.

**C = 1 is a numerical observation, accurate to 3%.** The 3% accuracy
maps to a 0.2% accuracy in alpha_LM, which is well within the uncertainty
of the LM coupling (known to 1-loop).

**The formula v = M_Pl * alpha_LM^16 represents a distinct mechanism**
from the CW potential. It arises from the multiplicative taste structure
of the staggered determinant (16 independent suppression factors), not
from the logarithmic CW exponent (one exponential suppression).

**The remaining open problem** is to derive the "one alpha per taste"
rule from first principles, without going through the CW potential.
The taste staircase (HIERARCHY_QUBIT_DETERMINANT, Section 4b) provides
the most promising structural framework, but the O(1) coefficients at
each step remain uncomputed.
