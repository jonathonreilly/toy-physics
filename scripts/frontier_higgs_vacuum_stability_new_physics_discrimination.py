"""Higgs + vacuum stability discrimination tests vs SM.

Verifies the discrimination claims of
`docs/HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md`:

1. Framework's bounded internal y_t(v) = 0.918 vs SM extraction 0.940;
   compute current tension level including the stated framework systematic.
2. Framework's m_H predictions (119.8/125.1/129.7 GeV) vs PDG 125.25 GeV;
   identify which versions are within bounded systematic.
3. Vacuum stability framework prediction vs SM metastability; identify
   the y_t threshold that discriminates.
4. Future experiment thresholds (HL-LHC, FCC-ee, FCC-hh, linear collider)
   for falsification.

This is NOT a derivation runner; it's a DISCRIMINATION CALCULATOR that
quantifies the framework's testable claims against current/future SM
precision.

Run with: .venv/bin/python3 scripts/frontier_higgs_vacuum_stability_new_physics_discrimination.py
"""

from __future__ import annotations

import math
import sys


def main() -> int:
    print("=" * 78)
    print("Higgs + Vacuum Stability — New-Physics Discrimination Tests")
    print("Source: docs/HIGGS_VACUUM_STABILITY_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md")
    print("=" * 78)

    # ----- Section 1: y_t discrimination -----
    print("\n--- Section 1: y_t(v) discrimination ---")
    yt_framework = 0.918
    yt_framework_systematic = 0.03  # ~3% QFP/RGE-surrogate per ASSUMPTION_DERIVATION_LEDGER
    yt_sm_central = 0.940
    yt_sm_uncertainty = 0.010  # current PDG-extraction uncertainty
    yt_stability_boundary = 0.93  # Buttazzo 2013 NNLO: stability boundary at fixed m_H=125.25
    delta_yt = yt_sm_central - yt_framework
    combined_sigma = math.sqrt(yt_sm_uncertainty**2 + (yt_framework * yt_framework_systematic)**2)
    tension_sigma = delta_yt / combined_sigma
    stability_boundary_sigma = (yt_sm_central - yt_stability_boundary) / yt_sm_uncertainty
    future_uncertainty_for_5sigma_boundary = (yt_sm_central - yt_stability_boundary) / 5.0

    print(f"  Framework y_t(v) = {yt_framework} ± {yt_framework * yt_framework_systematic:.4f}")
    print(f"  SM extraction y_t(v) = {yt_sm_central} ± {yt_sm_uncertainty}")
    print(f"  Difference: {delta_yt:.4f}")
    print(f"  Combined uncertainty: {combined_sigma:.4f}")
    print(f"  Current framework-vs-observation tension: {tension_sigma:.2f}σ")
    print(f"  Current distance above stability boundary y_t≈{yt_stability_boundary}: "
          f"{stability_boundary_sigma:.2f}σ on the observational error alone")
    print()
    print("  Discrimination thresholds:")
    print("    Stability claim falsified if the measured y_t lower 5σ bound exceeds "
          f"the stability boundary y_t≈{yt_stability_boundary}.")
    print(f"    If the central value remains {yt_sm_central}, this needs σ_y_t < "
          f"{future_uncertainty_for_5sigma_boundary:.4f}.")
    print("    Direct y_t=0.918 discrimination also requires narrowing the current "
          "3% framework-side transport systematic.")

    # ----- Section 2: m_H discrimination -----
    print("\n--- Section 2: m_H discrimination ---")
    mH_pdg = 125.25
    mH_pdg_uncertainty = 0.17

    mH_framework_versions = {
        "Naive m_H = v/(2u_0) (HIGGS_MASS_FROM_AXIOM)": 140.3,
        "Color-corrected 2-loop CW": 119.8,
        "Full 3-loop CW (current canonical)": 125.1,
        "Stability-boundary CW": 129.7,
    }

    print(f"  PDG m_H = {mH_pdg} ± {mH_pdg_uncertainty} GeV")
    for label, mH in mH_framework_versions.items():
        delta = abs(mH - mH_pdg)
        rel = delta / mH_pdg * 100
        within_5pct = abs(rel) < 5
        marker = "✓ within 5%" if within_5pct else "✗ outside 5%"
        print(f"    {label}: {mH} GeV ({rel:+.1f}%, {marker})")
    print()
    print("  Honest assessment: the framework has multiple m_H predictions across")
    print("  derivation routes. The 3-loop CW value (125.1 GeV) is closest to PDG and")
    print("  is the framework's canonical current value, but the version conflict reflects")
    print("  bounded systematic in the underlying y_t/RGE bridge chain.")

    # ----- Section 3: vacuum stability -----
    print("\n--- Section 3: Vacuum stability discrimination ---")
    print(f"  SM stability boundary (Buttazzo et al 2013, NNLO): y_t ≲ {yt_stability_boundary}")
    print(f"  Framework y_t(v) = {yt_framework}: {'STABLE' if yt_framework < yt_stability_boundary else 'METASTABLE'}")
    print(f"  SM extraction y_t = {yt_sm_central}: {'STABLE' if yt_sm_central < yt_stability_boundary else 'METASTABLE'}")
    print()
    print("  Bounded framework package predicts an absolutely stable EW vacuum.")
    print("  SM with current y_t extraction predicts METASTABLE (lifetime >> Hubble; observationally OK).")
    print("  Discrimination: a precision y_t measurement whose lower 5σ bound exceeds")
    print("  y_t≈0.93 would falsify the framework's stability claim.")

    # ----- Section 4: Experimental timeline -----
    print("\n--- Section 4: Discrimination experiment timeline ---")
    experiments = [
        ("HL-LHC (2030+)", "δm_t ~ 100 MeV; λ_3 to 50%", "y_t to <1%; stability via λ(v)"),
        ("FCC-ee (proposed 2040s)", "δm_t ~ 25 MeV (threshold); m_H to 4 MeV", "y_t to ~0.1%; m_H to 0.003%"),
        ("FCC-hh (proposed 2050s)", "λ_3 to 5%", "direct stability via λ shape"),
        ("Linear collider (ILC/CLIC)", "δm_t ~ 30 MeV; m_H to 14 MeV", "y_t / stability"),
    ]
    for exp, prec, disc in experiments:
        print(f"  {exp}: {prec}")
        print(f"    → discriminates: {disc}")

    # ----- Section 5: Discrimination summary -----
    print("\n--- Section 5: Discrimination summary ---")
    print("  Framework's distinguishing claims (relative to SM):")
    print()
    print(f"  D1. Vacuum is absolutely stable (vs SM metastable)")
    print(f"  D2. y_t(v) = 0.918 (vs SM extraction 0.940; current {tension_sigma:.2f}σ "
          "including framework systematic)")
    print(f"  D3. m_H ∈ [119.8, 129.7] GeV (vs SM free param; PDG 125.25)")
    print("  D4. λ(M_Pl) = 0 on the conditional CW-boundary surface (vs SM extracted ~ 0)")
    print()
    print(f"  Currently: {tension_sigma:.2f}σ tension between framework y_t(v) and SM extraction")
    print("  after including the stated 3% framework systematic.")
    print("  Near-term precision can falsify the stability claim if the lower 5σ")
    print("  observational bound rises above the y_t≈0.93 stability boundary.")
    print("  Direct y_t discrimination also needs a narrower audited framework-side systematic.")
    print()
    print("  This lane provides a bounded, current-testable discrimination surface against the SM.")

    print("\n" + "=" * 78)
    print("Block 01 discrimination tests complete.")
    print()
    print("Honest assessment:")
    print("  - Framework has 4 distinguishing predictions in this lane")
    print(f"  - Currently {tension_sigma:.2f}σ tension on y_t once framework systematic is included")
    print("  - Future precision can falsify the stability boundary claim if observational")
    print("    errors shrink enough while the central value stays above y_t≈0.93")
    print("  - Vacuum stability is the binary claim with cleanest discrimination")
    print()
    print("This makes the Higgs/y_t/stability lane a bounded beyond-SM discrimination")
    print("surface, contingent on future precision and a narrower framework transport bound.")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
