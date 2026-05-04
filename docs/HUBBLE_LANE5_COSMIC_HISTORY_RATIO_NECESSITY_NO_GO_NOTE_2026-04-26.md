# Lane 5 Cosmic-History-Ratio Necessity No-Go: `H_0` and `L` Cannot Be Derived From The Minimal Accepted Axiom Stack Alone

**Date:** 2026-04-26
**Status:** support no-go / program-boundary note on `main`. Bounds the
closure space for Lane 5: any proposed retained derivation of `H_0` (or
equivalently `L = Omega_Lambda`) requires at least one structural premise
beyond the
`MINIMAL_AXIOMS_2026-04-11.md` stack.
**Lane:** 5 — Hubble constant `H_0` derivation
**Workstream:** `hubble-h0-20260426`

---

## 0. Statement

Let `A_min` denote the minimal accepted input stack as recorded in
`docs/MINIMAL_AXIOMS_2026-04-11.md`:

1. local algebra `Cl(3)`,
2. spatial substrate `Z^3`,
3. microscopic dynamics (finite local Grassmann / staggered-Dirac partition
   on `Cl(3)/Z^3`),
4. canonical normalization `g_bare = 1` plus accepted plaquette / `u_0`
   surface and minimal APBC hierarchy block.

**No-Go Theorem (Lane 5 absolute-time necessity).**
On `A_min` alone, the present-day Hubble constant `H_0`, the de Sitter
Hubble scale `H_inf`, and the spectral-gap radius `R_Lambda` cannot be
derived as numerical values.

**No-Go Theorem (Lane 5 cosmic-history-ratio necessity).**
On `A_min` alone, the dimensionless ratio `L = (H_inf / H_0)^2` cannot be
derived without retaining at least one additional dimensionless input from
the cosmic-history layer — concretely, at least one of

```text
{ Omega_m,0 / Omega_Lambda,0,
  Omega_r,0 / Omega_Lambda,0,
  Omega_m,0 / Omega_r,0,
  rho_m,0 / rho_Lambda,0   (after absolute scale fixed),
  any cosmic-history-fixing observation reducible to one of the above } .
```

**Lane 5 closure-pathway corollary.**
Any retained Lane 5 closure requires premises drawn from **two** classes:
exactly one absolute-scale class `(C1)` premise, **and** exactly one
dimensionless-`L` class `(C2)` or `(C3)` premise.

- **(C1) absolute-scale axiom** [REQUIRED]. A derivation, on extended
  axioms, of an absolute physical scale (e.g., the lattice spacing `a` in
  physical units, or `M_Pl` retained from framework rather than from
  observation). This anchors `R_Lambda` and `H_inf` numerically; combined
  with retained `L`, fixes `H_0`. (C1) is necessary because `H_0` is
  dimensional and `A_min` does not fix absolute scales.
- **(C2) cosmic-history-ratio retirement** [one of two `L`-pathways].
  A retained derivation of one of the listed dimensionless cosmic-history
  ratios on extended axioms, retiring `eta`, `alpha_GUT`, or
  `T_CMB`-equivalent observational pins from the bounded
  `Omega_b -> R -> Omega_DM -> Omega_m -> Omega_Lambda` cascade.
- **(C3) direct cosmic-`L` derivation** [one of two `L`-pathways]. A
  framework-internal structural derivation of `L` itself (independent of
  the cosmic-history cascade), e.g., from a separate vacuum/topology
  argument that gives `Omega_Lambda` without going through the matter
  cascade.

No fourth class exists, and no single class is sufficient on its own.

## 1. Premises (all from retained surface)

| Identity | Authority |
|---|---|
| `MINIMAL_AXIOMS_2026-04-11.md` accepted-input stack | `MINIMAL_AXIOMS_2026-04-11.md` |
| `Lambda = 3 / R_Lambda^2` retained spectral-gap identity | `COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md` |
| `H_inf = c / R_Lambda` scale identification | `COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md` |
| `Omega_Lambda = (H_inf/H_0)^2` matter-bridge identity | `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md` |
| Open-number reduction: `S` is a function of `(H_0, L)` | `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md` (Cycle 2) |
| Bounded cosmology cascade `eta -> Omega_b -> R -> Omega_DM -> Omega_m -> Omega_Lambda` | `OMEGA_LAMBDA_DERIVATION_NOTE.md` |
| Planck-scale absolute-scale lane status (`a^(-1) = M_Pl` not yet derived from minimal stack) | `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` §3, `PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md` |

## 2. Proof of absolute-time necessity

`H_0` has units of inverse time `[T^{-1}]`. On `A_min` the only physical
scale carried by the stack is the bare lattice spacing `a` (a length scale
on `Z^3`). Per `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` §3:

> "on the accepted physical-lattice reading, the package currently carries
> `a^{-1} = M_Pl` as an explicit Planck-scale pin; that pin is not yet
> derived from the minimal accepted theorem stack."

So `A_min` does not fix `a` numerically; the Planck-scale pin
`a^{-1} = M_Pl` is a separate explicit assertion on the accepted
physical-lattice reading. The conditional packet
`PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md` derives
`a / l_P = 1` only after a primitive boundary count is accepted as the
gravitational boundary/action carrier — itself an additional premise.

`H_0`, `H_inf`, and `R_Lambda` are dimensional quantities (`[T^{-1}]`,
`[T^{-1}]`, `[L]` respectively). Their numerical values are functions of
the absolute physical scale. Hence on `A_min` alone, all three are
not-yet-numerical. `QED`

## 3. Proof of cosmic-history-ratio necessity

`L = (H_inf/H_0)^2` is dimensionless. By the open-number reduction
theorem (Cycle 2), every late-time bounded cosmology variable is an exact
function of `(H_0, L)` with `R = Omega_r,0` admitted. Inverting, given
`(R, q_0)` or `(R, z_mLambda)` or `(R, H(a))` for `a != 1`, the
single-ratio inverse reconstruction theorem (2026-04-25) recovers `L`.

So a retained `L` derivation must supply one of:

- (i) one of `(q_0, z_*, z_mLambda, H(a))` from framework structure, with
  `R` admitted;
- (ii) one of `(Omega_m,0, Omega_Lambda,0)` from framework structure, with
  `R` admitted;
- (iii) one of the bounded-cascade endpoints (`eta`, `alpha_GUT`-corrected
  `R = Omega_DM/Omega_b`, `Omega_b`) retained, propagating through the
  cascade.

Each `(i)` quantity is a late-time observable whose value depends on
matter/radiation/`Lambda` ratios — i.e., on cosmic-history content. Each
`(ii)` quantity is a cosmic-history-ratio in the listed set. Each `(iii)`
endpoint reduces under the bounded cascade to a cosmic-history ratio.

Hence retaining `L` requires retaining at least one cosmic-history ratio.
`A_min` carries only local-algebra / lattice / dynamics content; cosmic
history is the time-evolved ensemble of matter, radiation, and `Lambda`
densities, which is a separate macroscopic input not encoded in the
local minimal stack.

Therefore on `A_min` alone, `L` cannot be derived. `QED`

## 4. Closure-pathway corollary

By §2, retaining numerical `H_0`, `H_inf`, or `R_Lambda` from `A_min`
alone is impossible; a `(C1)` premise is required. By §3, retaining `L`
from `A_min` alone is impossible; a `(C2)` or `(C3)` premise is required.

Lane 5 closure is the joint retention of `H_0` (numerical) and `L`
(equivalently `Omega_Lambda`). It therefore requires both:

- a `(C1)` premise (absolute scale), AND
- a `(C2)` or `(C3)` premise (dimensionless `L`).

No single class is sufficient on its own:

- `(C1)` alone fixes `R_Lambda` (hence `H_inf`) numerically but leaves
  `L` open, so `H_0 = H_inf / sqrt(L)` is not derivable.
- `(C2)` or `(C3)` alone fixes `L` but leaves the absolute time scale
  open, so `H_0` and `R_Lambda` remain non-numerical.

Hence Lane 5 closure requires premises from at least two of the three
classes — specifically `(C1)` and one of `{(C2), (C3)}`. `QED`

The routes reviewed in the Hubble-H0 workstream all map into this taxonomy:

- **R6** (direct `R_Lambda` derivation, blocked by Planck lane) ∈ `(C1)`.
- **R5** (eta retirement audit) ∈ `(C2)` (eta retirement is a cosmic-
  history-ratio retirement via the cascade).
- **R3** (open-number reduction theorem, completed Cycle 2) is structural
  framing; on its own it does not close Lane 5.
- **R4** (Hubble Tension Structural Lock theorem, completed Cycle 1) is
  not a closure route; it is a falsifier on the surface.
- A future direct `Omega_Lambda` derivation from a vacuum/topology argument
  ∈ `(C3)`.

The complete Lane 5 closure path requires one route from `(C1)`-class
landed AND one route from `(C2)`-or-`(C3)`-class landed.

## 5. What this no-go closes and does not close

**Closes.**

- The "no fourth class of derivation" program-bounding statement made
  informally in `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md`
  §3.2.
- A precise classification of Lane 5 closure routes into the three
  classes `(C1), (C2), (C3)`.
- A precise statement of why `A_min` alone is insufficient.

**Does not close.**

- `(C1)`: the Planck-lane status. The conditional completion packet
  remains live; this no-go does not predict that `(C1)` is impossible,
  only that `A_min` alone is insufficient. Promotion of the
  conditional-completion premise (gravitational boundary/action carrier
  identification) lands `(C1)`.
- `(C2)`: the DM/leptogenesis lane status. Multiple no-gos have closed
  individual selector branches; the surviving live branches
  (`eta/eta_obs = 0.1888` exact one-flavor; `eta/eta_obs = 1.0`
  reduced-surface PMNS) remain open, and promotion lands `(C2)`.
- `(C3)`: this no-go does not rule out a direct framework-derivation of
  `Omega_Lambda` from a separate vacuum/topology argument. Such a route
  has not been opened in this workstream; it remains hypothetical.

## 6. Falsifier

The no-go is falsified if a candidate Lane 5 closure is exhibited that
derives numerical `H_0` from `A_min` alone, without any premise drawn
from `{(C1), (C2), (C3)}`. The proof's case structure (§2-§4) shows this
is impossible, so the falsifier is in principle existential — exhibit a
counterexample, and the no-go falls.

## 7. How this advances Lane 5

Before this no-go, the program-bounding statement was informal in the
Cycle-2 open-number reduction theorem. After this no-go, Lane 5's
closure pathways are:

- formally limited to `{(C1), (C2), (C3)}`;
- each pathway has a sharp open-premise statement;
- the workstream's effort allocation is correctly directed at retiring
  one of those three premises.

The bounded cosmology cascade in `OMEGA_LAMBDA_DERIVATION_NOTE.md`
(`eta -> Omega_b -> R -> Omega_DM -> Omega_m -> Omega_Lambda`) is the
explicit `(C2)` pathway. The Planck-lane work is the explicit `(C1)`
pathway. There is currently no active `(C3)` pathway.

## 8. Cross-references

- `MINIMAL_AXIOMS_2026-04-11.md` — `A_min` definition.
- `docs/publication/ci3_z3/INPUTS_AND_QUALIFIERS_NOTE.md` — current input
  ledger; absolute-scale pin.
- `PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md`,
  `PLANCK_SCALE_CONDITIONAL_COMPLETION_NOTE_2026-04-24.md`,
  `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`
  — `(C1)` pathway status.
- `OMEGA_LAMBDA_DERIVATION_NOTE.md` — bounded cosmology cascade `(C2)`.
- `OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md`,
  `COSMOLOGY_SINGLE_RATIO_INVERSE_RECONSTRUCTION_THEOREM_NOTE_2026-04-25.md`,
  `HUBBLE_TENSION_STRUCTURAL_LOCK_THEOREM_NOTE_2026-04-26.md` (Cycle 1),
  `COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md` (Cycle 2)
  — retained cosmology theorem stack used in §3-§4.
- `docs/lanes/open_science/05_HUBBLE_CONSTANT_DERIVATION_OPEN_LANE_2026-04-26.md`
  — Lane 5; this no-go formalizes the closure-pathway classification.
- the Hubble-H0 workstream route portfolio — routes R1-R8.

## 9. Boundary

This is a structural no-go bounding the closure space for Lane 5. It does
not claim that any of `(C1), (C2), (C3)` is impossible. It does not
retire any input; it classifies what retirement requires. External
references are limited to the cited retained items and the standard
dimensional analysis of `H_0` (textbook; admitted convention).

A runner is not authored for this cycle: the no-go is a structural
case-analysis on `A_min` and the retained cosmology stack, not a
numerical claim. The proof's case structure (§2-§4) is verified by
inspection rather than by sympy/numpy.

## Audit dependency repair links

This graph-bookkeeping section records explicit dependency links named by a prior conditional audit so the audit citation graph can track them. It does not promote this note or change the audited claim scope.

- [minimal_axioms_2026-04-11](MINIMAL_AXIOMS_2026-04-11.md)
- [cosmology_open_number_reduction_theorem_note_2026-04-26](COSMOLOGY_OPEN_NUMBER_REDUCTION_THEOREM_NOTE_2026-04-26.md)
- [omega_lambda_derivation_note](OMEGA_LAMBDA_DERIVATION_NOTE.md)
- [cosmology_scale_identification_and_reduction_note](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
- [omega_lambda_matter_bridge_theorem_note_2026-04-22](OMEGA_LAMBDA_MATTER_BRIDGE_THEOREM_NOTE_2026-04-22.md)
- [planck_scale_lane_status_note_2026-04-23](PLANCK_SCALE_LANE_STATUS_NOTE_2026-04-23.md)
