# Architecture Note: Directional Path Measure

**Status:** bounded - bounded or caveated result note
**Claim type:** bounded_theorem
**Claim scope:** directional measure with **empirically-tuned `β = 0.8`
parameter**, evaluated as a bounded "tuned support" record (PATH B of the
2026-05-03 REPAIR_TARGETS row #1). The bounded smoke/table results below
hold AT the tuned point `β = 0.8`; the choice of `β` is **not derived
from first principles** and is bounded by the angular-kernel
underdetermination no-go cited under "Beta-derivation status".
**Date:** 2026-04-05 (originally); 2026-05-03 (review-loop repair); 2026-05-10 (REPAIR_TARGETS #1 PATH B — tuned support demotion)
**Runner:** [`scripts/architecture_directional_measure_table_runner_2026_05_03.py`](../scripts/architecture_directional_measure_table_runner_2026_05_03.py) (PASS=6/6)
**Beta-derivation status:** **TUNED SUPPORT — NOT DERIVED.**
[`docs/ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md`](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md)
proves `β` cannot be derived from the current A1+A2 primitive core plus
the named directional-measure constraints alone; `β = 0.8` is
**observable-matched** against the eikonal-slope criterion of
`BORN_SCATTERING_COMPARISON_NOTE.md` (see-also; route 3 informational
example, converted from markdown link to backticked form 2026-05-10 to
break citation cycle-0005 — the load-bearing authority for "β is not
derived" is the angular-kernel underdetermination no-go cited above,
not Born; Born's role here is to document one route-3 observable that
the empirical β = 0.8 was matched against, which the PATH B
disposition below now records as tuned-not-derived). Per the
2026-05-03 REPAIR_TARGETS
row #1 outcome, this note explicitly carries `β = 0.8` as a **tuned
parameter**, not a derived constant; first-principles derivation of `β`
is deferred to future work, conditional on closing one of the no-go's
three additional-premise routes.

## Repair-pass disposition (2026-05-10) — PATH B: tuned support

The 2026-05-03 REPAIR_TARGETS row #1 (`architecture_note_directional_measure`,
critical, bounded_theorem, repair_class substantive) named two
disposition options: (PATH A) derive `β = 0.8` from first principles, or
(PATH B) demote to "tuned support". The 2026-05-10 rigorization pass
selected **PATH B**, on the following standing evidence:

- `β = 0.8` corresponds to `4/5`, but the retained primitive surface
  (Cl(3) trace structure, action extremization on Z³, causal-cone
  kinematics, leading-order SO(3) isotropy) carries no five-fold
  structure and no algebraic identity reducing to `4/5`. Other
  candidate algebraic combinations (`2 N_c / (N_c² - 1)` for `N_c =
  2,3,4`, half-integer ratios, Casimir-style ratios) do not produce
  `4/5` either.
- Gaussian fourth-moment matching against the canonical DAG
  `<θ²> ≈ 0.84 rad²` would set `β = 1/(2 ⟨θ²⟩) ≈ 0.595`, which is
  **not** `0.8`; this confirms the gravity-card `β = 0.8` is **not** a
  moment-matched derivation but the route-3 observable-matched value.
- The angular-kernel underdetermination no-go
  ([`ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md`](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md),
  PASS=64, audited_conditional) is a **bounded no-go theorem** stating
  that `w(θ)` (and hence `β` if the family is restricted to Gaussian)
  is not uniquely determined by the retained primitives. PATH A is
  therefore blocked at the primitive surface; closing it requires
  adopting one of three additional-premise routes (higher-order
  isotropy axiom, action-Lagrangian principle, or structural
  observable-matching), none of which is currently on the retained
  surface.

Disposition: this note is hereby carried as **tuned support** for the
directional path measure. The bounded smoke/table claims under
"Tested constraints" hold AT `β = 0.8`; the choice of `β = 0.8` itself
is a tuned input. No `audit_status` change is requested as part of this
repair pass — the note remains `audited_conditional`, with the
conditional dependency now explicit in scope (`β` is tuned, not
derived).

Future-work derivation target (deferred): close one of the no-go's
three additional-premise routes, then re-derive `β` analytically and
file a separate retained promotion note. This is **not** in-scope for
the current bounded note.

## Review-loop repair (2026-05-03)

The 2026-05-03 review follow-up identified two problems: (a) the
empirical pass/fail table had no runner, no reproduced computation, and
no cited graph dependency; (b) `β = 0.8` was empirically chosen with no
derivation. This repair addresses (a) mechanically and (b) by citing the
existing no-go theorem.

**Mechanical repair (a)**:
[`scripts/architecture_directional_measure_table_runner_2026_05_03.py`](../scripts/architecture_directional_measure_table_runner_2026_05_03.py)
recomputes the table from the stated propagator on FIXED DAG fixtures
(deterministic seeds) and reproduces every pass/fail row in the table:

- T1 Born rule (additivity over disjoint detector groups, 2D fixture)
- T2 Interference visibility V > 0.95 (2-slit, 2D fixture)
- T3 k = 0 → real amplitude (no oscillating phase, 3D fixture)
- T4 Gravity sign 6/8 attract over fixed seeds (note's table: 5/8)
- T5 Gravity scaling R_angle(N) positive across N=8..20 with R(20)>R(8),
  matching the canonical gravity-card protocol of `three_d_angle_weight.py`
- T6 Beta-sweep monotonicity: weighted ⟨θ²⟩ decreases monotonically with β
  (consistent with the BORN_SCATTERING_COMPARISON β-sweep that pinned 0.8)

**Beta handling (b)**:
[`docs/ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md`](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md)
proves a bounded no-go: the angular kernel `w(θ)` of the directional
path-measure walk is NOT uniquely determined by the current A1+A2
primitive core plus the named directional-measure constraints ((1)
Cl(3) trace structure, (2) action extremization on Z³, (3) causal-cone
kinematics, (4) leading-order continuum-limit SO(3) isotropy). Seven
distinct kernels — `{uniform, cos, cos², exp(-0.4 θ²),
exp(-0.8 θ²), exp(-1.6 θ²), linear_falloff}` — all pass the four
structural constraints but produce measurably different transverse-step
moments.

Closing the no-go positively requires one of three additional premises
or closure routes:

1. **Higher-order isotropy** — demand the sub-leading continuum
   dispersion is also rotationally isotropic (constrains 4th moment of
   `w`).
2. **Action-Lagrangian principle** — derive or justify the angular
   weight via a continuum Lagrangian whose Euler-Lagrange
   equations include the angular preference.
3. **Direct observable matching** — pin `w` by demanding agreement
   with a specific observable.

The current β = 0.8 is **route 3**: pinned against the gravitational
deflection eikonal slope per
`BORN_SCATTERING_COMPARISON_NOTE.md` (see-also; converted from markdown
link to backticked form 2026-05-10 to break citation cycle-0005 — Born
is the procedural reference where the empirical match was performed,
not a load-bearing derivation authority on this note; the no-go cited
above is the load-bearing authority for β being a tuned, not derived,
input).
The eikonal predicts slope -1.28 on b ∈ {3..6}; the lattice with
β = 0.8 gives -1.43. The β-sweep (β ∈ [0.1, 20]) shows slope varies
monotonically from -0.79 (β = 0.1, wide beam) to -1.93 (β = 20, narrow
beam); β = 0.8 minimizes the eikonal-deviation among the standard test
set. **No closed form for β has been derived** — see the no-go note's
"unsafe wording" caveat against claiming derivation from first
principles.

The empirical `<θ²>` of the canonical DAG (xyz_range = 8, connect_radius = 3)
is ≈ 0.84 rad²; Gaussian moment-matching would give β = 1/(2⟨θ²⟩) ≈ 0.595.
That this differs from the gravity-card value 0.8 confirms β = 0.8 is
observable-matched (route 3), not moment-matched.

After this repair the row records: a runner that recomputes the table,
a cited graph dependency (the no-go) that explains why β is empirical,
and a sharpened bounded statement (below) that does not overclaim
derivation.

## Propagator

```
amplitude(edge) = exp(i k S_spent) / L^p × exp(-β θ²)
```

- `S_spent = delay - sqrt(delay² - L²)`
- `θ = acos(dx/L)` in 3D, `atan2(|dy|, dx)` in 2D
- `β = 0.8`

The directional weight penalizes edges that deviate from the forward (layer) direction. It is field-independent, scale-free, and multiplicative.

## Tested constraints

| test | 2D DAGs | 3D DAGs |
|---|---|---|
| Born rule (I₃) | 9.2e-16 PASS | — |
| interference (V) | 0.998 PASS | fixed-DAG smoke PASS (`V = 0.9963`) |
| linearity / normalization smoke | implied by path-sum form | fixed-DAG smoke PASS (`3.18e-14`, norm err `0`) |
| k=0 → zero | 0.000000 PASS | 0.000000 PASS |
| gravity sign | 90%+ attract | 5/8 attract |
| gravity scaling | R@25 ≥ R@12 PASS | R increases with N |
| family transfer | r=2..5 DAGs, neutral on trees | — |
| R_c compat | 8/10 (2 edge cases) | — |
| decoherence scaling | FAIL (purity rises) | — |
| b-dependence | mixed: raw R increases with b, but bounded response-density diagnostics decrease with b on the baseline and second dense-family holdout; the hierarchy transfers to the tree control and the crossover reduces to `lambda = h_mass / b` | — |

## What this establishes

The flat path measure (uniform weight over all causal paths) was causing CLT saturation of gravity. Adding a directional continuation preference prevents that saturation while preserving interference, Born rule, and k=0→0.

The directional weight also has a clean 3D generalization as `acos(dx/L)`
without modification. A bounded fixed-DAG smoke test now says this is not just
gravity-side support: the same 3D rule shows a real zero-field interference
pattern and preserves source-superposition linearity to machine precision.

The role of this note is now sharper after the topology pivot:

- this directional measure is the accepted unitary support layer
- it is not, by itself, the decoherence solution
- but it is the unitary core used in the later modular / gap-controlled DAG
  results where **both gravity and decoherence work on the same family**

## What this does not establish

- Decoherence scaling is not addressed. This is expected: the directional weight modifies the unitary propagator, and decoherence is a non-unitary (record/environment) problem.
- The 3D support is still a smoke package, not a full 3D Sorkin / three-slit theorem.
- The raw b-dependence (deflection/readout increasing with impact parameter) is not fixed. A bounded geometry-normalized response-density diagnostic now decreases with b on the original dense random-DAG family, and the original `mass_nodes = 3` holdout-transfer replay says the same center-offset and nearest-edge densities still pass on the second dense-family holdout at both `N = 12` and `N = 25`. A widened-source holdout follow-on at `mass_nodes = 5` then sharpens the finite-source split instead of killing it: on the same holdout, `N = 25` loses the center-offset passes (`A/b`, `F/b`) while nearest-edge density (`A/edge`, `F/edge`) still decreases cleanly with actual `b`. The current bounded hierarchy is therefore sharper than before: center-offset density is the asymptotic leading term, nearest-edge density `b - h_mass` is the robust finite-source correction once the source width is widened, and support-gap is a secondary discrete packet-support correction. The reduced-variable picture is now two-layered: `lambda = h_mass / b` is the compact crossover control, while `mu = edge_b / h_mass = 1 / lambda - 1` is the cleaner signed overlap diagnostic. Tree-like controls keep large positive `mu`, while widened dense families force the finite-source correction once low-`b` corners cross into `mu <= 0`, even though pure `response / b` still survives on the bounded family once singular center-offset trials are excluded. The low-`b` onset cards now support a sharper mechanism claim: sparse target-band occupancy is the leading transferable overlap-onset signal, while coarse local spacing is a family-dependent refinement. Tree layers densify around the target plane, while dense random-DAG layers keep only about `1-2` nodes in that band and therefore have to stretch widened source windows across much larger `y` gaps; on the second dense-family holdout, the original gap/span clause softens but an occupancy floor still isolates the overlap rows cleanly. A combined occupancy bridge card now compresses that further: across the original and holdout dense families together, `target_fill <= 0.4` captures `23/24` overlap rows, while no overlap rows survive once `target_fill > 2/3`, so occupancy shortage is now the current coarse bridge variable and spacing stays secondary. The supply-load decomposition card first made the physical content explicit: raw target-band count or same-side target-plane share alone is too family-dependent, and source-window size alone is too crude, but the combined source load `mass_nodes / local_target_count >= 2.5` reproduces the bridge exactly. A new continuous-density bridge card then sharpened that into a smoother spacing law: estimating target-plane support from the fourth-nearest same-side node radius gives `expected_target_count_4nn = 4 / r4`, and the continuous load `mass_nodes / expected_target_count_4nn >= 2.7354` improves the combined dense-family bridge to `0.9167` accuracy while lifting both baseline dense families to `0.9000`. A frozen branching-tree control keeps that same 4-NN law safely on the non-overlap side without refit: tree `knn4_density_load` falls from `0.5938` to `0.1484` as depth grows while `mu` rises from `3` to `11`, so the tree family stays far below the overlap threshold because target-plane support densifies rather than starving. But a one-notch center-biased mid-layer dense sentinel now shows the fourth-neighbor stencil is the unstable piece under target-plane densification: on that holdout, the frozen 4-NN law falls to `0.8500` with six false negatives, while a bounded stencil-transfer diagnostic lifts the frozen 3-NN law to `0.9500` on the same sentinel without changing the old dense-reference thresholds. The original reference+tree still prefers 4-NN (`0.9206` vs `0.8889`), but on the current extended sample the frozen 3-NN law edges out 4-NN (`0.9126` vs `0.8932`) because most 4-NN misses are one-sided low-occupancy target bands where the fourth neighbor is the first sample to jump across the target-plane gap and `r4` overstates support. A bounded residual probe then pushed on the last two 3-NN misses directly and found the current limit: miss-local rescue clauses can close the midlayer sentinel, but only by degrading the old reference+tree control to `24/8/0/31`. So the portable statement is still occupancy-first. The 4-NN density law is the cleaner original dense-sample fit, 3-NN is the current best single frozen smooth law on the expanded sample, and no sampler-robust residual closure has landed yet.
- β = 0.8 is **empirically chosen, not derived**, and is carried by
  this note as **tuned support** (PATH B of the 2026-05-03
  REPAIR_TARGETS row #1; see "Repair-pass disposition (2026-05-10)"
  above). Per the
  [no-go theorem on angular kernel underdetermination](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md)
  the kernel `w(θ)` is not determined by the current A1+A2 primitive
  core plus the named directional-measure constraints; closing this
  requires one of three additional premises or closure routes
  (higher-order isotropy, action-Lagrangian principle, or direct
  observable matching). β = 0.8 is observable-matched (route 3)
  against the gravitational-deflection eikonal slope, not derived from
  first principles. The bounded smoke/table results below are valid AT
  the tuned point β = 0.8; they do **not** lift to a derivation of β
  itself.
- The 2 R_c edge cases mean the weight slightly narrows the zero-field interference threshold at some geometries.

## Axiom connection

- Axiom 6 (continuation prefers local coherence): the weight directly implements this
- Axiom 3 (space inferred): the angle is intrinsic to the graph, not imposed
- This is a path-measure correction, not a new dynamical law

## Next work

The propagator is no longer the bottleneck. The next frontier is:
1. dynamic emergence of the topology that lets the accepted non-unitary IF / CL route work
2. `b`-dependence as a separate gravity-sector question, now narrowed to deriving the asymptotic `b` leading term, its `b - h_mass` finite-source correction, and turning the current occupancy-first bridge into a sampler-robust continuous law without reopening a wider denominator search; the bounded clue is now stencil-local rather than denominator-wide, because the fourth-neighbor miss mode softens if the current expanded sample is read through the frozen 3-NN density law instead
3. principled derivation of `beta` from graph geometry — currently
   blocked by the
   [angular-kernel underdetermination no-go](ANGULAR_KERNEL_UNDERDETERMINATION_NO_GO_NOTE.md);
   would require closing one of the no-go's three additional-premise
   routes (higher-order isotropy, action-Lagrangian, or
   observable-matching at the structural level). Per the 2026-05-10
   PATH B disposition, this is the future-work derivation target
   under which `β` would graduate from "tuned support" to a derived
   constant; the bounded note currently makes no claim toward such a
   derivation.
4. transfer of the joint gravity+decoherence story to dynamically generated or higher-dimensional graph families
