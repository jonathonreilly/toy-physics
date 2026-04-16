# DM Eta Route Audit

**Date:** 2026-04-14  
**Branch:** `codex/dm-main-derived`  
**Purpose:** rank the surviving `eta` routes after the direct-observable
numerator pivot and the `g_bare` rigidity pass

---

## Status

**BOUNDED / OPEN**

This note answers two different questions cleanly:

1. what is the strongest paper-safe fallback if `eta` is still not derived?
2. if we still pursue a theorem-grade `eta`, which route is actually worth
   spending branch effort on?

The harsh answer is:

- fallback publication surface: `R(eta)`
- cleaner theorem-grade research program: leptogenesis via the taste staircase
- not promotable at paper bar: the current EW baryogenesis / transport stack

---

## Route Ranking

### 1. Paper-safe fallback: `R(eta)`

This is the strongest honest branch surface right now.

Claim boundary:

> Cl(3) on `Z^3` fixes the dark-sector freeze-out structure and therefore
> determines the dark-to-baryon ratio as a function of the baryon asymmetry
> `eta`; at the observed `eta`, this gives `R = 5.48`.

Why this wins:

- it uses the strongest surviving numerator authority
- it quarantines the unresolved denominator to one explicit cosmological input
- it avoids overstating the present `eta` routes

---

### 2. Best theorem-grade `eta` candidate: leptogenesis

Leptogenesis is the cleaner theorem program because it bypasses the branch's
worst EWBG contradiction entirely:

- no bubble-wall transport
- no detonation / deflagration fight
- no imported `C_tr` calibration
- no dependence on a disputed wall-local `v(T_n)/T_n` surface

Current branch state:

- `scripts/frontier_dm_leptogenesis.py` passes
- the observed `eta` falls inside a staircase band around `k_B = 7-8`
- `scripts/frontier_dm_select_kb.py` now shows a sharper signal:
  `k_B = 8` is the best structural candidate if neutrino Yukawas inherit a
  2-link suppression `y_nu ~ alpha_LM^2`
- `scripts/frontier_dm_neutrino_yukawa_candidate.py` strengthens that read:
  a second-order EWSB cascade gives a real bounded mechanism that lands near
  the `k_B = 8` Yukawa target
- `scripts/frontier_dm_neutrino_operator_selection_obstruction.py` exposed the
  old operator ambiguity between `Gamma_1` and `Xi_5`
- `scripts/frontier_dm_neutrino_dirac_bridge_theorem.py` now closes that local
  operator-selection step: the direct post-EWSB chiral surface is `Gamma_1`,
  while `Xi_5` is excluded as a direct Dirac operator
- `scripts/frontier_dm_neutrino_base_coupling_theorem.py` sharpened the old
  normalization ambiguity on the direct `Gamma_1` bridge
- `scripts/frontier_dm_neutrino_bosonic_normalization_theorem.py` now closes
  that ambiguity using the retained observable-principle toolkit: the raw
  chiral bridge has zero bosonic source-response, while the retained scalar
  completion `Gamma_1` carries the physical local response, so the full-space
  `g_weak/sqrt(2)` benchmark is selected and the active-space `g_weak`
  comparator is demoted
- `scripts/frontier_neutrino_majorana_residual_sharing_split_theorem.py` now
  fixes `eps/B = alpha_LM/2` on the minimal symmetric bridge
- `scripts/frontier_dm_z3_texture_factor_theorem.py` fixes the reduced
  democratic overlap factor exactly as `1/3`
- `scripts/frontier_dm_neutrino_atmospheric_scale_theorem.py` removes the old
  fitted `m_3` placeholder on the diagonal benchmark by predicting the
  atmospheric scale directly
- `scripts/frontier_dm_leptogenesis_universal_yukawa_nogo.py` proves the
  remaining reduced epsilon estimate cannot become exact while the Dirac
  Yukawa stays universal `Y = y_0 I`
- `scripts/frontier_dm_neutrino_schur_suppression_theorem.py` now closes the
  exact retained local second-order Dirac coefficient as well: the weak-axis
  selector curvature is `32`, the exact Schur complement generates `j^2/m`,
  and the retained local coefficient is therefore `g_weak^2 / 64`, which
  lands at `k_eff ~= 8.01`
- `scripts/frontier_dm_neutrino_weak_matching_obstruction.py` then closes the
  naive reuse question: the old top-Yukawa Ward / centrality mechanism does
  not transfer automatically, because `Gamma_1` is non-central and fails
  propagator / gauge-chain factorization
- `scripts/frontier_dm_neutrino_weak_vector_theorem.py` now closes one more

**Update after the new bridge/placement pass (2026-04-15):**

The branch no longer needs to treat the absolute staircase law as the live
open question on its minimal constructive bridge. It now has:

- exact doublet anchor on the endpoint-exchange bridge: `k_B = 8`
- exact singlet/doublet placement on the minimal adjacent lift:
  `k_A = 7`, `k_B = 8`

So the honest denominator blocker is now narrower:

> close the exact leptogenesis CP-asymmetry kernel on the already-fixed
> `A/B/epsilon` texture, now that the staircase placement, split law, and
> atmospheric benchmark inputs are fixed on the minimal bridge.
  operator-side question: the bridge family `Y_i = P_R Gamma_i P_L` is an
  exact weak spin-1 multiplet, so weak representation content is no longer the
  issue either
- `docs/DM_NEUTRINO_YUKAWA_BLOCKER_NOTE_2026-04-14.md` records why that is a
  real narrowing signal but still not a theorem
- the route is therefore bounded support, not unique closure

Exact blocker:

> the local Dirac selector is now closed strongly enough to select the
> `k_B ~= 8` scale on the present seesaw calibration. What remains open is the
> Majorana-side activation law: how the unique charge-`2` source turns on, and
> how that one amplitude feeds the three-generation `A/B/epsilon` structure.

The new obstruction is useful because it removes another fake escape hatch:
the branch no longer needs to keep pretending the denominator is blocked by
the Dirac coefficient. It is not. The live theorem target is now the Majorana
activation law, not another `Gamma_1` prefactor argument.

That means attacking:

1. an axiom-side activation law for the unique Majorana charge-`2` source
2. the map from that one-source amplitude to the three-generation
   `A/B/epsilon` texture
3. unification of the leptogenesis inputs with the complex-`Z_3` neutrino fit
4. `eps/B`, `m_3`, and the texture factor once the Majorana side is fixed

The new exact generation-side boundary matters here:

- `docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md`

It says the retained three-generation / `Z_3` texture does **not** rescue the
activation problem. It can organize an admitted pairing sector, but it cannot
turn one on inside the current retained normal grammar.

---

### 3. Current EW baryogenesis / transport: bounded support only

EWBG is numerically seductive because some branch scripts land near the
observed scale. It is still not promotable at theorem bar.

Why not:

1. the branch review still treats the live blocker as the transport sector
   behind `eta`
2. the branch still contains a regime mismatch between older partial-washout
   notes and newer stronger-EWPT / detonation notes
3. the surviving transport runners still lean on imported or bounded
   calibrations such as `C_tr`
4. the purported full-derivation runner still lives on that imported surface

Concrete audit points:

- `scripts/frontier_dm_coupled_transport.py` gives `eta / eta_obs ~ 0.38` on
  its own reconciled surface, but it still uses an FHS-calibrated transport
  coefficient
- `scripts/frontier_dm_eta_derivation.py` is exploratory EWBG support, not
  closure authority

So the correct read is:

- EWBG remains useful as bounded structural support
- EWBG is not the flagship theorem route for closing `eta`

---

### 4. Freeze-out bypass: valid logic, different blocker

The freeze-out bypass route is conceptually sharp:

`eta = C m_DM^2`

But it does not derive `eta` directly. It relocates the gap to the absolute
dark mass / hierarchy problem. That makes it a real long-term option, not the
best near-term closure route.

---

### 5. ADM and determinant/source-response: not current routes

- ADM is not viable as a branch closure route; the naive ratio is wrong and
  requires extra model-building
- determinant / source-response tooling is currently a dark-mass exploratory
  idea, not an `eta` derivation path

---

## Recommended Branch Policy

1. Package the flagship DM claim as `R(eta)`
2. Keep EWBG as bounded support only
3. If we keep spending research effort on `eta`, make leptogenesis the main
   theorem program
4. Only return to EWBG as flagship if a reconciled native EWPT result removes
   the detonation / regime-mismatch objection

---

## Clear Blocker

The next serious `eta` blocker is not "compute one more transport prefactor."
It is:

> derive or rule out the Majorana / `Z_3` activation law strongly enough to
> turn the now-closed local Dirac lane into a unique right-handed-neutrino
> scale and texture.

After the Schur pass, the sharpest way to say that is:

> the branch now has an exact retained local Dirac coefficient selecting
> `k_B ~= 8` on the present seesaw calibration. Without a Majorana activation
> law, however, the best result is still only a locally sharpened candidate
> plus a bounded leptogenesis surface.

The new mainline-atlas clarification is that the current observable-principle
toolkit is no longer a live rescue path: on the retained stack it is an exact
scalar charge-zero source-response theory, and its full observable jet is blind
to the Majorana amplitude. So the remaining theorem target is not "differentiate
the atlas harder." It is a genuinely new charge-`2` primitive or source law.

There is also a new positive clarification on the local bilinear lane: once a
charge-`2` primitive is admitted locally, the Pfaffian realization and local
generator `log(mu)` are forced. So the remaining theorem target is not local
Pfaffian bookkeeping either. It is primitive existence / activation.

The new final current-stack clarification is stronger still: the retained stack
is exhausted on that activation question. But the branch now also has a first
exact beyond-retained-stack extension principle:

- on the unique local `nu_R` block, the local quadratic source grammar closes
  as a pseudospin `su(2)`
- the retained normal slice is not closed under local canonical basis changes
- the minimal canonically closed source family is Nambu-complete

So the honest next move is no longer "derive some new charge-`2` source law
from scratch," and it is no longer "fix the staircase anchor or `eps/B`."
The branch now has all of those on the minimal bridge. The live blocker is
now downstream:

> derive the non-universal Dirac flavor texture (or equivalent extra
> structure) that makes the leptogenesis CP kernel nonzero on the fixed
> three-generation `Z_3` texture. The new universal-Yukawa no-go theorem
> now shows that the exact universal bridge `Y = y_0 I` cannot do it by
> unitary basis rotation alone. The newer CKM-texture transfer no-go theorem
> closes the next obvious rescue hatch too: the current CKM/NNI flavor tools
> do not transfer to this universal bridge, because its singular spectrum
> stays triple-degenerate, the GST/mass-hierarchy route collapses, the
> mass-basis NNI normalization becomes trivial, the Schur-complement route
> no longer generates hierarchical suppression, and phase-only companions
> still leave `Y^dag Y` proportional to `I`.

The new two-Higgs right-Gram bridge theorem sharpens that in a positive way:
the needed CP-supporting structure is not foreign to the local neutrino lane.
The canonical local two-Higgs neutrino branch already contains the
odd-circulant DM target on an exact admissible subcone `d >= 2 r`. So the
next honest theorem target is narrower:

> derive the actual axiom-side activation / coefficient law for the canonical
> distinct-charge two-Higgs neutrino branch, fixing the physical
> CP-supporting circulant data `(d,r,delta)` on the DM lane.

The new DM two-Higgs minimality theorem removes the last smaller-local-extension
loophole: once nonzero local DM CP support is required, single-Higgs and
repeated-charge lanes are exactly too small, and the canonical distinct-charge
two-Higgs class is the unique minimal exact local escape.

The new DM continuity sheet theorem removes the remaining local sheet loophole
too: on the DM circulant admissible subcone the residual `x <-> y` ambiguity is
fixed intrinsically by continuity to the retained universal bridge `Y = y_0 I`.

So the clean denominator-side blocker on the branch today is no longer a local
branch-selection or sheet-selection problem. It is the activation / coefficient
law for that now-isolated canonical two-Higgs branch.

The new odd-circulant residual-`Z_2` slot theorem and current-stack zero law
sharpen that once more into a final current-stack statement:

- the remaining local coefficient target is exactly the odd circulant slot
  `c_odd`
- the exact present-tense law on the retained local DM bank is
  `c_odd,current = 0`

So the next real move is no longer “derive a coefficient somehow” on the
present stack. It is derive a genuinely new residual-`Z_2`-odd bridge or
activator beyond the retained local bank.

The new odd-slot minimal mixed-bridge extension theorem then identifies the
smallest honest positive class for that object:

- residual-`Z_2` odd
- non-additive
- supported on the canonical non-universal two-Higgs locus
- one real amplitude on the unique odd class `i(S-S^2)`

And the strongest current positive route is now an explicit candidate family:

`K_lambda = d I + r (e^{i lambda delta_src} S + e^{-i lambda delta_src} S^2)`,

with exact weak-only source `delta_src = 2pi/3`. It is the best current
axiom-native prototype for turning on `c_odd`, but `lambda` is still not
derived on the retained bank.

That is the cleanest denominator-side blocker on the branch today.
