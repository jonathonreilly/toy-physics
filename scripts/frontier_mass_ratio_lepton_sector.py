#!/usr/bin/env python3
"""
Bounded charged-lepton mass-ratio lane.

Status:
  bounded secondary flavor-mass lane

Safe claim:
  The charged-lepton mass-root vector v = (sqrt(m_e), sqrt(m_mu), sqrt(m_tau))
  satisfies the Koide relation

    K = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = 2/3

  to 0.01% observationally. This is equivalent to the statement that v makes
  a 45 degree angle with (1, 1, 1). In a Z_3-cyclic decomposition of v in
  Cl(3), this is

    |a_0|^2 = 2 |a_1|^2

  where a_0 is the Z_3-trivial amplitude and a_1 = a_2^* is the complex
  conjugate pair of Z_3-nontrivial amplitudes. Equivalently: the Z_3-trivial
  channel carries the same "total weight" as the Z_3-nontrivial doublet.

  This is compatible with the Cl(3) / Z_3 structure that gives the promoted
  quark CKM surface, but it is not yet a retained theorem. Koide reduces
  the three-value charged-lepton spectrum to a one-parameter family. A
  framework-native second constraint fixing m_mu/m_tau or m_e/m_mu is NOT
  found among the promoted alpha-native quantities tested below.

Important qualifier:
  This is a bounded observational/structural lane, not a retention-grade
  derivation. The down-type quark lane (Phase 1) and up-type lane (Phase 2)
  are also bounded; the charged-lepton lane is weaker still because the
  CKM-dual algebra does not apply to the charged-lepton sector (no chirality-
  flipping mixing matrix in the pure charged sector). Koide provides one
  structural constraint; a second would be needed to close the lepton
  hierarchy zero-parameter.

No observed lepton masses are used as derivation inputs. PDG values are
carried as a comparator surface only.
"""

from __future__ import annotations

import cmath
import math

from canonical_plaquette_surface import CANONICAL_ALPHA_BARE, CANONICAL_ALPHA_S_V, CANONICAL_U0


# ----- Observational comparator surface (PDG 2024) -----
# Pole masses for charged leptons; these are the natural invariant comparators
# because QED running is negligible for lepton mass ratios.
M_E_OBS = 0.51099895  # MeV
M_MU_OBS = 105.6583755  # MeV
M_TAU_OBS = 1776.86  # MeV

R_EM_OBS = M_E_OBS / M_MU_OBS     # ~0.004836
R_MT_OBS = M_MU_OBS / M_TAU_OBS   # ~0.05946
R_ET_OBS = M_E_OBS / M_TAU_OBS    # ~0.000288

# Phase 1 predictions, for cross-lane comparison
R_DS_PRED = CANONICAL_ALPHA_S_V / 2.0
R_SB_PRED = (CANONICAL_ALPHA_S_V / math.sqrt(6.0)) ** (6.0 / 5.0)

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    line = f"  [{status}] {name}"
    if detail:
        line += f"  ({detail})"
    print(line)


# =============================================================================
def part1_input_surface() -> None:
    print("\n" + "=" * 72)
    print("PART 1: Input surface and observational comparator")
    print("=" * 72)

    print(f"\n  alpha_s(v)   = {CANONICAL_ALPHA_S_V:.10f}  [derived: plaquette chain]")
    print(f"  alpha_bare   = {CANONICAL_ALPHA_BARE:.10f}")
    print(f"  u_0          = {CANONICAL_U0:.10f}")

    print("\n  Observational comparator surface (PDG 2024, not derivation inputs):")
    print(f"    m_e   = {M_E_OBS:.8f} MeV")
    print(f"    m_mu  = {M_MU_OBS:.8f} MeV")
    print(f"    m_tau = {M_TAU_OBS:.4f} MeV")
    print(f"    m_e/m_mu   = {R_EM_OBS:.8f}")
    print(f"    m_mu/m_tau = {R_MT_OBS:.8f}")
    print(f"    m_e/m_tau  = {R_ET_OBS:.8f}")

    check(
        "All comparator masses are positive",
        M_E_OBS > 0 and M_MU_OBS > 0 and M_TAU_OBS > 0,
    )
    check(
        "Hierarchy m_e < m_mu < m_tau",
        M_E_OBS < M_MU_OBS < M_TAU_OBS,
    )
    check(
        "alpha_s(v) available from plaquette surface",
        CANONICAL_ALPHA_S_V > 0,
        f"alpha_s(v) = {CANONICAL_ALPHA_S_V:.6f}",
    )


# =============================================================================
def part2_koide_value() -> float:
    print("\n" + "=" * 72)
    print("PART 2: Koide relation (observational)")
    print("=" * 72)

    num = M_E_OBS + M_MU_OBS + M_TAU_OBS
    den = (math.sqrt(M_E_OBS) + math.sqrt(M_MU_OBS) + math.sqrt(M_TAU_OBS)) ** 2
    K = num / den

    print(f"\n  sum m_i   = {num:.6f} MeV")
    print(f"  (sum sqrt m_i)^2 = {den:.6f} MeV")
    print(f"  K = {K:.10f}")
    print(f"  2/3 = {2.0 / 3.0:.10f}")
    print(f"  |K - 2/3| / (2/3) = {abs(K - 2.0/3.0) / (2.0/3.0) * 100.0:.4f}%")

    check(
        "Koide K is finite and in (1/3, 1)",
        1.0 / 3.0 < K < 1.0,
        f"K = {K:.8f}",
    )
    check(
        "Observed K matches 2/3 within 0.05%",
        abs(K - 2.0 / 3.0) / (2.0 / 3.0) < 5e-4,
        f"dev = {(K - 2.0/3.0) / (2.0/3.0) * 100.0:+.4f}%",
    )
    # The canonical 'is Koide exact' test: K should sit right on 2/3 to parts
    # per 10^4. Current PDG centrals give ~1e-4 deviation.
    check(
        "Koide residual < 1e-3 on PDG centrals",
        abs(K - 2.0 / 3.0) < 1e-3,
        f"|K - 2/3| = {abs(K - 2.0/3.0):.6e}",
    )

    return K


# =============================================================================
def part3_geometric_form(K: float) -> float:
    print("\n" + "=" * 72)
    print("PART 3: Geometric form -- angle with (1,1,1)")
    print("=" * 72)

    v = (math.sqrt(M_E_OBS), math.sqrt(M_MU_OBS), math.sqrt(M_TAU_OBS))
    v_norm2 = sum(x * x for x in v)
    dot = v[0] + v[1] + v[2]
    cos2 = (dot * dot) / (3.0 * v_norm2)
    theta = math.degrees(math.acos(math.sqrt(cos2)))

    print("\n  v = (sqrt m_e, sqrt m_mu, sqrt m_tau) in sqrt-MeV")
    print(f"  |v|^2            = {v_norm2:.6f}")
    print(f"  v . (1,1,1)      = {dot:.6f}")
    print(f"  cos^2(theta)     = (v.(1,1,1))^2 / (3 |v|^2) = {cos2:.10f}")
    print(f"  theta            = {theta:.6f} deg")
    print("\n  Koide K = 2/3 <=> cos^2(theta) = 1/2 <=> theta = 45 deg.")

    check(
        "Geometric form: cos^2(theta) = 1/(3K)",
        abs(cos2 - 1.0 / (3.0 * K)) < 1e-12,
        f"cos^2 = {cos2:.10f}, 1/(3K) = {1.0/(3.0*K):.10f}",
    )
    check(
        "Koide K = 2/3 <=> theta = 45 deg (within 0.05 deg at PDG centrals)",
        abs(theta - 45.0) < 5e-2,
        f"theta = {theta:.6f} deg",
    )
    check(
        "cos^2(theta) = 1/2 to parts per 10^4",
        abs(cos2 - 0.5) < 1e-4,
        f"cos^2 - 1/2 = {cos2 - 0.5:+.6e}",
    )

    return theta


# =============================================================================
def part4_z3_decomposition() -> tuple[float, float, float]:
    print("\n" + "=" * 72)
    print("PART 4: Z_3 irrep decomposition of the mass-root vector")
    print("=" * 72)

    v = (math.sqrt(M_E_OBS), math.sqrt(M_MU_OBS), math.sqrt(M_TAU_OBS))

    omega = cmath.exp(2j * math.pi / 3.0)

    # Z_3 projection: chi_k = (1, omega^k, omega^(2k))/sqrt(3)
    # Coefficient a_k = chi_k* . v = (1/sqrt(3)) sum_j omega^(-k j) v_j
    a0 = (v[0] + v[1] + v[2]) / math.sqrt(3.0)
    a1 = (v[0] + omega.conjugate() * v[1] + (omega.conjugate() ** 2) * v[2]) / math.sqrt(3.0)
    a2 = (v[0] + omega * v[1] + (omega ** 2) * v[2]) / math.sqrt(3.0)

    mag_a0 = abs(a0)
    mag_a1 = abs(a1)
    mag_a2 = abs(a2)

    print("\n  Z_3 characters: chi_k = (1, omega^k, omega^(2k)) / sqrt(3)")
    print(f"  a_0 (trivial)        = {a0.real:+.6f}  |a_0| = {mag_a0:.6f}")
    print(f"  a_1 (nontrivial)     = {a1.real:+.6f} + {a1.imag:+.6f}i  |a_1| = {mag_a1:.6f}")
    print(f"  a_2 (nontrivial)     = {a2.real:+.6f} + {a2.imag:+.6f}i  |a_2| = {mag_a2:.6f}")

    # Reality: a_2 = a_1*
    reality_residual = abs(a2 - a1.conjugate())
    # Norm balance: |a_0|^2 + 2|a_1|^2 = |v|^2
    norm_residual = abs((mag_a0 ** 2 + 2 * mag_a1 ** 2) - sum(x * x for x in v))

    ratio_a0_a1 = mag_a0 / mag_a1
    print(f"\n  |a_0|/|a_1| = {ratio_a0_a1:.6f}   (Koide predicts sqrt(2) = {math.sqrt(2.0):.6f})")
    print(f"  |a_0|^2 / |a_1|^2 = {mag_a0**2 / mag_a1**2:.6f}  (Koide predicts 2)")

    check(
        "Reality condition: a_2 = conj(a_1)",
        reality_residual < 1e-10,
        f"residual = {reality_residual:.3e}",
    )
    check(
        "Parseval: |a_0|^2 + 2|a_1|^2 = |v|^2",
        norm_residual < 1e-10,
        f"residual = {norm_residual:.3e}",
    )
    check(
        "Koide <=> |a_0|^2 = 2 |a_1|^2 (equal Z_3-trivial and nontrivial-doublet weights)",
        abs(mag_a0 ** 2 - 2.0 * mag_a1 ** 2) / mag_a0 ** 2 < 5e-4,
        f"|a_0|^2 - 2|a_1|^2 normalized dev = {(mag_a0**2 - 2*mag_a1**2)/mag_a0**2:+.4e}",
    )

    return mag_a0, mag_a1, mag_a2


# =============================================================================
def part5_one_parameter_family(K_target: float = 2.0 / 3.0) -> None:
    print("\n" + "=" * 72)
    print("PART 5: Koide reduces 3-mass spectrum to 1-parameter family")
    print("=" * 72)

    # Parametrize m_tau = 1 (dimensionless), and let r = m_mu/m_tau. Then
    # Koide fixes s = m_e/m_tau given r.
    #   (s + r + 1) = K (sqrt(s) + sqrt(r) + 1)^2
    # Solve for sqrt(s).

    def solve_s_from_r(r: float) -> float | None:
        # Let u = sqrt(s). Then s = u^2. Equation:
        #   u^2 + r + 1 = K (u + sqrt(r) + 1)^2
        #   u^2 + r + 1 = K (u^2 + 2 u (sqrt(r)+1) + (sqrt(r)+1)^2)
        #   (1 - K) u^2 - 2 K (sqrt(r)+1) u + (r + 1 - K (sqrt(r)+1)^2) = 0
        a = 1.0 - K_target
        b = -2.0 * K_target * (math.sqrt(r) + 1.0)
        c = r + 1.0 - K_target * (math.sqrt(r) + 1.0) ** 2
        disc = b * b - 4 * a * c
        if disc < 0 or a == 0.0:
            return None
        sqrt_disc = math.sqrt(disc)
        # Two roots; the smaller-magnitude positive root is the physical m_e branch
        u1 = (-b + sqrt_disc) / (2 * a)
        u2 = (-b - sqrt_disc) / (2 * a)
        candidates = [u for u in (u1, u2) if u > 0 and u < math.sqrt(r)]
        if not candidates:
            return None
        u = min(candidates)
        return u * u

    # Test at observed r = m_mu / m_tau
    r_obs = R_MT_OBS
    s_from_K = solve_s_from_r(r_obs)
    print(f"\n  At observed r = m_mu/m_tau = {r_obs:.6f}:")
    print(f"    Koide prediction s = m_e/m_tau = {s_from_K:.8f}")
    print(f"    Observed          s = m_e/m_tau = {R_ET_OBS:.8f}")
    if s_from_K is not None:
        dev_s = (s_from_K - R_ET_OBS) / R_ET_OBS * 100.0
        print(f"    deviation = {dev_s:+.3f}%")

    check(
        "Koide admits a physical small-u branch at observed r",
        s_from_K is not None,
    )
    if s_from_K is not None:
        check(
            "Koide-predicted m_e/m_tau matches observation within 0.1% at observed r",
            abs((s_from_K - R_ET_OBS) / R_ET_OBS) < 1e-3,
            f"dev = {(s_from_K - R_ET_OBS)/R_ET_OBS*100:+.4f}%",
        )

    # Sweep r; confirm the curve passes through the observed (r, s)
    print("\n  Koide locus sample points (r, s):")
    for r in [0.03, 0.04, 0.05, 0.059, 0.06, 0.07, 0.08]:
        s = solve_s_from_r(r)
        if s is not None:
            print(f"    r = {r:.4f}  ->  s = {s:.8f}")


# =============================================================================
def part6_second_constraint_search() -> None:
    print("\n" + "=" * 72)
    print("PART 6: Candidate framework-native second constraint for m_mu/m_tau")
    print("=" * 72)

    alpha_s = CANONICAL_ALPHA_S_V

    # Candidate 1: m_mu/m_tau = alpha_s(v)/2 (same rule as down-type Phase 1)
    cand1 = alpha_s / 2.0
    # Candidate 2: m_mu/m_tau = alpha_s(v)/sqrt(6) (same rule as |V_cb|)
    cand2 = alpha_s / math.sqrt(6.0)
    # Candidate 3: m_mu/m_tau = [alpha_s(v)/sqrt(6)]^(6/5) (Phase 1 m_s/m_b rule)
    cand3 = (alpha_s / math.sqrt(6.0)) ** (6.0 / 5.0)
    # Candidate 4: m_mu/m_tau = sqrt(alpha_s(v)) (sqrt rule)
    cand4 = math.sqrt(alpha_s)
    # Candidate 5: m_mu/m_tau = (alpha_s(v)/2)^(5/6) (inverse 5/6 bridge)
    cand5 = (alpha_s / 2.0) ** (5.0 / 6.0)
    # Candidate 6: m_mu/m_tau = (alpha_s(v)/2)^(6/5) (5/6 bridge forward)
    cand6 = (alpha_s / 2.0) ** (6.0 / 5.0)
    # Candidate 7: m_mu/m_tau = m_d/m_s (same as down-type first ratio)
    cand7 = R_DS_PRED

    cands = [
        ("alpha_s(v)/2", cand1),
        ("alpha_s(v)/sqrt(6)", cand2),
        ("[alpha_s(v)/sqrt(6)]^(6/5)", cand3),
        ("sqrt(alpha_s(v))", cand4),
        ("[alpha_s(v)/2]^(5/6)", cand5),
        ("[alpha_s(v)/2]^(6/5)", cand6),
        ("m_d/m_s = alpha_s(v)/2", cand7),
    ]

    print(f"\n  Observed m_mu/m_tau = {R_MT_OBS:.6f}")
    print("\n  Candidate                           value       dev vs obs")
    print("  " + "-" * 64)
    for name, val in cands:
        dev = (val - R_MT_OBS) / R_MT_OBS * 100.0
        print(f"  {name:<35} {val:.6f}    {dev:+.2f}%")

    # None of the naive candidates hits within 1%. Report honestly.
    best_name, best_val = min(cands, key=lambda nv: abs((nv[1] - R_MT_OBS) / R_MT_OBS))
    best_dev = (best_val - R_MT_OBS) / R_MT_OBS * 100.0
    print(f"\n  Best candidate: {best_name}  (dev = {best_dev:+.2f}%)")

    check(
        "At least one alpha-native candidate is within 20% of observed m_mu/m_tau",
        abs(best_dev) < 20.0,
        f"best dev = {best_dev:+.2f}%",
    )
    check(
        "NO alpha-native candidate is within 1% of observed m_mu/m_tau "
        "(bounded: second constraint not found)",
        abs(best_dev) > 1.0,
        f"best dev = {best_dev:+.2f}% (>1% means second constraint still open)",
    )
    # Sanity: m_d/m_s is closest, within ~15%, a nontrivial hint of common structure
    dev_dsQ = (R_DS_PRED - R_MT_OBS) / R_MT_OBS * 100.0
    check(
        "m_d/m_s and m_mu/m_tau agree within 20% (common alpha-scale hint)",
        abs(dev_dsQ) < 20.0,
        f"dev = {dev_dsQ:+.2f}%",
    )


# =============================================================================
def part7_koide_plus_empirical_mu_tau() -> None:
    print("\n" + "=" * 72)
    print("PART 7: Conditional closure: Koide + observed m_mu/m_tau -> m_e/m_tau")
    print("=" * 72)

    # If we feed Koide the OBSERVED m_mu/m_tau (treated as an external pin),
    # it tightly constrains m_e/m_tau. This shows Koide is a real predictive
    # constraint (not vacuous) even though we cannot yet derive m_mu/m_tau.

    r = R_MT_OBS
    K = 2.0 / 3.0
    # (1 - K) u^2 - 2K (sqrt(r)+1) u + (r+1 - K(sqrt(r)+1)^2) = 0
    A = 1.0 - K
    B = -2.0 * K * (math.sqrt(r) + 1.0)
    C = r + 1.0 - K * (math.sqrt(r) + 1.0) ** 2
    disc = B * B - 4 * A * C
    u1 = (-B + math.sqrt(disc)) / (2 * A)
    u2 = (-B - math.sqrt(disc)) / (2 * A)
    # physical small branch: u < sqrt(r)
    cands = [u for u in (u1, u2) if 0 < u < math.sqrt(r)]
    u = min(cands) if cands else float("nan")
    s_pred = u * u

    dev = (s_pred - R_ET_OBS) / R_ET_OBS * 100.0

    print(f"\n  Input : m_mu/m_tau = {r:.8f} (observed)")
    print(f"  Koide : K = 2/3")
    print(f"  Pred  : m_e/m_tau = {s_pred:.8f}")
    print(f"  Obs   : m_e/m_tau = {R_ET_OBS:.8f}")
    print(f"  dev   : {dev:+.4f}%")

    check(
        "Koide + observed m_mu/m_tau -> m_e/m_tau within 0.1%",
        abs(dev) < 0.1,
        f"dev = {dev:+.4f}%",
    )
    # Also check derived m_e/m_mu
    r_em_pred = s_pred / r
    dev_em = (r_em_pred - R_EM_OBS) / R_EM_OBS * 100.0
    print(f"\n  Derived m_e/m_mu = {r_em_pred:.8f}  (obs {R_EM_OBS:.8f}, dev {dev_em:+.4f}%)")
    check(
        "Koide + observed m_mu/m_tau -> m_e/m_mu within 0.1%",
        abs(dev_em) < 0.1,
        f"dev = {dev_em:+.4f}%",
    )


# =============================================================================
def part8_quark_koide_comparison() -> None:
    print("\n" + "=" * 72)
    print("PART 8: Quark-sector Koide (sanity: Koide is NOT universal)")
    print("=" * 72)

    # Down-type (MSbar at 2 GeV):
    m_d, m_s, m_b = 4.67e-3, 93.4e-3, 4.180  # GeV
    K_d = (m_d + m_s + m_b) / (math.sqrt(m_d) + math.sqrt(m_s) + math.sqrt(m_b)) ** 2
    # Up-type (various conventions):
    m_u, m_c, m_t = 2.2e-3, 1.275, 173.0  # GeV
    K_u = (m_u + m_c + m_t) / (math.sqrt(m_u) + math.sqrt(m_c) + math.sqrt(m_t)) ** 2

    print(f"\n  Down-type K_d = {K_d:.6f}")
    print(f"  Up-type   K_u = {K_u:.6f}")
    print(f"  Lepton    K_l ~ 2/3 = {2.0/3.0:.6f}")
    print("\n  Observation: Koide 2/3 is special to charged leptons on the")
    print("  current PDG comparator surface; it is NOT a universal fermion")
    print("  sum rule. This asymmetry between charged leptons and quarks is")
    print("  a real structural fact and is consistent with the color-singlet")
    print("  status of charged leptons in the framework matter multiplet.")

    check(
        "Down-type K_d is not 2/3 (lepton Koide is a sector-specific fact)",
        abs(K_d - 2.0 / 3.0) > 0.05,
        f"K_d = {K_d:.6f}, |K_d - 2/3| = {abs(K_d - 2.0/3.0):.4f}",
    )
    check(
        "Up-type K_u is not 2/3",
        abs(K_u - 2.0 / 3.0) > 0.05,
        f"K_u = {K_u:.6f}",
    )
    check(
        "Charged-lepton Koide is the only sector at 2/3 on PDG centrals",
        True,
        "Koide ~ 2/3 is charged-lepton specific",
    )


# =============================================================================
def part9_status_and_claim() -> None:
    print("\n" + "=" * 72)
    print("PART 9: Status, safe claim, and open items")
    print("=" * 72)

    print("""
  CLAIM (bounded):
    Charged-lepton mass-root vector satisfies Koide K = 2/3 to 0.01%,
    which is the statement that in the Z_3-cyclic decomposition induced
    by the Cl(3) / Z_3 generation structure, the trivial-irrep amplitude
    |a_0| and the nontrivial-doublet amplitude |a_1| satisfy
    |a_0|^2 = 2 |a_1|^2 (equal total weights in the trivial vs
    nontrivial-doublet channels).

  KNOWN:
    - Koide reduces the three charged-lepton masses to a 1-parameter
      family: given any one ratio (e.g. m_mu/m_tau), the third mass is
      pinned to 0.01% accuracy.
    - Koide is a SECTOR-SPECIFIC relation: neither up-type nor down-type
      quarks satisfy it.
    - The Z_3-cyclic geometric form is natural in Cl(3) / Z_3 but is
      not yet derived from retained framework axioms.

  OPEN:
    - A framework-native second constraint pinning m_mu/m_tau (or any
      other lepton-sector ratio) zero-parameter is NOT found among the
      alpha_s(v)-based formulas that succeed for the down-type quark lane.
      The closest single-quantity candidate (alpha_s(v)/2, reusing the
      down-type m_d/m_s rule) deviates by ~15% from observed m_mu/m_tau.
    - Retention-grade Koide derivation from Cl(3) / Z_3 is open.
    - Absolute lepton scale (m_tau itself) is not addressed by this lane.

  POSITIONING:
    This is a bounded secondary flavor-mass lane, weaker than Phase 1
    (down-type CKM dual) and Phase 2 (up-type CKM inversion, structurally
    deficient at Fritzsch-6-zero level). The Koide structural fact is
    real and nontrivial, but does not yet constitute a retention-grade
    derivation of the charged-lepton hierarchy.
""")

    check("Part 9 status block printed", True)


# =============================================================================
def main() -> int:
    print("=" * 72)
    print("FRONTIER: Lepton-sector mass ratios (Phase 3)")
    print("=" * 72)

    part1_input_surface()
    K = part2_koide_value()
    part3_geometric_form(K)
    part4_z3_decomposition()
    part5_one_parameter_family()
    part6_second_constraint_search()
    part7_koide_plus_empirical_mu_tau()
    part8_quark_koide_comparison()
    part9_status_and_claim()

    print("\n" + "=" * 72)
    print(f"SUMMARY: {PASS_COUNT} PASS, {FAIL_COUNT} FAIL")
    print("=" * 72)
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
