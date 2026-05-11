# Spectral-Gap Cosmological-Constant Identity Theorem

**Date:** 2026-04-18 (audit-prep cite-chain rigorize 2026-05-10)
**Status:** structural identity theorem; current ledger `effective_status:
audited_conditional` (see "Audit-driven dependency-edge rigorization (2026-05-10)"
below). Separates the exact identity `Lambda = lambda_1(S^3_R)` from the
still-bounded numerical value of `R` / `Lambda`.
**Script:** `scripts/frontier_cosmological_constant_spectral_gap_identity.py`
**Claim type:** positive_theorem
**Claim scope:** the exact function identity `Lambda_vac = lambda_1(S^3_R) =
3 / R^2` for every `R > 0`, on the de Sitter stationary vacuum sector of the
direct-universal GR closure with retained `S^3` spatial topology, conditional
on the upstream-authority statuses recorded below; the numerical values of
`R` / `R_Lambda` / `Lambda` remain in the existing bounded cosmology rows.
**Upstream authorities (current ledger statuses, not assertions of
retainedness):**
[`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md)
(unaudited),
[`UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md`](UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md)
(unaudited),
[`UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`](UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md)
(unaudited),
[`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md)
(unaudited),
[`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)
(audited_conditional).

## Audit-driven dependency-edge rigorization (2026-05-10)

The 2026-04-30 leaf-resweep audit verdict on this row was `audited_conditional`
(load-bearing 19.996, direct-in-degree 23) with rationale: "The local step
cannot be promoted because direct upstream authorities remain unaudited,
support/open/unknown, or terminal non-clean." The named repair target was:
"dependency_not_retained: ratify or repair the listed upstream theorem/bridge
rows and rerun the local runner so it computes the disputed bridge rather
than only checking consequences."

The earlier framing of this note — "**proposed_retained structural identity
theorem** on `main`" with "Upstream authorities (all already retained on
`main`)" — predates the audit lane's later classification of those upstream
rows as `unaudited` or `audited_conditional`. This rigorize pass corrects the
header to track the live ledger so the audit graph routes to the correct
upstream statuses. It does not derive any of the upstream objects within this
packet, does not promote any sibling claim, and does not change this row's
`audited_conditional` status. Audit verdict and effective status are set by
the independent audit lane only; nothing in this rigorization edit promotes
status.

**Cited authorities and current ledger statuses (one-hop deps):**

| Cited authority | Role in this note | Current ledger status |
|---|---|---|
| [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md) | direct-universal discrete `3+1` GR closure on `PL S^3 x R` (theorem condition 1) | unaudited |
| [`UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md`](UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md) | smooth global weak gravitational stationary/Gaussian solution class (theorem condition 2) | unaudited |
| [`UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`](UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md) | canonical textbook Einstein-Hilbert action family with cosmological-constant sector (theorem condition 3, used in Leg A) | unaudited |
| [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md) | round `S^3` of radius `R` for any `R > 0` (theorem condition 4 part i) | unaudited |
| [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md) | `S^3` cap uniqueness (theorem condition 4 part ii) | audited_conditional |
| [`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md) | "exact on the retained internal surface" point 2 — Leg B Obata equality reference | unaudited |
| [`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) | "Fixed-gap vacuum scale" section — Leg A Einstein-side reference | audited_conditional |
| [`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md) | downstream EOS corollary that consumes this identity | unaudited |

**What the cite-chain does NOT close.** Five of the eight cited authorities
remain `unaudited`; two remain `audited_conditional`; none currently carry a
retained-grade ledger status. The `dependency_not_retained` repair target is
therefore not satisfied by this rigorize pass; the chain remains conditional
on those parent audits being upgraded. The runner's PASS=22/0 verifies the
two-leg algebraic identity (Leg A: vacuum Einstein trace contraction in
`D = 4` plus de Sitter throat Ricci giving `Lambda = 3/R^2` for `R` in
`{0.5, 1.0, 2.0, pi, 1e6, 1e26}`; Leg B: Lichnerowicz–Obata equality on
round `S^3` giving `lambda_1 = 3/R^2` for the same `R` sweep; closure:
both legs match to `0.0` residual at every `R`, with log-log slope `-2`
and intercept `log 3`); this is the bounded scope on which the row
stands.

**What this rigorize pass NEVER claims.** It does not derive the GR closure,
the smooth gravitational global solution class, the canonical textbook
continuum GR closure, or the round-`S^3` topology / cap-uniqueness from
the accepted axiom within this packet. It does not promote
`cosmological_constant_spectral_gap_identity_theorem_note` to retained or
remove the conditional perimeter on the upstream authorities listed above.

## Audit-aware repair path

Per `audit_ledger.json`, `notes_for_re_audit_if_any` for
`cosmological_constant_spectral_gap_identity_theorem_note`: the cheapest
path to a stronger audit verdict is to ratify or repair the eight
upstream theorem/bridge rows listed above and rerun the local runner so
it computes the disputed bridge rather than only checking consequences.
Either path makes the structural identity self-contained from retained-grade
upstream surfaces; the current note is conditional on those upstream rows
being upgraded.

## Role

The purpose of this note is to split the existing spectral-gap
cosmological-constant companion into two strictly separated pieces:

1. an **exact structural identity** `Lambda_vac = lambda_1(S^3_R) = 3 / R^2`
   on the retained direct-universal GR de Sitter stationary vacuum sector,
   valid for any `R`, and
2. the **numerical value** of `R` / `Lambda`, which remains the
   cosmology-scale identification blocker and stays bounded.

The identity is already called "exact on the retained internal surface" in
[`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md)
(section "Exact on the retained internal surface", point 2), and the GR-side
derivation is already written out in
[`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md)
(section "Fixed-gap vacuum scale"). This note does not add new science —
it crystallizes that already-internally-exact statement into a standalone
retained theorem surface so downstream corollaries (including
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md))
can anchor on a retained premise rather than on a companion-lane label.

## Theorem

Let the retained surface carry:

1. the retained direct-universal discrete 3+1 GR closure on `PL S^3 x R`
   with an exact global Einstein/Regge stationary action family (authority:
   [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md));
2. the retained smooth global weak gravitational stationary/Gaussian
   solution class on the chosen smooth realization of `PL S^3 x R`
   (authority:
   [`UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md`](UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md));
3. the retained canonical textbook Einstein-Hilbert-style weak/stationary
   action family on the chosen realization, carrying a well-defined
   cosmological-constant sector (authority:
   [`UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`](UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md));
4. retained `S^3` spatial topology on `PL S^3 x R` with round spatial metric
   of radius `R`, for any `R > 0` (authority:
   [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md),
   [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)).

**Theorem (spectral-gap cosmological-constant identity).** On the
stationary de Sitter vacuum sector of conditions (1)–(3), with spatial
topology from condition (4), the cosmological-constant scale `Lambda_vac`
and the first nonzero scalar-Laplacian eigenvalue `lambda_1(S^3_R)` are
equal as a structural identity:

  `Lambda_vac = lambda_1(S^3_R) = 3 / R^2`,

for every `R > 0`. The identity is an exact function identity in `R`; it
does **not** fix a numerical value of either `R` or `Lambda_vac`.

**Proof.** The proof has two independent legs that meet at `3 / R^2`.

*Leg A (Einstein side, vacuum equations).* On the canonical textbook
Einstein-Hilbert-style continuum GR closure (condition 3), the action on
`PL S^3 x R` is

  `S = (1 / (16 pi G)) integral (R_4d - 2 Lambda) sqrt(-g) d^4 x`,

where `R_4d` is the 4D Ricci scalar and `Lambda` is the cosmological-constant
parameter of the action. The vacuum Einstein equations from this action are

  `R_{mu nu} - (1/2) g_{mu nu} R_4d + Lambda g_{mu nu} = 0`.

Trace-contraction with `g^{mu nu}` in `D = 4` gives

  `R_4d - 2 R_4d + 4 Lambda = 0  ==>  R_4d = 4 Lambda`,

and substituting back:

  `R_{mu nu} = Lambda g_{mu nu}`.

The stationary de Sitter vacuum solution with compact spatial S^3 slicing
of constant spatial radius `R` has, on the `S^3` throat,
`R_{mu nu} = (3 / R^2) g_{mu nu}` in 4D (the standard de Sitter Ricci for
spatial S^3 of radius `R`). Therefore

  `Lambda_vac = 3 / R^2`.

This is the content of the "Fixed-gap vacuum scale" section of
[`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md).

*Leg B (spectral side, Lichnerowicz–Obata).* On the round S^3 of radius `R`
(condition 4), the scalar Laplacian has exact spectrum `lambda_n =
n (n + 2) / R^2`, with first nonzero eigenvalue

  `lambda_1(S^3_R) = 3 / R^2`.

This is the Obata equality for spheres (Lichnerowicz–Obata 1962/1968):
for an n-dimensional round sphere of radius `R`, `lambda_1 = n / R^2`, and
for `n = 3` this gives `3 / R^2`. This is the content of the
"exact on the retained internal surface" point 2 of
[`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md).

*Closing.* Legs A and B give the same function `3 / R^2` of the same
retained radius `R`, so as an identity on the retained de Sitter stationary
vacuum sector,

  `Lambda_vac = lambda_1(S^3_R)`.

This holds for every `R > 0`; the identity is retained even when the
numerical value of `R` is not. □

## What Is Retained Exactly by This Theorem

- the coefficient `3` on both sides (Einstein: `R_{mu nu} = (3/R^2) g_{mu nu}`;
  Laplacian: Obata equality on S^3);
- the `1 / R^2` scaling on both sides;
- the **function identity** `Lambda_vac = lambda_1(S^3_R)` as a statement
  that holds for every `R > 0`, with no free parameter on the right-hand
  side that is not also on the left-hand side;
- the specialization of this identity to the retained de Sitter stationary
  vacuum sector of the direct-universal GR + smooth GR closure.

## What Is **Not** Retained by This Theorem

- the numerical value of `R` / `R_Lambda`: the cosmology-scale identification
  remains the honest remaining gap, as recorded in
  [`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md),
  "Honest Remaining Gap";
- the numerical value of `Lambda`: remains the bounded companion
  result of
  [`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md);
- the present-day `Omega_Lambda` value: remains gated on the matter-content
  bridge, unchanged;
- the full FRW / expansion-history derivation: still conditional.

This theorem is deliberately narrower than the full cosmology-companion
portfolio. Its point is to isolate the single exact structural claim — the
`R`-free identity between `Lambda_vac` and `lambda_1(S^3_R)` — so that
downstream corollaries that depend only on the identity (not on its
numerical evaluation) can anchor on a retained surface.

## Relation to Existing Matrix Rows

The existing `Cosmological constant Lambda` row in
`PUBLICATION_MATRIX.md` carries
the status `bounded` because its claim is about the
**numerical value** of `Lambda` against the observed `~ 1.09 x 10^-52 m^-2`.
This theorem does **not** change that row: the numerical comparison remains
conditional on the cosmology-scale identification.

What this theorem adds is an **adjacent retained row** for the structural
identity itself, analogous to how
[`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md)
carries an exact `T = 0` confinement theorem independently of the bounded
`sqrt(sigma)` numerical scale.

## Publication Matrix Row

This note is now wired into
`PUBLICATION_MATRIX.md` as the
retained structural identity row in the cosmology block:

| Quantity / lane | Workstream | Framework result | Observation / comparator | Claim-strength status | Import class | Current publication decision | Authority / best source | Frozen-out ref |
|---|---|---|---|---|---|---|---|---|
| Spectral-gap cosmological-constant identity | retained GR + spectral-gap cosmology | `Lambda_vac = lambda_1(S^3_R) = 3 / R^2` as an exact function identity in `R` on the retained de Sitter stationary vacuum + round `S^3` spatial topology | n/a (identity, not a numerical comparison) | retained | retained direct-universal GR closure + retained smooth global gravitational stationary/Gaussian class + retained canonical textbook continuum GR closure + retained `S^3` topology + Lichnerowicz–Obata equality for spheres | retained structural identity may appear on the flagship / SI / theorem box; numerical `R_Lambda` / `Lambda` values stay in the existing bounded companion rows | this note + [COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md](../../COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md) + [COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md](../../COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md) | n/a |

The adjacent numerical `Cosmological constant Lambda` row, the
`\Omega_\Lambda` chain, the `spectral tilt n_s` row, the numerical graviton
compactness-mass companion row, and the rest of the cosmology companion
stack remain unchanged in status. Their numerical claims are still bounded
by the cosmology-scale identification and matter-bridge gaps.

## Downstream Effect

On the retained-status surface established by this theorem, the EOS
corollary of
[`DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md`](DARK_ENERGY_EOS_RETAINED_COROLLARY_THEOREM_NOTE.md)
no longer sits on a "companion-lane spectral-gap vacuum identification".
Condition 3 of that note is now satisfied by this retained structural
identity theorem. The EOS corollary becomes a retained corollary without any
companion-surface conditioning step.

Condition 4 of the EOS corollary (fixed `R`) is the separate statement
that the vacuum-sector `R_Lambda` does not evolve. On the retained
stationary vacuum sector of condition (1) + (2) of this theorem, that
fixedness is automatic: the stationary Einstein/Regge solution by
definition has `d R_Lambda / d t = 0`. So condition 4 of the EOS corollary
is also discharged by the retained surfaces cited here, with no companion
lane invoked.

## Commands Run

```bash
python3 scripts/frontier_cosmological_constant_spectral_gap_identity.py
```

## Boundaries

This note does not close:

- the numerical value of `R` / `R_Lambda`: cosmology-scale identification
  remains the honest remaining gap, recorded in
  [`COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md`](COSMOLOGY_SCALE_IDENTIFICATION_AND_REDUCTION_NOTE.md),
  "Honest Remaining Gap";
- the numerical value of `Lambda`: bounded companion result of
  [`COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md`](COSMOLOGICAL_CONSTANT_RESULT_2026-04-12.md);
- the present-day `Omega_Lambda` value: gated on the matter-content bridge;
- the full FRW / expansion-history derivation: still conditional;
- any retained-grade promotion of the eight upstream authorities listed in
  the audit-driven dependency-edge rigorization section above;
- any chain closure beyond the two-leg algebraic identity reported by the
  runner.
