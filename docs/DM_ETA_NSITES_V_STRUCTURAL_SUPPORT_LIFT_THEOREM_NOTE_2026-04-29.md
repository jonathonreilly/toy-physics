# DM eta N_sites · v Structural Support Theorem (V1)

**Date:** 2026-04-29
**Status (actual current surface):** `bounded` support theorem —
records that the DM η freeze-out-bypass quantitative theorem
(2026-04-25) has structural support from the composed product
`N_sites · v`, with retained N_sites + retained EW v on the A_min
surface. The G1 (dark-singlet collective-mode Coleman-Weinberg
mechanism) remains EXPLICITLY OPEN. No audit-ratified tier is claimed.
**Primary runner:** `scripts/frontier_dm_eta_nsites_v_structural_support_lift.py`

**Cited authorities (one-hop deps):**
- [DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md](DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md)
  — bounded DM η freeze-out-bypass identity `eta = C · m_DM²` +
  audit-discovered candidate `m_DM = N_sites · v`.
- [HIGGS_MASS_FROM_AXIOM_NOTE.md](HIGGS_MASS_FROM_AXIOM_NOTE.md)
  — retained `N_sites = 2^d = 16` on the minimal APBC block on Z^4.
- [OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md](OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md)
  — retained EW v = 246.282818290129 GeV.
- [R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md](R_BASE_GROUP_THEORY_DERIVATION_THEOREM_NOTE_2026-04-24.md)
  — retained R_base = 31/9 group-theory identity.

---

## 0. Headline

The DM η freeze-out-bypass theorem (2026-04-25) discovered, via a
systematic audit of 22 single-block structural multipliers, that
exactly one candidate `m_DM = N_sites · v = 16 · v ≈ 3940 GeV` lands
within 5% of the freeze-out target (next-closest at -29.63%, a 14×
gap). Among 10,743 structural identities of complexity up to 4, only
0.75% land within 5%.

The N_sites = 16 quantity is itself ALREADY retained on the framework
surface via HIGGS_MASS_FROM_AXIOM_NOTE — N_sites = 2^d = 16 is the
size of the minimal APBC block on Z^4 (4-dim spacetime).

The EW v = 246.28 GeV is ALREADY retained via
OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.

V1 composes these three: the N_sites · v structural product is
**framework-composed from retained pieces** (no new combinatorial
input). This gives bounded structural support for the DM η candidate
identification, without deriving the dark-singlet selector.

The remaining open piece — the structural mechanism that fixes the
dark singlet's collective mode at exactly N_sites · v rather than
some other framework scale (Coleman-Weinberg G1) — is unchanged and
explicitly carried forward.

---

## 1. The composed structural product

### 1.1 Retained N_sites = 16

By HIGGS_MASS_FROM_AXIOM_NOTE.md (lines 26-30, 40, 53, 57, 59-60,
84, 90):

```text
Minimal APBC block on Z^4 has L = 2, N_sites = 2^d = 2^4 = 16
N_tot = N_c · N_sites = 48
N_taste = N_sites = 16 (taste eigenvalues on the minimal block)
```

This is retained framework content with d = 4 (spacetime dimension
forced by anomaly-forced 3+1) and L = 2 (minimal APBC).

### 1.2 Retained EW v

By OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md:

```text
v = M_Pl · (7/8)^{1/4} · alpha_LM^16 = 246.282818290129 GeV
```

This is retained on the canonical Planck/hierarchy surface.

### 1.3 Composed structural product

```text
m_DM = N_sites · v = 16 · 246.282818290129 GeV = 3940.5251 GeV ≈ 3.94 TeV
```

This is a framework-composed product of two retained quantities. No
new audit input required.

### 1.4 Composition with the freeze-out-bypass theorem

DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM eq. (2):

```text
eta = C · m_DM²
C = K · x_F / (sqrt(g_*) · M_Pl · π · α_X² · R · 3.65e7)
```

Substituting `m_DM = N_sites · v`:

```text
eta = C · N_sites² · v²
    = C · 256 · (246.28 GeV)² ≈ 6.38 × 10^{-10}
```

at the central point `(x_F = 25, S_vis/S_dark = 1.59, α_X = α_LM)`.
The `α_X = α_LM` identification is the inherited candidate-route choice
from the bounded DM η note, not a new retained input.

This is `+4.22%` from the Planck observed value `eta_obs = 6.12 ×
10^{-10}` (within the bounded Sommerfeld + freeze-out band).

---

## 2. Theorem statement

**Theorem (DM eta N_sites · v Structural Support).**
On the A_min surface with retained N_sites = 16 (from minimal APBC
on Z^4) and retained EW v ≈ 246.28 GeV (from observable-principle-
from-axiom), the DM mass candidate

```text
m_DM = N_sites · v = 16 · v ≈ 3940 GeV
```

is the unique framework-composed single-block structural product
landing within 5% of the freeze-out-bypass target on the bounded DM
η identity `eta = C · m_DM²`. Combined with retained R_base = 31/9
and bounded Sommerfeld + freeze-out band, this gives the bounded
prediction band `eta_pred ∈ [5.25 × 10^{-10}, 8.11 × 10^{-10}]`,
bracketing the Planck observation.

**Status:** `bounded` support — the candidate is recorded as a
framework-composed structural product, but the dark-singlet
collective-mode mechanism G1 remains explicitly open. NOT a retained
closure of the DM mass.

### Proof

**Step 1 (N_sites retained).** By HIGGS_MASS_FROM_AXIOM_NOTE.md,
N_sites = 2^d = 16 on the minimal APBC block on Z^4 (where d = 4
is the spacetime dimension forced by anomaly-forced 3+1).

**Step 2 (v retained).** By OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE.md,
v = M_Pl · (7/8)^{1/4} · alpha_LM^{16} = 246.282818290129 GeV.

**Step 3 (compose).** The product N_sites · v is well-defined on the
framework's retained quantitative surface:
```text
N_sites · v = 16 · 246.282818290129 GeV = 3940.5251 GeV
```
No additional input required.

**Step 4 (substitute into DM η identity).** By DM_ETA_FREEZEOUT_BYPASS
eq. (2): eta = C · m_DM². Substituting m_DM = N_sites · v gives
eta = C · N_sites² · v². Numerically eta_pred ≈ 6.38 × 10^{-10}
(central).

**Step 5 (bounded band).** With bounded Sommerfeld continuation
S_vis/S_dark ∈ [1.4, 1.7] and freeze-out coefficient x_F ∈ [22, 28],
the bounded band on eta_pred is [5.25 × 10^{-10}, 8.11 × 10^{-10}],
bracketing eta_obs = 6.12 × 10^{-10}.

**Step 6 (uniqueness within the audit class).** The 22-multiplier
audit (from the freeze-out-bypass theorem) shows only N_sites · v
lands within 5%; next-closest at -29.63%. So the framework-composed
N_sites · v product is the unique candidate within the systematic
single-block multiplier class. **QED on the bounded support claim**; the
G1 mechanism remains separately open.

---

## 3. Status firewall fields

```yaml
actual_current_surface_status: bounded
conditional_surface_status: null
hypothetical_axiom_status: null
admitted_observation_status: null
proposal_allowed: false
proposal_allowed_reason: |
  V1 is landed as plain bounded support. It composes retained
  framework quantities (N_sites = 16, v, and R_base = 31/9) with the
  bounded DM η bypass identity into the structural product
  m_DM = N_sites · v. The alpha_X = alpha_LM step remains the bounded
  candidate-route choice inherited from the DM η note. No status
  upgrade is proposed while the G1
  collective-mode mechanism remains explicitly open.
audit_required_before_effective_retained: false
bare_retained_allowed: false
g1_dark_singlet_mechanism_status: open
sommerfeld_freezeout_band_status: bounded
alpha_x_route_status: bounded_candidate_route
m_dm_falsifiable_prediction: "3.94 TeV (m_DM = 16 v)"
```

---

## 4. What is closed, bounded, and open

### Closed by V1

1. structural composition of N_sites (retained Higgs) + v (retained
   EW) into the framework-composed product N_sites · v;
2. bounded support for the previously audit-discovered DM η
   freeze-out-bypass candidate as a framework-composed structural
   product;
3. enumeration that this is the unique audit-class candidate within 5%;
4. computed replay that the stated x_F/Sommerfeld rectangle brackets
   eta_obs.

### Single open ingredient carried forward

1. **G1 dark-singlet collective-mode Coleman-Weinberg mechanism** —
   open lane; the structural reason WHY the dark singlet's collective
   mode equals N_sites · v rather than some other scale is not yet
   derived.

### Bounded or inherited inputs, not new V1 closures

1. **Sommerfeld band** — bounded; not a single-point prediction.
2. **Freeze-out coefficient x_F** — bounded.
3. **alpha_X = alpha_LM** — inherited bounded candidate-route choice.
4. **A0 hierarchy compression** — inherited source-theorem assumption;
   V1 does not elevate or close it.
5. **Origin A vs Origin B** — N_sites = 16 has two factorization
   origins (APBC block vs Cl(3) chiral cube · SU(3) Casimir).
   Their unification is outside the V1 boundary.

---

## 5. Downstream bookkeeping

If V1 is kept as bounded support:
- **PUBLICATION_MATRIX line 125 (DM eta freeze-out-bypass support lane):**
  remain `bounded`, with a note that the candidate is now
  framework-composed and the G1 residual is still open.
- **DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM_NOTE_2026-04-25.md:**
  add §Note that the previously audit-discovered N_sites · v candidate
  is also framework-composed.
- **DM lane status:** the bounded band [5.25e-10, 8.11e-10] remains a
  bounded prediction until the G1 mechanism is derived.

---

## 6. Verification

```bash
python3 scripts/frontier_dm_eta_nsites_v_structural_support_lift.py
```

Audits:
1. Retained N_sites = 16 in HIGGS_MASS_FROM_AXIOM_NOTE
2. Retained v in OBSERVABLE_PRINCIPLE_FROM_AXIOM_NOTE
3. Retained R_base = 31/9 in R_BASE_GROUP_THEORY_DERIVATION_THEOREM
4. DM η freeze-out-bypass identity in DM_ETA_FREEZEOUT_BYPASS_QUANTITATIVE_THEOREM
5. Numerical verification of N_sites · v product
6. Eta bounded band reproduction from the stated x_F/Sommerfeld rectangle
7. Status firewall fields
8. G1 mechanism explicitly flagged as OPEN

Expected: PASS=N FAIL=0.

---

## 7. Honest residual

- G1 dark-singlet collective-mode mechanism: open
- Sommerfeld + freeze-out bounded band: not a single-point prediction
- alpha_X = alpha_LM: inherited bounded candidate-route choice
- A0 hierarchy compression: inherited assumption from the source theorem
- m_DM = 3.94 TeV is a falsifiable prediction (testable at LHC HL/HE
  upgrades with sufficient luminosity for WIMP-like DM searches)

The DM η freeze-out-bypass support is now structurally composed from
retained framework pieces; the G1 closure remains the named open
mechanism.
