# Koide / SU(2)_L Gauge-Exchange Mixing Note

**Date:** 2026-04-17
**Status:** exact negative structural result — SU(2)_L gauge-boson
exchange on the retained `hw=1` triplet is species-diagonal and does
NOT generate a cross-species propagator `b = K_{12}`; therefore it
does NOT force the Koide cone `a_0^2 = 2 |z|^2`. Closes successor
Mechanism 2 of the G5 successor-candidate list.
**Script:** `scripts/frontier_koide_su2_gauge_exchange_mixing.py`
**Authority role:** this note is the theorem-facing support record
that closes the SU(2)_L gauge-exchange lane named by Agent 4 in
[CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md).
It does NOT supersede the primary Koide attempt note
[CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md](./CHARGED_LEPTON_KOIDE_CONE_ATTEMPT_NOTE.md)
or the pure-APBC extension theorem
[CHARGED_LEPTON_CURVATURE_LT_EXTENSION_NOTE.md](./CHARGED_LEPTON_CURVATURE_LT_EXTENSION_NOTE.md);
it runs strictly on top of them.

## Safe statement

On the current retained `Cl(3)/Z^3` framework surface, one-gauge-boson
exchange of the retained native-cubic `SU(2)_L` vectors does NOT lift
the `b = K_{12} = 0` result on the retained `hw=1` triplet. Explicitly:

- The native `SU(2)_L` generators `S^a` live in the taste `Cl(3)`
  subalgebra and act trivially on the retained species label
  `{X1, X2, X3}` (as `I_species`).
- Therefore every `SU(2)_L`-gauge-exchange insertion commutes with
  the three exact lattice translations `T_x, T_y, T_z` and with every
  rank-1 species projector `P_i`.
- By the observable-descent lemma (three-generation observable theorem
  [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)),
  `<P_i (SU(2)_L-exchange) P_j> = 0` for `i != j`.
- The correction is species-diagonal to all orders in `g_2`, not just
  at the leading `O(g_2^2)` one-exchange level.
- Color dressing on the quark sector multiplies the species-diagonal
  part by a color-singlet factor `C_color` without generating cross-
  species matrix elements.
- Consequently the observable-principle curvature circulant
  `(a, b)` receives only an `a`-type shift; the character ratio
  `a_0^2 / |z|^2` is unchanged. If we start at `b = 0` (which is the
  retained minimal-block state from Agent 1 and Agent 4), we stay at
  `b = 0`.

So the Koide cone condition `a_0^2 = 2 |z|^2` is NOT forced by
`SU(2)_L` gauge-boson exchange on the retained `hw=1` surface.

## Verdict (three-outcome)

- `SU2_GAUGE_EXCHANGE_FORCES_KOIDE=TRUE` — not realized
- `SU2_GAUGE_EXCHANGE_GENERATES_B=PARTIAL` — not realized
- `SU2_GAUGE_EXCHANGE_GENERATES_B=FALSE` — **realized**

Runner output: `PASS = 49, FAIL = 0`.

## Structural core of the theorem

The core observation is that the retained `hw=1` triplet separates
species via translation characters, while the retained native
`SU(2)_L` lives in the taste `Cl(3)` subalgebra. These two structures
factor on the retained physical surface: taste and species labels are
orthogonal carriers.

Let `rho_hw1(S^a)` denote the matrix action of `S^a` on the retained
`hw=1` species label. Because `S^a` lives in the taste algebra and
the species label is the translation-character BZ corner,

  `rho_hw1(S^a) = I_species   for all a in {1,2,3}`.

This makes each `S^a` commute with every `T_mu` and every `P_i`. Any
polynomial in `{S^a, X : X species-diagonal}` therefore commutes with
every `P_i`, so its species-off-diagonal matrix elements vanish.
Gauge-boson exchange is a polynomial in `S^a` and species-diagonal
propagator factors, so it inherits species-diagonality. This extends
Agent 4's pure-APBC theorem to the SU(2)_L-dressed level and is the
source of the FALSE verdict.

## Sign and magnitude

Even though the mechanism does not lift `b`, the diagonal a-type shift
it produces is recorded here for completeness. Using the retained
native `g_2(v) = 0.6480` from
[YT_EW_COLOR_PROJECTION_THEOREM.md](./YT_EW_COLOR_PROJECTION_THEOREM.md)
and the species-label Casimir `sum_a rho_hw1(S^a)^2 = 3 I_species`,

  `delta K_{ii} = -3 g_2^2 * <(P_i G_D)^2> ~ -1.26 * <(P_i G_D)^2>`

(units of propagator-squared). The sign is NEGATIVE and the magnitude
is species-independent at this order. Color dressing on quarks scales
this diagonal shift by the framework-native color-singlet factor
`C_color = 8/9` (retained in
[YT_EW_COLOR_PROJECTION_THEOREM.md](./YT_EW_COLOR_PROJECTION_THEOREM.md)),
still without generating species-off-diagonal elements.

## Relationship to other Koide lanes

This note is one step in the multi-agent attack surface consolidated
in
[CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md).
The status note lists four successor-candidate mechanisms for
lifting `b = 0` on the retained hw=1 triplet. This note resolves
Mechanism 2 (SU(2)_L gauge-exchange) as structurally insufficient.
The four remaining open mechanisms are unaffected:

1. **Two-Higgs / Z_3 doublet-block.** Attacked in the separate G1
   Yukawa lane. Not touched here.
2. ~~SU(2)_L gauge-exchange~~ — resolved as FALSE by this note.
3. **Wilson / lattice-improvement operators.** Higher-derivative
   lattice corrections that break translation-character orthogonality.
   Not attacked here.
4. **Non-APBC temporal mixing.** Thermal or non-periodic temporal
   modifications that could lift `b = 0`. Not attacked here.
5. **Color-theoretic sector correction** (Agent 6 lane). Tantalizing
   `Q_d / Q_\ell = 1.0959` vs `sqrt(6/5) = 1.0955` numerical
   fingerprint. This note is strictly orthogonal to the Agent 6 lane:
   Agent 6 attacks the Koide-VALUE derivation via color exponents,
   while this note attacks the `b`-generation mechanism via the weak
   gauge sector. The lanes are non-overlapping and complementary.
6. **Anomaly-forced 3+1 cross-species mechanism** (Agent 8 lane).
   Identified by Agent 5 as a concrete successor candidate. Not
   overlapped by this note.

## What this does not claim

- It does NOT promote `Q_\ell = 2/3` to a retained theorem. The
  algebraic cone equivalence (Agent 1, Steps 1-5) remains theorem-
  grade; the cone-forcing step remains open.
- It does NOT claim SU(2)_L gauge exchange is irrelevant to the
  charged-lepton spectrum. The correction renormalizes the diagonal
  species-curvature elements (`a`-type shift). It just does not force
  Koide.
- It does NOT close all four remaining successor mechanisms; only
  Mechanism 2 is resolved.
- It does NOT alter any retained authority (observable-principle
  generator, three-generation observable theorem, native gauge
  closure, YT/EW color-projection theorem). It runs strictly on top
  of these authorities.

## Dependency contract

Retained authorities used (on live `main`):

- `frontier_three_generation_observable_theorem.py` `PASS=47, FAIL=0`
- `frontier_charged_lepton_hw1_observable_curvature.py` (Agent 1
  primary attempt) — Steps 1-5 symbolic identities reused here
- `frontier_charged_lepton_curvature_lt_extension.py` (Agent 4 pure-
  APBC extension) — translation-character orthogonality reused here
- `frontier_non_abelian_gauge.py` — native cubic `Cl(3)/SU(2)` closure
  providing the exact `S^a` generators
- `frontier_complete_prediction_chain.py` / `frontier_yt_zero_import_chain.py`
  — framework-native `g_2(v) = 0.6480`

No Higgs VEV insertion or imported Yukawa structure is used, so this
note does not collide with the separate G1 Yukawa / Z_3 doublet-block
thread.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, one-gauge-boson
> exchange of the native `SU(2)_L` vectors between the three `hw=1`
> species is species-diagonal because the weak generators live in the
> taste `Cl(3)` subalgebra while the species label is carried by
> orthogonal translation characters. The observable-descent lemma then
> forces every cross-species matrix element of the SU(2)_L-dressed
> curvature correction to vanish. Color dressing on the quark sector
> does not lift this. Therefore Agent 4's `b = 0` theorem on the
> retained `hw=1` triplet extends to all orders in `g_2`, and the
> `SU(2)_L` gauge-exchange candidate for forcing the Koide cone
> `a_0^2 = 2 |z|^2` is structurally closed as a negative result. The
> cone-forcing step still requires a genuinely new retained primitive
> from the remaining successor candidates (two-Higgs / Z_3 doublet,
> Wilson / lattice improvement, non-APBC temporal mixing, color-
> theoretic sector correction, or anomaly-forced 3+1 cross-species).

## Validation

- [frontier_koide_su2_gauge_exchange_mixing.py](./../scripts/frontier_koide_su2_gauge_exchange_mixing.py)

Runner state at creation: `PASS=49, FAIL=0`.
