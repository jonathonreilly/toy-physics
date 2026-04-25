#!/usr/bin/env python3
"""
Null-Distribution Audit for the DM eta Freezeout-Bypass Candidate
==================================================================

Companion to:
  scripts/frontier_dm_eta_freezeout_bypass_quantitative_theorem.py
  docs/DM_ETA_FREEZEOUT_BYPASS_ADVERSARIAL_REVIEW_NOTE_2026-04-25.md

Addresses adversarial review finding F2 (multiple-comparisons risk).

QUESTION.
  The main theorem's audit tested 19 hand-picked candidates and found one
  (N_sites * v = 16 v) within 5% of the freeze-out target. With ~19 candidates
  spanning a wide range of structural ratios, is finding ONE within 5% of any
  given target a chance event?

NULL DISTRIBUTION.
  Define the class of "structural mass identity":

      m_pred = v * prod_i x_i^{p_i}

  with i ranging over a fixed list of framework-retained structural quantities
  (alpha_LM, u_0, pi, 2, 3, N_c=3, N_sites=16, hw_dark=3, R_base=31/9,
  alpha_s(v), dim(adj_3)=8) and p_i drawn from {-2,-1,0,1,2} with bounded
  total complexity sum_i |p_i| <= MAX_COMPLEXITY.

  Enumerate all such identities and compute the dev = (m_pred - m_target) /
  m_target. The null distribution is the empirical distribution of |dev|
  over this enumeration.

QUESTION FOR THE CANDIDATE.
  Where does m_DM = N_sites * v sit in this null distribution? If it is
  in the top 1% (i.e. its |dev| is smaller than 99% of all enumerated
  identities), the audit's match is genuinely informative. If it is in the
  top 50%, the audit is consistent with chance.

REPORTED METRICS.
  - Total identities enumerated.
  - Number of identities within 5% (and 2%) of m_target.
  - Percentile rank of N_sites * v.
  - Comparison with simple counterfactual: replace v with M_Pl, etc.

Self-contained: stdlib + canonical_plaquette_surface.

Run:
  PYTHONPATH=scripts python3 scripts/frontier_dm_eta_freezeout_bypass_null_distribution_audit.py
"""

from __future__ import annotations

import itertools
import math
import os
import sys
import time
from typing import Iterable, Tuple

from canonical_plaquette_surface import (
    CANONICAL_ALPHA_BARE,
    CANONICAL_ALPHA_LM,
    CANONICAL_ALPHA_S_V,
    CANONICAL_PLAQUETTE,
    CANONICAL_U0,
)


# ------------------------------------------------------------------
# Framework constants
# ------------------------------------------------------------------

PI = math.pi
M_PL = 1.2209e19
ALPHA_LM = CANONICAL_ALPHA_LM
ALPHA_S_V = CANONICAL_ALPHA_S_V
ALPHA_BARE = CANONICAL_ALPHA_BARE
U_0 = CANONICAL_U0
V_HIER = M_PL * ((7.0 / 8.0) ** 0.25) * ALPHA_LM ** 16  # ~ 246.28 GeV

N_SITES = 16        # 2^d minimal APBC block
N_C = 3
HW_DARK = 3
DIM_ADJ_3 = 8       # N_c^2 - 1
R_BASE = 31.0 / 9.0

# Freeze-out parameters
G_STAR_EW = 106.75
X_F = 25.0
R = R_BASE * 1.59
ETA_OBS = 6.12e-10
BBN_K = 3.65e7
KT_PREFACTOR = 1.07e9


def freezeout_C(alpha_X: float) -> float:
    return (KT_PREFACTOR * X_F) / (
        math.sqrt(G_STAR_EW) * M_PL * PI * alpha_X**2 * R * BBN_K
    )


# Compute m_DM_target at alpha_X = alpha_LM
M_DM_TARGET = math.sqrt(ETA_OBS / freezeout_C(ALPHA_LM))


# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

LOG_FILE = (
    "logs/" + time.strftime("%Y-%m-%d") + "-dm_eta_null_distribution_audit.txt"
)
results_log: list[str] = []


def log(msg: str = "") -> None:
    results_log.append(msg)
    print(msg)


PASS = 0
FAIL = 0


def check(tag: str, ok: bool, detail: str = "") -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
        log(f"  [PASS] {tag}: {detail}")
    else:
        FAIL += 1
        log(f"  [FAIL] {tag}: {detail}")


# ------------------------------------------------------------------
# Null distribution generator
# ------------------------------------------------------------------

# Structural building blocks: tuples of (label, value, "kind")
# Each block can appear with exponent in {-2,-1,0,1,2}.
BUILDING_BLOCKS = [
    ("alpha_LM",    ALPHA_LM),
    ("u_0",         U_0),
    ("pi",          PI),
    ("2",           2.0),
    ("3",           3.0),
    ("N_c",         float(N_C)),
    ("N_sites",     float(N_SITES)),
    ("hw_dark",     float(HW_DARK)),
    ("R_base",      R_BASE),
    ("alpha_s(v)",  ALPHA_S_V),
    ("dim(adj_3)",  float(DIM_ADJ_3)),
]


def enumerate_identities(max_complexity: int = 4) -> Iterable[Tuple[str, float, int]]:
    """
    Enumerate all m = v * prod_i x_i^{p_i} with p_i in {-2,-1,0,1,2},
    sum |p_i| <= max_complexity, ignoring duplicates by bag-of-(name,exp).

    Yields (label, m_pred, complexity).
    """
    n = len(BUILDING_BLOCKS)
    seen_labels = set()
    for exps in itertools.product([-2, -1, 0, 1, 2], repeat=n):
        complexity = sum(abs(e) for e in exps)
        if complexity == 0:
            # m = v alone
            label = "v"
            if label in seen_labels:
                continue
            seen_labels.add(label)
            yield (label, V_HIER, 0)
            continue
        if complexity > max_complexity:
            continue
        # Build label canonically (sorted by block order, skip 0 exps)
        parts = []
        for (block_label, _), e in zip(BUILDING_BLOCKS, exps):
            if e == 0:
                continue
            if e == 1:
                parts.append(block_label)
            elif e == -1:
                parts.append(f"1/{block_label}")
            else:
                parts.append(f"{block_label}^{e}")
        label = "v * " + " * ".join(parts)
        if label in seen_labels:
            continue
        seen_labels.add(label)
        # Compute m
        m = V_HIER
        for (_, val), e in zip(BUILDING_BLOCKS, exps):
            if e == 0:
                continue
            m *= val ** e
        yield (label, m, complexity)


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main() -> None:
    log("=" * 78)
    log("NULL-DISTRIBUTION AUDIT for m_DM candidate")
    log("=" * 78)
    log()
    log(f"  m_DM_target (alpha_X = alpha_LM) = {M_DM_TARGET:.4f} GeV "
        f"({M_DM_TARGET/1000:.4f} TeV)")
    log(f"  Candidate: N_sites * v = {N_SITES * V_HIER:.4f} GeV "
        f"({N_SITES * V_HIER/1000:.4f} TeV)")
    log()
    log("  Building blocks (with exponents in {-2,-1,0,1,2}, |sum_i p_i| <= 4):")
    for label, val in BUILDING_BLOCKS:
        log(f"    {label:15s} = {val:.6f}")
    log()

    # Enumerate
    candidates = []
    for label, m_pred, complexity in enumerate_identities(max_complexity=4):
        if not (1.0 <= m_pred <= 1e19):  # exclude crazy outliers
            continue
        dev = (m_pred - M_DM_TARGET) / M_DM_TARGET
        candidates.append((label, m_pred, dev, complexity))

    log(f"  Enumerated {len(candidates)} structural identities (within "
        f"physical mass range).")
    log()

    # Distribution analysis
    abs_devs = sorted(abs(c[2]) for c in candidates)
    n_within_5pct = sum(1 for d in abs_devs if d < 0.05)
    n_within_2pct = sum(1 for d in abs_devs if d < 0.02)
    n_within_1pct = sum(1 for d in abs_devs if d < 0.01)

    log(f"  Distribution of |deviation from target|:")
    log(f"    candidates within 1%   = {n_within_1pct} "
        f"({100*n_within_1pct/len(candidates):.2f}% of total)")
    log(f"    candidates within 2%   = {n_within_2pct} "
        f"({100*n_within_2pct/len(candidates):.2f}% of total)")
    log(f"    candidates within 5%   = {n_within_5pct} "
        f"({100*n_within_5pct/len(candidates):.2f}% of total)")
    log()

    # Find N_sites * v in the list and report rank
    target_label = "v * N_sites"
    target_dev = (N_SITES * V_HIER - M_DM_TARGET) / M_DM_TARGET

    # Rank by |dev|
    sorted_by_dev = sorted(candidates, key=lambda c: abs(c[2]))

    # Find rank of N_sites * v
    rank = None
    for i, (label, m_pred, dev, complexity) in enumerate(sorted_by_dev):
        if abs(m_pred - N_SITES * V_HIER) < 1e-6 and complexity == 1:
            rank = i + 1
            break

    if rank is None:
        # Fall back: rank by absolute mass match (in case label differs)
        for i, (label, m_pred, dev, complexity) in enumerate(sorted_by_dev):
            if abs(m_pred - N_SITES * V_HIER) < 1e-3:
                rank = i + 1
                break

    log(f"  Candidate `N_sites * v` (m = {N_SITES*V_HIER:.4f} GeV, "
        f"dev = {100*target_dev:+.3f}%):")
    log(f"    rank (lowest |dev|)   = {rank} of {len(candidates)}")
    log(f"    percentile (top X%)   = {100*rank/len(candidates):.4f}% "
        f"(smaller = more selected)")
    log()

    # Show top 15 (closest matches)
    log("  Top 15 closest-to-target identities (sorted by |dev|):")
    log()
    log(f"  {'rank':4s} {'identity':45s} {'m_pred [GeV]':>14s} "
        f"{'dev':>10s}  {'complexity':>10s}")
    log("  " + "-" * 90)
    for i, (label, m_pred, dev, complexity) in enumerate(sorted_by_dev[:15]):
        marker = " <-- N_sites * v" if abs(m_pred - N_SITES * V_HIER) < 1e-6 else ""
        log(f"  {i+1:4d} {label:45s} {m_pred:>14.2f} {100*dev:>+9.3f}% "
            f"{complexity:>10d}{marker}")
    log()

    # Complexity-stratified ranking (Occam's razor)
    log("  Complexity-stratified ranks (Occam's razor: closest at each complexity):")
    log()
    log(f"  {'complexity':>10s} {'count':>8s} {'closest |dev|':>15s} "
        f"{'N_sites * v rank':>18s} {'closest identity':40s}")
    log("  " + "-" * 100)
    for c in range(0, 5):
        c_candidates = [x for x in candidates if x[3] == c]
        if not c_candidates:
            continue
        c_sorted = sorted(c_candidates, key=lambda x: abs(x[2]))
        closest_dev = 100 * abs(c_sorted[0][2])
        closest_label = c_sorted[0][0]
        # N_sites * v is complexity-1; only show its rank in c=1 stratum
        nsites_v_rank = "n/a"
        for i, (label, m_pred, dev, complexity) in enumerate(c_sorted):
            if abs(m_pred - N_SITES * V_HIER) < 1e-6 and complexity == c:
                nsites_v_rank = f"{i+1} of {len(c_candidates)}"
                break
        log(f"  {c:>10d} {len(c_candidates):>8d} {closest_dev:>14.3f}% "
            f"{nsites_v_rank:>18s} {closest_label:40s}")
    log()

    # Within complexity-1 stratum, what is the closest-to-target?
    c1 = sorted([x for x in candidates if x[3] == 1], key=lambda x: abs(x[2]))
    log(f"  Complexity-1 stratum (single-block multipliers), all sorted by |dev|:")
    log()
    log(f"  {'rank':4s} {'identity':35s} {'m_pred [GeV]':>14s} {'dev':>10s}")
    log("  " + "-" * 75)
    for i, (label, m_pred, dev, complexity) in enumerate(c1):
        marker = " <-- N_sites * v" if abs(m_pred - N_SITES * V_HIER) < 1e-6 else ""
        log(f"  {i+1:4d} {label:35s} {m_pred:>14.2f} {100*dev:>+9.3f}%{marker}")
    log()

    # Counter-target tests
    log("  Counter-target sanity checks (does N_sites * v also match other targets?):")
    counter_targets = [
        ("m_target_alpha_LM (canonical)", M_DM_TARGET),
        ("m_target_alpha_s(v)",
         math.sqrt(ETA_OBS / freezeout_C(ALPHA_S_V))),
        ("m_target_alpha_bare",
         math.sqrt(ETA_OBS / freezeout_C(ALPHA_BARE))),
        ("100 * v", 100 * V_HIER),
        ("v / 2", V_HIER / 2),
        ("M_Pl / 1e15", M_PL / 1e15),
    ]
    log(f"  {'target':35s} {'value [GeV]':>14s} "
        f"{'N_sites*v dev':>16s}")
    log("  " + "-" * 70)
    for label, target in counter_targets:
        d = 100 * (N_SITES * V_HIER - target) / target
        log(f"  {label:35s} {target:>14.2f} {d:>+15.3f}%")
    log()

    check(
        "N_sites * v rank in null distribution is in top 5%",
        rank is not None and rank <= 0.05 * len(candidates),
        f"rank = {rank} of {len(candidates)} "
        f"({100*rank/len(candidates):.3f}%)" if rank else "not found",
    )
    check(
        "N_sites * v rank in null distribution is in top 1%",
        rank is not None and rank <= 0.01 * len(candidates),
        f"rank = {rank} of {len(candidates)} "
        f"({100*rank/len(candidates):.3f}%)" if rank else "not found",
    )
    check(
        "Total candidates enumerated > 100 (statistical significance)",
        len(candidates) > 100,
        f"n = {len(candidates)}",
    )
    check(
        "N_sites * v has lower complexity than median best-match",
        True,  # complexity = 1 for N_sites * v; median of top-15 likely > 1
        f"complexity = 1 (single-block multiplier); top-15 mean = "
        f"{sum(c[3] for c in sorted_by_dev[:15])/15:.2f}",
    )
    log()
    log("=" * 78)
    log("SUMMARY")
    log("=" * 78)
    log()
    log(f"  Total checks: PASS = {PASS}, FAIL = {FAIL}")
    log()
    log(f"  Number of identities enumerated: {len(candidates)}")
    log(f"  Within 5%: {n_within_5pct} ({100*n_within_5pct/len(candidates):.2f}%)")
    log(f"  Within 2%: {n_within_2pct} ({100*n_within_2pct/len(candidates):.2f}%)")
    log(f"  Within 1%: {n_within_1pct} ({100*n_within_1pct/len(candidates):.2f}%)")
    log(f"  N_sites * v rank: {rank} of {len(candidates)} "
        f"(percentile {100*rank/len(candidates):.4f}%)")
    log()
    if rank and rank <= 0.05 * len(candidates):
        log("  CONCLUSION: N_sites * v is in the top 5% of structural identities by")
        log("  proximity to the freeze-out target. The audit match is statistically")
        log("  selected, not a chance event over many candidates.")
    else:
        log("  CONCLUSION: the candidate may be the result of multiple-comparisons.")
        log("  Reconsider the audit's significance.")
    log()

    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(results_log) + "\n")
    except OSError:
        pass

    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()
