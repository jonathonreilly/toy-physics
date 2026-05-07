# PR230 Open-Surface Bridge Intake

Date: 2026-05-07

Status: bounded-support / open-surface bridge intake; no current PR230 closure

Runner:
`scripts/frontier_yt_pr230_open_surface_bridge_intake.py`

Certificate:
`outputs/yt_pr230_open_surface_bridge_intake_2026-05-07.json`

```yaml
actual_current_surface_status: bounded-support / open-surface bridge intake; no current PR230 closure
conditional_surface_status: exact support if a future accepted route supplies certified O_H plus production C_ss/C_sH/C_HH pole rows with Gram flatness, or a physical neutral rank-one theorem, or a strict W/Z physical-response packet without forbidden imports
proposal_allowed: false
bare_retained_allowed: false
```

## Purpose

The block07 hard-residual gate showed that the current source-only PR230
surface does not determine the missing Higgs overlap.  The obstruction can be
written as a two-state flat-extension problem:

```text
O_sp = cos(theta) O_H + sin(theta) O_perp,
Delta_spH = C_HH - |C_sH|^2 / C_ss.
```

Current PR230 support rows do not force `theta = 0` or
`Delta_spH = 0`.  This note therefore widens the search beyond the current
repo surface.  The literature and math surfaces below are used only as route
guidance.  They are not imported as proof authority and do not promote PR230.

## Route Intake

| Rank | Open surface | What it could supply | Current posture |
|---:|---|---|---|
| 1 | FMS / lattice gauge-Higgs spectroscopy | A gauge-invariant physical `O_H` candidate plus production `C_ss/C_sH/C_HH` pole rows | Most concrete positive route, but requires an accepted same-surface EW/Higgs action or a derivation from `Cl(3)/Z^3` before proof use. |
| 2 | Osterwalder-Schrader / lattice transfer matrix | The correct time-kernel and pole-residue extraction framework for source-Higgs rows | Method authority only; still needs actual rows and certified operators. |
| 3 | Positive-cone / Perron-Frobenius / Krein-Rutman style theory | A possible neutral scalar rank-one or Gram-flatness theorem | Hard theorem route; blocked until PR230 supplies a physical positivity-improving transfer kernel. |
| 4 | Lattice Higgs-Yukawa top/bottom simulations | Established nonperturbative top/Higgs sector compute template | Useful method precedent, but not a y_t derivation if Yukawa is scanned or tuned as an input. |
| 5 | Planck criticality / multiple-point route | External RGE boundary condition that can numerically constrain top mass | Separate axiom/derivation problem; not the PR230 source-Higgs bridge and has known Standard Model tension. |

## Why This Changes The Target

The strongest route is not another static `C_sx/C_xx` shortcut.  It is:

```text
accepted O_H definition -> source-Higgs time-kernel rows
-> pole residues and Gram flatness -> y_t readout.
```

This matches the existing source-Higgs time-kernel manifest, but changes the
launch condition.  A production row campaign is meaningful only after `O_H` is
defined as a physical gauge-invariant operator on an accepted surface.  The
route should then require measured `C_ss(t)`, `C_sH(t)`, and `C_HH(t)` rows,
GEVP pole extraction, covariance, FV/IR checks, and a Gram-flatness result.  It
must not set `kappa_s`, `c2`, `Z_match`, `cos(theta)`, or any overlap factor to
one.

## Literature Bridges

- Froehlich, Morchio, and Strocchi, "Higgs phenomenon without symmetry breaking
  order parameter" ([IHES PDF](https://archives.ihes.fr/document/P_81_12.pdf)).
  This is the relevant physical language for a gauge-invariant Higgs operator,
  but it does not identify PR230's source operator with `O_H`.
- Maas, Sondenheimer, and Toerek, "On the observable spectrum of theories with
  a Brout-Englert-Higgs effect" ([arXiv:1709.07477](https://arxiv.org/abs/1709.07477)).
  This supports FMS as a route for gauge-invariant spectroscopy in BEH regimes.
- Maas and Toerek, "The spectrum of an SU(3) gauge theory with a fundamental
  Higgs field" ([arXiv:1804.04453](https://arxiv.org/abs/1804.04453)).  This is
  a concrete lattice spectroscopy precedent for gauge-invariant Higgs
  composites.
- Gerhold, "Upper and lower Higgs boson mass bounds from a chirally invariant
  lattice Higgs-Yukawa model" ([arXiv:1002.2569](https://arxiv.org/abs/1002.2569)).
  This is a top/bottom/Higgs lattice-method precedent, not a parameter-free
  PR230 derivation.
- Fradkin and Shenker, "Phase diagrams of lattice gauge theories with Higgs
  fields" ([DOI](https://doi.org/10.1103/PhysRevD.19.3682)).  This constrains
  admissible gauge-Higgs surface thinking, but is not an overlap selector.
- Osterwalder and Schrader, "Axioms for Euclidean Green's functions"
  ([Project Euclid PDF](https://projecteuclid.org/journals/communications-in-mathematical-physics/volume-31/issue-2/Axioms-for-Euclidean-Greens-functions/cmp/1103858969.pdf)).
  This is route support for Euclidean reconstruction, not a static-row closure.
- Luescher, "Construction of a selfadjoint, strictly positive transfer matrix
  for Euclidean lattice gauge theories" ([DOI](https://doi.org/10.1007/bf01614090)).
  This supports transfer positivity once the correct gauge-invariant operators
  and rows exist.
- Rugh, "Cones and gauges in complex spaces: Spectral gaps and complex
  Perron-Frobenius theory" ([Annals of Mathematics](https://annals.math.princeton.edu/2010/171-3/p07)).
  This is a candidate math toolkit for a neutral primitive theorem, not a
  proof that the PR230 neutral channel is rank one.
- Froggatt and Nielsen, "Standard Model Criticality Prediction: Top mass
  173 +/- 5 GeV and Higgs mass 135 +/- 9 GeV"
  ([arXiv:hep-ph/9511371](https://arxiv.org/abs/hep-ph/9511371)), and Haba,
  Kaneta, Takahashi, and Yamaguchi, "Gravitational effects on vanishing Higgs
  potential at the Planck scale" ([arXiv:1408.5548](https://arxiv.org/abs/1408.5548)).
  These keep the criticality route honest: it can constrain y_t only after the
  Planck boundary condition is derived natively, and it is not the PR230
  source-Higgs bridge.

## Claim Boundary

This block does not derive `y_t`, `m_t`, canonical `O_H`, or
`Delta_spH = 0`.  It does not use `yt_ward_identity`, `H_unit`, `y_t_bare`,
observed `y_t`, observed top mass, observed W/Z masses, observed `g2`,
`alpha_LM`, plaquette, `u0`, or value recognition.  It does not pre-promote
PR230 and does not authorize retained or `proposed_retained` wording.

## Exact Next Action

The next non-chunk target should be an explicit FMS/gauge-Higgs operator
candidate packet for PR230:

1. define the accepted surface and a gauge-invariant `O_H` candidate;
2. state whether the surface is derived from `Cl(3)/Z^3` or a new external
   extension;
3. wire it into the existing source-Higgs time-kernel manifest;
4. require measured `C_ss(t)`, `C_sH(t)`, and `C_HH(t)` rows plus Gram
   flatness before any top-Yukawa claim.

If that accepted `O_H` surface cannot be supplied, the second target is the
hard positive-cone theorem: formulate H3/H4 as a precise physical
positivity-improving transfer-kernel problem and attempt a rank-one proof.

## Verification

```bash
python3 -m py_compile scripts/frontier_yt_pr230_open_surface_bridge_intake.py
python3 scripts/frontier_yt_pr230_open_surface_bridge_intake.py
# SUMMARY: PASS=12 FAIL=0
```
