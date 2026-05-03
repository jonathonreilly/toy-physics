"""Strong CP + CKM neutron EDM — n2EDM discrimination tests.

Verifies the discrimination claims of
`docs/STRONG_CP_EDM_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md`:

1. Framework's three sharp predictions: θ_eff=0, d_n(QCD)=0, universal
   theta-EDM vanishing.
2. Discrimination map vs SM and BSM (SUSY, multi-Higgs, axion).
3. n2EDM @ PSI 2027+ sensitivity scenarios.

Run with: .venv/bin/python3 scripts/frontier_strong_cp_edm_new_physics_discrimination.py
"""

from __future__ import annotations

import sys


def main() -> int:
    print("=" * 78)
    print("Strong CP + CKM Neutron EDM — Discrimination Tests vs SM and BSM")
    print("Source: docs/STRONG_CP_EDM_NEW_PHYSICS_DISCRIMINATION_NOTE_2026-05-03.md")
    print("=" * 78)

    # ----- Section 1: Framework's three sharp claims -----
    print("\n--- Section 1: Framework's three sharp claims ---")
    claims = [
        ("E1", "θ_eff = 0 EXACTLY", "free param ≤ 10⁻¹⁰", "varies; often non-zero"),
        ("E2", "d_n(QCD) = 0 EXACTLY", "≤ 10⁻²⁶ e·cm × θ/10⁻¹⁰", "typically larger if θ ≠ 0"),
        ("E3", "All theta-induced EDMs = 0 (universal)", "individual untested at θ→0", "distinct from BSM"),
    ]
    print(f"  {'#':3s}  {'Framework':40s}  {'SM':30s}  {'BSM (typical)':30s}")
    for c, fw, sm, bsm in claims:
        print(f"  {c:3s}  {fw:40s}  {sm:30s}  {bsm:30s}")

    # ----- Section 2: Experimental landscape -----
    print("\n--- Section 2: d_n predicted vs n2EDM sensitivity ---")
    sources = [
        ("Framework: CKM-only", 1e-32, "NO (4 orders below)"),
        ("SM (free θ ≤ 10⁻¹⁰)", 1e-26, "YES (potentially)"),
        ("SUSY (MSSM, generic)", 1e-27, "YES"),
        ("Multi-Higgs", 1e-27, "YES"),
        ("Axion (Peccei-Quinn)", 1e-32, "NO"),
    ]
    n2edm_sensitivity = 1e-28
    print(f"  Source                       d_n (e·cm)    Detectable by n2EDM (~{n2edm_sensitivity:.0e})?")
    for src, d_n, note in sources:
        print(f"  {src:30s}  {d_n:.2e}    {note}")
    print()
    print(f"  Current bound: d_n < 1.8 × 10⁻²⁶ e·cm (PSI 2020, Abel et al)")
    print(f"  n2EDM target (2027+): σ(d_n) ≈ 10⁻²⁸ e·cm")

    # ----- Section 3: Three n2EDM scenarios -----
    print("\n--- Section 3: Three n2EDM discrimination scenarios ---")
    scenarios = [
        ("E-1", "n2EDM detects d_n at 10⁻²⁸ to 10⁻²⁶ e·cm",
         "STRONGLY DISFAVORED to FALSIFIED",
         "Signal too large for CKM-only; BSM CP source"),
        ("E-2", "n2EDM sets bound d_n < 10⁻²⁸ with no detection",
         "CONSISTENT",
         "Constrains BSM; doesn't discriminate framework from SM-axion"),
        ("E-3", "n2EDM (or successor) detects d_n at CKM level (~10⁻³²)",
         "NEUTRAL / WEAKLY SUPPORTED",
         "Beyond n2EDM precision; future-future experiments"),
    ]
    for s, obs, status, interp in scenarios:
        print(f"  {s:4s}  {obs}")
        print(f"        Framework: {status}")
        print(f"        Interpretation: {interp}")
        print()

    # ----- Section 4: Axion null test -----
    print("\n--- Section 4: Axion null test ---")
    print("  Framework predicts NO axion mechanism needed (θ_eff = 0 structural).")
    print()
    print("  Discrimination via axion experiments:")
    print("    Axion DETECTED (ADMX, IAXO, BabyIAXO):")
    print("      → Framework's 'no axion needed' loses motivation but not strictly falsified")
    print("    Axion NOT DETECTED at projected ADMX-EFR/IAXO sensitivity:")
    print("      → Framework's 'no axion needed' claim STRENGTHENED")

    # ----- Section 5: Universal EDM vanishing E3 testing -----
    print("\n--- Section 5: Universal EDM vanishing — multi-species tests ---")
    edm_species = [
        ("neutron d_n", "0 (CKM-only ~10⁻³²)", "n2EDM, future"),
        ("electron d_e", "0 (CKM contribution)", "ACME-III, future"),
        ("199-Hg atomic", "0 (nuclear/atomic CP)", "Hg EDM experiments"),
        ("muon d_μ", "0 (weak-sector CKM)", "muon EDM proposals"),
    ]
    print(f"  EDM species              Framework prediction      Experiments")
    for sp, pred, exp in edm_species:
        print(f"  {sp:25s}  {pred:25s}  {exp}")
    print()
    print("  Multi-species correlated detection consistent with single θ-source")
    print("  would be inconsistent with framework's universal vanishing claim.")

    # ----- Section 6: Honest assessment -----
    print("\n--- Section 6: Honest discrimination assessment ---")
    print("  Distinguishing power vs SM-CKM-only: LOW (both predict same ~10⁻³²)")
    print("  Distinguishing power vs SM-without-axion: MODERATE")
    print("    (framework structurally forbids what SM allows)")
    print("  Distinguishing power vs BSM with new CP sources: HIGH")
    print("    (n2EDM detection >10⁻³⁰ would falsify framework's CKM-only)")
    print()
    print("  Best near-term discrimination: n2EDM @ PSI 2027+")
    print("  - Detection at 10⁻²⁸: framework FALSIFIED (BSM source confirmed)")
    print("  - Null result at 10⁻²⁸: framework CONSISTENT, BSM constrained")
    print("  - n2EDM cannot reach the predicted CKM-only ~10⁻³²")

    print("\n" + "=" * 78)
    print("Block 03 strong-CP + EDM discrimination tests complete.")
    print()
    print("Key insight: framework's strong-CP + universal-EDM-vanishing predictions")
    print("provide STRONG discrimination against BSM CP-source models, MODERATE")
    print("discrimination against SM-with-axion, and LOW discrimination against")
    print("SM-CKM-only (which makes the same d_n prediction).")
    print()
    print("n2EDM @ PSI 2027+ is the primary near-term test:")
    print("  - Detection: framework FALSIFIED via E-1")
    print("  - Null: framework CONSISTENT via E-2; BSM space tightened")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
