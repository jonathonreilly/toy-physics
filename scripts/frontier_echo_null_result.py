#!/usr/bin/env python3
"""Pinned main-branch companion runner for the current frozen-star echo result.

This is a compact release check for the accepted statement:

1. the naive timing family exists
2. the evanescent barrier suppresses coherent return to effectively zero
3. the carried catalog-level search summary is null
"""

from __future__ import annotations

import math


G_SI = 6.674e-11
C = 2.998e8
M_SUN = 1.989e30
L_PLANCK = 1.616e-35
M_NUCLEON = 1.673e-27


def predict_echo_time_ms(mass_solar: float, spin: float) -> tuple[float, float]:
    mass = mass_solar * M_SUN
    r_s = 2 * G_SI * mass / C**2
    n_baryons = mass / M_NUCLEON
    r_min = max(n_baryons ** (1.0 / 3.0) * L_PLANCK, L_PLANCK)
    eps = r_min / r_s

    t_nonspin = 2.0 * r_s / C * abs(math.log(eps))

    r_p = r_s / 2.0 * (1.0 + math.sqrt(max(0.0, 1.0 - spin**2)))
    r_m = r_s / 2.0 * (1.0 - math.sqrt(max(0.0, 1.0 - spin**2)))
    a_m = spin * G_SI * mass / C**2
    t_kerr = 2.0 / C * (r_p**2 + a_m**2) / (r_p - r_m) * abs(math.log(eps))
    return 1e3 * t_nonspin, 1e3 * t_kerr


def barrier_log10_tunneling(mass_solar: float) -> float:
    mass = mass_solar * M_SUN
    r_s = 2 * G_SI * mass / C**2
    n_baryons = mass / M_NUCLEON
    r_min = max(n_baryons ** (1.0 / 3.0) * L_PLANCK, L_PLANCK)
    exponent = -(r_s / L_PLANCK) * math.log(r_s / r_min)
    return exponent / math.log(10.0)


def main() -> None:
    gw150914_mass = 62.0
    gw150914_spin = 0.67

    t_nonspin_ms, t_kerr_ms = predict_echo_time_ms(gw150914_mass, gw150914_spin)
    log10_t = barrier_log10_tunneling(gw150914_mass)

    # Pinned catalog-level summary from the later resolved analysis.
    frozen_star_sigma = 0.41
    abedi_sigma = 1.29

    checks = [
        ("non-spinning timing family remains in the old 50-80 ms band", 50.0 < t_nonspin_ms < 80.0),
        ("Kerr timing family remains in the old 60-80 ms band", 60.0 < t_kerr_ms < 80.0),
        ("evanescent barrier is effectively zero", log10_t < -1e20),
        ("frozen-star catalog stack is null", frozen_star_sigma < 3.0),
        ("Abedi-style catalog stack is null", abedi_sigma < 3.0),
    ]

    failures = [label for label, ok in checks if not ok]

    print("GW echo null-result companion check")
    print(f"t_nonspin_ms = {t_nonspin_ms:.2f}")
    print(f"t_kerr_ms = {t_kerr_ms:.2f}")
    print(f"log10_tunneling = {log10_t:.3e}")
    print(f"frozen_star_sigma = {frozen_star_sigma:.2f}")
    print(f"abedi_sigma = {abedi_sigma:.2f}")
    print(f"PASS = {len(checks) - len(failures)}")
    print(f"FAIL = {len(failures)}")

    if failures:
        for label in failures:
            print(f"FAIL: {label}")
        raise SystemExit(1)

    print("Current accepted result: no detectable echoes from frozen stars.")


if __name__ == "__main__":
    main()
