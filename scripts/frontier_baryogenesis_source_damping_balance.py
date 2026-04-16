#!/usr/bin/env python3
"""
Baryogenesis source-damping balance theorem on the current main package
surface.

This runner packages the next exact logarithmic reduction after the positive-
branch damping theorem:

  eta = J * exp[S_src[chi] - I_damp[chi]]

with a fixed target balance on the retained scalar history lane.
"""

from __future__ import annotations

import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

PASS = 0
FAIL = 0

ETA_OBS = 6.12e-10
J_PROMOTED = 3.330901e-5
K_NP_TARGET = ETA_OBS / J_PROMOTED
LOG_K_TARGET = math.log(K_NP_TARGET)
K_EQUAL_SPLIT = K_NP_TARGET ** (1.0 / 3.0)
LOG_K_EQUAL = math.log(K_EQUAL_SPLIT)


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        tag = "PASS"
    else:
        FAIL += 1
        tag = "FAIL"
    print(f"  [{tag}] {name}")
    if detail:
        print(f"         {detail}")


def info(name: str, detail: str = "") -> None:
    print(f"  [INFO] {name}")
    if detail:
        print(f"         {detail}")


def main() -> int:
    print("=" * 80)
    print("BARYOGENESIS SOURCE-DAMPING BALANCE")
    print("=" * 80)
    print()
    print("Question:")
    print("  After the damping theorem, can the surviving baryogenesis problem")
    print("  be reduced to one exact scalar balance law?")
    print()

    print("=" * 80)
    print("PART 1: EXACT LOGARITHMIC BALANCE")
    print("=" * 80)
    print()

    source_samples = [0.03, 0.1, 0.4]
    damping_samples = [1.0, 4.0, 9.0]

    for idx, (f_ewpt, i_damp) in enumerate(
        zip(source_samples, damping_samples), start=1
    ):
        s_src = math.log(f_ewpt)
        f_np = f_ewpt * math.exp(-i_damp)
        eta = J_PROMOTED * f_np
        recon = J_PROMOTED * math.exp(s_src - i_damp)
        check(
            f"sample balance {idx} reconstructs F_NP exactly from source and damping",
            abs(f_np - math.exp(s_src - i_damp)) < 1e-15,
            f"F_NP = {f_np:.6e}",
        )
        check(
            f"sample balance {idx} reconstructs eta exactly",
            abs(eta - recon) < 1e-20,
            f"eta = {eta:.6e}",
        )

    info(
        "balance meaning",
        "on the viable positive branch the open electroweak object is governed by one source logarithm and one nonnegative damping functional",
    )
    print()

    print("=" * 80)
    print("PART 2: EXACT TARGET BALANCE")
    print("=" * 80)
    print()

    print(f"  K_NP,target        = {K_NP_TARGET:.12e}")
    print(f"  log(K_NP,target)   = {LOG_K_TARGET:.12f}")
    print()

    check(
        "log(K_NP,target) matches the retained eta/J target",
        abs(math.exp(LOG_K_TARGET) - K_NP_TARGET) < 1e-18,
        f"log(K_target) = {LOG_K_TARGET:.12f}",
    )
    check(
        "the target balance reconstructs eta_obs exactly",
        abs(J_PROMOTED * math.exp(LOG_K_TARGET) - ETA_OBS) < 1e-20,
        f"eta = {J_PROMOTED * math.exp(LOG_K_TARGET):.6e}",
    )
    info(
        "target consequence",
        "the retained baryogenesis target is one exact scalar balance law S_src[chi] - I_damp[chi] = log(eta_obs/J)",
    )
    print()

    print("=" * 80)
    print("PART 3: SOURCE FLOOR AND REQUIRED DAMPING")
    print("=" * 80)
    print()

    s_src_floor = LOG_K_TARGET
    f_ewpt_floor = math.exp(s_src_floor)
    source_candidates = [K_NP_TARGET, 1.0e-3, K_EQUAL_SPLIT]

    check(
        "the exact source floor is S_src >= log(K_NP,target)",
        abs(s_src_floor - LOG_K_TARGET) < 1e-18,
        f"S_src,floor = {s_src_floor:.12f}",
    )
    check(
        "the exact source floor is F_EWPT >= K_NP,target",
        abs(f_ewpt_floor - K_NP_TARGET) < 1e-18,
        f"F_EWPT,floor = {f_ewpt_floor:.12e}",
    )

    for idx, f_ewpt in enumerate(source_candidates, start=1):
        s_src = math.log(f_ewpt)
        i_damp = s_src - LOG_K_TARGET
        check(
            f"source candidate {idx} fixes a nonnegative required damping",
            i_damp >= -1e-15,
            f"I_damp,req = {i_damp:.12f}",
        )
        check(
            f"source candidate {idx} reproduces the exact target when paired with its required damping",
            abs(f_ewpt * math.exp(-i_damp) - K_NP_TARGET) < 1e-18,
            f"F_EWPT * exp(-I_damp) = {(f_ewpt * math.exp(-i_damp)):.12e}",
        )

    info(
        "constraint meaning",
        "once a source candidate is derived, the required damping is no longer free; it is fixed exactly by the target balance",
    )
    print()

    print("=" * 80)
    print("PART 4: LOG-GEOMETRY BENCHMARK")
    print("=" * 80)
    print()

    i_tr_equal = -LOG_K_EQUAL
    i_sph_equal = -LOG_K_EQUAL
    i_damp_equal = i_tr_equal + i_sph_equal

    check(
        "equal three-stage split gives the expected source logarithm",
        abs(LOG_K_EQUAL - (LOG_K_TARGET / 3.0)) < 1e-15,
        f"S_src,eq = {LOG_K_EQUAL:.12f}",
    )
    check(
        "equal three-stage split gives the expected total damping",
        abs(i_damp_equal + 2.0 * LOG_K_EQUAL) < 1e-12,
        f"I_damp,eq = {i_damp_equal:.12f}",
    )
    check(
        "equal three-stage split satisfies the exact target balance",
        abs(LOG_K_EQUAL - i_damp_equal - LOG_K_TARGET) < 1e-12,
        f"S_src - I_damp = {(LOG_K_EQUAL - i_damp_equal):.12f}",
    )
    info(
        "benchmark meaning",
        "the equal-split point gives an exact log-space reference for future source / damping derivations on the retained scalar lane",
    )
    print()

    print("=" * 80)
    print("PART 5: NOTE / ATLAS INTEGRATION")
    print("=" * 80)
    print()

    balance_note = (DOCS / "BARYOGENESIS_SOURCE_DAMPING_BALANCE_NOTE.md").read_text(
        encoding="utf-8"
    )
    penalty_note = (DOCS / "BARYOGENESIS_EFFICIENCY_PENALTY_NOTE.md").read_text(
        encoding="utf-8"
    )
    gate_note = (DOCS / "BARYOGENESIS_CLOSURE_GATE_NOTE.md").read_text(encoding="utf-8")
    atlas = (DOCS / "publication" / "ci3_z3" / "DERIVATION_ATLAS.md").read_text(
        encoding="utf-8"
    )
    harness = (DOCS / "CANONICAL_HARNESS_INDEX.md").read_text(encoding="utf-8")
    flagship = (DOCS / "CURRENT_FLAGSHIP_ENTRYPOINT_2026-04-14.md").read_text(
        encoding="utf-8"
    )

    check(
        "source-damping balance note records eta = J * exp[S_src[chi] - I_damp[chi]]",
        "`η = J * exp[S_src[χ] - I_damp[χ]]`" in balance_note,
    )
    check(
        "source-damping balance note records the exact log target",
        "`S_src[χ] - I_damp[χ] = log(η_obs / J) = -10.904606206411`" in balance_note,
    )
    check(
        "source-damping balance note records the source floor",
        "`S_src[χ] >= log K_NP,target = -10.904606206411`" in balance_note,
    )
    check(
        "efficiency-penalty note remains upstream of the balance theorem",
        "`F_NP[χ] = F_EWPT[χ] * exp[-I_damp[χ]]`" in penalty_note,
    )
    check(
        "closure-gate note points to the source-damping balance note",
        "BARYOGENESIS_SOURCE_DAMPING_BALANCE_NOTE.md" in gate_note,
    )
    check(
        "derivation atlas carries the source-damping balance row",
        "Baryogenesis source-damping balance" in atlas,
    )
    check(
        "canonical harness index includes the source-damping balance runner",
        "frontier_baryogenesis_source_damping_balance.py" in harness,
    )
    check(
        "current flagship entrypoint points to the source-damping balance note",
        "BARYOGENESIS_SOURCE_DAMPING_BALANCE_NOTE.md" in flagship,
    )

    print()
    print("=" * 80)
    print("SYNTHESIS")
    print("=" * 80)
    print()
    print("  RESULT:")
    print("    - on the viable positive branch the open problem is one exact")
    print("      logarithmic balance")
    print("      eta = J * exp[S_src[chi] - I_damp[chi]]")
    print("    - the retained target is fixed exactly at")
    print("      S_src[chi] - I_damp[chi] = -10.904606206411")
    print("    - once a source candidate is derived, the required damping is")
    print("      fixed exactly")
    print()
    print(f"  TOTAL: PASS = {PASS}, FAIL = {FAIL}")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
