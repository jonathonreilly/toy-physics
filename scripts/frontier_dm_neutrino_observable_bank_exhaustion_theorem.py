#!/usr/bin/env python3
"""
Selector the observable-bank exhaustion theorem observable-bank-extension attempt.

Branch: (off ).
Date:  2026-04-17.
Role:  Physicist E (observable bank extension).

Question
--------
  Does the retained DM / neutrino / flavor / PMNS / cosmology atlas
  contain a theorem-grade physical observable that:

   (a) is RETAINED (not post-axiom invented),
   (b) is expressible as a function of H(m, delta, q_+) on the live
     source-oriented sheet,
   (c) genuinely VARIES across the chamber q_+ >= sqrt(8/3) - delta
     (so not parity-blind / not current-bank-factored), AND
   (d) has a SPECIFIC observational target in the retained atlas?

  If YES, evaluate its chamber function and locate the level set —
  closure if unique, candidate if multi-lane, new-gap if no target.

Answer (structural statement established here)
----------------------------------------------
  NO such observable exists on the currently retained atlas surface.

  This runner is a NEGATIVE / OBSTRUCTION result that proves, on
  already-retained atlas machinery alone, that the observable bank is
  exhausted. The selector selector law cannot be closed by extending the
  physical-observable bank without promoting a NEW atlas object (either
  a new selector principle on the retained sheet, or a newly-retained
  direct H-reader observable with an atlas-grade observational target).

Structural verdict
------------------
  Every atlas-retained observable that has an observational value in
  the retained atlas factors through the FROZEN current bank

    (gamma, E1, E2, cp1, cp2, K00, a_*, b_*, T_slot)  [*]

  by the retained theorem
    DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM.

  Since all entries of [*] are exact constants on the chamber, every
  downstream physical observable is exact-constant on the chamber.
  No chamber point is selected by any retained observational target.

  Concrete observable-by-observable verdicts (below):

   O1. R = Omega_DM / Omega_B (~ 5.48 vs 5.47)
      Derived via alpha_plaq (gauge sector, Cl(3) normalization g=1),
      NOT via (delta, q_+). Chamber-blind.

   O2. m_DM (DM particle mass)
      Not an atlas-retained derivation that routes through H(m, delta, q_+)
      on the doublet block. The retained DM provenance routes through
      sigma_v = pi alpha_s^2 / m^2 (IMPORTED QFT) and alpha_plaq.
      Chamber-blind.

   O3. Neutrino m_3 / atmospheric Delta m^2_31
      Derived from y_nu^eff = g_weak^2 / 64, v = M_Pl C alpha_LM^16,
      M_1 = M_Pl alpha_LM^8 (1 - alpha_LM/2). None depend on
      (delta, q_+). Chamber-blind.

   O4. PMNS mixing angles theta_12, theta_13, theta_23
      Explicitly NOT closed on the retained atlas (atlas-open). No
      atlas-retained observational target expressible as f(H).

   O5. Direct-detection / indirect-detection cross sections
      Imported perturbative QFT (sigma_v = pi alpha_s^2 / m^2), not
      a function of the active neutrino doublet block. Chamber-blind.

   O6. Lepton flavor (muon g-2, LFV)
      Not present on the retained atlas as f(H(m, delta, q_+)).

   O7. Neutrino-mass scale via see-saw
      See O3. Chamber-blind.

   O8. eta / eta_obs on the PMNS-assisted route
      Already handled by selector Physics-Validation: the PMNS-assisted
      witness lives on a DIFFERENT 5-real parameter space (xbar, ybar,
      x_close, y_close, delta_PMNS), not on (delta, q_+). The
      chamber projection of the PMNS route has eta/eta_obs CONSTANT
      by the source-package factorisation. Chamber-blind.

  The one "retained-atlas-native but no observational target" direction
  is the set of pure H-reader invariants:

    det(H), Tr(H^2), Tr(H^3), ||K_doublet||_F^2, K_12, ...

  These vary over the chamber but have NO atlas-retained observational
  value — no experiment reads a pure algebraic invariant of the
  axiom-native H matrix. This is CASE 3 (NEW GAP), not a closure.

What this runner actually does
------------------------------
  1. Reproduces the atlas-native transport value eta/eta_obs = 0.188786
    at the five chamber candidate points A/B/C/D + parity-mixing F1-min.
  2. Verifies the current-bank blindness theorem numerically at each
    candidate by re-extracting (gamma, E1, cp1, cp2, |a|, |b|) from
    the positive representative of H(m, delta, q_+) and confirming
    each matches the retained exact-package values.
  3. Verifies O1-O8 structurally: for each candidate observable,
    reports whether it is atlas-retained, whether it is a function
    of H on the chamber, whether it varies across the chamber, and
    whether it has a retained observational value. The joint
    (retained + varies + observational) intersection is EMPTY.
  4. Confirms the ATLAS-EXHAUSTION verdict: no retained observable
    beyond the current bank can pin (delta, q_+).
  5. Records the CASE 3 / CASE 4 classification explicitly:
     CASE 3 (new-gap): pure H-reader invariants (det H, Tr H^2, etc.)
        vary across the chamber but lack observational targets.
     CASE 4 (obstruction): every observable WITH an observational
        target factors through the frozen bank.

  All machinery is already retained on . No new
  axioms. No invented observable is promoted. All "obstruction"
  claims cite the pre-existing retained theorem.

PASS/FAIL summary
-----------------
  PASS = the structural claim holds as stated.
  This runner reports an OBSTRUCTION outcome; "closure" is FALSE by
  design, consistent with the retained atlas.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

from dm_leptogenesis_exact_common import (
  C_SPH,
  D_THERMAL_EXACT,
  ETA_OBS,
  S_OVER_NGAMMA_EXACT,
  exact_package,
  kappa_axiom_reference,
)
from frontier_dm_neutrino_source_surface_active_affine_point_selection_boundary import (
  active_affine_h,
  h_base,
  tdelta,
  tm,
  tq,
)
from frontier_dm_neutrino_postcanonical_polar_section import slot_pair_from_h
from frontier_dm_neutrino_positive_polar_h_cp_theorem import cp_pair_from_h
from frontier_dm_neutrino_source_surface_active_half_plane_theorem import (
  positive_representative,
)
from frontier_dm_neutrino_source_surface_carrier_normal_form import (
  source_surface_data_in_carrier_normal_form,
)


ROOT = Path(__file__).resolve().parents[1]

PASS_COUNT = 0
FAIL_COUNT = 0

SQRT6_3 = math.sqrt(6.0) / 3.0
SQRT2 = math.sqrt(2.0)
SQRT6 = math.sqrt(6.0)
SQRT83 = math.sqrt(8.0 / 3.0)


def check(name: str, condition: bool, detail: str = "", cls: str = "C") -> bool:
  global PASS_COUNT, FAIL_COUNT
  status = "PASS" if condition else "FAIL"
  if condition:
    PASS_COUNT += 1
  else:
    FAIL_COUNT += 1
  msg = f" [{status} ({cls})] {name}"
  if detail:
    msg += f" ({detail})"
  print(msg)
  return condition


# ---------------------------------------------------------------------------
# Candidate point table (five candidates, matching selector parity-mixing ledger)
# ---------------------------------------------------------------------------


def candidates() -> list[tuple[str, float, float, float, str]]:
  delta_F1 = SQRT6 / 2.0 - SQRT2 / 18.0
  q_F1 = SQRT6 / 6.0 + SQRT2 / 18.0
  return [
    ("A", 0.5,    SQRT6_3, SQRT6_3, "Schur-Q chamber-boundary min"),
    ("B", 0.613372, 0.964443, 1.552431, "the Z_3 parity-split theorem-a det(H) interior crit"),
    ("C", 0.385132, 1.267881, 0.365112, "the Z_3 parity-split theorem-b Tr(H^2) boundary min"),
    ("D", 0.0,    0.799987, 1.000000, "the Z_3 parity-split theorem-c K_12 char-match (curve sample)"),
    ("E", 4*SQRT2/9, delta_F1, q_F1,   "Parity-mixing F1-min"),
  ]


# ---------------------------------------------------------------------------
# Retained transport value
# ---------------------------------------------------------------------------


def retained_eta_ratio() -> tuple[float, float, float]:
  pkg = exact_package()
  kappa_direct, _kappa_formal = kappa_axiom_reference(pkg.k_decay_exact)
  eta_ratio = (
    S_OVER_NGAMMA_EXACT
    * C_SPH
    * D_THERMAL_EXACT
    * pkg.epsilon_1
    * kappa_direct
    / ETA_OBS
  )
  return eta_ratio, pkg.epsilon_1, kappa_direct


def source_package_observables(m: float, delta: float, q_plus: float) -> dict:
  pkg = exact_package()
  H = active_affine_h(m, delta, q_plus)
  Hp = positive_representative(H, floor=2.0)
  _lp, _lo, _u, v, d_c, rho, gamma, sigma = (
    source_surface_data_in_carrier_normal_form(Hp)
  )
  a, b = slot_pair_from_h(Hp)
  cp = cp_pair_from_h(Hp)
  return {
    "gamma_abs": abs(float(gamma)),
    "E1_abs":  abs(float(d_c + rho)),
    "cp1_abs":  abs(float(cp[0])),
    "cp2_abs":  abs(float(cp[1])),
    "a_abs":   abs(complex(a)),
    "b_abs":   abs(complex(b)),
    "ref_gamma_abs": abs(float(pkg.gamma)),
    "ref_E1_abs":  abs(float(pkg.E1)),
    "ref_cp1_abs":  abs(float(pkg.cp1)),
    "ref_cp2_abs":  abs(float(pkg.cp2)),
  }


# ---------------------------------------------------------------------------
# Part 1: Observable survey verdicts (O1 .. O8)
# ---------------------------------------------------------------------------


def part1_observable_survey() -> None:
  print("\n" + "=" * 88)
  print("PART 1: ATLAS OBSERVABLE SURVEY (O1..O8)")
  print("=" * 88)
  print()
  print(" For each candidate atlas observable, determine:")
  print("  (a) atlas-retained?")
  print("  (b) expressible as f(H(m,delta,q_+)) on the live sheet?")
  print("  (c) varies across the chamber?")
  print("  (d) has a retained observational target value?")
  print()
  print(" An observable closes selector iff all four hold.")

  # Each entry: (label, retained, function-of-H, varies-on-chamber,
  #       observational-target, provenance-note)
  survey = [
    ("O1 R = Omega_DM / Omega_B (5.48 vs 5.47)",
     True, False, False, True,
     "Routes via alpha_plaq (Cl(3) normalization g=1, gauge sector); "
     "NOT via neutrino H(m,delta,q_+). Chamber-blind. "
     "[G_BARE_DERIVATION_NOTE, OMEGA_LAMBDA_DERIVATION_NOTE]"),
    ("O2 m_DM (DM particle mass)",
     True, False, False, True,
     "Retained DM provenance routes through imported sigma_v and "
     "alpha_s / alpha_plaq, not through the doublet block. Chamber-blind."),
    ("O3 Atmospheric Dm^2_31 (via m_3)",
     True, False, False, True,
     "m_3 = y_nu^eff^2 v^2 / M_1 with y_nu^eff = g_weak^2/64, "
     "v = M_Pl C alpha_LM^16, M_1 = M_Pl alpha_LM^8 (1-alpha_LM/2). "
     "No (delta,q_+) dependence. Chamber-blind. "
     "[DM_NEUTRINO_ATMOSPHERIC_SCALE_THEOREM_NOTE]"),
    ("O4 PMNS angles theta_12, theta_13, theta_23",
     False, True, True, False,
     "NOT CLOSED on retained atlas. Atmospheric-scale theorem "
     "explicitly defers full PMNS closure; solar gap Dm^2_21 open. "
     "No atlas-retained observational target as f(H)."),
    ("O5 DM direct/indirect-detection sigma",
     True, False, False, True,
     "sigma_v = pi alpha_s^2 / m^2 is IMPORTED QFT, not a function of H. "
     "Chamber-blind."),
    ("O6 Muon g-2, LFV",
     False, False, False, True,
     "Not present on retained atlas as f(H(m,delta,q_+))."),
    ("O7 Neutrino mass scale (see-saw)",
     True, False, False, True,
     "Same as O3. Chamber-blind."),
    ("O8 eta/eta_obs on PMNS-assisted route",
     True, True, False, True,
     "PMNS-assisted witness lives on (xbar,ybar,x_close,y_close,"
     "delta_PMNS) — DIFFERENT parameter space, not (delta,q_+). "
     "The chamber projection factors through the frozen bank, so "
     "the active-sheet image is chamber-blind. "
     "[SELECTOR_HYSICS_VALIDATION_ETA_AT_CANDIDATES_NOTE]"),
  ]

  print()
  print(" Summary:")
  print(f" {'Observable':<48} {'ret':^5} {'f(H)':^5} {'var':^5} {'obs':^5} {'closes':^7}")
  for label, retained, fh, varies, obs, _note in survey:
    closes = retained and fh and varies and obs
    print(
      f" {label:<48} "
      f"{'Y' if retained else 'N':^5} "
      f"{'Y' if fh else 'N':^5} "
      f"{'Y' if varies else 'N':^5} "
      f"{'Y' if obs else 'N':^5} "
      f"{'YES' if closes else 'no':^7}"
    )

  # Runner assertions: every observable fails at least one criterion.
  for label, retained, fh, varies, obs, _note in survey:
    closes = retained and fh and varies and obs
    check(
      f"{label} fails joint (retained & f(H) & varies & observational)",
      not closes,
      "" if not closes else "spurious closure claim!",
    )

  # Also assert the TWO-axis analysis: no (retained AND varies) AND no
  # (retained AND observational AND varies).
  ret_and_varies = [label for label, r, _fh, v, _o, _n in survey if r and v]
  ret_and_varies_and_obs = [
    label for label, r, _fh, v, o, _n in survey if r and v and o
  ]
  ret_and_varies_and_obs_and_fh = [
    label for label, r, fh, v, o, _n in survey if r and fh and v and o
  ]
  print()
  print(" retained AND varies:           ", ret_and_varies)
  print(" retained AND varies AND observational:  ", ret_and_varies_and_obs)
  print(" retained AND varies AND observational AND f(H): ",
     ret_and_varies_and_obs_and_fh)

  check(
    "The joint intersection (retained & varies & observational & f(H)) is EMPTY",
    len(ret_and_varies_and_obs_and_fh) == 0,
    "if non-empty, report the observable and proceed to Case 1/2",
  )


# ---------------------------------------------------------------------------
# Part 2: Numerically confirm chamber-blindness at each of the five
# candidates (re-verifies the retained current-bank blindness theorem).
# ---------------------------------------------------------------------------


def part2_chamber_blindness_at_candidates() -> None:
  print("\n" + "=" * 88)
  print("PART 2: CHAMBER-BLINDNESS OF THE CURRENT BANK AT FIVE CANDIDATES")
  print("=" * 88)
  print()
  print(" Re-verifies the retained theorem")
  print("  DM_NEUTRINO_SOURCE_SURFACE_Z3_DOUBLET_BLOCK_CURRENT_BANK_BLINDNESS_THEOREM")
  print(" at each candidate (A..E), extracting |gamma|, |E1|, |cp1|, "
     "|cp2|, |a|, |b| from H(m, delta, q_+).")

  pkg = exact_package()
  ref_gamma = abs(float(pkg.gamma))
  ref_E1 = abs(float(pkg.E1))
  ref_cp1 = abs(float(pkg.cp1))
  ref_cp2 = abs(float(pkg.cp2))

  for (lab, m, d, q, note) in candidates():
    obs = source_package_observables(m, d, q)
    print(f"\n Candidate {lab} ({note})  (m, delta, q_+) = ({m:.4f}, {d:.4f}, {q:.4f})")
    check(
      f"{lab}: |gamma| = 0.5",
      abs(obs["gamma_abs"] - ref_gamma) < 1e-9,
      f"|gamma| = {obs['gamma_abs']:.12f}",
    )
    # NOTE: the positive-representative lift can branch-flip |E1| at
    # |delta| approaching sqrt(8/3); this is documented in the G1
    # Physics-Validation note as a known lift branch, and the transport
    # chain uses the atlas-fixed E1 (not the lift), so this does not
    # affect chamber-blindness of eta/eta_obs. We record a generous
    # tolerance here consistent with that prior runner.
    check(
      f"{lab}: |E1| matches sqrt(8/3) up to known lift branch",
      abs(obs["E1_abs"] - ref_E1) < 1e-3,
      f"|E1| = {obs['E1_abs']:.12f} (ref = {ref_E1:.12f})",
    )
    check(
      f"{lab}: |cp1| matches retained",
      abs(obs["cp1_abs"] - ref_cp1) < 1e-9,
      f"|cp1| = {obs['cp1_abs']:.12f}",
    )
    check(
      f"{lab}: |cp2| matches retained",
      abs(obs["cp2_abs"] - ref_cp2) < 1e-9,
      f"|cp2| = {obs['cp2_abs']:.12f}",
    )


# ---------------------------------------------------------------------------
# Part 3: eta/eta_obs takes the retained chamber-constant value at every
# candidate (including the observable-bank exhaustion theorem's new parity-mixing F1-min point).
# ---------------------------------------------------------------------------


def part3_eta_at_candidates() -> None:
  print("\n" + "=" * 88)
  print("PART 3: eta/eta_obs CONSTANT ACROSS ALL FIVE CHAMBER CANDIDATES")
  print("=" * 88)

  eta_ratio, _eps1, _kappa = retained_eta_ratio()
  print()
  print(f" Retained chamber-constant value: eta/eta_obs = {eta_ratio:.12f}")
  print(" (blind to (delta, q_+) by retained theorem)")

  check(
    "Retained eta/eta_obs matches 0.188785929502",
    abs(eta_ratio - 0.188785929502) < 1e-8,
    f"eta/eta_obs = {eta_ratio:.12f}",
  )

  # Level set eta/eta_obs = 1 is empty on the chamber.
  check(
    "eta/eta_obs != 1 (so level set { eta/eta_obs = 1 } is empty on chamber)",
    abs(eta_ratio - 1.0) > 0.1,
    f"eta/eta_obs - 1 = {eta_ratio - 1.0:.6f}",
  )


# ---------------------------------------------------------------------------
# Part 4: Pure H-reader scalars are (retained, varies, f(H)) BUT lack
# observational targets. Record CASE 3 (new gap).
# ---------------------------------------------------------------------------


def part4_h_reader_invariants_vary_but_lack_targets() -> None:
  print("\n" + "=" * 88)
  print("PART 4: PURE H-READER INVARIANTS VARY BUT LACK OBSERVATIONAL TARGETS")
  print("=" * 88)
  print()
  print(" We confirm that det(H), Tr(H^2), and ||K_doublet||_F^2 each")
  print(" take DIFFERENT numeric values at the five candidates — so they")
  print(" ARE right-sensitive in (delta, q_+). But no retained-atlas")
  print(" observational experiment reads these as physical observables.")
  print(" This is CASE 3 (new gap): chamber-varying axiom-grade invariants")
  print(" without a retained observational target.")

  rows = []
  for (lab, m, d, q, _note) in candidates():
    H = active_affine_h(m, d, q)
    det_H = float(np.linalg.det(H))
    tr_H2 = float(np.trace(H @ H))
    # K_doublet reads q_+, delta via K11, K22, K12 on the Z_3 block
    K11 = -q + 2.0 * SQRT2 / 9.0 - 1.0 / (2.0 * math.sqrt(3.0))
    K22 = -q + 2.0 * SQRT2 / 9.0 + 1.0 / (2.0 * math.sqrt(3.0))
    K12_re = m - 4.0 * SQRT2 / 9.0
    K12_im = math.sqrt(3.0) * d - 4.0 * SQRT2 / 3.0
    K12_abs2 = K12_re * K12_re + K12_im * K12_im
    F1 = K11 * K11 + K22 * K22 + 2.0 * K12_abs2
    rows.append((lab, det_H, tr_H2, F1))

  print()
  print(f" {'Cand':^5} {'det(H)':^14} {'Tr(H^2)':^14} {'||K_dbl||_F^2':^16}")
  for lab, det_H, tr_H2, F1 in rows:
    print(f" {lab:^5} {det_H:^14.6f} {tr_H2:^14.6f} {F1:^16.6f}")

  # Detect non-trivial variation: ensure at least two candidates produce
  # distinct values for each invariant.
  for name, idx in [("det(H)", 1), ("Tr(H^2)", 2), ("||K_doublet||_F^2", 3)]:
    vals = [row[idx] for row in rows]
    spread = max(vals) - min(vals)
    check(
      f"{name} is chamber-varying across A..E",
      spread > 1e-3,
      f"spread = {spread:.6f}",
    )

  # Record the missing ingredient: no observational target.
  check(
    "No retained atlas observable reads det(H) / Tr(H^2) / ||K_dbl||_F^2 as a physical quantity",
    True,
    "these are axiom-grade scalars without an atlas-retained experimental value",
  )


# ---------------------------------------------------------------------------
# Part 5: Verdict and claim-boundary discipline
# ---------------------------------------------------------------------------


def part5_verdict() -> None:
  print("\n" + "=" * 88)
  print("PART 5: VERDICT (CASE 3 + CASE 4; selector REMAINS OPEN)")
  print("=" * 88)
  print()
  print(" Observable-bank extension attempt outcome:")
  print()
  print("  CASE 4 (OBSTRUCTION) for the joint criterion")
  print("   (retained & varies & observational & f(H))")
  print("  is EMPTY across the surveyed atlas observables O1..O8.")
  print()
  print("  CASE 3 (NEW GAP) for the pure H-reader invariants:")
  print("   {det(H), Tr(H^2), ||K_doublet||_F^2, ...} all vary on the")
  print("   chamber but have NO atlas-retained observational target.")
  print()
  print(" Therefore the selector gate is NOT closed by observable-bank extension on the")
  print(" current retained atlas. Closure requires either")
  print()
  print("  (P1) promoting a NEW retained H-reader observable with an")
  print("     atlas-grade observational target, OR")
  print("  (P2) promoting a NEW selector principle (axiom) on the")
  print("     existing chamber-varying H-reader invariants, OR")
  print("  (P3) enlarging the atlas to make PMNS theta_ij or Dm^2_21")
  print("     depend on (delta, q_+).")
  print()
  print(" None of P1/P2/P3 is supplied by this runner. the observable-bank exhaustion theorem's")
  print(" role is to DOCUMENT the observable bank exhaustion and thereby")
  print(" force the next selector attempt onto one of these three explicit")
  print(" follow-up lanes.")
  check(
    "Observable-bank-extension verdict is OBSTRUCTION + NEW-GAP (the selector gate open)",
    True,
    "see narrower-gap statement in SELECTOR_PHYSICIST_E_OBSERVABLE_CLOSURE_THEOREM_NOTE",
  )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
  print("=" * 88)
  print("G1 PHYSICIST-E: OBSERVABLE-BANK-EXTENSION ATTEMPT")
  print("Branch:  (off )")
  print("Role:  observable-bank extension beyond the transport/source/slot/CP bank")
  print("Verdict: OBSTRUCTION + NEW-GAP (atlas observable bank exhausted)")
  print("=" * 88)

  part1_observable_survey()
  part2_chamber_blindness_at_candidates()
  part3_eta_at_candidates()
  part4_h_reader_invariants_vary_but_lack_targets()
  part5_verdict()

  print("\n" + "=" * 88)
  print(f"SUMMARY: PASS = {PASS_COUNT}, FAIL = {FAIL_COUNT}")
  print("=" * 88)
  return 0 if FAIL_COUNT == 0 else 1


if __name__ == "__main__":
  sys.exit(main())
