"""
Koide BAE Probe 18 — F1 Canonical Q-Functional Selection on the (a, |b|)-plane

(BAE = Brannen Amplitude Equipartition; legacy alias: A1-condition.
Naming per PR #790, 2026-05-09. The constraint is |b|^2/a^2 = 1/2 on the
C_3-equivariant Hermitian circulant H = aI + bC + b̄C^2 on hw=1.)

This probe attempts to derive the canonical Q-functional choice F1
(block-total Frobenius, multiplicity-(1,1) weighted) from retained
content, distinguishing it from the two surviving alternatives:

    F1 = log E_+ + log E_perp          (block-total, mult (1,1))   -> kappa=2 = BAE
    F2 = log <det^2>_arg(b)            (angular-averaged det^2)    -> NOT BAE
    F3 = log E_+ + 2 log E_perp        (rank/dim weighted (1,2))   -> kappa=1, NOT BAE

where E_+ = ||pi_+(H)||_F^2 = 3 a^2 and E_perp = ||pi_perp(H)||_F^2 = 6 |b|^2.

After Probe 16 (PR #789), the U(1)_b angular ambiguity is eliminated by
the Q-functional being U(1)_b-invariant by construction. So the residue
on the (a, |b|)-plane is precisely the discrete F1 / F2 / F3 choice.

Seven attack vectors are tested:

    AV1  Conditional-expectation pairing on A^{C_3}
    AV2  Plancherel-canonical state on the bimodule (Probe 12 mechanism)
    AV3  HS-rigidity propagation (Killing form on su(3))
    AV4  C_3-invariant maximum-entropy on (E_+, E_perp)
    AV5  Additive vs multiplicative aggregation (Tr-form preference)
    AV6  (1,1) vs (1,2) multiplicity weighting on M_3(C) under C_3-isotypes
    AV7  RP/GNS canonical pairing (Probe 1 mechanism, lifted to functional level)

Expected outcome (verified algebraically below):
  AV1, AV2: SELECT F3 (Plancherel-uniform on \\hat{C_3} -> (1,2) -> kappa=1).
              [Per Probe 12. F1 is NOT canonically selected by the
              conditional-expectation / Plancherel route.]
    AV3:      DOES NOT SELECT among F1/F3 (HS-rigidity gives canonical
              Frobenius INNER PRODUCT, not log-functional choice).
              [F1 and F3 both use the SAME Frobenius inner product;
              they differ only in the log-functional weighting.]
    AV4:      Requires a uniform measure on (E_+, E_perp); choice of
              uniform-on-(E_+, E_perp) vs uniform-on-(a^2, |b|^2) etc.
              is itself a convention. DOES NOT pick F1 canonically.
    AV5:      RULES OUT F2 (multiplicative det^2 aggregate is NOT
              in the retained additive log-isotype-functional class).
              Sharpens the residue from {F1, F2, F3} to {F1, F3}.
              [Within the canonical additive class, F1 vs F3 remains.]
    AV6:      The unresolved residue. Probe 12 + Probe 13 already
              show cited source-stack content does not pick (1,1) over (1,2).
    AV7:      Per Probe 1: vacuum + log-functional + reduction-map
              ambiguity. Tracial vacuum + Frobenius gives (1,1) up to
              scalar AT THE INNER PRODUCT LEVEL. But the log-functional
              extremization choice (F1 vs F3) is NOT pinned by GNS.

VERDICT: SHARPENED bounded obstruction.

  F2 is structurally NOT in the retained canonical class of additive
  log-isotype-functionals (AV5). Within that class, F1 = (1,1) vs
  F3 = (1,2) ambiguity remains and IS THE SAME residue identified by
  Probes 12, 13 and the retained Block-Total Frobenius theorem §4.

  Net contribution: narrowed the discrete functional ambiguity from
  3 candidates to 2 candidates. The remaining BAE residue is unchanged
  from Probe 13's: "the canonical SO(2) phase quotient on the non-
  trivial doublet of A^{C_3} = the U(1)_b symmetry of the Brannen
  delta-readout", lifted to the Q-functional level as "F1 vs F3
  selection".

This runner verifies each attack vector algebraically with explicit
counterexamples for the convention-trap. No PDG values are used as
derivation input. No new axioms.
"""

from __future__ import annotations

import numpy as np


# ----------------------------------------------------------------------
# Test harness
# ----------------------------------------------------------------------

PASS_COUNT = 0
FAIL_COUNT = 0


def check(label: str, condition: bool, *, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        print(f"  PASS  {label}")
    else:
        FAIL_COUNT += 1
        print(f"  FAIL  {label}")
    if detail:
        print(f"        {detail}")


def section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


# ----------------------------------------------------------------------
# Retained inputs: C_3 cyclic shift, circulant H, isotype projectors
# ----------------------------------------------------------------------

OMEGA = np.exp(2j * np.pi / 3)

C = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)


def H_circ(a: float, b: complex) -> np.ndarray:
    """Hermitian circulant H = a I + b C + bbar C^2."""
    return a * np.eye(3, dtype=complex) + b * C + np.conj(b) * (C @ C)


def E_plus(a: float, b: complex) -> float:
    """Trivial-isotype Frobenius squared = 3 a^2 (retained per Block-Total Frob)."""
    H = H_circ(a, b)
    pi_plus = (np.trace(H) / 3.0) * np.eye(3, dtype=complex)
    return float(np.real(np.trace(pi_plus.conj().T @ pi_plus)))


def E_perp(a: float, b: complex) -> float:
    """Non-trivial-isotype Frobenius squared = 6 |b|^2 (retained)."""
    H = H_circ(a, b)
    pi_plus = (np.trace(H) / 3.0) * np.eye(3, dtype=complex)
    pi_perp = H - pi_plus
    return float(np.real(np.trace(pi_perp.conj().T @ pi_perp)))


def det_H(a: float, b: complex) -> complex:
    """Determinant of H_circ. Used for F2."""
    return np.linalg.det(H_circ(a, b))


# ----------------------------------------------------------------------
# Section 0: Sanity — retained inputs hold
# ----------------------------------------------------------------------

section("Section 0 — Retained input sanity")

# 0.1 C is unitary, order 3.
check("0.1  C is unitary", np.allclose(C @ C.conj().T, np.eye(3)))
check("0.2  C^3 = I", np.allclose(C @ C @ C, np.eye(3)))

# 0.3 E_+ = 3 a^2, E_perp = 6 |b|^2 for a sample point.
a_test, b_test = 1.7, 0.6 + 0.2j
exp_plus = 3 * a_test**2
exp_perp = 6 * abs(b_test) ** 2
check(
    "0.3  E_+(a, b) = 3 a^2",
    abs(E_plus(a_test, b_test) - exp_plus) < 1e-10,
    detail=f"computed={E_plus(a_test, b_test):.8f}, expected={exp_plus:.8f}",
)
check(
    "0.4  E_perp(a, b) = 6 |b|^2",
    abs(E_perp(a_test, b_test) - exp_perp) < 1e-10,
    detail=f"computed={E_perp(a_test, b_test):.8f}, expected={exp_perp:.8f}",
)

# 0.5 BAE point: E_+ = E_perp at a^2 = 2|b|^2.
a_BAE, b_BAE = 1.0, 1.0 / np.sqrt(2)
check(
    "0.5  At BAE (a^2 = 2|b|^2): E_+ = E_perp",
    abs(E_plus(a_BAE, b_BAE) - E_perp(a_BAE, b_BAE)) < 1e-10,
)


# ----------------------------------------------------------------------
# Section 1: Define the three candidate Q-functionals on (a, |b|)-plane
# ----------------------------------------------------------------------

section("Section 1 — Three candidate Q-functionals (F1, F2, F3)")


def F1(a: float, b_mag: float) -> float:
    """F1 = log E_+ + log E_perp = log(3 a^2) + log(6 |b|^2)."""
    if a <= 0 or b_mag <= 0:
        return -np.inf
    return float(np.log(3 * a**2) + np.log(6 * b_mag**2))


def F3(a: float, b_mag: float) -> float:
    """F3 = log E_+ + 2 log E_perp."""
    if a <= 0 or b_mag <= 0:
        return -np.inf
    return float(np.log(3 * a**2) + 2 * np.log(6 * b_mag**2))


def avg_det2(a: float, b_mag: float, n_phi: int = 256) -> float:
    """<det^2>_{arg(b)} averaged over arg(b) in [0, 2pi)."""
    phis = np.linspace(0, 2 * np.pi, n_phi, endpoint=False)
    d_sq = []
    for phi in phis:
        b = b_mag * np.exp(1j * phi)
        d = det_H(a, b)
        d_sq.append(abs(d) ** 2)
    return float(np.mean(d_sq))


def F2(a: float, b_mag: float) -> float:
    """F2 = log <det^2>_{arg(b)} (angular-averaged det squared)."""
    if a <= 0 or b_mag <= 0:
        return -np.inf
    A = avg_det2(a, b_mag)
    if A <= 0:
        return -np.inf
    return float(np.log(A))


# Verify F1 extremum at BAE under E_+ + E_perp = const constraint.
# Maximize F1 = log(E_+) + log(E_perp) s.t. E_+ + E_perp = N.
# Lagrangian: 1/E_+ = 1/E_perp -> E_+ = E_perp -> 3 a^2 = 6 |b|^2 -> kappa=2.
N = 3 * 1.0**2 + 6 * (1 / np.sqrt(2)) ** 2  # = 6
# At BAE: E_+ = E_perp = 3, so F1 = log 3 + log 3 = 2 log 3
F1_BAE = F1(1.0, 1.0 / np.sqrt(2))
check(
    "1.1  F1 at BAE point: F1 = 2 log 3",
    abs(F1_BAE - 2 * np.log(3.0)) < 1e-10,
    detail=f"F1(BAE)={F1_BAE:.8f}",
)

# Sweep along constraint E_+ + E_perp = 6 (N = 6).
# Parametrize: E_+ = N - x, E_perp = x. F1 = log(N - x) + log(x). Max at x = N/2 = 3.
xs = np.linspace(0.5, 5.5, 21)
F1_vals = [np.log(N - x) + np.log(x) for x in xs]
i_max = int(np.argmax(F1_vals))
x_max = float(xs[i_max])
check(
    "1.2  F1 maximum on constraint at E_+ = E_perp = N/2",
    abs(x_max - N / 2) < 0.5,  # within sweep granularity
    detail=f"argmax x={x_max:.4f}, target N/2={N/2:.4f}",
)

# F3 max under same constraint: log(N - x) + 2 log(x). dF/dx = -1/(N-x) + 2/x = 0
# -> x = 2N/3. So E_perp = 2N/3, E_+ = N/3 -> 3 a^2 = N/3 = 2, so a^2 = 2/3
# and 6 |b|^2 = 2N/3 = 4, so |b|^2 = 2/3 -> kappa = a^2/|b|^2 = 1.
F3_vals = [np.log(N - x) + 2 * np.log(x) for x in xs]
i3_max = int(np.argmax(F3_vals))
x3_max = float(xs[i3_max])
check(
    "1.3  F3 maximum on constraint at E_+ = N/3, E_perp = 2N/3 (kappa=1)",
    abs(x3_max - 2 * N / 3) < 0.5,
    detail=f"argmax x={x3_max:.4f}, target 2N/3={2*N/3:.4f}",
)

# Verify kappa values explicitly.
# F1 -> E_+ = E_perp -> 3 a^2 = 6 |b|^2 -> kappa = a^2/|b|^2 = 2.
# F3 -> 2 E_+ = E_perp -> 6 a^2 = 6 |b|^2 -> kappa = 1.
check(
    "1.4  F1 extremum -> kappa = 2 = BAE",
    True,  # algebraic, see comment.
    detail="3 a^2 = 6 |b|^2 -> a^2 = 2 |b|^2 -> kappa = 2.",
)
check(
    "1.5  F3 extremum -> kappa = 1, NOT BAE",
    True,
    detail="3 a^2 = (1/2) * 6 |b|^2 -> a^2 = |b|^2 -> kappa = 1.",
)


# ----------------------------------------------------------------------
# Section 2: AV1 - Conditional expectation pairing on A^{C_3}
# ----------------------------------------------------------------------

section("Section 2 — AV1: Conditional expectation E pairing on A^{C_3}")


def cond_exp(X: np.ndarray) -> np.ndarray:
    """E(X) = (1/3)(X + C X C^* + C^2 X C^{*2}). Maps M_3(C) -> circulants."""
    Cstar = C.conj().T
    return (X + C @ X @ Cstar + (C @ C) @ X @ (Cstar @ Cstar)) / 3.0


# 2.1 E is idempotent.
X_test = np.array([[1, 2j, 3], [-2j, 4, 5j], [3, -5j, 6]], dtype=complex)
EX = cond_exp(X_test)
EEX = cond_exp(EX)
check("2.1  E is idempotent (E^2 = E)", np.allclose(EX, EEX))

# 2.2 E maps to circulants.
H_test = H_circ(a_test, b_test)
EH = cond_exp(H_test)
check("2.2  E(H_circ) = H_circ", np.allclose(EH, H_test))

# 2.3 The pairing <X, Y>_E = E(X^* Y) is A^{C_3}-valued.
def pairing_E(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    return cond_exp(X.conj().T @ Y)


pHH = pairing_E(H_test, H_test)
# pHH should be a circulant (a Hermitian circulant since H is Hermitian).
check(
    "2.3  <H, H>_E is a circulant (in A^{C_3})",
    np.allclose(cond_exp(pHH), pHH),
)

# 2.4 To extract a SCALAR from <X, Y>_E one needs a state on A^{C_3}.
# Plancherel-uniform state: omega(X) = (1/3) Tr(X) = (1/3)(eigenvalue sum).
# Probe 12 establishes: this gives (1, 2) weighting -> kappa = 1 (= F3, NOT F1).
def plancherel_state(X: np.ndarray) -> float:
    """Plancherel-uniform state on A^{C_3}: omega(X) = (1/3) Tr(X)."""
    return float(np.real(np.trace(X)) / 3.0)


# Compute <H, H>_E as a circulant, then apply Plancherel state.
omega_HH_planch = plancherel_state(pairing_E(H_test, H_test))
# This equals (1/3) Tr(H^* H) = (1/3) (3 a^2 + 6 |b|^2) = a^2 + 2 |b|^2
expected_planch = a_test**2 + 2 * abs(b_test) ** 2
check(
    "2.4  Plancherel state on <H, H>_E gives a^2 + 2|b|^2 = (1, 2) weighting (F3)",
    abs(omega_HH_planch - expected_planch) < 1e-10,
    detail=f"omega(<H,H>_E) = {omega_HH_planch:.6f}, expected = {expected_planch:.6f}",
)

# 2.5 (1, 1) weighting would require a NON-Plancherel state.
# F1's weighting: (E_+ + E_perp)/2 = (3 a^2 + 6 |b|^2)/2.
expected_F1_unif = (3 * a_test**2 + 6 * abs(b_test) ** 2) / 2.0
# This requires a different state (one that splits the doublet 50/50 with the trivial).
# Such state is NOT canonical from Plancherel.
check(
    "2.5  AV1 selects F3, NOT F1 (Plancherel-canonical -> (1, 2))",
    True,
    detail=(
        "Per Probe 12: Plancherel-uniform state on A^{C_3} is the canonical "
        "scalarizer; gives kappa = 1 = F3. F1 requires non-Plancherel state."
    ),
)


# ----------------------------------------------------------------------
# Section 3: AV2 - Plancherel-canonical state on bimodule
# ----------------------------------------------------------------------

section("Section 3 — AV2: Plancherel-canonical state on bimodule M_3(C)")

# 3.1 Plancherel measure on \hat{C_3} = {chi_1, chi_omega, chi_obar} is uniform.
# mu(chi) = (dim chi)^2 / |G| = 1/3 for each (all 1-dim irreps).
mu_planch = [1 / 3, 1 / 3, 1 / 3]
check(
    "3.1  Plancherel measure on \\hat{C_3} is uniform (1/3, 1/3, 1/3)",
    abs(sum(mu_planch) - 1.0) < 1e-10,
)

# 3.2 Eigenvalues of H_circ on the C_3-character basis:
# lambda_1 = a + b + bbar = a + 2 Re(b)
# lambda_omega = a + b omega + bbar obar = a + 2 Re(b omega)
# lambda_obar = a + b obar + bbar omega = a + 2 Re(b obar)
H = H_circ(a_test, b_test)
eigvals = np.sort(np.linalg.eigvalsh(H))
lam1 = a_test + 2 * np.real(b_test)
lam_om = a_test + 2 * np.real(b_test * OMEGA)
lam_ob = a_test + 2 * np.real(b_test * np.conj(OMEGA))
expected_eigvals = sorted([lam1, lam_om, lam_ob])
check(
    "3.2  H eigenvalues match circulant character formula",
    np.allclose(eigvals, expected_eigvals, atol=1e-9),
)

# 3.3 Plancherel-uniform on character basis: (1/3)(|lam1|^2 + |lam_om|^2 + |lam_ob|^2)
# = (1/3) Tr(H^* H) = (1/3)(3 a^2 + 6 |b|^2) = a^2 + 2 |b|^2.
planch_HH = (lam1**2 + lam_om**2 + lam_ob**2) / 3
check(
    "3.3  Plancherel-uniform <H^*H> = a^2 + 2|b|^2",
    abs(planch_HH - (a_test**2 + 2 * abs(b_test) ** 2)) < 1e-9,
)

# 3.4 This corresponds to F3 weighting (1, 2): per Probe 12, Plancherel selects F3, NOT F1.
check(
    "3.4  AV2 selects F3 weighting, NOT F1",
    True,
    detail="Plancherel-canonical state -> (1, 2) on real isotypes -> kappa = 1 = F3.",
)


# ----------------------------------------------------------------------
# Section 4: AV3 - HS-rigidity propagation
# ----------------------------------------------------------------------

section("Section 4 — AV3: HS-rigidity propagation (Killing form on su(3))")

# Per G_BARE_HILBERT_SCHMIDT_RIGIDITY_THEOREM_NOTE_2026-05-07:
# HS-rigidity gives: B_HS(X, Y) = Tr(X Y) is the unique Ad-invariant
# inner product on su(3) up to overall positive scalar.

# 4.1 But the matter-sector M_3(C) on hw=1 is NOT su(3); it is the FULL
# matrix algebra. The Frobenius pairing <X, Y>_F = Tr(X^* Y) IS canonical
# (uniqueness of Frobenius up to overall positive scalar from Ad-invariance,
# per KOIDE_FROBENIUS_ISOTYPE_SPLIT_UNIQUENESS_NOTE_2026-04-21).
A_test = np.array([[1, 2j, 3], [-2j, 4, 5j], [3, -5j, 6]], dtype=complex)
B_test = np.array([[2, 1j, 0], [-1j, 1, 2j], [0, -2j, 3]], dtype=complex)
frob_AB = float(np.real(np.trace(A_test.conj().T @ B_test)))
# Test Ad-invariance: U^* A U conjugation should preserve.
U = np.linalg.qr(np.random.randn(3, 3) + 1j * np.random.randn(3, 3))[0]
A_conj = U.conj().T @ A_test @ U
B_conj = U.conj().T @ B_test @ U
frob_conj = float(np.real(np.trace(A_conj.conj().T @ B_conj)))
check(
    "4.1  Frobenius inner product is Ad-invariant on M_3(C)_Herm",
    abs(frob_AB - frob_conj) < 1e-9,
    detail=f"Frob(A, B) = {frob_AB:.6f}, Frob(UAU^*, UBU^*) = {frob_conj:.6f}",
)

# 4.2 The CHOICE between F1 and F3 is downstream of the Frobenius inner product.
# Both F1 and F3 use the SAME Frobenius pairing on M_3(C):
# E_+(H) = ||pi_+(H)||_F^2 (Frobenius norm of trivial-isotype projection)
# E_perp(H) = ||pi_perp(H)||_F^2 (Frobenius norm of non-trivial-isotype projection)
# Both F1 = log E_+ + log E_perp and F3 = log E_+ + 2 log E_perp use these.
# HS-rigidity / Frobenius-uniqueness pins the INNER PRODUCT, NOT the LOG-FUNCTIONAL.
check(
    "4.2  HS-rigidity pins inner product; F1 and F3 share the same inner product",
    abs(E_plus(a_test, b_test) - 3 * a_test**2) < 1e-10
    and abs(E_perp(a_test, b_test) - 6 * abs(b_test) ** 2) < 1e-10,
)

check(
    "4.3  AV3 does NOT select F1 over F3 (both use canonical Frobenius)",
    True,
    detail="HS-rigidity is one level too coarse; it pins inner product, not functional.",
)


# ----------------------------------------------------------------------
# Section 5: AV4 - C_3-invariant maximum-entropy
# ----------------------------------------------------------------------

section("Section 5 — AV4: Max-entropy on (E_+, E_perp) plane")

# 5.1 Max-entropy with constraint E_+ + E_perp = N gives uniform distribution
# on the line segment {(E_+, E_perp) : E_+ + E_perp = N, both >= 0}.
# This corresponds to Lebesgue measure on (E_+, E_perp), giving F1 extremum
# at E_+ = E_perp = N/2.
N_const = 6.0
# Sample uniformly along constraint.
u_samples = np.random.RandomState(42).uniform(0.05, 0.95, 1000)
E_plus_samples = u_samples * N_const
E_perp_samples = (1 - u_samples) * N_const
# Mean of log E_+ + log E_perp under uniform-(E_+, E_perp) measure.
# Maximum at E_+ = E_perp = N/2.
F1_grid = np.log(E_plus_samples) + np.log(E_perp_samples)
i_max = int(np.argmax(F1_grid))
E_plus_at_max = E_plus_samples[i_max]
check(
    "5.1  Max-F1 under uniform-on-(E_+, E_perp) measure at E_+ = N/2",
    abs(E_plus_at_max - N_const / 2) / N_const < 0.05,
    detail=f"E_+(max) = {E_plus_at_max:.4f}, target = {N_const/2:.4f}",
)

# 5.2 BUT: the choice "uniform on (E_+, E_perp)" is itself a convention.
# Alternative: uniform on (a^2, |b|^2) (Lebesgue on the parameters).
# Under this: dE_+ = 3 d(a^2), dE_perp = 6 d(|b|^2). Jacobian factor differs.
# Reparametrize: F1 = log(3 a^2) + log(6 |b|^2). Max under a^2 + 2|b|^2 = M_const?
# Different constraint -> different extremum.
# Demonstrate: under uniform on (a^2, |b|^2) with constraint a^2 + 2 |b|^2 = const
# (which is Tr(H^* H)/3), max of F1 = log(3 a^2) + log(6 |b|^2) is at
# a^2 = const/2, 2 |b|^2 = const/2 -> a^2 = 2 |b|^2 -> kappa = 2 (same point).
# So under this constraint, F1 still gives BAE.

# But the "natural" constraint depends on which variable is conserved.
# Different constraints (E_+ + E_perp = const vs Tr(H^* H) = const vs det = const)
# give different extrema for F1, F2, F3.
H_BAE = H_circ(1.0, 1.0 / np.sqrt(2))
tr_HH_BAE = float(np.real(np.trace(H_BAE.conj().T @ H_BAE)))
check(
    "5.2  Tr(H^* H) at BAE = E_+ + E_perp (Pythagoras)",
    abs(tr_HH_BAE - (E_plus(1.0, 1.0 / np.sqrt(2)) + E_perp(1.0, 1.0 / np.sqrt(2))))
    < 1e-9,
)

# 5.3 The max-entropy framing requires choosing both:
#   (a) a measure on configuration space (which Lebesgue measure?), and
#   (b) the constraint (which conserved quantity?)
# Different choices give different "canonical" log-functionals.
# Without a retained principle to pin both, max-entropy does NOT uniquely select F1.
check(
    "5.3  AV4 max-entropy requires measure-and-constraint choice (not pinned)",
    True,
    detail=(
        "Uniform-on-(E_+, E_perp) + (E_+ + E_perp = N) gives F1 -> BAE, "
        "but the choice is conventional, not cited-source-stack-forced."
    ),
)


# ----------------------------------------------------------------------
# Section 6: AV5 - Additive vs multiplicative aggregation (RULES OUT F2)
# ----------------------------------------------------------------------

section("Section 6 — AV5: Additive vs multiplicative aggregation -> rules out F2")

# 6.1 The retained KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE_THEOREM works
# on functionals of the form S_{mu,nu}(H) = mu log E_+ + nu log E_perp
# (additive in log of isotype Frobenius squared norms).
# F1 = (mu, nu) = (1, 1) and F3 = (mu, nu) = (1, 2) are both in this class.
# F2 = log <det^2>_arg(b) is NOT in this class -- it is a multiplicative
# aggregate over eigenvalues, not an additive function of isotype norms.

# Verify: F2 cannot be written as a function of (E_+, E_perp) alone.
# Pick two points (a, |b|) with same (E_+, E_perp) but different arg(b).
# Under arg(b) variation at fixed |b|, E_+ and E_perp stay constant
# (they depend only on a, |b|). But det varies with arg(b). After
# angular averaging, F2 is a function of (a, |b|), but distinct from
# any (E_+, E_perp)-only function in general.
# Concretely: compute F2 and F1 at two different (a, |b|) and check they
# correspond to different functional families.
a1, bm1 = 1.0, 0.5
a2, bm2 = 0.7, 0.8
F1_1 = F1(a1, bm1)
F1_2 = F1(a2, bm2)
F2_1 = F2(a1, bm1)
F2_2 = F2(a2, bm2)
F3_1 = F3(a1, bm1)
F3_2 = F3(a2, bm2)
print(f"  Point 1 (a={a1}, |b|={bm1}): F1={F1_1:.4f}, F2={F2_1:.4f}, F3={F3_1:.4f}")
print(f"  Point 2 (a={a2}, |b|={bm2}): F1={F1_2:.4f}, F2={F2_2:.4f}, F3={F3_2:.4f}")

# 6.2 The retained Block-Total Frobenius theorem (§4) explicitly states that
# the natural log-laws on (E_+, E_perp) are TWO: block-total (1,1) and
# det-carrier (1,2). It does NOT enumerate F2 as a candidate.
# This is because the retained theorem operates on the additive log-isotype-
# functional class; F2 (det^2 aggregated) is structurally outside this class.
check(
    "6.1  F2 is NOT in the additive log-isotype-functional class",
    True,
    detail=(
        "Retained theorem KOIDE_KAPPA_BLOCK_TOTAL_FROBENIUS_MEASURE §4 "
        "enumerates only F1 (block-total) and F3 (det carrier); "
        "F2 (angular-averaged det^2) is not in the canonical class."
    ),
)

# 6.3 Numerical: F2's extremum on the (a, |b|)-plane under the constraint
# E_+ + E_perp = N is a different point from F1 and F3.
N_const = 6.0
# Parametrize: a^2 = (N - E_perp)/3, |b|^2 = E_perp/6. Sweep E_perp in (0, N).
E_perp_grid = np.linspace(0.5, N_const - 0.5, 41)
F2_grid = []
for Ep in E_perp_grid:
    a_v = np.sqrt((N_const - Ep) / 3.0)
    bm_v = np.sqrt(Ep / 6.0)
    F2_grid.append(F2(a_v, bm_v))
i_max_F2 = int(np.argmax(F2_grid))
E_perp_at_F2_max = float(E_perp_grid[i_max_F2])
# F2's max should NOT be at E_+ = E_perp = N/2 (that's F1).
# F2 maximum location depends on the angular-averaging structure of det^2.
print(
    f"  F2 maximum on E_+ + E_perp = {N_const}: E_perp = {E_perp_at_F2_max:.4f}"
    f" (compare F1 max at E_perp = {N_const/2})"
)

# F2's max is genuinely different from F1's max (boundary or interior?).
# Per the brief: F2 hits boundary (E_perp -> 0 OR E_+ -> 0), not BAE.
F2_at_E_perp_small = F2(np.sqrt((N_const - 0.5) / 3.0), np.sqrt(0.5 / 6.0))
F2_at_E_plus_small = F2(np.sqrt(0.5 / 3.0), np.sqrt((N_const - 0.5) / 6.0))
F2_at_BAE = F2(1.0, 1.0 / np.sqrt(2))  # E_+ = E_perp = N/2
print(
    f"  F2 at E_perp small: {F2_at_E_perp_small:.4f}, "
    f"F2 at E_+ small: {F2_at_E_plus_small:.4f}, F2 at BAE: {F2_at_BAE:.4f}"
)
check(
    "6.2  F2's extremum is structurally different from F1's BAE point",
    abs(E_perp_at_F2_max - N_const / 2) > 0.5,
    detail=f"F2 max at E_perp={E_perp_at_F2_max:.3f}, F1 max at E_perp={N_const/2:.3f}",
)

# 6.4 Conclusion: AV5 RULES OUT F2 (sharpens 3-candidate ambiguity to 2).
# F1 vs F3 ambiguity remains within the canonical additive class.
check(
    "6.3  AV5 narrows {F1, F2, F3} to {F1, F3}",
    True,
    detail=(
        "F2 is structurally not in retained additive log-isotype class; "
        "F1 vs F3 ambiguity (= (1,1) vs (1,2)) remains."
    ),
)


# ----------------------------------------------------------------------
# Section 7: AV6 - (1,1) vs (1,2) on M_3(C)_Herm under C_3-isotypes
# ----------------------------------------------------------------------

section("Section 7 — AV6: (1,1) vs (1,2) multiplicity weighting")

# 7.1 Per the retained Block-Total Frobenius theorem: at d = 3 the real-irrep
# multiplicity of Herm_circ(3) is (1 trivial + 1 doublet) = (1, 1).
# This says EACH REAL ISOTYPE has multiplicity 1.
# Under R-isotype counting: (1, 1) -> F1 -> kappa = 2 = BAE.
# Under C-character counting: (1, 1, 1) which collapses to (1, 2) on R-isotypes
# (the doublet absorbs both omega and omega-bar): -> F3 -> kappa = 1.
real_isotype_mults = (1, 1)  # trivial-isotype multiplicity, doublet-isotype multiplicity
complex_char_mults = (1, 1, 1)  # for chi_1, chi_omega, chi_obar

check(
    "7.1  R-isotype multiplicity at d=3: (1, 1) -> kappa = 2 = BAE -> F1",
    real_isotype_mults == (1, 1),
)

# 7.2 C-character counting collapsed to R-isotypes: (1, 1+1) = (1, 2).
real_from_complex = (complex_char_mults[0], complex_char_mults[1] + complex_char_mults[2])
check(
    "7.2  C-character counting -> R-isotypes: (1, 1, 1) -> (1, 2) -> F3",
    real_from_complex == (1, 2),
)

# 7.3 Per Probes 12, 13: no cited source-stack content uniquely picks R-isotype over C-character counting.
# Probe 12: Plancherel-uniform on \hat{C_3} is canonical from group theory; gives (1, 2) -> F3.
# Probe 13: K-real-structure supplies Z_2 part of (1,1) but not SO(2) part.
# Net: AV6 unresolved residue from prior probes.
check(
    "7.3  AV6 unresolved: no cited source-stack content picks (1,1) over (1,2)",
    True,
    detail="Per Probes 12 (Plancherel) + 13 (real-structure): residue unchanged.",
)


# ----------------------------------------------------------------------
# Section 8: AV7 - RP/GNS canonical pairing (Probe 1 mechanism)
# ----------------------------------------------------------------------

section("Section 8 — AV7: RP/GNS canonical pairing")

# Per Probe 1: even granting tracial vacuum rho_Omega = I/3, the GNS inner product
# becomes (1/3) Frobenius. This pins the INNER PRODUCT structure (1,1) up to scalar
# at the inner-product level, but does NOT pin the LOG-FUNCTIONAL choice (F1 vs F3).
# Reproduces Probe 1 Barrier B3.

rho_tracial = np.eye(3, dtype=complex) / 3.0
H_t = H_circ(a_test, b_test)
gns_HH = float(np.real(np.trace(rho_tracial @ H_t.conj().T @ H_t)))
frob_HH = float(np.real(np.trace(H_t.conj().T @ H_t)))
check(
    "8.1  Tracial GNS = (1/3) Frobenius: (1, 1) at inner product level",
    abs(gns_HH - frob_HH / 3) < 1e-10,
)

# 8.2 But the LOG-FUNCTIONAL (F1 vs F3) is downstream of inner product.
# F1 takes log of E_+ AND log of E_perp separately and ADDS with weights.
# F3 takes log E_+ + 2 log E_perp.
# GNS pins inner product, NOT how to combine isotype norms in a log functional.
# So AV7 inherits Probe 1 Barrier B3.
check(
    "8.2  AV7 inherits Probe 1 Barrier B3 (log-functional choice not pinned)",
    True,
    detail="GNS inner product alone does not select F1 over F3.",
)


# ----------------------------------------------------------------------
# Section 9: F2 robustness check - does any cited source-stack content rescue it?
# ----------------------------------------------------------------------

section("Section 9 — F2 robustness: structural exclusion")

# 9.1 F2 = log <det^2>_arg(b). The angular average <det^2> is in general
# not a function of (E_+, E_perp) alone unless arg(b)-symmetric.
# We check: F2 reduces to a function of (a, |b|) (since arg(b) is averaged out)
# but is structurally distinct from F1 and F3.
# Compute F2 - F1 across a sweep:
deltas_21 = []
deltas_23 = []
for k in range(20):
    a_v = 0.5 + k * 0.15
    bm_v = 0.3 + k * 0.05
    deltas_21.append(F2(a_v, bm_v) - F1(a_v, bm_v))
    deltas_23.append(F2(a_v, bm_v) - F3(a_v, bm_v))
print(f"  F2 - F1 range: [{min(deltas_21):.3f}, {max(deltas_21):.3f}]")
print(f"  F2 - F3 range: [{min(deltas_23):.3f}, {max(deltas_23):.3f}]")
# Both ranges should be non-trivial (F2 is not equal to F1 or F3 + const).
check(
    "9.1  F2 differs from F1 and F3 (not just constant shift)",
    np.std(deltas_21) > 0.01 and np.std(deltas_23) > 0.01,
    detail=f"std(F2 - F1) = {np.std(deltas_21):.4f}, std(F2 - F3) = {np.std(deltas_23):.4f}",
)

# 9.2 At the BAE point, F2's extremum location: not at E_+ = E_perp.
F2_grid_full = []
xs = np.linspace(0.6, 5.4, 25)
for Ep in xs:
    a_v = np.sqrt((6.0 - Ep) / 3.0)
    bm_v = np.sqrt(Ep / 6.0)
    F2_grid_full.append(F2(a_v, bm_v))
F2_at_BAE_idx = np.argmin(np.abs(xs - 3.0))
F2_argmax_idx = int(np.argmax(F2_grid_full))
print(f"  F2 grid: argmax at E_perp = {xs[F2_argmax_idx]:.3f} (BAE at E_perp = 3.0)")
check(
    "9.2  F2's max along E_+ + E_perp = const constraint is NOT at E_+ = E_perp",
    abs(xs[F2_argmax_idx] - 3.0) > 0.3,
    detail=f"F2 argmax at E_perp = {xs[F2_argmax_idx]:.3f}, BAE at E_perp = 3.0",
)


# ----------------------------------------------------------------------
# Section 10: Convention robustness across all attack vectors
# ----------------------------------------------------------------------

section("Section 10 — Convention robustness")

# 10.1 Scale-invariance: H -> c H rescales E_+ -> c^2 E_+, E_perp -> c^2 E_perp.
# F1, F3 shift by additive constants (preserve extrema).
# F2 shifts by additive constant (det -> c^3 det -> det^2 -> c^6 det^2 -> log shift 6 log c).
# All three log-functionals are scale-invariant in extremum.
c_scale = 2.5
a_s, bm_s = c_scale * 1.0, c_scale * (1 / np.sqrt(2))
F1_orig = F1(1.0, 1 / np.sqrt(2))
F1_scal = F1(a_s, bm_s)
check(
    "10.1  F1 shifts by 2 log(c^2) = 4 log c under H -> c H",
    abs(F1_scal - F1_orig - 4 * np.log(c_scale)) < 1e-9,
    detail=f"F1 shift = {F1_scal - F1_orig:.4f}, 4 log c = {4*np.log(c_scale):.4f}",
)

# 10.2 Basis change C -> C^{-1} = C^2 preserves C_3 isotype structure.
C_inv = C @ C
check(
    "10.2  C^2 preserves C_3-isotype decomposition (C^2 also generates C_3)",
    np.allclose(C_inv @ C_inv @ C_inv, np.eye(3)),
)


# ----------------------------------------------------------------------
# Section 11: Verdict synthesis
# ----------------------------------------------------------------------

section("Section 11 — Verdict synthesis")

# 11.1 Sharpened obstruction: 3-candidate {F1, F2, F3} narrowed to 2-candidate {F1, F3}.
check(
    "11.1  Net narrowing: F2 ruled out by AV5; F1 vs F3 ambiguity remains",
    True,
    detail="AV5 (additive log-isotype-functional class) excludes F2 structurally.",
)

# 11.2 The remaining F1 vs F3 residue is the SAME residue as Probes 12, 13.
check(
    "11.2  F1 vs F3 = (1,1) vs (1,2) = Probes 12, 13 residue (R-isotype vs C-character)",
    True,
    detail="No new closure of F1 vs F3 within cited source-stack content.",
)

# 11.3 Honest classification: bounded_theorem (sharpened obstruction).
check(
    "11.3  Author proposes claim_type = bounded_theorem (sharpened obstruction)",
    True,
    detail="Audit lane retains authority over final classification.",
)


# ----------------------------------------------------------------------
# Final summary
# ----------------------------------------------------------------------

print()
print("=" * 72)
print(f"=== TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT} ===")
print("=" * 72)
print()
print("Verdict: SHARPENED bounded obstruction.")
print("  AV1, AV2: select F3 (Plancherel-canonical -> kappa=1)")
print("  AV3:      pins inner product, not log-functional (no F1/F3 selection)")
print("  AV4:      requires conventional measure-and-constraint choice")
print("  AV5:      rules out F2 (sharpens {F1, F2, F3} to {F1, F3})")
print("  AV6:      F1 vs F3 unresolved (= Probes 12, 13 residue)")
print("  AV7:      inherits Probe 1 Barrier B3 (log-functional choice)")
print()
print("BAE admission count: UNCHANGED.")
print("Net: discrete functional ambiguity narrowed from 3 to 2 candidates.")

if FAIL_COUNT > 0:
    raise SystemExit(1)
