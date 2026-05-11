#!/usr/bin/env python3
"""Open-gate diagnostic for the Higgs lambda(M_Pl) matching-sign claim."""

from __future__ import annotations

import math
import sys


PASS = 0
FAIL = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    suffix = f"  ({detail})" if detail else ""
    print(f"[{tag}] {label}{suffix}")


# Existing Higgs-retention inputs used as bounded diagnostics.
G1_MPL = 0.466
G2_MPL = 0.507
G3_MPL = 0.489
YT_MPL = 0.382
LOOP = 16.0 * math.pi**2

DMH_D_LAMBDA = 312.0
SIGMA_MH_TOTAL = 3.17
LAMBDA_CAP = 1.0e-3


print("Higgs lambda(M_Pl) matching-sign open-gate diagnostic")
print()

su2_envelope = G2_MPL**4 / LOOP
all_gauge_envelope = (G1_MPL**4 + G2_MPL**4 + G3_MPL**4) / LOOP
yt_envelope = YT_MPL**4 / LOOP

check(
    "SU(2) one-loop size is O(10^-4)",
    3.0e-4 < su2_envelope < 6.0e-4,
    detail=f"g2^4/(16pi^2) = {su2_envelope:.3e}",
)
check(
    "all-gauge one-loop envelope is O(10^-3)",
    8.0e-4 < all_gauge_envelope < 1.4e-3,
    detail=f"sum g_i^4/(16pi^2) = {all_gauge_envelope:.3e}",
)
check(
    "top-Yukawa one-loop envelope is subleading at M_Pl",
    yt_envelope < su2_envelope,
    detail=f"yt^4/(16pi^2) = {yt_envelope:.3e}",
)

positive_example = +4.0e-4
negative_example = -4.0e-4
check(
    "positive finite part fits the magnitude envelope",
    abs(positive_example) <= LAMBDA_CAP,
    detail=f"delta_lambda = {positive_example:+.1e}",
)
check(
    "negative finite part also fits the same magnitude envelope",
    abs(negative_example) <= LAMBDA_CAP and negative_example < 0,
    detail=f"delta_lambda = {negative_example:+.1e}",
)
check(
    "magnitude envelope alone does not imply lambda_eff >= 0",
    negative_example < 0 and abs(negative_example) <= LAMBDA_CAP,
    detail="sign remains an independent matching calculation",
)

max_mh_shift = DMH_D_LAMBDA * LAMBDA_CAP
central_mh_shift = DMH_D_LAMBDA * abs(positive_example)
check(
    "|lambda| <= 1e-3 gives Delta m_H <= 0.312 GeV",
    abs(max_mh_shift - 0.312) < 1e-12,
    detail=f"Delta m_H cap = {max_mh_shift:.3f} GeV",
)
check(
    "central 4e-4 shift is about 0.125 GeV",
    0.12 < central_mh_shift < 0.13,
    detail=f"Delta m_H central = {central_mh_shift:.3f} GeV",
)
check(
    "1e-3 boundary uncertainty is below inherited Higgs-chain systematic",
    max_mh_shift < SIGMA_MH_TOTAL,
    detail=f"{max_mh_shift:.3f} GeV < {SIGMA_MH_TOTAL:.2f} GeV",
)

literature_central = -0.013
literature_sigma = 0.007
framework_positive_lower = 0.0
lit_upper_1sigma = literature_central + literature_sigma
check(
    "positive-side framework band would be disjoint from literature 1-sigma band if sign were derived",
    framework_positive_lower > lit_upper_1sigma,
    detail=f"0 - ({lit_upper_1sigma:+.3f}) = {framework_positive_lower - lit_upper_1sigma:+.3f}",
)
check(
    "but current diagnostic classifies that sign discriminator as open",
    negative_example < 0,
    detail="negative matching counterexample remains allowed by size bound",
)

print(f"\nTOTAL: PASS={PASS} FAIL={FAIL}")
sys.exit(1 if FAIL else 0)
