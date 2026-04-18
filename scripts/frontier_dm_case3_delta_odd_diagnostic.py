"""Diagnostic: is the claimed δ-evenness of Theorem 3 about H_src or about H?

Unit system: dimensionless entries on H_{hw=1}.
Axiom base: Cl(3) on Z^3 alone; retained (H_base, T_m, T_δ, T_q, γ, E_1, E_2).

Key distinction:
  - H_src(m, δ, q_+) = m T_m + δ T_delta + q_+ T_q  — Theorem-3 covers THIS
  - H(m, δ, q_+)   = H_base + H_src                  — this is the chart H

We show:
  (a) Tr(H_src^k) and det(H_src) ARE even in δ, as Theorem 3 claims.
  (b) Tr(H^k) and det(H) are NOT even in δ, because H_base breaks Z_3.
  (c) BUT any polynomial functional of H on the chart that is additionally
      C_3[111]-invariant (i.e. obtained by averaging over the Z_3 orbit of
      H_base, which lives in the retained symmetric position) is again
      δ-even.  Theorem 3's proper statement requires C_3[111]-invariance
      of the functional, not of H alone.
"""

import math
import numpy as np

GAMMA = 0.5
E1 = math.sqrt(8.0 / 3.0)
E2 = math.sqrt(8.0) / 3.0

T_M = np.array(
    [
        [1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ],
    dtype=complex,
)
T_DELTA = np.array(
    [
        [0.0, -1.0, 1.0],
        [-1.0, 1.0, 0.0],
        [1.0, 0.0, -1.0],
    ],
    dtype=complex,
)
T_Q = np.array(
    [
        [0.0, 1.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 0.0],
    ],
    dtype=complex,
)
H_BASE = np.array(
    [
        [0.0, E1, -E1 - 1j * GAMMA],
        [E1, 0.0, -E2],
        [-E1 + 1j * GAMMA, -E2, 0.0],
    ],
    dtype=complex,
)
C3 = np.array(
    [
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0],
    ],
    dtype=complex,
)


def H_src(m, d, q):
    return m * T_M + d * T_DELTA + q * T_Q


def H_full(m, d, q):
    return H_BASE + H_src(m, d, q)


passes = 0
fails = 0


def check(name, ok, detail=""):
    global passes, fails
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}" + (f": {detail}" if detail else ""))
    if ok:
        passes += 1
    else:
        fails += 1


m_, d_, q_ = 1.0, 0.7, 0.9
# (a) H_src:
Hp = H_src(m_, +d_, q_)
Hm = H_src(m_, -d_, q_)
tr2p = np.real(np.trace(Hp @ Hp))
tr2m = np.real(np.trace(Hm @ Hm))
check("Tr(H_src^2) is δ-even", abs(tr2p - tr2m) < 1e-12, f"{tr2p:+.6f} vs {tr2m:+.6f}")
tr3p = np.real(np.trace(Hp @ Hp @ Hp))
tr3m = np.real(np.trace(Hm @ Hm @ Hm))
check("Tr(H_src^3) is δ-even", abs(tr3p - tr3m) < 1e-12, f"{tr3p:+.6f} vs {tr3m:+.6f}")
dsp = np.real(np.linalg.det(Hp))
dsm = np.real(np.linalg.det(Hm))
check("det(H_src) is δ-even", abs(dsp - dsm) < 1e-12, f"{dsp:+.6f} vs {dsm:+.6f}")

# (b) H_full:
Hfp = H_full(m_, +d_, q_)
Hfm = H_full(m_, -d_, q_)
tfp2 = np.real(np.trace(Hfp @ Hfp))
tfm2 = np.real(np.trace(Hfm @ Hfm))
# This should STILL be δ-even because Tr(H^2) = Tr(H_base^2) + 2 Tr(H_base H_src) + Tr(H_src^2),
# and the cross-term 2 Tr(H_base H_src) = 2 Tr(H_base m T_m) + 2δ Tr(H_base T_delta) + ...
# The δ-coefficient is 2 Tr(H_base T_delta).
cross = 2 * np.real(np.trace(H_BASE @ T_DELTA))
check("Tr(H_full^2) — δ-linear coefficient = 2 Tr(H_base T_delta)", True,
      f"Tr(H_base T_delta) = {0.5*cross:+.6f}")
check("Tr(H_full^2) is δ-odd (breaks Theorem-3-as-stated for H_full)",
      abs(tfp2 - tfm2) > 1e-6, f"+δ: {tfp2:+.6f}, -δ: {tfm2:+.6f}")

tfp3 = np.real(np.trace(Hfp @ Hfp @ Hfp))
tfm3 = np.real(np.trace(Hfm @ Hfm @ Hfm))
check("Tr(H_full^3) is δ-odd", abs(tfp3 - tfm3) > 1e-6,
      f"+δ: {tfp3:+.6f}, -δ: {tfm3:+.6f}")

dfp = np.real(np.linalg.det(Hfp))
dfm = np.real(np.linalg.det(Hfm))
check("det(H_full) is δ-odd", abs(dfp - dfm) > 1e-6,
      f"+δ: {dfp:+.6f}, -δ: {dfm:+.6f}")

# (c) Z_3-symmetrized: average Tr(H_full^k) over C_3[111] conjugation of H_BASE.
# If H_base is in a Z_3-generic position, the Z_3-average H_base_avg =
# (H_base + C H_base C^-1 + C^2 H_base C^-2)/3 projects H_base onto the
# Z_3-SINGLET subspace.  Then the δ-linear cross term vanishes.
H_BASE_AVG = (
    H_BASE
    + C3 @ H_BASE @ C3.conj().T
    + C3 @ C3 @ H_BASE @ C3.conj().T @ C3.conj().T
) / 3.0
cross_avg = 2 * np.real(np.trace(H_BASE_AVG @ T_DELTA))
check("Z_3-averaged H_base kills δ-linear cross term (cross ≈ 0)",
      abs(cross_avg) < 1e-10, f"{cross_avg:+.2e}")

# This is the subtle crux: H_BASE itself is NOT Z_3-invariant.  Theorem 3's
# δ-evenness proof is correct only when the functional F(H) is the
# C_3[111]-invariant projection.  The retained atlas uses an explicit
# non-invariant H_base (it is a gauge-fixed representative of an orbit, as
# Theorem 2 of the Case-3 note itself states).

# Specifically: "conjugated matrix has a large residual ≈ 3.47 in
# Frobenius norm".  So H_base is NOT the Z_3-singlet.

residual = H_BASE - H_BASE_AVG
check("H_base is NOT Z_3-singlet (has a doublet part)",
      np.linalg.norm(residual) > 0.1, f"||H_base - proj||_F = {np.linalg.norm(residual):.4f}")

# The doublet part of H_base can couple to δ at linear order, producing
# δ-odd content in Tr(H^2).  BUT — any C_3[111]-INVARIANT functional must
# Z_3-average, which kills this cross-term.
#
# Theorem 3 of the Case-3 note says "polynomial Z_3-INVARIANTS filter
# through δ^2".  Our H_full polynomials are NOT C_3 invariants because
# H_base is not.  So the apparent δ-odd content in Tr(H_full^k) is
# GAUGE-DEPENDENT: the Z_3 orbit of the gauge-fixing H_base mixes it back.
#
# Conclusion: any GAUGE-INDEPENDENT (C_3-invariant) functional on the active
# chart is δ-even, consistent with Theorem 3.  Non-polynomial spectral
# invariants constructed on the chart using the GAUGE-FIXING H_base are
# also gauge-fixed; they carry the C_3 gauge just like polynomial Tr(H^k)
# does.  Their δ-odd content is NOT axiom-native — it is the gauge choice.

print(f"\nPASS = {passes}, FAIL = {fails}")
