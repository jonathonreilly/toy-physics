# PMNS Active Four-Real Source From Transport

**Status:** open - open or unresolved claim state
## Question
Once the active transport / response profile is derived at lower level, does the
remaining four-real active orbit-breaking source still need a separate theorem
object?

## Exact Result
No.

The non-averaged lower-level active transport / response profile determines the
active block exactly. From that active block:

- `xbar` is read from the `C3`-even diagonal mean
- `sigma` is read from the forward-cycle complex mean
- the residual active source is exactly the four-real vector

`(xi_1, xi_2, rho_1, rho_2)`

with:

- `xi_3 = -xi_1 - xi_2`
- `rho_3 = -rho_1 - rho_2`

So the active block rebuilds exactly from:

- `xbar`
- `sigma`
- `(xi_1, xi_2, rho_1, rho_2)`

Therefore the four-real source is no longer an extra unresolved object on the
lower-level active transport chain. It is just the centered non-averaged part
of the active transport profile.

## Boundary
This does not yet derive the lower-level active transport / response profile
itself from `Cl(3)` on `Z^3` alone. It only closes the residual four-real source
once that lower-level active profile is genuinely available.

## Active-block readout bridge theorem

The phrase "the residual active source is exactly the centered four-real
vector" is, as a self-contained statement, a finite-dimensional
real-linear-algebra theorem about the active-support subspace. This
section records that theorem and the runner Part 4 checks that verify
it. The theorem does not derive the lower-level active transport
profile itself; that remains the open class D registration target named
in the `Boundary` section above.

**Active-support subspace.** Let `S_act` denote the real vector
subspace of `M_3(C)` consisting of matrices `B` of the form

```text
B = diag(x_0, x_1, x_2)  +  diag(y_0, y_1, |y_2| e^{i*delta}) @ CYCLE
```

with `x_0, x_1, x_2 in R`, `y_0, y_1 in R`, `|y_2| >= 0`, `delta in R`,
where `CYCLE` is the forward 3-cycle permutation matrix. This is
exactly the support pattern produced by the lower-level active
transport operator `active_operator(x, y, delta)` in
`scripts/pmns_lower_level_utils.py`. As a real vector space `S_act`
has dimension `3 + 3 + 1 = 7` (three real diagonal entries, two real
cycle entries `c_0 = y_0` and `c_1 = y_1`, and one complex wrap-around
entry `c_2 = |y_2| e^{i*delta}` parameterised by two real numbers
`y_2_re = |y_2| cos(delta)` and `y_2_im = |y_2| sin(delta)`).

**Readout map.** Define the forward readout map `R: S_act -> R^7` by

```text
xbar    := (x_0 + x_1 + x_2) / 3
sigma   := (c_0 + c_1 + c_2) / 3       (complex; one real DOF for Re, one for Im)
xi_1    := x_0 - xbar
xi_2    := x_1 - xbar
rho_1   := Re(c_0) - Re(sigma)
rho_2   := Re(c_1) - Re(sigma)
```

with the inverse map `R^{-1}: R^7 -> S_act` given by

```text
xi_3       := -xi_1 - xi_2
rho_3      := -rho_1 - rho_2
x_i        := xbar + xi_i,             i = 0, 1, 2
Re(c_i)    := Re(sigma) + rho_i,       i = 0, 1
Re(c_2)    := Re(sigma) + rho_3
Im(c_0)    := 0
Im(c_1)    := 0
Im(c_2)    := 3 Im(sigma)
```

**Theorem (Active-block readout bijectivity).** The forward map `R`
is a real-linear bijection between `S_act` and `R^7`, the
imaginary-part signature `(Im(c_0), Im(c_1), Im(c_2)) = (0, 0, 3 Im(sigma))`
is invariant on `S_act`, and the inverse `R^{-1}` reproduces every
element of `S_act` exactly.

**Proof sketch.** (i) `R` is real-linear by construction (it is a fixed
real-affine combination of the entries of `B`, with no constants).
(ii) The centered residuals `(xi_1, xi_2, xi_3)` and `(rho_1, rho_2,
rho_3)` each sum to 0 by definition, so each set of three components is
parameterised by two free real numbers, recovering the 7-real-DOF
coordinate space `(xbar, Re(sigma), Im(sigma), xi_1, xi_2, rho_1,
rho_2)`. (iii) The imaginary-part signature
`(0, 0, |y_2| sin(delta))` holds on `S_act` by the explicit support
pattern, and `Im(sigma) = |y_2| sin(delta) / 3`, hence
`Im(c_2) = 3 Im(sigma)`. (iv) `R^{-1}` is the explicit reconstruction
that inverts each defining equation. The composition `R^{-1} circ R`
is the identity on `S_act` by direct substitution. Real-linear
bijection of two 7-dimensional real vector spaces follows from a
domain–codomain dimension match plus injectivity (no nonzero `B in
S_act` maps to the zero coordinate vector, since each of the seven
defining equations would force the corresponding entry to vanish).

**What this theorem covers.** The "precise active-block readout map"
half of the 2026-05-05 auditor repair target. The remaining half — a
retained-grade derivation of the lower-level active transport /
response profile itself from `Cl(3)` on `Z^3` — is not in scope for
this theorem and is registered as an open class D target in the
`Audit dependency repair links` section below.

**Runner verification.** All ten parts of the theorem (support
pattern, real-diagonal, single-phase entry, centered-residual sums,
imaginary-part signature, DOF count, forward injectivity, round-trip
identity, real-linearity) are exercised by Part 4 of the runner on a
64-sample fixture grid drawn from a fixed RNG seed (PASS = 10 / 10 on
the present worktree).

## Runner

```bash
PYTHONPATH=scripts python3 scripts/frontier_pmns_active_four_real_source_from_transport.py
```

Last run (2026-05-16): `PASS=17 FAIL=0` on the present worktree. The
runner exercises four parts: (Part 1) non-averaged transport recovers
the active block exactly via `derive_active_block_from_response_columns`
then re-derives the four-real source `(xi_1, xi_2, rho_1, rho_2)`;
(Part 2) two active blocks with identical native means but distinct
four-real sources are separated by the non-averaged readout; (Part 3) a
circularity guard verifies the lower-level active derivation function
takes no PMNS-side target values as inputs (the function signature is
checked against the banned-input set
`{d0_trip, dm_trip, delta_d_act, diag_a_pq, m_r}`); (Part 4) the
active-block readout bridge theorem is verified on a 64-sample fixture
grid through ten algebraic checks (T1–T10) — support pattern, real
diagonal, single-phase entry, centered residual sums, imaginary-part
signature, DOF dimension count, pairwise injectivity, round-trip
identity, and real-linearity.

## Audit dependency repair links

This graph-bookkeeping section records the explicit upstream authority
candidates the load-bearing transport-profile premise relies on, in
response to the 2026-05-05 audit verdict's `missing_bridge_theorem`
repair target (audit row:
`pmns_active_four_real_source_from_transport_note`). It does not
promote this note or change the audited claim scope, which remains the
conditional algebraic readout that, given a genuinely available
non-averaged lower-level active transport / response profile, the
residual four-real active source is determined by the active block
decomposition.

One-hop authority candidates cited:

- [`PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md`](PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md)
  — currently `audited_conditional` (audit row:
  `pmns_lower_level_end_to_end_closure_note`). Sibling note in the
  same lower-level PMNS cluster whose runner
  (`frontier_pmns_lower_level_end_to_end_closure.py`) supplies the
  active/passive response columns and the corresponding
  `derive_active_block_from_response_columns` reconstruction map.
  Both rows share the `pmns_lower_level_utils.py` helper module and
  the same fixed-input `BANNED_INPUT_NAMES` circularity guard. Because
  this sibling authority is itself `audited_conditional`, the present
  note's effective status is capped at `audited_conditional` under the
  standard cite-chain rule.
- [`PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md`](PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md)
  — currently `audited_renaming` (audit row:
  `pmns_corner_transport_active_block_note`). Adjacent PMNS active-block
  transport candidate authority in the same lower-level cluster. Because
  this candidate is `audited_renaming` rather than retained, it does not
  by itself promote the upstream premise to retained-grade.

Open class D registration targets named by the 2026-05-05 audit verdict
as `missing_bridge_theorem`:

- The non-averaged lower-level active transport / response profile is
  imported as a premise. Closing it requires a retained source note or
  authority deriving that active transport profile from `Cl(3)` on `Z^3`
  alone (the note's "Boundary" section explicitly flags this as the
  remaining sole-axiom gap). The 2026-05-05 audit verdict's
  `notes_for_re_audit_if_any` field names this as
  `missing_bridge_theorem: provide the theorem or retained authority
  deriving the lower-level active transport/response profile and the
  precise active-block readout map`.

## Honest auditor read

The 2026-05-05 audit recorded this row as `audited_conditional` with
load-bearing-step class A and `chain_closes=False`, observing that the
algebraic readout is plausible as a conditional decomposition but the
restricted packet provides no derivation or retained authority for the
lower-level active transport / response profile itself. The audit
ledger records `runner_path: None` for this row because the audit was
performed on the text-only restricted packet. The runner
`scripts/frontier_pmns_active_four_real_source_from_transport.py` now
verifies seventeen checks (PASS=17 FAIL=0 on 2026-05-16): the original
seven checks from Parts 1–3 (conditional readout, source separation,
circularity guard), plus the ten new checks added in Part 4 that
exercise the active-block readout bridge theorem (T1–T10) on a
64-sample fixture grid.

What the 2026-05-16 bridge addition covers: the "precise active-block
readout map" half of the auditor's `missing_bridge_theorem` repair
target is now stated as a self-contained finite-dimensional real-linear
algebra theorem with an explicit proof sketch in the
`Active-block readout bridge theorem` section and a corresponding
ten-check runner Part 4. This is class A algebra on the active-support
subspace `S_act`; it does not consume any PMNS target value or
lower-level transport-profile derivation as input.

What the 2026-05-16 bridge addition does not cover: the "lower-level
active transport / response profile" half of the auditor's repair
target. That remains an imported premise, explicitly flagged in the
note's `Boundary` section and registered as an open class D target in
`Audit dependency repair links` below. Without a retained source note
deriving the active transport / response profile from `Cl(3)` on `Z^3`
alone, the chain remains conditional and the effective status of this
row remains capped at `audited_conditional` under the standard
cite-chain rule (the closest cited candidate
`PMNS_LOWER_LEVEL_END_TO_END_CLOSURE_NOTE.md` is itself
`audited_conditional`, and the second candidate
`PMNS_CORNER_TRANSPORT_ACTIVE_BLOCK_NOTE.md` is `audited_renaming`,
neither retained-grade).

## Scope of this rigorization

This rigorization is class A (new self-contained bridge theorem with
runner verification) plus class B (graph-bookkeeping citation) plus
class D (open-target registration). The class A piece is the
active-block readout bijectivity theorem added in the
`Active-block readout bridge theorem` section and verified by Part 4
of the runner; it covers the algebraic half of the auditor's
`missing_bridge_theorem` repair target. The class B piece records
upstream authority candidates; the class D piece names the remaining
open transport-profile derivation target. The class B/D scaffolding
mirrors the live cite-chain pattern used by the
`DM_NEUTRINO_BOSONIC_NORMALIZATION_THEOREM_NOTE_2026-04-15.md` cluster
(commit `8e84f0c23`).
