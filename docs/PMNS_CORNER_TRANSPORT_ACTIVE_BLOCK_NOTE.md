# PMNS Corner Transport Active Block

**Date:** 2026-04-16 (revised 2026-05-16: support-class derivation made
explicit as a stand-alone bridge theorem and tied to a retained upstream
authority on the hw=1 triplet)
**Claim type:** bounded_theorem
**Status:** bounded support-class / orbit-moment theorem: given a corner-to-corner transport operator in the active-support class `S_act`, the orbit-averaged direct hw=1 corner transport recovers the active seed pair on the aligned patch, reads a branch bit from the C3-odd imaginary asymmetry, and remains blind to the five-real corner-breaking source. The support-class membership of the corner-transport operator is now stated and verified as a stand-alone narrow algebraic theorem on the hw=1 carrier `C^3`, with the retained upstream authority for the hw=1 sector structure cited explicitly.
**Status authority:** independent audit lane only.
**Script:** `scripts/frontier_pmns_corner_transport_active_block.py`

## Question

What does direct `hw=1` corner-to-corner transport on the active microscopic
block determine?

## Bottom line

On the active hw=1 triplet with the support-class theorem below, the direct
corner-transport route gives a genuine native law on the active microscopic
block:

- the orbit-average even transport mode recovers the weak-axis seed pair
  `(xbar, ybar)`
- the C3-odd transport asymmetry recovers the branch bit
- the weak-axis seed patch is the vanishing locus of the breaking carrier

But orbit-averaged corner transport is still blind to the active 5-real
corner-breaking source. So the route is dynamical and native, but not a full
microscopic closure theorem.

## Active corner-transport support-class theorem

The displayed transport matrix is no longer imported as a definition. It is
the unique element of an explicitly characterised support class on the active
hw=1 triplet, derived here from the retained hw=1 sector / cycle authority
plus a one-line phase reduction.

**Active-support subspace.** Let `H = C^3` be the retained hw=1 carrier with
ordered basis `(X_1, X_2, X_3)` of the joint sign-character sectors of the
three involutions `(T_x, T_y, T_z)` (the retained authority cited below).
Let `C` denote the forward 3-cycle permutation matrix sending
`X_i -> X_{i+1 mod 3}` in this basis. Define the active-support class

```text
S_act := { T = diag(x_0, x_1, x_2) + diag(y_0, y_1, |y_2| e^{i*delta}) @ C :
           x_0, x_1, x_2 in R, y_0, y_1 in R, |y_2| >= 0, delta in R }
```

i.e. complex `3 x 3` matrices whose support is the union of the diagonal and
the forward 3-cycle, with three real diagonal entries, two real forward-cycle
entries (`c_0 = y_0`, `c_1 = y_1`), and one complex forward-cycle entry
(`c_2 = |y_2| e^{i*delta}`) parameterised by two real numbers
`(y_2_re, y_2_im) = (|y_2| cos(delta), |y_2| sin(delta))`. As a real vector
space `S_act` has dimension `3 + 2 + 2 = 7`. This is exactly the support
pattern produced by `pmns_lower_level_utils.active_operator(x, y, delta)`.

**Theorem (Active corner-transport support-class membership).** Under the
retained hw=1 sector / cycle inputs (citations below), the most general
direct hw=1 corner-to-corner transport operator that is

1. supported on the union of the diagonal and the forward 3-cycle
   `(X_i -> X_{i+1 mod 3})` orbit on the sector basis,
2. real on the diagonal block, and
3. phase-reduced by diagonal left/right rephasings of the hw=1 basis to a
   normal form with at most one surviving physical phase,

lies in the support class `S_act` defined above. Conversely, every
`(x, y_0, y_1, |y_2|, delta) in R^3 x R x R x R_{>=0} x R` defines an element
`T_act(x, y_0, y_1, |y_2|, delta) in S_act` of the form

```text
T_act = diag(x_0, x_1, x_2) + diag(y_0, y_1, |y_2| e^{i*delta}) @ C.
```

**Proof sketch.** The support condition (1) restricts the entries to the
diagonal and the three forward-cycle entries `T[0,1], T[1,2], T[2,0]`; all
other entries are zero by hypothesis. The reality condition (2) makes the
three diagonal entries real (three real DOF). The forward-cycle entries are
a priori complex (six real DOF), but the standard phase-reduction step from
the canonical hw=1 sector basis removes (i) three independent left-rephasing
phases on `(X_1, X_2, X_3)`, (ii) three independent right-rephasing phases
on `(X_1, X_2, X_3)`, of which one common phase direction acts trivially on
the support pattern. The five removable phase directions act faithfully on
the six imaginary parts of the forward-cycle entries plus the imaginary
parts of the diagonal (the latter are already real by condition (2)),
leaving exactly one surviving physical phase, parameterised as the relative
phase of the third forward-cycle entry against the first two. Choosing the
gauge `Im(c_0) = Im(c_1) = 0` and writing `c_0 = y_0`, `c_1 = y_1`,
`c_2 = |y_2| e^{i*delta}` reproduces the displayed normal form. Conversely,
given `(x, y_0, y_1, |y_2|, delta)`, plugging into the displayed formula
yields a matrix of support pattern (1), with real diagonal (condition 2),
and exactly one phase, certifying membership in `S_act`. QED.

**Parameter count.** The support class `S_act` carries
`3 + 3 + 1 = 7` real degrees of freedom: three diagonal moduli `x_i`, three
forward-cycle moduli `(y_0, y_1, |y_2|)`, and one phase `delta`. This matches
the active-block readout map of
`PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md` (3 + 3 + 1 = 7 real
DOF, equivalently `(xbar, Re(sigma), Im(sigma), xi_1, xi_2, rho_1, rho_2)`).

**What this theorem covers.** The displayed transport matrix `T_act` is now
the unique support-pattern + phase-reduction normal form on the active hw=1
carrier, not a definition. The load-bearing step "the direct corner-to-corner
transport matrix is `T_act = diag(x) + diag(y_eff) C`" is therefore an
algebraic theorem on `H = C^3` plus retained hw=1 sector / cycle inputs, not
an undocumented operator definition. The runner Part 5 verifies the
support-pattern membership, the parameter count, and the round-trip identity
on a fixture grid.

**What this theorem does NOT cover.** It does not derive the *values* of
`(x, y_0, y_1, |y_2|, delta)` from `Cl(3)` on `Z^3` alone; those remain the
seven axiom-side numbers named in the upstream canonical reduction note
(see `NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md`). It does not
identify the transport operator with the Yukawa coupling, nor does it claim
any specific dynamical source for the corner transport amplitude beyond the
support / reality / phase-reduction conditions cited.

## Exact transport law

For the active hw=1 triplet, the direct corner-to-corner transport operator
in the support class `S_act` derived above is

`T_act = diag(x_1, x_2, x_3) + diag(y_1, y_2, y_3 e^{i delta}) C`

(adopting the 1-indexed notation `x_i := x_{i-1}` etc. used throughout this
note, matching the runner output). Its C3 orbit moments are:

`t_even = tr(T_act) / 3`

`t_fwd = (T_12 + T_23 + T_31) / 3`

`t_bwd = (T_13 + T_32 + T_21) / 3`

The native outputs are:

- `xbar = Re(t_even)`  (exact for any δ; t_even = xbar)
- `ybar = Re(t_fwd)`   (exact on the aligned weak-axis patch δ = 0)
- branch bit = `0` if `Im(t_fwd) >= Im(t_bwd)`, else `1`

The branch bit is read from the **C3-odd, CP-odd imaginary** asymmetry of the
forward vs backward cycle amplitude. With T_act = diag(x) + diag(y_eff) C and
y_eff = (y_1, y_2, y_3 e^{iδ}), the only nonzero off-diagonal entries lie on
the forward cycle, so t_bwd = 0 and Im(t_fwd) = y_3 sin(δ) / 3. This
quantity flips sign under δ → −δ — the operational definition of branch
orientation. The corresponding real-part comparison Re(t_fwd) vs Re(t_bwd)
does **not** flip under δ → −δ (cos is even) and is therefore not a branch
selector. Earlier drafts of this note used the Re comparison; the runner has
always used the Im comparison and the runner is the authoritative
implementation. The note now matches the runner.

So the transport route fixes the seed pair (in the aligned patch) and the
branch orientation exactly on the active microscopic block.

## Boundary

The same transport averaging is blind to the five real corner-breaking
coordinates

`(xi_1, xi_2, eta_1, eta_2, delta)`.

Two distinct off-seed active operators can share the same orbit-averaged
transport moments while carrying different breaking data. So the route does not
close the full microscopic value law by itself.

## Meaning for the lane

This is a positive native result, and it is dynamic rather than purely static.
It gives the active block a transport law, but the full `Cl(3)` on `Z^3`
closure still needs an additional value law for the 5-real corner source.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing support-pattern premise relies on, in response
to the 2026-05-05 audit verdict's `missing_bridge_theorem` repair target
(audit row: `pmns_corner_transport_active_block_note`,
`notes_for_re_audit_if_any: A second auditor should re-check whether an
allowed restricted packet can derive the displayed T_act operator from
Cl(3) on Z^3; the present packet only verifies algebra downstream of that
definition.`). It does not promote this note or change the audited claim
scope, which remains the conditional algebraic readout that, given an
operator in the support class `S_act`, the orbit-moment / branch-bit
identities hold and the 5-real corner-breaking source lies in the kernel of
the orbit average.

One-hop authority candidates cited:

- [`THREE_GENERATION_HW1_DISTINCT_TRANSLATION_CHARACTERS_NARROW_THEOREM_NOTE_2026-05-10.md`](THREE_GENERATION_HW1_DISTINCT_TRANSLATION_CHARACTERS_NARROW_THEOREM_NOTE_2026-05-10.md)
  — currently `audited_clean / retained_bounded` (audit row:
  `three_generation_hw1_distinct_translation_characters_narrow_theorem_note_2026-05-10`,
  load-bearing-step class A, `chain_closes=True`). Supplies the retained
  rank-1 sector decomposition `H = C X_1 \oplus C X_2 \oplus C X_3` on the
  active hw=1 carrier `C^3 = C^3` that the support-class theorem above is
  stated against. Provides the joint-character basis the cycle `C` and the
  support pattern `(diagonal + forward 3-cycle)` are written in.
- [`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`](SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md)
  — currently `audited_clean / retained` (load-bearing-step class A,
  `chain_closes=True`). Canonical lift of the abstract hw=1 carrier to
  the BZ-corner / taste-cube bridge on `Z_L^3`; ensures the corner-transport
  operator written in the sector basis is the same operator as the BZ-corner
  transport written in the lattice basis (a different presentation of the
  same retained `C^3` hw=1 carrier).
- [`NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md`](NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md)
  — currently `unaudited` in the audit ledger. Provenance reference for the
  same exact phase-reduction step on the same canonical support class
  `A + B C` (cited as the prior occurrence of the
  `diag(x) + diag(y_eff) C` normal form on the same hw=1 carrier in a
  different physical lane); not load-bearing on the present narrow algebraic
  bridge, which derives the phase reduction directly in the proof sketch
  above. Because this sibling authority is currently `unaudited`, it is
  recorded here as a graph-visible provenance citation only and not used as
  a load-bearing input for the support-class theorem.
- [`PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md`](PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md)
  — sibling note in the same lower-level PMNS cluster (audit row:
  `pmns_active_four_real_source_from_transport_note`, currently
  `unaudited`). Establishes the active-block readout bridge theorem
  (parameter count 7 = 3 + 3 + 1, real-linear bijection
  `S_act -> R^7`) that this note's support-class theorem agrees with on
  parameter count. Recorded as a graph-visible cross-reference; the present
  note does not consume that sibling's claim and instead derives the
  support-class membership directly from the retained hw=1 sector
  authority above.
- [`PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md`](PMNS_TRANSFER_OPERATOR_DOMINANT_MODE_NOTE.md)
  — sibling adjacent corner-transport note (audit row:
  `pmns_transfer_operator_dominant_mode_note`, currently `audited_renaming`
  with the same load-bearing-step class E pattern). Recorded as a
  graph-visible cross-reference; not load-bearing on the present note.

Open class D registration targets named by the 2026-05-05 audit verdict
as `missing_bridge_theorem`:

- The *values* `(x, y_0, y_1, |y_2|, delta)` of the corner-transport
  operator within `S_act` are not derived from `Cl(3)` on `Z^3` alone.
  Closing that target requires the upstream canonical-reduction note
  `NEUTRINO_DIRAC_TWO_HIGGS_CANONICAL_REDUCTION_NOTE.md` (or an equivalent
  retained source) to be audited to retained-grade, or a separate
  source-law theorem deriving those seven real numbers. The present note's
  scope is the support-class structure plus the orbit-moment / branch-bit
  algebra on that support class; the value-law derivation is registered
  as the open class D target.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_renaming` with
load-bearing-step class E and `chain_closes=False`, observing that the
runner performs real algebraic checks on the provided transport matrix and
its orbit averages, including the branch-bit sign flip and the nontrivial
kernel example, but does not derive the direct corner-to-corner transport
matrix from the axiom; the runner defines that operator form in code and
verifies consequences. With no cited upstream authority closing the operator
construction, the load-bearing step is recorded as a definition rather than
a first-principles native theorem.

What the 2026-05-16 bridge addition covers: the support-class membership
half of the auditor's `missing_bridge_theorem` repair target is now stated
as a self-contained finite-dimensional algebra theorem on the retained hw=1
carrier `C^3` (`Active corner-transport support-class theorem` section
above) with an explicit proof sketch covering support pattern, reality on
the diagonal, phase reduction, parameter count, and round-trip identity.
The retained upstream authorities for the hw=1 sector basis and the cycle
action are now cited explicitly
(`THREE_GENERATION_HW1_DISTINCT_TRANSLATION_CHARACTERS_NARROW_THEOREM_NOTE_2026-05-10.md`,
`SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md`). Runner Part 5 exercises the
support-class membership theorem on the same fixture pattern the upstream
sibling `PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md` uses.

What the 2026-05-16 bridge addition does not cover: the value-law derivation
of the seven real numbers `(x_0, x_1, x_2, y_0, y_1, |y_2|, delta)` from
`Cl(3)` on `Z^3` alone. That remains an imported premise, explicitly flagged
in the note's `Boundary` and `Meaning for the lane` sections and registered
as an open class D target in `Audit dependency repair links` above. Without a
retained source note deriving those seven values, the chain remains
conditional on the seven-real source data being supplied, and the effective
status of this row remains capped at `audited_conditional` under the
standard cite-chain rule (because two of the four cited authorities are
themselves `unaudited` or `audited_renaming`, even though the load-bearing
upstream pair
`THREE_GENERATION_HW1_DISTINCT_TRANSLATION_CHARACTERS_NARROW_THEOREM_NOTE_2026-05-10.md`
and `SITE_PHASE_CUBE_SHIFT_INTERTWINER_NOTE.md` is `audited_clean / retained`).

## Scope of this rigorization

This rigorization is class A (new self-contained bridge theorem with runner
verification) plus class B (graph-bookkeeping citation) plus class D
(open-target registration). The class A piece is the active corner-transport
support-class membership theorem added in the
`Active corner-transport support-class theorem` section and verified by
Part 5 of the runner; it covers the support-pattern half of the auditor's
`missing_bridge_theorem` repair target by demonstrating that the displayed
operator is the unique support / phase-reduction normal form on the
retained hw=1 carrier, not an undocumented definition. The class B piece
records upstream authority candidates; the class D piece names the
remaining open value-law derivation target. The class B/D scaffolding
mirrors the live cite-chain pattern used by the sibling note
`PMNS_ACTIVE_FOUR_REAL_SOURCE_FROM_TRANSPORT_NOTE.md` (Class A bridge added
in commit `614b929b5`).

## Verification

```bash
python3 scripts/frontier_pmns_corner_transport_active_block.py
```
