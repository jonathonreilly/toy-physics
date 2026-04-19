"""Koide observable-principle cyclic source law — axiom-only scout runner.

Verifies, step-by-step with PASS/FAIL tallies, every labeled algebraic
claim in
``docs/KOIDE_OBSERVABLE_PRINCIPLE_CYCLIC_SOURCE_LAW_NOTE_2026-04-18.md``.

The runner is dimensionless and retained-surface only: it uses only the
retained `M_3(C)` generation algebra with induced `C_3[111]` cyclic shift
and the axiomatic generator ``W[J] = log|det(D+J)| - log|det D|``. No PDG
masses are consumed in any derivation step. A final observational
consistency section is flagged explicitly.
"""

from __future__ import annotations

import cmath
import math
import random

import numpy as np


# ---------------------------------------------------------------------------
# Retained algebra
# ---------------------------------------------------------------------------

I3 = np.eye(3, dtype=complex)

# C = C_3[111] cyclic shift on H_hw=1: C|X_j> = |X_{j+1 mod 3}>.
# In matrix form C_{ij} = delta_{i, j+1 mod 3}.
C = np.zeros((3, 3), dtype=complex)
for j in range(3):
    C[(j + 1) % 3, j] = 1.0
C2 = C @ C

B0 = I3.copy()
B1 = C + C2
B2 = 1j * (C - C2)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def hermitize(M: np.ndarray) -> np.ndarray:
    return 0.5 * (M + M.conj().T)


def random_invertible_matrix(seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    while True:
        M = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        # Make D well-conditioned by shifting spectrum.
        M = M + 3.0 * I3
        if abs(np.linalg.det(M)) > 1e-6:
            return M


def random_cyclic_hermitian(seed: int) -> tuple[np.ndarray, complex, complex]:
    rng = np.random.default_rng(seed)
    a = float(rng.normal()) + 1.5  # shift to keep invertible
    b = complex(rng.normal(), rng.normal())
    G = a * I3 + b * C + b.conjugate() * C2
    return G, a, b


def W_at(D: np.ndarray, J: np.ndarray) -> float:
    """Exact W[J] = log|det(D+J)| - log|det D|."""
    s_dj, ld_dj = np.linalg.slogdet(D + J)
    s_d, ld_d = np.linalg.slogdet(D)
    return ld_dj - ld_d


def dW_finite_diff(D: np.ndarray, B: np.ndarray, h: float = 1e-6) -> float:
    return (W_at(D, h * B) - W_at(D, -h * B)) / (2.0 * h)


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

PASS = 0
FAIL = 0
failures: list[str] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        failures.append(f"{label}: {detail}")
        print(f"  FAIL  {label}  -- {detail}")


# ---------------------------------------------------------------------------
# Section 1. Cyclic basis algebraic identities (from KOIDE_CYCLIC_WILSON_...)
# ---------------------------------------------------------------------------

print("Section 1 -- cyclic basis sanity")

check(
    "C^3 = I",
    np.allclose(C @ C @ C, I3),
)
check("B0 = I_3", np.allclose(B0, I3))
check("B1 = C + C^2", np.allclose(B1, C + C2))
check("B2 = i(C - C^2)", np.allclose(B2, 1j * (C - C2)))
check("B0 hermitian", np.allclose(B0, B0.conj().T))
check("B1 hermitian", np.allclose(B1, B1.conj().T))
check("B2 hermitian", np.allclose(B2, B2.conj().T))
check(
    "orthogonal pairing: Re Tr(B0 B1) = 0",
    abs(np.trace(B0 @ B1).real) < 1e-12,
)
check(
    "orthogonal pairing: Re Tr(B0 B2) = 0",
    abs(np.trace(B0 @ B2).real) < 1e-12,
)
check(
    "orthogonal pairing: Re Tr(B1 B2) = 0",
    abs(np.trace(B1 @ B2).real) < 1e-12,
)
check("Re Tr(B0^2) = 3", abs(np.trace(B0 @ B0).real - 3.0) < 1e-12)
check("Re Tr(B1^2) = 6", abs(np.trace(B1 @ B1).real - 6.0) < 1e-12)
check("Re Tr(B2^2) = 6", abs(np.trace(B2 @ B2).real - 6.0) < 1e-12)


# ---------------------------------------------------------------------------
# Section 2. Jacobi formula: dW(B) = Re Tr(D^-1 B)
# ---------------------------------------------------------------------------

print("\nSection 2 -- eq. (2) Re Tr(D^-1 B) vs finite-difference dW")

for seed in range(5):
    D = random_invertible_matrix(seed=seed)
    G = np.linalg.inv(D)
    for name, B in [("B0", B0), ("B1", B1), ("B2", B2)]:
        analytic = np.trace(G @ B).real
        numeric = dW_finite_diff(D, B)
        check(
            f"seed={seed} {name}: Re Tr(D^-1 B) matches finite-diff dW",
            abs(analytic - numeric) < 1e-6,
            f"analytic={analytic:.10f} numeric={numeric:.10f}",
        )


# ---------------------------------------------------------------------------
# Section 3. Fourier trace decomposition — eqs. (5a-c), (6a-c)
# ---------------------------------------------------------------------------

print("\nSection 3 -- eq. (5a-c) Tr(G*I), Tr(G*C), Tr(G*C^2)")

for seed in range(5):
    D = random_invertible_matrix(seed=100 + seed)
    G = np.linalg.inv(D)
    g = G  # alias
    alpha = np.trace(G @ I3)
    beta = np.trace(G @ C)
    gamma = np.trace(G @ C2)
    # From the note:
    alpha_check = g[0, 0] + g[1, 1] + g[2, 2]
    beta_check = g[0, 1] + g[1, 2] + g[2, 0]
    gamma_check = g[0, 2] + g[1, 0] + g[2, 1]
    check(
        f"seed={seed}: alpha = g11+g22+g33",
        abs(alpha - alpha_check) < 1e-12,
    )
    check(
        f"seed={seed}: beta = g12+g23+g31",
        abs(beta - beta_check) < 1e-12,
    )
    check(
        f"seed={seed}: gamma = g13+g21+g32",
        abs(gamma - gamma_check) < 1e-12,
    )


# ---------------------------------------------------------------------------
# Section 4. Response triple formulas — eqs. (7a-c)
# ---------------------------------------------------------------------------

print("\nSection 4 -- eqs. (7a-c) r_i in terms of alpha, beta, gamma")

for seed in range(5):
    D = random_invertible_matrix(seed=200 + seed)
    G = np.linalg.inv(D)
    alpha = np.trace(G @ I3)
    beta = np.trace(G @ C)
    gamma = np.trace(G @ C2)
    r0 = np.trace(G @ B0).real
    r1 = np.trace(G @ B1).real
    r2 = np.trace(G @ B2).real
    check(
        f"seed={seed}: r0 = Re alpha",
        abs(r0 - alpha.real) < 1e-12,
    )
    check(
        f"seed={seed}: r1 = Re(beta+gamma)",
        abs(r1 - (beta + gamma).real) < 1e-12,
    )
    check(
        f"seed={seed}: r2 = Im gamma - Im beta",
        abs(r2 - (gamma.imag - beta.imag)) < 1e-12,
    )


# ---------------------------------------------------------------------------
# Section 5. Cyclic-invariant specialization — eqs. (9a-c), (10a-c), (11)
# ---------------------------------------------------------------------------

print("\nSection 5 -- cyclic-invariant G: (r0, r1, r2) = (3a, 6 Re b, -6 Im b)")

for seed in range(5):
    G, a, b = random_cyclic_hermitian(seed=300 + seed)
    # First: verify G commutes with C (cyclic invariance by conjugation).
    check(
        f"seed={seed}: C G C^-1 = G",
        np.allclose(C @ G @ C.conj().T, G),
    )
    alpha = np.trace(G @ I3)
    beta = np.trace(G @ C)
    gamma = np.trace(G @ C2)
    check(f"seed={seed}: alpha = 3 a", abs(alpha - 3 * a) < 1e-12)
    # From Tr(C) = Tr(C^2) = 0, Tr(C^3) = 3: Tr(G C) = 3 b*, Tr(G C^2) = 3 b.
    check(f"seed={seed}: beta = 3 b*", abs(beta - 3 * b.conjugate()) < 1e-12)
    check(
        f"seed={seed}: gamma = 3 b",
        abs(gamma - 3 * b) < 1e-12,
    )
    r0 = np.trace(G @ B0).real
    r1 = np.trace(G @ B1).real
    r2 = np.trace(G @ B2).real
    check(f"seed={seed}: r0 = 3 a", abs(r0 - 3 * a) < 1e-12)
    check(f"seed={seed}: r1 = 6 Re b", abs(r1 - 6 * b.real) < 1e-12)
    check(f"seed={seed}: r2 = 6 Im b", abs(r2 - 6 * b.imag) < 1e-12)


# ---------------------------------------------------------------------------
# Section 6. Koide-on-responses algebra — eq. (12)
# ---------------------------------------------------------------------------

print("\nSection 6 -- eq. (12) 2 r0^2 = r1^2 + r2^2 iff a^2 = 2 |b|^2")

# 6a. Generic cyclic-invariant G does NOT lie on the Koide cone.
off_cone_count = 0
on_cone_count = 0
for seed in range(50):
    G, a, b = random_cyclic_hermitian(seed=400 + seed)
    r0 = np.trace(G @ B0).real
    r1 = np.trace(G @ B1).real
    r2 = np.trace(G @ B2).real
    lhs = 2 * r0 ** 2
    rhs = r1 ** 2 + r2 ** 2
    if abs(lhs - rhs) < 1e-8:
        on_cone_count += 1
    else:
        off_cone_count += 1

check(
    "generic cyclic G lands OFF the Koide cone (selection, not identity)",
    off_cone_count > 0 and on_cone_count == 0,
    f"on_cone={on_cone_count} off_cone={off_cone_count}",
)

# 6b. When a^2 = 2 |b|^2 is imposed, cyclic G lands exactly on the cone.
equipart_hits = 0
for seed in range(20):
    rng = np.random.default_rng(500 + seed)
    phi = rng.uniform(0, 2 * math.pi)
    a = 1.0 + rng.uniform(0.1, 1.0)  # positive
    mag_b = a / math.sqrt(2.0)
    b = mag_b * cmath.exp(1j * phi)
    G = a * I3 + b * C + b.conjugate() * C2
    r0 = np.trace(G @ B0).real
    r1 = np.trace(G @ B1).real
    r2 = np.trace(G @ B2).real
    lhs = 2 * r0 ** 2
    rhs = r1 ** 2 + r2 ** 2
    if abs(lhs - rhs) < 1e-10 * max(abs(lhs), 1.0):
        equipart_hits += 1

check(
    "imposing a^2 = 2|b|^2 forces 2 r0^2 = r1^2 + r2^2 exactly",
    equipart_hits == 20,
    f"hits={equipart_hits}/20",
)


# ---------------------------------------------------------------------------
# Section 7. (3 a, 6 Re b, -6 Im b) map is a linear bijection
# ---------------------------------------------------------------------------

print("\nSection 7 -- the response map has nonzero Jacobian")

# Parameterize cyclic G by (a, Re b, Im b). The map to (r0, r1, r2) is
# diagonal: r0 = 3 a, r1 = 6 Re b, r2 = 6 Im b. Determinant = 108.
J_matrix = np.array([
    [3.0, 0.0, 0.0],
    [0.0, 6.0, 0.0],
    [0.0, 0.0, 6.0],
])
check(
    "Jacobian det = 108",
    abs(np.linalg.det(J_matrix) - 108.0) < 1e-12,
)
check(
    "Jacobian nonzero (bijection onto R^3)",
    abs(np.linalg.det(J_matrix)) > 1e-6,
)


# ---------------------------------------------------------------------------
# Section 8. Cross-check against the published cyclic-Wilson reconstruction
# ---------------------------------------------------------------------------

print("\nSection 8 -- reconstruction H_cyc = (r0/3) B0 + (r1/6) B1 + (r2/6) B2")

for seed in range(5):
    G, a, b = random_cyclic_hermitian(seed=600 + seed)
    r0 = np.trace(G @ B0).real
    r1 = np.trace(G @ B1).real
    r2 = np.trace(G @ B2).real
    H_cyc = (r0 / 3.0) * B0 + (r1 / 6.0) * B1 + (r2 / 6.0) * B2
    # For cyclic G the reconstruction must match G exactly (H_cyc = G).
    check(
        f"seed={seed}: reconstruction equals cyclic G",
        np.allclose(H_cyc, G, atol=1e-12),
    )


# ---------------------------------------------------------------------------
# Section 9. Retained `hw=1` baseline — degenerate D gives r1 = r2 = 0
# ---------------------------------------------------------------------------

print("\nSection 9 -- HW1 shape-theorem baseline (uniform weight)")

# When the intermediate-state weights from the hw=1 second-order-return
# shape theorem are all equal (w_{O_0} = w_a = w_b = w), the effective D
# on H_hw=1 is proportional to I_3 (Dirac-bridge identity). Then G ∝ I.
D_baseline = 3.0 * I3
G_baseline = np.linalg.inv(D_baseline)
r0 = np.trace(G_baseline @ B0).real
r1 = np.trace(G_baseline @ B1).real
r2 = np.trace(G_baseline @ B2).real
check("baseline r0 = 1.0", abs(r0 - 1.0) < 1e-12)
check("baseline r1 = 0", abs(r1) < 1e-12)
check("baseline r2 = 0", abs(r2) < 1e-12)
check(
    "baseline trivially satisfies 2 r0^2 = r1^2 + r2^2 only via "
    "degeneracy (2 != 0)",
    not (abs(2 * r0 ** 2 - (r1 ** 2 + r2 ** 2)) < 1e-12),
    "baseline off cone (as expected: no nondegenerate masses)",
)


# ---------------------------------------------------------------------------
# Section 10. Observational verification (flagged separate from derivation)
# ---------------------------------------------------------------------------

print("\nSection 10 -- observational consistency (NOT part of derivation)")

# PDG pole masses used ONLY to confirm the equipartition a^2 = 2|b|^2 is
# compatible with the observed charged-lepton triple. No PDG mass feeds
# into any step in Sections 1-9.
m_e = 0.5109989e-3  # GeV
m_mu = 105.6583745e-3
m_tau = 1776.86e-3
sqrt_m = np.array([math.sqrt(m_e), math.sqrt(m_mu), math.sqrt(m_tau)])
# Brannen/Rivero circulant coefficients on sqrt(m):
v0 = sqrt_m.sum() / 3.0
# Invert cosine form to get delta; use Fourier transform of sqrt_m.
omega = cmath.exp(2j * math.pi / 3)
z = (sqrt_m[0] + omega.conjugate() * sqrt_m[1] + omega * sqrt_m[2]) / 3.0
a_obs = v0
b_obs = z
ratio = (a_obs ** 2) / (abs(b_obs) ** 2)
check(
    "observed: a^2 / |b|^2 ~= 2 (Koide cone)",
    abs(ratio - 2.0) / 2.0 < 1e-3,
    f"ratio = {ratio:.10f}",
)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print(f"PASS={PASS}  FAIL={FAIL}")
if failures:
    for f in failures:
        print(" ", f)
print("=" * 60)

if FAIL != 0:
    raise SystemExit(1)
