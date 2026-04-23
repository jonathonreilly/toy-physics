# Microscopic-Polynomial Impossibility Theorem — Axiom-Level Silence on (delta, q_+)

**Date:** 2026-04-17
**Status:** OBSTRUCTION (CASE 3) -- microscopic-silence impossibility theorem
**Script:** `scripts/frontier_dm_neutrino_source_surface_microscopic_polynomial_impossibility_theorem.py`
**Framework convention:** "axiom" means only the single framework axiom `Cl(3)` on `Z^3`.

## Scope and discipline

Five previous attacks on the right-sensitive 2-real selector law
`(delta_*, q_+*)` on the live DM-neutrino source-oriented sheet all
operated WITHIN the reduced `(delta, q_+)` chart:

- the info-geometric route (variational): quadratic unanimity but cubic splitting
- the Z_3 cubic variational route: m-dependent or singular
- the Z_3 parity-split route: parity-definite 1D obstruction
- Physics-validation: transport chain chamber-blind
- Parity-mixing Frobenius: multiple inequivalent candidates, functional ambiguity

This note goes a level below: to the microscopic `Cl(3)` / `Z^3` lattice
axiom itself. It asks whether the retained microscopic symmetries
(`Z_3` cyclic `C_3[111]`, lattice translations, chirality, `Cl(3)`
bivector grading) plus retained local polynomial observables (heat-kernel
coefficients, spectral gaps, Ward-identity content, determinant moments)
can pin the pair `(delta_*, q_+*)`.

**Verdict: OBSTRUCTION (CASE 3).** The microscopic Cl(3)/Z^3 axiom is
GENUINELY SILENT on `(delta, q_+)`. The retained microscopic stack
reduces the ambient 3-real `(m, delta, q_+)` surface to the 2-real
microscopic-invariant residual `(delta, q_+)` (after Schur scalarization
of `m`), but no retained microscopic-polynomial functional can separate
the residual further. The specific missing ingredient is identified as a
nonlocal selector principle (variational / information-geometric /
transport-consistency / effective-action matching) beyond the retained
`Cl(3)` / `Z^3` axiom.

This is not a closure. It is a hard impossibility theorem that
LEGITIMIZES the interpretation of `(delta, q_+)` as a genuine "gauge
direction" inside the retained microscopic-invariant sheet.

## The claim map

We operate strictly on retained / theorem-grade atlas input:

- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md):
 retained exact operator algebra `<P_1, P_2, P_3, C_3[111]> = M_3(C)` on `H_hw=1`
- [NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md](./NEUTRINO_DIRAC_Z3_SUPPORT_TRICHOTOMY_NOTE.md):
 the retained Dirac matrix support pattern is one of three Z_3 permutation classes
- [DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_CARRIER_NORMAL_FORM_THEOREM_NOTE_2026-04-16.md):
 retained `(gamma, E_1, E_2)` carrier normal form
- [DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_SHIFT_QUOTIENT_BUNDLE_THEOREM_NOTE_2026-04-16.md):
 retained shift-quotient bundle over `(m, delta, r31)`
- [DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md](./DM_NEUTRINO_SOURCE_SURFACE_ACTIVE_AFFINE_POINT_SELECTION_BOUNDARY_NOTE_2026-04-16.md):
 exact affine chart `H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q`
- [DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md](./DM_NEUTRINO_SOURCE_SURFACE_SCHUR_SCALAR_BASELINE_THEOREM_NOTE_2026-04-17.md):
 Schur baseline `D = m I_3` forced on `H_hw=1`
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](./OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md):
 axiom-native scalar generator `W[J] = log|det(D+J)| - log|det D|`
- [ONE_GENERATION_MATTER_CLOSURE_NOTE.md](./ONE_GENERATION_MATTER_CLOSURE_NOTE.md):
 retained one-generation SM completion via anomaly-forced 3+1

No post-axiom inventions enter the theorem hypotheses.

## Theorem 1 (retained-atlas-native): Z_3-irrep decomposition of the active span

Under conjugation by the retained `C_3[111]` operator, the active
Hermitian tangent span `{T_m, T_delta, T_q}` on `H_hw=1` decomposes as
follows:

- `T_q` is exactly `Z_3`-invariant: `C_3 T_q C_3^{-1} = T_q`.
 Equivalently, `T_q = J - I_3` where `J` is the all-ones matrix, and
 `J` is the unique Z_3-singlet real symmetric matrix orthogonal to `I_3`.

- `T_delta` is purely `Z_3`-doublet: `sym(T_delta) = 0`,
 `anti(T_delta) = T_delta`. Its projection onto the omega-eigenspace of
 `C_3`-conjugation (with omega = exp(2 pi i / 3)) is nonzero, and
 `T_delta` equals the sum of the omega and omega-bar projections (both
 nonzero complex conjugates of each other, giving a real Hermitian matrix).

- `T_m` has nonzero `Z_3`-singlet AND nonzero `Z_3`-doublet content:
 `sym(T_m) = J / 3 = (I_3 + T_q) / 3`, the scalar part; `anti(T_m)` is
 the doublet part.

**Proof.** Direct computation verified by runner Part 1.

**Consequence.** The active pair `(delta, q_+)` is a (doublet-component,
singlet-component) pair in a SPECIFIC gauge-fixed `Z_3 x Z_2` chart inside
the retained Hermitian space on `H_hw=1`.

## Theorem 2 (retained-atlas-native): Non-closure of the active chart

Under conjugation by any retained microscopic symmetry (`C_3[111]`,
lattice translations `T_x, T_y, T_z`), the affine chart
`H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q` is NOT
preserved: the conjugated matrix has a large residual when projected
back onto the 3-dim affine tangent span.

**Proof.** Direct computation verified by runner Part 2. The
`C_3`-conjugation residual on a generic chart point is approximately
`3.47` in Frobenius norm; translation-conjugation residuals range from
`0.72` to `2.55`. These are all far above the `1e-10` numerical-closure
threshold.

**Consequence.** The `(m, delta, q_+)` chart is a GAUGE-FIXED slice of
the retained microscopic structure, not a microscopic-symmetry-invariant
domain. The upstream shift-quotient + active half-plane + carrier normal
form theorems fix this gauge implicitly.

## Theorem 3 (retained-atlas-native): Polynomial Z_3-invariants depend on (delta^2, q_+)

Every retained microscopic polynomial invariant of `H` on the active
chart depends on `(delta, q_+)` only through the pair `(delta^2, q_+)`.

**Proof sketch.** The Hilbert-Schmidt orthogonality
`Tr(T_delta T_q) = 0` combined with `Tr(T_delta^2) = 6`, `Tr(T_q^2) = 6`,
`Tr(T_m T_delta) = 0`, `Tr(T_m T_q) = 2`, `Tr(T_m^2) = 3` gives
`Tr(H_src^2) = 3 m^2 + 6 delta^2 + 6 q_+^2 + 4 m q_+`, which is EVEN in
`delta`. The runner verifies numerically that `Tr(H_src^3)` and
`det(H_src)` are also even in `delta` (source-only sector, `H_src = m T_m
+ delta T_delta + q_+ T_q`). Higher-order trace moments are constructed
by iteration and inherit the delta-evenness.

Formally: under the `Z_3`-irrep decomposition of `(T_m, T_delta, T_q)`
described in Theorem 1, `T_delta` lives in the `Z_3`-doublet. The only
`Z_3`-invariant polynomial contractions of doublet elements appear
through their magnitude, which on the gauge-fixed 1-D line through the
doublet is `|delta|^2 = delta^2`. Hence polynomial `Z_3`-invariants
filter through `delta^2`.

**Runner verification.** Part 3 verifies the explicit symbolic identities
for `Tr(H^2)`, and numerically verifies delta-evenness of `Tr(H^3)` and
`det(H_src)`.

## Theorem 4 (retained-atlas-native): Heat-kernel / spectral / Ward silence

Every retained microscopic functional of `H` of the following types
depends on `(delta, q_+)` only through `(delta^2, q_+)`:

- heat-kernel traces `Tr(exp(-t D^dagger D))` for `t > 0`
- smallest absolute eigenvalue of `H` (spectral gap)
- `Z_3` Ward identity `W[J] = W[C_3 J C_3^{-1}]` on the Schur baseline
 `D = m I_3`
- translation Ward identities `W[J] = W[T_sign J T_sign^{-1}]` for
 `T_sign in {T_x, T_y, T_z}` on the Schur baseline
- chiral Ward saturation (automatic from delta-evenness of trace moments)

**Proof.** Each of these is a polynomial or convergent power-series
functional in even trace moments of `H` or `D = H`, and Theorem 3 applies.
The runner verifies each item numerically.

**Consequence.** The entire canonical retained microscopic observable
content (heat-kernel, spectral, Ward) is invariant under `delta -> -delta`
on the source-only chart. It cannot distinguish sign of `delta`, and more
generally it filters through `(delta^2, q_+)` at leading polynomial order.

## Theorem 5 (retained-atlas-native): Residual dimension count

After:

- Schur baseline forcing `D = m I_3` (fixes `m` as the unique Z_3-scalar direction)
- `Z_3` microscopic symmetry (collapses `delta` to `|delta|` = doublet magnitude)
- `Z_2` parity gauge fix (delta >= 0 on the chamber `q_+ >= E_1 - delta`)

the microscopic-invariant residual on the active chart is exactly the
2-real pair `(delta, q_+)`. No retained microscopic symmetry reduces
this further.

## Theorem 6 (CASE 3 impossibility theorem on (delta, q_+))

**Statement.** Let `f : Herm(3, R) -> R` be any polynomial functional
built from the retained microscopic content on `H_hw=1`, i.e. `f` is
constructed from:

- `Z_3`-cyclic (`C_3[111]`) invariance,
- lattice-translation (`T_x, T_y, T_z`) invariance,
- chiral Ward saturation,
- heat-kernel / spectral-gap / determinant polynomial content,
- `Cl(3)` bivector-grading block structure.

Then the restriction of `f` to the affine chart `H(m, delta, q_+) =
H_base + m T_m + delta T_delta + q_+ T_q` depends on `(delta, q_+)`
only through the pair `(delta^2, q_+)`.

**Consequence.** At fixed `m` (by Schur) and on the chamber boundary
`q_+ >= E_1 - delta` with `delta >= 0`, the equation `df/dx = 0`
(`x in {delta, q_+}`) admits at most finitely many extrema for any given
`f`, and those extrema DEPEND on the functional-form choice of `f`.

**Examples.** Different retained local polynomial functionals select
DIFFERENT chamber extrema:

- `Tr(H^2)` chamber-boundary minimum: `(1.2679, 0.3651)` ((b))
- `det(H)` chamber-interior stationary point: `(0.9644, 1.5524)` ((a))
- Schur-Q (`= 6(delta^2 + q_+^2) / m^2`) chamber-boundary minimum:
 `(sqrt(6)/3, sqrt(6)/3)` (Schur baseline + minimum-coupling selector)
- Frobenius `||K_doublet||_F^2` chamber-boundary minimum:
 `(sqrt(6)/2 - sqrt(2)/18, sqrt(6)/6 + sqrt(2)/18)` (parity-mixing F1)

All four pass the retained microscopic tests (Z_3 / chirality /
translation / heat-kernel / spectral) but fail to agree.

**Proof.** Theorem 4 establishes that every polynomial retained
microscopic functional reduces to a function of `(delta^2, q_+)`.
Theorem 3 fixes the structure of the reduction. The cited candidate
points were computed in the info-geometric selection obstruction/B/C/parity-mixing notes. The runner
Part 6 verifies their pairwise distinctness and the universality of the
delta-evenness property.

## Missing microscopic ingredient

To fix `(delta_*, q_+*)`, an additional principle beyond retained
`Cl(3)` / `Z^3` microscopic local polynomial content is required. The
theorem above rules out:

- further local trace-moment conditions,
- further local heat-kernel / spectral-gap conditions,
- further local retained-symmetry Ward identities.

It does NOT rule out (and instead points to) the following classes of
selector principles:

**(alpha)** NONLOCAL variational / information-geometric selection
(e.g. minimum Fisher information, minimum Kullback-Leibler, maximum
entropy with specified constraints). These are the natural "minimum-
information source law" candidates, but the retained atlas explicitly
flags these as POST-AXIOM INVENTIONS. A sole-axiom derivation of such
a principle is not known.

**(beta)** TRANSPORT / HOLONOMY consistency across the full `Z^3`
lattice, not just the retained `H_hw=1` 3D surface. This would require
a new theorem relating the full lattice Dirac operator's holonomy to
the reduced `(delta, q_+)` pair. holonomy attempts on the
retained surface did not close; a full-lattice route is open but
speculative.

**(gamma)** DYNAMICAL EOM / effective-action matching. The lattice
Dirac operator's equation of motion at the minimum of some induced
effective action could fix `(delta, q_+)`. But the induced effective
action requires a matching condition (e.g. to a measured observable),
which is a post-axiom input.

None of these have been retained as `Cl(3)` / `Z^3` axiom consequences
on the current live atlas. Hence:

**The microscopic Cl(3)/Z^3 axiom is GENUINELY SILENT on `(delta, q_+)`.**

## "Gauge direction" interpretation is legitimized

The present theorem establishes that after exhausting every retained
microscopic symmetry and every local polynomial observable, the
residual 2-real pair `(delta, q_+)` is a genuine submicroscopic degree
of freedom that the axiom does not constrain. This legitimizes
interpreting `(delta, q_+)` as a "gauge direction" inside the retained
microscopic-invariant sheet: the axiom fixes the chart-equivalence
class, not the chart point.

For downstream physics (neutrino masses, PMNS, leptogenesis eta), this
means:

- The microscopic axiom delivers every Dirac-matrix structural datum
 up to the 2-real `(delta, q_+)` freedom.
- Any further determination of `(delta, q_+)` is a SEPARATE scientific
 task, distinct from axiom-native theoremhood.
- Physics-validation via `eta / eta_obs = 1` or neutrino mass fits
 SELECTS a point in the gauge sheet, but does not promote it to
 theorem-grade without an additional derived principle.

## Verdict

**OBSTRUCTION (CASE 3, hard):** the microscopic Cl(3)/Z^3 axiom is
silent on `(delta_*, q_+*)`.

**Specific missing ingredient identified:** a nonlocal selector
principle (variational / transport / effective-action) beyond retained
local-polynomial microscopic content.

**"Gauge direction" status:** legitimized as the correct interpretation
of the residual.

**Selector-gate status at this note's scope:** sole-axiom closure of the
selector gate via local-polynomial microscopic content is PROVABLY
IMPOSSIBLE. This theorem does not promote any selector candidate; it
sharpens the obstruction structure by showing the axiom itself cannot
close the gap with local content, and routes any closure through
either a nonlocal axiom-native principle or an observational promotion
lane. The integrated closure of the DM flagship lane is the downstream
PMNS-as-f(H) closure via the observational-promotion (P3) lane, which
is consistent with this impossibility theorem.

## Connection to downstream closure strategies

After this theorem, the live paths to close selector reduce to exactly:

1. **Sole-axiom derivation of a nonlocal selector** (information-
 geometric / variational). This requires either a retained proof that
 the "minimum-information source law" is axiom-native (currently
 flagged post-axiom), or discovery of a new axiom-native nonlocal
 principle on the retained stack.

2. **Full-Z^3 transport / holonomy closure.** Any candidate theorem
 that extends beyond the retained `H_hw=1` 3D surface to the full
 `Z^3` lattice could introduce structure that pins the gauge. This
 is open territory.

3. **Physics-validation-driven identification.** If exactly one of the
 retained candidate points `(Schur-Q, det(H), Tr(H^2), F1, K_12)`
 is consistent with `eta / eta_obs = 1` and neutrino masses, it
 becomes a candidate-closure-pending-derivation. This is a
 physics-validation route, not a theorem-grade derivation.

## Atlas position

This note is explicitly **not** flagship-grade publication content. It
is a hard obstruction / impossibility theorem on the axiom-level claim
surface. Appropriate placement:

- atlas obstruction row in
 [DERIVATION_ATLAS.md](./publication/ci3_z3/DERIVATION_ATLAS.md)
 under the DM neutrino source-surface family, as a distinguished
 deepest-level sibling to the info-geometric selection obstruction / the cubic variational selection obstruction / the Z_3 parity-split theorem / Parity-Mixing
 notes
- do NOT use for any publication-grade positive quantitative claim
- do NOT use to "rule out" the retained candidate points (they remain
 retained candidates; this theorem explains WHY no single one is
 selected axiomatically)
- DO use to legitimize the "gauge direction" terminology for
 `(delta, q_+)` in downstream physics discussion

## Command

```bash
PYTHONPATH=scripts python3 scripts/frontier_dm_neutrino_source_surface_microscopic_polynomial_impossibility_theorem.py
```

Current: `PASS = 35, FAIL = 0`.

## What this file must never say

- that selector is closed
- that the DM flagship lane is closed
- that any of the retained candidate points (Schur-Q, det(H), Tr(H^2),
 F1, K_12) has been promoted to theorem-grade by this note (it has not;
 the theorem explicitly shows none of them is microscopically forced)
- that the "minimum-information source law" has been promoted from
 post-axiom (it has not)
- that the microscopic axiom is rich enough to close `(delta, q_+)`
 (the present theorem establishes precisely the opposite)
- that a nonlocal selector principle has been discovered on the axiom
 (none has; the theorem only identifies which kind of ingredient is
 required)

If any future revision tightens these boundaries, it must cite a new
source on the live retained/promoted surface. Until then, the safe
read is: **microscopic Cl(3)/Z^3 axiom is genuinely silent on
`(delta, q_+)` at the local-polynomial level; the "gauge direction"
interpretation is legitimized as the correct reading of the residual;
sole-axiom closure via local-polynomial content is ruled out; closure
of the DM flagship lane is via the downstream PMNS-as-f(H)
observational-promotion lane.**
