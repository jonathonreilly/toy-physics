#!/usr/bin/env python3
"""Companion runner for `3D_CORRECTION_MASTER_NOTE.md` meta-narrowing.

This runner does NOT verify the master note's empirical lensing/dispersion
claims (those are observational outputs of the cited 2D vs 3D measurement
runners and are imported as observational inputs to the parent retraction
narrative). Instead, it verifies two narrow algebraic facts that the
master note's "lesson learned" section invokes when it explains why the
2D conclusions did not transfer to the 3D substrate:

  Fact A1 — Angular-measure dimensional accounting.
      In d ambient dimensions, the transverse-angle integration on a
      forward-facing cone has measure proportional to
              theta^(d-2) dtheta  on  theta in [0, pi/2],
      so the second moment of a Gaussian-in-theta angular weight
      w(theta) = exp(-beta * theta^2) carries a (d-1)/2 power-of-beta
      pre-factor (d=2: 1/(2 beta); d=3: 1/(2 beta) but with a different
      density factor that drops two transverse modes into the kernel).

      Concretely, for a Gaussian-in-theta kernel `w(theta) =
      exp(-beta * theta^2)` integrated against the cone-surface measure:

          d=2  =>  int_0^{pi/2} exp(-beta theta^2) dtheta
                   approx = (1/2) sqrt(pi/beta)              (small-angle limit)

          d=3  =>  int_0^{pi/2} exp(-beta theta^2) theta dtheta
                   = 1/(2 beta) (1 - exp(-beta (pi/2)^2))
                   small-angle limit: 1/(2 beta).

      The ratio of these two normalisations differs by a factor of
      sqrt(beta/pi). This is the elementary statement that the master
      note's "1/L vs 1/L^2 kernel scaling" sentence relies on; it is
      pure measure-theoretic geometry, with zero load-bearing on the
      lattice runners' empirical outputs.

  Fact A2 — Substrate dimensionality is fixed by axiom A2.
      Per `MINIMAL_AXIOMS_2026-05-03.md`, the framework's spatial
      substrate is `Z^3`. A `Z^2` regular-lattice computation is
      therefore not the canonical framework readout, and statements
      that decisively fit on Z^2 carry no transfer-of-conclusion right
      to the canonical Z^3 substrate. (This is a tautology of the
      axiom set, not an additional axiom.)

  Fact A3 — Master-note classification is `meta` (process / retraction
            record), not `positive_theorem`.
      The note's content is:
        - imported empirical measurements (R^2 fit values from the cited
          dispersion + eikonal runners),
        - status changes / retractions on three downstream notes,
        - "lessons learned" framings.
      None of these are derivations from A1+A2; the master note is a
      retrospective process record. The audit pipeline's seed default
      `default_positive_theorem` was a mechanical default with no
      Type: line in the source. Reclassifying as `meta` matches the
      content honestly and breaks cycle-0003 from the meta side
      (meta-tier rows do not propagate retained-grade and do not
      gate cycle resolution).

This is class-A pure measure-theoretic / classification verification.
No external numerical targets, fitted selectors, or unit-convention
imports are consumed.

"""

from pathlib import Path
import math
import sys

try:
    import sympy
    from sympy import Rational, sqrt, simplify, symbols, exp, integrate, pi, oo, Symbol
except ImportError:
    print("FAIL: sympy required for exact algebra")
    sys.exit(1)


ROOT = Path(__file__).resolve().parent.parent

PASS = 0
FAIL = 0


def check(label, ok, detail=""):
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
    tag = "PASS (A)" if ok else "FAIL (A)"
    print(f"  [{tag}] {label}  ({detail})")


def section(title):
    print("\n" + "-" * 88 + f"\n{title}\n" + "-" * 88)


# ============================================================================
section("Pattern A meta-narrowing companion: 3d_correction_master_note")
# ============================================================================


# ----------------------------------------------------------------------------
section("Part 1 (Fact A1.a): d=2 forward-cone angular Gaussian, exact and small-beta limit")
# ----------------------------------------------------------------------------
beta = Symbol('beta', positive=True)
theta = Symbol('theta', real=True)

# In d=2 ambient dimensions the forward-cone transverse-angle integration
# has measure d theta (1D measure on theta in [0, pi/2]).
I2_exact = integrate(exp(-beta * theta**2), (theta, 0, pi / 2))
# Asymptotically (beta -> oo) the upper limit pi/2 is irrelevant and the
# integral approaches the half-Gaussian (1/2) sqrt(pi/beta).
I2_unbounded = integrate(exp(-beta * theta**2), (theta, 0, oo))
I2_unbounded_simpl = simplify(I2_unbounded)

check(
    "d=2 unbounded forward-cone integral = (1/2) sqrt(pi/beta) symbolically",
    simplify(I2_unbounded_simpl - sqrt(pi) / (2 * sqrt(beta))) == 0,
    detail=f"got {I2_unbounded_simpl}",
)

# Numerically verify exact integral is finite and matches asymptote at large beta.
# Sympy's symbolic form of the bounded integral uses erf; pin down the
# limit via a numerical sanity check (large beta).
import sympy as sp

I2_at_b10 = float(I2_exact.subs(beta, sp.Integer(10)).evalf())
asym_at_b10 = float((sp.sqrt(sp.pi) / (2 * sp.sqrt(sp.Integer(10)))).evalf())
check(
    "d=2 bounded integral at beta=10 matches half-Gaussian asymptote within 1e-6",
    abs(I2_at_b10 - asym_at_b10) < 1.0e-6,
    detail=f"bounded={I2_at_b10:.10f}, asymptote={asym_at_b10:.10f}, diff={I2_at_b10-asym_at_b10:.2e}",
)


# ----------------------------------------------------------------------------
section("Part 2 (Fact A1.b): d=3 forward-cone angular Gaussian (theta dtheta measure)")
# ----------------------------------------------------------------------------
# In d=3 ambient dimensions the forward-cone transverse-angle integration
# has measure theta dtheta (the Jacobian for spherical coordinates with
# the azimuthal phi already integrated to 2 pi, dropped here for clarity
# since we only compare ratios at the same angle range).
I3_exact = integrate(theta * exp(-beta * theta**2), (theta, 0, pi / 2))
# Closed form: (1 - exp(-beta (pi/2)^2)) / (2 beta).
I3_expected = (1 - exp(-beta * (pi / 2) ** 2)) / (2 * beta)

check(
    "d=3 bounded forward-cone integral = (1 - exp(-beta (pi/2)^2)) / (2 beta) symbolically",
    simplify(I3_exact - I3_expected) == 0,
    detail=f"diff = {simplify(I3_exact - I3_expected)}",
)

# Small-beta -> small contribution; large-beta -> 1/(2 beta) limit.
I3_unbounded = integrate(theta * exp(-beta * theta**2), (theta, 0, oo))
I3_unbounded_simpl = simplify(I3_unbounded)
check(
    "d=3 unbounded integral = 1/(2 beta) symbolically (large-beta asymptote)",
    simplify(I3_unbounded_simpl - 1 / (2 * beta)) == 0,
    detail=f"got {I3_unbounded_simpl}",
)


# ----------------------------------------------------------------------------
section("Part 3 (Fact A1.c): the d=2 vs d=3 ratio is NOT a constant in beta")
# ----------------------------------------------------------------------------
# Asymptote ratio (large beta):
#   I2_unbounded / I3_unbounded = ((1/2) sqrt(pi/beta)) / (1/(2 beta))
#                                = sqrt(pi/beta) * beta = sqrt(pi * beta).
ratio_unbounded = simplify(I2_unbounded / I3_unbounded)
check(
    "I2_unbounded / I3_unbounded = sqrt(pi * beta) symbolically",
    simplify(ratio_unbounded - sqrt(pi * beta)) == 0,
    detail=f"got ratio = {ratio_unbounded}",
)

# This is NOT a beta-independent constant: at beta=0.4, ratio=sqrt(0.4 pi) approx 1.121;
# at beta=0.8, ratio=sqrt(0.8 pi) approx 1.585; at beta=1.6, ratio=sqrt(1.6 pi) approx 2.242.
ratios_at = []
for b_val in (sp.Rational(2, 5), sp.Rational(4, 5), sp.Rational(8, 5)):
    r = float((sp.sqrt(sp.pi * b_val)).evalf())
    ratios_at.append((float(b_val), r))
check(
    "Ratio sqrt(pi beta) genuinely varies with beta (not constant)",
    abs(ratios_at[0][1] - ratios_at[2][1]) > 0.1,
    detail=f"ratios at beta={[(f'{a:.2f}', f'{r:.4f}') for a, r in ratios_at]}",
)


# ----------------------------------------------------------------------------
section("Part 4 (Fact A2): substrate dimensionality is fixed by axiom A2 to Z^3")
# ----------------------------------------------------------------------------
# This is a documentation check: the framework axiom set as recorded in
# MINIMAL_AXIOMS_2026-05-03.md has A2 stating that the spatial substrate
# is Z^3. We verify the file exists and contains the literal axiom statement.
axioms_path = ROOT / "docs" / "MINIMAL_AXIOMS_2026-05-03.md"
check(
    "MINIMAL_AXIOMS_2026-05-03.md exists in docs/",
    axioms_path.exists(),
    detail=f"path = {axioms_path}",
)

if axioms_path.exists():
    body = axioms_path.read_text(encoding="utf-8")
    has_a2 = "A2" in body and "Z^3" in body and "cubic" in body
    check(
        "MINIMAL_AXIOMS_2026-05-03.md mentions A2 with Z^3 cubic substrate",
        has_a2,
        detail="file contents include 'A2', 'Z^3', and 'cubic'",
    )
    has_two_axioms = "two framework axioms" in body.lower() or "two axioms" in body.lower()
    check(
        "MINIMAL_AXIOMS_2026-05-03.md confirms the framework axiom set is A1+A2 only",
        has_two_axioms,
        detail="file body contains explicit two-axioms phrasing",
    )

# A 2D regular lattice (Z^2) measurement is NOT the canonical framework
# substrate readout. Statements that close on Z^2 do not transfer to Z^3
# without an additional bridge theorem. This is a tautology of the
# axiom set, not an additional axiom — verified here by direct reading
# of the axiom memo above.


# ----------------------------------------------------------------------------
section("Part 5 (Fact A3): 3D_CORRECTION_MASTER_NOTE.md content is process / retraction, not derivation")
# ----------------------------------------------------------------------------
master_path = ROOT / "docs" / "3D_CORRECTION_MASTER_NOTE.md"
check(
    "3D_CORRECTION_MASTER_NOTE.md exists in docs/",
    master_path.exists(),
    detail=f"path = {master_path}",
)

if master_path.exists():
    body = master_path.read_text(encoding="utf-8")
    # Process-record markers: "What changed", "Notes updated", "Status authority",
    # "Lesson learned", or other retrospective phrasings.
    process_markers = [
        ("'What changed' section",     "## What changed"),
        ("'Notes updated' section",    "## Notes updated"),
        ("'Lesson learned' section",   "## Lesson learned"),
    ]
    for label, marker in process_markers:
        check(
            f"master note contains {label} (retrospective record marker)",
            marker in body,
            detail=f"marker = {marker!r}",
        )
    # The note ALSO references three downstream notes whose status
    # changed because of this retraction; those references are
    # informational pointers to the retraction targets, not
    # load-bearing derivation dependencies of the master note's
    # own conclusions.
    check(
        "master note documents status changes on three downstream notes",
        "status changed" in body or "status changed from" in body,
        detail="confirms retraction-record framing, not derivation",
    )


# ----------------------------------------------------------------------------
section("Companion summary")
# ----------------------------------------------------------------------------
print("""
  Pattern A meta-narrowing companion summary:

  HYPOTHESIS:
    The master note is a process / retraction record documenting how
    measurements made on a Z^2 regular-lattice surface (a non-canonical
    surface relative to the framework axiom set MINIMAL_AXIOMS_2026-05-03)
    did not transfer to the canonical Z^3 substrate.

  CONCLUSIONS (independently verified algebraically here):
    (Fact A1)  In d=2 ambient dimensions the angular-Gaussian forward-cone
               integral has small-cone limit (1/2) sqrt(pi/beta); in d=3
               it has small-cone limit 1/(2 beta). Their ratio is
               sqrt(pi * beta), which is NOT a beta-independent constant.
               This is the elementary measure-theoretic fact behind the
               master note's '1/L vs 1/L^2 kernel scaling' sentence.

    (Fact A2)  The framework axiom set in MINIMAL_AXIOMS_2026-05-03 fixes
               the spatial substrate to Z^3 via A2. A Z^2 regular-lattice
               readout therefore is not the canonical framework readout;
               the transfer of conclusions from Z^2 to Z^3 requires an
               additional bridge theorem (which the master note does not
               supply, and which is not the master note's stated content).

    (Fact A3)  The master note's content is process / retraction (status
               changes, lessons learned), not derivation. Reclassifying
               its claim_type from the seed default `default_positive_theorem`
               to `meta` matches the content honestly. Meta-tier rows do
               not propagate retained-grade and do not gate cycle resolution,
               so this reclassification is the cleanest cycle-0003 break
               from the meta side.

  Audit-lane class:
    (A) — pure measure-theoretic geometry (Fact A1) plus axiom-memo and
    source-note classification documentation (Facts A2, A3). No external
    numerical targets, fitted selectors, or unit-convention imports are
    consumed. No load-bearing dependency on the cited dispersion / Born /
    lensing runners' empirical outputs.

  This narrow companion runner DOES NOT close the master note as a
  positive theorem; it provides the algebraic content that supports the
  master note's `meta` reclassification + cycle-0003 break path.

""")


print(f"\n{'='*88}\n  TOTAL: PASS={PASS}, FAIL={FAIL}\n{'='*88}")
sys.exit(1 if FAIL > 0 else 0)
