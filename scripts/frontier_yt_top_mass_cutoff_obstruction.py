#!/usr/bin/env python3
"""
Pilot-certificate checker for the direct top-correlator cutoff obstruction.

This is not a retained no-go theorem.  It records what the mass-bracketing
pilot says at the current Sommer scale: the physical top target would require
am_t ~= 81, while the direct staggered correlator scan up to bare mass 16 only
reaches fitted am ~= 6.9 and is already strongly sublinear.  That makes the
current production plan a cutoff-obstruction route, not a near-production
measurement.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "outputs" / "yt_direct_lattice_correlator_mass_bracket_certificate_2026-05-01.json"
OUTPUT = ROOT / "outputs" / "yt_top_mass_cutoff_obstruction_2026-05-01.json"
PDG_MT_GEV = 172.56

PASS_COUNT = 0
FAIL_COUNT = 0


def report(tag: str, ok: bool, msg: str) -> None:
    global PASS_COUNT, FAIL_COUNT
    if ok:
        PASS_COUNT += 1
        status = "PASS"
    else:
        FAIL_COUNT += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


def main() -> int:
    print("YT top-mass cutoff obstruction checker")
    print("=" * 72)

    cert = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    metadata = cert.get("metadata", {})
    ensembles = cert.get("ensembles", [])
    ensemble = ensembles[0] if ensembles else {}
    result = cert.get("result", {})
    mass_scan = ensemble.get("mass_parameter_scan", [])

    selected_m_lat = ensemble.get("mass_fit", {}).get("m_lat")
    selected_m_gev = result.get("m_t_pole_GeV")
    gev_per_lat = selected_m_gev / selected_m_lat
    target_m_lat = PDG_MT_GEV / gev_per_lat

    rows = []
    for row in mass_scan:
        fitted = float(row["m_fit_lat"])
        rows.append(
            {
                "m_bare_lat": float(row["m_bare_lat"]),
                "m_fit_lat": fitted,
                "m_fit_lat_err": float(row["m_fit_lat_err"]),
                "chi2_dof": float(row["chi2_dof"]),
                "m_fit_gev": fitted * gev_per_lat,
                "max_cg_residual": float(row["max_cg_residual"]),
            }
        )

    max_row = max(rows, key=lambda row: row["m_fit_lat"])
    slopes = []
    for left, right in zip(rows, rows[1:]):
        slopes.append((right["m_fit_lat"] - left["m_fit_lat"]) / (right["m_bare_lat"] - left["m_bare_lat"]))

    monotone = all(left["m_fit_lat"] < right["m_fit_lat"] for left, right in zip(rows, rows[1:]))
    sublinear_tail = slopes[-1] < slopes[0] / 4.0
    target_far = target_m_lat > 10.0 * max_row["m_fit_lat"]
    max_physical_far = max_row["m_fit_gev"] < 0.1 * PDG_MT_GEV
    cg_ok = all(row["max_cg_residual"] < 1.0e-8 for row in rows)

    report("certificate-is-pilot", metadata.get("phase") == "pilot", f"phase={metadata.get('phase')!r}")
    report("mass-scan-has-five-points", len(rows) == 5, f"scan points={len(rows)}")
    report("mass-fit-monotone", monotone, "fitted mass increases with bare mass")
    report("mass-response-sublinear", sublinear_tail, f"slopes={slopes}")
    report("cg-residuals-ok", cg_ok, "all mass-scan CG residuals below 1e-8")
    report(
        "physical-target-requires-huge-am",
        target_m_lat > 50.0,
        f"target am_t={target_m_lat:.3f}",
    )
    report(
        "target-far-beyond-scan",
        target_far,
        f"target am_t={target_m_lat:.3f}, max fitted am={max_row['m_fit_lat']:.3f}",
    )
    report(
        "max-scan-far-below-top",
        max_physical_far,
        f"max scan mass={max_row['m_fit_gev']:.3f} GeV, target={PDG_MT_GEV:.2f} GeV",
    )

    output = {
        "actual_current_surface_status": "bounded cutoff obstruction / pilot compute evidence",
        "verdict": (
            "At the current Sommer scale, the physical top target would require "
            "a lattice mass around 81.4.  The pilot mass scan up to bare mass 16 "
            "only reaches fitted lattice mass about 6.94 and shows sublinear "
            "response.  Full production at this scale is therefore not a near "
            "path to a direct physical top measurement."
        ),
        "certificate": str(CERTIFICATE.relative_to(ROOT)),
        "gev_per_lattice_unit": gev_per_lat,
        "pdg_mt_gev": PDG_MT_GEV,
        "target_m_lat": target_m_lat,
        "mass_scan": rows,
        "slopes": slopes,
        "max_scan_row": max_row,
        "open_route": "requires a much finer scale, heavy-quark effective treatment, or a different y_t selector",
        "pass_count": PASS_COUNT,
        "fail_count": FAIL_COUNT,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"\nWrote certificate: {OUTPUT.relative_to(ROOT)}")
    print(f"SUMMARY: PASS={PASS_COUNT} FAIL={FAIL_COUNT}")
    return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
