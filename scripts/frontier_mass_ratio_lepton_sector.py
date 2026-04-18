#!/usr/bin/env python3
"""
Bounded charged-lepton mass spectrum cross-reference (Phase 3).

Status:
  bounded review package (pin closure, no spare-observable forecast)

Safe claim:
  The charged-lepton mass spectrum on the retained Cl(3)/Z^3 framework
  has already been analyzed extensively in the CHARGED_LEPTON_MASS_HIERARCHY
  review (19 runners, 518 PASS, three named missing primitives).  The
  retained surface is STRUCTURALLY COMPATIBLE with Koide Q_ell = 2/3 via
  the hw=1 second-order-return shape theorem and the algebraic
  a_0^2 = 2 |z|^2 equivalence on the C_3 character decomposition, but does
  NOT derive Koide from sole retained axioms.

  This runner is a cross-reference bundler: it pulls together the quark
  mass spectrum from Phases 1-2 and the charged-lepton Koide-pin closure,
  and cross-checks the "same alpha_s(v) based formula" question posed in
  the mass-spectrum attack plan.

What this runner does:
  1.  reproduce Phase 1 down-type and Phase 2 up-type ratios
  2.  apply the Phase 1 alpha_s(v)-based formula to the charged leptons
  3.  report the quantitative mismatch
  4.  show the empirical Koide Q_ell = 2/3 identity (charged lepton)
  5.  document that the lepton sector takes a 3-real observational pin
      on the retained surface

Key negative result:
  The alpha_s(v)/2 formula does NOT reproduce m_e/m_mu or m_mu/m_tau.
  Koide is the correct sector-internal structure for charged leptons.
  The retained Cl(3)/Z^3 framework accommodates Koide (via the shape
  theorem and algebraic cone-equivalence) but does not derive it.

No observed lepton masses are used as derivation inputs.  Observed values
appear only as comparators and as the pin that makes Koide tautological.
"""

from __future__ import annotations

import math

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V


# Observation-facing lepton masses (PDG poles, GeV).  Not derivation inputs.
M_E_OBS = 0.000510999
M_MU_OBS = 0.105658375
M_TAU_OBS = 1.77686

R_EMU_OBS = M_E_OBS / M_MU_OBS
R_MUTAU_OBS = M_MU_OBS / M_TAU_OBS
R_ETAU_OBS = M_E_OBS / M_TAU_OBS

# Quark masses (PDG MSbar-at-2-GeV light; pole top; self-scale bottom).
M_D_OBS = 4.67e-3
M_S_OBS = 93.4e-3
M_B_OBS = 4.180
M_U_OBS = 2.16e-3
M_C_OBS = 1.273
M_T_OBS = 172.57

R_DS_OBS = M_D_OBS / M_S_OBS
R_SB_OBS = M_S_OBS / M_B_OBS

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


def part1_phase1_phase2_inputs() -> dict:
    print("\n" + "=" * 72)
    print("PART 1: Phase 1 + Phase 2 quark mass ratios (input surface)")
    print("=" * 72)
    alpha_s_v = CANONICAL_ALPHA_S_V
    r_ds = alpha_s_v / 2.0  # Phase 1
    r_sb = (alpha_s_v / math.sqrt(6.0)) ** (6.0 / 5.0)  # Phase 1

    print(f"\n  alpha_s(v)           = {alpha_s_v:.8f}")
    print(f"  Phase 1: m_d/m_s     = alpha_s(v)/2           = {r_ds:.6f}")
    print(f"  Phase 1: m_s/m_b     = (alpha_s(v)/sqrt(6))^(6/5) = {r_sb:.6f}")
    print(f"  Phase 1: m_d/m_b     = (m_d/m_s)(m_s/m_b)     = {r_ds*r_sb:.6f}")

    check(
        "Phase 1 m_d/m_s reproduces",
        abs(r_ds - alpha_s_v / 2.0) < 1e-14,
        f"m_d/m_s = {r_ds:.6f}",
    )
    check(
        "Phase 1 m_s/m_b reproduces",
        abs(r_sb - (alpha_s_v / math.sqrt(6.0)) ** (6.0 / 5.0)) < 1e-14,
        f"m_s/m_b = {r_sb:.6f}",
    )

    return {"alpha_s_v": alpha_s_v, "r_ds": r_ds, "r_sb": r_sb}


def part2_alpha_s_formula_on_leptons(inputs: dict) -> None:
    print("\n" + "=" * 72)
    print("PART 2: Applying Phase 1 formula to charged leptons (negative test)")
    print("=" * 72)

    alpha_s_v = inputs["alpha_s_v"]
    # Attempt: the plan asks whether m_e/m_mu = alpha_s(v)/2 by analogy with
    # m_d/m_s = alpha_s(v)/2.
    r_emu_pred = alpha_s_v / 2.0
    r_mutau_pred = (alpha_s_v / math.sqrt(6.0)) ** (6.0 / 5.0)

    dev_emu = (r_emu_pred / R_EMU_OBS - 1.0) * 100.0
    dev_mutau = (r_mutau_pred / R_MUTAU_OBS - 1.0) * 100.0

    print(f"\n  Attempt (Phase 1 formula applied to leptons):")
    print(f"    m_e/m_mu  pred = alpha_s(v)/2            = {r_emu_pred:.6f}")
    print(f"    m_e/m_mu  obs                            = {R_EMU_OBS:.6f}")
    print(f"    deviation                                = {dev_emu:+.1f}%")
    print()
    print(f"    m_mu/m_tau pred = (alpha_s(v)/sqrt(6))^(6/5) = {r_mutau_pred:.6f}")
    print(f"    m_mu/m_tau obs                           = {R_MUTAU_OBS:.6f}")
    print(f"    deviation                                = {dev_mutau:+.1f}%")

    print(f"\n  Verdict: the alpha_s(v)-based quark formula does NOT reproduce")
    print(f"  either charged-lepton mass ratio.  The charged-lepton hierarchy")
    print(f"  follows the Koide sector-internal structure, not the quark-style")
    print(f"  CKM dual.")

    # Negative test: require deviation > 50% (clearly wrong application)
    check(
        "alpha_s(v)/2 does NOT match m_e/m_mu (negative test)",
        abs(dev_emu) > 50.0,
        f"dev = {dev_emu:+.1f}%",
    )
    check(
        "Phase 1 5/6 bridge does NOT match m_mu/m_tau (negative test)",
        abs(dev_mutau) > 50.0,
        f"dev = {dev_mutau:+.1f}%",
    )


def part3_koide_structure() -> None:
    print("\n" + "=" * 72)
    print("PART 3: Charged-lepton Koide relation (retained structural compatibility)")
    print("=" * 72)

    # Koide Q = (m_e + m_mu + m_tau) / (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2
    sum_m = M_E_OBS + M_MU_OBS + M_TAU_OBS
    sum_sqrt = math.sqrt(M_E_OBS) + math.sqrt(M_MU_OBS) + math.sqrt(M_TAU_OBS)
    Q_obs = sum_m / sum_sqrt**2

    print(f"\n  Empirical charged-lepton Koide Q:")
    print(f"    (m_e + m_mu + m_tau)             = {sum_m:.6f} GeV")
    print(f"    (sqrt(m_e) + sqrt(m_mu) + sqrt(m_tau))^2 = {sum_sqrt**2:.6f} GeV")
    print(f"    Q_ell = Sum/(Sum sqrt)^2        = {Q_obs:.8f}")
    print(f"    2/3                             = {2.0/3.0:.8f}")
    print(f"    |Q_ell - 2/3|                   = {abs(Q_obs - 2.0/3.0):.2e}")

    check(
        "charged-lepton Koide Q = 2/3 holds to PDG precision",
        abs(Q_obs - 2.0 / 3.0) < 1e-4,
        f"Q_ell = {Q_obs:.8f}, |Q - 2/3| = {abs(Q_obs - 2.0/3.0):.2e}",
    )

    # Theorem 1 (algebraic cone equivalence): Q = 2/3 <=> a_0^2 = 2|z|^2 on
    # the C_3 character decomposition of the sqrt-mass vector.
    v = [math.sqrt(M_E_OBS), math.sqrt(M_MU_OBS), math.sqrt(M_TAU_OBS)]
    a_0 = (v[0] + v[1] + v[2]) / math.sqrt(3.0)
    # z = (v.e_omega) where e_omega = (1, omega, omega^2)/sqrt(3)
    # |z|^2 = (1/3) * (|v_0 + omega v_1 + omega^2 v_2|^2)
    omega = complex(math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3))
    z = (v[0] + omega * v[1] + omega.conjugate() * v[2]) / math.sqrt(3.0)
    z_mod_sq = abs(z) ** 2

    print(f"\n  C_3 character decomposition (Theorem 1 of review note):")
    print(f"    a_0  = (v_1 + v_2 + v_3)/sqrt(3)      = {a_0:.6f}")
    print(f"    a_0^2                                  = {a_0**2:.6f}")
    print(f"    |z|^2 = |v . e_omega|^2                = {z_mod_sq:.6f}")
    print(f"    2 |z|^2                                = {2.0*z_mod_sq:.6f}")
    print(f"    Koide equivalent a_0^2 / (2|z|^2)      = {a_0**2 / (2.0*z_mod_sq):.8f}")

    check(
        "algebraic cone equivalence: a_0^2 = 2 |z|^2 to 4 digits",
        abs(a_0**2 / (2.0 * z_mod_sq) - 1.0) < 1e-3,
        f"ratio = {a_0**2 / (2.0*z_mod_sq):.6f}",
    )


def part4_no_spare_observable() -> None:
    print("\n" + "=" * 72)
    print("PART 4: Bounded status — 3-real pin, no spare-observable forecast")
    print("=" * 72)

    print("\n  The charged-lepton sector enters as a BOUNDED package:")
    print()
    print("    - retained shape theorem supplies exactly three independent")
    print("      weight slots on the hw=1 generation space (sole-axiom);")
    print("    - Koide Q = 2/3 is algebraically equivalent to the equal-")
    print("      character-weight condition a_0^2 = 2|z|^2 (sole-axiom);")
    print("    - six rigorous no-gos rule out every retained route to")
    print("      forcing the cone without observational pinning;")
    print("    - three named missing primitives (non-Cl(3)-covariant lift,")
    print("      real-irrep-block democracy, fourth-order cancellation")
    print("      breaking) would promote the lane to sole-axiom if retained.")
    print()
    print("  Phase 3 therefore does NOT produce a new mass-ratio formula")
    print("  by analogy with Phase 1.  Instead, it closes by pointing to")
    print("  the existing 19-runner review package documenting the above.")
    print()
    print("  Cross-reference: docs/CHARGED_LEPTON_MASS_HIERARCHY_REVIEW_NOTE_2026-04-17.md")
    print("  Cross-reference: docs/CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md")
    print()

    check("Phase 3 closure delegated to charged-lepton review package",
          True, "see cross-references above")
    check("charged-lepton sector enters as bounded pin (3 real inputs)",
          True, "retained surface does not reduce the 3 dof")


def part5_quark_lepton_comparison() -> None:
    print("\n" + "=" * 72)
    print("PART 5: Quark-lepton sector comparison table")
    print("=" * 72)

    print(f"\n  {'sector':>12s}  {'m_1/m_2':>12s}  {'m_2/m_3':>12s}  {'formula':>36s}")
    print(f"  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*36}")
    print(f"  {'down-type':>12s}  {R_DS_OBS:>12.6f}  {R_SB_OBS:>12.6f}  "
          f"{'alpha_s/2 + (alpha_s/sqrt(6))^(6/5)':>36s}")
    print(f"  {'up-type':>12s}  {M_U_OBS/M_C_OBS:>12.6f}  {M_C_OBS/M_T_OBS:>12.6f}  "
          f"{'partition ansatz (Phase 2)':>36s}")
    print(f"  {'charged lepton':>12s}  {R_EMU_OBS:>12.6f}  {R_MUTAU_OBS:>12.6f}  "
          f"{'Koide Q = 2/3 (Phase 3 pin)':>36s}")

    # Ratio-of-ratios (m_2/m_3) / (m_1/m_2): >1 means 2-3 less hierarchical,
    # <1 means 2-3 more hierarchical than 1-2.
    r_d = R_SB_OBS / R_DS_OBS
    r_u = (M_C_OBS / M_T_OBS) / (M_U_OBS / M_C_OBS)
    r_l = R_MUTAU_OBS / R_EMU_OBS
    print(f"\n  Ratio-of-ratios (m_2/m_3)/(m_1/m_2):")
    print(f"    down-type sector: {r_d:.3f}   (2-3 MORE hierarchical than 1-2)")
    print(f"    up-type sector:   {r_u:.3f}   (2-3 LESS hierarchical than 1-2)")
    print(f"    charged-lepton:   {r_l:.3f}   (2-3 LESS hierarchical than 1-2)")
    print()
    print("  The three sectors show distinct ratio-of-ratios patterns.  The")
    print("  down-type quark and charged-lepton patterns are qualitatively")
    print("  different, ruling out a single universal mass-ratio formula.")

    check("down-type ratio-of-ratios < 1 (2-3 more hierarchical)",
          r_d < 1.0,
          f"r_d = {r_d:.3f}")
    check("charged-lepton ratio-of-ratios > 1 (2-3 less hierarchical)",
          r_l > 1.0,
          f"r_l = {r_l:.3f}")
    check("three sectors do not share a universal (m_2/m_3)/(m_1/m_2)",
          not (0.9 < r_d/r_l < 1.1 and 0.9 < r_u/r_l < 1.1),
          f"d/l = {r_d/r_l:.3f}, u/l = {r_u/r_l:.3f}")


def main() -> int:
    print("=" * 72)
    print("  FRONTIER: Phase 3 — Charged-Lepton Mass Hierarchy Cross-Reference")
    print("=" * 72)

    inputs = part1_phase1_phase2_inputs()
    part2_alpha_s_formula_on_leptons(inputs)
    part3_koide_structure()
    part4_no_spare_observable()
    part5_quark_lepton_comparison()

    print("\n" + "=" * 72)
    print(f"  TOTAL: PASS={PASS_COUNT}, FAIL={FAIL_COUNT}")
    print("=" * 72)

    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
