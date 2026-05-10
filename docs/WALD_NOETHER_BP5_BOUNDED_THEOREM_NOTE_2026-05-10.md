# Wald-Noether BP §5 Bounded Theorem Note

**Date:** 2026-05-10
**Claim type:** bounded_theorem
**Status authority:** independent audit lane only.
**Type:** bounded_theorem
**Primary runner:** [`scripts/frontier_wald_noether_bp5_bounded.py`](../scripts/frontier_wald_noether_bp5_bounded.py)

## Claim

Conditional on the two admitted upstream gates named in the
"Explicit admissions" section below — namely

- **(X1) closure of the staggered-Dirac realization gate**
  ([`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)),
- **(X2) audit-ratified link-local first-variation route**
  ([`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)) —

on the time-locked primitive event cell with the source-free state
`ρ_cell = I_16/16`, the gravitational boundary/action density carrier
`P_A` is the Hamming-weight-one packet `P_1`. The conditional
Bekenstein-Hawking entropy on a stationary Killing horizon of area `A`
is then

```text
S_BH = A / (4 G_Newton,lat),    G_Newton,lat = 1
```

in framework lattice units (where `a` is the framework's natural
lattice spacing and `G_kernel = 1/(4π)` is the bare kernel
normalization separated by
[`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)).

This is a bounded restatement of the chain previously composed in
[`BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`](BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md)
and §5 of
[`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md).
The narrowing of this note relative to those prior compositions is the
**explicit listing of admissions** that the chain depends on. This note
does NOT assert that `P_A = P_1` is forced by the two framework axioms
(`A1: Cl(3)`, `A2: Z^3`) alone; the two retained no-gos cited in the
"Constraints respected" section foreclose that stronger reading on the
current authority surface.

## Explicit admissions

The bounded result above rests on exactly the following two admitted
upstream gates. Each admission is named to the canonical parent note in
the live audit graph; the live `effective_status` is reported alongside
so this note's scope is unambiguous.

### (X1) Staggered-Dirac realization gate

**Admitted authority:** [`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md).

**Live audit ledger status (verified 2026-05-10):** `effective_status = open_gate`,
`claim_type = open_gate`.

**Role here:** Theorem 2 of
[`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
selects `P_A = P_1` from the first-order coframe-locality premise. The
link-local first-variation route (X2 below) supplies the action-native
provenance for that locality premise, and that route is itself defined
on the staggered-Dirac/Grassmann action surface. (X1) is therefore the
upstream gate whose closure is needed before (X2) can be the action
route used here, rather than an independent admission of the action
surface.

**Recategorization context:** the staggered-Dirac realization is
recategorized as an open gate (rather than a framework axiom) by
[`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md), which
restores the framework axiom set to the two-axiom core (`A1 = Cl(3)`,
`A2 = Z^3`). No new axiom is introduced or implied by this note.

### (X2) Link-local first-variation route

**Admitted authority:** [`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md).

**Live audit ledger status (verified 2026-05-10):** `effective_status = unaudited`,
`claim_type = positive_theorem`.

**Role here:** the link-local first-variation theorem records that, on
the staggered-Dirac action surface, the fundamental local source
variables `u_a` are one-link / one-axis variables, so the algebraic
first variation `dS_link / du_a` has support on the Hamming-weight-one
packet `P_1`. This is the additional structure that breaks the Hodge
ambiguity flagged by the (X1)-respected retained no-go cited below.
The current note is bounded on this route remaining as the route used;
if (X2) audits clean, the present chain inherits stronger derivational
footing. If (X2) fails audit, the present chain remains the same
bounded statement, but the conditional carrier identification reverts
to the explicit assumption form.

## Constraints respected

The bounded scope of this note respects two retained no-gos that
already foreclose stronger unconditional readings of the same chain.

### Retained no-go 1: Hodge-dual degeneracy under substrate symmetries

**Authority:** [`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md`](FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md).

**Live audit ledger status (verified 2026-05-10):** `effective_status = retained_no_go`,
`claim_type = no_go`, `audit_status = audited_clean` (cross-confirmed by
two independent fresh-context auditors).

**What this no-go forces here:** the stated substrate symmetries
(Boolean event cell + `Cl(3)` spin-lift + time parity + CPT grading +
complex Hilbert/Born surface + tensor-local number algebra) do *not*
force `P_A = P_1` over the Hodge-dual `P_3`. The Hodge-complement map
`* P_1 *^{-1} = P_3` exchanges the two rank-four projectors while
preserving exactly those listed structures. Hence the present bounded
theorem does NOT claim that the substrate symmetries alone force the
carrier; it requires (X2) (the additional action-native first-variation
structure) to break the Hodge degeneracy.

### Retained no-go 2: Free-fermion RT-ratio asymptotes to 1/6, not 1/4

**Authority:** [`BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md`](BH_ENTROPY_RT_RATIO_WIDOM_NO_GO_NOTE.md).

**Live audit ledger status (verified 2026-05-10):** `effective_status = unaudited`
(intrinsic), most recent prior cross-family audit verdict
`audited_conditional` with `auditor_confidence: high`,
`claim_type = no_go`. The internal Widom diamond integral is sound; the
prior `audited_conditional` verdict is dependency-driven (the upstream
carrier-definition authority [`BH_ENTROPY_DERIVED_NOTE.md`](BH_ENTROPY_DERIVED_NOTE.md)
is itself unaudited).

**What this no-go forces here:** the Widom-Gioev-Klich evaluation of
the half-filled 2D nearest-neighbor free-fermion straight-cut RT
bond-dimension ratio gives the asymptote `c_Widom = 1/6`, not `1/4`.
This is a sharp boundary: a discrete boundary readout chosen as the
free-fermion straight-cut RT ratio yields the wrong number. The
present bounded theorem therefore does NOT identify the gravitational
boundary/action density carrier with that straight-cut RT readout; it
identifies the carrier with the action-native first-variation projector
`P_A = P_1`, conditional on (X1) and (X2). The two readouts are
distinct objects in the same family of boundary observables, and the
no-go is what makes that distinction load-bearing.

## Cited authority context

The non-admission citations supply the existing framework chain that
this bounded theorem rides on. These are imported authorities; their
audit statuses are reported but they are not closed by this note.

- [`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
  (live `effective_status = unaudited`, `claim_type = positive_theorem`):
  Theorems 1-3 deriving `P_A = P_1`, `rank(P_A) = 4`,
  `c_cell = Tr(ρ_cell P_A) = 1/4` from first-order coframe locality,
  axis additivity, coframe-slot symmetry, and unit primitive
  response normalization. §5 explicitly names the gravitational
  boundary/action density bridge as the open premise.
- [`PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md`](PLANCK_BOUNDARY_DENSITY_EXTENSION_THEOREM_NOTE_2026-04-24.md)
  (live `effective_status = unaudited`, `claim_type = bounded_theorem`,
  most recent prior audit verdict `audited_conditional` with `auditor_confidence: high`):
  finite-boundary additivity extension `N_A(P) = c_cell A(P) / a²` on
  any finite face-union patch. This is the bounded route from the
  primitive coefficient to a macroscopic boundary density.
- [`BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`](BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md)
  (live `effective_status = unaudited`, `claim_type = bounded_theorem`):
  V1 composition of `c_cell = 1/4` (primitive carrier theorem) with the
  admitted Wald-Noether charge formula and the framework's retained
  Einstein-Hilbert equivalence on PL S³ × R, yielding
  `S_BH = A / (4 G_Newton,lat)` with `G_Newton,lat = 1` forced by the
  chain. The current note is narrower than V1 in that the two upstream
  admissions (X1, X2) are listed explicitly rather than being carried
  implicitly through the §5 bridge phrase.
- [`PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md`](PLANCK_SOURCE_UNIT_NORMALIZATION_SUPPORT_THEOREM_NOTE_2026-04-25.md)
  (live `effective_status = unaudited`, `claim_type = positive_theorem`):
  source-unit normalization separating bare `G_kernel = 1/(4π)` from
  conditional physical `G_Newton,lat = 1`. The 4π geometric factor
  between the bare kernel and the framework lattice-unit Newton
  constant is absorbed by this normalization.
- [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md)
  (meta): records the restored two-axiom core (`A1: Cl(3)`,
  `A2: Z^3`) and the recategorization of the staggered-Dirac
  realization from "axiom" to "open gate". The current note introduces
  no new axiom and uses only this canonical two-axiom labelling.

## Body (algebraic content)

The algebraic content is already verified by existing runners; this
note's substantive content is the explicit admissions framing above.
For completeness:

### Carrier identification (conditional on X1 + X2)

On the time-locked primitive event cell

```text
H_cell ≅ Λ* span(t, x, y, z) ≅ (C²)^4 ≅ C^16,
```

(X1) supplies the staggered-Dirac/Grassmann action surface. (X2)
records that the action-native first variation `dS_link / du_a` has
support on `P_1`. Combined with Theorem 2 of
[`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
(axis additivity + coframe-slot symmetry + unit response
normalization), the conditional carrier is

```text
P_A = P_1 = ∑_{a ∈ {t,x,y,z}} P_{ {a} }.
```

The trace identities

```text
Tr(P_A)        = rank(P_A) = C(4,1) = 4,
Tr(ρ_cell P_A) = 4 / 16     = 1/4,
```

are pure linear algebra on the Boolean event cell and are verified by
[`scripts/frontier_planck_primitive_coframe_boundary_carrier.py`](../scripts/frontier_planck_primitive_coframe_boundary_carrier.py)
and by the existing
[`scripts/frontier_bh_quarter_wald_noether_framework_carrier.py`](../scripts/frontier_bh_quarter_wald_noether_framework_carrier.py).
These identities are NOT new content of this note. The narrowing of
this note is the explicit "conditional on (X1) + (X2)" framing, not the
linear-algebra step.

### Composition with admitted Wald-Noether formula

The Wald-Noether charge formula for the Einstein-Hilbert Lagrangian
`L = R / (16π G_N)` evaluates to

```text
S_Wald = A / (4 G_N)
```

on a stationary Killing horizon of cross-section area `A`. This is
admitted as a universal-physics input by
[`BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md`](BH_QUARTER_WALD_NOETHER_FRAMEWORK_CARRIER_THEOREM_NOTE_2026-04-29.md);
this note does not derive the Wald formula and inherits that admission
unchanged.

Composing the conditional carrier identification with the finite
boundary-density extension and the Wald-Noether formula:

```text
S_BH = A · c_cell = A · (1/4) = A / 4    (framework lattice units, a = 1),
```

which matches `S_BH = A / (4 G_N)` with `G_Newton,lat = 1` after the
source-unit normalization step. This is the conditional `bounded`
conclusion stated at the top of this note.

## Open derivation gap

This note records two named open derivation routes whose closure
would promote the bounded result above to unconditional. Both are
already in flight on the audit graph; the present note does not close
either.

### (a) Staggered-Dirac realization gate closure

The canonical parent identity is
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
(live `effective_status = open_gate`). The closure work is spread
across multiple in-flight supporting notes — Grassmann forcing,
Kawamoto-Smit forcing, BZ corner forcing, physical-species direct
identification, AC narrowing — all currently `unaudited`. Closure
requires either a single canonical proof packet that runs the four
steps in
[`STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md`](STAGGERED_DIRAC_REALIZATION_GATE_NOTE_2026-05-03.md)
end-to-end on `A1 + A2`, or a coordinated retained-grade chain on the
existing supporting notes.

### (b) Link-local first-variation theorem audit promotion

The canonical authority is
[`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
(live `effective_status = unaudited`, `claim_type = positive_theorem`).
Audit promotion requires the independent audit lane to ratify the
algebraic claim that the link-local first variation on the
staggered-Dirac action surface has support on `P_1`, *and* the
conditional claim that the Hodge-dual `P_3` packet is not an
automorphism of the fundamental one-link source domain. Both are
already stated inside that note; ratification is what is open.

## Boundaries

This note does not close:

- the staggered-Dirac realization gate (X1);
- the link-local first-variation theorem (X2);
- the gravitational boundary/action density physical identification
  named in §5 of
  [`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md);
- the Wald-Noether charge formula (admitted as universal physics
  input, not derived);
- the Hawking temperature relation `T_H = κ / 2π` (kinematic side of
  BH thermodynamics; unchanged by this note);
- any higher-curvature correction to the framework's leading-order
  Einstein-Hilbert Lagrangian;
- any new axiom; the framework axiom set remains `A1 + A2` per
  [`MINIMAL_AXIOMS_2026-05-03.md`](MINIMAL_AXIOMS_2026-05-03.md).

## Verification

```bash
PYTHONPATH=scripts python3 scripts/frontier_wald_noether_bp5_bounded.py
```

The runner checks: structural markers on this note (explicit
admissions block, retained-no-go citations, open-derivation-gap
section), existence of all cited authority files, the algebraic
identities `Tr(P_A) = 4` and `Tr(ρ_cell P_A) = 1/4`, the Wald-EH
evaluation `S_Wald = A / (4 G_N)`, the chain identity
`c_cell = 1 / (4 G_Newton,lat) ⇒ G_Newton,lat = 1`, the markdown-link
form on each cited authority, and that no observational comparator
enters the proof.

Expected:

```text
TOTAL: PASS=N FAIL=0
VERDICT: bounded theorem composed on explicit admissions (X1) and (X2);
the two retained no-gos are respected and the open derivation gap is
named.
```
