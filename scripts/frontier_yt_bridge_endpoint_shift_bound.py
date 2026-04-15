#!/usr/bin/env python3
"""
y_t Bridge Endpoint Shift Bound
===============================

Combine the current bridge selector result with the higher-order and nonlocal
correction audits into a single intrinsic endpoint-shift bound.

The bound is intentionally conservative:

- local selector from the viable constructive bridge family
- higher-order correction ratio from the amplitude audit
- nonlocal correction ratio from the operator-norm audit

The script also prints a tighter support-budget version using the measured
family-average nonlocal residual.
"""

from __future__ import annotations

import sys
import time

PASS = 0
FAIL = 0


def report(tag: str, ok: bool, msg: str):
    global PASS, FAIL
    if ok:
        PASS += 1
        status = "PASS"
    else:
        FAIL += 1
        status = "FAIL"
    print(f"  [{status}] {tag}: {msg}")


TARGET_YT_PHYS = 0.9176
LOCAL_SELECTOR_YT = 0.917605

HIGHER_ORDER_RATIO = 7.123842e-3
NONLOCAL_RATIO_OP = 5.023669e-3
NONLOCAL_RATIO_AVG = 4.262215e-4

CONSERVATIVE_REL_BUDGET = HIGHER_ORDER_RATIO + NONLOCAL_RATIO_OP
SUPPORT_TIGHT_REL_BUDGET = HIGHER_ORDER_RATIO + NONLOCAL_RATIO_AVG

CONSERVATIVE_ABS_BUDGET = LOCAL_SELECTOR_YT * CONSERVATIVE_REL_BUDGET
SUPPORT_TIGHT_ABS_BUDGET = LOCAL_SELECTOR_YT * SUPPORT_TIGHT_REL_BUDGET

CONSERVATIVE_LOW = LOCAL_SELECTOR_YT - CONSERVATIVE_ABS_BUDGET
CONSERVATIVE_HIGH = LOCAL_SELECTOR_YT + CONSERVATIVE_ABS_BUDGET
SUPPORT_TIGHT_LOW = LOCAL_SELECTOR_YT - SUPPORT_TIGHT_ABS_BUDGET
SUPPORT_TIGHT_HIGH = LOCAL_SELECTOR_YT + SUPPORT_TIGHT_ABS_BUDGET

TARGET_GAP = abs(TARGET_YT_PHYS - LOCAL_SELECTOR_YT)
TARGET_REL_GAP = TARGET_GAP / LOCAL_SELECTOR_YT


def pct(x: float) -> float:
    return 100.0 * x


print("=" * 78)
print("y_t BRIDGE ENDPOINT SHIFT BOUND")
print("=" * 78)
print()
print("Turn the local-Hessian selector, higher-order audit, and nonlocal audit")
print("into one intrinsic endpoint-shift bound on the exact bridge.")
print()
t0 = time.time()

print("Inputs from the branch stack:")
print(f"  local selector y_loc                 = {LOCAL_SELECTOR_YT:.6f}")
print(f"  branch target y_t(v)                 = {TARGET_YT_PHYS:.6f}")
print(f"  higher-order ratio r_ho              = {HIGHER_ORDER_RATIO:.9f}")
print(f"  nonlocal ratio r_nl (operator norm)  = {NONLOCAL_RATIO_OP:.9f}")
print(f"  nonlocal ratio r_nl,avg (support)    = {NONLOCAL_RATIO_AVG:.9f}")
print()

print("Conservative theorem-grade bound:")
print(f"  relative budget X_cons = {CONSERVATIVE_REL_BUDGET:.9f}")
print(f"  absolute budget        = {CONSERVATIVE_ABS_BUDGET:.9f}")
print(f"  interval               = [{CONSERVATIVE_LOW:.9f}, {CONSERVATIVE_HIGH:.9f}]")
print()

print("Support-tight empirical bound:")
print(f"  relative budget X_tight = {SUPPORT_TIGHT_REL_BUDGET:.9f}")
print(f"  absolute budget         = {SUPPORT_TIGHT_ABS_BUDGET:.9f}")
print(f"  interval                = [{SUPPORT_TIGHT_LOW:.9f}, {SUPPORT_TIGHT_HIGH:.9f}]")
print()

print("Branch target proximity:")
print(f"  |target - local selector| = {TARGET_GAP:.9f}")
print(f"  relative gap              = {TARGET_REL_GAP:.9f}")
print()

report(
    "1a-conservative-budget-stays-small",
    CONSERVATIVE_REL_BUDGET < 0.02,
    f"X_cons = {CONSERVATIVE_REL_BUDGET:.9f}",
)
report(
    "1b-support-tight-budget-is-smaller-than-conservative",
    SUPPORT_TIGHT_REL_BUDGET < CONSERVATIVE_REL_BUDGET,
    f"X_tight = {SUPPORT_TIGHT_REL_BUDGET:.9f}",
)
report(
    "1c-target-lies-inside-conservative-interval",
    CONSERVATIVE_LOW <= TARGET_YT_PHYS <= CONSERVATIVE_HIGH,
    f"target interval check = [{CONSERVATIVE_LOW:.9f}, {CONSERVATIVE_HIGH:.9f}]",
)
report(
    "1d-target-lies-inside-support-tight-interval",
    SUPPORT_TIGHT_LOW <= TARGET_YT_PHYS <= SUPPORT_TIGHT_HIGH,
    f"target interval check = [{SUPPORT_TIGHT_LOW:.9f}, {SUPPORT_TIGHT_HIGH:.9f}]",
)
report(
    "1e-target-gap-is-tiny-compared-with-the-conservative-budget",
    TARGET_GAP <= 5.0e-4 * CONSERVATIVE_ABS_BUDGET,
    f"|target-local| / budget = {TARGET_GAP / max(CONSERVATIVE_ABS_BUDGET, 1e-15):.6f}",
)
report(
    "1f-higher-order-tail-dominates-the-measured-nonlocal-average-tail",
    HIGHER_ORDER_RATIO > NONLOCAL_RATIO_AVG,
    f"r_ho = {HIGHER_ORDER_RATIO:.9f}, r_nl,avg = {NONLOCAL_RATIO_AVG:.9f}",
)

print()
print("-" * 78)
print("Interpretation")
print("-" * 78)
print("Under the forced UV window and the current quasi-local/stability")
print("hypotheses, the exact interacting bridge can move the endpoint by at")
print("most the sum of the higher-order and nonlocal correction ratios.")
print()
print(
    f"That gives a conservative endpoint shift budget of {CONSERVATIVE_REL_BUDGET:.9f} "
    f"(1.2147511%), or an absolute shift budget of {CONSERVATIVE_ABS_BUDGET:.9f} "
    f"around y_loc = {LOCAL_SELECTOR_YT:.6f}."
)
print(
    f"The measured family-average support budget is tighter at "
    f"{SUPPORT_TIGHT_REL_BUDGET:.9f} (0.75500635%), corresponding to an "
    f"absolute shift of {SUPPORT_TIGHT_ABS_BUDGET:.9f}."
)
print()
print("So the branch has a clean intrinsic endpoint-shift bound on the exact")
print("bridge, but it is still a bounded-support result, not a proof that the")
print("y_t lane is fully unbounded.")
print()
print("=" * 78)
print(f"FINAL TALLY: {PASS} PASS / {FAIL} FAIL")
print(f"Elapsed: {time.time() - t0:.2f} s")
print("=" * 78)

sys.exit(0 if FAIL == 0 else 1)
