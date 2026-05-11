# Probe X-L1-Threshold — Heavy-Quark Wilson Chain Test (Negative Result, Bounded Obstruction)

**Date:** 2026-05-08
**Claim type:** bounded_theorem
**Status:** bounded - negative Wilson-chain extension test using
PDG masses only as falsifiability comparators; no Lane 1 threshold
closure or downstream status change.
**Scope:** Probe X-L1-Threshold of the Lane 1 (alpha_s) bridge
campaign. Tests whether the cited Wilson chain
`m = M_Pl * (7/8)^(1/4) * u_0 * alpha_LM^n` from
[`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
extends from the charged-lepton scale (m_tau) to the heavy-quark
scales (m_c, m_b, m_t), thereby converting "threshold matching"
from a literature import to a repo-derived chain.
**Primary runner:** [`scripts/cl3_koide_x_l1_threshold_2026_05_08_probeX_L1_threshold.py`](../scripts/cl3_koide_x_l1_threshold_2026_05_08_probeX_L1_threshold.py)
**Cache:** [`logs/runner-cache/cl3_koide_x_l1_threshold_2026_05_08_probeX_L1_threshold.txt`](../logs/runner-cache/cl3_koide_x_l1_threshold_2026_05_08_probeX_L1_threshold.txt)

## Result

The result is negative: the Wilson chain in the Probe-19 form does
**not** reach heavy-quark mass scales with integer or simple-rational
exponents at Probe-19 precision. Threshold matching coefficients
remain literature imports for the Lane 1 alpha_s closure.

## Context — what this probe addresses

The Lane 1 (alpha_s) bridge currently treats heavy-quark threshold
matching coefficients (charm at ~1.27 GeV, bottom at ~4.18 GeV, top at
~173 GeV in MS-bar running) as **literature imports**. These enter the
N5LO closed-form alpha_s(M_Z) closure as boundary conditions on
beta-coefficient generation hopping, but the matching coefficients
themselves are not derived from the physical `Cl(3)` local algebra on
the `Z^3` spatial substrate.

**Question:** does Probe 19's Wilson-chain pattern extend?

[`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
established (as a candidate positive theorem on the m_tau scale):

```
m_tau = M_Pl * (7/8)^(1/4) * u_0 * alpha_LM^18    [0.017% PDG match]
```

with exponent decomposition `18 = 16 + 2`: the EW exponent (16, taste
doublers in 4D) plus 2 additional powers of `alpha_LM` representing one
Yukawa-vertex factor at the lepton scale.

**If** the same chain pattern extends to heavy-quark mass scales — e.g.

```
m_q = M_Pl * (7/8)^(1/4) * u_0 * alpha_LM^(n_q)
```

for some repo-derivable integer or simple-rational `n_q` for each
of `m_c`, `m_b`, `m_t` — **then** threshold matching coefficients become
a repo-derived chain rather than a literature import, closing a known
admission in the Lane 1 bridge.

This probe runs the test and reports the result.

## Constraints (per task framing)

- **No new axioms** beyond the physical `Cl(3)` local algebra on the
  `Z^3` spatial substrate.
- **No new imports** beyond the cited Probe-19 chain.
- **No PDG values as derivation input.** PDG quark masses appear
  only as falsifiability comparators after the test is run.
- **Honest reporting.** Negative results are valuable; the whole point
  of this probe is to test whether Probe-19's Wilson chain extends, and
  to report what it actually does.

## Setup — cited Wilson chain (no derivation, no admission)

All values from [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
and [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md):

| Symbol | Value | Origin |
|---|---|---|
| `<P>` | 0.5934 | SU(3) plaquette MC at beta=6 (cited) |
| `M_Pl` | 1.221 * 10^19 GeV | Framework UV cutoff (cited) |
| `alpha_bare` | 1/(4 pi) ~= 0.07957747 | Cl(3) canonical (cited) |
| `u_0` | `<P>^(1/4)` ~= 0.87768 | Lepage-Mackenzie tadpole (cited) |
| `alpha_LM` | `alpha_bare/u_0` ~= 0.09067 | Geometric-mean coupling (cited) |
| `(7/8)^(1/4)` | ~= 0.96717 | APBC eigenvalue ratio (cited) |
| `A := M_Pl * (7/8)^(1/4) * u_0` | ~= 1.0365 * 10^19 GeV | Wilson chain prefix (cited) |

The Wilson chain prefix `A = M_Pl * (7/8)^(1/4) * u_0` is the common
factor across Probe-19's lepton chain, so the question reduces to:

> for each heavy quark `q in {c, b, t}`, is there a repo-derivable
> integer (or simple rational) `n_q` such that `A * alpha_LM^(n_q)`
> matches `m_q` to the same Probe-19-tier precision (~0.01-0.5%) that
> Probe 19 achieves for `m_tau`?

The Probe-19 reference exponent is `n_tau = 18` (giving `m_tau` to 0.017%).

## Test 1 — required exponent `n_q` for each heavy quark

Solving `A * alpha_LM^(n_q) = m_q^PDG` for `n_q`:

```
n_q = log(m_q^PDG / A) / log(alpha_LM)
```

with `log(alpha_LM) = -2.4006`. PDG values are used here ONLY to
compute the required exponent, not as derivation input.

| Quark | m_q (PDG) | n_q (required) | Residue from nearest integer |
|---|---|---|---|
| m_t (pole) | 173.0 GeV | 16.093 | +0.093 from 16 |
| m_t (MS-bar) | 162.5 GeV | 16.119 | +0.119 from 16 |
| m_b (MS-bar) | 4.18 GeV | 17.644 | -0.356 from 18 (or +0.644 from 17) |
| m_c (MS-bar) | 1.27 GeV | 18.140 | +0.140 from 18 |
| m_s (MS-bar) | 93.5 MeV | 19.227 | +0.227 from 19 |
| m_d (MS-bar) | 4.67 MeV | 20.475 | +0.475 from 20 |
| m_u (MS-bar) | 2.16 MeV | 20.796 | -0.204 from 21 |
| m_tau (PDG, ref) | 1.7768 GeV | **18.0001** | **+0.0001 from 18** |
| m_mu (PDG) | 105.66 MeV | 19.176 | +0.176 from 19 |
| m_e (PDG) | 0.5110 MeV | 21.397 | +0.397 from 21 |

**Observation 1.** Only `m_tau` lies on an integer exponent (18.0001,
matching the Probe-19 chain). The other charged leptons (m_e, m_mu) do
not — consistent with Probe 19's finding that the full lepton triplet
requires BAE + phi=2/9 admissions on top of the Wilson m_tau scale.

**Observation 2.** None of the heavy quarks (m_c, m_b, m_t) lie on
integer exponents to anywhere near the precision Probe-19 achieves
for m_tau. The smallest residues are +0.093 (m_t pole, +0.119 MS-bar)
and +0.140 (m_c). m_b is the worst: -0.356 from 18.

The required `alpha_LM^(0.1)` correction translates to a numerical
factor of about `exp(-0.1 * 2.4) = 0.787`, i.e. ~21% deviation from any
integer Wilson chain. For m_b the implied correction is `~57%`. This is
**three orders of magnitude worse** than Probe-19's m_tau match
(0.017%).

**Result for Test 1:** the Wilson chain in Probe-19's exact form does
NOT extend to heavy-quark mass scales with integer exponents.

## Test 2 — does any cited simple structural factor close the gap?

If `m_q = A * alpha_LM^(n_q) * F_q` for integer `n_q` and a simple
cited factor `F_q`, perhaps the Wilson chain still extends with
quark-specific structural prefactors.

**Candidate cited factors `F`:** `1/sqrt(2)`, `1/sqrt(3)`, `1/sqrt(6)`
(Clebsch-Gordan), `1/(4 pi) = alpha_bare`, `alpha_LM`, `u_0`, `1/u_0`,
`(7/8)^(1/4)`, the Brannen-tau structural factor `(1+sqrt(2)*cos(2/9))^2 ~= 5.66`.

Searching for matches `|A * alpha_LM^n * F - m_q| / m_q < 5%`:

| Quark | Best (n, F, predicted, residue) |
|---|---|
| m_t pole 173 GeV | NONE found at <5% (closest n=16, factor ~0.80, no simple rational) |
| m_t MS-bar 162.5 GeV | NONE found at <5% (closest n=16, factor ~0.75, no simple rational) |
| m_b 4.18 GeV | NONE found at <5% (closest n=18, factor ~0.43, no simple rational) |
| m_c 1.27 GeV | n=18, F=1/sqrt(2): 1.257 GeV, residue 1.05% (HIT but residue 60x worse than Probe 19 m_tau) |
| m_s 93.5 MeV | n=19, F=1/sqrt(3): 0.0930 GeV, residue 0.51% (HIT but residue 30x worse than Probe 19 m_tau) |

**Observation 3.** Two isolated near-hits exist (m_c with `1/sqrt(2)`,
m_s with `1/sqrt(3)`) but at residues `0.5-1%`, which is `30-60x` worse
than Probe-19's m_tau closure. These are most likely numerical
coincidences rather than structural derivations:
- The factors `1/sqrt(2)` and `1/sqrt(3)` are not picked out by any
  cited generation-distinguishing principle.
- The pattern is not consistent across the up-type or down-type
  triplet (no factor closes m_t or m_b at this precision).
- m_d, m_u show no simple-factor near-hits either.

**Result for Test 2:** no consistent cited simple structural factor
extends the Wilson chain to the full heavy-quark sector.

## Test 3 — do quark triplets satisfy a Brannen-circulant Koide identity?

Probe 19 closes the lepton triplet via the Brannen circulant
`H = aI + bC + b-bar*C^2` plus BAE (`|b|^2/a^2 = 1/2`) plus magic angle
(`phi = 2/9`). BAE forces Koide `Q = 2/3` exactly for the triplet
(per Theorem 1 of
[`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)).

If quarks lived on an analogous BAE circulant — even with a different
magic angle phi_q — they would also exhibit `Q = 2/3` exactly.

Computing Koide `Q = (sum m_q) / (sum sqrt(m_q))^2` for the up-type and
down-type triplets:

| Triplet | (m_1, m_2, m_3) GeV | Koide Q |
|---|---|---|
| Charged leptons | (0.000511, 0.10566, 1.7768) | 0.6667 (exact 2/3) |
| Up-type quarks | (0.00216, 1.27, 173.0) | **0.8491** (NOT 2/3) |
| Down-type quarks | (0.00467, 0.0935, 4.18) | **0.7313** (NOT 2/3) |

**Observation 4.** The up-type and down-type quark Koide ratios are
NOT 2/3. They differ from 2/3 by `~12%` (down-type) and `~27%` (up-type).
This is a robust empirical fact — the Koide identity is satisfied (to
high precision) by charged leptons, but is NOT satisfied by either
quark sector.

**Implication:** quarks cannot live on the same BAE circulant geometry
that closes Probe 19's lepton triplet. Even granting the BAE admission,
quarks satisfying `Q = 2/3` is empirically falsified. Therefore the
Probe-19 mechanism (Wilson m_tau scale + BAE + phi-magic giving the
full triplet) cannot extend to the quark sector via a parallel
construction.

**Result for Test 3:** the Brannen-BAE-circulant mechanism that closes
the lepton triplet at Probe 19 does NOT extend to either quark sector.

## Test 4 — sanity check: m_t = v_EW / sqrt(2) (y_t = 1 attractor) ?

The cited framework derives m_t through a separate route in
[`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md):
y_t Ward identity at M_Pl with `1/sqrt(6)` Clebsch-Gordan, 2-loop SM
RGE running, and `sqrt(8/9)` color-singlet projection, giving
`m_t(pole, 2-loop) = 172.57 GeV` (-0.07%).

A naive coincidence check: `m_t ~= v_EW / sqrt(2) = 174.16 GeV` (the
y_t = 1 limit), `0.67%` deviation from PDG 173.0 GeV. In Wilson chain
language this is `n = 16` (same as v_EW) with factor `1/sqrt(2)`. But
this is NOT the Probe-19 chain pattern — it is a different mechanism
(the y_t IR quasi-fixed-point attractor, cited), and the additional
factor `1/sqrt(2)` would need a separate derivation.

For m_b, [`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
explicitly establishes that the species-uniform reading of the cited
Ward identity falsifies `m_b` by 35x (gives 145 GeV vs PDG 4.18 GeV),
and a "species-differentiation primitive" is required to close the
absolute m_b scale. This is a known open admission separate from
the threshold-matching question.

**Result for Test 4:** the m_t scale is closed cited but via a
different mechanism (y_t QFP + RGE running) than Probe 19's direct
Wilson chain. m_b is explicitly an open admission. This is consistent
with the Probe-X-L1-Threshold negative result.

## Sharpened residue

This probe sharpens the L1 bridge admission landscape:

**(R1) Probe-19 chain is lepton-tau-specific.** The clean `n=18`
exponent that gives `m_tau` to 0.017% does not generalize to other
generation/quark species. The Wilson chain prefactor
`M_Pl * (7/8)^(1/4) * u_0` is universal; the integer exponent `18` is
not.

**(R2) Heavy-quark mass scales remain a literature import / open
admission.** The Lane 1 bridge's threshold matching coefficients
(charm, bottom, top) are NOT closed by the Wilson chain in Probe-19
form, by simple structural factors on top of integer Wilson powers,
nor by a parallel BAE-circulant mechanism. Each of these candidate
mechanisms fails distinctly:

- (R2a) integer-exponent Wilson chain: residues 0.09-0.36 at the
  exponent level (correspond to 20-57% mass deviations);
- (R2b) integer-exponent + simple structural factor: only sporadic
  isolated coincidences (m_c/m_s) at 30-60x worse precision than the
  m_tau closure, with no consistent pattern across triplets;
- (R2c) BAE-circulant Koide closure: empirically falsified by quark
  Koide Q values (0.85 up-type, 0.73 down-type, both significantly
  different from 2/3).

**(R3) Lane 1 admission landscape clarified.** The cited chain has
m_t closed via the y_t QFP + RGE route (separately cited).
m_b is a known open admission per
[`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md).
m_c and the threshold matching coefficients themselves remain
literature imports. This probe closes the question "does Probe 19 help"
in the negative.

## What this probe does NOT do

This note explicitly does **NOT**:

1. **Change any parent theorem.** No parent theorem is modified.
2. **Add a new axiom.** The physical `Cl(3)` local algebra on the
   `Z^3` spatial substrate remains the framework baseline.
3. **Use PDG values as derivation input.** PDG quark masses appear
   only as falsifiability comparators after the chain is constructed
   (and to compute the required exponent `n_q` for the negative test).
4. **Falsify any cited Probe-19 theorem.** Probe 19's m_tau closure
   is unaffected. This probe tests whether Probe 19's mechanism extends;
   the answer is no, but Probe 19 itself remains valid for m_tau.
5. **Falsify the cited y_t / m_t chain.** The cited m_t prediction
   via y_t QFP + RGE running (per
   [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md))
   is unaffected. This probe tests a different, simpler, candidate
   mechanism for m_t (and m_b, m_c) and reports it does not work.
6. **Close any L1 bridge admission.** Threshold matching coefficients
   remain a literature import. Probe X-L1-Threshold confirms this is
   the case under the Wilson-chain mechanism tested.

## What this probe DOES do

1. **Records a clean negative result.** Probe-19's exact Wilson chain
   does not extend to heavy-quark mass scales. The exponents `n_q`
   required are non-integer (residues 0.09-0.47 from nearest integer)
   and do not admit consistent cited simple-rational corrections.

2. **Sharpens the L1 bridge admission landscape.** Heavy-quark
   threshold matching coefficients remain literature imports; this
   probe forecloses one candidate route (Wilson-chain extension) for
   converting them to repo-derived chains.

3. **Confirms Probe 19's lepton-specific scope.** The clean `n=18`
   exponent for `m_tau` does not generalize. This is consistent with
   the prior 18-probe BAE finding that the lepton triplet's structure
   has lepton-specific algebraic content (BAE + phi=2/9) not shared
   by quarks.

4. **Provides a quantitative falsification basis** for any future
   probe that proposes a heavy-quark Wilson chain in the Probe-19 form.
   The required exponent residues are documented; any candidate
   mechanism must reach <0.5% precision to match the cited tier.

## Cross-references

### Foundational

- Minimal axioms: `MINIMAL_AXIOMS_2026-05-03.md`
- Substep-4 AC narrowing (PDG-input prohibition):
  `STAGGERED_DIRAC_SUBSTEP4_AC_NARROW_BOUNDED_NOTE_2026-05-07_substep4ac.md`

### Cited Wilson chain (Probe 19 source)

- Probe 19 m_tau Wilson chain:
  [`KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md`](KOIDE_BAE_PROBE_WILSON_CHAIN_MASS_SHARPENED_NOTE_2026-05-09_probe19.md)
- Complete prediction chain (v_EW, m_t, alpha_s):
  [`COMPLETE_PREDICTION_CHAIN_2026_04_15.md`](COMPLETE_PREDICTION_CHAIN_2026_04_15.md)
- alpha_LM geometric-mean identity:
  [`ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md`](ALPHA_LM_GEOMETRIC_MEAN_IDENTITY_THEOREM_NOTE_2026-04-24.md)

### Lane 1 admission landscape

- Bottom Yukawa species-differentiation admission:
  [`YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md`](YT_BOTTOM_YUKAWA_RETENTION_ANALYSIS_NOTE_2026-04-18.md)
- Charged-lepton Koide cone equivalence (Q = 2/3 from BAE):
  [`CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md`](CHARGED_LEPTON_KOIDE_CONE_ALGEBRAIC_EQUIVALENCE_NOTE.md)

## Validation

```bash
python3 scripts/cl3_koide_x_l1_threshold_2026_05_08_probeX_L1_threshold.py
```

Runner verifies:
1. Cited Wilson chain constants reproduce Probe-19 reference (m_tau
   to 0.017%).
2. Test 1: required `n_q` for each heavy quark is non-integer
   (residues > 0.09 in absolute value, vs Probe-19 m_tau residue 0.0001).
3. Test 2: no consistent cited simple structural factor closes
   the Wilson chain for the heavy-quark sector.
4. Test 3: up-type and down-type quark Koide Q values are NOT 2/3
   (0.85, 0.73 respectively), confirming quarks do not live on a
   BAE-circulant.
5. Test 4: sanity checks on the cited y_t / m_t alternative chain
   and the m_b open admission.
6. PDG values used only as comparators / for required-exponent computation,
   never as derivation input.
7. Honest negative result recorded.

## Future-use boundary

When reviewing future branches that propose to close threshold matching
coefficients via a Wilson-chain-style derivation:

1. The Probe-19 `n=18` exponent is m_tau-specific and does not extend
   to quarks; any candidate must address this directly.
2. Heavy-quark Koide Q is empirically not 2/3, ruling out a parallel
   BAE-circulant mechanism for the quark sector.
3. m_b remains a known open admission (species-differentiation
   primitive); m_c and threshold matching coefficients are literature
   imports unless explicitly derived.
4. Any candidate mechanism must reach Probe-19-tier precision
   (<0.5% on the mass scale) to be considered a closure rather than
   a coincidence.
5. PDG quark mass values must enter only as comparators after the
   derivation is constructed (substep-4 AC narrowing rule).
