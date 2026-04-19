# G5 via G1 H-operator — Charged-Lepton Sector Test

**Date:** 2026-04-17
**Status:** negative structural result — applying the G1 retained affine
Hermitian `H(m, delta, q_+)` to the charged-lepton sector at the G1
observational chamber pin does NOT reproduce the charged-lepton Koide
relation, the Koide cone condition, or the observed charged-lepton
mass-ratio direction. A multi-start search finds no chamber-interior pin
that simultaneously saturates `Q = 2/3` and matches the observed
hierarchy. Verdict: `G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH`.
**Script:** `scripts/frontier_g5_via_g1_h_charged_lepton.py`
**Runner:** `PASS = 14, FAIL = 0`
**Authority role:** negative structural support note for G5. Rules out
the simplest and most direct reading of "apply G1's retained H to charged
leptons"; identifies precisely which retained primitive is still missing
for cone-forcing on the charged-lepton sector.
**Framework convention:** "axiom" means only the single framework axiom
`Cl(3)` on `Z^3`.

## Safe statement

The retained G1 affine Hermitian on the three-generation observable
algebra,

```
H(m, delta, q_+) = H_base + m T_m + delta T_delta + q_+ T_q,
gamma = 1/2, E1 = sqrt(8/3), E2 = sqrt(8)/3,
```

with the PMNS-pinned chamber point
`(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`, has eigenvalue
triple

```
lambda = ( -1.30909, -0.32043, +2.28659 )   (ascending, real).
```

Neither the "eigenvalue-as-mass" reading (m_i = |lambda_i|) nor the
"eigenvalue-as-spectral-amplitude" reading (m_i = lambda_i^2) reproduces
Koide `Q = 2/3` at this point, and the mass ratios on either reading
fall far from observed charged-lepton ratios
`(m_e / m_mu, m_mu / m_tau) = (0.00484, 0.0594)`.

A multi-start search over the entire retained chamber
`q_+ >= sqrt(8/3) - delta` for a separate charged-lepton pin produces
best residuals of `9.2e-02` (interp a) and `4.4e-03` (interp b), with
best points requiring parameter magnitudes `10^4`–`10^15`, i.e. far
outside any physically compact chamber region. No chamber-interior
`(m_l, delta_l, q_l)` reproduces the observed charged-lepton direction
and saturates Koide simultaneously.

## Context and motivation

The Physicist-H G1 closure theorem
[G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md)
promoted PMNS mixing to retained by direct diagonalization of
`H(m, delta, q_+)` on the retained hw=1 triplet, with observational
chamber pin `(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`.

The consolidated G5 status note
[CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md)
records that six independent no-go theorems eliminate every retained
non-Yukawa cross-species primitive on the hw=1 triplet. It flags the
G1 retained H operator as the unique remaining retained primitive
capable of forcing Koide cone condition `a_0^2 = 2|z|^2` on the
charged-lepton sector, and identifies the next theorem target as
applying `H(m, delta, q_+)` to charged leptons.

This note executes exactly that test.

## Three-outcome verdict

### Outcome TRUE (FALSE)

Defining condition: `H(m_*, delta_*, q_+*)` eigenvalues, under either
interpretation, reproduce the observed charged-lepton mass-direction
unit vector to cosine similarity `> 0.9999` AND saturate
`|Q - 2/3| < 10^-3`.

Result: FALSE.

- Interp (a), `m_i = |lambda_i|`:
  - `Q_a = 0.3771414068`, `|Q_a - 2/3| = 0.2895`
  - cone ratio `a_0^2 / (2|z|^2) = 7.609`
  - cosine similarity to observed = `0.8839`
- Interp (b), `m_i = lambda_i^2` (Dirac spectral amplitude readout):
  - `Q_b = 0.4593706275`, `|Q_b - 2/3| = 0.2073`
  - cone ratio `a_0^2 / (2|z|^2) = 2.645`
  - cosine similarity to observed = `0.9557`

Neither interpretation comes close. The PMNS-pinned chamber point does
not secretly encode the charged-lepton mass direction.

### Outcome PARTIAL_MATCH (FALSE)

Defining condition: some other chamber-interior pin
`(m_l, delta_l, q_l)` exists under either interpretation that
reproduces observed charged-lepton ratios AND saturates Koide to the
search tolerance `10^-6`.

Result: FALSE.

- Interp (a) best chamber pin (80-seed Nelder–Mead): objective
  `9.21e-02` at `(m, delta, q_+) ~ (-8397, 6.2, 4199)`. Best eigenvalue
  triple `(-12596, 0, +4199)`, giving ratios `(0, 0.333, 1)` vs
  observed `(0.00029, 0.0595, 1)`. `Q = 0.5359`.
- Interp (b) best chamber pin (80-seed Nelder–Mead): objective
  `4.40e-03` at `(m, delta, q_+) ~ (-1.11e15, 1.30e8, 5.53e14)`. `Q`
  converges toward `0.625` (the `m_min -> 0` limit), not `2/3`. Mass
  ratios `(0, 0.111, 1)` still fail observed `(0.00029, 0.0595, 1)`.

Neither interpretation admits a chamber-native pin reproducing both
Koide and the charged-lepton direction. The `H(m, delta, q_+)` spectrum
is algebraically too constrained: `tr H = m`, and the two remaining
eigenvalue parameters are set by `delta, q_+` through the fixed
generator structure — so the 3-dim chamber does NOT parametrize
arbitrary eigenvalue triples.

### Outcome NO_NATURAL_MATCH (TRUE)

Defining condition: neither the PMNS-pinned chamber point nor any
chamber-interior pin reproduces observed charged-lepton structure under
either interpretation.

Result: TRUE. This is the verdict recorded by the runner:
`G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH`.

## Quantitative outputs

### At the G1 observational chamber pin

```
(m_*, delta_*, q_+*) = (0.657061342210, 0.933806343759, 0.715042329587)
chamber slack q_+ + delta - sqrt(8/3) = 0.015856  (interior)
H(m_*, delta_*, q_+*) Hermitian:  yes
eigenvalues (ascending): lambda = (-1.3090943662, -0.3204336927, +2.2865894011)
tr H                  =  0.6570613422   =  m_*   (consistency)
```

Interpretation (a), `m_i = |lambda_i|`:
```
masses (a)            =  (0.32043369,   1.30909437,   2.28658940)     (ascending)
Q_a                   =  0.3771414068
amplitude v_a         =  (0.56606863,   1.14415662,   1.51214728)  (= sqrt|lambda|)
a_0,   a_0^2          =  1.86043765,    3.46122824
|z|,   |z|^2          =  0.47691153,    0.22744461
2|z|^2                =  0.45488922
ratio a_0^2/(2|z|^2)  =  7.6089475498     (1.0 iff Koide)
cos-sim to obs ray    =  0.88394294
```

Interpretation (b), `m_i = lambda_i^2`:
```
masses (b)            =  (0.10267775,   1.71372806,   5.22849109)     (ascending)
Q_b                   =  0.4593706275
amplitude v_b         =  (0.32043369,   1.30909437,   2.28658940)  (= |lambda|)
a_0,   a_0^2          =  2.26097147,    5.11199199
|z|,   |z|^2          =  0.98308314,    0.96645246
2|z|^2                =  1.93290491
ratio a_0^2/(2|z|^2)  =  2.6447198469     (1.0 iff Koide)
cos-sim to obs ray    =  0.95567248
```

PDG comparison only (never derivation input):
```
observed direction (sqrt(m_e), sqrt(m_mu), sqrt(m_tau))/||.||
                   =  (0.01647334, 0.23687900, 0.97139949)
observed Q_ell     =  0.66665909          (2/3 to 0.001%)
observed cone ratio a_0^2/(2|z|^2) = 1.00002274  (saturated)
```

### Chamber-native search

80 Nelder–Mead restarts on each interpretation, random seeds on
`[0.05, 3.0]^3`, with soft chamber penalty. Objective:

```
obj = (m_min/m_max - r0_obs)^2 + (m_mid/m_max - r1_obs)^2 + (Q - 2/3)^2
```

plus chamber penalty. Best results:

```
Interp (a):
  obj = 9.212459e-02
  (m, delta, q_+) = (-8397.07, 6.20, 4198.85)
  eigenvalues      = (-12596.24, ~0, +4199.17)
  ratios / max     = (0, 0.3334, 1)
  Q                = 0.5359

Interp (b):
  obj = 4.403572e-03
  (m, delta, q_+) = (-1.107e15, 1.296e8, 5.534e14)
  eigenvalues      = (-1.660e15, +1.118e7, +5.534e14)
  ratios / max     = (0, 0.1111, 1)
  Q                = 0.6250  (limit m_min -> 0 reading)
```

Objective never falls below `~1e-3`, and best points require parameter
magnitudes that exit any physically compact chamber region. The
3-parameter family `H(m, delta, q_+)` cannot simultaneously hit
`Q = 2/3` and observed charged-lepton ratios.

## What this does not claim

- This note does NOT claim that the G1 retained H operator is wrong or
  that G1 closure is undermined. G1 closure on the PMNS sector
  [G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md)
  stands in full.
- This note does NOT claim that Koide on the charged-lepton sector is
  falsified. Observed `Q_ell = 0.66666` matches `2/3` at PDG precision;
  the algebraic equivalence `Q = 2/3 <==> a_0^2 = 2|z|^2` on the hw=1
  triplet is theorem-grade.
- This note does NOT claim the charged-lepton sector is completely
  decoupled from G1. A sector-specific readout or sector-specific pin
  using retained primitives beyond `H(m, delta, q_+)` may still route
  charged leptons through G1-type machinery; this note rules out only
  the most direct application.
- This note does NOT claim that no retained chamber-interior pin exists
  for the charged-lepton sector. It claims that within the three
  retained degrees of freedom `(m, delta, q_+)` on the live
  source-oriented sheet, no interior pin reproduces both Koide and the
  observed charged-lepton ratio direction under either interpretation.

## Relationship to G1 closure and to the eight G5 attack lanes

### G1 closure (Physicist-H)

The retained affine `H(m, delta, q_+)` is the G1 retained object. On
the neutrino sector it is constructed to reproduce PMNS angles via the
charged-lepton basis `U_e = I_3` assumption from the retained
Dirac-bridge theorem
[DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
— i.e. charged-lepton mass eigenbasis coincides with the axis basis of
`H_hw=1`. In that route, the charged-lepton mass eigenvalues are
specified not by diagonalizing `H(m, delta, q_+)` but by a separate
retained diagonal object in the axis basis. This note's negative
result is consistent with (and in fact strengthens) that architecture:
**`H(m, delta, q_+)` carries the neutrino Hermitian structure on the
axis basis, not the charged-lepton mass spectrum**, and trying to pull
charged-lepton masses out of the `H` eigenvalues is architecturally
wrong.

### The eight G5 attack lanes

All eight G5 no-go agents (see
[CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md))
converge on the conclusion that the Higgs Yukawa is the unique
retained cross-species primitive on hw=1. This note adds:

- The Higgs Yukawa may be the unique cross-species primitive, but on
  the live source-oriented sheet the retained affine `H(m, delta, q_+)`
  is constructed to realize neutrino Hermitian observables, not
  charged-lepton mass eigenvalues. The charged-lepton Yukawa
  (retained as `Gamma_1` diagonal in the axis basis per the
  Dirac-bridge theorem) is a DIFFERENT retained object than
  `H(m, delta, q_+)`.
- Therefore G1 closure does not automatically close G5 as a retained
  corollary; the route "diagonalize H at the G1 chamber pin and read
  off charged-lepton masses" is structurally incorrect, not merely
  numerically mistuned.

### Next theorem target

The narrowed gap after this note:

> The retained charged-lepton Yukawa is the diagonal operator
> `Gamma_1` in the axis basis on hw=1 (Dirac-bridge theorem, retained).
> What retained primitive specifies the three diagonal entries of
> `Gamma_1` (i.e. `m_e, m_mu, m_tau`)?

Concrete targets:

1. **Retained species-dependent diagonal carrier.** If `Gamma_1` is
   diagonal in the axis basis, its three entries are C_3-characters of
   a hw=1 carrier. What retained structure fixes their ratios? Agent 6
   flagged `(C_F - T_F)^{-1/4} = (6/5)^{1/4}` as an exact Casimir
   identity. Whether it can be lifted to a retained diagonal carrier
   on hw=1 is open.
2. **Higgs VEV insertion as the forcing primitive.** On hw=1 the Higgs
   VEV is the unique species-coupling primitive. If `Gamma_1`'s
   diagonal entries are `y_i <phi>` with `y_i` fixed by a retained
   Higgs-current observable, the Koide cone condition reduces to a
   character-weight equation on the hw=1 Higgs-current bank.
3. **Joint-pinning theorem.** If neutrino `H(m, delta, q_+)` and
   charged-lepton `Gamma_1` share a hw=1 source, a joint pin
   `(m_*, delta_*, q_+*; y_e, y_mu, y_tau)` may force both PMNS and
   Koide from the same retained source. This is the genuinely flagship
   theorem that would make G5 a G1-corollary; it is NOT what was tested
   here.

## Dependency contract

Retained authorities used as inputs:

- [G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17](./G1_PHYSICIST_H_PMNS_AS_F_H_CLOSURE_THEOREM_NOTE_2026-04-17.md)
  — exact form of `H(m, delta, q_+)`, `H_base`, `T_m`, `T_delta`,
  `T_q`, `gamma = 1/2`, `E1 = sqrt(8/3)`, `E2 = sqrt(8)/3`; the
  observational chamber pin
  `(m_*, delta_*, q_+*) = (0.657061, 0.933806, 0.715042)`.
- [CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17](./CHARGED_LEPTON_KOIDE_G5_STATUS_NOTE_2026-04-17.md)
  — the Koide cone condition `a_0^2 = 2|z|^2` on the hw=1 C_3 character
  decomposition; the eight-agent no-go surface.
- [THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md](./THREE_GENERATION_OBSERVABLE_THEOREM_NOTE.md)
  — retained three-generation observable algebra on hw=1.
- [DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md](./DM_NEUTRINO_DIRAC_BRIDGE_THEOREM_NOTE_2026-04-15.md)
  — `Gamma_1` diagonal in axis basis on hw=1 (charged-lepton basis).

No new retained primitive is proposed. No new axiom. No post-axiom
selector law. Only standard numerical diagonalization and a
multi-start chamber search using sympy-free numpy/scipy.

PDG values `(m_e, m_mu, m_tau) = (0.511, 105.66, 1776.86) MeV` and
`Q_ell = 0.66666` are used ONLY as comparison targets, NEVER as
derivation input.

## Runner-verified content

`scripts/frontier_g5_via_g1_h_charged_lepton.py` executes
`PASS = 14, FAIL = 0` across six parts:

- **Part 1 (structural).** `H` Hermitian at G1 pin; pin inside chamber
  (slack `0.0159`); three real eigenvalues;
  `tr H = m_*`.
- **Part 2 (Koide at pin).** `Q_a = 0.377`, `Q_b = 0.459`, both in
  algebraic range `[1/3, 1]`, both far from `2/3`.
- **Part 3 (cone condition).** `a_0^2 / (2|z|^2)` equals `7.61`
  (interp a) and `2.64` (interp b), both far from `1.0`. Hermitian
  symmetry `|z| = |z_bar|` on both amplitude vectors. Observed
  charged-lepton `sqrt(m)` vector saturates cone to `~1e-5` (PDG
  sanity check).
- **Part 4 (direction).** cosine similarity to observed direction
  `0.88` (a) and `0.96` (b); both below the `0.9999` verdict
  threshold.
- **Part 5 (chamber search).** 80 Nelder–Mead restarts per
  interpretation; best objective `9.2e-02` (a) and `4.4e-03` (b). Best
  points at parameter magnitudes `~10^4`–`10^15`. No chamber-interior
  pin found to tolerance `1e-6`.
- **Part 6 (verdict).** `G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH`.

## Command

```bash
cd /Users/jonBridger/Toy\ Physics/.claude/worktrees/inspiring-meitner
python3 scripts/frontier_g5_via_g1_h_charged_lepton.py
```

Expected: `PASS = 14, FAIL = 0`, verdict line
`G5_CLOSES_VIA_G1_H = NO_NATURAL_MATCH`.

## Paper-safe wording

> On the retained `Cl(3)/Z^3` framework surface, the G1 retained affine
> Hermitian `H(m, delta, q_+)` (Physicist-H, 2026-04-17) diagonalized at
> the observational PMNS chamber pin
> `(m_*, delta_*, q_+*) = (0.657, 0.934, 0.715)` produces eigenvalues
> `(-1.309, -0.320, +2.287)`. Neither the eigenvalue-as-mass reading
> nor the eigenvalue-as-spectral-amplitude reading reproduces the
> charged-lepton Koide relation: `Q` differs from `2/3` by `0.29` and
> `0.21` respectively, and the Koide cone ratio `a_0^2 / (2|z|^2)`
> evaluates to `7.6` and `2.6` versus the required `1.0`. An 80-seed
> multi-start search over the retained chamber finds no interior pin
> reproducing both Koide and the observed charged-lepton hierarchy.
> This rules out the direct reading "apply G1's retained H to
> charged leptons and read off masses"; the charged-lepton Yukawa is
> a separate retained object (diagonal `Gamma_1` in the axis basis
> per the Dirac-bridge theorem), and the G5 next-theorem target is
> the retained character-weight carrier that fixes the three diagonal
> entries of `Gamma_1`.

## What this file must never say

- that `G5_CLOSES_VIA_G1_H = TRUE` or `PARTIAL_MATCH` (it is
  `NO_NATURAL_MATCH`);
- that the G1 closure theorem is weakened or overturned by this
  negative result (G1 closes PMNS; this note tests a different
  sector-application, not the G1 result);
- that Koide `Q_ell = 2/3` is falsified (observed `Q_ell` matches
  `2/3` to PDG precision; only the direct-H route is ruled out);
- that the charged-lepton Koide problem is permanently closed (the
  Higgs-Yukawa / diagonal-`Gamma_1` route remains the active open
  lane); and
- that the cone condition `a_0^2 = 2|z|^2` is not the right retained
  algebraic equivalence (it is; only the particular source of the
  amplitude vector is wrong on the direct-H route).
