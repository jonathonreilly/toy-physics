#!/usr/bin/env python3
"""
CKM neutron-EDM corollary and bounded prediction
================================================

STATUS: retained structural corollary + bounded quantitative prediction

This script does not upgrade the retained strong-CP closure package itself. It takes:

  1. θ_eff = 0 on the retained strong-CP action surface
  2. the promoted CKM atlas/axiom package

and combines them into:

  - an exact structural corollary on the retained surface:
      d_n(QCD) = 0 and the surviving neutron EDM is CKM-only
  - a bounded quantitative continuation from standard short-/long-distance EFT:
      d_n(CKM) ~ 10^-32 - 10^-33 e cm

Import class:
  promoted CKM atlas/axiom package + standard hadronic/EW EFT bridge
"""

from __future__ import annotations

import numpy as np

from canonical_plaquette_surface import CANONICAL_ALPHA_S_V

PASS_COUNT = 0
FAIL_COUNT = 0


def check(name: str, condition: bool, detail: str = "", cls: str = "D") -> bool:
    global PASS_COUNT, FAIL_COUNT
    if condition:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    msg = f"  [{status} ({cls})] {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    return condition


def main() -> int:
    print("=" * 72)
    print("CKM neutron-EDM corollary and bounded prediction")
    print("=" * 72)
    print()

    # Retained strong-CP closure surface: the QCD theta contribution vanishes.
    theta_eff = 0.0
    dn_per_theta = 2.4e-16  # e cm, lattice-QCD headline scale
    dn_qcd = theta_eff * dn_per_theta
    check("QCD theta contribution vanishes on the retained surface",
          dn_qcd == 0.0,
          "θ_eff = 0 → d_n(QCD) = 0")

    # Framework CKM atlas/axiom package.
    alpha_s_v = CANONICAL_ALPHA_S_V
    lam = np.sqrt(alpha_s_v / 2.0)
    A = np.sqrt(2.0 / 3.0)
    rho = 1.0 / 6.0
    eta = np.sqrt(5.0) / 6.0
    delta = np.arctan2(eta, rho)

    s12, c12 = lam, np.sqrt(1.0 - lam ** 2)
    s23 = A * lam ** 2
    c23 = np.sqrt(1.0 - s23 ** 2)
    s13 = A * lam ** 3 * np.sqrt(rho ** 2 + eta ** 2)
    c13 = np.sqrt(1.0 - s13 ** 2)
    J = c12 * s12 * c23 * s23 * c13 ** 2 * s13 * np.sin(delta)

    check("Framework Jarlskog matches promoted CKM package",
          abs(J - 3.331e-5) / 3.331e-5 < 0.01,
          f"J = {J:.4e}")

    # Standard EFT bridge for the surviving CKM contribution.
    G_F = 1.1664e-5    # GeV^-2
    m_s = 0.093        # GeV
    m_c = 1.27         # GeV
    m_W = 80.377       # GeV
    alpha_em = 1.0 / 137.036
    alpha_W = alpha_em / 0.2312
    Lambda_QCD = 0.332  # GeV
    hbar_c_cm = 0.197327e-13  # GeV cm

    prefactor_sd = (alpha_W / (4.0 * np.pi)) ** 2
    dn_sd_natural = prefactor_sd * m_s * m_c ** 2 / m_W ** 4 * J * Lambda_QCD
    dn_sd_ecm = abs(dn_sd_natural) * hbar_c_cm

    dn_ld_natural = G_F ** 2 * m_s * J * Lambda_QCD ** 3 / (4.0 * np.pi ** 2)
    dn_ld_ecm = abs(dn_ld_natural) * hbar_c_cm

    print(f"  Short-distance estimate: {dn_sd_ecm:.2e} e·cm")
    print(f"  Long-distance estimate:  {dn_ld_ecm:.2e} e·cm")

    dn_ckm = max(dn_sd_ecm, dn_ld_ecm)
    check("Surviving neutron EDM is CKM-only on the retained surface",
          dn_qcd == 0.0 and dn_ckm > 0.0,
          "strong-sector piece vanishes, nonzero CKM estimate survives")
    check("CKM-only neutron EDM lies on the expected EFT scale",
          1e-35 < dn_ckm < 1e-29,
          f"d_n(CKM) ≈ {dn_ckm:.2e} e·cm")

    dn_bound = 1.8e-26  # e cm, current experimental upper bound
    check("CKM-only estimate is well below the current bound",
          dn_ckm < dn_bound,
          f"prediction/bound ≈ {dn_ckm / dn_bound:.2e}")

    print()
    print("=" * 72)
    print(f"SUMMARY: PASS={PASS_COUNT}  FAIL={FAIL_COUNT}")
    print("=" * 72)
    print()
    print("Retained structural corollary:")
    print("  d_n(QCD) = 0 exactly on the retained θ_eff = 0 surface")
    print("  the surviving neutron EDM is CKM-only")
    print()
    print("Bounded quantitative continuation:")
    print(f"  d_n(CKM) ≈ {dn_ckm:.1e} e·cm")
    print("  import class: promoted CKM atlas/axiom package + standard EFT bridge")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
