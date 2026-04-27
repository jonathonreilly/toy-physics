# Graviton-Mass Spectral-Gap Identity Theorem

**Date:** 2026-04-18
**Status:** **proposed_retained structural identity theorem** +
**bounded quantitative continuation**. Packages the already-exact-on-the-
retained-internal-surface relation `m_g^2 = 2 hbar^2 Lambda_vac / c^2` from
the graviton-mass companion into a standalone retained identity theorem,
built directly from the retained
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md)
on `main` and the Lichnerowicz TT spectrum on `S^3`. Publication matrix and
claims surfaces now capture the retained structural identity separately from
the bounded numerical companion.
**Script:** `scripts/frontier_graviton_mass_spectral_gap_identity.py`
**Upstream authorities (all retained on `main`):**
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md),
[`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md),
[`UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md`](UNIVERSAL_QG_SMOOTH_GRAVITATIONAL_GLOBAL_SOLUTION_CLASS_NOTE.md),
[`UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`](UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md),
[`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md),
[`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md)
**Related companion:**
[`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md) carries the
bounded numerical `m_g = 3.52 x 10^-33 eV` continuation and stays unchanged.

## Role

The purpose of this note is to split the existing graviton-mass companion
into two strictly separated pieces:

1. an **exact structural identity**
   `m_g^2 = 2 hbar^2 Lambda_vac / c^2 = 6 hbar^2 / (c^2 R^2)`
   on the retained de Sitter stationary vacuum + retained `S^3` spatial
   topology, valid for every `R > 0`; and
2. the **numerical value**
   `m_g = sqrt(6) hbar H_0 / c^2 ~ 3.52 x 10^-33 eV`, which is gated by the
   same cosmology-scale identification that keeps the numerical
   `Lambda` row bounded and which therefore stays bounded.

The identity is already explicitly called out as "exact" in
[`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md),
section "Exact (given S^3 with R = c/H_0)", point 6. This note does not add
new science — it packages that already-exact relation into a standalone
retained theorem that chains cleanly off
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md),
so the graviton-mass row can carry a dual-status architecture
(retained structural + bounded numerical) on the same template as
[`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md) and
[`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md).

## Theorem

Let the retained surface carry:

1. the retained spectral-gap cosmological-constant identity
   `Lambda_vac = lambda_1(S^3_R) = 3 / R^2` on the de Sitter stationary
   vacuum sector of the retained direct-universal GR closure (authority:
   [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md));
2. retained `S^3` spatial topology on `PL S^3 x R` with round spatial metric
   of radius `R`, for any `R > 0` (authority:
   [`S3_GENERAL_R_DERIVATION_NOTE.md`](S3_GENERAL_R_DERIVATION_NOTE.md),
   [`S3_CAP_UNIQUENESS_NOTE.md`](S3_CAP_UNIQUENESS_NOTE.md));
3. the standard Lichnerowicz operator on symmetric transverse-traceless
   (TT) rank-2 tensor perturbations of the retained metric, inherited from
   linear perturbation theory on the retained direct-universal GR +
   canonical textbook continuum GR closure on `PL S^3 x R` (authority:
   [`UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md`](UNIVERSAL_GR_DISCRETE_GLOBAL_CLOSURE_NOTE.md),
   [`UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md`](UNIVERSAL_QG_CANONICAL_TEXTBOOK_CONTINUUM_GR_CLOSURE_NOTE.md)).

**Theorem (graviton spectral compactness-mass identity).** Under conditions
(1)–(3), the TT graviton mass `m_g` on the retained de Sitter stationary
vacuum with round `S^3` slice of radius `R` satisfies the exact structural
identity

  `m_g^2  =  2 hbar^2 Lambda_vac / c^2  =  6 hbar^2 / (c^2 R^2)`,

for every `R > 0`. Equivalently the TT graviton Compton scale is
`lambda_C(g) = hbar / (m_g c) = R / sqrt(6)`. The identity is an exact
function identity in `R`; it does **not** fix a numerical value of either
`R`, `Lambda_vac`, or `m_g`.

**Higuchi corollary.** The Higuchi bound `m^2 >= 2 Lambda / 3` for a
non-ghost massive spin-2 field on de Sitter (Higuchi 1987) is satisfied on
the retained surface by exactly a factor of `3`:

  `m_g^2 / (2 Lambda_vac / 3)  =  (2 Lambda_vac) / (2 Lambda_vac / 3)  =  3`.

So the graviton is strictly non-tachyonic and strictly above the Higuchi
ghost threshold, with the overshoot determined by the retained spectral
ratio `lambda_2^TT / lambda_1 = 2` rather than by any input.

**Proof.** The proof has two independent legs that meet at `6 / R^2`.

*Leg A (Lichnerowicz TT spectrum on `S^3`).* On the round `S^3` of radius
`R` (condition 2), the Lichnerowicz operator `Delta_L` acting on symmetric
transverse-traceless rank-2 tensor modes `Y_l^{ab}` has spectrum

  `Delta_L Y_l^{ab}  =  ((l (l + 2) - 2) / R^2) Y_l^{ab}`,
  `l = 2, 3, 4, ...`

with lowest mode `l = 2` giving

  `lambda_2^TT  =  (2 * 4 - 2) / R^2  =  6 / R^2`.

There is no `l = 0` or `l = 1` TT mode because trace-free transverse
symmetric rank-2 tensors on `S^3` require at least quadrupolar angular
dependence. The `-2/R^2` curvature shift relative to the scalar Laplacian
eigenvalue `l (l + 2) / R^2` is the standard spin-2 Riemann-coupling term
on an Einstein manifold. (References: Higuchi 1987; Deser and Nepomechie
1984; Gibbons and Hawking 1993.) This is the content of
[`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md), Step 1,
rewritten here so the TT spectrum is in the chain of this note.

*Mass identification (KK-style compactness).* The linearized Einstein
equations on `PL S^3 x R` restricted to TT metric perturbations reduce,
after harmonic decomposition on `S^3`, to a family of decoupled 1+0D
oscillator equations for the modal amplitudes, one per spatial TT
harmonic. Each equation takes the form

  `(d^2 / dt^2 + c^2 lambda_l^TT) a_l(t)  =  0`,

so the modal amplitudes oscillate with angular frequency
`omega_l = c sqrt(lambda_l^TT)`. In the standard compactness / Kaluza-
Klein identification for a field on a compact spatial manifold, the 1+0D
effective rest-mass-squared per mode is `m_l^2 c^2 / hbar^2 = lambda_l^TT`
(equivalently `E_l = hbar omega_l` at vanishing linear momentum on the
compact slice). Applied to the lowest TT mode at `l = 2`:

  `m_g^2  =  hbar^2 lambda_2^TT / c^2  =  6 hbar^2 / (c^2 R^2)`.

This is the same identification recorded in
[`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md), Step 3,
as an exact consequence of the `S^3` Lichnerowicz spectrum. The retained
content of this theorem is the spectral identity and the KK rest-mass
identification; the separate question of whether this compactness-mass
behaves exactly like a 4D-effective-theory Fierz-Pauli mass at the quantum
level (the vDVZ issue) is **not** claimed and stays in the bounded
companion note (see "What Is Not Retained by This Theorem" below).

*Leg B (retained vacuum identity).* Condition (1) is the retained identity
theorem `Lambda_vac = 3 / R^2` for every `R > 0`. Substituting into the
Leg-A result gives

  `m_g^2  =  6 hbar^2 / (c^2 R^2)  =  2 * (3 / R^2) * hbar^2 / c^2
          =  2 hbar^2 Lambda_vac / c^2`.

*Closing.* Both forms are the same `R`-dependent function. The function
identity

  `m_g^2  =  2 hbar^2 Lambda_vac / c^2`

holds for every `R > 0` (equivalently for every admissible `Lambda_vac > 0`
in the retained de Sitter vacuum family). The Higuchi corollary follows by
substituting `m_g^2 = 2 hbar^2 Lambda_vac / c^2` into `m^2 c^2 / hbar^2
>= 2 Lambda / 3`: the left side is `2 Lambda` in mass-squared per `hbar^2
/ c^2`, and the right side is `2 Lambda / 3` in the same units, giving
a ratio of exactly `3`. □

## What Is Retained Exactly by This Theorem

- the Lichnerowicz TT lowest-eigenvalue coefficient `6` on `S^3`
  (standard spin-2 perturbation theory on Einstein manifolds);
- the `1 / R^2` scaling of `m_g^2`;
- the **function identity** `m_g^2 = 2 hbar^2 Lambda_vac / c^2` as a
  statement that holds for every `R > 0`, with no free parameter on the
  right-hand side that is not also on the left-hand side;
- the Higuchi-factor-of-3 corollary, with the factor fixed by the retained
  spectral ratio `lambda_2^TT / lambda_1 = 6/3 = 2` rather than by an
  input.

## What Is **Not** Retained by This Theorem

- the numerical value of `R` / `R_Lambda`: unchanged from
  [`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md);
- the numerical value of `m_g` in eV: remains the bounded continuation
  recorded in
  [`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md)
  and in the `graviton compactness mass m_g (numerical companion)` row of
  the current publication matrix;
- the 4D-effective-theory interpretation of the compactness mass `m_g` as
  a Fierz-Pauli-like massive-graviton mass with matching vDVZ behavior:
  the KK rest-mass identification is classical and standard, but the
  quantum-level defense that this compactness mass avoids the vDVZ
  discontinuity is only qualitative on `main` and is flagged as such in
  [`GRAVITON_MASS_DERIVED_NOTE.md`](GRAVITON_MASS_DERIVED_NOTE.md),
  Bounded point 8 and Step 5. This theorem covers only the spectral
  identity `m_g^2 = 2 hbar^2 Lambda_vac / c^2` in the retained KK rest-
  mass sense; it does **not** promote the full-4D-EFT "real graviton
  mass" claim;
- the Vainshtein-screening / solar-system consistency argument:
  quantitatively bounded-below-current-bounds in the companion, not a
  theorem;
- detectability: the prediction is `~10^10` below LIGO O3 and the
  strongest model-independent bound, unchanged on the retained surface.

## Dual-Status Architecture

The architecture is now directly parallel to
[`CKM_NEUTRON_EDM_BOUND_NOTE.md`](CKM_NEUTRON_EDM_BOUND_NOTE.md) and
[`CONFINEMENT_STRING_TENSION_NOTE.md`](CONFINEMENT_STRING_TENSION_NOTE.md):

- **retained structural identity (this note):**
  `m_g^2 = 2 hbar^2 Lambda_vac / c^2 = 6 hbar^2 / (c^2 R^2)` on the
  retained de Sitter + `S^3` surface, Higuchi-factor-3 corollary;
- **bounded quantitative continuation (unchanged):**
  `m_g ~ 3.52 x 10^-33 eV`, conditional on the cosmology-scale
  identification that keeps the numerical `Lambda` row bounded.

Unlike the EOS corollary row, this is a genuine dual-status row — both
pieces describe the same observable `m_g`. The retained piece fixes the
form of the relation; the bounded piece is the numerical evaluation.

## Relation to the Λ = λ_1(S^3_R) Identity

This theorem is strictly downstream of
[`COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md`](COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md):
that note retained `Lambda_vac = lambda_1(S^3_R) = 3/R^2`; this one adds
the Lichnerowicz TT lowest-mode side and reads off the pure-number
spectral ratio

  `lambda_2^TT / lambda_1  =  (6 / R^2) / (3 / R^2)  =  2`,

which converts the `Lambda_vac = 3/R^2` identity into

  `m_g^2 / Lambda_vac  =  (hbar^2 / c^2) * (lambda_2^TT / lambda_1)
                       =  2 hbar^2 / c^2`.

So:

- the scalar-Laplacian first eigenvalue `3/R^2` fixes `Lambda_vac`;
- the Lichnerowicz TT lowest eigenvalue `6/R^2` fixes `m_g^2 c^2/hbar^2`;
- the retained spectral ratio `6/3 = 2` is the number that turns the
  identity `Lambda_vac = 3/R^2` into the identity
  `m_g^2 = 2 hbar^2 Lambda_vac / c^2`.

Once the Λ identity is retained, the graviton-mass identity is one
spectral step away.

## Publication Matrix Capture

This theorem is now wired into
[`PUBLICATION_MATRIX.md`](publication/ci3_z3/PUBLICATION_MATRIX.md) as a
retained structural row distinct from the bounded numerical companion:

| Quantity / lane | Workstream | Framework result | Observation / comparator | Claim-strength status | Import class | Current publication decision | Authority / best source | Frozen-out ref |
|---|---|---|---|---|---|---|---|---|
| graviton spectral compactness-mass identity | retained `S^3` / topology cosmology | `m_g^2 = 2 hbar^2 Lambda_vac / c^2 = 6 hbar^2 / (c^2 R^2)` as an exact function identity in `R` on the retained de Sitter stationary vacuum + round `S^3` spatial topology; Higuchi factor-3 corollary | n/a (identity, not a numerical comparison) | retained | retained `Lambda_vac = lambda_1(S^3_R)` identity theorem + standard Lichnerowicz TT spectrum on `S^3` + classical KK-style compactness-mass identification for TT modes on the compact slice | retained theorem surface / SI eligible; bounded numerical `m_g` and the broader 4D-EFT/vDVZ interpretation stay in the companion row | this note + [COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md](../../COSMOLOGICAL_CONSTANT_SPECTRAL_GAP_IDENTITY_THEOREM_NOTE.md) | n/a |

The adjacent `Cosmological constant Lambda`, `Omega_Lambda`, spectral tilt
`n_s`, and other cosmology companion rows are unchanged in status. The
numerical `m_g` row stays bounded.

## Commands Run

```bash
python3 scripts/frontier_graviton_mass_spectral_gap_identity.py
```
