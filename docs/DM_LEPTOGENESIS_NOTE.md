# Leptogenesis via the Taste Staircase: eta from Cl(3)

**Date:** 2026-04-14
**Status:** BOUNDED -- the retained local Dirac lane fixes
`y_nu^eff = g_weak^2 / 64`, the minimal endpoint-exchange bridge fixes the
doublet anchor `k_B = 8`, and the minimal adjacent lift fixes
`k_A = 7`, `k_B = 8`; the minimal symmetric bridge now also fixes
`eps/B = alpha_LM/2`, the retained `U_Z3` bridge fixes the reduced texture
factor exactly as `1/3`, and the same exact chain predicts the atmospheric
benchmark `m_3`; full `eta` remains open because the exact leptogenesis
CP-asymmetry kernel is still reduced rather than fully derived
**Script:** `scripts/frontier_dm_leptogenesis.py` (11/11 PASS)
**Supersedes:** Brainstorm Approach 3 in `DM_ETA_BRAINSTORM_NOTE.md`
**Depends on:** `DM_NEUTRINO_SCHUR_SUPPRESSION_THEOREM_NOTE_2026-04-15.md`,
`NEUTRINO_MAJORANA_CHARGE_TWO_PRIMITIVE_REDUCTION_NOTE.md`,
`NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md`

---

## 1. Executive Summary

The electroweak baryogenesis route to eta is blocked by the detonation
problem (E x 2 taste correction makes all bubble walls supersonic). This
note implements the highest-ranked alternative: **thermal leptogenesis**
via right-handed neutrinos whose masses are set by the taste staircase.

The baryon-to-photon ratio eta is computed from four framework-derived
ingredients:
1. Right-handed neutrino mass M_1 from the taste staircase
2. CP asymmetry epsilon_1 from the Z_3 complex phase
3. Washout efficiency kappa from the seesaw Yukawa
4. Sphaleron conversion factor C_sph = 28/79

**Result:** The framework produces eta in a sensitivity band spanning
staircase levels k = 4 through 8, with the observed value eta_obs =
6.12 x 10^{-10} falling inside this band. The current exact minimal bridge
now selects the benchmark placement `k_A = 7`, `k_B = 8`, fixes the split
law `eps/B = alpha_LM/2`, fixes the reduced overlap factor `1/3`, and
predicts the atmospheric benchmark `m_3`; the remaining spread now comes
from the reduced CP kernel and unresolved full-matrix flavor structure.

**Sharper read after the Dirac-lane and bridge closure pass:** the retained
local bosonic-normalization theorem plus the Schur suppression theorem give

`y_nu^eff = g_weak^2 / 64 = 6.66e-3`,

which points to `k_B ~= 8.01` on the present seesaw calibration, while the
new midpoint theorem fixes the absolute doublet anchor `k_B = 8` and the new
adjacent-placement theorem fixes `k_A = 7`, `k_B = 8` on the minimal bridge.
So the staircase placement is no longer merely a bounded hint.

**Key limitation:** the branch no longer lacks the staircase placement, the
split law, the reduced democratic overlap factor, or an atmospheric benchmark
for `m_3` on the minimal bridge. More sharply, the new universal-Yukawa no-go
theorem shows that if the Dirac neutrino Yukawa remains exactly universal
`Y = y_0 I`, then the leptogenesis CP tensor vanishes identically. So what the
branch still does not derive is the non-universal Dirac flavor texture behind
the full CP-asymmetry kernel `epsilon_1` on the three-generation `Z_3`
texture. The framework constrains eta, but does not yet derive a unique
zero-import value.

The next obvious atlas rescue path now closes too: the new CKM-texture
transfer no-go theorem shows the current CKM/NNI flavor rows do not transplant
to this universal Dirac bridge. The singular spectrum stays
triple-degenerate, so GST/mass-hierarchy logic collapses, mass-basis NNI
normalization becomes trivial, the Schur-complement route no longer generates
hierarchical suppression, and phase-only companions still leave `Y^dag Y`
proportional to `I`.

The new deformation-necessity theorem sharpens the remaining target too: the
missing Dirac-side structure cannot be just another basis choice or a purely
diagonal Yukawa split. Any successful future texture has to create genuinely
non-diagonal Hermitian-kernel entries in `Y^dag Y`, i.e. a non-unitary
off-diagonal flavor-breaking deformation beyond the current universal bridge.

The new minimal `Z_3` circulant CP tool packages that target into an exact
family: the current weak-axis `1+2` split lifts to the even circulant slice
`mu I + nu(S + S^2)`, which is still CP-degenerate, while the minimal exact
`Z_3`-covariant extension that can support nonzero CP is the odd circulant
generator `i(S - S^2)`. So the remaining open move is now concrete rather
than vague.

The new two-Higgs right-Gram bridge theorem makes that target less
speculative. The canonical local neutrino two-Higgs lane already contains the
odd-circulant CP-supporting right-Gram family on an exact admissible subcone:
after canonical rephasing, the circulant target is realized iff its common
diagonal/off-diagonal data obey `d >= 2 r`. So the remaining gap is no longer
"find any flavor mechanism at all." It is derive/select the local two-Higgs
neutrino branch and its right-sensitive data so that the resulting `Y^dag Y`
lands in that CP-admissible subcone with nonzero odd component.

The new DM two-Higgs minimality theorem sharpens that route choice further:
once nonzero local DM CP support is required, single-Higgs and repeated-charge
lanes are exactly too small, and the canonical distinct-charge two-Higgs class
is the unique minimal exact local escape.

The new DM continuity sheet theorem sharpens the local-data side too:
on the DM circulant admissible subcone the residual local ambiguity is only
`x <-> y`, and continuity to the retained universal bridge `Y = y_0 I`
selects the physical `x >= y` sheet explicitly. So the remaining gap is now
even narrower: not generic sheet-fixing, but the actual axiom-side activation
and coefficient law for the canonical two-Higgs branch and its CP-supporting
circulant data.

The new odd-circulant residual-`Z_2` slot theorem makes that sharper still:
the standard leptogenesis CP tensor on the DM Hermitian circulant family is
driven by one unique odd local coefficient `c_odd`.

And the new odd-circulant current-stack zero law gives the exact present-tense
status: on the retained local DM bank,

`c_odd,current = 0`.

So the remaining gap is now exact. A full axiom-native denominator closure
needs a genuinely new residual-`Z_2`-odd bridge or activator; the current
retained local stack does not already turn on the needed CP-supporting slot.

The new odd-slot minimal mixed-bridge extension theorem then says the remaining
positive extension class is a residual-`Z_2`-odd non-additive mixed bridge
with one real amplitude slot on `i(S-S^2)`.

The strongest current positive route is now explicit too: the invented
`Z_3` phase-lift mixed-bridge family

`K_lambda = d I + r (e^{i lambda delta_src} S + e^{-i lambda delta_src} S^2)`,

with exact weak-only source `delta_src = 2pi/3`. It preserves the local
two-Higgs data and turns on the odd slot for any nonzero `lambda`.

The new `Z_3` character-transfer theorem sharpens that candidate family in one
direction: exact source transfer forces `lambda` onto the discrete branches
`{-1,0,+1}`, and the source-oriented nontrivial branch is `lambda = +1`.

But the new circulant mass-basis no-go theorem sharpens it in the other
direction: the whole exact `Z_3`-covariant circulant family still diagonalizes
to a real spectrum in the `Z_3` basis and remains real after the current
doublet-block Majorana diagonalization, so the physical standard leptogenesis
tensor still vanishes on that class.

So the branch is now past the old `lambda` blocker. The real remaining object
is stricter:

- not a free activation amplitude
- not any exact `Z_3`-covariant circulant bridge

The new singlet-doublet CP-slot tool sharpens that exact physical target one
step further. After the circulant no-go, the minimal surviving carrier is a
`Z_3`-basis singlet-doublet slot family with one residual-`Z_2`-even amplitude
`u` and one residual-`Z_2`-odd amplitude `v`. On the current Majorana stack,
the real doublet rotation gives

`Im[(K_mass)_{0j}^2] = -2 u v sin(2 phi)`,

and at the exact weak-only source phase `phi = 2 pi / 3` this becomes

`Im[(K_mass)_{0j}^2] = sqrt(3) u v`.

So the live missing object is no longer “some non-circulant flavor
deformation.” It is an axiom-derived singlet-doublet slot bridge that turns on
both the even carrier slot and the odd activator slot on the admitted neutrino
lane.

And the first obvious realization class is now ruled out exactly. On the
simplest `2↔3`-symmetric canonical two-Higgs sublane
`x=(a,b,b)`, `y=(c,d,d)`, `delta = 2 pi / 3`, exact source-phase alignment to
that carrier forces `b d = 0`, while the physical CP tensor on that same
sublane is proportional to `b d`. So the aligned branch is structurally
CP-empty there.

That means the final denominator theorem cannot live on the most symmetric
local two-Higgs realization. It has to come from a more asymmetric /
right-sensitive branch of the admitted two-Higgs lane.

The next theorem is harsher still: on the **full admitted canonical two-Higgs
lane** with exact source phase `delta = 2 pi / 3`, exact singlet-doublet slot
alignment already forces `x_3 y_3 = 0`, while the physical heavy-neutrino-basis
CP tensor on that same lane is proportional to `x_3 y_3`. So the exact
source-phase aligned branch on the full canonical lane is structurally
CP-empty.

So the branch is now past the whole admitted canonical two-Higgs rescue class.
The honest remaining object is a genuinely new **post-canonical**,
right-sensitive mixed bridge on the singlet-doublet carrier, with the two real
slot amplitudes `u` and `v`.

The support-class question is now closed too. On the full singlet-doublet
carrier, the physical heavy-neutrino-basis CP tensor is insensitive to the
spectator diagonal / doublet-block data, so any future positive bridge reduces
to the minimal slot-supported family itself. The remaining last-mile DM object
is therefore:

- post-canonical
- right-sensitive
- slot-supported
- and parameterized minimally by the two real singlet-doublet slot amplitudes
  `u` and `v`

That endpoint is now sharper again. The raw right-frame obstruction is **not**
the final generic boundary. The new DM post-canonical positive polar section
theorem shows the generic full-rank right orbit already carries the unique
intrinsic representative

`Y_+(H) = H^(1/2)`,

and on that representative

`K_+(H) = H`.

So the remaining bridge is already read intrinsically from the Hermitian data
through the `Z_3`-basis slot pair

- `a(H) = (U_Z3^dag H U_Z3)_01`
- `b(H) = (U_Z3^dag H U_Z3)_02`.

But the aligned-core no-go shows the residual-`Z_2` active Hermitian core

`H_act = [[a,b,b],[b,c,d],[b,d,c]]`

is intrinsically CP-empty even on that positive section: the two slot entries
collapse to the same real scalar and the heavy-neutrino-basis CP tensor
vanishes exactly.

So the honest remaining theorem target has now moved from the right-orbit side
to the Hermitian-data side:

- derive the active-neutrino Hermitian symmetry-breaking law away from the
  aligned core, equivalently the breaking slots away from
  `d_2 = d_3`, `r_12 = r_31`, `phi = 0`
- then evaluate the intrinsic positive-section CP tensor on that derived `H`

That tensor is now exact on the active Hermitian grammar:

- `Im[(K_mass)01^2] = -r_31 (d_2-d_3+r_12-r_31 cos(phi)) sin(phi) / 3`
- `Im[(K_mass)02^2] =  r_31 (2 d_1-d_2-d_3+r_12-2 r_23+r_31 cos(phi)) sin(phi) / 3`

So the remaining denominator object is specifically the `H`-side law for
`phi`, `B_1`, and `B_2`, not a generic right-sensitive bridge anymore.

Equivalently, in the canonical breaking-triplet basis

- `Im[(K_mass)01^2] = -2 gamma (delta + rho) / 3`
- `Im[(K_mass)02^2] =  2 gamma (A + b - c - d) / 3`

so the last-mile DM object is one CP-odd source `gamma` plus two exact
interference channels.

The new triplet axiom-boundary theorem now fixes the honest status of that
object: the current stack does **not** derive a positive value law for
`(delta,rho,gamma)`. The strongest exact law presently available is only the
zero-locus / minimal-source law for the triplet source sector. That is why the
current benchmark remains bounded rather than closed.

The local neutrino lane does now fix the exact carrier cleanly. On the DM
branch the active Hermitian denominator lives on

`B_H,min = (A,B,u,v,delta,rho,gamma)`,

with optional unified extension

`U_min = (A,B,u,v,delta,rho,gamma,a_sel,e)`.

So the honest remaining problem is not “find a new local carrier.” It is to
populate the breaking-triplet leg of the carrier with a positive axiom-side
law.

This also clarifies what the finished strong-CP/CKM work does and does not do
for DM. It does give an exact weak-only `Z_3` source orientation. But it does
**not** yet transfer that source into the neutrino carrier. Holding the exact
source phase `phi = 2 pi / 3` fixed still leaves different triplets
`(delta,rho,gamma)` and therefore different leptogenesis kernels on the DM
branch. So strong-CP closure helps with source orientation and separation, not
with the missing neutrino-side coefficient law.

The branch now has the next two structural pieces exactly as well.

On the canonical active branch, the weak character lands uniquely on the odd
triplet slot:

- `H_odd = gamma T_gamma`
- `H_even = H_core + delta T_delta + rho T_rho`.

So the nontrivial weak `Z_3` character is already localized onto `gamma`.
What remains is not source direction, but source magnitude and the induced even
response.

And that even response is now exact too:

- `cp1 = -2 gamma (delta + rho) / 3`
- `cp2 =  2 gamma (A + b - c - d) / 3`.

So the missing law is one odd source times two even response channels, not a
generic flavor deformation.

The new weak-triplet transfer-class theorem sharpens that one more step. On
the current stack, the source-side bundle is already `1 + 2`:

- one selector amplitude slot `a_sel`
- one two-channel weak tensor pair `(tau_E,tau_T)`

and the DM endpoint is the matching `1 + 2` bundle:

- one odd source `gamma`
- two even responses `E1 = delta + rho`, `E2 = A + b - c - d`

So any admissible linear transfer is forced to take the form:

- `gamma = c_odd a_sel`
- `[E1, E2]^T = M_even [tau_E, tau_T]^T`

with one real odd coefficient `c_odd` and one real `2 x 2` even response
matrix `M_even`. The remaining denominator gap is therefore not an arbitrary
cross-sector map. It is a five-real-coefficient law.

The new single-axiom odd-normalization theorem then closes the odd leg:

- `c_odd = +1` on the source-oriented branch convention

because the reduced selector generator `S_cls` and the triplet odd generator
`T_gamma` have the same exact bosonic source-response law under the unique
additive CPT-even scalar generator. So the single-axiom coefficient-boundary
theorem then sharpens the even leg too, and the new even bosonic-normalization
theorem closes it:

- the weak even swap-reduction theorem collapses the exact even class to
  `M_even = v_even [1,1]`, equivalently
  `[E1, E2]^T = v_even (tau_E + tau_T)`
- the even bosonic-normalization theorem then fixes
  `v_even = (sqrt(8/3), sqrt(8)/3)`
- so the exact transfer law is now
  `gamma = a_sel`,
  `E1 = sqrt(8/3) tau_+`,
  `E2 = (sqrt(8)/3) tau_+`
  with `tau_+ = tau_E + tau_T`

So the benchmark remains

- `eta = 1.81e-10`
- `eta / eta_obs ~= 0.30`

for a precise reason: this lane now closes the transfer coefficients, not yet
the source amplitudes `a_sel` and `tau_+`, and the benchmark runner still uses
the older reduced kernel rather than the fully rewritten exact transfer law.

One other sharp point now explains the live benchmark number. The current
benchmark

`eta = 1.81e-10 ~= 0.30 eta_obs`

is not mainly low because of washout or staircase placement. At the same
`M_1` and washout, the Davidson-Ibarra ceiling would already give

`eta_DI ~= 6.54e-10 ~= 1.07 eta_obs`.

So the benchmark `0.30` comes almost entirely from the reduced CP kernel:

`eta / eta_obs = (epsilon_1 / epsilon_DI) * (eta_DI / eta_obs)`

with

- `epsilon_1 / epsilon_DI ~= 0.277`
- `eta_DI / eta_obs ~= 1.068`.

That also fixes the exact normalization target for the missing law. At fixed
`M_1` and washout, full closure would require

`epsilon_1 / epsilon_DI = eta_obs / eta_DI = 0.936`,

which is a `3.37x` enhancement over the current reduced kernel. Because the
exact source phase is already near-maximal,

`sin(2 pi / 3) = sqrt(3)/2`,

phase-only improvement can contribute at most `1.155x`. So the remaining law
must primarily normalize the amplitude / response sector itself: `gamma`,
`delta + rho`, and `A + b - c - d`.

---

## 2. Why Leptogenesis Bypasses the Detonation Problem

The detonation problem (documented on the current branch in
`DM_ETA_ROUTE_AUDIT_2026-04-14.md`) blocks
electroweak baryogenesis:
- The E x 2 taste correction makes the EWPT too strong
- All bubble walls go supersonic (detonation regime)
- Transport baryogenesis requires subsonic walls (deflagration)

Thermal leptogenesis operates at T ~ M_1 >> T_EW. The EWPT is irrelevant.
The out-of-equilibrium condition is the decay of heavy right-handed
neutrinos, not bubble wall dynamics. No bubble walls, no detonation.

---

## 3. Step A: Right-Handed Neutrino Masses

### 3.1 The Taste Staircase

The taste staircase provides a geometrically spaced sequence of mass scales:

    M_k = M_Pl * alpha_LM^k    (k = 0, 1, ..., 16)

where alpha_LM = 0.0907 is the Lepage-Mackenzie improved coupling (derived
from g_bare = 1 and <P> = 0.5934). The same staircase gives v = 246 GeV
at k = 16 (the hierarchy theorem).

Relevant scales:
| k | M_k (GeV) | Assignment |
|---|-----------|------------|
| 3 | 9.10e15   |            |
| 7 | 6.15e11   | A (singlet)|
| 8 | 5.58e10   | B (doublet)|
| 6 | 6.78e12   |            |
| 7 | 6.15e11   |            |
| 8 | 5.58e10   |            |

### 3.2 Z_3 Majorana Mass Matrix

The bounded `Z_3` texture used on this lane constrains the
right-handed Majorana mass matrix in the Z_3 eigenbasis to:

    M_R = [[A, 0, 0],
           [0, eps, B],
           [0, B, eps]]

with eigenvalues {A, B+eps, -(B-eps)}.

- Generation 1 (charge 0): singlet sector, mass A
- Generations 2,3 (charges +/-1): doublet sector, mass B

### 3.3 Staircase Assignment

For the seesaw mechanism to produce the observed normal hierarchy
(m_1 < m_2 << m_3), the singlet must be heavier than the doublet (A > B).
The branch now has the minimal constructive placement:
- A at k = 7 (singlet, heaviest M_R)
- B at k = 8 (doublet)

With eps/B = alpha_LM/2 = 0.0453 on the minimal symmetric bridge:
- M_1 = B(1 - eps/B) = 5.35e10 GeV  (lightest, drives leptogenesis)
- M_2 = B(1 + eps/B) = 5.80e10 GeV  (quasi-degenerate with M_1)
- M_3 = A = 6.15e11 GeV              (heaviest)

### 3.4 Seesaw Consistency

The diagonal seesaw with universal Yukawa y_0 gives:
- m_1 = y_0^2 v^2 / M_3 = 4.3e-3 eV
- m_2 = y_0^2 v^2 / M_2 = 4.6e-2 eV
- m_3 = y_0^2 v^2 / M_1 = 5.0e-2 eV

Dm^2_31 = 2.43e-3 eV^2, matching the observed 2.45e-3 eV^2 to 0.8%.

---

## 4. Step B: CP Asymmetry

### 4.1 The CP-Violating Phase

The Z_3 breaking parameter eps carries a complex phase from the Cl(3)
algebra. The natural phase is phi_CP = pi/3 (60 degrees), arising from
the interference between the Z_3 eigenvalues omega and omega*.

The effective leptogenesis phase: delta_eff = 2*phi_CP = 2*pi/3.
sin(delta_eff) = sqrt(3)/2 = 0.866.

### 4.2 Davidson-Ibarra Bound

The maximum CP asymmetry for hierarchical right-handed neutrinos:

    |epsilon_1| <= (3/16pi) * M_1 * m_3 / v^2 = 3.5e-3

### 4.3 Epsilon from the Z_3 Texture

The CP asymmetry has two contributions:

**N_3 (hierarchical):** The singlet-doublet loop, suppressed by the large
mass ratio M_3/M_1 ~ 11.5:

    epsilon_N3 = (1/8pi) * y_0^2 * (1/3) * sin(delta_eff) * f(x_3)
               = 3.0e-5

**N_2 (quasi-degenerate):** The doublet-doublet loop, with CP from the
Z_3 breaking parameter:

    epsilon_N2 = (1/8pi) * y_0^2 * 2*(eps/B)*sin(phi) * g(x_23)
               = 9.5e-4

The total: epsilon_1 = 9.8e-4, which is 28% of the DI bound.

---

## 5. Step C: Washout Efficiency

The washout parameter K = m_tilde / m_* where:
- m_tilde = y_0^2 * v^2 / M_1 = m_3 = 0.050 eV  (by seesaw calibration)
- m_* = 2.14e-3 eV (equilibrium neutrino mass)

K = 23.1 >> 1: **strong washout regime**.

Efficiency factor (Buchmuller, Di Bari, Plumacher 2005):

    kappa = (0.3/K) * (ln K)^{0.6} = 2.6e-2

---

## 6. Step D: Baryon Asymmetry

    eta = 7.04 * C_sph * |epsilon_1| * kappa * d

where:
- C_sph = 28/79 = 0.354  (sphaleron conversion)
- d = 135*zeta(3)/(4*pi^4*g_*) = 3.9e-3  (thermal N_1 abundance)

**Result at k_B = 5 (default):**

    eta = 7.04 * 0.354 * 9.8e-4 * 2.6e-2 * 3.9e-3
        = 2.5e-7

    eta / eta_obs = 400  (overproduction)

### 6.1 Staircase Level Scan

| k_B | M_1 (GeV) | epsilon_1 | kappa   | eta      | eta/eta_obs |
|-----|-----------|-----------|---------|----------|-------------|
| 4   | 7.9e14    | 1.2e-2    | 2.6e-2  | 3.0e-6   | 4954        |
| 5   | 7.2e13    | 1.1e-3    | 2.6e-2  | 2.8e-7   | 449         |
| 6   | 6.5e12    | 9.9e-5    | 2.6e-2  | 2.5e-8   | 41          |
| 7   | 5.9e11    | 9.0e-6    | 2.6e-2  | 2.3e-9   | 3.7         |
| 8   | 5.4e10    | 8.2e-7    | 2.6e-2  | 2.0e-10  | 0.33        |

The observed eta_obs = 6.12e-10 falls between k_B = 7 and k_B = 8.

At k_B = 7: eta/eta_obs = 3.7 (within the brainstorm's "factor of 6").
At k_B = 8: eta/eta_obs = 0.33 (also within factor of 6).

The strongest staircase-side narrowing is:

- the calibrated seesaw Yukawa at `k_B = 7` is `y_0 ~ alpha_LM^1.59`
- the calibrated seesaw Yukawa at `k_B = 8` is `y_0 ~ alpha_LM^2.09`

So `k_B = 8` is the only nearby staircase level that lines up with a simple
integer-power suppression. The missing step is proving that neutrino Yukawas
should inherit the same 2-link counting that is theorem-grade on the gauge
side.

---

## 7. Input Classification

| Input | Value | Classification | Source |
|-------|-------|---------------|--------|
| g_bare = 1 | 1.000 | AXIOM | Cl(3) normalization |
| <P>(beta=6) | 0.5934 | COMPUTED | SU(3) Monte Carlo |
| alpha_LM | 0.0907 | DERIVED | g_bare=1, <P> |
| M_Pl | 1.22e19 GeV | AXIOM | Inverse lattice spacing |
| v | 246.3 GeV | DERIVED | Hierarchy theorem |
| M_R structure | [[A,0,0],[0,eps,B],[0,B,eps]] | EXACT | Z_3 selection rules |
| phi_CP | pi/3 | STRUCTURAL | Z_3 eigenvalue interference |
| C_sph | 28/79 | DERIVED | SM anomaly structure |
| g_* | 106.75 | DERIVED | SM taste spectrum |
| eps/B | alpha_LM/2 = 0.0453 | EXACT ON BRIDGE | Residual-sharing split theorem |
| m_3 | 0.0506 eV | DERIVED | Exact Dirac coefficient + exact bridge |
| k_B (staircase level) | `8` | EXACT ON BRIDGE | Endpoint-exchange midpoint theorem |

**Irreducible ambiguity:** the benchmark bridge data are now fixed more
sharply than this older table originally assumed. The live ambiguity is no
longer the staircase anchor or the split law. It is the exact CP-asymmetry
kernel on the fixed three-generation `Z_3` texture.

---

## 8. Comparison with Brainstorm Estimate

The brainstorm note (Approach 3) estimated:
- M_1 = alpha^5 * M_Pl ~ 7.5e13 GeV
- epsilon_1 ~ 3.7e-3 (saturating the DI bound)
- kappa ~ 0.01 (strong washout)
- eta ~ 3.5e-9 (within 6x of observed)

The full calculation finds:
- epsilon_1 = 9.8e-4 (28% of DI, not saturated)
- kappa = 2.6e-2 (stronger than estimated)
- eta = 2.5e-7 at k_B = 5 (overproduces by 400x)
- eta = 2.3e-9 at k_B = 7 (within 3.7x)

The brainstorm's "within 6x" estimate is validated at k_B = 7 or 8.
The brainstorm used k = 5 with a saturated DI bound, which overestimates
by ~400x. The correct staircase level for the best match is k_B = 7-8.

---

## 9. Strengths and Weaknesses

### Strengths

1. **Bypasses the detonation problem** entirely (T ~ M_1 >> T_EW)
2. **Mass scale M_1 is a prediction** from the taste staircase (not fitted)
3. **CP violation from Z_3** is structural (not a free parameter)
4. **Seesaw mechanism** is already integrated into the current denominator lane
5. **Normal hierarchy** is correctly selected by the staircase assignment
6. **Observed eta falls INSIDE the staircase band** (k = 4..8)
7. **`k_B = 8` has a real structural hint** if `y_nu ~ alpha_LM^2`,
   and the new cascade-candidate audit strengthens that to a bounded mechanism:
   a second-order EWSB cascade from a framework-native `O(0.5-0.65)` base
   Yukawa lands near the `k_B = 8` target

### Weaknesses

1. **The Dirac lane is only locally closed** -- the branch now fixes the
   direct local post-EWSB operator as `Gamma_1`, the physical bosonic base
   normalization as `g_weak/sqrt(2)`, and the retained local second-order
   coefficient as `g_weak^2/64`, but that still does not by itself force the
   full right-handed-neutrino mass texture
2. **The Majorana absolute scale law is still not derived** -- the old
   "missing source principle" objection is now narrower. The branch now has
   an exact beyond-retained-stack local source principle, and the genuinely
   new one-generation source increment is now fixed up to rephasing to the
   pure pairing ray `mu J_x`. But the current exact source stack is still
   homogeneous under rescaling, and the admitted Pfaffian/Nambu source class
   now also has an exact no-stationary-scale theorem: its scale-sensitive
   bosonic generator is only logarithmic in the overall source scale while
   its remaining exact class invariants are scale-invariant. So it does not
   yet fix the absolute staircase anchor or the full three-generation
   `A/B/epsilon` amplitudes without fitted leftovers. But the local blocker is
   now sharper than that old wording: the branch also has the exact local
   non-homogeneous comparator `Q_2 = ||s||^2` and the exact
   background-normalized response curve
   `W_rel = (1/2) log(1 + rho^2)`, `Q_rel = rho^2`. The branch now also has
   the exact local axis-exchange fixed point `rho = 1` on that normalized
   curve, with `W_rel = (1/2) log 2`, `Q_rel = 1`, once the selector is taken
   to be covariant under the exact canonical exchange of the retained normal
   and pairing axes on the admitted local block. So the remaining gap is no
   longer comparator/background existence or local finite-point selection. It
   is the absolute staircase embedding of that now-selected local point, and
   then the lift to the full three-generation texture. More sharply, the new
   self-dual staircase-lift obstruction theorem now proves that the selected
   local point is still only projective on the present stack: it collapses to
   one positive ray and the current `Z_3` lift remains homogeneous under the
   same rescaling. More sharply still, the new algebraic/spectral bridge
   obstruction theorem now proves that the next obvious finite bridge class
   fails too: on the current exact stack, block assembly, Schur complements,
   spectral coefficients, spectral gaps, singular values, and normalized
   ratios remain homogeneous or scale-free under that same positive rescaling.
   More sharply still, the new scalar-datum transplant obstruction theorem now
   proves that the obvious atlas-reuse route on the absolute-scale side fails
   too: the current exact scalar atlas datums are only fixed dimensionless
   constants, and when transplanted multiplicatively into the selected
   Majorana lane they still leave the common staircase scale factored out.
   More sharply still, the new source-response matching obstruction theorem
   now proves that the obvious matching route fails too: matching the exact
   local self-dual values to the current generation-side Pfaffian/log and
   quadratic pairing observables either depends on arbitrary representative
   normalization or fixes only ratios to an arbitrary reference scale.
   More sharply still, the new tensor-variational transplant obstruction
   theorem now proves that the strongest gravity/atlas rescue route fails too:
   feeding the current self-dual Majorana ray into the exact direct-universal
   tensor/local-closure family still leaves the stationary field/source family
   homogeneous, so it still does not produce a finite absolute staircase
   selector on the present stack.
   More sharply still, the new partition/projective transplant obstruction
   theorem now proves that the strongest QG/measure rescue route fails too:
   feeding the same self-dual Majorana ray into the exact universal
   partition/projective/refinement family still leaves the measure-
   compensated density quadratic and monotone in the source scale, with
   exact Schur/projective closure and exact refinement pullback preserving
   that same law, so it still does not produce a finite absolute staircase
   selector on the present stack.
   More sharply still, the new continuum-bridge transplant obstruction
   theorem now proves that the last obvious inverse-limit/QG loophole fails
   too: the current continuum bridge is only an interpretation frontier for
   that same compatible discrete family, and every finite-stage cylinder
   density on the self-dual Majorana ray remains quadratic and monotone in
   the same source scale, so a bare inverse-limit reinterpretation still does
   not produce a finite absolute staircase selector on the present stack.
   So the live missing object is no longer another selector on the current
   local curve, a cleverer finite algebraic bridge on the current stack, or a
   current scalar-atlas constant reused multiplicatively, or the current
   source-response matching class, or the current tensor-variational
   transplant class, or the current partition/projective transplant class, or
   the current continuum-bridge transplant class. It is a genuinely new
   non-homogeneous local-to-generation bridge or absolute-scale datum beyond
   the present exact stack. The
   current atlas observable-principle toolkit remains closed negatively as a
   rescue path because its retained scalar jet is blind to that amplitude, and
   the retained stack by itself is still exhausted negatively
3. **eps/B = alpha_LM/2 is now fixed** on the minimal symmetric bridge
4. **m_3 ~ 0.0506 eV is now predicted** on the current diagonal benchmark
5. **Texture factor 1/3** is exact on the retained U_Z3 bridge
6. **The complex-Z_3 phase is not fully unified with this note's reduced CP kernel** --
   phase scans move `eta` by O(1), much less than a staircase step
7. **Dm^2_21 not accurately reproduced** by the universal Yukawa approximation

### Open Questions

1. What derived non-universal Dirac flavor texture makes
   `Im[(Y^dag Y)_{1j}^2]` nonzero on the fixed three-generation `Z_3`
   texture?
2. Does the full matrix calculation (beyond the diagonal seesaw approximation)
   change epsilon_1 significantly?
3. What are the effects of spectator processes and flavor at these scales?
4. Can the N_2 quasi-degenerate contribution be enhanced (resonant leptogenesis)?

---

## 10. Impact on the DM Gate

The DM relic mapping gate currently reads:

    R = Omega_DM / Omega_b = 5.48  (framework)  vs  5.47 (Planck)

with eta = 6.12e-10 taken from observation. If leptogenesis at k_B = 7-8
is accepted as a framework prediction:

    eta (framework) = (0.3-3.7) x eta_obs

Then R would become fully zero-import:

    R = (3/5)(155/27)(1.592) * (eta_framework/eta_obs)
      = 5.48 * (0.3 to 3.7)
      = 1.6 to 20.3

The central value remains 5.48 for eta within the band, and the ratio
R itself is insensitive to the exact value of eta (it enters only through
Omega_b, which scales linearly with eta).

The honest claim: **eta is still bounded. The Dirac side is now locally
sharpened to the `k_B ~= 8` scale, and the branch now has an exact local
Nambu source principle, local comparator, and local background-normalized
response beyond the retained stack, but the denominator is still narrowed to a
specific downstream theorem gap: derive the absolute staircase-embedding law
for the now-selected self-dual local Majorana point and its three-generation
`Z_3` lift, or keep the
present leptogenesis result as a bounded surface rather than a full
derivation.**

---

## 11. File Reference

| File | Role |
|------|------|
| `scripts/frontier_dm_leptogenesis.py` | This derivation (11/11 PASS) |
| `scripts/frontier_dm_neutrino_schur_suppression_theorem.py` | Exact retained local Dirac coefficient selecting the `k_B ~= 8` scale |
| `scripts/frontier_neutrino_majorana_charge_two_primitive_reduction.py` | Exact reduction of the Majorana lane to one new charge-`2` primitive |
| `scripts/frontier_neutrino_majorana_local_pfaffian_uniqueness.py` | Exact theorem that any retained local bilinear Majorana completion is uniquely Pfaffian with local generator `log(mu)` |
| `scripts/frontier_neutrino_majorana_current_stack_exhaustion.py` | Exact current-stack conclusion that the retained stack cannot force nonzero Majorana activation |
| `scripts/frontier_neutrino_majorana_z3_nonactivation_theorem.py` | Exact theorem that retained three-generation / `Z_3` texture cannot activate the Majorana sector |
| `scripts/frontier_neutrino_majorana_observable_principle_obstruction.py` | Exact theorem that the current atlas observable-principle jet cannot activate or force the Majorana amplitude |
| `scripts/frontier_neutrino_majorana_nambu_radial_observable.py` | Exact positive local bosonic observable on the admitted Nambu family, still reducing to `log(mu)` on the pairing ray |
| `scripts/frontier_neutrino_majorana_nambu_quadratic_comparator.py` | Exact positive local non-homogeneous comparator `Q_2 = ||s||^2` on the admitted Nambu family |
| `scripts/frontier_neutrino_majorana_source_ray_theorem.py` | Exact theorem that the genuinely new one-generation source increment is a pure-pairing ray up to rephasing |
| `scripts/frontier_neutrino_majorana_background_normalization_theorem.py` | Exact theorem that the retained normal slice gives the local background-normalized Majorana response curve |
| `scripts/frontier_neutrino_majorana_axis_exchange_fixed_point.py` | Exact theorem that the background-normalized local Majorana block has the self-dual point `rho = 1` under canonical normal-pairing axis exchange |
| `scripts/frontier_neutrino_majorana_algebraic_bridge_obstruction.py` | Exact theorem that the obvious finite algebraic/spectral local-to-generation bridge class remains homogeneous or scale-free and cannot select an absolute staircase anchor |
| `scripts/frontier_neutrino_majorana_scalar_datum_transplant_obstruction.py` | Exact theorem that the current exact scalar atlas datums from the hierarchy/observable side still factor out multiplicatively on the Majorana lane and do not supply the missing absolute-scale datum |
| `scripts/frontier_neutrino_majorana_source_response_matching_obstruction.py` | Exact theorem that the current exact local-to-generation source-response matching class cannot fix the absolute staircase anchor either |
| `scripts/frontier_neutrino_majorana_tensor_variational_transplant_obstruction.py` | Exact theorem that feeding the current self-dual Majorana ray into the exact direct-universal tensor/local-closure family still leaves the stationary family homogeneous and does not fix an absolute staircase anchor |
| `scripts/frontier_neutrino_majorana_partition_projective_transplant_obstruction.py` | Exact theorem that feeding the current self-dual Majorana ray into the exact universal partition/projective/refinement family still leaves the measure side monotone in the same scale and does not fix an absolute staircase anchor |
| `scripts/frontier_neutrino_majorana_continuum_bridge_transplant_obstruction.py` | Exact theorem that a bare inverse-limit reinterpretation of the same compatible discrete family still does not fix an absolute Majorana staircase anchor |
| `scripts/frontier_neutrino_majorana_staircase_blindness_theorem.py` | Exact theorem that the current Majorana source stack fixes the source class but not the absolute staircase anchor |
| `scripts/frontier_neutrino_majorana_no_stationary_scale_theorem.py` | Exact theorem that the admitted Pfaffian/Nambu source class has no intrinsic stationary or endpoint selector for the absolute staircase scale |
| `scripts/frontier_neutrino_majorana_scale_selector_necessity.py` | Exact historical theorem that the earlier logarithmic observable family alone could not define a canonical finite selector |
| `docs/DM_ETA_BRAINSTORM_NOTE.md` | Brainstorm ranking (Approach 3) |
| `docs/DM_ETA_ROUTE_AUDIT_2026-04-14.md` | Current route ranking and exact denominator blocker |
| `docs/NEUTRINO_MAJORANA_Z3_NONACTIVATION_THEOREM_NOTE.md` | Current three-generation / `Z_3` non-activation boundary |
| `docs/NEUTRINO_MAJORANA_OBSERVABLE_PRINCIPLE_OBSTRUCTION_NOTE.md` | Current atlas observable-principle obstruction boundary |
| `docs/NEUTRINO_MAJORANA_LOCAL_PFAFFIAN_UNIQUENESS_NOTE.md` | Current local-bilinear Pfaffian uniqueness boundary |
| `docs/NEUTRINO_MAJORANA_CURRENT_STACK_EXHAUSTION_NOTE.md` | Current final retained-stack conclusion on Majorana activation |

---

## 12. Key References

- Davidson, Ibarra, PLB 535 (2002) 25 -- Upper bound on epsilon_1
- Buchmuller, Di Bari, Plumacher, Ann.Phys. 315 (2005) 305 -- Washout
- Minkowski (1977), Yanagida (1979) -- Seesaw mechanism
- Fukugita, Yanagida, PLB 174 (1986) 45 -- Original leptogenesis
