# Planck Primitive Clifford-Majorana Edge Derivation Theorem

**Date:** 2026-04-30
**Status:** audited_renaming audit verdict; chain does not close
**Runner:** `scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py`

```yaml
claim_type_author_hint: bounded_theorem
claim_scope: "Algebraic consistency theorem: GIVEN the rank-four carrier
  K = P_A H_cell as an admitted upstream-conditional input from the cited
  link-local first-variation candidate authority, the explicit Hermitian
  generator set {Gamma_t, Gamma_n, Gamma_tau1, Gamma_tau2} on C^4 realizes
  the irreducible complex Cl_4(C) module, the two-mode CAR algebra
  F(C^2) by oriented Majorana pairing, and the consistency identity
  c_Widom = c_cell = 1/4. The note does NOT derive the substrate-to-P_A
  selection; that step is sourced as conditional provenance to
  PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM (unaudited
  candidate) and remains the named open premise."
admitted_premises:
  - "P_A = Hamming-weight-one projector on H_cell is the active block
    carrier (admitted from upstream conditional authority; not derived
    here; see SUBSTRATE_TO_P_A_FORCING_THEOREM and
    FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO for the symmetry-only
    no-go boundaries)."
  - "Complex Hilbert structure on H_cell (sourced to I3_ZERO_EXACT_THEOREM
    as the retained pairwise-interference/Born surface)."
status_authority: "Independent audit lane only. This note self-classifies
  the load-bearing step as a renaming-class consistency check, not a
  substrate forcing derivation. Two prior independent audits returned
  audited_renaming with load_bearing_step_class F; this self-classification
  aligns the claim type with those prior verdicts. Re-audit at any time
  may revise both the class and the audit verdict."
```

## Cited authorities (one-hop deps)

This note records explicit one-hop authority citations for the renaming-gap
identified by audit: the algebraic `Cl_4(C)` construction here is correct on
`C^4`, but the substrate action does not by itself force the active block to
be `P_A H_cell`. The citations below make the conditional substrate-to-`P_A`
provenance explicit on the live authority chain, while leaving the audit
status of this row at `audited_renaming` (status authority is the independent
audit lane).

- [`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
  — unaudited candidate authority that supplies the conditional
  substrate-to-`P_A` route from the named microscopic action surface. The
  algebraic differential of the link-local staggered-Dirac / Grassmann
  action with respect to its fundamental local link variables has support
  on exactly the Hamming-weight-one packet `P_1`. Hodge-dual `P_3` is
  excluded because Hodge maps a one-link source to a three-link composite,
  which is not an automorphism of the fundamental source domain. That
  theorem supplies the action-native provenance for the rank-four packet
  selection on which the present note's `Cl_4(C)` construction acts.
- [`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md`](PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM_NOTE_2026-04-25.md)
  — companion conditional carrier note that selects `P_A` from the
  first-order coframe boundary variation under the same link-local
  first-variation provenance. Its closure status is `audited_conditional`;
  it is the upstream surface on which the present `Cl_4(C)` carrier acts.
- [`SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md`](SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
  (`retained_no_go`) — exact negative boundary clarifying that
  symmetry-only substrate content does *not* uniquely force `P_A`. This is
  why the link-local first-variation route above is needed: the
  substrate-to-`P_A` step requires action-source structure beyond pure
  symmetries.
- [`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md`](FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md)
  (`retained_no_go`) — exact Hodge-degeneracy negative boundary: pure
  substrate symmetries cannot force first-order over Hodge-dual
  third-order. The link-local first-variation route changes the premise
  surface (it adds the action source domain as additional structure beyond
  pure symmetries), and on that enlarged surface the Hodge ambiguity is
  broken because Hodge duality maps a one-link source to a three-link
  composite.
- `MINIMAL_AXIOMS_2026-05-03.md`
  — current framework memo: physical `Cl(3)` on `Z^3` is the repo-wide
  axiom set, with the staggered-Dirac / Grassmann realization recategorized
  as an open gate rather than a framework axiom. The link-local
  first-variation route is therefore a conditional action-surface route,
  not a new repo-wide axiom and not retained by this note.

The one-hop dependencies above name the conditional substrate-to-`P_A`
provenance and the negative boundaries it must respect. The present note's
`Cl_4(C)` construction is unchanged; what is sharpened is the explicit
provenance of the active-packet selection step that audit flagged as
renaming, recorded as conditional on the cited link-local first-variation
authority rather than left implicit.

## Purpose

The Planck Target 3 Clifford bridge identified one explicit remaining premise:
the active primitive boundary response on the rank-four packet must be the
metric-compatible Clifford coframe response. In
`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`, that
premise is stated as

```text
D(v)^2 = ||v||^2 I_K
```

on `K = P_A H_cell ~= C^4`, and is explicitly marked as "native candidate,
not yet independently forced."

This note records the attempted construction. It uses the retained native
`Cl(3)` / `SU(2)` bivector content, the graph-first structural `SU(3)`
surface, and the anomaly-forced `3+1` time-axis closure to construct an
explicit complex `Cl_4(C)` module on the primitive packet. Audit accepted the
algebraic construction but rejected the claimed derivation of that carrier
from the supplied substrate inputs.

This is not a Hilbert-rank-only argument. The Hilbert-only no-go in
`PLANCK_TARGET3_PHASE_UNIT_EDGE_STATISTICS_BOUNDARY_NOTE_2026-04-25.md`
remains valid if the Clifford substrate content is stripped away.

## Audit Outcome

Fresh-context audit returned `audited_renaming`. The algebraic construction is
correct as an explicit `Cl_4(C)` / two-mode CAR representation, and the runner
still verifies all eight construction checks. The derivation does not close as
a retained substrate theorem because the load-bearing step identifies

```text
rank(P_A H_cell) = 4
```

with the irreducible complex `Cl_4` module by dimension and representation
theory, but does not prove that the retained event-cell substrate action
restricts invariantly and uniquely to that module on `P_A H_cell`.

The missing step is therefore:

```text
retained Cl(3)+time event-cell action
  -> invariant active P_A block
  -> induced Cl_4(C) generators on that block.
```

Until that substrate-to-packet forcing theorem is supplied, the primitive
Clifford-Majorana edge algebra remains a carrier assignment for the Planck
chain, not a derived consequence of the cited upstream content.

The follow-up no-go
[SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md](./SUBSTRATE_TO_P_A_FORCING_THEOREM_NOTE_2026-04-30.md)
tests the missing step directly. It finds that the stated substrate symmetries
do not uniquely force `P_A`: the Hamming-weight-three projector and additional
rank-four local equivariant sums satisfy the same spin/time/CPT/Born/locality
checks. Therefore the repair target requires an additional first-order
boundary/orientation principle, not only the symmetries listed in PR #228.

The next repair attempt is also negative and has now been audited clean:
[FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md](./FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM_NOTE_2026-04-30.md)
checks whether the retained substrate symmetries force the first-order coframe
carrier over its Hodge-dual third-order carrier. They do not. The oriented
Hodge-complement map exchanges `P_1` and `P_3` while preserving the same
spin-lift, time-parity, CPT, complex-Hilbert, and tensor-local number-algebra
structure. Thus a first-order boundary/orientation law remains an additional
input unless it is derived by a stronger theorem not currently in the retained
bank.

## Upstream Authorities

The construction cites these existing framework authorities:

- [MINIMAL_AXIOMS_2026-04-11.md](./MINIMAL_AXIOMS_2026-04-11.md): the accepted
  local `Cl(3)` on `Z^3` plus finite Grassmann / staggered-Dirac partition
  surface.
- [NATIVE_GAUGE_CLOSURE_NOTE.md](./NATIVE_GAUGE_CLOSURE_NOTE.md): native cubic
  `Cl(3)` gives exact `SU(2)` through the spatial Clifford / bivector
  subalgebra.
- [GRAPH_FIRST_SU3_INTEGRATION_NOTE.md](./GRAPH_FIRST_SU3_INTEGRATION_NOTE.md):
  graph-first structural `SU(3)` integration on the selected-axis surface.
- [ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md):
  anomaly cancellation plus chirality and single-clock evolution force one
  temporal dimension, giving the `3+1` coframe.
- [I3_ZERO_EXACT_THEOREM_NOTE.md](./I3_ZERO_EXACT_THEOREM_NOTE.md): exact
  Hilbert-surface `I_3=0` / pairwise-interference anchor. It is cited as the
  quantum-content surface, not as a CAR-statistics derivation.

The theorem does not use `OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md`, does not
use `YT_WARD_IDENTITY_DERIVATION_THEOREM.md`, and does not use any
`alpha_LM = alpha_bare/u_0` decoration chain.

## Theorem Statement (consistency, given the admitted P_A carrier)

This is an algebraic consistency theorem on a stipulated carrier. The
substrate-to-`P_A` selection step is NOT derived in this note; it is
admitted as an upstream-conditional input from the cited link-local
first-variation candidate authority (see header `admitted_premises` and
the "Substrate-to-`P_A` provenance" paragraph in §3 below). The two prior
independent audits returned `audited_renaming` precisely on this step.
What follows is the explicit module realization on the admitted carrier
and its CAR identification — neither more, nor less.

Let

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z ~= C^16
```

be the time-locked primitive event cell, and ADMIT (not derive) the
Hamming-weight-one primitive boundary packet as the active carrier:

```text
K = P_A H_cell,        dim K = rank(P_A) = 4    [ADMITTED carrier].
```

For a selected oriented primitive face, write the primitive coframe as

```text
(t, n, tau_1, tau_2),
```

where `n` is the face normal and `tau_1,tau_2` are tangent axes. On the
retained `Cl(3)/Z^3` framework, with native `SU(2)` supplied by cubic
`Cl(3)` bivectors and the time axis supplied by anomaly-forced `3+1` closure,
the active primitive block carries four Hermitian generators

```text
Gamma_t, Gamma_n, Gamma_tau1, Gamma_tau2 in End(K)
```

obeying

```text
{Gamma_a, Gamma_b} = 2 delta_ab I_K.
```

The generated algebra is

```text
<Gamma_t, Gamma_n, Gamma_tau1, Gamma_tau2> = End(K) ~= M_4(C),
```

so `K` is the irreducible complex `Cl_4(C)` module. The oriented pairings

```text
c_N = (Gamma_t + i Gamma_n) / 2,
c_T = (Gamma_tau1 + i Gamma_tau2) / 2
```

then obey the two-mode CAR relations:

```text
{c_a, c_b} = 0,
{c_a, c_b^dagger} = delta_ab I_K.
```

Therefore

```text
K ~= F(C^2)
```

as the primitive Clifford-Majorana edge carrier.

## Four-Step Derivation Chain

### 1. Retained Bivector Content

The load-bearing spatial input is not a chosen two-qubit factorization. It is
the retained cubic Clifford content:

```text
Cl(3) = span(1, e_i, e_i e_j, e_1 e_2 e_3).
```

The spatial bivectors

```text
B_1 = -i e_2 e_3,
B_2 = -i e_3 e_1,
B_3 = -i e_1 e_2
```

are Hermitian on the complex spinor representation and satisfy

```text
[B_i, B_j] = 2 i epsilon_ijk B_k.
```

Thus `T_i = B_i/2` generate the retained native `su(2)`. This is the same
`Cl(3)` / staggered-taste content recorded in
[NATIVE_GAUGE_CLOSURE_NOTE.md](./NATIVE_GAUGE_CLOSURE_NOTE.md), not a new
edge-statistics postulate.

On the primitive face, the spatial axes are `(n,tau_1,tau_2)`. Their bivectors
are the retained spatial `Cl(3)` even subalgebra restricted to that face.
Duality by the spatial pseudoscalar recovers the spatial coframe generators,
so the bivector data are not external to the coframe response.

### 2. Extension By The Anomaly-Forced Time Axis

[ANOMALY_FORCES_TIME_THEOREM.md](./ANOMALY_FORCES_TIME_THEOREM.md) supplies a
single time axis from anomaly cancellation, chirality, and one-clock
codimension-1 evolution. Add this orthogonal generator to the retained spatial
triple:

```text
Gamma_t^2 = I,
{Gamma_t, Gamma_n} = {Gamma_t, Gamma_tau1} = {Gamma_t, Gamma_tau2} = 0.
```

The complexified primitive coframe algebra is therefore

```text
Cl_4(C) ~= M_4(C).
```

The framework's Wick-rotated lattice calculation surface uses the Euclidean
Clifford anticommutator for the local primitive block. Lorentzian signature is
recovered at the continuum interpretation layer; the local complex Clifford
module class is unchanged after complexification.

### 3. Primitive Packet Restriction

The active primitive boundary packet is the Hamming-weight-one packet in the
four-axis event cell:

```text
rank(P_A) = C(4,1) = 4.
```

The unique irreducible complex `Cl_4` module has dimension `4`. Since
`Cl_4(C) ~= M_4(C)` has complex dimension `16`, a faithful active
representation cannot fit in dimensions `1`, `2`, or `3`, and an `8`-dimensional
faithful representation is a reducible two-copy module with non-scalar
commutant. The rank-four primitive packet is therefore exactly the
irreducible module, with no active spectator sector.

**Substrate-to-`P_A` provenance (conditional, not derived here).** The audit
verdict `audited_renaming` correctly flags that the equality `K = P_A H_cell`
does not by itself follow from rank-matching and the cited spatial / time /
gauge inputs alone — symmetry content does not uniquely select `P_A` from the
17 rank-four equivariant projector classes (see the cited
`SUBSTRATE_TO_P_A_FORCING_THEOREM` no-go), and the Hodge-dual `P_3` survives
all listed constraints (see the cited
`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM`). The present note's
`Cl_4(C)` construction therefore takes `K = P_A H_cell` as an input on this
surface, and its substrate-to-`P_A` provenance is sourced explicitly to the
cited link-local first-variation candidate authority above, which selects
`P_A` from the algebraic first variation of the retained link-local
microscopic action. That route survives the listed no-gos because it adds the
action source domain as additional structure beyond pure symmetries. The
present note does not claim to derive that selection; it cites it as
conditional provenance, with the named open premise being the gravitational
boundary/action density bridge inherited from the upstream
`PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM` §5.

Metric compatibility is now not an added response law. It is the Clifford
anticommutator applied to the constructed primitive coframe:

```text
D(v) = sum_a v_a Gamma_a,
D(v)^2 = ||v||^2 I_K.
```

Polarization gives

```text
D(u)D(v) + D(v)D(u) = 2 <u,v> I_K.
```

This is the premise required by the old Target 3 bridge, constructed from the
retained spatial Clifford content plus the anomaly-forced time axis.

### 4. CAR Fock-Space Identification

Pair the four Majorana generators by the oriented normal/tangent decomposition:

```text
(t,n),        (tau_1,tau_2).
```

Then

```text
c_N = (Gamma_t + i Gamma_n)/2,
c_T = (Gamma_tau1 + i Gamma_tau2)/2
```

satisfy

```text
{c_N,c_N} = {c_T,c_T} = {c_N,c_T} = 0,
{c_N,c_N^dagger} = {c_T,c_T^dagger} = I,
{c_N,c_T^dagger} = 0.
```

Thus the rank-four packet is

```text
K ~= F(C^2).
```

A reversal of the tangent orientation conjugates the tangent pairing
`c_T <-> c_T^dagger` or applies an equivalent Bogoliubov/unitary
transformation. It does not change the CAR algebra or the primitive Fock-space
carrier.

## Explicit Matrix Construction

The runner uses the following Hermitian generators:

```text
Gamma_t    = sigma_x otimes I,
Gamma_n    = sigma_y otimes I,
Gamma_tau1 = sigma_z otimes sigma_x,
Gamma_tau2 = sigma_z otimes sigma_y.
```

They obey the `Cl_4` anticommutator exactly at machine precision and their
Clifford words span all `16` complex matrix units of `M_4(C)`.

The retained spatial `Cl(3)` subblock is

```text
Gamma_n, Gamma_tau1, Gamma_tau2.
```

Its Hermitian bivectors

```text
-i Gamma_tau1 Gamma_tau2,
-i Gamma_tau2 Gamma_n,
-i Gamma_n Gamma_tau1
```

close `su(2)`, matching the native cubic bivector content. Adding `Gamma_t`
doubles the spatial `Cl_3(C)` span from dimension `8` to dimension `16`,
which is the primitive `Cl_4(C)` lift.

## Uniqueness

Complex `Cl_4` is the simple algebra `M_4(C)`. Therefore every irreducible
complex representation is the defining four-dimensional module, and every
automorphism is inner up to the standard matrix-algebra automorphism class.
Changing the ordered primitive coframe by a signed orthogonal transformation,
or changing the gamma-matrix basis by a unitary conjugation, gives an
equivalent `Cl_4(C)` module.

The runner verifies this representation-theoretically:

- the rank-four module has scalar commutant only;
- the direct two-copy module has commutant `M_2(C)` and is reducible;
- among faithful dimensions `<= 8`, only dimension `4` has scalar commutant;
- signed/permuted generator sets preserve the same full `M_4(C)` algebra.

Thus the lift is unique up to standard `Cl_4(C)` automorphism on the primitive
rank-four packet.

## Connection To The Existing Conditional Chain

This theorem closes the active-block algebraic premise of
`PLANCK_TARGET3_CLIFFORD_PHASE_BRIDGE_THEOREM_NOTE_2026-04-25.md`:

```text
metric-compatible Clifford response D(v)^2 = ||v||^2 I
on P_A H_cell.
```

It also closes the residual statement isolated by
`AREA_LAW_NATIVE_CAR_SEMANTICS_TIGHTENING_NOTE_2026-04-25.md`:

```text
the active primitive boundary response is generated by a local irreducible
Clifford-Majorana edge algebra.
```

once the active block is taken to be `P_A H_cell`. The remaining
substrate-to-`P_A` step is sourced to the cited link-local first-variation
candidate authority above; this note does not promote that step.

Therefore the former conditional chain becomes, on the cited live authority
chain and pending independent audit ratification of the link-local
first-variation theorem:

```text
retained Cl(3) spatial bivectors                    [native_gauge_closure]
  + graph-first SU(3) / anomaly-complete gauge surface  [graph_first_su3]
  + anomaly-forced time axis                        [anomaly_forces_time]
  + complex Hilbert / Born-rule packet              [i3_zero_exact_theorem]
  + retained link-local first-variation P_A forcing
        [PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM, unaudited candidate]
  -> active block = P_A H_cell, rank 4              [substrate-to-P_A step]
  -> irreducible Cl_4(C) module on K                [present note]
  -> F(C^2) two-mode CAR edge                       [present note]
  -> c_Widom = c_cell = 1/4                         [cross-validation]
  -> G_Newton,lat = 1 in natural lattice units      [SOURCE_UNIT_NORMALIZATION]
  -> a/l_P = 1                                      [BOUNDARY_DENSITY_EXTENSION]
        conditional on (BP) gravitational boundary/action density bridge.
```

The last arrow still uses the already separate source-unit normalization
support theorem. The SI physical-units conversion remains metrology. The
named open bridge premise (BP) — that the framework's first-order coframe
boundary carrier `P_A` is the microscopic gravitational boundary/action
density carrier — is unchanged by this note and remains the residual Planck
target inherited from `PLANCK_PRIMITIVE_COFRAME_BOUNDARY_CARRIER_THEOREM` §5.

## Cross-Validation

The CAR carrier has one normal mode and one tangent mode:

```text
normal crossings = 2,
tangent crossings = 2 * (1/2) = 1,
<N_x> = 3.
```

The Widom-Gioev-Klich coefficient is

```text
c_Widom = <N_x>/12 = 3/12 = 1/4.
```

The primitive packet trace is

```text
c_cell = Tr((I_16/16)P_A) = 4/16 = 1/4.
```

So

```text
c_Widom = c_cell = 1/4.
```

This is a consistency check with
`AREA_LAW_PRIMITIVE_CAR_EDGE_IDENTIFICATION_THEOREM_NOTE_2026-04-25.md` and
the existing primitive coefficient theorem. It is not a new fitted coefficient.

## Non-Claims

This theorem does not claim:

- a derivation of the SI decimal value of `hbar`;
- a physical-units derivation of Newton's constant `G`;
- strong-field continuum gravity, black-hole interiors, or a full quantum
  gravity completion;
- a Hilbert-only derivation of CAR statistics;
- any new structural identity between `c_cell`, `G_Newton`, `hbar`, and
  `l_P` beyond the already recorded source-unit and natural-unit chain.

The theorem fixes the primitive Clifford-Majorana edge-statistics carrier on
the retained substrate. `G_Newton,lat=1` and `a/l_P=1` are natural-lattice-unit
consequences only after the source-unit support theorem is applied.

## Audit Robustness Checks

### Metric Signature

The construction is explicitly the Euclidean local lattice construction
`Cl(4,0)_C ~= Cl_4(C) ~= M_4(C)`. The Hermitian generators in the runner obey

```text
Gamma_a^2 = I,        {Gamma_a,Gamma_b} = 2 delta_ab I.
```

This is the Wick-rotated primitive-block algebra used by the lattice
calculation surface. A Lorentzian reading would replace the real quadratic
form by signature `(1,3)` before complexification, but

```text
Cl(1,3)_C ~= Cl(4,0)_C ~= M_4(C).
```

So the complex primitive module and the CAR pairing are not sensitive to a
separate signature choice. The theorem does not use Lorentzian signature as an
additional premise.

### Face Orientation

The oriented face choice only chooses a basis of the already constructed
orthonormal four-axis coframe. If

```text
Gamma'_a = R_a^b Gamma_b
```

for an orthogonal relabeling of `(t,n,tau_1,tau_2)` induced by a substrate
face rotation or tangent-orientation reversal, then the Clifford
anticommutator is preserved:

```text
{Gamma'_a,Gamma'_b} = 2 delta_ab I.
```

By the uniqueness of the irreducible complex `Cl_4` module, this relabeling is
implemented on `K` by a unitary Clifford automorphism, up to the usual central
phase. The induced change on `(c_N,c_T)` is therefore a CAR-preserving
Bogoliubov/unitary transformation. In particular, reversing
`tau_1,tau_2` conjugates the tangent mode or swaps an equivalent oriented
pairing; it does not add a new edge-statistics carrier.

### Complex Structure

The complex scalar `i` used in

```text
c_N = (Gamma_t + i Gamma_n)/2,
c_T = (Gamma_tau1 + i Gamma_tau2)/2
```

is not introduced as an extra Clifford-Majorana premise. The theorem is stated
on the retained quantum packet

```text
H_cell ~= C^2_t otimes C^2_x otimes C^2_y otimes C^2_z,
K = P_A H_cell ~= C^4,
```

whose complex Hilbert structure is the same pairwise-interference/Born-rule
surface recorded by `I_3=0`. The real Clifford generators act by Hermitian
endomorphisms of this already complex module, and the CAR modes use the
module's retained complex structure to combine Majorana pairs. If an auditor
does not accept the complex Hilbert packet as retained input, the correct
verdict is `audited_conditional`; the construction does not hide that issue in
the CAR pairing step.

## Audit Verdict and Self-Narrowing

This note originally self-declared `proposed_retained` and requested an
independent audit of the load-bearing step. Two independent audits
returned `audited_renaming` with `load_bearing_step_class = F`. In light
of that, the note now self-classifies its claim type as a bounded
algebraic consistency theorem on the admitted P_A carrier (see header
`claim_type_author_hint: bounded_theorem` and the renamed Theorem
Statement section). This self-narrowing does not promote audit status;
the status authority remains the independent audit lane, and re-audit
may revise both the class and the verdict.

The original audit-loop question was:

> Are the retained native `Cl(3)` / `SU(2)` bivectors, graph-first `SU(3)`
> gauge surface, anomaly-forced single time axis, and rank-four
> Hamming-weight-one primitive packet sufficient to derive the local
> irreducible Clifford-Majorana edge algebra on `P_A H_cell` without adding a
> new structural premise?

The audit judged that restriction to be an additional carrier assignment. Its
verdict is `audited_renaming`: the construction names the rank-four primitive
packet as the irreducible `Cl_4(C)` module, but the supplied inputs do not force
the substrate action to preserve `P_A` and induce the displayed generators.
Consequently, the Planck-pin conditional chain is not promoted by this note.
The substrate-to-`P_A` and first-order-coframe follow-up no-gos localize the
remaining scientific gap: an audit-clean positive route must derive a
first-order boundary/orientation law, or bypass the full-cell carrier
selection by an intrinsic active-block theorem that does not use `P_A` as an
input.

**Conditional repair route, cited (not promoted here).** The cited
`PLANCK_LINK_LOCAL_FIRST_VARIATION_P_A_FORCING_THEOREM` (one-hop deps above)
supplies a candidate substrate-to-`P_A` route by deriving `P_A = P_1` from the
algebraic first variation of the retained link-local microscopic action (see
that note's Theorem and §3 for why this route survives the
`SUBSTRATE_TO_P_A_FORCING_THEOREM` and
`FIRST_ORDER_COFRAME_UNCONDITIONALITY_NO_GO_THEOREM` no-gos). That theorem is
currently unaudited. If it audits clean, the present note's substrate-to-`P_A`
provenance inherits stronger derivational footing through the cited live
authority chain. If it fails audit, the present note retains its
`audited_renaming` status with the explicit conditional provenance of the
`P_A` selection step recorded above. Either way, this rigorization does not
re-open the audit verdict; the status authority remains the independent audit
lane.

## Verification

Run:

```bash
python3 scripts/frontier_planck_primitive_clifford_majorana_edge_derivation.py
```

The runner checks eight blocks:

1. four Hermitian `Cl_4` generators on `C^4`;
2. faithful `M_4(C)` generation and irreducibility;
3. retained spatial `Cl(3)` bivectors closing the native `SU(2)` subset;
4. anomaly-forced time-axis extension from `Cl_3` to `Cl_4`;
5. oriented Majorana-pair construction of the two CAR modes;
6. `dim F(C^2)=4=rank(P_A)`;
7. uniqueness up to standard `Cl_4(C)` automorphism by commutant class;
8. `c_Widom=1/4=c_cell` cross-validation.

Current output:

```text
Summary: PASS=8  FAIL=0
```
